# Use Cases And Prompts

## 1) 通用行銷策略

### Use Case

當使用者想把某個 campaign、頁面或活動用 S-O-R 重新拆解時。

### Prompt

`請用 $sor-marketing-strategy 分析這個 campaign 的 Stimulus、Organism、Response，並產出可執行的策略與 KPI ladder。`

## 2) 電商轉換

### Use Case

當使用者有流量與點擊，但下單率低，想知道問題卡在價值、信任還是摩擦。

### Prompt

`我們的商品頁有流量但轉換差，請用 $sor-marketing-strategy 判斷刺激設計、心理機制與轉換阻力，並提出實驗計畫。`

### Output Focus

- `sor_map`
- `strategy_actions`
- `experiment_plan`

## 3) 會員 CRM / 回購

### Use Case

當使用者想提升會員回購、續約或再啟動。

### Prompt

`請用 $sor-marketing-strategy 幫我設計會員 CRM 策略，目標是提高回購。要同時分析被重視感與被打擾風險，並列出 KPI 與 guardrail。`

### Output Focus

- `organism` 需同時寫 relevance 與 intrusiveness
- `response` 主目標為 `repurchase`
- `guardrail` 必須含退訂或靜音風險

## 4) 品牌活動 / 聲量

### Use Case

當使用者有曝光與聲量，但不知道為什麼沒有更深層的 engagement 或 conversion。

### Prompt

`這個品牌活動有很多曝光，但沒帶動轉換。請用 $sor-marketing-strategy 拆解聲量、情緒、信任與行動之間的斷點。`

## 5) 文案前置策略

### Use Case

當使用者真正想要的是文案，但還沒想清楚心理機制、主張角度與 CTA 策略。

### Prompt

`先不要直接寫文案。請用 $sor-marketing-strategy 產出 message strategy brief，再說明哪些部分應交給 $copywriting。`

### Handoff Rule

- 先輸出：
  - `core_tension`
  - `message_angles`
  - `proof_points`
  - `cta_directions`
- 再建議用 `$copywriting` 成稿
