# Host 操作：建立、編輯、驗收、回滾

這份是 host 上的實際操作程序。**所有 CLI 旗標都先 `openclaw <command> --help`
驗證過再用** —— OpenClaw 版本之間可能不同。

## 目錄

1. 開場：建立 host 脈絡
2. 編輯 openclaw.json 的安全做法
3. 建立流程（新 agent）
4. 編輯流程（既有 agent）
5. 驗收
6. 回滾
7. 常用 CLI 速查

---

## 1. 開場：確定操作目標並連線

每次任務的第一件事 —— 先於訪談、先於一切。

### 1.1 本機還是 SSH

問使用者：要操作的 OpenClaw 跑在**本機**還是要**SSH 連到別台**。

- 本機 → 直接用本機 shell，跳到 1.3。
- SSH → 進 1.2。

### 1.2 SSH 連線

向使用者問齊：

- **主機位址 + port**（預設 22）
- **登入帳號**
- **驗證方式**：
  - SSH 金鑰 / 既有 `~/.ssh/config` 別名（最推薦）—— 問金鑰路徑或 Host 別名。
  - 密碼 —— 若對方只有密碼,照常接受使用,並提醒一句「密碼會出現在這段對話裡,
    建議事後考慮改用金鑰或更換密碼」。不拒絕,只是讓對方知情。

憑證處理規則：

- 密碼 / 金鑰**只用於連線**。絕不寫進任何檔案、`openclaw.json`、log,也不在回覆裡
  複述。
- 密碼登入若需非互動,可用 `sshpass`；理解密碼會短暫出現在指令中,操作後不留存。
- 建議建一個可重用連線（SSH ControlMaster),後續指令免重複認證:
  ```bash
  # 範例：開一個持久連線,後續指令共用
  ssh -M -S /tmp/oc-ctl -o ControlPersist=10m <user>@<host>
  # 之後：ssh -S /tmp/oc-ctl <user>@<host> "openclaw …"
  ```

**先測連線再往下**：

```bash
ssh <target> "openclaw --version"
```

連得上且 `openclaw` 回得出版本,1.2 才算完成。連不上先解決連線,不要硬做。

### 1.3 驗證脈絡

確定能在目標機器操作後（本機直接跑,遠端透過 SSH 跑）：

```bash
openclaw --version                 # CLI 可用？版本？
openclaw status                    # gateway 在跑嗎？session 狀態？
cat ~/.openclaw/openclaw.json      # 讀現有設定
ls ~/.openclaw/                    # 看現有 workspace 與 agents 目錄
```

從 config 的 `agents.list[]` 知道現有哪些 agent；`bindings[]` 知道路由現況；
`channels` 知道接了哪些 channel。

> **本 runbook 後面所有 `openclaw …` 指令與檔案讀寫,都針對這台目標機器。**
> 本機直接跑；SSH 就一律透過連線跑。下面各節的指令範例為求簡潔寫成本機形式,
> 遠端時請自行包成 `ssh <target> "…"`。

---

## 2. 編輯 openclaw.json 的安全做法

`openclaw.json` 是 JSON5 格式（容許註解、尾逗號）。

1. **先備份**：
   ```bash
   cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M%S)
   ```
2. **編輯**：直接改檔。能直接改檔就直接改檔 —— 比走 `agents add` 精靈更可控、可
   diff、可重複執行。
3. **驗證能解析**：改完用 OpenClaw 的工具驗證（例如 `openclaw config …` 相關指令；
   先 `--help` 確認有沒有 validate / check 子指令）。若無，至少用一個 JSON5 parser
   確認語法正確。**絕不留下無法解析的 config。**
4. config 類改動要**重啟 gateway** 才生效。

---

## 3. 建立流程（新 agent）

對應 SKILL.md 的 Phase 4–6。前置：Phase 2 訪談完、Phase 3 計畫已獲使用者確認。

```
步驟 1  挑 agentId（短、小寫、無空白、不與既有 id 衝突）
步驟 2  建 workspace 目錄
        mkdir -p ~/.openclaw/workspace-<agentId>
步驟 3  產出注入式檔案到 workspace
        SOUL.md / AGENTS.md / IDENTITY.md / USER.md
        （用 file-templates.md + 嵌入 security-hardening.md 四道防線）
步驟 4  若有知識庫 → 建 knowledge/（見 knowledge-rag.md）
步驟 5  備份 openclaw.json
步驟 6  編輯 openclaw.json：
        - agents.list[] 加新 agent（id, name, workspace, agentDir,
          model, tools.allow/deny, sandbox）
        - bindings[] 加路由
        - 服務型 agent → 加 / 確認 session.dmScope: "per-channel-peer"
        - channels.<channel> 加帳號設定與 dmPolicy / allowFrom
步驟 7  驗證 config 可解析
步驟 8  channel 登入（需掃碼的 channel）
        openclaw channels login --channel <ch> --account <id>
步驟 9  重啟 gateway
        openclaw gateway restart   （先 --help 確認指令）
步驟 10 驗收（見下節）
```

