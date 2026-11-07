# 教練紀錄同步實作與驗收 — 2026-11-07

狀態：實作與隔離測試完成；正式 commit／push 被工作階段的 `.git` 唯讀權限阻擋，未上線。原始 HEAD 仍為 `a5a5426bc3bb6da5ff82b8be8353856c7bb04ab3`，正式 `data.js` 未變動，避免留下無法提交的半套同步。

## 目標、範圍與執行狀態

- [x] 讀取現有 JS 與 Markdown，確認 44 個 topics、45 筆 mastery、112 筆追蹤列。
- [x] 新增 Python 標準函式庫腳本，正則局部替換，保留其他位元組與 mastery 的 note。
- [x] 新增 README「教練紀錄自動同步」說明，不建立或修改排程。
- [x] 實際 dry-run、候選資料語法與位元組驗證、獨立整合測試／審查。
- [ ] 正式寫入資料、commit、push 與實際 repo 的第二次 no change 驗收：受 `.git` 唯讀限制阻擋。

未修改 index.html、fig/、追蹤表、~/.claude 或其他分支。此報告為使用者指定的本機證據檔，不提交到 public repo。

## 修改檔案

- `tools/sync_mastery.py`：新增 225 行。
- `README.md`：新增 15 行，既有內容未改。
- `data.js`：實際 0 行；已驗證的候選資料涉及 25 筆 mastery、27 行欄位替換，僅 status／date，無概念改名。
- `tools/sync_report_20261107.md`：本報告，行數見最終回報。

## 對應結果

還原 Markdown 的 `\|` 後，`條件機率輸出與風險分流 P(Y|X)` 已直接符合正式名稱，保持原名。共 41／45 筆可直接對應；去空白、NFKC 全半形正規化與唯一包含比對均無法為以下 4 筆找到可信對應，保留原 concept／status／date：

- 3.2-01 — PCA降維原理
- 3.2-01 — PCA協方差矩陣與特徵值分解
- 3.2-01 — PCA核心直覺-找最大變異方向
- 6.1-01 — L23401 資料隱私安全與合規

追蹤表中的 PCA 比較、PCA 不看標籤與差分隱私 ε 等列各自測不同概念，未擅自當作這四個概念的掌握證據。

## 驗收 1：通過

`python3 tools/sync_mastery.py --dry-run` exit 0，正式 data.js 位元組不變，無 commit／push。

完整輸出：

```text
3.2-01 | PCA解釋變異量比例 | ⚪→⚪ | →-
3.2-01 | PCA應用限制與PCA vs t-SNE | ⚪→⚪ | →-
3.3-01 | 非凸函數 | ⚪→⚪ | →-
3.3-03 | 損失函數與輸出層配對 | 🟦→🔴 | 2026-09-26→2026-09-26
4.3-01 | CNN 卷積神經網路 | ⚪→⚪ | →-
4.3-01 | VGG16 與 VGG19 | ⚪→⚪ | →-
4.3-01 | Pooling（池化層） | ⚪→⚪ | →-
4.3-02 | 激活函數 | 🟢→🟢 | 2026-09-26→2026-11-02
4.3-04 | RNN 原理 | ⚪→⚪ | →-
4.3-04 | LSTM 用途 | ⚪→⚪ | →-
4.3-05 | 多頭注意力與位置編碼 | ⚪→⚪ | →-
4.3-05 | BERT vs GPT 讀懂用編碼器生成用解碼器 | ⚪→⚪ | →-
4.3-06 | 反向傳播 | ⚪→⚪ | →-
4.3-07 | 微調三選一 特徵萃取全面微調LoRA | ⚪→⚪ | →-
4.3-08 | 微調三選一 特徵萃取全面微調LoRA | ⚪→⚪ | →-
4.3-09 | RAG 與混合搜尋 | ⚪→⚪ | →-
5.1-01 | 特徵縮放與距離型模型 | 🟢→🔴 | 2026-10-13→2026-11-02
5.1-05 | 資料洩漏與訓練集 fit | ⚪→⚪ | →2026-10-01
5.1-05 | 115-1 Q44 LDA 管線洩漏 | ⚪→⚪ | →-
5.2-01 | SHAP | ⚪→⚪ | →-
5.3-01 | 交叉驗證選型 | ⚪→🟢 | →2026-11-02
5.3-03 | 混淆矩陣四格 | ⚪→⚪ | →-
5.3-06 | 偏差—變異診斷 射箭比喻 | ⚪→⚪ | →-
5.3-06 | 過擬合判讀 | ⚪→⚪ | →-
5.4-03 | 網格搜尋與隨機搜尋 | ⚪→⚪ | →-
unmatched: 3.2-01 | PCA降維原理
unmatched: 3.2-01 | PCA協方差矩陣與特徵值分解
unmatched: 3.2-01 | PCA核心直覺-找最大變異方向
unmatched: 6.1-01 | L23401 資料隱私安全與合規
```

## 驗收 2：阻擋，未完成

先測 Git 寫入權限：

