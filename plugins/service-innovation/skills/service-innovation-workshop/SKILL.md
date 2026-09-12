---
name: service-innovation-workshop
description: >-
  This skill MUST be used to develop service innovation opportunities into
  concepts, comparisons, or prototype validation plans (服務創新、創新機會、
  服務原型、創新流程、服務體驗工程). It SHOULD also be used when the user wants
  new service directions, value co-creation, or ways to test an existing
  service concept without naming a method. Match the workflow to the task;
  a standalone method request does not require a full workshop.
metadata:
  version: "1.2.0"
---

# Service Innovation Workshop

## Overview

把服務創新題目整理成可比較、可測試、可執行的創新方案，先判斷創新機會與類型，再提出概念、原型測試與風險檢查。
如果任務已經轉成完整商業模式、營收結構或九宮格設計，提示銜接 `business-model-architect`。

## Input Contract

辨識創新目標、服務對象、現有服務或流程，以及痛點或市場變化。依判斷需要補充競爭情境、資源與技術限制、期望的創新程度、既有資產及交付格式。

資訊足以界定問題就開始。關鍵缺項會影響方向時先確認，其餘可用明示假設推進。

## Workflow

完整工作坊依序完成下列階段。局部發想、概念比較或原型驗證只處理相關階段，核對必要的問題依據。使用者已選定方向時，承接既有決定安排驗證。

| 階段 | 工作與閱讀時機 |
| --- | --- |
| 界定機會 | 說清楚為誰改善什麼、為何現在要做。判斷類型與機會來源前，讀 [服務創新視角](references/service-innovation-lenses.md) |
| 生成與比較概念 | 發想或選方法前，讀 [方法與工具](references/service-innovation-methods.md)。提出有實質差異的選項，比較顧客價值、執行難度與風險，說明優先理由，不以數量湊方案 |
| 設計原型驗證 | 規劃測試前，讀方法文件的「原型與測試最小要求」，把概念中的關鍵假設轉成可觀察的測試 |
| 檢查與交付 | 交付前讀 [輸出模板](references/service-innovation-output-templates.md)，逐項檢查誤區並提出對應修正，依任務範圍整理成果 |

## Output Contract

預設使用繁體中文 Markdown。完整工作坊採模板六段，局部需求交付相關分析、依據與下一步。課堂報告或簡報依指定格式呈現，保留範圍內的比較理由與驗證內容。

## Quality Rules

- 機會判斷同時檢視顧客需求變化、組織能力、技術或流程條件。
- 概念要說明服務內容、流程或互動如何改變，不能只換包裝或只講技術新穎。
- 推薦方向須有實質比較依據，不能把同一概念換名當成替代方案。
- 原型測試須能回答關鍵假設，風險修正須對應實際執行條件。
