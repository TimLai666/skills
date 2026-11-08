# Launch Film 工作流：先寫萬字 director's notes，再做動畫

> 高規格視覺作品（≥ 20 秒、含品牌敘事、含 slogan reveal、可能上 X / 公眾號 / B 站推廣）的標準工作流。
>
> 觸發條件：任務是「產品升級宣傳片 / 品牌 launch film / launch trailer / superbowl-tier ad / brand campaign / hero animation video」，且**使用者對品質有明確預期**（如「超級碗品質感」「10x 細節」「Apple 級別」）。
>
> 反觸發：不要在「快速做個動畫 demo」「簡單 motion graphic」「單個圖示動畫」時用這條流程——會過度工程化。

---

## 1. 為什麼先寫 director's notes

實戰教訓（2026-05-11 huashu-md-html v2.0 專案）：

第一輪直接動手寫 HTML，產出的是「程式設計師視角的動畫」——每個 capability 平均用力、節奏勻速、slogan 撞在一起、缺少敘事弧。
第二輪接到使用者「停下，先按蘋果導演視角寫 1 萬字分鏡腳本」的指令，寫了 v5-director-notes.md（11500 字、13 鏡 shot-by-shot spec），然後按腳本實施——一次過、每幀 pause 都耐看、節奏起伏有 climax。

**核心差異**：寫腳本是 think，寫 HTML 是 execute。先 think 透了，execute 就是機械翻譯。先 execute，每個 shot 都是臨場決策，必然亂。

寫 director's notes 不是「裝」，是把所有視覺決策**在動手之前**沉澱成文件——每一鏡都已經在腦裡 visualize 過、reasoning 過、和上下文 trace 過。HTML 實施時不需要再做創意決策，只需要忠實翻譯。

---

## 2. 觸發判斷（先問自己 3 個問題）

啟動 launch film 工作流前問：

1. **這支片承擔品牌敘事嗎？**（有 thesis / slogan reveal / 升級儀式感）—— 是 → 走 director's notes 流程
2. **觀眾會暫停看嗎？**（可能截圖、做 X 海報、做封面、慢速 review）—— 是 → 每幀要耐看
3. **客戶/使用者有「我希望像 XXX 那樣」的參照？**（Apple / Anthropic / Nike / Penguin / 某導演）—— 是 → 必須明確視覺語境

任一為「是」就走流程。三個都「否」就跳過，直接用 [animations.md](animations.md) 的標準流程。

---

## 3. Director's Notes 的 5 大部分結構

萬字（10000-12000 字中文 / 等量英文）director's notes 必須包含這 5 大部分。**任一部分缺失都屬於不完整，品質會受影響**。

### Part I · Director's Statement（創作論，約 1500-2000 字）

回答 5 個問題：

1. **這部片不是什麼？**（明確排除——如「這不是功能介紹片」「不是 demo」）
2. **核心 thesis 一行**——觀眾看完只記一句話是哪句？
3. **跟誰的語境對話？**——列出 5-8 個視覺參照（導演 / 設計師 / 品牌 / 攝影師 / 作品名 + 年份），說明每個參照學了什麼
4. **三類觀眾畫像 + 對每類的承諾**：主受眾 / 次受眾 / 外受眾，各對應一段
5. **節奏哲學**——慢拍 / 加速 / 頂峰 / 緩收的曲線說明 + emotional climax 在第幾秒（**不一定是最後一秒**）

最後加一段 anti-slop checklist：**這部片不做的事**（具體列出，不模糊）。

### Part II · Visual System（視覺系統全譜，約 1500-2500 字）

這是工程化的視覺 spec。完整後任何執行者拿到都能產出一致的視覺。

必含子節：

