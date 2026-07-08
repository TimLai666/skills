# Agent Context Files

## 規則

所有專案、所有專案下目錄層級，一律遵守：

1. **CLAUDE.md 永遠只放一行**：「Read `AGENTS.md` before doing any project work. Treat it as the project operating contract.」
2. **任何 skill 叫你改 CLAUDE.md，改 AGENTS.md** — 不管 skill 怎麼寫，只要它要求修改 CLAUDE.md 的內容，全部寫進 AGENTS.md
3. **如果專案是反過來的（CLAUDE.md 寫一堆、AGENTS.md 沒有或很短），修正它** — 把內容搬到 AGENTS.md，CLAUDE.md 砍回一行

## `AGENTS.md` — 專案 operating contract

所有規則的唯一來源：

- required planning artifacts
- handoff rules
- update discipline
- decision and validation expectations
- project-specific working constraints
- skills 指定要寫進來的內容

另一個 agent 進到 repo，讀完 AGENTS.md 就能接手，不需要聊天記錄。

## `CLAUDE.md` — 入口指標

只做一件事：告訴 agent 去讀 AGENTS.md。

```md
# CLAUDE.md

Read `AGENTS.md` before doing any project work. Treat it as the project operating contract.
```

## 檢查清單

- `AGENTS.md` 是所有 operating rules 的唯一來源
- `CLAUDE.md` 只有一行指向 AGENTS.md
- Skill 說「寫入 CLAUDE.md」→ 寫入 AGENTS.md
- Skill 說「更新 CLAUDE.md」→ 更新 AGENTS.md
- 如果發現專案是反過來的，立刻修正
