# 設計風格庫：網頁 20 種 + PPT 20 種（HTML 原生優先）

> **2026-06 重構**。基於對全球 10 大網站類型 + 10 大演示類型、各 top5 公認最佳設計（共 100 個真實案例）的調研反推。
> 舊版 20 種「平面/裝置設計師哲學」庫的致命問題：大膽風格幾乎全是 AI-生成-only（粒子/光影/手繪），**使用者預設無生圖能力、default 全走 HTML 時，大膽半場直接清零，只剩極簡——這是「default 千篇一律」的根因**。本庫每一種都標了「純 HTML/CSS 無生圖」下的**還原度**。
>
> ⚖️ **但記住定位**：這是**「沒思路時翻的彈藥」，不是「必須從這裡選」的清單**。使用者給了內容/品牌/參考，設計就從那裡展開，別套庫。skill 的職責是幫使用者規避最差，不是規定好設計長什麼樣——好設計從使用者的真實需求里長出來。

## 這個庫怎麼用

1. **先按輸出類型選半區**：做網頁/落地頁/官網 → 網頁 20 種；做 PPT/deck/演示 → PPT 20 種。
2. **溫度體系**：每種標了 `大膽 / 中性 / 安靜`。**故意讓大膽款佔多數**——模型的確定性偏差天然偏安靜極簡，庫的配比要把它往大膽推。
   - 方向 A（穩妥底盤）從安靜/中性裡按需求選；方向 B 取不同溫度拉反差；**方向 C 由 SKILL 的「秒數輪盤」強制注入大膽款**。
   - ❌ 三個方向不要都落在「米白+留白+一個點綴色」——那是最常見的失敗模式。
3. **還原度**：≥90% 閉眼做；70-90% 主體可做、個別細節降級；<70%（如 Memphis 做舊紋理）必須在產出裡**明確標註哪部分用純色塊降級**，不假裝能做出原版質感。
4. **字型**：每種給了開源替代（Inter/Geist/Manrope/Space Grotesk/Fraunces/Playfair 等），不要寫付費字型（Söhne/Circular 等）。
5. 配套：SKILL「設計方向顧問」Phase 3-5 用本庫推 3 方向；`assets/showcases/` 有預製截圖畫廊。

## 三軸校準（翻庫之前先定強度）

壓縮自 [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill)（MIT）的 dial 概念。沒有 design context、要從庫裡推方向時，先從 brief 讀出三個軸的檔位再去選半區和溫度——三軸管「多強」，溫度體系管「哪種氣質」：

- **變異度**（版面離安全預設多遠）：低＝對稱網格、居中；中＝錯位重疊、混合圖片比例；高＝masonry、fractional grid、大偏置留白。高檔位在 `<768px` 一律塌回單列。
- **動態強度**：低＝只有 hover/active；中＝transform/opacity 過渡＋載入級聯；高＝scroll-driven 編排（CSS `animation-timeline` 或 GSAP ScrollTrigger；**硬禁 `window.addEventListener('scroll')`**）。
- **視覺密度**：低＝畫廊式大留白（`py-32`+）；中＝日常 app（`py-16`～`py-24`）；高＝駕駛艙式緊湊、1px 分線、數字一律 `font-mono`。

| 情境 | 變異 | 動態 | 密度 |
|---|---|---|---|
| SaaS 主流 landing | 中高 | 中 | 中 |
| Agency／創意 landing | 高 | 高 | 低 |
| 高階消費品牌 | 中高 | 中 | 低 |
| 設計師作品集 | 高 | 中高 | 低 |
| 開發者作品集 | 中 | 中 | 中 |
| Editorial／Blog | 中 | 低中 | 低 |
| 公部門／合規敏感 | 低 | 低 | 中高 |
| Redesign（Preserve） | 跟現況 | 現況略升 | 跟現況 |

檔位是推薦起點：使用者點名的風格、既有 design context 永遠優先。

## 深度風格包（方向選中後加載）

三個方向有完整執行協議（精確色板、字型堆疊、元件規格、動效編排），選中後讀對應 pack，不要只憑庫裡的速查條目做：

| Pack | 氣質 | 適用 |
|---|---|---|
| `style-pack-minimalist.md` | 安靜｜暖單色編輯部極簡（Notion 系文件風） | 工作台/文件/知識產品、內容為主的官網 |
| `style-pack-brutalist.md` | 大膽｜瑞士工業印刷 或 軍規終端（兩模式擇一，不可混用） | 資料密集 dashboard、開發者作品集、宣言式編輯站 |
| `style-pack-soft.md` | 大膽/中性｜高階 agency 流（Ethereal Glass／Editorial Luxury／Soft Structuralism 三 vibe 擇一） | SaaS/AI 產品、生活方式品牌、組合作品集 |

---

## 色彩推導協議（用任何風格前先走這三步）

> ⚠️ **以下所有風格條目裡的 hex 是示例錨點，不是配方。** 同一風格用於不同內容，應通過本協議推匯出不同色值——直接複製條目 hex，只是在生產品味更好的 slop。為什麼：寫死配方讓 100 個使用者拿到 100 份同色產出，色彩的資訊量歸零；推導讓色彩成為「這個內容獨有」的證據。
>
> **字型同理**：條目裡的字型名也是示例錨點。選定風格後，display+body 配對先過 `references/typography.md` 的配對邏輯與「已被用爛名單」——**名單與條目衝突時以 typography.md 為準**（如條目寫 Fraunces，按名單換 Newsreader 等平替）。

### 三步法：取樣 → 收斂 → 論證

| 步驟 | 做什麼 | 為什麼 |
|------|--------|--------|
| **1. 取樣** | 主色從三個來源取，不憑空發明：①品牌資產（logo/已有 VI 直接吸色）②內容真圖（產品截圖/攝影素材裡的主導色）③文化語境（內容主題自帶的色彩記憶，見下表） | 憑空選色=從模型先驗裡抽籤，抽出來的永遠是那幾個網紅色；從內容裡採的色天然帶「為什麼」 |
| **2. 收斂** | 用 oklch 把調色盤壓到 **2-3 個有彩色 + 1 組中性色**。中性色寫成明度序列（如 L 0.15/0.35/0.65/0.92/0.98），有彩色之間拉開 oklch 色相角 H ≥60° 或明度 L 差 ≥0.3 | 色多必亂；oklch 的 L 通道感知均勻，明度序列寫出來就是層級系統，比一堆孤立 hex 可推理 |
| **3. 論證** | 一句話寫出「為什麼是這個色」，寫進產出註釋或交付說明。例：「主色取自使用者 logo 的赭石，壓低 chroma 到 0.08 模擬油墨」 | **寫不出這句話=你在抄配方。** 論證是防 slop 的自檢門，不是儀式 |

### 印刷色質感：為什麼低飽和比純螢幕色高階

油墨印在紙上永遠達不到螢幕 RGB 的最大飽和度——CMYK 色域更窄、紙張吸墨、環境光反射，都會把顏色「壓灰」。人眼幾十年被印刷品訓練出的「高階感」，本質是這層物理灰度。所以螢幕設計裡刻意壓 chroma，等於借用印刷的質感記憶。

