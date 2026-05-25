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
