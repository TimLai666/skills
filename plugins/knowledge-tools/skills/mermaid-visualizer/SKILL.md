---
name: mermaid-visualizer
description: >-
  Transform text content into professional Mermaid diagrams for presentations
  and documentation. This skill MUST be used when the user names Mermaid, and
  SHOULD be used when they ask to visualize concepts, create flowcharts, or
  make diagrams from text (流程圖、架構圖、關係圖、時序圖、心智圖). For diagrams
  inside HTML Artifacts, MUST prefer the artifact’s existing HTML/CSS/SVG or
  diagram approach; select Mermaid when it fits, not merely because a flowchart
  was requested. Explicit Excalidraw requests MUST use excalidraw-diagram, and
  explicit Obsidian Canvas requests MUST use obsidian-canvas-creator.
metadata:
  version: "1.2.0"
---

# Mermaid Visualizer

## 選用與目標

依內容與交付位置自動選用，使用者不必記住 skill 名稱。適合把步驟、
概念關係、架構或互動整理成 Mermaid 圖。明確指定其他圖表格式時尊重指定。
HTML Artifact 內先沿用既有 HTML、CSS、SVG 或圖表工具；Mermaid 符合
整份交付物的需求時才使用，不因「流程圖」一詞就強制切換。

## Workflow

1. 理解概念、關係、順序與圖表用途，確認呈現位置及可用的 Mermaid 版本。
2. 依下表選圖類型。需要分組、回饋迴圈或中心節點範例時，讀 [完整圖例](references/examples.md)。
3. 套用使用者指定的方向、細節與風格；未指定時以 TB、適中細節為起點，依畫面調整。配色或設計選項見 [設計參考](references/design-options.md)，其中選項不是通用 API 參數。
4. 產生 Mermaid 程式碼，遵守下方易錯規則。特殊標點、換行、subgraph、樣式或解析錯誤，先讀 [語法與排錯](references/syntax-rules.md) 對應段落。
5. 執行下方驗收，修正受影響的圖。Markdown 使用 mermaid code fence；HTML 依既有整合方式嵌入。
6. 交付圖表及必要說明，指出實際驗證的工具與尚未確認的相容性。

## 圖表選擇

| 內容 | 圖類型 |
|---|---|
| 步驟、決策、工作流程 | Flowchart，TB 或 LR |
| 循環與回饋 | Flowchart 加回饋連線，不保證自動排成圓形 |
| 方案比較 | 平行分組或對照流程 |
| 概念階層 | Mindmap |
| 元件間隨時間的訊息互動 | Sequence diagram |
| 狀態與轉換 | State diagram |

## 易錯規則

- 節點與 subgraph 使用明確 ID，顯示名稱另外設定，例如 `subgraph core["Core Process"]`。連線引用 ID。
- 含特殊標點的標籤先用引號包住並正確編碼，保留原文意思，不一律把括號或引號換成其他標點。
- 若目標工具出現 `Unsupported markdown: list`，檢查編號標籤與 Markdown 字串的處理方式，再改成可解析且不改意思的寫法。
- 換行、HTML 標籤與樣式支援依實際版本及設定驗證，不預設換行只適用圓形節點。
- Mermaid 註解用獨立一行的 `%%`。錯誤示範與說明文字不得混入可執行圖例。
- `-->` 是實線箭頭，`-.->` 是虛線箭頭，`==>` 是粗箭頭，`~~~` 是不可見的佈局連線。
- 使用一致配色及清楚標籤，不使用 Emoji。採用目標工具的預設樣式也可以，不強制每張圖都有 style 宣告。

## 驗收

- 在目標渲染工具或相同版本的環境解析並實際查看畫面，檢查節點、分組、連線與標籤是否符合原意。
- 確認文字完整、無不當遮擋、方向清楚、配色可讀。解析通過不能代替畫面驗證。
- 涉及互動時實際操作；修正後重新檢查受影響部分。
- 若只能在其他版本或工具中驗證，明說差異；無法渲染時回報未驗證，不宣稱已相容所有平台。
