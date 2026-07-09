# 雙環境分離

目標：development 與 production 是兩套**完全獨立**的 Supabase 專案，程式碼透過環境變數決定連哪一套，且**預設 development**。連 production 永遠是需要刻意指定的例外。

## 建立兩個 Supabase 專案

在 Supabase Dashboard 開兩個專案，例如：

- `myapp-dev`（開發環境）
- `myapp-prod`（正式環境）

各自有獨立的 Project URL、anon key、service_role key、資料庫。記下兩者的 **project ref**（專案網址裡那段 ID），CLI 會用到。

本機日常開發也可以用 `supabase start` 跑本地 Docker stack 取代 dev 雲端專案——本地 stack 可隨時 `supabase db reset` 重建、不怕弄壞，最適合日常開發。`myapp-dev` 雲端專案則留給需要真實雲端環境的測試（例如 Auth callback、Edge Functions）。不論用哪種，原則一致：**開發只碰非 production 的資料庫**。

## 環境變數檔規劃

不要把 dev 跟 prod 的值塞在同一個檔案。用「同欄位名、不同檔案」的方式，程式碼永遠讀同樣的變數名，靠載入哪個檔案來切換：

| 檔案 | 內容 | 進 git？ |
|---|---|---|
| `.env.example` | 範本，欄位名 + 空值或假值 | ✅ 要 |
| `.env.development` | 真實 dev 金鑰 | ❌ 絕不 |
| `.env.production` | 真實 prod 金鑰 | ❌ 絕不 |

`.env.development` 與 `.env.production` 內欄位名相同：

```
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
```

`SUPABASE_SERVICE_ROLE_KEY` 會繞過 RLS，**只能在伺服器端使用，絕不可出現在前端 bundle 或 client 程式碼**。前端只用 anon key。

`.gitignore` 至少要包含：

```
.env
.env.*
!.env.example
supabase/.temp
supabase/.branches
```

## APP_ENV 載入器（預設 development）

用一個 `APP_ENV` 變數決定載入哪個 env 檔，**不設值時一律 development**。

### Node / JavaScript

```js
// config.js
import dotenv from 'dotenv';

const APP_ENV = process.env.APP_ENV || 'development';   // 預設 development
dotenv.config({ path: `.env.${APP_ENV}` });

if (APP_ENV === 'production') {
  console.warn('⚠️  目前連線到 PRODUCTION Supabase。');
}

export const appEnv = APP_ENV;
export const supabaseUrl = process.env.SUPABASE_URL;
export const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;
```

`package.json` scripts —— 預設指令一律 development，正式環境另開明確的 `:prod` 指令：

```json
{
  "scripts": {
    "dev": "APP_ENV=development next dev",
    "start": "APP_ENV=development next start",
    "start:prod": "APP_ENV=production next start"
  }
}
```

### Python / Streamlit

```python
# config.py
import os
from dotenv import load_dotenv

APP_ENV = os.getenv("APP_ENV", "development")   # 預設 development
load_dotenv(f".env.{APP_ENV}")

if APP_ENV == "production":
    print("⚠️  目前連線到 PRODUCTION Supabase。")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
```

啟動指令預設 development：

```bash
# 開發（預設）
streamlit run app.py
# 正式環境（必須明確指定）
APP_ENV=production streamlit run app.py
```

可在程式啟動時印出目前環境，讓人一眼看到自己連的是哪一套。

## Supabase CLI 與環境

`supabase init` 後，`supabase/config.toml` 進 git。CLI 一次只 link 一個遠端專案：

```bash
supabase link --project-ref <DEV_REF>     # 平常 link 著 dev
```

- 本機開發：`supabase start` / `supabase stop`，搭配 `supabase db reset` 隨時重建。
- 推 migration 到 dev：`supabase db push`（會推到目前 link 的專案——確認是 dev）。
- 推 migration 到 prod：屬於上線動作，流程見 `production-safety.md`，必須先取得使用者同意。

原則：CLI 平時就 link 著 dev 專案，讓「不小心 push」也只會打到 dev。要動 prod 時才刻意切過去，動完切回來。
