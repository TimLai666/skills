# Validation Checklist

## RED: Baseline Findings From Previous Skill

- Frontmatter 不合規，包含 `version` 與 `author`
- 缺少 `When to Use / Do Not Use / Handoff`
- 沒有 `Data Sufficiency Gate`
- 沒有固定三大主題 taxonomy
- 沒有理論與 14 題項的分層規則
- 沒有 references 與壓力場景
- 容易讓模型直接輸出建議，但沒有先處理證據邊界

## GREEN: Post-Redesign Checks

- `SKILL.md` frontmatter 只有 `name` 與 `description`
- description 以 `Use when...` 開頭
- 預設語言與內容為 UTF-8 繁體中文
- 明確定義 `service_experience`、`product_performance`、`value_perception`
- 明確定義四個理論 overlay 的用途
- 明確定義 14 題項與 `0-7` 分規則
- 有 `MissingDataOutput`
- 有雙層輸出契約
- 已建立 5 份 reference 檔
- 已建立 3 份 pressure scenario 與 1 份 checklist

## REFACTOR: What To Recheck After Use

- Executive Summary 是否過度理論化
- 是否每次都保留三大主題第一層
- 是否在缺證據時維持題項 `0`
- 是否有明確偏誤與信心註記
- 是否把理論當成證據而不是解釋框架
- 是否把單一評論誤寫成趨勢

## Acceptance Gate

只有在以下都成立時，才可宣稱重構完成：

- 結構完整
- 無編碼亂碼
- 規則可執行
- 驗證資產齊備
- 預設輸出偏商業，可選研究附錄
