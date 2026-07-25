# Design Philosophy Showcases — 樣例資產索引

> 8 種場景 × 3 種風格 = 24 個預製設計樣例
> 用於 Phase 3 推薦設計方向時，直接展示「這個風格做出來長什麼樣」

## 風格說明

| 代號 | 流派 | 風格名稱 | 視覺氣質 |
|------|------|---------|---------|
| **Pentagram** | 資訊建築派 | Pentagram / Michael Bierut | 黑白克制、瑞士網格、強字型層級、#E63946紅色強調 |
| **Build** | 極簡主義派 | Build Studio | 奢侈品級留白(70%+)、微妙字重(200-600)、#D4A574暖金、精緻 |
| **Takram** | 東方哲學派 | Takram | 柔和科技感、自然色(米色/灰/綠)、圓角、圖表如藝術 |

## 場景速查表

### 內容設計場景

| # | 場景 | 規格 | Pentagram | Build | Takram |
|---|------|------|-----------|-------|--------|
| 1 | 公眾號封面 | 1200×510 | `cover/cover-pentagram` | `cover/cover-build` | `cover/cover-takram` |
| 2 | PPT資料頁 | 1920×1080 | `ppt/ppt-pentagram` | `ppt/ppt-build` | `ppt/ppt-takram` |
| 3 | 直式資訊圖 | 1080×1920 | `infographic/infographic-pentagram` | `infographic/infographic-build` | `infographic/infographic-takram` |

### 網站設計場景

| # | 場景 | 規格 | Pentagram | Build | Takram |
|---|------|------|-----------|-------|--------|
| 4 | 個人主頁 | 1440×900 | `website-homepage/homepage-pentagram` | `website-homepage/homepage-build` | `website-homepage/homepage-takram` |
| 5 | AI導航站 | 1440×900 | `website-ai-nav/ainav-pentagram` | `website-ai-nav/ainav-build` | `website-ai-nav/ainav-takram` |
| 6 | AI寫作工具 | 1440×900 | `website-ai-writing/aiwriting-pentagram` | `website-ai-writing/aiwriting-build` | `website-ai-writing/aiwriting-takram` |
| 7 | SaaS landing page | 1440×900 | `website-saas/saas-pentagram` | `website-saas/saas-build` | `website-saas/saas-takram` |
| 8 | 開發者文件 | 1440×900 | `website-devdocs/devdocs-pentagram` | `website-devdocs/devdocs-build` | `website-devdocs/devdocs-takram` |

> 每個條目同時有 `.html`（原始碼）和 `.png`（截圖）兩個檔案

## 使用說明

### Phase 3 推薦時引用
推薦設計方向後，可展示對應場景的預製截圖：
```
「這是 Pentagram 風格做公眾號封面的效果 → [展示 cover/cover-pentagram.png]」
「Takram 風格做 PPT 資料頁是這種感覺 → [展示 ppt/ppt-takram.png]」
```

### 場景匹配優先順序
1. 使用者需求的場景有精確匹配 → 直接展示對應場景
2. 無精確匹配但類型相近 → 展示最近似的場景（如「產品官網」→ 展示 SaaS landing page）
3. 完全不匹配 → 跳過預製樣例，直接進 Phase 3.5 現場生成

### 橫向對比展示
同一場景的 3 個風格適合並排展示，幫助使用者直觀比較：
- 「這是同一個公眾號封面，分別用 3 種風格實現的效果」
- 展示順序：Pentagram（理性克制）→ Build（奢華極簡）→ Takram（柔和溫暖）

## 內容詳情

### 公眾號封面（cover/）
- 內容：Claude Code Agent 工作流 — 8 個並行 Agent 架構
- Pentagram：巨大紅色「8」+ 瑞士網格線 + 資料條
- Build：超細字重「Agent」懸浮於 70% 留白中 + 暖金細線
- Takram：8 節點放射狀流程圖作為藝術品 + 米色底

### PPT資料頁（ppt/）
- 內容：GLM-4.7 開源模型 Coding 能力突破（AIME 95.7 / SWE-bench 73.8% / τ²-Bench 87.4）
- Pentagram：260px「95.7」錨點 + 紅/灰/淺灰對比條形圖
- Build：三組 120px 超細數字懸浮 + 暖金漸層對比條
- Takram：SVG 雷達圖 + 三色疊加 + 圓角資料卡片

### 直式資訊圖（infographic/）
- 內容：AI 記憶系統 CLAUDE.md 從 93KB 最佳化到 22KB
- Pentagram：巨大「93→22」數字 + 編號區塊 + CSS 資料條
- Build：極致留白 + 柔影卡片 + 暖金連線線
- Takram：SVG 環形圖 + 有機曲線流程圖 + 毛玻璃卡片

### 個人主頁（website-homepage/）
- 內容：獨立開發者 Alex Chen 的作品集首頁
- Pentagram：112px 大名 + 瑞士網格分欄 + 編輯數字
- Build：玻璃態導航 + 懸浮統計卡片 + 超細字重
- Takram：紙質紋理 + 小圓形頭像 + 髮絲細分隔線 + 不對稱佈局

### AI導航站（website-ai-nav/）
- 內容：AI Compass — 500+ AI 工具目錄
- Pentagram：方角搜尋框 + 編號工具列表 + 大寫分類標籤
- Build：圓角搜尋框 + 精緻白色工具卡片 + 藥丸標籤
- Takram：有機錯位卡片佈局 + 柔和分類標籤 + 圖表式連線

### AI寫作工具（website-ai-writing/）
- 內容：Inkwell — AI 寫作助手
- Pentagram：86px 大標題 + 線框編輯器模型 + 網格特性列
- Build：漂浮編輯器卡片 + 暖金 CTA + 奢華寫作體驗
- Takram：詩意襯線標題 + 有機編輯器 + 流程圖

### SaaS landing page（website-saas/）
- 內容：Meridian — 商業智慧分析平台
- Pentagram：黑白分欄 + 結構化儀表板 + 140px「3x」錨點
- Build：懸浮儀表板卡片 + SVG 面積圖 + 暖金漸層
- Takram：圓角柱狀圖 + 流程節點 + 柔和地球色

### 開發者文件（website-devdocs/）
- 內容：Nexus API — 統一 AI 模型閘道器
- Pentagram：左側導覽列 + 方角程式碼塊 + 紅色字串高亮
- Build：居中漂浮程式碼卡片 + 柔影 + 暖金圖示
- Takram：米色程式碼塊 + 流程圖連線 + 虛線特性卡片

## 檔案統計

- HTML 原始檔：24 個
- PNG 截圖：24 個
- 總資產：48 個檔案

---

**版本**：v1.0
**建立日期**：2026-02-13
**適用於**：huashu-design GUIDE Phase 3 推薦環節