- **完整色板**：至少 8-10 色，每色含 HEX + 功能定義 + 佔畫面比例上限
- **字體系統**：至少 6 個字級層級，每層級含字型名 + weight + size + letter-spacing + 用途
- **網格系統**：畫布尺寸 + 外邊距 + column grid + baseline grid + 關鍵安全區 + 黃金分割錨點
- **動畫系統**：easing 庫（4 條以內）+ duration 字典 + stagger 法則 + scene 過渡規則
- **Chrome 元素**：貫穿全片的小細節（counter / chip / ticker / watermark / texture），每個含位置 + 入退場時機
- **音訊系統**：BGM 30 秒走向曲線（分層）+ SFX 字典（10+ cues 含時間碼 + 音量 + 頻段隔離）
- **反 AI slop checklist**：per-shot 自檢表（10-15 項）

鐵律：**所有視覺決策都從 Visual System 推導，不要在 shot list 裡臨時發明新值**。

### Part III · Story Arc（故事弧，約 500-800 字）

三幕結構 + 情緒曲線：

- **Act I · SETUP**（0 → 第 1/5 時長，e.g. 0-6s for 30s）：觀眾進入，問題被提出
- **Act II · ESCALATION**（中間 2/3）：答案展開，主題鋪陳
- **Act III · PAYOFF**（最後 1/4）：昇華、slogan reveal、品牌印章

含 ASCII 情緒曲線圖 + emotional climax 時刻標記。

**關鍵決策**：climax 不一定在末尾。30s 片子 climax 通常在 22-25s（不是 29s）——最後幾秒是 resolution / decay，不是 peak。這條規則違反必然讓作品「虎頭蛇尾」。

### Part IV · Shot-by-Shot Storyboard（分鏡腳本，約 5000-7000 字 · 佔 60% 篇幅）

每鏡含 10 個欄位（缺一不可）：

```
SHOT NN · NAME
[TIMECODE]    起止時間 + 時長
[FUNCTION]    這一鏡在故事弧中的功能（一句話）
[VISUAL]      畫面構圖 + 元素位置 + 運動方向
[TYPE]        排版 spec（字型 / 字級 / 字距 / 行高 / 顏色 / 對齊）
[ANIM]        每元素 in/out 時機 + easing + duration + stagger + delay
[AUDIO]       music beat + SFX cue（每鏡對應 BGM 節奏 + 必含 SFX 時間表）
[CHROME]      四角元素狀態（哪些 chrome 在 / 哪些 fade in/out / 哪個 pulse）
[ANTI-SLOP]   這一鏡通過了哪些自檢項 + 有什麼 120% 細節簽名
[WHY]         承接上一鏡的邏輯 + 推進下一鏡的鉤子
```

**欄位平均 30-80 字 → 每鏡 400-700 字 → 12-15 鏡 → 5000-7000 字**。

實戰經驗：寫完 storyboard 後**自己讀一遍**——任意一鏡刪掉，整支片是否還成立？如果可以刪，那鏡就是多餘的，刪掉。

### Part V · Production Manifest（製作清單，約 800-1200 字）

工程交付清單：

- 字型載入 URL（含 preconnect）
- CSS 變數（直接可貼上）
- BGM 來源選擇標準 + Suno/Udio prompt 關鍵詞 + 備選庫
- SFX 字典（按時間碼逐 cue 列出檔案路徑 + 音量）
- **關鍵幀驗證計劃**：12-15 張 pause-and-check 關鍵幀時間碼，每幀驗證項列出（fonts / positions / chrome state）
- 錄製參數（fps / codec / bitrate / preset）
- ffmpeg 音訊混合命令（含 audio stream 驗證）
- 交付物清單（mp4 / mp4-60fps / gif / poster.png / silent.mp4 / shot-list.csv）
- 全鏈路時間估算（小時級精度）

---

## 4. 寫 director's notes 的 5 條建議

**4.1 用導演的口吻，不用 PM 的口吻**

❌「This shot displays the product features.」
✅「This is the hero shot — if the audience pauses anywhere, I want it to be here.」

導演筆記是給執行者讀的，但也是給未來的自己讀的。第一人稱 + judgment 表達比 description 表達留更多決策線索。

**4.2 引用具體作品（含年份），不只是流派名**

❌「Apple-inspired」
✅「Apple 'Designed by Apple in California' (2013, dir. Mark Romanek) — 學的是慢拍 + 襯線 + 大白底」

