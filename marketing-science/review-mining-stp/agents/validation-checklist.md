# Validation Checklist

## RED: Baseline Failures To Replace

- 舊 skill 非 STP router
- 不支援 stage-aware `run_mode`
- 不支援 `MissingPrerequisiteOutput`
- 缺少 `current-target-market` / `potential-target-market`
- 缺少品牌欄 + 理想點的定位評分表契約
- 缺少 `POD / POP`
- 缺少四象限策略矩陣
- 缺少 `每群占比 > 5%` rerun guardrail

## GREEN: Required Post-Upgrade Checks

- `SKILL.md` name 已改為 `review-mining-stp`
- description 以 `Use when...` 開頭
- `run_mode` 含 `full | segmentation | targeting | positioning | custom`
- `requested_modules` 已定義固定白名單
- 含 `MissingPrerequisiteOutput`
- `Execution Scope Summary` 為永遠必填
- segmentation 明確包含：
  - 人／貨／場
  - `System 1 / System 2`
  - Maslow 五需求關鍵字
  - 區隔變數 taxonomy
  - `>5%` rerun guardrail
- targeting 明確包含：
  - `current-target-market`
  - `potential-target-market`
  - `ANOVA / regression`
  - `chi-square / logistic regression`
  - `Target Selection Decision`
- positioning 明確包含：
  - 定位評分表
  - 品牌欄
  - 理想點
  - `factor_analysis` default
  - `MDS` exception rule
  - `POD / POP`
  - 訴求 / 改善 / 改變 / 放棄
- `Dynamic Scorecard Summary` 明確要求信度 / 效度分析
- references 已改為 STP 規格語氣
- validation scenarios 已覆蓋：
  - full STP
  - segmentation only
  - targeting with upstream
  - positioning only
  - custom missing prerequisite

## REFACTOR: Final Audit Checks

- 是否仍有舊 skill 名稱殘留識別字
- 是否仍有對話式主流程敘述
- 是否漏掉 `Maslow keywords`
- 是否漏掉 `cluster >5%`
- 是否漏掉 `LLM bridge -> positioning scorecard`
- 是否漏掉 `ideal point`
- 是否漏掉 `POD / POP`
- 是否漏掉 `訴求 / 改善 / 改變 / 放棄`
- 是否可從 `references/07-review-mining-improve-traceability.md` 完成最終對照

## Acceptance Gate

僅在下列條件全部成立時，方可視為完成：

- skill 身份已改成 `review-mining-stp`
- full / partial / custom 三種操作方式均已明確定義
- `review-mining-improve.md` 的核心要求均有落點
- 壓力場景足以驗證 renamed skill、partial run 與 STP 完整鏈
