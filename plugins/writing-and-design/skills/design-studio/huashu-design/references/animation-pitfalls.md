# Animation Pitfalls：HTML 動畫踩過的坑與規則

做動畫時最常踩的 bug 和如何避免。每條規則都來自真實失敗案例。

寫動畫之前讀完這篇，能省一輪迭代。

## 1. 疊層佈局 —— `position: relative` 是預設義務

**踩的坑**：一個 sentence-wrap 元素包了 3 個 bracket-layer（`position: absolute`）。沒給 sentence-wrap 設 `position: relative`，結果 absolute 的 bracket 以 `.canvas` 為座標系，飄到螢幕底部 200px 外。

**規則**：
- 任何包含 `position: absolute` 子元素的容器，**必須**顯式 `position: relative`
- 即使視覺上不需要「偏移」，也要寫 `position: relative` 作為座標系錨點
- 如果你在寫 `.parent { ... }`，其子元素裡有 `.child { position: absolute }`，下意識給 parent 加 relative

**快速檢查**：每出現一個 `position: absolute`，往上數 ancestor，確保最近的 positioned 祖先是你*想要的*座標系。

## 2. 字元陷阱 —— 不依賴稀有 Unicode

**踩的坑**：想用 `␣` (U+2423 OPEN BOX) 視覺化「空格 token」。Noto Serif SC / Cormorant Garamond 都沒這個字形，渲染為空白/豆腐，觀眾完全看不到。

**規則**：
- **動畫裡出現的每個字元，都必須在你選定的字型裡存在**
- 常見稀有字元黑名單：`␣ ␀ ␐ ␋ ␨ ↩ ⏎ ⌘ ⌥ ⌃ ⇧ ␦ ␖ ␛`
- 要表達「空格 / 回車 / 製表符」這類元字元，用 **CSS 構造的語義盒子**：
  ```html
  <span class="space-key">Space</span>
  ```
  ```css
  .space-key {
    display: inline-flex;
    padding: 4px 14px;
    border: 1.5px solid var(--accent);
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.3em;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }
  ```
- Emoji 也要驗證：某些 emoji 在 Noto Emoji 以外字型會 fallback 成灰色方框，最好用 `emoji` font-family 或 SVG

## 3. 資料驅動的 Grid/Flex 模板

**踩的坑**：程式碼裡 `const N = 6` 個 tokens，但 CSS 寫死 `grid-template-columns: 80px repeat(5, 1fr)`。結果第 6 個 token 沒有 column，整個矩陣錯位。

**規則**：
- 當 count 從 JS 陣列來（`TOKENS.length`），CSS 模板也應該資料驅動
- 方案 A：用 CSS 變數從 JS 注入
  ```js
  el.style.setProperty('--cols', N);
  ```
  ```css
  .grid { grid-template-columns: 80px repeat(var(--cols), 1fr); }
  ```
- 方案 B：用 `grid-auto-flow: column` 讓瀏覽器自動擴充套件
- **停用「固定數字 +  JS 常量」的組合**，N 改了 CSS 不會同步更新

## 4. 過渡斷層 —— 場景切換要連續

**踩的坑**：zoom1 (13-19s) → zoom2 (19.2-23s) 之間，主句子已經 hidden，zoom1 fade out（0.6s）+ zoom2 fade in（0.6s）+ stagger delay（0.2s+）= 約 1 秒純空白畫面。觀眾以為動畫卡住了。

**規則**：
- 連續切換場景時，fade out 和 fade in 要**交叉重疊**，不是前一個完全消失再開始下一個
  ```js
  // 差：
  if (t >= 19) hideZoom('zoom1');      // 19.0s out
  if (t >= 19.4) showZoom('zoom2');    // 19.4s in → 中間 0.4s 空白

  // 好：
  if (t >= 18.6) hideZoom('zoom1');    // 提前 0.4s 開始 fade out
  if (t >= 18.6) showZoom('zoom2');    // 同時 fade in（cross-fade）
  ```
- 或者用一個「錨點元素」（如主句子）作為場景之間的視覺連線，zoom 切換期間它短暫回顯
- 配 CSS transition 的 duration 算清楚，避免 transition 還沒結束就觸發下一個

