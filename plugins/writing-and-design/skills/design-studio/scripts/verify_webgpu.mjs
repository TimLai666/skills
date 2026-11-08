#!/usr/bin/env node
/**
 * verify_webgpu.mjs：檢查 WebGPU 特效頁的三條路徑（WebGPU、WebGL 2、減少動態效果）
 * 完整用法：node scripts/verify_webgpu.mjs --help
 */
import { createRequire } from 'node:module';
import { existsSync, mkdirSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { tmpdir } from 'node:os';

const HELP = `verify_webgpu.mjs：用 Playwright 開啟特效頁，分別走 WebGPU、WebGL 2、減少動態效果三種情況，
截圖並回報實際路徑、幀時間與 console 錯誤數。

用法：
  node scripts/verify_webgpu.mjs <html 檔或網址> [選項]

選項：
  --out <資料夾>        截圖輸出位置（預設：系統暫存資料夾/verify-webgpu-<時間>）
  --modes <清單>        要跑的情況，逗號分隔：webgpu,webgl,reduced-motion,auto（預設前三個）
  --param <名稱>        頁面用哪個網址參數切換路徑（預設 renderer，即 ?renderer=webgpu）
  --attr <名稱>         頁面把實際路徑寫在 <html data-*> 的哪個欄位（預設 renderer）
  --duration <毫秒>     每種情況量測幀時間的長度（預設 3000）
  --viewport <寬x高>    視窗大小（預設 1440x900）
  --chrome <路徑>       指定 Chrome 執行檔（預設：Windows/macOS/Linux 的本機 Chrome，找不到才用 Playwright 內建瀏覽器）
  --headed              開出看得到的視窗（預設 headless）
  --swiftshader         改用軟體模擬的 WebGPU（沒有 GPU 的 CI 環境用；幀時間不代表真實效能）
  --flags "<旗標>"      額外的 Chrome 啟動旗標，空白分隔
  --json                只輸出 JSON
  -h, --help            顯示這段說明

各情況的預期結果：
  webgpu          網址加 ?renderer=webgpu，預期 data-renderer = webgpu
  webgl           網址加 ?renderer=webgl， 預期 data-renderer = webgl
  reduced-motion  模擬系統「減少動態效果」，不加參數，預期 data-renderer = static
  auto            不加參數，只回報實際路徑，不判定對錯

頁面要求：
  - 把實際路徑寫在 document.documentElement.dataset.<attr>（webgpu|webgl|static），初始化完成前寫 pending
  - 可選：原因寫在 data-<attr>-reason，會一併回報

結束代碼：任何情況路徑不符、逾時或有 console 錯誤時為 1，全部通過為 0。

Playwright 來源（依序嘗試）：環境變數 PLAYWRIGHT_MODULE 指定的路徑 → playwright → playwright-core
（從本腳本所在處或目前工作目錄解析）。例如：
  PLAYWRIGHT_MODULE=/path/to/node_modules/playwright-core node scripts/verify_webgpu.mjs page.html

注意：WebGPU 只在安全環境（https、localhost、file://）可用；about:blank 與一般 http 網址拿不到 navigator.gpu。`;

// ── 參數解析 ──
const argv = process.argv.slice(2);
const opts = { modes: 'webgpu,webgl,reduced-motion', param: 'renderer', attr: 'renderer', duration: 3000, viewport: '1440x900', flags: '' };
let target = null;
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  const next = () => {
    const v = argv[++i];
    if (v === undefined) fail(`${a} 需要一個值`);
    return v;
  };
  if (a === '-h' || a === '--help') { console.log(HELP); process.exit(0); }
  else if (a === '--out') opts.out = next();
  else if (a === '--modes') opts.modes = next();
  else if (a === '--param') opts.param = next();
  else if (a === '--attr') opts.attr = next();
  else if (a === '--duration') opts.duration = Number(next());
  else if (a === '--viewport') opts.viewport = next();
  else if (a === '--chrome') opts.chrome = next();
  else if (a === '--flags') opts.flags = next();
  else if (a === '--headed') opts.headed = true;
  else if (a === '--swiftshader') opts.swiftshader = true;
  else if (a === '--json') opts.json = true;
  else if (a.startsWith('-')) fail(`不認得的選項 ${a}，用 --help 看用法`);
  else if (!target) target = a;
  else fail(`多了一個參數 ${a}`);
}
if (!target) fail('缺少要檢查的 html 檔或網址，用 --help 看用法');
if (!Number.isFinite(opts.duration) || opts.duration < 500) fail('--duration 至少 500 毫秒');
const vp = /^(\d+)x(\d+)$/.exec(opts.viewport);
if (!vp) fail('--viewport 格式是 寬x高，例如 1440x900');
const viewport = { width: Number(vp[1]), height: Number(vp[2]) };
const KNOWN = { webgpu: 'webgpu', webgl: 'webgl', 'reduced-motion': 'static', auto: null };
const modes = opts.modes.split(',').map((s) => s.trim()).filter(Boolean);
for (const m of modes) if (!(m in KNOWN)) fail(`不認得的情況 ${m}，可用：${Object.keys(KNOWN).join(', ')}`);

function fail(msg) { console.error(`錯誤：${msg}`); process.exit(2); }

// ── 載入 Playwright ──
async function loadPlaywright() {
  const tried = [];
  const candidates = [];
  if (process.env.PLAYWRIGHT_MODULE) candidates.push(process.env.PLAYWRIGHT_MODULE);
  candidates.push('playwright', 'playwright-core');
  const requirers = [createRequire(import.meta.url), createRequire(join(process.cwd(), 'noop.js'))];
  for (const c of candidates) {
    for (const req of requirers) {
      try { return req(c); } catch (e) { tried.push(c); }
    }
  }
  fail(`找不到 Playwright（試過：${[...new Set(tried)].join('、')}）。請 npm install playwright，或設定 PLAYWRIGHT_MODULE 指向 playwright-core 資料夾`);
}

