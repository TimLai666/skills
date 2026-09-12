# Agent Skills

60 個 agent skills，分成 10 個 plugins，這個 repo 同時是 Claude Code plugin marketplace。

## 安裝方式

### Claude Code（推薦，一次裝一整組）

這是兩個獨立指令，先註冊 marketplace，再安裝 plugin：

```
# 1. 把這個 repo 註冊成 plugin marketplace（只需做一次）
/plugin marketplace add TimLai666/skills

# 2. 安裝想要的 plugin，格式是 <plugin名>@<marketplace名>（marketplace 名固定是 skills）
/plugin install dev-workflow@skills
```

裝一個 plugin 就會拿到該組全部 skills。plugin 名稱見下方目錄，也可以直接輸入 `/plugin` 開選單挑著裝。

### npx skills CLI

```bash
# 互動式挑選要裝哪些 skills
npx skills add TimLai666/skills

# 裝全部
npx skills add TimLai666/skills --all

# 裝單一 skill（指定完整路徑）
npx skills add https://github.com/TimLai666/skills/tree/main/plugins/dev-workflow/skills/software-engineering-guidelines
```

### claude.ai（逐個上傳 zip）

在 repo 根目錄執行 `python3 zip_subfolders.py`，會把每個 skill 壓成 `output/<skill>.zip`，再到 claude.ai Settings → Capabilities 上傳。

## Plugin 目錄

### `thinking-frameworks` — 通用思考框架

| Skill | 適合什麼需求 |
| --- | --- |
| `ultrathink` | 釐清尚有疑點或取捨的問題，依需要選用方法，查證假設、比較方案與反例，再提出建議。六語分析與完整謬誤檢核依需要自動啟用，也可明確指定。 |
| `plan-grilling` | 釐清或壓力測試功能、行銷、提案、流程與個人計畫，先查事實，再逐題處理未決選擇，整理範圍、驗收條件與決策紀錄。 |
| `subtraction-thinking` | 想在動手前、途中、完成後強制做一輪減法審查：商業決策、組織流程、產品、行銷、提案報告、程式開發都適用。移除沒有存在理由的東西，簡化留下來的東西。 |

### `business-strategy` — 商業策略與評估

| Skill | 適合什麼需求 |
| --- | --- |
| `business-model-architect` | 想拆解或設計商業模式，整理價值主張、客群、通路、收入、成本與關鍵資源。 |
| `bcg-growth-share-matrix` | 想用 BCG growth-share matrix 分析產品、品牌、事業組合的投資優先順序。 |
| `pestel-analysis` | 想做嚴謹的 PESTEL / 外部環境掃描，作為 SWOT 或策略規劃前置分析。 |
| `swot-analysis` | 想做完整 SWOT 策略分析、外部環境掃描與 SO/ST/WO/WT 策略碰撞。 |
| `decision-bias-quality-control` | 想在高風險決策、提案審查、go/no-go 判斷前做偏誤檢查。 |
| `red-flag-contract-scanner` | 想對合約、租約、服務條款、聘僱契約等進行「紅旗條款」與不利條件掃描，並轉化為白話建議。 |

### `customer-insight` — 顧客研究與洞察

| Skill | 適合什麼需求 |
| --- | --- |
| `orchestrating-mixed-methods` | 不確定研究該做質化、量化、還是 mixed methods，想先決定方法。 |
| `customer-persona-framer` | 想先把目標客群整理成清楚的 persona。 |
| `customer-journey-mapper` | 已經有 persona，想進一步做 customer journey map 或 touchpoint journey table。 |
| `review-mining-stp` | 想把評論、客服紀錄、回饋文字整理成 STP 分析。 |
| `theory-analysis` | 想用產品定位、購買動機、口碑動機三套理論分析跨來源證據（訪談摘要、工單、貼文、研究筆記、觀察紀錄），逐句標註構面並保留可追溯引文。可同時套用多個理論。 |
| `review-scoring-docx` | 想把評論資料抽取屬性並做產品評分，輸出為 Word（.docx）報告。 |
| `review-salience-xlsx` | 想把評論做顯著度評分、PCA、K-means 分群並輸出 Excel（.xlsx）。 |
| `product-conjoint-analysis` | 想做商品屬性偏好分析、估算屬性重要性與願付價格（WTP），找出最佳商品組合與定價/成本效益方向。 |

### `marketing-strategy` — 行銷策略與訊息設計

