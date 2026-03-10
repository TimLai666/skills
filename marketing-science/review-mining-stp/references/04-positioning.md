# Positioning

## Purpose

本文件定義評論資料如何轉換為定位評分表、知覺圖與定位診斷。

## LLM Bridge

LLM 介面位於評論探勘與定位分析之間。此步驟的功能為將品牌知覺轉換為可量化的定位基礎分數，供後續定位方法使用。

## Positioning Scorecard

### Columns

- 各競爭品牌
- `理想點`

### Rows

- 屬性功能
- 利益與用途
- 品牌個性與形象

至少涵蓋：

- 包裝美感 / 質感
- 成分或品質
- 口感或性能
- 價格合理
- 提神、功效或用途
- 犒賞自己 / 分享
- 浪漫、品味、歡樂、高貴等品牌形象

## Dynamic Scorecard Summary

此段落必須同時交代：

- 高低分定位基礎
- 理想點相對距離
- 重要性與表現差距
- 信度 / 效度分析

## Perceptual Map Method Rule

- 預設方法：`factor_analysis`
- 僅當輸入資料為品牌相似性或非屬性資料時使用 `MDS`
- 輸出中必須標示 `positioning_method_used`

## Required Diagnostics

- 關鍵因素評估
- 標竿分析
- 理想點分析
- 競爭態勢分析
- `POD / POP`
- 四象限策略矩陣：
  - 訴求重點
  - 改善重點
  - 改變重點
  - 放棄重點

## Required Outputs

- `Positioning Scorecard`
- `Dynamic Scorecard Summary`
- `Perceptual Map Summary`
- `Positioning Diagnostics`
- `Strategy Matrix`
