# AGENTS.md

This file provides guidance to coding agents (Claude Code and others) when working in this repository. `CLAUDE.md` only references this file.

## Repo 性質

這是一個 Agent Skills 集合 repo（62 個 skill，分成 11 個 plugin），同時是 Claude Code plugin marketplace。沒有 build、lint、test 流程，唯一的腳本是打包工具：

```bash
python3 zip_subfolders.py
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

Frontmatter 依 [Agent Skills 規範](https://agentskills.io/specification)，只用規範定義的欄位，不要自創：

| 欄位 | 本 repo 的規定 |
| --- | --- |
| `name` | 必填。必須等於資料夾名，小寫英數與連字號，≤64 字元 |
| `description` | 必填。英文觸發說明並嵌入中文觸發詞，<1024 字元。**必須含 RFC 2119 關鍵字**（見下節）。內含半形冒號加空格時**必須用雙引號包住**，否則 YAML 解析失敗、skill 完全載入不了 |
| `metadata.version` | 必填（本 repo 自訂要求）。字串形式的語意化版本，例如 `version: "1.0.0"`。規範沒有頂層 `version` 欄位，一律放在 `metadata` 底下 |
| `license`、`compatibility`、`allowed-tools` | 選填，有需要才加 |

Claude Code 另有 `disable-model-invocation`、`user-invocable`、`disallowed-tools`、`context`、`agent`、`model` 等擴充欄位，需要時可用，但會綁定 Claude Code。

範本級 skill 可參考：`plugins/marketing-strategy/skills/sor-marketing-strategy`（完整結構）、`plugins/service-innovation/skills/scamper`（精簡版）、`plugins/dev-workflow/skills/postgrest-baas-builder`（大型多檔）。

內容語言以繁體中文（台灣）為主，frontmatter description 為英文夾中文觸發詞。

### description 的 RFC 2119 關鍵字

模型會替自己找理由跳過 skill：「這看起來很簡單，不用載入除錯 skill 吧。」即使訊息裡就有觸發詞。純敘述句的 description（`Use when...`、`Triggers on:`）讀起來像自我介紹，不像指令。

所以每個 description **必須**用 RFC 2119 關鍵字寫出義務強度。只有大寫算數（RFC 8174），小寫的 must 只是普通英文。

| 關鍵字 | 給什麼情況 |
| --- | --- |
| `MUST` | 使用者打出字面觸發詞、或這個 skill 是該類任務的預設做法。每個 description 至少要有一個 |
| `SHOULD` | 語意相關但要判斷的旁圈觸發，例如使用者沒點名卻在描述同一件事 |
| `MUST NOT` | 要擋的具體誤用，通常是「因為看起來簡單所以跳過」，或互斥的替代 skill |

`MAY` 不用。最低強度就是 `SHOULD`，再低等於沒寫。

寫法規定：

- **關鍵字寫進原有句子，不要外掛一段。** `Use when X` 改成 `This skill MUST be used when X`，不要在句尾另接「This skill MUST be invoked.」。
- **既有的語氣詞直接換掉。** `Always trigger` → `MUST trigger`，`Never do X` → `MUST NOT do X`，`Do NOT use for` → `MUST NOT be used for`。
- **不要每個 skill 都堆滿 MUST。** RFC 2119 自己就寫了只有真正必要才用 MUST。全部都是 MUST 等於沒有分級，模型看到的是一堆互相搶的義務。
- **互斥的 skill 用 MUST NOT 劃界。** 例如 excalidraw-diagram / mermaid-visualizer / obsidian-canvas-creator 三選一，各自標明點名哪個格式就用哪個。
- **中文 description 一樣要加**，關鍵字維持大寫英文插進中文句子，例如「MUST 觸發於……」。
- **注意 1024 字元上限。** 加關鍵字會變長，改完要量。`ultrathink` 目前 1016，只剩 8 格。

## 增減修改 skills 的必做事項

### 新增 skill

1. 先決定歸屬哪個 plugin，資料夾建在 `plugins/<plugin>/skills/<skill>/`，不要放根目錄。
2. SKILL.md 遵守上方結構慣例（章節順序、frontmatter 欄位、name 等於資料夾名），description 依 [RFC 2119 關鍵字](#description-的-rfc-2119-關鍵字)寫出義務強度。
3. 在 `README.md` 對應 plugin 區塊的表格加一列（skill 名 / 適合什麼需求），並更新 README 開頭的 skill 總數。
4. 若這個 skill 改變了 plugin 的收納範圍描述，同步更新 `.claude-plugin/marketplace.json` 與該 plugin 的 `plugin.json` 的 description。
5. 調升該 plugin 的 `plugin.json` version（內容變了，已安裝的使用者靠版本號知道要更新）。

### 修改 skill

1. 只動該 skill 資料夾內的檔案；SKILL.md 與 references/ 的相對連結要保持有效。
2. 若 name 或觸發 description 變了，確認 frontmatter name 仍等於資料夾名，且 description 仍符合 [RFC 2119 關鍵字](#description-的-rfc-2119-關鍵字)規定。
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
- 動到某個 skill 的內容時，同時調升該 skill 的 `metadata.version` 與所屬 plugin 的 `plugin.json` version。前者標示這個 skill 本身變了，後者讓已安裝的使用者知道要更新。
- `plugins/*/skills/*/SKILL.md` 的數量、README 表格列數、README 開頭總數三者一致。
- 所有動過的 JSON 能正常解析，所有動過的 SKILL.md frontmatter 能通過 YAML parser。
- 動過的 description 至少含一個 `MUST`，該有的 `SHOULD` 與 `MUST NOT` 也在，且總長仍 <1024 字元。
- 需要 claude.ai 上傳包時，跑 `python3 zip_subfolders.py` 確認 exit 0。

skill 若會在使用者專案裡產生檔案，額外檢查三條：

- **不自創根目錄檔案。** 用既有的協調檔（`AGENTS.md`、`CLAUDE.md`、`DESIGN.md`、`delivery-plan.md`、`ENG.md`、`DESIGN-REVIEW.md`），或放進 `docs/<skill-name>/`。根目錄是使用者的，不是 skill 的工作檯。
- **寫了要有人讀。** 新增一個檔之前先講得出誰讀、在哪一步讀。找不到讀者就別落檔，或降級成交給使用者的成品——成品沒有下游是正常的，協調檔沒有下游就是死檔。共用同一個檔時只更新自己那幾段，不刪不認得的段落。
- **狀態檔不帶日期與 branch。** 反映當前狀態、就地更新的檔（多數屬於此類）用固定檔名，版本歷史與分支隔離交給 git。只有一次性、多份並存才有意義的紀錄檔（例如 `plan-grilling` 的訪談紀錄）才帶日期。覆寫前先讀，不要盲寫。

## Active Issues

<!-- ACTIVE_ISSUES_START -->

| ID | Task | Status |
|---|---|---|

<!-- ACTIVE_ISSUES_END -->

## 重要注意事項

- 根目錄可能有草稿散檔或筆記，是使用者刻意保留的，不要清理或移動。
- 這個 repo 的擁有者對變更把關很嚴：不要一次大批新增或重寫多個 skill。先提案討論方向、拿到同意再動手；小步交付，一次一個 skill，讓使用者驗貨再繼續。
- LLM 自動評審通過不等於使用者會接受，不要拿它當交付依據。
