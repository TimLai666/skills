# 多視角並行實驗 · Case Study

> huashu-md-html v2.0 launch film 專案 · 2026-05-11
> 6 位藝術家視角的並行 director's notes + HTML + 關鍵幀實驗

---

## 背景

使用者要求「為 huashu-md-html v2.0 製作 30 秒升級宣傳片」時，主執行緒先產出了 v5 基線（Anthropic / Penguin Classics 出版社品位）。但使用者認為可以做得更好，給了 critical instruction：

> 「呼叫不同的 subagent 分別再去生成 6 個全然不同的表達方式和視覺設計的版本。你可以試試啟用不同的導演和藝術家。然後全都完成後，再評判審校。」

這是首次系統化的「多視角並行 director's notes」實驗，驗證了一套可複用的工作流。

---

## 6 個視角的選擇邏輯

不要隨便選 6 個 designer——他們必須**視覺差異度極高**，避免趨同。

最終選擇的 6 個視角（含選擇理由）：

| 視角 | 流派 | 美學錨點 | 跟其他視角的差異 |
|------|------|---------|----------------|
| **v5 基線** | 現代出版社 | Anthropic 赤陶橙 + Penguin Classics 襯線 + Vignelli grid | 安全的「品位」選擇 |
| **v5a Wes Anderson** | 電影章節美學 | The French Dispatch 雜誌感 + 1960 Olivetti 工業目錄 | 對稱構圖 + 章節卡片 + 裝飾邊框 |
| **v5b Saul Bass** | 60s 影片標題藝術 | cut-paper + Trajan caps + 流動幾何 | 剪紙 silhouette + 大字 + 強對角線 |
| **v5c 王家衛** | 港式新浪潮 | 《花樣年華》《2046》 letterboxing + 中文襯線 | 慢拍 + 霧化光暈 + 中文為主 |
| **v5d Massimo Vignelli** | 1970 現代主義 | Knoll identity manual + NYC Subway map | 嚴格 grid + 3 色鐵律 + 拒絕裝飾 |
| **v5e Kenya Hara** | 極簡日式 | MUJI 海報 + 《白》 | 留白哲學 + 無 chrome + ma 間 |
| **v5f Yayoi Kusama** | 裝置藝術 | Infinity Mirror Rooms + Polka Dot Obsession | obsessive 重複 + 單一強色 + 圓點 |

**選擇原則**：
1. **3 個不同地理文化**（西方電影 / 日本設計 / 港式中文）
2. **3 個不同年代**（1960s / 1970s / 2010s+）
3. **3 個不同載體**（電影 / 平面設計 / 裝置藝術）
4. **每個都有「跟訓練語料裡通用 SaaS 美學完全相反」的視覺簽名**

---

## 實施流程

### Step 1 · 為每個視角寫獨立 brief（約 15 分鐘）

每個 brief 包含 8 個固定欄位：

```
1. 專案背景（同一份）
2. 必讀參考（同一份 v5-director-notes.md 作方法論模板）
3. 你要做的事（4 項交付清單）
4. 該藝術家 DNA（核心欄位 6 項）：
   - 色板（具體 HEX）
   - 字型（具體名字 + 替代方案）
   - 視覺語言（核心幾條）
   - 招牌元素（identifiable signatures）
   - 節奏（區別其他視角）
   - 反 AI slop 強化版（在該風格語境下的禁區）
5. 30 秒結構參考（4-6 個 shot 草擬）
6. destination cards 設計要求（保持真實可讀）
7. 關鍵約束（30s / 1920×1080 / file:// / Google Fonts CDN）
8. 輸出驗證清單 + 完成報告格式
```

**關鍵**：每個 brief 必須強調「**不要重複 v5 的美學**」——否則 subagent 會被 v5 director-notes 影響而趨同。

### Step 2 · 並行啟動 6 個 subagent（同一 message 中 6 個 Agent tool calls）

```js
Agent({ subagent_type: "general-purpose", run_in_background: true, name: "v5a-anderson", ... })
Agent({ subagent_type: "general-purpose", run_in_background: true, name: "v5b-bass", ... })
// ... 6 個
```

後台執行，預期 30-60 分鐘。

### Step 3 · 等待期間的 idle work

不要 polling agent 狀態。subagent 完成會自動 task-notification。等待期間做：

