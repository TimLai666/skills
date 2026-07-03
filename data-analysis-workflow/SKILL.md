---
name: data-analysis-workflow
description: Use when planning or executing a full data analysis workflow, including schema inspection, data quality audit, data cleaning, EDA, relationship analysis, feature engineering, modeling, evaluation, and report generation. Trigger on requests like 資料分析流程, EDA 到建模, 數據分析規劃, 分析報告產出, or end-to-end analytics workflow.
---

# Data Analysis Workflow

## Overview

把資料分析任務拆成可重複執行的 12 個步驟，從初始化到最終報告。每一步都有明確的進入條件、退出條件與決策門檻，確保分析完整、可追蹤、可交付、可重現。工具中立，pandas、SQL 或其他堆疊皆可套用。

## Use This Skill

Use when:
- 需要從原始資料一路做完 EDA、建模、評估與洞察。
- 需要把分析任務標準化成固定步驟與輸出物。
- 需要先做分析流程規劃，再開始實作。

Do not use when:
- 只要回答單一指標或一次性查詢，沒有完整分析流程需求。
- 任務僅限資料擷取或單純視覺化，不包含方法論流程。

## Execution Order (Step 0-12)

每步驟三欄：進入條件（何時可開始）、退出條件（做到什麼程度才能進下一步）、最常見陷阱。詳細規則與門檻值見 [references/data-analysis-flow.md](./references/data-analysis-flow.md)。

### Step 0: Initialization
- 進入：拿到 dataset（與 metadata，如果有）。
- 退出：資料成功載入且驗證過完整性，取得 shape、column list、dtypes。
- 陷阱：沒確認編碼與分隔符就硬讀，欄位被切錯而不自知。

### Step 1: Schema Inspection
- 進入：Step 0 完成。
- 退出：每個欄位分類為 numeric / categorical / datetime / text / boolean，產出 schema_report。
- 陷阱：把存成字串的數字或日期當 text，後續統計全部失真。

### Step 2: Data Quality Audit
- 進入：schema_report 完成。
- 退出：每欄 missing_ratio、整體 duplicate_ratio、outlier_summary 全部量化列表。
- 陷阱：只看整體缺失率，漏掉單一關鍵欄位缺失 40% 的事實。

### Step 3: Data Cleaning
- 進入：品質問題已量化，且已依 Gate A 決定清理深度。
- 退出：clean_dataset 產出，每個清理動作（規則、影響筆數）都有紀錄。
- 陷阱：清理動作沒記錄，結果不可重現，也回答不了「為什麼少了 300 筆」。

### Step 4: EDA
- 進入：clean_dataset 存在。
- 退出：numeric 欄位有分佈統計與圖、categorical 有頻率表，異常與偏態已標記，產出 eda_report。
- 陷阱：畫了 30 張圖卻沒有一句文字結論，圖表淪為裝飾。

### Step 5: Relationship Analysis
- 進入：eda_report 完成。
- 退出：變數關係已檢查（correlation / ANOVA / chi-square），高相關與共線性已標記。
- 陷阱：把相關直接寫成因果放進發現。

### Step 6: Task Identification
- 進入：關係分析完成，已理解資料能支撐什麼問題。
- 退出：依 Gate B 判定 regression / classification / clustering / 只需描述統計，並定下目標變數與主評估指標。
- 陷阱：預設一定要建模，沒確認任務目標其實描述統計就夠。

### Step 7: Feature Engineering
- 進入：Gate B 判定需要建模。
- 退出：feature_dataset 產出，所有需要 fit 的轉換（補值、標準化、encoding）都只 fit 在 train set。
- 陷阱：先做特徵工程再 split，造成 data leakage。

### Step 8: Modeling
- 進入：feature_dataset 與 train/test split 完成，naive baseline 已建立。
- 退出：至少 2-3 個候選模型訓練完成，可與 baseline 同表比較。
- 陷阱：時序資料用隨機 split，等於用未來預測過去。

### Step 9: Evaluation
- 進入：候選模型全部訓練完成。
- 退出：指標表（含 baseline 對比）完成，通過 Gate C 判定可否交付，產出 model_performance。
- 陷阱：類別不平衡下只報 accuracy，95% 準確率其實等於全猜多數類。

### Step 10: Insight Extraction
- 進入：模型評估完成（或 Gate B 判定不建模，由 Step 5 直接進入）。
- 退出：重要變數、影響方向、商業意義各自成句，產出 insight_summary。
- 陷阱：只列 feature importance 數字，沒翻譯成業務語言與可行動建議。

### Step 11: Visualization
- 進入：洞察確定，知道要支撐哪些結論。
- 退出：每個關鍵結論都有一張對應圖表，圖有標題、單位與一句話結論。
- 陷阱：為了視覺效果截斷 y 軸或省略基準線，誤導讀者。

