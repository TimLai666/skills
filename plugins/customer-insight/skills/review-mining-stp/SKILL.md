---
name: review-mining-stp
description: >-
  This skill MUST be used when customer reviews, support tickets, app store
  feedback, or similar text must be scored and analyzed statistically for
  segmentation, targeting, and positioning (評論分析、客群區隔、目標市場、產品定位、STP).
  It MUST NOT be used for qualitative summaries or review tagging alone.
metadata:
  version: "1.5.0"
---

# Review Mining STP

## Overview

把評論轉成市場區隔（Segmentation）、目標市場選擇（Targeting）與產品定位（Positioning），再提出有評論及統計依據的策略。

先逐篇閱讀評論，整理評分項目、理論標記及原文，再交給腳本做統計與報告。評分流程可使用適合的工具，不限定 API 或服務。腳本只接受已評分的資料，不負責讀取原始評論來判斷分數。

## Input Contract

先確認分析目標、評論範圍、比較品牌及要執行的階段。只有原始評論時，從項目整理與評分開始。已有評分資料時，先依[輸入欄位與執行模式](references/01-router-and-gates.md)檢查是否可用。

完整執行 `full` 需要：

- `review_scoring_table.csv`：逐篇評論原文及各項評分。
- `review_foundation.json`：項目定義、主題、理論及統計用途。
- `attribute_catalog.csv`：固定的評分項目與原文範例。
- `analysis_context.json`：分析目標、比較項目及範圍限制。
- `brands.json`、`ideal_point.json`：比較品牌及理想點。

每篇評論保留 `review_id`、`unit_id`、`brand`、`product`、`review_text`。沒有可靠的個人識別資料時，`unit_id` 可使用 `review_id`，解讀時應說明分析單位是評論。

## Data Sufficiency Gate

- 評分所需的原文或分析背景不足時，列出缺少的資料，以 `MissingDataOutput` 說明可完成的部分。
- 腳本所需檔案不足時，回傳 `MissingPrerequisiteOutput`，不要自動補造評分資料。
- 項目數與理論涵蓋率依評論內容決定。資料支持時以至少 30 項為目標，不足則填寫 `shortfall_reason`。沒有出現的預設理論記入 `theory_gap`。
- 品質評分缺漏時保留空值，並在統計結果中交代實際採用及排除的資料。無法支持某項分析時，說明缺口。定位資料不足時，腳本會以非零狀態結束，保留先前階段的檔案，但不產生完整報告。

## Workflow

### 1. 讀完評論，固定評分項目

先讀完整批評論，收集關注、讚美、抱怨與使用情境，再合併成各自可辨認的項目。不同問題即使常一起出現，也不要因此合成一項。名稱使用一般人看得懂的短詞，主題由這批評論歸納。

每項保留定義、提及評論數、一篇原文範例及 `review_id`。依[項目整理與理論標記](references/09-attribute-discovery-and-theories.md)檢查適用理論。預設使用產品定位、Maslow 需求、購買動機與口碑動機四類。評論有明確依據時，可依規定登錄其他理論。

評分前，把項目、穩定的 `attribute_key`、理論標記及配對評分欄位寫入目錄並固定。正式評分期間不增刪或改名。後續發現遺漏時記錄限制，維持本次評分項目一致。

### 2. 逐篇評分，分開記錄提及程度與品質評價

每項都有 `<attribute_key>_salience` 與 `<attribute_key>_quality` 兩欄。

| 評分 | 衡量內容 | 規則 |
| --- | --- | --- |
| `salience`，0–7 整數 | 這項內容在評論中有多明顯 | 0 沒提到，1–3 略提或間接提到，4 有清楚提到但著墨有限，5–6 明確討論，7 是主要關注點。正負評價不決定提及分數。 |
| `quality`，0–10 整數或空白 | 評論者認為這項表現有多好 | 0 完全失效，1–3 明顯不滿，4 偏負面，5 有評價但正負混合或中立，6–7 大致滿意，8–9 明確滿意，10 毫無保留地稱讚。沒有評價就留空。 |

`salience = 0` 時，`quality` 必須留空。即使 `salience > 0`，只有描述存在、沒有表達好壞，也應把 `quality` 留空。

