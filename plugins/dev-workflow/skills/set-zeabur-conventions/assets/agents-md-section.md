## Zeabur 部署規範

本專案的正式部署目標為 **Zeabur**。

**核心限制**

- Zeabur **支援 Dockerfile 部署**：自動偵測專案根目錄的 `Dockerfile` 並以它建置部署。
- Zeabur **不支援 `docker-compose.yml`**：多服務線上編排改用 Zeabur 多服務專案，或把 compose 轉成 Zeabur Template YAML（官方工具：`zeabur/docker-compose-to-zeabur-template`）。

**開發原則**

- 任何要在 Zeabur 上跑的服務，都必須能單靠一份 `Dockerfile`（或 Zeabur 自動偵測的建置方式）完成部署。只有 compose 才跑得起來的服務，視為在 Zeabur 上壞掉。
- `docker-compose.yml` 可保留，定位是本地開發與測試環境，不是線上部署設定。
- 每個要部署到 Zeabur 的服務，都要有自己可獨立建置的 `Dockerfile`。
- 保持 `docker-compose.yml` 與線上設定等價：compose 裡的環境變數、port、啟動指令，要能對應到 Zeabur 服務設定或 Dockerfile。
- 新增服務或依賴前先確認它只靠 Dockerfile 在 Zeabur 上跑得起來。
- 部署文件與指令以 Dockerfile / Zeabur 服務設定為主，不用 `docker compose up` 當作部署步驟。

**每個 Dockerfile 開頭必須註解該服務在 Zeabur 上要設定的環境變數**

註解至少包含：

- **必填 vs 選填**：各附一行用途與典型值。
- **dev / prod 對應值**：兩個環境不同的值要明確寫出（例如 Supabase URL）。
- **Runtime vs Build-time**：
  - **Runtime 變數**（後端 / 長駐進程啟動時讀）在 Zeabur 設 **Variables**。改完必須在 Dashboard 對該 service 手動點「Redeploy」才生效，「Restart」不夠。
  - **Build-time 變數**（Vite 等靜態建置工具在 build 階段寫進 bundle）在 Zeabur 設 **Build-time Variables / Build Args**，改值後必須重新 build。Dockerfile 裡用 `ARG` 宣告。
- **安全邊界**：會打包進前端 bundle 的變數（例如 Vite 的 `VITE_*`）在瀏覽器端公開可見，禁止放 service_role key、後端 API token 等敏感值。

改 Dockerfile 或新增 / 移除環境變數時，同步更新這段註解。

**Zeabur 環境變數的 propagation 行為**

- 改 runtime env var 後不會自動 redeploy：到 Dashboard 對該 service 點「Redeploy」才生效。
- `${VAR}` 是 project-shared 引用：service A 設 `JWT_SECRET=xxx`，service B 的 `${JWT_SECRET}` 解析到 A 的值。改 A 的值後，所有引用該變數的 service 都要分別 Redeploy。
- PREBUILT_V2 template 把 env 渲染進配置檔（例如 Supabase Kong 把 ANON_KEY 寫進 `/home/kong/kong.yml`），並以 read-only mount 進容器。改 env 後必須走 Dashboard「Redeploy」，重啟容器不會重新渲染。
- 刪 project 重建後可能殘留 stale shared variables（例如 `POSTGRESQL_HOST` 指向已不存在的 service）。診斷：service log 連到陌生 service-XXX 且 Connection refused。處理：把該變數寫死成內部 hostname（如 `postgresql`、`auth`）。