---

## 4. 編輯流程（既有 agent）

對應 SKILL.md 的「編輯現有 agent」。改的是運作中的 agent，會**立即影響線上行為**。

```
步驟 1  確認目標：要改哪個 agent、改什麼
        讀出該 agent 現有的 workspace 檔與 agents.list[] / bindings[] 設定，
        先把現況給使用者看
步驟 2  備份：
        - cp openclaw.json 一份 .bak
        - 要改的 workspace 檔，各 cp 一份副本
步驟 3  提出 diff：把改前/改後攤給使用者，取得確認
步驟 4  套用改動（編輯對應檔案 / config）
步驟 5  config 類改動 → 重啟 gateway；只改 workspace 檔 → 不必重啟
        （但建議仍發測試訊息確認）
步驟 6  驗收（見下節）
```

**順手安全健檢**：對照 `security-hardening.md` 看這個 agent 四道防線有沒有缺。
既有 agent 常見缺漏：服務型沒設 `session.dmScope`、SOUL.md 沒寫「名字 ≠ 身份」、
`tools` 沒收緊。缺的補上，並在 diff 裡跟使用者說明。

**高風險改動，改前特別提醒使用者：**
- 放寬 `dmPolicy`（如 `allowlist` → `open`）：等於對更多人開放。
- 放寬 `tools.allow`：等於給 agent 更多手段。
- 改 `bindings`：可能讓訊息路由到非預期的 agent。
- 改 SOUL/AGENTS 的範圍與身份段落：直接改變安全行為。

---

## 5. 驗收

建立或編輯後都要跑：

```bash
openclaw doctor                      # 抓有風險 / 設錯的 DM policy 等
openclaw security audit              # 安全稽核
openclaw agents list --bindings      # 確認 agent 清單與路由
openclaw channels status --probe     # 確認 channel 連線
```

（每個指令先 `--help` 確認子指令與旗標存在。）

接著做一次**功能測試**：

- 從一個**授權的**識別碼發測試訊息，確認 agent 有回應。
- 問一個**範圍內**的問題 → 應正常回答。
- 問一個**範圍外**的問題 → 應依拒答模板婉拒、不臨場發揮。
- 服務型 agent：若可行，用兩個不同身份各發訊息，確認對話沒有互串（驗證
  `dmScope`）。

doctor / audit 有警告就**先處理再交付**，把結果回報使用者。

---

## 6. 回滾

出問題時：

```bash
# 還原 config
cp ~/.openclaw/openclaw.json.bak-<timestamp> ~/.openclaw/openclaw.json
openclaw gateway restart

# 還原 workspace 檔：用步驟 2 留的副本覆蓋回去

# 整個移除一個剛建立的新 agent：
#   1) 從 openclaw.json 的 agents.list[] 與 bindings[] 刪掉對應項目
#   2) 重啟 gateway
#   3) 視需要刪掉 workspace 目錄與 ~/.openclaw/agents/<agentId>/
#      （刪 agents/<id> 會一併刪掉 session 歷史，刪前向使用者確認）
```

每次任務都保留備份直到使用者確認新狀態正常。

---

## 7. 常用 CLI 速查

> 全部以 `openclaw <command> --help` 的實際輸出為準。下面是依文件整理的對照。

| 目的 | 指令（待 host 驗證） |
|---|---|
| 版本 | `openclaw --version` |
| gateway 狀態 | `openclaw status` |
| 重啟 gateway | `openclaw gateway restart` |
| 列出 agent + 路由 | `openclaw agents list --bindings` |
| 新增 agent（精靈） | `openclaw agents add <id>` |
| channel 登入 | `openclaw channels login --channel <ch> --account <id>` |
| channel 狀態 | `openclaw channels status --probe` |
| 健檢 | `openclaw doctor` |
| 安全稽核 | `openclaw security audit` |
| DM 配對核准 | `openclaw pairing approve <channel> <code>` |
| 看 session | `openclaw sessions --json` |
| 發訊息測試 | `openclaw message send --target <id> --message "…"` |

`openclaw agents add` 精靈也能用，但本 runbook 偏好「直接編輯 `openclaw.json`」，
因為對 Claude 來說可 diff、冪等、好回滾。精靈適合互動式快速建立。
