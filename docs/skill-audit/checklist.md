# Skills 簡化清單

目前完成優化：**3 / 62**。ultrathink 已經使用者確認並要求推送。每次只處理一個 skill，實際修改、必要驗證並經使用者確認接受後，才勾選該項。

審查範圍：目前 repository 的 `plugins/*/skills/*`，共 62 個 skills、10 個 plugins。不是本機所有第三方已安裝 skills 的清單。已逐一閱讀全部 SKILL.md，涉及重複、相依或矛盾的建議另查相關 references、模板或腳本；這不是所有附屬檔案逐行審計，也未實測所有技能的執行效果。

依據：[Eric Provencher：Rethinking skills and prompts for GPT-6 Astra](https://x.com/pvncher/status/2095991462416490862)。文章提醒縮短並精確描述適用情境、只在需要時讀取細節、減少過度固定的流程，以及清楚界定完成條件和需要停下來的決策。下列各項是對本 repo 的審查判斷，不是作者對這些 skills 的評語。

## 建議先處理的五個

| 順序 | 項目 | 先處理的理由 |
| --- | --- | --- |
| 1 | #54 ultrathink | 每個決策都跑六種語言及整套檢核，額外工作最明顯。 |
| 2 | #53 subtraction-thinking | 每次輸出都增加前中後審查與固定提醒。 |
| 3 | #60 human-writing | 幾乎每個回覆都會觸發，而且短主檔仍要求讀五份文件。 |
| 4 | #59 design-studio | 多階段確認、文件、多版本與模型品牌判定集中在同一流程。 |
| 5 | #29 software-engineering-guidelines | 日常開發都會載入，且與專案及其他技能重複要求。 |

高優先 35 項、中優先 25 項、低優先 2 項。優先度代表觸發範圍、額外工作與相依影響，不代表技能無用，也不代表每一條建議都應採用。

## 怎麼使用這份清單

- **合併文字**：重複定義保留一份，必要例子改成按需查閱。保持原有功能與規則。
- **調整行為**：縮小觸發、改預設輸出、取消固定數量或例行確認，都先確認該 skill 的具體改法。
- **修正矛盾**：檔名、公式、評分與格式相容性問題另做對應驗證，不能把字數減少當成修好了。
- **完成條件**：保留約定功能，檢查相對連結、frontmatter、skill/plugin 版本與必要的 README 連動。用正常請求、局部修改、資料不足等與該次變更相關的情境，確認不會誤觸發、卡住或擴大工作。沒有腳本或行為變更時不硬加測試。

不設定統一字數或刪減比例。完整課堂格式、安全限制、工具特有格式及使用者刻意設定的偏好，不能只因文章建議簡化就取消。現有 repo 要求 description 含 MUST；可以先保留 MUST 並縮窄其適用條件，無須先重寫整份 AGENTS.md。

## 逐項清單

### business-strategy

- [ ] **01. bcg-growth-share-matrix**（中優先）

  **可以改哪裡：** 觸發列表重複 description；分類規則與 references/01 重複；八大輸出主體、90 天追蹤與四份參考檔每次必讀，讓簡單分類也變成完整資本配置報告。

  **建議改法：** 主檔保留市場口徑、公式、門檻與例外判讀；欄位明細移到模板；快速分類只出座標/象限/依據，要求配置時才產出資本方案與追蹤；參考檔改按分類、策略、例外需求讀取。

  **應保留：** 最大競爭者分母、成長門檻來源、邊界敏感度、Dogs 協同例外與 Question Marks 投資停止條件。

  **原文位置：** [主檔:22](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:22)、[主檔:87](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:87)、[主檔:122](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:122)、[主檔:198](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:198)、[主檔:206](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:206)。

- [ ] **02. business-model-architect**（高優先）

  **可以改哪裡：** 八個必要輸入連 WT 都列缺一不可；宣稱九個主體實列十個；四份擴充輸出重述九要素；震央決定順序卻另強制不得跳序；固定至少三策略三實驗與七張臉孔擴大每次工作。

  **建議改法：** 分核心商模與完整驗證兩種交付深度；九要素整合成一表，foundation/四構面/operating/WT 只在需求涉及時展開；震央控制設計次序，輸出順序可另固定；缺口只擋受影響結論；同步 references/06 模板與評分，消除多處契約漂移。

  **應保留：** 九要素連貫、核心要素較深入、事實與假設區分、具成功指標的驗證實驗。

  **原文位置：** [主檔:34](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:34)、[主檔:73](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:73)、[主檔:99](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:99)、[主檔:110](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:110)、[主檔:159](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:159)、[主檔:191](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:191)、[主檔:226](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:226)。

- [ ] **03. decision-bias-quality-control**（中優先）

  **可以改哪裡：** 泛提案審查與個人選擇容易觸發；每次先讀五份檔且所有模式都強制十二題逐題量化與固定三至五項，會把會議引導變成評分報告；評分摘要與 references/04 重複。

  **建議改法：** 縮到明確偏誤品管/重大決策方法需求；主檔保留模式入口和十二問證據檢查，題庫與評分只讀一次權威來源；會議/教練可先交關鍵追問，正式評分模式再展開雙軌和完整計算。

  **應保留：** 十二問方法本體、證據支持、團隊共識不可推定；完整評分時保留可重算規則。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:3)、[主檔:22](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:22)、[主檔:76](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:76)、[主檔:95](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:95)、[主檔:107](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:107)、[主檔:124](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:124)。

- [ ] **04. pestel-analysis**（高優先）

  **可以改哪裡：** description 混入執行評分；六面向教科書問句和案例常駐；每面向硬找三至五候選；SWOT 輸入包與末尾移交包重複且即使只要 PESTEL 也產出。

  **建議改法：** description 只描述 PESTEL/總體環境用途；掃描題庫、評分表與長案例移 references；六面向檢查但不硬湊數；因素表只保留一份，只有要接 SWOT 才建立一次移交包；來源未可核對的法規範例改成清楚的假設示例或補來源。

  **應保留：** 分析地區與時間、來源、具體影響機制、可解釋的優先排序與中性因素條件。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:3)、[主檔:41](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:41)、[主檔:122](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:122)、[主檔:167](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:167)、[主檔:203](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:203)、[主檔:243](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:243)、[主檔:272](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:272)。

- [ ] **05. red-flag-contract-scanner**（中優先）

  **可以改哪裡：** description 堆疊契約類型與關鍵詞；主檔內嵌整份報告模板；超過三十頁直接當可能不完整、首輪強制問格式且已有預設；硬綁 /mnt/skills/public/docx 與 message_compose_v1。

  **建議改法：** 壓縮為不利條款審閱用途及兩三種辨識訊號；報告骨架移用既有 assets；只在實際截斷時追問，按既定預設直接交付；依現有 Word 能力產檔；無關且未出現條款不逐一占正文，保留實質缺漏；法律提醒集中一次。

  **應保留：** 原條文位置與引用、司法管轄區不確定性、具體協商改法與不代替使用者決定簽約。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:3)、[主檔:25](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:25)、[主檔:58](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:58)、[主檔:66](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:66)、[主檔:72](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:72)、[主檔:76](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:76)、[主檔:134](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:134)、[主檔:159](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:159)。

- [ ] **06. swot-analysis**（高優先）

  **可以改哪裡：** 觸發範圍含 PEST 與一般競爭策略；無論證據是否足夠都強制先跑 PESTEL 並停下；窮舉所有元素配對、固定選一主策略與放棄清單；策略定調卡重複輸出。

  **建議改法：** 縮到 SWOT/TOWS 工作；允許直接承接已有可信外部證據，缺總體掃描才補 PESTEL；按實質相關性配對而不窮舉；只在策略選擇需求展開評分/取捨；保留一份策略表，長教程、示例與定調卡移參考檔/模板。

  **應保留：** 比較基準、S/W 與 O/T 來源、策略與來源元素連結、不是數項目決定態勢。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:3)、[主檔:50](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:50)、[主檔:77](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:77)、[主檔:132](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:132)、[主檔:180](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:180)、[主檔:234](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:234)、[主檔:280](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:280)。

### customer-insight

- [ ] **07. customer-journey-mapper**（高優先）

  **可以改哪裡：** 可選情緒模組連 matplotlib/Chart.js 與固定五欄尺寸都常駐，與自訂階段政策衝突；主檔三處重述表格行序；缺完整 persona 強制轉交，和快速草稿條款界線不清；範例情緒加減分多筆與公式不符。

  **建議改法：** 主檔只保留核心旅程欄位與客戶視角；情緒評分、Word 與聊天渲染各按需讀 reference，尺寸由實際階段數推導；允許足以界定客群的輸入，資料不足才補 persona；表格骨架只維護一次；修正範例算式，明示推估分數而非實測。

  **應保留：** 動機先於行動、使用者自訂階段、情緒與接觸點連結、handoff 使用者覆寫優先。

  **原文位置：** [主檔:20](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-journey-mapper/SKILL.md:20)、[主檔:86](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-journey-mapper/SKILL.md:86)、[主檔:124](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-journey-mapper/SKILL.md:124)、[主檔:171](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-journey-mapper/SKILL.md:171)、[主檔:194](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-journey-mapper/SKILL.md:194)、[主檔:205](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-journey-mapper/SKILL.md:205)、[主檔:267](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-journey-mapper/SKILL.md:267)。

