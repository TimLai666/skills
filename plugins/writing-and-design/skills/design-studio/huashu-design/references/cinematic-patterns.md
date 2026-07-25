# Cinematic Patterns · Workflow Demo 的 Best Practice

> 從「PPT 動畫」升級到「發表會級 cinematic」的 5 個關鍵 pattern。
> 蒸餾自 2026-04 「聊聊 skill」 deck 的兩個 cinematic demo（Nuwa workflow + Darwin workflow），實測可復現。

---

## 0 · 這份文件解決什麼問題

當你需要做「演示一個工作流的 demo 動畫」時（典型場景：skill 工作流、產品 onboarding、API 呼叫流程、agent 任務執行），有兩種常見做法：

| 範式 | 長什麼樣 | 後果 |
|---|---|---|
| **PPT 動畫**（差） | step 1 fade in → step 2 fade in → step 3 fade in，4 個 box 同一畫面排列 | 觀眾感覺「就是一個 PPT 加了 fade 效果」，沒有 wow moment |
| **Cinematic**（好） | scene-based，一次只 focus 一件事，scene 之間是 dissolve / focus pull / morph | 觀眾感覺「這是一個產品發表會片段」，會想截圖分享 |

差異的根源**不是動畫技術**，是**敘事範式**。本文件講怎麼從前者升級到後者。

---

## 1 · 五個核心 pattern

### Pattern A · Dashboard + Cinematic Overlay 雙層結構

**問題**：單純的 cinematic 預設是黑畫面 + 一個 ▶ 按鈕，使用者翻到這頁如果沒點，什麼都看不到。

**解決**：
```
DEFAULT 狀態 (永遠顯示)：完整靜態 workflow dashboard
  └── 觀眾一眼看清這個 skill / 工作流怎麼跑

POINT ▶ 觸發 (overlay 浮上來)：22 秒 cinematic
  └── 跑完自動 fade 回 DEFAULT

```

**實現要點**：
- `.dash` 預設 visible，`.cinema` 預設 `opacity: 0; pointer-events: none`
- `.play-cta` 是右下角金色小按鈕（不是中央大覆蓋）
- 點選 → `cinema.classList.add('show')` + `dash.classList.add('hide')`
- 用 `requestAnimationFrame` 跑一次（不是迴圈），結束後 `endCinematic()` reverse 狀態

**反 pattern**：預設 = 中央大 ▶ overlay 覆蓋一切，沒點之前頁面是空白的。

---

### Pattern B · Scene-based, NOT Step-based

**問題**：把動畫拆成「step 1 顯示 → step 2 顯示 → ...」就是 PPT 思維。

**解決**：拆成 5 個 scene，每個 scene 是**獨立的鏡頭**，整個畫面只 focus 一件事：

| Scene 類型 | 職責 | 時長 |
|---|---|---|
| 1 · Invoke | 使用者輸入觸發（終端 typewriter）| 3-4s |
| 2 · Process | 核心工作流的視覺化（獨特視覺語言）| 5-6s |
| 3 · Result/Insight | 提煉出的關鍵產物（視覺化）| 4-5s |
| 4 · Output | 實際產物展示（檔案 / diff / 數字）| 3-4s |
| 5 · Hero Reveal | 收尾 hero moment（大字 + 價值主張）| 4-5s |

**總時長 ≈ 22 秒**——這是經過測試的黃金長度：
- 短於 18 秒：PM 還沒進入狀態就結束了
- 長於 25 秒：失去耐心
- 22 秒剛好夠「鉤住 → 展開 → 收束 → 留下印象」

**實現要點**：
- `T = { DURATION: 22.0, s1_in: [0, 0.7], s2_in: [3.8, 4.6], ... }` 全域時間軸
- 單個 `requestAnimationFrame(render)` 跑所有 scene 的 opacity / transform 計算
- 不要用 setTimeout 鏈（容易斷掉、難除錯）
- Easing 必用 `expoOut` / `easeOut` / cubic-bezier，**禁止 linear**

---

### Pattern C · 每個 demo 的視覺語言必須獨立

**問題**：做完第一個 cinematic 後，做第二個時偷懶複用同一個模板（同樣的 orbit + pentagon + typewriter + hero 大字），只換了文案。

**後果**：觀眾發現兩個 skill「長得一模一樣」，等於在說「這兩個 skill 沒區別」。

**解決**：每個工作流的核心隱喻不同，視覺語言就必須不同。

**對照案例**：

