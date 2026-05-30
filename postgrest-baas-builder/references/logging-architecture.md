# Logging 架構：業界四層分工與最低要求

「該記什麼」這個問題比「怎麼記」更基本。新手只做 DB trigger 就以為 log 蓋滿了——其實 trigger 只蓋住「DB 層的狀態變更」，沒蓋到「誰從哪台機器打了什麼 API、結果怎樣、為什麼」。出事查不出來。

這份是業界 logging 的**四層分工** + **每層該長什麼樣** + **依專案規模哪些層必做**。技術實作細節（trigger SQL、pg_cron 排程語法）見 `logging-retention.md`。

---

## 四層分工總表

| Tier | 目的 | 抓什麼 | 寫到哪 | 不做的後果 |
|---|---|---|---|---|
| **1. DB-layer audit** | 資料表狀態變更追溯 | INSERT/UPDATE/DELETE + 整列前後 | `audit_log` (trigger) | 不知道資料怎麼被改成現在這樣 |
| **2. Application/Request audit** | 每支 API 呼叫的脈絡 | method / path / status / latency / IP / UA / actor / request_id | `request_log` (middleware) | 客訴「不是我下的單」追不到 IP；駭客掃 API 完全靜默 |
| **3. Security / SIEM** | 認證事件 + 異常告警 | 失敗登入、權限升級、off-hours 操作、批次刪除 | Supabase auth log + 告警系統 | 帳號被盜後沒人發現 |
| **4. Compliance archive** | 法規長期保存 | Tier 1+2 的子集 | 冷儲存（S3 Glacier / WORM） | 稅務／法律稽查無憑證 |

實務上 Tier 1+2 是「自己一定要建」的；Tier 3 部分有 Supabase Auth 自帶（`auth.audit_log_entries`）；Tier 4 用 cloud storage 排程匯出即可。

---

## 5W1H：每筆 log 該回答的問題

任何一筆 log 都該回答 5W1H，不然事後查不出價值：

| 維度 | 該抓什麼 | DB trigger 抓得到嗎 | Middleware 抓得到嗎 |
|---|---|---|---|
| **Who** 誰做的 | `actor_id` + **`actor_email`/name snapshot** | ✅ 走 `auth.uid()` + lookup（見 `db-integrity-checklist.md` B2） | ✅ JWT claims |
| **What** 做什麼 | action verb + entity + before/after diff | ✅ `tg_op` + `to_jsonb(old/new)` | ✅ method + path + body |
| **When** 何時 | `timestamp with tz` | ✅ `now()` | ✅ 開始/結束 |
| **Where** 從哪 | IP / user agent / region / endpoint | ❌ DB 沒這資訊 | ✅ `c.ClientIP()` + `User-Agent` header |
| **Why** 業務原因 | reason / change_reason 欄位 | ⚠️ 應用層傳進 trigger 才有 | ⚠️ 同 |
| **How** 來源管道 | source: admin/liff/cron/service-token/webhook | ❌ | ✅ 看 path prefix 或 auth 方式 |
| **Correlation** | `request_id` / `trace_id` 串多服務 | ❌ | ✅ middleware 生成並設 `X-Request-ID` |

**重點**：DB trigger 抓不到 IP/UA/path/request_id。所以 Tier 2 不能省——只靠 trigger 等於失明。

---

## Tier 2：Application/Request audit 該長什麼樣

### 資料表

```sql
create table public.request_log (
  id            bigint generated always as identity primary key,
  created_at    timestamptz not null default now(),
  request_id    text,                  -- UUID per request，跨服務串
  method        text not null,         -- GET/POST/PATCH/DELETE
  path          text not null,         -- /api/admin/orders/:id
  status        int,                   -- HTTP status code
  latency_ms    int,
  source        text not null,         -- 'liff' | 'admin' | 'service' | 'public' | 'webhook'
  actor_id      uuid,
  actor_email   text,                  -- snapshot；不靠 join auth.users
  actor_kind    text,                  -- 'user' | 'service' | 'anon'
  ip            inet,
  user_agent    text,
  error_message text,                  -- status >= 400 時填
  metadata      jsonb not null default '{}'::jsonb
);

create index request_log_created_at_idx on public.request_log (created_at);
create index request_log_actor_idx      on public.request_log (actor_id) where actor_id is not null;
create index request_log_status_idx     on public.request_log (status);
create index request_log_path_idx       on public.request_log (path);

alter table public.request_log enable row level security;

create policy "request_log_admin_read"
  on public.request_log for select
  to authenticated
  using (public.is_admin());
```

