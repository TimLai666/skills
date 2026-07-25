# Video Export：HTML 動畫匯出為 MP4/GIF

動畫 HTML 完成後，使用者常想「能匯出影片嗎」。這份指南給出完整流程。

## 何時匯出

**匯出時機**：
- 動畫完整跑通、視覺驗證過（Playwright 截圖確認各時間點狀態正確）
- 使用者在瀏覽器裡看過至少一次，表示效果 OK
- **不要**在動畫 bug 沒修完的階段匯出——匯出到影片後改起來更貴

**使用者可能說的觸發語**：
- 「能匯出成影片嗎」
- 「轉成 MP4」
- 「做成 GIF」
- 「60fps」

## 產出規格

預設一次給三種格式，讓使用者選：

| 格式 | 規格 | 適合場景 | 典型大小（30s） |
|---|---|---|---|
| MP4 25fps | 1920×1080 · H.264 · CRF 18 | 公眾號嵌入、視頻號、YouTube | 1-2 MB |
| MP4 60fps | 1920×1080 · minterpolate 插幀 · H.264 · CRF 18 | 高幀率展示、B站、作品集 | 1.5-3 MB |
| GIF | 960×540 · 15fps · palette 最佳化 | Twitter/X、README、Slack 預覽 | 2-4 MB |

## 工具鏈

這些腳本在 `scripts/`：

### 1. `render-video.js` — HTML → MP4

錄一個 25fps 的 MP4 基礎版本。依賴全域安裝的 playwright。

```bash
NODE_PATH=$(npm root -g) node <skill根目錄>/scripts/render-video.js <html檔案>
```

可選參數：
- `--duration=30` 動畫時長（秒）
- `--width=1920 --height=1080` 解析度
- `--trim=2.2` 從影片開頭裁掉的秒數（去掉 reload + 字型載入時間）
- `--fontwait=1.5` 字型載入等待時間（秒），字型多時調高

輸出：與 HTML 同目錄，同名 `.mp4`。

### 2. `add-music.sh` — MP4 + BGM → MP4

給無聲 MP4 混入背景音樂，按場景（mood）從內建 BGM 庫裡選，也可自帶音訊。自動匹配時長、加淡入淡出。

```bash
bash add-music.sh <input.mp4> [--mood=<name>] [--music=<path>] [--out=<path>]
```

**內建 BGM 庫**（在 `assets/bgm-<mood>.mp3`）：

| `--mood=` | 風格 | 適配場景 |
|-----------|------|---------|
| `tech`（預設） | Apple Silicon / 蘋果發表會，極簡合成器+鋼琴 | 產品發布、AI工具、Skill 宣傳 |
| `ad` | upbeat 現代電子，有 build + drop | 社交媒體廣告、產品預告、促銷片 |
| `educational` | 溫暖明亮、輕吉他/電鋼琴，inviting | 科普、教學介紹、課程預告 |
| `educational-alt` | 同類備選，換一首試試 | 同上 |
| `tutorial` | lo-fi 環境音，幾乎無存在感 | 軟體演示、程式設計教學、長演示 |
| `tutorial-alt` | 同類備選 | 同上 |

**行為**：
- 音樂按影片時長裁剪
- 0.3s 淡入 + 1s 淡出（避免硬切）
- 影片流 `-c:v copy` 不重編碼，音訊 AAC 192k
- `--music=<path>` 優先順序高於 `--mood`，可以直接指定任意外部音訊
- 傳錯 mood 名會列出所有可用選項，不會靜默失敗

**典型流水線**（動畫匯出三件套 + 配樂）：
```bash
node render-video.js animation.html                        # 錄影
bash convert-formats.sh animation.mp4                      # 派生 60fps + GIF
bash add-music.sh animation-60fps.mp4                      # 加預設 tech BGM
# 或針對不同場景：
bash add-music.sh tutorial-demo.mp4 --mood=tutorial
bash add-music.sh product-promo.mp4 --mood=ad --out=promo-final.mp4
```

### 3. `convert-formats.sh` — MP4 → 60fps MP4 + GIF

從已有 MP4 生成 60fps 版本和 GIF。

```bash
bash <skill根目錄>/scripts/convert-formats.sh <input.mp4> [gif_width] [--minterpolate]
```

輸出（與輸入同目錄）：
- `<name>-60fps.mp4` — 預設用 `fps=60` 幀複製（相容性廣）；加 `--minterpolate` 啟用高品質插幀
- `<name>.gif` — palette 最佳化的 GIF（預設 960 寬，可改）

**60fps 模式選擇**：

