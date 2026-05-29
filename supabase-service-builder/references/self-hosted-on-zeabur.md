# 自架 Supabase on Zeabur

第一次接手一個 Zeabur 上的 Supabase stack（不論是自己剛建的、別人交接的、dev 還是 prod），開工前先跑這份 checklist。它把所有 Zeabur 自架 Supabase 已知的踩雷模式整理在一個地方 —— 一次性掃過比之後追怪 502 / Connection refused 省時間。

執行 checklist 前要安裝 Zeabur MCP（見 `zeabur-deployment` skill），所有檢查都用 `mcp__zeabur__*` 工具加 `curl` / `psql` 完成。

---

## 與 Supabase Cloud 的關鍵差異

| 面向 | Cloud | 自架（Zeabur） |
|---|---|---|
| Auth 簽章 | JWKS 非對稱（ES256 / RS256） | HS256 對稱 + 共享 `JWT_SECRET` |
| 後端驗章 | `keyfunc` 抓 `/auth/v1/.well-known/jwks.json` | 用 `SUPABASE_JWT_SECRET` env var 對稱驗 |
| ANON / SERVICE_ROLE | Dashboard 自動發、可輪換 | 自己用 JWT_SECRET 簽的固定 JWT |
| Secret rotation | Dashboard 一鍵 | 手動：產新 secret → 重簽兩把 JWT → 改 stack 所有服務 env → cascade redeploy |
| Migration 管理 | `mcp__supabase__list_migrations` / `apply_migration` | 沒這工具，要 `psql -f` 或 `supabase db push --db-url` |
| Advisors | `mcp__supabase__get_advisors` | 沒這工具，要自己寫 SQL 查 pg_stat_* |
| Logs | `mcp__supabase__get_logs` | 用 `mcp__zeabur__get-runtime-logs` 對單一 service 看 |
| Storage | 託管 | 自架 = `storage-api` + `minio`（S3 後端）|
| Branching (preview DB) | Cloud Pro 功能 | 沒有；要自己再開一個 stack |
| 自動備份 / PITR | 有 | 自己做 `pg_dump` cron |

---

## 第一次接手 checklist

### A. 確認你連的是「你以為的那個 stack」

最常見的錯：dev / prod 分兩個 Zeabur project，操作時連錯邊。

**步驟**：
1. `mcp__zeabur__list-projects` → 確認當前要動的 project name + ID 對得上專案文件
2. `mcp__zeabur__list-services projectId=<id>` → 12 個 Supabase 服務都在嗎？全 RUNNING 嗎？
3. 比對 Kong 的對外 domain（`mcp__zeabur__get-service` for kong service）跟專案 `.env` / CLAUDE.md 寫的 `SUPABASE_URL` 是否一致
4. 看 backend / dashboard 的 Zeabur env vars，確認他們的 `SUPABASE_URL` 也指到正確 project 的 Kong domain
5. 如果有 dev/prod 兩套，務必 cross-check：dev backend → dev Kong，prod backend → prod Kong，**不能交叉**

---

### B. JWT / 密碼是不是 demo 預設值（重大安全問題）

Supabase 官方範例 docker-compose 用一組**公開**的 demo key 跟 secret，全網路 Google 一搜就有。Zeabur Supabase PREBUILT_V2 template 直接套用這組，初次部署就是 demo 狀態。

**判斷**：
```bash
# 看 Kong service 的 env vars（mcp__zeabur__get-service-variables）
# 是 demo 的特徵：
JWT_SECRET == "your-super-secret-jwt-token-with-at-least-32-characters-long"

# ANON_KEY / SERVICE_ROLE_KEY 解 base64 第二段（payload）:
# 是 demo 的特徵: iss == "supabase-demo"
echo "$ANON_KEY" | cut -d. -f2 | base64 -d
# {"role":"anon","iss":"supabase-demo","iat":1641769200,"exp":1799535600}
                              ^^^^^^^^^^^^^^

# kong.yml 內 grep:
mcp__zeabur__execute-command kong-service "sh -c 'grep -c supabase-demo /home/kong/kong.yml'"
# > 0 表示 demo 還寫死在 kong.yml
```

