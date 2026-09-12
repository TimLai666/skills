# Skills 簡化清單

目前完成優化：**43 / 62**。已勾選項目均經使用者確認。每次只處理一個 skill，實際修改、必要驗證並經使用者確認接受後，才勾選該項。

初次審查範圍：repository 的 `plugins/*/skills/*`，共 62 個 skills、10 個 plugins。不是本機所有第三方已安裝 skills 的清單。已逐一閱讀全部 SKILL.md，涉及重複、相依或矛盾的建議另查相關 references、模板或腳本；這不是所有附屬檔案逐行審計，也未實測所有技能的執行效果。

依據：[Eric Provencher：Rethinking skills and prompts for GPT-6 Astra](https://x.com/pvncher/status/2095991462416490862)。文章提醒縮短並精確描述適用情境、只在需要時讀取細節、減少過度固定的流程，以及清楚界定完成條件和需要停下來的決策。下列各項是對本 repo 的審查判斷，不是作者對這些 skills 的評語。

## 共通調整：Suggested Prompt 與 commit 訊息

依使用者要求，移除以下 15 個 skills 的 Suggested Prompt／Suggested Prompts 段落，並同步移除 psychological-trigger-marketing 驗證清單對該段的要求。這次共通調整不代表各 skill 的個別審查已完成，未驗收項目維持未勾選。

- [maslow-five-needs-marketing](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md)
- [psychological-trigger-marketing](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md)
- [sor-marketing-strategy](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md)
- [landing-page-studio](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md)
- [open-slide-studio](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md)
- [bcg-growth-share-matrix](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md)
- [decision-bias-quality-control](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md)
- [business-model-architect](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md)
- [service-design-workshop](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-design-workshop/SKILL.md)
- [scamper](/Users/timlai/Developer/skills/plugins/service-innovation/skills/scamper/SKILL.md)
- [service-innovation-workshop](/Users/timlai/Developer/skills/plugins/service-innovation/skills/service-innovation-workshop/SKILL.md)
- [orchestrating-mixed-methods](/Users/timlai/Developer/skills/plugins/customer-insight/skills/orchestrating-mixed-methods/SKILL.md)
- [customer-journey-mapper](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-journey-mapper/SKILL.md)
- [customer-persona-framer](/Users/timlai/Developer/skills/plugins/customer-insight/skills/customer-persona-framer/SKILL.md)
- [theory-analysis](/Users/timlai/Developer/skills/plugins/customer-insight/skills/theory-analysis/SKILL.md)

commit 訊息規範放在 [software-engineering-guidelines](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md#commit-messages)，ship-it 在建立 commit 前引用。使用者明確指示優先，其次專案規範；未指定格式時使用 Conventional Commits，未指定語言時以英文撰寫。所有修改的 skills 與六個所屬 plugins 均調升版本。

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

- [x] **01. bcg-growth-share-matrix**（中優先）

  **可以改哪裡：** 觸發列表重複 description；分類規則與 references/01 重複；八大輸出主體、90 天追蹤與四份參考檔每次必讀，讓簡單分類也變成完整資本配置報告。

  **建議改法：** 主檔保留市場口徑、公式、門檻與例外判讀；欄位明細移到模板；快速分類只出座標/象限/依據，要求配置時才產出資本方案與追蹤；參考檔改按分類、策略、例外需求讀取。

  **應保留：** 最大競爭者分母、成長門檻來源、邊界敏感度、Dogs 協同例外與 Question Marks 投資停止條件。

  **原文位置：** [主檔:22](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:22)、[主檔:87](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:87)、[主檔:122](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:122)、[主檔:198](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:198)、[主檔:206](/Users/timlai/Developer/skills/plugins/business-strategy/skills/bcg-growth-share-matrix/SKILL.md:206)。

  **完成修改：** 完整分析仍為預設，只有明確要求分類或計算時縮小交付。合併重複規則與欄位，保留四象限方法、發展潛力、轉移條件及座標資料。修正已有相對市佔仍索取原始市佔的矛盾；缺口以自然語言說明。模板移除重複座標欄，時程依本案調整。刪除提示詞參考文件，保留介面 default_prompt。skill 與 business-strategy plugin 均為 1.2.0。使用者已確認接受並要求提交、推送。

  **驗證：** quick_validate、YAML／JSON、引用、圍欄、模板欄位、skill／README 數量及 git diff --check 通過。三種文件情境推演涵蓋完整配置、只做分類及缺資料不允許假設；並修正追問清單仍可能重複索取原始市佔的問題。

- [x] **02. business-model-architect**（高優先）

  **可以改哪裡：** 八個必要輸入連 WT 都列缺一不可；宣稱九個主體實列十個；四份擴充輸出重述九要素；震央決定順序卻另強制不得跳序；固定至少三策略三實驗與七張臉孔擴大每次工作。

  **建議改法：** 分核心商模與完整驗證兩種交付深度；九要素整合成一表，foundation/四構面/operating/WT 只在需求涉及時展開；震央控制設計次序，輸出順序可另固定；缺口只擋受影響結論；同步 references/06 模板與評分，消除多處契約漂移。

  **應保留：** 九要素連貫、核心要素較深入、事實與假設區分、具成功指標的驗證實驗。

  **原文位置：** [主檔:34](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:34)、[主檔:73](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:73)、[主檔:99](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:99)、[主檔:110](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:110)、[主檔:159](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:159)、[主檔:191](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:191)、[主檔:226](/Users/timlai/Developer/skills/plugins/business-strategy/skills/business-model-architect/SKILL.md:226)。

  **完成修改：** 完整分析仍為預設，僅明確縮小需求時局部交付。保留四種震央、主次關係、推導例句與核心深入設計，取消固定核心格數及設計順序矛盾。輸入改為盤點，缺口只影響相關結論。整合重複分析與報告模板，策略數量、實驗時程與敏感度幅度依本案，保留方法與驗證條件。skill 1.2.0、business-strategy plugin 1.3.0，介面 default_prompt 保留。使用者已確認接受並要求提交、推送。

  **驗證：** quick_validate、YAML／JSON、引用、圍欄、skill／README 數量與 git diff --check 通過。完整分析、局部調整及缺資料情境完成文件推演，並補明局部任務不重新選震央或追加無關策略與實驗；未宣稱完成模型行為實測。

- [x] **03. decision-bias-quality-control**（中優先）

  **完成修改：** 保留獨立 skill、完整十二問及雙軌審查，新增 self-agent 自行查核與方案修正，ultrathink 自動轉接。合併重複流程與評分規則，依需求交付腳本或完整審查。補齊三因子定義、小數門檻及缺資料的分數範圍，行動數量與期限依本案安排。文字以現行操作為主。skill 1.3.0、business-strategy plugin 1.5.0，ultrathink 2.3.0、thinking-frameworks plugin 0.43.0。使用者已確認接受並要求提交、推送。

  **驗證：** quick_validate、YAML／JSON、引用、圍欄、skill／README 數量及 git diff --check 通過。評分檢查涵蓋 3,003 個小數門檻案例、637 組分組合計及未知題範圍計算。未做模型行為實測。

  **可以改哪裡：** 泛提案審查與個人選擇容易觸發；每次先讀五份檔且所有模式都強制十二題逐題量化與固定三至五項，會把會議引導變成評分報告；評分摘要與 references/04 重複。

  **建議改法：** 縮到明確偏誤品管/重大決策方法需求；主檔保留模式入口和十二問證據檢查，題庫與評分只讀一次權威來源；會議/教練可先交關鍵追問，正式評分模式再展開雙軌和完整計算。

  **應保留：** 十二問方法本體、證據支持、團隊共識不可推定；完整評分時保留可重算規則。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:3)、[主檔:22](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:22)、[主檔:76](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:76)、[主檔:95](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:95)、[主檔:107](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:107)、[主檔:124](/Users/timlai/Developer/skills/plugins/business-strategy/skills/decision-bias-quality-control/SKILL.md:124)。

- [x] **04. pestel-analysis**（高優先）

  **完成修改：** 完整分析為預設，明確限定需求時局部交付。精簡觸發與輸入確認，六面向依證據掃描，題庫與假設示例移至參考文件並指定讀取時機。保留三項評分與乘積，釐清數值及時間邊界、比較基準、未知範圍與時間視窗優先順序。統一因素記錄與 SWOT 輸入包，區分經濟及環境編號。skill 1.2.0、business-strategy plugin 1.6.0。使用者已驗收並要求提交、推送。

  **驗證：** quick_validate、YAML／JSON、引用、圍欄、description、60 個 skill／README 數量及 git diff --check 通過。計算檢查涵蓋 75 組評分、7 個影響程度邊界、5 個時效邊界及示例範圍。文件審查修正局部交付與時間視窗的規則衝突，未做模型行為實測。

  **可以改哪裡：** description 混入執行評分；六面向教科書問句和案例常駐；每面向硬找三至五候選；SWOT 輸入包與末尾移交包重複且即使只要 PESTEL 也產出。

  **建議改法：** description 只描述 PESTEL/總體環境用途；掃描題庫、評分表與長案例移 references；六面向檢查但不硬湊數；因素表只保留一份，只有要接 SWOT 才建立一次移交包；來源未可核對的法規範例改成清楚的假設示例或補來源。

  **應保留：** 分析地區與時間、來源、具體影響機制、可解釋的優先排序與中性因素條件。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:3)、[主檔:41](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:41)、[主檔:122](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:122)、[主檔:167](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:167)、[主檔:203](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:203)、[主檔:243](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:243)、[主檔:272](/Users/timlai/Developer/skills/plugins/business-strategy/skills/pestel-analysis/SKILL.md:272)。

