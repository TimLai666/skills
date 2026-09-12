#!/usr/bin/env python3
"""Validate and normalize LandingPageInput for landing-page-studio skill."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

REQUIRED_FIELDS = [
    "brand_theme",
    "value_props",
    "primary_cta",
]

ALLOWED_OUTPUT_MODES = {"single-file-html", "react-project"}
ALLOWED_VARIANT_MODES = {"single", "batch"}
ALLOWED_AUTONOMY_MODES = {"single-pass", "multi-iteration"}
ALLOWED_ANIMATION_LEVELS = {"low", "medium", "high"}

DEFAULTS: Dict[str, Any] = {
    "variant_mode": "single",
    "autonomy_mode": "multi-iteration",
    "animation_level": "high",
    "motion_preference": "respect-reduced-motion",
}

REACT_STACK_OPTIONS = [
    {
        "id": "vite-react-tailwind-framer",
        "pros": ["啟動快", "生成效率高", "動畫整合快"],
        "cons": ["SEO 能力需額外配置"],
    },
    {
        "id": "nextjs-app-router",
        "pros": ["SEO 友好", "路由與部署成熟"],
        "cons": ["結構較重", "學習與維護成本較高"],
    },
    {
        "id": "react-css-modules",
        "pros": ["依賴少", "樣式可控"],
        "cons": ["動效整合與速度通常較慢"],
    },
]


def _load_input(args: argparse.Namespace) -> Dict[str, Any]:
    if args.input_json:
        return json.loads(args.input_json)
    if args.file:
        with open(args.file, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    raw = sys.stdin.read().strip()
    if not raw:
        raise ValueError("No input provided. Use --input-json, --file, or stdin JSON.")
    return json.loads(raw)


def _missing_output(missing: List[str], extra_reasons: Dict[str, str]) -> Dict[str, Any]:
    why_needed = {
        "brand_theme": "決定視覺語言與文案語氣",
        "value_props": "決定核心轉換訊息與三卡區塊內容",
        "primary_cta": "決定行動路徑與按鈕文案",
        "style_direction": "決定視覺方向；未定時先走 design-studio 風格庫（三軸校準＋40 風格＋深度風格包）選定",
        "output_mode": "決定輸出格式與專案結構",
    }
    why_needed.update(extra_reasons)

    return {
        "type": "MissingDataOutput",
        "missing_fields": missing,
        "why_needed": {k: why_needed.get(k, "此欄位為必要輸入") for k in missing},
        "questions_to_user": [f"請提供 `{field}`" for field in missing],
        "next_step_rule": "補齊缺失欄位後重新執行生成。",
    }


def validate_intake(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Input must be a JSON object.")
    data = {**DEFAULTS, **payload}
    project = data.get("existing_project", {})
    if not isinstance(project, dict):
        raise ValueError("existing_project must be an object with output_mode and optional react_stack.")
    data.setdefault("output_mode", project.get("output_mode", "single-file-html"))
    if data["output_mode"] == "react-project":
        data.setdefault("react_stack", project.get("react_stack", "vite-react-tailwind-framer"))

    reasons: Dict[str, str] = {}
    for field in ("brand_theme", "primary_cta"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            reasons[field] = "必須提供非空白字串。"
    props = data.get("value_props")
    if not isinstance(props, list) or not props or any(not isinstance(v, str) or not v.strip() for v in props):
        reasons["value_props"] = "提供非空白字串陣列，預設整理三個真實價值主張，依內容可調整數量。"
    enums = {
        "output_mode": ALLOWED_OUTPUT_MODES,
        "variant_mode": ALLOWED_VARIANT_MODES,
        "autonomy_mode": ALLOWED_AUTONOMY_MODES,
        "animation_level": ALLOWED_ANIMATION_LEVELS,
        "motion_preference": {"respect-reduced-motion"},
        "react_stack": {option["id"] for option in REACT_STACK_OPTIONS},
    }
    for field, choices in enums.items():
        if field == "react_stack" and field not in payload and field in project:
            if not isinstance(project[field], str) or not project[field].strip():
                reasons[field] = "既有專案技術組合必須是非空白字串。"
            continue
        if field in data and (not isinstance(data[field], str) or data[field] not in choices):
            reasons[field] = "有效值：" + ", ".join(sorted(choices))
    for field in ("style_direction", "target_audience", "industry"):
        if field in data and not isinstance(data[field], str):
            reasons[field] = "必須是字串。"
    if reasons:
        return _missing_output(list(reasons), reasons)
    style_selection_required = not data.get("style_direction", "").strip()
    return {
        "type": "LandingPageInputNormalized",
        "valid": True,
        "framework_choice_required": False,
        "style_selection_required": style_selection_required,
        "next_step_rule": "先沿用既有視覺方向，或依 design-studio 完成風格選型再生成。" if style_selection_required else "依已確認內容生成並驗證頁面。",
        "normalized_input": data,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate landing-page-studio intake payload")
    parser.add_argument("--input-json", help="Input JSON string")
    parser.add_argument("--file", help="Path to JSON file")
    args = parser.parse_args()

    try:
        payload = _load_input(args)
        result = validate_intake(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("valid") else 2
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        error = {"type": "error", "message": str(exc)}
        print(json.dumps(error, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
