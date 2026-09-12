---
name: bcg-growth-share-matrix
description: >-
  This skill MUST be used when the user names the BCG growth-share matrix
  (BCG 矩陣、成長佔有率矩陣、搖錢母牛), and SHOULD be used when assessing
  investment priorities across businesses, products, or brands using market
  growth and relative market share, including 資源配置、事業組合、產品組合、
  投資、維持、收割、重定位或退出.
metadata:
  version: "1.2.0"
---

# BCG 成長佔有率矩陣

## Overview

用市場成長率與相對市佔率判讀事業或產品組合，連結現金來源、投資需求及資本配置。預設以繁體中文提供完整分析，保留 `Cash Cows / Stars / Question Marks / Dogs` 英文對照；`Pets`、`Problem Child`、`Wild Cat` 等別名也依相同概念處理。

只有使用者明確要求分類或計算時，才縮小交付範圍。BCG 是組合篩選工具，不取代完整策略判斷；沒有組合配置問題的單一事業策略深挖，或需要更細的產業吸引力與競爭力評估時，應改用適合的分析框架。

## Input Contract

從現有素材取得集團背景、策略目標、資金限制、時間範圍與事業體清單。組合分析至少包含兩個事業體或產品；每個單位需要：

- 名稱與市場成長率。
- 相對市佔率，或可用來計算的自身市佔率與最大競爭者市佔率。已有相對市佔率時，不再把原始市佔率列為分類的必要缺口。

收入規模、現金生成能力、協同效應、競爭優勢、資本支出強度與產業門檻，用於後續資本建議。資料來源、期間與市場定義須能支撐所做的比較。

## Data Sufficiency Gate

先判斷缺口影響哪個結論，不直接硬分類。用自然語言說明缺什麼、為何影響判斷，再追問最關鍵的資料；不強制輸出缺資料 JSON。

有缺值、只有高／中／低、口徑不清或需要暫時假設時，讀 [資料齊備與追問](references/02-intake-and-data-sufficiency.md)。足以分類但不足以決定資本動作時，可先完成分類，指出資本建議仍待哪些資料。暫時假設須說明依據、風險與後續補證；沒有可用資料且不允許假設時，不給確定象限。

## Workflow

1. **確認市場與計算口徑**：分類前讀 [BCG 基礎與衡量](references/01-bcg-foundation-and-metrics.md)，依其中的公式、門檻與邊界規則計算。保留來源或計法，說明使用的門檻；接近分界時標記敏感度與替代判讀。
2. **判讀各事業體**：提供象限及依據。完整分析再讀 [四象限策略手冊](references/03-quadrant-strategy-playbook.md)，判斷發展潛力、可能轉移路徑、成立條件、策略姿態及資本優先序。
3. **形成組合建議**：完整分析讀 [現代市場限制與組合邏輯](references/04-modern-caveats-and-portfolio-logic.md)，連結成熟業務的現金與成長業務的投資需求，檢查接棒、資源分散及依賴風險。以現金、協同、競爭優勢與資本需求校正建議；若與象限衝突，保留量化象限並解釋例外。只做分類時，遇到這類例外也讀此文件，但不擴寫整份資本方案。
4. **整理交付**：讀 [分析模板](assets/templates/bcg-portfolio-analysis-template.md) 取得完整欄位與座標格式。依 Output Contract 選用內容，追蹤時程配合決策期限及投資驗證週期。

## Output Contract

- **完整分析為預設**：包含組合概況、各事業體分類與發展判斷、各象限策略、資本配置、調整優先序、座標資料、假設與限制，以及待補資料、實驗或財務驗證、追蹤指標。完整欄位由模板定義。
- **只要求分類或計算**：提供座標、象限、判定依據、門檻與相關缺口或邊界說明，不額外產出資本配置與追蹤方案。
- 兩種範圍都保留 `matrix_plot_data`。資料不足的單位明列缺口，不用零或臆造座標補齊。

## Quality Rules

- 以資料支持分類與資本動作，說明哪些判斷可能因市場定義、門檻或資料品質而改變。
- 策略不能只由象限名稱決定。各象限的投資、維持、收割、退出與例外條件依策略手冊判斷，不只輸出標籤。
- 只說明本案相關的 BCG 限制及仍需驗證的決策，不固定重述一段框架免責說明。