function defaultChrome() {
  const list = process.platform === 'win32'
    ? ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe']
    : process.platform === 'darwin'
      ? ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
      : ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium'];
  return list.find((p) => existsSync(p));
}

function withParam(url, name, value) {
  const u = new URL(url);
  u.searchParams.set(name, value);
  return u.href;
}

function stats(samples) {
  if (!samples.length) return { avg: null, p95: null, n: 0 };
  const sorted = [...samples].sort((a, b) => a - b);
  const avg = samples.reduce((s, v) => s + v, 0) / samples.length;
  const p95 = sorted[Math.min(sorted.length - 1, Math.ceil(sorted.length * 0.95) - 1)];
  return { avg: +avg.toFixed(2), p95: +p95.toFixed(2), n: samples.length };
}

// ── 主流程 ──
const pw = await loadPlaywright();
const chromium = pw.chromium;
const baseUrl = /^[a-z]+:\/\//i.test(target) ? target : pathToFileURL(resolve(target)).href;
const outDir = resolve(opts.out || join(tmpdir(), `verify-webgpu-${new Date().toISOString().replace(/[:.]/g, '-')}`));
mkdirSync(outDir, { recursive: true });

const executablePath = opts.chrome || defaultChrome();
const args = opts.flags.split(/\s+/).filter(Boolean);
if (opts.swiftshader) args.push('--enable-unsafe-webgpu', '--use-webgpu-adapter=swiftshader');
const browser = await chromium.launch({ headless: !opts.headed, args, ...(executablePath ? { executablePath } : {}) });
const browserVersion = browser.version();

const results = [];
for (const mode of modes) {
  const context = await browser.newContext({ viewport, reducedMotion: mode === 'reduced-motion' ? 'reduce' : 'no-preference' });
  const page = await context.newPage();
  const errors = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('requestfailed', (r) => errors.push(`request failed: ${r.url()} (${r.failure()?.errorText})`));

  const url = mode === 'webgpu' || mode === 'webgl' ? withParam(baseUrl, opts.param, mode) : baseUrl;
  const r = { mode, url, expected: KNOWN[mode], renderer: null, reason: null, frame: null, errors: 0, screenshot: null, pass: false };
  try {
    await page.goto(url, { waitUntil: 'load', timeout: 30000 });
    await page.waitForFunction((attr) => {
      const v = document.documentElement.dataset[attr];
      return v && v !== 'pending';
    }, opts.attr, { timeout: 15000 });
    const info = await page.evaluate((attr) => ({
      renderer: document.documentElement.dataset[attr],
      reason: document.documentElement.dataset[attr + 'Reason'] ?? null,
      gpu: !!navigator.gpu,
      secure: isSecureContext,
    }), opts.attr);
    Object.assign(r, info);

    // 等特效淡入後再截圖
    await page.waitForTimeout(1500);
    r.screenshot = join(outDir, `${mode}.png`);
    await page.screenshot({ path: r.screenshot });

    // 量幀時間：在頁面裡用 requestAnimationFrame 記錄相鄰兩幀的間隔
    const samples = await page.evaluate((ms) => new Promise((done) => {
      const out = []; let last = 0; const end = performance.now() + ms;
      const tick = (now) => {
        if (last) out.push(now - last);
        last = now;
        if (now < end) requestAnimationFrame(tick); else done(out);
      };
      requestAnimationFrame(tick);
    }), opts.duration);
    r.frame = stats(samples);
    // 量測後再讀一次，抓「量測途中自動降級」的情況
    r.rendererAfter = await page.evaluate((attr) => document.documentElement.dataset[attr], opts.attr);
  } catch (e) {
    errors.push(`verify: ${e.message.split('\n')[0]}`);
  }
  r.errors = errors.length;
  r.errorMessages = errors.slice(0, 10);
  r.pass = r.errors === 0 && (r.expected === null ? !!r.renderer : r.renderer === r.expected && r.rendererAfter === r.expected);
  results.push(r);
  await context.close();
}
await browser.close();

const report = { target: baseUrl, browser: `${executablePath || 'playwright bundled'} (${browserVersion})`, headless: !opts.headed, swiftshader: !!opts.swiftshader, outDir, results };
if (opts.json) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`目標：${report.target}`);
  console.log(`瀏覽器：${report.browser}，${report.headless ? 'headless' : 'headed'}${report.swiftshader ? '，SwiftShader' : ''}`);
  console.log(`截圖：${outDir}`);
  for (const r of results) {
    const f = r.frame ? `平均 ${r.frame.avg} ms，p95 ${r.frame.p95} ms（${r.frame.n} 幀）` : '無幀時間';
    console.log(`\n[${r.pass ? 'PASS' : 'FAIL'}] ${r.mode}`);
    console.log(`  路徑：${r.renderer ?? '（未回報）'}${r.reason ? `（${r.reason}）` : ''}${r.expected ? `，預期 ${r.expected}` : ''}${r.rendererAfter && r.rendererAfter !== r.renderer ? `，量測後變成 ${r.rendererAfter}` : ''}`);
    console.log(`  幀時間：${f}`);
    console.log(`  console 錯誤：${r.errors}`);
    for (const m of r.errorMessages) console.log(`    - ${m}`);
    if (r.screenshot) console.log(`  截圖：${r.screenshot}`);
  }
}
process.exit(results.every((r) => r.pass) ? 0 : 1);
