# 資料分析流程（標準規格）

本檔提供 12 步流程的完整規則與門檻值。門檻值為預設值，領域慣例不同時可調整，但任何調整都必須在最終報告中註明。三個關鍵分岔（Gate A/B/C）的判定規則見 SKILL.md 的 Decision Gates。

## Step 0 - 初始化（Initialization）

輸入：dataset、metadata（如果有）。

必做：
1. 讀取資料。先確認編碼（UTF-8 / Big5 / cp950）與分隔符，不要用預設值硬讀。
2. 驗證載入完整性：實際列數是否符合來源宣稱、有沒有整列位移或欄位錯位。
3. 建立資料摘要，輸出：dataset shape、column list、data types。

規則：
- 資料量超出記憶體負荷時，先隨機抽樣（10% 或 10 萬列取小者）完成 Step 1-5，建模前再決定全量或分塊處理。
- 多個資料檔要 join 時，先各自完成 Step 0-2 再 join；join 後必須核對列數變化是否符合預期，多對多 join 會讓列數暴增而不自知。

## Step 1 - 結構檢查（Schema Inspection）

把每個欄位分類為 numeric / categorical / datetime / text / boolean。

判斷規則：
- 數字存成字串（"1,234"、"85%"、"$100"）→ 歸類 numeric，待 Step 3 轉型，不是 text。
- 整數欄但數值無大小意義（郵遞區號、店號、代碼）→ categorical，禁止計算平均。
- 唯一值數 ≈ 列數的欄位 → 標記為 identifier，排除在統計與建模之外。
- 字串欄抽樣 100 筆，可被日期解析的比例 > 95% → datetime。
- categorical 與 text 的分界：唯一值數佔列數 > 50% 且內容為自由文字 → text，否則 categorical。

輸出 schema report，例如：

```yaml
column_summary:
  age: numeric
  gender: categorical
  wage: numeric
  education: numeric
```

## Step 2 - 資料品質檢查（Data Quality Audit）

### Missing values

- 先辨識偽裝缺失：空字串、"N/A"、"unknown"、"-"、0 或 -999 這類 sentinel 值，轉成真缺失後再計算 missing_ratio，否則缺失率會被低估。
- 每欄輸出 missing_ratio；missing_ratio > 30% 的欄位 flag 起來（處理決策見 Step 3 與 Gate A）。
- 檢查缺失是否集中在特定子群（某來源、某時間段）；集中式缺失比隨機缺失危險，會讓子群分析整段失真。

### Duplicate rows

- 分開計算「全列重複」與「主鍵重複」兩種 duplicate_ratio。
- duplicate_ratio > 5% 時，優先懷疑匯入重跑或 join 錯誤，先追資料產生流程，不要直接去重了事。

### Outliers

方法選擇：
- 分佈近似常態 → z-score > 3。
- 偏態明顯（|skewness| > 1）→ IQR 法（低於 Q1 - 1.5×IQR 或高於 Q3 + 1.5×IQR）。
- 不確定時預設 IQR，對極端值較穩健。

輸出 outlier_summary：每欄 outlier 筆數與比例，外加最極端的 5 個值供人工判讀是錯誤還是真實。

## Step 3 - 資料清理（Data Cleaning）

### Missing values 決策樹

- 缺失 < 5%：刪列或簡單補值皆可，擇一執行並記錄。
- 缺失 5% - 30%：補值並新增 missing_flag 欄。numeric 偏態用 median、近似常態可用 mean；categorical 用 mode 或獨立類別 "missing"。
- 缺失 > 30%：預設刪欄。例外：缺失模式本身可能有資訊（MNAR，例如「未填收入」與違約行為相關）→ 保留 missing_flag 當特徵，原始欄可刪。
- 補值前先判斷缺失機制：MCAR（完全隨機）、MAR（與其他欄相關）、MNAR（與自身值相關）。MNAR 用中位數硬補會扭曲分佈，優先保留 flag。

### Outliers

第一步永遠是判斷「資料錯誤」還是「真實極端」：
- 資料錯誤（負年齡、未來日期、超出物理範圍）→ 修正或刪除。
- 真實極端（高消費 VIP、災難月份）→ 預設保留。只有在模型對極端敏感（線性模型、距離類）且極端值不是分析重點時，才 winsorize（截到 1% / 99% 分位）。
- 刪除比例 > 2% 時停下重新檢視：可能不是 outlier，而是雙峰分佈或未辨識的子群體。

