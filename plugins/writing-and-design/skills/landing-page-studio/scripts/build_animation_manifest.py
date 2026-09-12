#!/usr/bin/env python3
"""Build animation manifest for landing-page-studio outputs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List

ANIMATION_LEVEL_FACTORS = {
    "high": 1.0,
    "medium": 0.7,
    "low": 0.45,
}


def _load_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.input_json:
        return json.loads(args.input_json)
    if args.file:
        with open(args.file, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)


def build_manifest(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Input must be a JSON object.")
    for field in ("webgl_supported", "prefers_reduced_motion"):
        if field in payload and type(payload[field]) is not bool:
            raise ValueError(field + " must be a JSON boolean.")
    if payload.get("animation_level", "high") not in ANIMATION_LEVEL_FACTORS:
        raise ValueError("animation_level must be low, medium, or high.")
    if payload.get("motion_preference", "respect-reduced-motion") != "respect-reduced-motion":
        raise ValueError("motion_preference must be respect-reduced-motion.")
    if payload.get("output_mode", "single-file-html") not in {"single-file-html", "react-project"}:
        raise ValueError("output_mode must be single-file-html or react-project.")
    style_direction = payload.get("style_direction", "")
    animation_level = payload.get("animation_level", "high")
    motion_preference = payload.get("motion_preference", "respect-reduced-motion")
    webgl_supported = bool(payload.get("webgl_supported", True))
    prefers_reduced_motion = bool(payload.get("prefers_reduced_motion", False))

    factor = ANIMATION_LEVEL_FACTORS.get(animation_level, ANIMATION_LEVEL_FACTORS["high"])
    reduce = motion_preference == "respect-reduced-motion" and prefers_reduced_motion

    if not webgl_supported and not reduce and animation_level != "low":
        raise ValueError("WebGL unavailable: requested animation cannot run; repair the environment or obtain approval to change the effect.")

    manifest: List[Dict[str, Any]] = []

    if webgl_supported and not reduce and animation_level != "low":
        manifest.append(
            {
                "id": "hero_webgl_layer",
                "category": "hero",
                "library": "three",
                "target": "#hero-canvas",
                "trigger": "on-load",
                "fallback": "report-error",
                "intensity": round(0.8 * factor, 2),
            }
        )
    else:
        manifest.append(
            {
                "id": "hero_svg_drift",
                "category": "hero",
                "library": "animejs",
                "target": "#hero-svg",
                "trigger": "on-load",
                "fallback": "report-error",
                "intensity": round(0.45 * factor, 2),
            }
        )

    manifest.extend(
        [
            {
                "id": "section_stagger_reveal",
                "category": "section-enter",
                "library": "gsap",
                "target": "[data-reveal]",
                "trigger": "on-scroll",
                "fallback": "report-error",
                "intensity": 0.0 if reduce else round(0.65 * factor, 2),
            },
            {
                "id": "cta_magnetic",
                "category": "interaction",
                "library": "gsap",
                "target": "[data-magnetic]",
                "trigger": "on-pointer-move",
                "fallback": "report-error",
                "intensity": 0.0 if reduce else round(0.7 * factor, 2),
            },
            {
                "id": "background_noise_drift",
                "category": "background",
                "library": "css",
                "target": "body::before",
                "trigger": "always",
                "fallback": "report-error",
                "intensity": round(0.4 * factor, 2),
            },
        ]
    )

    if animation_level == "high" and not reduce:
        manifest.append(
            {
                "id": "border_beam",
                "category": "interaction",
                "library": "css",
                "target": ".beam-border",
                "trigger": "always",
                "fallback": "report-error",
                "intensity": round(0.55 * factor, 2),
            }
        )

    if reduce:
        for effect in manifest:
            effect.update(library="none", trigger="none", intensity=0.0)
            effect["fallback"] = "static-gradient" if effect["category"] == "hero" else "static-visible-content"
    if reduce:
        notes = [
            "reduced motion detected: all effects static",
            "webgl effects replaced with static/svg alternatives",
        ]
    else:
        notes = ["full animation profile enabled"]

    return {
        "status": "planned",
        "verification_required": "Compare targets, triggers, fallbacks and runtime behavior with the delivered page; this is not observed QA.",
        "style_direction": style_direction,
        "animation_level": animation_level,
        "manifest_count": len(manifest),
        "animation_manifest": manifest,
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build animation manifest")
    parser.add_argument("--input-json", help="Input JSON string")
    parser.add_argument("--file", help="Path to JSON file")
    args = parser.parse_args()

    try:
        payload = _load_payload(args)
        result = build_manifest(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        print(json.dumps({"type": "error", "message": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