| 用途 | oklch chroma 參考 | 效果 |
|------|------------------|------|
| 大面積底色 | 0.01–0.04 | 紙感、不刺眼 |
| 品牌主色/強調 | 0.08–0.15 | 油墨感，夠醒目但不塑膠 |
| 小面積點睛（按鈕/連結） | 0.15–0.22 | 保留活力，僅限小面積 |
| >0.25 滿版鋪 | 慎用 | 螢幕熒光感，只適合 Wrapped/糖果這類刻意「電子原生」的風格 |

### 文化語境速查：同一色相，不同語境

選色不只是選色相，是選它背後的文化座標。同是「紅」，落點差之千里：

| 色相 | 語境 A | 語境 B | 差在哪 |
|------|--------|--------|--------|
| 紅 | 故宮硃紅（偏橙、帶灰，oklch 低 L 低 C，比可樂紅更暗更濁）→ 傳統/莊重 | 可樂紅（高飽和正紅）→ 消費/興奮 | chroma 一降，從貨架跳到宮牆 |
| 藍 | 日本藍染/琉璃紺（深、偏紫灰）→ 手工/沉靜 | 科技藍 #0066FF 系 → SaaS/效率 | 後者是模型最愛的預設藍，用之前先問自己是不是在抽籤 |
| 綠 | 抹茶/苔綠（黃相、低飽和）→ 自然/日式 | 熒光綠 #39FF14 → 終端/hacker | 同為綠，一個喝茶一個敲程式碼 |
| 黃 | 藤黃/芥末（帶棕灰）→ 復古印刷 | 警示黃/Mailchimp 黃 → 醒目/玩味 | 灰度決定它是舊書頁還是安全帽 |
| 白 | 奶油紙白 #F5F0E8 → 出版物/暖 | 純白 #FFF → 實驗室/瑞士 | 底色的 2% 色溫差就是氣質分野 |

---

## 網頁風格庫(20種)

#### 大膽派

**媒體級粗野主義 Editorial Brutalism（巨號Helvetica壓小正文）** `大膽·還原98%`
- 參考:Bloomberg Businessweek（Richard Turley 2010-2014 改版，Code and Theory操刀）；Neue Haas Grotesk譜系
- 適配:媒體/內容出版、AI產品釋出、品牌官網hero、調研報告封面、觀點型長文頭圖
- 視覺DNA:配色純黑#000+純白#FFF+超連結藍#0000EE，點綴訊號橙紅#FF433D/終端綠#00A33E。字型Helvetica/Neue Haas Grotesk，120px+巨號headline左對齊緊字距直接壓住14px小正文，極端字號反差。佈局模組化網格+1px規則線分欄切割，高資訊密度刻意不留白。標誌元素：rule line分欄、超連結藍下劃線、黑白底大色塊。
- HTML實現:純CSS可1:1還原。CSS Grid做模組網格+border做規則線分欄，clamp()做超大響應式字號+letter-spacing收緊，系統Helvetica/Arial棧或Inter兜底，超連結直接#0000EE下劃線。零素材依賴。
- 字型:Inter（替Helvetica/Neue Haas Grotesk），程式碼用Geist Mono

**新粗野主義撞色資訊流 Neo-Brutalism（粗黑描邊卡片+高飽和撞色）** `大膽·還原95%`
- 參考:The Verge 2022 redesign（in-house team，PolySans + Mānuka）
- 適配:媒體/內容站、AI產品聚合頁、活動landing、社群榜單頁、小紅書風資訊卡
- 視覺DNA:配色電光紫#5200FF~品紅#E1306C高飽和主色+亮黃#F8E000強調+純黑#08080D+白，大面積撞色塊刻意不柔和。字型幾何無襯線大標題+襯線正文反差。佈局卡片化feed流、2-4px粗黑描邊、硬色塊分割槽、近乎無圓角。標誌元素：粗描邊卡片hover撞色翻轉、未完成介面氣質。
- HTML實現:純CSS強項。border:3px solid #000粗描邊+box-shadow硬投影偏移(4px 4px 0 #000)+grid/flex卡片流+:hover切換background撞色翻轉。無3D/光影障礙。
- 字型:Space Grotesk（替PolySans）+ 任一襯線如Fraunces

**孟菲斯復古拼貼最大化 Memphis Maximalism（撞色塊+錯位疊放+復古字型）** `大膽·還原72%`
- 參考:Gucci Vault概念店（Alessandro Michele）；Memphis設計運動 / Sagmeister叛逆基因
- 適配:電商概念店、創意活動頁、品牌實驗campaign、Y2K復古主題、節日營銷頁
- 視覺DNA:配色復古紅/芥末黃/寶藍/紫/橄欖綠大面積撞色並置+做舊米色暖底，濃烈刻意不和諧。字型復古襯線+裝飾字混用、印刷質感、打破網格錯位疊放。佈局反網格拼貼策展、模組大小不一錯落疊壓、像逛數字房間。標誌元素：撞色塊、錯位疊放、非常規導航彩蛋。
- HTML實現:transform:rotate()做錯位疊放+position:absolute疊壓+高飽和background撞色塊+復古Google Fonts。真實做舊紋理無法CSS還原，降級為純色塊+mix-blend-mode/contrast濾鏡模擬肌理，幾何拼貼版成立、archival做舊版會降級。
- 字型:DM Serif Display + Bungee（裝飾）+ Space Mono

**糖果色凸起立體按鈕遊戲化 Friendly Geometric Candy** `大膽·還原85%`
- 參考:Duolingo（Johnson Banks + Monotype，Feather Bold字型）；反矽谷極簡
- 適配:教育語言學習、消費級App landing、遊戲化產品、面向大眾親和產品、活動報名頁
- 視覺DNA:配色Duo綠#58CC02+鴨子黃#FFC800+天藍#1CB0F6糖果高飽和+白底，圓潤友好。字型超粗圓體（Feather Bold感）。佈局大圓角卡片、凸起3D按鈕（底部硬陰影=可按壓感）、吉祥物位+進度氣泡。標誌元素：3px實底陰影立體按鈕、按下位移動畫、超圓角。
- HTML實現:純CSS。box-shadow:0 4px 0生硬底陰影做凸起按鈕+:active translateY(4px)消陰影模擬按壓，border-radius大圓角，純色塊。吉祥物無生圖時用CSS幾何形或emoji佔位（輕微降級）。
- 字型:Baloo 2 / Nunito（超粗圓體替Feather）