```text
$ git add -- tools/sync_mastery.py README.md
fatal: Unable to create '/Users/anthea/Documents/Codex/ipas-l23-starmap/.git/index.lock': Operation not permitted
exit 128
```

實際執行同步腳本（stdout 為同一份 25 筆差異與 4 筆 unmatched）：

```text
$ python3 tools/sync_mastery.py
sync_mastery: git fetch origin main:refs/remotes/origin/main failed: error: cannot open '.git/FETCH_HEAD': Operation not permitted
exit 1
```

腳本在 Git preflight 失敗，尚未寫入資料，data.js 與原檔逐位元組相同。沒有以替代 git-dir、其他 clone 或其他執行通道繞過權限。需要在可寫入本 repo `.git` 的工作階段繼續；使用者已授權 commit／push，缺的是環境寫入能力，不是再次授權。

```text
$ git log -1 --oneline
a5a5426 分隔線：加寬觸控熱區、拖曳時亮起、加提示
exit 0
$ git status -sb
## main...origin/main
 M README.md
?? tools/
exit 0
$ node --check data.js
exit 0
```

初始 `git ls-remote origin refs/heads/main` 確認遠端為 `a5a5426bc3bb6da5ff82b8be8353856c7bb04ab3`。`main...origin/main` 目前同步僅代表舊提交相同，不代表此功能已提交或上線。

## 驗收 3：正式 repo 未完成

未在相同權限阻擋下重複執行；正式資料仍舊，第二次不應誤稱 no change。隔離測試在暫存 repo 與本機 bare remote 驗證：第一次更新提交並推送、第二次印 no change／exit 0／HEAD 不變；push 拒絕時保留同步 commit，再跑只推送該 commit、不新增 commit。

## 驗收 4：候選差異通過；正式變更尚未套用

```text
$ git diff a5a5426 -- data.js index.html
exit 0
```

正式 data.js 與 index.html 皆無 diff。額外對候選資料做以下獨立檢查：移除 mastery 陣列後原始字串完全一致；JSON 結構還原 concept／status／date 後完全相等；mastery note 保留；再次同步輸出逐位元組一致。`node --check /private/tmp/sync-mastery-tests/actual-after-data.js` exit 0。

```text
45 mastery entries; 25 changed entries; 27 changed fields; 4 unmatched
Outside mastery bytes identical; extra fields unchanged; second render identical
Tracker SHA256: 634e1b967294cac09c2613ba3dcb9278e88d9650a980c1de7298950e3a047a05
```

候選資料 diff（未寫入正式 data.js）：

```diff
--- data.js (a5a5426)
+++ data.js (verified candidate)
@@ -368,12 +368,12 @@
     {
      "concept": "PCA解釋變異量比例",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     },
     {
      "concept": "PCA應用限制與PCA vs t-SNE",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -563,7 +563,7 @@
     {
      "concept": "非凸函數",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -727,7 +727,7 @@
    "mastery": [
     {
      "concept": "損失函數與輸出層配對",
-     "status": "🟦",
+     "status": "🔴",
      "date": "2026-09-26"
     }
    ],
@@ -1159,17 +1159,17 @@
     {
      "concept": "CNN 卷積神經網路",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     },
     {
      "concept": "VGG16 與 VGG19",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     },
     {
      "concept": "Pooling（池化層）",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -1379,7 +1379,7 @@
     {
      "concept": "激活函數",
      "status": "🟢",
-     "date": "2026-09-26"
+     "date": "2026-11-02"
     }
    ],
    "quiz": [
@@ -1488,12 +1488,12 @@
     {
      "concept": "RNN 原理",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     },
     {
      "concept": "LSTM 用途",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -1545,12 +1545,12 @@
     {
      "concept": "多頭注意力與位置編碼",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     },
     {
      "concept": "BERT vs GPT 讀懂用編碼器生成用解碼器",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -1632,7 +1632,7 @@
     {
      "concept": "反向傳播",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -1731,7 +1731,7 @@
     {
      "concept": "微調三選一 特徵萃取全面微調LoRA",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -1855,7 +1855,7 @@
     {
      "concept": "微調三選一 特徵萃取全面微調LoRA",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -1898,7 +1898,7 @@
     {
      "concept": "RAG 與混合搜尋",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -1944,8 +1944,8 @@
    "mastery": [
     {
      "concept": "特徵縮放與距離型模型",
-     "status": "🟢",
-     "date": "2026-10-13",
+     "status": "🔴",
+     "date": "2026-11-02",
      "note": "部分：縮短間隔再驗"
     }
    ],
@@ -2224,12 +2224,12 @@
     {
      "concept": "資料洩漏與訓練集 fit",
      "status": "⚪",
-     "date": ""
+     "date": "2026-10-01"
     },
     {
      "concept": "115-1 Q44 LDA 管線洩漏",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -2428,7 +2428,7 @@
     {
      "concept": "SHAP",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     },
     {
      "concept": "內在可解釋模型選擇",
@@ -2494,8 +2494,8 @@
    "mastery": [
     {
      "concept": "交叉驗證選型",
-     "status": "⚪",
-     "date": ""
+     "status": "🟢",
+     "date": "2026-11-02"
     },
     {
      "concept": "模型診斷 變異殘差與交叉驗證",
@@ -2711,7 +2711,7 @@
     {
      "concept": "混淆矩陣四格",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -2939,12 +2939,12 @@
     {
      "concept": "偏差—變異診斷 射箭比喻",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     },
     {
      "concept": "過擬合判讀",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
@@ -3363,7 +3363,7 @@
     {
      "concept": "網格搜尋與隨機搜尋",
      "status": "⚪",
-     "date": ""
+     "date": "-"
     }
    ],
    "quiz": [
```

