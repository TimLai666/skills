# Apple Gallery Showcase · 畫廊展示牆動畫風格

> 靈感來源：Claude Design 官網 hero 影片 + 蘋果產品頁「作品牆」式陳列
> 實戰出處：huashu-design 發布 hero v5
> 適用場景：**產品發布 hero 動畫、skill 能力演示、作品集展示**——任何需要把「多件高品質產出」同時展陳並引導觀眾注意力的場景

---

## 觸發判斷：什麼時候用這個風格

**適合**：
- 有10張以上真實產出要同一畫面展示（PPT、App、網頁、資訊圖）
- 觀眾是專業受眾（開發者、設計師、產品經理），對「質感」敏感
- 希望傳遞的氣質是「克制、展覽式、高級、有空間感」
- 需要焦點和整體同時存在（看細節但不失整體）

**不適合**：
- 單產品聚焦（用 frontend-design 的產品 hero 模板）
- 情緒向/故事性強的動畫（用時間軸敘事模板）
- 小螢幕 / 直式（傾斜視角在小畫面上會糊）

---

## 核心視覺 Token

```css
:root {
  /* 淺色畫廊調板 */
  --bg:         #F5F5F7;   /* 主畫布底 — 蘋果官網灰 */
  --bg-warm:    #FAF9F5;   /* 溫暖米白變體 */
  --ink:        #1D1D1F;   /* 主字色 */
  --ink-80:     #3A3A3D;
  --ink-60:     #545458;
  --muted:      #86868B;   /* 次級文字 */
  --dim:        #C7C7CC;
  --hairline:   #E5E5EA;   /* 卡片1px邊框 */
  --accent:     #D97757;   /* 赤陶橙 — Claude brand */
  --accent-deep:#B85D3D;

  --serif-cn: "Noto Serif SC", "Songti SC", Georgia, serif;
  --serif-en: "Source Serif 4", "Tiempos Headline", Georgia, serif;
  --sans:     "Inter", -apple-system, "PingFang SC", system-ui;
  --mono:     "JetBrains Mono", "SF Mono", ui-monospace;
}
```

**關鍵原則**：
1. **絕不用純黑底**。黑底會讓作品看起來像電影、不像「可以被採用的工作成果」
2. **赤陶橙是唯一色相accent**，其他全部是灰階 + 白
3. **三字型棧**（serif英+serif中+sans+mono）營造「出版物」而非「網際網路產品」的氣質

---

## 核心佈局模式

### 1. 懸浮卡片（整個風格的基本單元）

```css
.gallery-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 6px;                          /* 內邊距是「裝裱紙」 */
  border: 1px solid var(--hairline);
  box-shadow:
    0 20px 60px -20px rgba(29, 29, 31, 0.12),   /* 主陰影，軟且長 */
    0 6px 18px -6px rgba(29, 29, 31, 0.06);     /* 第二層近光，製造浮感 */
  aspect-ratio: 16 / 9;                  /* 統一 slide 比例 */
  overflow: hidden;
}
.gallery-card img {
  width: 100%; height: 100%;
  object-fit: cover;
  border-radius: 9px;                    /* 比卡片圓角略小，視覺巢狀 */
}
```

**反面教材**：不要貼邊瓷磚（無padding無border無shadow）——那是資訊圖密度表達，不是展覽。

### 2. 3D傾斜作品牆

```css
.gallery-viewport {
  position: absolute; inset: 0;
  overflow: hidden;
  perspective: 2400px;                   /* 深一些的透視，傾斜不誇張 */
  perspective-origin: 50% 45%;
}
.gallery-canvas {
  width: 4320px;                         /* 畫布 = 2.25× viewport */
  height: 2520px;                        /* 留出pan空間 */
  transform-origin: center center;
  transform: perspective(2400px)
             rotateX(14deg)              /* 向後傾 */
             rotateY(-10deg)             /* 向左轉 */
             rotateZ(-2deg);             /* 輕微傾斜，去掉太規整 */
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 40px;
  padding: 60px;
}
```

**參數 sweet spot**：
- rotateX: 10-15deg（再多就像開酒會 VIP 背景板）
- rotateY: ±8-12deg（左右對稱感）
- rotateZ: ±2-3deg（「這不是機器擺的」的人味）
- perspective: 2000-2800px（小於2000會魚眼，大於3000接近正投影）

