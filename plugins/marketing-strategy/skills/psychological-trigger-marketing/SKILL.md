---
name: psychological-trigger-marketing
description: >-
  This skill MUST be used when generating high-conversion marketing angles,
  campaign hooks, landing page messaging, promotional copy directions, social
  post hooks, or CTA concepts with psychological triggers such as FOMO,
  justification, desire, priming, anchoring, and framing, especially for
  offers, launches, limited-time promotions, and Traditional Chinese marketing
  for Taiwan audiences.
metadata:
  version: "1.2.0"
---

# Psychological Trigger Marketing

## Overview

為促銷活動、商品服務、頁面訊息與 CTA 選擇心理驅動，轉成可用的文案方向。
預設使用繁體中文與台灣用語。依受眾狀態、決策阻力與真實條件設計說服方式。

純心理學教學、無轉換目標的品牌敘事不使用本流程。本 skill 不代替醫療、法律、
金融等專業宣稱所需的審核，也不以虛構數據、稀缺或見證完成促銷。

## Input Contract

確認 `product_or_offer`、`target_audience`、`goal`、`channel` 與 `conversion_stage`。
從使用者提供的內容判斷，不要求照欄位填表。

- `channel`：廣告、落地頁、社群、活動或促銷。
- `conversion_stage`：初次接觸（cold）、正在比較（warm）、接近決策（hot）。
- 補充資料：價格、優惠與期限、證據素材、品牌語氣與其他限制。

## Data Sufficiency Gate

缺少產品／方案或目標，且無法從上下文確認時，先問關鍵問題。
受眾、通路或階段不明時，判斷是否會改變訊息方向；需要假設才能推進的部分，
簡短說明假設，不把猜測寫成已知資料。

證據素材為空，不等於不能發想。根據已知產品價值提出方向，但不補上不存在的
原價、期限、名額、口碑或成效。只有需要結構化交接時使用
[缺資料格式](./references/03-output-contracts.md#缺資料格式)。

## Workflow

### 1. 判斷決策阻力

先確認這次要讓受眾注意、理解價值、接受價格或立即行動，以及目前卡在哪裡。
受眾階段是判斷線索，不能取代對實際情境的分析。

### 2. 選擇心理驅動

選擇前讀[觸發器完整定義與例句](./references/01-trigger-playbook.md)的相關段落，
確認機制、適用情境與所需條件。共有七種：嚇唬／失落、安撫／正當化、引誘／渴望、
同伴驅動、促發、錨定與框架，保留原有雙軌命名。

| 情境／阻力 | 優先考慮 | 判斷重點 |
| --- | --- | --- |
| cold：還未注意或感到相關 | 引誘、促發 | 先建立具體畫面與關聯 |
| warm：比較價值與成本 | 安撫、錨定 | 補足購買理由與可核對的比較基準 |
| hot：知道價值但延後行動 | 嚇唬、框架 | 找出延後的原因與行動的實際意義 |
| 高單價或非必需品 | 安撫 | 受眾需要哪種價值解釋 |
| 需要比較或建立價值基準 | 錨定 | 什麼參考點能幫助理解差異 |
| 他人參與會影響決策 | 同伴驅動 | 共同參與如何改變動機與阻力 |


依需要選一種或多種，說明每種處理的阻力與作用。不固定數量，也不強制湊齊
主驅動與輔助模組。上述組合是候選，應依實際條件取捨。

### 3. 寫成通路適用的訊息

讀[通路與目標套用矩陣](./references/02-application-matrix.md)的相關段落，
安排開頭、理由、比較與行動呼籲。例句用來理解機制，不能把其中的情境或條件
變成通用要求，也不能直接套用案例中的事實。

完整策略先確立主軸與選擇理由，再展開角度、標題與 CTA。
單一文案需求直接交付所需文案，必要時簡短說明理由，不附帶整包策略。

### 4. 核對條件並交付

檢查文案是否對應目標、產品與通路，實際使用的事實與承諾是否有依據。
只列會影響採用的資料缺口、假設或問題，不為空欄位另寫一份報告。
完整策略或 JSON 交接使用[輸出格式](./references/03-output-contracts.md)。

## Output Contract

- **單一 CTA／標題**：直接交付指定內容與數量，需要時附簡短理由。
- **多個方向**：各選項要有不同角度，數量依使用者要求與任務需要決定。
- **完整策略**：交代主軸、觸發器作用、訊息角度及所需的標題與 CTA，
  並說明影響決策的假設與證據缺口。欄位格式見參考文件。

## Hard Rules

- 允許高刺激、高推進力表達；實際使用的事實與承諾須有依據，不捏造或誤導。
- 不要把焦慮當成唯一手段；強刺激後要有合理承接，不可只靠情緒轟炸
- 價值訴求要連回產品與受眾的實際關係，不能只堆抽象好話
- 不得生成違法、歧視、羞辱、恐嚇或明顯誤導 claims
- 預設使用繁體中文與台灣市場說法，不用中國用語

## Quick Reference

- [觸發器方法與例句](./references/01-trigger-playbook.md)：選擇心理驅動前讀相關段落，保留七種方法與完整台灣例句。
- [通路套用矩陣](./references/02-application-matrix.md)：安排訊息節奏及通路寫法時讀。
- [輸出格式](./references/03-output-contracts.md)：完整策略、結構化交接或缺資料格式需要時讀。
