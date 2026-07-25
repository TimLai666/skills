# Content Guidelines：反AI slop、內容準則、Scale規範

AI設計裡最容易掉進去的陷阱。這是一份「不做什麼」的清單，比「做什麼」更重要——因為AI slop是預設值，你不主動避免就會發生。

## AI Slop 完整黑名單

### 視覺陷阱

**❌ 激進漸變背景**
- 紫色 → 粉色 → 藍色 全屏漸變（AI生成網頁的典型味道）
- 任何方向的rainbow gradient
- Mesh gradient鋪滿背景
- ✅ 如果要用漸變：subtle、單色系、有意圖地點綴（比如button hover）

**❌ 圓角卡片 + 左border accent色**
```css
/* 這是AI味卡片的典型簽名 */
.card {
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  padding: 16px;
}
```
這種卡片在AI生成的Dashboard裡氾濫。想做強調？用更有設計感的方式：背景色對比、字重/字號對比、plain分隔線、或者乾脆不分卡片。

**❌ Emoji 裝飾**
除非品牌本身使用emoji（比如Notion、Slack），否則不要在UI上放emoji。**尤其不要**：
- 標題前的 🚀 ⚡️ ✨ 🎯 💡
- Feature列表的 ✅
- CTA按鈕裡的 →（箭頭單獨出現OK，emoji箭頭不行）

沒圖示用真icon庫（Lucide/Heroicons/Phosphor），或者用placeholder。

**❌ SVG 畫 imagery**
不要試圖用SVG畫：人物、場景、裝置、物品、抽象藝術。AI畫的SVG imagery一眼就是AI味，幼稚且廉價。**一個灰色矩形+"插畫位 1200×800"的文字標籤，比一個拙劣的SVG hero illustration強100倍**。

唯一可以用SVG的場景：
- 真正的icon（16×16到32×32級別）
- 幾何圖形做裝飾元素
- Data viz的chart

**❌ 過多iconography**
不是每個標題/feature/section都需要icon。濫用icon會讓介面像toy。Less is more。

**❌ "Data slop"**
編造的stats裝飾：
- "10,000+ happy customers" （你都不知道有沒有）
- "99.9% uptime" （沒有真資料就別寫）
- 用圖示+數字+片語成的裝飾"metric cards"
- Mock table裡的假資料裝點得花裡胡哨

如果沒真資料，留placeholder或問使用者要。

**❌ "Quote slop"**
編造的使用者評價、名人名言裝飾頁面。留placeholder問使用者要真quote。

### 字型陷阱

**❌ 避免這些爛大街字型**：
- Inter（AI生成的網頁預設）
- Roboto
- Arial / Helvetica
- 純system font stack
- Fraunces（AI發現了這個就用濫了）
- Space Grotesk（最近AI的最愛）

**✅ 用有特點的display+body配對**。靈感方向：
- 襯線display + 無襯線body（editorial feel）
- Mono display + sans body（technical feel）
- Heavy display + light body（contrast）
- Variable font做hero的粗細動畫

字型資源：
- Google Fonts的冷門好選項（Instrument Serif、Cormorant、Bricolage Grotesque、JetBrains Mono）
- 開源字型站（Fraunces的兄弟字型、Adobe Fonts）
- 不要憑空發明字型名

### 色彩陷阱

**❌ 憑空發明顏色**
不要從頭設計一整套不熟悉的色彩。這通常不和諧。

**✅ 策略**：
1. 有品牌色 → 用品牌色，缺的color token用oklch插值
2. 沒有品牌色但有參考 → 從參考產品截圖吸色
3. 完全從零 → 選一個known的配色系統（Radix Colors / Tailwind預設palette / Anthropic brand），不要自己調

**oklch定義色彩**是最現代的做法：
```css
:root {
  --primary: oklch(0.65 0.18 25);      /* 溫暖的terracotta */
  --primary-light: oklch(0.85 0.08 25); /* 同色系淺色 */
  --primary-dark: oklch(0.45 0.20 25);  /* 同色系深色 */
}
```
oklch能保證調整亮度時色相不漂移，比hsl好用。

**❌ 夜間模式隨手加反色**
不是簡單invert顏色。好的dark mode需要重新調整飽和度、對比度、accent色。不想做dark mode就別做。

### Layout陷阱

**❌ Bento grid 過度氾濫**
每個AI生成的landing page都想搞bento。除非你的資訊structure確實適合bento，否則用其他layout。

**❌ 大hero + 3-column features + testimonials + CTA**
這個landing page模板被用爛了。想創新就真創新。

