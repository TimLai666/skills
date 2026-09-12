# BCG 事業組合分析報告（Template）

完整分析使用以下內容，可依閱讀需求調整呈現順序。使用者只要求分類或計算時，取第 2 節的分類、依據與邊界欄位，第 6 節座標資料，以及相關門檻與缺口說明。

## 0. 基本資訊
- 集團 / 公司：
- 分析範圍：
- 戰略目標：
- 分析期間：
- 使用門檻：
  - Relative Market Share cut-off：
  - Market Growth cut-off：

## 1. Portfolio Snapshot
- 組合概況：
- 主要現金來源：
- 主要投資黑洞：
- 最大風險：
- 優先動作：

## 2. Unit Classification Table
| 事業體 | 市佔率 | 最大競爭者市佔 | Relative Market Share | Market Growth | 象限 | 判定依據 | 例外/邊界 | 發展潛力 | 可能遷移路徑 | 遷移條件 | 策略姿態 | 資本優先序 |
|---|---:|---:|---:|---:|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |  |

原始市佔資料未提供但已有可用的相對市佔率時，原始欄位註明未提供，不反推或補造數值。分類依據附來源或計法。

## 3. Quadrant Recommendations

### Cash Cows
- 名單：
- 策略：
- 現金運用：

### Stars
- 名單：
- 策略：
- 投資重點：

### Question Marks
- 名單：
- 策略：
- 驗證條件 / 停損條件：

### Dogs
- 名單：
- 策略：
- 保留或退出理由：

## 4. Capital Allocation Actions
- 從哪些單位釋出資金：
- 優先投向哪些單位：
- 哪些單位只做階段式投資：
- 哪些單位應收割 / 出售 / 關閉 / 重定位：

## 5. Portfolio Rebalance Priorities

依決策期限與投資驗證週期安排時程，列出各階段的動作與完成條件。

### 優先執行
- 

### 接續執行
- 

### 後續安排
- 

## 6. Matrix Plot Data

保留以下欄位：`x_axis`、`y_axis`、`quadrant_cutoffs`、`points`；每個可定位單位含 `name`、`x`、`y`、`quadrant`、`borderline`。`x` 是相對市佔率，`y` 是市場成長率百分比數值，與分類表一致。採用本案門檻，缺資料無法定位者另列缺口，不填假座標。

下列為格式示例，Business A 與數值皆為假設，交付時換成本案資料：
```json
{
  "x_axis": "relative_market_share",
  "y_axis": "market_growth_rate",
  "quadrant_cutoffs": {
    "relative_market_share_cutoff": 1.0,
    "market_growth_cutoff": 10.0
  },
  "points": [
    {
      "name": "Business A",
      "x": 1.2,
      "y": 12.5,
      "quadrant": "Stars",
      "borderline": false
    }
  ]
}
```

## 7. Assumptions And Limitations
- 使用的假設：
- 資料缺口：
- BCG 在本案能解釋與可能漏掉的事：
- 還需要哪些更深驗證：

## 8. Follow-ups
- 追蹤期間與檢查時點：
- 要補的資料：
- 要做的實驗或財務驗證：
- 要追的 KPI：
