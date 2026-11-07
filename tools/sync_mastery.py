#!/usr/bin/env python3
"""Sync coach mastery values, then commit and push only data.js on main."""

import argparse
from datetime import date
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata


REPO = Path(__file__).resolve().parents[1]
TRACKER = Path.home() / (
    "Library/Mobile Documents/com~apple~CloudDocs/Claude/學習工作區/"
    "IPAS-AI-中級/StudyVault/concepts/03-機器學習技術與應用.md"
)
STRING = r'"(?:\\.|[^"\\])*"'
MASTERY = re.compile(r'"mastery"\s*:\s*(\[(?:[^"\[\]]|' + STRING + r')*\])')
ENTRY = re.compile(r'\{(?:[^"{}]|' + STRING + r')*\}')
FIELD = re.compile(r'("(concept|status|date)"\s*:\s*)(' + STRING + r')')
HEADER = ["Concept", "Attempts", "Correct", "Last Tested", "Status",
          "Next Review", "Stage", "Error Notes"]


def parse_tracker(text):
    """Read the named table; escaped pipes belong to cells, not separators."""
    records = {}
    in_table = False
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if in_table:
                break
            continue
        cells = [cell.strip().replace(r"\|", "|")
                 for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
        if cells == HEADER:
            in_table = True
            continue
        if not in_table or all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        if not line.endswith("|") or len(cells) != len(HEADER):
            raise ValueError("Malformed concept tracker row")
        concept, tested, status = cells[0], cells[3], cells[4]
        if not concept or not status or concept in records:
            raise ValueError(f"Empty or duplicate tracker value: {concept}")
        if tested != "-":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", tested):
                raise ValueError(f"Invalid Last Tested: {concept}: {tested}")
            date.fromisoformat(tested)
        records[concept] = {"concept": concept, "status": status, "date": tested}
    if not records:
        raise ValueError("Concept tracker table is missing or empty")
    return records


def normalized(name):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", name))


def match_concept(concept, records):
    if concept in records:
        return concept
    key = normalized(concept)
    equal = [name for name in records if normalized(name) == key]
    if equal:
        return equal[0] if len(equal) == 1 else None
    contained = [name for name in records
                 if key and (key in normalized(name) or normalized(name) in key)]
    return contained[0] if len(contained) == 1 else None


def decode_data(source):
    match = re.fullmatch(r"\s*window\.MAP_DATA\s*=\s*(\{.*\})\s*;\s*", source, re.S)
    if not match:
        raise ValueError("Unsupported data.js structure")
    return json.loads(match[1])


def synchronize(source, records):
    """Replace only changed JSON string tokens inside each mastery array."""
    expected = decode_data(source)
    topics = expected["topics"]
    arrays = list(MASTERY.finditer(source))
    if len(arrays) != len(topics):
        raise ValueError("Mastery array count does not match topics")
    changes, unmatched, replacements = [], [], []
    for topic, array in zip(topics, arrays):
        if json.loads(array[1]) != topic["mastery"]:
            raise ValueError(f"Mastery array mismatch: {topic['id']}")
        entries = list(ENTRY.finditer(array[1]))
        if len(entries) != len(topic["mastery"]):
            raise ValueError(f"Unsupported mastery entry: {topic['id']}")
        for old, entry in zip(topic["mastery"], entries):
            if not {"concept", "status", "date"} <= set(old):
                raise ValueError(f"Missing mastery fields: {topic['id']}")
            name = match_concept(old["concept"], records)
            if name is None:
                unmatched.append(f"{topic['id']} | {old['concept']}")
                continue
            new = records[name]
            if all(old[key] == value for key, value in new.items()):
                continue
            label = name if name == old["concept"] else f"{old['concept']} → {name}"
            changes.append(f"{topic['id']} | {label} | {old['status']}→{new['status']}"
                           f" | {old['date']}→{new['date']}")
            def replace_field(field):
                value = new[field[2]]
                if json.loads(field[3]) == value:
                    return field[0]
                return field[1] + json.dumps(value, ensure_ascii=False)
            replacement = FIELD.sub(replace_field, entry[0])
            start = array.start(1) + entry.start()
            replacements.append((start, start + len(entry[0]), replacement))
            old.update(new)
    updated = source
    for start, end, replacement in reversed(replacements):
        updated = updated[:start] + replacement + updated[end:]
    if decode_data(updated) != expected:
        raise ValueError("Replacement validation failed")
    return updated, changes, unmatched


def git(*args):
    result = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}, timeout=120,
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: "
                           f"{result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def pending_commits():
    behind, ahead = map(int, git("rev-list", "--left-right", "--count",
                                "origin/main...HEAD").split())
    if behind:
        raise RuntimeError("main is behind/diverged from origin/main; reconcile manually")
    for commit in git("rev-list", "origin/main..HEAD").splitlines():
        subject = git("show", "-s", "--format=%s", commit)
        files = git("diff-tree", "--no-commit-id", "--name-only", "-r", commit)
        parents = git("show", "-s", "--format=%P", commit).split()
        if (not re.fullmatch(r"教練紀錄同步 \d{4}-\d{2}-\d{2}", subject)
                or files != "data.js" or len(parents) != 1):
            raise RuntimeError("Unpushed non-sync commit; refusing to publish unrelated work")
    return ahead


def atomic_write(path, content):
    """Keep original mode and line endings; never leave a partially written file."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(path.stat().st_mode)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="print changes without writing")
    args = parser.parse_args(argv)
    try:
        # Lock the existing script, so concurrent launchd/manual runs cannot race.
        with Path(__file__).open("rb") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            records = parse_tracker(TRACKER.read_text(encoding="utf-8"))
            path = REPO / "data.js"
            original = path.read_bytes()
            updated, changes, unmatched = synchronize(original.decode("utf-8"), records)
            for change in changes:
                print(change)
            for missing in unmatched:
                print(f"unmatched: {missing}")
            if args.dry_run:
                if not changes:
                    print("no change")
                return 0
            if git("branch", "--show-current") != "main":
                raise RuntimeError("Must run on main; no branch was changed")
            if git("diff", "--cached", "--name-only") or git("diff", "--name-only", "--", "data.js"):
                raise RuntimeError("Staged changes or dirty data.js; refusing to overwrite/commit user work")
            ahead = pending_commits()
            if not changes and not ahead:
                print("no change")
                return 0
            git("fetch", "origin", "main:refs/remotes/origin/main")
            ahead = pending_commits()
            if changes:
                atomic_write(path, updated.encode("utf-8"))
                try:
                    message = f"教練紀錄同步 {date.today().isoformat()}"
                    print(git("commit", "--only", "-m", message, "--", "data.js"))
                except (OSError, RuntimeError, subprocess.TimeoutExpired):
                    atomic_write(path, original)
                    git("reset", "--quiet", "HEAD", "--", "data.js")
                    raise
            if changes or ahead:
                try:
                    git("push", "origin", "main")
                except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
                    raise RuntimeError(f"{error}; commit retained, rerun this script to retry push") from error
                print("pushed origin main")
            else:
                print("no change")
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"sync_mastery: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
