# Theory Overlay Map

## Purpose

理論是本技能的必經分析階段。每次分析都必須套用四個理論視角，並提供可追溯的證據映射。

## Mandatory Application Policy

- 每次分析都要執行理論映射，不可跳過
- 四個理論都要有對應結果，不可只挑 1-2 個理論
- 若某理論證據不足，必須標示 `low confidence` 與限制，不能留空
- 理論映射必須在主題整合之前完成

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

## Evidence Trace Schema

每個理論至少輸出：

```json
{
  "theory": "",
  "mapping_unit": "review|cluster",
  "mapped_constructs": [],
  "evidence_refs": [],
  "confidence": "high|medium|low",
  "limitations": []
}
```

## Agent-Assisted Deepening

其他 skill 或 agent 僅能在理論深挖時補充，不能取代必經理論流程。

允許情境：
- 使用者要求跨理論對照
- 使用者要求研究型擴展
- 使用者要求特定領域理論補充

強制規則：
- 主分析骨架必須由 `customer-review-mining` 完成
- 外部 skill 產出視為補充材料
- 輸出需標示外部協作來源與侷限
