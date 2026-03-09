# Validation Checklist

## RED: Baseline Findings From Previous Skill

- 主檔內容存在編碼汙染風險
- 存在固定 14 題項假設
- 沒有語料級共用題項生成步驟
- 沒有條件式 agent 協作理論流程
- 容易讓模型在證據不足時仍完成完整評分

## GREEN: Post-Redesign Checks

- `SKILL.md` frontmatter 只有 `name` 與 `description`
- description 以 `Use when...` 開頭
- 預設語言與內容為 UTF-8 繁體中文
- 明確定義三大主題
- 明確定義動態題項生成與 `0-7` 分規則
- 明確定義條件式理論協作
- 有 `MissingDataOutput`
- 有雙層輸出契約
- 已建立 5 份 reference 檔
- 已建立 3 份 pressure scenario 與 1 份 checklist

## REFACTOR: What To Recheck After Use

- 題項是否為整批評論共用，而不是逐篇漂移
- 同義題項是否有正常合併
- 低頻訊號是否被錯誤升格為核心題項
- 理論協作是否變成強制流程
- Executive Summary 是否過度理論化
- 是否仍有無證據因果推論

## Acceptance Gate

只有在以下都成立時，才可宣稱重構完成：

- 結構完整
- 無固定題項依賴
- 動態題項規則可執行
- 條件式 agent 協作規則明確
- 驗證資產齊備