引用具體作品的好處：(a) 任何觀眾都能上網搜到對照 (b) 你逼自己想清楚學的是什麼具體技術 (c) 防止「靈感模糊」。

**4.3 每個決策都 trace 回 first principle**

整支片有一句 first principle（如 "Markdown is the new typewriter."）。每個具體決策——配色 / 字型 / 節奏 / chrome——都要能 trace 回這句話。

trace 不上的決策就是裝飾，刪掉。

**4.4 寫 anti-slop 比寫 do-this 更重要**

「這部片不做的事」清單（紫漸層 / emoji / Lorem ipsum / Inter display / SVG 畫人物 / 圓角卡 + 左 border accent）比「這部片做的事」清單更能保護品質。

正向決策無窮多，負向 checklist 是有限的——但負向 checklist 一旦違反就是 slop。

**4.5 寫完不要立即實施——隔 30 分鐘再讀一遍**

寫作時大腦在「生產模式」，看不見 inconsistency。隔 30 分鐘讀自己寫的 storyboard，會發現：
- 某兩鏡功能重複（刪一個）
- 某鏡敘事跳躍太大（加過渡）
- emotional climax 位置錯（移動）
- chrome 元素和 shot 數量不匹配（重新對齊）

這 30 分鐘省下的是後期 2 小時的返工。

---

## 5. Director's Notes → HTML 實施流程

寫完 director's notes 後，HTML 實施步驟：

1. **複用 starter components**（`assets/animations.jsx` 的 Stage/Sprite/Easing/interpolate）— 不重新發明
2. **CSS 變數直接從 Visual System Part II 貼上** — 不在 HTML 裡臨時改色
3. **按 Sprite start/end 時間軸對照 Part IV 時間碼** — 不擅自加鏡
4. **chrome 元素抽成獨立元件**（ChromeA/B/C/D），用 useTime() 驅動狀態切換
5. **destination cards 內容必須真實可讀**（不是 fake bar lines）—— 這是 v5 專案裡最被反覆提及的 120% 細節簽名
6. **每寫完一鏡就立即截關鍵幀驗證**（用 `?t=NN` URL 參數 + Playwright），不要寫完全片再統一驗證

---

## 6. 關鍵幀驗證流程

URL 參數實現（必須在 Stage 元件加）：

```js
const urlMatch = window.location.search.match(/[?&]t=([\d.]+)/);
const frozenTime = urlMatch ? parseFloat(urlMatch[1]) : null;
const [time, setTime] = useState(frozenTime != null ? frozenTime : 0);
const [playing, setPlaying] = useState(frozenTime == null);
```

→ 這樣 `file:///path/animation.html?t=14.5` 直接 freeze 在 14.5 秒。

批次截圖：

```bash
for t in 0.5 2.5 4.9 7.0 10.5 13.5 16.5 19.0 21.5 23.4 25.5 28.0 29.9; do
  npx -y playwright screenshot \
    "file://$PWD/animation.html?t=$t" \
    "keyframes/t-$t.png" \
    --viewport-size=1920,1136 \
    --wait-for-timeout=2500
done
```

每張截圖必須驗證：
- [ ] 元素無溢位 1920×1080 canvas
- [ ] 字距、行高 visually correct（不擠、不散）
- [ ] 關鍵 typography 細節（句點顏色 / em-dash / italic / small caps）可識別
- [ ] chrome 元素位置 + 狀態正確
- [ ] 反 AI slop checklist 通過
- [ ] 「pause 時值得看」的 120% 細節存在

---

## 7. 多視角並行策略（advanced）

複雜專案（如 launch film 選不出方向 / 想看多個美學差異 / 客戶沒拍板風格）可以**啟動多個 subagent 並行做不同導演視角的版本**。

實戰配置（2026-05-11 huashu-md-html 專案，並行 6 個版本）：

```
v5  · 基線（Anthropic / Penguin Classics 出版社品味）
v5a · Wes Anderson（對稱 + 復古 + 章節卡片）
v5b · Saul Bass（剪紙 + 60s 大字 + 幾何切割）
v5c · 王家衛（中文襯線 + 慢動作 + 懷舊）
v5d · Massimo Vignelli（現代主義 grid + 紅黑）
v5e · 原研哉 Kenya Hara（極簡日式 + 留白）
v5f · 草間彌生 Yayoi Kusama（圓點 + 重複 + 單一強色）
```

