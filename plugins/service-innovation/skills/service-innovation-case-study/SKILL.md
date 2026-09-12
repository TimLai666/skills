---
name: service-innovation-case-study
description: >-
  This skill MUST be used for service innovation case studies (服務創新案例分析),
  complete classroom-format reports, or research combining frameworks such as
  PESTEL, Five Forces, SWOT, STP, BMC, persona, service blueprints, and CJM.
  It SHOULD also be used when researching a 品牌、App、平台或服務 to understand its
  innovation, business model, customer experience, or outcomes, even without
  naming a framework. Match the analysis scope to the request.
metadata:
  version: "1.2.0"
---

# 服務創新案例研究

## Overview

研究服務如何創造價值、如何運作，以及目前效果。完整報告保留生態系地圖、PESTEL、五力、SWOT、策略、STP、BMC、Persona、服務藍圖與 CJM 的分析承接，從來源推導結論。

## Input Contract

確認案例的正式名稱、官網與主要業務，避免混入同名公司。辨識研究問題、市場與時間範圍、使用者提供的資料、課堂要求及交付格式。

| 需求 | 執行範圍 |
| --- | --- |
| 完整案例報告或完整服務創新研究 | 完成全條分析鏈及報告章節，數量與判斷依案例證據 |
| 指定課堂格式或沿用本 skill 的課堂報告 | 保留完整章節與課堂設定，使用者提供的要求優先 |
| 局部研究、單一問題或修訂既有區段 | 完成相關分析，核對會影響該結論的上游依據與下游內容 |

依需求判斷範圍，無法判斷且會明顯影響成果時再確認。課堂模式的數量、評分與章節規格集中在 [區段規格](references/03-section-specs.md)，一般完整報告不因採彈性數量而省略分析環節。

## Workflow

### 1. 建立研究依據

新案例開始前讀 [資料查核流程](references/01-research-protocol.md)。檢視公司、創辦人、資金、功能、市場與外部評價各面向，依案例找適用的來源。讀過並核對資料後才寫入事實，記錄來源與資料時間。

既有材料可使用，但須核對來源、適用範圍與時效。找不到的資料標為本次未找到，來源無法存取則標示受阻。推論與評分寫出依據，不能用看似合理的資料填補缺口。

### 2. 完成分析承接

完整研究開始分析前讀 [分析鏈](references/02-analysis-chain.md)，依下列順序推進。局部研究讀取其中相關段落及其必要上游規格。

| 分析 | 對後續工作的作用 |
| --- | --- |
| 生態系地圖 | 界定參與者、關係、交換與競爭範圍 |
| PESTEL、五力 | 辨識外部機會、威脅、競爭結構與議價條件 |
| SWOT、策略比較 | 整合內外部依據，選出有比較理由的主要方向 |
| STP | 依環境、競爭、能力及需求證據選客群，形成與主要方向一致的定位 |
| BMC | 比較創新起點，串接九格的價值創造、傳遞與收益邏輯 |
| Persona | 從目標客群與實際使用者資料整理有依據的複合人物 |
| 服務藍圖、CJM | 對應同一使用者情境，分析交付流程與真實體驗摩擦 |
| 效果與啟發 | 區分品牌宣稱、已證實效果與缺口，提出有適用條件的啟發 |

需要細部方法時，讀取可用的對應 skill：`pestel-analysis`、`business-model-architect`、`ecosystem-map-and-blueprint`、`customer-journey-mapper`。保持本次已確定的範圍與課堂要求，不能讓其他技能擴大交付。課堂參數以區段規格為準，一般研究說明使用的評分與篩選依據。

每完成一段，確認引用與分析依據足以支撐結論。後續發現新證據時回頭更新相關段落，不保留互相矛盾的結論。

### 3. 整理報告並驗收

完整報告撰寫前讀 [區段規格](references/03-section-specs.md) 與 [報告模板](assets/report-template.md)，保留完整章節順序。局部交付只讀取並使用相關部分。

交付前讀 [完整品質檢查清單](references/04-quality-checklist.md)，逐項核對本次範圍。缺少必要證據的部分保留明確缺口，不能宣稱已驗證。使用者指定的課堂作業不得縮成摘要。

## Output Contract

- 預設交付台灣繁體中文 Markdown。完整報告採模板章節，局部研究交付問題、證據、分析與結論。
- 正文的事實就近引用，完整報告另有最後的統一參考資料清單，編號不可重複。
- 圖表依指定格式呈現，未指定時生態系地圖可用 Mermaid。關係種類與確認狀態分別標明，避免同一符號混用。
- 使用指定位置或工作區既有成果目錄。沒有慣例時，報告放在 `docs/service-innovation-case-study/[品牌名]_report.md`。既有檔案先讀取，再更新相關部分。
- 完整研究可逐階段更新同一份報告，維持章節與引用一致，不因中途落檔而把未完成內容當成定稿。

## Quality Rules

- 資料來源須能支持具體主張。公司自述、獨立測試、使用者評論與分析推論各有不同用途。
- 策略、目標客群與創新起點依證據比較，不預設 ST、特定客群或資源導向。
- 保留實際摩擦與負面證據，也不能為湊正反平衡捏造批評。找不到相關回饋時記錄研究缺口。
- 分清現況、公司規劃與研究者建議。情緒評分等分析結果不能包裝成使用者直接提供的數據。
