---
name: landing-page-studio
description: >-
  This skill MUST be used when creating or improving conversion-oriented
  landing pages, LPs, hero sections, animated marketing pages, or 活動頁、
  產品落地頁、轉換頁面. It SHOULD also be used when a page needs clearer
  value propositions and a primary action without naming a landing page.
  Visual direction follows design-studio; this skill handles conversion
  structure, animation, implementation, and delivery.
metadata:
  version: "2.1.1"
---

# Landing Page Studio

## Overview

產出可使用的 Landing Page，兼顧轉換訊息、視覺辨識度、動畫與效能。支援單檔 HTML、React 專案及既有頁面修改；視覺方法沿用 design-studio。

## Input Contract

先從對話、原稿與專案確認品牌／主題、價值主張、主要行動及目的地。預設三個價值主張、至少兩類真實信任證據；可用內容不足時補查或詢問，不能為湊數捏造。

既有專案沿用技術、樣式與輸出方式。新頁面未指定輸出時，依使用需求選擇，單純靜態交付可用單檔 HTML；只有會改變需求或相容性的未決事項才詢問。輸入欄位、模式與預設見 [01 輸入與模式](references/01-intake-and-mode-selection.md)，整理輸入或使用驗證腳本時讀。

## Workflow

### 1. 接續設計方向

讀 design-studio 的 `shared/anti-slop.md`、`shared/hard-rules.md`、`shared/guardrails.md`，遵守其適用規則。沿用既有 `DESIGN.md` 與設計資訊；新設計依 design-studio 的公約建立並維護，局部修改依其流程判斷需要更新的範圍。

沿用品牌與已確認的方向。方向未定時，依 design-studio 的 `practical/references/design-styles.md` 提出三個方向，完成既有風格選型與確認流程；選中風格後讀對應深度風格包與色彩推導協議。本 skill 不另維護風格庫。

### 2. 安排內容與行動

寫頁面內容時讀 [06 文案與轉換結構](references/06-copy-and-conversion-structure.md)。保留預設三個價值主張與至少兩類信任證據，依真實資料、使用者指定與頁面範圍調整。局部修改只處理受影響區塊，不要求重建整頁。

真實品牌素材依 design-studio 的 `shared/brand-asset.md` 取得；其餘圖片沿用 Unsplash／Pexels 的來源規則。核對來源並保留所需 attribution，成品不能殘留模板佔位、無依據數字、技能名稱或內部設定。圖像後方的文字須可讀，需要時加遮罩。

### 3. 實作與動畫

新建時選對應 starter，既有專案直接在原結構修改，不重新搭骨架。React 未指定組合時沿用專案；無既有組合才依需求選用，普通獨立頁可採 Vite React。

動畫預設 `high`，至少涵蓋 Hero、區塊進場、互動與背景四類。設計或實作動畫前讀 [03 動畫與失效處理](references/03-animation-system-and-fallbacks.md)，保留 SVG、GSAP、Anime.js 與可選 WebGL 的方法。依實際效果選工具，不為了四類效果載入四套函式庫。

保留高動畫預設，尊重使用者的 reduced motion 偏好。WebGL、動畫依賴或 CDN 失效時明確報錯，說明受影響效果並修復原因，不自動改用低階效果或當作完成。內容與 CTA 保持可用；改變已約定效果須先取得同意。

### 4. 檢查並修正

預設在同一個實作上自主檢查並修正，依轉換清晰度、視覺一致性、可讀性與效能的實際問題迭代，不另強制生成多份完整候選稿。`variant_mode=batch` 或使用者要求比較時才交付多版；這不改變 design-studio 的風格提案流程。

交付前讀 [05 品質驗收](references/05-quality-gates.md)，實測畫面、主要行動、動畫偏好、失效處理與效能。`single-pass` 只省去探索性迭代，仍須修正驗收發現的問題。未達門檻時處理原因，不能只把自評分數調高。

## Output Contract

交付頁面／專案、素材來源、實際動畫清單與驗證結果。單檔模式交付 `index.html`；React 模式交付可啟動的專案或既有專案修改。只回報實際產生與測得的內容，未驗證項目明列限制。需要結構化輸出、批次比較或清單欄位時讀 [04 交付契約](references/04-output-contracts.md)。

## Scripts and Templates

- [validate_intake.py](scripts/validate_intake.py)：整理新頁面輸入，檢查型態與有效選項；局部修改不必填完整新頁面契約。
- [build_animation_manifest.py](scripts/build_animation_manifest.py)：產生 starter 動畫計畫，成品須依實際元件、觸發方式與失效處理核對，不能當成已驗證的清單。
- [single-file-starter.html](assets/templates/single-file-starter.html)：單檔骨架，替換內容、素材與真實 CTA 目的地後使用。
- [react-vite-starter](assets/templates/react-vite-starter/)：新 Vite React 專案骨架；其他技術組合依專案實作。