**純CSS幾何插畫+響應式變形彩蛋 Pure-CSS Art** `大膽·還原80%`
- 參考:Lynn Fisher（lynnandtonic.com，純CSS藝術傳奇，Adobe專文報道）
- 適配:個人主頁、創意404/彩蛋頁、品牌玩味landing、技術部落格頭圖、設計師自我展示
- 視覺DNA:配色2-4色高對比扁平面（每個breakpoint換調色）。字型粗幾何無襯線標題。佈局核心是「圖隨視口變形」——一組CSS形狀在不同斷點重組成不同畫面（如建築隨屏寬變換層數）。標誌元素：純CSS繪製的幾何插畫、斷點驅動的重排彩蛋、零圖片。
- HTML實現:純CSS的炫技戰場，零素材是優勢。div+border-radius/clip-path/transform/box-shadow堆疊幾何形，@media斷點改變形狀尺寸位置實現變形。難度在設計構思而非技術，但需要精心手搓每個形狀。
- 字型:Rubik / Archivo（粗幾何替自定義）

**巨型字黑白高對比時裝大字報 Bold Big-Type Editorial** `大膽·還原88%`
- 參考:Jacquemus官網 / Rik Oostenbroek / Domestika；時裝雜誌大字報
- 適配:電商時尚、作品集、媒體專題、品牌宣言頁、影片課程封面、調研報告大字版
- 視覺DNA:配色極簡黑白+單一克制點綴色（裸粉#E8C4C0或正紅）。字型超大Display無襯線/高反差襯線，標題佔滿整屏。佈局全幅網格、巨字與負空間博弈、圖文1:1分割。標誌元素：屏佔比巨型headline、奢侈級留白、左右對位排版。
- HTML實現:純CSS完美還原。clamp()巨號字+CSS Grid全幅分割+大量padding留白+vh單位讓標題佔滿視口。無圖時用純色塊/文字塊替代時裝大片佔位（輕降級但版式成立）。
- 字型:Archivo Expanded / Anton（Display）+ Playfair Display（高反差襯線）

**復古未來太空圖錄 Cosmic Retro-Futurism** `大膽·還原75%`
- 參考:Perplexity Comet瀏覽器釋出站（The Brand Identity：Black/Blue/Cream；《2001太空漫遊》氣質）
- 適配:AI產品釋出站、科技品牌宣言頁、活動倒計時頁、未來感landing、概念釋出會
- 視覺DNA:配色純黑#0A0A0A+奶油紙白cream#F0EAD8+一抹鈷藍-孔雀藍#2B4F91，低飽和像老式天文圖錄。字型高反差襯線（古典天文圖冊感）+留白。佈局線描軌道/拋物線SVG、行星圓點、奶油底壓黑字、古籍式排印。標誌元素：SVG天體軌道線、奶油+藍+黑三色、復古襯線大字、天文圖錄質感。
- HTML實現:純CSS+SVG還原靜態版八成氣質。SVG path畫軌道拋物線+CSS徑向定位行星圓點+三色變數+高反差襯線。缺口是「太空落到地球」的全屏影片轉場（靈魂部分）——降級為CSS scroll視差+SVG軌道旋轉近似。
- 字型:Cormorant Garamond / EB Garamond（高反差襯線）+ Space Mono

**電影感聲波視覺化 Cinematic Sound-Viz Dark** `大膽·還原72%`
- 參考:ElevenLabs；電影片頭title sequence（Saul Bass式極簡動態）× 音訊工程介面
- 適配:音訊/語音AI產品、音樂科技站、播客平台、媒體釋出頁、影院級品牌hero
- 視覺DNA:配色純黑#000底+純白文字+藍紫漸變accent波形。字型大號無襯線標題Saul Bass式極簡。佈局全幅暗場、聲波/頻譜視覺化貫穿、巨標題壓波形、卡片功能區。標誌元素：彩色audio-waveform波形帶、電影片頭式極簡、高對比黑白+單漸變、聲音視覺化母題。
- HTML實現:純CSS+SVG還原70%氣質（骨架完美，波形是降級點）。SVG polyline畫靜態波形或多條不等高div柱陣+CSS animation做『假波形』跳動近似。缺口：隨聲音即時跳動的Web Audio/Canvas頻譜不可純CSS還原，靜態版像、動態靈魂還不了。
- 字型:Inter / Sora（大號無襯線）

**畫素遊戲橫版敘事 Pixel-Game Side-Scroller** `大膽·還原70%`
- 參考:Robby Leonardi互動簡歷（8/16-bit平台動作遊戲敘事，致敬任天堂SNES）
- 適配:創意簡歷/作品集、品牌玩味campaign、遊戲化landing、活動彩蛋頁、個人趣味主頁
- 視覺DNA:配色復古遊戲多段分割槽——森林綠#4CAF50草地+天藍#5DADE2，過渡太空紫#2C2A4A、火山橙紅#E8743B、海底青#1ABC9C，每『關卡』換一套高飽和卡通調色。字型畫素字型（8-bit感）+粗無襯線。佈局橫版/縱向滾動分關卡場景、視差分層、scroll觸發位移。標誌元素：分關卡換色、畫素美學、視差滾動、遊戲HUD式UI。
- HTML實現:純CSS+少量JS還原骨架（原作就是HTML+CSS+jQuery無WebGL）。視差分層position+scroll位移、image-rendering:pixelated、CSS逐幀background-position做sprite動畫、分段背景色。缺口：原創角色/場景手繪畫素插畫——無生圖時用CSS方塊拼簡易畫素圖示替代（美術降級，技術不降）。
- 字型:Press Start 2P / VT323（畫素字）+ Inter


#### 中性派

**包豪斯幾何標誌+扁平插畫系統 Bauhaus Geometric** `中性·還原90%`
- 參考:Khan Academy rebrand（六邊形+花瓣logomark + Wonder Blocks設計系統）；Bauhaus幾何構成
- 適配:教育課程站、品牌logo系統、資訊圖、兒童親和向產品、活動KV
- 視覺DNA:配色三原色譜系——包豪斯紅#E63946/黃#FFB703/藍#0077B6+黑白，純色塊拼接。字型幾何無襯線（圓潤幾何感）。佈局圓/三角/方基本幾何單元搭建插畫，對齊柵格、模組化拼圖。標誌元素：純幾何形態logomark、扁平無漸變插畫、原色塊構成。
- HTML實現:純CSS幾何全能。border-radius:50%做圓、clip-path/border三角形、方塊div拼幾何插畫，CSS Grid柵格對齊，純色fill無需素材。插畫用CSS形狀或內聯SVG幾何路徑手搓。
- 字型:Poppins / Manrope（幾何圓潤替Wonder Blocks）

**暗色雙色側欄開發者作品集 Dark Editorial（深底+單熒光accent+等寬字）** `中性·還原96%`
- 參考:Brittany Chiang（brittanychiang.com v4，dev portfolio事實標準）
- 適配:作品集個人主頁、開發者向產品、技術品牌站、簡歷頁、AI工具landing
- 視覺DNA:配色深墨綠/海軍底#0A192F+板岩灰文字#8892B0+單一熒光青綠accent#64FFDA。字型無襯線正文+等寬字（編號/標籤）。佈局左固定側欄導航+右滾動主區雙欄，section編號01/02、連結hover下劃線滑入。標誌元素：單accent色、等寬編號標籤、側欄錨點高亮。
- HTML實現:純CSS完全還原。position:sticky做固定側欄+CSS Grid雙欄+單accent變數+等寬字標籤+:hover下劃線transform滑入。零素材，純版式與微互動。
- 字型:Inter + JetBrains Mono（等寬）