### Middleware 範例

不同框架做法差不多——進 request 時生成 request_id、`next()` 跑完後 async 寫一筆。

**Go / Gin**:

```go
func RequestLog(db *supabase.Client) gin.HandlerFunc {
  return func(c *gin.Context) {
    start := time.Now()
    reqID := uuid.NewString()
    c.Set("request_id", reqID)
    c.Header("X-Request-ID", reqID)

    c.Next()

    // 在 response 之後才知道 status / actor（auth middleware 跑過後才有）
    actorID    := c.GetString("admin_user_id")
    actorEmail := c.GetString("admin_user_email")
    actorKind  := c.GetString("admin_kind")          // 'user' / 'service' / ''
    if actorKind == "" { actorKind = "anon" }

    payload := map[string]any{
      "request_id":  reqID,
      "method":      c.Request.Method,
      "path":        c.FullPath(),                     // 路由模板，不是實值（避免 PII 寫死）
      "status":      c.Writer.Status(),
      "latency_ms":  int(time.Since(start).Milliseconds()),
      "source":      deriveSource(c.Request.URL.Path),
      "actor_id":    actorID,
      "actor_email": actorEmail,
      "actor_kind":  actorKind,
      "ip":          realClientIP(c),         // ★ 不是 c.ClientIP()！見下方「IP 與 reverse proxy」
      "user_agent":  c.Request.UserAgent(),
    }
    if c.Writer.Status() >= 400 && len(c.Errors) > 0 {
      payload["error_message"] = c.Errors.String()
    }

    // async 寫入避免 block response；失敗只 log 不 panic（best-effort）
    go func() {
      if err := db.WriteRequestLog(payload); err != nil {
        log.Printf("[request_log] write failed: %v", err)
      }
    }()
  }
}
```

**Node / Express**:

```js
import { randomUUID } from 'crypto'

export function requestLog(supabase) {
  return (req, res, next) => {
    if (req.path === '/healthz' || req.path === '/') return next()

    const start = Date.now()
    const reqID = randomUUID()
    req.requestId = reqID
    res.setHeader('X-Request-ID', reqID)

    res.on('finish', () => {
      const payload = {
        request_id: reqID,
        method: req.method,
        path: req.route?.path || req.path,            // 路由模板
        status: res.statusCode,
        latency_ms: Date.now() - start,
        source: deriveSource(req.path, req.adminKind),
        actor_id: req.adminUserId || null,
        actor_email: req.adminUserEmail || null,
        actor_kind: req.adminKind || 'anon',
        ip: realClientIP(req),                  // ★ 不是 req.ip！見下方「IP 與 reverse proxy」
        user_agent: req.get('user-agent'),
      }
      // 不 await：log 失敗不影響業務
      supabase.from('request_log').insert(payload).then(({ error }) => {
        if (error) console.error('[request_log]', error)
      })
    })

    next()
  }
}
```

**Python / FastAPI**:

```python
import uuid, time, asyncio
from fastapi import Request

async def request_log_middleware(request: Request, call_next):
    if request.url.path in ("/", "/healthz"):
        return await call_next(request)

    start = time.perf_counter()
    req_id = str(uuid.uuid4())
    request.state.request_id = req_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = req_id

    payload = {
        "request_id": req_id,
        "method": request.method,
        "path": request.scope.get("route").path if request.scope.get("route") else request.url.path,
        "status": response.status_code,
        "latency_ms": int((time.perf_counter() - start) * 1000),
        "source": derive_source(request.url.path, getattr(request.state, "admin_kind", None)),
        "actor_id": getattr(request.state, "admin_user_id", None),
        "actor_email": getattr(request.state, "admin_user_email", None),
        "actor_kind": getattr(request.state, "admin_kind", "anon"),
        "ip": real_client_ip(request),                       # ★ 不是 request.client.host！見下方
        "user_agent": request.headers.get("user-agent"),
    }
    # fire-and-forget
    asyncio.create_task(write_request_log(payload))
    return response
```

