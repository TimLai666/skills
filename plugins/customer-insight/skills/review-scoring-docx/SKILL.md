---
name: review-scoring-docx
description: >-
  This skill MUST be used when the user wants to infer product attributes from
  review files, score product quality, and deliver a Word (.docx) report, or
  explicitly requests review-scoring-docx. Triggers include 「評論評分 Word」、
  「產品屬性比較報告」 with Word output, and reviews-to-scores-to-docx.
  It SHOULD be used for review-based product comparisons whose agreed deliverable
  is Word. It MUST NOT force Word output for general review analysis or substitute
  quality scores for attribute salience.
metadata:
  version: "1.2.0"
---

# Review Scoring → Word Document

## Overview

從完整評論歸納產品屬性，以 0–10 分評估各產品在每項屬性的表現，製作 Word 屬性目錄及產品比較表。評分反映評論中的品質與使用經驗。

## Input Contract

- 評論檔案（CSV、JSON、TXT 等）、產品對應方式，以及評論正文欄位。
- 報告語言與 Word 交付需求。明確點名本 skill 時，依使用者指定的交付格式處理。
- 欄位與產品可明確辨識就直接使用。有多個合理選項時才確認。

## Data Sufficiency Gate

納入所有非空白評論，保留短評、各種語言、完整原文及可追溯的檔案與列號。空白判斷可去除首尾空白，保存的原文不截短。解析失敗須指出檔案與原因，不能默默跳過。

先列出各產品原始筆數、非空白筆數及排除原因。沒有評論的產品保留在比較範圍，標示資料不足。全部沒有正文時停止評分，請使用者補資料。

## Workflow

### 1. 歸納並固定屬性目錄

閱讀所有產品的完整評論，整理反覆出現的稱讚、抱怨與未滿足需求。少數但具體的重大問題也可列入，須標示證據有限。

屬性描述可評估的使用經驗，例如「實際防霧效果」。每項記錄：

| 欄位 | 內容 |
| --- | --- |
| `id` | 固定且不重複的編號，例如 01、02 |
| `label` | 屬性名稱 |
| `dimension` | 哪些評論內容表示表現好或差 |
| `maslow_tier` | 有證據支持的需求層級，無法判定時填 null |
| `evidence` | 原文引句及來源位置 |

Maslow 可分為生理（身體與感官）、安全（保護與可靠性）、歸屬（關係與群體）、尊重（被重視與自我價值）、自我實現（能力與目標實現）。依評論中的需求判定，沒有證據的層級標示未觀察到。

屬性數量由語料決定，不設定總數或各層配額。評分前固定目錄與順序。若後續發現必須調整定義，更新目錄後重評所有受影響的產品。

### 2. 依完整評論評分

逐產品、逐屬性整理正負評價的頻率、強度及使用情境，再給一個整數分數。每筆分數附上評價筆數、代表引文與來源，以及判分理由。遇到相反評價，保留兩方依據。

| 分數 | 評論中的表現 |
| --- | --- |
| 0–2 | 幾乎都是負評，存在嚴重失敗 |
| 3–4 | 負評占多數 |
| 5 | 有實際中性評價，或正負評價相當 |
| 6–7 | 大多正面，但有部分抱怨 |
| 8–9 | 持續獲得稱讚，負評很少 |
| 10 | 有充分且一致的正面評價，幾乎沒有反例 |
| null | 沒有提及、沒有可判讀的評價，或證據不足以判分 |

5 分須有中性或混合評價支持。沒有負評本身不足以給 10 分。短評能支持哪項就評哪項，例如「很耐用」可支持耐用性，「讚」無法單獨支持某項具體屬性。證據稀少時附上限制，無法判分就留空。

保存為 `scores: dict[product_id, list[int | None]]`，各列與固定目錄一一對應。JSON 使用 `null`，不要使用字串「null」、0 或 5 代替空值。

### 3. 計算平均與比較

使用 [scripts/score_summary.py](scripts/score_summary.py) 的 `summarize_scores(scores, attribute_ids)` 計算報告數值。它只彙總已判定的分數，不自動推論評論品質。

- 平均＝有分數的項目加總 ÷ 有分數的項目數。空值不計入分子或分母，真正的 0 分照算。全部空白時平均也留空。
- 每個平均都顯示有效項目數／總項目數。屬性平均的分母是有評分的產品數，產品平均的分母是有評分的屬性數。
- 各產品「已評屬性平均」只描述自身資料。排名使用所有待比較產品都有分數的共同屬性，等權平均，並列出共同屬性及占完整目錄的比例。
- 沒有共同屬性，或只有一個產品，就不排名。不得為了產生排名自行刪除缺資料的產品。相同分數並列，排序以未四捨五入數值為準。
- 排名僅適用於共同屬性，不能宣稱產品整體最好。屬性間若有重疊、資料量很少或評價情境不同，需說明比較限制。

假設評分為 8、6、空白，平均是 7（2/3 項）。若為 8、6、0，平均是 4.67（3/3 項）。

### 4. 製作與交付 Word

製作文件前，讀取環境中可用的 Word 文件技能與 [references/word-layout.md](references/word-layout.md)。依使用中的文件工具設定頁面與表格，檢查實際渲染結果。

交付可點擊的檔案連結或環境提供的附件。摘要列出各產品評論數、語言、共同屬性比較結果及資料缺口。有至少兩個有效分數的屬性才可比較差異幅度，並標示參與比較的產品數。

## Output Contract

- 屬性目錄：名稱、評估定義、需求層級及證據來源。
- 產品 × 屬性表：整數品質分數、缺值、有效筆數與平均。
- 比較說明：共同屬性、排名或無法排名的原因，以及可追溯的判分依據。
- 完成的 Word 文件。文件產生或渲染受阻時，明確說明完成到哪裡。

## Quality Rules

完整讀取、多語同等、目錄固定及證據可追溯，都是評分前提。報告中的分數、平均、排名與色彩必須對應同一份資料。評分是對評論的判讀，不能當成產品認證或實測結果。

## Common Mistakes

- 用提及頻率代替品質好壞。頻率只能協助判斷證據多寡。
- 對不同屬性集合的產品平均排名，或把空值當成中性分數。
- 把歷史案例的屬性和分數套到新資料。

需要看目錄與矩陣的舊版範例時，讀取 [references/worked-example.md](references/worked-example.md)。其中缺值處理與本版不同，不能用來校準本版分數。