## 5. Pure Render 原則 —— 動畫狀態應可 seek

**踩的坑**：用 `setTimeout` + `fireOnce(key, fn)` 鏈式觸發動畫狀態。正常播放沒問題，但做逐幀錄製/seek到任意時間點時，之前的 setTimeout 已經執行過就無法「回到過去」。

**規則**：
- `render(t)` 函數理想上是 **pure function**：給定 t 輸出唯一 DOM 狀態
- 如果必須用副作用（如 class 切換），用 `fired` set 配合顯式 reset：
  ```js
  const fired = new Set();
  function fireOnce(key, fn) { if (!fired.has(key)) { fired.add(key); fn(); } }
  function reset() { fired.clear(); /* 清所有 .show class */ }
  ```
- 暴露 `window.__seek(t)` 供 Playwright / 除錯用：
  ```js
  window.__seek = (t) => { reset(); render(t); };
  ```
- 動畫相關的 setTimeout 不要跨越 >1 秒，否則 seek 回跳時會亂套

## 6. 字型載入前測量 = 測錯

**踩的坑**：頁面一 DOMContentLoaded 就呼叫 `charRect(idx)` 測量 bracket 位置，字型還沒載入，每個字元寬度是 fallback 字型的寬度，位置全錯。等字型一載入（約 500ms 後），bracket 的 `left: Xpx` 還是老值，永久偏移。

**規則**：
- 任何依賴 DOM 測量（`getBoundingClientRect`、`offsetWidth`）的佈局程式碼，**必須**包在 `document.fonts.ready.then()` 裡
  ```js
  document.fonts.ready.then(() => {
    requestAnimationFrame(() => {
      buildBrackets(...);  // 此時字型已就緒，測量準確
      tick();              // 動畫開始
    });
  });
  ```
- 額外的 `requestAnimationFrame` 給瀏覽器一幀時間提交 layout
- 如果用 Google Fonts CDN，`<link rel="preconnect">` 加速首次載入

## 7. 錄製準備 —— 為影片匯出預留抓手

**踩的坑**：Playwright `recordVideo` 預設 25fps，從 context 建立就開始錄。頁面載入、字型載入的前 2 秒都被錄進去。交付時影片前面 2 秒空白/閃白。

**規則**：
- 提供 `render-video.js` 工具處理：warmup navigate → reload 重啟動畫 → 等 duration → ffmpeg trim head + 轉 H.264 MP4
- 動畫的**第 0 幀**要是最終佈局已就位的完整初始狀態（不是空白或載入中）
- 想要 60fps？用 ffmpeg `minterpolate` 後處理，不指望瀏覽器源幀率
- 想要 GIF？兩階段 palette（`palettegen` + `paletteuse`），對 30s 1080p 動畫能壓到 3MB

參見 `video-export.md` 獲取完整指令碼呼叫方式。

## 8. 批次匯出 —— tmp 目錄必須帶 PID 防併發衝突

**踩的坑**：用 `render-video.js` 3 個程序並行錄 3 個 HTML。因為 TMP_DIR 只用 `Date.now()` 命名，3 個程序同毫秒啟動時共用同一個 tmp 目錄。最先完成的程序清理 tmp，另外兩個讀目錄時 `ENOENT`，全部崩潰。

**規則**：
- 任何多程序可能共用的臨時目錄，命名必須帶 **PID 或隨機字尾**：
  ```js
  const TMP_DIR = path.join(DIR, '.video-tmp-' + Date.now() + '-' + process.pid);
  ```
- 如果確實想多檔案並行，用 shell 的 `&` + `wait` 而不是在一個 node 腳本里 fork
- 批次錄多個 HTML 時，保守做法：**序列**執行（2 個以內可並行，3 個以上老實排隊）

## 9. 錄屏裡有進度條/重播按鈕 —— Chrome 元素汙染影片

**踩的坑**：動畫 HTML 加了 `.progress` 進度條、`.replay` 重播按鈕、`.counter` 時間戳，方便人類除錯播放。錄成 MP4 交付時這些元素出現在影片底部，像把開發者工具截進去了一樣。

