# Dynamic Item Generation And Scoring

## Purpose

把評論中的重複訊號萃取成一組共用評分題項，讓每次分析都能對應當次語料，而不是被固定 rubric 綁死。

前置條件：
- 已完成逐條語意解析
- 已完成四理論必經映射
- 已完成初步主題整合

## Generation Flow

### Step 1: Extract Candidate Items

從整批評論抓出高重複、高辨識度的評價面向，例如：
- 回覆快
- 安裝容易
- 品質不穩
- 價格值得

## Step 2: Normalize

合併同義詞與近似概念，例如：
- 回覆快 / 客服快 / 溝通迅速 -> `response_speed`
- 值得 / CP 值高 / 價格合理 -> `value_for_money`

## Step 3: Define Shared Items

每個題項至少要有：
- `label`
- `definition`
- `parent_theme`
- `evidence_cues`
- `status`

`status` 規則：
- `core`: 由重複評論支撐，可納入主分數集
- `exploratory`: 僅低頻出現，保留觀察但不作核心比較

## Step 4: Score Each Review

用同一組題項回頭評分每則評論，分數為 `0-7`：
- `0`: 沒提到或沒有足夠證據
- `1-3`: 間接、輕微或模糊提及
- `4`: 中立、保留或正反混雜
- `5-6`: 明確提及
- `7`: 強烈且完整表達

## Item Quality Rules

- 題項必須來自整批語料，不可單篇即興生成
- 同一分析範圍只能有一組共享題項 taxonomy
- 題項命名必須可比較，不可過長或過於口語
- 單一孤立訊號只能標成 `exploratory`
- 不可為了表格完整而補造題項

## Recommended Aggregates

每個題項可匯總：
- `coverage`
- `avg_score`
- `high_score_rate`
- `low_score_rate`
- `sample_quotes`

## Example Output

```json
[
  {
    "label": "response_speed",
    "definition": "顧客對回覆或支援速度的評價",
    "parent_theme": "service_experience",
    "evidence_cues": ["回很快", "秒回", "等很久"],
    "status": "core"
  }
]
```
