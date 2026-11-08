# WebGPU 特效製作手冊

這份手冊講怎麼把霧、光、景深這類電影氛圍，做成網頁上的即時特效，而且在任何裝置上都不拖慢頁面、不留白。

名詞先講清楚：

- **WebGPU**：瀏覽器新一代的繪圖介面，可以直接叫顯示卡算圖，比 WebGL 更有效率，但還不是每個瀏覽器都有。
- **WebGL 2**：上一代的繪圖介面，幾乎所有現代瀏覽器都支援，當 WebGPU 的備案。
- **著色器（shader）**：交給顯示卡跑的小程式。「片段著色器」會對畫面上每個像素各算一次顏色，全螢幕背景特效幾乎都靠它。
- **DPR（裝置像素比）**：一個 CSS 像素對應幾個實體像素。手機常見 3，代表同樣大小的畫面要算 9 倍像素。
- **幀時間**：畫面相鄰兩次更新的間隔。60Hz 螢幕順暢時約 16.7 毫秒。

---

## 1. 技術選擇

| 需求 | 用什麼 | 外部套件 |
| --- | --- | --- |
| 只要一張全螢幕背景特效（霧、液態漸層、光束、顆粒） | 原生 WebGPU 片段著色器＋WebGL 2 備案，直接從 [`assets/webgpu-starter.html`](../assets/webgpu-starter.html) 改 | 0 |
| 有 3D 物件、相機、燈光、粒子系統、後製特效 | three.js 的 `WebGPURenderer`＋TSL | three.js |

