# 和 Claude 內建的 Design 一起用

Claude 內建的 Design 是一種設計畫布，可以在畫布上排好幾張網頁、App 畫面或海報。相關的類型還有 Design System（設計系統）和 Slides（簡報）。在 claude.ai 網頁版和 Claude 桌面版 App 的 Claude Code 裡，都是透過 Artifact 工具建立。

這些類型自帶一份格式說明，建立或讀取時會一併取得。design-studio 負責方向與設計規則，Design 類型負責檔案格式與交付。兩邊都要照做。

## 分工

| 項目 | 誰說了算 |
|---|---|
| 方向、配色推導、段落節奏、景深層、形狀語言、反 AI 範本規則 | design-studio |
| 檔案格式、能用哪些外部資源、怎麼交付到畫布、畫布上的操作順序 | Design 類型的格式說明。不照它寫，畫布會顯示不出來 |
| 字型與配色 token | 使用者在 Design System 設了預設時用預設，design-studio 在預設範圍內定方向。沒有預設時，design-studio 定出的方向就是設計系統 |

## 在畫布上走流程

1. **讀現況與查事實**：照常做。使用者的預設 Design System 視同既有的 `DESIGN.md`。
2. **一次問完**：照常做。畫布的格式說明要求問不到人時自己決定並說明假設，與 design-studio 一致。
3. **定方向**：照常做。方向寫進給使用者的說明，不另外寫檔。
4. **寫規格再製作**：先在對話中整理規格重點（段落節奏、景深層、形狀語言），再照畫布格式寫 artboard。
5. **驗證**：照畫布的規定，使用者沒要求就不截圖、不渲染檢查。改成在寫 artboard 前，用 `shared/verification.md` 的「AI-Look Checklist」逐條檢查規格。

## 三個衝突點的處理

- **驗證**：如上，在畫布上不主動截圖。使用者在畫布上看得到即時畫面，有問題會直接回饋。
- **WebGPU 特效**：畫布不允許直接從網路載入 three.js 這類套件，要先上傳成畫布的附檔才能引用；畫面元素也要用它規定的標記寫，不能用程式動態產生。畫布上能不能跑 WebGPU 還沒確認。確認前，需要 WebGPU 特效時做成獨立的 HTML 頁面（`webgpu-effects.md`），畫布上放靜態版本，並告訴使用者兩者的關係。
- **DESIGN.md 與過程檔**：在畫布上做、沒有專案資料夾時，不寫 `DESIGN.md` 和 `docs/design/` 的過程檔。在專案資料夾裡工作時照常寫。

## Slides 類型與其他簡報路線

- Slides 類型：design-studio 定方向，Slides 類型管格式。電影感方向的構圖與小裝飾仍參考 `cinematic-slides.md`，只要能用 Slides 的格式表達。
- design-studio 自己的 HTML 簡報（`slide-decks.md`）：要 PDF 或可編輯 PPTX 時用。
- open-slide-studio：使用者要它那套可以本機編輯、部署成網址的 React 簡報環境時才用。