### Type correction

string → datetime、string → numeric（去除千分位逗號、貨幣符號、百分比）、string → categorical。轉換失敗的值要列出來人工判讀，不得靜默轉成缺失。

### 清理紀錄（必要）

每個清理動作記錄三件事：套用的規則、影響筆數、代表性前後對照。沒有 cleaning_log 的 clean_dataset 視為不合格交付。

輸出：clean_dataset + cleaning_log。

## Step 4 - 探索式分析（EDA）

### 單變量統計

所有 numeric 欄位計算：mean、median、std、min、max、skewness、kurtosis。
- |skewness| > 1 → 標記偏態，Step 7 考慮 log transform。
- mean 與 median 差距大 → 分佈被長尾拉動，報告描述典型值時用 median。

### 分布圖

每個關鍵 numeric 欄位至少 histogram + boxplot。圖很多時只挑「有異常或影響結論」的 3-5 張進 eda_report，其餘留在 visualization_set。

### 類別統計

- categorical 欄位計算 frequency 與 proportion；基數 > 20 時只列 top 10 + "others" 合計。
- 最大類別佔比 > 95% 的欄位 → 近似常數，標記為低資訊欄位，建模時考慮剔除。

### 異常清單

把雙峰、斷點、異常尖峰、與常識不符的值域寫成文字清單，每條一句話。這份清單必須流進 Step 12 的報告，不能只留在分析過程。

輸出：eda_report（統計表 + 異常清單 + 3-5 張關鍵圖 + 每張圖一句文字發現）。

## Step 5 - 關係探索（Relationship Analysis）

### Numeric vs Numeric

- correlation matrix：分佈偏態或含 outlier 用 Spearman，否則 Pearson。
- |r| > 0.9 → 共線性警告，建模前兩者擇一保留（留業務上較可解釋的那個）。
- scatter plots 只畫與目標變數相關性最高的前 5 組，不全畫。

### Categorical vs Numeric

- group mean + 檢定：兩組用 t-test，三組以上用 ANOVA。
- p 值與效果量一起報：樣本大時 p 值很小，但組間差異可能毫無商業意義。

### Categorical vs Categorical

- contingency table + chi-square。
- 期望次數 < 5 的格子超過 20% 時，改 Fisher exact test 或先合併稀疏類別。

輸出：relationship_report（高相關對、顯著關係、共線性警告清單）。

## Step 6 - 任務判定（Task Identification）

判斷順序：
1. 先問任務目標（對應 Gate B）：
   - 描述現況、回答「發生了什麼」→ 不建模，跳過 Step 7-9，由 Step 5 直接進 Step 10。
   - 量化影響、回答「為什麼」→ 迴歸或統計檢定即可，不一定要 ML。
   - 預測未來、對個體打分排序 → 進建模流程。
2. 再看 target：存在且 numeric → regression；categorical → classification；無 target → clustering / segmentation。
3. 檢查資料量下限：分類任務每類 < 50 筆，或總樣本 < 特徵數的 10-20 倍 → 降級為描述統計 + 檢定，不硬建模。

輸出：analysis_task（任務型別 + 目標變數 + 主評估指標，三者都要定下來）。

## Step 7 - 特徵工程（Feature Engineering）

順序鐵則：先做 train/test split，再做任何需要 fit 的轉換（補值統計量、標準化、encoding）。所有轉換只 fit 在 train set，再 transform 到 test set。違反此順序即 data leakage。

可建立的特徵：
- log transform：|skewness| > 1 的 numeric 欄。
- ratios 與 interaction：income_per_person、purchase_frequency 這類業務比率。
- date features：年、月、星期、是否假日、距今天數、距上次事件天數。

### 類別編碼選擇規則

- 基數 < 10 → one-hot encoding。
- 基數 10 - 50 → frequency encoding 或 target encoding；target encoding 必須只用 train fold 的統計量（建議 CV 內編碼），否則就是 leakage。
- 基數 > 50 → 先依業務邏輯合併類別，或用 frequency encoding；樹模型可直接 label encoding。
- 有自然順序（低/中/高、S/M/L）→ ordinal encoding，順序自己指定，不能交給字母排序。

### 標準化

線性模型、SVM、KMeans、KNN 等距離敏感模型需要 standardization；樹模型（RandomForest、GradientBoosting、XGBoost）不需要。

輸出：feature_dataset。

## Step 8 - 建模（Modeling）

### Train/test split 規則

