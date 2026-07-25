# SFX Library · huashu-design

> 全部由 ElevenLabs Sound Generation API 生成，蘋果發表會級音質。
> 產品級 SFX 資產庫，覆蓋花叔動畫/演示/產品 Demo 全場景。

**資產位置**：`assets/sfx/<category>/<name>.mp3`
**總數**：37 個 SFX（30 批次生成 + 7 個 v7b 保留）
**生成模型**：ElevenLabs Sound Generation API（prompt_influence 0.4）
**音質**：44.1kHz MP3，蘋果發表會級清晰度，無額外混響

---

## 目錄結構

```
assets/sfx/
├── keyboard/      type, type-fast, delete-key, space-tap, enter
├── ui/            click, click-soft, focus, hover-subtle, tap-finger, toggle-on
├── transition/    whoosh, whoosh-fast, swipe-horizontal, slide-in, dissolve
├── container/     card-snap, card-flip, stack-collapse, modal-open
├── feedback/      success-chime, error-tone, notification-pop, achievement
├── progress/      loading-tick, complete-done, generate-start
├── impact/        logo-reveal, logo-reveal-v2, brand-stamp, drop-thud
├── magic/         sparkle, ai-process, transform
└── terminal/      command-execute, output-appear, cursor-blink
```

---

## 快速索引

### ⌨️ Keyboard（鍵盤輸入）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/keyboard/type.mp3` | 0.5s | 單鍵敲擊（mechanical keyboard single key） | mechanical keyboard single key press |
| `sfx/keyboard/type-fast.mp3` | 1.5s | 連續快速打字（演示輸入提示詞） | fast continuous typing rhythm, apple magic keyboard |
| `sfx/keyboard/delete-key.mp3` | 0.5s | backspace 回刪 | single backspace key, low pitched thud |
| `sfx/keyboard/space-tap.mp3` | 0.5s | 空格鍵輕擊 | soft spacebar tap, wide flat |
| `sfx/keyboard/enter.mp3` | 0.5s | 回車確認（v7b 保留） | enter key press, crisp tactile |

### 🎯 UI（介面互動）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/ui/click.mp3` | 0.5s | 標準 UI 點選（v7b 保留） | crisp modern interface click |
| `sfx/ui/click-soft.mp3` | 0.5s | 柔和 UI click（次要按鈕/連結） | soft gentle button click, mid pitched |
| `sfx/ui/focus.mp3` | 0.5s | 元素聚焦/選中（v7b 保留） | subtle focus tone, element highlight |
| `sfx/ui/hover-subtle.mp3` | 0.5s | 懸停提示（微秒級回饋） | barely audible tick, air whisper |
| `sfx/ui/tap-finger.mp3` | 0.5s | 行動裝置 tap（iOS 介面） | finger tap on touchscreen, muted thud |
| `sfx/ui/toggle-on.mp3` | 0.5s | 開關開啟 | ios toggle switch flip, satisfying click |

### 🌊 Transition（過渡）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/transition/whoosh.mp3` | 0.5s | 標準 whoosh（v7b 保留） | air whoosh transition |
| `sfx/transition/whoosh-fast.mp3` | 0.6s | 快速 whoosh（標題閃入、標籤切換） | quick fast air whoosh, cinematic |
| `sfx/transition/swipe-horizontal.mp3` | 0.7s | 橫向滑動（輪播、tab 切換） | smooth left-to-right air movement |
| `sfx/transition/slide-in.mp3` | 0.6s | 元素滑入（side panel、抽屜） | smooth soft whoosh with arrival |
| `sfx/transition/dissolve.mp3` | 0.8s | 柔化融化（圖片淡出淡入） | soft dissolve, airy shimmer |

### 🃏 Container（卡片/容器）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/container/card-snap.mp3` | 0.5s | 卡片吸附/定位（v7b 保留） | card snap into place |
| `sfx/container/card-flip.mp3` | 0.7s | 卡片翻轉（前後面切換） | playing card flip, crisp snap |
| `sfx/container/stack-collapse.mp3` | 0.8s | 堆疊合攏（列表聚合） | cards stacking, paper taps collapsing |
| `sfx/container/modal-open.mp3` | 0.6s | 模態框開啟 | modal popping open, whoosh + thud |

### 🔔 Feedback（通知/回饋）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/feedback/success-chime.mp3` | 1.0s | 成功提示（支付成功、任務完成） | two ascending bell tones, ios-style |
| `sfx/feedback/error-tone.mp3` | 0.7s | 錯誤提示（警告、失敗） | descending two-note warning, soft |
| `sfx/feedback/notification-pop.mp3` | 0.6s | 訊息彈出（toast、通知） | notification bloop, ios message alert |
| `sfx/feedback/achievement.mp3` | 1.5s | 成就達成（里程碑、徽章） | triumphant rising arpeggio, game-style |

### ⏳ Progress（進度/狀態）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/progress/loading-tick.mp3` | 0.5s | 載入計時（進度條節拍） | soft short pulse, minimal ambient |
| `sfx/progress/complete-done.mp3` | 0.8s | 完成確認（step 完成） | two ascending satisfying tones |
| `sfx/progress/generate-start.mp3` | 0.8s | AI 開始生成 | soft rising shimmer, magical whoosh |

### 💥 Impact（品牌/衝擊）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/impact/logo-reveal.mp3` | 0.7s | Logo impact（v7b 保留） | logo reveal thud |
| `sfx/impact/logo-reveal-v2.mp3` | 1.5s | 更長的 Logo impact（電影感） | cinematic bass hit with shimmer tail |
| `sfx/impact/brand-stamp.mp3` | 1.0s | 印章重擊（認證、蓋章） | rubber stamp thud, paper contact |
| `sfx/impact/drop-thud.mp3` | 0.7s | 物件落地（插入、放置） | heavy thud, wood surface contact |

