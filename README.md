# Agent Skills

62 個 agent skills，分成 10 個 plugins，這個 repo 同時是 Claude Code plugin marketplace。

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

在 repo 根目錄執行 `python zip_subfolders.py`，會把每個 skill 壓成 `output/<skill>.zip`，再到 claude.ai Settings → Capabilities 上傳。

## Plugin 目錄

### `thinking-frameworks` — 通用思考框架

| Skill | 適合什麼需求 |
| --- | --- |
| `ultrathink` | 想在產出文章、報告、提案、商業模式、程式等任何交付物之前，先依序跑過全部內建思考框架（目前含邏輯推導：MECE、空雨傘、魚骨圖；創意發想：六頂思考帽、腳本圖、心智圖；市場分析：3C 分析、SWOT 分析、4P與4C；進度管理：惠特默模型、KPI 樹狀圖、PDCA；權衡得失：決策矩陣、PMI 表、力場分析；預測未來：S 型曲線、鴻溝理論、長尾模型；思維模型：第一性原理、反向思考法、二階思考），把方向與重點想清楚再動手。 |

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
| `theory-analysis-product-positioning` | 想用產品定位理論分析跨來源證據（訪談摘要、工單、貼文、研究筆記、觀察紀錄），拆解產品屬性、功能、利益與使用/服務情境。 |
| `theory-analysis-purchase-motivation` | 想用購買動機理論辨識跨來源證據中的功能性、保障性、關係性驅動因素。 |
| `theory-analysis-wom-motivation` | 想用口碑動機理論解析跨來源證據中的利他、社交認同、專業展現與情緒表達動機。 |
| `review-scoring-docx` | 想把評論資料抽取屬性並做產品評分，輸出為 Word（.docx）報告。 |
| `review-salience-xlsx` | 想把評論做顯著度評分、PCA、K-means 分群並輸出 Excel（.xlsx）。 |
| `product-conjoint-analysis` | 想做商品屬性偏好分析、估算屬性重要性與願付價格（WTP），找出最佳商品組合與定價/成本效益方向。 |

### `marketing-strategy` — 行銷策略與訊息設計

| Skill | 適合什麼需求 |
| --- | --- |
| `sor-marketing-strategy` | 想用 S-O-R 模型把刺激、心理反應、行為回應整理成行銷策略。 |
| `psychological-trigger-marketing` | 想產出更有轉換力的行銷角度、CTA、campaign hooks、促發點。 |
| `maslow-five-needs-marketing` | 想用 Maslow needs 分層整理受眾動機、情緒訴求與訊息方向。 |
| `content-growth-studio` | 想製作成長導向內容、標題、腳本、社群包裝，或設計內容生產與複製流程。 |
| `threads-viral-growth` | 想在 Threads 平台產出高互動爆文、設計社群貼文策略、趨勢研究與發文劇本。 |
| `experiential-guerrilla-marketing` | 想規劃體驗行銷與游擊行銷整合策略、快閃活動、低預算高創意行銷與 KPI 評估。 |

### `service-innovation` — 服務設計與創新

| Skill | 適合什麼需求 |
| --- | --- |
| `ecosystem-map-and-blueprint` | 想用生態系地圖拆解服務參與者與價值交換，或用服務藍圖展示前台後台運作流程。 |
| `service-design-workshop` | 想把服務設計題目轉成可執行的工作坊輸出，包含問題框架、利害關係人、服務架構、接觸點與驗證步驟。 |
| `service-innovation-case-study` | 想把服務創新案例做成可教學、可討論、可演練的分析輸出，快速萃取關鍵洞察與可複用策略。 |
| `service-innovation-workshop` | 想把服務創新機會轉成多個概念選項、原型測試與風險檢查。 |
| `scamper` | 想對現有產品、服務、流程或商業模式套用 SCAMPER 奔馳法，從七個思維維度系統化產出創新構想與優先方案。 |
| `subtraction-thinking` | 想在提案、報告、流程、產品或服務設計前後強制做減法審查，移除冗餘與簡化複雜度。 |

### `writing-and-design` — 提案與頁面產出

