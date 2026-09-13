---
name: arxiv
description: >-
  This skill MUST be used for arXiv searches, arXiv URLs or paper IDs, and explicit
  requests to retrieve arXiv papers. It SHOULD be used as one source in general
  literature searches, preprint discovery, and related-work research when relevant
  to the topic. It MUST NOT treat arXiv as the only source for a general literature
  search. Triggers include arXiv、論文搜尋、預印本、文獻搜尋、相關研究。
metadata:
  version: "1.2.0"
---

# arXiv Research

## Overview

搜尋與擷取 arXiv 論文。一般文獻搜尋可將 arXiv 作為其中一個來源，依領域及問題搭配其他資料庫。需要引文關係或相關論文時，可使用 Semantic Scholar 補充。

## Input Contract

接受研究主題、作者、分類、arXiv 網址或編號。保留使用者指定的版本後綴。依需求確認搜尋範圍、時間及交付深度，單篇查詢不必補問完整研究計畫。

## Workflow

### 1. 選擇操作

使用 Python 3 標準函式庫腳本 [search_arxiv.py](scripts/search_arxiv.py)。完整功能、參數、預設值與範例都在腳本 help：

```bash
python3 <skill-directory>/scripts/search_arxiv.py --help
```

將 `<skill-directory>` 換成此 skill 的實際路徑。無參數執行也會顯示總覽。先讀 help，再依需求搜尋主題、作者或分類，或擷取指定編號。

### 2. 檢查結果與閱讀

- 搜尋結果先檢查題目、完整摘要、日期與版本，再判斷是否符合問題。
- 留意撤稿或撤回通知。摘要中的關鍵字只是線索，必要時檢查摘要頁與論文原文，不將缺少關鍵字視為確認未撤稿。
- 要解釋方法、結果或限制時閱讀全文。使用環境可用的 HTML 或 PDF 閱讀工具，記錄實際讀到的版本與範圍。只取得摘要時明確標示。
- 引用連結保留實際讀取的版本後綴，避免新版內容取代原先依據。
- 欄位缺少、HTTP 錯誤或解析失敗須明確回報，不能當作搜尋沒有結果。

### 3. 依需求擴充研究

只查指定論文時，完成該篇即可。需要相關研究、被引用情況或作者資料時，讀 [related-work.md](references/related-work.md)。不固定每次都查引用量與作者背景。

連續呼叫 arXiv API 時至少間隔三秒。多個代理共用同一連線來源時統一安排請求，避免各自並行呼叫。遇到限流先停止並依回應等候，不無限重試。批次或分頁需求依 [arXiv 官方 API 文件](https://info.arxiv.org/help/api/user-manual.html) 處理，並說明實際搜尋範圍。

## Output Contract

依任務提供論文清單或單篇說明，包含題目、作者、日期、帶版本的連結、與問題的關聯，以及閱讀範圍。需要引用格式時，從已確認的 metadata 產生，缺欄位不補猜。

一般文獻搜尋列出使用過的來源與限制。只搜尋 arXiv 時，說明結果僅涵蓋此來源。

## Quality Rules

- 以原文支持對論文的判讀，區分作者結論與自己的推論。
- 引用量可補充背景，不單獨決定研究品質或相關性。
- 原始論文編號、新舊編號格式與版本後綴都須保留。
- 指令操作以腳本 help 為準，API 細節查官方文件。
