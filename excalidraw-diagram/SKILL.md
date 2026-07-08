---
name: excalidraw-diagram
description: Generate hand-drawn style Excalidraw diagrams from text content. Supports three output modes - Obsidian (.md), Standard (.excalidraw), and Animated (.excalidraw with animation order). Choose this over Obsidian Canvas when the user wants an Excalidraw hand-drawn whiteboard style. Triggers on "Excalidraw", "畫圖", "Excalidraw流程圖", "Excalidraw心智圖", "標準Excalidraw", "standard excalidraw", "Excalidraw動畫", "動畫圖".
metadata:
  version: 1.2.1
---

# Excalidraw Diagram Generator

Create Excalidraw diagrams from text content with multiple output formats.

## Output Modes

根據使用者的觸發詞選擇輸出模式：

| 觸發詞 | 輸出模式 | 檔案格式 | 用途 |
|--------|----------|----------|------|
| `Excalidraw`、`畫圖`、`Excalidraw流程圖`、`Excalidraw心智圖` | **Obsidian**（預設） | `.md` | 在 Obsidian 中直接開啟 |
| `標準Excalidraw`、`standard excalidraw` | **Standard** | `.excalidraw` | 在 excalidraw.com 開啟/編輯/分享 |
| `Excalidraw動畫`、`動畫圖`、`animate` | **Animated** | `.excalidraw` | 拖到 excalidraw-animate 產生動畫 |

## Workflow

1. **Detect output mode** from trigger words (see Output Modes table above)
2. Analyze content - identify concepts, relationships, hierarchy
3. Choose diagram type (see Diagram Types below)
4. Generate Excalidraw JSON (add animation order if Animated mode)
5. Output in correct format based on mode
6. **Automatically save to current working directory**
7. Notify user with file path and usage instructions

## Output Formats

### Mode 1: Obsidian Format (Default)

**嚴格按照以下結構輸出，不得有任何修改：**

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
```json
{JSON 完整資料}
```
%%
```

**關鍵要點：**
- Frontmatter 必須包含 `tags: [excalidraw]`
- 警告訊息必須完整
- JSON 必須被 `%%` 標記包圍
- 不能使用 `excalidraw-plugin: parsed` 以外的其他 frontmatter 設定
- **副檔名**：`.md`

### Mode 2: Standard Excalidraw Format

直接輸出純 JSON 檔案，可在 excalidraw.com 開啟：

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

**關鍵要點：**
- `source` 使用 `https://excalidraw.com`（不是 Obsidian 外掛）
- 純 JSON，無 Markdown 包裝
- **副檔名**：`.excalidraw`

### Mode 3: Animated Excalidraw Format

與 Standard 格式相同，但每個元素添加 `customData.animate` 欄位控制動畫順序：

```json
{
  "id": "element-1",
  "type": "rectangle",
  "customData": {
    "animate": {
      "order": 1,
      "duration": 500
    }
  },
  ...其他標準欄位
}
```

**動畫順序規則：**
- `order`: 動畫播放順序（1, 2, 3...），數字越小越先出現
- `duration`: 該元素的繪製時長（毫秒），預設 500
- 相同 `order` 的元素同時出現
- 建議順序：標題 → 主要框架 → 連接線 → 細節文字

**使用方法：**
1. 產生 `.excalidraw` 檔案
2. 拖到 https://dai-shi.github.io/excalidraw-animate/
3. 點擊 Animate 預覽，然後匯出 SVG 或 WebM

**副檔名**：`.excalidraw`

---

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
  - 次要註釋：14px（僅限不重要的辅助說明，慎用）
  - **絕對禁止低於 14px**
- **行高**：所有文字使用 `lineHeight: 1.25`
- **文字置中估算**：獨立文字元素沒有自动置中，需手動計算 x 座標：
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

### Color Palette

**文字顏色（strokeColor for text）：**

| 用途 | 色值 | 說明 |
|------|------|------|
| 標題 | `#1e40af` | 深藍 |
| 副標題/連接線 | `#3b82f6` | 亮藍 |
| 正文文字 | `#374151` | 深灰（白底最淺不低於 `#757575`） |
| 強調/重點 | `#f59e0b` | 金色 |