### ✨ Magic（AI 變換）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/magic/sparkle.mp3` | 0.8s | 魔法閃光（AI 高亮、驚喜） | bright twinkling stars, fairy dust |
| `sfx/magic/ai-process.mp3` | 1.2s | AI 處理音（thinking 狀態） | modulating digital hum with shimmer |
| `sfx/magic/transform.mp3` | 1.0s | 變換過渡（morph 效果） | rising shimmer whoosh with sparkle tail |

### 💻 Terminal（命令列）

| 檔案 | 時長 | 用途 | Prompt 要點 |
|---|---|---|---|
| `sfx/terminal/command-execute.mp3` | 0.5s | 命令執行 | crisp digital beep with tick, hacker ui |
| `sfx/terminal/output-appear.mp3` | 0.6s | 輸出出現 | rapid digital ticks, retro printout |
| `sfx/terminal/cursor-blink.mp3` | 0.5s | 游標閃爍 | subtle soft digital pulse, rhythmic |

---

## 按場景推薦搭配

### 💻 Terminal 互動演示
```
type (0.5s) → enter (0.5s) → command-execute (0.5s) → output-appear (0.6s)
```
迴圈元素：`cursor-blink` 作為 idle 時的環境音。

### 🃏 卡片選擇流程
```
hover-subtle (0.5s, UI懸停) → click-soft (0.5s, 點選) → card-snap (0.5s, 定位)
```
或進階版：`card-flip` 做前後面切換。

### 🤖 AI 生成全流程
```
generate-start (0.8s, 啟動) → ai-process (1.2s, 處理) → sparkle (0.8s, 閃現) → complete-done (0.8s, 完成)
```
錯誤時用 `error-tone` 替代 `complete-done`。

### 🎬 Logo Reveal（品牌時刻）
```
whoosh-fast (0.6s, 鋪墊) → logo-reveal-v2 (1.5s, 落點) → sparkle (0.8s, 尾韻)
```
簡版：`whoosh → logo-reveal`（直接 v7b 兩件套）。

### 📱 UI 互動演示（行動裝置）
```
tap-finger (0.5s, 點選) → slide-in (0.6s, 面板滑入) → toggle-on (0.5s, 開關)
```
完成後：`success-chime` 或 `notification-pop`。

### 📊 資料視覺化/儀表板
```
loading-tick (0.5s, 節拍) × N → complete-done (0.8s, 資料到位) → achievement (1.5s, 驚豔落點)
```

### 🎯 表單提交流程
```
click-soft (0.5s) → loading-tick ×2 (1.0s) → success-chime (1.0s)
```
失敗分支：`error-tone (0.7s)`。

### 🪄 Magic Transform 場景
```
whoosh-fast (0.6s) → transform (1.0s) → sparkle (0.8s)
```
適合：元素變形、效果前後對比、"AI 重寫"等演示。

---

## 使用規範

### 音量建議（來自 apple-gallery-showcase.md 音訊雙軌制）
- **SFX 主軌**：`1.0`（不做衰減）
- **BGM 背景軌**：`0.4 ~ 0.5`（SFX 明顯穿透）
- **多 SFX 疊加**：用 `amix=inputs=N:duration=longest:normalize=0` 保留動態範圍

### ffmpeg 拼接模板
```bash
# 單 SFX 對齊時間點：
ffmpeg -i video.mp4 -itsoffset 2.5 -i sfx/ui/click.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=longest:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4

# 多 SFX + BGM：
ffmpeg -i video.mp4 \
  -itsoffset 1.0 -i sfx/transition/whoosh-fast.mp3 \
  -itsoffset 1.6 -i sfx/impact/logo-reveal-v2.mp3 \
  -i bgm.mp3 \
  -filter_complex "[3:a]volume=0.4[bgm];[0:a][1:a][2:a][bgm]amix=inputs=4:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4
```

### 選型決策樹
1. **有 tactile 動作**（打字/點選/滑動）→ `keyboard/` or `ui/`
2. **元素進場/出場** → `transition/`
3. **容器層操作**（卡片/模態） → `container/`
4. **狀態回饋**（成功/失敗/通知） → `feedback/`
5. **進度/時間流逝** → `progress/`
6. **品牌落點/重要時刻** → `impact/`
7. **AI 魔法/變換** → `magic/`
8. **命令列/程式碼演示** → `terminal/`

### 避免疊音堆積
- 同一個時間點 `max 2 個 SFX` 併發
- BGM 降到 0.3 以下時可以放 3 個
- 品牌 impact 時清空其他 SFX（留空 0.2s 再落點）

---

## Prompt 撰寫原則（供複用）

參考風格：`apple keynote, tight, minimal, no reverb unless ambient, crisp, elegant`

**好 prompt 的三要素**：
1. **聲音物理描述**：什麼物體、什麼動作（"mechanical keyboard single key press"）
2. **質感/風格限定**：apple-style / ios-style / cinematic / retro
3. **反例排除**：no reverb / clean studio / minimal

❌ "click sound"
✅ "crisp ui button click, clean modern interface sound, apple-style, high pitched"

❌ "magic"
✅ "bright twinkling stars sound, high pitched glittery chime, fairy dust"

---

## 詳見
- 音訊雙軌制與 ffmpeg 拼接：`apple-gallery-showcase.md`
- 原始生成腳本：`/tmp/gen_sfx_batch.sh`（一次性批次生成器）
