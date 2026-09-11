# Excalidraw JSON Schema Reference

生成任何模式前讀取本檔。以下個別元素範例只展示該類型差異，須與共用欄位組合；不是完整 drawing。

## 共用欄位與相容性

以下是未綁定元素的起始範例。`boundElements: null` 只適用於沒有綁定對象；
綁定文字時必須同時設定容器的 `boundElements` 與文字的 `containerId`，見下方範例。
`boundElements` 可為陣列或 null，不應清空既有的有效綁定。

`frameId`、`index`、`versionNonce` 是官方元素欄位，不能一律當作不合法欄位刪除。
`updated` 是更新時間戳，不必固定為 1。範例中的 1 是初始示例值。
新增或編輯時依目標版本的匯出格式處理，保留有效既有欄位；不要自行加入未知欄位。
不同工具版本的相容性，須以實際開啟、渲染及必要互動確認。

查證來源：[官方元素型別](https://github.com/excalidraw/excalidraw/blob/master/packages/element/src/types.ts)。

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

## Element Types

### Rectangle
```json
{
  "type": "rectangle",
  "id": "unique-id",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "strokeColor": "#1e40af",
  "backgroundColor": "#dbeafe",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 3 }
}
```

### Text
```json
{
  "type": "text",
  "id": "unique-id",
  "x": 150,
  "y": 130,
  "text": "Content here",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e40af",
  "backgroundColor": "transparent"
}
```

### Arrow
```json
{
  "type": "arrow",
  "id": "unique-id",
  "x": 300,
  "y": 140,
  "width": 100,
  "height": 0,
  "points": [[0, 0], [100, 0]],
  "strokeColor": "#374151",
  "strokeWidth": 2,
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

### Ellipse
```json
{
  "type": "ellipse",
  "id": "unique-id",
  "x": 100,
  "y": 100,
  "width": 120,
  "height": 120,
  "strokeColor": "#10b981",
  "backgroundColor": "#d1fae5",
  "fillStyle": "solid"
}
```

### Diamond
```json
{
  "type": "diamond",
  "id": "unique-id",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 100,
  "strokeColor": "#f59e0b",
  "backgroundColor": "#fef3c7",
  "fillStyle": "solid"
}
```

### Line
```json
{
  "type": "line",
  "id": "unique-id",
  "x": 100,
  "y": 100,
  "points": [[0, 0], [200, 100]],
  "strokeColor": "#374151",
  "strokeWidth": 2
}
```

## Full JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

配色請使用 [色票與對比規則](design-palette.md)。

## Font Family Values

| Value | Font Name |
|-------|-----------|
| 1 | Virgil (hand-drawn) |
| 2 | Helvetica |
| 3 | Cascadia |
| 4 | Assistant |
| 5 | Excalifont (recommended) |

## Fill Styles

- `solid` - Solid fill
- `hachure` - Hatched lines
- `cross-hatch` - Cross-hatched
- `zigzag` - Zigzag pattern

## Roundness Types

- `{ "type": 1 }` - Sharp corners
- `{ "type": 2 }` - Slight rounding
- `{ "type": 3 }` - Full rounding (recommended)

## Element Binding

To connect text to a container, maintain both sides with matching IDs. These fragments extend the common fields:

```json
{
  "type": "rectangle",
  "id": "container-id",
  "boundElements": [{ "id": "text-id", "type": "text" }]
}
```

```json
{
  "type": "text",
  "id": "text-id",
  "containerId": "container-id"
}
```

## Arrow Binding

To connect arrows to shapes, use the target version’s exported binding format and update the shapes’ reverse `boundElements` references. The following is a legacy focus/gap example; do not copy it into a different version without verifying import and movement behavior:

```json
{
  "type": "arrow",
  "startBinding": {
    "elementId": "source-shape-id",
    "focus": 0,
    "gap": 5
  },
  "endBinding": {
    "elementId": "target-shape-id",
    "focus": 0,
    "gap": 5
  }
}
```
