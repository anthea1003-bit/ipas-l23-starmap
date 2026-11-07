# iPAS AI 應用規劃師（中級）科目三 機器學習星圖

互動星圖：44 個考點、115 題（114-2、115-1 公告試題＋官方樣題科目三），每題附提示與解析，題目附圖一併收錄。

- 星星大小：正式卷出題數；顏色：章節（L231～L234）
- 左上小點：教練概念追蹤表的掌握狀態（2026-10-22 快照）
- 每題「原卷 p.N」可用陪讀閱讀器直接翻到原卷頁面

資料來源：官方學習指引、公告試題與樣題（答案為官方公告答案）。白話說明、提示與解析為整理撰寫。

## 教練紀錄自動同步

`tools/sync_mastery.py` 以 Python 3 標準函式庫讀取 iCloud 的 `Claude/學習工作區/IPAS-AI-中級/StudyVault/concepts/03-機器學習技術與應用.md`，將 `data.js` 的 `topics[*].mastery` 狀態與日期更新為追蹤表的 `Status`、`Last Tested`（`-` 保留原樣），其餘內容與格式保持不變。先還原概念名的 `\|`，依序比對正式名稱、去空白與全半形正規化、唯一的名稱包含關係；能唯一對應才改用正式名稱，無法對應或有歧義者保留原值並列出 `unmatched`。

```sh
python3 tools/sync_mastery.py --dry-run  # 只列出差異，不寫檔、不 commit、不 push
python3 tools/sync_mastery.py            # 有差異時更新、commit、push origin main
```

可從任何工作目錄以腳本絕對路徑執行。提交訊息為「教練紀錄同步 YYYY-MM-DD」（執行當地日期），只提交 `data.js`；完全無變動且無待推送提交時印出 `no change`。push 失敗會保留同步 commit、輸出原因到 stderr 並非 0 結束，下次即使資料無差異也會重試 push，不重複 commit。追蹤表讀取／解析失敗不修改資料；commit 失敗會還原本次資料寫入。

執行環境需有 Python 3.10+、Git 與既有 origin 推送權限，且位於 `main`。腳本拒絕已暫存的變更、尚未提交的 `data.js`、落後／分歧的分支，以及非同步用途的未推送提交；不自動切分支、合併或 force push。排程可重入但同時只允許一個同步程序。

上方及頁面內的 2026-10-22 說明是原始快照註記；教練紀錄現在可由此腳本更新。此變更不安裝排程，launchd 掛接由 Tech Lead 另行處理；追蹤表保持唯讀。推送到既有 `origin main` 後由 GitHub Pages 自動部署。
