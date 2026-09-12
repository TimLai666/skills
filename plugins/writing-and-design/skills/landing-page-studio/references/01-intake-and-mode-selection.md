# Intake and Mode Selection

## 欄位與預設

由對話、現有頁面及專案整理輸入，不要求使用者記住欄位名稱。

| 欄位 | 內容與預設 |
| --- | --- |
| brand_theme | 品牌與頁面主題，非空字串 |
| value_props | 非空字串陣列，預設整理三個真實價值主張 |
| primary_cta | 主要行動文案，交付前還需確認實際目的地或互動 |
| style_direction | 沿用已確認方向；未定時走 design-studio 風格選型 |
| output_mode | single-file-html / react-project，沿用專案或依交付需求選擇 |
| variant_mode | single（預設）/ batch |
| autonomy_mode | multi-iteration（預設）/ single-pass |
| animation_level | high（預設）/ medium / low |
| motion_preference | respect-reduced-motion |
| target_audience / industry | 受眾與產業背景，依需要補足 |
| react_stack | 沿用現有技術，無既有組合才選擇 |

## 資料不足

新頁面需要品牌／主題、真實價值主張及主要行動；先使用已提供資料，僅詢問影響方向的缺項。預設三個價值主張，不因實際只有兩個或使用者要求更多而拒絕。缺風格先選型，缺技術選項可依現況判斷，不能要求使用者從頭填表。

局部修改沿用上下文，只確認受影響範圍。缺證據不得捏造見證、客戶或成果；明列待補內容與交付限制。

驗證腳本供新頁面輸入使用：缺必要資料回 `MissingDataOutput`，包含缺項、原因與問題；型態或選項無效時回錯誤，不默默覆蓋使用者設定。

## 模式與技術選擇

- `single-file-html`：靜態頁面、單一檔案交付，可依需求使用 CDN；單檔不自動代表離線可用。
- `react-project`：既有 React 頁面或需要元件與應用整合；沿用專案組合。
- 無既有組合時，普通獨立頁可用 `vite-react-tailwind-framer`；需要 Next.js 應用整合時用 `nextjs-app-router`；採 CSS Modules 的專案沿用 `react-css-modules`。不固定要求先比較三種再等選擇。
- 已有其他技術組合時保留，不為符合 starter 遷移專案。

`single` 交付一版，`multi-iteration` 在該版上修正實際問題；`batch` 才交付多版及差異摘要。風格提案依 design-studio 的既有流程。

驗證器可接收 `existing_project`，內含已確認的 `output_mode` 與 `react_stack`，供沿用專案組合；現有組合名稱不受 starter 選項限制。`vite-react-tailwind-framer` 保留為既有輸入識別，實際動畫依賴依專案與效果選擇。
