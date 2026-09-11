# Mode 3: Animated Excalidraw Format

先讀 [Standard 完整 drawing 格式](mode-standard.md)。與 Standard 格式相同，但每個元素添加 `customData.animate` 欄位控制動畫順序：

```json
{
  "id": "element-1",
  "type": "rectangle",
  "customData": {
    "animate": {
      "order": 1,
      "duration": 500
    }
  }
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

產出前先讀 [共用元素格式](excalidraw-schema.md)，將實際元素放入完整 drawing。

## 開啟方式與回覆範例

以下為回覆示例，實際交付時使用可點擊的完整檔案路徑，並補上實際驗證結果。

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
