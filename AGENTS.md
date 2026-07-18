# AGENTS.md

This file provides guidance to coding agents (Claude Code and others) when working in this repository. `CLAUDE.md` only references this file.

## Repo 性質

這是一個 Agent Skills 集合 repo（63 個 skill，分成 10 個 plugin），同時是 Claude Code plugin marketplace。沒有 build、lint、test 流程，唯一的腳本是打包工具：

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

## 增減修改 skills 的必做事項

### 新增 skill

1. 先決定歸屬哪個 plugin，資料夾建在 `plugins/<plugin>/skills/<skill>/`，不要放根目錄。
2. SKILL.md 遵守上方結構慣例（章節順序、frontmatter 只有 name 與 description、name 等於資料夾名）。
3. 在 `README.md` 對應 plugin 區塊的表格加一列（skill 名 / 適合什麼需求），並更新 README 開頭的 skill 總數。
4. 若這個 skill 改變了 plugin 的收納範圍描述，同步更新 `.claude-plugin/marketplace.json` 與該 plugin 的 `plugin.json` 的 description。
5. 調升該 plugin 的 `plugin.json` version（內容變了，已安裝的使用者靠版本號知道要更新）。

### 修改 skill

1. 只動該 skill 資料夾內的檔案；SKILL.md 與 references/ 的相對連結要保持有效。
2. 若 name 或觸發 description 變了，確認 frontmatter name 仍等於資料夾名。
3. 若 skill 的定位或適用需求變了，同步更新 README.md 表格中該列的描述。
4. 調升該 plugin 的 `plugin.json` version。

### 刪除 skill

1. 刪除 `plugins/<plugin>/skills/<skill>/` 整個資料夾。
2. 從 README.md 對應表格移除該列，並更新 README 開頭的 skill 總數。
3. 若 plugin description 有點名這個 skill，同步更新 marketplace.json 與 plugin.json。
4. 調升該 plugin 的 `plugin.json` version。

### 搬移 skill（換 plugin）

1. 用 `git mv` 保留歷史，搬到新的 `plugins/<plugin>/skills/` 底下。
2. README.md 把該列從舊 plugin 表格移到新 plugin 表格。
3. 兩個受影響 plugin 的 description（marketplace.json + plugin.json）都檢查是否要改，version 都要調升。

### 收尾檢查（所有操作共通）

- 每次把新內容加進 skill，先判斷它該落在哪個檔案、哪個段落，插到最合適的位置，必要時重新組織該檔的分組或順序。不要一律附加在檔尾，不要製造重複段落、不順的引用或檔案間的耦合。加了新規則後，回頭檢查既有內容（尤其示例）是否仍符合全部規則。
- `plugins/*/skills/*/SKILL.md` 的數量、README 表格列數、README 開頭總數三者一致。
- 所有動過的 JSON 能正常解析。
- 需要 claude.ai 上傳包時，跑 `python zip_subfolders.py` 確認 exit 0。

## 重要注意事項

- 根目錄可能有草稿散檔或筆記，是使用者刻意保留的，不要清理或移動。
- 這個 repo 的擁有者對變更把關很嚴：不要一次大批新增或重寫多個 skill。先提案討論方向、拿到同意再動手；小步交付，一次一個 skill，讓使用者驗貨再繼續。
- LLM 自動評審通過不等於使用者會接受，不要拿它當交付依據。