**規則**：
- HTML 裡給人類用的「chrome 元素」（progress bar / replay button / footer / masthead / counter / phase labels）和影片內容本體分開管理
- **約定 class 名** `.no-record`：任何帶這個 class 的元素，錄屏指令碼自動隱藏
- 指令碼端（`render-video.js`）預設注入 CSS 隱藏常見 chrome class 名：
  ```
  .progress .counter .phases .replay .masthead .footer .no-record [data-role="chrome"]
  ```
- 用 Playwright 的 `addInitScript` 注入（會在每次 navigate 前生效，reload 也穩）
- 想看原樣 HTML（帶 chrome）時加 `--keep-chrome` flag

## 10. 錄屏開頭幾秒動畫重複 —— Warmup 幀洩漏

**踩的坑**：`render-video.js` 的舊流程 `goto → wait fonts 1.5s → reload → wait duration`。錄製從 context 建立就開始，warmup 階段動畫已經播了一段，reload 後從 0 重啟。結果影片前幾秒是「動畫中段 + 切換 + 動畫從 0 開始」，重複感強。

**規則**：
- **Warmup 和 Record 必須用獨立的 context**：
  - Warmup context（無 `recordVideo` 選項）：只負責 load url、等字型、然後 close
  - Record context（有 `recordVideo`）：fresh 狀態開始，animation 從 t=0 開始錄
- ffmpeg `-ss trim` 只能裁 Playwright 的一點點 startup latency（~0.3s），**不能**用來掩蓋 warmup 幀；源頭要乾淨
- 錄製 context 關閉 = webm 檔案寫入磁碟，這是 Playwright 的約束
- 相關程式碼模式：
  ```js
  // Phase 1: warmup (throwaway)
  const warmupCtx = await browser.newContext({ viewport });
  const warmupPage = await warmupCtx.newPage();
  await warmupPage.goto(url, { waitUntil: 'networkidle' });
  await warmupPage.waitForTimeout(1200);
  await warmupCtx.close();

  // Phase 2: record (fresh)
  const recordCtx = await browser.newContext({ viewport, recordVideo });
  const page = await recordCtx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(DURATION * 1000);
  await page.close();
  await recordCtx.close();
  ```

## 11. 畫面內別畫「偽 chrome」—— 裝飾版 player UI 與真 chrome 撞車

**踩的坑**：動畫用 `Stage` 元件，已經自帶 scrubber + 時間碼 + 暫停按鈕（屬於 `.no-record` chrome，匯出時自動隱藏）。我又在畫面底部畫了一條「`00:60 ──── CLAUDE-DESIGN / ANATOMY`」的"雜誌頁碼感裝飾進度條"，自我感覺良好。**結果**：使用者看到兩條進度條——一條是 Stage 控制器，一條是我畫的裝飾。視覺上完全撞車，認定為 bug。「影片內還有個進度條是怎麼回事？」

**規則**：

- Stage 已經提供：scrubber + 時間碼 + 暫停/重播按鈕。**畫面內不要再畫**進度指示、當前時間碼、版權署名條、章節計數器——它們要麼和 chrome 撞車，要麼就是 filler slop（違反「earn its place」原則）。
- 「頁碼感」「雜誌感」「底部署名條」這些**裝飾訴求**，是 AI 自動加上的高頻 filler。每一個出現都要警覺——它真的傳達了不可替代的資訊嗎？還是單純填滿空白？
- 如果你堅信某個底部條帶必須存在（例如：動畫主題就是講 player UI），那它必須**敘事必要**，且**視覺上和 Stage scrubber 顯著區分**（不同位置、不同形式、不同色調）。

**元素歸屬測試**（每個畫進 canvas 的元素必須能回答）：

| 它屬於什麼 | 處理 |
|------------|------|
| 某一幕的敘事內容 | OK，留著 |
| 全域性 chrome（控制/除錯用） | 加 `.no-record` class，匯出時隱藏 |
| **既不屬於任何幕，又不是 chrome** | **刪**。這就是無主之物，必然是 filler slop |

**自檢（交付前 3 秒）**：截一張靜態圖，問自己——

- 畫面裡有沒有「看起來像 video player UI 的東西」（橫線進度條、時間碼、控制按鈕模樣）？
- 如果有，刪掉它敘事是否有損？無損就刪。
- 同一類資訊（進度/時間/署名）有沒有出現兩次？合併到 chrome 一處。

