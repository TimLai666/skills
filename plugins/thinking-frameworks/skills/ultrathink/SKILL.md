---
name: ultrathink
description: >-
  This skill MUST be used when the user requests ultrathink, 深度思考, or
  深入思考. It SHOULD be used when substantive uncertainty or trade-offs
  remain, including questions of meaning, tone, or reader interpretation.
  Unless explicitly requested, it MUST NOT be used for routine work with
  no substantive uncertainty or trade-offs.
metadata:
  version: "2.1.3"
---

# Ultrathink

## Overview

協助處理尚有疑點或取捨的問題：釐清要決定什麼、查證關鍵假設、比較可行方案，找出可能推翻結論的反例，再提出有依據的建議。

依問題選擇合適方法。六語分析與完整謬誤檢核依下列條件自動啟用，也可由使用者明確指定。

## Input Contract

從對話取得要解決的問題、目的、已有資料及限制。已知資訊直接沿用，只問會改變結論或授權範圍的缺項。

資料不足時，先查證能查到的部分。缺口不影響建議的，可標明假設繼續；會影響結論的，暫不下該結論，說明缺什麼及如何補足。其他可獨立處理的部分繼續。

## Workflow

1. **界定問題與完成條件**：確認這次要做的決定及判準。複合任務只在需要各自下結論時拆開，已決定的方向不重新開題。
2. **選擇能解決疑點的方法**：用下表找相關工具，查閱所需段落。已有足夠證據時可直接分析；使用者明確指定方法時，保留該方法必要的步驟與自檢。
3. **分析與反證**：核對關鍵前提，比較有實質差異的選項，檢查最可能推翻建議的證據、失敗情境與連鎖影響。若現有方法解不了疑點，再補其他方法。
4. **收斂與完成**：結論能對應證據、重要疑點已解決或明確限制了可下的結論，就形成建議。說明哪些條件改變時應換方案。若已授權實作，接續完成約定產出與驗證；只要求討論或審查時，交付相應結果。

## 工具索引

| 要處理的問題 | 可選工具與參考文件 |
| --- | --- |
| 拆結構、辨識成因、從事實導出行動 | [邏輯推導](references/01-logical-reasoning.md)：MECE、空雨傘、魚骨圖 |
| 產生替代方案或具體化使用情境 | [創意發想](references/02-creative-ideation.md)：六頂思考帽、腳本圖、心智圖 |
| 客群、競爭、定位或通路 | [市場分析](references/03-market-analysis.md)：3C、SWOT、4P 與 4C |
| 目標、指標、執行與改善 | [進度管理](references/04-progress-management.md)：惠特默模型、KPI 樹狀圖、PDCA |
| 比較選項、改變現狀或分配資源 | [權衡得失](references/05-weighing-tradeoffs.md)：決策矩陣、PMI、力場分析 |
| 生命週期、採用擴散或時間變化 | [預測未來](references/06-predicting-future.md)：S 型曲線、鴻溝理論、長尾模型 |
| 檢查提案或論證是否成立 | [辯論思考](references/07-debate-thinking.md)：論點三要素、需根解損、判定立駁 |
| 質疑前提、推演失敗與後果、辨識知識限制 | [思維模型](references/08-mental-models.md)：第一性原理、反向思考、二階思考、能力圈、奧坎剃刀 |
| 懷疑特定論證有錯 | [謬誤檢核](references/fallacy-checklist.md)：只查相關條目 |

## 選用的深入複核

兩項各依自己的啟用條件判斷。

- **六語分析**：問題有多種合理解釋、現有分析可能受單一角度限制，或重要取捨仍未釐清，需要多條獨立思考路徑互相檢驗時，自動啟用；使用者明確要求時也啟用。依 [multilingual-thinking.md](references/multilingual-thinking.md) 讓六種語言各自完整分析同一問題，再核對分歧與證據。不以文化差異為前提，不預先分配角色或觀點。翻譯資料或指定輸出語言本身不是啟用依據。
- **完整謬誤檢核**：結論依賴多層且互相牽動的論證，局部檢查不足以確認是否成立時，自動啟用；使用者明確要求完整清單、七組逐條或地毯式檢核時也啟用。依 [fallacy-checklist.md](references/fallacy-checklist.md) 執行。

## Output Contract

先給結論或建議，再說必要的依據、取捨、成立條件及未解決事項。資料不足以裁決時，改給缺口與查證方式。格式與詳略依任務，不固定輸出狀態碼、路由表或完整工作筆記。

使用者要求說明分析過程時，提供可核對的依據、方法摘要與判斷理由。原有 `show_thinking` 請求也依此處理，不輸出內部逐步思考紀錄。

## Quality Rules

- 方法要用在當前問題上，不只複述定義；不以語言數、框架數或勾選數證明品質。
- 不捏造資料、案例、分數或尚未發生的驗證結果。已知、推論、假設與未知要分清。
- 不為支持既定答案挑選工具。出現反例或新證據時，重新評估受影響的判斷。
- 不以多數意見取代查證。額外分析或獨立複核應解決實際疑點。
- PDCA 等跨階段方法尚未完成時，交代已完成部分、待做部分與續行條件；不得聲稱完整循環已完成。