- [ ] **08. customer-persona-framer**（中優先）

  **可以改哪裡：** persona-only 本身簡潔；journey-framing 固定 Persona、5W1H、五元素、階段及 handoff 多次重述同一資料；快速版固定三至五假設容易湊數。

  **建議改法：** 保留 persona-only/journey-framing 分流，前置分析整合為一張可直接交接的客群與旅程資料表；只有教學或簡報需求才展開 5W1H；未知項按實際缺口標示，不固定假設數量。

  **應保留：** 不得捏造人口背景、可觀察行為/限制、persona-only 不追加旅程、下游必要欄位。

  **原文位置：** [主檔:23](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-persona-framer/SKILL.md:23)、[主檔:56](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-persona-framer/SKILL.md:56)、[主檔:78](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-persona-framer/SKILL.md:78)、[主檔:115](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-persona-framer/SKILL.md:115)、[主檔:170](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-persona-framer/SKILL.md:170)。

- [ ] **09. orchestrating-mixed-methods**（高優先）

  **可以改哪裡：** 泛研究/分析/診斷甚至 what/why 問句都是入口，會套到大量單方法任務；強制輸出長 YAML 與未採用路線理由；五維判斷、路線定義、workflow、禁例及 references/01 重複。

  **建議改法：** 限縮至需要選方法、安排質性與量化研究順序或整合兩類證據；已指定方法則不載入；主檔用短決策表，複雜 tie-breaker 留 reference；一般只用一句方法及理由，結構化路由僅供真正下游工具需要。

  **應保留：** 最小可行方法、缺某軌不能宣稱混合證據完成、相互矛盾證據不平均掩蓋。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/customer-insight/skills/orchestrating-mixed-methods/SKILL.md:3)、[主檔:31](/Users/timlai/Developer/skills/plugins/customer-insight/skills/orchestrating-mixed-methods/SKILL.md:31)、[主檔:62](/Users/timlai/Developer/skills/plugins/customer-insight/skills/orchestrating-mixed-methods/SKILL.md:62)、[主檔:89](/Users/timlai/Developer/skills/plugins/customer-insight/skills/orchestrating-mixed-methods/SKILL.md:89)、[主檔:105](/Users/timlai/Developer/skills/plugins/customer-insight/skills/orchestrating-mixed-methods/SKILL.md:105)、[主檔:150](/Users/timlai/Developer/skills/plugins/customer-insight/skills/orchestrating-mixed-methods/SKILL.md:150)、[主檔:180](/Users/timlai/Developer/skills/plugins/customer-insight/skills/orchestrating-mixed-methods/SKILL.md:180)。

- [ ] **10. product-conjoint-analysis**（高優先）

  **可以改哪裡：** description 排除純問卷但內文要求評分問卷切 OLS；五階段、報告、口頭 checklist 重複；所有分析強制四種洞察，即缺成本也用以一元代填；實際商品一律拆模型的案例經驗被寫成普遍規則。

  **建議改法：** 收斂至已宣告的觀察資料範圍，問卷只留轉向提示；公式/程式/案例移已有 references 和 scripts，主檔留決策點；WTP、ROI、機率只在資料與估計可支持時產出；拆模型改成診斷後選擇，不能把簡化當修復統計識別。

  **應保留：** 參考層編碼、價格尺度換算、評論選擇偏誤、真實獨立樣本數、估計限制；模型方法修正需另做專業驗證，不能只刪文。

  **原文位置：** [主檔:53](/Users/timlai/Developer/skills/plugins/customer-insight/skills/product-conjoint-analysis/SKILL.md:53)、[主檔:116](/Users/timlai/Developer/skills/plugins/customer-insight/skills/product-conjoint-analysis/SKILL.md:116)、[主檔:157](/Users/timlai/Developer/skills/plugins/customer-insight/skills/product-conjoint-analysis/SKILL.md:157)、[主檔:197](/Users/timlai/Developer/skills/plugins/customer-insight/skills/product-conjoint-analysis/SKILL.md:197)、[主檔:261](/Users/timlai/Developer/skills/plugins/customer-insight/skills/product-conjoint-analysis/SKILL.md:261)、[主檔:309](/Users/timlai/Developer/skills/plugins/customer-insight/skills/product-conjoint-analysis/SKILL.md:309)。

- [ ] **11. review-mining-stp**（高優先）

  **可以改哪裡：** 理論定義、抽取、workflow、Hard Rules 多處重複；完整 schema 與報告契約占主檔且 references/05 已有；四理論只能用/可擴充互相矛盾，必須全覆蓋與資料不足標缺口不一致。

  **建議改法：** 主檔保留上游評分/下游腳本界線、雙軸及入口，理論字典/欄位schema/各統計模式契約按需讀；四家族與數量以證據支持為限，統一擴充規則；讓給讀者的報告摘要與機器重現附件分層，重複規則只留單一權威來源。

  **應保留：** salience 0–7、quality 0–10、缺 salience 留空 quality、凍結屬性、原文 review_id、腳本契約和驗證器相容；移文不能擅改欄位。

  **原文位置：** [主檔:40](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-mining-stp/SKILL.md:40)、[主檔:76](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-mining-stp/SKILL.md:76)、[主檔:111](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-mining-stp/SKILL.md:111)、[主檔:150](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-mining-stp/SKILL.md:150)、[主檔:245](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-mining-stp/SKILL.md:245)、[主檔:419](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-mining-stp/SKILL.md:419)、[主檔:501](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-mining-stp/SKILL.md:501)。

- [ ] **12. review-salience-xlsx**（中優先）

  **可以改哪裡：** 相同三個 references 導引逐字重複；內嵌 CSV 範例與步驟重複工具細節；PCA/K-means-only 也要求讀 xlsx；硬綁 present_files、recalc.py 和工作目錄複製。

  **建議改法：** 刪去重複導引，主檔只留階段選擇/評分契約/全樣本覆蓋，載入格式技能只在輸出該格式時；I/O 程式移腳本或 reference；用當前環境的檔案交付能力，只有公式存在才要求重算。

  **應保留：** 使用者只要哪階段就跑哪階段、salience 不是情緒、整數與屬性順序、分群後每筆仍得到歸屬。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-salience-xlsx/SKILL.md:3)、[主檔:18](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-salience-xlsx/SKILL.md:18)、[主檔:34](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-salience-xlsx/SKILL.md:34)、[主檔:77](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-salience-xlsx/SKILL.md:77)、[主檔:142](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-salience-xlsx/SKILL.md:142)、[主檔:164](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-salience-xlsx/SKILL.md:164)、[主檔:173](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-salience-xlsx/SKILL.md:173)。

- [ ] **13. review-scoring-docx**（高優先）

  **可以改哪裡：** description 連未要求 Word 的一般屬性比較也強制觸發；硬湊至少三十屬性及五層配額，和由語料歸納矛盾；未提及直接給五分讓無證據混成中性；內嵌 I/O 與 Word 排版指南重複下游能力。

  **建議改法：** 限定評論比較並需要 Word 的任務；取消屬性及各層硬配額，無證據保留未觀察狀態，連同平均分規則一起調整；保留屬性定義和評分規準在主檔，程式及版面移 scripts/reference；格式依現有文件技能。

  **應保留：** 完整評論覆蓋、多語同等、凍結可追溯屬性、評分依據、數值與視覺一致；缺值變更須同步驗證所有平均分。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-scoring-docx/SKILL.md:3)、[主檔:13](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-scoring-docx/SKILL.md:13)、[主檔:37](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-scoring-docx/SKILL.md:37)、[主檔:52](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-scoring-docx/SKILL.md:52)、[主檔:73](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-scoring-docx/SKILL.md:73)、[主檔:94](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-scoring-docx/SKILL.md:94)、[主檔:120](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-scoring-docx/SKILL.md:120)、[主檔:161](/Users/timlai/Developer/skills/plugins/customer-insight/skills/review-scoring-docx/SKILL.md:161)。

- [ ] **14. theory-analysis**（低優先）

  **可以改哪裡：** 主檔已做到按所選理論與 STP 需求讀 reference，宜低優先保留；description 仍含逐句多理論與 STP 欄位操作細節；即使只做質性判讀也固定 JSON+Markdown，references/01 永遠含 STP 對接欄。

  **建議改法：** 先只縮 description 到觸發與排除條件；JSON 僅結構化交付或串接需要時提供；STP 區塊隨交接需求產出；維持現有短入口，不為省字刪 taxonomy 判讀。

  **應保留：** 多理論可同時標、引文可逐字核對、無證據 insufficient、item-level 與 attribute-level 邊界。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/customer-insight/skills/theory-analysis/SKILL.md:3)、[主檔:56](/Users/timlai/Developer/skills/plugins/customer-insight/skills/theory-analysis/SKILL.md:56)、[主檔:65](/Users/timlai/Developer/skills/plugins/customer-insight/skills/theory-analysis/SKILL.md:65)、[主檔:85](/Users/timlai/Developer/skills/plugins/customer-insight/skills/theory-analysis/SKILL.md:85)。