**端對端驗證**：
```bash
# 用 demo service_role key 打 PostgREST
curl https://<kong-domain>/rest/v1/ \
  -H "apikey: <demo_service_role>" \
  -H "Authorization: Bearer <demo_service_role>"
# 回 200 → demo 真的還能用 → 任何人都能洗你 DB
# 回 401 → demo 已失效，安全
```

**如果是 demo，要全套換掉**（流程見後面「JWT/keys 替換 SOP」）。

dev 環境如果接受暫時用 demo（短期 PoC），**也至少把 Kong 對外 domain 拆掉**，走 internal-only，否則公開可洗。

---

### C. 掃 stale shared variables（避免錯連其他 project 的關鍵）

Zeabur 的 `${VAR}` 是 **project-level shared variable pool**。**刪掉一個 project 後在另一個 project 重建 Supabase**，shared variable pool 可能殘留**舊 project 的 service ID** —— 例如 `POSTGRESQL_HOST` 還指向上一個已不存在的 service。

**症狀**：service runtime log 顯示 `Connection refused` 連 `service-XXX:port`，但 X 不在當前 `list-services` 結果裡。

**掃查步驟**：

1. 拿到「真實 service ID 集合」：
   ```bash
   mcp__zeabur__list-services projectId=<id>
   # 記下每個 service 的 _id（例如 service-6a19b8d85a225abf61ee13cc）
   ```

2. 對每個 Supabase 服務跑 `get-service-variables`，**抓出所有 `*_HOST` 變數**：
   ```
   POSTGRESQL_HOST=service-XXXXX
   AUTH_HOST=service-YYYYY
   ...
   ```

3. 任何 `XXX_HOST` value 不在「真實 service ID 集合」裡 → **stale**。

4. 找出有哪些 env var 引用了這些 stale vars（典型嫌疑犯：`PGRST_DB_URI`、`DATABASE_URL`、`GOTRUE_DB_DATABASE_URL`、`SUPABASE_DB_URL` 等）。

5. 修法（從穩到不穩排序）：
   - **(最穩)** 改成 `${XXX_DEV_HOST}` / `${XXX_PROD_HOST}`（Zeabur 給新 service 自動生的版本，有 `-DEV` 後綴；對應 service 改名後自動更新）
   - 寫死正確的 service ID `service-6a19...` —— 用 ID 解析最直接
   - **(不建議)** 用內部 hostname（`postgresql`、`auth`）—— DNS 也可能 stale（見下節）

---

### D. DNS stale entry 檢查（比 shared variables 更深的雷）

更慘的情況：即使 shared var 對了，**Zeabur 內部 DNS 的 hostname 也可能有 stale entry**。具體案例：hostname `postgresql` 的 **IPv6 entry 解析正確**（指向新 service），**IPv4 entry 卻指向已刪 project 的舊 service 的 pod IP**。

**症狀**：service 連 `postgresql:5432` 拿到 `10.x.x.x` (IPv4) 結果 Connection refused；其他服務（用 IPv6）卻 OK。PostgREST 預設 prefer IPv4 是最容易踩中的服務之一。

**驗證**：
```bash
mcp__zeabur__execute-command <some-service> "sh -c '
  echo === IPv6 ===; getent hosts postgresql
  echo === IPv4 ===; getent ahostsv4 postgresql
  echo === reachability ===; nc -zv -w 3 postgresql 5432
'"
```

**判斷**：
- IPv6 (`a2b:...`) + IPv4 (`10.x.x.x`) 都指向有效 service？OK
- IPv4 connection refused 但 service-id-based 連得通？stale DNS

**修法**：用 `${XXX_DEV_HOST}`（會解析成 `service-6a19...`，走 service-ID-based 而不是 hostname），繞過 DNS stale。**hostname 寫死的服務最危險**，因為看起來像正解但其實踩雷。