**暖色出版物 Warm Editorial（奶油紙底+赤陶橙+襯線無襯線混排）** `中性·還原97%`
- 參考:Anthropic / Claude（DBCo + Geist Studio，Styrene×Tiempos）；Penguin/Pelican平裝書排印
- 適配:AI產品站、品牌官網、長文閱讀頁、橙皮書電子書、調研報告、培訓材料
- 視覺DNA:配色奶油紙底#F5F0E8+赤陶橙#CC785C/#D97757點綴+近黑文字#191919，溫暖低飽和。字型襯線標題（Tiempos感）×無襯線正文（Styrene感）混排。佈局書籍式單欄閱讀流、舒適行高、節制分隔線。標誌元素：紙感暖底、赤陶橙、出版級排印節奏。
- HTML實現:純CSS 100%還原，零素材。背景色變數+襯線無襯線字型棧混排+max-width限制閱讀寬度+line-height 1.7舒適行高。這是Anthropic赤陶橙暖色版的安全主場。
- 字型:Fraunces / Newsreader（替Tiempos襯線）+ Inter（替Styrene）

**Linear暗色發光+Bento網格 Glassmorphism Bento** `中性·還原85%`
- 參考:Linear / Cursor（'The Linear Look'現象級流派，Frontend Horse有程式碼配方）
- 適配:SaaS/AI產品站、開發者工具、技術品牌hero、產品功能展示、深色dashboard演示
- 視覺DNA:配色近黑底#08090A+去飽和藍紫品牌#5E6AD2+低飽和青紫微光漸變#4EA7FC→#B59AFF。字型幾何無襯線負字距緊湊。佈局便當盒bento網格分塊、髮絲分割線、玻璃擬態卡片。標誌元素：暗底發光漸變邊框、bento分塊、流光streamer、磨砂玻璃。
- HTML實現:純CSS強還原。box-shadow/filter blur+radial-gradient做發光暈，backdrop-filter:blur玻璃擬態，conic/linear-gradient邊框，CSS Grid拼bento。缺口僅「真實產品UI截圖」——用色塊+文字拼簡化假UI替代（這部分降級）。
- 字型:Inter / Geist（負字距）+ Geist Mono

**斜切流體漸變帶 Angled Fluid Gradient** `中性·還原92%`
- 參考:Stripe（標誌性angled gradient banner，Klim定製Söhne字型）
- 適配:SaaS/Fintech落地頁、品牌官網hero、產品釋出頁、活動banner、AI產品營銷頁
- 視覺DNA:配色多色流體漸變（靛藍#635BFF→青→粉→橙暖調）做hero背景+純白內容區+近黑文字。字型精緻無襯線（Söhne感）。佈局傾斜分割色塊（skew切角分割槽）、漸變hero壓結構化柵格正文。標誌元素：angled斜切邊界、多色流體漸變、理性柵格壓表達漸變。
- HTML實現:純CSS。transform:skewY()或clip-path:polygon()做斜切分割槽，linear-gradient多色疊加（可加CSS animation緩慢流動）做流體漸變帶，Grid做下方結構化正文。零素材。
- 字型:Inter / Hanken Grotesk（替Söhne）

**實用主義彩虹分類文件 Utility-First Colorful Docs** `中性·還原98%`
- 參考:Tailwind CSS Docs（Sky/Cyan品牌色+功能分類彩虹色相條）
- 適配:技術文件、API參考、設計系統站、教程站、開發者knowledge base、SaaS幫助中心
- 視覺DNA:配色Sky藍#38BDF8品牌+teal→cyan→sky青藍漸變+Slate灰階#0F172A/#64748B/#F8FAFC，文件用彩虹色相條區分功能分類（粉#EC4899/紫#A855F7/綠#10B981/橙）。字型清爽無襯線+等寬程式碼。佈局左側欄導航+中正文+右TOC三欄，彩色高亮程式碼塊、分類色標。標誌元素：青藍漸變hero、彩虹分類色、三欄文件骨架、語法高亮程式碼塊。
- HTML實現:純CSS 98%還原（它本身就是CSS框架文件）。Grid三欄+linear-gradient青藍hero+分類色變數+程式碼塊語法色用span著色。Inter開源，唯暗色切換/copy需輕量JS。零光影/3D/手繪。
- 字型:Inter + JetBrains Mono / Fira Code（程式碼）

**終端核軟未來 Terminal-Core Soft-Futurism（等寬字+等距立方）** `中性·還原80%`
- 參考:Cursor (Anysphere)；開發者終端美學 × Teenage Engineering工業極簡
- 適配:AI程式設計工具站、CLI產品landing、開發者基礎設施、技術品牌hero、終端類產品
- 視覺DNA:配色炭黑#0B0D14底+暖白文字#F2F0EF+克制藍紫漸變accent點綴按鈕與光暈。字型等寬字為主角（命令列感）+無襯線輔助。佈局命令列/程式碼塊前景、bento分割槽、2.5D等距cube示意。標誌元素：等寬字命令列、等距投影立方體、暖白×炭黑、克制漸變光暈、工業極簡。
- HTML實現:純CSS 80%還原。等寬字程式碼塊+暗色bento+box-shadow光暈；2.5D等距cube用CSS 3D transform(rotateX/Y+skew)或SVG等距投影手搓。缺口：可點選切換的多介面demo需JS+假UI拼接。無WebGL剛需。
- 字型:Geist Mono / JetBrains Mono（主角）+ Inter（輔助）


#### 安靜派

**功能主義網格社群 Functional Brutalism（灰線分割+系統字+藍連結）** `安靜·還原98%`
- 參考:Are.na / Lobsters / Quartz；Müller-Brockmann柵格數字落地 + Tufte資訊密度
- 適配:社群/UGC平台、內容聚合站、文件知識庫、移動優先內容流、極客向產品
- 視覺DNA:配色近白底#FBFBFB+黑文字+1px灰分割線#E0E0E0+經典連結藍#0000EE/已訪問紫。字體系統字棧（-apple-system/無裝飾）。佈局高密度資訊列表、細灰線分欄、極小留白、緊湊行距。標誌元素：髮絲灰分割線、藍連結、系統字、資訊密度優先。
- HTML實現:純CSS最易還原，這是Brutalist Web的本色。border-bottom:1px灰線列表+system-ui字棧+緊湊padding+藍連結。幾乎不需要任何素材或JS，純結構。
- 字型:system-ui系統字棧 / IBM Plex Sans（兜底）