### Step 12: Report Generation
- 進入：所有中間產物就緒。
- 退出：analysis_report 完成，結論先行、方法可重現、限制誠實列出。
- 陷阱：EDA 與品質檢查的重要發現沒進報告，讀者不知道結論建立在多少帶病假設上。

## Decision Gates

三個關鍵分岔，到達時必須明確判定再往下走，不得默默通過。

### Gate A: 資料品質——停下清理 vs 標注後帶病分析（Step 2 → 3）

缺失率（逐欄判斷）：
- < 5%：刪列或簡單補值即可，不需停。
- 5% - 30%：補值並加 missing_flag，分析照常，但報告限制段必須標注。
- > 30%：停下判斷。選項：刪欄、把缺失本身當特徵（可能是 MNAR 訊號）、回頭確認資料源。不得默默補值後當正常欄位用。

重複率：
- < 1%：直接去重，記錄筆數。
- 1% - 5%：先確認是否真重複（同 ID 不同時間戳可能是合法事件），確認後去重。
- > 5%：停下。高機率是匯入重跑或 join 錯誤，先追資料產生流程，修不了才去重續行。

帶病分析規則：時程不允許回頭修資料時可以繼續，但每個未修復問題必須寫進 analysis_report 的限制段，並註明對結論的影響方向（高估／低估／不確定）。

### Gate B: 需要建模 vs 描述統計就夠（Step 6）

依任務目標判斷，不是依資料長相：
- 目標是「描述現況、回答發生了什麼」→ 描述統計 + EDA + 分組比較就夠，跳過 Step 7-9。
- 目標是「量化某變數的影響、回答為什麼」→ 需要迴歸或統計檢定，不一定需要 ML。
- 目標是「預測未來值、對個體打分排序」→ 需要建模。

資料量下限：分類任務每類至少約 50 筆、或總樣本至少為特徵數的 10-20 倍；達不到就退回描述統計 + 檢定，不硬建模。

### Gate C: 模型表現多差就不交付（Step 9 → 10）

- 必建 naive baseline：regression 用「全預測 train 平均或中位數」（時序用前一期值），classification 用「全猜多數類」。
- 交付規則：主指標必須明確優於 baseline（如 RMSE 更低、macro-F1 更高）。贏不了 baseline → 不交付模型，改交付「現有特徵對目標解釋力不足」這個發現與資料補強建議。
- 過擬合檢查：train 與 test 指標差距懸殊（例如 train R² 0.95、test 0.40）→ 不得交付，回 Step 7/8 簡化模型或修特徵。

## Expected Deliverables

四個必交產物，格式固定：

- `schema_report`：一欄一列的表，含 column、型別分類、missing_ratio、基數（唯一值數）、範例值；附 dataset shape。
- `eda_report`：單變量分佈統計 + 異常清單（outlier、偏態、意外值）+ 3-5 張關鍵圖（只放影響結論的圖）+ 每張圖一句文字發現。
- `model_performance`：所有候選模型與 naive baseline 同表對比的指標表；classification 附 confusion matrix，regression 附殘差圖；註明 split 方式與資料量。
- `analysis_report`：結論先行（第一段直接給答案與信心程度）→ 方法（資料、清理、模型摘要）→ 限制（品質問題、假設、不可外推範圍）→ 建議。

建議同時保留中間產物：`clean_dataset`（附 cleaning_log）、`relationship_report`、`insight_summary`、`visualization_set`。

## Common Mistakes

交付前逐條自查：

- Data leakage：split 之前就做補值、標準化、target encoding，統計量洩漏測試集資訊。正確順序：先 split，轉換只 fit 在 train。
- 類別不平衡只看 accuracy：正類佔 5% 時全猜負類就有 95% accuracy。必看 confusion matrix 與 precision / recall / macro-F1 / AUC。
- 反覆用測試集挑模型：test set 只能在最後看一次，調參與選模用 validation set 或 cross-validation。
- 時序資料隨機 split：訓練集混入未來資料。時序一律用時間切分。
- Outlier 一律刪除：先判斷是資料錯誤（負年齡、未來日期）還是真實極端值；真實極端值（如高價值客戶）可能正是分析重點。
- 清理動作不記錄：刪了哪些列、補了什麼值、影響幾筆都要留紀錄，否則結果不可重現。
- EDA 發現沒進報告：Step 4/5 找到的異常與模式必須反映在 Step 12，不能只留在分析過程。
- 相關寫成因果：correlation 與 feature importance 都不是因果證據，報告措辭必須區分「相關」與「導致」。

## Reference Usage Rule

- 需要完整 12 步規則、門檻值與範例時：讀 `references/data-analysis-flow.md`。
- 只需要快速執行主幹流程時：優先使用該檔案中的「簡化版流程」。
- 需要完整專案交付（含建模與報告）時：依該檔案 Step 0-12 全部規則執行，不可只走簡化版。
