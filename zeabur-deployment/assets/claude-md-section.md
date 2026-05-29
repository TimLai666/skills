## Zeabur 部署規範

本專案的正式部署目標為 **Zeabur**。Zeabur 的部署方式有一個關鍵限制，開發時務必遵守。

**核心限制**

- Zeabur **支援 Dockerfile 部署** — 會自動偵測專案根目錄的 `Dockerfile` 並以它建置部署。
- Zeabur **不支援 `docker-compose.yml`** — 平台不會讀取 compose 檔。多服務線上編排需改用 Zeabur 多服務專案，或把 compose 轉成 Zeabur Template YAML（官方工具：`zeabur/docker-compose-to-zeabur-template`）。

**開發原則**

- **不能把 `docker compose` 當成唯一的部署路徑。** 任何「要能在 Zeabur 上跑」的服務，都必須能單靠一份 `Dockerfile`（或 Zeabur 自動偵測的建置方式）完成部署。若某服務只有 compose 才跑得起來、沒有對應的 Dockerfile 部署路徑，那它在 Zeabur 上就是壞的。
- **但 `docker-compose.yml` 仍可保留，供本地開發與測試使用。** 一次起 app + DB + cache 做本地測試很方便，這是允許且鼓勵的。compose 的定位是「本地開發/測試環境」，**不是「線上部署設定」**。
- 每個要部署到 Zeabur 的服務，都要有自己可獨立建置的 `Dockerfile`。
- 保持 `docker-compose.yml` 與線上設定等價：compose 裡的環境變數、port、啟動指令，要能對應到 Zeabur 服務設定或 Dockerfile，避免兩邊漂移。
- 新增服務或依賴前先自問：「這個只靠 Dockerfile 在 Zeabur 上跑得起來嗎？」答案要是「可以」。
- 部署文件與指令以 Dockerfile / Zeabur 服務設定為主，不要用 `docker compose up` 當作部署步驟。

**每個 Dockerfile 開頭必須註解該服務在 Zeabur 上要設定的環境變數**

Zeabur 的環境變數是在每個 service 的 UI 個別填，沒有清單就要翻原始碼才知道要設什麼、設在哪。為了讓部署的人（包含未來的自己）一目了然，每個 Dockerfile 開頭都要有一段「Zeabur 環境變數設定」註解，內容至少包含：

- **必填 vs 選填**：哪些不設會直接壞掉、哪些可以省略，並附一行說明各自的用途與典型值。
- **dev / prod 對應值**：例如 Supabase URL 在兩個環境是不同 project，要明確寫出來，避免設錯環境。
- **Runtime vs Build-time** — 這是 Zeabur 上最容易踩的坑，務必清楚標示：
  - **Runtime 變數**（後端 / 長駐進程啟動時讀）→ 在 Zeabur 設 **Variables**。**改完一定要在 Dashboard 對該 service 手動點「Redeploy」才會生效** — Zeabur 不會因為 env 改了就自動重啟容器，光按「Restart」也不夠（特別是配置檔靠 envsubst 渲染的 PREBUILT 模板，例如 Supabase Kong）。
  - **Build-time 變數**（Vite 等靜態建置工具在 build 階段就寫死進 bundle）→ 在 Zeabur 設 **Build-time Variables / Build Args**，**改值後必須重新 build 才會生效**。Dockerfile 裡要對應地用 `ARG` 宣告。
- **安全邊界警告**：所有會被打包進前端 bundle 的變數（例如 Vite 的 `VITE_*`）在瀏覽器端公開可見，嚴禁放 service_role key、後端 API token 等敏感值。

改 Dockerfile 或新增 / 移除環境變數時，要同步更新這段註解，避免註解與實際讀取的變數漂移。

**Zeabur 環境變數的 propagation 行為**（協助多服務專案時要記住）

- **改 runtime env var 後不會自動 redeploy**：改完到 Dashboard 對該 service 點「Redeploy」才生效。
- **`${VAR}` 是 project-shared 引用**：service A 設 `JWT_SECRET=xxx`，service B 的 `${JWT_SECRET}` 會解析到 A 的值。改 A 的值後 B 不會自動 redeploy — 所有引用該變數的 service 都要分別 Redeploy。
- **PREBUILT_V2 template 把 env 渲染進配置檔**（例如 Supabase Kong 把 ANON_KEY 寫進 `/home/kong/kong.yml`），然後檔案以 read-only mount 進容器。改 env 後光重啟容器不會重新渲染檔案；必須走 Dashboard「Redeploy」。
- **刪 project 重建後可能有 stale shared variables**：舊 project 的 service ID 可能殘留在 shared pool（例如 `POSTGRESQL_HOST` 還指向已不存在的 service）。診斷：service log 顯示連到陌生 service-XXX 且 Connection refused。修法：把該變數寫死成內部 hostname（如 `postgresql`、`auth`），不要依賴 stale shared。
