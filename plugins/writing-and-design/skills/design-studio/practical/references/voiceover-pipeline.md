# Voiceover Pipeline · 解說驅動動畫

> 把動畫從「無聲畫面 + 後期配音」升級為「**先有解說詞，再按音訊實測時長驅動畫面**」的工作流。
> 適用：5-20 分鐘概念解說影片、教學影片、長篇知識科普。
>
> 配套 `references/animation-best-practices.md` 使用——本檔案管 **怎麼把解說和畫面對上**，
> animation-best-practices 管 **每一幀畫面怎麼動**。

---

## 🛑 鐵律 · 在寫一行程式碼之前必讀

> **強調多少遍都不夠：解說動畫的失敗模式 #1 是做成了帶配音的 PowerPoint。**

### 第一條 · 整片是一個連續的運動敘事，不是一組獨立場景

PowerPoint 是 7 張投影片。我們做的是 **1 段持續 X 分鐘的電影**。

**身份切換**：
- ❌ 你不是「在做 7 個 scene 的內容」
- ✅ 你是「在螢幕上讓一個或幾個 hero element 演 X 分鐘的戲」

**視覺骨架 = 一個或幾個貫穿全片的 hero element**：
- 它從 t=0 出現，到結束才離場
- 每個 cue 是它的**狀態變化**（位置 / 大小 / 顏色 / 透視 / 形態），不是「換一個新元素」
- scene 邊界在劇本裡有，**在畫面裡不應該有**——觀眾看不出"這是第 3 個 scene"，只看到一段連續的運動

**反例（本 skill v1 實戰踩坑 · 2026-05-10）**：
- 7 個 `<Scene>` 各自獨立 layout，scene 切換 = 整頁 opacity 1→0 切到下一頁
- 每個 cue = `opacity: p, transform: translateY((1-p)*30px)`（fade-up 單調使用）
- 結果：觀眾看完第一反應「像一頁頁 keynote」，整片質感歸零

**正確模式**：
- 選定 1-2 個 hero element（如本文章 demo 應選「md」「html」兩個字元作為骨架）
- 這兩個字元**從片頭到片尾**一直在螢幕上
- 每段「scene」實際是 hero element 的一次狀態變化
  - opening：兩字元在螢幕中央對峙
  - md-side：md 變大變粗佔據畫面，html 退到角落小字；資料圍繞 md 湧入
  - html-side：html 反轉為主角；md 退到角落
  - the-real-question：兩字元回到中央，但中間出現「≠」分隔
  - the-split：兩字元向兩側推開，中間空白展開
  - activity-proof：兩字元在 timeline 上交替閃爍
  - closing：兩字元落地為最終答案位置
- 這樣整片是「md 和 html 在螢幕上演了 X 分鐘」，不是 7 張獨立 PPT

**最小實現骨架**（直接抄改）：

