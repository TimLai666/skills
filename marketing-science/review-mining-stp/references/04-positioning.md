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
- `factor_analysis` 路徑必須輸出 `projection_interpretation`
- `MDS` 路徑若無屬性向量，`projection_interpretation.status` 必須為 `not_available` 並附原因

## Perceptual Map Figure Specification

知覺圖必須以真實散佈圖為基底，不得以純文字、示意圖或摘要替代。

### Factor Analysis Path

- 品牌點 / 理想點座標來源：因素分數
- 屬性向量來源：因素負荷量
- 圖面必須保留品牌點、理想點與屬性向量
- 屬性向量必須由原點 `(0,0)` 出發
- `projection_interpretation` 需說明：
  - 品牌點沿屬性向量投影如何判讀屬性表現
  - 理想點投影如何判讀屬性重要性

### MDS Path

- 品牌點 / 理想點座標來源：MDS 座標
- 若輸入資料不是屬性資料，原則上不得定義屬性向量
- 若無法定義屬性向量，輸出中必須明示 `attribute_vectors_not_defined`
- 若無法定義屬性向量，`projection_interpretation` 必須明示不可定義原因

## Coordinate Table Schema

### Perceptual Map Coordinate Table

- `label`
- `point_type = brand | ideal`
- `x`
- `y`

### Perceptual Map Vector Table

- `label`
- `vector_type = attribute`
- `x_start = 0`
- `y_start = 0`
- `x_end`
- `y_end`
- `x_loading`
- `y_loading`

## Allowed Visual Processing

- 標籤避讓
- 顏色分層
- 理想點特殊符號
- 向量箭頭
- 圖例
- 軸標
- 透明度調整
- 字體調整

## Forbidden Transformations

- 刪除品牌點
- 改變實際座標
- 以示意線替代真實向量
- 將向量起點移離原點
- 在 `MDS` 路徑下偽造屬性向量

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
- `Perceptual Map Figure`
- `Perceptual Map Coordinate Table`
- `Perceptual Map Vector Table`
- `Perceptual Map Method`
- `Perceptual Map Interpretation`
- `projection_interpretation`
- `Positioning Diagnostics`
- `Strategy Matrix`
