# Animation Best Practices · 正向動畫設計語法

> 基於 Anthropic 官方三支產品動畫（Claude Design / Claude Code Desktop / Claude for Word）
> 的深度拆解，提煉出的"Anthropic 級"動畫設計規則。
>
> 配套 `animation-pitfalls.md`（避坑清單）使用——本檔案是「**應該這樣做**」，
> pitfalls 是「**不要這樣做**」，兩者正交，都要讀。
>
> **約束宣告**：本檔案只收錄**運動邏輯和表達風格**，**不引入任何品牌色具體色值**。
> 色彩決策走 §1.a 核心資產協議（從品牌 spec 抽取）或「設計方向顧問」
> （20 種哲學各自的配色方案）。本 reference 討論的是「**怎麼動**」，不是「**什麼色**」。

---

## §0 · 你是誰 · 身份與品味

> 在讀後面任何技術規則之前，先讀這一節。規則是**從身份湧現的**——
> 不是相反。

### §0.1 身份錨點

**你是一個研究過 Anthropic / Apple / Pentagram / Field.io 運動檔案的 motion designer。**

做動畫時，你不是在調 CSS transition——你是在用數字元素**模擬一個物理世界**，
讓觀眾的潛意識相信「這是有重量、有慣性、會溢位的物體」。

你不做 PowerPoint 式動畫。你不做「fade in fade out」動畫。你做的動畫**讓人相信螢幕
是一個可以伸手進去的空間**。

### §0.2 核心信念（3 條）

1. **動畫是物理學，不是動畫曲線**
   `linear` 是數字，`expoOut` 是物體。你相信螢幕上的畫素值得被當作"物體"對待。
   每一條 easing 的選擇，都是在回答「這個元素有多重？摩擦係數多大？」的物理問題。

2. **時間分配比曲線形狀更重要**
   Slow-Fast-Boom-Stop 是你的呼吸。**均勻節奏的動畫是技術演示，有節奏的動畫是敘事。**
   在正確的時刻慢下來——比在錯誤的時刻用對 easing 更重要。

3. **禮讓觀眾，比炫技更難**
   關鍵結果前停 0.5 秒是**技術**，不是妥協。**讓人類大腦有反應時間，是動畫師的最高素養。**
   AI 預設會做一個沒有停頓的、資訊密度滿格的動畫——那是新手。你要做的是克制。

### §0.3 品味標準 · 什麼是美

你對「好」和「great」的判斷標準如下。每一條都有**識別方法**——當你看到一個候選動畫時，
用這些問題判斷它是否達標，而不是機械對照 14 條規則。

| 美的維度 | 識別方法（觀眾反應） |
|---|---|
| **物理重量感** | 動畫結束時，元素"**落**"得穩——不是"**停**"在那裡。觀眾潛意識覺得"這有重量" |
| **禮讓觀眾** | 關鍵資訊出現前有一個可感的 pause（≥300ms）——觀眾來得及"**看見**"再繼續 |
| **留白** | 收尾是戛然而止 + hold，不是 fade to black。最後一幀清晰、肯定、有決定感 |
| **克制** | 全片只有一處「120% 精緻」，其餘 80% 恰到好處——**到處炫技是廉價的訊號** |
| **手感** | 弧線（不是直線）、不規律（不是 setInterval 的機械節奏）、有呼吸感 |
| **敬意** | 展示 tweak 的過程、展示 bug 的修復——**不藏工作、不給"魔法"**。AI 是協作者不是魔術師 |

### §0.4 自檢 · 觀眾第一反應法

做完一支動畫，**觀眾看完第一反應是什麼？**——這是你唯一要最佳化的指標。

| 觀眾反應 | 評級 | 診斷 |
|---|---|---|
| "看起來挺流暢的" | good | 合格但無特色，你在做 PowerPoint |
| "這個動畫真順" | good+ | 技術對了，但沒驚豔 |
| "這個東西看起來真的像**從桌面上浮起來的**" | great | 你觸到了物理重量感 |
| "這不像是 AI 做的" | great+ | 你觸到了 Anthropic 的門檻 |
| "我想**截圖**發朋友圈" | great++ | 你做到了讓觀眾主動傳播 |

