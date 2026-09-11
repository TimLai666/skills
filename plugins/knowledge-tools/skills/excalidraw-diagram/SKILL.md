---
name: excalidraw-diagram
description: >-
  Create editable Excalidraw diagrams in Obsidian, standard or animated formats.
  This skill MUST be used when the user names Excalidraw. It SHOULD be selected
  from natural-language requests for standalone diagrams, concept relationships,
  mind maps, editable whiteboards or diagrams whose elements appear in sequence
  (畫圖、流程圖、心智圖、關係圖、白板、逐步呈現), without requiring the user to
  know the skill name. Choose by content and destination; illustration or photo
  requests need other tools. For diagrams inside HTML Artifacts, MUST prefer
  HTML/CSS/SVG or the artifact's existing diagram tools; use Excalidraw there only
  when explicitly requested or a concrete Excalidraw capability is needed.
  Hand-drawn styling alone is insufficient. Explicit Mermaid requests MUST use
  mermaid-visualizer instead.
metadata:
  version: "1.4.0"
---

# Excalidraw Diagram Generator

## 選用與輸出模式

依使用者想表達的內容與交付位置選擇，不要求使用者記住工具名稱。
獨立的流程、架構、概念關係、心智圖或可編輯白板，可依需求自動選用。
若圖是 HTML Artifact 的一部分，優先使用 HTML、CSS、SVG 或該 Artifact
既有的圖表工具。只有明確指定 Excalidraw，或需要可編輯 Excalidraw 檔、
整合既有圖稿等具體能力時，才在 HTML Artifact 中使用；手繪風格本身不足以切換。

使用者指定格式或使用情境時照其要求；未指定時維持 Obsidian 預設。
選定模式後，生成前必讀對應文件的完整模板與要求：

| 使用情境 | 模式與必讀文件 | 檔案 |
|---|---|---|
| Obsidian 筆記，或未指定格式 | [Obsidian](references/mode-obsidian.md) | `[主題].[類型].md` |
| 在 Excalidraw 網站開啟、編輯或分享 | [Standard](references/mode-standard.md) | `[主題].[類型].excalidraw` |
| 圖中元素依序出現、動畫繪製 | [Animated](references/mode-animated.md) | `[主題].[類型].animate.excalidraw` |

## Workflow

1. 確認交付位置與模式，分析概念、關係和層級，依下表選圖表形式。
2. 讀取所選模式文件，以及 [共用元素格式](references/excalidraw-schema.md)。需要配色時讀 [色票與對比規則](references/design-palette.md)。
3. 產生完整 drawing，確保唯一 ID、有效引用及正確的模式包裝。綁定文字或箭頭時，先讀格式文件對應的綁定章節。
4. 儲存到使用者指定位置；否則沿用專案成品目錄，沒有安排時放 `docs/excalidraw-diagram/`。非專案工作可使用目前工作目錄。檔名表達主題，已有同名檔先讀再判斷是否更新。
5. 執行下方格式與畫面驗證，修正本次造成的問題。
6. 回報可點擊的檔案路徑、模式、驗證結果，以及所選模式文件的開啟方式。簡述有助理解的設計選擇。

## Diagram Types & Selection Guide

選擇合適的圖表形式，以提升理解力與視覺吸引力。

| 類型 | 英文 | 使用情境 | 做法 |
|------|------|---------|------|
| **流程圖** | Flowchart | 步驟說明、工作流程、任務執行順序 | 用箭頭連接各步驟，清晰表達流程走向 |
| **心智圖** | Mind Map | 概念發散、主題分類、靈感捕捉 | 以中心為核心向外發散，放射狀結構 |
| **層級圖** | Hierarchy | 組織結構、內容分級、系統拆解 | 自上而下或自左至右建構層級節點 |
| **關係圖** | Relationship | 要素之間的影響、依賴、互動 | 圖形間用連線表示關聯，箭頭與說明 |
| **對比圖** | Comparison | 兩種以上方案或觀點的對照分析 | 左右兩欄或表格形式，標明比較維度 |
| **時間線圖** | Timeline | 事件發展、專案進度、模型演化 | 以時間為軸，標出關鍵時間點與事件 |
| **矩陣圖** | Matrix | 雙維度分類、任務優先級、定位 | 建立 X 與 Y 兩個維度，座標平面安置 |
| **自由版面配置** | Freeform | 內容零散、靈感記錄、初步資訊收集 | 無需結構限制，自由放置圖塊與箭頭 |

