# Mode 2: Standard Excalidraw Format

直接輸出純 JSON 檔案，可在 excalidraw.com 開啟：

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
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


產出前先讀 [共用元素格式](excalidraw-schema.md)，將實際元素放入完整 drawing。

## 開啟方式與回覆範例

以下為回覆示例，實際交付時使用可點擊的完整檔案路徑，並補上實際驗證結果。

**Standard 模式：**
```
Excalidraw 圖已產生！

儲存位置：商業模式.relationship.excalidraw

使用方式：
1. 開啟 https://excalidraw.com
2. 點擊左上角選單 → Open → 選擇此檔案
3. 或直接拖曳檔案到 excalidraw.com 頁面
```

