#!/usr/bin/env node
/**
 * export_deck_pdf.mjs：把多檔案投影片（每頁一個 HTML）匯出成一份 PDF。
 * 用法與依賴見 --help。檔案依檔名排序（01-xxx.html → 02-xxx.html → ...）。
 */

import { createRequire } from 'module';
import fs from 'fs/promises';
import path from 'path';

const require = createRequire(import.meta.url);
const { loadModule, loadPlaywright, launchChromium, fileUrl, waitForFonts } = require('./node-deps.cjs');

const HELP = `export_deck_pdf.mjs：把多檔案投影片匯出成一份 PDF

用法：
  node export_deck_pdf.mjs --slides <資料夾> --out <檔案.pdf> [--width 1920] [--height 1080]

說明：
  - 每個 HTML 用 Chromium 印成一頁，再合併成一份 PDF，版面與瀏覽器看到的一致。
  - 英數文字保留向量可搜尋；部分中文網路字型嵌入後可能無法複製或搜尋，交付前用 PDF 閱讀器試一次。
  - 大量 SVG 濾鏡或點描會讓檔案變大，處理方式見 references/illustration-craft.md。

依賴：playwright（或 playwright-core）與 pdf-lib
  在任一資料夾跑 npm install playwright pdf-lib，然後在該資料夾執行本腳本，
  或設定 DESIGN_STUDIO_NODE_MODULES 指向那個 node_modules。
  沒裝 Playwright 自帶的瀏覽器時，會改用本機 Chrome（也可用 CHROME_PATH 指定）。
`;

function parseArgs() {
  const a = process.argv.slice(2);
  if (!a.length || a.includes('--help') || a.includes('-h')) {
    console.log(HELP);
    process.exit(a.length ? 0 : 1);
  }
  const args = { width: 1920, height: 1080 };
  for (let i = 0; i < a.length; i += 2) args[a[i].replace(/^--/, '')] = a[i + 1];
  if (!args.slides || !args.out) {
    console.error('缺少 --slides 或 --out。用法見 --help。');
    process.exit(1);
  }
  args.width = parseInt(args.width, 10);
  args.height = parseInt(args.height, 10);
  return args;
}

async function main() {
  const { slides, out, width, height } = parseArgs();
  const { chromium } = loadPlaywright();
  const { PDFDocument } = loadModule('pdf-lib');
  const slidesDir = path.resolve(slides);
  const outFile = path.resolve(out);

  const files = (await fs.readdir(slidesDir)).filter((f) => f.endsWith('.html')).sort();
  if (!files.length) {
    console.error(`${slidesDir} 裡沒有 .html 檔`);
    process.exit(1);
  }
  console.log(`找到 ${files.length} 頁：${slidesDir}`);

  const browser = await launchChromium(chromium);
  const ctx = await browser.newContext({ viewport: { width, height } });

  const pageBuffers = [];
  for (const f of files) {
    const page = await ctx.newPage();
    const url = fileUrl(path.join(slidesDir, f));
    await page.goto(url, { waitUntil: 'networkidle' }).catch(() => page.goto(url));
    await waitForFonts(page, 800);
    await page.emulateMedia({ media: 'screen' });
    const buf = await page.pdf({
      width: `${width}px`,
      height: `${height}px`,
      printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
      preferCSSPageSize: false,
    });
    pageBuffers.push(buf);
    await page.close();
    console.log(`  [${pageBuffers.length}/${files.length}] ${f}`);
  }
  await browser.close();

  const merged = await PDFDocument.create();
  for (const buf of pageBuffers) {
    const src = await PDFDocument.load(buf);
    const copied = await merged.copyPages(src, src.getPageIndices());
    copied.forEach((p) => merged.addPage(p));
  }
  const bytes = await merged.save();
  await fs.writeFile(outFile, bytes);
  console.log(`\n完成：${outFile}（${(bytes.byteLength / 1024 / 1024).toFixed(1)} MB，${files.length} 頁）`);
}

main().catch((e) => { console.error(e); process.exit(1); });