| 維度 | Nuwa（蒸餾人）| Darwin（最佳化 skill）|
|---|---|---|
| 核心隱喻 | 收集 → 提煉 → 寫 | 迴圈 → 評估 → 棘輪 |
| 視覺運動 | 漂浮 / 輻射 / pentagon | 迴圈 / 上升 / 對比 |
| Scene 2 | 3D Orbit · 8 張檔案在透視橢圓漂浮 | Spin Loop · token 沿 6 節點圓環跑 5 圈 |
| Scene 3 | Pentagon · 5 token 從中央輻射 | v1 vs v5 · 並列 diff（紅版 vs 金版） |
| Scene 4 | SKILL.md typewriter | Hill-Climb · 全畫面曲線繪製 |
| Scene 5 hero | 「21 分鐘」serif italic 大字 | 旋轉齒輪 ⚙ + 「KEPT +1.1」金色 tag |

**判斷標準**：蓋住文案，只看視覺，能不能區分這是哪個 demo？區分不了就是偷懶。

---

### Pattern D · 用 AI 生成的真實素材，不要 emoji 或 SVG 手畫

**問題**：3D orbit / gallery 裡需要素材碎片漂浮，emoji（📚🎤）醜且無品牌、SVG 手畫書脊永遠不像真書。

**解決**：用 `huashu-gpt-image` 跑一張 4×2 grid 大圖（8 件主題相關物品 · 白底 · 60px breathing space · unified style），用 `extract_grid.py --mode bbox` 去背成 8 張獨立透明 PNG。

**Prompt 要點**（詳細 prompt patterns 見 `huashu-gpt-image` skill）：
- IP 錨定（"1960s Caltech archive aesthetic" / "Hearthstone-style consistent treatment"）
- 白底（便於去背，灰底氛圍好但去背困難）
- 4×2 不要 5×5（避免末行壓縮 bug）
- Persona finishing（"You are a Wired magazine curator preparing an exhibition photo"）

**反 pattern**：用 emoji 當 icon、用 CSS 剪影代替產品圖。

---

### Pattern E · BGM + SFX 雙軌制

**問題**：只有動畫沒有聲音，觀眾潛意識感覺「這玩意像個窮酸 demo」。

**解決**：BGM 長音 + 11 個 SFX cues。

**通用 SFX cue 配方**（適用於工作流 demo）：

| 時點 | SFX | 觸發場景 |
|---|---|---|
| 0.10s | whoosh | 終端從下方升起 |
| 3.0s | enter | typewriter 完成、按 enter |
| 4.0s | slide-in | scene 2 元素入場 |
| 5-9s × 5 次 | sparkle | 關鍵過程節點（每代 / 每個 token / 每個資料點）|
| 14s | click | 切換到 output scene |
| 17.8s | logo-reveal | hero reveal 時刻 |
| typewriter | type | 每 2 字元觸發一次（密度別太高）|

**頻段隔離**：BGM volume 0.32（低頻底噪），SFX volume 0.55（中高頻 punch），sparkle 0.7（要醒目），logo-reveal 0.85（最強 hero moment）。

**使用者控制**：
- 必須有 ▶ 啟動覆蓋（瀏覽器 autoplay 限制）
- 右上角小 mute 按鈕（使用者隨時切靜音）
- 不要做成「翻到這頁就強制響」

---

## 2 · 靜態 Dashboard 設計要點

Dashboard 是雙層結構的 Layer 1，PM 不點 ▶ 也能看懂這個 skill。

**佈局**：3 列 grid（或 1 大 + 2 小），每個 panel 解決一個問題：

| Panel 類型 | 解決什麼問題 | 案例 |
|---|---|---|
| **Pipeline / Flow Diagram** | 「這個 skill 的工作流程是什麼？」| Nuwa 4 階段 pipeline · Darwin autoresearch loop |
| **Snapshot / State** | 「跑出來的真實資料長什麼樣？」| Darwin 8 維 rubric snapshot |
| **Trajectory / Evolution** | 「多次執行後怎麼變化？」| Darwin 5 代 hill-climb 曲線 |
| **Examples / Gallery** | 「已經產出過哪些東西？」| Nuwa 21 personas gallery |
| **Strip · Example I/O** | 「輸入什麼 → 輸出什麼」| Nuwa example strip：`› nuwa 蒸餾 費曼 → feynman.skill (21 min)` |

**關鍵約束**：
- 資訊密度要夠（每個 panel 都要承載差異化資訊）
- 但不能塞資料 slop（每個數字都要有意義）
- 配色與 cinematic 一致（同色系，方便切換不突兀）

---

## 3 · 除錯與開發工具

任何長動畫必須配三個 dev 工具，否則除錯會爆炸。