**形狀填充色（backgroundColor, fillStyle: "solid"）：**

| 色值 | 語意 | 適用情境 |
|------|------|---------|
| `#a5d8ff` | 淺藍 | 輸入、資料源、主要節點 |
| `#b2f2bb` | 淺綠 | 成功、輸出、已完成 |
| `#ffd8a8` | 淺橙 | 警告、待處理、外部依賴 |
| `#d0bfff` | 淺紫 | 處理中、中間件、特殊項 |
| `#ffc9c9` | 淺紅 | 錯誤、關鍵、告警 |
| `#fff3bf` | 淺黃 | 備註、決策、規劃 |
| `#c3fae8` | 淺青 | 儲存、資料、快取 |
| `#eebefa` | 淺粉 | 分析、指標、統計 |

**區域背景色（大矩形 + opacity: 30，用於分層圖表）：**

| 色值 | 語意 |
|------|------|
| `#dbe4ff` | 前端/UI 層 |
| `#e5dbff` | 邏輯/處理層 |
| `#d3f9d8` | 資料/工具層 |

**對比度規則：**
- 白底上文字最淺不低於 `#757575`，否則不可讀
- 淺色填充上用深色變體文字（如淺綠底用 `#15803d`，不用 `#22c55e`）
- 避免淺灰色文字（`#b0b0b0`、`#999`）出現在白底上

參考：[references/excalidraw-schema.md](references/excalidraw-schema.md)

## JSON Structure