### data-and-research

- [ ] **15. arxiv**（中優先）

  **可以改哪裡：** description 把所有 paper/related-work 都強制用 arxiv；inline XML parser、curl examples 與既有 helper script 是多份操作路徑；Semantic Scholar 全套及七步完整研究流程常駐，即使只查指定 ID。

  **建議改法：** 限定 arXiv 搜尋/擷取；以 helper 為主入口，curl/XML/BibTeX 移按需 reference，Semantic Scholar 只在 citation/related-work 需求讀；七步改任務路由，不必每次查作者與影響力。

  **應保留：** 版本後綴、撤稿檢查、API 限流、Atom格式處理與原文閱讀/引用。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/data-and-research/skills/arxiv/SKILL.md:3)、[主檔:35](/Users/timlai/Developer/skills/plugins/data-and-research/skills/arxiv/SKILL.md:35)、[主檔:174](/Users/timlai/Developer/skills/plugins/data-and-research/skills/arxiv/SKILL.md:174)、[主檔:243](/Users/timlai/Developer/skills/plugins/data-and-research/skills/arxiv/SKILL.md:243)。

- [ ] **16. data-analysis-workflow**（高優先）

  **可以改哪裡：** 主檔固定 Step0–12 與 model_performance，reference 缺目標就一律 clustering（237–254）、缺失值固定median/mode、異常remove/winsorize（103–129）；所謂簡化版仍強制Model（423–434），不是按需求減步驟。

  **建議改法：** 目標判定前移；主檔只保留問題→品質→必要分析→驗證→報告。描述性/推論/預測分支按需讀，非建模不生成 model artifacts；清理方式由資料機制與用途決定，不用固定閾值/填值/刪除；合併reference三套重複流程。

  **應保留：** 資料結構與品質查核、來源/清理決策可追蹤、使用適合評估且報告實際限制。

  **原文位置：** [主檔:30](/Users/timlai/Developer/skills/plugins/data-and-research/skills/data-analysis-workflow/SKILL.md:30)、[主檔:48](/Users/timlai/Developer/skills/plugins/data-and-research/skills/data-analysis-workflow/SKILL.md:48)、[references/data-analysis-flow.md:237](/Users/timlai/Developer/skills/plugins/data-and-research/skills/data-analysis-workflow/references/data-analysis-flow.md:237)。

- [ ] **17. investment-research-prompts**（中優先）

  **可以改哪裡：** 定位是 prompt 模板，但 description 網羅全部投資研究；多場景必先問主軸、缺資料固定五欄 MissingDataOutput，連產出可填 prompt 也被同一門檻卡住；reference 八模板有冗長履歷式角色，固定10/15–20標的及全分析項。

  **建議改法：** description 收斂研究prompt/框架；先分生成模板與執行研究，模板可保留槽位，分析才查必要資料。八場景做短索引＋按段讀；角色改簡短專業任務，不需20年/$60B履歷；清單與標的數改依需求，缺資料用簡短必要問題。

  **應保留：** 時效資料查證、來源、假設/未知區分，DCF敏感度與情境風險等專業內容。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/data-and-research/skills/investment-research-prompts/SKILL.md:3)、[主檔:48](/Users/timlai/Developer/skills/plugins/data-and-research/skills/investment-research-prompts/SKILL.md:48)、[主檔:58](/Users/timlai/Developer/skills/plugins/data-and-research/skills/investment-research-prompts/SKILL.md:58)、[主檔:99](/Users/timlai/Developer/skills/plugins/data-and-research/skills/investment-research-prompts/SKILL.md:99)、[references/prompt-library.md:22](/Users/timlai/Developer/skills/plugins/data-and-research/skills/investment-research-prompts/references/prompt-library.md:22)。

### dev-workflow

- [ ] **18. db-engineering**（高優先）

  **可以改哪裡：** 任何 DB 工作都必載十一條鐵則及完整性清單；原則、流程、收尾重述同樣規則。微小查詢也帶入雙實例、全稽核、軟刪、BCNF 等架構選擇；日常流程自動要求 commit。

  **建議改法：** description 聚焦 DB 設計、migration、資料安全與效能；主檔縮成任務分流及不可遺失的安全檢查，建表／查詢／稽核／上線各讀對應 reference。環境、軟刪、稽核、正規化寫成有前提的專案政策；commit 依授權。消除主文與收尾逐條複製。

  **應保留：** migration 可追溯、正式環境授權與備份、FK 刪除影響、資料讀寫路徑與實測效能證據。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/db-engineering/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/db-engineering/SKILL.md:15)、[主檔:55](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/db-engineering/SKILL.md:55)、[主檔:69](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/db-engineering/SKILL.md:69)、[主檔:94](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/db-engineering/SKILL.md:94)、[主檔:110](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/db-engineering/SKILL.md:110)。

- [ ] **19. dev-task-loop**（高優先）

  **可以改哪裡：** description 塞入整個工作流程；每次固定六問、選首張、每張再問、三輪停下，使已授權 backlog loop 重複確認。正文宣稱平台中立卻內嵌特定瀏覽器 API、固定 merge/rebase/force push 與歷史偏好。

  **建議改法：** description 只保留 backlog 場景及單票排除；六項改成可從上下文補齊的工作契約，只問缺項。依一次授權持續執行；提交合併同步策略從專案契約取得。平台操作移按需 reference；附件需實際讀取即可，不一律要求每票用瀏覽器。

  **應保留：** 一個 OpenSpec change 是一張票、UI 實際驗證、範圍隔離、逐票完成條件與回寫驗證、阻礙及剩餘票清單。

  **原文位置：** [主檔:4](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:4)、[主檔:25](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:25)、[主檔:56](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:56)、[主檔:70](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:70)、[主檔:113](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:113)、[主檔:143](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:143)、[主檔:155](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:155)、[主檔:185](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:185)、[主檔:201](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/dev-task-loop/SKILL.md:201)。

- [ ] **20. diff-inspector**（中優先）

  **可以改哪裡：** description 含執行策略；technical review 與 perspectives 重複測試、安全、效能、資料/API 契約檢查；子 agent prompt 又重列一份。

  **建議改法：** description 留下程式 diff 審查觸發及純文件排除；將兩套檢查合成一份按變更類型選用的清單。子 agent 引用該清單並指定獨立找反例，不複製全部風險分類；大段文件種類可收成受影響使用者／agent 文件。

  **應保留：** 完整 diff 覆蓋、契約上下游追查、具體失敗情境與檔案行號、相關 diff 未變可沿用結論、高影響變更才派獨立審查。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:3)、[主檔:37](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:37)、[主檔:74](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:74)、[主檔:87](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:87)、[主檔:111](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:111)。

- [ ] **21. eng-architect**（高優先）

  **可以改哪裡：** 任何非小功能實作前都必載，卻同時包架構、切票、UI 審查兩種任務。每功能流程／測試位置與整體圖逐關確認；每次強制 ENG、狀態、票、AGENTS、CLAUDE 多項成品。主檔重列 reference 的狀態格式與大量模板及舊檔名遷移歷史。

  **建議改法：** 縮窄至架構決策或切票要求；工程與 UI 分流後僅讀對應 reference（先不新增 skill）。每功能仍分析，但只把真正待決策部分集中確認。既有專案沿用其文件與票系統，只有需要跨票交接時建立協調檔；模板、操作命令、舊名稱遷移移入按需 reference。狀態 schema 主檔只鏈接單一來源。

  **應保留：** 按使用者可驗收行為切票、依賴關係、錯誤及邊界覆蓋、共享決策與單票驗收分工、讀後局部更新及不覆寫其他 skill 區段。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:3)、[主檔:18](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:18)、[主檔:30](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:30)、[主檔:72](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:72)、[主檔:100](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:100)、[主檔:152](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:152)、[主檔:168](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:168)、[主檔:203](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:203)、[主檔:238](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:238)、[主檔:289](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:289)、[主檔:377](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:377)、[references/delivery-status-guidelines.md:5](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/references/delivery-status-guidelines.md:5)。

- [ ] **22. investigate**（高優先）

  **可以改哪裡：** 所有 bug 強制 3–5 假說並填機率，即使已有直接證據；固定三次修正封頂；強制修正與回歸測試各自 commit。禁止改 code 的診斷範例卻要求加 logging／pin 版本，且示例直接印環境變數。

  **建議改法：** description 留下未知根因的系統除錯及明確點名；依現有證據決定假說數，不填假精確百分比。以沒有新增證據或需要額外權限為升級條件；合併重複停止規則與報告。保留可逆診斷修改並遮蔽敏感值；測試順序及 commit 服從專案與授權。

  **應保留：** 先定位根因、反證測試、追到最早偏離位置、原症狀重現與修後回歸證據。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:3)、[主檔:34](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:34)、[主檔:64](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:64)、[主檔:101](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:101)、[主檔:127](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:127)。