**反例**：底部畫 `00:42 ──── PROJECT NAME`、畫面右下角畫"CH 03 / 06"章節計數、畫面邊緣畫版本號"v0.3.1"——都是偽 chrome filler。

## 12. 錄屏前置空白 + 錄屏起點偏移 —— `__ready` × tick × lastTick 三聯陷阱

**踩的坑（A · 前置空白）**：60 秒動畫匯出 MP4，前 2-3 秒是空白頁面。`ffmpeg --trim=0.3` 剪不掉。

**踩的坑（B · 起點偏移，2026-04-20 真實事故）**：匯出 24 秒影片，使用者觀感「影片 19 秒才開始播第一幀」。實際上動畫從 t=5 開始錄，錄到 t=24 後 loop 回 t=0，再錄 5 秒到 end——所以影片最後 5 秒才是動畫真正的開頭。

**根因**（兩個坑共享一個根因）：

Playwright `recordVideo` 從 `newContext()` 那一刻就開始寫 WebM，此時 Babel/React/字型載入共耗時 L 秒（2-6s）。錄屏指令碼等 `window.__ready = true` 作為「動畫從這裡開始」的錨點——它和動畫 `time = 0` 必須嚴格 pair。有兩種常見錯法：

| 錯法 | 症狀 |
|------|------|
| `__ready` 在 `useEffect` 或同步 setup 階段設（在 tick 第一幀之前） | 錄屏指令碼以為動畫開始了，實際 WebM 還在錄空白頁 → **前置空白** |
| tick 的 `lastTick = performance.now()` 在**指令碼頂層**初始化 | 字型載入 L 秒被算進首幀 `dt`，`time` 瞬間跳到 L → 錄屏全程滯後 L 秒 → **起點偏移** |

**✅ 正確的完整 starter tick 模板**（手寫動畫必須用這個骨架）：

```js
// ━━━━━━ state ━━━━━━
let time = 0;
let playing = false;   // ❗ 預設不播，等字型 ready 再啟動
let lastTick = null;   // ❗ sentinel——tick 首幀時 dt 強制為 0（別用 performance.now()）
const fired = new Set();

// ━━━━━━ tick ━━━━━━
function tick(now) {
  if (lastTick === null) {
    lastTick = now;
    window.__ready = true;   // ✅ pair：「錄屏起點」與「動畫 t=0」同一幀
    render(0);               // 再渲一次確保 DOM 就緒（此時字型已 ready）
    requestAnimationFrame(tick);
    return;
  }
  const dt = (now - lastTick) / 1000;   // 首幀之後 dt 才開始推進
  lastTick = now;

  if (playing) {
    let t = time + dt;
    if (t >= DURATION) {
      t = window.__recording ? DURATION - 0.001 : 0;  // 錄製時不 loop，留 0.001s 保留末幀
      if (!window.__recording) fired.clear();
    }
    time = t;
    render(time);
  }
  requestAnimationFrame(tick);
}

// ━━━━━━ boot ━━━━━━
// 不要在頂層立即 rAF——等字型載入完才啟動
document.fonts.ready.then(() => {
  render(0);                 // 先把初始畫面畫出來（字型已就緒）
  playing = true;
  requestAnimationFrame(tick);  // 首次 tick 會 pair __ready + t=0
});

// ━━━━━━ seek 介面（供 render-video 防禦性矯正用）━━━━━━
window.__seek = (t) => { fired.clear(); time = t; lastTick = null; render(t); };
```

**為什麼這個模板對**：

| 環節 | 為什麼必須這樣 |
|------|-------------|
| `lastTick = null` + 首幀 `return` | 避免「指令碼載入到 tick 首次執行」的 L 秒被算進動畫時間 |
| `playing = false` 預設 | 字型載入期間 `tick` 即使執行也不推進 time，避免渲染錯位 |
| `__ready` 在 tick 首幀設 | 錄屏指令碼此刻開始計時，對應的畫面是動畫真正的 t=0 |
| `document.fonts.ready.then(...)` 裡才啟動 tick | 規避字型 fallback 寬度測量、避免首幀字型跳變 |
| `window.__seek` 存在 | 讓 `render-video.js` 可以主動矯正——第二道防線 |

