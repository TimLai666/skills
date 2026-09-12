---
name: scamper
description: >-
  This skill MUST be used when applying SCAMPER (奔馳法) to generate or review
  innovation ideas for products, services, processes, business models, or concepts.
  It SHOULD also be used for 創意發想、創新思考、產品改良、服務優化、創意激盪、系統化創新
  when the user wants to explore multiple creative angles for an existing target,
  even without naming the framework.
metadata:
  version: "1.2.0"
---

# SCAMPER 奔馳法創意思考工具

## Overview

運用替代、合併、調適、修改、挪作他用、消除、重組／逆向七個維度，探索現有產品、服務、流程或概念的改變方式，再比較值得推進的方案。

## Input Contract

從自然語言與既有材料辨識下列資訊，不要求使用者填寫欄位：

- `target_object`：要創新的對象及其現有形式、功能與使用情境。
- `innovation_goal`：希望改善的結果，例如降低成本、提升體驗或開拓市場。
- `context`、`constraints`：背景、痛點、預算、技術、時間及不可改變的條件。
- `depth`：`full`（預設，完整分析）或 `quick`（快速概覽）。
- `focus_dimensions`：使用者指定的維度，例如「只看替代、合併、消除」。
- `output_language`：預設台灣繁體中文。

只有目標而無具體對象時，先釐清要改變什麼。其他缺漏依對結果的影響決定是否詢問。能合理推進的假設須標明，不用固定數量的假設補滿輸入。

## Workflow

### 1. 確認對象與探索範圍

整理核心特點、功能、使用情境、痛點與限制，作為發想依據。

| 模式 | 探索與交付範圍 |
| --- | --- |
| full | 完整檢視七維度，展開具體構想與比較理由 |
| quick | 同樣檢視七維度，以精簡表格呈現構想與優先理由 |
| 指定維度 | 只展開指定範圍，依 full 或 quick 決定說明深度 |

### 2. 依方法發散構想

開始前必讀 [七維度定義與提問矩陣](references/01-dimensions-and-questions.md)。對核心特點提出各維度的問題，探索「具體改變什麼、如何產生效果」。M 包含修改、放大、縮小，R 包含重組與逆向，不能只想到其中一種。

先展開不同機制與切入點，容許大膽構想。暫時需要突破限制的想法須說明成立條件，留到篩選階段評估。各維度的構想數量依有效差異決定，不用換句話湊數。

做教學演練、自然類比或受限材料發想時，讀 [實戰演練與進階技法](references/02-practice-and-advanced.md)。需要企業案例解釋方法或作為類比時，讀 [案例分析](references/03-case-studies.md)。

### 3. 比較並收斂

合併重複或互補的構想，依目標貢獻、可行性、資源需求與關鍵假設比較。從中提出值得優先推進的方向與理由，數量依問題決定。新奇程度不能代替優先判斷。

若某維度探索後沒有值得保留的構想，交代嘗試的方向及不採用原因，不硬選一個最佳方案。若尚無方案符合限制，說明缺口及下一步驗證，不宣稱可執行。

## Output Contract

依任務交付現況分析、各維度構想與優先方向。沿用 `subject_analysis`、`scamper_dimensions`、`priority_innovations` 名稱供需要固定欄位的情境使用，一般回覆使用自然中文標題。

- 每個構想說清楚改變的對象、做法與預期效果。
- 優先方向提供比較理由、重要成立條件及可開始的下一步。
- 資源、風險與驗證方式放在對應方案下，需要集中說明時再使用 `implementation_note`。

組織分析輸出時讀 [輸出模板](references/04-output-templates.md)，依模式使用。模板提供結構，不規定構想或優先方向的數量。

## Quality Rules

- 同一構想可涉及多個維度，但只列一次並註明關係，不重複包裝。
- 企業案例的 SCAMPER 分類是分析視角。事實、研究結果、預期效果與假設分清楚，具體事實附來源。
