---
name: sor-marketing-strategy
description: >-
  This skill MUST be used when the user names S-O-R, Stimulus-Organism-Response,
  or 刺激-有機體-反應, and when analyzing how marketing stimuli affect consumer
  psychology and behavior. SHOULD be used for requests such as 廣告有點擊卻沒轉換、
  推播有開卻沒回購、品牌活動有聲量卻沒行動, or when turning 消費者行為分析、行銷心理
  into a strategy or testable hypothesis. Users need not name the model.
  MUST NOT trigger solely for analytics implementation, general KPI reporting,
  or an A/B test that does not need a consumer-psychology hypothesis.
metadata:
  version: "1.2.0"
---

# S-O-R 行銷策略

## Overview

完整分析外部刺激（S）、消費者內在心理歷程（O）、行為反應（R），
找出行銷問題可能卡在哪裡，再提出可執行、可驗證的策略。
模型描述的是待檢查的作用路徑，不能只因三段串得通，就宣稱已證明因果。

## Input Contract

從現有資料確認品牌／方案、目標受眾、商業目標、通路與希望改變的行為。
補充資訊包括既有刺激、受眾洞察、證據素材、可取得指標、預算、期間與限制。

純文案成稿、事件追蹤實作或一般報表不需要本模型時，不啟用整套分析。

## Data Sufficiency Gate

先查現有材料，只有缺口會改變分析或妨礙交付時才問。
不知道品牌提供什麼、對誰溝通、希望對方做什麼時，先釐清再提出具體策略。
通路不明但可以先判讀心理機制時，完成可分析的部分並標明適用前提。

不捏造受眾洞察、數據或結果。資料不足的環節說明缺口與驗證方式，
不能用假設補成已確認事實，也不能略過該環節。

## Workflow

### 1. 確認目標與模型邊界

先完整讀[模型基礎與研究邊界](./references/01-sor-foundation-and-research.md)。
確定主要目標行為，再倒推可能需要的心理變化與刺激調整。
若同時有其他目標，交代主次與取捨，避免只看短期轉換而漏掉本次要求的回購或推薦。

### 2. 完成 S、O、R 分析

三段都必須分析，不能只列刺激、心理名詞或結果指標。
分析深度依問題調整，但每條建議都要說得出三段如何連接，以及依據是什麼。

| 環節 | 必須釐清 | 執行前讀取 |
| --- | --- | --- |
| S：刺激 | 現有刺激、缺口或衝突、可調整之處 | [刺激設計](./references/02-stimulus-design-playbook.md)的分類與相關通路段落 |
| O：心理 | 目前狀態、預期變化、作用理由、證據或假設 | [心理面向](./references/03-organism-psychology-map.md)的判讀方式與相關面向 |
| R：反應 | 目標行為、可觀察的結果與驗證方式 | [行為與衡量](./references/04-response-metrics-and-experiments.md)的行為層級及指標原則 |

S 涵蓋感官、資訊、社會、技術與情境刺激；O 從認知、情緒、品牌態度、
信任與風險、價值評估、侵擾與摩擦六個面向判讀。
依情境辨認有影響的因素，不要求各類湊足固定數量。

同一刺激可能帶來相反作用。個人化題目須同時分析「被理解、感到相關」
與「被打擾、被監視」的可能反應，根據受眾情境與資料判斷，不預設一定有益或有害。

### 3. 整合措施與驗證

用一張連貫的分析表呈現：現有問題、刺激調整、預期心理變化、目標行為、
依據或假設、衡量方式。同一措施不在 S-O-R 表、三段措施及行動表重複敘述。

衡量需能區分過程中的前導訊號與最終結果。選擇能檢查這條路徑的指標，
數量依問題與資料而定；有重要副作用時，安排相應觀察方式。
前導訊號改善不等於已證明心理機制或最終成果。

若已有信任、理解或相關性問題，說明它如何影響路徑，再決定措施。
不以一個指標直接認定某心理因素就是根因。

### 4. 按需求展開交付

- 需要跨通路計畫時，標明各接觸點的訊息作用、時機與銜接。
- 需要實驗時，讀[實驗設計段落](./references/04-response-metrics-and-experiments.md#experiment-mapping)，
  明列假設、比較方式、指標與決策規則。
- 需要文案時，從分析整理主訴求、證據與 CTA，再配合可用且適用的寫作能力完成。
- 需要正式樣本量、統計檢定或追蹤實作時，依可用工具與專項能力完成相應工作，
  不固定依賴特定 skill 名稱，也不把策略骨架當成已完成實作。
- 需要執行排程時，依實際期間安排工作，未指定時不自動附完整 30 天計畫。

場景參考見[應用情境與分析重點](./references/05-application-scenarios.md)，需要把模型套用到具體問題時讀。
案例中的方法與指標是示範，不轉成每個任務都要滿足的條件。

### 5. 核對結果與後續調整

確認 S、O、R 分析完整，主張與資料相符，措施能回應問題。
有成效資料時，根據結果回看低效刺激與心理假設，提出調整及下一步驗證。
尚無資料時，只列待驗證方向，不宣稱已改善。

## Output Contract

基本交付包含主要判斷、完整 S-O-R 分析、建議措施及驗證方式。
完整表格見[策略模板](./assets/templates/sor-strategy-template.md)。
只有需要通路計畫、實驗、文案或排程時才展開對應段落。
若使用者指定既有 JSON 結構，依相同分析填入，避免用重複文字湊欄位。

## Quality Rules

- S、O、R 都有具體內容，連結有理由，未知事項明示。
- 不把相關性、前導指標或模型推論直接當成因果證據。
- 文案與策略實際使用的事實、比較、背書及承諾須有依據。
- 信任、被打擾感與長期反應是效果分析的一部分，依實際影響判斷，不另做道德評分。
- 指標要交代衡量的行為與統計範圍；無法取得的資料列出替代驗證方式或限制。

## Quick Reference

- [模型基礎](./references/01-sor-foundation-and-research.md)：每次分析前完整讀，含理論、研究脈絡與因果界線。
- [刺激設計](./references/02-stimulus-design-playbook.md)：盤點 S 時讀分類及相關通路方法。
- [心理面向](./references/03-organism-psychology-map.md)：判讀 O 時讀相關面向、反例與狀態描述方式。
- [衡量與實驗](./references/04-response-metrics-and-experiments.md)：判讀 R 時讀衡量原則，設計實驗時再讀實驗段落。
- [應用情境與分析重點](./references/05-application-scenarios.md)：需對照實際問題時讀，含七種情境的分析方向與資料判讀重點。
- [策略模板](./assets/templates/sor-strategy-template.md)：表格交付時使用，完整 S-O-R 核心與延伸交付分開。