## Design Rules

### Text & Format
- **所有文字元素必須使用** `fontFamily: 5`（Excalifont 手寫字型）
- **文字中的雙引號替換規則**：`"` 替換為 `『』`
- **文字中的圓括號替換規則**：`()` 替換為 `「」`
- **字型大小規則**（硬性下限，低於此值在正常縮放下不可讀）：
  - 標題：20-28px（最小 20px）
  - 副標題：18-20px
  - 正文/標籤：16-18px（最小 16px）
  - 次要註釋：14px（僅限不重要的輔助說明，慎用）
  - **絕對禁止低於 14px**
- **行高**：所有文字使用 `lineHeight: 1.25`
- **文字置中估算**：獨立文字元素沒有自動置中，需手動計算 x 座標：
  - 估算文字寬度：`estimatedWidth = text.length * fontSize * 0.5`（CJK 字元用 `* 1.0`）
  - 置中公式：`x = centerX - estimatedWidth / 2`
  - 範例：文字 "Hello"（5字元, fontSize 20）置中於 x=300 → `estimatedWidth = 5 * 20 * 0.5 = 50` → `x = 300 - 25 = 275`

### Layout & Design
- **畫布範圍**：建議所有元素在 0-1200 x 0-800 區域內
- **最小形狀尺寸**：帶文字的矩形/橢圓不小於 120x60px
- **元素間距**：最小 20-30px 間距，防止重疊
- **層次清晰**：使用不同顏色和形狀區分不同層級的資訊
- **圖形元素**：適當使用矩形框、圓形、箭頭等元素來組織資訊
- **禁止 Emoji**：不要在圖表文字中使用任何 Emoji 符號，如需視覺標記請使用簡單圖形（圓形、方形、箭頭）或顏色區分

配色與對比度詳見 [色票](references/design-palette.md)。

## Common Mistakes to Avoid

- **文字偏移** — 獨立 text 元素的 `x` 是左邊緣，不是中心。必須用置中公式手動計算，否則文字會偏到一邊
- **元素重疊** — y 座標相近的元素容易堆疊。放置新元素前檢查與周圍元素是否有至少 20px 間距
- **畫布留白不足** — 內容不要貼著畫布邊緣。在四周留 50-80px 的 padding
- **標題沒有置中於圖表** — 標題應置中於下方圖表的整體寬度，不是固定在 x=0
- **箭頭標籤溢出** — 長文字標籤（如 "ATP + NADPH"）會超出短箭頭。保持標籤簡短或加大箭頭長度
- **對比度不夠** — 淺色文字在白底上幾乎不可見。文字顏色不低於 `#757575`，有色文字用深色變體
- **字級太小** — 低於 14px 在正常縮放下不可讀，正文最小 16px

## 格式與畫面驗證

- 用 JSON parser 檢查 drawing，確認元素 ID 唯一，綁定、圖片等引用存在。Obsidian 模式另核對 Markdown 包裝。
- 在目標工具實際開啟或以相容渲染器產生畫面並查看，確認文字不裁切、節點不重疊、箭頭方向與標籤正確、對比與留白清楚。僅通過 JSON 解析不能證明圖可讀。
- 有綁定關係時，移動容器檢查文字或箭頭是否正確跟隨；Animated 模式實際預覽順序與時長。
- 修正後重新檢查受影響畫面與互動。工具不可用時，明說未驗證的模式、畫面或互動，不宣稱已完整驗證。
