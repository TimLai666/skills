# 音訊設計規則 · huashu-design

> 所有動畫 demo 的音訊應用配方。和 `sfx-library.md`（資產清單）配套使用。
> 實戰錘鍊：huashu-design 發布 hero v1-v9 迭代 · Anthropic 三支官方片子的 Gemini 深度拆解 · 8000+ 次 A/B 對比

---

## 核心原則 · 音訊雙軌制（鐵律）

動畫音訊**必須分兩層獨立設計**，不能只做一層：

| 層 | 作用 | 時間尺度 | 和視覺的關係 | 佔據頻段 |
|---|---|---|---|---|
| **SFX（節拍層）** | 標記每個視覺 beat | 0.2-2 秒短促 | **強同步**（幀級對齊） | **高頻 800Hz+** |
| **BGM（氛圍底）** | 情緒鋪底、聲場 | 連續 20-60 秒 | 弱同步（段落級） | **中低頻 <4kHz** |

**只做BGM的動畫是半成品**——觀眾潛意識感知到「畫在動但沒聲音響應」，廉價感的根源就在這裡。

---

## 金標準 · 黃金配比

這幾組數值是實測 Anthropic 三支官方片子 + 我們自己 v9 定版對比得出的**工程硬參數**，直接套用即可：

### 音量
- **BGM 音量**：`0.40-0.50`（相對滿刻度 1.0）
- **SFX 音量**：`1.00`
- **響度差**：BGM 比 SFX peak **低 -6 到 -8 dB**（不是靠SFX絕對響度突出，靠響度差）
- **amix 參數**：`normalize=0`（絕不用 normalize=1，會把動態範圍壓平）

### 頻段隔離（P1 硬最佳化）
Anthropic 的秘訣不是「SFX 音量大」，是**頻段分層**：

```bash
[bgm_raw]lowpass=f=4000[bgm]      # BGM 限制在 <4kHz 的中低頻
[sfx_raw]highpass=f=800[sfx]      # SFX 推到 800Hz+ 的中高頻
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]
```

為什麼：人耳對 2-5kHz 區間最敏感（即「presence 頻段」），SFX 如果都在這個區間，BGM 又全頻段覆蓋，**SFX 會被BGM的高頻部分遮蓋**。用 highpass 把 SFX 推高 + lowpass 把 BGM 壓下，兩者在頻譜上各佔一方，SFX 清晰度直接上一檔。

### Fade
- BGM 入：`afade=in:st=0:d=0.3`（0.3s，避免硬切）
- BGM 出：`afade=out:st=N-1.5:d=1.5`（1.5s 長尾，收束感）
- SFX 自帶 envelope，不需要額外 fade

---

## SFX cue 設計規則

### 密度（每10秒多少個SFX）
實測 Anthropic 三支片子的 SFX 密度有三檔：

| 片子 | 每10s SFX 數 | 產品性格 | 場景 |
|---|---|---|---|
| Artifacts（ref-1） | **~9個/10s** | 功能密集、資訊多 | 複雜工具演示 |
| Code Desktop（ref-2） | **0個** | 純氛圍、冥想感 | 開發工具專注狀態 |
| Word（ref-3） | **~4個/10s** | 平衡、辦公節奏 | 生產力工具 |

**啟發式**：
- 產品性格冷靜/專注 → SFX 密度低（0-3個/10s），BGM 為主
- 產品性格活潑/資訊多 → SFX 密度高（6-9個/10s），SFX 驅動節奏
- **不要填滿每個視覺 beat**——留白比密集更高級。**刪掉 30-50% 的 cue 會讓剩下的更有戲劇性**。

### Cue 選擇優先順序
每個視覺 beat 不都要配 SFX。按這個優先順序選：

**P0 必配**（省略會有違和感）：
- 打字（終端/輸入）
- 點選/選擇（使用者決策時刻）
- 焦點切換（視覺主角轉移）
- Logo reveal（品牌收束）

**P1 推薦配**：
- 元素入場/離場（modal / card）
- 完成/成功回饋
- AI 生成開始/結束
- 重大過渡（scene 切換）

