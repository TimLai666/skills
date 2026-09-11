---
name: zettelkasten
description: >-
  This skill MUST be used when building, maintaining, or auditing a
  Zettelkasten (slip-box) note system, or when applying atomic-note discipline
  to an existing markdown knowledge base — atomicity checks, card-splitting
  decisions, linking rules, note-type workflow. Trigger on
  卡片盒筆記法、卡片盒、Zettelkasten、原子筆記、永久筆記、文獻筆記、結構筆記、拆卡、筆記連結、smart notes、atomic
  notes、permanent notes、slip-box, and SHOULD be used when another skill (e.g.
  llm-wiki) needs per-change note-discipline checks.
metadata:
  version: "1.2.0"
---

# Zettelkasten 卡片盒筆記法

## Overview

用 Luhmann 的卡片盒方法建立與維護「一卡一想法」的筆記系統：原子卡片、用自己的話改寫、
強制連結、結構由連結網絡湧現。適用於任何 markdown 筆記庫，Obsidian 或純目錄皆可。

這個 skill 有兩種用法：

1. **獨立使用** — 從零建立卡片盒，或把靈感、文獻素材處理成永久卡片。
2. **供其他 skill 引用** — 作為筆記寫入紀律的檢核標準。`llm-wiki` 的頁面寫入
   即引用本 skill 的變更檢核清單（原子性、拆卡、連結）。

紀律是本體，資料夾結構只是預設建議。套用在既有筆記庫（例如 llm-wiki 維護的 wiki）時，
沿用該庫的結構與慣例，只套紀律。

## Input Contract

必填其中至少一項：

- `vault_path` — 筆記庫路徑（新建或既有）
- 要處理的素材 — 靈感、文獻內容、貼上的文字，或要檢核的既有筆記

可選：

- `mode` — `init`（初始化）/ `capture`（收集）/ `process`（處理成永久卡片，預設）/ `audit`（盤點體檢）
- 既有筆記庫的慣例（frontmatter、連結語法）— 未提供時沿用現場觀察到的慣例

## Workflow

### 筆記類型

| 類型 | 用途 | 生命週期 |
|------|------|----------|
| 靈感筆記 fleeting | 快速捕捉，未加工 | 1-2 天內處理掉，不留 |
| 文獻筆記 literature | 來源說了什麼（自己的話＋出處） | 永久保留，供永久卡引用 |
| 永久筆記 permanent | 系統的本體。概念卡（一個主張）或實體卡（一個人／事件／組織／作品／具名方法） | 持續演化 |
| 結構筆記 structure | 卡片地圖、入口、閱讀動線 | 隨連結成長更新 |

### 流程

1. **確認慣例** — 新建筆記庫、選擇筆記類型或套用到既有知識庫前，讀
   [原則、筆記類型與慣例](./references/01-principles-and-note-types.md)，包含命名、
   frontmatter、完整卡片範例與 llm-wiki 對應。既有目錄與語法優先沿用。
2. **捕捉** — 靈感進 inbox；讀來源時用自己的話寫文獻筆記並標出處。
   process 模式須將素材處理成永久卡，不能只累積文獻筆記。
3. **處理** — 搜尋既有卡片，再判斷素材包含哪些獨立想法。已有相同想法就更新；
   新想法寫成新卡；與既有卡衝突時保留雙方，另寫新卡互連並依筆記庫慣例標明分歧。
   概念卡用陳述句標題，實體卡用實體名稱，事實、時間線或步驟寫成可掃讀的結構。
4. **拆卡** — 在新增或修改卡片前，完整讀取
   [拆卡判準、操作步驟與檢核範例](./references/02-split-and-checklist.md)。
   概念卡聚焦一個能獨立理解與引用的想法，實體卡聚焦一個實體。
   若包含多個可獨立成立的主張，應拆成不同卡片並建立連結。
   篇幅長短不能單獨決定是否拆分；同一想法的解釋、例子與必要脈絡可以留在同張卡片，
   但不能以保留脈絡為由，把不同想法全部留在一起。拆出的卡須補足必要背景，單獨讀也成立。
   實體卡長出獨立論點時，依參考文件拆為概念卡。
5. **連結** — 內文提到既有卡的詞就地連結，必要時用 `[[目標卡|顯示文字]]`
   保持語句通順。至少 1-2 條出連結；內文沒自然提到但關係重要的卡（對比、反駁）
   補在文末並說明關係。判斷被連卡是否需要回連、相關結構筆記是否要更新。
   結構筆記可用連結清單安排閱讀動線，隨卡片關係成長，不用預設大綱限制卡片去向。
6. **寫入前檢核** — 每次新增或修改都逐項執行參考文件的
   [變更檢核清單](./references/02-split-and-checklist.md#變更檢核清單勾選版)，
   通過才寫入。因回連觸發的被連卡編輯只檢查連結，不重跑全清單或遞迴觸發下一層回連。
7. **盤點**（audit 模式）— 先讀上述拆卡判準與清單，檢查孤兒卡、待拆卡、重複卡、
   不對稱連結（A→B 無回連且無合理原因）、未處理 inbox，提出路徑與建議動作。

## Output Contract

- `cards_written` — 新增與更新的卡片清單（含類型）。
- `split_decisions` — 實際拆分與依據，以及影響卡片邊界的不拆理由。
- `links_updated` — 連結、回連及結構筆記的實際變更；會影響理解或後續處理的例外須說明，
  不必逐條列出所有未新增的回連。
- `audit_report` — audit 模式列出孤兒卡、待拆卡、重複卡、不對稱連結、inbox 積壓，
  附路徑與建議動作。

## Quality Rules

- 永久卡用自己的話寫；文獻筆記標原始出處，永久卡引用文獻筆記。
  套用 llm-wiki 時，依[既有知識庫對應](./references/01-principles-and-note-types.md#套用在既有知識庫)
  處理來源與頁面類型的例外。
- 原子性的單位是想法，不是句子。完整拆卡判準與逐項檢核統一維護在參考文件，
  不以本主檔的摘要取代。

## Quick Reference

- [原則、筆記類型與慣例](./references/01-principles-and-note-types.md)：新建或套用筆記庫時讀，
  包含六原則、命名與 frontmatter、四張完整卡片範例、資料夾結構及 llm-wiki 對應。
- [拆卡判準與變更檢核清單](./references/02-split-and-checklist.md)：新增、修改或盤點卡片前完整讀，
  包含拆與不拆的判準、實體卡拆分、操作步驟、逐項清單及拆卡／更新案例。
