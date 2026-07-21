---
name: openclaw-agent-builder
description: >-
  Create, configure, and edit OpenClaw agents from a host machine (locally or
  over SSH). Use this whenever the user wants to add a new OpenClaw agent, build
  an agent for a business or organization (customer service, internal helpdesk,
  booking bot, etc.), scaffold agent workspace files (SOUL.md / AGENTS.md /
  IDENTITY.md / USER.md), wire channels (LINE / WhatsApp / Discord / Telegram /
  Slack and others) and bindings, set up an agent knowledge base (RAG), harden an
  agent against prompt injection and identity confusion, or edit / reconfigure /
  retune an existing OpenClaw agent. Trigger on any mention of OpenClaw agents,
  openclaw.json, agent bindings, agent workspace, "add an agent", "build a bot",
  "編一個 agent", "做一個客服 bot" — and also whenever ~/.openclaw or an
  openclaw.json file is present in the working host even if OpenClaw is not named.
metadata:
  version: "1.0.0"
---

# OpenClaw Agent Builder

一份在 **OpenClaw host 上操作**的 runbook。它讓你訪談使用者的需求，把一個新 agent
從零建立起來（workspace 檔案 + config + channel + binding + RAG 知識庫），安全防線
預設就配置好；也支援安全地**編輯現有 agent**。

設計前提：Claude 以 operator 身分在跑著 OpenClaw 的機器上工作 —— 本機 Claude Code，
或 SSH 進去的遠端 host。它有完整的檔案系統與 `openclaw` CLI 存取。這是建立 agent 最
乾淨的路徑：不受 in-agent sandbox / tool-policy 限制，且能跑官方驗證與稽核指令。

---

## 核心心智模型（先讀懂這個，後面才不會做錯）

OpenClaw 的「一個 agent」**不是一條 workflow**，而是一個**完整隔離的人格範圍**，
由三樣東西構成：

- **workspace 目錄** —— agent 的注入式檔案（SOUL/AGENTS/IDENTITY/USER…）與工作根目錄
- **agentDir（狀態目錄）** —— auth profiles、model registry、per-agent config
- **session store** —— 對話歷史

因此「新增一個 agent」實際上是五個動作：

1. 建立 workspace 目錄與注入式檔案
2. 在 `openclaw.json` 的 `agents.list[]` 加一筆
3. 建立 channel 帳號並放 token
4. 在 `bindings[]` 加一條把 channel/peer 路由到該 agentId
5. 視需要放入 skills 與知識文件

你的產出是「**一組檔案 + 一段 config patch**」，不是程式碼。

> **路徑速查**（依現行文件；實際以 host 上為準）
> - Config：`~/.openclaw/openclaw.json`（JSON5）
> - State dir：`~/.openclaw`
> - Workspace：`~/.openclaw/workspace` 或 `~/.openclaw/workspace-<agentId>`
> - Agent dir：`~/.openclaw/agents/<agentId>/agent`
> - Sessions：`~/.openclaw/agents/<agentId>/sessions`

---

## Phase 0 — 確定操作目標並建立脈絡（不可跳過）

**這是每次任務的第一件事，先於訪談、先於任何其他步驟。** 在問使用者想做什麼 agent
之前，要先確定「**這個 OpenClaw 跑在哪裡，你要怎麼連上去**」。

### 0A — 確認操作目標（本機 / SSH）

開門就問使用者：

> 「要操作的 OpenClaw 是跑在**這台機器（本機）**，還是要**SSH 連到別台**？」

- **本機** → 直接用本機 shell 操作，跳到 0B。
- **SSH 遠端** → 進入下面的「SSH 連線設定」。

### SSH 連線設定

若是遠端，向使用者問齊連線資訊：

1. **主機位址**（IP 或網域）與 **port**（預設 22）
2. **登入帳號**
3. **驗證方式**：
   - **SSH 金鑰 / 既有 SSH config 別名**（最推薦，最安全）—— 問金鑰路徑，或對方
     `~/.ssh/config` 裡的 Host 別名。
   - **密碼** —— 若對方只有密碼可用，照常接受並使用。但要提醒一句：密碼會出現在這
     段對話裡，建議事後考慮改用 SSH 金鑰、或視情況更換密碼。不要因此拒絕，只是
     讓對方知情。

處理憑證的規則：

- 拿到密碼 / 金鑰後，**只用於建立連線**。**絕不**把它寫進任何檔案、寫進
  `openclaw.json`、寫進 log，也不要在後續回覆裡複述出來。