每個 subagent 接到獨立 brief：
- 專案背景（同一份）
- 必讀參考（同一份 v5-director-notes.md 作為方法論模板）
- **指定的藝術家 DNA**（色板 / 字型 / 視覺語言 / 節奏 / 招牌元素 / 反 slop 強化版本，每條 30-50 字）
- 統一任務清單（director-notes.md + animation.html + keyframes/ + README.md）
- 統一約束（30s / 1920×1080 / file:// / Google Fonts）

並行啟動 + 背景執行，約 30-60 分鐘出 6 套完整版本。

完成後審校對比：
1. 各版本核心美學決策表
2. 關鍵幀並排對比（每版同時刻一幀）
3. 投票：哪個最貼近使用者的真實需求

**關鍵**：不要讓 subagent 之間相互參考——它們必須獨立產出，否則就會撞到「平均值」。每個 subagent 的指令裡要明說「不要重複 v5 的美學」。

---

## 8. 觸發的幾種典型場景

| 使用者場景 | 是否觸發 | 備註 |
|---------|---------|------|
| 「做個 SaaS 升級宣傳片」 | ✅ 觸發 | 預設走完整流程 |
| 「Apple 級別 / 超級碗品質感的影片」 | ✅ 觸發 + 升級 | 強力推薦多視角並行 |
| 「30 秒品牌 launch film」 | ✅ 觸發 | |
| 「這個專案 1 萬字腳本再做動畫」 | ✅ 觸發 | 使用者明確指明 |
| 「簡單 motion graphic，logo 轉一下」 | ❌ 不觸發 | 用 animations.md 標準流程 |
| 「做個 onboarding 動畫 demo」 | ❌ 不觸發 | 用 animations.md |
| 「教程影片帶配音」 | ❌ 不觸發 | 走 voiceover-pipeline.md |
| 「單個 hero animation」 | ⚠️ 看複雜度 | 如果是高規格 hero，觸發；普通 hero 用 hero-animation-case-study.md |

---

## 9. 參考樣本

完整 director's notes 參考樣本（self-contained，本 skill 內）：

`assets/director-notes-samples/launch-film-30s-sample.md`（約 78KB · 11500 字 · 13 鏡 · 5 大部分齊全）

原始專案位置（含對應實施 HTML + 關鍵幀）：

- v5-director-notes.md（director's notes，作者本地，未隨倉庫分發）
- v5-six-forms.html（HTML 實施，作者本地，未隨倉庫分發）
- v5-keyframes/（關鍵幀驗證截圖，作者本地，未隨倉庫分發）

寫新專案時強烈建議**先 Read 這份樣本**，理解工作量和細節密度，再決定要不要全套走流程。

---

## 10. 反模式（不要這樣做）

❌ **寫 1000 字的精簡版 director's notes 就動手**
→ 精簡版必然漏 Visual System 的某個子項，導致 HTML 實施時不停回頭補 spec。要做就做萬字級，要省就直接跳過。

❌ **storyboard 只寫 5-8 鏡**
→ 30 秒片至少 12-15 鏡（每鏡 2-3 秒）。鏡少 = 節奏勻速 = 沒 climax。

❌ **director's notes 寫完就交付，不做實施**
→ 文件不是交付物，動畫才是。文件 + 動畫一起交付，文件作為「設計依據」附錄。

❌ **多視角並行時讓 subagent 看其他版本**
→ 各 subagent 必須獨立，否則趨同。審校階段才對比。

❌ **跳過關鍵幀驗證直接錄 MP4**
→ 必然返工。關鍵幀驗證是最便宜的 quality gate。

❌ **把動畫細節決策推遲到「等我錄的時候再想」**
→ 錄製階段是機械執行，不能做創意決策。所有決策必須在 director's notes 寫死。

---

*最後修訂：2026-05-11*
*真實案例：huashu-md-html v2.0 launch film（v5-director-notes.md）*