```jsx
// ── Step 1: 定義 hero 在每個 scene 的目標狀態（位置/大小/不透明度）──
const HERO_KEYS = {
  opening:    { md: { x: 50, y: 35, scale: 1.0, opacity: 1 }, html: { x: 50, y: 65, scale: 1.0, opacity: 1 } },
  'md-side':  { md: { x: 78, y: 50, scale: 1.6, opacity: 1 }, html: { x: 92, y: 8,  scale: 0.25, opacity: 0.4 } },
  'html-side':{ md: { x: 8,  y: 8,  scale: 0.25, opacity: 0.4 }, html: { x: 22, y: 50, scale: 1.6, opacity: 1 } },
  // ... 每段一個 entry，連貫的運動從前一段的 final → 本段的 from
};

// ── Step 2: easing + lerp 工具 ──
const expoOut = t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
const lerp = (a, b, t) => a + (b - a) * t;
const lerpPos = (from, to, t) => ({
  x: lerp(from.x, to.x, t), y: lerp(from.y, to.y, t),
  scale: lerp(from.scale, to.scale, t),
  opacity: lerp(from.opacity ?? 1, to.opacity ?? 1, t),
});

// ── Step 3: HeroAnchor 元件 —— 直接掛在 <NarrationStage> 子級，不放進 <Scene> ──
const HeroAnchor = () => {
  const { time, scene, timeline } = useNarration();
  if (!scene) return null;
  const idx = timeline.scenes.findIndex(s => s.id === scene.id);
  const prevId = idx > 0 ? timeline.scenes[idx - 1].id : scene.id;
  const from = HERO_KEYS[prevId];
  const to   = HERO_KEYS[scene.id];

  // 段內前 ~45% 時間用於從 prev 狀態 morph 到本段狀態，剩餘 hold
  const transitionDur = Math.min(2.0, scene.duration * 0.45);
  const t = expoOut(Math.min(1, (time - scene.start) / transitionDur));
  const md   = lerpPos(from.md,   to.md,   t);
  const html = lerpPos(from.html, to.html, t);

  // 加 subtle breathing 讓任意一幀都有運動（對應鐵律第三條）
  const breath = 1 + Math.sin(time * 0.6) * 0.012;

  const renderHero = (label, pos, color) => (
    <div style={{
      position: 'absolute', left: `${pos.x}%`, top: `${pos.y}%`,
      transform: `translate(-50%, -50%) scale(${pos.scale * breath})`,
      opacity: pos.opacity, color, fontSize: 360, fontWeight: 800,
      lineHeight: 1, willChange: 'transform, opacity', pointerEvents: 'none',
    }}>{label}</div>
  );
  return <>
    {renderHero('md',   md,   '#1B4965')}
    {renderHero('html', html, '#C04A1A')}
  </>;
};

// ── Step 4: 主元件 —— hero 在 NarrationStage 子級，scene 內輔助元素另外管 ──
const App = () => (
  <NarrationStage timeline={TIMELINE} audioSrc="_narration/voiceover.mp3" width={1920} height={1080}>
    <HeroAnchor />  {/* ← 跨 scene 持續存在，整片視覺骨架 */}
    {/* scene 內輔助元素用 useSceneFade 控制軟淡入淡出，不要硬切 */}
    <MdSideAux />
    <HtmlSideAux />
    {/* ... */}
  </NarrationStage>
);
```

**完整可執行參考**：`demos/md-html-narration/md-html-demo.html`（3 分 21 秒，7 段，21 cue，已實戰驗證）

### 第二條 · 場景之間不能「硬切」

| 錯誤模式（PowerPoint slop） | 正確模式（電影感） |
|---|---|
| scene A 整體 `opacity 1→0` 同時 scene B `opacity 0→1` | scene A 的核心元素 **morph 進** B（位置/大小/顏色平滑變換） |
| 每個 scene 獨立 layout，元素出現/消失 | 元素在螢幕上**持續存在**，只是位置和形態在變 |
| `keepMounted=false`，scene 切換瞬間元件被解除安裝 | hero 用 `keepMounted=true`，跨 scene 共享 DOM 節點 |
| 字幕條/資料卡片各自 fade in fade out | 字幕條作為畫面唯一的"非 hero" 入場，hold 後**配合 hero 的運動一起退出** |

實現層面：
- **共享元素跨 scene** → 把 hero 提到 `<NarrationStage>` 直接子級，**不放在任何 `<Scene>` 裡**
- 用 `useNarration()` hook 在 hero 裡讀 `time`、`scene`、`isCueTriggered`，自己根據當前時間決定形態
- `<Scene>` 只用來管那些只在該段出現的輔助元素（資料卡、引用塊等），並且**這些輔助元素也不要硬切**——出場用 expoOut + stagger，退場用 fade overlap 跟下一段疊

### 第三條 · 每一幀畫面都必須有運動

**自檢方法**：在錄製中**任意截一幀**（不是 cue 觸發那一秒）。
- 如果畫面看起來「**完全靜止**」→ 錯。回去加底層運動（background drift / hero subtle scale / camera pan / parallax）
- 永遠有一個**底層運動**在跑（即使不是焦點）：
  - hero element 的 `scale: 1 ↔ 1.02` 5 秒呼吸迴圈
  - 背景 `translateX: 0 ↔ -20px` 緩慢漂移
  - 資料卡片入場後保留 `translateY` 微抖（Perlin noise）
- 一個完全靜止的畫面 = PowerPoint slop

### 第四條 · Easing / Stagger / Hold 是底線

