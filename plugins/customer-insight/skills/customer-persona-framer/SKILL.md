---
name: customer-persona-framer
description: >-
  This skill MUST be used to create, review, or update a persona,
  人物誌、顧客輪廓、使用者輪廓 or a target-customer profile from research,
  audience clues, a product or service, or usage context. It SHOULD also be
  used when customer understanding needs a coherent profile of needs,
  behavior, decision factors, and constraints. Journey-preparation work is
  included only when explicitly requested. It MUST NOT add journey maps,
  stage planning, or handoff artifacts to persona-only requests.
metadata:
  version: "1.2.0"
---

# Customer Persona Framer

## Overview

建立能用於理解顧客、產品規劃與溝通的人物誌，整理顧客的需求、痛點、行為、決策因素與限制。預設交付一份繁體中文 persona，旅程前置是明確要求時才啟用的選用用途。

## Input Contract

可從下列任一資料開始：

- 顧客研究、訪談、觀察或既有 persona。
- 目標客群、初步輪廓或使用情境。
- 產品或服務及可辨識的受眾線索。

同時確認人物誌的用途，例如理解使用者需求、產品設計或溝通規劃。用途已明確時沿用，只有會改變分析方向的缺項才追問。做 persona 不以產品名稱、旅程階段或接觸點資料為必要前提。

預設一個核心 persona，使用者要求多個客群時依需求處理。不同客群的行為或限制互不相容時，先說明差異，避免拼成一個不存在的典型人物。

保留 `mode: auto | persona-only | journey-framing`：

- `auto`：預設 `persona-only`。只有明確要求顧客旅程前置分析或指定 `journey-framing` 時才使用該模式。
- `persona-only`：交付人物誌，或依要求審查、修改既有人物誌。
- `journey-framing`：以人物誌為基礎，加上使用者要求的旅程前置內容。

提到情緒、接觸點、階段或 5W1H，本身不構成切換模式的理由。「只要 persona」「先不要旅程」優先。只要求完成旅程地圖時交由 customer-journey-mapper，該技能需要補足顧客輪廓時，本 skill 只處理所缺輪廓。

## Data Sufficiency Gate

資料足以辨識本案客群及描述與用途相關的需求、行為和限制時，開始整理。資訊缺口只限制受影響的結論，能確定的部分先完成。

區分三類內容：

- **研究或已知資料**：保留來源名稱、訪談編號或可核對的位置，避免把單一受訪者反應直接當成全體特徵。
- **分析推論**：交代依據與推導關係，沒有證據支持普遍性時保留適用條件。
- **待驗證假設**：使用者要求草稿或允許假設時，依線索提出必要假設，數量依缺口決定，並說明如何確認。

「直接幫我整理」只表示整理現有資料，不自動授權補造內容。人口背景、收入、家庭、偏好與引言須有資料支持。允許草稿也不把虛構個人細節寫成研究事實。缺少資料的欄位可省略或標待確認，不以合理想像填滿。

連分析對象或用途都無法合理界定時，先確認關鍵資訊。旅程前置另依 [選用旅程前置](references/journey-framing.md) 判斷所需資料。

## Workflow

### 1. 整理依據與差異

讀取既有資料，確認本次用途與範圍。依可觀察的行為、需要、決策方式及限制找出共同特徵，保留會影響判斷的差異和反例。使用者提供的研究結果或明確修正優先於舊版輪廓。

### 2. 建立人物誌

使用下方 Output Contract 整理：

- **需求**：顧客要達成什麼、為何重要。
- **痛點**：目前哪個阻礙讓需求難以滿足。
- **期望**：顧客希望改善後有什麼結果或體驗。
- **行為與情境**：顧客何時、在哪裡、如何處理問題，採取哪些做法或替代方案。
- **決策因素**：顧客如何比較、接受或拒絕選項，哪些條件會改變選擇。
- **限制**：時間、知識、預算、權限、裝置習慣等如何具體影響行動。

同一資訊只維護一份完整敘述，其他部分需要時引用。角色代稱用來識別客群，年齡與生活背景只在有依據且影響用途時保留。

### 3. 依本次範圍交付

一般人物誌依下方結構交付。只要求審查或局部修改時，回覆問題、依據或受影響的內容，沿用其餘有效資料。

只有 `journey-framing` 才讀取 [選用旅程前置](references/journey-framing.md) 並補上對應成果。要求簡報化摘要時保留實質內容，改寫成適合投影片的條列，不因此增加旅程分析。實際投影片檔案依指定格式處理。

## Output Contract

### Persona 卡

以 `persona_block` 作為人物誌卡本體，保留此名稱供後續引用。卡內整合以下資訊，不另在結尾重複一份相同摘要：

| 欄位 | 內容 |
| --- | --- |
| 顧客輪廓 | 角色代稱、代表的客群及相關特徵 |
| 角色背景 | 與本案有關且有依據的背景 |
| 核心需求 | 主要目標及其重要性 |
| 主要痛點 | 目前做法的具體阻礙 |
| 期望 | 希望達成的結果或體驗 |
| 使用情境 | 何時、何地、在什麼條件下處理需求 |
| 行為與替代方案 | 已知做法、習慣及替代選擇 |
| 決策線索 | 比較標準、採用條件及拒絕原因 |
| 核心限制 | 對行動有實際影響的限制 |

欄位中的資料與推論附對應依據，假設在相關內容旁標明。未知資訊依 Data Sufficiency Gate 處理。

### 必要說明與待確認事項

補充影響解讀的客群差異、資料限制或關鍵假設，列出真正需要確認的資訊與方法。已有完整說明的欄位不重述。只交付 persona 時，結束於人物誌與必要說明。

## Quality Rules

- 人物誌能讓讀者辨識顧客、理解其需求及選擇原因。
- 需求、痛點、期望各有具體內容，行為與限制相容。
- 特徵有來源或明確推論依據，假設沒有冒充研究事實。
- 沒有用刻板印象、虛構引言或裝飾性背景補滿卡片。
- 相同資訊只寫一次，原有可重用欄位與 persona_block 名稱保留。
- 交付符合人物誌、局部審查或明確指定的旅程前置用途。