**Obsidian 模式：**
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [...],
  "appState": { "gridSize": null, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

**Standard / Animated 模式：**
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": { "gridSize": null, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
```

## Element Template

Each element requires these fields (do NOT add extra fields like `frameId`, `index`, `versionNonce`, `rawText` -- they may cause issues on excalidraw.com. `boundElements` must be `null` not `[]`, `updated` must be `1` not timestamps):

```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 200, "height": 50,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "roundness": {"type": 3},
  "seed": 123456789,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

`strokeStyle` values: `"solid"`（實線，預設）| `"dashed"`（虛線）| `"dotted"`（點線）。虛線適合表示選擇性路徑、非同步流、弱關聯等。

Text elements add:
```json
{
  "text": "顯示文字",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "顯示文字",
  "autoResize": true,
  "lineHeight": 1.25
}
```

**Animated 模式額外添加** `customData` 欄位：
```json
{
  "id": "title-1",
  "type": "text",
  "customData": {
    "animate": {
      "order": 1,
      "duration": 500
    }
  },
  ...其他欄位
}
```

See [references/excalidraw-schema.md](references/excalidraw-schema.md) for all element types.

---

## Additional Technical Requirements

### Text Elements 處理
- `## Text Elements` 部分在 Markdown 中**必須留空**，僅用 `%%` 作為分隔符
- Obsidian ExcaliDraw 外掛會根據 JSON 資料**自動填充文字元素**
- 不需要手動列出所有文字內容

### 座標與佈局
- **座標系統**：左上角為原點 (0,0)
- **建議範圍**：所有元素在 0-1200 x 0-800 像素範圍內
- **元素 ID**：每個元素需要唯一的 `id`（可以是字串，如「title」「box1」等）

### Required Fields for All Elements

**IMPORTANT**: Do NOT include `frameId`, `index`, `versionNonce`, or `rawText` fields. Use `boundElements: null` (not `[]`), and `updated: 1` (not timestamps).

```json
{
  "id": "unique-identifier",
  "type": "rectangle|text|arrow|ellipse|diamond",
  "x": 100, "y": 100,
  "width": 200, "height": 50,
  "angle": 0,
  "strokeColor": "#color-hex",
  "backgroundColor": "transparent|#color-hex",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid|dashed|dotted",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "roundness": {"type": 3},
  "seed": 123456789,
  "version": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

### Text-Specific Properties
文字元素 (type: "text") 需要額外屬性（do NOT include `rawText`）：
```json
{
  "text": "顯示文字",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "顯示文字",
  "autoResize": true,
  "lineHeight": 1.25
}
```

### appState 配置
```json
"appState": {
  "gridSize": null,
  "viewBackgroundColor": "#ffffff"
}
```

### files 欄位
```json
"files": {}
```

## Common Mistakes to Avoid

- **文字偏移** — 獨立 text 元素的 `x` 是左邊緣，不是中心。必須用置中公式手動計算，否則文字會偏到一邊
- **元素重疊** — y 座標相近的元素容易堆疊。放置新元素前檢查與周圍元素是否有至少 20px 間距
- **畫布留白不足** — 內容不要貼著畫布邊緣。在四周留 50-80px 的 padding
- **標題沒有置中於圖表** — 標題應置中於下方圖表的整體寬度，不是固定在 x=0
- **箭頭標籤溢出** — 長文字標籤（如 "ATP + NADPH"）會超出短箭頭。保持標籤簡短或加大箭頭長度
- **對比度不夠** — 淺色文字在白底上幾乎不可見。文字顏色不低於 `#757575`，有色文字用深色變體
- **字級太小** — 低於 14px 在正常縮放下不可讀，正文最小 16px

## Implementation Notes

### Auto-save & File Generation Workflow

當產生 Excalidraw 圖表時，**必須自動執行以下步驟**：

#### 1. 選擇合適的圖表類型
- 根據使用者提供的內容特性，參考上方 「Diagram Types & Selection Guide」 表
- 分析內容的核心訴求，選擇最合適的視覺化形式

#### 2. 產生有意義的檔案名稱

根據輸出模式選擇副檔名：

| 模式 | 檔案名稱格式 | 範例 |
|------|-----------|------|
| Obsidian | `[主題].[類型].md` | `商業模式.relationship.md` |
| Standard | `[主題].[類型].excalidraw` | `商業模式.relationship.excalidraw` |
| Animated | `[主題].[類型].animate.excalidraw` | `商業模式.relationship.animate.excalidraw` |

- 優先使用中文以提高清晰度

#### 3. 使用 Write 工具自動儲存檔案
- **儲存位置**：目前工作目錄（自動偵測環境變數）
- **完整路徑**：`{current_directory}/[filename].md`
- 這樣可以實現靈活遷移，無需寫死路徑

#### 4. 確保 Markdown 結構完全正確
**必須按以下格式產生**（不能有任何修改）：

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
```json
{完整的 JSON 資料}
```
%%
```

#### 5. JSON 資料要求
- 包含完整的 Excalidraw JSON 結構
- 所有文字元素使用 `fontFamily: 5`
- 文字中的 `"` 替換為 `『』`
- 文字中的 `()` 替換為 `「」`
- JSON 格式必須有效，通過語法檢查
- 所有元素有唯一的 `id`
- 包含 `appState` 和 `files: {}` 欄位

#### 6. 使用者回饋與確認
向使用者報告：
- 圖表已產生
- 精確的儲存位置
- 如何在 Obsidian 中檢視
- 圖表的設計選擇說明（選擇了什麼類型的圖表、為什麼）
- 是否需要調整或修改

### Example Output Messages

**Obsidian 模式：**
```
Excalidraw 圖已產生！

儲存位置：商業模式.relationship.md

使用方式：
1. 在 Obsidian 中開啟此檔案
2. 點擊右上角 MORE OPTIONS 選單
3. 選擇 Switch to EXCALIDRAW VIEW
```

**Standard 模式：**
```
Excalidraw 圖已產生！

儲存位置：商業模式.relationship.excalidraw

使用方式：
1. 開啟 https://excalidraw.com
2. 點擊左上角選單 → Open → 選擇此檔案
3. 或直接拖曳檔案到 excalidraw.com 頁面
```

**Animated 模式：**
```
Excalidraw 動畫圖已產生！

儲存位置：商業模式.relationship.animate.excalidraw

動畫順序：標題(1) → 主框架(2-4) → 連接線(5-7) → 說明文字(8-10)

產生動畫：
1. 開啟 https://dai-shi.github.io/excalidraw-animate/
2. 點擊 Load File 選擇此檔案
3. 預覽動畫效果
4. 點擊 Export 匯出 SVG 或 WebM
```
