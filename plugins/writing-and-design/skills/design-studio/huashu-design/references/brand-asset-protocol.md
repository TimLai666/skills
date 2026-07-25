# 核心資產協議（完整版）

> 從 GUIDE.md「核心哲學 #1.a」下沉的完整協議（2026-06 瘦身）。GUIDE.md 留了觸發條件 + 5 步標題 + 自檢；這裡是 5 步詳細操作、下載命令、brand-spec 模板、全流程失敗保底、反例與代價對比。
> 觸發：任務涉及具體品牌/產品時強制執行。回 GUIDE.md 看精簡版與上下文。

#### 1.a 核心資產協議（涉及具體品牌時強制執行）

> **這是 v1 最核心的約束，也是穩定性的生命線。** Agent 是否走通這個協議，直接決定輸出品質是 40 分還是 90 分。不要跳過任何一步。
>
> **v1.1 重構（2026-04-20）**：從「品牌資產協議」升級為「核心資產協議」。之前的版本過度聚焦色值和字型，漏掉了設計中最基礎的 logo / 產品圖 / UI 截圖。花叔的原話：「除了所謂的品牌色，顯然我們應該找到並且用上大疆的 logo，用上 pocket4 的產品圖。如果是網站或者 app 等非實體產品的話，logo 至少該是必須的。這可能是比所謂的品牌設計的 spec 更重要的基本邏輯。否則，我們在表達什麼呢？」

**觸發條件**：任務涉及具體品牌——使用者提了產品名/公司名/明確客戶（Stripe、Linear、Anthropic、Notion、Lovart、DJI、自家公司等），不論使用者是否主動提供了品牌資料。

**前置硬條件**：走協議前必須已通過「#0 事實驗證先於假設」確認品牌/產品存在且狀態已知。如果你還不確定產品是否已發布/規格/版本，先回去搜。

##### 核心理念：資產 > 規範

**品牌的本質是「它被認出來」**。認出來靠什麼？按識別度排序：

| 資產類型 | 識別度貢獻 | 必需性 |
|---|---|---|
| **Logo** | 最高 · 任何品牌出現 logo 就一眼識別 | **任何品牌都必須有** |
| **產品圖/產品渲染圖** | 極高 · 實體產品的"主角"就是產品本身 | **實體產品（硬體/包裝/消費品）必須有** |
| **UI 截圖/介面素材** | 極高 · 數位產品的"主角"是它的介面 | **數位產品（App/網站/SaaS）必須有** |
| **色值** | 中 · 輔助識別，脫離前三項時經常撞衫 | 輔助 |
| **字型** | 低 · 需配合前述才能建立識別 | 輔助 |
| **氣質關鍵詞** | 低 · agent 自檢用 | 輔助 |

**翻譯成執行規則**：
- 只抽色值 + 字型、不找 logo / 產品圖 / UI → **違反本協議**
- 用 CSS 剪影/SVG 手畫替代真實產品圖 → **違反本協議**（生成的就是「通用科技動畫」，任何品牌都長一樣）
- 找不到資產不告訴使用者、也不 AI 生成，硬做 → **違反本協議**
- 寧可停下問使用者要素材，也不要用 generic 填充

##### 5 步硬流程（每步有 fallback，絕不靜默跳過）

##### Step 1 · 問（資產清單一次問全）

不要只問「有 brand guidelines 嗎？」——太寬泛，使用者不知道該給什麼。按清單逐項問：

```
關於 <brand/product>，你手上有以下哪些資料？我按優先順序列：
1. Logo（SVG / 高畫質 PNG）—— 任何品牌必備
2. 產品圖 / 官方渲染圖 —— 實體產品必備（如 DJI Pocket 4 的產品照）
3. UI 截圖 / 介面素材 —— 數位產品必備（如 App 主要頁面截圖）
4. 色值清單（HEX / RGB / 品牌色盤）
5. 字型清單（Display / Body）
6. Brand guidelines PDF / Figma design system / 品牌官網連結

有的直接發我，沒有的我去搜/抓/生成。
```

##### Step 2 · 搜官方管道（按資產類型）

| 資產 | 搜尋路徑 |
|---|---|
| **Logo** | `<brand>.com/brand` · `<brand>.com/press` · `<brand>.com/press-kit` · `brand.<brand>.com` · 官網 header 的 inline SVG |
| **產品圖/渲染圖** | `<brand>.com/<product>` 產品詳情頁 hero image + gallery · 官方 YouTube launch film 截幀 · 官方新聞稿附圖 |
| **UI 截圖** | App Store / Google Play 產品頁截圖 · 官網 screenshots section · 產品官方演示影片截幀 |
| **色值** | 官網 inline CSS / Tailwind config / brand guidelines PDF |
| **字型** | 官網 `<link rel="stylesheet">` 引用 · Google Fonts 追蹤 · brand guidelines |