- [ ] **23. openclaw-agent-builder**（高優先）

  **可以改哪裡：** 只要 host 有 ~/.openclaw 就強制觸發，會把無關任務拉進來；已說明新增或編輯仍問模式、本機/SSH；SSH 教學、概念、型態、部署及編輯 runbook 全放主檔，且編輯時要求順手補全部安全項目。

  **建議改法：** 觸發限明確 OpenClaw agent 建立／修改，不靠檔案存在。沿用已知目標與模式，只問缺失；主檔保留決策分流、安全必備與驗收，SSH、型態展開、編輯對照、部署細節放 reference。安全健檢發現範圍外缺口先列建議；未來圖形化平台段移出執行主檔。

  **應保留：** 對現有設定讀取與備份、目標機器確認、版本/schema 查證、服務型 session 隔離、已驗證身分、權限最小化、具體 diff 與線上操作授權。

  **原文位置：** [主檔:4](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:4)、[主檔:59](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:59)、[主檔:159](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:159)、[主檔:166](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:166)、[主檔:199](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:199)、[主檔:256](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:256)、[主檔:281](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:281)、[主檔:311](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:311)、[主檔:336](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:336)。

- [ ] **24. openclaw-ops**（中優先）

  **可以改哪裡：** scope 與轉交 builder 重述多次；debug、設定寫入、SSH 已有 reference 卻在主檔重列 runbook。每次先問目標且 debug 也逐步確認；dmPolicy 在分類矩陣屬 ops，但關係段又宣稱 builder 領域。

  **建議改法：** 主檔縮成目標/版本/授權檢查、分流矩陣、完成條件；操作細節只在對應 reference。沿用已建立連線，不為讀取再次確認；保留具體破壞性操作授權但消除多份同意流程。統一 agent 設定與 channel 設定的責任界線。

  **應保留：** 按需載入 references、讀取現狀、版本驗證、設定備份與生效驗證、破壞性操作護欄與憑證遮蔽。

  **原文位置：** [主檔:4](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:4)、[主檔:25](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:25)、[主檔:38](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:38)、[主檔:43](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:43)、[主檔:119](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:119)、[主檔:151](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:151)、[主檔:193](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:193)、[主檔:213](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:213)、[主檔:228](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:228)、[主檔:257](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:257)、[主檔:285](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:285)、[references/debug.md:19](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/references/debug.md:19)。

- [ ] **25. postgrest-baas-builder**（中優先）

  **可以改哪裡：** 任何 RLS/PostgREST 查詢先載完整 db-engineering；主檔同時載 Supabase Cloud、自架、InsForge/MCP 設定，不同平台內容無條件伴隨。欄位慣例與收尾重複規則。

  **建議改法：** 只在涉及 schema／migration 等 DB 工作載入對應 DB 指引；先辨別平台及任務，再讀 RLS、Auth、效能、自架或 InsForge reference。MCP 安裝及平台限制移 reference；主檔保留平台分流與安全檢查，不重列通用欄位。

  **應保留：** RLS 與授權驗證、內建 Auth 適配、金鑰不進 git、明列查詢欄位、實際平台可用的安全/效能驗證。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:15)、[主檔:47](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:47)、[主檔:68](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:68)、[主檔:87](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:87)、[主檔:93](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:93)、[主檔:109](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:109)。

- [ ] **26. project-memory**（高優先）

  **可以改哪裡：** 每個既有專案啟動與收尾必載，必須口頭表態並自動 add；主檔大量解釋為何強制與為何採 JSONL，重複 add 命令及各階段規則。記憶全 key 永久輸出可能隨規模成長。

  **建議改法：** description 改精準記錄／回顧專案經驗任務，既有專案採相關性按需搜尋；若保留自動記憶模式，先由使用者啟用。主檔留下 load/search/add 最小操作與記錄資格，格式、合併、匯出細節移按需參考。刪除重複勸說與口頭無事宣告；大庫以任務相關檢索為入口。

  **應保留：** 腳本處理轉義、去重可追溯、專案特有且實際發生的經驗、不把開放問題混入記憶、不自動匯出至版本控制文件。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:3)、[主檔:14](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:14)、[主檔:26](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:26)、[主檔:68](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:68)、[主檔:98](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:98)、[主檔:106](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:106)、[主檔:143](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:143)、[主檔:169](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:169)、[主檔:183](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:183)、[主檔:199](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:199)、[主檔:213](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:213)。

- [ ] **27. set-zeabur-conventions**（中優先）

  **可以改哪裡：** 觸發限制中英重述，主檔在寫部署規範任務裡同載 MCP 安裝、完整 envsubst 維運知識及罕見 shared variable 故障；description 說只支援 Dockerfile，正文承認自動偵測建置，規則有漂移風險。

  **建議改法：** description 留一次精準部署目標與排除；主檔只留查既有段落、更新模板、驗證，MCP 安裝／環境變數生效／特殊診斷移按需 reference。長期約束只在模板保留一份；平台能力先依官方現況驗證再更新，避免把舊限制寫成永遠事實。

  **應保留：** 明確 Zeabur 意圖才改專案、compose 本機用途、AGENTS 區段不重複且尊重既有客製、安全金鑰與 runtime/build-time 差異。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:3)、[主檔:12](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:12)、[主檔:24](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:24)、[主檔:61](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:61)、[主檔:85](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:85)、[主檔:104](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:104)。

- [ ] **28. ship-it**（高優先）

  **可以改哪裡：** release/deploy/merge 等廣泛觸發卻只支援 feature branch→PR；固定 merge 同步、全套測試及新路徑 100% 覆蓋；收尾強制 project-memory。讀 legacy delivery-plan.md，與 eng-architect 的 delivery-status.md 不一致。

  **建議改法：** 定位清楚限定分支交付到 PR；先讀專案既有交付規則、已驗證證據與授權。同步和測試依變更風險及專案需求，避免重跑同一 diff 審查；PR 模板移素材並優先 repo 模板；記憶改有實際新經驗且啟用才記錄。統一狀態文件入口並兼容舊檔，不把 PR 建立稱完整上線。

  **應保留：** 秘密掃描、工作目標確認、修正引入的失敗、必要審查與 CI 證據、PR URL 和實際交付狀態。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:15)、[主檔:53](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:53)、[主檔:65](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:65)、[主檔:75](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:75)、[主檔:87](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:87)、[主檔:146](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:146)、[主檔:163](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:163)。

- [ ] **29. software-engineering-guidelines**（高優先）

  **可以改哪裡：** 任何軟體活動甚至一行變更都必載；原則→流程→清單重複同一事項。範圍外問題一律寫 AGENTS、初始化一律把 CLAUDE 改指標，有額外副作用。所有變更與全測試一刀切。

  **建議改法：** 先確定哪些屬使用者持續偏好留在單一規則來源，skill 保留有操作價值的範圍／成功條件／按風險驗證流程。三組重述合併一組；低風險文案等用比例適當驗證。範圍外問題先回報，只有專案採此慣例才寫 Follow-ups，沿用既有 CLAUDE/AGENTS 結構。

  **應保留：** 不擴需求、不覆蓋他人、不亂重構、重大變更測試先行、可驗證成功條件、不得削弱測試掩飾問題。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:3)、[主檔:8](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:8)、[主檔:42](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:42)、[主檔:44](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:44)、[主檔:48](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:48)、[主檔:88](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:88)、[主檔:109](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:109)。

- [ ] **30. test-and-fix**（高優先）

  **可以改哪裡：** 泛用測試 skill 寫死 web route、固定 port、base branch 禁測；為 CLI/library 也要啟動 app。修 bug 強制 fix/test 分開 commit，沒有框架就要 bootstrap。仍讀 delivery-plan.md。

  **建議改法：** 先依測試目標分 web／API／library／CLI；已提供測試命令或範圍即直接沿用，必要時才讀 branch diff，不要求 feature branch。從專案設定找啟動方法；fix loop 保留根因/回歸，commit 依授權。模板與偵測命令移參考，沒有框架可先提供重現驗證再判斷是否需引入依賴。統一狀態入口。

  **應保留：** 實際受影響路由及狀態驗證、失敗證據、根因未知才深入 investigate、回歸測試確實先壞後好。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:15)、[主檔:35](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:35)、[主檔:47](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:47)、[主檔:62](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:62)、[主檔:90](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:90)、[主檔:101](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:101)、[主檔:139](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:139)。

### knowledge-tools

- [ ] **31. excalidraw-diagram**（高優先）

  **可以改哪裡：** 主檔兩次列完整 element/text schema（233–295、311–368），Obsidian 包裝也重複（42–69、407–426）；三模式模板與三段回覆範例常駐；「畫圖／動畫圖」觸發過廣。主檔 boundElements 一律 null 與 reference 綁定範例有差異。

  **建議改法：** 主檔保留模式選擇、產出及驗證；每種模式模板、完整 schema、色票與回覆例移 references/assets，schema 單一來源。description 收斂至 Excalidraw／手繪白板；對 boundElements 等相容性禁令先查證適用版本，再統一範例，勿直接刪保護。

  **應保留：** 三模式實際格式差異、唯一 ID、JSON 合法性、文字可讀性與版面檢查。

  **原文位置：** [主檔:233](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/excalidraw-diagram/SKILL.md:233)、[主檔:311](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/excalidraw-diagram/SKILL.md:311)、[主檔:407](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/excalidraw-diagram/SKILL.md:407)。

