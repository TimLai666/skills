---
name: zettelkasten
description: Use when building, maintaining, or auditing a Zettelkasten (slip-box) note system, or when applying atomic-note discipline to an existing markdown knowledge base — atomicity checks, card-splitting decisions, linking rules, note-type workflow. Trigger on 卡片盒筆記法、卡片盒、Zettelkasten、原子筆記、永久筆記、文獻筆記、結構筆記、拆卡、筆記連結、smart notes、atomic notes、permanent notes、slip-box, or when another skill (e.g. llm-wiki) needs per-change note-discipline checks.
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

### 核心原則

1. **原子性** — 一卡一想法，實體卡則一卡一實體。標題需要「與、以及」才能描述內容，就是兩張卡。
2. **自主性** — 每張卡單獨讀要成立，不依賴來源或前後文。
3. **自己的話** — 改寫不摘抄。抄原文不等於理解。
4. **連結優先** — 連結長在內文：提到其他卡的概念或實體，就地把那個詞變成 `[[連結]]`。新卡至少連到 1-2 張既有卡，連不上的卡等於遺失。
5. **湧現結構** — 不預設階層。用結構筆記當入口，結構跟著連結長。
6. **矛盾是發展點** — 新想法與既有卡衝突時不覆蓋，寫成新卡並互連標明分歧。

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
| 永久筆記 permanent | 系統的本體。概念卡（一個主張）或實體卡（一個人／事件／組織／作品） | 持續演化 |
| 結構筆記 structure | 卡片地圖、入口、閱讀動線 | 隨連結成長更新 |

### 流程

1. **捕捉** — 靈感進 inbox；讀來源時寫文獻筆記（自己的話、標出處）。
2. **處理** — 對每個想法問：這是一個想法還是多個？已有卡片嗎？
   已有 → 更新既有卡；沒有 → 寫成新的永久卡。概念卡標題用陳述句，
   實體卡標題用實體名稱。
3. **連結** — 內文提到既有卡的詞就地連結，必要時用 `[[目標卡|顯示文字]]`
   保持語句通順；內文沒自然提到但關係重要的卡（對比、反駁）補在文末並說明
   關係；判斷被連卡是否回連、相關結構筆記是否要收錄這張卡。
4. **變更檢核** — 每次 create/update 都跑下方檢核清單，再寫入。
5. **盤點**（audit 模式）— 掃孤兒卡、待拆卡、重複卡、未處理 inbox，出報告。

### 變更檢核清單（每次寫入必跑）

任何卡片的新增或修改，寫入前依序檢查：

1. **原子性** — 這次要寫的是單一想法（實體卡：單一實體）嗎？寫入後這張卡是否涵蓋 2+ 個獨立想法？
2. **拆卡判斷** — 命中任一判準就拆（完整判準見 references/02）：
   標題需要「與」才完整、某段落可被其他脈絡獨立引用、卡片回答了多個問題。
   拆法：每個想法一張新卡、互相連結，原卡改為摘要＋連結或併入結構筆記。
3. **重複檢查** — 這個想法是否已存在？已存在就更新既有卡，不開新卡。
4. **連結** — 內文提到其他卡片主題的詞都就地連結了嗎（至少 1-2 條出連結）？內文沒提到的重要關係補在文末了嗎？被連卡需要回連嗎？結構筆記要更新嗎？
5. **自主性** — 卡片單獨讀成立嗎？
6. **自己的話** — 是改寫還是貼原文？

## Output Contract

- `cards_written` — 新增與更新的卡片清單（含類型）
- `split_decisions` — 拆了哪些卡、依據哪條判準；判斷不拆的邊界案例也要說明理由
- `links_updated` — 新增的連結與回連、更新的結構筆記
- `audit_report` —（audit 模式）孤兒卡、待拆卡、重複卡、inbox 積壓，附路徑與建議動作

## Quality Rules

- 概念卡標題用陳述句（「間隔重複比集中複習有效」，不是「間隔重複」）；
  實體卡標題用實體名稱（「颶風基科（1989）」），內文寫成可掃讀的事實與時間線，
  提到相關概念（如快速增強）時在內文就地連結。
- 連結長在內文提到的詞上，不為了連結另立清單；文末補充段只放內文沒自然提到的
  關係（對比、反駁）並標明關係。結構筆記除外，它天生就是連結清單。
- 拆卡不拆到失去自主性，拆出來的每張卡都要單獨成立。
- 套在既有筆記庫上時沿用其 frontmatter 與連結語法（Obsidian 語法參考 `obsidian-markdown` skill）。
- 文獻筆記必須標出處；永久卡引用文獻筆記，不直接引用原始來源。

## Common Mistakes

- 收藏癖：狂寫文獻筆記，從不煉成永久卡。系統的價值在永久卡與連結網絡。
- 用資料夾階層分類代替連結。卡片盒的結構在連結，不在目錄樹。
- 孤兒卡：寫完不連結，等於丟進黑洞。
- 拆卡過頭：一句話一張卡，碎到無法單獨理解。原子性的單位是「想法」不是「句子」。
- 把結構筆記寫成強制大綱，反過來限制新卡的去向。
- 檢核清單只在盤點時跑。它是每次寫入的紀律，不是定期作業。

## Quick Reference

- 六原則詳解、筆記類型（含概念卡與實體卡之分）、命名與 frontmatter 慣例、四張卡片完整範例、預設資料夾結構、套用在既有知識庫（含 llm-wiki 對應與 ingest 拆頁範例）：讀 [references/01-principles-and-note-types.md](./references/01-principles-and-note-types.md)
- 拆卡判準與不拆判準（各附案例）、實體卡的拆卡、拆卡操作步驟、變更檢核清單勾選版、拆卡與更新情境的檢核走查：讀 [references/02-split-and-checklist.md](./references/02-split-and-checklist.md)

## Suggested Prompt

Use `$zettelkasten` to build or maintain an atomic, linked slip-box note system, or to run atomicity and card-splitting checks on an existing markdown knowledge base.
