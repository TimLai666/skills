# Theory Overlay Map

## Purpose

理論是本技能的必經分析階段。每次分析都必須套用四個理論視角，並提供可追溯的證據映射。

## Mandatory Application Policy

- 每次分析都要執行理論映射，不可跳過
- 四個理論都要有對應結果，不可只挑 1-2 個理論
- 若某理論證據不足，必須標示 `low confidence` 與限制，不能留空
- 理論映射必須在主題整合之前完成
- 馬斯洛映射必須先嘗試由 `$maslow-five-needs-marketing` 協作產出
- 若外部 skill 不可用，才可回退本技能內建映射，且必須紀錄 `fallback_reason`

## Built-In Theory Lenses

### Product Positioning Theory

映射重點：
- 產品屬性
- 產品功能
- 消費者利益
- 使用情境與服務場景

### Purchase Motivation Theory

映射重點：
- 功能性動機
- 保障性動機
- 關係性動機

### Maslow's Hierarchy of Needs

映射重點：
- 生理需求
- 安全需求
- 社交需求
- 尊重需求
- 自我實現需求

### Word-of-Mouth Motivation Theory

映射重點：
- 助人利他
- 社交認同
- 專業展現
- 情緒表達

## Mapping Unit

可用兩種映射單位：
- 單篇評論映射
- 評論群（cluster）映射

無論哪種單位，都必須可回溯到原始評論。

## Maslow Collaboration Protocol

路由策略固定：`預設呼叫 + 可回退`。

### Minimum Input To `$maslow-five-needs-marketing`

- `review_text`（必填）
- `analysis_goal`（建議）
- `segment` 或 `channel`（若有）
- `locale`（若有）

### Expected Return Fields

- `maslow_level_mapping`：每筆評論或每個群組對應到五需求層
- `evidence_refs`：引文或證據索引
- `confidence`：`high|medium|low`
- `limitations`：證據不足時的限制說明

### Fallback Rule

- 若 `$maslow-five-needs-marketing` 無法使用，必須在本技能內完成馬斯洛映射
- 回退結果必須標記 `source_skill: customer-review-mining:fallback`
- 回退結果預設為保守信心；除非證據密度高，否則不得標示 `high`

## Evidence Trace Schema

每個理論至少輸出：

```json
{
  "theory": "",
  "mapping_unit": "review|cluster",
  "mapped_constructs": [],
  "evidence_refs": [],
  "source_skill": "maslow-five-needs-marketing|customer-review-mining:fallback|customer-review-mining",
  "confidence": "high|medium|low",
  "limitations": []
}
```

## Agent-Assisted Deepening

其他 skill 或 agent 僅能在理論深挖時補充，不能取代必經理論流程。
馬斯洛層級是例外中的必跑協作：需先嘗試 `$maslow-five-needs-marketing`，再決定是否回退。

允許情境：
- 使用者要求跨理論對照
- 使用者要求研究型擴展
- 使用者要求特定領域理論補充

強制規則：
- 主分析骨架必須由 `customer-review-mining` 完成
- 外部 skill 產出視為補充材料
- 輸出需標示外部協作來源與侷限
- 不可把 fallback 當作外部 skill 成功協作
