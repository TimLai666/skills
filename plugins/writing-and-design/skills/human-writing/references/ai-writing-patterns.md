# AI writing patterns to remove

Use this checklist after drafting or rewriting.

## High-priority patterns

- Invented shorthand modifiers
  - Examples:「不繞」「最穩」「一直在撐」「很頂」「不演」, and bare potential complements:「XX接得住」「XX補得完」「讀得完的XX」
  - Fix: rewrite the whole sentence to say the concrete thing in ordinary spoken wording; when no repair that keeps the word sounds natural, drop the word and use an ordinary verb（「接得住」→「流量翻倍也能承受」;「不演」→「不假裝是當場想到的」）. See rules 2 and 3 in [human-writing-principles.md](./human-writing-principles.md).

- Clipped verbs
  - Examples:「範例照抄也要驗」「命中的已拆」「表現優異的項目也要查」「改好再給你驗」, and the verb dropped entirely:「一律進例集」
  - Fix: write the verb whole and say what it acts on, and keep the actor recoverable（「改好再給你驗」→「改好了，等你看過確認」）. See rules 5 and 10 in [human-writing-principles.md](./human-writing-principles.md).

- Invented abbreviations
  - Examples:「產品經理」cut to「產經」, or an acronym coined mid-paragraph in English.
  - Fix: keep only abbreviations already in circulation, or choose a shorter complete wording（「產經」→ write「產品經理」out）. See rule 10 in [human-writing-principles.md](./human-writing-principles.md).

- Unfamiliar imagery and literal translated terms
  - Examples:「基線」「閉環」when the reader does not already use them.
  - Fix: say who does what, what information they have, and what remains unresolved. See rule 9 in [human-writing-principles.md](./human-writing-principles.md); example 17 in [human-writing-examples.md](./human-writing-examples.md) shows the full rewrite of「閉環」.

- Invented details in a rewrite
  - Examples: adding a price, a time, a person, a feature, or a scene that the source text does not provide.
  - Fix: use only facts from the source or facts you have verified. If no concrete detail is available, remove the vague claim instead of making one up.

- Vague attribution
  - Examples: "experts say", "observers note", "industry reports suggest"
  - Fix: name the source or state the claim directly.

- Fake profundity
  - Examples: "marks a pivotal moment", "reflects a broader shift", "underscores the importance"
  - Fix: say what changed and why it matters in plain terms.

- Promotional padding
  - Examples: "vibrant", "groundbreaking", "seamless", "powerful", "rich", "stunning"
  - Fix: replace with specifics or remove.

- AI vocabulary clusters
  - Examples: "additionally", "delve", "showcase", "foster", "landscape", "pivotal", "valuable", "underscores"
  - Fix: use simpler, more ordinary wording.

- Filler transitions
  - Examples: "in order to", "it is important to note", "at this point in time"
  - Fix: compress to direct language.

- Padding verbs and classical residue in ordinary Chinese prose
  - Examples:「進行討論」「加以檢視」where「討論」「檢視」does the work;「係」「惟」「俾」in an email, product doc, or announcement; compressed forms like「未」「免」in conversational reporting:「編號未動，連結免改」.
  - Fix: cut the padding verb and keep the real one（進行優化→優化）; replace classical residue with plain words（係→是、惟→但、未→沒、免→不用）. Characters like 未 and 免 rarely appear in natural speech, and two compressed forms in a row is a blatant machine signal: write「編號沒動，連結也不用改」. Keep them only in genres whose register requires them（公文、契約、法律條款）— see the fixed-format genre rule in [human-writing-principles.md](./human-writing-principles.md).

- Empty「直接」intensifier
  - Examples:「手機版可以直接簽核」in feature copy. Most common in proposals and pitches, where「直接」is padded before a verb purely to add force while the sentence never says how.
  - Fix: delete「直接」and look at what remains（「手機版可以直接簽核」→「手機版可以簽核」, nothing lost）. If the claim is empty, state the actual mechanism or cut the sentence. Keep「直接」only when it literally means a step is skipped.

- Over-hedging
  - Examples: "could potentially", "it may perhaps", "seems to suggest"; also the structural form, a limitation or disclaimer appended to every claim, even in a proposal meant to persuade.
  - Fix: keep only the uncertainty the claim actually needs, and park risks in the genre's own risk section instead of on each sentence. See rule 8 in [human-writing-principles.md](./human-writing-principles.md).

## Structural patterns

- Rule-of-three overuse
  - Fix: stop forcing every list into three items.

- Outline-sounding prose
  - Examples: "challenges and opportunities", "future outlook", "key takeaways" when the body is empty
  - Fix: turn headings into real claims or remove them.

- Em dash abuse
  - Fix: use commas or periods unless the interruption genuinely matters.
  - In Chinese, do not lean on long or repeated 破折號 just to fake tone or emphasis.

- Symmetry artifacts
  - Examples: every sentence same length, every paragraph same arc, repeated "not just X, but Y" or「不是……而是……」
  - Fix: vary cadence and sentence design. Keep「不是……而是……」only where a real misunderstanding needs correcting.

- Setup-and-reveal reflex（先抑後揚、先破後立）
  - Examples:「很多人以為……但其實……」「傳統做法的問題在於……而我們……」, sections that first build a wrong view just to knock it down.
  - Fix: state the point directly and support it. Keep one correction only when the reader actually holds the misconception; never invent one, and never use the move as the skeleton of every section.

- Slogan rhythm from stacked fragments
  - Examples:「看見問題、快速判斷、即時處理、完整追蹤」— short fragments piled up with 頓號 for cadence. The same rhythm shows up in summaries and reports as strung negations:「不編造、不演、不平均分配」.
  - Fix: unless the items genuinely need enumerating, write full sentences that state how they relate:「不編造、不演、不平均分配」→「不編造個人經歷，不演出自發性，也不把情緒平均鋪在每一句」. Example 28 in [human-writing-examples.md](./human-writing-examples.md) rewrites the first example in full.

- Headline-style body copy
  - Examples:「效率，從此不同。」「一個平台，解決所有問題。」— body paragraphs built from tagline sentences that would work unchanged as slide titles.
  - Fix: write running prose. Give each sentence a subject, a verb, and a connection to the sentence before it; keep headline diction in actual headings.

- Semicolon overuse in ordinary Chinese prose
  - Fix: replace each semicolon with a full stop, comma, or clearer sentence boundary. See rule 26 in [human-writing-principles.md](./human-writing-principles.md).

## Bilingual cleanup notes

- In Chinese, avoid translated English rhetoric such as empty abstract nouns and forced formalism.
- In English, avoid over-smoothed consultant language when plain writing would be clearer.
- In mixed-language text, remove stiffness without flattening deliberate code-switching.