**great 和 good 的區別，不在於技術正確度，在於品味判斷**。技術正確 + 品味對 = great。
技術正確 + 品味空 = good。技術錯誤 = 沒入門。

### §0.5 身份和規則的關係

下面 §1-§8 的技術規則，是這套身份在具體場景的**執行手段**——不是獨立規則清單。

- 遇到規則沒覆蓋的場景 → 回到 §0，用**身份**判斷，不要瞎猜
- 遇到規則之間有衝突 → 回到 §0，用**品味標準**判斷哪條更重要
- 想破一條規則 → 先回答："這樣做符合 §0.3 哪一條美？" 答得上就破，答不上就別破

好。繼續讀下去。

---

## 總覽 · 動畫是物理學的三層展開

大多數 AI 生成動畫有廉價感的根源是——**它們表現得像「數字」不是「物體」**。
真實世界的物體有質量、有慣性、有彈性、會溢位。Anthropic 三支片子的「高階感」根源，
就在於給數字元素一套**物理世界的運動規則**。

這套規則有 3 個層次：

1. **敘事節奏層**：Slow-Fast-Boom-Stop 的時間分配
2. **運動曲線層**：Expo Out / Overshoot / Spring，拒絕 linear
3. **表達語言層**：展示過程、滑鼠弧線、Logo 形變收束

---

## 1. 敘事節奏 · Slow-Fast-Boom-Stop 5 段結構

Anthropic 三支片子無一例外遵循這個結構：

| 段 | 佔比 | 節奏 | 作用 |
|---|---|---|---|
| **S1 觸發** | ~15% | 慢 | 給人類反應時間，建立真實感 |
| **S2 生成** | ~15% | 中 | 視覺驚豔點出現 |
| **S3 過程** | ~40% | 快 | 展示可控性/密度/細節 |
| **S4 爆發** | ~20% | Boom | 鏡頭拉遠/3D pop-out/多面板湧現 |
| **S5 落幅** | ~10% | 靜 | 品牌 Logo + 戛然而止 |

**具體時長對映**（15 秒動畫為例）：
S1 觸發 2s · S2 生成 2s · S3 過程 6s · S4 爆發 3s · S5 落幅 2s

**禁止做的事**：
- ❌ 均勻節奏（每秒資訊密度一樣）— 觀眾疲勞
- ❌ 持續高密度 — 無峰值無記憶點
- ❌ 漸弱收尾（fade out 到透明）— 應該**戛然而止**

**自檢**：用紙筆畫 5 個 thumbnail，每個代表一段的高潮畫面。如果 5 張圖差別不大，
說明節奏沒做出來。

---

## 2. Easing 哲學 · 拒絕 linear，擁抱物理

Anthropic 三支片子的所有動效都用帶「阻尼感」的貝塞爾曲線。預設的 cubic easeOut
（`1-(1-t)³`）**不夠銳**——起步不夠快、停頓不夠穩。

### 三個核心 Easing（animations.jsx 已內建）

```js
// 1. Expo Out · 迅速啟動緩慢剎車（最常用，預設主 easing）
// 對應 CSS: cubic-bezier(0.16, 1, 0.3, 1)
Easing.expoOut(t) // = t === 1 ? 1 : 1 - Math.pow(2, -10 * t)

// 2. Overshoot · 帶彈性的 toggle/按鈕彈出
// 對應 CSS: cubic-bezier(0.34, 1.56, 0.64, 1)
Easing.overshoot(t)

// 3. Spring 物理 · 幾何體歸位、自然落位
Easing.spring(t)
```

### 用法對映

| 場景 | 用哪個 Easing |
|---|---|
| 卡片 rise-in / 面板入場 / Terminal fade / focus overlay | **`expoOut`**（主 easing，最常用） |
| Toggle 切換 / 按鈕彈出 / 強調互動 | `overshoot` |
| Preview 幾何體歸位 / 物理落位 / UI 元素抖彈 | `spring` |
| 持續運動（如滑鼠軌跡插值） | `easeInOut`（保留對稱性） |

### 反直覺洞察

大多數產品宣傳片的動畫**太快太硬**。`linear` 讓數字元素像機器，`easeOut` 是基礎分，
`expoOut` 才是「高階感」的技術根源——它給數字元素一種**物理世界的重量感**。