- [x] **05. red-flag-contract-scanner**（中優先）

  **已依使用者要求刪除並經驗收：** 移除 skill 主檔、六份參考文件與兩份模板。內容主要是常見審閱清單與報告格式，缺乏經驗證的額外效益，參考文件另有錯誤法規與無來源斷言。原文可從 Git 歷史取得。

  **驗證：** JSON 解析、59 個 skill／README 列數／AGENTS.md 數量一致及 git diff --check 通過。除了本項歷史紀錄，沒有剩餘引用。使用者已要求提交、推送。

  **同步調整：** README 移除項目，README 與 AGENTS.md 的現有 skill 數量改為 59。business-strategy plugin 與 marketplace 描述移除合約紅旗掃描，plugin 升至 1.7.0。審查分母維持 62，本機已安裝版本不在這次刪除範圍。以下保留初次審查紀錄。

  **可以改哪裡：** description 堆疊契約類型與關鍵詞；主檔內嵌整份報告模板；超過三十頁直接當可能不完整、首輪強制問格式且已有預設；硬綁 /mnt/skills/public/docx 與 message_compose_v1。

  **建議改法：** 壓縮為不利條款審閱用途及兩三種辨識訊號；報告骨架移用既有 assets；只在實際截斷時追問，按既定預設直接交付；依現有 Word 能力產檔；無關且未出現條款不逐一占正文，保留實質缺漏；法律提醒集中一次。

  **應保留：** 原條文位置與引用、司法管轄區不確定性、具體協商改法與不代替使用者決定簽約。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:3)、[主檔:25](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:25)、[主檔:58](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:58)、[主檔:66](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:66)、[主檔:72](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:72)、[主檔:76](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:76)、[主檔:134](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:134)、[主檔:159](/Users/timlai/Developer/skills/plugins/business-strategy/skills/red-flag-contract-scanner/SKILL.md:159)。

- [x] **06. swot-analysis**（高優先）

  **完成修改：** 完整分析維持預設，明確限定需求時局部交付。承接適用的外部資料，缺少總體環境證據時才補 PESTEL，保留階段一「情況 A」的交接位置。修正機會的能力補強條件、威脅時間視窗及優劣勢排除條件。依實質關聯配對，跨象限比較候選，保留三項評分並釐清可行性、時間餘裕、同分與資料不足的處理。合併重複交付，零候選與單一候選依實際結果呈現。skill 1.2.0、business-strategy plugin 1.8.0，README 已同步。使用者已驗收並要求提交、推送。

  **驗證：** quick_validate、YAML／JSON、description、59 個 skill／README 數量、PESTEL 交接位置及 git diff --check 通過。27 組三項評分組合的總分範圍檢查通過。獨立文件推演涵蓋局部分類、已有外部資料與能力補強、零候選、單一候選及跨象限同分未定。這是文件與邏輯驗證，沒有量測模型效果。以下保留初次審查紀錄，採用範圍以上述修改為準。

  **可以改哪裡：** 觸發範圍含 PEST 與一般競爭策略；無論證據是否足夠都強制先跑 PESTEL 並停下；窮舉所有元素配對、固定選一主策略與放棄清單；策略定調卡重複輸出。

  **建議改法：** 縮到 SWOT/TOWS 工作；允許直接承接已有可信外部證據，缺總體掃描才補 PESTEL；按實質相關性配對而不窮舉；只在策略選擇需求展開評分/取捨；保留一份策略表，長教程、示例與定調卡移參考檔/模板。

  **應保留：** 比較基準、S/W 與 O/T 來源、策略與來源元素連結、不是數項目決定態勢。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:3)、[主檔:50](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:50)、[主檔:77](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:77)、[主檔:132](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:132)、[主檔:180](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:180)、[主檔:234](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:234)、[主檔:280](/Users/timlai/Developer/skills/plugins/business-strategy/skills/swot-analysis/SKILL.md:280)。

### customer-insight

- [x] **07. customer-journey-mapper**（高優先）

  **完成修改：** 主檔集中輸入判斷、八列順序與交付，保留預設五階段、自訂階段及使用者覆寫優先。足以辨識客群與服務情境即可製表，缺口及草稿假設依實際需要處理。情緒評分與呈現各移至按需參考文件，修正五列範例為 2、3、4.5、4.5、4 分。區分推估與研究資料，最大情緒改善不直接判為 Aha Moment。曲線依實際欄寬與階段數定位，產圖與嵌入保持比例，純 Markdown 依格式能力呈現。skill 1.2.0、customer-insight plugin 1.5.0，README 與介面描述已同步。使用者已驗收並要求提交、推送。

  **驗證：** quick_validate、YAML／JSON、description、相對連結、圍欄、59 個 skill／README 數量及 git diff --check 通過。由範例表重算五列分數，六種相鄰差值情境通過。依呈現規格產出並檢視單階段、四／五／六階段、不等寬及缺值共六種 PNG，尺寸與欄中心座標檢查通過。獨立文件推演涵蓋客群文字、handoff、階段覆寫、快速草稿、局部更新及各種分數狀態。尚未驗證 Word 嵌入、網頁互動或模型效果。測試腳本、圖片與隔離 Python 環境位於 /private/tmp/cjm-verify.WE2Z1C，沒有加入 repo。以下保留初次審查紀錄，採用範圍以上述修改為準。

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

- [x] **19. dev-task-loop**

  **已依使用者要求刪除。** 原內容可從 Git 歷史取得。README 已移除項目，現有 skill 數量為 61。eng-architect 的兩處交接說明改為直接指向任務目錄，避免依賴已刪除的 skill。

- [x] **20. diff-inspector**（中優先）

  **已完成並經使用者確認：** 合併 Technical review 與 Review perspectives 的重複檢查，保留具體檢查內容、上下游追查與文件一致性。主審與 sub-agent 統一使用 CONFIRMED／NEEDS INVESTIGATION，已確認缺陷與有證據的待查疑點分開呈現。skill 1.5.0、plugin 1.23.0。

  **可以改哪裡：** description 含執行策略；technical review 與 perspectives 重複測試、安全、效能、資料/API 契約檢查；子 agent prompt 又重列一份。

  **建議改法：** description 留下程式 diff 審查觸發及純文件排除；將兩套檢查合成一份按變更類型選用的清單。子 agent 引用該清單並指定獨立找反例，不複製全部風險分類；大段文件種類可收成受影響使用者／agent 文件。

  **應保留：** 完整 diff 覆蓋、契約上下游追查、具體失敗情境與檔案行號、相關 diff 未變可沿用結論、高影響變更才派獨立審查。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:3)、[主檔:37](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:37)、[主檔:74](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:74)、[主檔:87](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:87)、[主檔:111](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/diff-inspector/SKILL.md:111)。

- [x] **21. eng-architect**（高優先）

  **已完成並經使用者確認：** 精確化觸發及模式判斷，集中尚未定案的決策；沿用專案現有文件與任務系統，無安排且需要完整交接時保留原本整套文件。工程與 UI 流程分檔並保留完整範例，狀態格式只維護一份，舊檔遷移按需讀取。測試入口與覆蓋依行為邊界、風險及效能目標決定。skill 1.11.0、plugin 1.24.0。

  **追加修改，已確認：** 四段 shell 指令改成查找與驗證要求，保留根目錄定位、相關內容完整讀取與既有文件保護，移除指令輸出標記的相依文字。架構圖、錯誤表與切票範例保留。主檔集中列出各檔案用途、建立或更新條件與讀取時機。skill 1.11.2、plugin 1.24.2，已提交於 75a5cb6。

  **流程微調，已確認：** 區分架構分析與切票成果，先切票再更新狀態，合併重複文件說理，要求 UI 實際渲染與互動驗證，修正評分與設計依據判斷及付款範例的外部服務標示。skill 1.11.3、plugin 1.24.3。Human Writing 同步加入「收一次」的原句與「微調」改寫，並補充動作不明的判斷原則（skill 1.9.4、plugin 1.20.3）。使用者已確認並要求提交、推送。

  **可以改哪裡：** 任何非小功能實作前都必載，卻同時包架構、切票、UI 審查兩種任務。每功能流程／測試位置與整體圖逐關確認；每次強制 ENG、狀態、票、AGENTS、CLAUDE 多項成品。主檔重列 reference 的狀態格式與大量模板及舊檔名遷移歷史。

  **建議改法：** 縮窄至架構決策或切票要求；工程與 UI 分流後僅讀對應 reference（先不新增 skill）。每功能仍分析，但只把真正待決策部分集中確認。既有專案沿用其文件與票系統，只有需要跨票交接時建立協調檔；模板、操作命令、舊名稱遷移移入按需 reference。狀態 schema 主檔只鏈接單一來源。

  **應保留：** 按使用者可驗收行為切票、依賴關係、錯誤及邊界覆蓋、共享決策與單票驗收分工、讀後局部更新及不覆寫其他 skill 區段。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:3)、[主檔:18](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:18)、[主檔:30](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:30)、[主檔:72](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:72)、[主檔:100](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:100)、[主檔:152](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:152)、[主檔:168](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:168)、[主檔:203](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:203)、[主檔:238](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:238)、[主檔:289](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:289)、[主檔:377](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/SKILL.md:377)、[references/delivery-status-guidelines.md:5](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/eng-architect/references/delivery-status-guidelines.md:5)。

