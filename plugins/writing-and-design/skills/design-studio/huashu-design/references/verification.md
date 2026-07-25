# Verification：輸出驗證流程

一些 design-agent 原生環境（如 Claude.ai Artifacts）有內建的 `fork_verifier_agent` 起 subagent 用 iframe 截圖檢查。大部分 agent 環境（Claude Code / Codex / Cursor / Trae / 等）裡沒有這個內建能力——用 Playwright 手動做就能覆蓋相同的驗證場景。

## 驗證清單

每次產出HTML後，按這個清單做一遍：

### 1. 瀏覽器渲染檢查（必做）

最基礎：**HTML能不能開啟**？在macOS上：

```bash
open -a "Google Chrome" "/path/to/your/design.html"
```

或者用Playwright截圖（下一節）。

### 2. 控制台錯誤檢查

HTML檔案裡最常見的問題是JS報錯導致白屏。用Playwright跑一遍：

```bash
python ~/.claude/skills/huashu-design/scripts/verify.py path/to/design.html
```

這個指令碼會：
1. 用headless chromium開啟HTML
2. 截圖儲存到專案目錄
3. 抓取控制台錯誤
4. 報告status

詳見`scripts/verify.py`。

### 3. 多視口檢查

如果是響應式設計，抓多個viewport：

```bash
python verify.py design.html --viewports 1920x1080,1440x900,768x1024,375x667
```

### 4. 互動檢查

Tweaks、動畫、按鈕切換——預設的靜態截圖看不到。**建議讓使用者自己開瀏覽器點一遍**，或者用Playwright錄屏：

```python
page.video.record('interaction.mp4')
```

### 5. 幻燈片逐頁檢查

Deck類HTML，一張張截：

```bash
python verify.py deck.html --slides 10  # 截前10張
```

生成 `deck-slide-01.png`、`deck-slide-02.png`... 方便快速瀏覽。

## Playwright Setup

首次使用需要：

```bash
# 如果還沒裝
npm install -g playwright
npx playwright install chromium

# 或者Python版
pip install playwright
playwright install chromium
```

如果使用者已經全域性安裝 Playwright，直接用即可。

## 截圖最佳實踐

### 截完整頁面

```python
page.screenshot(path='full.png', full_page=True)
```

### 截viewport

```python
page.screenshot(path='viewport.png')  # 預設只截可見區域
```

### 截特定元素

```python
element = page.query_selector('.hero-section')
element.screenshot(path='hero.png')
```

### 高畫質截圖

```python
page = browser.new_page(device_scale_factor=2)  # retina
```

### 等動畫結束再截

```python
page.wait_for_timeout(2000)  # 等2秒讓動畫settle
page.screenshot(...)
```

## 把截圖發給使用者

### 本地截圖直接開啟

```bash
open screenshot.png
```

使用者會在自己的 Preview/Figma/VSCode/瀏覽器 裡看。

### 上傳圖床分享連結

如果需要給遠端協作者看（比如 Slack/飛書/微信），讓使用者用自己的圖床工具或 MCP 上傳截圖，拿到一個永久連結，可以貼上到任何地方。

## 驗證出錯時

### 頁面白屏

控制台一定有錯。先檢查：

1. React+Babel script tag的integrity hash對不對（見`react-setup.md`）
2. 是不是`const styles = {...}`命名衝突
3. 跨檔案的元件有沒有export到`window`
4. JSX語法錯誤（babel.min.js不報錯，換babel.js非壓縮版）

### 動畫卡

- 用Chrome DevTools Performance tab錄一段
- 找layout thrashing（頻繁的reflow）
- 動效優先用`transform`和`opacity`（GPU加速）

### 字型不對

- 檢查`@font-face`的url是否可訪問
- 檢查fallback字型
- 中文字型載入慢：先顯示fallback，載入完再切換

### 佈局錯位

- 檢查`box-sizing: border-box`是否全域性應用
- 檢查`*  margin: 0; padding: 0`reset
- Chrome DevTools裡開啟gridlines看實際佈局

## 驗證=設計師的第二雙眼

**永遠要自己過一遍**。AI寫程式碼時經常出現：

- 看起來對但interaction有bug
- 靜態截圖好但scroll時錯位
- 寬屏好看但窄屏崩
- Dark mode忘了測
- Tweaks切換後某些元件沒響應

**最後1分鐘的驗證可以省1小時的返工**。

## 常用驗證指令碼命令

```bash
# 基礎：開啟+截圖+抓錯
python verify.py design.html

# 多viewport
python verify.py design.html --viewports 1920x1080,375x667

# 多slide
python verify.py deck.html --slides 10

# 輸出到指定目錄
python verify.py design.html --output ./screenshots/

# headless=false，開啟真實瀏覽器給你看
python verify.py design.html --show
```