---

## 3. 運動語言 · 8 條共性原則

### 3.1 底色不用純黑純白

Anthropic 三支片子沒有一支用 `#FFFFFF` 或 `#000000` 做主底色。**帶色溫的中性色**
（或暖或冷）有"紙張 / 畫布 / 桌面"的物質感，削弱機器感。

**具體色值決策**走 §1.a 核心資產協議（從品牌 spec 抽取）或「設計方向顧問」
（20 種哲學各自的底色方案）。本 reference 不給具體色值——那是**品牌決策**，不是運動規則。

### 3.2 Easing 絕不是 linear

見 §2。

### 3.3 Slow-Fast-Boom-Stop 敘事

見 §1。

### 3.4 展示「過程」而非「魔法結果」

- Claude Design 展示 tweak 參數、拖滑塊（不是一鍵生成完美結果）
- Claude Code 展示程式碼報錯 + AI 修復（不是一次成功）
- Claude for Word 展示 Redline 紅刪綠增的修改過程（不是直接給最終稿）

**共同潛台詞**：產品是**協作者、結對工程師、資深編輯**——不是一鍵魔術師。
這精準打擊專業使用者對「可控性」和「真實性」的痛點。

**反 AI slop**：AI 預設會做「魔法一鍵成功」的動畫（一鍵生成 → 完美結果），
這是通用公約數。**反過來做**——展示過程、展示 tweak、展示 bug 和修復——
是品牌識別度的來源。

### 3.5 滑鼠軌跡人工繪製（弧線 + Perlin Noise）

真人滑鼠運動不是直線，是「起步加速 → 弧線 → 減速修正 → 點選」。
AI 直接直線插值的滑鼠軌跡**有潛意識排斥感**。

```js
// 二次貝塞爾曲線插值（起點 → 控制點 → 終點）
function bezierQuadratic(p0, p1, p2, t) {
  const x = (1-t)*(1-t)*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0];
  const y = (1-t)*(1-t)*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1];
  return [x, y];
}

// 路徑：起點 → 偏離中點 → 終點（做弧線）
const path = [[100, 100], [targetX - 200, targetY + 80], [targetX, targetY]];

// 再疊加極小的 Perlin Noise（±2px）製造「手抖」
const jitterX = (simpleNoise(t * 10) - 0.5) * 4;
const jitterY = (simpleNoise(t * 10 + 100) - 0.5) * 4;
```

### 3.6 Logo「形變收束」(Morph)

Anthropic 三支片子的 Logo 出場**都不是簡單 fade-in**，是**前一個視覺元素形變而來**。

**共同模式**：倒數 1-2 秒做 Morph / Rotate / Converge，讓整個敘事在品牌點上「坍縮」。

**低成本實現**（不用真 morph）：
讓前一個視覺元素「坍縮」成一個色塊（scale → 0.1，向中心 translate），
色塊再「膨脹」展開成 wordmark。過渡用 150ms 快切 + motion blur
（`filter: blur(6px)` → `0`）。

```js
<Sprite start={13} end={14}>
  {/* 坍縮：前一個元素 scale 0.1，opacity 保持，filter blur 增加 */}
  const scale = interpolate(t, [0, 0.5], [1, 0.1], Easing.expoOut);
  const blur = interpolate(t, [0, 0.5], [0, 6]);
</Sprite>
<Sprite start={13.5} end={15}>
  {/* 膨脹：Logo 從色塊中心 scale 0.1 → 1，blur 6 → 0 */}
  const scale = interpolate(t, [0, 0.6], [0.1, 1], Easing.overshoot);
  const blur = interpolate(t, [0, 0.6], [6, 0]);
</Sprite>
```

### 3.7 襯線 + 無襯線雙字型

- **品牌 / 旁白**：襯線（有「學術感 / 出版物感 / 品位」）
- **UI / 程式碼 / 資料**：無襯線 + 等寬

**單一字型都是不對的**。襯線給「品位」，無襯線給「功能」。

具體字型選擇走品牌 spec（brand-spec.md 的 Display / Body / Mono 三棧）或設計方向
顧問的 20 種哲學。本 reference 不給具體字型——那是**品牌決策**。

