# v5 · "Markdown is the new typewriter."

> Director's Notes for the **huashu-md-html v2.0** launch film
> 30 seconds · 1920×1080 · 25 fps · no voiceover
> Director: huashu-design (acting as Apple-tier launch film director)
> Composer: TBD (target: Max Richter / Ólafur Arnalds / Jóhann Jóhannsson minimal-cinematic register)
> Color base: ivory white #FAFAF6 · ink #1A1A1A · terracotta #C2410C
> Type: Newsreader (display + body) · JetBrains Mono (interface) · Noto Serif SC (中文)

---

## 目錄

- [Part I · Director's Statement](#part-i--directors-statement)
- [Part II · Visual System](#part-ii--visual-system)
- [Part III · Story Arc](#part-iii--story-arc)
- [Part IV · Shot-by-Shot Storyboard](#part-iv--shot-by-shot-storyboard)
- [Part V · Production Manifest](#part-v--production-manifest)

---

# Part I · Director's Statement

## 1.1 這不是一支「功能介紹片」

絕大多數 SaaS 升級影片都犯同一個錯——把鏡頭當成 PPT。開啟 → 6 個功能滑過 → logo + slogan → 結束。每一秒都在「展示」，沒有一秒在「講」。觀眾離開時記住的不是產品，而是「又一個看著像 AI 做的頁面」。

**這支片不要做這個**。

我們要講一個故事。故事只有一行：

> **「md 是原始碼，萬物是產物。」**

這不是 slogan，是世界觀。Markdown 不是「一種輕量級文件格式」——它是寫作的源頭。一切下游的形式（html、docx、pdf、epub）都是從這同一個源頭派生出的產物。huashu-md-html v2.0 把這條產物鏈從 4 條延長到 6 條——但延長的不是「功能列表」，是**源頭的影響力半徑**。

如果觀眾看完這支片只記住一件事，我希望那件事是：「原來 md 才是原始碼」。功能列表能記多少都是 bonus。

## 1.2 視覺語言的語境對話

每一部好的宣傳片都在跟一組前作對話。我希望這支片對話的語境是：

**Apple — "Designed by Apple in California" (2013)**

那支片子是我心目中科技公司宣傳片的天花板。導演 Mark Romanek 做對了三件事：
1. **純白底 + 襯線字型**——告訴觀眾這是一支「關於設計的設計」，不是 demo
2. **慢拍**——每一句話的字幕都比觀眾閱讀速度慢半拍，強迫觀眾停留
3. **Jony Ive 的旁白幾乎像耳語**——不是兜售，是分享

我們這支片**沒有 voiceover**，所以前兩個原則要被 typography 和 timing 強化到 200%。

**Apple Silicon Launch Films (M1 / M2 / M3, 2020-2024)**

這一系列短片教會我**typography 也能跳舞**。"M1" 三個字元可以從消失、到出現、到放大、到旋轉、到爆炸成塵埃、再到重組——觀眾看著一個 logo 在 30 秒裡成為一支舞劇的主角。

**這支片的 hero 不是產品 UI，是 `md.` 這兩個字元 + 一個橙色句點**。它要在 30 秒裡成為舞劇主角。

**Anthropic 品牌語言（2024-2026）**

Anthropic 把「赤陶橙 + 襯線 + 幾何抽象」做成了 AI 公司的反 slop 樣板。它告訴行業：你可以是科技公司，但你也可以看起來像 Penguin Classics 出版的一本哲學小書。

我們繼承這套色彩。但要做得**更克制**——Anthropic 偶爾用純赤陶橙作大色塊；我們的赤陶橙永遠只作 accent（佔總畫面 < 8% 面積），剩下 92% 留給象牙白和墨黑。

**Penguin Classics（1947 起，Romek Marber 1961 grid 之後）**

Penguin 教會我**typography 的勇敢**。一本書的封面可以是大字級襯線 + 一條黑橫線 + 沒有插圖——讀者反而會停下來。

第 25-29 秒的 slogan reveal 借這個語言：**ONE SOURCE.** 和 **SIX FORMS.** 不是「裝飾文字」，它們就是畫面本身。

**Pentagram (Paula Scher / Michael Bierut)**

Pentagram 的招牌是**資訊建築**——文字和文字之間的距離、文字和邊界的距離、文字層級之間的字級比，都不是「憑直覺」，是數學。

我們的網格系統（Part II.3）來自這一傳統。

**Kenya Hara《白》(2008)**

Hara 寫過：「白不是顏色，是一種感受性。」（白は色彩ではなく、感受性なのだ）

這支片的真正主角不是 `md.`，是包圍它的**那片象牙白**。每一個 shot 都要留出至少 60% 的負空間。負空間不是「還沒填滿」，是內容本身。

**Massimo Vignelli — Modernism in design**

Vignelli 的 8 字格言：「If you can design one thing, you can design everything.」（能設計好一件東西，你就能設計好一切）

我們的設計系統不允許「這一鏡臨時加一種字型」「這一鏡臨時加一個圓角值」。所有 12 個 shots 共享同一套 5 個色值、3 種字型、4 個 easing curves。

## 1.3 觀眾畫像

三類觀眾，按重要性排：

**主受眾 A · 已使用 v1 的 huashu-md-html 老使用者（約佔 60% 流量）**

他們開啟片子是為了知道「升級了啥」。我們對他們的承諾：30 秒之內，你必須明確知道——
- 新增能力 5：md → 出版級 PDF
- 新增能力 6：md → 標準 EPUB
- 這兩個能力的視覺品質比想像中更高（不是「我用 wkhtmltopdf 也能搞」級別）

→ Shot 08 和 Shot 09 各 3 秒，必須有「★ NEW」標籤 + destination card 上必須能看到「印廠裁切標記」「Apple Books frame」這類**看得見的專業級細節**——讓老使用者秒懂「這不是湊數功能，是正經做了的」。

**次受眾 B · 聽說過 huashu-md-html 但沒用的 AI Native 創作者（約 25%）**

他們關心的是「這個 skill 跟我有什麼關係」。我們對他們的承諾：30 秒之內，你必須意識到——
- 你寫文章 / 做調查 / 做白皮書時，**md 應該是你的 source of truth**
- 6 種下遊格式，一次命令解決

→ Shot 04（any → md）要讓他們看到 PDF/DOCX/PPTX/XLSX/HTML 一起被 md 吸收——這是「源頭思維」的視覺具象化。

**外受眾 C · 完全不熟悉的設計師 / 編輯 / 出版人（約 15%）**

他們看到的是一支「漂亮的科技短片」，不一定 follow up。我們對他們的承諾：30 秒之內，你必須留下印象——
- 這家做的東西**有出版社品味**
- 跟你過去看到的 AI 工具不一樣

→ 整支片的反 AI slop 自檢（Part II.7）就是為他們做的。任何紫漸層、emoji 圖示、SVG 手畫人物——一律不出現。

## 1.4 節奏哲學

蘋果宣傳片的節奏不是勻速的。它是**慢拍 — 加速 — 頂峰 — 緩收**的曲線（詳見 Part III 情緒曲線圖）。

具體到這支片：

- **0-3s 慢拍**：觀眾進入。typography 一個字元一個字元地呼吸。
- **3-6s 第一加速**：md 字元誕生，6 個檔案 cards 魚貫飛入。
- **6-22s 第二加速段**：6 個 capability 一氣呵成，每個 3 秒不鬆手。
- **22-26s 頂峰**：slogan 雙行 reveal，所有 chrome 同步律動。
- **26-30s 緩收**：capability map 慢慢淡入，最後一秒留給品牌印章 + 極弱的 piano 殘響。

**關鍵決策**：第 22 秒是這支片的高潮點（不是第 29 秒）。29 秒是 resolution，22 秒是 climax。這兩個不要混。

## 1.5 這支片**不**做的事（反 AI slop 自檢）

按重要性排：

| 不做 | 原因 |
|------|------|
| 不用紫漸層 | 訓練語料裡「科技感」的萬能公式，2026 年看是 cyber slop |
| 不用 emoji 作圖示 | 「不專業就用 emoji 湊」的病 |
| 不畫 SVG 人物 / 手 / 抽象人形 | AI 畫的 SVG 人物永遠五官錯位、比例詭異 |
| 不用 Inter/Roboto/Arial 作 display | 太常見，撞 system fonts |
| 不用賽博霓虹 / 深藍底 #0D1117 | GitHub dark mode 美學的爛大街複製 |
| 不堆 effects（blur/glow/particle）| 一個 effect 出現兩次就是裝飾，三次就是 slop |
| 不用 Lorem ipsum | 每一段假文都用真正能讀的內容（含「md is the source. Anything else is product.」這種 hook） |
| 不用 stock photo | 整支片不出現任何真實照片（it's about typography, not lifestyle） |
| 不畫進度條 + 時間碼 + 版權署名條 | 這些是 player chrome，不是 content chrome——會和外部播放器撞 |
| 不讓 md 字元在每個 scene 都長得一樣 | 它要在 12 鏡裡有 12 種狀態，但保持同一個核心字形 |

## 1.6 一句話定位

> **"Markdown is the new typewriter."**
>
> A 30-second film about source-of-truth thinking, made for designers who write and writers who design.

---

# Part II · Visual System

## 2.1 完整色板

不是 3 色，是 10 色。每一色都有**功能定義**（不是「好看就用」）。

```
名稱            HEX        作用                           佔畫面比例上限
─────────────────────────────────────────────────────────────────────
Ivory paper    #FAFAF6    主底色（象牙白，一抹溫度）         60-70%
Mist           #F2EDE4    次級背景層（card 陰影下的微暗）    < 15%
Mica           #E6E1D6    細線 / 分隔符 / 卡片邊框          < 5%
Smoke          #6B6B6B    次級文字 / metadata             < 5%
Cinder         #3D3530    次級深色（深褐黑，不是純黑）       < 10%
Ink            #1A1A1A    主黑 / 主文字                    20-25%
Charred        #2A2620    極深褐黑（封面卡專用）            < 5%
Terracotta     #C2410C    主 accent（Anthropic 調）         5-8%
Terra Hot      #E55D21    高光 variant（僅 NEW 標籤亮起一瞬）< 1%
Terra Deep     #8B2D08    陰影 variant（赤陶橙投影）         < 1%
```

**鐵律**：
- 任何一鏡不出現以上 10 色之外的顏色。**沒有「這一鏡臨時加點冷灰」**。
- 赤陶橙系（Terracotta + variants）三色合計佔畫面 < 10%，否則視覺過載。
- 任何文字只能用 4 色之一：Ink / Cinder / Smoke / Terracotta。

## 2.2 字體系統

```
字級層級        字型                  weight    用途                       字距 (em)
────────────────────────────────────────────────────────────────────────────────────
Display XXL    Newsreader            700       slogan 頂字（200px）         -0.035
Display XL     Newsreader            700       capability number（48px）   -0.020
Display L      Newsreader            600       hero md 字元（300-480px）   -0.040
Display M      Newsreader            600       chapter title (32-44px)     -0.015
Body L         Newsreader            400       essay 正文 (18-22px)         0
Body M (zh)    Noto Serif SC         500       中文 sub-line (20-26px)     +0.04
Italic         Newsreader italic     400       引語、副標                   +0.01
Mono S         JetBrains Mono        500       標籤 / capability counter   +0.18
Mono XS        JetBrains Mono        700       NEW / version chip (11-14px) +0.22
Caret          (block 3px wide)      —         typing cursor               —
```

**字型載入策略**：
- Google Fonts 預連線 `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`
- 單一 `<link>` 請求合併所有 weights，減少 round-trip
- 錄製 MP4 前必須 `document.fonts.ready` 完成才開始計時（Stage 已實現）

## 2.3 網格系統

**主畫布**：1920 × 1080

**外邊距（safe zone）**：80px 上下左右

**主內容區**：1760 × 920

**12-column grid**：column-width = 132px，gutter = 16px

**Baseline grid**：8px 基礎律。所有 vertical position 必須是 8 的倍數（除非有特殊視覺理由）。

**黃金分割錨點**：
- 上 1/3 線：y = 360
- 下 1/3 線：y = 720
- 中線：y = 540（hero md 預設 anchor）
- 黃金分割上：y = 412
- 黃金分割下：y = 668

**關鍵安全區**：
- 頂部 60px 內：chrome 元素區（capability counter, version chip）
- 底部 60px 內：watermark / metadata 區
- 中央 800×600 區域：主內容禁區（每一鏡的 hero 元素必須落在此區域內）

## 2.4 動畫系統

**Easing 庫**（共 4 條，停用其他）：

```
名稱           曲線公式                            用途
──────────────────────────────────────────────────────────────────
expoOut       1 - 2^(-10t)                       預設 ease（90% 的入場用這個）
overshoot     cubic-bezier(0.34, 1.56, 0.64, 1)  NEW 標籤彈出 / 按鈕浮現
linear        t                                   底色 fade / paper texture 移動
expoIn        2^(10(t-1))                        退場 ease（10% 的出場用這個）
```

**Duration 字典**：

```
事件類型                  持續時間      備註
────────────────────────────────────────────────────────
字元 stagger              30-50ms       打字效果 / slogan 字元依次出現
小元素入場                300ms         file card / pill / chip
中元素入場                500ms         destination card / capability number
hero 元素入場             700-900ms     md 字元 morph
slogan 字元入場           800ms         "ONE SOURCE." 整體
scene 之間過渡            300ms 重疊    cross-dissolve + scale
退場                      200-300ms     出場永遠快於入場
```

**Stagger 法則**：
- 多元素同時進場時，相鄰元素 delay 30-80ms（不是 0，也不超過 100ms）
- 6 個 pill 進場：累計 stagger 250ms（每個 50ms）
- slogan 字元進場：累計 stagger 280ms（每個 ~30ms × 10 字元）

**Scene 之間過渡**：
- 永遠是 **cross-dissolve + soft scale**（不切換硬切）
- 上一鏡在末尾 300ms 內：opacity 1 → 0, scale 1 → 0.96
- 下一鏡在開頭 300ms 內：opacity 0 → 1, scale 1.04 → 1
- 兩鏡重疊 300ms（在時間軸上 Sprite end 比下一鏡 start 大 0.3s）

## 2.5 Chrome 元素（貫穿全片）

這些是 **持續在畫面裡的小東西**，提供「這是一支完整的片子」的感覺。

**Chrome A · top-left · capability counter（00-22s）**

```
   ┌─────────────┐
   │  ●  CAP·01  │     pulse dot (terracotta) + label
   │  ●●●●○○○○○  │     6-dot progress (filled = current)
   └─────────────┘
```

- 字型：JetBrains Mono 12px，letter-spacing 0.24em
- 顏色：Ink for label, Terracotta for current dot, Mica for upcoming dots
- 動畫：每次切 scene 時，下一個 dot 從空心 → 實心（500ms expoOut）

**Chrome B · top-right · version chip（02-30s）**

```
   ╔═════════════════════════╗
   ║ ● HUASHU-MD-HTML · v2.0 ║
   ╚═════════════════════════╝
```

- 字型：JetBrains Mono 13px Bold，letter-spacing 0.22em
- 顏色：Terracotta dot + Ink label
- 入場：02s 時整體 fade-in 600ms
- pulse dot：每 4 秒做一次極弱呼吸（opacity 1 → 0.6 → 1, 1500ms ease-in-out）

**Chrome C · bottom-center · timeline ticker（07-22s）**

```
   any→md  ━━━━●━━━━━━━━━━━━  md→html  ─  html→md  ─  md→docx  ─  md→pdf  ─  md→epub
```

- 字型：JetBrains Mono 11px，letter-spacing 0.18em
- 當前 capability 用 Terracotta + bold，其他用 Smoke
- 一條橫線連線 6 個名字，進度點（●）隨時間從左滑到右
- 入場：07s 時整條 fade-in 500ms

**Chrome D · bottom-right · watermark（持續）**

```
   CREATED BY HUASHU-DESIGN
```

- 字型：JetBrains Mono 10px，letter-spacing 0.24em
- 顏色：rgba(26,26,26,0.32)
- 完全靜態，不動

**Chrome E · 極淡 paper texture（持續）**

- SVG 噪點 + 極慢的 0.3% scale 呼吸
- opacity ≤ 0.04
- 錄影時幾乎看不見，但能讓畫面有「呼吸」

## 2.6 音訊系統

### BGM 走向（30 秒分段曲線）

```
強度
 │                            ╱╲
1│                          ╱╱  ╲╲
 │                       ╱╱      ╲╲
 │                    ╱╱             ╲
 │                ╱╱                   ╲
 │            ╱╱                          ╲
 │       ╱╱                                  ╲
 │   ╱╱                                          ╲
0└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴
   0  2  4  6  8 10 12 14 16 18 20 22 24 26 28 30s
   │  │     │              │           │  │
   入場│   絃樂進 │      節奏律動加入  │ 頂峰 │  decay
      piano                              swell
```

**層級（每層 30 秒持續，強度變化由 envelope 控制）**：

- **L0 · Room tone**（00-30s）：極弱 background noise，給畫面「不死寂」的呼吸感
- **L1 · Piano single note**（00-08s）：單一鋼琴音持續敲擊，每 1.2 秒一次，慢慢累積
- **L2 · Piano arpeggio**（03-22s）：鋼琴琶音入場，給「拾起節奏」的感覺
- **L3 · Cello drone**（08-22s）：低頻絃樂鋪底，給「重量」
- **L4 · Pulse**（15-22s）：極弱 sub-kick，4/4 節奏（不是 dance beat，是 cinematic pulse）
- **L5 · String swell**（22-26s）：整組絃樂 swell up 到 climax
- **L6 · Decay + reverb tail**（26-30s）：所有層級 decay，留下鋼琴 + reverb

**風格目標**：Max Richter 的 *On the Nature of Daylight* + Ólafur Arnalds 的 *Re:member* + Jóhann Jóhannsson 的 *Orphée*

### SFX 字典

```
Cue                          時間        類型               音量
────────────────────────────────────────────────────────────────────
keyboard click               00.5-02.0   keypress × 12     -18dB（每次 30ms）
cursor blink                 02.0-02.8   subtle tick        -28dB
md morph swell               02.8-03.2   soft whoosh + bloom -16dB
file card whoosh × 6         05.5-08.0   short whoosh       -20dB（每次 200ms）
absorb / ink drop             08.0-08.4   "absorb" splash    -16dB
paper rustle                 08.5-09.0   paper turn         -22dB
chime: capability 02 →        09.0       single chime tone  -18dB
chime: capability 03 →        12.0       single chime tone  -18dB
chime: capability 04 →        15.0       single chime tone  -18dB
chime: NEW (05)               18.0       double chime + glow -14dB
chime: NEW (06)               21.0       double chime + glow -14dB
build sweep                  22.0-22.6   ascending sweep    -10dB
impact (slogan ONE)          22.6        deep impact         -8dB
impact (slogan SIX)          23.4        deep impact         -8dB
pen flourish                 24.0-24.4   pen on paper        -22dB
final stamp / sign-off       29.0-29.5   ink stamp           -14dB
```

**SFX 頻段隔離**（防止互相打架）：
- BGM 佔低頻 (40Hz-2kHz)
- SFX whooshes / chimes 佔中高頻 (2kHz-8kHz)
- SFX impacts 佔低頻 sub (40Hz-120Hz) — 與 BGM cello 重疊但 BGM 同時 duck -3dB

## 2.7 反 AI slop 自檢表（per-shot）

每一鏡在執行前必須過這個 checklist：

```
□  沒有紫色（任何飽和度）
□  沒有圓角卡片 + 左 border accent 的組合（除了 destination card 的誠實 mica border）
□  沒有 emoji 作為圖示
□  沒有 SVG 畫的人物 / 抽象人形
□  沒有未在 Part II.1 色板裡的顏色
□  沒有 Inter / Roboto / Arial 作為 display
□  字距、行高、字級都來自 Part II.2 字體系統（沒有「憑手感」加的值）
□  vertical position 是 8 的倍數（除了刻意的視覺理由）
□  赤陶橙在本鏡佔畫面 < 10%
□  這一鏡有至少一處「pause 暫停時值得截圖」的細節（120% 簽名）
□  上一鏡到這一鏡的過渡是 cross-dissolve + scale，不是硬切
□  本鏡結束時為下一鏡做了視覺「讓位」（不是「全畫面填滿到最後」）
```

---

# Part III · Story Arc

## 3.1 三幕結構

**ACT I · SET-UP (00.0 — 06.0s)**

觀眾進入畫面。問題被提出：什麼是 source of truth？

- SHOT 01 (0.0-1.5s) · BLANK PAGE
- SHOT 02 (1.5-3.0s) · THE CURSOR
- SHOT 03 (3.0-5.0s) · THE TRANSFORMATION
- SHOT 04 (5.0-6.0s) · 進入 gathering（與 ACT II 重疊）

**ACT II · ESCALATION (06.0 — 22.0s)**

答案展開：md 是源頭。它向外輻射 6 條產物鏈。

- SHOT 04 (5.0-8.5s) · GATHERING（any → md）
- SHOT 05 (8.5-11.5s) · FIRST FLOWER（md → html）
- SHOT 06 (11.5-14.5s) · REVERSE FLOW（html → md）
- SHOT 07 (14.5-17.5s) · PUBLISHER GRADE（md → docx）
- SHOT 08 (17.5-20.5s) · ★ NEW · PRINT（md → pdf）
- SHOT 09 (20.5-22.5s) · ★ NEW · EBOOK（md → epub，與 ACT III 重疊 0.5s）

**ACT III · PAYOFF (22.5 — 30.0s)**

主題昇華。slogan 出現。品牌印章。

- SHOT 10 (22.5-24.0s) · THE CONVERGENCE
- SHOT 11 (24.0-26.5s) · ONE SOURCE.
- SHOT 12 (26.5-29.0s) · SIX FORMS.
- SHOT 13 (29.0-30.0s) · SIGN-OFF

## 3.2 情緒曲線

```
情緒強度
 │                                       ╔═══╗
 │                                    ╔══╝   ╚══╗
 │                              ╔═════╝         ╚══╗
 │                          ╔═══╝                   ╚══╗
 │                       ╔══╝                          ╚══╗
 │                   ╔═══╝                                 ╚════════╗
 │             ╔═════╝                                              ╚══╗
 │       ╔═════╝                                                       ╚══
 │  ╔════╝
 │══╝
 0──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──┼──>
    0     2     4     6     8    10    12    14    16    18    20    22    24    26    28    30s
    │     │     │            │           │            │            │     │     │
    blank cursor morph      gather       cap 02-04   cap 05/06 ★  slogan slogan sign-off
                                                                  ONE   SIX
                                                                  ──────►
                                                                  PEAK 24.5s
```

**關鍵 emotional beats**：
- **02.0s**：第一個 keyboard click → 觀眾進入
- **03.0s**：md 字元誕生 → 第一次「awe」
- **08.0s**：6 個檔案 cards 收攏進 md → 「啊，原來 md 是源」第一次 click
- **18.0s**：第一個 NEW 標籤出現 → 老使用者「噢」
- **22.5s**：所有 chrome 收攏，準備進入 Act III → tension build-up peak
- **24.5s**：SIX FORMS. 落地 → emotional climax
- **30.0s**：md 印章靜靜停留 → resolution

---

# Part IV · Shot-by-Shot Storyboard

每一鏡的格式：

```
SHOT NN · NAME
[TIMECODE]  |  FUNCTION
[VISUAL]     畫面構圖
[TYPE]       排版精確 spec
[ANIM]       每元素 in/out/easing/delay
[AUDIO]      music beat + SFX cue
[CHROME]     四角元素狀態
[ANTI-SLOP]  通過的自檢項
[WHY]        承接 + 推進
```

---

## SHOT 01 · "BLANK PAGE"

**[TIMECODE]** 00.00 — 01.50s (1.5s) `|` **FUNCTION** 開場。引觀眾進入。給「空」一個時間。

**[VISUAL]**

整個 1920×1080 是 Ivory paper #FAFAF6。**畫面裡什麼都沒有**。

唯一的存在：一層極淡的 paper texture（SVG 噪點 + 0.3% scale 極慢呼吸），幾乎看不見，但賦予畫面「這是一張真的紙」的潛意識。

構圖：完全空。這是 Kenya Hara 意義上的「白」——不是「還沒畫」，是「內容本身」。

**[TYPE]** 無文字。

**[ANIM]**

- 0.00s · paper texture opacity 從 0 → 0.04（500ms linear）
- 0.50-1.50s · 整個畫面 hold，無動作。讓觀眾的眼睛適應這個白。
- 1.40-1.50s · 畫面中央偏左（x=860, y=540）開始浮現一個 cursor 的位置（透明，下一鏡才顯形）

**[AUDIO]**

- BGM: room tone 進入 (300ms fade-in to -38dB)
- SFX: 無

**[CHROME]** 全部隱藏。Chrome A/B/C/D/E 都還沒顯形。

**[ANTI-SLOP]**

- ✅ 沒有 logo、沒有「Loading...」、沒有任何品牌前置
- ✅ 沒有漸層、沒有 effects
- ✅ 這一鏡的「pause-and-look」signature：畫面有質感（paper texture）但絕不搶戲

**[WHY]**

蘋果 "Designed by Apple in California" 也是這樣開場——給空白一個時間。它告訴觀眾「這部片需要你慢下來」。如果開場就堆 logo 和 chrome，觀眾的注意力被分散，後面 30 秒都收不回。

這 1.5 秒是這支片最重要的 1.5 秒之一。

---

## SHOT 02 · "THE CURSOR"

**[TIMECODE]** 01.50 — 03.00s (1.5s) `|` **FUNCTION** typewriter 誕生。第一個內容。

**[VISUAL]**

畫面中央偏左（x=860, y=540），一個垂直的黑色 block（3px × 56px, Ink #1A1A1A）開始閃爍。這是 cursor。

閃爍兩次（0.7s 一週期 × 2）後，cursor 後面開始逐字出現 `# markdown.md`，字型 JetBrains Mono 56px，顏色 Ink #1A1A1A，letter-spacing -0.01em。

每打一個字元，鍵盤 click 音響一次。打完最後一個字元（13 個字元總計），cursor 在 `.md` 之後繼續閃爍 1 次。

**[TYPE]**

- Text: `# markdown.md`
- Font: JetBrains Mono 500 weight
- Size: 56px
- Color: Ink #1A1A1A
- Letter-spacing: -0.01em
- Position: horizontal center, y = 540（baseline，文字 vertical center 略低於此）

**[ANIM]**

- 01.50s · cursor block opacity 0 → 1 (200ms)
- 01.50-01.85s · cursor blink 第一次（off 200ms / on 200ms）
- 01.85-02.20s · cursor blink 第二次
- 02.20-02.85s · 13 個字元 staggered 出現，每個間隔 50ms（共 650ms 完成），每個字元各自 fade + 1px slide-down (180ms expoOut)
- 02.85-03.00s · cursor 在末尾再 blink 一次（最後一次，標誌輸入完成）

**[AUDIO]**

- BGM: piano 第一音敲擊 at 01.50s (-22dB)
- SFX: keyboard click × 13 (每字一次, -18dB, 30ms each)
- SFX: 最後一次 cursor blink 後 200ms 靜默（給下一鏡 morph 讓位）

**[CHROME]** 仍隱藏。

**[ANTI-SLOP]**

- ✅ cursor 不是 sci-fi 閃爍（不是 0.1s 極快閃爍），是 macOS terminal cursor 節奏的真實模擬
- ✅ typing 不是「字元一次性出現」，是真的有節奏的打字
- ✅ font 是 JetBrains Mono，不是 Courier 或 Menlo 這種系統預設 mono
- ✅ pause-and-look signature：cursor 的 3px 寬度（不是 2px 或 4px）—— 一個非常精確的細節，懂行的人會注意到這是「真實 terminal 設計的」

**[WHY]**

這一鏡是 setup 的核心：**markdown 不是一個名詞，它是一個動作**——它是「敲擊鍵盤把字元變成結構」這件事本身。

cursor 是寫作的最小單位。從一個 cursor 開始，是「原始碼」的誕生。

下一鏡的 morph 就建立在這個觀眾已經接受「我們在寫 markdown」的前提上。

---

## SHOT 03 · "THE TRANSFORMATION"

**[TIMECODE]** 03.00 — 05.00s (2.0s) `|` **FUNCTION** 揭示 hero。`# markdown.md` morph 成 hero `md.`

**[VISUAL]**

第 03.00 秒：`# markdown.md`（56px mono）開始向中央收攏、放大、變形。

**morph 過程**（詳細解構）：

- 03.00-03.30s（300ms）：`# markdown.md` 的 `#` 和 `arkdown` 部分淡出（opacity 1 → 0），同時 `m` 和 `d.md` 的 `md` 部分留下。
- 03.30-04.10s（800ms）：留下的 `md` 從 mono 字型 morph 成 Newsreader serif，從 56px 放大到 480px，從 Ink 變成 Ink（不變色），位置不變（仍在畫面中央）。
- 04.10-04.80s（700ms）：在 `md` 字元的右下角，一個 Terracotta 句點 `.` 浮現（fade-in + scale 0.6 → 1 + overshoot easing）。
- 04.80-05.00s（200ms）：句點正式 settle，hero 完整。下方 30px 出現一條 320px 寬的赤陶橙細線（terracotta accent rule, 2px thick），從中心向兩端展開。

**結束幀**：`md.`（Newsreader 600 weight, 480px, Ink with Terracotta dot）+ 下方一條赤陶橙細線。畫面其他全空。

**[TYPE]**

- Text: `md.`（`md` Ink, `.` Terracotta）
- Font: Newsreader 600 weight
- Size: 480px (display L)
- Letter-spacing: -0.04em
- Color: `m`+`d` Ink #1A1A1A, `.` Terracotta #C2410C
- 在 hero 中線（y = 540）水平垂直居中
- accent rule 下方 30px，width 320px（從 0 長成）

**[ANIM]**

- 03.00-03.30s · `#` `arkdown` `md`（中段）淡出 (opacity 1 → 0, expoOut)
- 03.30-04.10s · `md` morph：fontFamily 切換、fontSize 從 56 → 480、weight 從 500 → 600（800ms expoOut，注意 morph 不是 abrupt 切換，而是 ghost 殘影疊加 + scale up + opacity 切換）
- 04.10-04.80s · `.` 入場 (700ms overshoot, scale 0.6 → 1)
- 04.80-05.00s · accent rule width 0 → 320px (300ms expoOut)

**[AUDIO]**

- BGM: piano 第二音 at 03.00s (-20dB), 第三音 at 04.20s (-18dB) — piano 累積
- SFX: 03.00-03.20s soft whoosh（morph 開始時, -16dB）
- SFX: 04.10s subtle bloom（句點出現的瞬間, -20dB）
- SFX: 04.80s short paper rustle（accent rule 展開, -22dB）

**[CHROME]**

- 04.50s · Chrome B（version chip top-right）開始浮現 (fade-in 600ms)
  - 形態：`● HUASHU-MD-HTML · v2.0`
  - terracotta dot, mono text, Ink color
  - 進入位置：top: 78px, right: 80px
- 仍隱藏：Chrome A, C, E（visible only ≥ 06s）

**[ANTI-SLOP]**

- ✅ morph 不是「淡出 + 淡入」的廉價 transition，是真正的字元變形（含 ghost 殘影疊加）
- ✅ 句點是 hero 的「簽名細節」（120% 做到的那個）：Terracotta 句點小如指甲，但是這部片的視覺錨點，**所有後面的鏡頭裡這個句點都保留為 hero 標識**
- ✅ accent rule 不是裝飾，是 hero 的 base line——它在 Shot 11 的 slogan 那裡會再次出現，建立首尾呼應
- ✅ pause-and-look signature：480px Newsreader 'md' 的字距 -0.04em 讓 m 和 d 之間幾乎貼合但不接觸，這是 Newsreader 這個字型在大字級時的招牌質感

**[WHY]**

這是 hero shot。後面 25 秒整部片的「主角」（`md.`）在此誕生。

morph 的設計哲學：**從 mono 到 serif，是從「我在打字」到「我在寫作」的隱喻**。mono 是 typewriter，serif 是 publishing。md 同時是兩者——它在鍵盤上敲，但它是 publishing 的原始碼。

下一鏡進入 ACT II，hero 已經站住了——它會被推到畫面上方，讓出空間給「物質化的產物」。

---

## SHOT 04 · "GATHERING" (any → md)

**[TIMECODE]** 05.00 — 08.50s (3.5s) `|` **FUNCTION** CAPABILITY 01 揭示。萬物 → md。建立「md 是源」的世界觀。

**[VISUAL]**

05.00s：hero `md.` 從畫面中央（y=540）向上滑到 y=280（即 1/4 高度位置），同時縮小到 220px。

隨後畫面下半部（y=520 ~ y=900 區域）出現 6 張檔案 cards，按順序從畫面外（下方 y=1140）飛入，沿一條隱形的拋物線軌跡向 md hero 收攏。

6 張 cards 的設計（**每張都是真實檔案類型的迷你 demo，不是 fake bar lines**）：

```
.pdf   │ 雙欄佈局 + 頁首 "doc.pdf" + 頁碼 "— 12 —" + 幾行真實排版的小文字
.docx  │ heading "On Markdown" + 副標 italic + 6 行段落 ascii
.pptx  │ 標題 "MD AS SOURCE" + 一個簡化的 bar chart 佔位
.xlsx  │ 6×4 的 spreadsheet 網格 + 一些數字
.epub  │ Apple Books 風的頁面 + 章節標題 "Chapter 01"
.html  │ 一個瀏覽器 chrome（三個圓點 + URL bar "example.com"）+ 標題 + 段落
```

每張 card 尺寸 130×180px，白底 + Mica 邊框 + 24°右上角 fold。

**飛行軌跡**：從下方 y=1140 出發，沿拋物線向 md hero 的「.」位置（約 x=960+50, y=280+90）匯聚。中段（在畫面中部時）6 張 cards 排成扇形，每相鄰兩張間隔 220px。最終所有 6 張被 md 「吸收」（scale 1 → 0.5 + opacity 1 → 0，同時 position 收攏到一個點）。

吸收時機：從 05.60s 開始，每隔 0.18s 一張 launch。每張飛行 1.1s 後被吸收。最後一張 absorb 完成時間約 07.60s。

吸收完成後（07.60-08.20s），下方 60px 處出現 tagline：「萬物 → md」（中文襯線，36px，Ink，italic）

08.20-08.50s · 整體 hold，準備進入 Shot 05。

**[TYPE]**

- hero `md.`：縮小到 220px（同 SHOT 03 字型規格）
- 6 cards 內部排版：JetBrains Mono 12-14px for labels, Newsreader 12-16px for content
- tagline「萬物 → md」：Noto Serif SC 36px italic + 中間的 → 是 Newsreader italic + Terracotta
- 頂部 Chrome A 文字：JetBrains Mono 12px

**[ANIM]**

- 05.00-05.30s · hero md 縮放 + 上移（300ms expoOut）
- 05.30s · Chrome A capability counter 入場（CAPABILITY · 01 顯示，第一個 dot 實心）
- 05.60-07.60s · 6 張 cards 依次發射（每張 launch delay = 5.60 + i × 0.18s, 飛行 1.1s，absorb at launch+1.1）
- 07.60-08.20s · tagline「萬物 → md」入場（fade-in 400ms + slight y slide 12px → 0）
- 08.20-08.50s · hold

**[AUDIO]**

- BGM: piano arpeggio L2 進入 at 05.00s（-26dB → -20dB 漸入）
- SFX: file card whoosh × 6（每張 launch 時一次，每次 200ms，-20dB）
- SFX: absorb / ink drop（最後一張 card 被吸收時，-16dB）
- SFX: paper rustle（tagline 入場時，-22dB）

**[CHROME]**

- A（top-left capability counter）: ON, 顯示 `CAPABILITY · 01`, 第一個 dot 實心
- B（version chip）: ON, 持續顯示
- C（timeline ticker）: OFF (會在 SHOT 05 入場)
- D（watermark）: ON, 永遠 ON
- E（paper texture）: ON

**[ANTI-SLOP]**

- ✅ 6 張 cards 不是 emoji 也不是圖示，是**有內部內容的迷你 demo**——每張都 readable
- ✅ 飛行軌跡是拋物線（重力感），不是直線（電腦感）
- ✅ 收攏時是「吸收」（scale + position 同時收）不是「疊加」
- ✅ 沒有給 md 字元任何 glow 或 particle effects（不需要解釋「md 在吸收」，觀眾自己看得懂）
- ✅ pause-and-look signature：每一張 card 在飛行中段 pause 看，都能讀出來「這是個 PDF / 這是個 DOCX」——這就是 120% 做到的細節
- ✅ tagline 用「→」而不是「to」或「至」，是 markdown 自己的字元

**[WHY]**

這是 ACT II 的開門鏡。如果觀眾看完這 3.5 秒沒意識到「噢，md 是源」，後面的鏡頭就白做了。

3.5 秒裡有 3 個 micro-narrative beats：
1. hero 讓位（md 上移）—— 暗示「我讓位給我的產物們」
2. 6 個產物現身 —— 揭示「我能收的東西」
3. 全部歸位回 md —— 「但他們最終都是 md」

下一鏡進入 md → html 的正向流動——觀眾已經接受「md 是源」，現在 ready to see「md 怎麼變」。

---

## SHOT 05 · "FIRST FLOWER · HTML" (md → html)

**[TIMECODE]** 08.50 — 11.50s (3.0s) `|` **FUNCTION** CAPABILITY 02。第一次正向輸出。建立 ScenePipeline 模式（後續 5 鏡共用此結構）。

**[VISUAL]**

08.50s：hero `md.` 從中心上方位置滑到畫面左側（x=480, y=540），尺寸保持 220px。

同時畫面右側 (x=1400, y=540) 出現一個 destination card：模擬「Tufte CSS 風的 essay html」。

destination card 設計（**真實可讀的內容，不是 bar lines**）：

```
┌─────────────────────────────────┐
│                                  │
│  On Markdown                     │  ← Newsreader 600, 32px, Ink
│  AN ESSAY · 2026                 │  ← Mono 11px, 0.18em, Smoke
│  ▬▬▬                             │  ← Terracotta rule 60×3px
│                                  │
│  md is the source of truth.      │  ← Newsreader 400, 18px, line-height 1.7
│  Anything else is product.       │
│  We write once. Publish six      │
│  ways. The river forks; the      │
│  spring stays the same.          │
│                                  │
│  ─ huashu, 2026.05.11            │  ← italic 14px, Smoke
│                                  │
│  article.html · TUFTE THEME      │  ← Mono 10px, 0.18em, Smoke (bottom)
└─────────────────────────────────┘
   寬 480px × 高 560px
   白底 + Mica border + 24° 角折
```

md 字元與 destination card 之間用一條 terracotta 細線連線，從 md 的 dot 出發，向右生長 380px，箭頭 head 觸達 card 左邊界。線上方 30px 處顯示 label「md → html」（JetBrains Mono 14px Terracotta，letter-spacing 0.14em）。

09.80s 時：Chrome C（timeline ticker）首次入場，固定在 y=1000 處。

**[TYPE]**

- 見 visual description 內嵌
- label「md → html」字級 14px， Mono Bold，Terracotta，letter-spacing 0.14em
- destination card 頂部 chapter title 是 Newsreader 600, 32px, Ink
- destination card 底部小印 mono 10px Smoke 0.18em

**[ANIM]**

- 08.50-08.80s · hero md 從 center-top 滑到 left-mid（300ms expoOut）
- 08.80-09.10s · arrow line 從 md.dot 起點向右生長（300ms expoOut, 0 → 380px）
- 09.10s · arrow head 浮現（200ms overshoot）
- 09.20-09.40s · label「md → html」入場（fade-in + 8px y slide-down, 300ms expoOut）
- 09.40-10.10s · destination card 整體入場（700ms expoOut, scale 0.85 → 1 + opacity 0 → 1）
- 10.10-10.80s · destination card 內部 staggered 入場：title (400ms delay 0) → 副標 metadata (delay 200ms) → terracotta rule (delay 400ms) → 6 行正文 (each delay 60ms cascade) → 簽名 (delay 1000ms) → bottom mono (delay 1100ms)
- 10.80-11.50s · hold + 微觀呼吸 (整體 scale 1 → 1.005 → 1, 600ms ease-in-out infinite, 但本鏡只播放半個週期)

**[AUDIO]**

- BGM: cello drone L3 入場 at 09.00s (-30dB → -24dB)
- SFX: chime: capability 02 at 09.00s (-18dB)
- SFX: paper rustle（card 入場時, -22dB）
- SFX: micro ticks（每行文字 staggered 入場時, -26dB each）

**[CHROME]**

- A: 推進到 `CAPABILITY · 02`, 第二個 dot 實心
- B: ON
- **C: 首次入場** at 09.80s，`any→md  ━━━━●━━━━━  md→html  ─  html→md  ─  md→docx  ─  md→pdf  ─  md→epub`，進度點 ● 位於第二格上方
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ destination card 的「On Markdown」essay 內容是真的可讀的英文哲學小段，不是 Lorem ipsum
- ✅ 「article.html · TUFTE THEME」這個小印是「pause 時能讀出來的細節簽名」
- ✅ 沒用任何 glow 或 particle 來「強調」md → html 的轉換——靠 typography 和構圖自己講清楚
- ✅ arrow line 不是 dashed 或 dotted（避免「網頁教學」感），是 1.5px 實線 Terracotta
- ✅ pause-and-look signature：destination card 頂部的「AN ESSAY · 2026」副標用了 Newsreader 的 small caps OpenType feature，0.18em 字距——是這一鏡的 120% 細節

**[WHY]**

這是 ScenePipeline 模式的首次建立。後續 5 個 capability shots 都會按這個結構推進：
1. md 在左、destination 在右
2. arrow + label 在中間
3. destination card 內部 staggered 入場（每個 card 都有 6-8 個文字層級）
4. card 內容是真實可讀的，不是 fake bar lines

觀眾看到第二次（SHOT 06）就會理解這個模式，看到第六次（SHOT 09）會有「啊，又來一次，但這次是 NEW」的感覺——這正是 ACT II 的節奏設計。

---

## SHOT 06 · "REVERSE FLOW · MD" (html → md)

**[TIMECODE]** 11.50 — 14.50s (3.0s) `|` **FUNCTION** CAPABILITY 03。反向歸檔：html → md。建立「雙向流」概念。

**[VISUAL]**

cross-dissolve 進入。前一鏡的 destination card 在 11.50-11.80s 內縮小退場到右下角，新的 destination card（這次顯示 markdown 原始碼）從右側入場。

新的 destination card 設計：**深底 markdown source 檢視**（與 SHOT 05 的淺底 html 形成視覺對比）。

```
┌─────────────────────────────────┐
│                                  │  ← 背景 Charred #2A2620
│  # On Markdown                   │  ← Terracotta, mono 14px
│                                  │
│  An essay · 2026                 │  ← Smoke, mono 14px
│                                  │
│  > md is the source.             │  ← italic Smoke, mono 14px
│  > Anything else is **product**. │     `**product**` 高亮 mica + bold
│                                  │
│  - 1 source                      │  ← mono 14px Smoke
│  - 6 forms                       │
│  - ∞ outputs                     │
│                                  │
│  essay.md · CLEAN MARKDOWN       │  ← bottom Mono 10px Smoke
└─────────────────────────────────┘
   480×560px, Charred 底, 頂部 24° 角折是 Cinder
```

arrow direction 反向：從右側 destination card 向左 md 字元方向（短 Terracotta 線 + 箭頭 head 指向左）。label 改為「html → md」。

**關鍵差異點**（和 SHOT 05 形成 visual rhyme）：
- destination 在右、md 在左（同 SHOT 05）
- 但 arrow direction 反向（visual: 我們在歸檔/拉回來）
- card 是深底（視覺對比，強調這是 source）

**[TYPE]**

- 全卡片內部都是 JetBrains Mono 14px
- markdown 語法元素配色：`#` 標題 Terracotta，`>` 引用 italic Smoke，`**bold**` Mica + bold，列表 dash Smoke
- bottom mono 10px Smoke

**[ANIM]**

- 11.50-11.80s · 上一鏡 card 退場（縮 → 右下角, fade out）+ md 字元保持
- 11.80-12.10s · arrow line 反向生長（這次從右向左, 300ms expoOut）
- 12.10s · arrow head（指向左）浮現
- 12.20-12.40s · label「html → md」入場
- 12.40-13.10s · 新 destination card 入場（同 SHOT 05 入場邏輯）
- 13.10-13.80s · markdown 內部 6 行 staggered 入場（每行 100ms delay）
  - 特殊 micro-detail：每一行入場時模擬 typewriter——line 的 character-by-character cascade reveal（讓觀眾感覺到「這是 markdown 被「寫出來」的過程」）
- 13.80-14.50s · hold

**[AUDIO]**

- BGM: 持續 L1+L2+L3 layers
- SFX: chime: capability 03 at 12.00s (-18dB)
- SFX: paper rustle (12.40s)
- SFX: 每行入場時極弱 keyboard click ticker（-26dB each, 100ms apart）

**[CHROME]**

- A: 推進到 `CAPABILITY · 03`，第三個 dot 實心
- B: ON
- C: 進度點 ● 滑到「html→md」位置
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ 這是整支片唯一的「深底」鏡頭——刻意製造視覺對比，讓觀眾知道「這是 source code」，不是「又來一個 destination」
- ✅ markdown 內部的 syntax highlighting 用的顏色不是 cyber 配色（不是 VS Code Dark+ 那種），是出版社配色（Terracotta + Smoke + Mica）
- ✅ 「essay.md · CLEAN MARKDOWN」底部小印 → pause-and-look signature
- ✅ 反向 arrow 不是「U-turn 曲線」，是直線 + 反向箭頭——保持結構一致性

**[WHY]**

這一鏡的真正作用不是「秀 capability 03」，是**告訴觀眾這條管道是雙向的**。

如果整支片 6 個 capability 都是從 md 向外輻射，觀眾會以為「md 只是出去」。第 3 個 capability 讓流動反向，建立「md 是一切的中樞」的世界觀。

這是為什麼 capability 順序我選了 02 (md→html) → 03 (html→md) → 04 (md→docx) ——故意把反向 capability 卡在第 3 位，最大化「雙向流」的認知 surprise。

---

## SHOT 07 · "PUBLISHER GRADE · DOCX" (md → docx)

**[TIMECODE]** 14.50 — 17.50s (3.0s) `|` **FUNCTION** CAPABILITY 04。出版社品味 docx。建立「md 不只是給程式設計師的」論點。

**[VISUAL]**

回到淺底，回到「md 在左、destination 在右」。

destination card 設計：**出版社級 docx 章節首頁**（高密度資訊，但完全克制）。

```
┌─────────────────────────────────┐
│                       ON MARKDOWN│  ← page header, right-aligned, Smoke italic mono 9px
│  CHAPTER · 01                    │  ← Terracotta mono 11px bold 0.22em
│                                  │
│  On Markdown                     │  ← Newsreader 700, 36px, Ink, lh 1.1
│  A short essay on source-of-truth│  ← Newsreader italic 14px, Smoke
│  thinking                        │
│                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━     │  ← Terracotta full-width rule 3px
│                                  │
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬       │  ← 10 lines of mica bar paragraphs
│  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬           │     (varied widths 76-95%)
│  ...                             │
│                                  │
│                — 1 —             │  ← page number, centered, mono 10px Smoke
└─────────────────────────────────┘
   480×580px, white card, Mica border, 24° corner fold
```

**特別細節**：
- 頂部右上角的「page header」（書名 italic 灰色 mono）是真實出版社 docx 的細節簽名
- 「CHAPTER · 01」前綴讓觀眾一眼意識到「這是一本書的一頁，不是一篇文章」
- terracotta full-width rule（不是細線，而是 3px 粗 rule）是出版社章節首頁的招牌
- 底部 page number「— 1 —」前後的破折號是 Newsreader 的 em-dash，不是 hyphen

**[TYPE]**

- page header: Newsreader italic 9px, Smoke, letter-spacing 0.14em
- CHAPTER · 01: JetBrains Mono Bold 11px, Terracotta, letter-spacing 0.22em
- main title: Newsreader 700, 36px, Ink, line-height 1.05
- subtitle: Newsreader italic 14px, Smoke
- terracotta rule: 3px thick, full card width
- bar paragraphs: Mica color #E6E1D6, height 6px
- page number: JetBrains Mono 10px, Smoke, letter-spacing 0.18em

**[ANIM]**

- 14.50-14.80s · 前一鏡 card 退場 + md 保持
- 14.80-15.10s · arrow line 正向生長
- 15.10s · arrow head, label「md → docx」入場
- 15.30-16.10s · destination card 整體入場
- 16.10-17.00s · 內部 stagger：page header (delay 0) → CHAPTER 標 (delay 100ms) → title (delay 300ms) → subtitle (delay 500ms) → rule (delay 700ms) → 10 行段落 cascade (delay 850ms + 60ms cascade) → page number (delay 1600ms)
- 17.00-17.50s · hold

**[AUDIO]**

- BGM: 持續；at 15.00s BGM 整體 swell +2dB（暗示我們在向高潮推進）
- SFX: chime: capability 04 at 15.00s (-18dB)
- SFX: paper rustle (15.30s)

**[CHROME]**

- A: `CAPABILITY · 04`, 第四個 dot 實心
- B/C/D/E: ON

**[ANTI-SLOP]**

- ✅ 不寫「這是一本書的內頁 mockup」的解釋字（讓排版自己說話）
- ✅ bar paragraphs 用 Mica（#E6E1D6）這種極淡灰色，不是黑色——給「這是排版樣式預覽，不是真內容」的誠實訊號
- ✅ pause-and-look signature：頂部 right-aligned page header italic mono——99% 的觀眾不會看，1% 的設計師看到會知道「這家做了功課」
- ✅ 這一鏡是 6 個 capability 裡色彩最飽和的（Terracotta 佔了 page rule + chapter label + 頂部右 chrome counter）——剛好在故事弧的中段，符合「向高潮 build-up」的曲線

**[WHY]**

CAPABILITY 04 是承上啟下的關鍵一鏡：
- 它確認了「md 不只是 web 用」——它能做出版社級別的 docx
- 它建立了「印刷品」的視覺語境，為 SHOT 08（pdf）和 SHOT 09（epub）做準備

觀眾看完這一鏡，對「md → 印刷品」這條鏈條 ready。接下來兩鏡的 NEW 標籤就有了承接。

---

## SHOT 08 · "★ NEW · PRINT" (md → pdf)

**[TIMECODE]** 17.50 — 20.50s (3.0s) `|` **FUNCTION** CAPABILITY 05。**NEW**。md → 出版級 PDF。第一次「升級」標誌亮起。

**[VISUAL]**

cross-dissolve 進入。這一鏡的視覺強度**顯著高於** SHOT 05-07——因為這是「新東西」，需要被記住。

視覺差異點：
1. **NEW 標籤**：top-left 在 capability counter 旁邊亮起一個 Terracotta 矩形框，內含「★ NEW」字元（JetBrains Mono Bold 13px, Terracotta, letter-spacing 0.22em，4px Terracotta border, 6px×12px padding）
2. **destination 不是單一卡片，是兩張 PDF fan 出來**：A4 在後面（輕微 +5° 旋轉），大32開（176×240mm，中文紙本書規格）在前面（輕微 -3° 旋轉），形成「兩個 page-size 都支援」的視覺
3. **每張 PDF 上有「印刷裁切標記」（crop marks）**——四角各一個 L 型小線，2px 粗，Smoke 色——這是真正印廠 PDF 的細節
4. arrow + label 配色全部用 Terracotta（不是 Ink），整體配色更暖

**兩張 PDF 內容**：

PDF A（A4, 後面）：

```
┌──────────────────────────┐
│ ┌                      ┐ │  ← crop marks
│  A4 · 210×297mm           │  ← Mono Bold 10px Terracotta
│  ─── (Terracotta rule)    │
│  On Markdown              │  ← Newsreader 22px
│  ──────────────────       │
│  ▬▬▬▬▬▬▬▬▬▬▬             │  ← 7 lines mica bars
│  ▬▬▬▬▬▬▬▬▬▬▬▬            │
│  ...                      │
│                           │
│ └                      ┘ │  ← crop marks
└──────────────────────────┘
   360×460px, white card, +5° rotation
```

PDF B（大32開，前面）：

```
┌────────────────────┐
│ ┌                ┐ │  ← crop marks
│  大32開 · 176×240mm│  ← Mono Bold 10px Terracotta
│  ───                │
│  On Markdown        │  ← Newsreader 19px
│  ──────────         │
│  ▬▬▬▬▬▬▬▬▬▬        │  ← 6 lines mica bars
│  ...                │
│ └                ┘ │
└────────────────────┘
   290×410px, white card, -3° rotation
```

**[TYPE]**

- NEW 標籤：Mono Bold 13px Terracotta, 0.22em letter-spacing, 1.5px Terracotta border
- arrow label「md → pdf」：Mono Bold 14px Terracotta, 0.14em
- PDF spec labels (A4 · 210×297mm 等)：Mono Bold 10px Terracotta, 0.2em
- chapter titles inside PDFs：Newsreader 600 weight, 19-22px, Ink

**[ANIM]**

- 17.50-17.80s · 前一鏡 card 退場 + md 保持
- 17.70s · **NEW 標籤亮起**（特殊處理：scale 0.8 → 1.1 → 1.0 over 400ms with overshoot easing；同時一道極弱 terracotta glow 短暫 pulse 然後消失）
- 17.80-18.10s · arrow + label 入場（這次用 Terracotta accent，強調「這是 NEW」）
- 18.20-18.60s · PDF B（前面那張）入場（400ms expoOut, scale 0.85 → 1 + 順時針 -8° → -3°）
- 18.50-18.90s · PDF A（後面那張）緊隨入場（400ms expoOut, scale 0.85 → 1 + 順時針 0° → +5°，stagger delay 300ms）
- 18.90-19.70s · 兩張 PDF 內部 cascade staggered 入場
- 19.70s · 4 個 crop marks（PDF B 的）依次出現（80ms cascade，給「印廠工藝」的細節簽名）
- 19.70-20.50s · hold

**[AUDIO]**

- BGM: percussion pulse L4 加入 at 18.00s (-32dB)（極弱 sub-kick 4/4 節奏建立）
- **SFX: chime: NEW (05) at 17.70s（double chime + soft glow + reverb tail, -14dB）** ← 這是整支片最重要的 SFX cue 之一
- SFX: paper rustle × 2（每張 PDF 入場時，-22dB each）
- SFX: subtle "ink stamp" at 19.70s（crop marks 出現時, -22dB）

**[CHROME]**

- A: `CAPABILITY · 05`, 第五個 dot 實心
- A 旁邊新增 NEW 標籤
- B: ON, 此時 version chip 旁的橙點同步 pulse（強調「v2.0 新增」）
- C: 進度點 ● 滑到「md→pdf」位置, 這個位置的文字字級加大 0.5px 強調
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ NEW 標籤不是 emoji 不是 sticker——是 typographic mark（mono + 0.22em + ★ + border）
- ✅ 兩張 PDF 不是「疊在一起」的廉價 stacking，是 fan + 旋轉（暗示「開啟看」的物理動作）
- ✅ crop marks 是真正印廠術語的視覺表達，pause 時能看到「啊這是 print-ready」
- ✅ 沒用 glow 或 particle 來強調「NEW」——靠 typography 和 SFX 自己說話
- ✅ pause-and-look signature：PDF B 頂部的「大32開 · 176×240mm」中英混排，是花叔生態對中文紙本書規格的尊重

**[WHY]**

這是 ACT II 高潮鏡之一。兩件事必須同時發生：
1. 觀眾必須 immediate 意識到「這是新功能」
2. 必須用視覺細節說明「這不是湊數的 wkhtmltopdf 包裝，是真正出版級」

NEW 標籤 + crop marks + 兩張 PDF fan + 完整的 A4 / 大32開規格說明——四件事一起做到上面兩件。

下一鏡的 epub 是雙 NEW 鏡頭裡的第二個，節奏感、情緒強度要比這一鏡再上一檔。

---

## SHOT 09 · "★ NEW · EBOOK" (md → epub)

**[TIMECODE]** 20.50 — 22.50s (2.0s) `|` **FUNCTION** CAPABILITY 06。**NEW**。md → 標準 EPUB3。第二個新功能。最後一個 capability。

**[VISUAL]**

cross-dissolve 進入。這一鏡的鏡頭時長**比前面短**（只 2.0s 而不是 3.0s）——因為我們已經建立了「NEW + destination」的模式，第二次出現觀眾秒懂，節奏可以加速。

destination card 設計：**Apple Books 風的 EPUB reader frame**（強調「這本書已經在閱讀器裡了」的現實感）。

```
   ╔════════════════════════════════════╗
   ║ ● ● ●                              ║  ← window chrome (Apple Books)
   ╠════════════════════════════════════╣
   ║                                    ║
   ║  HUASHU · ORANGE BOOK              ║  ← Mono Bold 10px Terracotta 0.22em
   ║                                    ║
   ║                                    ║
   ║  On                                ║  ← Newsreader 700, 30px, Ivory paper
   ║  Markdown                          ║     (on Charred bg)
   ║                                    ║
   ║  ───                               ║  ← Terracotta rule 40×2px
   ║                                    ║
   ║  an essay · 花叔                   ║  ← italic 14px Smoke on Charred
   ║                                    ║
   ╠════════════════════════════════════╣
   ║ Apple Books · 1 of 24    EPUB 3   ║  ← Mono 10px Smoke 0.14em
   ╚════════════════════════════════════╝
   460×470px, ivory paper outer + Charred inner book cover area
   2px Ink border, 22px border-radius (modern app frame)
```

**關鍵視覺差異**：
- 整體 frame 是「macOS app 視窗」感（三個圓點 + 圓角 22px）
- 中間是「開啟的電子書」cover area（Charred 底 + 出版社品味的 typography）
- 底部是「Apple Books · 1 of 24」reader chrome
- 整張 card 給人「我在 Apple Books 裡讀這本書」的現實感

**[TYPE]**

- HUASHU · ORANGE BOOK：Mono Bold 10px, Terracotta, 0.22em
- book title (On Markdown)：Newsreader 700, 30px, Ivory (on Charred bg), line-height 1.0
- terracotta rule：40×2px
- author italic：Noto Serif SC italic 14px, Smoke
- Apple Books chrome：Mono 10px, Smoke, 0.14em

**[ANIM]**

- 20.50-20.80s · 前一鏡 PDF 退場 + md 保持
- 20.70s · NEW 標籤**保持亮起**（這次不重新彈出，因為已經在 SHOT 08 建立了——直接顯示「★ NEW」即可）
- 20.80-21.10s · arrow + label「md → epub」入場（Terracotta accent，同 SHOT 08）
- 21.20-21.80s · EPUB destination card 整體入場（600ms expoOut, scale 0.88 → 1）
- 21.30-22.00s · 內部 staggered：window chrome dots (delay 0) → 頂部 brand label (delay 200ms) → book title 「On」(delay 400ms) → 「Markdown」(delay 480ms) → rule (delay 700ms) → author italic (delay 850ms) → bottom chrome (delay 1000ms)
- 22.00-22.50s · hold + 準備 transition 到 ACT III

**[AUDIO]**

- BGM: percussion 持續，但 at 22.00s 整體 BGM swell +3dB（為 SHOT 10 的 convergence build-up）
- **SFX: chime: NEW (06) at 20.70s（double chime + soft glow，比 SHOT 08 高半個音, -14dB）**——半音差讓兩個 NEW 鏡頭形成 musical relationship
- SFX: window chrome subtle "click" at 21.20s（macOS 視窗出現感, -24dB）
- SFX: page turn rustle at 21.40s

**[CHROME]**

- A: `CAPABILITY · 06`, 第六個 dot 實心（**全部實心 — 6/6**）
- A 旁邊 NEW 標籤持續
- B: 版本 chip 的橙點 pulse 加強（amplitude × 1.5）
- C: 進度點 ● 抵達最右端「md→epub」位置
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ 不畫 Kindle 或 Apple Books 的真 logo（避免 IP 風險）；用 macOS 視窗 chrome 暗示「閱讀器」即可
- ✅ 沒用 e-ink 灰色濾鏡（避免 Kindle slop）
- ✅ 「Apple Books · 1 of 24」chrome 是真實出版資料感（24 章節，第 1 章）
- ✅ pause-and-look signature：書名 「On / Markdown」**斷行**——Newsreader 在 30px 大字級下的換行設計，致敬 Penguin Classics 封面排版

**[WHY]**

這一鏡是 ACT II 的收尾。兩件事必須完成：
1. 6 個 capability 全部展示完畢（counter 6/6 實心）
2. 情緒開始向 ACT III 的高潮 build-up

鏡頭長度從 3.0 → 2.0s 是刻意的——節奏在加速，觀眾感知到「我們要到頂峰了」。

---

## SHOT 10 · "THE CONVERGENCE"

**[TIMECODE]** 22.50 — 24.00s (1.5s) `|` **FUNCTION** ACT II → ACT III 的過渡。所有元素歸位。準備 slogan。

**[VISUAL]**

22.50s：所有之前的 destination card 已退場。Chrome A/C 開始 fade out（capability counter 已 6/6 完成，使命達成）。

畫面中央，md 字元從左側位置（x=480）滑回正中（x=960），同時尺寸從 220px → 300px。

md 周圍的 6 個 capability label（any→md / md→html / html→md / md→docx / md→pdf / md→epub）從遠處（圓周 r=380px）逐個浮現，環繞 md 字元成圓形，每 60° 一個，按順時針順序排列（頂部從「any→md」開始）。這些 label 是 Mono Bold 14px Smoke（非 active）+ Terracotta（actually new）的 mix。

整體效果：**md 字元是太陽，6 個 capability 是行星。**

但這一鏡不需要讓觀眾停留太久——這是過渡鏡。

23.50-24.00s：6 個 capability label 緩慢 fade out（200ms 每個，inverse cascade），md 字元繼續保持在中央，縮小到 180px，準備讓位給 slogan。

**[TYPE]**

- 6 個 capability label：JetBrains Mono Bold 14px, letter-spacing 0.16em
  - 前 4 個（any→md / md→html / html→md / md→docx）：Smoke
  - 後 2 個（md→pdf / md→epub）：Terracotta

**[ANIM]**

- 22.50-22.80s · 上一鏡 EPUB card 退場，Chrome A/C fade out（300ms linear）
- 22.50-23.00s · md 字元滑回中央 + 放大（500ms expoOut）
- 22.80-23.40s · 6 個 capability label 從 md 周圍浮現（每個 60° 位置，r=380px，stagger 80ms each, fade-in 300ms + 微 outward slide 20px）
- 23.40-23.80s · hold（6 個 label 在 md 周圍 settle）
- 23.80-24.00s · 6 個 label 同時 fade out（200ms linear），md 字元縮小到 180px（200ms expoOut）

**[AUDIO]**

- BGM: at 23.00s, all-layer swell 開始（L1+L2+L3+L4 → +4dB）
- BGM: at 23.50s, percussion 短暫停頓 1 拍（給 sudden silence 的張力）
- SFX: 6 個 capability label 入場時極弱「click」（-30dB each, staggered）
- SFX: 23.50s 開始 ascending sweep（build-up 到 24.00s）

**[CHROME]**

- A: fade out at 22.50s（counter 已 6/6，使命完成）
- B: ON, 但開始為 ACT III 準備過渡（保持位置不變，但內部 spacing 略微 tighten）
- C: fade out at 22.50s
- D: ON
- E: ON

**[ANTI-SLOP]**

- ✅ 6 個 capability label 不是「圍著 md 轉一圈」（避免「行星 spinner」的 cyber slop）；是「在固定位置 settle，然後一起 fade」（更克制）
- ✅ Chrome A/C 在使命完成後體面退場（不是「永遠在畫面上」），這是「為下一幕讓位」的好習慣
- ✅ pause-and-look signature：23.40s 時 6 個 label 同時在畫面上，按順時針順序讀，是這部片唯一的「全 capability 全景」一幀——觀眾如果暫停在此處，能完整看到 6 條管道——這是 marketing 截圖的最佳 frame

**[WHY]**

這是一座橋。

ACT II 結束在 22.50s（NEW (06) 剛做完），但 slogan 還需要在 24.00s 才入場——中間這 1.5s 不能是「空白等待」，必須有 narrative motion。

「convergence」的概念：6 條管道做完後，所有 capability 收攏回 md 這個源頭。這正是這支片整個故事的 essence——**所有的流，最終都回到源**。

下一鏡，讓位給 slogan。md 字元縮小到 180px，準備成為 slogan 的「品牌印章」。

---

## SHOT 11 · "ONE SOURCE."

**[TIMECODE]** 24.00 — 26.50s (2.5s) `|` **FUNCTION** ACT III peak first half。slogan 上行入場。情緒 climax。

**[VISUAL]**

md 字元已縮小到 180px，停留在畫面中央（y=540）。

24.00s：md 字元**繼續向畫面 top-left 滑動**到 (x=128, y=88)，縮小到 56px——成為「品牌印章」固定在左上角。這是品牌的歸位。

24.20s：畫面中央偏上（y=460）開始浮現 hero slogan top line：

```
ONE SOURCE.
```

字型：Newsreader 700, **168px**, letter-spacing -0.03em, line-height 0.95, Ink #1A1A1A
位置：水平居中（x=960），y=460（character baseline）

入場方式：**staggered letter reveal**——10 個字元（O-N-E-space-S-O-U-R-C-E-.）按 30ms stagger 依次入場，每個字元 fade + 12px y slide-down + scale 0.92 → 1.0（260ms expoOut each）。

26.00s：在 slogan 下方 30px 出現一條短 Terracotta rule（320×3px），從中央向兩端展開（300ms expoOut）。

26.50s：進入下一鏡。

**[TYPE]**

- ONE SOURCE.：Newsreader 700, 168px, Ink, letter-spacing -0.03em, line-height 0.95
- terracotta rule: 320×3px, centered, accent

**[ANIM]**

- 24.00-24.30s · md 字元滑到 top-left（300ms expoOut，size 180 → 56）
- 24.20s · ONE SOURCE. 第一個字元 'O' 入場（260ms expoOut）
- 24.23s · 'N' 入場
- 24.26s · 'E' 入場
- 24.29s · space（無視覺，但 layout 佔位）
- 24.32s · 'S'
- 24.35s · 'O'
- 24.38s · 'U'
- 24.41s · 'R'
- 24.44s · 'C'
- 24.47s · 'E'
- 24.50s · '.'（句點）
- 24.20-25.00s · 整個 ONE SOURCE. 完成（10 字元 × 30ms stagger + 260ms each = total ~560ms）
- 25.00-26.00s · hold（讓觀眾讀「ONE SOURCE.」）
- 26.00-26.30s · Terracotta rule 出現（300ms expoOut from 0 → 320px）
- 26.30-26.50s · hold

**[AUDIO]**

- BGM: 22.00s 開始的 swell 在 24.50s 達到 peak（最響 -6dB）
- BGM: 整組絃樂進入（L5），cello + violin + viola 三層疊加
- **SFX: impact (slogan ONE) at 24.20s — deep bass impact + short reverb tail (-8dB)** ← 這是這支片最強的 SFX cue
- SFX: 極輕的 pen-on-paper stroke at 26.00s（rule 出現時, -22dB）

**[CHROME]**

- A: OFF (已退場)
- B: ON, 但**重要變化**：version chip 此時 cross-dissolve 成新形態——在右上角的同位置，但 chip 的尺寸略大，字級 18px（之前 16px），更突出。同時 Terracotta dot 的 pulse amplitude × 2（強調「v2.0 升級時刻」）
- C: OFF (已退場)
- D: ON
- E: ON

**新增 chrome**：
- md 字元（top-left, 56px, Newsreader 600 + Terracotta dot）正式入駐 corner，成為品牌印章

**[ANTI-SLOP]**

- ✅ slogan 不是「整詞 fade-in」（廉價），是 letter-by-letter stagger（電影級）
- ✅ 單字元的 stagger 時間 30ms 是經過計算的——足夠看到 cascade，但不會拖慢節奏（如果 60ms 就會顯慢）
- ✅ 字級 168px 是經過 layout 驗證的——再大會撞 SIX FORMS.（SHOT 12），再小則氣勢不夠
- ✅ pause-and-look signature：「ONE SOURCE.」末尾的「.」是 Terracotta（不是 Ink），呼應 hero md 字元的 Terracotta dot——首尾品牌簽名一致

**[WHY]**

這是 emotional climax 的第一半。

「ONE SOURCE.」是這部片的 thesis。如果觀眾看完整支片只記住一句話，就是這一句。

讓 md 字元在此刻退到 top-left 是策略性的——slogan 是主角，md 是品牌印章。兩者不搶戲。

下一鏡，SIX FORMS. 落下，thesis 完整。

---

## SHOT 12 · "SIX FORMS."

**[TIMECODE]** 26.50 — 29.00s (2.5s) `|` **FUNCTION** ACT III peak second half。slogan 下行 + capability map 完整呈現。整支片的 emotional resolution。

**[VISUAL]**

26.50s：ONE SOURCE. 仍在畫面上方位置（y=460）。

畫面下半部分（y=720）開始入場 hero slogan bottom line：

```
SIX FORMS.
```

字型：Newsreader 700, 168px, letter-spacing -0.03em, line-height 0.95, **Terracotta #C2410C**
位置：水平居中（x=960），y=720（character baseline）

入場方式：與 SHOT 11 鏡像——staggered letter reveal，9 個字元 + 1 個 .（共 10），每個 30ms stagger（更慢的 stagger 因為這是 climax）。

入場細節：每個字元是 fade + 12px y **slide-up**（而不是 SHOT 11 的 slide-down，方向對稱）+ scale 0.92 → 1.0（260ms expoOut each）。

27.20s：SIX FORMS. 完成，整個 slogan 雙行 typography 完整。

27.20-27.80s：在 SIX FORMS. 下方 30px 處，出現 6 個 capability pills，依次入場：

```
[any→md] [md→html] [html→md] [md→docx] [md→pdf ★NEW] [md→epub ★NEW]
```

每個 pill：
- 字型：JetBrains Mono Bold 14px, letter-spacing 0.16em
- 大小：10px×18px padding, 1.5px border
- 前 4 個：Ink text + Ink border + transparent background
- 後 2 個（NEW）：Terracotta text + Terracotta border + Mist (#FFF7F0) background + 右上角 -8/-10px 處 Terra Hot 「NEW」mini badge

每個 pill 間距 14px。整組水平居中（x=960），y=820。

入場：從左到右 staggered，每個 80ms delay，fade-in + 4px y slide-up (300ms expoOut)。

27.80-28.30s：副標行入場（y=890）：

```
md 是原始碼，萬物是產物。
```

字型：Noto Serif SC italic 26px, Ink, letter-spacing 0.04em
水平居中。

入場：fade-in + 8px y slide-up (400ms expoOut)。

28.30-29.00s：整體 hold。這是這部片最靜態的一幀——所有元素到位，讓觀眾"讀完它"。

**[TYPE]**

- SIX FORMS.：Newsreader 700, 168px, Terracotta, letter-spacing -0.03em, line-height 0.95
- pills：JetBrains Mono Bold 14px, letter-spacing 0.16em, 1.5px border
- 副標：Noto Serif SC italic 26px, Ink, letter-spacing 0.04em

**[ANIM]**

- 26.50-27.20s · SIX FORMS. 字元 stagger（同 SHOT 11 鏡像）
- 27.20-27.30s · short hold
- 27.30-27.80s · 6 pills cascade（每 80ms stagger × 6 = 480ms total + 300ms each pill duration）
- 27.80-28.30s · 副標入場（400ms）
- 28.30-29.00s · 整體 hold

**[AUDIO]**

- BGM: 26.50s peak swell 持續，至 27.20s 達到全片最響（-4dB）
- BGM: 27.20s 後 BGM 開始 sustain（不再增強，但保持 peak intensity）
- **SFX: impact (slogan SIX) at 26.50s — deep bass impact，比 ONE 鏡的 impact 稍重半音 (-7dB)**
- SFX: 6 個 pills 入場時 staggered metallic clicks（每個 -24dB, 50ms）
- SFX: 27.80s 極輕 pen flourish（副標入場）

**[CHROME]**

- B: ON, version chip 持續
- D: ON, watermark 持續
- E: ON
- md 印章 (top-left): ON

**[ANTI-SLOP]**

- ✅ ONE SOURCE. 是 Ink, SIX FORMS. 是 Terracotta——分別代表「源」和「物」的色彩對比，不是裝飾用色
- ✅ 6 pills 中 NEW 那兩個 background 是 #FFF7F0（極淡 mist tint），不是「橙色填充」——克制
- ✅ NEW mini badge 在 pill 的右上角 -8/-10px 突出位置，但只有 9px 字級——細節簽名的標準位置
- ✅ 副標用「，」中文逗號 + 句號「。」——是中文排版的尊重
- ✅ 這一幀（28.30s）是這支片的「marketing 用最完整一幀」——可以截圖作為 thumbnail / X 海報 / 公眾號封面圖，所有資訊都在一幀裡：slogan + 6 capability + 副標 + 品牌印章 + version

**[WHY]**

這是 resolution 鏡。

如果 SHOT 11 是 thesis（ONE SOURCE.），SHOT 12 就是 antithesis + synthesis（SIX FORMS. 加上完整 capability map）。

觀眾在這一幀 27.50s 時，應該一邊聽著絃樂 peak，一邊視覺上 fully absorbed by typography——這是這部片最值得的 5 秒。

下一鏡是收尾，讓絃樂 decay，讓 md 印章獨自閃耀。

---

## SHOT 13 · "SIGN-OFF"

**[TIMECODE]** 29.00 — 30.00s (1.0s) `|` **FUNCTION** 結尾。讓所有 slogan 元素退場，留下 md 印章獨自閃耀。品牌印記。

**[VISUAL]**

29.00s：SIX FORMS. + 6 pills + 副標開始 hold-in-place。

29.20-29.60s：ONE SOURCE. + SIX FORMS. + 6 pills + 副標緩慢 fade out（每個 400ms linear，**不要 stagger**，是同步淡出——形成「畫面在沉澱」的感覺）。

29.40s：top-left 的 md 印章字元從 56px 緩慢放大到 88px，同時位置從 (128, 88) 滑向畫面中央 (960, 540)——這是 md 的「最後迴歸」。

29.40-29.80s：md 字元在畫面中央 settle，size 88px, color Ink + Terracotta dot。

29.80-30.00s：md 字元下方 30px 出現一條短 Terracotta rule（120×2px，比 SHOT 03 短，更精緻），從 0 長成。

30.00s：所有元素到位。最後一幀是：

```
                                                                  ● HUASHU-MD-HTML · v2.0
                                                                                              (top-right chrome)


                                            md.                   ← Newsreader 600, 88px, Ink + Terracotta dot
                                          ───                     ← Terracotta rule, 120×2px

                                                                                CREATED BY HUASHU-DESIGN
                                                                                              (bottom-right watermark)
```

整個畫面只有 4 個元素：md 印章、accent rule、top-right chrome、bottom-right watermark。所有其他全空。

**[TYPE]**

- md.：Newsreader 600, 88px, Ink + Terracotta dot
- accent rule: 120×2px Terracotta

**[ANIM]**

- 29.00-29.20s · 上一鏡 hold（讓觀眾完整吸收）
- 29.20-29.60s · ONE SOURCE. + SIX FORMS. + 6 pills + 副標同步 fade out（400ms linear, 同步）
- 29.40-29.80s · md 印章放大 + 滑到中央（400ms expoOut, size 56 → 88, position (128,88) → (960,540)）
- 29.80-30.00s · accent rule 展開（200ms expoOut, 0 → 120px）
- 30.00s · final hold（如果有 loop，loop 回 00.00s）

**[AUDIO]**

- BGM: 29.00s 開始 decay 進入 L6（全部 layers 漸弱）
- BGM: 29.40s 絃樂 fade，留下 piano + reverb tail
- BGM: 30.00s, 一切歸於 silence + room tone
- **SFX: final stamp / sign-off at 29.40s（ink stamp + soft reverb, -14dB）**——md 落到中央時
- SFX: 極輕 paper rustle at 29.80s（accent rule 入場）

**[CHROME]**

- B: ON, 持續
- D: ON, 持續
- E: ON, 持續
- 其他全部 OFF

**[ANTI-SLOP]**

- ✅ 不用「Thank you」「Made with love」之類 sign-off 文字（廉價）
- ✅ 不用 logo 大放大（不需要）
- ✅ md 印章是這支片整個故事的真正主角，最後讓它獨自留在畫面中央，是 resolution 的最簡形式
- ✅ pause-and-look signature：最後一幀的 md. 在 88px Newsreader 字型下，Terracotta dot 是整個畫面的視覺焦點——觀眾的眼睛會自然停留在這個 dot 上，然後看到下方的 accent rule，再到 top-right 的 version chip。這條「視線動線」是 visual hierarchy 設計的成功
- ✅ silence 在最後 0.2s 給畫面留 breathing room

**[WHY]**

整部片始於一個空白頁面，終於一個 md 印章 + 一抹赤陶橙。

這是首尾呼應（visual rhyme）：
- 0.0s：blank ivory page（空）
- 30.0s：ivory page + md（滿）

觀眾從「空」走到「滿」，但「滿」其實只是一個 `md.` 字元——這就是「source-of-truth」的視覺宣言：**一切源於一個簡單的 md。**

如果整部片讓觀眾記住一幀，我希望是這一幀。

---

# Part V · Production Manifest

## 5.1 字型清單 + 載入方式

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400;1,500&family=JetBrains+Mono:wght@400;500;700&family=Noto+Serif+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
```

**實測載入時長**：約 800-1500ms 取決於 CDN 狀態。`document.fonts.ready` 等待必須等到 returns true 才啟動 Stage 計時器（Stage 已實現）。

## 5.2 色板 CSS 變數

```css
:root {
  --paper:       #FAFAF6;
  --mist:        #F2EDE4;
  --mica:        #E6E1D6;
  --smoke:       #6B6B6B;
  --cinder:      #3D3530;
  --ink:         #1A1A1A;
  --charred:     #2A2620;
  --terracotta:  #C2410C;
  --terra-hot:   #E55D21;
  --terra-deep:  #8B2D08;
}
```

## 5.3 BGM 來源選擇標準

**首選**：自己用 Suno v6.0 / Udio v1.5 生成 30 秒 cinematic minimal piece，prompt 關鍵詞：

```
minimal cinematic piano, slow tempo 60bpm, single piano notes,
sparse arpeggio, low cello drone, subtle sub-kick percussion,
swelling strings at climax, decay to silence,
in the style of Max Richter on the nature of daylight,
no vocals, 30 seconds duration, ivory paper mood
```

**備選**：搜尋免版權庫
- artlist.io: "minimal cinematic"
- bensound.com: "cinematic"
- musicbed.com: "Jóhann Jóhannsson style"

**最低標準**：BGM 30 秒長度，44.1kHz 取樣率，aim for -16 LUFS integrated loudness。

## 5.4 SFX 來源

**首選**：用 huashu-design skill 的 `assets/sfx/<category>/*.mp3` 37 個預製資源：

```
事件                          推薦 SFX 檔案
─────────────────────────────────────────────────────
keyboard clicks            sfx/ui/keyboard-click-*.mp3
cursor blink               sfx/ui/tick-soft.mp3
md morph swell             sfx/cinematic/whoosh-bloom.mp3
file card whoosh           sfx/cinematic/whoosh-short-*.mp3
absorb / ink drop          sfx/foley/ink-drop.mp3
paper rustle               sfx/foley/paper-turn.mp3
chime capability           sfx/melodic/chime-single-*.mp3
chime NEW (double)         sfx/melodic/chime-double-warm.mp3
build sweep                sfx/cinematic/ascending-sweep.mp3
impact (slogan)            sfx/cinematic/deep-impact-*.mp3
pen flourish               sfx/foley/pen-stroke.mp3
final stamp                sfx/foley/ink-stamp.mp3
```

## 5.5 截圖驗證計劃

實施 HTML 後必須驗證以下關鍵幀（用 Playwright + `?t=NN` URL 參數）：

```
t=0.5    ← SHOT 01 mid: blank ivory page (檢驗 paper texture 不搶戲)
t=2.5    ← SHOT 02 mid: typing in progress (檢驗 cursor blink + JetBrains Mono)
t=3.8    ← SHOT 03 mid: md morphing (檢驗 ghost residual + scale curve)
t=5.0    ← SHOT 03 end: hero md settled (檢驗 480px + Terracotta dot)
t=7.0    ← SHOT 04 mid: cards in flight (檢驗拋物線 + card 內容真實可讀)
t=8.4    ← SHOT 04 tagline (檢驗「萬物 → md」中文 italic)
t=10.5   ← SHOT 05 mid: html card complete (檢驗 essay 內容可讀)
t=13.5   ← SHOT 06 mid: md source visible (檢驗 syntax highlighting)
t=16.5   ← SHOT 07 mid: docx page complete (檢驗 chapter title + page number)
t=19.0   ← SHOT 08 mid: PDFs fanned out (檢驗 crop marks 可見)
t=21.5   ← SHOT 09 mid: EPUB frame complete (檢驗 Apple Books chrome)
t=23.4   ← SHOT 10 mid: 6 capability orbit (檢驗完整 capability 全景)
t=25.0   ← SHOT 11 mid: ONE SOURCE. complete (檢驗字距 + Terracotta period)
t=27.5   ← SHOT 12 mid: SIX FORMS. + pills (檢驗完整 slogan 雙行)
t=28.5   ← SHOT 12 marketing frame (檢驗整體 marketing-ready 一幀)
t=29.9   ← SHOT 13 final hold (檢驗 md 印章 + accent rule)
```

每幀必須滿足：
- 沒有元素溢位 1920×1080 canvas
- 字距、行高 visually correct
- 反 AI slop checklist 通過
- 關鍵 typography 細節（如 Terracotta dot, page number em-dash, chapter title small caps）可識別

## 5.6 錄製參數

```bash
node scripts/render-video.js \
  --file file:///path/to/v5-six-forms.html \
  --duration 30 \
  --fps 25 \
  --width 1920 \
  --height 1080 \
  --out v5-final-silent.mp4
```

**關鍵 codec 參數**：
- video codec: libx264
- pixel format: yuv420p (相容性)
- bitrate: 12 Mbps (high quality, 30s 檔案約 45MB)
- profile: high
- preset: slow (quality > speed)

**後續插幀**（可選，60fps 流暢版）：

```bash
bash scripts/convert-formats.sh v5-final-silent.mp4 --fps 60
```

## 5.7 音訊混合

```bash
# Step 1: 加 BGM
bash scripts/add-music.sh v5-final-silent.mp4 \
  --bgm assets/bgm/cinematic-minimal-30s.mp3 \
  --bgm-volume -18dB \
  --out v5-with-bgm.mp4

# Step 2: 加 SFX cues (按 Part II.6 SFX 字典逐 cue 加)
# 用 ffmpeg 的 -filter_complex amix 多路混合
ffmpeg -i v5-with-bgm.mp4 \
  -i assets/sfx/ui/keyboard-click-1.mp3 \
  -i assets/sfx/ui/keyboard-click-2.mp3 \
  ... \
  -filter_complex "[1]adelay=500|500[s1];[2]adelay=550|550[s2];...;[0][s1][s2]...amix=inputs=N:duration=longest:dropout_transition=0[out]" \
  -map 0:v -map "[out]" \
  -c:v copy -c:a aac -b:a 192k \
  v5-final.mp4

# Step 3: 驗證 audio stream
ffprobe -i v5-final.mp4 -show_streams -select_streams a 2>&1 | grep -E "(codec_type|sample_rate|channels|duration)"
```

**期望輸出**：
- audio codec: aac
- sample rate: 44100Hz or 48000Hz
- channels: 2 (stereo)
- duration: 30.0s

## 5.8 交付物清單

```
v5-final.mp4              主交付（30s, 1920×1080, 25fps, with audio, ~50MB）
v5-final-60fps.mp4        高幀率版（60fps 插幀, ~80MB, 用於 X / YouTube）
v5-final.gif              社交媒體版（30s, palette 最佳化, < 8MB, 用於公眾號嵌入）
v5-final-silent.mp4       靜音版（備份，方便後續重新配音/換 BGM）
v5-poster.png             海報版（截 t=28.5s 這一幀, 用於 X 卡片 / 公眾號封面）
v5-director-notes.md      本文件（導演筆記）
v5-six-forms.html         原始檔（HTML 動畫）
v5-shot-list.csv          shot 時間碼 + 關鍵參數對照表（pause 驗證用）
```

## 5.9 全鏈路時間估算

| 步驟 | 預計耗時 |
|-----|----------|
| Director's notes 撰寫 | 已完成 |
| HTML 動畫實施 | 4-6 小時 |
| 關鍵幀截圖 + 視覺校驗 | 1 小時 |
| 錄製無聲 MP4 | 5-10 分鐘（含 Playwright 啟動） |
| BGM 生成 / 選擇 | 30 分鐘 |
| SFX 配 cue + 混音 | 2-3 小時 |
| GIF 派生 | 5 分鐘 |
| 海報截圖 + 命名 | 10 分鐘 |
| 最終交付 + git 提交 | 10 分鐘 |
| **合計** | **8-11 小時** |

---

# 附錄 · 這部片的 first principle

如果我作為導演只能保留這部片的一句話，那就是：

> **一支關於「源頭」的 typographic film，主角是一個 `md.` 字元。**

所有其他設計決策——色板、字型、節奏、SFX、chrome、anti-slop checklist——都從這一句話推導而來。

如果某個具體決策無法 trace 回這一句話，就不要做。

---

*Director's notes — end of document*
*Total word count: 約 11500 中文字*
*Next: 使用者 review 通過後，進入 HTML 實施階段*
