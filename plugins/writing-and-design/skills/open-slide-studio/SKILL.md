---
name: open-slide-studio
description: >-
  This skill MUST be used when the user names open-slide, and SHOULD be used
  for web-based slide decks, live presenting, presenter mode, or presentations
  shared or deployed as a URL. MUST NOT be used for editable .pptx deliverables;
  use design-studio's PPTX route instead. 觸發詞：open-slide、網頁簡報、簡報網站、
  簡報部署、線上簡報、presenter mode。
metadata:
  version: "1.0.4"
---

# Open Slide Studio

## Overview

本 skill 負責網頁簡報的交付格式分流、工作區建立，以及視覺與撰寫流程的交接。`design-studio` 決定視覺，[open-slide](https://github.com/1weiho/open-slide) 提供 React 簡報、放映與靜態部署環境，工作區內建 skills 負責頁面撰寫規範。

## Input Contract

從使用者的描述與既有專案取得簡報主題、素材及交付格式。已有 open-slide 工作區（含 `open-slide.config.ts` 與 `slides/`）就沿用；視覺方向依 Workflow 處理。

| 使用者要的 | 處理方式 |
| --- | --- |
| 可編輯的 .pptx（進 PowerPoint 修改、套公司模板） | 交給 `design-studio` 的 PPTX 路線 |
| 網頁簡報、現場放映、presenter mode、部署成網址或從網頁簡報匯出 PDF | 使用本 skill |
| PPTX 且可接受每頁是圖片 | 使用本 skill，交付前告知圖片版不可編輯 |

只有交付格式仍不明時，才詢問要可編輯的 .pptx 或網頁簡報；已確定就不重問。執行需要本機 Node.js，環境不具備時明說限制，不以手寫 HTML 冒充 open-slide。

## Workflow

1. **準備工作區** — 新工作區才執行：

   ```bash
   npx @open-slide/cli init <dir>
   cd <dir>
   pnpm install
   ```

   套件管理器依 init 指示與既有 lockfile 選擇。先讀工作區 `AGENTS.md`，再依下列任務讀取對應的內建 skill；Claude Code 使用 `.claude/skills/`，Codex 等 agent 使用 `.agents/skills/`。

2. **接續視覺設計** — 先讀既有 `DESIGN.md`、簡報與其主題，依 `design-studio` 的公約處理：

   - **修改既有簡報**：沿用已定案的視覺與主題。局部修改不重新選風格或建立主題。
   - **建立新簡報**：有適用主題就沿用；需要新視覺方向時，使用 design-studio 的風格選定流程。將已定案的方向與主題一併交給撰寫流程，避免重新詢問。
   - **建立或調整主題**：先讀工作區內建 `create-theme`，把 DESIGN.md 的色彩、字體、層級與風格寫成它要求的完整主題產物，包括 `themes/<id>.md` 與配套的 `themes/<id>.demo.tsx` 預覽檔，實際格式依工作區版本。主題文件供 `create-slide` 讀取，預覽檔供主題介面呈現。

3. **撰寫與修改** — 依任務交給工作區內建 skills：

   | 任務 | 何時讀取 |
   | --- | --- |
   | 建立新簡報 | 用 `create-slide` 組織內容，沿用已確認的需求與主題 |
   | 撰寫或修改頁面 | 動手前讀 `slide-authoring`，並依它的指示讀取相關參考 |
   | 套用頁面上的 comment | 用 `apply-comments` 處理 |
   | 使用者指稱「這一頁」「這個元素」 | 先用 `current-slide` 確定位置，再修改 |

   檔案位置、依賴與編輯範圍遵守工作區當下的 `AGENTS.md` 及內建 skills，不在此維護另一份撰寫規範。

4. **預覽與交付** — 依工作區 scripts 執行，以下為 pnpm 工作區的指令：

   | 需求 | 做法 |
   | --- | --- |
   | 開發、檢視與放映 | `pnpm dev`，支援全螢幕與 presenter mode（講者備註、下一頁預覽、計時器）；也可在頁面元素留下 comment |
   | 建置與部署 | `pnpm build` 產出 `dist/`，以 `pnpm preview` 預覽，再依交付需求部署至靜態網站服務 |
   | PDF | toolbar 的 Export 選單，每頁一張 1920×1080 橫向頁（Safari 不支援） |
   | 圖片版 PPTX | toolbar 的 Export 選單 |

## Output Contract

- 指定工作區內完成或修改的 `slides/<id>/` 簡報。
- 新建或調整主題時，交付 Workflow 所列的完整主題產物；沿用主題時不重建。
- 放映、部署或匯出的使用方式與格式限制。
- 本次有新的定案視覺時，依 design-studio 公約更新專案 `DESIGN.md`。

## Quality Rules

- 視覺決策依 design-studio 的 DESIGN.md、風格庫與品牌公約，不由本 skill 或內建撰寫 skills 另選色板。
- 不複製上游撰寫規範到本 skill 或專案文件，依工作區安裝版本讀取。
- 內建 skills 由 `@open-slide/core` 管理，不就地修改，避免被同步覆蓋。需要更新時使用 `pnpm up @open-slide/core`，再執行 `pnpm sync:skills`，套件管理器依工作區調整。