### 3.8 焦點切換 = 背景減弱 + 前景銳化 + Flash 引導

焦點切換**不只是**降低 opacity。完整配方是：

```js
// 非焦點元素的濾鏡組合
tile.style.filter = `
  brightness(${1 - 0.5 * focusIntensity})
  saturate(${1 - 0.3 * focusIntensity})
  blur(${focusIntensity * 4}px)        // ← 關鍵：加 blur 才真的"退後"
`;
tile.style.opacity = 0.4 + 0.6 * (1 - focusIntensity);

// 焦點完成後在焦點位置做 150ms Flash highlight 引導視線迴流
focusOverlay.animate([
  { background: 'rgba(255,255,255,0.3)' },
  { background: 'rgba(255,255,255,0)' }
], { duration: 150, easing: 'ease-out' });
```

**為什麼 blur 是必須的**：只靠 opacity + brightness，焦點外的元素還是「銳利」的，
視覺上沒有「退到後景」的效果。blur(4-8px) 讓非焦點真的退一層景深。

---

## 4. 具體運動技巧（可直接抄的程式碼片段）

### 4.1 FLIP / Shared Element Transition

按鈕「膨脹」成輸入框，**不是**按鈕消失 + 新面板出現。核心是**同一個 DOM 元素**在
兩種狀態間 transition，不是兩個元素 cross-fade。

```jsx
// 用 Framer Motion layoutId
<motion.div layoutId="design-button">Design</motion.div>
// ↓ 點選後同 layoutId
<motion.div layoutId="design-button">
  <input placeholder="Describe your design..." />
</motion.div>
```

原生實現參考 https://aerotwist.com/blog/flip-your-animations/

### 4.2「呼吸式」展開（width→height）

面板展開**不是同時拉 width 和 height**，而是：
- 前 40% 時間：只拉 width（保持 height 小）
- 後 60% 時間：width 保持，撐 height

這模擬物理世界「先展開，再注水」的感覺。

```js
const widthT = interpolate(t, [0, 0.4], [0, 1], Easing.expoOut);
const heightT = interpolate(t, [0.3, 1], [0, 1], Easing.expoOut);
style.width = `${widthT * targetW}px`;
style.height = `${heightT * targetH}px`;
```

### 4.3 Staggered Fade-up（30ms stagger）

表格行、卡片列、列表項入場時，**每個元素延遲 30ms**，`translateY` 從 10px 回到 0。

```js
rows.forEach((row, i) => {
  const localT = Math.max(0, t - i * 0.03);  // 30ms stagger
  row.style.opacity = interpolate(localT, [0, 0.3], [0, 1], Easing.expoOut);
  row.style.transform = `translateY(${
    interpolate(localT, [0, 0.3], [10, 0], Easing.expoOut)
  }px)`;
});
```

### 4.4 非線性呼吸 · 關鍵結果前懸停 0.5s

機器執行快且連貫，但**關鍵結果出現前懸停 0.5 秒**，讓觀眾大腦有反應時間。

```jsx
// 典型場景：AI 生成完 → 懸停 0.5s → 結果浮現
<Sprite start={8} end={8.5}>
  {/* 0.5s 停頓——什麼也不動，讓觀眾盯著載入狀態 */}
  <LoadingState />
</Sprite>
<Sprite start={8.5} end={10}>
  <ResultAppear />
</Sprite>
```

**反例**：AI 生成完立刻無縫切到結果——觀眾沒反應時間，資訊流失。

### 4.5 Chunk Reveal · 模擬 token 流式

AI 生成文字**不要用 `setInterval` 單字元蹦出**（像老電影字幕），要用 **chunk reveal**
——一次出現 2-5 個字元，間隔不規律，模擬真實 token 流式輸出。

```js
// 分 chunk 而不是分字元
const chunks = text.split(/(\s+|,\s*|\.\s*|;\s*)/);  // 按詞 + 標點切
let i = 0;
function reveal() {
  if (i >= chunks.length) return;
  element.textContent += chunks[i++];
  const delay = 40 + Math.random() * 80;  // 不規律 40-120ms
  setTimeout(reveal, delay);
}
reveal();
```