`WebSearch` 保底關鍵詞：
- Logo 找不到 → `<brand> logo download SVG`、`<brand> press kit`
- 產品圖找不到 → `<brand> <product> official renders`、`<brand> <product> product photography`
- UI 找不到 → `<brand> app screenshots`、`<brand> dashboard UI`

##### Step 3 · 下載資產 · 按類型三條保底路徑

**3.1 Logo（任何品牌必需）**

> ⚠️ **別隻試 `curl <brand>.com/logo.svg` 就放棄**——現在的官網大多是 SPA，直連靜態路徑基本返回空殼 HTML（2026-06-06 實測 Trae 官網 5 條直連路徑全是空殼）。**數位產品 / SaaS / AI 工具優先用圖示聚合源**，命中率最高、直出乾淨 SVG。

按成功率遞減：
0. **圖示聚合源（知名數位產品/SaaS/AI 工具首選，命中率最高）**：
   ```bash
   unset ALL_PROXY HTTP_PROXY HTTPS_PROXY all_proxy http_proxy https_proxy   # 清代理，否則 TLS 易炸
   # svgl —— AI/開發者品牌覆蓋最全（Claude/Cursor/OpenAI/Copilot/Anthropic/Vercel…），含 light/dark + wordmark
   curl -s "https://api.svgl.app?search=<brand>"   # 返回 JSON，取 route(.light/.dark) 的 svg URL 再下載
   # simpleicons —— 單色 glyph，可直接按品牌色上色
   curl -o logo.svg "https://cdn.simpleicons.org/<slug>/<hexcolor>"
   ```
1. 獨立 SVG/PNG 檔案 / 官方 brand 頁（如 `<brand>.com/brand`、`/press`）：
   ```bash
   curl -A "Mozilla/5.0" -L -o assets/<brand>-brand/logo.svg "<official-logo-url>"
   ```
2. 官網 HTML 全文提取 inline SVG：
   ```bash
   curl -A "Mozilla/5.0" -L https://<brand>.com -o assets/<brand>-brand/homepage.html
   # 然後 grep <svg>...</svg> 提取 logo 節點
   ```
3. **Google favicon 服務（站點真實 mark 保底，幾乎不失敗）**：
   ```bash
   curl -o logo.png "https://www.google.com/s2/favicons?domain=<brand-domain>&sz=256"   # 256px 官方站點圖示
   ```
4. 官方社交媒體 avatar（最後手段）：GitHub/Twitter/LinkedIn 的公司頭像通常是 400×400 或 800×800 透明底 PNG

下載後**逐個核對**：`file <logo>` 確認是真 SVG/PNG（不是 106 位元組佔位或 HTML 空殼），`head -c 90 <logo.svg>` 看是否 `<svg`。

**3.2 產品圖/渲染圖（實體產品必需）**

按優先順序：
1. **官方產品頁 hero image**（最高優先順序）：右鍵檢視圖片地址 / curl 獲取。解析度通常 2000px+
2. **官方 press kit**：`<brand>.com/press` 常有高畫質產品圖下載
3. **官方 launch video 截幀**：用 `yt-dlp` 下載 YouTube 影片，ffmpeg 抽幾幀高畫質圖
4. **Wikimedia Commons**：公共領域常有
5. **AI 生成保底**（nano-banana-pro）：把真實產品圖作為參考發給 AI，讓它生成符合動畫場景的變體。**不要用 CSS/SVG 手畫代替**

```bash
# 示例：下載 DJI 官網產品 hero image
curl -A "Mozilla/5.0" -L "<hero-image-url>" -o assets/<brand>-brand/product-hero.png
```

**3.3 UI 截圖（數位產品必需）**

- App Store / Google Play 的產品截圖（注意：可能是 mockup 而非真實 UI，要對比）
- 官網 screenshots section
- 產品演示影片截幀
- 產品官方 Twitter/X 的發布截圖（常是最新版本）
- 使用者有帳號時，直接截圖真實產品介面

**3.4 · 素材品質門檻「5-10-2-8」原則（鐵律）**

> **Logo 的規則不同於其他素材**。Logo 有就必須用（沒有就停下問使用者）；其他素材（產品圖/UI/參考圖/配圖）遵循「5-10-2-8」品質門檻。
>
> 2026-04-20 花叔原話：「我們的原則是搜尋 5 輪，找到 10 個素材，選擇 2 個好的。每個需要評分 8/10 以上，寧可少一些，也不為了完成任務濫竽充數。」

