---
name: service-innovation-workshop
description: Use when turning a service innovation problem into concept options, prototype testing, and risk checks, especially for 服務創新, 創新機會, 價值共創, 服務原型, SCAMPER, 購買者效用矩陣, 創新流程, 創新困境, or 服務體驗工程. Trigger when the task asks for practical innovation directions, concept generation, opportunity framing, or validation planning rather than only concept definitions.
---

# Service Innovation Workshop

## Overview

把服務創新題目整理成可比較、可測試、可執行的創新方案，先判斷創新機會與類型，再提出概念、原型測試與風險檢查。
如果任務已經轉成完整商業模式、營收結構或九宮格設計，提示銜接 `business-model-architect`。

## Skill Boundaries

- 題目已縮小到單一元件、流程或物件，只需要快速跑七個改造動作，不需要機會分類與方案比較：改用 `scamper`。本 skill 在 `concept_options` 階段可以內嵌 SCAMPER 當發想引擎，但輸出仍要走完比較矩陣與風險檢查。
- 「現有服務壞掉要修好」用 `service-design-workshop`；「要做一個現在沒有的服務、客群或模式」用本 skill。一句話測試：問使用者「你是要把現有服務做對，還是要做一個不一樣的服務？」前者 design，後者 innovation。
- 概念選定後要展開營收結構、九宮格、定價：交 `business-model-architect`，不要在本 skill 裡直接寫九宮格。
- 建議串接順序：本 skill 選出概念 → `service-design-workshop` 落地前後台與驗證 → `business-model-architect` 補商業模式。

## Input Contract

至少要有以下其中兩項：

- `innovation_goal`
- `target_users_or_market`
- `current_service_or_process`
- `pain_points_or_market_change`

可選：

- `competitive_context`
- `technology_or_resource_constraints`
- `desired_degree_of_innovation`
- `existing_assets`
- `requested_format`

資訊不足但使用者要求快速提案時，先列出 `3-5` 個假設，再繼續產出。

## Workflow

1. 定義 `innovation_challenge`，說清楚要改善什麼、為什麼現在要做。
2. 判斷 `innovation_type_and_opportunity_source`，分類創新類型、來源與拉力。
3. 生成 `concept_options`，至少提出 `3` 個方向，避免只給單一點子。
4. 收斂成 `recommended_service_innovation_concept`，說明為何優先。
5. 製作 `prototype_test_plan`，定義雛型、測試對象、學習目標與成功訊號。
6. 補上 `risk_and_pitfall_check`，避免落入技術本位、假服務、過度承諾等常見誤區。

## Opportunity Source Classification

在 `innovation_type_and_opportunity_source` 段落，先用五類驅動力定位機會。每類用辨識問題檢核，答不出來就不要硬套：

| 驅動力 | 辨識問題 | 範例 |
|---|---|---|
| 技術驅動 | 有沒有一項技術讓過去做不到或太貴的服務變可行？成本降了幾倍？ | 生成式 AI 讓 24 小時個人化課後答疑從人力不可行變成可行 |
| 需求驅動 | 客群結構、行為或期望是否已改變，但服務還停在舊樣態？證據是什麼？ | 高齡獨居戶增加，藥局從賣藥轉成送藥到府＋用藥提醒服務 |
| 法規政策驅動 | 新法規、補助、開放或禁令是否創造了合規需求或新市場？時間窗多長？ | 碳盤查要求上路，出現中小企業碳管理代辦與顧問服務 |
| 商業模式驅動 | 同樣的服務內容，改變收費方式、綁定方式或提供方式會不會更有價值？ | 健身房從賣年約改成按次訂閱不綁約，打進低頻運動族群 |
| 資源重組驅動 | 手上有哪些閒置資產、通路、資料或人力，可以重組成新服務？ | 超商用密集門市＋物流網重組出冷凍代收與到店取件服務 |

判讀規則：

- 一個題目通常有 1-2 個主驅動力，五類全勾等於沒分析；標出主驅動與次驅動即可。
- 技術驅動必須立刻反問需求面：技術可行不等於有人要，強制搭配風險清單的「偽需求」檢查。
- 法規驅動要標時間窗：政策紅利有期限，寫清楚紅利結束後概念是否還成立。
- 這個分類與 references 的內部／外部來源分類互補：先用內外部來源找線索，再用驅動力分類定位主軸。

## Concept Comparison Matrix

從 `concept_options` 收斂到 `recommended_service_innovation_concept` 之間必須做比較矩陣，規則如下：

- 至少 3 個真正不同的概念。檢查方式：三個方案的「改變了什麼」不能互為同義改寫；若兩案只差程度不差方向，合併成一案再補新方向。
- 固定五個維度：顧客價值、可行性、差異化、成本、風險。用 1-5 分；成本與風險反向計分（分數愈高＝成本愈低、風險愈低），避免加總時方向錯亂。
- 每格評分附一句依據，不可裸數字；沒有依據的格子標「假設」。
- 預設顧客價值權重 ×2；要調整權重必須寫出理由。
- 淘汰規則：顧客價值 ≤2 直接淘汰，不看總分；風險 =1（風險極高）且提不出緩解措施，淘汰或降級為觀察名單；總分最高但可行性 ≤2，不可直接推薦，改標「需分階段驗證」。
- 平手時用「哪個最快能做出可測試的原型」決勝。
- 被淘汰的概念在 `concept_options` 留一行淘汰原因，不要無聲消失。