對於 Supabase PREBUILT_V2 template 預設用 hostname 寫死的服務（`auth`、`storage`、`rest`、`postgresql` 等），如果 stack 是「重建」過的，全部要 audit 一次。

**Kong 特別注意**：Supabase template 的 Kong 預設 `KONG_DNS_ORDER=LAST,A,CNAME`，**只查 IPv4 不查 IPv6**。一旦 Zeabur 內部 DNS 的 IPv4 entry 是 stale，Kong 對所有 upstream（`http://auth:9999`、`http://rest:3000` 之類）的路由全部會 fail，症狀是 `/rest/v1/` 等對外端點 502 「invalid response from upstream」。

修法：改 `KONG_DNS_ORDER=LAST,AAAA,A,CNAME`（優先 IPv6、後備 IPv4），然後 Redeploy kong。這繞過 stale IPv4 走 IPv6 解析（多數情況 IPv6 是新的、對的）。

這個修法**不能改 kong.yml**（read-only mount）所以無法把 hostname 換成 service-ID；只能靠 DNS order 改用 IPv6。如果 IPv6 也 stale 就要 fork template 自 build image，把 kong.yml 內所有 `http://service-name:port` 改成 service-id（這時就是「不可避免要走 zeabur-deployment skill 的路線 B」）。

---

### E. Postgres health

```bash
# 在 postgresql service 容器內跑（容器沒裝 less，要關 pager）
mcp__zeabur__execute-command postgresql-service "sh -c '
  PAGER=cat psql -U supabase_admin -d postgres -P pager=off -tAc \"select version();\"
  PAGER=cat psql -U supabase_admin -d postgres -P pager=off -tAc \"select count(*) from pg_tables where schemaname=\$\$public\$\$;\"
  PAGER=cat psql -U supabase_admin -d postgres -P pager=off -tAc \"select string_agg(extname, \$\$, \$\$) from pg_extension;\"
  PAGER=cat psql -U supabase_admin -d postgres -P pager=off -tAc \"show shared_preload_libraries;\"
'"
```

**檢查**：
- Postgres 主版本：自架可能 15.x，Cloud 通常 17.x。**確認 migration 沒用 16+ 特有功能**（罕見，但 jsonb 17 新方法、SQL/JSON 標準語法等要避開）
- Extensions：`pg_cron`、`pgjwt`、`uuid-ossp`、`pgcrypto`、`pg_net`、`pg_stat_statements`、`supabase_vault` 至少要在
- `shared_preload_libraries` 內含 `pg_cron`（沒有的話 `CREATE EXTENSION pg_cron` 會 fail）

**如果 migration 用 `cron.schedule(...)` 但 pg_cron 沒裝 / 沒 preload**，套 migration 會炸。要嘛在 Zeabur Postgres 容器內啟用，要嘛把 cron job 改用 backend goroutine ticker 或外部 cron 打 API。

---

### F. 對外網域 / 內部隔離

```bash
mcp__zeabur__get-service kong-service-id
# 看 .domains，確認 public domain 是不是預期的（自動生成 *.zeabur.app 或自訂網域）
```

**dev**：可考慮**完全不對外**（拔 Kong public domain），backend 走 internal hostname `http://kong-dev:8000`。Dashboard 沒法用、但內部測試夠。

**prod**：Kong 必須對外（dashboard / 顧客 SPA 要連），但設 `ip-restriction` plugin 限定來源（backend container 內 IP / Cloudflare CIDR），不要裸開。

```bash
# 看 KONG_PLUGINS 是否含 ip-restriction
mcp__zeabur__get-service-variables kong-service-id
# 找 KONG_PLUGINS
```

`KONG_PLUGINS` 預設通常已含 `ip-restriction`，但 kong.yml 內的 service 沒套 plugin 也沒用。要在 kong.yml 裡實際綁定 plugin 到 routes —— 但 kong.yml 是 read-only mount，要 fork template 自己 build image 才能改（見 zeabur-deployment skill）。

---

### G. dev / prod 金鑰隔離