**❌ Card grid裡每個card長一樣**
Asymmetric、不同大小的cards、有的帶image有的只有文字、有的跨列——這才像真設計師做的。

## 內容準則

### 1. Don't add filler content

每個元素都必須earn its place。空白是設計問題，用**構圖**解決（對比、節奏、留白），**不是**靠內容填滿。

**判斷filler的問題**：
- 如果去掉這段內容，設計會變差嗎？答案若是"不會"，就去掉。
- 這個元素解決了什麼真問題？如果是"讓頁面不那麼空"，刪掉。
- 這個stats/quote/feature有真資料支援嗎？沒有就不要憑空寫。

「One thousand no's for every yes」。

### 2. Ask before adding material

你覺得多加一段/一頁/一個section會更好？先問使用者，不要單方面加。

原因：
- 使用者知道他的受眾比你清楚
- 加內容有成本，使用者可能不想要
- 單方面加內容違反了"junior designer彙報工作"的關係

### 3. Create a system up front

探索完design context後，**先口頭說出你要用的系統**，讓使用者確認：

```markdown
我的設計系統：
- 色彩：#1A1A1A主體 + #F0EEE6背景 + #D97757 accent（來自你的品牌）
- 字型：Instrument Serif做display + Geist Sans做body
- 節奏：section title用full-bleed彩色背景 + 白字；普通section用白背景
- 影像：hero用full-bleed照片，feature section用placeholder等你提供
- 最多用2種背景色，避免雜亂

確認這個方向我就開始做。
```

使用者確認後再動手。這個check-in能避免"做完一半發現方向錯"。

## Scale 規範

### 幻燈片（1920×1080）

- 正文最小 **24px**，理想 28-36px
- 標題 60-120px
- Section title 80-160px
- Hero headline 可以用 180-240px 的大字
- 永遠不要用 <24px 的字放幻燈片

### 印刷文件

- 正文最小 **10pt**（≈13.3px），理想 11-12pt
- 標題 18-36pt
- Caption 8-9pt

### Web和移動端

- 正文最小 **14px**（老年人友好用16px）
- 移動端正文 **16px**（避免iOS自動縮放）
- Hit target（可點選元素）最小 **44×44px**
- 行高 1.5-1.7（中文1.7-1.8）

### 對比度

- 正文 vs 背景 **至少 4.5:1**（WCAG AA）
- 大字 vs 背景 **至少 3:1**
- 用Chrome DevTools的accessibility工具檢查

## CSS 神器

**高階CSS特性**是設計師的好朋友，大膽用：

### 排版

```css
/* 讓標題換行更自然，不會最後一行孤單單一個詞 */
h1, h2, h3 { text-wrap: balance; }

/* 正文換行，避免寡孀和孤兒 */
p { text-wrap: pretty; }

/* 中文排版神器：標點擠壓、行首行尾控制 */
p { 
  text-spacing-trim: space-all;
  hanging-punctuation: first;
}
```

### Layout

```css
/* CSS Grid + named areas = 可讀性爆表 */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
}

/* Subgrid對齊卡片內容 */
.card { display: grid; grid-template-rows: subgrid; }
```

### 視覺效果

```css
/* 有設計感的捲軸 */
* { scrollbar-width: thin; scrollbar-color: #666 transparent; }

/* 玻璃擬態（克制使用） */
.glass {
  backdrop-filter: blur(20px) saturate(150%);
  background: color-mix(in oklch, white 70%, transparent);
}

/* View transitions API讓頁面切換絲滑 */
@view-transition { navigation: auto; }
```

### 互動

```css
/* :has()選擇器讓條件樣式變容易 */
.card:has(img) { padding-top: 0; } /* 有圖片的卡片無頂padding */

/* container queries讓元件真的響應式 */
@container (min-width: 500px) { ... }

/* 新的color-mix函式 */
.button:hover {
  background: color-mix(in oklch, var(--primary) 85%, black);
}
```

## 決策速查：當你猶豫時

- 想加個漸變？→ 大機率不加
- 想加個emoji？→ 不加
- 想給卡片加圓角+border-left accent？→ 不加，換其他方式
- 想用SVG畫個hero插畫？→ 不畫，用placeholder
- 想加一段quote裝飾？→ 先問使用者有沒有真quote
- 想加一排icon features？→ 先問要不要icon，可能不需要
- 用Inter？→ 換一個更有特點的
- 用紫色漸變？→ 換一個有根據的配色

**當你覺得"加一下會更好看"的時候——那通常是AI slop的徵兆**。先做最簡的版本，只在使用者要求時加。
