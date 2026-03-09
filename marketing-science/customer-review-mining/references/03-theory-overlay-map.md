# Theory Overlay Map

## Purpose

理論是第二層解釋框架，用來補充評論背後的需求、動機與價值判斷。它不取代第一層商業主題，也不取代引文證據。

## Built-In Theory Lenses

### Product Positioning Theory

用來看評論在評價什麼：
- 產品屬性
- 產品功能
- 消費者利益
- 使用情境與服務場景

### Purchase Motivation Theory

用來看顧客購買時在意什麼：
- 功能性動機
- 保障性動機
- 關係性動機

### Maslow's Hierarchy of Needs

用來看評論背後隱含的需求層次：
- 生理需求
- 安全需求
- 社交需求
- 尊重需求
- 自我實現需求

### Word-of-Mouth Motivation Theory

用來看評論者為何願意分享：
- 助人利他
- 社交認同
- 專業展現
- 情緒表達

## Conditional Agent-Assisted Support

只有在以下情況才建議讓 agent 使用其他 skill 協助：
- 使用者要求更深理論詮釋
- 需要跨理論框架對照
- 需要特定領域或研究型補充

協作規則：
- 主分析骨架仍由 `customer-review-mining` 完成
- 其他 skill 只能補充理論解釋、研究背景或後續轉譯
- 若有使用其他 skill，輸出要標示其用途與限制

## Usage Rules

- 理論標籤只在有語意證據時使用
- 理論摘要必須附至少一段代表性評論或濃縮證據
- 不可把「某需求被滿足」直接寫成成長因果
- 管理摘要中只保留最有用的 1-3 個理論視角
