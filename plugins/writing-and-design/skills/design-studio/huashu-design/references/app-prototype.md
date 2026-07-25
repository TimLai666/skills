# App / iOS 原型專屬守則 · 完整操作手冊

> 從 GUIDE.md 下沉的完整版。GUIDE.md 保留 7 條硬規則速查，本檔案是每條規則的展開：架構選型、取圖渠道與程式碼、AppPhone JSX 骨架、ios_frame 三步用法、品位錨點全表。


做 iOS/Android/移動 app 原型時（觸發：「app 原型」「iOS mockup」「移動應用」「做個 app」），下面四條**覆蓋**通用 placeholder 原則——app 原型是 demo 現場，靜態擺拍和米白佔位卡沒有說服力。

### 0. 架構選型（必先決定）

**預設單檔案 inline React**——所有 JSX/data/styles 直接寫進主 HTML 的 `<script type="text/babel">...</script>` 標籤，**不要**用 `<script src="components.jsx">` 外部載入。原因：`file://` 協議下瀏覽器把外部 JS 當跨 origin 攔截，強制使用者起 HTTP server 違反「雙擊就能開」的原型直覺。引用本地圖片必須 base64 內嵌 data URL，別假設有 server。

**拆外部檔案只在兩種情況**：
- (a) 單檔案 >1000 行難維護 → 拆成 `components.jsx` + `data.js`，同時明確交付說明（`python3 -m http.server` 命令 + 訪問 URL）
- (b) 需要多 subagent 並行寫不同屏 → `index.html` + 每屏獨立 HTML（`today.html`/`graph.html`...），iframe 聚合，每屏也都是自包含單檔案

**選型速查**：

| 場景 | 架構 | 交付方式 |
|------|------|----------|
| 單人做 4-6 屏原型（主流） | 單檔案 inline | 一個 `.html` 雙擊開 |
| 單人做大型 App（>10 屏） | 多 jsx + server | 附啟動命令 |
| 多 agent 並行 | 多 HTML + iframe | `index.html` 聚合，每屏獨立可開 |

### 1. 先找真圖，不是 placeholder 擺著

預設主動去取真實圖片填充，不要畫 SVG、不要拿米白卡擺著、不要等使用者要求。常用渠道：

| 場景 | 首選渠道 |
|------|---------|
| 美術/博物館/歷史內容 | Wikimedia Commons（公共領域）、Met Museum Open Access、Art Institute of Chicago API |
| 通用生活/攝影 | Unsplash、Pexels（免版權） |
| 使用者本地已有素材 | `~/Downloads`、專案 `_archive/` 或使用者配置的素材庫 |

Wikimedia 下載避坑（本機 curl 走代理 TLS 會炸，Python urllib 直接走得通）：

```python
# 合規 User-Agent 是硬性要求，否則 429
UA = 'ProjectName/0.1 (https://github.com/you; you@example.com)'
# 用 MediaWiki API 查真實 URL
api = 'https://commons.wikimedia.org/w/api.php'
# action=query&list=categorymembers 批次拿系列 / prop=imageinfo+iiurlwidth 取指定寬度 thumburl
```

**只有**當所有渠道都失敗 / 版權不清 / 使用者明確要求時，才退回誠實 placeholder（仍然不畫爛 SVG）。

**真圖誠實性測試**（關鍵）：取圖之前先問自己——「如果去掉這張圖，資訊是否有損？」

| 場景 | 判斷 | 動作 |
|------|------|------|
| 文章/Essay 列表的封面、Profile 頁的風景頭圖、設定頁的裝飾 banner | 裝飾，與內容無內在關聯 | **不要加**。加了就是 AI slop，等同紫色漸變 |
| 博物館/人物內容的肖像、產品詳情的實物、地圖卡片的地點 | 內容本身，有內在關聯 | **必須加** |
| 圖譜/視覺化背景的極淡紋理 | 氛圍，服從內容不搶戲 | 加，但 opacity ≤ 0.08 |

**反例**：給文字 Essay 配 Unsplash「靈感圖」、給筆記 App 配 stock photo 模特——都是 AI slop。取真圖的許可不等於濫用真圖的通行證。

### 2. 交付形態：預設「平鋪 + 可操作」，不要問使用者

iOS App 原型的**預設交付形態就一種，不要再問使用者「要平鋪還是可操作」**：**平鋪 4-6 個主介面，且每一台都能互動**。一眼看全貌（多台 iPhone 並排），又每台都能點 tab 切換、在介面上做基本操作（展開、切換、選中、開啟彈層）。兩個好處一次給齊，別讓使用者二選一。

| 維度 | 預設做法 |
|------|---------|
| **畫面數** | 平鋪 **4-6 個主介面**（覆蓋 app 的核心功能面，不是隨便擺幾個）。多於 6 個抓最主要的 4-6 個，其餘可在單台內通過 tab/導航到達 |
| **佈局** | 多台獨立 iPhone 橫向 `flexWrap` 並排，每台上方一行 italic 小字標籤說明這是哪個介面 |
| **每台互動** | 每台都是獨立的迷你狀態機：tab bar 可切、介面內按鈕/卡片/開關可點、能彈 modal——不是靜態擺拍 |

**只有兩種特例才偏離預設**（使用者明確說了才走，否則一律預設）：
- 使用者明確「只要靜態截圖 / 不用能點 / 就看 layout」→ 退回純靜態 overview（每台只渲染 `ScreenComponent`，不掛狀態機）
- 使用者明確「只演示一條流程 / 走一遍 onboarding / 單機 demo」→ 單台 `AppPhone` 走完整 flow

**預設骨架**（平鋪多台，每台各自一個帶 state 的 AppPhone）：