### 重要設計細節

1. **用 `c.FullPath()` 而不是 `c.Request.URL.Path`**：前者是路由模板 `/api/admin/orders/:id`，後者含實際 ID `/api/admin/orders/abc-123`。要查「這個 endpoint 多慢」用模板才能 group；要查「這個 ID 被誰動過」走 `audit_log.entity_id`。
2. **async 寫入**：log 寫入不能 block API response。go routine 寫，失敗只記 stdout、不影響業務。
3. **記 `actor_kind`**：區分 user/service/anon。service token 進來時要看得出是「cron 自動跑」還是「腳本手動跑」（後者可加 metadata 標）。
4. **failed auth 也記**：middleware 順序是 `RequestLog -> AdminAuth -> handler`。401/403 在 AdminAuth 中 abort 後，RequestLog 仍會在 `c.Next()` 後跑（Gin 的 defer 機制），所以失敗也會被記。
5. **避免記 request body**：body 可能含密碼、token、PII。要記就 redact 後再寫，或只記 schema 不記值。
6. **真實使用者 IP 不是 `c.ClientIP()`**：見下方「IP 與 reverse proxy」段。
7. **記下 reverse proxy 給的 trace id**：Cloudflare 的 `CF-Ray`、Zeabur 等平台的 request id 都可以放進 `metadata`，事後對應上游平台的 access log。

---

### IP 與 reverse proxy（容易踩坑）

幾乎所有 production 服務都坐在 reverse proxy 後面（Cloudflare、Cloudflare Tunnel、Zeabur、Fly.io、Nginx、AWS ALB…）。框架預設的 `c.ClientIP()` / `req.ip` / `request.client.host` **拿到的是上游 proxy 的 IP**，不是使用者 IP。

直接記就會發生：
- 整個 `request_log` 的 IP 都是 Cloudflare 的 173.245.x.x / 172.71.x.x（CF 邊緣節點）
- 出事完全分不出是哪個使用者
- 失敗登入告警永遠指向同一批 CF IP，做為 SIEM 訊號完全沒意義

### 各家 proxy 用的 header

| Proxy | 真實 client IP header | 額外可記欄位 |
|---|---|---|
| **Cloudflare**（包含 Tunnel）| `CF-Connecting-IP` | `CF-Ray`（trace）、`CF-IPCountry`、`CF-Connecting-IPv6` |
| **Vercel** | `X-Forwarded-For` 最左 | `X-Vercel-Id` |
| **Zeabur** | `X-Forwarded-For` 最左 | — |
| **Fly.io** | `Fly-Client-IP` | `Fly-Request-Id`、`Fly-Region` |
| **AWS ALB** | `X-Forwarded-For` 最左 | `X-Amzn-Trace-Id` |
| **Nginx 慣例** | `X-Real-IP` 或 `X-Forwarded-For` | — |

`X-Forwarded-For` 格式是 `"client, proxy1, proxy2, ..."`，**最左**才是真實 client，後面是經過的 proxy 鏈。

### 通用 fallback 順序

寫一個 helper 函式按順序找：

```
1. CF-Connecting-IP          ← Cloudflare 覆寫，不可偽造（前提：origin 只接 CF）
2. X-Forwarded-For 最左 IP    ← 通用 proxy chain 標準
3. X-Real-IP                  ← Nginx / 部分 LB
4. 框架預設 ClientIP()         ← 最後 fallback
```

**Go / Gin**:

```go
func realClientIP(c *gin.Context) string {
  if ip := strings.TrimSpace(c.GetHeader("CF-Connecting-IP")); ip != "" {
    return ip
  }
  if xff := c.GetHeader("X-Forwarded-For"); xff != "" {
    if i := strings.Index(xff, ","); i > 0 {
      return strings.TrimSpace(xff[:i])
    }
    return strings.TrimSpace(xff)
  }
  if ip := strings.TrimSpace(c.GetHeader("X-Real-IP")); ip != "" {
    return ip
  }
  return c.ClientIP()
}
```