### 4.6 Anticipation → Action → Follow-through

Disney 12 原則中的 3 條。Anthropic 用得很顯式：

- **Anticipation**（預備）：動作開始前有小反向動作（按鈕輕微縮小再彈出）
- **Action**（動作）：主要動作本身
- **Follow-through**（跟隨）：動作結束後有餘韻（卡片落位後輕微 bounce）

```js
// 卡片入場的完整三段
const anticip = interpolate(t, [0, 0.2], [1, 0.95], Easing.easeIn);     // 預備
const action  = interpolate(t, [0.2, 0.7], [0.95, 1.05], Easing.expoOut); // 主動
const settle  = interpolate(t, [0.7, 1], [1.05, 1], Easing.spring);       // 回彈
// 最終 scale = 三段乘積或分段應用
```

**反例**：只有 Action 沒有 Anticipation + Follow-through 的動畫，像「PowerPoint 動畫」。

### 4.7 3D Perspective + translateZ 分層

想要「傾斜 3D + 懸浮卡片」的氣質，給容器加 perspective，給單個元素不同的 translateZ：

```css
.stage-wrap {
  perspective: 2400px;
  perspective-origin: 50% 30%;  /* 視線略俯視 */
}
.card-grid {
  transform-style: preserve-3d;
  transform: rotateX(8deg) rotateY(-4deg);  /* 黃金比例 */
}
.card:nth-child(3n) { transform: translateZ(30px); }
.card:nth-child(5n) { transform: translateZ(-20px); }
.card:nth-child(7n) { transform: translateZ(60px); }
```

**為什麼 rotateX 8° / rotateY -4° 是黃金比例**：
- 大於 10° → 元素扭曲感過強，看起來像「倒下」
- 小於 5° → 像「錯切」而不是「透視」
- 8° × -4° 的非對稱比例模擬「鏡頭在桌面左上角俯視」的 natural angle

### 4.8 斜向 Pan · 同時動 XY

鏡頭運動不是純上下或純左右，而是**同時動 XY** 模擬斜向移動：

```js
const panX = Math.sin(flowT * 0.22) * 40;
const panY = Math.sin(flowT * 0.35) * 30;
stage.style.transform = `
  translate(-50%, -50%)
  rotateX(8deg) rotateY(-4deg)
  translate3d(${panX}px, ${panY}px, 0)
`;
```

**關鍵**：X 和 Y 的頻率不同（0.22 vs 0.35），避免 Lissajous 迴圈規則化。

---

## 5. 場景配方（三種敘事模板）

參考材料裡三支影片對應三種產品性格。**選一種最貼合你的產品**，不要混搭。

### 配方 A · Apple Keynote 戲劇式（Claude Design 類）

**適合**：大版本釋出、hero 動畫、視覺驚豔優先
**節奏**：Slow-Fast-Boom-Stop 強弧線
**Easing**：全程 `expoOut` + 少量 `overshoot`
**SFX 密度**：高（~0.4/s），SFX 音高調到 BGM 音階
**BGM**：IDM / 極簡科技電子，冷靜+精密
**收束**：鏡頭急拉遠 → drop → Logo 形變 → 空靈單音 → 戛然而止

### 配方 B · 一鏡到底工具式（Claude Code 類）

**適合**：開發者工具、生產力 App、心流場景
**節奏**：持續穩定 flow，沒有明顯峰值
**Easing**：`spring` 物理 + `expoOut`
**SFX 密度**：**0**（純靠 BGM 驅動剪輯節奏）
**BGM**：Lo-fi Hip-hop / Boom-bap，85-90 BPM
**核心技巧**：關鍵 UI 動作踩在 BGM kick/snare 瞬態上——「**音樂律動即互動音效**」

### 配方 C · 辦公效率敘事式（Claude for Word 類）

**適合**：企業軟體、文件/表格/日曆類、專業感優先
**節奏**：多 scene 硬切 + Dolly In/Out
**Easing**：`overshoot`（toggle）+ `expoOut`（面板）
**SFX 密度**：中（~0.3/s），UI click 為主
**BGM**：Jazzy Instrumental，小調，BPM 90-95
**核心亮點**：某一幕必有「全片高光」—— 3D pop-out / 脫離平面浮起