| 模式 | 命令 | 相容性 | 使用場景 |
|---|---|---|---|
| 幀複製（預設）| `convert-formats.sh in.mp4` | QuickTime/Safari/Chrome/VLC 全通 | 通用交付、上傳平台、社交媒體 |
| minterpolate 插幀 | `convert-formats.sh in.mp4 --minterpolate` | macOS QuickTime/Safari 可能拒打 | B站等需要真插幀的展示場景，**交付前必須本地測**目標播放器 |

為什麼預設改成幀複製？minterpolate 輸出的 H.264 elementary stream 有 known compat bug——之前預設 minterpolate 時多次踩到「macOS QuickTime 打不開」的問題。詳見 `animation-pitfalls.md` §14。

`gif_width` 參數：
- 960（預設）—— 社交平台通用
- 1280 —— 更清晰但檔案更大
- 600 —— Twitter/X 優先載入

### 4. `render-video-seek.js` — 真 60fps / 確定性渲染（推薦高品質交付）

`render-video.js` 的 recordVideo 路徑有三個固有限制：幀率被 Chromium compositor 鎖死 25fps、開頭有載入黑幀需 trim、60fps 只能靠事後 minterpolate 插幀（有 ghosting + macOS QuickTime 相容 bug，見 `animation-pitfalls.md §14`）。需要**真 60fps、確定性輸出、或交付 B站/作品集**時，改用 seek 渲染。

它逐幀 seek 到時間戳截圖、再用 ffmpeg 把 PNG 序列編碼成 MP4。技術核心借鑑 HeyGen HyperFrames（Apache 2.0）的「凍結時鐘 + seek 截圖」思路，但不引入任何第三方包——只用本 skill 已有的 playwright + ffmpeg，runtime 中立。

```bash
NODE_PATH=$(npm root -g) node /path/to/claude-design/scripts/render-video-seek.js <html檔案> --fps=60
```

參數：`--duration` · `--fps`（預設 60）· `--width` · `--height` · `--concurrency`（預設 4 個 worker 並行）· `--settle`（seek 後等幾個 rAF 再截圖，預設 2，重 layout 動畫可調高）· `--keep-chrome`。輸出與 HTML 同目錄、同名 `.mp4`。

正面解決 recordVideo 三死結：
- **真原生任意幀率**：`--fps=60` 出真 60fps（每幀都是真實 seek 畫面），不再經 `convert-formats.sh` 的 minterpolate 插幀，繞開 ghosting + macOS 相容 bug
- **無開頭黑幀**：不走錄影，根本沒有載入期黑幀，不需要 `--trim` / `--fontwait`
- **確定性**：seek 到時間戳截圖，同輸入同輸出，不受機器負載/丟幀影響

**適用邊界（重要）**：只支援走 Stage 時鐘的動畫——`assets/animations.jsx` 的 `<Stage>` 或 `narration_stage.jsx` 的 `<NarrationStage>`，它們會響應 `window.__seekRender` 凍結自驅時鐘並暴露 `window.__seek(t)`。純 CSS `@keyframes` / Lottie / 手寫非 Stage 動畫不吃 `__seek`，這類繼續用 `render-video.js`（腳本檢測不到 `__seek` 會報錯並提示）。

**代價**：逐幀截圖，長影片總耗時可能比 recordVideo 即時錄更久（靠 `--concurrency` 多 worker 緩解）；大量臨時 PNG 佔磁碟空間，渲染前建議關其他大記憶體 App。

**二選一策略**：預設仍用 `render-video.js`（零風險、覆蓋所有動畫類型）；需要真 60fps / 確定性 / 高品質交付、且動畫走 Stage 時鐘時，用 `render-video-seek.js`。帶解說的長動畫用 `render-narration.sh --seek` 一鍵走 seek 渲染 + 混音。

## 完整流程（標準推薦）

使用者說「匯出影片」後：

```bash
cd <專案目錄>

# 假設 $SKILL 指向本 skill 的根目錄（自行按安裝位置替換）

# 1. 錄 25fps 基礎 MP4
NODE_PATH=$(npm root -g) node "$SKILL/scripts/render-video.js" my-animation.html

# 2. 派生 60fps MP4 和 GIF
bash "$SKILL/scripts/convert-formats.sh" my-animation.mp4

# 產出清單：
# my-animation.mp4         (25fps · 1-2 MB)
# my-animation-60fps.mp4   (60fps · 1.5-3 MB)
# my-animation.gif         (15fps · 2-4 MB)
```

## 技術細節（排錯用）

### Playwright recordVideo 的坑

