# 場景模板庫：按輸出類型組織

> 與 design-styles.md 的「提示詞DNA」組合使用。
> 公式：`[風格提示詞DNA] + [場景模板] + [具體內容描述]`

---

## 1. 公眾號封面 / 文章題圖

**規格**：
- 封面圖：2.35:1（900×383px 或 1200×510px）
- 正文插圖：16:9（1200×675px）或 4:3（1200×900px）

**關鍵設計要素**：
- 視覺衝擊力優先（使用者在資訊流中快速掃過）
- 文字極少或無文字（公眾號標題會覆蓋在上面）
- 色彩飽和度適中（微信閱讀環境偏白）
- 避免過度細節（縮圖也要可辨識）

**推薦風格**：01 Pentagram / 11 Build / 12 Sagmeister / 18 Kenya Hara / 07 Field.io

**場景提示詞模板**：
```
[風格DNA插入此處]
- Article cover image for WeChat subscription
- Landscape format, 2.35:1 aspect ratio
- Bold visual impact, minimal or no text
- Moderate color saturation for white reading environment
- Must remain recognizable as thumbnail
- Clean composition with clear focal point
```

---

## 2. 正文配圖 / 概念插畫

**規格**：
- 16:9（1200×675px）最通用
- 1:1（800×800px）適合強調
- 4:3（1200×900px）適合資訊密集

**關鍵設計要素**：
- 服務於文章論點，不是裝飾
- 與上下文形成視覺節奏
- 簡潔表達一個核心概念
- AI生成優先，HTML截圖僅在精確資料表格時用

**推薦風格**：根據文章調性選擇，常用 01/04/10/17/18

**場景提示詞模板**：
```
[風格DNA插入此處]
- Article illustration, concept visualization
- [16:9 / 1:1 / 4:3] aspect ratio
- Single clear concept: [描述核心概念]
- Serve the argument, not decoration
- [Light/Dark] background to match article tone
```

---

## 3. 資訊圖 / 資料視覺化

**規格**：
- 豎版長圖：1080×1920px（手機閱讀）
- 橫版：1920×1080px（文章內嵌）
- 方形：1080×1080px（社交媒體）

**關鍵設計要素**：
- 資訊層級清晰（標題 → 核心資料 → 細節）
- 資料準確，不編造
- 視覺引導線（使用者閱讀路徑）
- 適當使用圖示/圖表輔助理解

**推薦風格**：04 Fathom / 10 Müller-Brockmann / 02 Stamen / 17 Takram

**場景提示詞模板**：
```
[風格DNA插入此處]
- Infographic / data visualization
- [Vertical 1080x1920 / Horizontal 1920x1080 / Square 1080x1080]
- Clear information hierarchy: title → key data → details
- Visual flow guiding reader's eye path
- Icons and charts for comprehension
- Data-accurate, no decorative distortion
```

---

## 4. PPT / Keynote 演示

**規格**：
- 標準：16:9（1920×1080px）
- 寬屏：16:10（1920×1200px）

**關鍵設計要素**：
- 每頁一個核心資訊（不堆砌）
- 字號層級明確（標題40pt+ / 正文24pt+ / 註釋16pt+）
- 大量留白，投影時更清晰
- 圖文比例至少 60:40
- 一致的視覺系統（顏色、字型、間距）

**推薦風格**：01 Pentagram / 10 Müller-Brockmann / 11 Build / 18 Kenya Hara / 04 Fathom

**場景提示詞模板**：
```
[風格DNA插入此處]
- Presentation slide design, 16:9
- One core message per slide
- Clear type hierarchy (title 40pt+, body 24pt+)
- Generous whitespace for projection clarity
- Consistent visual system throughout
- [Light/Dark] theme
```

---

## 5. PDF 白皮書 / 技術報告

**規格**：
- A4 縱向（210×297mm / 595×842pt）
- Letter 縱向（216×279mm / 612×792pt）