最後：確認 dev 跟 prod 的 secret 是**完全獨立**的兩組。

- `JWT_SECRET` dev / prod 不可共用（共用會讓 dev 的 service_role token 在 prod 也能解，等於 dev 漏 = prod 漏）
- ANON_KEY / SERVICE_ROLE_KEY 各自獨立簽（不同 secret 簽出來自然不同）
- Studio dashboard password 各自獨立
- Postgres password 各自獨立
- 上 prod 時要產一組**全新**的 secret + 重簽 keys，**不要從 dev 抄過去**

---

## JWT / keys 替換 SOP（從 demo 換到 production-safe）

第一次接手後發現是 demo 預設值（多半是），按這個流程換：

### 1. 產新 secret + 重簽兩把 JWT

```bash
SECRET=$(openssl rand -base64 48 | tr -d '\n=' | tr '+/' '-_')
b64() { openssl base64 -e -A | tr '+/' '-_' | tr -d '='; }
sign_jwt() {
  local payload="$1"
  local h=$(printf '%s' '{"alg":"HS256","typ":"JWT"}' | b64)
  local p=$(printf '%s' "$payload" | b64)
  local s=$(printf '%s' "$h.$p" | openssl dgst -sha256 -hmac "$SECRET" -binary | b64)
  printf '%s.%s.%s\n' "$h" "$p" "$s"
}
NOW=$(date +%s)
EXP=$((NOW + 60*60*24*365*10))  # 10 年
ANON=$(sign_jwt "{\"iss\":\"supabase\",\"role\":\"anon\",\"iat\":$NOW,\"exp\":$EXP}")
SVC=$(sign_jwt "{\"iss\":\"supabase\",\"role\":\"service_role\",\"iat\":$NOW,\"exp\":$EXP}")
STUDIO_PW=$(openssl rand -base64 24 | tr -d '\n=' | tr '+/' '-_')

echo "JWT_SECRET=$SECRET"
echo "ANON_KEY=$ANON"
echo "SERVICE_ROLE_KEY=$SVC"
echo "DASHBOARD_PASSWORD=$STUDIO_PW"
```

### 2. 更新 Kong service 的 raw env vars（用 Zeabur MCP）

```
mcp__zeabur__update-environment-variable kong JWT_SECRET <新值>
mcp__zeabur__update-environment-variable kong ANON_KEY <新 anon JWT>
mcp__zeabur__update-environment-variable kong SERVICE_ROLE_KEY <新 svc JWT>
mcp__zeabur__update-environment-variable kong PASSWORD <新 Studio pw>
```

這四個是 raw value、是 source of truth。其他服務透過 `${JWT_SECRET}` / `${ANON_KEY}` / `${SERVICE_ROLE_KEY}` 引用，會自動讀新值（但要 redeploy 才生效）。

### 3. cascade Redeploy

**叫使用者去 Zeabur Dashboard** 對下列服務逐個按 Redeploy（Zeabur 不 cascade）：

| Service | 為什麼 |
|---|---|
| **kong** | kong.yml 重新 envsubst（demo keys → 新 keys、密碼） |
| **auth** | GOTRUE_JWT_SECRET 讀新值 |
| **rest** | PGRST_JWT_SECRET |
| **storage** | PGRST_JWT_SECRET |
| **realtime** | API_JWT_SECRET |
| **functions** | SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY |
| **studio** | AUTH_JWT_SECRET / SUPABASE_ANON_KEY / SUPABASE_SERVICE_KEY |
| **supavisor** | API_JWT_SECRET / METRICS_JWT_SECRET |

不用 redeploy：`postgresql`、`minio`、`imgproxy`、`meta`（沒讀 JWT_SECRET）。

### 4. 驗證

```bash
# kong.yml 應該渲染新值
mcp__zeabur__execute-command kong "sh -c '
  grep -c supabase-demo /home/kong/kong.yml   # should be 0
  grep -c <新 anon 的特徵字串> /home/kong/kong.yml  # should be 1
'"

# 用新 service_role 打 PostgREST -> 200
curl https://<kong-domain>/rest/v1/ -H "apikey: <新 svc>" -H "Authorization: Bearer <新 svc>"

# 用 demo service_role -> 401
curl https://<kong-domain>/rest/v1/ -H "apikey: <demo svc>" -H "Authorization: Bearer <demo svc>"
```