- [x] **22. investigate**（高優先）

  **已完成並經使用者確認：** 精確化根因調查觸發，取消固定假說數與無依據百分比；診斷允許可逆修改並保護機密資訊，一般指令改為查證要求。測試順序依專案及風險，無其他安排時保留修正與回歸測試分開提交。停止條件依新增證據及實際阻礙，未解問題按相關性說明。skill 1.3.1、plugin 1.25.1。

  **可以改哪裡：** 所有 bug 強制 3–5 假說並填機率，即使已有直接證據；固定三次修正封頂；強制修正與回歸測試各自 commit。禁止改 code 的診斷範例卻要求加 logging／pin 版本，且示例直接印環境變數。

  **建議改法：** description 留下未知根因的系統除錯及明確點名；依現有證據決定假說數，不填假精確百分比。以沒有新增證據或需要額外權限為升級條件；合併重複停止規則與報告。保留可逆診斷修改並遮蔽敏感值；測試順序及 commit 服從專案與授權。

  **應保留：** 先定位根因、反證測試、追到最早偏離位置、原症狀重現與修後回歸證據。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:3)、[主檔:34](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:34)、[主檔:64](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:64)、[主檔:101](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:101)、[主檔:127](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/investigate/SKILL.md:127)。

- [ ] **23. openclaw-agent-builder**（高優先）

  **已討論，保留原版：** 使用者要求完整還原本次修改，不調整此 skill。相關 README 與 plugin 版本變更一併還原，新增參考文件已移除。本項不勾選。

  **可以改哪裡：** 只要 host 有 ~/.openclaw 就強制觸發，會把無關任務拉進來；已說明新增或編輯仍問模式、本機/SSH；SSH 教學、概念、型態、部署及編輯 runbook 全放主檔，且編輯時要求順手補全部安全項目。

  **建議改法：** 觸發限明確 OpenClaw agent 建立／修改，不靠檔案存在。沿用已知目標與模式，只問缺失；主檔保留決策分流、安全必備與驗收，SSH、型態展開、編輯對照、部署細節放 reference。安全健檢發現範圍外缺口先列建議；未來圖形化平台段移出執行主檔。

  **應保留：** 對現有設定讀取與備份、目標機器確認、版本/schema 查證、服務型 session 隔離、已驗證身分、權限最小化、具體 diff 與線上操作授權。

  **原文位置：** [主檔:4](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:4)、[主檔:59](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:59)、[主檔:159](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:159)、[主檔:166](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:166)、[主檔:199](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:199)、[主檔:256](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:256)、[主檔:281](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:281)、[主檔:311](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:311)、[主檔:336](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-agent-builder/SKILL.md:336)。

- [ ] **24. openclaw-ops**（中優先）

  **已略過，保留原版：** 依使用者要求不修改，本項不勾選。

  **可以改哪裡：** scope 與轉交 builder 重述多次；debug、設定寫入、SSH 已有 reference 卻在主檔重列 runbook。每次先問目標且 debug 也逐步確認；dmPolicy 在分類矩陣屬 ops，但關係段又宣稱 builder 領域。

  **建議改法：** 主檔縮成目標/版本/授權檢查、分流矩陣、完成條件；操作細節只在對應 reference。沿用已建立連線，不為讀取再次確認；保留具體破壞性操作授權但消除多份同意流程。統一 agent 設定與 channel 設定的責任界線。

  **應保留：** 按需載入 references、讀取現狀、版本驗證、設定備份與生效驗證、破壞性操作護欄與憑證遮蔽。

  **原文位置：** [主檔:4](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:4)、[主檔:25](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:25)、[主檔:38](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:38)、[主檔:43](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:43)、[主檔:119](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:119)、[主檔:151](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:151)、[主檔:193](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:193)、[主檔:213](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:213)、[主檔:228](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:228)、[主檔:257](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:257)、[主檔:285](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/SKILL.md:285)、[references/debug.md:19](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/openclaw-ops/references/debug.md:19)。

- [x] **25. postgrest-baas-builder**（中優先）

  **已完成並經使用者確認：** 保留 db-engineering 前置要求；主檔保留「自架 Supabase 補充」與「InsForge 補充」提醒，並加入平台與任務導讀；完整平台設定及範例保留於原參考文件，欄位慣例改引用。收尾改為實際角色、功能及平台可用的安全／效能驗證，同步修正 performance 參考文件的 advisors 要求。skill 1.3.0、plugin 1.26.0。各規則段落保留直接文件連結與閱讀時機。

  **可以改哪裡：** 任何 RLS/PostgREST 查詢先載完整 db-engineering；主檔同時載 Supabase Cloud、自架、InsForge/MCP 設定，不同平台內容無條件伴隨。欄位慣例與收尾重複規則。

  **建議改法（依討論調整）：** 保留 db-engineering 前置要求；先辨別平台及任務，再讀 RLS、Auth、效能、自架或 InsForge reference。MCP 安裝指令由 reference 提供；主檔保留自架 Supabase 與 InsForge 的易踩坑補充、平台分流與安全檢查，不重列通用欄位。

  **應保留：** RLS 與授權驗證、內建 Auth 適配、金鑰不進 git、明列查詢欄位、實際平台可用的安全/效能驗證。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:15)、[主檔:47](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:47)、[主檔:68](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:68)、[主檔:87](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:87)、[主檔:93](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:93)、[主檔:109](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/postgrest-baas-builder/SKILL.md:109)。

- [x] **26. project-memory**（高優先）

  **已完成並經使用者確認：** 保留自動讀取與記錄、完整索引及操作範例。縮短重複解釋，合併、儲存格式與匯出細節移至明確引用的參考文件；主檔與腳本提醒取消強制宣告沒有內容可記。skill 1.10.0、plugin 1.27.0。

  **可以改哪裡：** 每個既有專案啟動與收尾必載，必須口頭表態並自動 add；主檔大量解釋為何強制與為何採 JSONL，重複 add 命令及各階段規則。記憶全 key 永久輸出可能隨規模成長。

  **建議改法（依討論調整）：** 保留自動讀取與記錄及完整索引。主檔保留 load/search/add 的時機、範例與記錄資格，格式、合併、匯出細節移至有直接引用的參考文件。縮短重複解釋及腳本提醒，取消口頭無事宣告。

  **應保留：** 腳本處理轉義、去重可追溯、專案特有且實際發生的經驗、不把開放問題混入記憶、不自動匯出至版本控制文件。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:3)、[主檔:14](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:14)、[主檔:26](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:26)、[主檔:68](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:68)、[主檔:98](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:98)、[主檔:106](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:106)、[主檔:143](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:143)、[主檔:169](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:169)、[主檔:183](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:183)、[主檔:199](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:199)、[主檔:213](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/project-memory/SKILL.md:213)。

- [ ] **27. set-zeabur-conventions**（中優先）

  **已略過，保留原版：** 依使用者要求不修改，本項不勾選。

  **可以改哪裡：** 觸發限制中英重述，主檔在寫部署規範任務裡同載 MCP 安裝、完整 envsubst 維運知識及罕見 shared variable 故障；description 說只支援 Dockerfile，正文承認自動偵測建置，規則有漂移風險。

  **建議改法：** description 留一次精準部署目標與排除；主檔只留查既有段落、更新模板、驗證，MCP 安裝／環境變數生效／特殊診斷移按需 reference。長期約束只在模板保留一份；平台能力先依官方現況驗證再更新，避免把舊限制寫成永遠事實。

  **應保留：** 明確 Zeabur 意圖才改專案、compose 本機用途、AGENTS 區段不重複且尊重既有客製、安全金鑰與 runtime/build-time 差異。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:3)、[主檔:12](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:12)、[主檔:24](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:24)、[主檔:61](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:61)、[主檔:85](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:85)、[主檔:104](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/set-zeabur-conventions/SKILL.md:104)。

- [x] **28. ship-it**（高優先）

  **已完成並經使用者確認：** 限定分支到 PR 的交付流程，同步、提交、測試依專案及既有授權。採用現行交付文件並相容舊檔，PR 優先使用專案模板，區分推送、PR、CI 與部署狀態；記憶遵循新版 project-memory，PR 不附共同作者署名。skill 1.4.0、plugin 1.28.0。AI 主動追蹤必要 CI 與指定部署流程，受阻時回報未驗證項目，不等待 GitHub 通知。

  **可以改哪裡：** release/deploy/merge 等廣泛觸發卻只支援 feature branch→PR；固定 merge 同步、全套測試及新路徑 100% 覆蓋；收尾強制 project-memory。讀 legacy delivery-plan.md，與 eng-architect 的 delivery-status.md 不一致。

  **建議改法：** 定位清楚限定分支交付到 PR；先讀專案既有交付規則、已驗證證據與授權。同步和測試依變更風險及專案需求，避免重跑同一 diff 審查；PR 模板移素材並優先 repo 模板；記憶沿用 project-memory，自動記錄符合條件的實際經驗，不強制口頭宣告無事可記。統一狀態文件入口並兼容舊檔，不把 PR 建立稱完整上線。

  **應保留：** 秘密掃描、工作目標確認、修正引入的失敗、必要審查與 CI 證據、PR URL 和實際交付狀態。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:15)、[主檔:53](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:53)、[主檔:65](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:65)、[主檔:75](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:75)、[主檔:87](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:87)、[主檔:146](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:146)、[主檔:163](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/ship-it/SKILL.md:163)。