**關鍵設計要素**：
- 長文閱讀最佳化（行寬66字元、行高1.5-1.8）
- 清晰的章節導航系統
- 頁首/頁尾/頁碼的統一設計
- 圖表與正文的優雅共存
- 引用/註釋系統
- 封面頁設計精緻

**推薦風格**：10 Müller-Brockmann / 04 Fathom / 03 Information Architects / 17 Takram / 19 Irma Boom

**場景提示詞模板**：
```
[風格DNA插入此處]
- PDF document / white paper design
- A4 portrait format (210×297mm)
- Long-form reading optimized (66 char line width, 1.5 line height)
- Clear chapter navigation system
- Elegant header/footer/page number design
- Charts integrated with body text
- Professional cover page
```

---

## 6. 落地頁 / 產品官網

**規格**：
- Desktop: 1440px 寬度設計（響應至320px）
- 首屏高度：100vh

**關鍵設計要素**：
- 首屏5秒內傳達核心價值
- 清晰的CTA（行動按鈕）
- 滾動敘事結構（問題→方案→證明→行動）
- 移動端適配
- 載入速度

**推薦風格**：05 Locomotive / 01 Pentagram / 11 Build / 08 Resn / 06 Active Theory

**場景提示詞模板**：
```
[風格DNA插入此處]
- Landing page / product website
- Desktop 1440px width, responsive
- Hero section 100vh, core value in 5 seconds
- Clear CTA button design
- Scroll narrative: problem → solution → proof → action
- Modern web aesthetic
```

---

## 7. App UI / 原型介面

**規格**：
- iOS: 390×844pt（iPhone 15）
- Android: 360×800dp
- 平板: 1024×1366pt（iPad Pro）

**關鍵設計要素**：
- 觸控友好（最小點選區44×44pt）
- 系統設計語言一致性
- 狀態列/導航欄/Tab欄的標準處理
- 資訊密度適中（移動端不宜過密）

**推薦風格**：17 Takram / 11 Build / 03 Information Architects / 01 Pentagram

**場景提示詞模板**：
```
[風格DNA插入此處]
- Mobile app UI design
- iOS [390×844pt] / Android [360×800dp]
- Touch-friendly (44pt minimum tap targets)
- Consistent design system
- Standard status bar / navigation / tab bar
- Moderate information density
```

---

## 8. 小紅書配圖

**規格**：
- 豎版：3:4（1080×1440px）最佳
- 方形：1:1（1080×1080px）
- 首圖決定點選率

**關鍵設計要素**：
- 視覺吸引力第一（在瀑布流中競爭）
- 可以有少量文字（但不超過畫面20%）
- 色彩鮮明但不俗
- 生活感/質感/氛圍感

**推薦風格**：12 Sagmeister / 11 Build / 20 Neo Shen / 09 Experimental Jetset

**場景提示詞模板**：
```
[風格DNA插入此處]
- Social media image for Xiaohongshu (RED)
- Vertical 3:4 (1080×1440px)
- Eye-catching in waterfall feed
- Minimal text overlay (under 20% of area)
- Vivid but tasteful colors
- Lifestyle/texture/atmosphere feel
```

---

## 組合示例

**場景**：公眾號封面，介紹一款AI程式設計工具，想要專業但有溫度

**Step 1**：選風格 → 17 Takram（專業+溫度）
**Step 2**：取Takram提示詞DNA + 公眾號封面模板

```
Takram Japanese speculative design:
- Elegant concept prototypes and diagrams
- Soft tech aesthetic (rounded corners, gentle shadows)
- Charts and diagrams as art pieces
- Modest sophistication
- Neutral natural colors (beige, soft gray, muted green)
- Design as philosophical inquiry

Article cover image for WeChat subscription
- Landscape format, 2.35:1 aspect ratio (1200×510px)
- Bold visual impact, minimal text
- Moderate color saturation for white reading environment
- Must remain recognizable as thumbnail
- Clean composition with clear focal point

Content: An AI coding assistant tool, showing the concept of human-AI collaboration
in software development, warm and professional atmosphere
```

---

**版本**：v1.0
**更新日期**：2026-02-13
