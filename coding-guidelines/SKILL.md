---
name: coding-guidelines
version: 1.0.0
description: "Behavioral guidelines for writing code. Think before coding, simplicity first, surgical changes, TDD, verifiable success criteria. Triggers on: 寫 code, 改 code, 做功能, 修 bug, refactor, 開發, coding, development, 實作, 實現, 寫程式, 改程式, 加功能, 修問題"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
---

## Auto-trigger

**任何寫 code 或改 code 的工作都要先載入這個 skill。** 不論是新功能、bug fix、refactor、還是 code review，只要動到程式碼就先讀。

---

## 核心原則

### 1. 想清楚再寫

**不要假設。不要隱藏困惑。把 tradeoff 搬上檯面。**

實作前：
- 明確陳述你的假設。不確定就問。
- 有多種解法就都列出，不要默默選一個。
- 有更簡單的做法就講，該擋就擋。
- 有不清楚的地方就停下來，說清楚哪裡不懂，問。

### 2. 最小變更

**能少改就少改，只解決被要求的事。**

- 不做沒被要求的功能。
- 不為一次性使用的 code 做抽象。
- 不加沒被要求的「彈性」或「可配置」。
- 不為不可能的場景加 error handling。
- 寫了 200 行但 50 行就能搞定，重寫。

問自己：「資深工程師會不會覺得太複雜？」會的話就簡化。

### 3. 精準手術

**只動該動的。只清自己製造的垃圾。**

改既有 code 時：
- 不要「順便改善」旁邊的 code、註解或格式。
- 不要 refactor 沒壞的東西。
- 沿用現有風格，即使你會寫不一樣。
- 發現不相關的死 code 就提一下，不要刪。

當你的變更產生 orphan 時：
- 刪除你的變更造成的 unused imports/variables/functions。
- 不要删既有的死 code，除非被要求。

**檢驗標準：每一行改動都要能直接追溯到使用者的需求。**

### 4. TDD（Test-Driven Development）

**所有變更和功能都必須有對應的測試。沒有測試等於沒做完。**

流程：
```
1. 寫失敗的 test（定義期望行為）
2. 寫最少的 code 讓 test 通過
3. 重構，確保 test 仍通過
4. 重複
```

規則：
- **先寫 test，再寫 implementation。** 不要寫完 code 才補 test。
- **每個 bug fix 都要先有一個能重現 bug 的 test。** 修完後 test 要通過。
- **每個新功能都要有對應的 test。** 功能沒有 test 覆蓋就不算完成。
- **重構前先確認所有 test 都通過。** 重構後再確認一次。
- **不要為了讓 test 過而硬改 test。** 除非 test 本身確實寫錯。
- Test 要能證明這次修改有效，不是只為了 coverage 數字。

### 5. 目標驅動執行

**定義成功標準。跑迴圈直到驗證通過。**

把任務轉成可驗證的目標：
- 「加 validation」→ 「為無效輸入寫 test，然後让它通過」
- 「修 bug」→ 「寫一個能重現 bug 的 test，然後让它通過」
- 「refactor X」→ 「確認 test 在改前改後都通過」

多步驟任務要列出計畫：
```
1. [步驟] → 驗證：[怎麼確認]
2. [步驟] → 驗證：[怎麼確認]
3. [步驟] → 驗證：[怎麼確認]
```

強的成功標準讓你自己能跑迴圈。弱的成功標準（「讓它能用」）需要一直問人。

---

## 工作流程

### A. 開始寫 code 前

1. 確認你理解需求。有不清楚的先問。
2. 陳述假設和限制。
3. 列出可能的解法，說明你選哪個、為什麼。
4. 定義成功標準：怎麼樣算「做完」。
5. 如果有既有 test，先跑一次確認都通過。

### B. 寫 code 時

1. **TDD 迴圈**：紅 → 綠 → 重構。
2. 每個變更都要能追溯到需求。
3. 不動不該動的東西。
4. 保持 code 簡單，不超過需求。
5. 沿用既有 code style。

### C. 完成後

1. 跑全部 test，確認都通過。
2. 跑 linter / type checker（如果專案有的話）。
3. 檢查：每一行改動都能追溯到需求嗎？
4. 檢查：有沒有不小心動到不該動的東西？
5. 檢查：code 夠簡單嗎？資深工程師會不會覺得太複雜？

---

## 常見地雷

- **Gold plating**：加了沒被要求的功能，因為「順手」。
- **Premature abstraction**：只出現一次的邏輯就抽成共用函式。
- **Defensive coding for impossible scenarios**：為不可能發生的錯誤加 error handling。
- **Refactoring unrelated code**：改 A 的時候順便改 B，結果 B 壞了。
- **Test-after**：先寫 code 再補 test，結果 test 只能測到表面。
- **Making test pass by weakening assertion**：test 失敗了就改 test 而不是改 code。

---

## 收尾自我檢查

- [ ] 每一行改動都能追溯到使用者的需求。
- [ ] 沒有做沒被要求的事。
- [ ] 沒有為一次性使用的 code 做抽象。
- [ ] 所有變更和功能都有對應的 test。
- [ ] 先寫了 test，再寫 implementation。
- [ ] Bug fix 有一個能重現 bug 的 test。
- [ ] 全部 test 都通過。
- [ ] Linter / type checker 沒有報錯。
- [ ] Code 夠簡單，不超過需求。