```jsx
// 每台 = 一個獨立狀態機，初始落在自己負責的主介面
function AppPhone({ initial }) {
  const [screen, setScreen] = React.useState(initial);
  const [modal, setModal] = React.useState(null);
  // 按 screen 渲染對應 ScreenComponent，傳入 onTabChange/onOpen/onClose/onToggle 等 callback
  return (
    <IosFrame>
      <ScreenComponent
        screen={screen}
        onTabChange={setScreen}
        onOpen={setModal}
        onClose={() => setModal(null)}
      />
    </IosFrame>
  );
}

// 平鋪：4-6 台並排，每台 initial 落在不同主介面
<div style={{display: 'flex', gap: 32, flexWrap: 'wrap', padding: 48, alignItems: 'flex-start'}}>
  {mainScreens.map(s => (
    <div key={s.id}>
      <div style={{fontSize: 13, color: '#666', marginBottom: 8, fontStyle: 'italic'}}>{s.label}</div>
      <AppPhone initial={s.id} />
    </div>
  ))}
</div>
```

Screen 元件接 callback props（`onTabChange`、`onOpen`、`onClose`、`onToggle`、`onAnnotation`），不硬編碼狀態。TabBar、按鈕、作品卡、開關加 `cursor: pointer` + hover 反饋。每台落在不同主介面，但 tab 切換後能到達彼此——平鋪給全貌，點選給縱深。

### 3. 交付前跑真實點選測試

靜態截圖只能看 layout，互動 bug 要點過才發現。用 Playwright 跑 3 項最小點選測試：進入詳情 / 關鍵標註點 / tab 切換。檢查 `pageerror` 為 0 再交付。Playwright 可用 `npx playwright` 呼叫，或按本機全域性安裝路徑（`npm root -g` + `/playwright`）。

### 4. 品位錨點（pursue list，fallback 首選）

沒有 design system 時預設往這些方向走，避免撞 AI slop：

| 維度 | 首選 | 避免 |
|------|------|------|
| **字型** | 襯線 display（Newsreader/Source Serif/EB Garamond）+ `-apple-system` body | 全場 SF Pro 或 Inter——太像系統預設，沒風格 |
| **色彩** | 一個有溫度的底色 + **單個** accent 貫穿全場（rust 橙/墨綠/深紅）| 多色聚類（除非資料真的有 ≥3 個分類維度） |
| **資訊密度·克制型**（預設）| 少一層容器、少一個 border、少一個**裝飾性** icon——給內容留氣口 | 每條卡片都配無意義的 icon + tag + status dot |
| **資訊密度·高密度型**（例外）| 當產品核心賣點是「智慧 / 資料 / 上下文感知」時（AI 工具、Dashboard、Tracker、Copilot、番茄鍾、健康監測、記賬類），每屏需**至少 3 處可見的產品差異化資訊**：非裝飾性資料、對話/推理片段、狀態推斷、上下文關聯 | 只放一個按鈕一個時鐘——AI 的智慧感沒表達出來，跟普通 App 沒區別 |
| **細節簽名** | 留一處「值得截圖」的質感：極淡油畫底紋 / serif 斜體引語 / 全屏黑底錄音波形 | 到處平均用力，結果處處平淡 |

**兩條原則同時生效**：
1. 品位 = 一個細節做到 120%，其它做到 80%——不是所有地方都精緻，而是在合適的地方足夠精緻
2. 減法是 fallback，不是普適律——產品核心賣點需要資訊密度支撐時（AI / 資料 / 上下文感知類），加法優先於克制。詳見下文「資訊密度分型」

### 5. iOS 裝置框必須用 `assets/ios_frame.jsx`——禁止手寫 Dynamic Island / status bar

做 iPhone mockup 時**硬性繫結** `assets/ios_frame.jsx`。這是已經對齊過 iPhone 15 Pro 精確規格的標準外殼：bezel、Dynamic Island（124×36、top:12、居中）、status bar（時間/訊號/電池、兩側避讓島、vertical center 對齊島中線）、Home Indicator、content 區 top padding 都處理好了。

**禁止在你的 HTML 裡自己寫**以下任何一項：
- `.dynamic-island` / `.island` / `position: absolute; top: 11/12px; width: ~120; 居中的黑圓角矩形`
- `.status-bar` with 手寫的時間/訊號/電池圖示
- `.home-indicator` / 底部 home bar
- iPhone bezel 的圓角外框 + 黑描邊 + shadow

自己寫 99% 會撞位置 bug——status bar 的時間/電池被島擠壓、或 content top padding 算錯導致第一行內容蓋在島下。iPhone 15 Pro 的劉海是**固定 124×36 畫素**，留給 status bar 兩側的可用寬度很窄，不是你憑空估的。

**用法（嚴格三步）**：

```jsx
// 步驟 1: Read 本 skill 的 assets/ios_frame.jsx（相對本 GUIDE.md 的路徑）
// 步驟 2: 把整個 iosFrameStyles 常量 + IosFrame 元件貼進你的 <script type="text/babel">
// 步驟 3: 你自己的屏元件包在 <IosFrame>...</IosFrame> 裡，不碰 island/status bar/home indicator
<IosFrame time="9:41" battery={85}>
  <YourScreen />  {/* 內容從 top 54 開始渲染，下邊留給 home indicator，你不用管 */}
</IosFrame>
```

**例外**：只有使用者明確要求「假裝是 iPhone 14 非 Pro 的劉海」「做 Android 不是 iOS」「自定義裝置形態」時才繞過——此時讀對應 `android_frame.jsx` 或修改 `ios_frame.jsx` 的常量，**不要**在專案 HTML 裡另起一套 island/status bar。
