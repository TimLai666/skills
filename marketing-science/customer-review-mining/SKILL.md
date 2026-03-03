---
name: customer-review-mining
description: 探勘顧客評論並輸出主題、情緒、痛點優先級與可執行建議的分析技能。
version: 1.0.0
author: marketing-science team
---

# 技能說明（給模型看的說明書）

## 目的
此技能用於將大量顧客評論（App Store、問卷、客服訊息、社群回覆）轉為可行動的洞察，適合用在以下情境：
- 找出近期最重要的負評痛點與流失原因
- 比較不同產品、版本、市場的評論差異
- 產出產品優先級、客服改善與行銷訊息調整建議

## 輸入格式
使用者可提供 `CSV`、`JSON`、`純文字清單` 其中一種，建議優先使用 `CSV` 或 `JSON`。

必要欄位與型態：
- `review_text`：`string`，評論原文（必要）
- `created_at`：`string`（ISO 日期）或 `datetime`，評論時間（必要）
- `rating`：`number`（1-5，可缺）
- `product`：`string`，產品或方案名稱（可缺）
- `channel`：`string`，來源渠道（可缺）
- `locale`：`string`，語系或地區（可缺）

規模限制（建議）：
- 單次輸入建議 `100` 到 `20,000` 則評論
- 超過 `20,000` 則時，先做分批分析與抽樣驗證

## 分析步驟（工作流程）
1. 任務定義
- 先重述分析目標（例如：找流失原因、比較版本痛點）。
- 明確設定比較維度（時間、產品、渠道、地區）。

2. 資料檢查與清理
- 檢查必要欄位是否存在；缺失時先回報再分析。
- 移除重複、空白、純廣告或無意義文本。
- 保留兩份文本：`raw_text`（原文）與 `clean_text`（清理後）。

3. 文本標準化
- 統一大小寫、符號、日期格式。
- 多語系資料先分語言，再各自分析後整併結果。

4. 主題萃取與分類
- 先抽取候選主題，再整理為穩定 taxonomy（主題/子主題）。
- 每則評論可多標籤，並記錄 `confidence`（0-1）。

5. 情緒與嚴重度分析
- 情緒分類：`positive`、`neutral`、`negative`。
- 嚴重度分級：`1` 到 `5`（5 為最嚴重）。
- 每個主題至少保留 1-3 則代表性證據句。

6. 量化指標計算
- 計算各主題 `count`、`share`、`negative_rate`、`avg_severity`。
- 優先級分數：`impact_score = count * avg_severity * business_weight`。
- `business_weight` 若未提供，預設為 `1.0`。

7. 洞察與建議生成
- 產出 Top 痛點、成長機會、風險警示。
- 每個高優先主題提供對應行動建議與預期影響指標。

8. 品質檢查
- 確認所有結論都可回溯到原始評論證據。
- 標示資料偏誤與信心限制（樣本、語言、來源偏差）。

## 輸出格式
輸出必須使用以下段落順序：

1. `Executive Summary`
- 2-5 點核心結論
- 1-3 點優先行動

2. `Theme Analysis Table`（Markdown 表格）
| theme | subtheme | count | share | negative_rate | avg_severity | impact_score | sample_quote |
|---|---|---:|---:|---:|---:|---:|---|
| 功能 | 搜尋不準 | 120 | 18.2% | 71.0% | 4.3 | 516.0 | 「搜尋常找不到我要的」 |

3. `Action Plan`（Markdown 表格）
| priority | action | owner | eta | expected_outcome | metric |
|---:|---|---|---|---|---|
| 1 | 修正搜尋排序邏輯 | Product | 2026-03-31 | 降低負評占比 | 搜尋相關負評率 |

4. `Appendix (JSON)`（可選）
- 若使用者要求結構化輸出，附上 JSON，至少包含：
`theme, subtheme, count, negative_rate, avg_severity, impact_score, evidence`

## 進階規則或備註
- 需引用 `references/*.md` 的情況：
  - 使用者指定特定產業 taxonomy、品牌語氣、或既有 KPI 定義
  - 需要比對公司內部既有分類規則
- 禁止事項：
  - 不可臆測不存在的欄位或數值
  - 不可把單一評論當作整體結論
  - 不可輸出無證據支撐的因果推論
- 風格要求：
  - 預設使用繁體中文
  - 語氣專業、精簡、可執行