### 3. 2×2 四角匯聚（選擇場景）

```css
.grid22 {
  display: grid;
  grid-template-columns: repeat(2, 800px);
  gap: 56px 64px;
  align-items: start;
}
```

每張卡片從對應角落（tl/tr/bl/br）向中心滑入 + fade in。對應的 `cornerEntry` 向量：

```js
const cornerEntry = {
  tl: { dx: -700, dy: -500 },
  tr: { dx:  700, dy: -500 },
  bl: { dx: -700, dy:  500 },
  br: { dx:  700, dy:  500 },
};
```

---

## 五種核心動畫模式

### 模式 A · 四角匯聚（0.8-1.2s）

4 個元素從視口四角滑入，同時縮放 0.85→1.0，對應 ease-out。適合「展示多方向選擇」的開場。

```js
const inP = easeOut(clampLerp(t, start, end));
card.style.transform = `translate3d(${(1-inP)*ce.dx}px, ${(1-inP)*ce.dy}px, 0) scale(${0.85 + 0.15*inP})`;
card.style.opacity = inP;
```

### 模式 B · 選中放大 + 其他滑出（0.8s）

被選中的卡片放大 1.0→1.28，其他卡片 fade out + blur + 向四角漂回：

```js
// 被選中
card.style.transform = `translate3d(${cellDx*outP}px, ${cellDy*outP}px, 0) scale(${1 + 0.28*easeOut(zoomP)})`;
// 未選中
card.style.opacity = 1 - outP;
card.style.filter = `blur(${outP * 1.5}px)`;
```

**關鍵**：未選中的要 blur，不是純 fade。blur 模擬景深，視覺上把被選中的「推出來」。

### 模式 C · Ripple 漣漪展開（1.7s）

從中心向外，按距離 delay，每張卡片依次淡入 + 從 1.25x 縮到 0.94x（「鏡頭拉遠」）：

```js
const col = i % COLS, row = Math.floor(i / COLS);
const dc = col - (COLS-1)/2, dr = row - (ROWS-1)/2;
const dist = Math.sqrt(dc*dc + dr*dr);
const delay = (dist / maxDist) * 0.8;
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
card.style.opacity = easeOut(Math.min(1, localT));

// 同時整體 scale 1.25→0.94
const galleryScale = 1.25 - 0.31 * easeOut(rippleProgress);
```

### 模式 D · Sinusoidal Pan（持續漂移）

用正弦波 + 線性漂移組合，避免 marquee 那種「有起點有終點」的迴圈感：

```js
const panX = Math.sin(panT * 0.12) * 220 - panT * 8;    // 橫向左漂
const panY = Math.cos(panT * 0.09) * 120 - panT * 5;    // 縱向上漂
const clampedX = Math.max(-900, Math.min(900, panX));   // 防止露邊
```

**參數**：
- 正弦週期 `0.09-0.15 rad/s`（慢，約30-50秒一個擺動）
- 線性漂移 `5-8 px/s`（比觀眾眨眼慢）
- 振幅 `120-220 px`（大到能感覺，小到不會暈）

### 模式 E · Focus Overlay（焦點切換）

**關鍵設計**：focus overlay 是一個**平面元素**（不傾斜），浮在傾斜畫布之上。被選中的 slide 從瓦片位置（約400×225）縮放到螢幕中央（960×540），背景畫布不傾斜變化但**變暗到 45%**：

```js
// Focus overlay (flat, centered)
focusOverlay.style.width = (startW + (endW - startW) * focusIntensity) + 'px';
focusOverlay.style.height = (startH + (endH - startH) * focusIntensity) + 'px';
focusOverlay.style.opacity = focusIntensity;

// 背景卡片變暗，但依然可見（關鍵！不要100%遮罩）
card.style.opacity = entryOp * (1 - 0.55 * focusIntensity);   // 1 → 0.45
card.style.filter = `brightness(${1 - 0.3 * focusIntensity})`;
```

**清晰度鐵律**：
- Focus overlay 的 `<img>` 必須 `src` 直連原圖，**不要複用 gallery 裡的壓縮縮圖**
- 提前 preload 所有原圖到 `new Image()[]` 陣列
- overlay 自身 `width/height` 按幀計算，瀏覽器每幀 resample 原圖

---

## 時間軸架構（可複用骨架）