**P2 選配**（多了會亂）：
- hover / focus-in
- 進度 tick
- 裝飾性 ambient

### 時間戳對齊精度
- **同幀對齊**（0ms 誤差）：點選/焦點切換/Logo 落定
- **前置 1-2 幀**（-33ms）：快速 whoosh（給觀眾心理預期）
- **後置 1-2 幀**（+33ms）：物體落地/impact（符合真實物理）

---

## BGM 選擇決策樹

huashu-design skill 自帶 6 首 BGM（`assets/bgm-*.mp3`）：

```
動畫性格是什麼？
├─ 產品發布 / 技術演示 → bgm-tech.mp3（minimal synth + piano）
├─ 教學講解 / 工具使用 → bgm-tutorial.mp3（warm, instructional）
├─ 教育學習 / 原理解釋 → bgm-educational.mp3（curious, thoughtful）
├─ 行銷廣告 / 品牌宣傳 → bgm-ad.mp3（upbeat, promotional）
└─ 同類風格需要變體 → bgm-*-alt.mp3（各自替代版）
```

### 無 BGM 的場景（值得考慮）
參考 Anthropic Code Desktop（ref-2）：**0 SFX + 純 Lo-fi BGM** 也能很高級。

**何時選無BGM**：
- 動畫時長 <10s（BGM 建立不起來）
- 產品性格是「專注/冥想」
- 場景本身有環境音/講解聲
- SFX 密度很高時（避免聽覺過載）

---

## 場景配方（開箱即用）

### 配方 A · 產品發布 hero（huashu-design v9 同款）
```
時長：25 秒
BGM：bgm-tech.mp3 · 45% · 頻段 <4kHz
SFX 密度：~6個/10s

cue：
  終端打字 → type × 4（間隔0.6s）
  回車     → enter
  卡片匯聚 → card × 4（錯峰 0.2s）
  選中     → click
  Ripple   → whoosh
  4次焦點  → focus × 4
  Logo     → thud（1.5s）

音量：BGM 0.45 / SFX 1.0 · amix normalize=0
```

### 配方 B · 工具功能演示（參考 Anthropic Code Desktop）
```
時長：30-45 秒
BGM：bgm-tutorial.mp3 · 50%
SFX 密度：0-2個/10s（極少）

策略：讓 BGM + 講解 voiceover 驅動，SFX 只在**決定性時刻**（檔案儲存/命令執行完成）
```

### 配方 C · AI 生成演示
```
時長：15-20 秒
BGM：bgm-tech.mp3 或無 BGM
SFX 密度：~8個/10s（高密度）

cue：
  使用者輸入 → type + enter
  AI 開始處理 → magic/ai-process（1.2s 迴圈）
  生成完成 → feedback/complete-done
  結果呈現 → magic/sparkle
  
亮點：ai-process 可以迴圈 2-3 次貫穿整個生成過程
```

### 配方 D · 純氛圍長鏡頭（參考 Artifacts）
```
時長：10-15 秒
BGM：無
SFX：單獨使用 3-5 個精心設計的 cue

策略：每個 SFX 都是主角，沒有BGM「糊在一起」的問題。
適合：單產品慢鏡頭、特寫展示
```

---

## ffmpeg 合成模板

### 模板 1 · 單 SFX 疊加到影片
```bash
ffmpeg -y -i video.mp4 -itsoffset 2.5 -i sfx.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4
```

### 模板 2 · 多 SFX 時間軸合成（按cue時間對齊）
```bash
ffmpeg -y \
  -i sfx-type.mp3 -i sfx-enter.mp3 -i sfx-click.mp3 -i sfx-thud.mp3 \
  -filter_complex "\
[0:a]adelay=1100|1100[a0];\
[1:a]adelay=3200|3200[a1];\
[2:a]adelay=7000|7000[a2];\
[3:a]adelay=21800|21800[a3];\
[a0][a1][a2][a3]amix=inputs=4:duration=longest:normalize=0[mixed]" \
  -map "[mixed]" -t 25 sfx-track.mp3
```
**關鍵參數**：
- `adelay=N|N`：前面是左聲道延遲(ms)，後面是右聲道，寫兩遍保證立體聲對齊
- `normalize=0`：保留動態範圍，關鍵！
- `-t 25`：截斷到指定時長