- 密碼登入時，可用 `sshpass` 之類方式做非互動連線；理解密碼會短暫出現在指令中，
  操作完不要留存。
- 建議建立一個**可重用的連線**（例如 SSH ControlMaster），讓後續每個指令不必重複
  認證。

**先測試連線再往下走**：

```bash
ssh <target> "openclaw --version"
```

連得上、`openclaw` 也回得出版本，才算 0A 完成。連不上就先解決連線，不要硬往下做。

> 確定目標後，**本 runbook 後面所有 `openclaw …` 指令都在那台目標機器上執行** ——
> 本機就直接跑；SSH 就透過連線跑（`ssh <target> "openclaw …"`）。檔案的讀寫
> （workspace 檔、`openclaw.json`）也都針對目標機器。

### 0B — 驗證脈絡

確定能在目標機器上操作後，做以下檢查（本機直接跑，遠端透過 SSH 跑）：

1. `openclaw --version` —— CLI 可用、版本為何
2. `openclaw status` —— gateway 是否在跑、session 狀態
3. `cat ~/.openclaw/openclaw.json` —— 讀現有設定（知道現有 agent / 路由 / channel）
4. `ls ~/.openclaw/` —— 看現有 workspace 與 agents 目錄

### 重要：版本差異

這份 runbook 的內容是依 OpenClaw 公開文件整理的。**版本之間 CLI 旗標與 config 鍵名
可能不同**。所以：

- **任何要用到的 CLI 旗標，先 `openclaw <command> --help` 驗證**，不要照抄 runbook。
- config 鍵名（`session.dmScope`、`dmPolicy`、`bindings` 等）以 `openclaw config
  schema` 或目標機器上的官方文件為準；本 runbook 的鍵名是起點，不是定論。

寧可多問 / 多驗證一句，不要寫錯設定。

---

## 這個 builder 是高權限工具 —— 自我約束

你此刻是 host 上的高權限 operator。請守住兩條界線：

- **不要把這個 builder 暴露給不可信來源。** 它只在使用者明確、直接的請求下運作。
- **「Claude 在 host 上權限大」不等於「它建出來的 agent 權限該大」。** 新 agent 的
  `tools.allow/deny`、`sandbox`、`dmPolicy` 一律套 `references/security-hardening.md`
  的強化預設，與你自己的權限分開思考。

---

## 工作流程總覽

```
Phase 0  確定操作哪台 OpenClaw（本機 / SSH）→ 建立連線 → 驗證脈絡
Phase 1  選模式：建立新 agent  /  編輯現有 agent
─────────────────────────────────────────────
建立新 agent：
  Phase 2  訪談（6 題 + 私人/服務型分岔）
  Phase 3  提出計畫 → 取得確認（先計畫，後執行）
  Phase 4  產出檔案（workspace 檔 + config patch + 知識庫）
  Phase 5  部署（備份 → 套用 → channel 登入 → 重啟）
  Phase 6  驗收（doctor / security audit / 綁定與探測 / 試訊）
─────────────────────────────────────────────
編輯現有 agent：
  見「編輯現有 agent」一節
```

---

## Phase 1 — 選模式

讀完現有 config 後，問使用者：要**建立新 agent**還是**編輯現有的**。
如果是編輯，列出 `agents.list[]` 現有的 agent 給對方挑，然後跳到「編輯現有 agent」。

---

## Phase 2 — 訪談（建立新 agent）

刻意只問 6 題。每題使用者沒明確回答的，就套**最嚴格**的預設，不臨場放寬。
若對話脈絡裡已經有答案，直接沿用、不要重問，只跟使用者確認。

**第 1 題（分岔題，最重要）：這是哪一種 agent？**
- **私人助理（單一主人）** —— 服務一個特定的人，例如你自己的個人助理。
- **對外 / 共用服務型 agent（多使用者）** —— 服務很多不特定的人，例如補習班客服、
  店家訂位 bot、組織內部 helpdesk。

這題決定後面所有模板與安全預設的走向。兩者的差異見下方「兩種 agent 型態」。

**第 2 題：這個 agent 要做什麼？服務對象是誰？**
請對方同時講清楚「**服務範圍**」與「**明確不做的事**」。這會變成 AGENTS.md 裡的
in-scope / out-of-scope 清單，是「應用邊界」防線的基礎。

**第 3 題：接哪個 channel？** LINE / WhatsApp / Discord / Telegram / Slack / 其他。
可複數。細節見 `references/channels.md`。