**錄屏指令碼端的對應防禦**：
1. `addInitScript` 注入 `window.__recording = true`（先於 page goto）
2. `waitForFunction(() => window.__ready === true)`，記錄此刻偏移作為 ffmpeg trim
3. **額外**：`__ready` 之後主動 `page.evaluate(() => window.__seek && window.__seek(0))`，把 HTML 可能的 time 偏差強制歸零——這是第二道防線，對付不嚴格遵守 starter 模板的 HTML

**驗證方法**：匯出 MP4 後
```bash
ffmpeg -i video.mp4 -ss 0 -vframes 1 frame-0.png
ffmpeg -i video.mp4 -ss $DURATION-0.1 -vframes 1 frame-end.png
```
首幀必須是動畫 t=0 的初始狀態（不是中段，不是黑），末幀必須是動畫終態（不是第二輪 loop 的某個時刻）。

**參考實現**：`assets/animations.jsx` 的 Stage 元件、`scripts/render-video.js` 都已按此協議實現。手寫 HTML 必須套 starter tick 模板——每一行都是防過具體 bug。

## 13. 錄製時禁止 loop —— `window.__recording` 訊號

**踩的坑**：動畫 Stage 預設 `loop=true`（瀏覽器裡方便看效果）。`render-video.js` 錄完 duration 秒還多等 300ms 緩衝才停止，這 300ms 讓 Stage 進入下一迴圈。ffmpeg `-t DURATION` 擷取時，最後 0.5-1s 落入下一迴圈——影片結尾突然回到第一幀（Scene 1），觀眾以為影片出 bug。

**根因**：錄製指令碼和 HTML 之間沒有"我在錄製"的握手協議。HTML 不知道自己被錄，依然按瀏覽器互動場景迴圈。

**規則**：

1. **錄製指令碼**：在 `addInitScript` 裡注入 `window.__recording = true`（先於 page goto）：
   ```js
   await recordCtx.addInitScript(() => { window.__recording = true; });
   ```

2. **Stage 元件**：識別這個訊號，強制 loop=false：
   ```js
   const effectiveLoop = (typeof window !== 'undefined' && window.__recording) ? false : loop;
   // ...
   if (next >= duration) return effectiveLoop ? 0 : duration - 0.001;
   //                                                       ↑ 留 0.001 防止 Sprite end=duration 被關掉
   ```

3. **結尾 Sprite 的 fadeOut**：錄製場景下應設 `fadeOut={0}`，否則影片末尾會漸變到透明/暗色——使用者期望停在清晰的最後一幀，不是淡出。手寫 HTML 時建議結尾 Sprite 都用 `fadeOut={0}`。

**參考實現**：`assets/animations.jsx` 的 Stage / `scripts/render-video.js` 都已內建握手。手寫 Stage 必須實現 `__recording` 檢測——否則錄製必踩這個坑。

**驗證**：匯出 MP4 後 `ffmpeg -ss 19.8 -i video.mp4 -frames:v 1 end.png`，檢查倒數 0.2 秒是否還是預期最後一幀，沒有突然切換到另一個 scene。

## 14. 60fps 影片預設用幀複製 —— minterpolate 相容性差

**踩的坑**：`convert-formats.sh` 用 `minterpolate=fps=60:mi_mode=mci...` 生成的 60fps MP4，在 macOS QuickTime / Safari 部分版本下無法開啟（一片黑或直接拒打）。VLC / Chrome 能開啟。

**根因**：minterpolate 輸出的 H.264 elementary stream 包含某些播放器解析有問題的 SEI / SPS 欄位。

**規則**：

- 預設 60fps 用簡單 `fps=60` filter（幀複製），相容性廣（QuickTime/Safari/Chrome/VLC 都能開）
- 高質量插幀用 `--minterpolate` flag 顯式啟用——但**必須本地測過**目標播放器再交付
- 60fps 標籤價值是**上傳平台的演算法識別**（Bilibili / YouTube 上 60fps 標記會優先推流），實際感知流暢度對 CSS 動畫來說提升微弱
- 加 `-profile:v high -level 4.0` 提升 H.264 通用相容性