- 修主執行緒的 v5 基線 bug
- 寫 review framework（每個版本要打的分維度 / Q&A）
- 沉澱方法論到 skill（這正是這份 case study 的來源）
- 準備 final summary 文件骨架

### Step 4 · 失敗處理（約 16% 失敗率，可接受）

實戰觀測：6 個 subagent 中約 1 個會因網路或 token 超限失敗（Bass 首輪 socket error）。處理：

1. 收到 completion notification 時**立即檢查**該 agent 的輸出資料夾
2. 缺少關鍵交付物 → 重啟該 agent（同樣 brief，可標註「上次失敗，請重新執行」）
3. 部分完成（如有 html 沒截圖）→ 主執行緒補 Playwright 截圖，不重啟 agent

### Step 5 · 6 版本完成後系統審校

審校 framework（5 維度 + 3 頂層問 + use case 分配）：

```
5 維度評分（每維 1-10）：
- Distinctiveness 視覺差異化
- Coherence 美學一致性
- Anti-slop 反 AI slop 執行
- Story arc 節奏與故事弧
- Pause-and-look 細節密度

3 頂層問：
- Q1 截圖分享？（能在社交平台觸發暫停）
- Q2 記一句話？（能留下命題級記憶）
- Q3 跨時代？（5 年後回看不顯廉價）

use case 分配（按平台和受眾）：
- 公眾號 / X / B 站 / 朋友圈 / Dribbble / 客戶演示 / 私域 / ...
```

詳見 `assets/director-notes-samples/launch-film-30s-sample.md` 的同目錄 REVIEW.md。

---

## 實驗產出（事實）

### 文件量

- v5 基線 director-notes：11500 字
- 6 視角 director-notes 各 4000-12000 字
- 總文件量：約 55000-70000 字
- 5 大部分結構齊全：6/6 版本

### HTML 實施

- 每版獨立 animation.html，30 秒，1920×1080
- 檔案大小 28-74KB
- 全部 file:// 可開啟（不依賴 server）

### 關鍵幀

- 每版 10-18 張 PNG，覆蓋完整 30 秒故事弧
- 總截圖量：80+ 張
- 平均每張 PNG 大小：100-200KB

### 時長

- 6 個 subagent 並行執行：約 12-15 分鐘（duration_ms 顯示）
- 主執行緒並行 idle work（修 v5 + 寫方法論）：同期完成
- 整體「從啟動 6 視角到所有 deliverable 到位」：約 60 分鐘

---

## 關鍵洞察（寫給 huashu-design 的未來使用者）

### 洞察 1 · 「先寫萬字 director's notes」方法論**完全 reproducible**

6 個 subagent 都按 5 大部分結構產出了 4000-12000 字的完整 spec，且實施 HTML 時都達到了 marketing-ready 質量。這證明方法論本身不依賴單一執行者的天賦——**只要 brief 給得清楚，多個獨立執行者能產出一致的高質量結果**。

### 洞察 2 · 「視角」必須具體到「作品 + 年份」

每個 brief 裡都列出具體作品對話：
- Anderson → *The French Dispatch* (2021) + *Moonrise Kingdom* (2012) + Penguin Classics dust jackets + 1960s Olivetti catalogues
- WKW → *In the Mood for Love* (2000) + *2046* (2004)
- Vignelli → 1972 NYC Subway map + Knoll identity manual + *The Vignelli Canon*
- Hara → MUJI brand 1995-2023 + 《白》 + Junya Ishigami transparency
- Kusama → Infinity Mirrored Rooms (2013-2023) + Polka Dot Obsession 裝置

**實戰結果**：所有 subagent 都準確捕捉到了該作品的核心 visual DNA，而不是流派的「平均值」。

### 洞察 3 · 反 AI slop 的「風格強化版本」是關鍵

通用 anti-slop（紫漸變 / emoji / SVG 人物）適用所有版本。但**每個風格還要寫「專屬 anti-slop」**：

- Bass: 不用 Helvetica（太乾淨，Bass 是粗獷）
- Vignelli: 不用圓角（所有 corner 90°）
- Hara: 不用任何漸變 + 不用 sans display
- Kusama: 不用現代 SaaS look
- Anderson: 不用 cyber 配色
- WKW: 不用 Inter（WKW 用襯線）

加了這些後，6 個版本風格純度極高，無一相互趨同。

