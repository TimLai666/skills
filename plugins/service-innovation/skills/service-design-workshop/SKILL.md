---
name: service-design-workshop
description: >-
  This skill MUST be used to turn a service design problem into a practical
  brief, service architecture, touchpoint analysis, or prototype validation plan,
  including 服務設計、服務流程、接觸點、前台後台、服務實證、顧客體驗、利害關係人、服務概念、服務架構.
  It SHOULD also be used to improve part of an existing service design or prepare
  workshop outputs, even when the user does not name a method or workshop.
metadata:
  version: "1.2.0"
---

# Service Design Workshop

## Overview

從顧客體驗與服務運作兩個視角，把問題整理成服務概念、架構、接觸點與驗證計畫。適用於完整設計、工作坊準備及既有方案的局部改善。

若需求只有 persona、顧客旅程圖或生態系地圖／服務藍圖，分別使用可用的 `customer-persona-framer`、`customer-journey-mapper` 或 `ecosystem-map-and-blueprint`。完整服務設計需要這些工具時，可搭配使用，不中止其餘工作。

## Input Contract

從需求與既有材料辨識服務問題、對象、場域及痛點，再整理營運目標、限制、接觸點、利害關係人與指定格式。

以是否足以界定本次問題和範圍判斷資料是否足夠，不按欄位數量判斷。缺少會改變設計方向的資訊時先確認。能合理推進時先做草稿，標示必要假設與待確認事項，避免把推測當成觀察結果。

## Workflow

### 1. 確認範圍與所需方法

沿用已有且適用的資料與成果。完整設計涵蓋下列各階段，局部修改則處理相關階段並檢查受影響的交接與驗證。

- 問題模糊、需釐清服務設計定位或規劃整體流程時，讀 [原則與流程](references/service-design-principles-and-process.md)。
- 需要選擇研究、歸納、發想或評估方法時，讀 [方法與工具](references/service-design-methods.md)，依資料缺口及階段選用。
- 組織交付成果時，讀 [輸出模板](references/service-design-output-templates.md)，完整設計使用全套，局部修改使用相關部分。

### 2. 依階段完成設計

| 階段 | 必要成果 |
| --- | --- |
| 問題與場域 | 現況、痛點、服務對象、限制與設計目標，區分資料依據與假設 |
| 利害關係人與需求 | 檢視顧客、第一線、後台與合作方的需求、角色及衝突 |
| 服務概念與架構 | 為誰提供什麼價值、服務承諾、主要階段、交接方式與所需資源 |
| 接觸點與營運 | 按服務階段對應顧客行動、前台、後台、支援流程及服務實證，說明負責角色與交接 |
| 原型與驗證 | 原型形式、要驗證的假設、測試對象、方法、觀察指標、成功訊號與下一步 |

先理解問題再發想，依顧客價值、可行性與營運支撐比較方案。已有概念時從需要修正的問題開始，不重做無關階段。

### 3. 檢查完整性與可驗證性

逐階段檢查相關角色、活動、交接與服務實證。資料不足處列為待確認，確實不適用的項目說明理由。完整性不能只靠每欄填入一個項目判斷。

驗證計畫須說明觀察到什麼結果才支持方案，以及不支持時要調整什麼。成功訊號依目標與現有資料訂定，缺少比較資料時先安排觀察，不任意填入成效數字。

## Output Contract

預設以台灣繁體中文 Markdown 交付。完整設計包含服務摘要與各階段成果，局部修改交付修改內容、判斷理由及受影響的相關部分。使用者指定簡報或課堂作業格式時，依用途調整呈現，保留本次範圍內的必要資訊。

模板保留 `service_design_brief` 與各階段欄位名稱供固定格式使用，一般回覆可用自然中文標題。提出研究或驗證計畫時，明確區分預計執行與已取得的結果。

## Quality Rules

- 接觸點寫出實際互動及其服務階段，不能只列通路名稱。
- 後台是支撐前台交付的幕後活動，支援流程包含其他內部支援與外部系統，依活動分類。
- 服務實證是可觀察的實體或數位物件，例如空間、介面、通知、文件、制服、包裝。
- 選用的方法須能處理本案資料缺口，不用方法名稱取代分析。
