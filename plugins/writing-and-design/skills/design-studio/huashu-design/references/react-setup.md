# React + Babel 專案規範

用HTML+React+Babel做原型時必須遵守的技術規範。不遵守會炸。

## Pinned Script Tags（必須用這些版本）

在HTML的`<head>`裡放這三個script tag，用**固定版本+integrity hash**：

```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
```

**不要**用`react@18`或`react@latest`這種unpinned版本——會出現版本漂移/快取問題。

**不要**省略`integrity`——CDN一旦被劫持或篡改，這是防線。

## 檔案結構

```
專案名/
├── index.html               # 主HTML
├── components.jsx           # 元件檔案（type="text/babel"載入）
├── data.js                  # 資料檔案
└── styles.css               # 額外CSS（可選）
```

HTML 裡的載入方式：

```html
<!-- 先React+Babel -->
<script src="https://unpkg.com/react@18.3.1/..."></script>
<script src="https://unpkg.com/react-dom@18.3.1/..."></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/..."></script>

<!-- 然後你的元件檔案 -->
<script type="text/babel" src="components.jsx"></script>
<script type="text/babel" src="pages.jsx"></script>

<!-- 最後主入口 -->
<script type="text/babel">
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<App />);
</script>
```

**不要**用`type="module"`——會和Babel衝突。

## 三條不可違反的規矩

### 規矩1：styles 物件必須用唯一命名

**錯誤**（多元件時必炸）：
```jsx
// components.jsx
const styles = { button: {...}, card: {...} };

// pages.jsx  ← 同名覆蓋！
const styles = { container: {...}, header: {...} };
```

**正確**：每個元件檔案的styles用唯一前綴。

```jsx
// terminal.jsx
const terminalStyles = { 
  screen: {...}, 
  line: {...} 
};

// sidebar.jsx
const sidebarStyles = { 
  container: {...}, 
  item: {...} 
};
```

**或者用inline styles**（小元件推薦）：
```jsx
<div style={{ padding: 16, background: '#111' }}>...</div>
```

這條是**非協商**的。每次寫`const styles = {...}`都必須replace成specific命名，否則多元件載入時整批報錯。

### 規矩2：Scope 不共享，需手動export

**關鍵認知**：每個`<script type="text/babel">`被Babel獨立編譯，它們之間**scope不通**。`components.jsx`裡定義的`Terminal`元件，在`pages.jsx`裡**預設是undefined**。

**解決方式**：在每個元件檔案末尾，把要共享的元件/工具export到`window`：

```jsx
// components.jsx 末尾
function Terminal(props) { ... }
function Line(props) { ... }
const colors = { green: '#...', red: '#...' };

Object.assign(window, {
  Terminal, Line, colors,
  // 所有你要在別處用的都列在這裡
});
```

然後`pages.jsx`就能直接用`<Terminal />`，因為JSX會去`window.Terminal`找。

### 規矩3：不要用 scrollIntoView

`scrollIntoView`會把整個HTML容器往上推，搞壞web harness的佈局。**永遠不要用**。

替代方案：
```js
// 滾到容器內某個位置
container.scrollTop = targetElement.offsetTop;

// 或者用element.scrollTo
container.scrollTo({
  top: targetElement.offsetTop - 100,
  behavior: 'smooth'
});
```

## 調 Claude API（HTML內）

部分原生 design-agent 環境（如 Claude.ai Artifacts）有免配置的 `window.claude.complete`，但大部分 agent 環境（Claude Code / Codex / Cursor / Trae / etc.）本地裡**沒有**。

如果你的 HTML 原型需要呼叫 LLM 做 demo（比如做個聊天 interface），兩個選項：

### 選項A：不真調，用mock

Demo場景推薦。寫一個假helper，返回預設的response：
```jsx
window.claude = {
  async complete(prompt) {
    await new Promise(r => setTimeout(r, 800)); // 模擬延遲
    return "這是一個mock回應。真部署時請替換為真API。";
  }
};
```