**Node / Express**:

```js
function realClientIP(req) {
  const cf = req.get('cf-connecting-ip')
  if (cf) return cf.trim()
  const xff = req.get('x-forwarded-for')
  if (xff) return xff.split(',')[0].trim()
  const xreal = req.get('x-real-ip')
  if (xreal) return xreal.trim()
  return req.ip
}
```

**Python / FastAPI**:

```python
def real_client_ip(request: Request) -> str | None:
    cf = request.headers.get("cf-connecting-ip")
    if cf:
        return cf.strip()
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    xreal = request.headers.get("x-real-ip")
    if xreal:
        return xreal.strip()
    return request.client.host if request.client else None
```

### 安全：headers 可以偽造

`CF-Connecting-IP` / `X-Forwarded-For` 都是 HTTP header，任何人都能塞。**只有當 origin 確實只透過已知 proxy 進來時**才能信任：

- ✅ **可信**：Cloudflare Tunnel（流量只能從 CF 進來，沒辦法繞過）
- ✅ **可信**：origin 防火牆只開 CF / proxy IP 範圍
- ❌ **不可信**：origin 公開可達，使用者可以直接連 origin port → 攻擊者塞假 CF-Connecting-IP，整個 audit 就被汙染
- ⚠️ **看設定**：Zeabur / Vercel / Fly.io 預設只接平台流量，可信；自己架的 Nginx 要設好 `set_real_ip_from` 限定來源

如果 origin 不是只接 CF/proxy 流量，至少要：
- 在 reverse proxy 強制覆蓋 `X-Forwarded-For`（清掉 client 自己塞的），讓只能信任最右邊那個自己加上的 hop
- 或記下「兩個 IP」：proxy 給的 + 框架看到的，兩個對不上時當異常標記

### 把 proxy 給的 trace 也記下來

Cloudflare 的 `CF-Ray`、Vercel 的 `X-Vercel-Id`、Fly 的 `Fly-Request-Id` 都是 proxy 自己的 request id。把它放進 `request_log.metadata`，事後就能：
- 出事時拿 cf-ray 去 Cloudflare 後台撈完整 edge log（含 WAF 判斷、cache hit 等）
- 跨平台關聯：自家 request_id ↔ Cloudflare 的 ray ↔ Sentry / Datadog 的 trace id

```go
metadata := map[string]any{}
if ray := c.GetHeader("CF-Ray"); ray != "" { metadata["cf_ray"] = ray }
if cc  := c.GetHeader("CF-IPCountry"); cc != "" { metadata["cf_country"] = cc }
```

### 設計時規則

- **任何 production middleware 都要走 `realClientIP()` 而不是 `c.ClientIP()`**。
- **明確記下 origin 流量來源前提**（README / ARCHITECTURE.md）：origin 是否只接 proxy 流量？沒接好就要記「兩個 IP」做交叉驗證。
- **proxy 的 trace id（cf-ray 等）放進 metadata**，跨平台關聯。
- **Cloudflare 慣例的 country header 也記**（`CF-IPCountry`），對失敗 auth 來自哪個國家做 SIEM 訊號很有用。

---

## 保留期：依法規 + 業務情境設

90 天保留是新手預設，但**對業務憑證遠遠不夠**。常見法規最低值：

| 場景 | 最低保留期 | 依據 |
|---|---|---|
| 台灣商業會計憑證 | **5 年** | 商業會計法第 38 條 |
| 台灣稅務憑證 | **7 年**（最長查核期）| 稅捐稽徵法第 21、30 條 |
| GDPR 個資存取紀錄 | **6 年** 慣例 | GDPR Art. 30（無明文，業界共識）|
| PCI DSS（金流）| **1 年** 熱、3 個月即時 | PCI DSS Req 10.7 |
| HIPAA（醫療美國）| **6 年** | 45 CFR § 164.530(j) |
| SOC 2 | **1 年** 起跳，常見 7 年 | Trust Services Criteria CC7.3 |

### 分流保留策略（推薦）

`audit_log` 一張表內混不同性質的紀錄，用不同保留期：