- [x] **29. software-engineering-guidelines**（高優先）

  **已完成並經使用者確認：** 原則保留完整判斷標準，Workflow 改為執行順序與原則引用，Pre-Ship Checklist 簡短核對範圍、驗證及完成條件。linter／type checker 與驗證缺口回報集中於測試原則。skill 1.4.2、plugin 1.20.2。保留 Principles 現有標題分節。格式檢查通過，使用者已要求提交並推送。

  **目前已確認並修改：** 文件操作沿用專案既有安排；沒有安排時，額外問題記在 AGENTS.md 的 Follow-ups，AGENTS.md 放實際指令、CLAUDE.md 作為入口。既有實質內容保留。澄清先查證可取得的資訊，重要缺項才確認，其餘採合理假設繼續。測試依影響範圍選擇，重大變更測試先行，專案完整測試照規則執行。skill 版本 1.4.1、plugin 版本 1.20.1；此為前一階段紀錄，重複敘述整理已完成。

  **可以改哪裡：** 任何軟體活動甚至一行變更都必載；原則→流程→清單重複同一事項。範圍外問題一律寫 AGENTS、初始化一律把 CLAUDE 改指標，有額外副作用。所有變更與全測試一刀切。

  **建議改法：** 先確定哪些屬使用者持續偏好留在單一規則來源，skill 保留有操作價值的範圍／成功條件／按風險驗證流程。三組重述合併一組；低風險文案等用比例適當驗證。範圍外問題先回報，只有專案採此慣例才寫 Follow-ups，沿用既有 CLAUDE/AGENTS 結構。

  **應保留：** 不擴需求、不覆蓋他人、不亂重構、重大變更測試先行、可驗證成功條件、不得削弱測試掩飾問題。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:3)、[主檔:8](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:8)、[主檔:42](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:42)、[主檔:44](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:44)、[主檔:48](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:48)、[主檔:88](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:88)、[主檔:109](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/software-engineering-guidelines/SKILL.md:109)。

- [x] **30. test-and-fix**（高優先）

  **已完成並經使用者確認：** 依測試目標選方法，主分支可測試，啟動資訊由專案取得；測試順序遵循 software-engineering-guidelines，沒有框架先評估既有工具。提交遵循使用者與專案安排，沒有指定時保留修正、回歸測試分開 commit 的原規則。移除固定連接埠與 delivery-plan.md 依賴，改讀相關既有任務紀錄。skill 1.4.0、plugin 1.21.0，README 同步。格式檢查通過，使用者已要求提交並推送；未實跑測試情境。

  **可以改哪裡：** 泛用測試 skill 寫死 web route、固定 port、base branch 禁測；為 CLI/library 也要啟動 app。修 bug 強制 fix/test 分開 commit，沒有框架就要 bootstrap。仍讀 delivery-plan.md。

  **建議改法：** 先依測試目標分 web／API／library／CLI；已提供測試命令或範圍即直接沿用，必要時才讀 branch diff，不要求 feature branch。從專案設定找啟動方法；fix loop 保留根因/回歸，commit 依授權。模板與偵測命令移參考，沒有框架可先提供重現驗證再判斷是否需引入依賴。統一狀態入口。

  **應保留：** 實際受影響路由及狀態驗證、失敗證據、根因未知才深入 investigate、回歸測試確實先壞後好。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:15)、[主檔:35](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:35)、[主檔:47](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:47)、[主檔:62](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:62)、[主檔:90](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:90)、[主檔:101](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:101)、[主檔:139](/Users/timlai/Developer/skills/plugins/dev-workflow/skills/test-and-fix/SKILL.md:139)。

### knowledge-tools

- [x] **31. excalidraw-diagram**（高優先）

  **已完成並經使用者確認：** 保留自然語意自動選用與三種模式，HTML Artifact 內優先沿用 HTML 做法。模式模板及完整回覆範例分檔，共用元素格式與色票集中維護，主檔保留直接引用與閱讀時機。依官方型別修正綁定與欄位禁令，要求實際畫面及相關互動驗證。skill 1.4.0、plugin 1.4.0。

  **可以改哪裡：** 主檔兩次列完整 element/text schema（233–295、311–368），Obsidian 包裝也重複（42–69、407–426）；三模式模板與三段回覆範例常駐；「畫圖／動畫圖」觸發過廣。主檔 boundElements 一律 null 與 reference 綁定範例有差異。

  **建議改法：** 主檔保留模式選擇、產出及驗證；每種模式模板、完整 schema、色票與回覆例移 references/assets，schema 單一來源。description 依自然語意及交付位置自動選用，不要求記住名稱；HTML Artifact 內優先沿用 HTML 方法；對 boundElements 等相容性禁令先查證適用版本，再統一範例，勿直接刪保護。

  **應保留：** 三模式實際格式差異、唯一 ID、JSON 合法性、文字可讀性與版面檢查。

  **原文位置：** [主檔:233](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/excalidraw-diagram/SKILL.md:233)、[主檔:311](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/excalidraw-diagram/SKILL.md:311)、[主檔:407](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/excalidraw-diagram/SKILL.md:407)。

- [ ] **32. llm-wiki**（高優先）

  **已略過，保留原版：** 依使用者要求不修改，本項不勾選。

  **可以改哪裡：** 把一般研究自動升級成建 wiki；每次查詢也先讀 schema/index/log＋一致性探查；初始化模板、Ingest、21項 lint、headless 安裝全常駐。筆記規律在主檔、模板、Ingest、Pitfalls 多次重述，且跨 skill 同步一份 checklist。

  **建議改法：** description 限定 wiki 建置／維護／查詢，不因研究一詞自建；按 init/ingest/query/lint 分流 references；templates 與 headless 安裝各按需讀。查詢只讀相關索引與頁面，寫入才查完整規範；七項檢核只留一份權威內容＋極短後備，減少每個 backlink 不處理理由的重複紀錄。

  **應保留：** 來源可追溯、raw 保護、矛盾不覆寫、去重、非遞迴回連、索引同步；不要因簡化丟掉這些功能。

  **原文位置：** [主檔:26](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/llm-wiki/SKILL.md:26)、[主檔:163](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/llm-wiki/SKILL.md:163)、[主檔:206](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/llm-wiki/SKILL.md:206)、[主檔:512](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/llm-wiki/SKILL.md:512)。

- [x] **33. mermaid-visualizer**（中優先）

  **已完成並經使用者確認：** 合併流程與驗收，完整圖例、色票及設計選項分檔，保留直接引用。自然語意觸發與 HTML Artifact 整合界線同步，語法限制依渲染環境判斷，修正參考文件的換行、不可見連線與註解示例。要求實際畫面驗證。skill 1.2.0、plugin 1.5.0。獨立完整圖例使用 mermaid fence，語法片段與錯誤示範使用 text。

  **可以改哪裡：** Quick Start 與 Workflow 是同一五步，Critical Syntax 與 Workflow 檢查及 Quality Checklist 重複；六種圖類型常識、虛擬配置選單與示例占主要篇幅。

  **建議改法：** 合併成一份流程與驗收；圖種類型表精簡，色票與完整範例按需讀；主檔保留 renderer 易錯語法。節點標點一律替換、style declarations 必有改為依實際 renderer 需求，先驗證再保留限定。

  **應保留：** 明確 ID／display label、subgraph 引用、目標 renderer 相容性與實際渲染驗證。

  **原文位置：** [主檔:22](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/mermaid-visualizer/SKILL.md:22)、[主檔:193](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/mermaid-visualizer/SKILL.md:193)、[主檔:270](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/mermaid-visualizer/SKILL.md:270)。

- [x] **34. obsidian-bases**（中優先）

  **已完成並經使用者確認：** 主檔保留最小可用範例、屬性與公式對應、引號、Duration 與空值提醒，以及實際 Obsidian 驗證。三份完整案例、schema／視圖／彙總表、屬性與公式範例分檔，主檔明確引用。觸發範圍維持。skill 1.2.0、plugin 1.6.0。

  **可以改哪裡：** 三個完整範例常駐（297–420），Duration 教學與 troubleshooting 重複；完整 file properties／summary 清單可按需查。

  **建議改法：** 主檔留最小 schema、屬性/公式命名與驗證；完整範例另存 references/examples，函數及彙總表按需求讀；Duration 與 null guard 各留一個代表反例。

  **應保留：** YAML 引號、空值檢查、Duration 先取數值欄位、formula 定義對應與 Obsidian 渲染驗證。

  **原文位置：** [主檔:197](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-bases/SKILL.md:197)、[主檔:297](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-bases/SKILL.md:297)、[主檔:465](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-bases/SKILL.md:465)。