假設評論只說「有附收納袋」，可以記錄提及程度，但沒有依據給收納袋的品質分數。若說「收納袋太薄，放進背包就破了」，才有負面評價可評分。

逐篇評分完成後，由腳本依品牌及項目計算品質平均，只納入有實際評價的分數。提及數與有效評價數分開呈現，空白不當成 0 分或 5 分。

### 3. 執行需要的 STP 分析

| 階段 | 分析重點 | 執行前讀取 |
| --- | --- | --- |
| `segmentation` | 依評論關注與需求形成客群，保留人／貨／場、System 1／2、Maslow 及客群輪廓 | [市場區隔](references/02-segmentation.md) |
| `targeting` | 比較現有及潛在客群，提出優先、次優先及暫不投入的客群 | [目標市場選擇](references/03-targeting.md) |
| `positioning` | 比較品牌、理想點及品牌間距離，產生定位圖與改善方向 | [產品定位](references/04-positioning.md) |

區隔採用 `factor_analysis -> K-means`，保留群體占比 `>5%` 的檢查與重跑紀錄。目標市場的變數來自 `dimension_catalog.stat_roles`，`analysis_context.comparison_axes` 可指定比較項目。連續反應變數用 ANOVA／迴歸，二元反應變數用卡方／邏輯斯迴歸，顯著 ANOVA 要有成對比較。

定位預設使用因素分析。有明確相似度輸入時才用 MDS，並保留理想點距離與品牌間距離。定位圖要從座標表實際繪製，MDS 不產生虛構的屬性向量。

選 `full` 可串接全部階段，`custom` 只執行指定模組。單階段可使用既有統計中間檔重跑，所需檔案見[執行模式](references/01-router-and-gates.md#run-modes)。

### 4. 整理結論與可核對的依據

先說明這批評論呈現哪些客群、哪些客群值得投入，以及品牌應改善或強調什麼。各階段交代理論、方法、使用哪一種評分、主題涵蓋情況及限制。

每個主要發現附原文、`review_id`、支持的評分項目、統計結果與重現步驟。報告中的引文必須與 `review_scoring_table.csv.review_text` 一致。理論沒有出現時標示 `not_evidenced`，不把所有預設理論寫成已獲支持。

## Output Contract

交付分析範圍、項目整理摘要、已執行階段的結論、整合策略、限制與 `appendix.json`。報告本文要看得到項目摘要、代表項目、主題與理論涵蓋情況。

完整執行另產生 `segmentation_variables.csv`、`targeting_dataset.csv`、`positioning_scorecard.csv`。有定位分析時，交付座標表與實際產生的定位圖。

[輸出欄位與品質規則](references/05-output-contract-and-quality-rules.md)集中定義報告、發現、統計結果及重現步驟的固定欄位。保留這些欄位，文字說明以非統計背景的讀者能理解為準。

## Quality Rules

- 評分以原文為依據，保留固定項目與原始引文，腳本不得改寫引文或重新判定分數。
- `quality` 是欄位、指標及彙總軸的一致名稱。保留 `product` 欄位。
- 理論標記必須有評論依據。每項至少對應一類適用理論，沒有適合的對應時先重新檢查定義或登錄有根據的擴充理論。
- 所有平均值與模型要交代有效資料及缺漏處理，不能把沒有評價解讀成負評或中立。
- 檢查分析結果與原文是否支持結論。欄位完整或驗證程式通過，不能代替這項判斷。

## Quick Reference

在 skill 目錄下執行：

```bash
python -m pip install -r requirements.txt
python scripts/run_review_mining_stp.py --run-mode full --input-dir <artifacts> --output-dir <output>
python scripts/validate_review_mining_stp.py --run-mode full --output-dir <output>
```

- 需要輸入與重跑範例時，讀[端到端範例](references/06-end-to-end-examples.md)。
- 修改腳本時，使用 [fixtures/minimal](fixtures/minimal/) 及[驗證情境](references/08-verification-scenarios.md)核對行為。
- 查核規則與程式輸出的對應時，讀[證據對照表](references/07-traceability-evidence-matrix.md)。
