---
name: data-analysis-workflow
description: >-
  This skill MUST be used when planning or executing an end-to-end data analysis
  or when explicitly asked for 資料分析流程、分析規劃、分析報告產出.
  It SHOULD guide methodological choices in multi-step analysis, including
  descriptive analysis, inference, prediction, or clustering. It MUST NOT force
  modeling into descriptive work or expand a single metric query into a full workflow.
metadata:
  version: "1.2.0"
---

# Data Analysis Workflow

## Overview

協助模型判斷分析方法與完成條件，避免固定流程改變資料或偏離問題。一般資料操作、統計公式與工具用法由模型及工具文件處理。

## Input Contract

先確認要回答的問題、資料來源、觀測單位，以及需要交付的結果。能從上下文判斷就直接使用，只有缺少會影響方法的資訊時才詢問。沒有資料時可規劃分析，不能產生實際分析結論。

## Workflow

1. 先了解問題與資料。確認欄位含義、單位、樣本涵蓋範圍及缺值，區分零、未觀察與不適用。重複紀錄可能是重複觀測，不能只因內容相同就刪除。
2. 先做探索性資料分析，再決定方法。檢視資料分布與缺值，數值欄位通常查看平均數、中位數、標準差、四分位數與範圍，必要時查看偏度、峰度及分布圖。類別欄位查看次數與比例，時間資料查看趨勢。依欄位意義選擇摘要，不對識別碼等數字計算無意義的統計。
3. 結合原本想回答的問題與探索結果，確認資料能支持哪些分析，再選擇比較、推論、預測或分群等方法。問題尚未明確時，可由探索提出可研究的方向。只執行需要的分析，沒有預測目標不等於需要分群。

探索與後續分析遵守以下原則：
- 清理前判斷缺值與極端值的原因。保留原始資料，記錄處理方法、影響筆數與理由。必要時比較不同合理處理方式是否改變結論。
- 做模型評估時，先依時間、個體或群組關係安排訓練與測試資料。用來選方法或特徵的探索只使用訓練資料，避免看過測試結果後調整方法。補值、標準化、特徵選擇與調參只能從訓練資料學習，交叉驗證時每一折各自處理。測試資料保留作最後評估。
- 統計比較先檢查方法假設、樣本量與觀測是否獨立。區分事先提出的問題與探索後發現的關係，報告效果大小與不確定性，不只報顯著與否。
- 結論依資料能支持的範圍表達。相關性不能單獨證明因果，預測準確也不能證明影響機制。不要固定把研究結果轉成商業建議。

需要判斷驗證方式時，讀 [references/data-analysis-flow.md](references/data-analysis-flow.md)。

## Output Contract

提供問題的答案、資料範圍、關鍵處理與方法、支持結論的結果，以及限制。圖表與中間資料依閱讀或重現需求交付，不固定產生一整套報告檔案。只有做了模型才提供模型評估結果。

## Quality Rules

完成條件是約定問題已有可核對的答案，或已確認資料不足並交代缺口。以實際資料與執行結果驗證，不用完成了多少步驟代替。保留重現必要的來源、程式與方法設定，避免未使用的額外分析延長任務。
