---
name: brand-strategy-system
description: Use when designing or diagnosing brand strategy with positioning theory (Ries & Trout), Keller CBBE pyramid, Aaker brand identity, 12 brand archetypes, voice charter, and SCCT crisis communication. Trigger on brand positioning, brand equity audit, brand voice, brand archetype, crisis response, 品牌定位、品牌策略、品牌識別、品牌原型、品牌聲音、品牌資產、品牌健檢、rebranding、品牌重塑、品牌診斷、品牌危機、公關危機.
---

# Brand Strategy System 品牌策略系統

## Overview

以四個可切換的模式，做品牌策略的「設計與診斷」：定位設計、品牌資產健檢、聲音與人格、危機回應。每個模式有獨立的輸入需求、工作流程與固定輸出格式。

理論基礎：Ries & Trout 定位理論與定位聲明公式、Keller CBBE 品牌資產金字塔、Aaker 品牌識別系統、Mark & Pearson 12 品牌原型、品牌聲音憲章、Coombs SCCT 情境危機溝通理論。

## 分工邊界

- 本 skill 負責「品牌策略設計與診斷」：產出定位聲明、健檢報告、voice charter、危機回應方案。
- `theory-analysis-product-positioning`：用定位理論「編碼分析證據」（訪談、評論、工單等原始資料）。手上是原始證據要先分析時轉交該 skill；其輸出的 `theory_annotations` 可作為本 skill positioning 模式的輸入。
- 行銷訊息層（`sor-marketing-strategy`、`psychological-trigger-marketing`、`maslow-five-needs-marketing`）：策略定案後的訊息設計與活動企劃。本 skill 的 positioning statement 與 voice charter 是它們的上游輸入。
- 內容產製層（`threads-viral-growth`、`content-growth-studio`）：成稿與貼文。不在本 skill 範圍。

Do not use：

- 使用者只要單篇文案、貼文或活動企劃，沒有策略設計或診斷需求。
- 使用者手上是原始評論 / 訪談資料要做編碼分析（轉 `theory-analysis-product-positioning` 或 `review-mining-stp`）。
- 純視覺識別需求（logo、色彩、版式）——本 skill 產出的是策略層定義，不做視覺設計。

## Mode Routing

依序判斷，命中即停：

1. **crisis** — 有進行中或迫近的負面事件（事故、爆料、客訴擴散、負評潮、媒體追問）。危機當下不做定位重談，先處理危機。
2. **positioning** — 新品牌、新產品線、進新市場，或明確要求重定位 / rebranding。
3. **equity-audit** — 品牌已存在，症狀是「不知道哪裡出問題」「品牌老化 / 形象模糊」「銷售疲軟但不確定是不是品牌問題」「要健檢」。
4. **voice** — 定位已確立，需要人格、原型、語氣、voice charter、跨通路語氣一致性。

補充規則：

- 模糊時優先序：crisis > equity-audit > positioning > voice（先診斷再開藥）。
- rebranding 請求 = 壓縮版 equity-audit + positioning：先驗證「現有定位真的失效」再重定位，不可直接跳到新定位。
- 使用者只丟一句「幫我做品牌策略」時，先問品牌是否已存在、目前最痛的症狀，再路由。

## Input Contract

共同必填：

- `brand_name`
- `category_context` — 產業、品類、主要競爭者
- `target_audience` — 目標客群描述

依模式加填：

- **positioning**：可驗證的產品事實與優勢（RTB 候選）、主要競爭者的定位主張；重定位另需「現有定位與其失效證據」
- **equity-audit**：品牌現況資料至少一類（知名度數據 / 顧客評價 / 回購率 / NPS / 社群數據，或可安排訪談的內部與顧客名單）
- **voice**：已確立的定位聲明或核心價值、現有溝通樣本 3 份以上（貼文 / 文案 / 客服回覆）
- **crisis**：事件描述、已知事實 vs 未知事項、擴散狀態（是否已被報導 / 轉發）、品牌過去是否發生過同類事件

## Data Sufficiency Gate

缺必填欄位時回傳 `MissingDataOutput`，不硬做：

```json
{
  "mode": "",
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "next_step_rule": "補齊必填欄位後再產出完整結果"
}
```

例外規則：

- crisis 模式在事件進行中允許用「已知 / 未知」框架先產出首發聲明骨架，不得以資料不齊為由延遲回應。但責任歸因判斷仍為必經步驟。
- positioning 模式若完全沒有 RTB 候選，不得產出定位聲明，只能輸出「RTB 缺口清單」要求補件。

## Workflow

四模式主幹（各步驟細節在對應 reference）：