- [ ] **32. llm-wiki**（高優先）

  **可以改哪裡：** 把一般研究自動升級成建 wiki；每次查詢也先讀 schema/index/log＋一致性探查；初始化模板、Ingest、21項 lint、headless 安裝全常駐。筆記規律在主檔、模板、Ingest、Pitfalls 多次重述，且跨 skill 同步一份 checklist。

  **建議改法：** description 限定 wiki 建置／維護／查詢，不因研究一詞自建；按 init/ingest/query/lint 分流 references；templates 與 headless 安裝各按需讀。查詢只讀相關索引與頁面，寫入才查完整規範；七項檢核只留一份權威內容＋極短後備，減少每個 backlink 不處理理由的重複紀錄。

  **應保留：** 來源可追溯、raw 保護、矛盾不覆寫、去重、非遞迴回連、索引同步；不要因簡化丟掉這些功能。

  **原文位置：** [主檔:26](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/llm-wiki/SKILL.md:26)、[主檔:163](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/llm-wiki/SKILL.md:163)、[主檔:206](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/llm-wiki/SKILL.md:206)、[主檔:512](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/llm-wiki/SKILL.md:512)。

- [ ] **33. mermaid-visualizer**（中優先）

  **可以改哪裡：** Quick Start 與 Workflow 是同一五步，Critical Syntax 與 Workflow 檢查及 Quality Checklist 重複；六種圖類型常識、虛擬配置選單與示例占主要篇幅。

  **建議改法：** 合併成一份流程與驗收；圖種類型表精簡，色票與完整範例按需讀；主檔保留 renderer 易錯語法。節點標點一律替換、style declarations 必有改為依實際 renderer 需求，先驗證再保留限定。

  **應保留：** 明確 ID／display label、subgraph 引用、目標 renderer 相容性與實際渲染驗證。

  **原文位置：** [主檔:22](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/mermaid-visualizer/SKILL.md:22)、[主檔:193](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/mermaid-visualizer/SKILL.md:193)、[主檔:270](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/mermaid-visualizer/SKILL.md:270)。

- [ ] **34. obsidian-bases**（中優先）

  **可以改哪裡：** 三個完整範例常駐（297–420），Duration 教學與 troubleshooting 重複；完整 file properties／summary 清單可按需查。

  **建議改法：** 主檔留最小 schema、屬性/公式命名與驗證；完整範例另存 references/examples，函數及彙總表按需求讀；Duration 與 null guard 各留一個代表反例。

  **應保留：** YAML 引號、空值檢查、Duration 先取數值欄位、formula 定義對應與 Obsidian 渲染驗證。

  **原文位置：** [主檔:197](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-bases/SKILL.md:197)、[主檔:297](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-bases/SKILL.md:297)、[主檔:465](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-bases/SKILL.md:465)。

- [ ] **35. obsidian-canvas-creator**（中優先）

  **可以改哪裡：** 使用條件再次擴成任意 visual diagram；ID、間距、escaping 在產生/驗證/Critical/Pitfalls 重複；兩個範例只是重講分析流程。

  **建議改法：** description 與 body 同限 Obsidian Canvas；合併結構規則和驗收，保留一次；版面與尺寸/色票移按需 reference，兩個重述流程範例可移除。把固定 320/200 間距改為預設起點＋依卡片尺寸驗證。

  **應保留：** nodes/edges 結構、ID 唯一、引用存在、groups 圖層順序與實際開啟檢查。

  **原文位置：** [主檔:19](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-canvas-creator/SKILL.md:19)、[主檔:104](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-canvas-creator/SKILL.md:104)、[主檔:142](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-canvas-creator/SKILL.md:142)。

- [ ] **36. obsidian-cli**（低優先）

  **可以改哪裡：** 基本 CLI 內容已緊湊並以 obsidian help 查現況，未見需要大改；但 note 操作也常載入完整 plugin debug 段，description 重列多種同義操作。

  **建議改法：** 低優先保留主體；description 壓成 vault 操作與 plugin/theme debugging 兩類；71–115 開發命令移專用 reference，僅開發任務讀。

  **應保留：** 執行中的 Obsidian 前提、help、vault/file/path 目標解析差異與引號語法。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-cli/SKILL.md:3)、[主檔:71](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-cli/SKILL.md:71)。

- [ ] **37. obsidian-markdown**（高優先）

  **可以改哪裡：** 語法 skill 強制新 vault 採 llm-wiki 架構，混入另一項產品決策；每個新 note 被要求 frontmatter、embeds、callouts，非必要也易照做；完整例及一般 Math/Mermaid 教學常駐。

  **建議改法：** description 僅保留 Obsidian 特有語法觸發；移出強制 vault 架構到建庫 skill。流程改成依需要使用 properties/embed/callout，完整例移 reference，主檔只留特有差異。

  **應保留：** wikilinks、block IDs、嵌入、callouts 特有語法與既有 vault 慣例。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-markdown/SKILL.md:3)、[主檔:18](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-markdown/SKILL.md:18)、[主檔:198](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-markdown/SKILL.md:198)。

- [ ] **38. tutor**（中優先）

  **可以改哪裡：** 即使使用者已說考哪一節也強制再選 Session；綁死 AskUserQuestion 的四題四選項；read quiz-rules、無暗示、檔案更新與語言在 reference 與主檔反覆重述；初始化模板每次載入。

  **建議改法：** Session 僅目標不明才問；四題短回合保留預設，但工具格式移適配段，無工具可用正常文字測驗；模板按首次建立才讀，檢核與更新規則只保留單一來源。

  **應保留：** 零暗示、選項位置變化、四題短回合、錯題換情境、批改後更新 concept 與 dashboard。

  **原文位置：** [主檔:42](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor/SKILL.md:42)、[主檔:109](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor/SKILL.md:109)、[主檔:156](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor/SKILL.md:156)。

- [ ] **39. tutor-setup**（高優先）

  **可以改哪裡：** 三模式主檔負擔不均（Codebase 已外移，Document/Wiki 還完整常駐）；已知模式/來源仍多次必問確認；PDF 只能 pdftotext，無視掃描/圖表；Equal Depth 要將每個旁枝補成 textbook note。題數/比例機械化且兩模式分析題規則不一致；Wiki >200 行拒絕與 llm-wiki 長度不是拆分理由衝突。

  **建議改法：** 主檔縮為模式路由＋來源/學習進度保護，各模式按需讀；已明確指定不重問；PDF 依內容採文字抽取或必要視覺辨識；深度依學習目標，題目數及比例當預設。200行改內容判斷；輸入界線改使用者授權路徑，刪除/rename 同步另列可審閱處理，保留進度；統一 quality-checklist 對應規則。

  **應保留：** source mapping 不憑檔名、答案摺疊、增量 manifest、保留既有學習進度和手寫筆記、來源驗證。

  **原文位置：** [主檔:11](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:11)、[主檔:20](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:20)、[主檔:43](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:43)、[主檔:70](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:70)、[主檔:234](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:234)、[主檔:280](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:280)。

- [ ] **40. zettelkasten**（中優先）

  **可以改哪裡：** 核心原則、流程、檢核、Quality/Common Mistakes 反覆講原子性、自己話與連結；同一 checklist 又複製 reference 並要求同步 llm-wiki（reference 02 行3）。

  **建議改法：** 主檔用一份短判斷清單作核心；詳例及拆卡過程留 references，不再重列原则/錯誤。跨 skill 保留一個權威 checklist 與明確讀取入口；只紀錄實際拆分及有影響邊界決策，不為每條未回連新增說明。

  **應保留：** 長度不是拆卡標準、不拆到失去自主性、既有筆記庫慣例、矛盾保留與非遞迴回連。

  **原文位置：** [主檔:31](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/zettelkasten/SKILL.md:31)、[主檔:76](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/zettelkasten/SKILL.md:76)、[主檔:99](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/zettelkasten/SKILL.md:99)。

### marketing-strategy

- [ ] **41. content-growth-studio**（高優先）

  **可以改哪裡：** description 泛到任何 URL、上傳筆記、標題與重寫，容易越界一般內容任務；入口/模式在決策樹、Entry Paths、Mode Routing 與 references/01 重複；快速草稿固定三至五假設。

  **建議改法：** 縮到以成長為目的的內容規劃/製作；主檔合成一張模式路由表，場景例表移 references；每種模式明列何時讀哪份通路/輸出模板；缺口按需要列，不為數量發明假設。

  **應保留：** 來源意思、不可虛構成效/競品資料、跨通路須改寫節奏、專項技能只在需深入時使用。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:3)、[主檔:24](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:24)、[主檔:47](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:47)、[主檔:76](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:76)、[主檔:115](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:115)。

- [ ] **42. experiential-guerrilla-marketing**（高優先）

  **可以改哪裡：** 行銷 KPI 等泛詞強制觸發；主檔大量理論教材、案例、年度趨勢/倍數主張，缺直接可核對來源；每活動強制多模組/完整5E；搭配八個技能表容易擴展工作。

  **建議改法：** 縮到體驗/游擊活動；主檔留目標→場域→參與機制→衡量與風險，理論/戰術/案例拆按需 reference；不固定至少兩模組；數字先查證加來源或改無數字示例，搭配技能僅按缺失能力選擇。

  **應保留：** SCHMITT 與5E 專業選擇框架、現場許可與不阻礙交通、活動目標和衡量一致。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:3)、[主檔:16](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:16)、[主檔:29](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:29)、[主檔:59](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:59)、[主檔:118](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:118)、[主檔:134](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:134)、[主檔:182](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:182)、[主檔:200](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:200)。