**`convert-formats.sh` 已預設改成相容模式**。如果你需要插幀高質量，加 `--minterpolate` flag：
```bash
bash convert-formats.sh input.mp4 --minterpolate
```

## 15. `file://` + 外部 `.jsx` 的 CORS 陷阱 —— 單檔案交付必須內聯引擎

**踩的坑**：動畫 HTML 裡用 `<script type="text/babel" src="animations.jsx"></script>` 外部載入引擎。本機雙擊開啟（`file://` 協議）→ Babel Standalone 走 XHR 拉 `.jsx` → Chrome 報 `Cross origin requests are only supported for protocol schemes: http, https, chrome, chrome-extension...` → 整頁黑屏，不報 `pageerror` 只報 console error，很容易當"動畫沒觸發"誤診。

啟 HTTP server 也未必救得了——本機有全域性代理時 `localhost` 也會走代理，返回 502 / 連線失敗。

**規則**：

- **單檔案交付（雙擊開啟即用的 HTML）** → `animations.jsx` 必須**內聯**到 `<script type="text/babel">...</script>` 標籤內，不要用 `src="animations.jsx"`
- **多檔案專案（起 HTTP server 演示）** → 可以外部載入，但交付時明確寫清 `python3 -m http.server 8000` 命令
- 判斷標準：交付給使用者的是"HTML 檔案"還是"帶 server 的專案目錄"？前者用內聯
- Stage 元件 / animations.jsx 經常 200+ 行——貼進 HTML `<script>` 塊完全可接受，別怕體積

**最小驗證**：雙擊你生成的 HTML，**不要**通過任何 server 開啟。如果 Stage 正常顯示動畫首幀，才算通過。

## 16. 跨 scene 反色上下文 —— 畫面內元素不要硬編碼顏色

**踩的坑**：做多場景動畫時，`ChapterLabel` / `SceneNumber` / `Watermark` 等**跨 scene 都出現**的元素，在元件裡寫死 `color: '#1A1A1A'`（深色文字）。前 4 個 scene 淺底 OK，到第 5 個黑底 scene 時"05"和水印直接消失——不報錯、不觸發任何檢查、關鍵資訊隱形。

**規則**：

- **跨多 scene 複用的畫面內元素**（chapter 標籤 / scene 編號 / 時間碼 / 水印 / 版權條）**禁止硬編碼顏色值**
- 改用三種方式之一：
  1. **`currentColor` 繼承**：元素只寫 `color: currentColor`，父 scene 容器設 `color: 計算值`
  2. **invert prop**：元件接受 `<ChapterLabel invert />` 手動切換深淺
  3. **基於底色自動計算**：`color: contrast-color(var(--scene-bg))`（CSS 4 新 API，或 JS 判斷）
- 交付前用 Playwright 抽**每個 scene 的代表幀**，人眼過一遍"跨 scene 元素"是否都可見

這條坑的隱蔽性在於——**沒有 bug 報警**。只有人眼或 OCR 能發現。

## 17. 離線/無 CDN 的真·自包含 —— React/Babel 全內聯，且引擎也要 transpile

**踩的坑（2026-05 覓遊宣傳動畫）**：動畫 HTML 用 `<script src="https://unpkg.com/react...">` + `<script src=".../@babel/standalone">` 走 CDN。本機有全域性代理，Playwright 錄製時 chromium 連 unpkg / Google Fonts 全部 `net::ERR_CONNECTION_CLOSED`：

1. React/ReactDOM 沒載入 → `window.React undefined`
2. Babel 沒載入 → `<script type="text/babel">` 裡的 JSX 當普通 JS 跑 → `Unexpected token '<'`

修了 React/Babel 後又踩第二個坑：**把 `animations.jsx` 引擎當普通 `<script>` 內聯，依然報 `Unexpected token '<'` → `window.Animations is undefined`**。根因：**`animations.jsx` 引擎本身含 JSX**（`Stage`/`Sprite` 元件 `return (<div>...)`），它原設計是用 `<script type="text/babel">` 由 Babel 轉譯載入的。只 transpile 了 app 程式碼、忘了 transpile 引擎 → 引擎那段 JSX 沒被編譯。

**規則**（要做「雙擊即開 / 離線 / 能被 Playwright 錄」的真自包含單檔案時）：

