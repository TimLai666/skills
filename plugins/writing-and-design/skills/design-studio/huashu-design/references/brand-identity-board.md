# 品牌識別板（Brand Identity Board）· 從零打造品牌識別

> Curated from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) (MIT) 的 brandkit，改寫對接本 skill 的生圖與 HTML 流程。
>
> **適用邊界**：本檔管「**新品牌從零做識別**」——logo 概念、識別系統、單張品牌識別板。品牌**已存在**（有 logo、有官網）一律走 `shared/brand-asset.md` 資產協議，MUST NOT 用本檔重新發明人家的 logo。

## 產出物是什麼

一張「品牌識別板」：像正經識別工作室的提案板——網格分格、格間留溝、極少文字、一個品牌概念貫穿所有格。兩種實現：

| 形式 | 工具 | 適合 |
|------|------|------|
| AI 生圖單張板 | huashu 生圖流程（見文末 prompt 結構） | 快速提案、方向探索、發表會素材 |
| HTML 識別板 | 標準流程 + `react-setup.md` | 要精確排版、可迭代、可匯出 PDF |

預設版型 `3×3`（完整識別系統）或 `2×3`（迷你 deck），比例 4:3 或 16:10。

## 第一步 · 品牌策略先行

生任何視覺之前，先推出品牌策略：品類、受眾、產品功能、情感承諾、信任層級、核心隱喻、這個品牌該避免什麼。**視覺系統必須從意義推導**，不是從風格庫抽。

| 品類 | 核心概念 | 符號邏輯候選 |
|------|---------|-------------|
| 開發者工具 | 建造、速度、精準、掌控 | 游標、框架、閃電、鷹架、網格 |
| AI 助理 | 委派、智慧、清晰 | 火花、軌道、訊號、路徑、節點 |
| 資安 | 保護、警戒、邊界 | 盾、眼、封印、被保護的核心 |
| 語音 AI | 聲音、節奏、指令、流動 | 波形、麥克風、球體、語音路徑 |
| 法遵／信任 | 秩序、規則、保護 | 封印、徽章、文件、盾 |
| 無人機／機器人 | 飛行、控制、視野、任務 | 翼、貓頭鷹、十字準星、航線 |
| 奢侈品／編輯 | 品味、材質、儀式、克制 | 花押字、封蠟、紙、壓印 |
| 生產力 | 專注、動能、清晰 | 路徑、勾選、方塊、光 |

符號不能隨機挑——挑不出「為什麼是它」的符號就換。

## 第二步 · Logo 概念法（五選一，最多合併兩種）

1. **字母 + 隱喻**：品牌首字母融合一個隱喻（`K`+風箏、`S`+聲波、`A`+攀升）。用負空間、切割、摺疊、幾何——不要做無聊的字母 icon。
2. **產品動作**：把產品的核心動作變成符號（build→鷹架／游標、protect→邊界／盾、speak→波形、automate→迴圈／交棒）。抽象而高級，不要太字面。
3. **隱喻融合**：兩個有意義的概念融成一個精簡符號（貓頭鷹+無人機視野、盾+山、月+波形、游標+閃電）。融合要含蓄但讀得出來。
4. **負空間**：用留白製造聰明感（隱藏箭頭、被保護的中心、挖空字母、摺角、交疊成形的眼）。負空間邊緣要俐落。
5. **幾何構成**：從明確系統長出來的 mark（圓、斜切、網格、模組方塊、軌道、十字準星）。可以留一格展示構成邏輯。

**Logo 品質底線**：簡單、可記、可縮放、可擁有（ownable）、與品牌概念相連，能同時當 icon／wordmark／徽章／UI mark／pattern。好 logo 看起來像「研究後的減法」，不是靈光一閃的裝飾。

## 板面構成節奏

板不是九宮格填空——是有節奏的策展序列：**安靜 → 功能 → 情感 → 技術 → 氛圍 → 細節**。不要每格一樣大聲。

### 3×3 預設格配置

1. **Logo 封面**——大 logo + wordmark，強負空間
2. **Logo 構成**——幾何拆解、網格、負空間邏輯，回答「這個 mark 為什麼存在」
3. **數位應用**——瀏覽器 chrome、app header、終端機、app icon
4. **品牌精髓**——一句 tagline，大字，極簡構圖
5. **色彩系統**——色票、色盤卡、材質 chip
6. **字型**——大型字樣、字母列、主副字型配對
7. **實體應用**——名片、徽章、海報、標籤、封蠟、包裝
8. **影像方向**——電影感風景、halftone 海報、材質特寫、editorial 場景
9. **系統細節**——UI chip、輸入列、icon 列、pattern 局部

