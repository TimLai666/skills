#!/usr/bin/env python3
"""verify.py：用 Playwright 開啟設計產出的 HTML，截圖、收集錯誤、檢查橫向捲動。

用法與依賴見 --help。
"""

import argparse
import os
import sys
import tempfile
import time
from pathlib import Path

HELP_EPILOG = """範例：
  python verify.py design.html                          # 預設 1440x900 與 375x812 各截首屏與整頁
  python verify.py design.html --viewports 1920x1080    # 只用一種視窗大小
  python verify.py deck.html --slides 10                # 單檔投影片：按右鍵翻頁，逐頁截前 10 張
  python verify.py design.html --output ./shots         # 指定截圖資料夾
  python verify.py design.html --show                   # 開出看得到的瀏覽器視窗

檢查項目：
  - pageerror（JavaScript 執行錯誤）：有就以結束碼 1 結束
  - 橫向捲動（scrollWidth 大於視窗寬度）：有就以結束碼 1 結束
  - console 的 error 與 warning：列出供檢查，不影響結束碼

依賴：
  pip install playwright
  沒有安裝 Playwright 自帶的 Chromium（playwright install chromium）時，會改用本機 Chrome，
  也可用 --chrome 或環境變數 CHROME_PATH 指定。
  多檔案投影片請改用 node scripts/export_deck_pdf.mjs 或 gen_deck_thumbs.mjs 截圖。
"""


def setup_stdout():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def parse_viewport(text):
    w, h = text.lower().split("x")
    return {"width": int(w), "height": int(h)}


def local_chrome():
    if os.environ.get("CHROME_PATH"):
        return os.environ["CHROME_PATH"]
    if sys.platform == "win32":
        paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    elif sys.platform == "darwin":
        paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    else:
        paths = ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser"]
    return next((p for p in paths if Path(p).exists()), None)


def launch(p, show, chrome):
    if chrome:
        return p.chromium.launch(headless=not show, executable_path=chrome)
    try:
        return p.chromium.launch(headless=not show)
    except Exception:
        fallback = local_chrome()
        if not fallback:
            raise
        return p.chromium.launch(headless=not show, executable_path=fallback)


def verify_html(html_path, viewports, slides, output_dir, show, wait, chrome):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("錯誤：沒有安裝 Python 版 Playwright。請執行 pip install playwright。")
        return 2

    html_path = Path(html_path).resolve()
    if not html_path.exists():
        print(f"錯誤：找不到檔案 {html_path}")
        return 2

    if output_dir is None:
        output_dir = Path(tempfile.gettempdir()) / f"design-verify-{html_path.stem}-{time.strftime('%Y%m%d-%H%M%S')}"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_url = html_path.as_uri()
    stem = html_path.stem
    console_msgs, page_errors, overflow = [], [], []

    with sync_playwright() as p:
        browser = launch(p, show, chrome)
        for viewport in viewports:
            context = browser.new_context(viewport=viewport)
            page = context.new_page()
            size = f"{viewport['width']}x{viewport['height']}"
            page.on("console", lambda msg, size=size: console_msgs.append(f"[{size} {msg.type}] {msg.text}")
                    if msg.type in ("error", "warning") else None)
            page.on("pageerror", lambda err, size=size: page_errors.append(f"[{size}] {err}"))

            print(f"\n→ 開啟 {file_url} @ {size}")
            page.goto(file_url, wait_until="networkidle")
            page.evaluate("document.fonts ? document.fonts.ready.then(() => true) : true")
            page.wait_for_timeout(wait)

            widths = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            if widths[0] > widths[1]:
                overflow.append(f"{size}：scrollWidth {widths[0]} 大於視窗寬 {widths[1]}")

            if slides > 0:
                for i in range(slides):
                    shot = output_dir / f"{stem}-{size}-slide-{i + 1:02d}.png"
                    page.screenshot(path=str(shot))
                    print(f"  ✓ 第 {i + 1} 頁 → {shot.name}")
                    if i < slides - 1:
                        page.keyboard.press("ArrowRight")
                        page.wait_for_timeout(500)
            else:
                shot = output_dir / f"{stem}-{size}.png"
                page.screenshot(path=str(shot))
                full = output_dir / f"{stem}-{size}-full.png"
                page.screenshot(path=str(full), full_page=True)
                print(f"  ✓ 首屏 → {shot.name}，整頁 → {full.name}")

            if show:
                input("  （瀏覽器視窗保持開啟，按 Enter 繼續）")
            context.close()
        browser.close()

    print("\n" + "=" * 50 + "\n驗證結果\n" + "=" * 50)
    print(f"\n{'❌' if page_errors else '✅'} pageerror：{len(page_errors)}")
    for e in page_errors:
        print(f"  - {e}")
    print(f"{'❌' if overflow else '✅'} 橫向捲動：{'；'.join(overflow) if overflow else '沒有'}")
    print(f"{'⚠️ ' if console_msgs else '✅'} console error／warning：{len(console_msgs)}")
    for m in console_msgs[:20]:
        print(f"  - {m}")
    if len(console_msgs) > 20:
        print(f"  …另外 {len(console_msgs) - 20} 則")
    print(f"\n📸 截圖：{output_dir}")
    return 1 if (page_errors or overflow) else 0


def main():
    setup_stdout()
    parser = argparse.ArgumentParser(
        description="用 Playwright 驗證設計產出的 HTML：截圖、pageerror、橫向捲動、console 訊息。",
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("html_path", help="要檢查的 HTML 檔")
    parser.add_argument("--viewports", default="1440x900,375x812", help="逗號分隔的視窗大小 WxH（預設 1440x900,375x812）")
    parser.add_argument("--slides", type=int, default=0, help="單檔投影片模式：按右鍵翻頁，截前 N 頁")
    parser.add_argument("--output", default=None, help="截圖資料夾（預設：系統暫存資料夾，不寫進專案）")
    parser.add_argument("--show", action="store_true", help="開出看得到的瀏覽器視窗")
    parser.add_argument("--wait", type=int, default=1500, help="字型載入後再等幾毫秒（預設 1500）")
    parser.add_argument("--chrome", default=None, help="指定 Chrome 執行檔路徑")
    args = parser.parse_args()
    viewports = [parse_viewport(v) for v in args.viewports.split(",") if v.strip()]
    return verify_html(args.html_path, viewports, args.slides, args.output, args.show, args.wait, args.chrome)


if __name__ == "__main__":
    sys.exit(main())