- [ ] **43. maslow-five-needs-marketing**（高優先）

  **可以改哪裡：** IQ300 角色重複兩次無可檢查行動價值；CTA/文案方向泛觸發；每次固定五層全產出、多 KPI/30天動作/每層三標題三CTA，且六份 reference 全串讀；硬綁 copywriting。

  **建議改法：** 移除空泛角色設定；限縮馬斯洛需求訊息策略；主檔保留五層判準及相關需求選取，低相關層標不適用，不強迫全層文案；完整跨通路方案才展開排程/KPI，參考按目的讀，長文案交現有寫作能力。

  **應保留：** 可驗證需求與訊息關係、真實證據、不假承諾、受眾不同可有不同優先序。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:15)、[主檔:60](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:60)、[主檔:73](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:73)、[主檔:92](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:92)、[主檔:129](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:129)、[主檔:137](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:137)、[主檔:181](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:181)。

- [ ] **44. psychological-trigger-marketing**（中優先）

  **可以改哪裡：** description 與 When to Use 重複；七模組摘要與 references/01 再述；每次硬選二至四觸發器並至少三標題三CTA，即單一CTA需求也膨脹。

  **建議改法：** 主檔留受眾階段→觸發器選擇表及證據限制，詳細理論與例句按需讀；只用足以滿足任務的觸發器和候選數量；單一文案請求不強出完整 JSON 策略包。

  **應保留：** 真實限量/原價/見證依據、焦慮不能唯一手段、冷暖熱受眾差異。

  **原文位置：** [主檔:20](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:20)、[主檔:76](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:76)、[主檔:121](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:121)、[主檔:135](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:135)、[主檔:161](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:161)。

- [ ] **45. sor-marketing-strategy**（高優先）

  **可以改哪裡：** 泛 KPI/A-B 測試/CRM 觸發與排除單一實驗互相競爭；三類措施加 sor_map/策略行動等重複敘述；每類至少三因子與完整三十天計畫強制；四份 references 不分任務全讀。

  **建議改法：** 觸發縮到刺激→心理→行為的策略分析；主檔保留模型決策和反例，將措施合併成一張因果與衡量表；完整活動需求再加通路/實驗/排程；參考檔按刺激、心理、量測疑問讀取，專項交接不硬綁不存在的工具名。

  **應保留：** 刺激不能直接視為因果、信任與侵擾雙面判讀、前導/結果指標、假證據禁止。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:3)、[主檔:79](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:79)、[主檔:95](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:95)、[主檔:150](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:150)、[主檔:214](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:214)。

- [ ] **46. threads-viral-growth**（高優先）

  **可以改哪裡：** 泛社群詞及未指定平台即啟動 Threads；任何潤稿都強制趨勢查詢、候選湊三、七步流程/固定五件套/十五分鐘劇本；主檔常駐時間表與缺來源算法百分比，且權重順序前後不同。

  **建議改法：** 限定 Threads 寫作/經營；時事/趨勢型才要求即時研究，已給材料改寫可直接做；主檔留需求→取材→成稿→核對，模板/排程/互動按需求 reference；去除定時久候與候選硬配額，數字/最佳時間改可查來源與待測假設；交付只含需求相關內容。

  **應保留：** 可直接使用的台灣語氣稿、與受眾/主體連結、資料來源、真實互動與成效驗證，不保證爆文。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:3)、[主檔:29](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:29)、[主檔:36](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:36)、[主檔:43](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:43)、[主檔:83](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:83)、[主檔:118](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:118)、[主檔:173](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:173)、[主檔:200](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:200)、[主檔:222](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:222)、[主檔:285](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:285)。

### service-innovation

- [ ] **47. ecosystem-map-and-blueprint**（中優先）

  **可以改哪裡：** 兩套圖型教材一起載入，案例和清單重複；泛服務設計／接觸點觸發。所有情境要求跨部門共同參與，不適合個人資料草稿。

  **建議改法：** 觸發收斂兩種圖的製作／審查；先選圖型再讀所需結構和案例。跨部門協作放正式驗證階段，草稿標待查證者；缺口診斷不預設導入科技，允許減少流程。

  **應保留：** 參與者、價值交換、前後台與支援區分、方向與缺口、未證實資料標示。

  **原文位置：** [主檔:4](/Users/timlai/Developer/skills/plugins/service-innovation/skills/ecosystem-map-and-blueprint/SKILL.md:4)、[主檔:27](/Users/timlai/Developer/skills/plugins/service-innovation/skills/ecosystem-map-and-blueprint/SKILL.md:27)、[主檔:75](/Users/timlai/Developer/skills/plugins/service-innovation/skills/ecosystem-map-and-blueprint/SKILL.md:75)、[主檔:153](/Users/timlai/Developer/skills/plugins/service-innovation/skills/ecosystem-map-and-blueprint/SKILL.md:153)、[主檔:171](/Users/timlai/Developer/skills/plugins/service-innovation/skills/ecosystem-map-and-blueprint/SKILL.md:171)、[主檔:200](/Users/timlai/Developer/skills/plugins/service-innovation/skills/ecosystem-map-and-blueprint/SKILL.md:200)。

- [ ] **48. scamper**（中優先）

  **可以改哪裡：** 已有 quick 與 focus_dimensions，仍要求七維度各 2–3 構想、Top 3、缺資料列 3–5 假設。泛創意詞與工作坊重疊。

  **建議改法：** 觸發突出 SCAMPER 方法；quick／指定維度決定展開範圍，完整工作坊才走全套。取消機械配額，保留可比較的獨立構想；企業案例按需讀。

  **應保留：** 七維度方法、限制條件、不重複包裝點子；明確要求完整七維度時保留完整度。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/service-innovation/skills/scamper/SKILL.md:3)、[主檔:36](/Users/timlai/Developer/skills/plugins/service-innovation/skills/scamper/SKILL.md:36)、[主檔:40](/Users/timlai/Developer/skills/plugins/service-innovation/skills/scamper/SKILL.md:40)、[主檔:44](/Users/timlai/Developer/skills/plugins/service-innovation/skills/scamper/SKILL.md:44)、[主檔:70](/Users/timlai/Developer/skills/plugins/service-innovation/skills/scamper/SKILL.md:70)。

- [ ] **49. service-design-workshop**（中優先）

  **可以改哪裡：** 服務藍圖、顧客體驗、利害關係人皆觸發；固定兩項輸入、3–5 假設、六段輸出，局部問題走全套。

  **建議改法：** 限定服務設計工作坊，單張圖交專用技能；輸入以足以界定目標和場域為準。六段放完整模板，局部修改只交相關部分；流程與輸出合為階段成果對照。

  **應保留：** 顧客／營運雙視角、接觸點對應前後台、原型對象與成功訊號。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-design-workshop/SKILL.md:3)、[主檔:22](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-design-workshop/SKILL.md:22)、[主檔:37](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-design-workshop/SKILL.md:37)、[主檔:39](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-design-workshop/SKILL.md:39)、[主檔:47](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-design-workshop/SKILL.md:47)。

- [ ] **50. service-innovation-case-study**（高優先）

  **可以改哪裡：** description 塞參考檔與讀檔指令；一般品牌研究也走全套。Doji 條件泛化為固定投資／電商層、三項 SWOT、八策略、48 分門檻和資源導向順序；reference 以 ST 組合預設定位。主檔與分析鏈重複。

  **建議改法：** 區分完整課堂格式與一般案例研究，原課堂模式完整保留。主檔只留模式、證據、分析承接和交付，細節用既有 references。數量／門檻／ST 示例／Doji 分類限定模板，一般研究按問題選框架和策略。輸出位置依工作區，不綁 /mnt。

  **應保留：** 可追溯來源、分析一致、真實摩擦、公司宣稱與證實效果；指定課堂作業不可縮成摘要。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-case-study/SKILL.md:3)、[主檔:24](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-case-study/SKILL.md:24)、[主檔:134](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-case-study/SKILL.md:134)、[主檔:286](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-case-study/SKILL.md:286)、[主檔:320](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-case-study/SKILL.md:320)、[references/02-analysis-chain.md:61](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-case-study/references/02-analysis-chain.md:61)、[references/02-analysis-chain.md:179](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-case-study/references/02-analysis-chain.md:179)。

- [ ] **51. service-innovation-workshop**（中優先）

  **可以改哪裡：** SCAMPER、價值共創等泛詞重複觸發，固定 3–5 假設、至少三方向、六段輸出。

  **建議改法：** 聚焦從機會到概念驗證的工作坊；不搶單方法任務。方向數依實質選項，已選方向就補原型與測試；六段留模板，references 依機會、方法、格式選讀。

  **應保留：** 概念比較、顧客需求、組織能力、原型成功訊號。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-workshop/SKILL.md:3)、[主檔:22](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-workshop/SKILL.md:22)、[主檔:37](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-workshop/SKILL.md:37)、[主檔:39](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-workshop/SKILL.md:39)、[主檔:48](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-workshop/SKILL.md:48)。