| 項 | 必須 | 禁止 |
|---|---|---|
| Easing | `expoOut` 主軸（`cubic-bezier(0.16, 1, 0.3, 1)`），`overshoot` 強調，`spring` 落位 | `linear`、`ease`、CSS 預設 |
| 多元素入場 | 30ms stagger（每個晚 30ms 進） | 一刀切全部出現 |
| 關鍵 cue 前 | hold 0.3-0.5s 讓觀眾"看見"（前一段元素先靜止 0.3s，再觸發 cue） | 一段說完無縫切下一段 |
| 收尾 | 戛然而止，最後一幀 hold 1s | fade to black |

詳細規則參考 `animation-best-practices.md` 的 §1-§4。

### 自檢 · 第一觀眾反應

做完拿給一個沒看過的人看（或自己 24 小時後再看），**他們的第一反應**是什麼？

| 反應 | 評級 | 行動 |
|---|---|---|
| 「這是帶配音的 PPT」 | 失敗 | 回去重做 |
| 「畫面跟著聲音在切換」 | 不及格 | 缺連續敘事，hero element 不存在或沒貫穿 |
| 「這個東西在動」 | 合格 | 但沒記憶點 |
| 「我想看完」 | 良 | 節奏對了 |
| 「這一段我想截圖」 | great | 你做到了 |

---

## 工作流（高層）

```
                ┌──────────────────────────┐
                │  解說稿 .md（## scene + │
                │  [[cue:xx]] 標關鍵句）   │
                └──────────────┬───────────┘
                               │
                  narrate-pipeline.mjs
                               │
                               ▼
            ┌──────────────────────────────┐
            │ voiceover.mp3 (拼接的整段)  │
            │ timeline.json (實測時長)    │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌─────────────────┐      ┌──────────────────┐
    │ HTML 動畫       │      │ 錄製 MP4 + 混音  │
    │ (NarrationStage)│      │ render-narration │
    │ 實播帶 audio 同步│      │ → 最終發布 MP4   │
    └─────────────────┘      └──────────────────┘
       交付形態 1                交付形態 2
```

## 解說稿格式

放在專案目錄下任意位置，檔名建議 `script.md`：

```markdown
---
title: 什麼是 LLM
voice: S_JSdgdWk22   # 可選，覆蓋 .env 預設音色
speed: 1.0           # 可選，0.5-2.0
gap: 0.4             # 段間靜音秒數，預設 0.3
---

## intro
大家好，今天我們 5 分鐘講清楚 LLM 是什麼。

## what-is
LLM 全稱 Large Language Model，[[cue:bigmodel]]它是一個有幾千億參數的神經網路。
本質是一個文字接龍的預測器。

## demo
比如你輸入「今天天氣」，[[cue:input]]模型會預測下一個字最可能是什麼。
[[cue:predict]]也許是「真好」，也許是「不錯」。
```

**規則**：
- 段標題 `## scene-id` 是英文/數字 + 連字元（如 `## what-is`、`## scene-1`）
- `[[cue:xx]]` 標在**關鍵句中間**——腳本執行時會在該位置切割文字，cue 之後那一刻就是畫面的觸發點
- cue id 在動畫 HTML 裡用 `<Cue id="xx">` 監聽
- 寫解說時**關注節奏 + 短句**，長句 TTS 出來會平淡

## timeline.json schema

```ts
{
  title: string,
  voice: string | null,
  speed: number,
  gap: number,
  totalDuration: number,        // 整段 voiceover.mp3 的實測秒數
  voiceover: 'voiceover.mp3',   // 相對 timeline.json 的路徑
  scenes: [
    {
      id: string,
      start: number,            // 該段在整段音訊裡的開始時間
      end: number,
      duration: number,
      audio: 'audio/<id>.mp3',  // 該段單獨音訊（合併前的子段已 concat）
      text: string,             // 已剝離 [[cue:xx]] 標記的整段文字
      // chunks 是字幕顯示的源——每個 chunk 是被 cue 切開的子段，含 TTS 實測時間窗
      chunks: [
        {
          text: string,            // 子段文字
          start: number,           // 段內相對時間
          end: number,
          absoluteStart: number,   // 整軌絕對時間（對齊 voiceover.mp3）
          absoluteEnd: number,
        }
      ],
      cues: [
        {
          id: string,
          offset: number,       // 段內相對時間
          absoluteTime: number, // 整段時間軸上的絕對時間
        }
      ]
    }
  ]
}
```

`absoluteTime` 和 `absoluteStart/End` 都是**真實測出來的**——pipeline 把段內文字按 cue 切成子段分別 TTS，時間 = 累加前面子段的實測時長。**不是按字元數線性估算的近似值**。