**預設用 three.js 的 `WebGPURenderer`＋TSL。** TSL 是 three.js 自己的著色語言，用 JavaScript 寫一次，three.js 會依瀏覽器能力轉成 WebGPU 或 WebGL 2 的著色器。`WebGPURenderer` 預設先用 WebGPU，不支援時自動改用 WebGL 2；要測備案路徑時加 `forceWebGL: true`。初始化是非同步的，用 `setAnimationLoop()` 會自動等它準備好，自己用 `requestAnimationFrame` 的話要先 `await renderer.init()`。
出處：[three.js 手冊 WebGPURenderer](https://threejs.org/manual/#en/webgpurenderer)（原始檔 [manual/pages/webgpurenderer.html @ r186](https://github.com/mrdoob/three.js/blob/r186/manual/pages/webgpurenderer.html)）、[WebGPURenderer API](https://threejs.org/docs/pages/WebGPURenderer.html)。

同一份手冊也寫明：`ShaderMaterial`、`RawShaderMaterial`、`onBeforeCompile()` 和舊的 `EffectComposer` 在 `WebGPURenderer` 不支援，要改寫成節點材質與 TSL。網路上的舊 three.js 著色器範例不能直接搬。

### 固定版本與載入方式

已實測可用：**three.js 0.186.1**（r186），用 importmap 從 jsDelivr 載入：

```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.webgpu.min.js",
    "three/webgpu": "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.webgpu.min.js",
    "three/tsl": "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.tsl.min.js",
    "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.core.js": "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.core.min.js"
  }
}
</script>
<script type="module">
  import * as THREE from 'three/webgpu';
  import { uv, time, vec3, mix, color, mx_fractal_noise_float } from 'three/tsl';

  const forceWebGL = new URLSearchParams(location.search).get('renderer') === 'webgl';
  const renderer = new THREE.WebGPURenderer({ antialias: false, forceWebGL });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(innerWidth, innerHeight);
  document.body.append(renderer.domElement);
  await renderer.init();
  // 實際走哪條路，寫給驗證腳本讀
  document.documentElement.dataset.renderer = renderer.backend.isWebGPUBackend ? 'webgpu' : 'webgl';
</script>
```

- 版本號一律寫死，不用 `@latest`。three.js 每個月都有版本，`WebGPURenderer` 手冊自己寫它仍在實驗階段，換版本前重跑一次驗證。
- 最後一行對應是刻意的：jsDelivr 自動壓縮的 `three.webgpu.min.js` 內部引用的是未壓縮的 `./three.core.js`，不加這行會多下載約 160KB。
- `*.min.js` 是 jsDelivr 自動產生的檔案，檔頭註明不要對它用 SRI（子資源完整性雜湊）。正式上線若要鎖雜湊，改成自己打包或自架檔案。

### 只要一張背景時用輕量寫法

全螢幕背景只需要「每個像素算一個顏色」，不需要場景、相機、材質系統。直接寫原生 WebGPU（WGSL 著色器）加一份對應的 WebGL 2（GLSL）備案，整頁零外部套件。範本 `assets/webgpu-starter.html` 就是這種寫法，換效果時只改兩份著色器裡的演算法，其他（降級、暫停、自適應解析度）不用動。

---

## 2. 三層降級

```
WebGPU（原生或 three.js）
  └ 失敗 → WebGL 2
      └ 失敗 → 靜態 CSS/SVG 畫面
減少動態效果、或判定裝置太弱 → 直接靜態，不嘗試前兩層
```

| 情況 | 走哪層 | 怎麼判斷 |
| --- | --- | --- |
| 系統開了「減少動態效果」 | 靜態 | `matchMedia('(prefers-reduced-motion: reduce)')`，並監聽 `change`，使用者中途打開也要立刻停 |
| 省流量模式 | 靜態 | `navigator.connection.saveData` |
| CPU 2 核以下或記憶體 2GB 以下 | 靜態 | `navigator.hardwareConcurrency`、`navigator.deviceMemory`（只有 Chromium 有） |
| 沒有 `navigator.gpu`、拿不到轉接器 | WebGL 2 | `navigator.gpu.requestAdapter()` 回傳 `null` |
| WebGPU 只拿到「後備轉接器」 | WebGL 2 | `adapter.info.isFallbackAdapter` 為真，代表是軟體模擬的 GPU |
| WebGL 2 是軟體繪圖 | 靜態 | `WEBGL_debug_renderer_info` 的名稱含 SwiftShader、llvmpipe、Software |
| 著色器編譯失敗、裝置遺失、context 遺失 | 下一層 | `getCompilationInfo()`、`device.lost`、`webglcontextlost` |
| 執行中一路降解析度還是太慢 | 靜態 | 見第 3 節 |

出處：[MDN WebGPU API](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API)（整個 API 只在安全環境可用）、[GPUAdapterInfo.isFallbackAdapter](https://developer.mozilla.org/en-US/docs/Web/API/GPUAdapterInfo/isFallbackAdapter)、[prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)、[Navigator.deviceMemory](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/deviceMemory)。

實作要點：

- **同一張 canvas 拿過 `webgpu` context 就拿不到 `webgl2`**。從 WebGPU 退到 WebGL 2 時要換一張新的 canvas。
- **靜態層永遠墊在最底下**，不是失敗時才補上。特效 canvas 畫好第一幀才淡入，所以初始化期間、降級瞬間看到的都是靜態層，不會閃黑。
- **靜態層是完成的設計，不是空底色。** 用同一組品牌色變數，以多層 `radial-gradient` 做霧團、`conic-gradient` 加遮罩做光束、SVG `feTurbulence` 做顆粒，讓它看起來像特效的一張定格。範本的靜態版和動態版共用 `--fx-*` 四個顏色。
- 網址參數 `?renderer=webgpu|webgl|static` 強制路徑，方便截圖驗證。強制時略過「裝置太弱」判斷，但「減少動態效果」仍然優先。
- 把實際路徑寫在 `document.documentElement.dataset.renderer`，原因寫在 `data-renderer-reason`，驗證腳本靠它判斷。

---

## 3. 效能上限

| 規則 | 數值 | 做法 |
| --- | --- | --- |
| 首屏不等特效 | 特效在 `load` 之後、瀏覽器空閒時才初始化 | `requestIdleCallback(start, { timeout: 1200 })`，沒有就 `setTimeout` |
| DPR 上限 | 手機 1.5、桌機 2 | 觸控為主（`pointer: coarse`）或寬度小於 768px 算手機 |
| 離開畫面就暫停 | 特效區塊完全離開視窗時停 | `IntersectionObserver` 觀察特效所在區塊 |
| 分頁隱藏就暫停 | `document.visibilityState !== 'visible'` 時停 | 監聽 `visibilitychange` |
| 自適應解析度 | 每累積 1000 毫秒的幀算一次平均，平均超過 **24 毫秒**就降一級；倍率 1 → 0.75 → 0.5 → 0.35，最低一級還是慢就改走靜態 | 剛啟動或剛改解析度後先略過 500 毫秒；超過 1 秒的單一間隔不計 |
| 外部套件 | 輕量背景 **0 個**；three.js 特效頁所有外部模組合計壓縮後傳輸 **300KB 以內** | 見下方量測 |

出處：[IntersectionObserver](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)、[visibilitychange](https://developer.mozilla.org/en-US/docs/Web/API/Document/visibilitychange_event)、[requestIdleCallback](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback)。

暫停時也要停止累計動畫時間，恢復後從原地繼續；單幀時間差上限 50 毫秒，卡頓後霧才不會瞬間跳一大段。

### 門檻怎麼訂出來的

量測環境：Windows 11、NVIDIA GeForce GT 1030（入門級獨顯）、Chrome 156 headless、1440×900、DPR 1，60Hz。用範本的 `?stress=n` 讓著色器每個像素多算 n 次雜訊來模擬較弱的 GPU，以 `?renderer=webgpu&stress=n`（或 `webgl`）開頁，在頁面內用 `requestAnimationFrame` 記錄相鄰幀間隔 10 秒，同時記下 `window.__fx.scale` 何時改變。量測方式與 `scripts/verify_webgpu.mjs` 的幀時間量測相同。

| 負載 | 前 60 幀平均 / p95（毫秒） | 自適應結果 |
| --- | --- | --- |
| 正常（無 stress） | 16.7 / 16.8 | 不降級 |
| stress 16（WebGPU） | 21.1 / 33.4，偶爾掉幀 | 不降級，肉眼仍順 |
| stress 32（WebGPU） | 32.2 / 83.3 | 約 1.5 秒降到 0.75，之後平均 23.5 |
| stress 64（WebGPU） | 49.7 / 116.8 | 1.6 秒降到 0.75、3.2 秒降到 0.5 |
| stress 64（WebGL 2） | 40.3 / 83.4 | 1.5 秒降到 0.75、3.0 秒降到 0.5 |
| stress 64、DPR 2 | — | 2.7、4.3、5.9 秒逐級下降，7.4 秒改走靜態 |

- **24 毫秒**落在「順暢」（16.7）和「明顯卡」（27 以上）之間，約等於低於 42fps。
- **用時間區間平均，不用「連續 N 個慢幀」。** 實測 WebGL 2 在中重度負載時幀間隔會 16.7、50 交替出現，連續計數永遠被好幀歸零，完全不會觸發；以幀數為單位的視窗則在很慢的裝置上要等二十幾秒才反應。
- 螢幕若被系統限在 30Hz（例如部分手機的省電模式，未實測），幀間隔本來就約 33 毫秒，會一路降到靜態。這對省電情境是可接受的結果；若專案不想這樣，把門檻改成依實際更新率計算。

### 首屏時序實測

同一環境下，首次內容繪製（FCP）與特效寫出路徑的時間：WebGPU 路徑 FCP 312 毫秒、特效就緒 434 毫秒；WebGL 2 路徑 FCP 284 毫秒、特效就緒 296 毫秒。兩者都在文字出現之後才初始化。

### 外部套件大小實測

用 Chrome DevTools Protocol 的 `Network.loadingFinished.encodedDataLength`（實際傳輸位元組，jsDelivr 回傳 brotli 壓縮）量 three.js 0.186.1 `WebGPURenderer`＋TSL 的最小頁面：

| 載入方式 | 傳輸量 | 首幀（毫秒，頁面時間） |
| --- | --- | --- |
| 未壓縮 `three.webgpu.js`＋`three.core.js`＋`three.tsl.js` | 678KB | 284 |
| `.min.js`，但 core 沒對應 | 427KB（core 仍是未壓縮的 261KB） | 260 |
| `.min.js`＋core 對應到 `three.core.min.js`（上面的 importmap） | **269KB** | 250 |

所以 three.js 特效頁的外部模組上限訂 **300KB**：照上面 importmap 載入剛好放得下，只留約 30KB 給額外的 addon。超過就代表載了不必要的東西，或沒用壓縮版。輕量範本整檔 30.0KB、gzip 後 10.9KB，沒有外部請求。

---

## 4. 效果庫：電影語法 → WebGPU 效果

電影語法的編號對應 `data/background-techniques.md`（A～F）與 `data/camera-shots-50.md`（#）。效能成本以範本的霧為基準：範本每個像素呼叫 5 次 5 層雜訊（fbm）。在上面的 GT 1030、1440×900 實測，每像素約 13 次 fbm 仍穩定 60fps，約 21 次開始掉幀。DPR 2 時像素變 4 倍，預算要除以 4。

| 效果 | 用途 | 對應電影語法 | 實作要點 | 效能成本 |
| --- | --- | --- | --- | --- |
| 流動的霧 | 首屏氛圍、科幻或懸疑開場 | E3 雷射霧、D10 煙霧粒子、F12《異星入境》 | 兩層座標扭曲的 fbm（domain warping）；霧密度往畫面上方遞減；時間係數 0.015～0.03，越慢越像 Villeneuve | 中（範本約 5 次 fbm） |
| 斜光與光束 | 給畫面一個光源方向，引導視線到標題 | A2 方向性光源、A4 錐形放射、F8《花樣年華》 | 光源點外的高斯光暈，加上以角度取樣的雜訊做光束；光束乘上霧密度，光才像穿過霧 | 低 |
| 液態漸層 | 品牌首頁、產品發表的流動色塊 | E1 流體漸層、A3 漸層網格、B1 漸層流動 | 2～3 層 fbm 只取低頻，混合品牌色；不需要扭曲兩層 | 低 |
| 流場粒子 | 數據、AI、網路主題 | D5 流場、D2 星空視差、D3 粒子連線 | 粒子位置存在 GPU 緩衝區，每幀用計算著色器沿雜訊方向場推進；three.js 用 TSL 的計算節點寫 | 中～高，隨粒子數線性增加，要逐案實測 |
| 隨捲動變形 | 從首屏捲到內容時的轉場 | #29 推軌變焦（Vertigo）、#33 視差分層、#44 捲動景深轉移 | 每幀讀一次捲動進度傳進著色器：放大座標做推軌變焦；不同頻率的雜訊用不同速度位移做視差；捲動越深，雜訊越少高頻做失焦。範本示範霧隨捲動上飄、變濃 | 低（只多一個參數） |
| 散景光點 | 夜景、溫暖敘事、節慶 | #44 景深、D8 光線追蹤點、F15《神隱少女》 | 一批柔邊圓形，依假想深度決定大小與模糊程度；疊加用加亮混合 | 中，重疊越多越貴 |
| 空間扭曲、色差 | 衝擊、故障、科技感轉場 | E4 扭曲空間、E5 色彩分離、F4《星際效應》 | 需要一張畫面當貼圖再扭曲取樣；色差是三個色版各自位移取樣 | 中，多一次全螢幕貼圖取樣 |
| 膠片顆粒 | 任何特效的收尾質感 | C1 膠片顆粒、C8 暈影 | 在著色器最後加一點隨時間變化的雜訊；同時能消除漸層色階。靜態層用 SVG 顆粒 | 幾乎免費 |

組合原則沿用 `data/background-techniques.md` 的混搭公式：基底層（液態漸層或霧）＋氛圍層（光束）＋細節層（顆粒、暈影）＋動態層。全部在同一個著色器裡疊，比疊好幾張 canvas 便宜。

---

## 5. 和 Claude 內建 Design 畫布的關係

以下兩條限制出自 [claude-design.md](claude-design.md)，本手冊沒有另外實測：

- 畫布不允許直接從網路載入套件，要用的函式庫必須先上傳成畫布附檔。
- 畫布上的畫面元素不能用程式動態產生。

**WebGPU 在畫布上能不能跑，目前尚未確認。** 確認之前的做法：

1. 特效做成獨立 HTML（從 `assets/webgpu-starter.html` 改），用第 7 節的驗證流程跑過三條路徑。
2. 畫布上放靜態版：用獨立 HTML 的 `?renderer=static` 截圖，或直接把靜態層的 CSS 搬上去。
3. 在交付說明寫清楚「動態版在獨立 HTML」，不要讓人以為畫布上那張就是最終效果。

---

## 6. 從範本改出新效果

1. 改 `:root` 的 `--fx-bg`、`--fx-fog-1`、`--fx-fog-2`、`--fx-light` 套品牌色，任何 CSS 顏色寫法都可以。
2. 換演算法時，WGSL 的 `fs` 和 GLSL 的 `main` 要一起改，兩份邏輯保持一致。WebGPU 的像素座標 y 朝下，範本已在 WGSL 開頭翻成 y 朝上。
3. 同步改 `.fx-static` 的靜態畫面，讓它像新效果的一張定格。
4. 首屏文字下方保留壓暗的漸層，確保任何一層背景上文字都清楚。
5. 不要動降級、暫停、自適應的程式；需要調整時只改 `CONFIG` 的數值，並重新量測。

---

## 7. 驗證

```bash
node scripts/verify_webgpu.mjs assets/webgpu-starter.html --out <暫存資料夾>
node scripts/verify_webgpu.mjs --help   # 全部選項
```

腳本會分別以 WebGPU（`?renderer=webgpu`）、WebGL 2（`?renderer=webgl`）、減少動態效果三種情況開頁面，各截一張圖，回報實際路徑、平均與 p95 幀時間、console 錯誤數；任何一項不符預期就以代碼 1 結束。截圖一定要打開看，路徑對了不代表畫面對了。

repo 沒有 `node_modules` 時，用環境變數指向別處裝好的 Playwright：

```bash
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright-core node scripts/verify_webgpu.mjs page.html
```

實測輸出（範本，Chrome 156 headless）：

```
[PASS] webgpu          路徑：webgpu（forced）   平均 16.67 ms，p95 16.8 ms，console 錯誤 0
[PASS] webgl           路徑：webgl（forced）    平均 16.67 ms，p95 16.8 ms，console 錯誤 0
[PASS] reduced-motion  路徑：static（reduced-motion）                       console 錯誤 0
```

### headless Chrome 能不能跑 WebGPU（實測結論）

在 Windows 11＋GT 1030＋Chrome 156，用 Playwright 的 `executablePath` 指向本機 Chrome：

| 情況 | 結果 |
| --- | --- |
| headless、不加任何旗標、頁面是 `file://` | **可以**，拿到真實 NVIDIA 轉接器（非後備） |
| 頁面是 `about:blank` | `navigator.gpu` 不存在，WebGPU 只在安全環境（https、localhost、file://）開放 |
| 加 `--enable-unsafe-webgpu`、`--use-angle=d3d11` | 結果與不加相同，這台機器不需要 |
| 加 `--use-webgpu-adapter=swiftshader`（腳本的 `--swiftshader`） | 拿到軟體模擬的後備轉接器；範本自動模式會因此改走 WebGL 2，強制 `?renderer=webgpu` 仍可跑。適合沒有 GPU 的 CI，幀時間不代表真實效能 |
| 加 `--enable-features=Vulkan --use-angle=vulkan` | `requestAdapter()` 回傳 `null`，Windows 上不要這樣設 |
| headless 時切換分頁 | `visibilityState` 一直是 `visible`，無法用切分頁測暫停；改在頁面裡覆寫 `visibilityState` 並送出 `visibilitychange` 事件來測 |

Linux 伺服器要讓 headless Chrome 用到實體 GPU，Chrome 官方文章的做法是 `--headless=new --use-angle=vulkan --enable-features=Vulkan --disable-vulkan-surface --enable-unsafe-webgpu`，而且要裝對應的顯示卡驅動與 Vulkan 工具，光加旗標不夠（[Chrome for Developers：Supercharge Web AI model testing](https://developer.chrome.com/blog/supercharge-web-ai-testing)）。這組 Linux 設定本手冊沒有實測。

### 幀時間的解讀

- headless 的 `requestAnimationFrame` 也是 60Hz，所以順暢時一律約 16.7 毫秒，看不出「還有多少餘裕」。要知道餘裕，用 `?stress=n` 加負載，看幾輪開始掉幀。
- 幀間隔量的是整體節奏，不是 GPU 實際花的時間。量 GPU 時間要用 WebGPU 的 `timestamp-query` 功能，本手冊沒有實測。
- 驗證機器的 GPU 越強，結果越樂觀。交付前至少在一台手機上開 `?debug=1` 看實際路徑與幀時間。