```js
const T = {
  DURATION: 25.0,
  s1_in: [0.0, 0.8],    s1_type: [1.0, 3.2],  s1_out: [3.5, 4.0],
  s2_in: [3.9, 5.1],    s2_hold: [5.1, 7.0],  s2_out: [7.0, 7.8],
  s3_hold: [7.8, 8.3],  s3_ripple: [8.3, 10.0],
  panStart: 8.6,
  focuses: [
    { start: 11.0, end: 12.7, idx: 2  },
    { start: 13.3, end: 15.0, idx: 3  },
    { start: 15.6, end: 17.3, idx: 10 },
    { start: 17.9, end: 19.6, idx: 16 },
  ],
  s4_walloff: [21.1, 21.8], s4_in: [21.8, 22.7], s4_hold: [23.7, 25.0],
};

// 核心 easing
const easeOut = t => 1 - Math.pow(1 - t, 3);
const easeInOut = t => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2;
function lerp(time, start, end, fromV, toV, easing) {
  if (time <= start) return fromV;
  if (time >= end) return toV;
  let p = (time - start) / (end - start);
  if (easing) p = easing(p);
  return fromV + (toV - fromV) * p;
}

// 單一 render(t) 函式讀時間戳、寫所有元素
function render(t) { /* ... */ }
requestAnimationFrame(function tick(now) {
  const t = ((now - startMs) / 1000) % T.DURATION;
  render(t);
  requestAnimationFrame(tick);
});
```

**架構精髓**：**所有狀態由時間戳 t 推導**，沒有狀態機、沒有 setTimeout。這樣：
- 播放到任意時刻 `window.__setTime(12.3)` 立刻跳轉（方便 playwright 逐幀截）
- 迴圈天然無縫（t mod DURATION）
- Debug 時能凍結任意一幀

---

## 質感細節（容易被忽略但致命）

### 1. SVG noise texture

淺色底最怕「太平」。疊加一層極弱的 fractalNoise：

```html
<style>
.stage::before {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.078  0 0 0 0 0.078  0 0 0 0 0.074  0 0 0 0.035 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  opacity: 0.5;
  pointer-events: none;
  z-index: 30;
}
</style>
```

看上去沒區別，去掉就知道有了。

### 2. 角落品牌標識

```html
<div class="corner-brand">
  <div class="mark"></div>
  <div>HUASHU · DESIGN</div>
</div>
```

```css
.corner-brand {
  position: absolute; top: 48px; left: 72px;
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
}
```

只在作品牆 scene 顯示，淡入淡出。像美術館展籤。

### 3. 品牌收束 wordmark

```css
.brand-wordmark {
  font-family: var(--sans);
  font-size: 148px;
  font-weight: 700;
  letter-spacing: -0.045em;   /* 負字距是關鍵，讓字緊湊成標誌 */
}
.brand-wordmark .accent {
  color: var(--accent);
  font-weight: 500;           /* accent字元反而細一點，視覺差 */
}
```

`letter-spacing: -0.045em` 是蘋果產品頁大字的標準做法。

---

## 常見失敗模式

| 症狀 | 原因 | 解法 |
|---|---|---|
| 看起來像 PPT 模板 | 卡片沒有 shadow / hairline | 加上兩層 box-shadow + 1px border |
| 傾斜感廉價 | 只用了 rotateY 沒加 rotateZ | 加 ±2-3deg rotateZ 打破工整 |
| Pan 感覺「卡頓」 | 用了 setTimeout 或 CSS keyframes 迴圈 | 用 rAF + sin/cos 連續函式 |
| Focus 時字看不清 | 複用了 gallery 瓦片的低解析度圖 | 獨立 overlay + 原圖 src 直連 |
| 背景太空 | 純色 `#F5F5F7` | 疊加 SVG fractalNoise 0.5 opacity |
| 字型太"網際網路" | 只有 Inter | 加 Serif（中英各一）+ mono 三棧 |

---

## 引用

- 完整實現樣本：hero-animation-v5.html（作者本地樣本，未隨倉庫分發）
- 原始靈感：claude.ai/design hero 影片
- 參考審美：Apple 產品頁、Dribbble shot 集合頁

遇到「多件高品質產出要陳列」的動畫需求，直接從此檔案 copy 骨架，換內容 + 調 timing 即可。