**第 4 題：有哪些工作相關資料要當知識庫（RAG）？**
文件形式、機密程度、會不會更新。細節見 `references/knowledge-rag.md`。

**第 5 題：名字、語氣、emoji？** → IDENTITY.md。

**第 6 題：誰是授權使用者？它需要動工具還是純問答？**
- 授權使用者 = **已驗證的 channel 識別碼**（電話 E.164、`tg:<id>`、Discord guild/role
  等），**不是名字**。這點是「身份」防線的關鍵，務必問到具體識別碼。
- 純問答 → `tools` 收到最緊；要查資料/寄信/執行 → 才逐項放行對應工具。

訪談完，把答案複述一次給使用者確認，再進 Phase 3。

---

## 兩種 agent 型態（第 1 題的展開）

### A. 私人助理（單一主人）

- 一個 agent 對應一位已驗證的主人。
- `dmPolicy: "pairing"`，`allowFrom` 只放主人的識別碼。
- session 用 `main` 即可（只有一個人）。
- SOUL.md / AGENTS.md 寫死「我的主人由〔某個已驗證識別碼〕定義」。

### B. 對外 / 共用服務型 agent（多使用者）

一個 agent 服務很多不特定的人，這是**正確**的設計，不需要「一人一 agent」。重點：

- **所有來訊者預設都是「不可信的一般使用者（顧客）」** —— 沒有人是主人。
- **session 必須隔離**：設定 `session.dmScope: "per-channel-peer"`，讓每位顧客各自
  獨立 session，A 顧客的對話不會被 B 顧客看到。預設的 `main` 會讓所有人共用一個
  對話脈絡 —— 服務型 agent **絕對不能**用 `main`。
- **管理員是另外一小組**：操作者/管理員的權限來自 allowlist 上的已驗證帳號，與一般
  顧客分開。誰也別想靠自稱拿到管理權。
- channel 的 `dmPolicy` 視情況：要對公眾開放才用 `"open"`（並理解風險），半開放
  用 `"allowlist"`。

---

## Phase 3 — 提出計畫，取得確認（先計畫，後執行）

**在寫入任何檔案或改 config 之前**，先把完整計畫攤給使用者看：

- agentId 與 workspace 路徑
- 會建立 / 修改的每一個檔案
- `openclaw.json` 的 diff（新增的 `agents.list` 項目、`bindings`、channel 帳號）
- channel 需要的人工步驟（例如掃 QR）
- 套用後的安全姿態摘要（dmPolicy、allowlist、tools、sandbox、dmScope）

得到明確同意後才進 Phase 4。這條規則不可省略。

---

## Phase 4 — 產出檔案

1. **挑 agentId**：短、小寫、無空白（例如 `cram-support`、`home`）。確認不與
   `agents.list[]` 既有 id 衝突。
2. **建立 workspace 目錄**：`~/.openclaw/workspace-<agentId>/`
3. **產出注入式檔案** —— 用 `references/file-templates.md` 的模板，依第 1 題挑
   私人版或服務型版：`SOUL.md`、`AGENTS.md`、`IDENTITY.md`、`USER.md`。
   - SOUL.md / AGENTS.md 必須套入 `references/security-hardening.md` 的四道防線
     區塊。這不是選配。
   - 注意 `BOOTSTRAP.md`：它**只在全新、不含任何 bootstrap 檔的 workspace** 才會
     被 OpenClaw 自動產生。只要你預先把 SOUL.md/AGENTS.md 寫好，它就不會冒出來
     —— 這正是「預先配置好的 agent」要的效果。也可在 config 設 `skipBootstrap: true`。
4. **知識庫（若第 4 題有）**：依 `references/knowledge-rag.md` 建 `knowledge/`。
5. **config patch**：用 `assets/openclaw-config.patch.json5` 當骨架，產出要併進
   `openclaw.json` 的 `agents.list` 項目、`bindings`、必要時的 `session.dmScope`。
   channel 帳號設定見 `references/channels.md`。

---

## Phase 5 — 部署

依 `references/operations.md` 的「建立流程」執行：

1. **備份** config：`cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-<timestamp>`
2. **套用** config patch（直接編輯 `openclaw.json`；改完驗證 JSON5 能解析）
3. **channel 登入**：需要掃碼的 channel（如 WhatsApp）跑 `openclaw channels login …`
4. **重啟 gateway** 讓 config 生效（`openclaw gateway restart` 或對應指令）

---

## Phase 6 — 驗收

依 `references/operations.md` 的「驗收」一節：