- [ ] **35. obsidian-canvas-creator**（中優先）

  **已略過，保留原版：** 依使用者要求不修改，本項不勾選。

  **可以改哪裡：** 使用條件再次擴成任意 visual diagram；ID、間距、escaping 在產生/驗證/Critical/Pitfalls 重複；兩個範例只是重講分析流程。

  **建議改法：** description 與 body 同限 Obsidian Canvas；合併結構規則和驗收，保留一次；版面與尺寸/色票移按需 reference，兩個重述流程範例可移除。把固定 320/200 間距改為預設起點＋依卡片尺寸驗證。

  **應保留：** nodes/edges 結構、ID 唯一、引用存在、groups 圖層順序與實際開啟檢查。

  **原文位置：** [主檔:19](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-canvas-creator/SKILL.md:19)、[主檔:104](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-canvas-creator/SKILL.md:104)、[主檔:142](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-canvas-creator/SKILL.md:142)。

- [x] **36. obsidian-cli**（低優先）

  **已完成並經使用者確認：** 僅將外掛／主題開發段落原文移至 references/plugin-development.md，主檔加入直接引用及閱讀時機。一般操作、觸發範圍與完整開發指令維持。skill 1.1.1、plugin 1.6.1。

  **可以改哪裡：** 基本 CLI 內容已緊湊並以 obsidian help 查現況，未見需要大改；但 note 操作也常載入完整 plugin debug 段，description 重列多種同義操作。

  **建議改法：** 依討論保留主體與 description；開發命令原文移專用 reference，主檔標明開發／除錯外掛或主題前必讀。

  **應保留：** 執行中的 Obsidian 前提、help、vault/file/path 目標解析差異與引號語法。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-cli/SKILL.md:3)、[主檔:71](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-cli/SKILL.md:71)。

- [ ] **37. obsidian-markdown**（高優先）

  **已略過，保留原版：** 依使用者要求不修改，本項不勾選。

  **可以改哪裡：** 語法 skill 強制新 vault 採 llm-wiki 架構，混入另一項產品決策；每個新 note 被要求 frontmatter、embeds、callouts，非必要也易照做；完整例及一般 Math/Mermaid 教學常駐。

  **建議改法：** description 僅保留 Obsidian 特有語法觸發；移出強制 vault 架構到建庫 skill。流程改成依需要使用 properties/embed/callout，完整例移 reference，主檔只留特有差異。

  **應保留：** wikilinks、block IDs、嵌入、callouts 特有語法與既有 vault 慣例。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-markdown/SKILL.md:3)、[主檔:18](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-markdown/SKILL.md:18)、[主檔:198](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/obsidian-markdown/SKILL.md:198)。

- [x] **38. tutor**（中優先）

  **已完成並經使用者確認：** 已指定範圍直接開始，目標不明才選 Session；保留四題四選項與零暗示，依工具能力呈現，不適合時用一般文字。出題規則與檔案更新各維護一份，初始化模板分檔並直接引用。skill 1.2.0、plugin 1.7.0。

  **可以改哪裡：** 即使使用者已說考哪一節也強制再選 Session；綁死 AskUserQuestion 的四題四選項；read quiz-rules、無暗示、檔案更新與語言在 reference 與主檔反覆重述；初始化模板每次載入。

  **建議改法：** Session 僅目標不明才問；四題短回合保留預設，但工具格式移適配段，無工具可用正常文字測驗；模板按首次建立才讀，檢核與更新規則只保留單一來源。

  **應保留：** 零暗示、選項位置變化、四題短回合、錯題換情境、批改後更新 concept 與 dashboard。

  **原文位置：** [主檔:42](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor/SKILL.md:42)、[主檔:109](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor/SKILL.md:109)、[主檔:156](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor/SKILL.md:156)。

- [x] **39. tutor-setup**（高優先）

  **已完成並經使用者確認：** 僅採用第 1、3、4、5 項，模式確認與 CWD 限制維持。三模式分檔並直接引用，PDF 依內容抽取或查看原頁；深度保留原理、前置知識、例外及應用分析，題數比例改共用預設。同步以具體對應保護手寫內容與進度，刪改來源先核對處理，長度不作拒絕匯入門檻。skill 1.2.0、plugin 1.8.0。

  **可以改哪裡：** 三模式主檔負擔不均（Codebase 已外移，Document/Wiki 還完整常駐）；已知模式/來源仍多次必問確認；PDF 只能 pdftotext，無視掃描/圖表；Equal Depth 要將每個旁枝補成 textbook note。題數/比例機械化且兩模式分析題規則不一致；Wiki >200 行拒絕與 llm-wiki 長度不是拆分理由衝突。

  **建議改法：** 主檔縮為模式路由＋來源/學習進度保護，各模式按需讀；已明確指定不重問；PDF 依內容採文字抽取或必要視覺辨識；深度依學習目標，題目數及比例當預設。200行改內容判斷；輸入界線改使用者授權路徑，刪除/rename 同步另列可審閱處理，保留進度；統一 quality-checklist 對應規則。

  **應保留：** source mapping 不憑檔名、答案摺疊、增量 manifest、保留既有學習進度和手寫筆記、來源驗證。

  **原文位置：** [主檔:11](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:11)、[主檔:20](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:20)、[主檔:43](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:43)、[主檔:70](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:70)、[主檔:234](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:234)、[主檔:280](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/tutor-setup/SKILL.md:280)。

- [x] **40. zettelkasten**（中優先）

  **已完成：** 合併重複原則與檢核，新增／修改前完整讀取拆卡判準與範例；明定獨立主張應拆，不能以保留脈絡為由混放不同想法。保留兩份參考文件全文及 llm-wiki 既有引用，移除 Suggested Prompt，回報聚焦實際變更與重要邊界決策。

  **可以改哪裡：** 核心原則、流程、檢核、Quality/Common Mistakes 反覆講原子性、自己話與連結；同一 checklist 又複製 reference 並要求同步 llm-wiki（reference 02 行3）。

  **建議改法：** 主檔用一份短判斷清單作核心；詳例及拆卡過程留 references，不再重列原则/錯誤。跨 skill 保留一個權威 checklist 與明確讀取入口；只紀錄實際拆分及有影響邊界決策，不為每條未回連新增說明。

  **應保留：** 長度不是拆卡標準、不拆到失去自主性、既有筆記庫慣例、矛盾保留與非遞迴回連。

  **原文位置：** [主檔:31](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/zettelkasten/SKILL.md:31)、[主檔:76](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/zettelkasten/SKILL.md:76)、[主檔:99](/Users/timlai/Developer/skills/plugins/knowledge-tools/skills/zettelkasten/SKILL.md:99)。

### marketing-strategy

- [x] **41. content-growth-studio**（高優先）

  **已完成：** 保留自然語意自動觸發，排除僅因網址或一般潤稿誤啟用；合併模式表並標明參考文件讀取時機，取消假設數量門檻，依任務選用完整輸出模板，移除 Suggested Prompt。完整分析方法、通路規則與專項分工表保留。

  **可以改哪裡：** description 泛到任何 URL、上傳筆記、標題與重寫，容易越界一般內容任務；入口/模式在決策樹、Entry Paths、Mode Routing 與 references/01 重複；快速草稿固定三至五假設。

  **建議改法：** 縮到以成長為目的的內容規劃/製作；主檔合成一張模式路由表，場景例表移 references；每種模式明列何時讀哪份通路/輸出模板；缺口按需要列，不為數量發明假設。

  **應保留：** 來源意思、不可虛構成效/競品資料、跨通路須改寫節奏、專項技能只在需深入時使用。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:3)、[主檔:24](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:24)、[主檔:47](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:47)、[主檔:76](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:76)、[主檔:115](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/content-growth-studio/SKILL.md:115)。

- [x] **42. experiential-guerrilla-marketing**（高優先）

  **已完成：** 主檔整合為目標、場域、體驗、執行與衡量流程，四份參考文件保留框架、戰術、案例與模板並標明讀取時機。取消模組數量、完整 5E 與四層指標的硬性要求。成效採小幅修正：Canon 調查數字補來源保留，其餘未核實倍數移除，案例做法保留；依使用者修正，埋伏行銷聚焦手法與應用，移除專門法律限制，不加入道德評判。

  **可以改哪裡：** 行銷 KPI 等泛詞強制觸發；主檔大量理論教材、案例、年度趨勢/倍數主張，缺直接可核對來源；每活動強制多模組/完整5E；搭配八個技能表容易擴展工作。

  **建議改法：** 縮到體驗/游擊活動；主檔留目標→場域→參與機制→衡量與風險，理論/戰術/案例拆按需 reference；不固定至少兩模組；數字先查證加來源或改無數字示例，搭配技能僅按缺失能力選擇。

  **應保留：** SCHMITT 與5E 專業選擇框架、現場許可與不阻礙交通、活動目標和衡量一致。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:3)、[主檔:16](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:16)、[主檔:29](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:29)、[主檔:59](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:59)、[主檔:118](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:118)、[主檔:134](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:134)、[主檔:182](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:182)、[主檔:200](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/experiential-guerrilla-marketing/SKILL.md:200)。

