# Review-Mining-Improve Traceability

## Purpose

本文件用於逐條對照 `review-mining-improve.md`，確認規格覆蓋完整。

## Required Traceability Checks

### 核心概念

- [ ] Maslow 五需求均有對應關鍵字
- [ ] `Dynamic Scorecard Summary` 包含信度 / 效度分析
- [ ] cluster 規則明確寫成 `每群占比 > 5%`
- [ ] 小群 `< 5%` 觸發降 `k` 重跑
- [ ] 每群均有明確特徵描述

### Segmentation

- [ ] 保留人／貨／場探勘
- [ ] `貨` 含 `System 1 / System 2`
- [ ] 市場區隔變數 taxonomy 含地理 / 人口 / 心理 / 行為
- [ ] 含消費者畫像敘事

### Targeting

- [ ] 含 `current-target-market`
- [ ] 含 `potential-target-market`
- [ ] 連續反應變數使用 `ANOVA / regression`
- [ ] 二元反應變數使用 `chi-square / logistic regression`
- [ ] 輸出含 `target selection decision`

### Positioning

- [ ] LLM 位於評論探勘與定位分析之間
- [ ] 含定位評分表
- [ ] 定位評分表含品牌欄與理想點
- [ ] 定位基礎含屬性功能 / 利益用途 / 品牌個性形象
- [ ] 預設使用 `factor_analysis`
- [ ] 僅在相似性資料時使用 `MDS`
- [ ] 含關鍵因素評估
- [ ] 含標竿分析
- [ ] 含理想點分析
- [ ] 含競爭態勢分析
- [ ] 含 `POD / POP`
- [ ] 含訴求 / 改善 / 改變 / 放棄

### Partial / Custom Run

- [ ] 含 `run_mode`
- [ ] 含 `requested_modules`
- [ ] 含 `upstream_artifacts`
- [ ] partial / custom 缺件時回 `MissingPrerequisiteOutput`
- [ ] 有評論時僅補跑最小必要前置
- [ ] 無評論且無 artifacts 時停止

### Final Audit Rule

- [ ] 完成後再讀一次 `review-mining-improve.md`
- [ ] 所有條目均可在 `SKILL.md` 或 references 中定位