## 測試、獨立審查與限制

RED：腳本未建立時實際 `python3 tools/sync_mastery.py --dry-run` exit 2（檔案不存在）；獨立測試 RED 證據位於 `/private/tmp/sync-mastery-tests/red.txt`。

獨立 reviewer：`gpt-5.6-sol` 子代理 `/root/sync_tests`。agy 的已安裝包裝器會寫 `~/.claude/logs/agy-usage.log`，與本次明示禁寫範圍衝突，故未執行；改用不同模型做唯讀技術審查與隔離測試。未呼叫可能寫入 ~/.claude 的 Tech Lead CLI；不宣稱 Tech Lead 已裁決或驗收。

隔離測試使用 Python unittest 與暫存本機 git repo／bare remote，沒有碰實際 origin。測試原始碼與完整輸出：`/private/tmp/sync-mastery-tests/test_sync_mastery.py`、`green.txt`、`review.md`。Python AST parse、git diff --check、node --check 均通過；來源追蹤表 SHA256 與起始讀取完全一致。

殘餘限制：正式 GitHub 推送／Pages 部署尚未驗證；lock contention 與 timeout 路徑未實測；fcntl 鎖定適用 POSIX（本任務為 macOS launchd）。本任務依要求不做瀏覽器驗收。


獨立測試最終結果：9／9 通過，review verdict 為 PASS。

```text
test_commit_hook_refusal_restores_data_index_and_head (test_sync_mastery.Tests.test_commit_hook_refusal_restores_data_index_and_head) ... ok
test_dirty_data_refuses_without_overwriting_or_committing (test_sync_mastery.Tests.test_dirty_data_refuses_without_overwriting_or_committing) ... ok
test_dry_run_any_cwd_and_match_reporting (test_sync_mastery.Tests.test_dry_run_any_cwd_and_match_reporting) ... ok
test_exact_byte_preservation_empty_date_and_idempotence (test_sync_mastery.Tests.test_exact_byte_preservation_empty_date_and_idempotence) ... ok
test_failed_push_then_retry_without_new_commit (test_sync_mastery.Tests.test_failed_push_then_retry_without_new_commit) ... ok
test_malformed_and_duplicate_tracker_each_refuse_without_mutation (test_sync_mastery.Tests.test_malformed_and_duplicate_tracker_each_refuse_without_mutation) ... ok
test_missing_tracker_no_mutation (test_sync_mastery.Tests.test_missing_tracker_no_mutation) ... ok
test_unrelated_staged_refused_and_not_committed (test_sync_mastery.Tests.test_unrelated_staged_refused_and_not_committed) ... ok
test_wrong_branch_refuses_without_mutation (test_sync_mastery.Tests.test_wrong_branch_refuses_without_mutation) ... ok

----------------------------------------------------------------------
Ran 9 tests in 2.468s

OK
```

隔離 repo 第二次執行證據（不是正式 repo）：

```text
HEAD before: f6806a26c32a23718a5f0530ecf5ab44e0d43f44
HEAD after:  f6806a26c32a23718a5f0530ecf5ab44e0d43f44
returncode: 0
stdout:
unmatched: three | 網路
unmatched: four | 找不到資料
no change
stderr:
```

## 問題與後續

- `schema-assumption`：首次實際 dry-run 發現 3 筆 mastery 有額外 note；已改成只要求必要欄位並保留 note，加入位元組回歸測試。一次修正，無需升級永久規則。
- `sandbox-git-write`：Git 寫入由環境拒絕；不繞過、不假稱發布完成。`~/.codex/state/error-tally.json` 不在可寫範圍，僅在此記錄類別。
- 恢復可寫 `.git` 後，先將工具與 README 作為實作提交並推送，再跑同步腳本，使最後一筆為「教練紀錄同步 YYYY-MM-DD」。腳本會拒絕未推送的非同步提交，因此不能留下未推送的實作提交就直接跑它。

```sh
git add -- tools/sync_mastery.py README.md
git commit -m "新增教練紀錄自動同步工具"
git push origin main
python3 tools/sync_mastery.py --dry-run
python3 tools/sync_mastery.py
node --check data.js
python3 tools/sync_mastery.py
git log -1 --oneline
git status -sb
git diff a5a5426 -- data.js index.html
```

以上後續指令尚未執行；避免使用 `git add .`，本報告維持本機證據用途。
