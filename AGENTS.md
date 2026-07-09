# AGENTS.md

This file provides guidance to coding agents (Claude Code and others) when working in this repository. `CLAUDE.md` only references this file.

## Repo 性質

這是一個 Agent Skills 集合 repo（61 個 skill，分成 9 個 plugin），同時是 Claude Code plugin marketplace。沒有 build、lint、test 流程，唯一的腳本是打包工具：

```powershell
python zip_subfolders.py
```

它會掃描 `plugins/*/skills/*`，把每個 skill 資料夾壓成 `output/<skill_name>.zip`（覆蓋重建）。`output/` 與 `*.zip` 已在 .gitignore。

## Marketplace / Plugin 結構

```
.claude-plugin/marketplace.json      ← marketplace 宣告，列出所有 plugins
plugins/<plugin>/
├── .claude-plugin/plugin.json       ← plugin 名稱、描述、版本
└── skills/<skill>/                  ← skill 本體
```

安裝方式：`/plugin marketplace add TimLai666/skills` 後 `/plugin install <plugin>@skills`；也支援 `npx skills add`（靠該 CLI 的遞迴 fallback 探測）。

## Skill 結構慣例

每個 skill 一個資料夾，位於 `plugins/<plugin>/skills/<skill>/`：

- `SKILL.md` — 精簡主檔（約 100-200 行），章節依序為：Overview → Input Contract → Data Sufficiency Gate（可選）→ Workflow → Output Contract → Quality Rules → Common Mistakes → Quick Reference → Suggested Prompt（後幾節視 skill 需要取捨）
- `references/` — 細節、理論、播放手冊，SKILL.md 用相對連結指向它們
- `assets/templates/` — 輸出模板
- `scripts/` — 可執行工具（少數 skill 有）
- `agents/` — 驗證情境或壓力測試案例（少數 skill 有）

Frontmatter 只有兩個欄位：`name`（必須等於資料夾名）與 `description`（英文觸發說明並嵌入中文觸發詞，<1024 字元）。不要加其他欄位。

範本級 skill 可參考：`plugins/marketing-strategy/skills/sor-marketing-strategy`（完整結構）、`plugins/service-innovation/skills/scamper`（精簡版）、`plugins/dev-workflow/skills/postgrest-baas-builder`（大型多檔）。

內容語言以繁體中文（台灣）為主，frontmatter description 為英文夾中文觸發詞。

## 必須同步的東西

新增、改名、刪除、搬移 skill 時，以下三處必須同步：

1. `README.md` 對應 plugin 區塊的目錄表（skill 名 / 適合什麼需求）。
2. 若 plugin 的收納範圍變了，`.claude-plugin/marketplace.json` 與該 plugin 的 `plugin.json` 的 description 也要跟著改。
3. skill 資料夾必須放在某個 `plugins/<plugin>/skills/` 底下，不要放回根目錄。

## 重要注意事項

- 根目錄可能有草稿散檔或筆記，是使用者刻意保留的，不要清理或移動。
- 這個 repo 的擁有者對變更把關很嚴：不要一次大批新增或重寫多個 skill。先提案討論方向、拿到同意再動手；小步交付，一次一個 skill，讓使用者驗貨再繼續。
- LLM 自動評審通過不等於使用者會接受，不要拿它當交付依據。