```sql
select cron.schedule(
  'purge-audit-log',
  '0 3 * * *',
  $$
    -- 業務憑證類：保留 5 年（會計／稅務 / 客訴溯源）
    delete from public.audit_log
    where created_at < now() - interval '5 years'
      and entity_type in ('orders', 'order_items', 'customers', 'profiles', 'products', 'push_log');

    -- 派生資料 / 運算 cache：90 天（重算的，丟了沒差）
    delete from public.audit_log
    where created_at < now() - interval '90 days'
      and entity_type in ('customer_segments');
  $$
);
```

`request_log` 通常 **30-90 天**就夠（資安事件多在這時間內被發現），但**特定 endpoint**（如登入、金流）建議拉到 1 年。

---

## 依專案規模選擇要做哪些層

不是每個專案都要做四層。對照表：

| 規模 / 性質 | Tier 1 | Tier 2 | Tier 3 | Tier 4 | 備註 |
|---|---|---|---|---|---|
| 個人練習 / hackathon | ✅ | optional | — | — | trigger 就夠 |
| 小型本地商家 / 早期 MVP | ✅ | ✅（簡化版） | 看 Supabase auth log 即可 | ⚠️ 業務 log 保留期符合法規即可 | 我們專案落這格 |
| B2C SaaS 中小型 | ✅ | ✅ | ✅（Datadog / Sentry）| 開始考慮 | 加異常告警 |
| 上市 / 金融 / 醫療 | ✅ | ✅ | ✅（完整 SIEM）| ✅（WORM / Glacier）| 加雜湊鏈 / partition |

對小商家／早期 MVP 的**業界及格線**：
1. DB audit trigger 全覆蓋（含 actor email snapshot）
2. 業務憑證 log 保留**至少符合當地會計法規最低值**（台灣 5 年）
3. middleware 級 request log（IP / UA / endpoint / status）
4. failed auth 嘗試有紀錄

---

## 設計時規則

- **Tier 1 trigger 是底線**：所有 `public` 業務表掛 `audit_<table>` trigger（除了 audit/request log 自己、與真正高頻運算 cache）。
- **Tier 2 middleware 不能省**：DB trigger 抓不到 IP/UA/request_id；缺 Tier 2 等於失明。
- **保留期照法規分流**：業務憑證 5 年起跳；運算 cache / request log 30-90 天即可。一張 `audit_log` 表內按 `entity_type` 設不同保留期 cron。
- **failed auth 一定要記**：middleware 401/403 也走 request_log。
- **actor_email snapshot 不能省**：FK 顯示用欄位要凍住（見 `db-integrity-checklist.md` B2）。
- **async + best-effort 寫入**：log 寫入失敗不能阻斷業務。
- **`source` / `actor_kind` 欄位區分管道**：'liff' / 'admin' / 'service' / 'webhook' / 'cron'，否則出事看不出哪個入口。

---

## 不要做的事（除非真的有理由）

- **不在 log 表加 audit trigger**：log 自己會無限遞迴。
- **不在 log 表用軟刪**：log 是 append-only，沒有「軟刪 log」的概念；要刪走保留策略 cron。
- **不把 request body 整包塞進 metadata**：可能含密碼、token、卡號。先 redact。
- **不在 hot path 用同步 log 寫入**：用 async 寫；DB trigger 例外（同步是為了完整性）。
- **不用 `*` snapshot 整列到 log**：log 表只放查詢用得到的欄位，整列前後狀態交給 `audit_log.metadata` jsonb。

---

## 檢查 SQL：對齊 5W1H 看缺什麼

```sql
-- 列出所有 log/audit 類表的欄位，人工對照 5W1H
select table_name, column_name, data_type
from information_schema.columns
where table_schema = 'public'
  and (table_name like '%_log' or table_name like '%_audit' or table_name = 'audit_log')
order by table_name, ordinal_position;
```

逐表檢查：
- [ ] Who：actor_id + actor_email snapshot
- [ ] What：action / entity / metadata
- [ ] When：created_at
- [ ] Where：ip / user_agent（request_log 必有；audit_log 可選）
- [ ] How：source / actor_kind
- [ ] Correlation：request_id（request_log 必有；audit_log 想關聯到 request 也要存）

缺哪個就補哪個。