### thinking-frameworks

- [ ] **52. plan-grilling**（高優先）

  **可以改哪裡：** 一般規劃或已定案也強制壓問；所有決策逐題問且立即寫時間戳、拒絕選項，固定要求新 framing 與兩週指標。所有領域都綁 git branch 檔名，只為 eng-architect 找檔。

  **建議改法：** 聚焦使用者要求釐清/壓測未決計畫；已決方向不重開。只問影響範圍與資源的未決問題，記錄實質決策而非每句訪談；reframe、兩週驗收改依情境。主檔留訪談判斷，完整訪談表與模板移 reference；明確傳交計畫路徑，非工程規劃不受 Git 檔名約束。

  **應保留：** 先查事實再問決策、真正痛點與範圍、假設反例、使用者可驗收的工作切分、只建議後續開發步驟而不逕自開發。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:3)、[主檔:29](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:29)、[主檔:51](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:51)、[主檔:83](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:83)、[主檔:94](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:94)、[主檔:111](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:111)、[主檔:146](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:146)、[主檔:184](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:184)、[主檔:224](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/plan-grilling/SKILL.md:224)。

- [ ] **53. subtraction-thinking**（高優先）

  **可以改哪裡：** 對所有輸出前中後強制審查、超過五組成就停、必做 Won’t List、每次硬附減法段落甚至一句提醒；減法本身增加大量固定形式。場域問法與反模式重複核心問題。

  **建議改法：** 觸發改為簡化/移除/複雜度評估，或具體出現不必要複雜；把三階段合成目標、每項價值、移除損失、替代方案四問，實際重要變更再重檢。域別例子放 reference，輸出只呈現實質發現，允許無需簡化且不硬湊 Won’t List。

  **應保留：** 減法包括保留但變簡單、豐富不等於冗餘、根據實際損失判斷、不以數量作完成標準。

  **決定：保留原版，不修改。** 使用者已結束本項調整；原有數量門檻、Won’t List、審查流程、輸出格式與版本全部保留。上述審查建議未採用，本項不計入完成優化數，也不再列為待驗收。已比對 Git 提交版本，確認 skill 與所屬 plugin 版本均已還原。

