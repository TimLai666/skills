---
name: open-slide-studio
description: >-
  Deliver web-based slide decks on open-slide, the React slide framework for
  agents, with present mode, one-command static deploy, and PDF export. This
  skill MUST be used when the user names open-slide, and SHOULD be used when a
  簡報/deck request emphasizes live presenting, a shareable URL, deployment, or
  presenter mode. Visual style comes from design-studio (DESIGN.md + style
  library) and is written into the workspace as an open-slide theme; deck
  authoring is handed off to the workspace's built-in skills (create-slide,
  slide-authoring, apply-comments). MUST NOT be used when the deliverable is an
  editable .pptx file — that is design-studio's PPTX route — and MUST NOT be
  used without a local Node.js environment. 觸發詞：open-slide、網頁簡報、簡報網站、簡報部署、線上簡報、presenter
  mode。
metadata:
  version: "1.0.2"
---

# Open Slide Studio

## Overview

本 skill 是疊在 `design-studio` 上的**簡報跑道層**：design-studio 出視覺，[open-slide](https://github.com/1weiho/open-slide) 當執行環境（React、1920×1080 canvas、present mode、靜態部署），本 skill 只管三件事——交付格式分流、工作區建立與視覺接軌、交棒給工作區內建 skills。

簡報怎麼寫（canvas 規範、type scale、版面規則）由 open-slide scaffold 進工作區的內建 skills 負責，且隨 `@open-slide/core` 版本更新。本 skill 不複製那些規範，過時風險留給上游。

### 交付格式分流

| 使用者要的 | 走哪裡 |
| --- | --- |
| 可編輯的 .pptx（進 PowerPoint 改、套公司模板） | `design-studio` 的 PPTX 路線，不用本 skill |
| 現場放映、presenter mode、部署成網址、PDF | 本 skill（open-slide） |
| PPTX 但可接受每頁是圖片、不可編輯 | 本 skill 可出（toolbar 匯出），交付前必須告知不可編輯 |

格式不明時問一次「要可編輯的 .pptx 檔，還是網頁簡報？」，不要反覆確認。

## Input Contract

必要：

- `topic` — 簡報主題與內容素材（大綱、文件、或口頭描述）
- `delivery` — 交付格式（依上表分流後確定）

選填：

- `workspace_dir` — 工作區位置；已有 open-slide 工作區（有 `open-slide.config.ts` 與 `slides/`）就沿用，不重複 init
- `style_direction` — 視覺方向；沒給就走 design-studio 的風格庫選定流程

## Workflow

1. **分流** — 依上表確認交付格式。落在 design-studio 路線就交還，不繼續。
2. **工作區** — 沒有現成工作區時執行：

   ```bash
   npx @open-slide/cli init <dir>
   cd <dir>
   pnpm install
   ```

   套件管理器以 init 輸出的指示為準。init 會 scaffold 內建 skills（create-slide、slide-authoring、apply-comments、create-theme、current-slide）與工作區 `AGENTS.md`；skills 同時放在 `.claude/skills/` 與 `.agents/skills/` 兩個路徑，Claude Code、Codex 等 agent 都能用，依你所在的 agent 讀對應路徑。
3. **視覺接軌** — 依 design-studio 的 DESIGN.md 公約：專案有 `DESIGN.md` 就先讀並沿用 token；沒有就照 design-studio 流程建立。然後把視覺決策（色彩、字體、層級、風格語彙）寫成工作區的 `themes/<id>.md` 主題檔，格式照工作區內建 `create-theme` skill 的規範——`create-slide` 寫頁面前會讀主題檔，這是視覺進入 open-slide 的正式管道。
4. **交棒撰寫** — 起草新 deck 用工作區內建 `create-slide`，任何頁面編輯前先讀 `slide-authoring`。遵守工作區 `AGENTS.md` 的硬規則：slide 放 `slides/<kebab-case-id>/index.tsx`、不新增依賴、不動 `package.json` 與其他 deck。
5. **迭代** — `pnpm dev` 起 dev server，使用者在頁面上點元素留 comment，回來跑內建 `apply-comments` 套用。使用者說「這一頁」「這個元素」時用內建 `current-slide` 解析指涉。
6. **交付** — 依格式收尾：

   | 格式 | 做法 |
   | --- | --- |
   | 放映 | `pnpm dev`，全螢幕播放或 presenter mode（講者備註、下一頁預覽、計時器） |
   | 部署 | `pnpm build` 產 `dist/` 靜態站，丟 Vercel／Cloudflare Pages／Netlify／Zeabur／GitHub Pages |
   | PDF | toolbar 的 Export 選單，每頁一張 1920×1080 橫向頁（Safari 不支援） |
   | PPTX（圖片版） | toolbar Export，每頁是一張圖貼進 PowerPoint，不可編輯 |

## Output Contract

- open-slide 工作區（或沿用的既有工作區），含 `slides/<id>/` 完成的 deck
- `themes/<id>.md` — 由 DESIGN.md 導出的主題檔
- 交付說明：放映／部署／匯出的指令與格式限制
- 依 design-studio 公約，把本次定案的視覺 token 寫回專案 `DESIGN.md`

## Quality Rules

- 視覺決策一律出自 design-studio（DESIGN.md、風格庫、brand 協議），本 skill 與工作區內建 skills 都不自創色板。
- 不把 open-slide 內建 skills 的內容複製進本 skill 或專案文件；規範以工作區當下版本為準，更新走 `pnpm up @open-slide/core && pnpm sync:skills`。
- 工作區內建 skills（`.claude/skills/` 與 `.agents/skills/`）由 `@open-slide/core` 管理，不就地修改，改了會被 sync 覆蓋。
- PPTX 圖片版交付前必須告知不可編輯；使用者要能改的檔就回到分流表。
- 環境沒有 Node.js 時明說做不了，不要退化成手寫 HTML 假裝是 open-slide。

## Common Mistakes

- 把 open-slide 當 .pptx 產生器接單，最後才發現匯出的 PPTX 不可編輯。
- 跳過 `themes/<id>.md`，讓 `create-slide` 用預設美感寫頁面，DESIGN.md 形同虛設。
- 把 1920×1080、type scale 等規範抄進本 skill「以防萬一」，半年後與上游版本打架。
- 在 `slides/` 外亂放檔案或新增依賴，違反工作區 `AGENTS.md` 硬規則。
- 每輪都重問交付格式。

## Quick Reference

| 動作 | 指令 |
| --- | --- |
| 建工作區 | `npx @open-slide/cli init <dir>` |
| 開發／放映 | `pnpm dev` |
| 靜態站建置 | `pnpm build`（產 `dist/`） |
| 預覽建置結果 | `pnpm preview` |
| 更新內建 skills | `pnpm up @open-slide/core && pnpm sync:skills` |

## Suggested Prompt

Use `$open-slide-studio` to turn a deck request into an open-slide workspace: route the delivery format, bridge design-studio visuals in as a theme, then hand authoring to the workspace's built-in skills.
