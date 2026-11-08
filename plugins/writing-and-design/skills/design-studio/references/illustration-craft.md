# 插畫筆觸手冊

沒有照片時，畫面要靠插畫撐起來。插畫要有筆觸、明暗與材質，像在 Illustrator 用筆刷、點描、排線畫出來的感覺。只用等寬外框加平塗色塊的「著色本」畫法不合格。

可直接開啟的範例：`assets/illustration-techniques.html`，六格分別是反例、毛邊加明暗加顆粒、點描、排線、水彩暈染、乾筆。要用哪個技法，先打開範例看效果，再複製對應的 `<filter>` 或 `<pattern>`。

## 什麼都能畫

人物、人臉、手、動物、具名的真實產品、場景、室內、靜物都可以畫。品質要求只有兩條：

- **認得出來**：通過 `shared/composition-rules.md` 的三秒看懂測試。畫具名的真實產品時，照官方外觀的輪廓、比例與關鍵細節畫，讓認識這個產品的人一眼認得。
- **比例站得住**：人物先抓頭身比與五官位置，手先畫成手套形再分手指。畫完放大檢查一次。

## 每個物件至少三層

| 層 | 做法 |
|---|---|
| 底色 | 物件的固有色，用毛邊濾鏡讓邊緣像筆刷畫的 |
| 暗面 | 依固定光源（例如左上）在背光面疊一塊較深的色，或用點描、排線做陰影 |
| 亮面 | 受光處一筆較淺的高光，常用一道粗、圓頭、半透明的筆畫 |

再加上落在地面的影子，物件才會站在畫面裡。整份作品光源方向一致。

## 技法

### 毛邊（筆刷邊緣）

用雜訊把形狀邊緣推得不規則，像筆刷或剪紙。`scale` 越大越粗獷，3 到 8 之間最常用。

```html
<filter id="rough" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
</filter>
```

把整組物件包在 `<g filter="url(#rough)">` 裡，不要每個小形狀各套一次。

### 顆粒材質

只上在形狀內部的細顆粒，像粉彩、炭筆或紙的纖維。疊在物件上方，透明度 0.3 到 0.6。

```html
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="noise"/>
  <feColorMatrix in="noise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.4 1.1" result="speckle"/>
  <feComposite in="SourceGraphic" in2="speckle" operator="in"/>
</filter>
```

### 點描陰影

點的圖樣用漸層遮罩控制疏密，越暗的地方點越密。點的大小、間距、旋轉角度可以調整風格。

```html
<pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(30)">
  <circle cx="3.5" cy="3.5" r="1.6" fill="#3b2b1c"/>
</pattern>
<linearGradient id="shadeFade" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/>
  <stop offset="1" stop-color="#fff" stop-opacity="1"/>
</linearGradient>
<mask id="shadeMask"><rect width="100%" height="100%" fill="url(#shadeFade)"/></mask>
<!-- 用物件形狀當 clipPath，再鋪點 -->
<rect ... fill="url(#dots)" mask="url(#shadeMask)" clip-path="url(#objectClip)"/>
```

要更自然的點描（點的大小隨明暗變化、位置不規則），用小程式依明暗圖產生一批 `<circle>`，或在 canvas 上執行時畫點。點數超過幾千顆時改用 canvas。

### 排線陰影

同點描，把圖樣換成斜線。線的方向順著物件的曲面，暗處可以再疊一層交叉方向的線。排線群組再套一次毛邊，線條才不會像尺畫的。

```html
<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">
  <line x1="0" y1="0" x2="0" y2="6" stroke="#2c3a2e" stroke-width="1.6"/>
</pattern>
```

### 水彩暈染

形狀邊緣不規則、中間比邊緣淡，適合天空、霧、背景色塊。多層半透明疊在一起時，用 `mix-blend-mode: multiply` 讓顏色像顏料一樣加深。

```html
<filter id="wash" x="-20%" y="-20%" width="140%" height="140%">
  <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="4" seed="11" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="18" result="d"/>
  <feGaussianBlur in="d" stdDeviation="2.2" result="b"/>
  <feComposite in="b" in2="d" operator="arithmetic" k1="0" k2="0.55" k3="0.6" k4="0"/>
</filter>
```

### 乾筆筆畫

筆畫中間斷斷續續，像筆刷沾的顏料不夠。適合草、枝條、書法感的線、標題底下的強調筆。

```html
<filter id="drybrush" x="-5%" y="-20%" width="110%" height="140%">
  <feTurbulence type="fractalNoise" baseFrequency="0.06 0.6" numOctaves="2" seed="3" result="streak"/>
  <feColorMatrix in="streak" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.5" result="mask"/>
  <feComposite in="SourceGraphic" in2="mask" operator="in" result="broken"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="9" result="w"/>
  <feDisplacementMap in="broken" in2="w" scale="4"/>
</filter>
```

### 粗細變化的線

需要輪廓線時，不要用單一 `stroke-width` 從頭畫到尾。把線畫成填色的細長形狀（兩端尖、中段寬），或疊兩三條粗細不同、略微錯開的筆畫，再套毛邊。輪廓也可以只畫在暗面那一側，受光面讓它斷開。

## 怎麼選

| 方向 | 建議組合 |
|---|---|
| 水墨、山水 | 水彩暈染做霧與遠山，乾筆做近景枝葉，毛邊加淡彩做物件 |
| 銅版、雕版、復古印刷 | 排線或點描做全部陰影，墨色單色或雙色 |
| 繪本、溫暖生活感 | 毛邊加明暗三層加顆粒，色彩飽和一點 |
| 報紙、普普 | 大顆點描（半調網點）加粗輪廓 |
| 電影劇照感 | 水彩暈染做光與霧，顆粒材質疊全畫面，物件用明暗三層 |

整份作品選一種組合。可以在同一組合裡混用技法，例如物件用毛邊加明暗、背景用暈染。

## 效能與匯出

- 濾鏡很耗效能：同一個 `<filter>` 重複使用，套在群組上，`x/y/width/height` 只留需要的範圍。
- 匯出 PDF 時，套了濾鏡的區塊會被轉成點陣圖，檔案會變大。簡報要寄送時，把大面積的暈染改成預先算好的圖樣，或降低濾鏡範圍，匯出後檢查檔案大小。
- 大量點描也會讓 PDF 變大：每個 `<circle>` 都會被轉成多段曲線。用程式產生點時，把同一區的點合併成一條複合 `<path>`，點畫成不規則的小多邊形，畫面看不出差別，檔案可以小一半以上。
- 會動的畫面（捲動、動畫）避免每一幀重算濾鏡：動的是外層的 `transform` 與 `opacity`，濾鏡留在不動的內層。
- 大量點描、粒子與會流動的筆觸，改用 canvas 或 WebGPU（`webgpu-effects.md`）。

## 交付前檢查

- [ ] 每個主要物件都有底色、暗面、亮面，地面有影子
- [ ] 沒有只靠等寬外框加平塗的物件
- [ ] 整份作品光源方向一致、技法組合一致
- [ ] 人物、產品放大看過，比例與關鍵細節正確
- [ ] 三秒看懂測試通過
