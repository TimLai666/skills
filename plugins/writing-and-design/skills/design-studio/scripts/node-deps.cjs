/**
 * node-deps.cjs: shared loader for the Node scripts in this folder.
 *
 * The skill folder has no node_modules of its own, so each script looks for its
 * dependencies in this order:
 *   1. an explicit path from an environment variable (PLAYWRIGHT_MODULE, or
 *      DESIGN_STUDIO_NODE_MODULES pointing at a node_modules folder)
 *   2. the current working directory (run the script from a folder where you ran
 *      `npm install`)
 *   3. this scripts folder
 * Playwright falls back from `playwright` to `playwright-core`.
 *
 * Browser: when Playwright's bundled browser is not installed, the local Chrome is
 * used (CHROME_PATH, or the standard install path for the platform).
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');
const { pathToFileURL } = require('url');

function requirers() {
  const list = [];
  const extra = process.env.DESIGN_STUDIO_NODE_MODULES;
  if (extra) list.push(createRequire(path.join(path.resolve(extra), '..', 'noop.js')));
  list.push(createRequire(path.join(process.cwd(), 'noop.js')));
  list.push(createRequire(__filename));
  return list;
}

function loadModule(names, installHint) {
  const candidates = Array.isArray(names) ? names : [names];
  for (const name of candidates) {
    for (const req of requirers()) {
      try { return req(name); } catch (e) { /* try the next location */ }
    }
  }
  const hint = installHint || `npm install ${candidates[0]}`;
  console.error(`錯誤：找不到 ${candidates.join(' 或 ')}。請在要執行的資料夾跑 \`${hint}\`，`
    + '或設定 DESIGN_STUDIO_NODE_MODULES 指向已安裝的 node_modules 資料夾。');
  process.exit(2);
}

function loadPlaywright() {
  if (process.env.PLAYWRIGHT_MODULE) {
    try { return require(path.resolve(process.env.PLAYWRIGHT_MODULE)); } catch (e) {
      console.error(`錯誤：PLAYWRIGHT_MODULE 指向的 ${process.env.PLAYWRIGHT_MODULE} 載入失敗：${e.message}`);
      process.exit(2);
    }
  }
  return loadModule(['playwright', 'playwright-core'], 'npm install playwright');
}

function localChrome() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH;
  const list = process.platform === 'win32'
    ? ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe']
    : process.platform === 'darwin'
      ? ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
      : ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser'];
  return list.find((p) => fs.existsSync(p));
}

/** Launch Chromium: Playwright's bundled browser first, the local Chrome when it is missing. */
async function launchChromium(chromium, options = {}) {
  if (process.env.CHROME_PATH) return chromium.launch({ ...options, executablePath: process.env.CHROME_PATH });
  try {
    return await chromium.launch(options);
  } catch (e) {
    const chrome = localChrome();
    if (!chrome) throw e;
    return chromium.launch({ ...options, executablePath: chrome });
  }
}

/** Absolute file path to a file:// URL that works on Windows, macOS and Linux. */
function fileUrl(p) {
  return pathToFileURL(path.resolve(p)).href;
}

/** Wait until web fonts are loaded, plus a short settle time for layout and paint. */
async function waitForFonts(page, settleMs = 400) {
  await page.evaluate(async () => { if (document.fonts) await document.fonts.ready; }).catch(() => {});
  await page.waitForTimeout(settleMs);
}

module.exports = { loadModule, loadPlaywright, launchChromium, localChrome, fileUrl, waitForFonts };