- [x] **43. maslow-five-needs-marketing**（高優先）

  **已完成：** 五層都須分析需求、產品回應、依據或缺口與目標關聯，完成後才決定投入優先序，不能以低關聯或不投入略過。移除 IQ 人格、固定逐層投放與 70%／30% 配比；資料、排程、標題與 CTA 數量依需求，理論及五層判讀先完整讀，其他文件依工作目的載入。解除 copywriting 固定依賴，改用具體品質檢核與事實／承諾檢查，完整方法與模板保留。

  **可以改哪裡：** IQ300 角色重複兩次無可檢查行動價值；CTA/文案方向泛觸發；每次固定五層全產出、多 KPI/30天動作/每層三標題三CTA，且六份 reference 全串讀；硬綁 copywriting。

  **建議改法：** 移除空泛角色設定；限縮馬斯洛需求訊息策略；主檔保留五層判準及相關需求選取，低相關層標不適用，不強迫全層文案；完整跨通路方案才展開排程/KPI，參考按目的讀，長文案交現有寫作能力。

  **應保留：** 可驗證需求與訊息關係、真實證據、不假承諾、受眾不同可有不同優先序。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:3)、[主檔:15](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:15)、[主檔:60](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:60)、[主檔:73](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:73)、[主檔:92](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:92)、[主檔:129](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:129)、[主檔:137](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:137)、[主檔:181](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/maslow-five-needs-marketing/SKILL.md:181)。

- [x] **44. psychological-trigger-marketing**（中優先）

  **已完成：** 合併重複說明並明列參考讀取時機，七種觸發器與完整例句保留；取消固定組合與文案數量，單一 CTA／標題直接交付，完整策略格式保留於參考文件。三個情境與驗證清單改按行為和真實條件驗收，修正六種／七種不一致。

  **可以改哪裡：** description 與 When to Use 重複；七模組摘要與 references/01 再述；每次硬選二至四觸發器並至少三標題三CTA，即單一CTA需求也膨脹。

  **建議改法：** 主檔留受眾階段→觸發器選擇表及證據限制，詳細理論與例句按需讀；只用足以滿足任務的觸發器和候選數量；單一文案請求不強出完整 JSON 策略包。

  **應保留：** 真實限量/原價/見證依據、焦慮不能唯一手段、冷暖熱受眾差異。

  **原文位置：** [主檔:20](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:20)、[主檔:76](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:76)、[主檔:121](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:121)、[主檔:135](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:135)、[主檔:161](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/psychological-trigger-marketing/SKILL.md:161)。

- [x] **45. sor-marketing-strategy**（高優先）

  **已完成：** 保留完整 S/O/R 分析，合併重複措施表；取消固定項數與 30 天排程，參考文件依工作需求讀取。補齊第六項品牌態度，保留理論、案例與衡量方法，解除固定專項工具名稱，移除案例 Prompt 段落，文件改名為 references/05-application-scenarios.md，定位為七種應用情境與分析重點，主檔引用同步更新。信任與侵擾依實際效果分析，不另做道德評分。

  **可以改哪裡：** 泛 KPI/A-B 測試/CRM 觸發與排除單一實驗互相競爭；三類措施加 sor_map/策略行動等重複敘述；每類至少三因子與完整三十天計畫強制；四份 references 不分任務全讀。

  **建議改法：** 觸發縮到刺激→心理→行為的策略分析；主檔保留模型決策和反例，將措施合併成一張因果與衡量表；完整活動需求再加通路/實驗/排程；參考檔按刺激、心理、量測疑問讀取，專項交接不硬綁不存在的工具名。

  **應保留：** 刺激不能直接視為因果、信任與侵擾雙面判讀、前導/結果指標、假證據禁止。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:3)、[主檔:79](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:79)、[主檔:95](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:95)、[主檔:150](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:150)、[主檔:214](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/sor-marketing-strategy/SKILL.md:214)。

- [x] **46. threads-viral-growth**（高優先）

  **已完成並經使用者確認：** 保留一般社群文案的自然語意觸發，未指定平台時使用共通方法。新稿與既有材料改寫皆先查滿 Threads 平台討論、網路搜尋、競品／同類帳號、跨平台時事四類來源。來源受阻須說明缺口，不能算已查完；不因任務簡單或已有素材省略研究。

  **依討論採用的簡化：** 取消固定研究耗時、候選／留言配額、篇幅硬上限與每篇完整經營包。主檔集中流程、品質與閱讀時機，50 個開頭例句、五種結構、六種情緒與完整案例保留。快速指南的獨有短稿移入案例集後移除，語氣 prompt 段改成資料使用方法，圖卡製作 prompt 保留。

  **證據與一致性修正：** 核對 QSearch 原始研究，修正時段排名並移除無來源權重表；保留 Buffer 42% 觀察及 Berger／Milkman 情緒研究的適用範圍。移除無依據成效保證，行銷手法依事實與實際反效果判斷。Views 與觸及人數分開，模板取消固定成效門檻。skill 1.2.0、marketing-strategy plugin 1.7.0，README 描述同步。

  **驗證：** quick_validate、YAML／JSON、30 個相對連結與錨點、git diff --check 通過。逐句比對50個原有Hook例句完整保留，五種結構、六種情緒、三個完整案例與移入短稿均存在。現有skill數量與README表格／開頭均為61；審查進度沿用原始62項，本項已經使用者驗收。獨立規則走查四個情境後修正跨平台入口、受阻處理與少樣本結論的歧義，未實際執行貼文研究或驗證成效。使用者已確認並要求提交、推送；未同步安裝版本。

  **初次建議未採用部分：** 不限縮為僅Threads任務，不取消既有材料研究，也不將四類來源改成任選。舊建議不作後續執行依據。

  **目前位置：** [主流程](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/SKILL.md:29)、[四類來源研究](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/references/01-trend-research.md:12)、[數據口徑](/Users/timlai/Developer/skills/plugins/marketing-strategy/skills/threads-viral-growth/assets/analytics-template.md:5)。

### service-innovation

- [x] **47. ecosystem-map-and-blueprint**（中優先）

  **已完成並經使用者確認：** 保留服務設計、流程、接觸點與參與者關係的自然語意觸發。主檔依需求選圖並明列閱讀時機，兩套完整方法與案例分別移入 references。

  **依討論採用的簡化：** 合併重複工具選擇與協作規則，允許先用材料做草稿，正式作業依據須經相關角色驗證。缺口不預設靠科技解決，可減少步驟或改善交接。

  **完整性要求：** 保留生態系地圖與服務藍圖完整檢查清單，逐項區分已確認、待確認、不適用及理由。只取消案例專屬項目的強制套用，不省略人、組織、地點、系統、各類交換及藍圖各層的檢視。未知不能當成不適用。

  **定義與案例：** 修正為五個內容層與三條分界線，支援流程包含內部團隊。數位接觸點須完整，Tech Layer 是否獨立按需求判斷。配餐與 YouBike 案例保留，後者標明來源不可追溯的教學情境。沒有 Suggested Prompt 同類殘留。skill 1.2.0、service-innovation plugin 2.1.0。定位未改變，README 原列描述適用。

  **驗證：** quick_validate、YAML／JSON、兩個相對連結、16 項完整性檢查及 git diff --check 通過。skill 數與 README 表格／總數均為 61。已檢視草稿缺資料、非數位服務、內部支援及案例套用的規則一致性，未執行真實服務工作坊。使用者已驗收並要求提交、推送，未同步安裝版本。

  **目前位置：** [主檔](../../plugins/service-innovation/skills/ecosystem-map-and-blueprint/SKILL.md)、[生態系地圖](../../plugins/service-innovation/skills/ecosystem-map-and-blueprint/references/ecosystem-map.md)、[服務藍圖](../../plugins/service-innovation/skills/ecosystem-map-and-blueprint/references/service-blueprint.md)。

- [x] **48. scamper**（中優先）

  **已完成並經使用者確認：** 保留自然語意觸發，full 與 quick 都逐一檢視七維度，只有使用者指定部分維度時才縮小範圍。移除固定構想數、Top 3 與假設配額，保留具體構想、比較理由與下一步。

  **依討論採用的簡化：** 合併主檔與演練文件的重複流程，先發散再依目標及限制收斂。七維度方法必讀，其餘參考文件明列閱讀時機。模板同步調整，保留 M 的修改／放大／縮小及 R 的重組／逆向。不存在值得保留的構想時，說明探索及不採用原因。

  **案例與證據：** 保留七維度提問、白板擦、自然類比、受限材料、灰姑娘及企業案例。修正灰姑娘 P 分類，並補上真正轉用故事用途的示例。查到 Hussain 與 Carignan 原始摘要，保留 p=.003 與效應量，修正重複測量設計與因果推論。企業事實附來源，未核實的具體做法改為假設練習，移除無來源成效保證。沒有 Suggested Prompt 同類殘留。

  **驗證：** quick_validate、YAML／JSON、四個相對連結、七維度方法、Markdown 圍欄與 git diff --check 通過。skill 數與 README 表格／總數均為 61。獨立走查快速圖書館流程、指定 S／C 雨傘收納、完整白板擦教學三案，修正受限材料的範圍規則及案例 A 分類。未實測產品或營運成效。

  **版本與範圍：** skill 1.2.0、service-innovation plugin 2.2.0。README 原列描述仍符合定位，未改動。使用者已驗收並要求提交、推送，未同步安裝版本。

  **目前位置：** [主檔](../../plugins/service-innovation/skills/scamper/SKILL.md)、[方法](../../plugins/service-innovation/skills/scamper/references/01-dimensions-and-questions.md)、[演練](../../plugins/service-innovation/skills/scamper/references/02-practice-and-advanced.md)、[案例](../../plugins/service-innovation/skills/scamper/references/03-case-studies.md)、[模板](../../plugins/service-innovation/skills/scamper/references/04-output-templates.md)。