| Skill | 適合什麼需求 |
| --- | --- |
| `sor-marketing-strategy` | 想用 S-O-R 模型把刺激、心理反應、行為回應整理成行銷策略。 |
| `psychological-trigger-marketing` | 想產出更有轉換力的行銷角度、CTA、campaign hooks、促發點。 |
| `maslow-five-needs-marketing` | 完整分析 Maslow 五層受眾需求，再依證據決定主次訴求、投入順序與訊息方向。 |
| `content-growth-studio` | 依自然語意處理內容分析、主題發想、影片標題、文章與社群改編，或設計內容生產流程，配合受眾與通路改善觸及、閱讀及互動。 |
| `threads-viral-growth` | 撰寫或改善 Threads 與一般社群文案，新稿與改寫皆先查四類來源，再設計切角、語氣與互動；依需求提供排程和成效分析。 |
| `experiential-guerrilla-marketing` | 想規劃快閃、品牌體驗與游擊活動，設計受眾參與方式、現場執行安排，並依活動目標評估成效。 |

### `service-innovation` — 服務設計與創新

| Skill | 適合什麼需求 |
| --- | --- |
| `ecosystem-map-and-blueprint` | 想用生態系地圖拆解服務參與者與價值交換，或用服務藍圖展示前台後台運作流程。 |
| `service-design-workshop` | 規劃或改善服務設計，整理問題、利害關係人、服務架構、接觸點與驗證計畫，支援完整工作坊及局部修改。 |
| `service-innovation-case-study` | 研究服務創新案例，串接市場、策略、商業模式與顧客體驗，支援完整報告、課堂格式與局部研究。 |
| `service-innovation-workshop` | 從服務創新機會形成概念、比較方案或驗證既有方向，支援完整工作坊與局部需求。 |
| `scamper` | 想對現有產品、服務、流程或商業模式套用 SCAMPER 奔馳法，從七個思維維度系統化產出創新構想與優先方案。 |

### `writing-and-design` — 提案與頁面產出

| Skill | 適合什麼需求 |
| --- | --- |
| `commercial-proposal-writing` | 想寫或改提案、合作方案、募資 deck、商業計畫。 |
| `landing-page-studio` | 想產出偏高轉換導向的 landing page、hero section、行銷頁面。 |
| `design-studio` | 所有設計事務的統一入口：網站、App、簡報、動畫、資訊圖、品牌設計。建立或變更共用視覺規範時更新 `DESIGN.md`，純評論與局部修改沿用既有設計資料。支援電影感（cinematic-ui）與實作導向（practical）雙引擎。 |
| `open-slide-studio` | 想把簡報做成可放映、可部署成網址的網頁簡報（open-slide 框架），視覺由 design-studio 供給；要可編輯 .pptx 仍走 design-studio。 |
| `human-writing` | 想要產出文案、文章、內容重寫或其他寫作支援。 |

### `dev-workflow` — 開發流程與工程支援

| Skill | 適合什麼需求 |
| --- | --- |
| `eng-architect` | 設計技術架構、釐清模組邊界、按可驗收行為拆任務，或審查 UI。沿用專案既有文件與任務系統，沒有安排且需要完整交接時建立預設協作文件。 |
| `diff-inspector` | 想在合併前審查 diff：scope drift check、critical code review、specialist 並行掃描、adversarial review。 |
| `test-and-fix` | 依指定範圍或 diff 測試網站、API、命令列工具與函式庫，追查失敗原因、修復並驗證回歸測試。 |
| `ship-it` | 整理功能分支並建立或更新 PR：依專案規則同步、測試與審查，確認 CI 狀態，收尾記錄實際經驗。 |
| `project-memory` | 想記錄專案教訓、踩過的雷、學到的 pattern，支援搜尋與匯出。 |
| `investigate` | 錯誤原因不明時，依證據提出假說、追查資料流並驗證修正；也適用於明確要求根因調查。 |
| `software-engineering-guidelines` | 任何軟體規劃、架構、實作、重構、review、測試前先載入：想清楚再做、最小變更、精準手術、每次變更都有測試，大改動採 TDD、目標驅動。 |
| `db-engineering` | 任何資料庫相關工作都要先載入：先畫 ER model、以 BCNF 優先設計並至少維持 3NF，再處理 migration、稽核 log、軟刪除、效能、完整性與環境分離。 |
| `postgrest-baas-builder` | 用 Supabase / InsForge 做後端時：RLS policy、Auth 串接、PostgREST 查詢、MCP 設定。需搭配 db-engineering。 |
| `set-zeabur-conventions` | 想為專案設定 Zeabur 部署規範（寫入 AGENTS.md，給所有 agent 看）。 |
| `openclaw-agent-builder` | 想建立、配置或改造 OpenClaw agent，包括 workspace、channel、bindings、RAG 知識庫與安全設定。 |
| `openclaw-ops` | 想在運行中的 OpenClaw 機器上做運維、配置、診斷。 |

