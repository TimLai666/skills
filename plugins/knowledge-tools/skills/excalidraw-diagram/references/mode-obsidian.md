# Mode 1: Obsidian Format (Default)

**嚴格按照以下結構輸出，不得有任何修改：**

````markdown
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
````

**關鍵要點：**
- Frontmatter 必須包含 `tags: [excalidraw]`
- 警告訊息必須完整
- JSON 必須被 `%%` 標記包圍
- 不能使用 `excalidraw-plugin: parsed` 以外的其他 frontmatter 設定
- `## Text Elements` 留空，外掛會依 Drawing JSON 填入文字元素。
- Drawing 的 `source` 使用 `https://github.com/zsviczian/obsidian-excalidraw-plugin`。
- **副檔名**：`.md`


產出前先讀 [共用元素格式](excalidraw-schema.md)，將實際元素放入完整 drawing。

## 開啟方式與回覆範例

以下為回覆示例，實際交付時使用可點擊的完整檔案路徑，並補上實際驗證結果。

**Obsidian 模式：**
```
Excalidraw 圖已產生！

儲存位置：商業模式.relationship.md

使用方式：
1. 在 Obsidian 中開啟此檔案
2. 點擊右上角 MORE OPTIONS 選單
3. 選擇 Switch to EXCALIDRAW VIEW
```