矩陣格式（示意，依據欄不可省略）：

| 維度（權重） | 方案 A | 方案 B | 方案 C |
|---|---|---|---|
| 顧客價值（×2） | 4：解決已驗證的等待痛點 | 2：需求證據僅來自內部想像 | 3：對次要客群有感 |
| 可行性（×1） | 3：需新增排班規則 | 4：現有人力可做 | 2：依賴未談定的外部平台 |
| 差異化（×1） | 4：區域內無同型服務 | 2：同業已有 | 3：包裝差異 |
| 成本（×1，反向） | 3 | 4 | 2 |
| 風險（×1，反向） | 3 | 4 | 1：單點依賴未解 |
| 加權總分 | 21 | 18 | 14 |
| 判定 | 推薦 | 淘汰：顧客價值 ≤2 | 淘汰：風險極高且無緩解 |

## Output Contract

固定輸出以下段落：

- `innovation_challenge`
- `innovation_type_and_opportunity_source`
- `concept_options`
- `recommended_service_innovation_concept`
- `prototype_test_plan`
- `risk_and_pitfall_check`

預設使用繁體中文 Markdown。若使用者要課堂報告或簡報版，保留相同欄位，只壓縮成較可投影片化的句型。

## Risk Check Traps

`risk_and_pitfall_check` 至少掃過以下清單，每項用檢查問題自問，中招的寫進輸出表：

- 偽需求：顧客現在用什麼替代方案？有沒有人願意付錢或改變行為的證據？答不出替代方案，需求可能不存在。
- 通路不可達：目標客群實際出現在哪個通路？我們進得去嗎？取得一個顧客的成本估多少？
- 單點依賴：概念是否依賴單一供應商、平台、關鍵個人或單一大客戶？它抽走會怎樣？
- 法規門檻：需要哪些執照、個資、金流或行業法規？申請要多久、花多少錢？
- 營運複雜度爆炸：客製選項 × 通路 × 客群的組合有幾種？第一線人員背得起來嗎？
- 單位經濟不成立：多服務一個顧客的變動成本會隨規模下降，還是人力線性增加？
- 冷啟動：價值是否要先有足夠多的供給或需求才成立？第一批使用者從哪裡來？
- 模仿無門檻：現有大玩家看到後多久能抄走？抄走之後我們還剩什麼？
- 組織抗體：這個概念會動到誰的 KPI、獎金或地盤？內部誰會擋、打算怎麼處理？
- 尖峰失守：需求尖峰或例外事件發生時，服務承諾還守得住嗎？失守一次的代價是什麼？

## Quick Reference

- 分類、來源與流程：讀 [references/service-innovation-lenses.md](./references/service-innovation-lenses.md)
- 方法與發想工具：讀 [references/service-innovation-methods.md](./references/service-innovation-methods.md)
- 輸出模板：讀 [references/service-innovation-output-templates.md](./references/service-innovation-output-templates.md)
- 工作坊促進：讀 [references/service-innovation-facilitation-guide.md](./references/service-innovation-facilitation-guide.md)

## Quality Rules

- 先判斷創新機會與類型，再提解法，不要直接丟點子。
- 至少同時看顧客需求變化、組織能力、技術或流程條件。
- 概念方案要能比較，避免三個方案其實只是同一件事換說法。
- 原型測試要寫可學到什麼，而不是只寫「先試試看」。
- 風險檢查要明講誤區與修正方式。

## Common Mistakes

- 把服務創新寫成單一促銷活動。症狀：方案只有折扣與活動檔期，沒有流程、體驗或服務內容變化 → 修法：檢查「改變了什麼」欄，若答案是價格就退回重想。
- 只講技術新不新。症狀：滿篇技術規格，沒有說為誰解決什麼需求 → 修法：套用機會來源分類的技術驅動辨識問題，補「偽需求」檢查。
- 直接挑一個方案。症狀：沒有機會來源分類，也沒有比較替代概念 → 修法：退回 Workflow 第 2、3 步，補齊至少 3 個概念與比較矩陣。
- 三個方案假多元。症狀：三案只是同一點子的不同包裝 → 修法：用「改變了什麼」互相比對，同義者合併，強制補一個不同驅動力的方案。
- 風險檢查敷衍。症狀：只挑「成本高」「要人力」等空泛項 → 修法：對照 Risk Check Traps 十項逐一問過，寫不進表的要註明為何不適用。

## Suggested Prompt

Use `$service-innovation-workshop` to turn a service innovation challenge into Traditional Chinese concept options, a recommended direction, a prototype test plan, and a risk check.
