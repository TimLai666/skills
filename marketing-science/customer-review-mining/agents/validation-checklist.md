# Validation Checklist

## RED: Baseline Findings From Previous Skill

- 理論流程是條件式，與「理論必經」要求衝突
- Workflow 順序未強制「逐條語意解析 -> 理論映射 -> 主題整合」
- `Theory Coding Summary` 不是必填段落
- JSON 最小欄位缺少理論必填欄位
- 未明確規範 `$maslow-five-needs-marketing` 的必跑路由與 fallback 記錄
- 缺少單一文件的端到端範例鏈（input -> theory -> dynamic items -> output）
- 缺少「評分後必做統計驗證與分群」的固定流程
- 缺少統計檢定完整欄位（FDR、effect size、CI）
- 缺少分群穩定度與低樣本 guardrail
- 壓力場景未完整覆蓋理論必經失敗模式

## GREEN: Post-Redesign Checks

- `SKILL.md` frontmatter 只有 `name` 與 `description`
- description 以 `Use when...` 開頭
- 明確定義「理論必經」與四理論全覆蓋
- 明確定義 Maslow 路由為 `預設呼叫 + 可回退`
- Workflow 已固定為：
  - 逐條語意解析
  - 必經理論映射
  - 主題整合
  - 動態題項生成與評分
  - 統計驗證
  - 顧客分群
- `Theory Coding Summary` 為預設必填段落
- `Theory Coding Summary` 有 Maslow 協作狀態欄位：
  - `attempted`
  - `used`
  - `fallback_reason`
- JSON 最小欄位包含：
  - `theory_application_summary`
  - `theory_evidence_trace`
- `theory_evidence_trace` 可標記 `source_skill`
- 動態題項仍為語料級共用集合
- 外部 skill 協作仍是補充，不是主流程替代
- `Do not use` 不再禁止統計檢定，僅禁止因果過度宣稱
- `customer_id` 已列為強烈建議欄位
- 主報告必含：
  - `Statistical Validation Summary`
  - `Customer Cluster Summary`
  - `Cluster Archetype Cards`
  - `Cluster-Specific Priority Actions`
- JSON 最小欄位已包含：
  - `statistical_validation_summary`
  - `statistical_test_results`
  - `multiple_comparison_control`
  - `cluster_configuration`
  - `cluster_profiles`
  - `cluster_assignments`
  - `cluster_stability`
  - `cluster_action_map`
- `references/06-end-to-end-examples.md` 已存在且可從 `SKILL.md` 直接導覽
- `references/07-statistical-and-clustering-validation.md` 已存在且可從 `SKILL.md` 導覽
- 範例同時覆蓋：
  - 成功協作（Maslow used=true）
  - fallback（attempted=true, used=false）
  - 小樣本低信心情境
  - 同義題項合併前後對照
  - Scorecard -> Clustering 完整鏈路（Example E）

## REFACTOR: Mandatory Theory Compliance Checks

- 是否每次都套用四理論
- 是否每個理論都有證據追溯
- 是否每個理論都有信心等級
- 是否在低證據時標示限制而非跳過
- 是否先嘗試 `$maslow-five-needs-marketing`，失敗才 fallback
- 是否避免把 fallback 說成成功協作
- 是否避免理論段落過長壓過商業重點
- 是否仍阻擋無證據因果推論
- 是否有完整 JSON appendix 範例且欄位齊全
- 是否避免在範例中復活固定 14 題 rubric
- 是否先評分再分群（不可反序）
- 是否使用 `core` 題項共享分數矩陣分群
- 是否同時輸出 `K-medoids` 主分群與 `Ward` 群間解讀
- 是否有統計檢定 + FDR + effect size + CI
- 是否有 bootstrap 分群穩定度（ARI/NMI）與最小群體占比
- 低樣本是否 `exploratory=true` 且 `confidence=low`
- 是否避免把關聯差異寫成因果

## Acceptance Gate

只有以下都成立，才可宣稱完成：

- 理論流程為必經且可驗證
- 輸出契約含理論必填段落與欄位
- Maslow 協作路由與 fallback 可審計
- 動態題項規則保持有效
- 統計與分群規則可審計且可重現
- 壓力場景可捕捉理論必經違規
