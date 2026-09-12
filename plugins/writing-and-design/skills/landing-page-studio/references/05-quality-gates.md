# Quality Gates

> 除本檔數值門檻外，產出同時要通過 design-studio 的 `shared/hard-rules.md`（版面／狀態／內容硬規則）與 `shared/verification.md`（交付前 QA）。

## Performance and Accessibility Thresholds

最低門檻：

1. Desktop
- Performance >= 85
- Accessibility >= 90

2. Mobile
- Performance >= 75
- Accessibility >= 90

## Responsive Gate

必須檢查以下斷點至少一次：

- 390x844 (mobile)
- 768x1024 (tablet)
- 1440x900 (desktop)

要求：

- Hero 文字不可溢出
- CTA 必須在首屏可見（或可快速抵達）
- Navbar 不可遮蔽主內容

## Readability Gate

1. 主標與背景對比需可讀
2. 內文 line length 建議 45-85 字元
3. 重要 CTA 對比需明顯高於次要按鈕

## Motion Gate

1. reduced-motion 模式必須可正常使用
2. 動畫不可阻塞互動
3. 一般進場過渡可用 300–900ms 作參考；互動即時回饋依用途決定，reduced motion 使用靜態切換。

## Autonomy QA Loop

多輪模式下，每輪至少檢查：

- conversion clarity
- visual coherence
- readability
- performance risk

先指出可觀察的問題，再修正受影響部分並重驗。自評不能代替瀏覽器與效能工具的實際結果，不以固定分數或輪數判定完成。

## Failure Handling

新頁面依全部適用門檻驗收；局部修改驗證受影響範圍與是否造成退步，既有且無關的問題回報，不自行擴成整站重做。適用門檻未達時：

1. 回報未達項目
2. 依原因修正效能或相容性問題，保留已約定的動畫；需要改變效果時先取得同意
3. 再輸出修正版與前後差異

## 互動與失效驗證

- 主 CTA 有真實目的地或完成相應互動，不可只連到 `#`。
- 以減少動態模式載入，並在頁面開啟後切換偏好，確認循環、進場與指標動效停止，內容保持可讀。
- 模擬 WebGL 初始化失敗與動畫 CDN 無法載入，確認顯示明確錯誤、沒有自動改用其他動效，且內容與主要行動仍可使用。
- 檢查模板佔位、未證實數字、內部設定文字及實際動畫清單是否已清除或對齊。
- Lighthouse 分數須來自實測；環境無法執行時標為未驗證，不能用示例分數代填。
