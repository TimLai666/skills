#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A/B 測試樣本數計算器（Python 標準函式庫，不需 scipy / statsmodels）。

支援兩種指標型態：
  proportion  比例型指標（轉換率、點擊率、留存率）
  continuous  連續型指標（AOV、停留秒數、每人營收）

計算方法：兩獨立組、雙尾檢定、正態近似。
  proportion: n = (z_{a/2} + z_b)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)^2
  continuous: n = 2 * (z_{a/2} + z_b)^2 * sigma^2 / delta^2

z 值不查 scipy，直接用 math.erf 定義的正態 CDF 反解（二分法，精度 1e-10）。
常用值對照（可自行驗證）：
  alpha 0.05（雙尾）→ z_{a/2} = 1.9600
  alpha 0.01（雙尾）→ z_{a/2} = 2.5758
  power 0.80        → z_b    = 0.8416
  power 0.90        → z_b    = 1.2816

範例：
  python sample_size.py proportion --baseline 0.02 --mde 0.10 --daily-traffic 8000
  python sample_size.py proportion --baseline 0.02 --mde 0.002 --mde-type absolute
  python sample_size.py proportion --baseline 0.05 --mde 0.08 --variants 3 --power 0.9
  python sample_size.py continuous --mean 850 --std 620 --mde 0.05 --daily-traffic 3000
  python sample_size.py continuous --std 620 --mde 40 --mde-type absolute

注意：結果為正態近似，與其他計算器（pooled 公式、精確法）相差 ±5% 屬正常。
"""

import argparse
import math
import sys


def normal_cdf(x: float) -> float:
    """標準常態分布 CDF，Phi(x) = 0.5 * (1 + erf(x / sqrt(2)))。"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def z_from_quantile(p: float) -> float:
    """反解標準常態分位數（inverse CDF），二分法，精度 1e-10。"""
    if not 0.0 < p < 1.0:
        raise ValueError("分位數必須在 (0, 1) 之間")
    lo, hi = -10.0, 10.0
    while hi - lo > 1e-10:
        mid = (lo + hi) / 2.0
        if normal_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def n_per_group_proportion(p1: float, p2: float, alpha: float, power: float) -> int:
    """比例型指標每組所需樣本（unpooled 正態近似，雙尾）。"""
    z_a = z_from_quantile(1.0 - alpha / 2.0)
    z_b = z_from_quantile(power)
    delta = abs(p2 - p1)
    var_sum = p1 * (1.0 - p1) + p2 * (1.0 - p2)
    n = (z_a + z_b) ** 2 * var_sum / delta**2
    return math.ceil(n)


def n_per_group_continuous(std: float, delta: float, alpha: float, power: float) -> int:
    """連續型指標每組所需樣本（等變異數假設，雙尾）。"""
    z_a = z_from_quantile(1.0 - alpha / 2.0)
    z_b = z_from_quantile(power)
    n = 2.0 * (z_a + z_b) ** 2 * std**2 / delta**2
    return math.ceil(n)


def duration_report(n_per_group: int, variants: int, daily_traffic: float) -> str:
    """給定日流量，估工期並附工期規則提醒。"""
    total = n_per_group * variants
    days = math.ceil(total / daily_traffic)
    weeks_rounded = math.ceil(days / 7) * 7
    lines = [
        f"日進實驗流量    : {daily_traffic:,.0f}",
        f"預估工期        : {days} 天（向上取整到完整週 → 建議 {max(weeks_rounded, 7)} 天）",
    ]
    if days < 7:
        lines.append("提醒：樣本雖然幾天就夠，仍至少跑滿 1 週（建議 2 週）涵蓋週間與週末。")
    if days > 56:
        lines.append("警告：工期超過 8 週，觸發 Data Sufficiency Gate——")
        lines.append("      不建議硬跑。考慮：放大 MDE（只測更大的改動）、改用更靈敏的")
        lines.append("      proxy 指標、或改用 pre-post + 控制組 / quasi-experiment / 質化驗證。")
    return "\n".join(lines)


def fmt_common(n: int, variants: int, alpha: float, power: float) -> str:
    return "\n".join(
        [
            f"alpha（雙尾）   : {alpha}",
            f"power           : {power}",
            f"每組所需樣本    : {n:,}",
            f"組數            : {variants}",
            f"總樣本          : {n * variants:,}",
        ]
    )