**深色畫廊裱框 Gallery Dark（深黑負空間+單列大圖+EXIF小字）** `安靜·還原75%`
- 參考:Glass (glass.photo) / Bottega Veneta；美術館暗房 + Apple Photos內容至上
- 適配:攝影作品集、奢侈品電商、視覺內容沉浸展示、個人畫廊頁、高階產品陳列
- 視覺DNA:配色純黑底#0A0A0A+作品圖本身提供唯一色彩+極淡灰EXIF小字#666。字型極細無襯線小字。佈局單列居中大圖、巨幅負空間裱框、圖下metadata小字。標誌元素：暗房黑底、內容至上UI退隱、EXIF式小字註腳、大圖獨佔視口。
- HTML實現:純CSS還原版式骨架。純黑底+居中max-width單列+巨幅padding裱框留白+小字metadata。缺口是「真實攝影作品」本身——用佔位圖/純色塊代替則失靈魂，但暗房氛圍與版式100%可搭。
- 字型:Inter（細字重300）/ Cormorant（襯線奢侈感可選）

**Swiss極致黑白 Swiss Monochrome（Vercel式純黑白+Geist+銳利邊角）** `安靜·還原98%`
- 參考:Vercel / Next.js Docs（自研Geist已開源）；Massimo Vignelli少即是多
- 適配:開發者工具文件、技術品牌官網、AI產品站、SaaS落地頁、極簡調研報告
- 視覺DNA:配色純黑#000+純白#FFF+灰階#888，零彩色或僅一抹藍連結。字型Geist幾何無襯線+Geist Mono。佈局銳利直角（無圓角或極小）、高對比、精密柵格、克制留白。標誌元素：純黑白、銳利邊角、Geist字型、三角/箭頭幾何標記。
- HTML實現:純CSS 100%還原，Geist開源可直接引。CSS Grid精密柵格+純黑白變數+border-radius:0銳角+髮絲邊框。這是HTML最舒適的極簡主場，零素材依賴。
- 字型:Geist + Geist Mono（Vercel開源原版）

**日式留白白盒畫廊 Kenya Hara White Gallery** `安靜·還原80%`
- 參考:Cosmos (cosmos.so) / Aesop伊索官網；原研哉『白』的空寂 + 瑞士網格混血
- 適配:高階電商、創意畫廊、內容策展平台、設計師作品集、品牌精品店、moodboard站
- 視覺DNA:配色近全白#FAFAFA底+純黑文字#0A0A0A+極淡灰分割#EFEFEF，內容圖提供全部色彩、UI退到背景。字型極簡系統/幾何無襯線小字、大字距。佈局masonry瀑布網格、極致留白、淡灰髮絲分隔、東方空寂。標誌元素：白盒美學、奢侈留白、內容至上UI隱退、瀑布流策展。
- HTML實現:純CSS還原靜態版式（與暗色畫廊區分在『白』）。CSS columns或Grid做masonry+近白變數+大padding留白+淡灰分隔。缺口是Lenis/GSAP絲滑慣性滾動與圖片入場緩動（高階感60%在此），CSS僅基礎transition，動效層降級。
- 字型:Inter（細字重）/ Cooper Hewitt（Aesop同款開源）


## PPT風格庫(20種)

#### 大膽派