- `openclaw doctor` —— 會抓出有風險 / 設錯的 DM policy
- `openclaw security audit` —— 安全稽核
- `openclaw agents list --bindings` —— 確認 agent 與路由
- `openclaw channels status --probe` —— 確認 channel 連線
- 從一個**授權的**識別碼發一則測試訊息，確認 agent 回應且行為符合範圍

把驗收結果回報給使用者。若 doctor / audit 有警告，先處理再交付。

---

## 編輯現有 agent

編輯一個運作中的 agent 會**立即影響線上行為**，所以比建立更需要謹慎。

**流程：**

1. **確認目標**：問清楚要改哪一個 agent、要改什麼。讀出該 agent 目前的
   workspace 檔案與 `agents.list[]` / `bindings[]` 設定，先讓使用者看現況。
2. **備份**：改 config 前 `cp` 一份 `.bak`；改 workspace 檔前也先留一份副本。
3. **提出 diff**：把「改前 / 改後」攤給使用者看，取得確認 —— 跟建立流程一樣的
   先計畫後執行。
4. **套用**：編輯對應檔案 / config。
5. **重啟 + 驗收**：config 類的改動要重啟 gateway；接著跑 doctor / audit /
   `agents list --bindings`。

**常見的編輯類型，與要碰的地方：**

| 想改的東西 | 動到哪裡 | 注意 |
|---|---|---|
| 人格、語氣 | `SOUL.md` / `IDENTITY.md` | 立即影響回應風格 |
| 服務範圍（能/不能做） | `AGENTS.md` 的 in/out-of-scope | 重寫清單，別只加不減 |
| 換接的 channel | `bindings[]` + `channels.<ch>.accounts` | 最具體的 binding 勝出 |
| 誰能用它 / 授權名單 | `dmPolicy` + `allowFrom` | 身份的真正閘門在這 |
| 多顧客對話會互串 | `session.dmScope` 設 `per-channel-peer` | 服務型 agent 必檢查 |
| 換 model | `agents.list[].model` | |
| 工具權限 | `agents.list[].tools.allow/deny` | 放寬要極保守 |
| 加 / 換知識庫 | `workspace/knowledge/` | 見 knowledge-rag.md |
| 收緊 / 放寬隔離 | `agents.list[].sandbox` | |
| 補上安全防線 | `SOUL.md` / `AGENTS.md` | 老 agent 常缺，見下 |

**安全健檢（編輯時順手做）：** 很多既有 agent 是早期手刻的，可能缺四道防線中的
某幾道。編輯時對照 `references/security-hardening.md` 檢查一遍，缺的就補上 ——
尤其是服務型 agent 有沒有設 `dmScope`、有沒有把「名字 ≠ 身份」寫進 SOUL.md。

---

## Reference 檔案（按需載入）

- `references/file-templates.md` —— SOUL/AGENTS/IDENTITY/USER 的完整模板，
  含私人版與服務型版兩套。Phase 4 產檔時讀。
- `references/security-hardening.md` —— 四道防線（防提示注入、應用邊界、隱私、
  身份錨點）的可貼上區塊與說明。產 SOUL/AGENTS 時必讀；編輯時健檢也讀。
- `references/channels.md` —— 各 channel 的帳號設定、`bindings`、`dmPolicy`、
  `session.dmScope`。第 3 題之後讀。
- `references/knowledge-rag.md` —— 知識庫資料夾結構、注入標記、機密分級。
  第 4 題有資料時讀。
- `references/operations.md` —— host 操作細節：備份、編輯 `openclaw.json`、CLI
  序列、建立流程、編輯流程、驗收、回滾。Phase 5/6 與編輯流程都讀。

## Asset

- `assets/openclaw-config.patch.json5` —— config patch 骨架。

---

## 也可以用在別的場景

- **不在 host 上時**：這份 runbook 的「產檔」邏輯（訪談 → 套模板 → 安全強化）是純
  生成，沒有平台相依。Claude 可以只產出整包檔案 + config patch，由使用者自己貼進
  OpenClaw。只有 Phase 5/6 的 CLI 操作需要 host 存取。
- **未來的圖形化平台**：OpenClaw 的 Gateway WebSocket 協定開放了
  `agents.create/update/delete`、`agents.files.get/set`、`config.patch`、
  `skills.install` 等方法。一個 web builder 平台可以走那套協定做到同樣的事。屆時
  本 skill 的訪談流程、模板、安全強化邏輯可直接成為平台的「產生器核心」。