- **positioning**：讀 [references/01-positioning.md](./references/01-positioning.md) → 品類框架選擇（既有品類 vs 創新品類）→ POP 盤點確認入場券 → POD 候選過三準則 → 填定位聲明公式 → 四關測試 → 重定位時加跑風險檢查 → 輸出。
- **equity-audit**：讀 [references/02-cbbe-and-identity.md](./references/02-cbbe-and-identity.md) → CBBE 四層由下而上逐層量測判讀 → 鎖定卡關層 → Aaker 四視角識別盤點 → identity vs image 落差分析 → 介入建議按優先序輸出。
- **voice**：讀 [references/03-archetypes-and-voice.md](./references/03-archetypes-and-voice.md) → 四動機軸定位客群渴望 → 原型選擇三因子論證 → voice charter（形容詞 + this-but-not-that + do/don't）→ 跨通路語氣調節表。
- **crisis**：讀 [references/04-crisis-scct.md](./references/04-crisis-scct.md) → 責任歸因分類（victim / accidental / preventable）→ 修正因子調整 → 回應策略矩陣選擇 → 首發聲明四段式模板 → 升級判斷 → 危機後修復路徑。

模式串接規則：

- equity-audit 發現卡關層在 salience 或 judgments 且根因是定位模糊 → 建議串 positioning 模式，不直接開溝通處方。
- positioning 完成後，若使用者要落地溝通 → 串 voice 模式產 charter，再轉交行銷訊息層 skills。
- crisis 收尾進入修復路徑時 → 建議三至六個月後跑 equity-audit 驗證 judgments 層回復程度。
- voice 模式若發現定位聲明根本不存在或內部說法分歧 → 退回 positioning，不硬做 charter。

## Output Contract

依模式輸出固定段落，繁體中文 Markdown。結構如下：

**positioning**：

```json
{
  "positioning_statement": "完整公式 + 逐欄位理由",
  "pop_pod_table": "POP 達標狀態 + POD 三準則檢核",
  "four_test_results": "四關逐關過/不過 + 證據",
  "alternatives_rejected": "被淘汰的定位方向與理由",
  "migration_risk": "重定位時必填：流失評估 + 過渡設計"
}
```

**equity-audit**：

```json
{
  "cbbe_scorecard": "四層各標 健康/偏弱/卡關 + 證據或「需補測」",
  "bottleneck_layer": "單一主要卡關層 + 判定依據",
  "identity_audit": "Aaker 四視角盤點 + core/extended 區分",
  "gap_analysis": "落差類型：溝通落差/體驗落差/認知時滯",
  "intervention_plan": "按優先序，每項含量測指標與回測時點"
}
```

**voice**：

```json
{
  "archetype_choice": "主原型 + 副原型（至多一）+ 三因子論證",
  "voice_charter": "3-4 形容詞，各附 this-but-not-that + do/don't 例句",
  "channel_modulation_table": "各通路的正式度與滑桿設定"
}
```

**crisis**：

```json
{
  "attribution_classification": "cluster 判定 + 修正因子調整結果",
  "response_strategy": "主策略 + 可搭配策略 + 誤用警告",
  "first_statement_draft": "已知/未知/正在做/何時更新 四段式",
  "escalation_triggers": "升級為聲明 / CEO 出面的觸發條件",
  "recovery_path": "承諾兌現 → 靜默修復 → 重新敘事 + 時機判準"
}
```

## Quality Rules

- 定位聲明必過四關測試（顧客在乎嗎 / 做得到嗎 / 對手難抄嗎 / 能撐五年嗎）。任一關不過，必須標明並提供替代方向，不得帶病輸出。
- POD 主張前必先確認 POP 達標。未達品類入場券水準的品牌，介入建議不得以差異化溝通為主軸。
- 原型選擇不可與品類第一名的原型重複，除非能明確論證執行差異或市場區隔理由，並寫進 `archetype_choice`。
- 危機回應必先完成責任歸因判斷才能選策略，不得跳過歸因直接寫聲明。preventable cluster 禁用 deny 策略。
- 所有量測指標標明「有數據」或「需補測」，不得假造基準值或編造調查結果。
- equity-audit 結論必須指向單一主要卡關層。四層都列問題卻不排序，視為未完成診斷。
- 每個模式的建議都要附「這個判斷在什麼條件下會是錯的」，讓使用者知道何時該重新評估。

## Common Mistakes

- 把定位聲明寫成 slogan 或 tagline。定位聲明是內部戰略文件，用來對齊所有決策，不是對外文案。
- POD 選了 desirable 但 not deliverable 的主張——顧客在乎，但品牌根本做不到或撐不久。
- 原型只因「聽起來厲害」選 Hero 或 Magician，忽略組織真實性格，執行時穿幫。
- 危機時先寫道歉稿再回頭想歸因，導致 victim cluster 事件過度道歉、自認全責。
- equity-audit 只看知名度數據就下結論。salience 高不代表 resonance 存在，知名不等於健康。
- voice charter 只列形容詞不做 this-but-not-that 界定，落地時每個小編各自解讀。
- 重定位時只算新客獲取，不算既有顧客流失，上線後才發現核心營收客群被新定位排斥。

## Suggested Prompts

- `請用 $brand-strategy-system 幫這個新品牌做定位，我有產品資料和競品清單。`
- `品牌感覺老化了但說不出哪裡有問題，請用 $brand-strategy-system 做一次品牌健檢。`
- `定位已經確定，請用 $brand-strategy-system 幫我選品牌原型並產出 voice charter。`
- `我們出事了，請用 $brand-strategy-system 判斷責任歸因並給首發聲明。`