- [x] **49. service-design-workshop**（中優先）

  **已完成並經使用者確認：** 保留自然語意觸發，適用完整服務設計、工作坊與局部改善。單獨的 persona、旅程圖、生態系地圖或藍圖交由可用專用技能，完整任務可搭配使用。

  **依討論採用的簡化：** 取消兩項輸入及 3–5 假設配額，以問題、對象與場域是否足夠判斷。流程與成果合併成階段對照，完整任務涵蓋全套，局部修改處理相關階段及受影響交接。三份參考文件均明列閱讀時機，原則、方法與提問保留。

  **模板與驗證：** 分開後台活動與支援流程，補上角色、交接內容及對象。逐階段檢查完整性，取消填一項即可的門檻。原型驗證補上成功訊號、判斷依據與未達預期時的調整，保留五個驗證問題並提供假設示例。

  **設定與版本：** agents/openai.yaml 的 default_prompt 是介面呼叫文字，保留原設定。skill 1.2.0、service-innovation plugin 2.3.0，README 同步描述完整及局部需求。

  **驗證：** quick_validate、YAML／JSON、三個相對連結、Markdown 圍欄與 git diff --check 通過。方法、原則與介面設定比對 Git 確認未變，skill 數與 README 表格／總數均為 61。逐項走查完整設計、局部接觸點修改與缺資料草稿的規則，未執行真實工作坊或使用者測試。使用者已驗收並要求提交、推送，未同步安裝版本。

  **目前位置：** [主檔](../../plugins/service-innovation/skills/service-design-workshop/SKILL.md)、[模板](../../plugins/service-innovation/skills/service-design-workshop/references/service-design-output-templates.md)。

- [x] **50. service-innovation-case-study**（高優先）

  **已完成並經使用者確認：** 保留自然語意觸發，區分完整研究、課堂格式與局部分析。完整研究保留全條分析鏈及 25 個報告章節，局部研究核對相關上下游。主檔集中範圍、閱讀時機與交付，方法留在既有參考文件。

  **方法與模板：** 課堂模式保留 SWOT 各三項、八策略及 PESTEL 門檻，一般研究依問題與證據判斷。取消預設 ST、AX 客群與資源導向，保留四類策略、BMC 九格及延伸分析。研究面向逐項判斷適用來源，區分未找到、無法存取及確認未公開。修正藍圖五層三線、圖例與情緒評分，保留完整品質清單。輸出依工作區，不再綁定 /mnt。

  **版本與範圍：** skill 1.2.0、service-innovation plugin 2.4.0，README 同步完整、課堂與局部研究定位。未發現 Suggested Prompt 同類殘留。

  **驗證：** quick_validate、YAML／JSON、13 個相對連結、Markdown 圍欄與 git diff --check 通過。比對原模板確認 25 個章節與順序保留，Persona 副標改為複合人物。skill 數與 README 表格／總數均為 61。獨立走查圖書館局部定位、資料不足的課堂報告、顧客導向且採 SO 的完整研究三案，修正模板強制創辦人引言與風險等同情緒低點的殘留。此次為文件及規則驗證，未執行真實案例研究或圖表渲染。使用者已驗收並要求提交、推送，未同步安裝版本。

  **目前位置：** [主檔](../../plugins/service-innovation/skills/service-innovation-case-study/SKILL.md)、[研究流程](../../plugins/service-innovation/skills/service-innovation-case-study/references/01-research-protocol.md)、[分析鏈](../../plugins/service-innovation/skills/service-innovation-case-study/references/02-analysis-chain.md)、[區段規格](../../plugins/service-innovation/skills/service-innovation-case-study/references/03-section-specs.md)、[品質清單](../../plugins/service-innovation/skills/service-innovation-case-study/references/04-quality-checklist.md)、[模板](../../plugins/service-innovation/skills/service-innovation-case-study/assets/report-template.md)。

- [x] **51. service-innovation-workshop**（中優先）

  **已完成並經使用者確認：** 保留自然語意觸發，支援完整工作坊、局部發想、概念比較與既有方向驗證。取消兩項輸入、3–5 假設與至少三方案的配額，保留實質比較。SCAMPER 七維度逐一檢視，不強迫每維產生一案。

  **流程與交付：** 主檔依階段標明三份參考文件的閱讀時機，完整六段集中於既有模板，局部需求按範圍交付。測試補上觀察方式、比較對象及繼續／修正／停止的判斷依據。分類、機會來源、方法、風險清單與成功訊號例子保留。

  **版本與設定：** skill 1.2.0、service-innovation plugin 2.5.0，README 同步定位。agents/openai.yaml 的 default_prompt 是介面呼叫設定，維持原文。

  **驗證：** quick_validate、YAML／JSON、三個相對連結、Markdown 圍欄與 git diff --check 通過。比對 Git 確認視角參考及介面設定未變，skill 數與 README 表格／總數均為 61。逐項走查完整發想、已選定方案只做測試、SCAMPER 部分維度沒有合適改法三種情境，確認完整流程、局部範圍與七維度判斷各有對應規則。這是文件規則走查，未執行真實工作坊或原型測試。使用者已驗收並要求提交、推送，未同步安裝版本。

  **目前位置：** [主檔](../../plugins/service-innovation/skills/service-innovation-workshop/SKILL.md)、[方法](../../plugins/service-innovation/skills/service-innovation-workshop/references/service-innovation-methods.md)、[模板](../../plugins/service-innovation/skills/service-innovation-workshop/references/service-innovation-output-templates.md)。

### thinking-frameworks

- [x] **52. plan-grilling**（高優先）

  **已完成並經使用者確認：** 保留自然語意觸發、一次一題與推薦理由，先查事實，沿用已定案事項，處理影響方向、範圍、資源及驗收的未決選擇。完整十項審查保留，取消固定重構問題配額、兩週指標與每答必記時間戳。

  **方法與交付：** 訪談指南及計畫／決策模板分檔，主檔明列閱讀時機。保留使用者可驗收的工作切分及共用基礎工作，純文字整理不重問，改變能力或範圍時確認。紀錄實質決策與重要取捨，計畫依工作區慣例命名，以實際路徑交接。規劃不自動授權實作。 補上停止條件：資訊足以形成可執行、可驗收的計畫，且沒有待使用者決定的重要事項時結束提問，其餘列待驗證假設；使用者要求停止或先整理時交付目前結論與未決事項。

  **版本與驗證：** skill 2.3.0、thinking-frameworks plugin 0.41.0，README 同步。quick_validate、YAML／JSON、兩個相對連結、Markdown 圍欄及 git diff --check 通過。skill 數與 README 表格／總數均為 61。走查已定案功能的文字整理、尚待取捨的行銷計畫、無 Git 工作區的個人計畫三種情境，核對是否需要提問、落檔位置與交接規則；未執行真人訪談。使用者已驗收並要求提交、推送。

  **目前位置：** [主檔](../../plugins/thinking-frameworks/skills/plan-grilling/SKILL.md)、[訪談指南](../../plugins/thinking-frameworks/skills/plan-grilling/references/interview-guide.md)、[模板](../../plugins/thinking-frameworks/skills/plan-grilling/references/plan-template.md)。

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

- [x] **55. defuddle**（中優先）

  **可以改哪裡：** 49行本體已精簡，主要問題是 description 把每個 URL 都鎖成 MUST instead of WebFetch，且只用 .md 字尾判例外。

  **建議改法：** 工具可用且一般 HTML 抽取合適時使用；直接 markdown 依內容類型辨識，動態/登入頁留適合工具，失敗可 fallback；保留短 CLI 用法，不需要再拆 reference。

  **應保留：** --md、metadata 抽取和輸出格式這些真正工具差異。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/utilities/skills/defuddle/SKILL.md:3)、[主檔:16](/Users/timlai/Developer/skills/plugins/utilities/skills/defuddle/SKILL.md:16)。

  **已採用第 2、3、4 點並經使用者確認：** Markdown 依回應類型與本文辨識，不只看 .md 字尾，可用 WebFetch 或 curl 直接讀取。保留精簡主檔及 CLI 範例，未安裝時可用 npx，全域安裝留作重複使用選項。第 1 點未採用，原有一般網頁觸發與 WebFetch 優先序保留。skill 1.2.0、utilities plugin 1.2.0。

  **第 4 點已查證並依使用者確認修改：** 官方 src/fetch.ts 拒絕非 HTML 回應，src/cli.ts 將本機檔案按 UTF-8 HTML 解析，不支援直接解析 PDF。Defuddle 0.19.2 本機 HTML 實測：--json 同時輸出 content（HTML）與 contentMarkdown，--json --md 則 content 為 Markdown，沒有 contentMarkdown 欄位。README 已改為 HTML 網頁，JSON 輸出表已區分參數組合，原先認為 --json 不會同時輸出兩種格式的建議不準確。來源：https://github.com/kepano/defuddle/blob/main/src/cli.ts 、https://github.com/kepano/defuddle/blob/main/src/fetch.ts 。

  **驗證與交付：** quick_validate、YAML／JSON、description 與 git diff --check 通過，skill 數與 README 列數／總數均為 61。使用者已確認並要求提交、推送。