## 字幕（Subtitles）

> **字幕是預設帶的**——長解說影片沒字幕，留存率會顯著下降。NarrationStage 提供 `<Subtitles />` 開箱即用。

### 用法（一行）

```jsx
const { NarrationStage, Subtitles } = NarrationStageLib;
<NarrationStage timeline={TIMELINE} audioSrc="...">
  {/* 你的 hero / scene 內容 */}
  <Subtitles />  {/* ← 自動從 timeline.scenes[].chunks 取活動文字 */}
</NarrationStage>
```

### 視覺規則（B 站風 · 反 PowerPoint）

| 項 | 規則 | 反例 |
|---|---|---|
| 背景 | **無背景**（不要黑色橫條不要 backdrop-blur）| 半透明黑底 + blur = 字幕條壓住畫面 = PPT 感 |
| 字色 | **淺底用深墨 `#1a1a1a` + 白光暈**；深底用白字 + 黑光暈 | 淺底白字+黑描邊 = 字糊 |
| 字級 | 32px（1080p 影片）| <24px 看不清，>40px 搶主視覺 |
| 字型 | `PingFang SC` / `Noto Sans SC`（無襯線，B 站標準）| 襯線字型 = 像電影字幕 |
| 位置 | bottom: 90px（不貼邊）| 貼底邊顯得廉價 |
| 單行長度 | **≤ 12-13 字**（中英混合時英文按 0.5 字算）| >15 字一行手機端讀不完 |
| 切句規則 | **絕不跨句號截斷**：先按 `。！？` 切句，每句再按 `，、；：` 合併到 ≤maxLen | 按字數硬切，把「這是好的」切成「這是好」+「的」 |

`<Subtitles />` 預設按以上規則跑，不需要傳 props。深底場景：`<Subtitles color="#fff" haloColor="rgba(0,0,0,0.85)" />`。

### 切句演算法（已在 narration_stage.jsx 內建）

```js
splitChunkToLines(text, maxLen = 13)
// 1. 強標點切句（。！？\n）
// 2. 每句 ≤ maxLen 直接保留
// 3. 否則按弱標點（，、；：）切片，合併到 ≤ maxLen
// 4. 保底硬切（罕見）
// 中英混合：英文/數字按 0.5 字算視覺寬度
```

如果 chunk 切完後某行明顯太長或太短，**改解說稿裡 cue 位置**（cue 把段切得更細），不要在前端調切句邏輯。

## NarrationStage API

```jsx
import 'assets/narration_stage.jsx';
const { NarrationStage, Scene, Cue, useNarration } = NarrationStageLib;

<NarrationStage
  timeline={TIMELINE}                  // timeline.json 內容
  audioSrc="_narration/voiceover.mp3"  // 相對當前 HTML 的路徑
  width={1920} height={1080}
  background="#f5f1e8"
  controls={true}                      // 實播時顯示底部播放條
>
  {/* hero element：跨 scene 持續存在 —— 直接放在 NarrationStage 子級 */}
  <HeroAnchor />

  {/* scene 內輔助元素：只在該段出現 */}
  <Scene id="intro">
    <Cue id="bigmodel">{(triggered, progress) => (
      <SomeElement style={{ opacity: progress }} />
    )}</Cue>
  </Scene>
</NarrationStage>
```

**Hooks**：
- `useNarration()` 返回 `{ time, scene, sceneTime, isCueTriggered, cueProgress }`
- 在自訂元件裡直接讀，不需要傳 props

**Scene 元件**：
- 預設只在 `scene.id === id` 時掛載
- 加 `keepMounted` 持續掛載（跨 scene 動畫連續時用）

**Cue 元件**：
- children 必須是 `(triggered, progress) => ReactNode`
- progress 是 cue 觸發後 0→1 的漸進值（預設 0.6s ramp）

## 時間源（雙軌）

NarrationStage 自動檢測 `window.__recording`：
- **實播模式**（預設）：跟隨 audio 元素的 currentTime，使用者暫停/拖動 seek 都能同步
- **錄影片模式**（render-video.js 設定 `window.__recording = true`）：rAF wall-clock 自驅動從 0 開始，暴露 `window.__seek(t)` 給 render-video.js 復位

## 工具腳本