**新瑞士大字報 / Neo-Swiss Billboard Editorial** `大膽·還原98%`
- 參考:Scribe $75M、Flock Safety $47M 等 AI/SaaS 路演 deck 的 Big-Number Editorial 流派；Bloomberg Businessweek 資訊圖；Pentagram
- 適配:融資路演、QBR/業務回顧、年度趨勢復盤、產品釋出關鍵頁
- 視覺DNA:配色=純白(#FFFFFF)或近黑(#0A0A0A)底+單一高飽和強調色(電光藍#2D5BFF/熒光綠#00E676/品牌橙#FF6B2C)+中性網格線#E5E5E5。字型=超大粗體無襯線，標題佔半屏，數字tabular-nums等寬收緊字距。母版=①大色塊章節頁一個詞②巨型數字佔半屏(3.2x)+小注③左右分欄對比④全幅扁平折線/柱狀。標誌=billboarding大字、嚴格基線網格、大色塊章節頁
- HTML實現:超大數字用clamp()；嚴格網格用CSS Grid；大色塊章節頁background-color；折線柱狀用純div+CSS或內聯SVG(比貼圖更銳利)；數字對齊font-variant-numeric:tabular-nums。零插畫零3D
- 字型:Inter / Geist / Söhne替代Neue Haas Grotesk；數字配Geist Mono

**黑底巨型數字劇場 / Black Big-Number Stage** `大膽·還原97%`
- 參考:Steve Jobs 2007 iPhone Keynote、小米SU7 Ultra雷軍釋出會、Spotify Wrapped、Presentation Zen(Garr Reynolds)
- 適配:產品釋出主題演講、思想演示、全員town hall、情緒向年度回顧
- 視覺DNA:配色=純黑#000000底+純白#FFFFFF字高反差，一頁只一個品牌強調色高亮(小米橙#FF6900/Spotify綠#1ED760/Apple藍#2997FF)。字型=幾何無襯線粗體，一屏一詞或一個超大數字佔滿視野，字距收緊。母版=①標題頁黑底居中一行大字②資料高潮頁巨型數字+單位+一行注③左右參數對比雙欄(強調色vs灰)④slogan單頁。大量負空間
- HTML實現:黑底白字幾行CSS；巨型數字clamp()+flex居中；強調色highlight單獨span；左右對比CSS Grid兩列+條形高亮；tabular-nums。去掉產品照改純文字反而更接近Zen本質
- 字型:Geist / Inter / 思源黑替代SF Pro

**高飽和單色品牌撞色海報 / Mono-Brand Type-as-Hero** `大膽·還原96%`
- 參考:Spotify Wrapped視覺系統、Mailchimp Brand Book(Collins)、Netflix紅黑現代復刻、COLLINS品牌系統
- 適配:品牌/營銷策略、campaign宣講、town hall文化頁、活動主視覺
- 視覺DNA:配色=單一品牌主色滿版鋪底(Spotify綠#1ED760/Mailchimp黃#FFE01B/Netflix紅#E50914)+黑或白反差字，撞色兩層。字型=超大字型即主視覺(type-as-hero)頂天立地。母版=①滿色塊底+反白巨字②雙色塊上下/左右分割③巨型數字撐滿。標誌=單色滿版、字型當圖、高對比撞色
- HTML實現:滿版background-color；超大字clamp()佔滿；雙色用兩個100vh色塊；字型當圖靠font-weight900+負letter-spacing。純色塊零素材，HTML原生最爽
- 字型:Inter / Manrope / Archivo(超粗)替代Circular/Cavendish

**全幅漸變宣言版式 / Full-Bleed Gradient Manifesto** `大膽·還原82%`
- 參考:Zuora『Tell a Different Story』銷售deck(Andy Raskin拆解)、Nike『Just Do It』campaign、National Geographic跨頁
- 適配:銷售提案願景頁、品牌宣言、keynote轉折頁、使命願景單頁
- 視覺DNA:配色=滿版CSS漸變(暖橙→品紅/深藍→青)或純色出血+反白宣言大字+hashtag口號(#shifthappens)。字型=厚重無襯線全大寫標語橫貫。母版=①滿幅漸變+居中反白宣言②應許之地願景頁③客戶logo牆。標誌=full-bleed出血、反白大標語、hashtag口號
- HTML實現:linear-gradient/radial-gradient滿版(不做粒子/光影，純CSS漸變是允許的)；反白字position居中；logo牆用grid灰度SVG/文字佔位。原本靠紀實大照片的部分降級為CSS漸變鋪底+大字，照片缺失這一項還原度降約15%
- 字型:Archivo / Anton / Manrope(超粗)

**CS50單概念糖果舞台 / Candy-Color Lecture Stage** `大膽·還原94%`
- 參考:Harvard CS50(David Malan)、Lessig Method/高橋流、Presentation Zen
- 適配:教育課件、技術講座、概念解釋、程式碼教學
- 視覺DNA:配色=深黑底#0A0A0A+高飽和糖果色大字輪換(品紅#FF2D95/青#00E5FF/明黃#FFD500/綠#39FF14)。字型=無襯線超大字漂浮居中，一屏一概念，文字極少。母版=①深黑底單個糖果色大詞②等寬程式碼塊語法高亮③舞台聚光感大字。標誌=深黑漂浮糖果色大字、等寬程式碼高亮、強舞台聚光、極少文字
- HTML實現:深黑背景+單色超大字clamp()居中；程式碼塊用pre+等寬字+span上色做語法高亮；聚光感用極淡radial-gradient暗角(非粒子光效)。還原度高
- 字型:Inter超粗 + JetBrains Mono(程式碼)

**玩味手繪極簡 / Playful Maximalist Editorial (Collins式)** `大膽·還原75%`
- 參考:Mailchimp Brand Book(Collins 2018)、New Yorker漫畫氣質、Cooper圓潤襯線、Cavendish熒光黃
- 適配:有態度的品牌deck、創意機構提案、文化向town hall、反SaaS極簡的營銷頁
- 視覺DNA:配色=Cavendish熒光黃#FFE01B大面積+黑+少量撞色，反SaaS極簡。字型=Cooper式圓潤襯線大標題(playful)+雜誌式留白編排。母版=①熒光黃滿底+怪誕標題②雜誌式不規則留白排版③大字玩梗文案。標誌=熒光黃、圓潤襯線、playful編排、怪誕手繪氣質(降級為幾何色塊/emoji替代真插畫)
- HTML實現:熒光黃background；圓潤襯線font-family；雜誌留白用非對稱Grid。手繪猩猩/插畫這一核心元素無AI生圖無法做，降級為CSS幾何色塊+大號emoji+不規則transform旋轉的文字塊替代，插畫缺失還原度降約20%
- 字型:Fraunces(可調圓潤)/ Bree Serif替代Cooper；正文Inter

**不羈玩梗流行版 / Irreverent Pop (Reddit式)** `大膽·還原80%`
- 參考:Reddit Ads銷售deck(被Dock列為最有性格)、David Carson式不羈排版、90年代web復古、Memphis玩味
- 適配:Z世代品牌、玩梗營銷deck、社群/創作者向、敢於不正經的提案
- 視覺DNA:配色=Reddit橙紅#FF4500+撞色，90s web復古色。字型=混排/打破網格的David Carson式排版，玩梗口語文案。母版=①fun頁玩梗大字②facts頁節奏轉折嚴肅資料③口語標題。標誌=打破網格混排、橙紅、玩梗口語、fun→facts節奏反轉、復古web質感
- HTML實現:故意打破網格用transform旋轉/重疊定位/混合字號；橙紅+撞色塊；復古質感用粗黑邊border+硬陰影box-shadow(無blur)。自定義meme插畫降級為emoji+幾何拼貼，但混排排版本身HTML可還原
- 字型:Archivo / Space Grotesk + 混搭Inter製造對比

**Y2K膨脹大字 / Maximalist 3D-Type (Wrapped式)** `大膽·還原78%`
- 參考:Spotify Wrapped 2022/2023/2025、Memphis撞色、Y2K/Maximalism、duotone人像漸變
- 適配:年度回顧(情緒出圈向)、個性化資料卡、社交分享直式卡、品牌年終
- 視覺DNA:配色=高飽和撞色滿版背景(品紅+青+橙)+Spotify綠點睛+duotone雙色漸變。字型=頂天立地巨型數字，年份/數字做3D膨脹/金屬質感。母版=①撞色滿版+巨型膨脹數字②duotone人像/色塊底+反白大字③直式可分享卡。標誌=巨型膨脹3D數字、撞色滿版、duotone漸變、年份金屬質感、直式story卡
- HTML實現:撞色滿版background；3D膨脹數字用CSS text-shadow多層疊加+transform:perspective或SVG+stroke製造立體(非真3D渲染)；duotone用mix-blend-mode+漸變疊在灰度圖佔位塊上。金屬質感降級為漸變填充文字background-clip:text，還原度降約15%
- 字型:Archivo Black / Anton超粗 + 數字Clash Display


#### 中性派

**Bento便當格模組網格 / Bento Grid** `中性·還原95%`
- 參考:Apple Keynote Bento Grid時代、新一代MBB Bento/Big-Type deck(2024-2026)、Stripe年報指標卡矩陣、Pitch.com QBR模板
- 適配:產品功能彙總、諮詢/QBR資料彙報、銷售成果頁、town hall指標頁
- 視覺DNA:配色=淺灰/奶白底(#F5F5F7/cream)或近黑底+品牌主色+1-2強調色，卡片淺色分割槽底+圓角+微描邊/微陰影。字型=超大display標題+常規正文，字重對比強烈，KPI數字tabular figures。母版=①標題頁巨型單句+留白②bento頁2×2/3列不等高卡片每卡一洞見(數字/線性icon/sparkline)③one-insight超大數字頁。標誌=不等高卡片網格、圓角微描邊、呼吸感
- HTML實現:CSS Grid的grid-template-areas做不等高bento；卡片border-radius+box-shadow微陰影+1px hairline；sparkline用內聯SVG；線性icon用inline SVG stroke。零貼圖
- 字型:Inter / Geist + 數字Geist Mono

**Neo-Swiss暗色終端美學 / Dark Hairline Terminal** `中性·還原94%`
- 參考:Linear pitch deck、Vercel設計語言、CS50深黑舞台課件；字型Inter Tight+JetBrains Mono
- 適配:開發者工具/技術產品釋出、技術路演、工程向彙報
- 視覺DNA:配色=近黑底(#0D0D0F/#111113)+hairline細線#262629網格+單一紫藍強調(#5B5BD6/#7C7CFF)。字型=Inter Tight大標題+JetBrains Mono做標籤/資料。母版=①極簡標題頁一句話+mono小標②hairline分隔的資料網格③mono標籤的特性列表。標誌=1px細線網格、mono單等寬標籤、極致留白、近黑非純黑
- HTML實現:近黑背景+border:1px solid的hairline網格；mono標籤用等寬font-family；微光用極淡box-shadow/border highlight而非真光效(降級避開賽博霓虹禁區)。注意避開#0D1117深藍禁區，用中性近黑
- 字型:Inter Tight + JetBrains Mono / IBM Plex Mono

**雙字型諮詢版 / Two-Font Consulting (Bower式)** `中性·還原90%`
- 參考:McKinsey 2019品牌系統(Wolff Olins設計，Bower襯線+無襯線)、BCG Executive Perspectives、深藍細線pattern
- 適配:諮詢報告、高管彙報、行業研究、權威機構提案
- 視覺DNA:配色=深藍(#051C2C/McKinsey深藍)×白二元+單一品牌色高亮(BCG綠#00805A)，暖灰底帶呼吸感。字型=characterful襯線大標題(Bower式)與無襯線正文高對比並置。母版=①左上角結論式action-title②藍色細線pattern裝飾③雜誌式左右分工(結論文字+視覺)④大數字data-point卡。標誌=襯線×無襯線高對比、深藍細線pattern、action-title、暖灰高階感
- HTML實現:雙字型font-family並置(襯線標題+無襯線正文)；細線pattern用repeating-linear-gradient或SVG line；data-point卡純CSS；照片灰度處理這一項無照片可省。藍紫edge shimmer降級為純色邊
- 字型:Playfair Display / Fraunces襯線標題 + Inter正文(替代Bower)

**圖譜箭頭企業版 / Diagram-Driven Isotype** `中性·還原88%`
- 參考:Salesforce銷售deck、Isotype(Otto Neurath)譜系、Gene Zelazny《Say It With Charts》、Hans Rosling/Gapminder
- 適配:平台/架構講解、客戶旅程、流程方法論、生態地圖
- 視覺DNA:配色=企業藍色塊+產品線分色區分+圖示化能力網格。字型=清晰無襯線。母版=①橫向客戶旅程箭頭流②分層平台架構圖③圖示化能力網格④2×2/瀑布/金字塔結構圖。標誌=箭頭流程、分層架構盒、Isotype圖示網格、流程即敘事
- HTML實現:箭頭流程用Flexbox+CSS clip-path三角或SVG arrow；架構分層用巢狀帶邊框div；圖示用inline SVG stroke統一描邊；瀑布/金字塔用Grid+斜切。氣泡圖可用CSS圓形+定位。純向量繪製
- 字型:Inter / IBM Plex Sans(圖表友好)

**單圖母圖概念圖解 / Diagrammatic Minimalism** `中性·還原95%`
- 參考:Simon Sinek黃金圓環(Golden Circle)TED、Bauhaus幾何抽象、資訊建築『一圖定全場』
- 適配:理論框架講解、TED式思想傳播、模型/方法論視覺化、單概念keynote
- 視覺DNA:配色=極簡白/淺底+黑+1個強調色，幾何純色。字型=無襯線，標籤大寫嵌入圖形。母版=①唯一幾何母圖(同心圓/三角/矩陣)承載全部概念②由內向外箭頭③對比案例。標誌=單一幾何母圖、巢狀同心圓/三角、大寫標籤、一圖承載概念
- HTML實現:同心圓用border-radius:50%巢狀div或SVG circle；三角用clip-path/SVG polygon；箭頭SVG marker；標籤absolute定位貼在圖形上。純幾何，HTML完美還原
- 字型:Manrope / Futura系(Jost開源替代)幾何感

**Sparkline敘事波形 / Narrative Sparkline (Duarte式)** `中性·還原91%`
- 參考:Nancy Duarte《Resonate》Sparkline敘事圖譜、Al Gore《An Inconvenient Truth》、Duarte Inc.資料敘事
- 適配:演講結構設計、變革敘事、before/after對照、資料故事弧線
- 視覺DNA:配色=深底或白底+品牌橙強調轉折點+灰化對照。字型=無襯線，annotation標註點。母版=①橫貫全屏的振盪波形線②波形上text標註點③上下並置對照波形④全黑底孤懸一條資料線⑤逐步reveal。標誌=橫貫波形線、波形標註點、橙色轉折、對照波形、爬出畫面的曲線
- HTML實現:波形線用內聯SVG path(平滑貝塞爾)；標註點用SVG circle+text定位；對照波形上下兩條path；reveal用CSS動畫stroke-dashoffset。純SVG繪製無素材
- 字型:Inter + 數字Geist Mono


#### 安靜派

**斷言-證據 / Tufte資訊設計** `安靜·還原93%`
- 參考:Michael Alley Assertion-Evidence(Penn State實證)、McKinsey/BCG action-title、Edward Tufte資料墨水比、Barbara Minto金字塔原理
- 適配:學術/工程彙報、資料嚴謹型諮詢頁、政策研報、技術評審
- 視覺DNA:配色=白/極淺灰底+黑正文+單一克制強調色(深藍/磚紅)。字型=整句話標題(非名詞短語)，標題下獨佔一張圖，文字標註嵌進圖裡。母版=①整句action-title②標題下單圖證據③零bullet。標誌=整句標題、單圖證據、嵌入式標註、零chartjunk、高資料墨水比
- HTML實現:整句標題靠排版層級；圖表用純CSS/內聯SVG畫極簡折線散點(去網格線去圖例，標註直接text定位在資料點旁)；零裝飾。Tufte的克制正是HTML強項
- 字型:Source Serif / Lora標題 + Inter正文(雙字型閱讀級)

**瑞士機構極簡 / Institutional Swiss Minimal** `安靜·還原96%`
- 參考:Sequoia官方10頁pitch模板、Airbnb 2009種子輪deck、Müller-Brockmann網格、Massimo Vignelli
- 適配:投資路演、標準商業提案、問題-解法敘事、品牌去裝飾提案
- 視覺DNA:配色=純白底+黑灰正文+單一品牌強調色(Airbnb珊瑚紅#FF5A3C/中性藍)。字型=Helvetica系無襯線，標題中號粗體一句話，正文短句大間距。母版=①居中logo+slogan②頂部一句話標題帶+下方3欄對仗(Problem/Solution三點)③TAM大數字分層④2×2競品矩陣。標誌=頂部標題帶、三欄對仗、單色強調、2×2矩陣
- HTML實現:Flexbox三欄對仗；2×2矩陣純CSS Grid+border畫；TAM分層用巢狀div或同心方塊；一頁一資訊。幾乎純排版網格，HTML理想物件
- 字型:Inter / Helvetica Now替代Helvetica；正文Inter

**雜誌編輯長文流 / Editorial Longform** `安靜·還原95%`
- 參考:Stripe Annual Letter($1.9T)、Amazon六頁敘事備忘錄、Benedict Evans『X eats the world』、Stripe Press
- 適配:年度信/復盤敘事、深度思想長文、內部更新、研報型閱讀物
- 視覺DNA:配色=奶白/米白底(#FBFAF8)+深墨字+品牌色點睛(Stripe紫#635BFF)。字型=襯線或高品質無襯線，散文體段落+內聯資料卡，超大display數字穿插。母版=①刊頭大標題②多欄散文+內聯指標卡③超大數字段落錨點。標誌=出版物閱讀節奏、內聯資料卡、克制留白、散文體而非bullet
- HTML實現:多欄column-count或Grid；內聯資料卡float/inline-block嵌入正文；襯線正文max-width控制行寬65ch；超大數字穿插。純排版，零素材
- 字型:Newsreader / Source Serif正文 + Inter輔助；數字tabular

**人文圓角卡片 / Humanist Rounded Cards (Khan式)** `安靜·還原80%`
- 參考:Khan Academy Wonder Blocks設計系統、Source Serif Pro襯線、森林綠品牌、友善人文主義
- 適配:教育產品、親和力課件、公益/非盈利deck、溫暖品牌提案
- 視覺DNA:配色=森林綠#14BF96/#0A5C4B+米白底+暖色輔助，柔和不刺眼。字型=Source Serif襯線標題(人文氣)+無襯線正文。母版=①圓角卡片元件組②襯線標題+親和正文③真實攝影位(降級為綠色系幾何/圓角色塊)。標誌=森林綠、襯線標題、大圓角卡片、人文溫暖、不完美親和質感
- HTML實現:大圓角border-radius卡片+柔和box-shadow；襯線標題font-family；暖米白底。真實師生攝影這一項無AI生圖，降級為綠色系幾何插畫塊/大圓角純色佔位+emoji人物，照片缺失還原度降約18%
- 字型:Source Serif 4標題 + Nunito Sans / Inter正文(Nunito圓潤呼應人文)

**研報密集圖表 / Dense Research Report (Meeker式)** `安靜·還原92%`
- 參考:Mary Meeker《Internet Trends》(BOND)、CB Insights《State of AI》、McKinsey Global Institute《Year in Charts》、FT/Bloomberg資料新聞
- 適配:趨勢研報、行業資料復盤、密集資料彙報、市場地圖
- 視覺DNA:配色=白底+品牌色(BOND/CB Insights亮藍#0066FF)階梯單色高亮其餘灰化，幾乎零留白。字型=結論式句子標題，每頁1圖密度，極小來源腳註。母版=①結論句標題+滿頁單圖②logo網格market map③大數字KPI卡④密集多圖網格+腳註。標誌=結論句標題、零留白研報感、單色階梯高亮、logo市場地圖、來源腳註規範
- HTML實現:密集圖表全用純CSS/內聯SVG畫(柱/折線/堆疊/散點)；logo market map用Grid+文字/SVG佔位格；KPI卡CSS；腳註小字。極致資訊密度正是HTML擅長，零素材
- 字型:Inter + IBM Plex Sans + 數字tabular Geist Mono

**純文字宣言備忘錄 / All-Text Manifesto (Netflix/Amazon式)** `安靜·還原97%`
- 參考:Netflix Culture Deck(2009，125頁)、Amazon六頁敘事備忘錄(Bezos)、Tufte反PowerPoint主張、Matthew Carter閱讀級排印
- 適配:文化宣言、價值觀宣講、深度備忘錄、反PPT的純文件演示
- 視覺DNA:配色=純白或純黑底+單一強調色(Netflix紅#E50914)做唯一高亮，極致克制。字型=閱讀級排印，一頁一觀點金句斷言/純散文零bullet零圖。母版=①滿版底+金句斷言②口語化坦誠段落③制度名詞高亮(Keeper Test)④六頁散文+附錄表。標誌=純文字一頁一觀點、零圖零bullet、單色高亮金句、口語坦誠、silent-read文件感
- HTML實現:純排版：金句用大字clamp()左對齊層級；散文max-width控制行寬；唯一強調色span高亮關鍵短語；附錄用極簡table。零素材零圖，純文字是HTML最穩的還原
- 字型:Newsreader / Source Serif(閱讀級)或Inter(宣言式)；標題可Archivo超粗


---

## ⚠️ AI 生圖專用風格（僅在確認使用者有生圖能力時才推，default 不可選）

下面這些風格的靈魂在**動態生成視覺 / 3D / 粒子 / 電影級光影 / 手繪插畫**，純 HTML/CSS 無生圖下只能做出嚴重劣化的 mock，**從 default 推薦池剔除**。使用者明確有生圖能力（走 `huashu-gpt-image`）時才作為候選：

| 風格 | 靈魂 | 為什麼 HTML 做不了 |
|------|------|------------------|
| Active Theory（WebGL 粒子） | 3D 粒子系統/即時渲染 | 純 CSS 無法 |
| Field.io（生成藝術） | 演算法生成圖形 | 靜態 SVG 只能做僵化簡化版 |
| Resn（插畫互動） | 角色插畫+遊戲化 | 依賴手繪素材 |
| Zach Lieberman（即時生成） | creative coding 筆觸 | 依賴即時生成 |
| Raven Kwok（分形參數） | 遞迴分形 | CSS 做不出複雜度 |
| Ash Thorp（電影光影） | 電影級體積光/概念美術 | CSS 光影是劣化 |
| Territory Studio（FUI 全息） | 科幻全息介面 | 依賴大量發光層疊素材 |
| Neo Shen（水墨暈染） | 水墨有機暈染 | CSS 漸變≠水墨 |
| Sagmeister & Walsh（色彩爆發） | 手作實物+實驗排版 | 撞色骨架可做（已併入網頁「Memphis/孟菲斯」與 PPT「單色撞色海報」），手作質感做不了 |

> 這些款不是「不好」，是「載體不對」——它們的原生載體是 AI 直出圖，不是瀏覽器 DOM。

---

## 預設審美禁區（使用者可按自己品牌 override）

- ❌ **GitHub-dark 偷懶解**：均勻深藍底（#0D1117）+ 通用青/紫霓虹 glow——只禁這一種爛大街組合，不是「暗色一律禁」
- ✅ **不在禁區**：電影級戲劇光影、暖色賽博（Ash Thorp 橙/青）、運動詩學暗場敘事——有作者意圖的暗色保留（本庫「Linear 暗色發光」「黑底數字劇場」「CS50 糖果舞台」都是合法暗色）
- ❌ 激進紫漸變萬能公式、emoji 當圖示、圓角卡片+左彩 border accent（除非品牌本身用）
- ❌ 封面圖加個人署名/水印

---

## 有生圖能力時的提示詞心法（Mood, Not Layout）

> 僅當走 AI 生圖路徑時適用；HTML 路徑直接按上面各風格的「HTML 實現」寫程式碼。

短提示詞 > 長提示詞。描述情緒和內容，比堆 30 行佈局細節有效。

| 殺死多樣性的寫法 | 激發創造力的寫法 |
|----------------|----------------|
| 指定顏色比例（60%/25%/15%） | 描述情緒（"warm like Sunday morning"） |
| 規定佈局位置 | 引用具體美學（"Pentagram editorial feel"） |
| 列出所有視覺元素 | 描述觀眾應該感受到什麼 |

完整 AI 生圖方法論 → `huashu-gpt-image` skill。

---

**版本**：v3.0（2026-06 全面重構為 HTML 原生 40 種庫）
**適用**：網頁/PPT/PDF/資訊圖/封面/App 等所有視覺設計的 default HTML 路徑