### 模板 3 · 影片 + SFX track + BGM（帶頻段隔離）
```bash
ffmpeg -y -i video.mp4 -i sfx-track.mp3 -i bgm.mp3 \
  -filter_complex "\
[2:a]atrim=0:25,afade=in:st=0:d=0.3,afade=out:st=23.5:d=1.5,\
     lowpass=f=4000,volume=0.45[bgm];\
[1:a]highpass=f=800,volume=1.0[sfx];\
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k final.mp4
```

---

## 失敗模式速查

| 症狀 | 根因 | 修復 |
|---|---|---|
| SFX 聽不見 | BGM 高頻部分遮蓋 | 加 `lowpass=f=4000` 給BGM + `highpass=f=800` 給SFX |
| 音效過響刺耳 | SFX 絕對音量太大 | SFX 音量降到 0.7，同時降低 BGM 到 0.3，保持差值 |
| BGM 和 SFX 節奏衝突 | BGM 選錯了（用了有強beat的music） | 換成 ambient / minimal synth 的 BGM |
| 動畫結束 BGM 突然斷 | 沒做 fade out | `afade=out:st=N-1.5:d=1.5` |
| SFX 重疊成糊 | cue 太密 + 每個 SFX 時長太長 | SFX 時長控到 0.5s 以內，cue 間隔 ≥ 0.2s |
| 公眾號 mp4 沒聲音 | 公眾號有時會 mute auto-play | 不用擔心，使用者點開會有聲音；gif 本來就沒聲音 |

---

## 和視覺的聯動（進階）

### SFX 音色要和視覺風格匹配
- 暖米/紙張感視覺 → SFX 用**木質/柔和**音色（Morse, paper snap, soft click）
- 冷黑科技視覺 → SFX 用**金屬/數位**音色（beep, pulse, glitch）
- 手繪/童趣視覺 → SFX 用**卡通/誇張**音色（boing, pop, zap）

我們當前 `apple-gallery-showcase.md` 的暖米底色 → 搭配 `keyboard/type.mp3`（mechanical）+ `container/card-snap.mp3`（soft）+ `impact/logo-reveal-v2.mp3`（cinematic bass）

### SFX 可以引導視覺節奏
進階技巧：**先設計 SFX 時間軸，然後調整視覺動畫去對齊 SFX**（不是反過來）。
因為 SFX 每個 cue 都是一個「鐘錶 tick」，視覺動畫配合 SFX 節奏會非常穩——反之 SFX 去追視覺，常常 ±1 幀對不上就有違和感。

---

## 品質檢查清單（發布前自檢）

- [ ] 響度差：SFX peak - BGM peak = -6 到 -8 dB？
- [ ] 頻段：BGM lowpass 4kHz + SFX highpass 800Hz？
- [ ] amix normalize=0（保留動態範圍）？
- [ ] BGM fade-in 0.3s + fade-out 1.5s？
- [ ] SFX 數量是否合適（按場景性格選密度）？
- [ ] 每個 SFX 和視覺 beat 同幀對齊（±1 幀內）？
- [ ] Logo reveal 音效時長夠（建議 1.5s）？
- [ ] 關閉 BGM 聽一遍：SFX 單獨是否足夠有節奏感？
- [ ] 關閉 SFX 聽一遍：BGM 單獨是否有情緒起伏？

兩層任何一層單獨聽都應該自洽。如果只有兩層疊加才好聽，說明沒做好。

---

## 參考

- SFX 資產清單：`sfx-library.md`
- 視覺風格參考：`apple-gallery-showcase.md`
- Anthropic 三支片子深度音訊分析：AUDIO-BEST-PRACTICES.md（作者本地資料，未隨倉庫分發）
- huashu-design v9 實戰案例：hero-animation-v9-final.mp4（作者本地樣本，未隨倉庫分發）