- 預設 80/20 隨機切分；classification 一律用 stratified split 維持類別比例。
- 時序資料例外：禁止 shuffle，一律時間切分（前段訓練、後段測試）；交叉驗證改用 rolling 或 expanding window。
- 同一實體多筆資料（同客戶多筆交易、同病患多次就診）→ group split，同一實體不得同時出現在 train 與 test。
- 總樣本 < 1000 → 用 k-fold CV（k = 5 或 10）取代單次 split。

### Baseline（必建，Gate C 的比較基準）

- Regression → 全部預測 train 的 mean 或 median。
- Classification → 全部預測多數類（majority class）。
- 時序預測 → 預測值 = 前一期實際值（naive forecast）。

### 候選模型

- Regression：OLS、Ridge、RandomForest、GradientBoosting。
- Classification：Logistic、RandomForest、XGBoost、SVM。
- Clustering：KMeans、Hierarchical、DBSCAN。

規則：
- 從最簡單的模型開始。複雜模型的主指標若沒有明顯優於簡單模型（改善 < 2-5%），交付簡單模型。
- 調參只能用 validation set 或 CV；test set 全程只能在最後評估時使用一次。

## Step 9 - 模型評估（Evaluation）

### Regression

R²、RMSE、MAE，外加殘差圖：檢查殘差是否隨預測值放大（異方差）、是否有系統性彎曲（漏掉非線性關係）。

### Classification

- 類別平衡時：accuracy + F1。
- 不平衡（少數類 < 20%）時：以 macro-F1、AUC-PR、per-class recall 為主，accuracy 只能當參考。
- confusion matrix 必附，並換算成業務語言（漏抓幾個、誤殺幾個）。

### Clustering

- silhouette score：> 0.5 結構清楚；0.25 - 0.5 弱結構；< 0.25 很可能沒有自然分群，要誠實回報。
- cluster size distribution：某群 < 5% 或某群 > 80% → 重新檢討 k 值或改用 DBSCAN。

### 交付判斷（對應 Gate C）

- 主指標未明確優於 baseline → 不交付模型，改交付「現有特徵對目標解釋力不足」的發現與資料補強建議。
- train 與 test 指標差距懸殊（如 train R² 0.95 / test 0.40）→ 過擬合，回 Step 7/8 簡化模型或修特徵。

輸出：model_performance（所有候選模型 + baseline 同表對比）。

## Step 10 - 解釋與洞察（Insight Extraction）

每條洞察的固定形狀：「變數 X 越…，Y 傾向…（相關性，非因果）→ 業務上代表…，建議…」。

規則：
- feature importance 與 correlation 都不是因果證據；要主張因果需要實驗設計或因果推論方法，報告措辭必須區分「相關」與「導致」。
- 洞察 3-7 條為宜，每條都要能指回對應的證據（某張圖、某個指標）。
- 與業務常識矛盾的發現不要蓋掉：先檢查是否為資料問題，查無誤則如實呈現並標注。

輸出：insight_summary。

## Step 11 - 視覺化（Visualization）

必備圖表：distribution plots（關鍵變數）、correlation heatmap、feature importance（有建模時）、model diagnostics（classification → confusion matrix；regression → 殘差圖）。

規則：
- 每張圖必有標題、軸標籤與單位、一句話結論。
- bar chart 的 y 軸從 0 開始；比較圖要有基準線。
- 一張圖只講一件事，塞兩個以上訊息就拆圖。

輸出：visualization_set。

## Step 12 - 最終報告（Report Generation）

固定結構與順序：
1. 結論先行：第一段直接給答案、關鍵數字與信心程度，讀者只看這段也能行動。
2. 資料概況與品質：資料範圍、清理決策摘要（引用 cleaning_log）、帶病分析項目。
3. 方法：EDA 重點、任務型別、模型與 split 方式。
4. 結果：指標表（含 baseline 對比）、關鍵圖表。
5. 限制：資料品質問題、假設、不可外推的範圍。
6. 建議與下一步。

規則：
- Step 2-5 的重要發現必須出現在報告中，不能只留在分析過程。
- 限制段不可省略；Gate A 標注過的帶病項目在此逐條列出，並註明對結論的影響方向。

輸出：analysis_report。

---

# 簡化版流程

最核心的流程只有六步：Load Data → Inspect Schema → Clean Data → EDA → Model → Interpret Results。

即使走簡化版，仍要遵守三件事：清理動作要記錄、split 先於特徵工程、模型贏過 baseline 才交付。