### 2×3 迷你 deck 配置

Logo/wordmark → 產品表面（瀏覽器列／輸入框） → 功能格（終端機／install 指令） → 氛圍影像 → 符號構成／徽章 → tagline。

## 視覺模式速查

模式決定全板氣質；細部色彩與字型從 `design-styles.md` 40 風格庫對應條目取，不要另起爐灶：

| 模式 | 適用品牌 | 視覺要素 | 對應風格庫方向 |
|------|---------|---------|---------------|
| 暗色開發者 | dev tools、infra、coding agent | 近黑面板、等寬字、終端機、青／珊瑚 accent | 大膽・技術系 |
| 暗色資安 | 資安、監控、網路 | 黑／深藍、盾形、雷達線、紅藍警示 chip | 大膽・冷峻系 |
| 淺色信任 | 法務、法遵、文件 | 暖象牙、紙紋、小襯線標籤、封印徽章 | 安靜・出版系 |
| 奢侈編輯 | 美妝、時尚、旅宿 | 象牙／石灰／espresso、襯線 wordmark、壓印 | 安靜・奢華系 |
| 語音溝通 | voice AI、助理 | 深靛、丁香紫光、波形、手機裁切 | 中性・柔和系 |
| 文化實驗 | 音樂、創作工具、活動 | halftone、CRT、印刷質感、海報格 | 大膽・復古系 |

## 色彩紀律

一個主色盤走完全板：底色 + 主 accent + 副 accent + 中性色。規則：

- accent 必須跨格重複出現（一個 accent 可以撐起整個系統）
- 不出現隨機彩虹；不用通用紫藍 AI 光暈（除非品牌真的是）
- 參考組合：黑+青+霧珊瑚、森林綠+萊姆+霧灰、象牙+深藍+紅+金、黑+丁香紫、炭灰+白+淡藍

## 文字與標語

**極少文字**。允許：品牌名、一句 tagline、一個 URL、一條指令、2-5 個區段標籤、短 UI chip。禁止：長段落、假內文、選單堆疊、lorem ipsum。

Tagline 要短而具體（"Nothing random."、"Your network. Our watch."、"Build better."），不要通用企業口號與 buzzword 湯。

## 影像與 Mockup 方向

- 影像要像 art-directed：電影感山景、暮色、halftone 雲、暗色產品特寫、有情緒的建築。避免：通用 stock 人像、辦公室照、機器人陳腔。影像必須貼合色盤與隱喻。
- Mockup 是**識別應用，不是功能 demo**：瀏覽器 chrome、URL 列、終端機、app icon、卡片堆、徽章、資料夾、輸入列。避免塞滿假資料的完整 dashboard。

## 品牌專屬反通用規則

通用禁區走 `../../shared/anti-slop.md`（含 AI Tells）。以下是品牌識別特有的：

- ❌ 假貴族徽章／crest（沒有歷史的品牌裝什麼百年老店）
- ❌ 隨機動物（動物必須來自符號邏輯表的推導）
- ❌ 抄知名 mark 的形（會被認出來，也不可擁有）
- ❌ 同一板上 logo 變體不一致（icon／wordmark／徽章必須同一套幾何）
- ❌ 無意義光點與 sparkle（「AI 感」的最廉價寫法）

**與 AI Tells 的邊界**：小頁碼、角落小標籤、構成輔助線在**識別板上是體裁慣例**（識別 deck 本來就長這樣），允許節制使用；同樣的元素放到**網站／landing page 上**仍然是 AI Tells 禁區。體裁決定合法性，不要跨界套用。

## 生圖 prompt 結構（AI 生圖路徑用）

```
Create a premium brand-kit overview image for "<品牌名>".
Brand strategy: category / audience / personality / core metaphor / logo idea（符號如何連結品牌意義）
Layout: <3×3 / 2×3> grid on a <dark/light> presentation canvas, strong gutters, refined negative space
Panels: <從上面格配置挑>
Visual mode: <模式> · Palette: <紀律色盤>
Style: premium, sparse, cinematic, intentional, brand-guidelines deck, no clutter, no copied real-world logos
Logo: professional, symbolic, simple, ownable, repeated consistently across panels
```

生完跑一遍自檢：logo 跨格一致？accent 有重複？文字夠少？每格能答「它在板上的敘事角色是什麼」？答不出的格重生。