### 工具 1 · `?seek=N` 凍結到第 N 秒

```js
const seek = parseFloat(params.get('seek'));
if (!isNaN(seek)) {
  started = true; muted = true;
  frozenT = seek;  // render() 用這個 t 而不是 elapsed
  cinema.classList.add('show'); dash.classList.add('hide');
}

// render() 裡：
let t = frozenT !== null ? frozenT : (elapsed % T.DURATION);
```

用法：`http://.../slide.html?seek=12` 直接看第 12 秒畫面，不用等播放。

### 工具 2 · `?autoplay=1` 跳過 ▶ overlay

方便 playwright 自動截圖測試，也方便嵌入 iframe 時 force 啟動。

### 工具 3 · 手動 REPLAY 按鈕

右上角小按鈕，使用者/除錯時可以重播任意次。CSS：

```css
.replay{position:absolute;top:18px;right:18px;background:rgba(212,165,116,0.1);
  border:1px solid rgba(212,165,116,0.3);color:#D4A574;
  font-family:monospace;font-size:10px;letter-spacing:.28em;text-transform:uppercase;
  padding:6px 12px;border-radius:1px;cursor:pointer;backdrop-filter:blur(6px);z-index:6}
```

---

## 4 · iframe 嵌入坑（如果 cinematic 嵌在 deck 裡）

### 坑 1 · 父視窗的 click zone 攔截 iframe 內按鈕

如果 deck index.html 加了「左右 22vw 透明 click zone 翻頁」，會**覆蓋到 iframe 內的 ▶ play 按鈕**——使用者點按鈕被吞成「下一頁」。

**修復**：click zone 加 `top: 12vh; bottom: 25vh`，給頂部和底部 25% 不攔截，讓 iframe 內的中央 ▶ 和右下角 ▶ 都能點。

### 坑 2 · iframe 搶焦點後鍵盤事件丟失

使用者點過 iframe 後，焦點在 iframe 裡，父視窗的 ←/→ 鍵盤事件收不到。

**修復**：
```js
iframe.addEventListener('load', () => {
  // 注入鍵盤轉發器
  const doc = iframe.contentDocument;
  doc.addEventListener('keydown', (e) => {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: e.key, ... }));
  });
  // 點選後焦點拉回父視窗
  doc.addEventListener('click', () => setTimeout(() => window.focus(), 0));
});
```

### 坑 3 · file:// vs https:// 行為差異

本地 file:// 測好的 cinematic 部署後可能崩，因為：
- file:// 下 iframe contentDocument 同源
- https:// 下也同源（如果同 host），但 audio autoplay 限制更嚴格

**修復**：
- 部署前用 `python3 -m http.server` 起本地 HTTP 測試一遍
- BGM 必須等使用者點選 ▶ 後再 `bgm.play()`，不要 page-load 立刻播

---

## 5 · 反 pattern 速查表

| ❌ 反 pattern | ✅ 正 pattern |
|---|---|
| 預設 = 黑畫面 ▶ overlay | 預設 = 靜態 dashboard，▶ 是輔助 |
| 4 個 step 橫排同一畫面 fade in | 5 個 scene 全畫面切換，每場只 focus 一件事 |
| 複用模板換文案做不同 demo | 每個 demo 獨立視覺語言（蓋文案能區分） |
| emoji / SVG 手畫當素材 | gpt-image-2 大圖 + extract_grid 去背 |
| 無 BGM 無 SFX | BGM + 11 SFX cues 雙軌制 |
| 用 setTimeout 鏈 schedule | requestAnimationFrame + 全域時間軸 T 物件 |
| linear 動畫 | Expo / cubic-bezier easing |
| 沒有 dev 工具 | `?seek=N` + `?autoplay=1` + REPLAY 按鈕 |
| iframe 內的按鈕被父 click zone 吞 | click zone 加 top/bottom margin 給按鈕讓位 |

---

## 6 · 時間預算

按這套 pattern，一個完整 cinematic demo（含 dashboard）：

| 任務 | 時間 |
|---|---|
| 設計 5-scene narrative + 視覺語言 | 30 分鐘（要慎重，決定獨立性）|
| Dashboard 靜態佈局 + 內容 | 1 小時 |
| Cinematic 5 scenes 實現 | 1.5 小時 |
| Audio cues 調時序 + replay 按鈕 | 30 分鐘 |
| Playwright 截圖驗證 5 個關鍵時刻 | 15 分鐘 |
| **單個 demo 總計** | **3-4 小時** |

第二個 demo 複用框架但**視覺語言必須獨立**，時間約 2-3 小時。