| 腳本 | 輸入 | 輸出 |
|---|---|---|
| `scripts/tts-doubao.mjs` | 單段文字 | 單個 mp3 + 實測時長 |
| `scripts/narrate-pipeline.mjs` | 解說稿 .md | voiceover.mp3 + timeline.json |
| `scripts/mix-voiceover.sh` | 影片 + voiceover.mp3 [+ BGM] | 帶音訊的 MP4 |
| `scripts/render-narration.sh` | 解說 HTML + timeline.json | 最終 MP4（錄製 + 混音一條龍）|

## .env 配置

skill 根目錄下 `.env`（已 gitignore）：

```
DOUBAO_TTS_API_KEY=<your_api_key>
DOUBAO_TTS_VOICE_ID=zh_female_xiaohe_uranus_bigtts
DOUBAO_TTS_ENDPOINT=https://openspeech.bytedance.com/api/v3/tts/unidirectional
```

也可使用控制台的 App ID + Access Token 鑑權：

```
DOUBAO_APP_ID=<your_app_id>
DOUBAO_ACCESS_KEY=<your_access_token>
DOUBAO_TTS_VOICE_ID=zh_female_xiaohe_uranus_bigtts
```

`DOUBAO_TTS_RESOURCE_ID` 預設按音色自動推斷：`S_` 克隆音色使用 `seed-icl-1.0`，`uranus` 官方音色使用 `seed-tts-2.0`，其他官方音色使用 `seed-tts-1.0`。

## 標準工作流（10 步）

1. **寫解說稿**：解說稿是原始碼。先把整段口播寫完整，標段標題 `## scene-id`，關鍵句前加 `[[cue:xx]]`
2. **跑 narrate-pipeline**：`node scripts/narrate-pipeline.mjs --script script.md --out-dir _narration`
3. **聽整段 voiceover.mp3**：節奏不對回去改稿。**這一步決定整片品質上限**
4. **🛑 設計前先回答鐵律**：hero element 是什麼？它在每段是什麼狀態？跨場景怎麼 morph？答不上不要寫程式碼
5. **寫動畫 HTML**：用 NarrationStage + 一個或幾個 hero element 跨 scene 演戲
6. **實播預覽**：瀏覽器開啟 HTML，點 ▶ Play，聽畫面+解說同步
7. **第一觀眾自檢**：用上面「自檢 · 第一觀眾反應」表打分。失敗回到 Step 4 重做
8. **錄影片**：`bash scripts/render-narration.sh demo.html --timeline=_narration/timeline.json`（自動錄無聲 MP4 + 混入 voiceover）
9. **可選 BGM**：在 render-narration 加 `--bgm-mood=educational`（或 tech / tutorial 等）
10. **交付**：瀏覽器 HTML（即時演示用）+ 最終 MP4（發布用）

## 異常處理

| 問題 | 解決 |
|---|---|
| TTS API 報錯 | 檢查 .env 裡 `DOUBAO_TTS_API_KEY`，或 `DOUBAO_APP_ID` + `DOUBAO_ACCESS_KEY` 是否正確 |
| 某段音訊明顯比解說稿長/短 | 該段文字裡有奇怪標點或 emoji，TTS 解析異常 → 改稿 |
| cue absoluteTime 不準 | 段內子段拼接時 ffmpeg 有問題 → 檢查 mp3 編碼一致性 |
| 錄影片結果出現黑畫面 | render-video.js 沒拿到 `window.__ready` 訊號 → 檢查 NarrationStage 是否正常掛載 |
| 錄影片畫面卡頓 | 動畫裡有重 layout（大量 box-shadow / blur）→ 簡化或預合成 |
| 實播音畫不同步 | audio 元素載入延遲 → 加 `preload="auto"` 或本地預載入 |

## 何時不用這套 pipeline

- **<60s 短動畫**：直接做無聲動畫 + 後期配音（add-music.sh + 一段單獨 TTS）即可，不需要 timeline 驅動
- **純 BGM 影片**：用 `add-music.sh` 加預設 BGM
- **真人錄音替換 TTS**：把 `voiceover.mp3` 替換成真人錄音，timeline 自己手寫或用 ffprobe 測段時長 + 工具腳本生成 → 流程其餘部分通用

---

**最後一次提醒**：寫程式碼前回到鐵律。**別做帶配音的 PowerPoint**。