- [x] **54. ultrathink**（高優先）

  **可以改哪裡：** 非明顯結論都觸發；雖只選 1–2 類，類內工具全部跑，再每決策單元固定六語完整重析，及五模型、七組約160條謬誤、另載 subtraction。Workflow/Quality/Common Mistakes/Quick Reference 重述大量不可跳規定。

  **建議改法：** 主檔改為選與決策相關的工具、證據/反例/條件改變時選項的最小流程。六語和全謬誤審查保留為可明確選用的進階模式，不在每個任務固定跑；獨立複核按風險與未解爭點派發，不以語言數或檢核條數代表品質。分類表作唯一入口，去除逐段重述；輸出只留結論、依據、限制、待查項。

  **應保留：** 不捏造資料、資料不足單元暫不裁決、各類按需載入、不同觀點不靠票數判真、反證與完成證據、進階方法內容可保留不刪。

  **目前狀態：已修改、完成必要檢查並經使用者確認。** 上述問題保留為初次審查紀錄。

  **措辭修正：** 不再按文字修改、事實查詢或既定步驟一律排除，改看是否有實質疑點或取捨。語意、語氣及讀者理解均可納入；使用者明確要求深入思考時仍啟用。此次以規則檢閱及格式檢查驗證，未重跑獨立情境評估。

  **實際變更：** 主檔 146 → 67 行，description 997 → 319 字元。日常依問題選工具；六語分析、七組完整謬誤檢核改成依具體疑點自動啟用，也可明確指定；六語各自完整分析，不按文化或預設角色分工。保留方法內容、資料不足不裁決、反證與完成證據。

  | 檔案（相對 repository） | 變更摘要 |
  | --- | --- |
  | `plugins/thinking-frameworks/skills/ultrathink/SKILL.md` | 縮小觸發與主流程，將反覆「不跑完整套」提醒收斂為依問題選方法；移除重述用途的 Suggested Prompt；skill 版本 2.1.3。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/01-logical-reasoning.md` | 改為依疑點選工具，保留方法。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/02-creative-ideation.md` | 同上。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/03-market-analysis.md` | 同上。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/04-progress-management.md` | 同上。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/05-weighing-tradeoffs.md` | 同上。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/06-predicting-future.md` | 同上。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/07-debate-thinking.md` | 依論證類型選方法，依疑點或明確要求啟用完整謬誤檢核。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/08-mental-models.md` | 取消固定共用層，僅執行選中模型。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/multilingual-thinking.md` | 明定啟用條件、無獨立上下文時的限制及查證收斂方式。 |
  | `plugins/thinking-frameworks/skills/ultrathink/references/fallacy-checklist.md` | 明定局部查閱與完整模式；全部謬誤條目保持原文。 |
  | `plugins/thinking-frameworks/.claude-plugin/plugin.json` | 同步介紹，plugin 版本 0.40.3。 |
  | `.claude-plugin/marketplace.json` | 同步 thinking-frameworks 介紹。 |
  | `README.md` | 更新 ultrathink 適用需求。 |
  | `docs/skill-audit/checklist.md` | 記錄本項變更、驗證及驗收狀態。 |

  **驗證：** skill-creator 的 quick_validate 通過；YAML／JSON 可解析，相對連結有效，README 與實際 skill 數量均為 62，git diff --check 通過。與修改前比對，謬誤清單的全部條目保持原文。獨立複核實際回答一般決策、資料不足兩例；六語、七組及簡單改寫三例只檢查啟用規則，未執行完整六語或七組流程。沒有量測時間或 token 節省，未同步安裝版本；本次依使用者要求提交與推送。

  **目前位置：** [主流程](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/ultrathink/SKILL.md:26)、[進階模式](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/ultrathink/SKILL.md:47)、[輸出及品質](/Users/timlai/Developer/skills/plugins/thinking-frameworks/skills/ultrathink/SKILL.md:54)。

### utilities

- [ ] **55. defuddle**（中優先）

  **可以改哪裡：** 49行本體已精簡，主要問題是 description 把每個 URL 都鎖成 MUST instead of WebFetch，且只用 .md 字尾判例外。

  **建議改法：** 工具可用且一般 HTML 抽取合適時使用；直接 markdown 依內容類型辨識，動態/登入頁留適合工具，失敗可 fallback；保留短 CLI 用法，不需要再拆 reference。

  **應保留：** --md、metadata 抽取和輸出格式這些真正工具差異。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/utilities/skills/defuddle/SKILL.md:3)、[主檔:16](/Users/timlai/Developer/skills/plugins/utilities/skills/defuddle/SKILL.md:16)。

- [ ] **56. folder-organizer**（中優先）

  **可以改哪裡：** description 將一般 file audit/analyze 全捕捉；同一確認門檻在 description/Core/Phase4/Phase5 重述；固定每檔都提新名、分類、刪除與 zip，即使只問資料夾建議；上傳路徑與 bash_tool 寫死環境。

  **建議改法：** 觸發限定整理、分類、重新命名或搬移規劃；合併成盤點→按需求提改動表→已授權範圍執行。單一確認門檻保留，已有完整授權不重問。工具與上傳路徑依環境取得；沒有改名/刪除需求不硬產方案。

  **應保留：** 碰檔案前盤點、明確來源/目的映射、重名處理、不可讀檔標未知與使用者確認實際整理計畫。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/utilities/skills/folder-organizer/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/utilities/skills/folder-organizer/SKILL.md:15)、[主檔:93](/Users/timlai/Developer/skills/plugins/utilities/skills/folder-organizer/SKILL.md:93)。

- [ ] **57. windows-rescue-from-linux**（中優先）

  **可以改哪裡：** 已做好按症狀讀 reference，安全限制有必要；仍每次先全套 bootstrap、Node/Claude/skill安裝，再問症狀，與末段先問症狀互斥；一律五階段、每個sudo說明加雙確認增加負擔。通用驗證區同列 dry-run 和真正 ntfsfix 寫入。

  **建議改法：** 保留安全入口與症狀路由，環境bootstrap另分準備USB需求及缺工具時讀；重複安全敘述合併成一次確認具体高風險步驟，沿用既有授權。驗證按實際修復選唯讀檢查，真正寫入 ntfsfix 留修復路徑，不當通用驗證。

  **應保留：** 唯讀掛載、寫前備份/壞碟先映像、BitLocker金鑰、hive備份、破壞性動作確認及 Linux 無法修復的界線。

  **原文位置：** [主檔:28](/Users/timlai/Developer/skills/plugins/utilities/skills/windows-rescue-from-linux/SKILL.md:28)、[主檔:76](/Users/timlai/Developer/skills/plugins/utilities/skills/windows-rescue-from-linux/SKILL.md:76)、[主檔:94](/Users/timlai/Developer/skills/plugins/utilities/skills/windows-rescue-from-linux/SKILL.md:94)、[主檔:269](/Users/timlai/Developer/skills/plugins/utilities/skills/windows-rescue-from-linux/SKILL.md:269)。

### writing-and-design

- [ ] **58. commercial-proposal-writing**（高優先）

  **可以改哪裡：** 起草與審稿共用完整輸入門檻，局部審稿也會因缺 KPI／客群停下；九段正文、七項審稿成果、至少三風險及 A/B/C/D 補件皆固定。主檔與 reference 重複輸入和模式。

  **建議改法：** 分完整提案、局部改稿、純審查，只問必需資料。九段、風險數量、無資料選項改完整提案模板。純審查不預設整篇重寫。核心保留受眾、決策請求與證據，細節按模式載入，合併重複規則。

  **應保留：** 決策對象、資源、財務假設推導、不捏造，以及使用者指定完整提案結構。

  **原文位置：** [主檔:24](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/commercial-proposal-writing/SKILL.md:24)、[主檔:42](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/commercial-proposal-writing/SKILL.md:42)、[主檔:147](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/commercial-proposal-writing/SKILL.md:147)、[主檔:183](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/commercial-proposal-writing/SKILL.md:183)、[主檔:215](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/commercial-proposal-writing/SKILL.md:215)、[references/01-intake-and-audience-routing.md:5](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/commercial-proposal-writing/references/01-intake-and-audience-routing.md:5)。

- [x] **59. design-studio**（高優先）

  **本次已完成，使用者已確認並要求推送：** 按實際工具與上下文限制適配流程，取消非 Claude 自動降級；移除需求重述與規格的字數門檻；純評論及不涉及視覺規範的小修改沿用既有設計資料；影片音軌依用途與約定驗證，有音訊時建議同時設計節拍層與氛圍底。保留三版設計、風格流程及確認要求。其餘初次審查建議尚未採用。

  **變更檔案：** SKILL.md（1.13.1）、practical/GUIDE.md、shared/verification.md、practical/references/audio-design-rules.md、README.md、plugin.json（1.20.1）及本清單。

  **驗證：** quick_validate、YAML／JSON 解析與 git diff --check 通過；核對主檔、實作流程與音訊參考的一致性。這次修改的是流程文件，尚未實跑設計或影片匯出；本次依使用者要求提交與推送。以下為初次審查紀錄。

  **可以改哪裡：** 所有設計都寫 DESIGN.md、讀五份 shared 文件；practical 七階段、三版本、秒數抽風格、多次停等，並以非 Claude 判定能力不足。雙主題與音訊的預設也增加工作。

  **建議改法：** 主檔只分流產出類型，完整模板移既有 template；小改與純審查不強制作文件。多版本、隨機風格、萬字導演筆記改選用；只在關鍵未決定事項停等。依實際工具能力調整，不依模型品牌降級。雙主題和音訊由交付需求決定。

  **應保留：** 真實素材、可用性、實際畫面互動驗證及匯出工具必要限制；電影風格等專長保留選用。

  **原文位置：** [主檔:21](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/design-studio/SKILL.md:21)、[主檔:135](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/design-studio/SKILL.md:135)、[practical/GUIDE.md:192](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/design-studio/practical/GUIDE.md:192)、[practical/GUIDE.md:350](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/design-studio/practical/GUIDE.md:350)、[practical/GUIDE.md:473](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/design-studio/practical/GUIDE.md:473)、[shared/guardrails.md:18](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/design-studio/shared/guardrails.md:18)、[shared/verification.md:34](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/design-studio/shared/verification.md:34)。

- [x] **60. human-writing**（高優先）

  **完成決定：** 使用者已確認並要求提交、推送。完整閱讀範例移到起草前，移除 Suggested Prompt，取消自動附加 Kept as-is 備註。依文章比較新增規則與三組範例：減少過度使用「代表」句型，按句意與中文習慣處理連接、條件及搭配，具體替換詞只作例句示範。原有「這代表每位照護者必須照看更多長者。」保留。

  **變更及驗證：** SKILL.md（1.9.2）、四份寫作參考文件及模式文件、plugin.json（1.19.2）與本清單。quick_validate、JSON／YAML、相對連結及 git diff --check 通過。兩個 Luna 曾比較 1.8.4 與 1.8.6，未見明顯全面改善；1.9.2 尚未重跑比較。測試文章與流程紀錄已清除，skill 的教學範例保留。以下為初次審查紀錄，未採用的建議不再列為待辦。

  **可以改哪裡：** 任何對話文字都觸發；46 行主檔要求讀五份參考文件，原則、反模式、清單重複。

  **建議改法：** 濃縮日常核心，長文、改稿與特殊文類才讀細節，例集改按需查閱；同一原則只維護一份完整定義。是否縮小所有回覆皆適用的範圍，另由使用者決定。

  **應保留：** 不編造、原意與適用範圍、台灣用語、文類慣例、具體可讀。細緻例句先保留作查閱材料。

  **原文位置：** [主檔:4](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/human-writing/SKILL.md:4)、[主檔:24](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/human-writing/SKILL.md:24)、[references/final-checklist.md:3](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/human-writing/references/final-checklist.md:3)。

- [ ] **61. landing-page-studio**（高優先）

  **可以改哪裡：** 固定三個價值主張、預設高動畫、多稿比較、至少四類動畫；缺輸出模式停止，React 還先問技術組合。要求同時寫在主檔及腳本。

  **建議改法：** 先完成一個符合轉換目標的頁面，再按實際問題修正；多稿、動畫種類改選項，價值主張依真實內容決定。沿用現有技術，只問改變目標的缺項。同步調整輸入驗證與動畫清單腳本，合併重複檢查。

  **應保留：** 主要行動按鈕、真實內容、窄螢幕可讀、減少動態偏好、效能與可用性驗證。

  **原文位置：** [主檔:41](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:41)、[主檔:59](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:59)、[主檔:97](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:97)、[主檔:101](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:101)、[主檔:128](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:128)、[scripts/validate_intake.py:24](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/scripts/validate_intake.py:24)、[scripts/validate_intake.py:88](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/scripts/validate_intake.py:88)。

- [ ] **62. open-slide-studio**（中優先）

  **可以改哪裡：** description 塞框架功能、內建技能和流程，格式限制與指令在多節重複。已有不複製上游規範的好設計。

  **建議改法：** description 留網頁簡報與可編輯 PPTX 排除；合併流程、速查、常見錯誤重複。新工作區才初始化與完整視覺接軌，改一頁沿用主題；工作區規則依當下 AGENTS.md，避免維護兩份。

  **應保留：** 圖片版 PPTX 不可編輯的告知、Node 前提、theme 交接、不覆寫上游管理檔。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:3)、[主檔:49](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:49)、[主檔:80](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:80)、[主檔:88](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:88)、[主檔:96](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:96)。

## 一起留意的相依問題

這些不是額外的技能完成項目。處理對應 skill 時一起檢查，不另開一批重寫。

1. **觸發描述彼此競爭。** 研究類、行銷類、服務設計類與通用思考類都有很廣的入口。逐項縮短時，應用同一個實際請求比較相鄰技能，保留最適合的入口，不把所有技能合併成更大的入口。
2. **文件已改名，下游仍找舊名。** [eng-architect](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:66) 已改用 delivery-status.md，但 [ship-it](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:26) 與 [test-and-fix](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:31) 仍查 delivery-plan.md。簡化時定義單一交接名稱，並處理既有舊檔相容性。
3. **不能只改 Markdown。** landing-page-studio 的價值主張數量、預設動畫與多輪設定也在腳本；評論分析的評分、缺值與欄位會影響下游計算。調整這些項目時，相關腳本與模板必須一起檢查。
4. **範例不能替代方法。** service-innovation-case-study 的 Doji 模式、product-conjoint-analysis 的特定商品模型，以及顧客旅程的情緒加減分，須分清案例示範、使用者指定格式和一般方法。統計與外部格式相容性的變更需要再查證，這輪不宣稱已解決。
5. **長度不是拆分依據。** [tutor-setup 的 200 行限制](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:284) 與 llm-wiki／zettelkasten 的內容判斷需要統一。單純把主檔搬到一份每次必讀的大 reference，也沒有真正減少載入內容。

## 審查證據與限制

- 檔案盤點與 README 開頭均為 62 個 skills；[AGENTS.md](/Users/timlai/Developer/skills/AGENTS.md:9) 仍寫 61 個。這個數量差異另列提醒，本輪未修改。
- 初次審查時使用 YAML parser 讀取 62 個主檔的 frontmatter，description 合計 30,318 字元，全數低於 1,024 字元。這不是 token 數，也不表示描述已精確。最長為 ultrathink 997、dev-task-loop 924、openclaw-ops 916 字元。
- 三個分組審查覆蓋 52 個 skills，其餘 10 個由主審閱讀。主審核對分組結論及每項原文節錄，再整合此表。
- 高／中／低優先是根據文字與流程的審查判斷，尚未量測省下多少 token、時間或產出品質差異。
- 初次審查只新增這份清單。後續 ultrathink 的修改與驗證記錄於 #54；其他 skills 尚未修改，沒有刪除任何 skill，沒有提交、推送、部署或同步本機安裝版本。

Skills：skill-creator、subtraction-thinking、human-writing。