- **React + ReactDOM 本地內聯**：`curl` 下載 `react.production.min.js`（~10KB）+ `react-dom.production.min.js`（~131KB）到本地，inline 進 `<script>`，不走 CDN
- **構建期 Babel 預編譯，執行期不帶 Babel**：用 `@babel/standalone`（下載一次，僅構建用）在 node 裡 `Babel.transform(src,{presets:['react']}).code`，把 JSX → `React.createElement`。**app 和 `animations.jsx` 引擎兩段都要過 transform**——引擎含 JSX，漏了它必報 `Unexpected token '<'`
- **字型改系統字型**：Google Fonts CDN 同樣會被代理掐斷。中文動畫用 `'PingFang SC'`（sans）/ `'Songti SC'`（serif）系統字型，不依賴網路。`document.fonts.ready` 對系統字型立即 resolve，錄製不卡
- **base64 內聯圖片素材**：`<img src="png/x.png">` 相對路徑在 `file://` 能渲染，但要真便攜（移動檔案不丟圖）就 base64 data URL 內聯；背景大圖先轉 JPEG 壓一下再 base64
- **構建模板化**：HTML 模板留 `__REACT__/__REACTDOM__/__ASSETS__/__ENGINE__` token + 一段 `type="text/jsx-source"` 的 app 原始碼，node 構建指令碼讀 token 注入（vendor 原樣、引擎+app 過 Babel）→ 寫出最終單檔案。改動畫只改模板重跑構建

**驗證**：Playwright `page.evaluate(()=>({React:typeof window.React, Animations:typeof window.Animations}))`——兩個都該是 `object`。任一 `undefined` → 對應 `<script>` 拋了錯（多半是沒 transpile 的 JSX）。

**和坑 #15 的關係**：#15 講「單檔案別用 `src=` 外鏈 `.jsx`（file:// CORS）」；本坑更進一步——連 React/Babel/字型的**遠端 CDN 在受限網路下也會斷**，要做到真自包含必須全內聯 + 構建期 transpile。

## 快速自查清單（開工前 5 秒）

- [ ] 每個 `position: absolute` 的父元素都有 `position: relative`？
- [ ] 動畫裡的特殊字元（`␣` `⌘` `emoji`）都在字型裡存在？
- [ ] Grid/Flex 模板的 count 和 JS 資料的 length 一致？
- [ ] 場景切換之間有 cross-fade，沒有 >0.3s 的純空白？
- [ ] DOM 測量程式碼包在 `document.fonts.ready.then()` 裡？
- [ ] `render(t)` 是 pure 的，或有明確的 reset 機制？
- [ ] 第 0 幀是完整初始狀態，不是空白？
- [ ] 畫面內沒有「偽 chrome」裝飾（進度條/時間碼/底部署名條與 Stage scrubber 撞車）？
- [ ] 動畫 tick 第一幀同步設 `window.__ready = true`？（用 animations.jsx 自帶；手寫 HTML 自己加）
- [ ] Stage 檢測 `window.__recording` 強制 loop=false？（手寫 HTML 必加）
- [ ] 結尾 Sprite 的 `fadeOut` 設為 0（影片末尾停清晰幀）？
- [ ] 60fps MP4 預設用幀複製模式（相容性），高質量插幀才加 `--minterpolate`？
- [ ] 匯出後抽第 0 幀 + 末幀驗證是動畫初始/最終狀態？
- [ ] 涉及具體品牌（Stripe/Anthropic/Lovart/...）：走完了「品牌資產協議」（SKILL.md §1.a 五步）？有沒有寫 `brand-spec.md`？
- [ ] 單檔案交付的 HTML：`animations.jsx` 是內聯的，不是 `src="..."`？（file:// 下 external .jsx 會 CORS 黑屏）
- [ ] 跨 scene 出現的元素（chapter 標籤/水印/scene 編號）沒有硬編碼顏色？在每個 scene 底色下都可見？
- [ ] 要離線/真自包含：React+ReactDOM 本地內聯、**app 和 `animations.jsx` 引擎都過 Babel transpile**、字型用系統字型？（見坑 #17；引擎含 JSX，漏 transpile 必報 `Unexpected token '<'`）