### 選項B：真調Anthropic API

需要API key，使用者必須在HTML裡填入自己的key才能跑。**永遠不要把key硬編碼在HTML裡**。

```html
<input id="api-key" placeholder="貼上你的Anthropic API key" />
<script>
window.claude = {
  async complete(prompt) {
    const key = document.getElementById('api-key').value;
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5',
        max_tokens: 1024,
        messages: [{ role: 'user', content: prompt }]
      })
    });
    const data = await res.json();
    return data.content[0].text;
  }
};
</script>
```

**注意**：瀏覽器直接調Anthropic API會遇到CORS問題。如果使用者給你的預覽環境不支援CORS bypass，這條路不通。這時候用選項A mock，或者告訴使用者需要一個proxy後端。

### 選項 C：用 agent 側的 LLM 能力生成 mock 資料

如果只是本地演示用，可以在當前 agent 會話裡臨時呼叫該 agent 的 LLM 能力（或使用者裝的 multi-model 類 skill）先生成 mock 回應資料，再硬編碼寫進 HTML。這樣 HTML 執行時完全不依賴任何 API。

## 典型 HTML 起手模板

複製這個模板作為React原型的骨架：

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Prototype Name</title>

  <!-- React + Babel pinned -->
  <script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
  <script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>

  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: 100%; width: 100%; }
    body { 
      font-family: -apple-system, 'SF Pro Text', sans-serif;
      background: #FAFAFA;
      color: #1A1A1A;
    }
    #root { min-height: 100vh; }
  </style>
</head>
<body>
  <div id="root"></div>

  <!-- 你的元件檔案 -->
  <script type="text/babel" src="components.jsx"></script>

  <!-- 主入口 -->
  <script type="text/babel">
    const { useState, useEffect } = React;

    function App() {
      return (
        <div style={{padding: 40}}>
          <h1>Hello</h1>
        </div>
      );
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
```

## 常見報錯及解決

**`styles is not defined` 或 `Cannot read property 'button' of undefined`**
→ 你在一個檔案裡定義了`const styles`，另一個檔案覆蓋了。給每個改成specific命名。

**`Terminal is not defined`**
→ 跨檔案引用時scope不通。在定義Terminal的檔案末尾加`Object.assign(window, {Terminal})`。

**整個頁面白屏，控制台沒錯誤**
→ 多半是JSX語法錯誤但Babel沒報在控制台。把`babel.min.js`臨時換成`babel.js`非壓縮版，錯誤資訊更清晰。

**ReactDOM.createRoot is not a function**
→ 版本不對。確認用了react-dom@18.3.1（而不是17或其他）。

**`Objects are not valid as a React child`**
→ 你渲染了一個物件而不是JSX/字串。通常是`{someObj}`寫成了`{someObj.name}`。

## 大專案怎麼拆檔案

**>1000行的單檔案**難維護。分拆思路：

```
專案/
├── index.html
├── src/
│   ├── primitives.jsx      # 基礎元素：Button、Card、Badge...
│   ├── components.jsx      # 業務元件：UserCard、PostList...
│   ├── pages/
│   │   ├── home.jsx        # 首頁
│   │   ├── detail.jsx      # 詳情頁
│   │   └── settings.jsx    # 設定頁
│   ├── router.jsx          # 簡單路由（React state切換）
│   └── app.jsx             # 入口元件
└── data.js                 # mock data
```

HTML裡按順序載入：
```html
<script type="text/babel" src="src/primitives.jsx"></script>
<script type="text/babel" src="src/components.jsx"></script>
<script type="text/babel" src="src/pages/home.jsx"></script>
<script type="text/babel" src="src/pages/detail.jsx"></script>
<script type="text/babel" src="src/pages/settings.jsx"></script>
<script type="text/babel" src="src/router.jsx"></script>
<script type="text/babel" src="src/app.jsx"></script>
```

**每個檔案末尾**都要`Object.assign(window, {...})`匯出要共享的東西。