def run_proportion(args: argparse.Namespace) -> None:
    p1 = args.baseline
    if not 0.0 < p1 < 1.0:
        sys.exit("錯誤：--baseline 必須在 (0, 1) 之間，例如 2% 轉換率寫 0.02")
    if args.mde_type == "relative":
        p2 = p1 * (1.0 + args.mde)
        mde_desc = f"相對 {args.mde:+.1%}"
    else:
        p2 = p1 + args.mde
        mde_desc = f"絕對 {args.mde:+.4f}"
    if not 0.0 < p2 < 1.0:
        sys.exit(f"錯誤：目標轉換率 {p2:.4f} 超出 (0, 1)，請檢查 MDE 設定")
    if abs(p2 - p1) < 1e-12:
        sys.exit("錯誤：MDE 不可為 0")

    n = n_per_group_proportion(p1, p2, args.alpha, args.power)
    print("=== A/B 樣本數計算（比例型指標）===")
    print(f"基準轉換率      : {p1:.4%}")
    print(f"目標轉換率      : {p2:.4%}（MDE：{mde_desc}）")
    print(fmt_common(n, args.variants, args.alpha, args.power))
    if args.daily_traffic:
        print(duration_report(n, args.variants, args.daily_traffic))


def run_continuous(args: argparse.Namespace) -> None:
    if args.std <= 0:
        sys.exit("錯誤：--std 必須大於 0")
    if args.mde_type == "relative":
        if args.mean is None:
            sys.exit("錯誤：相對 MDE 需要 --mean（絕對差 = mean × MDE）")
        delta = abs(args.mean * args.mde)
        mde_desc = f"相對 {args.mde:+.1%}（絕對差 {delta:,.4g}）"
    else:
        delta = abs(args.mde)
        mde_desc = f"絕對差 {delta:,.4g}"
    if delta <= 0:
        sys.exit("錯誤：MDE 不可為 0")

    n = n_per_group_continuous(args.std, delta, args.alpha, args.power)
    print("=== A/B 樣本數計算（連續型指標）===")
    if args.mean is not None:
        print(f"基準平均值      : {args.mean:,.4g}")
    print(f"標準差          : {args.std:,.4g}")
    print(f"MDE             : {mde_desc}")
    print(fmt_common(n, args.variants, args.alpha, args.power))
    if args.daily_traffic:
        print(duration_report(n, args.variants, args.daily_traffic))


def add_shared_args(sub: argparse.ArgumentParser) -> None:
    sub.add_argument("--mde", type=float, required=True,
                     help="最小可偵測效果。relative 時為比例（0.10 = 相對提升 10%%）；absolute 時為指標的絕對差")
    sub.add_argument("--mde-type", choices=["relative", "absolute"], default="relative",
                     help="MDE 型態，預設 relative")
    sub.add_argument("--alpha", type=float, default=0.05, help="顯著水準（雙尾），預設 0.05")
    sub.add_argument("--power", type=float, default=0.80, help="統計檢定力，預設 0.80")
    sub.add_argument("--variants", type=int, default=2,
                     help="組數（含控制組），預設 2。注意：多變體請另做多重比較校正")
    sub.add_argument("--daily-traffic", type=float, default=None,
                     help="每日可進實驗的流量（所有組加總），提供時會估工期")


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(
        description="A/B 測試樣本數計算器（stdlib only，正態近似）",
        epilog="範例：python sample_size.py proportion --baseline 0.02 --mde 0.10 --daily-traffic 8000",
    )
    subs = parser.add_subparsers(dest="metric_type", required=True)

    sp = subs.add_parser("proportion", help="比例型指標（轉換率、點擊率）")
    sp.add_argument("--baseline", type=float, required=True, help="基準轉換率，例如 0.02")
    add_shared_args(sp)
    sp.set_defaults(func=run_proportion)

    sc = subs.add_parser("continuous", help="連續型指標（AOV、停留秒數）")
    sc.add_argument("--mean", type=float, default=None, help="基準平均值（relative MDE 時必填）")
    sc.add_argument("--std", type=float, required=True, help="指標標準差")
    add_shared_args(sc)
    sc.set_defaults(func=run_continuous)

    args = parser.parse_args()

    if not 0.0 < args.alpha < 1.0:
        sys.exit("錯誤：--alpha 必須在 (0, 1) 之間")
    if not 0.0 < args.power < 1.0:
        sys.exit("錯誤：--power 必須在 (0, 1) 之間")
    if args.variants < 2:
        sys.exit("錯誤：--variants 至少為 2（含控制組）")
    if args.daily_traffic is not None and args.daily_traffic <= 0:
        sys.exit("錯誤：--daily-traffic 必須大於 0")

    args.func(args)


if __name__ == "__main__":
    main()