---

## 6. 反例 · 這樣做就是 AI slop

| 反 pattern | 為什麼錯 | 正確做法 |
|---|---|---|
| `transition: all 0.3s ease` | `ease` 是 linear 的親戚，所有元素同速 | 用 `expoOut` + 分元素 stagger |
| 所有入場都 `opacity 0→1` | 沒有運動方向感 | 配合 `translateY 10→0` + Anticipation |
| Logo 淡入 | 沒有敘事收束感 | Morph / Converge / 坍縮-展開 |
| 滑鼠直線移動 | 潛意識機器感 | 貝塞爾弧線 + Perlin Noise |
| 打字單字蹦出（setInterval） | 像老電影字幕 | Chunk Reveal，隨機間隔 |
| 關鍵結果無懸停 | 觀眾沒反應時間 | 結果前 0.5s 懸停 |
| 焦點切換隻改 opacity | 非焦點元素還銳利 | opacity + brightness + **blur** |
| 純黑底 / 純白底 | 賽博感 / 反光疲勞 | 帶色溫的中性色（走品牌 spec） |
| 所有動畫同樣快 | 無節奏 | Slow-Fast-Boom-Stop |
| Fade out 收尾 | 無決定感 | 戛然而止（hold 最後一幀） |

---

## 7. 自檢清單（動畫交付前 60 秒）

- [ ] 敘事結構是 Slow-Fast-Boom-Stop，不是均勻節奏？
- [ ] 預設 easing 是 `expoOut`，不是 `easeOut` 或 `linear`？
- [ ] Toggle / 按鈕彈出用了 `overshoot`？
- [ ] 卡片 / 列表入場有 30ms stagger？
- [ ] 關鍵結果前有 0.5s 懸停？
- [ ] 打字用 Chunk Reveal，不是 setInterval 單字？
- [ ] 焦點切換加了 blur（不只是 opacity）？
- [ ] Logo 是形變收束（Morph），不是淡入？
- [ ] 底色不是純黑 / 純白（帶色溫）？
- [ ] 文字有襯線 + 無襯線層次？
- [ ] 收尾是戛然而止，不是漸弱？
- [ ] （有滑鼠的話）滑鼠軌跡是弧線，不是直線？
- [ ] SFX 密度符合產品性格（見配方 A/B/C）？
- [ ] BGM 和 SFX 有 6-8dB 響度差？（見 `audio-design-rules.md`）

---

## 8. 與其他 reference 的關係

| reference | 定位 | 關係 |
|---|---|---|
| `animation-pitfalls.md` | 技術避坑（16 條） | 「**不要這樣做**」· 本檔案的反面 |
| `animations.md` | Stage/Sprite 引擎用法 | 動畫**怎麼寫**的基礎 |
| `audio-design-rules.md` | 雙軌制音訊規則 | 動畫**配音訊**的規則 |
| `sfx-library.md` | 37 個 SFX 清單 | 音效**素材庫** |
| `apple-gallery-showcase.md` | Apple 畫廊展示風格 | 一種特定運動風格的專題 |
| **本檔案** | 正向運動設計語法 | 「**應該這樣做**」 |

**呼叫順序**：
1. 先看 GUIDE.md 工作流程 Step 3 的form推導五問（決定敘事角色和視覺溫度）
2. 選定方向後讀本檔案確定**運動語言**（配方 A/B/C）
3. 寫程式碼時參考 `animations.md` 和 `animation-pitfalls.md`
4. 匯出影片時走 `audio-design-rules.md` + `sfx-library.md`

---

## 附錄 · 本檔案素材來源

- Anthropic 官方動畫拆解：花叔專案目錄的 `參考動畫/BEST-PRACTICES.md`
- Anthropic 音訊拆解：同目錄 `AUDIO-BEST-PRACTICES.md`
- 3 支參考影片：`ref-{1,2,3}.mp4` + 對應 `gemini-ref-*.md` / `audio-ref-*.md`
- **嚴格過濾**：本 reference 不收錄任何具體品牌色值、字型名、產品名。
  色彩/字型決策走 §1.a 核心資產協議或 20 種設計哲學。