- 幀率固定 25fps，無法直接錄 60fps（Chromium headless 的 compositor 上限）
- 從 context 建立就開始錄，必須用 `trim` 裁掉前面的載入時間
- 預設 webm 格式，需要 ffmpeg 轉 H.264 MP4 才能通用播放

`render-video.js` 已處理以上問題。

### ffmpeg minterpolate 參數

當前配置：`minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`

- `mi_mode=mci` — motion compensation interpolation（運動補償）
- `mc_mode=aobmc` — adaptive overlapped block motion compensation
- `me_mode=bidir` — 雙向運動估計
- `vsbmc=1` — 可變 size block motion compensation

對 CSS **transform 動畫**（translate/scale/rotate）效果好。
對**純 fade** 可能產生輕微 ghosting——如果使用者嫌棄，退化為簡單幀複製：

```bash
ffmpeg -i input.mp4 -r 60 -c:v libx264 ... output.mp4
```

### GIF palette 為何要兩階段

GIF 只能 256 色。一次 pass 的 GIF 會把全動畫色彩壓到 256 色通用 palette，對米色底+橙色這種細膩配色會糊。

兩階段：
1. `palettegen=stats_mode=diff` —— 先掃描全片，生成**針對此動畫的 optimal palette**
2. `paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle` —— 用這個 palette 編碼，rectangle diff 只更新變化區域，大幅減小檔案

對 fade 過渡用 `dither=bayer` 比 `none` 更平滑，但檔案大一點。

## Pre-flight check（匯出前）

匯出前 30 秒自檢：

- [ ] HTML 在瀏覽器裡完整跑過一遍，無控制台錯誤
- [ ] 動畫第 0 幀是完整初始狀態（不是空白載入中）
- [ ] 動畫最後一幀是穩定的收尾狀態（不是半截）
- [ ] 字型/圖片/emoji 全部正常渲染（參考 `animation-pitfalls.md`）
- [ ] Duration 參數與 HTML 裡的實際動畫時長匹配
- [ ] HTML 中 Stage 檢測 `window.__recording` 強制 loop=false（手寫 Stage 必查；用 `assets/animations.jsx` 自帶）
- [ ] 結尾 Sprite 的 `fadeOut={0}`（影片末幀不淡出）
- [ ] 含「Created by Huashu-Design」浮水印（僅動畫場景必加；第三方品牌作品加「非官方出品 · 」前綴。詳見 GUIDE.md §「Skill 推廣浮水印」）

## 交付時附帶的說明

匯出完成後給使用者的標準說明格式：

```
**完整交付**

| 檔案 | 格式 | 規格 | 大小 |
|---|---|---|---|
| foo.mp4 | MP4 | 1920×1080 · 25fps · H.264 | X MB |
| foo-60fps.mp4 | MP4 | 1920×1080 · 60fps（運動插幀）· H.264 | X MB |
| foo.gif | GIF | 960×540 · 15fps · palette 最佳化 | X MB |

**說明**
- 60fps 用 minterpolate 做運動估計插幀，transform 動畫效果好
- GIF 用 palette 最佳化，30s 動畫可壓到 3MB 左右

要換尺寸或幀率說一聲。
```

## 常見使用者追加需求

| 使用者說 | 應對 |
|---|---|
| 「太大了」 | MP4：提高 CRF 到 23-28；GIF：降解析度到 600 或 fps 到 10 |
| 「GIF 太糊」 | 提高 `gif_width` 到 1280；或者建議用 MP4 代替（微信朋友圈也支援） |
| 「要直式 9:16」 | 改 HTML 源的 `--width=1080 --height=1920`，重新錄 |
| 「加浮水印」 | ffmpeg 加 `-vf "drawtext=..."` 或 `overlay=` 一個 PNG |
| 「要透明背景」 | MP4 不支援 alpha；用 WebM VP9 + alpha 或 APNG |
| 「要無損」 | CRF 改 0 + preset veryslow（檔案會大 10 倍） |

## Skill 推廣浮水印模板（僅動畫匯出用）

GUIDE.md 規定動畫 MP4/GIF 預設帶浮水印，模板如下（深底改用 `rgba(255,255,255,0.35)`；第三方品牌動畫前綴「非官方出品 · 」）：

```jsx
<div style={{
  position: 'absolute', bottom: 24, right: 32,
  fontSize: 11, color: 'rgba(0,0,0,0.4)',
  letterSpacing: '0.15em', fontFamily: 'monospace',
  pointerEvents: 'none', zIndex: 100,
}}>
  Created by Huashu-Design
</div>
```
