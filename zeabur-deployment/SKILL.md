---
name: zeabur-deployment
description: 在專案中建立並維護 Zeabur 部署規範，會在專案根目錄的 CLAUDE.md 寫入一段部署約束（Zeabur 只支援 Dockerfile、不支援 docker-compose；compose 僅供本地開發測試）。僅在使用者明確指定專案要部署到 Zeabur 時才使用 — 例如使用者明說「這個專案要部署到 Zeabur」「要上 Zeabur」「設定 Zeabur 部署」，或直接呼叫此 skill。不要在僅僅提到 Docker、寫 Dockerfile、討論部署平台、或泛泛談到 Zeabur 時觸發；必須有明確的「部署到 Zeabur」意圖。Only trigger when the user explicitly states the project deploys to Zeabur — do not infer from Docker usage or general deployment talk.
---

# Zeabur 部署規範

把一個專案的部署目標設定成 Zeabur 時，最容易踩的坑是：開發者習慣用 `docker-compose.yml` 把整套服務跑起來，理所當然地以為「compose 跑得起來 = 上線跑得起來」。在 Zeabur 上這個假設是錯的。這個 skill 的工作是把這個約束寫進專案的 `CLAUDE.md`，讓之後在這個專案裡工作的 Claude（包含未來的你自己）一開始就知道規則。

> **只在明確指定 Zeabur 部署時使用。** 這個 skill 只處理「使用者明說專案要部署到 Zeabur」的情況。單純提到 Docker、寫 Dockerfile、或泛泛討論部署平台，都不該觸發 — 不要從這些線索去推測。若不確定使用者是不是真的要用 Zeabur，先問清楚，不要先動 `CLAUDE.md`。

## 核心事實

Zeabur 是 PaaS 平台，部署機制如下：

- **支援 Dockerfile**：Zeabur 會自動偵測專案根目錄的 `Dockerfile`，並以它建置部署。
- **不支援 `docker-compose.yml`**：Zeabur 不會讀取 `docker-compose.yml`。多服務的線上編排要靠「Zeabur 多服務專案」或把 compose 轉成 **Zeabur Template YAML**（Zeabur 有官方轉換工具 `zeabur/docker-compose-to-zeabur-template`）。
- 因此：**任何「要能在 Zeabur 上跑」的服務，都必須能單靠一份 `Dockerfile`（或 Zeabur 自動偵測的建置方式）完成部署。**

但 — `docker-compose.yml` 不需要刪掉。它在「本地開發與測試」這個用途上仍然有價值（一次起 app + DB + cache 很方便），這是允許且鼓勵的。重點是把它的定位講清楚：**compose 是本地開發/測試環境，不是線上部署設定。**

## 觸發此 skill 時要做的事

### 步驟 1：找到專案根目錄的 CLAUDE.md

從目前工作目錄往上找專案根（通常有 `.git`、`package.json`、`pyproject.toml` 等標記）。目標檔案是該根目錄的 `CLAUDE.md`。若不存在就建立一個。

### 步驟 2：檢查是否已有 Zeabur 區段

讀 `CLAUDE.md`，看是否已有標題為 `## Zeabur 部署規範` 的區段。

- **沒有** → 把 `assets/claude-md-section.md` 的完整內容附加到檔案末尾（前面留一個空行）。
- **已有** → 比對內容，若與 `assets/claude-md-section.md` 不一致就更新成最新版本；一致就不動，並告知使用者已經是最新。

絕不重複插入同一個區段。

### 步驟 3：回報

簡短告訴使用者做了什麼（新增 / 更新 / 已存在），並把寫入的核心規則用一兩句話覆述，確認對方認可。

## 寫入後的長期行為

這段規範一旦進了 `CLAUDE.md`，就要在這個專案的後續開發中實際遵守，不是放著好看：

1. **新增服務或依賴時**，先自問：「這個只靠 Dockerfile 在 Zeabur 上跑得起來嗎？」答案必須是「可以」。若某服務只有 compose 才跑得起來、沒有對應的 Dockerfile 部署路徑，要主動指出這在 Zeabur 上會壞掉。
2. **不要把 `docker compose up` 當成部署指令**或部署文件的主要路徑。部署說明要以 Dockerfile / Zeabur 服務設定為主。
3. **保持 compose 與線上設定等價**：`docker-compose.yml` 裡的環境變數、port、啟動指令，要能對應到 Zeabur 服務設定或 Dockerfile，避免兩邊漂移。
4. **多服務線上編排**不要寄望 compose；建議改用 Zeabur 多服務專案，或把 compose 轉成 Zeabur Template YAML。
5. 若使用者明確要為 Zeabur 寫 Dockerfile，協助時要確保它能獨立建置（compose 之外）。
6. **每個 Dockerfile 開頭要註解該服務在 Zeabur 上需設定的環境變數**。Zeabur 的環境變數是在每個 service 的 UI 個別填，沒有清單就要翻原始碼才知道要設什麼。協助寫 / 改 Dockerfile 時都要主動補上或更新這段註解，內容包含：
   - **必填 vs 選填** + 一行用途、典型值。
   - **dev / prod 對應值**（例如 Supabase URL 兩個環境是不同 project）。
   - **Runtime vs Build-time 的明確區分**：
     - 後端 / 長駐進程是 **runtime env**（Zeabur Variables，重啟即生效）。
     - Vite 等靜態建置工具是 **build-time arg**（Zeabur Build-time Variables / Build Args，**改值後必須重新 build**），Dockerfile 裡要對應地用 `ARG` 宣告再 `ENV` 轉成 build 環境變數。
   - **安全邊界警告**：所有 Vite `VITE_*` 之類會打包進前端 bundle 的變數都公開可見，嚴禁放 service_role key、後端 API token 等敏感值。
   新增 / 移除環境變數時要同步改註解，避免與實際讀取的變數漂移。若使用者已有 Dockerfile 但缺這段註解，可主動建議補上。

## 邊界情況

- **專案已有別的 deployment 區段**：不要覆蓋，獨立加 `## Zeabur 部署規範` 區段即可。
- **使用者只是在本地用 compose 開發、還沒要部署**：仍可寫入規範，但回報時說明「compose 本地用沒問題，規範是給之後上 Zeabur 時用的」，不要讓使用者誤以為要他現在停用 compose。
- **monorepo / 多個可部署服務**：規範一樣適用 — 重點變成「每個要上 Zeabur 的服務各自要有可獨立建置的 Dockerfile」。可在回報時點出這一點。
