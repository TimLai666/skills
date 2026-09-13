# 模型估計與限制

## 先確認反應與分析單位

| 資料 | 模型安排 |
| --- | --- |
| 商品卡評分 | 依評分量尺選線性或序位等模型，處理同一受訪者重複評分 |
| 已知集合內單選 | 條件式選擇模型，集合內比較商品屬性 |
| 真正獨立的二元事件 | 依事件定義考慮二元模型，不能拿展開後的商品列冒充獨立事件 |
| 排序、多選或未知可選集合 | 先安排適合設計，不能套本工具的單選估計 |

附帶工具只實作單選資料，不宣稱支援所有 conjoint 方法。評分模型的預測仍是
評分尺度，不能直接套 logistic 函數解讀為購買機率。

## 選擇資料契約

每筆購買或問卷作答是一個選擇事件，用 `choice_set_id` 識別，顧客識別另存。
同一人可能回答多次。商品 ID 在同一集合內唯一，每組至少兩項可選、恰一項
被選中。可選集合必須包括已選商品，缺值或未知商品 ID 先處理。

`build_stacked_data.py` 展開每個事件，`validate_stacked` 逐組檢查。
提供 `consideration_set_col` 指定每筆紀錄的可選商品清單；沒有該欄時，只有在
研究已採用全商品可選的假設後，才傳 `assume_all_available=True`。
全商品皆可選不能由評論資料自動推論。若需要「不購買」，
在資料與研究設計中明確納入該選項，未觀察到它就不能估計市場不購買率。

## 估計與診斷

`fit_single_model` 使用 statsmodels `ConditionalLogit`，以選擇事件分組，
不加入共同截距。共同截距會在集合內比較時抵消。組內中心化後的設計矩陣
須能區分所選預測欄；原始矩陣滿秩不保證組內可識別。

工具估計時依事件中心化並調整各欄尺度，避免改變單位造成假收斂。
回傳的 `coefficients`、`covariance` 與 `std_errors` 已轉回原始輸入單位，
可與原單位商品表一起計算指標。`model_object` 保留標準化後的資料與參數，
不能把其中的參數直接套回原商品表。

估計前檢查缺值、有限數值、編碼與屬性共變。估計後檢查收斂、警告、
係數與不確定性。未收斂、分離或數值異常時不將結果送往商業指標計算。
收斂只是數值條件，還需依研究目的檢查模型設計、價格混淆、樣本與預測表現。

同一顧客重複選擇需要處理顧客內依賴，不能只靠事件分組就宣稱標準誤適當。
工具的實際推論支援與限制以回傳結果及函式說明為準，未支援的設計需另用
適合的方法。報告分別列顧客數、事件數、商品列數，不以固定列數宣稱樣本足夠。

目前回傳的 `inference` 為 `model_based_independent_choice_events`，
`repeated_customers` 標示是否有同一人多次作答。後者為真時，回傳的標準誤
尚未調整顧客內相關性，WTP 工具會拒絕使用這份不確定性估計。

## 執行工具

Python 環境需有 pandas、numpy、scipy 與 statsmodels。從 skill 的 `scripts/`
目錄匯入下列函式，傳入已載入的商品表 `cards` 與選擇紀錄 `purchases`。
此例假設資料欄位已定義 `quality`（二元）、`price`，以及 `considered_cards`：

```python
from build_stacked_data import build_stacked_data
from fit_logistic_conjoint import fit_single_model, diagnostic_report

stacked = build_stacked_data(cards, purchases, consideration_set_col="considered_cards")
result = fit_single_model(stacked, ["quality", "price"])
print(diagnostic_report(result))
```

`result` 包含具名係數、共變異數、模型與事件數，可交給指標工具。
若需要重現腳本檢查，從 skill 目錄執行
`python -m unittest discover -s scripts/tests -v`。測試使用合成資料，不能替代
使用者資料的研究有效性檢查。

## 無法分辨屬性時

若品牌 A 總是大尺寸、品牌 B 總是小尺寸，資料只支持組合差異。可以改為
有意義的組合比較、補足交叉組合資料，或縮小問題，並交代因此放棄的判斷。
不能將品牌模型與尺寸模型的係數相加，或用另一模型的價格係數計算願付價格。

`fit_split_models` 僅保留分開的探索結果，不回傳合併效用。探索模型不是
「控制其他屬性後的獨立效果」，也不能拿來拼裝完整商品的機率。

## 不確定性與後續使用

保留同一模型的係數、共變異數與估計設定。價格係數不符合預期時，檢查
遺漏屬性、樣本、測量及設計等可能原因，不能斷言只因價格範圍太窄。
不要以固定 p 值區間把不確定結果重新命名為可靠方向。

## 方法依據

- [statsmodels ConditionalLogit](https://www.statsmodels.org/stable/generated/statsmodels.discrete.conditional_models.ConditionalLogit.html)：分組條件概似與截距限制。
- [Train，Logit，第 3 章](https://eml.berkeley.edu/choice2/ch3.pdf)：選擇集合內機率及模型假設。