| 維度 | 標準 | 反模式 |
|---|---|---|
| **5 輪搜尋** | 多管道交叉搜（官網 / press kit / 官方社媒 / YouTube 截幀 / Wikimedia / 使用者帳號截圖），不是一輪抓前 2 個就停 | 第一頁結果直接用 |
| **10 個候選** | 至少湊 10 個備選才開始篩 | 只抓 2 個，沒得選 |
| **選 2 個好的** | 從 10 個裡精選 2 個作為最終素材 | 全都用 = 視覺過載 + 品味稀釋 |
| **每個 8/10 分以上** | 不夠 8 分**寧可不用**，用誠實 placeholder（灰塊+文字標籤）或 AI 生成（nano-banana-pro 以官方參考為基底）| 湊數 7 分素材進 brand-spec.md |

**8/10 評分維度**（打分時記錄在 `brand-spec.md`）：

1. **解析度** · ≥2000px（印刷/大螢幕場景 ≥3000px）
2. **版權清晰度** · 官方來源 > 公共領域 > 免費素材 > 疑似盜圖（疑似盜圖直接 0 分）
3. **與品牌氣質契合度** · 和 brand-spec.md 裡的「氣質關鍵詞」一致
4. **光線/構圖/風格一致性** · 2 個素材放一起不打架
5. **獨立敘事能力** · 能單獨表達一個敘事角色（不是裝飾）

**為什麼這個門檻是鐵律**：
- 花叔的哲學：**寧缺毋濫**。濫竽充數的素材比沒有更糟——汙染視覺品味、傳遞「不專業」訊號
- **「一個細節做到 120%，其他做到 80%」的量化版**：8 分是"其他 80%" 的底線，真正 hero 素材要 9-10 分
- 消費者看作品時，每一個視覺元素都在**積分或扣分**。7 分素材 = 扣分項，不如留空

**Logo 例外**（重申）：有就必須用，不適用「5-10-2-8」。因為 logo 不是「多選一」問題，而是「識別度根基」問題——就算 logo 本身只有 6 分，也比沒有 logo 強 10 倍。

##### Step 4 · 驗證 + 提取（不只是 grep 色值）

| 資產 | 驗證動作 |
|---|---|
| **Logo** | 檔案存在 + SVG/PNG 可開啟 + 至少兩個版本（深底/淺底用）+ 透明背景 |
| **產品圖** | 至少一張 2000px+ 解析度 + 去背或乾淨背景 + 多個角度（主視角、細節、場景） |
| **UI 截圖** | 解析度真實（1x / 2x）+ 是最新版本（不是舊版）+ 無使用者資料汙染 |
| **色值** | `grep -hoE '#[0-9A-Fa-f]{6}' assets/<brand>-brand/*.{svg,html,css} \| sort \| uniq -c \| sort -rn \| head -20`，過濾黑白灰 |

**警惕示範品牌汙染**：產品截圖裡常有使用者 demo 的品牌色（如某工具截圖演示喜茶紅），那不是該工具的色。**同時出現兩種強色時必須區分**。

**品牌多切面**：同一品牌的官網行銷色和產品 UI 色經常不同（Lovart 官網暖米+橙，產品 UI 是 Charcoal + Lime）。**兩套都是真的**——根據交付場景選合適的切面。

##### Step 5 · 固化為 `brand-spec.md` 檔案（模板必須覆蓋所有資產）

```markdown
# <Brand> · Brand Spec
> 採集日期：YYYY-MM-DD
> 資產來源：<列出下載來源>
> 資產完整度：<完整 / 部分 / 推斷>

## 🎯 核心資產（一等公民）

### Logo
- 主版本：`assets/<brand>-brand/logo.svg`
- 淺底反色版：`assets/<brand>-brand/logo-white.svg`
- 使用場景：<片頭/片尾/角落浮水印/全域>
- 停用變形：<不能拉伸/改色/加描邊>

### 產品圖（實體產品必填）
- 主視角：`assets/<brand>-brand/product-hero.png`（2000×1500）
- 細節圖：`assets/<brand>-brand/product-detail-1.png` / `product-detail-2.png`
- 場景圖：`assets/<brand>-brand/product-scene.png`
- 使用場景：<特寫/旋轉/對比>

### UI 截圖（數位產品必填）
- 主頁：`assets/<brand>-brand/ui-home.png`
- 核心功能：`assets/<brand>-brand/ui-feature-<name>.png`
- 使用場景：<產品展示/Dashboard 漸現/對比演示>

## 🎨 輔助資產

### 色板
- Primary: #XXXXXX  <來源標註>
- Background: #XXXXXX
- Ink: #XXXXXX
- Accent: #XXXXXX
- 停用色: <品牌明確不用的色系>

### 字型
- Display: <font stack>
- Body: <font stack>
- Mono（資料 HUD 用）: <font stack>

### 簽名細節
- <哪些細節是「120% 做到」的>

### 禁區
- <明確不能做的：比如 Lovart 不用藍色、Stripe 不用低飽和暖色>

### 氣質關鍵詞
- <3-5 個形容詞>
```