| Skill | 適合什麼需求 |
| --- | --- |
| `commercial-proposal-writing` | 想寫或改提案、合作方案、募資 deck、商業計畫。 |
| `landing-page-studio` | 想產出偏高轉換導向的 landing page、hero section、行銷頁面。 |
| `design-studio` | 所有設計事務的統一入口：網站、App、簡報、動畫、資訊圖、品牌設計。每次設計會產出或擴充 `DESIGN.md`（Google 格式設計系統檔）。支援電影感（cinematic-ui）與實操快速（huashu-design）雙引擎。 |
| `human-writing` | 想要產出文案、文章、內容重寫或其他寫作支援。 |

### `dev-workflow` — 開發流程與工程支援

| Skill | 適合什麼需求 |
| --- | --- |
| `feature-planner` | 想規劃功能、釐清痛點、挑戰 scope。一題一題問，每題提供 agent 建議，決策立即記錄。 |
| `eng-architect` | 想設計技術架構、畫 architecture diagram、做 error map、建立 delivery-plan.md 等協作 artifact。 |
| `diff-inspector` | 想在合併前審查 diff：scope drift check、critical code review、specialist 並行掃描、adversarial review。 |
| `test-and-fix` | 想跑測試、根據 diff 自動找出 affected routes、修復後加回歸測試。 |
| `ship-it` | 想準備 PR、sync base、跑測試、開 PR，上線後提醒你 CI/deploy 監控方式。 |
| `project-memory` | 想記錄專案教訓、踩過的雷、學到的 pattern，支援搜尋與匯出。 |
| `investigate` | 想先調查根因、驗證假設、再修復，不要先修再問。 |
| `software-engineering-guidelines` | 任何軟體規劃、架構、實作、重構、review、測試前先載入：想清楚再做、最小變更、精準手術、TDD、目標驅動。 |
| `dev-task-loop` | 想用已知 backlog / ticket / 設計參考，一次處理一系列開發任務。 |
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
| `llm-wiki` | 想把來源資料（文章、論文、筆記）整理成結構化 Obsidian 知識庫，含 entity/concept 頁面、交叉引用與版本追蹤。 |
| `tutor-setup` | 想建立 Obsidian StudyVault，從既有 wiki 或文件匯入學習素材，設定 quiz 規則與進度追蹤。 |
| `tutor` | 想用互動式 quiz 學習 StudyVault 裡的概念，追蹤已知/未知、生成練習題與解釋。 |
| `obsidian-markdown` | 想建立或編輯 Obsidian Flavored Markdown，處理 wikilinks、callouts、frontmatter、embeds 等語法。 |
| `obsidian-cli` | 想用 CLI 操作 Obsidian vault（搜尋、替換、匯出、管理 vault）。 |
| `obsidian-bases` | 想在 Obsidian 裡建立資料庫視圖（類似 Notion database），管理結構化資料。 |
| `obsidian-canvas-creator` | 想建立 Obsidian Canvas（.canvas），做空間佈局、心智圖或自由版面配置。 |
| `excalidraw-diagram` | 想產出手繪風格的 Excalidraw 圖（流程圖、心智圖、對比圖），支援 Obsidian .md、標準 .excalidraw 與動畫模式。 |
| `mermaid-visualizer` | 想把文字內容轉成 Mermaid 圖表（流程圖、序列圖、架構圖等），用於簡報與文件。 |

### `utilities` — 通用工具

| Skill | 適合什麼需求 |
| --- | --- |
| `defuddle` | 想從網頁或 PDF 提取乾淨的 markdown 內容，移除廣告與導航列。 |
| `folder-organizer` | 想整理檔案與資料夾結構，快速把專案內容分類成可上傳或分享的格式。 |
| `windows-rescue-from-linux` | 想用 Linux Live USB 救援無法開機或受損的 Windows 電腦，修復 BCD/UEFI、NTFS、BitLocker、資料救援與密碼重設。 |

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
python zip_subfolders.py
```

- 腳本會做的事：
  - 掃描 `plugins/*/skills/*` 下的每個 skill 資料夾。
  - 將每個 skill 壓縮成 `output/<skill_name>.zip`。
  - 若同名 zip 已存在，會覆蓋重建。

- 退出行為：
  - 全部成功時回傳 `0`。
  - 任一資料夾失敗時回傳非 `0`。
  - 終端會輸出每個資料夾的 `OK/SKIP/FAIL` 與最後 `Summary`。
