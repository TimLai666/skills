# Gallery Ripple + Multi-Focus · 場景編排哲學

> 從 huashu-design hero 動畫 v9（25 秒，8 場景）裡提煉出的**一種可複用的視覺編排結構**。
> 不是動畫製作流水線，是**什麼場景下這種編排是"對的"**。
> 實戰參考：[https://www.huasheng.ai/huashu-design-hero/](https://www.huasheng.ai/huashu-design-hero/)

## 一句話先行

> **當你有 20+ 同質視覺素材、場景需要"表達規模感和深度"時，優先考慮 Gallery Ripple + Multi-Focus 這套編排，而不是堆砌排版。**

通用 SaaS feature 動畫、產品釋出會、skill 推廣、系列作品集展示——只要素材數量夠、風格一致，這套結構幾乎都能出效果。

---

## 這個手法究竟在表達什麼

不是"秀素材"——是通過**兩個節奏變化**講一個敘事：

**第一拍 · Ripple 展開（~1.5s）**：從中心向四周擴散出 48 張卡片，觀眾被"量"震住——「哦，這東西有這麼多產出」。

**第二拍 · Multi-Focus（~8s，4 次迴圈）**：鏡頭在慢速 pan 的同時，4 次把背景 dim + desaturate，把某一張卡單獨放大到螢幕中央——觀眾從"量的衝擊"切換到"質的凝視"，每次 1.7s 節奏穩定。

**核心敘事結構**：**規模（Ripple） → 凝視（Focus × 4） → 淡出（Walloff）**。這三拍組合起來表達的是「Breadth × Depth」——不只是能做很多，每一個還都值得停下來看。

對比一下反例：

| 做法 | 觀眾感知 |
|------|---------|
| 48 張卡靜態排列（沒有 Ripple）| 好看但無敘事，像一張 grid screenshot |
| 一張一張快切（沒有 Gallery context）| 像 slideshow，失去"規模感" |
| 只有 Ripple 沒有 Focus | 震住了但沒讓人記住任何具體一張 |
| **Ripple + Focus × 4（本配方）** | **先震撼於量，再凝視於質，最後平靜淡出——完整情緒弧線** |

---

## 前置條件（必須全部滿足）

這套編排**不是萬能的**，下面 4 條缺一不可：

1. **素材規模 ≥ 20 張，最好 30+**
   少於 20 張 Ripple 會顯得"空"——48 格里每格都在動才有密度感。v9 用了 48 格 × 32 張圖（迴圈填充）。

2. **素材視覺風格一致**
   全是 16:9 slide 預覽 / 全是 app 截圖 / 全是封面設計——長寬比、色調、版式得像是"一套"。混搭會讓 Gallery 看起來像剪貼簿。

3. **素材單獨放大後仍有可讀資訊**
   Focus 是把某張卡放大到 960px 寬，如果原圖放大後糊了或資訊稀薄，Focus 這一拍就廢了。反向驗證：能不能從 48 張裡挑出 4 張作為"最有代表性"的？挑不出來就說明素材質量不齊。

4. **場景本身是 landscape 或 square，不是直式**
   Gallery 的 3D 傾斜（`rotateX(14deg) rotateY(-10deg)`）需要橫向延伸感，直式會讓傾斜效果看起來窄且彆扭。

**缺條件的後備路徑**：

| 缺什麼 | 退化為什麼 |
|-------|-----------|
| 素材 < 20 張 | 改用「3-5 張並排靜態展示 + 逐個 focus」 |
| 風格不一致 | 改用「封面 + 3 章節大圖」的 keynote-style |
| 資訊稀薄 | 改用「data-driven dashboard」或「金句 + 大字」 |
| 直式場景 | 改用「vertical scroll + sticky cards」 |

---

## 技術配方（v9 實戰參數）

### 4-Layer 結構

```
viewport (1920×1080, perspective: 2400px)
  └─ canvas (4320×2520, 超大 overflow) → 3D tilt + pan
      └─ 8×6 grid = 48 cards (gap 40px, padding 60px)
          └─ img (16:9, border-radius 9px)
      └─ focus-overlay (absolute center, z-index 40)
          └─ img (matches selected slide)
```

**關鍵**：canvas 比 viewport 大 2.25 倍，這樣 pan 才有"窺視更大世界"的感覺。

### Ripple 展開（距離延遲演算法）

```js
// 每張卡的入場時間 = 距中心的距離 × 0.8s 延遲
const col = i % 8, row = Math.floor(i / 8);
const dc = col - 3.5, dr = row - 2.5;       // 到中心的 offset
const dist = Math.hypot(dc, dr);
const maxDist = Math.hypot(3.5, 2.5);
const delay = (dist / maxDist) * 0.8;       // 0 → 0.8s
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
const opacity = expoOut(Math.min(1, localT));
```

**核心參數**：
- 總時長 1.7s（`T.s3_ripple: [8.3, 10.0]`）
- 最大延遲 0.8s（中心最早出，角落最晚）
- 每張卡入場時長 0.7s
- Easing: `expoOut`（爆發感，不是平滑）

**同時做的事**：canvas scale 從 1.25 → 0.94（zoom out to reveal）—— 配合出現的同步推遠感。

### Multi-Focus（4 次節奏）

```js
T.focuses = [
  { start: 11.0, end: 12.7, idx: 2  },  // 1.7s
  { start: 13.3, end: 15.0, idx: 3  },  // 1.7s
  { start: 15.6, end: 17.3, idx: 10 },  // 1.7s
  { start: 17.9, end: 19.6, idx: 16 },  // 1.7s
];
```

**節奏規律**：每個 focus 1.7s，間隔 0.6s 喘息。總計 8s（11.0–19.6s）。

**每次 focus 內部**：
- In ramp: 0.4s（`expoOut`）
- Hold: 中間 0.9s（`focusIntensity = 1`）
- Out ramp: 0.4s（`easeOut`）

**背景變化（這是關鍵）**：

```js
if (focusIntensity > 0) {
  const dimOp = entryOp * (1 - 0.6 * focusIntensity);  // dim to 40%
  const brt = 1 - 0.32 * focusIntensity;                // brightness 68%
  const sat = 1 - 0.35 * focusIntensity;                // saturate 65%
  card.style.filter = `brightness(${brt}) saturate(${sat})`;
}
```

**不只是 opacity——同時 desaturate + darken**。這讓前景 overlay 的色彩"跳出來"，而不是隻是"變亮一點"。

**Focus overlay 尺寸動畫**：
- 從 400×225（入場）→ 960×540（hold 態）
- 外圍有 3 層 shadow + 3px accent 色 outline ring，呈現"被框住的感覺"

### Pan（持續感讓靜止不無聊）

```js
const panT = Math.max(0, t - 8.6);
const panX = Math.sin(panT * 0.12) * 220 - panT * 8;
const panY = Math.cos(panT * 0.09) * 120 - panT * 5;
```

- 正弦波 + 線性 drift 雙層運動——不是純迴圈，每個時刻位置都不同
- X/Y 頻率不同（0.12 vs 0.09）避免視覺上看出"規律迴圈"
- clamp 在 ±900/500px 防止漂出

**為什麼不用純線性 pan**：純線性觀眾會"預測"下一秒在哪；正弦+drift 讓每一秒都是新的，3D 傾斜下產生"微暈船感"（好的那種），注意力被拉住。

---

## 5 個可複用模式（從 v6→v9 迭代中蒸餾）

### 1. **expoOut 作為主 easing，不是 cubicOut**

`easeOut = 1 - (1-t)³`（平滑）vs `expoOut = 1 - 2^(-10t)`（爆發後迅速收斂）。

**選擇理由**：expoOut 的前 30% 很快達到 90%，更像物理阻尼，符合"重的東西落地"的直覺。特別適合：
- 卡片入場（重量感）
- Ripple 擴散（衝擊波）
- Brand 浮起（落定感）

**什麼時候仍用 cubicOut**：focus out ramp、對稱的微動效。

### 2. **紙感底色 + 赤陶橙 accent（Anthropic 血統）**

```css
--bg: #F7F4EE;        /* 暖紙 */
--ink: #1D1D1F;       /* 幾乎黑 */
--accent: #D97757;    /* 赤陶橙 */
--hairline: #E4DED2;  /* 暖線條 */
```

**為什麼**：溫暖底色在 GIF 壓縮後依然有"呼吸感"，不像純白會顯得"螢幕感"。赤陶橙作為唯一 accent 貫穿 terminal prompt、dir-card 選中、cursor、brand hyphen、focus ring——所有視覺錨點都被這一個色串起來。

**v5 教訓**：加了 noise overlay 以模擬"紙紋"，結果 GIF 幀壓縮全廢（每幀都不同）。v6 改為"只用底色 + 暖 shadow"，紙感保留 90%，GIF 體積縮小 60%。

### 3. **兩檔 Shadow 模擬深度，不用真 3D**

```css
.gallery-card.depth-near { box-shadow: 0 32px 80px -22px rgba(60,40,20,0.22), ... }
.gallery-card.depth-far  { box-shadow: 0 14px 40px -16px rgba(60,40,20,0.10), ... }
```

用 `sin(i × 1.7) + cos(i × 0.73)` 確定性演算法給每張卡分配 near/mid/far 三檔 shadow——**視覺上有"三維堆疊"感，但每幀 transform 完全不變，GPU 消耗 0**。

**真 3D 的代價**：每個 card 單獨 `translateZ`，GPU 每幀都在算 48 個 transform + shadow blur。v4 試過，Playwright 錄製 25fps 都吃力。v6 的兩檔 shadow 肉眼效果差距 <5%，但成本差 10 倍。

### 4. **字重變化（font-variation-settings）比字號變化更電影感**

```js
const wght = 100 + (700 - 100) * morphP;  // 100 → 700 over 0.9s
wordmark.style.fontVariationSettings = `"wght" ${wght.toFixed(0)}`;
```

Brand wordmark 從 Thin → Bold 用 0.9s 漸變，配合 letter-spacing 微調（-0.045 → -0.048em）。

**為什麼比放大縮小好**：
- 放大縮小觀眾看過太多，預期固化
- 字重變化是"內在的充實感"，像氣球被吹滿，而不是"被推近"
- variable fonts 是 2020+ 才普及的特性，觀眾下意識感覺"現代"

**限制**：必須用支援 variable font 的字型（Inter/Roboto Flex/Recursive 等）。普通靜態字型只能擬態（切換幾個固定 weight 有跳變）。

### 5. **Corner Brand 低強度持續簽名**

Gallery 階段左上角有個 `HUASHU · DESIGN` 小標識，16% opacity 色值，12px 字號，寬字距。

**為什麼加這個**：
- Ripple 爆發後觀眾容易"失焦"不記得在看什麼，左上角輕標示幫助 anchor
- 比全屏大 logo 更高階——做品牌的人知道，品牌簽名不需要喊
- 在 GIF 被截圖分享時仍留下歸屬訊號

**規則**：只在中段（畫面 busy）出現，開場關閉（不遮 terminal），結尾關閉（brand reveal 是主角）。

---

## 反例：什麼時候不要用這套編排

**❌ 產品演示（要展示功能的）**：Gallery 讓每一張都一閃而過，觀眾記不住任何一個功能。改用「單畫面 focus + tooltip 標註」。

**❌ 資料驅動內容**：觀眾要讀數字，Gallery 的快速節奏不給時間讀。改用「資料圖表 + 逐項 reveal」。

**❌ 故事敘事**：Gallery 是"並列"結構，故事需要"因果"。改用 keynote 章節切換。

**❌ 素材只有 3-5 張**：Ripple 密度不夠，看起來像"補丁"。改用「靜態排列 + 逐張高亮」。

**❌ 直式（9:16）**：3D tilt 需要橫向延伸，直式會讓傾斜感覺"歪"而不是"展開"。

---

## 如何判斷自己的任務適用這套編排

三步快速檢查：

**Step 1 · 素材數量**：數一下你有多少同類視覺素材。< 15 → 停；15-25 → 湊；25+ → 直接用。

**Step 2 · 一致性測試**：把 4 張隨機素材並排放，是否像「一套」？不像 → 先統一風格再做，或改方案。

**Step 3 · 敘事匹配**：你要表達的是「Breadth × Depth」（量 × 質）嗎？還是「流程」「功能」「故事」？不是前者就別硬套。

三步都 yes，直接 fork v6 HTML，改 `SLIDE_FILES` 陣列和時間軸就能複用。調色盤改 `--bg / --accent / --ink`，整體換皮不換骨。

---

## 相關 Reference

- 完整技術流程：[references/animations.md](animations.md) · [references/animation-best-practices.md](animation-best-practices.md)
- 動畫匯出流水線：[references/video-export.md](video-export.md)
- 音訊配置（BGM + SFX 雙軌）：[references/audio-design-rules.md](audio-design-rules.md)
- Apple 畫廊風格的橫向參考：[references/apple-gallery-showcase.md](apple-gallery-showcase.md)
- 源 HTML（v6 + 音訊整合版）：`www.huasheng.ai/huashu-design-hero/index.html`
