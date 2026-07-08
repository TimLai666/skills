# Skill 審查與修改紀錄

> 日期：2026-07-08
> 狀態：已完成

## 修改範圍

以下 10 個 skill

## 衝突處理

| 衝突                                                           | 決定                                                                | 狀態      |
| -------------------------------------------------------------- | ------------------------------------------------------------------- | --------- |
| `mermaid-visualizer` vs 全域 `~/.gemini/config/skills/mermaid` | 保留 repo 版（mermaid-visualizer），全域已刪除                      | ✅ 已解決 |
| `excalidraw-diagram` vs `obsidian-canvas-creator` 觸發詞重疊   | 在 description 中更明確區分，各自明確定義為手繪圖表與 native canvas | ✅ 已解決 |

## 簡體→繁體轉換

| 檔案                               | 狀態                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| `excalidraw-diagram/SKILL.md`      | ✅ 轉換完成，觸發詞與內文改為繁體台灣用語                                     |
| `tutor/SKILL.md`                   | ✅ 轉換完成，韓文殘留與觸發詞改為繁體台灣語系                                 |
| `tutor-setup/SKILL.md`             | ✅ 轉換完成，韓文範例改為繁體中文對照                                         |
| `defuddle/SKILL.md`                | ✅ 純英文，無需修改                                                           |
| `llm-wiki/SKILL.md`                | ✅ 已微調觸發器，以確保使用者要求新建立 Obsidian 結構時預設使用 llm-wiki 架構 |
| `mermaid-visualizer/SKILL.md`      | ✅ 純英文，無需修改                                                           |
| `obsidian-bases/SKILL.md`          | ✅ 純英文，無需修改                                                           |
| `obsidian-canvas-creator/SKILL.md` | ✅ description 已調整，以明確區隔 Excalidraw                                  |
| `obsidian-cli/SKILL.md`            | ✅ 純英文，無需修改                                                           |
| `obsidian-markdown/SKILL.md`       | ✅ 已加入新建立 Obsidian 結構時預設使用 llm-wiki 架構之規範                   |