### 洞察 4 · 多視角的真正價值不是「選 winner」

最初設想是 A/B test 選最好的版本。實際審校時發現：**6 個版本各自有清晰 use case**：
- v5 基線 → 產品頁 / 微信讀書（資訊密度高）
- Anderson → 公眾號長文頭圖（翻雜誌感強）
- WKW → B 站 / 中文文化向（懷舊溫度）
- Vignelli → 設計圈 / Dribbble（每幀都是印刷海報）
- Hara → 客戶演示 / 靜態截圖（極簡哲學）
- Kusama → X 短影片 / 病毒傳播（視覺衝擊）

**結論**：marketing 不是 single-shot，是 platform-specific multiplex。6 視角並行的真正價值是**讓一個專案有 6 個差異化武器**，不是讓 5 個版本上不了檯面。

### 洞察 5 · subagent 的失敗率 ~16% 是可接受的

6 個裡 1 個失敗（Bass 首輪 socket error）。處理代價：重啟 + 5 分鐘簡化版 brief，再等 12-15 分鐘。**對比 vs. 等 1 個 agent 順序跑 6 個版本（90+ 分鐘）**——並行 + 重試明顯更經濟。

### 洞察 6 · 主執行緒在等待期間必須做 substantive idle work

subagent 完成需要 12-15 分鐘。這段時間主執行緒絕不該空閒：

- **修主版本 bug**（使用者已經反饋的）
- **寫 review framework**（等審校時填）
- **沉澱方法論到 skill**（如這份 case study）
- **準備 final summary**（使用者回來一目瞭然）

這是 parallel multi-agent workflow 的「主執行緒職責」——不是 PM 等結果，是 orchestrator 同步推進。

---

## 何時啟用「多視角並行」

| 場景 | 是否啟用 | 原因 |
|------|---------|------|
| 使用者明確說「想看不同方向」「再多做幾個版本」 | ✅ 立刻啟用 | 直接需求 |
| 第一版做出來使用者不滿意但說不清要啥 | ✅ 啟用 | A/B 選優於「我猜你要啥」 |
| 專案準備多平台分發（X / 公眾號 / B 站 / 朋友圈） | ✅ 啟用 | 每平台一個版本 |
| 客戶沒拍板風格但有預算（time + token） | ✅ 啟用 | 反覆改 = 5 倍代價 |
| 使用者已經給了明確風格參考且只要 1 個版本 | ❌ 不啟用 | 浪費 |
| 任務是簡單 motion graphic / icon 動畫 | ❌ 不啟用 | 過度工程化 |
| 時間緊 < 30 分鐘 | ❌ 不啟用 | subagent 跑不完 |

---

## 完整方法論流程圖

```
使用者 brief（含質量預期）
       ↓
[主執行緒] 寫 v5 基線 director's notes（萬字級 5 大部分）
       ↓
[主執行緒] 實施 v5 HTML + 截關鍵幀（marketing baseline）
       ↓
[決策點] 是否啟用多視角？
       ↓ YES
[主執行緒] 選 6 個差異化視角 + 寫 6 份獨立 brief（每份 8 欄位）
       ↓
[6 subagents 並行]
   ├── v5a brief → director-notes + html + keyframes + README
   ├── v5b brief → ...
   ├── v5c brief → ...
   ├── v5d brief → ...
   ├── v5e brief → ...
   └── v5f brief → ...
       ↓
[主執行緒同步做] 修 v5 bug · 寫 review framework · 沉澱方法論
       ↓
[全 6 通知到達]
       ↓
[主執行緒] 失敗檢測 + 重試 / 補截圖
       ↓
[主執行緒] 5 維度評分 + 3 頂層問 + use case 分配
       ↓
[主執行緒] 寫 final REVIEW.md
       ↓
[交付] 6 完整版本 + review + 平台分發推薦
```

---

## 相關文件

- 完整方法論：`references/launch-film-director-notes.md`
- 單視角樣本：`assets/director-notes-samples/launch-film-30s-sample.md`（v5 基線）
- 實戰專案位置：作者本地 demos 目錄（含 6 + 1 視角全套檔案，未隨倉庫分發）
- 審校 review：作者本地 REVIEW.md（未隨倉庫分發）

---

*Last updated: 2026-05-11*
*Real case study: huashu-md-html v2.0 launch film 6-perspective parallel experiment*
