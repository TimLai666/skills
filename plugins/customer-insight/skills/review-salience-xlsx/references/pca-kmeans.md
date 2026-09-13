# PCA 與 K-means

僅在需要降維或分群時讀取。可執行函式集中於
[`../scripts/salience_analysis.py`](../scripts/salience_analysis.py)，避免報告與程式各維護一套算法。
需要 Python、NumPy 與 scikit-learn；先確認目前環境是否已有，再使用環境允許的安裝方式。

## 輸入與執行

每列是一篇評論，保留 `review_id`、`product` 與各項 `s01`、`s02` 等
0–7 整數評分。`attr_ids`、`attr_labels` 必須與評分欄位同序。
不可依列的位置拼接另一批評論；所有中間資料都保留原始順序與識別碼。

下例適用於同時要求 PCA 與分群的任務。`skill_dir`、`work_dir` 使用實際路徑，
`work_dir` 是本次已選定的工作資料夾；不要預設特定平台目錄。

```python
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(skill_dir) / "scripts"))
from salience_analysis import analyze_salience

work = Path(work_dir)
rows = json.loads((work / "semantic_salience.json").read_text(encoding="utf-8"))
# attr_ids、attr_labels 取自本次已確認的屬性清單。
pca_result, pc_data, result = analyze_salience(rows, attr_ids, attr_labels, k_start=5)
for name, data in (("pca_results.json", pca_result),
                   ("pc_scores.json", pc_data),
                   ("kmeans_enriched.json", result)):
    (work / name).write_text(json.dumps(data, ensure_ascii=False, allow_nan=False), encoding="utf-8")
```

若只要求 PCA，使用 `fit_salience_pca(X)`，回傳評論分數矩陣及 PCA 摘要。
若只要求對既有 PC 分數分群，使用 `cluster_pc_scores(PC)`；其結果按輸入列順序排列，
由呼叫端附回同序的 `review_id`。不要因此重跑原文評分或其他階段。

## PCA 規則

1. 固定值欄位不參與 PCA，零起算的位置記入 `excluded_constant_columns`，輸出負荷量保留原目錄順序並在這些欄位填 0。其餘欄位先用 `StandardScaler` 標準化，再做 PCA。主成分上限為評論數與可用屬性數的較小值，
   因此三篇評論、四項屬性也能執行。
2. 優先保留特徵值大於 1 的主成分（Kaiser）。資料有變化但沒有成分符合時，
   保留第一個有效成分並回報 `selection=first_positive_component_fallback`，不宣稱符合 Kaiser。
3. 只有一篇評論、全部為零或各篇評分完全相同時，無法估計有意義的差異。
   回傳 `status=unavailable`、原因與零個主成分，不製造虛假的解釋率。
4. 檢視各成分中絕對負荷量至少 0.30 的屬性，分別理解正、負方向後再命名。
   負荷量公式保留為主成分係數乘特徵值平方根；它描述本次降維中的關聯方向與強弱，
   不代表因果或滿意程度。

`pca_results.json` 保留 `n_components`、`attr_ids`、`attr_labels`、`loadings`、
`eigenvalues`、`explained_variance_ratio`、`cumulative_variance`、`n_reviews`，
並提供 `status`、`reason` 與可估計時的 `selection`。
`pc_scores.json` 每列保留 `review_id`、`product` 與 `PC01` 等分數。

## K-means 規則

- 使用 PC 分數，不直接改用原始提及評分。起始群數依資料及可解釋性決定，
  `k_start=5` 僅是預設值，上限自動限制為有效列數與不同分數組合數。
- 若比較多個群數，可在 2–9 的可行範圍查看群內平方距離與 silhouette。
  不為湊到五群切出沒有意義的小群，也不只憑最高 silhouette 決定。
- 最低人數固定按原始評論總數計算：`ceil(總數 × 0.05)`。
  移除低於門檻的小群作為後續擬合資料，減少群數並重新擬合，直到保留群都達門檻。
- 若剩下不足兩群，重新擬合單群，不能傳回前一輪含不合格小群的模型。
  若所有列都被暫時排除，恢復全體資料作單群處理。
- 最後用最終模型對**全部評論**重新指派，保留每篇評論的結果，再檢查每群至少佔 5%。
  `active_mask` 僅表示是否參與最後擬合，不表示該評論被刪除。
- 沒有可用主成分或只能形成一群時，所有列仍有 `final_labels=0`，
  但 `status=unsegmented` 明確表示未形成多群，不能命名成成功找到的客群。
- silhouette 只在實際群數介於 2 與評論數減 1 時計算，其他情況留 `null`。
  重新指派後分數可能上升或下降，按實際結果說明，不預設小群都是雜訊。

`kmeans_enriched.json` 保留總數、門檻、每輪 `history`、`final_k`、
`final_silhouette`、`cluster_sizes`、`final_labels`、`pc_centroids`、
`attr_centroids`、`attr_labels`、`review_ids`、`products`，另有
`status`、`reason`、`active_mask`。單群和不足資料也使用同一份輸出結構。

## 解讀與交付

每群說明人數與比例、主要 PC 方向、平均提及分數最高的屬性及產品組成。
根據評論實際談論的內容命名，例如「重視耐用的評論」；沒有個人識別資料時，
這些是評論群，不可把評論篇數當成不重複客戶數，也不推定人口特徵。

高提及分數表示談得明顯，不能推論喜歡、滿意或產品表現好。
回看代表性原文確認命名，並揭露主成分解釋率、單群狀態及資料不足的限制。

## 驗證

```bash
python -m unittest discover -s "<skill_dir>/scripts" -p "test_salience_analysis.py"
```

驗證涵蓋小樣本、完全相同評分、離群小群、正常分群與全列對齊。