---

## 常見故障 → 排查方法

| 症狀 | 根因候選 | 排查 |
|---|---|---|
| `/rest/v1/` 502 「invalid response from upstream」 | rest-dev 連不到 Postgres | 看 rest log → 通常是 stale shared var 或 stale DNS（C/D 節） |
| `/rest/v1/` 401 但用對的 key | (1) Kong 沒 redeploy、kong.yml 還是 demo keyauth；(2) JWT_SECRET 換了但 rest 沒 redeploy → PostgREST 用舊 secret 驗章 fail | 確認 kong.yml 內 keyauth 跟 rest-dev 的 PGRST_JWT_SECRET 都已更新 |
| dashboard 登入 success 但呼叫 backend 403 | backend 用 JWKS 驗章但自架是 HS256 | 改 backend client.go：`jwt.WithValidMethods(["HS256"])` + secret 從 env 讀 |
| 同 stack 部分服務正常、PostgREST/Storage 連不上 | IPv6 hostname OK 但 IPv4 stale（D 節） | `getent ahostsv4 <hostname>` 確認；改用 `${XXX_DEV_HOST}` |
| **所有 Kong 對外端點 502**「invalid response from upstream」但其他服務內部直連 OK | Kong `KONG_DNS_ORDER=LAST,A,CNAME` 預設只查 IPv4，碰到 stale IPv4 entry 全部 fail | 改 `KONG_DNS_ORDER=LAST,AAAA,A,CNAME` 後 Redeploy kong；不行就 fork template 改 kong.yml 用 service-id |
| 改了 env var 但服務行為沒變 | Zeabur 不會自動 redeploy | 叫使用者在 Dashboard 點 Redeploy |
| Kong.yml 怎麼編輯都不生效 | read-only bind mount，envsubst 在 deploy 時做 | 改 env var 後在 Dashboard 點 kong service Redeploy |
| 改了 kong service 的 ANON_KEY，functions/studio 容器內讀到還是舊的 | `${ANON_KEY}` reference 只在「該服務 redeploy 時」解析 | redeploy functions、studio 才會吃新值 |

---

## 收尾 checklist

第一次接手做完上述後，至少能回答以下問題：

- [ ] 當前 Zeabur project name + ID 是？跟專案文件對得上嗎？
- [ ] 12 個 Supabase 服務是否都在當前 project 之下、全 RUNNING？
- [ ] Kong public domain 是？跟 `.env` 的 `SUPABASE_URL` 一致嗎？
- [ ] JWT_SECRET 不是 `your-super-secret-jwt-token-with-at-least-32-characters-long`？
- [ ] ANON_KEY / SERVICE_ROLE_KEY payload 的 `iss` 不是 `supabase-demo`？
- [ ] Studio dashboard password 不是 stack 預設 random（換成 password manager 產的）？
- [ ] 用 demo service_role 打 `/rest/v1/` 回 401（demo 已失效）？
- [ ] 所有 `*_HOST` shared var 都指向當前 project 的真實 service？沒有 stale？
- [ ] 所有用到的內部 hostname（`postgresql`、`auth`、`storage`、`rest`…）都 IPv4 + IPv6 都解析到當前 project 的 service？
- [ ] Postgres 主版本 + extensions 符合 migration 假設？
- [ ] dev / prod 的 JWT_SECRET 是兩組完全不同的值（如果有雙環境）？
- [ ] backend 的驗章程式碼是 HS256 + `SUPABASE_JWT_SECRET`，不是 JWKS？
- [ ] Kong public domain 對外政策符合預期（dev 可內部、prod 必設 IP 白名單或 Cloudflare 前置）？

跑完這份 checklist 並把結果整理給使用者，再開始實際工作。
