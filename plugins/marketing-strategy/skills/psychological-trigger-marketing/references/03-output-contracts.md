# 輸出格式

完整策略或使用者要求結構化交接時讀取。單一 CTA／標題不使用整包格式。

## 完整策略

可用 Markdown 呈現以下內容，要求 JSON 時使用此結構：

```json
{
  "strategy_summary": "",
  "trigger_stack": [],
  "message_angles": [],
  "headline_options": [],
  "cta_options": [],
  "risk_flags": [],
  "assumptions_used": []
}
```

- strategy_summary：主軸與選擇理由。
- trigger_stack：每個選用方法的 why 與 role，不強制區分主／輔或限定數量。
- message_angles、headline_options、cta_options：依需求展開，有實質不同的角度。
- risk_flags：影響採用的條件、承諾或證據缺口。
- assumptions_used：實際使用的假設。

JSON 空陣列可以表示沒有相關項目，不能為填欄位而捏造內容。

## 缺資料格式

只有需要結構化交接時使用，對話中直接問關鍵問題即可。

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "temporary_assumptions": [],
  "risk_of_assumption": []
}
```