### `data-and-research` — 資料分析與研究

| Skill | 適合什麼需求 |
| --- | --- |
| `data-analysis-workflow` | 想把資料分析從資料檢查、清理、EDA、建模、評估一路做成標準化流程並產出分析報告。 |
| `investment-research-prompts` | 想快速套用股票篩選、投資組合風險、股息策略、財報前瞻、DCF、技術分析或趨勢識別等投資研究模板。 |
| `arxiv` | 想搜尋 arXiv 論文、查 Semantic Scholar 引用數據、產生 BibTeX、做學術文獻回顧。 |

### `knowledge-tools` — 知識管理與圖表

| Skill | 適合什麼需求 |
| --- | --- |
| `llm-wiki` | 想把來源資料（文章、論文、筆記）整理成結構化 Obsidian 知識庫，含 entity/concept 頁面、交叉引用與版本追蹤，頁面寫入採卡片盒筆記法紀律。 |
| `zettelkasten` | 想建立或維護卡片盒筆記系統（原子卡片、永久筆記、連結網絡），或替既有筆記庫套上原子性檢核、拆卡判準與連結紀律。 |
| `tutor-setup` | 想建立 Obsidian StudyVault，從既有 wiki 或文件匯入學習素材，設定 quiz 規則與進度追蹤。 |
| `tutor` | 想用互動式 quiz 學習 StudyVault 裡的概念，追蹤已知/未知、生成練習題與解釋。 |
| `obsidian-markdown` | 想建立或編輯 Obsidian Flavored Markdown，處理 wikilinks、callouts、frontmatter、embeds 等語法。 |
| `obsidian-cli` | 想用 CLI 操作 Obsidian vault（搜尋、替換、匯出、管理 vault）。 |
| `obsidian-bases` | 想在 Obsidian 裡建立資料庫視圖（類似 Notion database），管理結構化資料。 |
| `obsidian-canvas-creator` | 想建立 Obsidian Canvas（.canvas），做空間佈局、心智圖或自由版面配置。 |
| `excalidraw-diagram` | 依需求產出獨立流程圖、心智圖、關係圖或可編輯白板，支援 Obsidian、標準 Excalidraw 與動畫；HTML Artifact 內的圖優先沿用 HTML 做法。 |
| `mermaid-visualizer` | 依文字與使用情境產出 Mermaid 流程圖、時序圖或架構圖，配合目標渲染工具驗證，HTML Artifact 優先沿用既有製作方式。 |

### `utilities` — 通用工具

| Skill | 適合什麼需求 |
| --- | --- |
| `defuddle` | 想從 HTML 網頁提取乾淨的 Markdown 內容，移除廣告與導航列。 |
| `windows-rescue-from-linux` | 用 Linux 救援 Windows，將完整系統與工具預裝至 USB 救援碟，處理開機、NTFS、BitLocker、資料與帳號問題，也能從 Windows 映像提取檔案替換損壞的系統組件。 |

## Repo 結構

```
.claude-plugin/marketplace.json      ← marketplace 宣告
plugins/<plugin>/
├── .claude-plugin/plugin.json       ← plugin 描述
└── skills/<skill>/
    ├── SKILL.md
    ├── references/                  ← 細節文件（可選）
    ├── assets/                      ← 模板（可選）
    └── scripts/                     ← 可執行工具（可選）
```

## Notes

- 根目錄的草稿、zip、筆記不是 install path。
- 要確認某個 skill 的細節，進 `plugins/<plugin>/skills/<skill>/SKILL.md` 看。

## 子資料夾壓縮腳本用法

- 腳本位置：`zip_subfolders.py`（repo 根目錄）
- 在 repo 根目錄執行：

```powershell
python3 zip_subfolders.py
```

- 腳本會做的事：
  - 掃描 `plugins/*/skills/*` 下的每個 skill 資料夾。
  - 將每個 skill 壓縮成 `output/<skill_name>.zip`。
  - 若同名 zip 已存在，會覆蓋重建。

- 退出行為：
  - 全部成功時回傳 `0`。
  - 任一資料夾失敗時回傳非 `0`。
  - 終端會輸出每個資料夾的 `OK/SKIP/FAIL` 與最後 `Summary`。