**寫完 spec 後的執行紀律（硬要求）**：
- 所有 HTML 必須**引用** `brand-spec.md` 裡的資產檔案路徑，不允許用 CSS 剪影/SVG 手畫代替
- Logo 作為 `<img>` 引用真實檔案，不重畫
- 產品圖作為 `<img>` 引用真實檔案，不用 CSS 剪影代替
- CSS 變數從 spec 注入：`:root { --brand-primary: ...; }`，HTML 只用 `var(--brand-*)`
- 這讓品牌一致性從「靠自覺」變成「靠結構」——想臨時加色要先改 spec

##### 全流程失敗的保底

按資產類型分別處理：

| 缺失 | 處理 |
|---|---|
| **Logo 完全找不到** | **停下問使用者**，不要硬做（logo 是品牌識別度的根基） |
| **產品圖（實體產品）找不到** | 優先 nano-banana-pro AI 生成（以官方參考圖為基底）→ 次選向使用者索取 → 最後才是誠實 placeholder（灰塊+文字標籤，明確標註"產品圖待補"） |
| **UI 截圖（數位產品）找不到** | 向使用者索取自己帳號的截圖 → 官方演示影片截幀。不用 mockup 生成器湊 |
| **色值完全找不到** | 按「設計方向顧問模式」走，向使用者推薦 3 個方向並標註 assumption |

**禁止**：找不到資產就靜默用 CSS 剪影/通用漸層硬做——這是協議最大的反 pattern。**寧可停下問，也不要湊**。

##### 反例（真實踩過的坑）

- **Kimi 動畫**：憑記憶猜「應該是橙色」，實際 Kimi 是 `#1783FF` 藍色——返工一遍
- **Lovart 設計**：把產品截圖裡演示品牌的喜茶紅當成 Lovart 自己的色——差點毀整個設計
- **DJI Pocket 4 發布動畫（2026-04-20，觸發本協議升級的真實案例）**：走了舊版只抽色值的協議，沒下載 DJI logo、沒找 Pocket 4 產品圖，用 CSS 剪影代替產品——做出來是「通用黑底+橙 accent 的科技動畫」，沒有大疆識別度。花叔原話：「否則，我們在表達什麼呢？」→ 協議升級。
- 抽完色沒寫進 brand-spec.md，第三頁就忘了主色數值，臨場加了個「接近但不是」的 hex——品牌一致性崩潰
- **五大 Coding Agent 對比 PPT（2026-06-06，觸發觸發條件擴充的真實案例）**：agent 把任務判成「PPT + 沒風格參考」走 Fallback 設計方向顧問，只抽了五家品牌色就 spawn 三套設計邏輯，**五個產品 logo（Claude Code / Cursor / Codex / Copilot / Trae）一個沒取**——被花叔抓現行「我們為什麼沒去取這些產品的 logo」。根因：把「對比 / 榜單 deck」誤判為不觸發 §1.a（以為 §1.a 只管「為單一客戶做物料」），且 Fallback 路徑裡沒有任何 logo 檢查點。→ 修復：①觸發條件擴成兩類（含「設計裡點名/並列真實產品」）②Fallback 不豁免取 logo ③Phase 3.5 加「具名產品 logo 子門」spawn 前必過 ④Step 3.1 補 svgl/simpleicons/Google favicon 可靠取圖鏈。

##### 協議代價 vs 不做代價

| 場景 | 時間 |
|---|---|
| 正確走完協議 | 下載 logo 5 min + 下載 3-5 張產品圖/UI 10 min + grep 色值 5 min + 寫 spec 10 min = **30 分鐘** |
| 不做協議的代價 | 做出沒識別度的通用動畫 → 使用者返工 1-2 小時，甚至重做 |

**這是穩定性最便宜的投資**。尤其對商單/發表會/重要客戶專案，30 分鐘的資產協議是保命錢。