- [x] **56. folder-organizer**（中優先）

  **已依使用者要求刪除並經驗收：** 內容主要重述模型既有整理能力及通用檔案操作規則，未提供足以獨立保留的工具或方法。原文可從 Git 歷史取得。

  **同步調整：** README 移除項目，README 與 AGENTS.md 的現有 skill 數量改為 60。utilities plugin 與 marketplace 描述移除檔案整理，plugin 升至 1.3.0。審查仍以原始 62 項追蹤，其他已略過項目維持原決定。

  **驗證：** JSON 解析、skill 數／README 列數／總數一致、引用檢查及 git diff --check 通過。除了本項歷史紀錄，沒有剩餘 folder-organizer 引用。使用者已要求提交、推送。本機已安裝版本未移除。

- [x] **57. windows-rescue-from-linux**（中優先）

  **可以改哪裡：** 已做好按症狀讀 reference，安全限制有必要；仍每次先全套 bootstrap、Node/Claude/skill安裝，再問症狀，與末段先問症狀互斥；一律五階段、每個sudo說明加雙確認增加負擔。通用驗證區同列 dry-run 和真正 ntfsfix 寫入。

  **建議改法：** 保留安全入口與症狀路由，環境bootstrap另分準備USB需求及缺工具時讀；重複安全敘述合併成一次確認具体高風險步驟，沿用既有授權。驗證按實際修復選唯讀檢查，真正寫入 ntfsfix 留修復路徑，不當通用驗證。

  **應保留：** 唯讀掛載、寫前備份/壞碟先映像、BitLocker金鑰、hive備份、破壞性動作確認及 Linux 無法修復的界線。

  **原文位置：** [主檔:28](/Users/timlai/Developer/skills/plugins/utilities/skills/windows-rescue-from-linux/SKILL.md:28)、[主檔:76](/Users/timlai/Developer/skills/plugins/utilities/skills/windows-rescue-from-linux/SKILL.md:76)、[主檔:94](/Users/timlai/Developer/skills/plugins/utilities/skills/windows-rescue-from-linux/SKILL.md:94)、[主檔:269](/Users/timlai/Developer/skills/plugins/utilities/skills/windows-rescue-from-linux/SKILL.md:269)。

  **完成修改：** 分開救援碟準備與實機救援，按症狀讀參考、按需安裝工具，合併安全與授權規則。新增映像單檔提取、備份、替換與還原流程，版本不符仍可說明差異後試修。同步修正 registry 編輯、唯讀掛載、掃描與診斷腳本的錯誤判斷，補入使用者同意後由 AI 製作救援 USB 的下載、工具準備、目標確認、清除前完整備份、寫入與驗證流程，備份未驗證成功不清除。救援碟採完整系統安裝，工具與 skill 預裝在 USB 系統，驗收重開與離線功能，不以 Live USB 代替。更新 README；skill 1.2.3、utilities 1.4.3。

  **驗證：** YAML／JSON、引用、138 段 shell 範例語法、8 支腳本語法與相關模擬測試通過。用 wimlib 實際建立並提取 WIM／ESD／SWM 測試映像，單檔內容一致，錯誤路徑與 index 會失敗。尚未實測 Windows 開機、實際 NTFS 系統檔替換與 hive 寫回，USB 完整安裝亦未實機驗證。使用者已確認接受並要求提交、推送。

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

  **後續用字修正：** 加入「仍」的語意判斷與完整測試例句，避免在一般規則中加入不存在的轉折。同步原則、例集、反模式與最後檢查表；skill 1.9.3、plugin 1.20.2。

  **完成決定：** 使用者已確認並要求提交、推送。完整閱讀範例移到起草前，移除 Suggested Prompt，取消自動附加 Kept as-is 備註。依文章比較新增規則與三組範例：減少過度使用「代表」句型，按句意與中文習慣處理連接、條件及搭配，具體替換詞只作例句示範。原有「這代表每位照護者必須照看更多長者。」保留。

  **變更及驗證：** SKILL.md（1.9.2）、四份寫作參考文件及模式文件、plugin.json（1.19.2）與本清單。quick_validate、JSON／YAML、相對連結及 git diff --check 通過。兩個 Luna 曾比較 1.8.4 與 1.8.6，未見明顯全面改善；1.9.2 尚未重跑比較。測試文章與流程紀錄已清除，skill 的教學範例保留。以下為初次審查紀錄，未採用的建議不再列為待辦。

  **可以改哪裡：** 任何對話文字都觸發；46 行主檔要求讀五份參考文件，原則、反模式、清單重複。

  **建議改法：** 濃縮日常核心，長文、改稿與特殊文類才讀細節，例集改按需查閱；同一原則只維護一份完整定義。是否縮小所有回覆皆適用的範圍，另由使用者決定。

  **應保留：** 不編造、原意與適用範圍、台灣用語、文類慣例、具體可讀。細緻例句先保留作查閱材料。

  **原文位置：** [主檔:4](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/human-writing/SKILL.md:4)、[主檔:24](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/human-writing/SKILL.md:24)、[references/final-checklist.md:3](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/human-writing/references/final-checklist.md:3)。

- [x] **61. landing-page-studio**（高優先）

  **可以改哪裡：** 固定三個價值主張、預設高動畫、多稿比較、至少四類動畫；缺輸出模式停止，React 還先問技術組合。要求同時寫在主檔及腳本。

  **建議改法：** 先完成一個符合轉換目標的頁面，再按實際問題修正；多稿、動畫種類改選項，價值主張依真實內容決定。沿用現有技術，只問改變目標的缺項。同步調整輸入驗證與動畫清單腳本，合併重複檢查。

  **應保留：** 主要行動按鈕、真實內容、窄螢幕可讀、減少動態偏好、效能與可用性驗證。

  **原文位置：** [主檔:41](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:41)、[主檔:59](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:59)、[主檔:97](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:97)、[主檔:101](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:101)、[主檔:128](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/SKILL.md:128)、[scripts/validate_intake.py:24](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/scripts/validate_intake.py:24)、[scripts/validate_intake.py:88](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/landing-page-studio/scripts/validate_intake.py:88)。

  **完成修改：** 保留使用者指定的三個價值主張、至少兩類真實信任證據，以及高動畫、至少四類動畫的預設。沿用既有技術與設計流程，單版依問題迭代，不額外強制產生多份完整稿。保留各參考教學並合併重複流程與交付欄位；修正輸入型態、減少動態與模板降級問題。依後續確認保留高動畫預設，WebGL／CDN 失效明確報錯，不自動替代；減少動態偏好另行尊重。skill 2.1.1、writing-and-design 1.21.1。使用者已確認接受並要求提交、推送。 後續失效處理驗證涵蓋兩模板的正常、WebGL 初始化失敗、動畫依賴載入失敗、context 遺失及減少動態，共十個情境；失敗顯示可見錯誤，不啟動替代動畫，並已查看錯誤畫面。

  **驗證：** 輸入與動畫腳本測試、YAML／JSON、引用、skill／README 數量及 git diff --check 通過。React 測試副本 production build 通過；兩套模板的正常／CDN 與 WebGL 失敗、動態偏好切換、三斷點與 CTA 檢查通過。失效報錯調整前，填入測試文案後 Lighthouse：React 手機／桌面效能皆 100，HTML 手機 94、桌面 100，無障礙皆 100。Three 獨立區塊仍有大小提醒；未測真實客戶內容、後端與部署。測試依賴只在暫存副本，測試 server 已停止。

- [x] **62. open-slide-studio**（中優先）

  **可以改哪裡：** description 塞框架功能、內建技能和流程，格式限制與指令在多節重複。已有不複製上游規範的好設計。

  **建議改法：** description 留網頁簡報與可編輯 PPTX 排除；合併流程、速查、常見錯誤重複。新工作區才初始化與完整視覺接軌，改一頁沿用主題；工作區規則依當下 AGENTS.md，避免維護兩份。

  **應保留：** 圖片版 PPTX 不可編輯的告知、Node 前提、theme 交接、不覆寫上游管理檔。

  **原文位置：** [主檔:3](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:3)、[主檔:49](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:49)、[主檔:80](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:80)、[主檔:88](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:88)、[主檔:96](/Users/timlai/Developer/skills/plugins/writing-and-design/skills/open-slide-studio/SKILL.md:96)。

  **完成修改：** 精簡 description 與重複流程，保留自然語意觸發、格式分流與 design-studio 視覺交接。區分新建與局部修改，沿用既有主題；建立或調整主題時依工作區 create-theme 產出主題文件及預覽檔。skill 1.0.4、writing-and-design 1.21.2。使用者已確認接受並要求提交、推送。

  **驗證：** quick_validate、YAML／JSON、description、引用、Markdown 圍欄、skill／README 數量及 git diff --check 通過。本次為指引修改，未建立或部署實際簡報。

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
