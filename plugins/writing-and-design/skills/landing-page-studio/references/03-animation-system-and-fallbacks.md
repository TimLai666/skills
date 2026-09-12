# Animation System and Fallbacks

> 動效與效能底線依 design-studio 的 `shared/guardrails.md`（只動 transform/opacity、reduced-motion 強制、blur/grain 限制）。本檔管 LP 的動畫分層與失效處理。

## Required Animation Categories

預設高動畫，至少覆蓋下列四類；使用者選擇減少動態時保留可讀的靜態內容：

1. Hero 動畫
2. 區塊進場動畫
3. 互動動畫（CTA/卡片/游標）
4. 背景層動畫

## Recommended Libraries

- GSAP: 時序控制、ScrollTrigger 類效果
- Anime.js: 輕量數值補間、SVG 路徑動畫
- Three.js: WebGL 粒子/幾何（可選）
- CSS Native: fallback 與低功耗模式

## 動畫選擇參考

下表是主動選擇效果強度時的參考，不是失效後自動切換的順序。高動畫維持預設；未達效能要求先優化實作，變更已約定效果須取得同意。

| Scenario | WebGL Layer | Hero Motion | Scroll Motion | Interaction Motion |
| --- | --- | --- | --- | --- |
| High capability | Three.js enabled | SVG + shader-like overlay | Stagger + parallax | Magnetic + beam + tilt |
| Mid capability | Optional | SVG-only | Stagger only | Tilt + subtle glow |
| Low capability | Disabled | Static gradient + tiny float | Fade-in only | Color/opacity transitions |
| prefers-reduced-motion | Disabled | Static hero | No scroll animation | No magnetic/tilt |

## Detection Rules

1. `prefers-reduced-motion: reduce` -> 停止循環、進場與指標動效，保留靜態內容；載入時與偏好切換時都要生效
2. 無 WebGL context、初始化失敗或 context 遺失 -> 停止失效效果，顯示可見錯誤並記錄受影響功能，不自動換成 SVG／CSS
3. `animation_level=low` -> 停用高刺激動畫
4. 行動裝置 -> 預設降低粒子密度與陰影層數

## Animation Manifest Schema

```json
{
  "animation_manifest": [
    {
      "id": "hero_webgl_layer",
      "category": "hero",
      "library": "three",
      "target": "#hero-canvas",
      "trigger": "on-load",
      "fallback": "report-error"
    }
  ]
}
```

腳本輸出是 `status: planned` 的 starter 計畫，包含效果強度及待核對說明。交付前按實際 DOM／元件核對 target、trigger 與 fallback；效果改了，清單也要更新。reduced motion 時所有效果強度為 0、trigger 為 none，不把計畫當成實測結果。

## Guardrails

- 不可讓動畫壓過主訊息可讀性
- 不可因動畫導致 CTA 可點擊區域不穩定
- 動畫依賴或 CDN 載入失敗時顯示錯誤、保留可讀內容與 CTA；修復後重新驗證，不能把失效頁面視為完成。
- `fallback: report-error` 表示明確報錯而非替代效果；reduced motion 的靜態呈現是使用者偏好，不是工具故障。
