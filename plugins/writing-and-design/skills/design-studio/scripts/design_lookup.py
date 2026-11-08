#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""design_lookup.py - 用英文關鍵字查 UI/UX 設計參考資料（BM25）。

移植自 ui-ux-pro-max 2.15.0 的 scripts/core.py
（https://github.com/nextlevelbuilder/ui-ux-pro-max-skill，MIT License）。
授權全文見 data/ui-ux/LICENSE-ui-ux-pro-max.txt。

只用 Python 標準函式庫，相容 Python 3.9+。資料位於 ../data/ui-ux/。
用法說明請執行：python design_lookup.py --help
"""

import argparse
import csv
import difflib
import json
import re
import sys
from collections import defaultdict
from math import log
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "ui-ux"
MAX_RESULTS = 3
TRUNCATE_AT = 300

# ============ DOMAINS ============
CSV_CONFIG = {
    "style": {
        "file": "styles.csv",
        "summary": "視覺風格（minimalism、brutalism、editorial 等）的特徵、配色、效果與適用情境",
        "search_cols": ["Style ID", "Style Category", "Aliases", "Keywords", "Best For", "Type", "AI Prompt Keywords"],
        "output_cols": ["Style ID", "Style Category", "Aliases", "Status", "Parent Style ID", "Preferred Mode", "Type", "Keywords", "Primary Colors", "Effects & Animation", "Best For", "Light Mode ✓", "Dark Mode ✓", "Performance", "Accessibility", "Framework Compatibility", "Complexity", "AI Prompt Keywords", "CSS/Technical Keywords", "Implementation Checklist", "Design System Variables"],
    },
    "color": {
        "file": "colors.csv",
        "summary": "依產品類型整理的語意色票（primary、accent、background、border 等）",
        "search_cols": ["Product Type", "Notes"],
        "output_cols": ["Product Type", "Primary", "On Primary", "Secondary", "On Secondary", "Accent", "On Accent", "Background", "Foreground", "Card", "Card Foreground", "Muted", "Muted Foreground", "Border", "Destructive", "On Destructive", "Ring", "Notes"],
    },
    "typography": {
        "file": "typography.csv",
        "summary": "標題與內文字體搭配、氣質關鍵字與適用情境",
        "search_cols": ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"],
        "output_cols": ["Font Pairing Name", "Category", "Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Google Fonts URL", "CSS Import", "Tailwind Config", "Notes"],
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "summary": "易用性與無障礙檢查項目，附該做與不該做的寫法",
        "search_cols": ["Category", "Issue", "Description", "Platform"],
        "output_cols": ["Category", "Issue", "Platform", "Description", "Do", "Don't", "Code Example Good", "Code Example Bad", "Severity"],
    },
    "chart": {
        "file": "charts.csv",
        "summary": "依資料型態挑圖表類型、不適用情境與無障礙注意事項",
        "search_cols": ["Data Type", "Keywords", "Best Chart Type", "When to Use", "When NOT to Use", "Accessibility Notes"],
        "output_cols": ["Data Type", "Keywords", "Best Chart Type", "Secondary Options", "When to Use", "When NOT to Use", "Data Volume Threshold", "Color Guidance", "Accessibility Grade", "Accessibility Risk", "Accessibility Notes", "A11y Fallback", "Library Recommendation", "Interactive Level"],
    },
    "landing": {
        "file": "landing.csv",
        "summary": "落地頁區塊順序、CTA 位置與轉換重點",
        "search_cols": ["Pattern ID", "Pattern Name", "Aliases", "Keywords", "Conversion Optimization", "Section Order"],
        "output_cols": ["Pattern ID", "Pattern Name", "Aliases", "Keywords", "Section Order", "Primary CTA Placement", "Color Strategy", "Conversion Optimization"],
    },
    "product": {
        "file": "products.csv",
        "summary": "依產品類型（SaaS、電商、醫療等）建議的風格、落地頁與配色方向",
        "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations"],
        "output_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern", "Dashboard Style (if applicable)", "Color Palette Focus"],
    },
    "threejs": {
        "file": "threejs.csv",
        "summary": "Three.js / WebGL 的效能、渲染與資源管理守則，附正反範例程式",
        "search_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad"],
        "output_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Code Good", "Code Bad", "Severity", "Docs URL", "Applies To", "Status", "Verified At"],
    },
}
DOMAINS = list(CSV_CONFIG)

# Code samples and checklists lose their value when cut mid-way.
UNTRUNCATED_COLS = {
    "Code Example Good", "Code Example Bad", "Code Good", "Code Bad",
    "Implementation Checklist", "Design System Variables", "CSS Import",
    "Tailwind Config",
}

# ============ CALIBRATION (from core.py) ============
_DOMAIN_SCORE_FLOORS = {"style": 4.3, "landing": 4.0, "product": 6.0}
_SEARCH_THRESHOLDS = {
    domain: {"min_score": _DOMAIN_SCORE_FLOORS.get(domain, 0.0),
             "min_margin": 0.0, "min_coverage": 0.5 if domain == "landing" else 0.0}
    for domain in CSV_CONFIG
}
# core.py applies this threshold to every stack file, threejs included.
_SEARCH_THRESHOLDS["threejs"] = {"min_score": 3.6, "min_margin": 0.0, "min_coverage": 1 / 3}

_STYLE_IDENTITY_FIELDS = ("Style ID", "Style Category", "Aliases")
_LANDING_IDENTITY_FIELDS = ("Pattern ID", "Pattern Name", "Aliases")
_DOMAIN_QUERY_REWRITES = {
    "color": {term: None for term in (
        "color", "palette", "hex", "rgb", "token", "semantic",
        "destructive", "muted", "foreground")},
    "landing": {"testimonial": "testimonials"},
    "style": {"css": None, "implementation": None, "variable": None,
              "checklist": None, "tailwind": None},
    "ux": {"ux": "accessibility", "usability": "accessibility",
           "wcag": "accessibility"},
    "typography": {"typography": "font"},
}

# ============ TOKENIZATION ============
_STOPWORDS = {
    "to", "in", "on", "at", "is", "of", "by", "or", "an", "if", "no", "so",
    "do", "be", "we", "it", "as", "the", "and", "for", "are", "was",
}

_SYNONYMS = {
    "q&a": "question answer",
    "e-commerce": "ecommerce",
    "dark-mode": "dark",
    "darkmode": "dark",
    "light-mode": "light",
    "lightmode": "light",
    "a11y": "accessibility",
    "nav": "navigation",
    "sign-up": "signup",
    "log-in": "login",
    "colour": "color",
    "colours": "colors",
    "customisation": "customization",
    "organisation": "organization",
    "behaviour": "behavior",
    "ux/ui": "ux ui",
}

_SYNONYM_PATTERNS = [
    (re.compile(r"(?<!\w)" + re.escape(variant) + r"(?!\w)", re.IGNORECASE), canonical)
    for variant, canonical in sorted(_SYNONYMS.items(), key=lambda item: len(item[0]), reverse=True)
]

_CJK_RE = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯豈-﫿＀-￯]")
CJK_HINT = "資料與斷詞只支援英文，請改用英文關鍵字（例如「茶葉品牌」改成 \"tea brand\"）。"


def _normalize(text):
    """Apply longest-first synonym substitution at token boundaries."""
    normalized = str(text)
    for pattern, canonical in _SYNONYM_PATTERNS:
        normalized = pattern.sub(canonical, normalized)
    return normalized


# ============ BM25 ============
class BM25:
    """BM25 ranking over whitespace-tokenized English text."""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.doc_lengths = []
        self.avgdl = 0.0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0
        self._term_freqs = []

    def tokenize(self, text):
        text = _normalize(str(text).lower())
        text = re.sub(r"[^\w\s]", " ", text)
        return [w for w in text.split() if len(w) >= 2 and w not in _STOPWORDS]

    def fit(self, documents):
        corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in corpus]
        self.avgdl = sum(self.doc_lengths) / self.N or 1.0
        for doc in corpus:
            tf = defaultdict(int)
            for word in doc:
                tf[word] += 1
            self._term_freqs.append(tf)
            for word in tf:
                self.doc_freqs[word] += 1
        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        query_tokens = self.tokenize(query)
        scores = []
        for idx in range(self.N):
            score = 0.0
            doc_len = self.doc_lengths[idx]
            term_freqs = self._term_freqs[idx]
            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs.get(token, 0)
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    score += self.idf[token] * numerator / denominator
            scores.append((idx, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def vocabulary(self):
        return list(self.idf.keys())


# ============ DATA ============
_csv_cache = {}


def _load_csv(filepath):
    if filepath not in _csv_cache:
        with open(filepath, "r", encoding="utf-8", newline="") as f:
            _csv_cache[filepath] = list(csv.DictReader(f))
    return _csv_cache[filepath]


def _load_rows_or_empty(filepath):
    try:
        return _load_csv(filepath)
    except (csv.Error, OSError, UnicodeDecodeError):
        return []


def _row_filter(domain):
    """Rows indexed per domain: active styles only, current threejs guidance only."""
    if domain == "style":
        return lambda row: row.get("Status", "active") == "active"
    if domain == "threejs":
        return lambda row: row.get("Status", "unverified") != "deprecated"
    return None


# ============ SEARCH HELPERS ============
def _query_coverage(index, query):
    tokens = set(index.tokenize(query))
    if not tokens:
        return 0.0
    vocabulary = set(index.vocabulary())
    return sum(token in vocabulary for token in tokens) / len(tokens)


def _passes_threshold(index, query, threshold):
    ranked = index.score(query)
    top_score = ranked[0][1] if ranked else 0.0
    runner_up_score = ranked[1][1] if len(ranked) > 1 else 0.0
    return (top_score > threshold["min_score"]
            and _query_coverage(index, query) >= threshold["min_coverage"]
            and (threshold["min_margin"] <= 0
                 or top_score - runner_up_score >= threshold["min_margin"]))


def _suggest_terms(bm25, query, limit=6, threshold=None):
    """Nearest indexed terms for a query that returned no hits."""
    if bm25 is None:
        return []
    query_tokens = set(bm25.tokenize(query))
    if not query_tokens:
        return []
    candidates = []
    for term in bm25.vocabulary():
        if term in query_tokens:
            continue
        similarity = max(difflib.SequenceMatcher(None, token, term).ratio()
                         for token in query_tokens)
        if (similarity >= 0.72
                and (threshold is None or _passes_threshold(bm25, term, threshold))):
            candidates.append((-similarity, -bm25.doc_freqs.get(term, 0), term))
    return [term for _, _, term in sorted(candidates)[:limit]]


def _row_identities(row, fields):
    identities = []
    for field in fields:
        values = row.get(field, "").split("|") if field == "Aliases" else [row.get(field, "")]
        identities.extend(value.strip() for value in values if value.strip())
    return identities


def _suggest_identities(rows, query, fields, limit=6):
    """Suggest complete identities so a retry can hit an exact match."""
    tokenizer = BM25()
    query_tokens = set(tokenizer.tokenize(query))
    if not query_tokens:
        return []
    candidates = []
    for row in rows:
        for identity in _row_identities(row, fields):
            identity_tokens = set(tokenizer.tokenize(identity))
            if not identity_tokens:
                continue
            similarity = max(
                difflib.SequenceMatcher(None, source, target).ratio()
                for source in query_tokens for target in identity_tokens
            )
            if similarity >= 0.72 and identity.casefold() != str(query).strip().casefold():
                candidates.append((-similarity, len(identity_tokens), identity))
    return [identity for _, _, identity in sorted(set(candidates))[:limit]]


def _style_identity(rows, query, allow_contained=True):
    """Resolve an explicit style name/ID/alias in the query."""
    folded = str(query or "").strip().casefold()
    query_tokens = set(re.findall(r"\w+", _normalize(folded), re.UNICODE))
    generic_tokens = {"app", "design", "interface", "style", "system", "ui"}
    candidates = []
    for row in rows:
        identities = _row_identities(row, _STYLE_IDENTITY_FIELDS)
        if folded in {identity.casefold() for identity in identities}:
            return row
        if not allow_contained:
            continue
        for identity in identities:
            identity_tokens = set(re.findall(r"\w+", _normalize(identity.casefold()), re.UNICODE))
            if (identity_tokens and identity_tokens <= query_tokens
                    and any(len(token) >= 4 for token in identity_tokens)):
                distinctive = identity_tokens - generic_tokens
                candidates.append((len(distinctive), len(identity_tokens), len(identity), row))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    best_score = candidates[0][:3]
    best_rows = {c[3].get("Style ID", ""): c[3] for c in candidates if c[:3] == best_score}
    return next(iter(best_rows.values())) if len(best_rows) == 1 else None


def _style_destination(rows, matched):
    """Follow a deprecated style to its active parent or replacement."""
    if not matched or matched.get("Status", "active") != "deprecated":
        return matched, None
    parent_id = matched.get("Parent Style ID", "").strip()
    if parent_id:
        return next((row for row in rows if row.get("Style ID") == parent_id), None), None
    domain = matched.get("Replacement Domain", "").strip()
    replacement_id = matched.get("Replacement ID", "").strip()
    if domain == "style" and replacement_id:
        return next((row for row in rows if row.get("Style ID") == replacement_id), None), None
    if domain and replacement_id:
        return None, {"domain": domain, "id": replacement_id}
    return None, None


def _exact_row_identity(rows, query, fields):
    folded = str(query or "").strip().casefold()
    matches = [row for row in rows
               if folded in {identity.casefold() for identity in _row_identities(row, fields)}]
    return matches[0] if len(matches) == 1 else None


def _project_row(row, columns):
    return {column: row.get(column, "") for column in columns if column in row}


# ============ DOMAIN DETECTION ============
_DOMAIN_KEYWORDS = None


def _load_product_keywords():
    """High-signal product labels from products.csv plus a built-in seed."""
    seed = ["saas", "ecommerce", "fintech", "healthcare", "gaming", "portfolio",
            "crypto", "fitness", "marketplace", "banking", "cybersecurity",
            "education", "travel", "restaurant", "real estate", "social media",
            "beauty", "spa", "salon", "wellness", "booking"]
    rows = _load_rows_or_empty(DATA_DIR / CSV_CONFIG["product"]["file"])
    keywords = set(seed)
    for row in rows:
        label = re.sub(r"\([^)]*\)", "", row.get("Product Type", "")).strip().lower()
        if len(label) >= 4:
            keywords.add(label)
    return sorted(keywords, key=len, reverse=True)


def _domain_keywords():
    global _DOMAIN_KEYWORDS
    if _DOMAIN_KEYWORDS is None:
        _DOMAIN_KEYWORDS = {
            "color": ["color", "palette", "hex", "rgb", "token", "semantic", "accent", "destructive", "muted", "foreground"],
            "chart": ["time series", "chart", "graph", "visualization", "trend", "bar chart", "pie", "scatter", "heatmap", "funnel", "forecast"],
            "landing": ["landing", "page", "cta", "conversion", "hero", "testimonial", "pricing", "section"],
            "product": _load_product_keywords(),
            "style": ["style", "design", "ui", "minimalism", "glassmorphism", "neumorphism", "brutalism", "dark mode", "flat", "aurora", "css", "implementation", "variable", "checklist", "tailwind"],
            "ux": ["ux", "usability", "accessibility", "wcag", "touch", "scroll", "animation", "keyboard", "navigation", "mobile"],
            "typography": ["font pairing", "typography pairing", "heading font", "body font", "font", "fonts", "typography", "typeface", "serif", "sans serif", "monospace", "display font", "handwriting font"],
            "threejs": ["three.js", "threejs", "webgl", "webgpu", "3d scene", "shader", "gltf", "r3f", "react three fiber", "orbitcontrols", "draw call", "instancing"],
        }
    return _DOMAIN_KEYWORDS


def _contains_phrase(text, phrase):
    if re.search(r"\w", phrase):
        return bool(re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text))
    return phrase in text


def _rewrite_query_for_domain(query, domain, index):
    """Apply explicit rewrites for routing words the corpus does not contain."""
    keywords = _domain_keywords().get(domain)
    if not keywords:
        return query, []
    normalized = _normalize(query.lower())
    vocabulary = set(index.vocabulary())
    rewrites, replacement_terms = [], []
    for keyword in keywords:
        if not _contains_phrase(normalized, keyword):
            continue
        if set(index.tokenize(keyword)) & vocabulary:
            continue
        replacement = _DOMAIN_QUERY_REWRITES.get(domain, {}).get(keyword)
        if replacement:
            rewrites.append("%s->%s" % (keyword, replacement))
            replacement_terms.append(replacement)
    if not replacement_terms:
        return query, []
    return "%s %s" % (query, " ".join(sorted(set(replacement_terms)))), sorted(set(rewrites))


_DOMAIN_TIEBREAK_ORDER = ["ux", "product", "style", "color", "typography", "chart", "landing", "threejs"]
_DOMAIN_TIEBREAK_RANK = {domain: rank for rank, domain in enumerate(_DOMAIN_TIEBREAK_ORDER)}


def detect_domain(query):
    """Pick a domain by weighted keyword hits; returns (domain, runner_up)."""
    query_lower = _normalize(query.lower())
    scores = {}
    for domain, keywords in _domain_keywords().items():
        total = 0.0
        for kw in keywords:
            if _contains_phrase(query_lower, kw):
                specificity = max(1, len(kw.split()))
                total += 2.0 * specificity if domain != "product" else specificity
        scores[domain] = total
    if re.search(r"(?<!\w)#[0-9a-f]{3,8}(?!\w)", query_lower, re.IGNORECASE):
        scores["color"] += 2.0
    ranked = sorted(scores.items(),
                    key=lambda item: (item[1], -_DOMAIN_TIEBREAK_RANK.get(item[0], 999)),
                    reverse=True)
    best_domain, best_score = ranked[0]
    runner_up = ranked[1][0] if len(ranked) > 1 and ranked[1][1] > 0 else None
    return (best_domain if best_score > 0 else "style"), runner_up


# ============ SEARCH ============
def _search_csv(filepath, domain, query, max_results):
    config = CSV_CONFIG[domain]
    data = _load_csv(filepath)
    row_filter = _row_filter(domain)
    if row_filter is not None:
        data = [row for row in data if row_filter(row)]
    if not data:
        return [], None
    bm25 = BM25()
    bm25.fit([" ".join(str(row.get(col, "")) for col in config["search_cols"]) for row in data])
    search_query, _ = _rewrite_query_for_domain(query, domain, bm25)
    ranked = bm25.score(search_query)
    threshold = _SEARCH_THRESHOLDS[domain]
    top_score = ranked[0][1] if ranked else 0.0
    runner_up_score = ranked[1][1] if len(ranked) > 1 else 0.0
    abstain = (top_score <= threshold["min_score"]
               or _query_coverage(bm25, search_query) < threshold["min_coverage"]
               or (threshold["min_margin"] > 0
                   and top_score - runner_up_score < threshold["min_margin"]))
    results = []
    if not abstain:
        for idx, score in ranked[:max_results]:
            if score <= 0:
                continue
            results.append(_project_row(data[idx], config["output_cols"]))
    return results, bm25


def search(query, domain=None, max_results=MAX_RESULTS):
    auto_detected = domain is None
    runner_up = None
    exact = None
    redirect = None
    style_rows = None
    style_path = DATA_DIR / CSV_CONFIG["style"]["file"]

    if domain is None:
        style_rows = _load_rows_or_empty(style_path)
        matched = _style_identity(style_rows, query, allow_contained=False)
        if matched is not None:
            domain = "style"
            exact, redirect = _style_destination(style_rows, matched)
        else:
            domain, runner_up = detect_domain(query)

    config = CSV_CONFIG[domain]
    filepath = DATA_DIR / config["file"]
    if not filepath.exists():
        return {"error": "找不到資料檔：%s" % filepath, "domain": domain}

    try:
        landing_rows = []
        if domain == "style" and exact is None and redirect is None:
            if style_rows is None:
                style_rows = _load_csv(filepath)
            exact, redirect = _style_destination(style_rows, _style_identity(style_rows, query))
        elif domain == "landing":
            landing_rows = _load_csv(filepath)
            exact = _exact_row_identity(landing_rows, query, _LANDING_IDENTITY_FIELDS)

        if exact is not None:
            results, bm25 = [_project_row(exact, config["output_cols"])], None
        elif redirect is not None:
            results, bm25 = [], None
        else:
            results, bm25 = _search_csv(filepath, domain, query, max_results)
    except (csv.Error, OSError, UnicodeDecodeError) as exc:
        return {"error": "無法讀取資料檔 %s：%s" % (filepath.name, exc), "domain": domain}

    out = {"domain": domain, "query": query, "file": config["file"],
           "count": len(results), "results": results}
    if auto_detected:
        out["auto_detected"] = True
        if runner_up:
            out["runner_up_domain"] = runner_up
    if redirect is not None:
        out["redirect"] = redirect
    if not results and redirect is None:
        if domain == "landing":
            out["suggestions"] = _suggest_identities(landing_rows, query, _LANDING_IDENTITY_FIELDS)
        else:
            out["suggestions"] = _suggest_terms(bm25, query, threshold=_SEARCH_THRESHOLDS[domain])
    return out


# ============ OUTPUT ============
def format_output(result, full=False):
    if "error" in result:
        return "Error: %s" % result["error"]
    domain_note = result["domain"]
    if result.get("auto_detected"):
        domain_note += "（自動判斷"
        if result.get("runner_up_domain"):
            domain_note += "，次選 %s" % result["runner_up_domain"]
        domain_note += "）"
    lines = [
        "## Design lookup",
        "**Domain:** %s | **Query:** %s" % (domain_note, result["query"]),
        "**Source:** data/ui-ux/%s | **Found:** %d" % (result["file"], result["count"]),
        "結果只作參考與檢查，不直接套用。",
        "",
    ]
    if result["count"] == 0:
        redirect = result.get("redirect")
        if redirect:
            lines.append("這個舊風格名稱已改列在 `%s` domain 的 `%s`，請改查該 domain。"
                         % (redirect["domain"], redirect["id"]))
            return "\n".join(lines)
        lines.append("資料庫沒有符合的結果。請換更廣或不同的英文關鍵字，或用 --domain 指定其他類別再查。")
        suggestions = result.get("suggestions") or []
        if suggestions:
            lines.append("**相近詞：** %s" % ", ".join(suggestions))
        return "\n".join(lines)
    for i, row in enumerate(result["results"], 1):
        lines.append("### Result %d" % i)
        for key, value in row.items():
            value_str = str(value)
            if not full and key not in UNTRUNCATED_COLS and len(value_str) > TRUNCATE_AT:
                value_str = value_str[:TRUNCATE_AT] + "..."
            lines.append("- **%s:** %s" % (key, value_str))
        lines.append("")
    return "\n".join(lines)


# ============ CLI ============
def _build_parser():
    domain_lines = "\n".join("  %-11s %s" % (name, cfg["summary"]) for name, cfg in CSV_CONFIG.items())
    description = (
        "用英文關鍵字查 UI/UX 設計參考資料（BM25 關鍵字比對）。\n"
        "結果只作參考與檢查用：拿來對照方向、補漏、檢查易用性，不直接套用色票、字體或風格。\n"
        "資料與斷詞只支援英文，中文查詢不會有結果。\n\n"
        "domains（不給 --domain 時依關鍵字自動判斷，判斷不出來時用 style）：\n" + domain_lines
    )
    epilog = (
        "範例：\n"
        "  python design_lookup.py \"tea brand organic craft\"\n"
        "  python design_lookup.py \"editorial magazine\" --domain style -n 3\n"
        "  python design_lookup.py \"dashboard\" --domain chart\n"
        "  python design_lookup.py \"shadow performance\" --domain threejs\n"
        "  python design_lookup.py \"form error\" --domain ux --json\n\n"
        "查不到時會列出資料裡的相近詞，可用相近詞重查。\n"
        "資料移植自 ui-ux-pro-max 2.15.0（MIT），授權見 data/ui-ux/LICENSE-ui-ux-pro-max.txt。"
    )
    parser = argparse.ArgumentParser(
        prog="design_lookup.py",
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", help="英文關鍵字，多個字用空白分開並加引號")
    parser.add_argument("--domain", "-d", choices=DOMAINS, help="指定查詢類別；省略時自動判斷")
    parser.add_argument("-n", "--max-results", type=int, choices=range(1, 21), default=MAX_RESULTS,
                        metavar="N", help="最多回傳幾筆，1-20（預設 %d）" % MAX_RESULTS)
    parser.add_argument("--json", action="store_true", help="輸出 JSON（不截斷欄位）")
    parser.add_argument("--full", action="store_true",
                        help="文字輸出不截斷長欄位（預設超過 %d 字會截斷）" % TRUNCATE_AT)
    return parser


def _use_utf8_stdio():
    for stream in (sys.stdout, sys.stderr):
        try:
            if stream.encoding and stream.encoding.lower().replace("-", "") != "utf8":
                stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main(argv=None):
    _use_utf8_stdio()
    argv = sys.argv[1:] if argv is None else argv
    parser = _build_parser()
    if not argv:
        parser.print_help()
        return 0
    args = parser.parse_args(argv)
    query = args.query.strip()
    if not query:
        parser.error("query 不可為空白")

    if _CJK_RE.search(query):
        print("提示：" + CJK_HINT, file=sys.stderr)
        if not re.search(r"[A-Za-z0-9]", query):
            if args.json:
                print(json.dumps({"error": CJK_HINT, "query": query}, ensure_ascii=False, indent=2))
            return 2

    result = search(query, args.domain, args.max_results)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result, full=args.full))
    return 1 if "error" in result else 0


if __name__ == "__main__":
    sys.exit(main())
