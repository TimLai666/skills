# Human writing principles

Use these rules to make prose feel written by a person. They follow the order in which you make decisions: what to say, who will read it, how to structure it, how it should sound, and finally punctuation.

## Make it concrete

### 1. Prefer specificity over abstraction

- Replace broad claims with concrete points.
- Use nouns and verbs that name the thing instead of circling around it.
- Cut lines that only announce importance without adding information.

### 2. Do not use abstract adjectives and adverbs

Abstract modifiers can feel descriptive to the writer, but they give the reader no picture of what happened or what makes something good. The reader has to guess. Watch for four forms:

- **AI-invented shorthand that no real person says**, such as「不繞」「最穩」「一直在撐」「很頂」. These sound punchy to the model but are not how people talk, and the reader cannot even tell what quality is being claimed. This form is the strongest AI tell of the four.
- **Impression summaries**, such as「很好」「很棒」「非常愉快」. They report the writer's feeling about the thing instead of the thing, so the picture in the writer's head never reaches the reader.
- **Ambiguous abstractions**, such as「彈性」「完善」or "robust", "seamless". Every reader decodes them differently, so the writer thinks the point is made while each reader understands something else.
- **Ornate stacked modifiers**, such as「深刻地」「優雅地」「淋漓盡致」. They perform style without adding content. If deleting the word loses no information, it was empty.

Rewrite the sentence in ordinary words. Say what happened, how much, compared with what, what it looks like in use, or what the reader can do. If you do not know a concrete detail, remove the modifier and keep the plain statement. Never invent a number or detail to fill the gap.

The test is whether the reader can picture the scene or carry out the operation, not whether the sentence has a number.「結帳從五步縮成兩步」still fails because the reader does not know those five steps. Concrete writing lets the reader follow the action:「以前在購物網站下單，每次都要重打一遍地址。改版後登入會員，結帳頁直接帶出上次的地址，按送出就完成了」.

The ban targets modifiers that replace content, not all modifiers. When a sentence is already concrete and unambiguous, a modifier can ride on it:「按送出就結束了，順很多」works because the reader has just seen the operation and knows exactly what "順" refers to. Two limits still apply: do not reuse the same modifier across the text, and do not attach a modifier to every sentence. When most sentences stand plain, the few modifiers that remain actually register.

### 3. Give every action and object an anchor

- Every verb needs a stated object, and every scene needs a stated setting.「一頁一頁按」— pressing what, on which screen?「登入」— logging into which site or app? If the reader has to guess what an action lands on or where it takes place, the sentence is not concrete yet, no matter how plain it sounds.
- Establish the setting once, early:「在購物網站買東西」. After that, later actions inherit the setting and do not need to re-specify it. Anchoring is done at the scene level, not by re-explaining every sentence.
- Stop condition: the text is concrete enough when the intended reader would no longer ask「哪個？」「按什麼？」about anything that matters to the point. Specificity serves the reader's purpose. Do not drill down forever or pad the text with detail the point does not need.

## Write for a reader with zero context

### 4. Assume zero shared context

- Write as if the reader has none of the Agent's prior conversation, planning, reasoning, project background, or unstated domain knowledge.
- Do not use「如上」「這一層」「前述問題」or similar references unless the current text has clearly introduced them.
- Make the reader's understanding depend on what is written, not on what the writer remembers thinking.

### 5. Keep internal reasoning out of the final prose

- Do not assume the reader knows the categories, layers, sequence, or terminology created during planning.
- Translate internal frameworks into concrete actions, observable facts, order, reasons, or consequences.
- Introduce a concept before using it as a shared reference. If it cannot help the reader understand or act, remove it.

### 6. Do not over-explain

- Explain what the reader needs to understand the point, then stop.
- Do not add an answer to an objection, accusation, or inner judgment that no one raised.
- If a sentence only defends against an imagined criticism and removing it does not weaken the point, remove it.

### 7. Avoid unexplained niche vocabulary

- Prefer common words over niche terms, jargon, project shorthand, and author-created labels.
- If a term such as「剪刀差」is necessary, explain it in plain language at first use. Otherwise, directly describe the difference or consequence it refers to.
- Do not treat a familiar term within one field as familiar to every reader.
- Do not use unfamiliar imagery or literal translated terms just because they sound compact or professional. Words such as「基線」and「閉環」make readers stop and work out what the sentence means. Unless the intended reader already uses the term and its technical precision matters, replace it with the people, actions, information, and unresolved consequence it hides.

### 8. Do not clip a two-syllable verb down to one character

- A one-character Chinese verb needs something behind it to stand on: an object（查資料）, a complement（改好了、查清楚）, or an aspect marker（測過了、拆掉）. Left bare at the end of a clause, it stops sounding like anything a person would say.「範例照抄也要驗」「命中的已拆」「表現優異的項目也要查」are all the same failure.
- Clipping the verb usually drops its object with it, so putting the second character back is not enough.「範例照抄也要驗一次」reads more smoothly, but the reader still cannot tell what to verify. Write「就算照抄範例，也要自己檢查每一條有沒有放錯欄位」. This is rule 3 from another angle: a verb worn down to one character is usually the sign that its object went missing.
- Status columns in a table are the exception. The row subject already supplies the object, so it does not need repeating, but the verb still has to be whole: write「驗過」, not「已驗」.
- Column width is not a reason to shave characters. When something has to be shorter, choose a shorter complete wording instead.
- The same applies to nouns: do not coin an abbreviation on the spot. Use only ones already in circulation（健保、台大、API）, and drop any that collides with an existing word —「產品經理」cut down to「產經」reads as 產業經濟.
- In English the matching habit is inventing an acronym mid-paragraph, or using a verb as a noun ("a solve", "the ask", "learnings"). Restore the ordinary wording.

### 9. Remove unexplained figurative language

- Keep a metaphor only when the reader can tell what it refers to and what it means in the situation.
- Replace vague images such as「漏過去」with the concrete missing data, action, location, or consequence.

## Structure the argument straight

### 10. Lead with the point in informational writing

- When the text informs — announcements, emails, reports, documentation, status updates — put the decision, change, or required action in the first sentence, and the reasons and background after it. Readers of informational text scan for what changed and what to do; making them read the build-up first is author-centric ordering.
-「鑑於近期內部作業流程有所調整，經多方評估與審慎考量後，本公司決定自下月一日起，將週會調整至週三下午辦理」buries the only fact the reader needs. Write「下個月起，週會改到週三下午開（原本是週一上午）」, or in a formal register,「本年度健康檢查 9 月 1 日至 15 日開放報名，名額增至三百名」with the reasons following. Leading with the point changes the order, not the register.
- Headings state content, not category.「5/20 凌晨 2–4 點系統暫停服務」tells the reader what is happening;「系統維護公告」only names a drawer to look in. A heading should answer, not tease.
- Voiced writing may earn a slower opening, but even there, never bury the fact the reader came for.

### 11. Write instructions as doable actions

- When the reader must do something, the sentence needs an actor, an action with its object, and a deadline.「相關資料應於期限內補齊，逾期恕不受理」names no one, no document, and no date; write「申請人請於 8 月 29 日前，將身分證影本上傳至報名系統」.
- Every obligation needs a subject.「本案應予處理」— by whom?
- Put the condition before the action（「如果 X，就做 Y」）so readers it excludes can stop reading early.
- When the text expects the reader to act, end with the next step.「若有疑問歡迎隨時聯繫」closes nothing; write「請回信告訴我選方案一還是方案二，我週五前要回覆廠商」.

### 12. Fixed-format genres keep their conventions

- Some document types carry a fixed format and conventional phrases: 台灣公文 with 主旨／說明 and 期望語（請查照、請核示）, contracts and legal clauses with their set formulas. In these genres the conventions are how a person writes. Stripping them to sound plainer makes the text less human, not more.
- Apply only the structural rules there — the conclusion goes into 主旨, details move down into 說明, actors and deadlines stay explicit — and leave the register, formulaic phrases, and required vocabulary alone.「主旨：請轉知所屬同仁報名本校 9 月 10 日及 17 日辦理之資訊安全教育訓練，請查照。」keeps every convention and still leads with the point.
- Vocabulary cleanup works the same way.「係」「惟」「俾」are padding in an email and normal register in a contract. Judge by the genre the reader expects, not by a universal word list.

### 13. Do not default to setup-and-reveal structures

- 先抑後揚 and 先破後立 start by building up a wrong view, then reveal the real point. Models fall into this pattern easily. When every section starts that way, readers learn to skip the first half of each paragraph.
- Most points are stronger stated directly: lead with the claim, then support it.
- Keep the structure only when the intended reader genuinely holds the misconception and correcting it is the point of the passage. Never invent a strawman just to have something to knock down. Even when justified, use it once in a piece, not as the skeleton of every section.

### 14. Make the point clear

- The reader should be able to tell what the writer thinks or wants them to understand.
- In grounded writing, state the judgment clearly and keep the framing consistent.
- In voiced writing, use opinion, tension, or a light edge when it helps the point.

### 15. Write body text as body text, not as slogans

- Body sentences need a subject, a verb, and a connection to the sentences before and after. A paragraph built from headline-style declarations, such as「效率，從此不同」「一個平台，解決所有問題」, reads like presentation titles pasted together, and the reader cannot find the line of reasoning.
- Headline diction belongs in headings. If a sentence would work unchanged as a slide title, it is probably not doing body-text work.
- State the claim as a full sentence with its reason or consequence attached, then continue the thread into the next sentence.

### 16. Break sterile symmetry

- Do not force every idea into neat triples.
- Vary paragraph length, and let sentence length change with the point.
- When every paragraph follows the same arc, break the arc.

## Control rhythm and tone

### 17. Vary rhythm on purpose

- Mix short sentences with longer ones.
- Avoid paragraphs where every sentence has the same shape.
- Let emphasis come from contrast, not from constant intensity.

### 18. Choose stronger verbs before adding adjectives

- Fix weak verb choice first.
- Prefer "cut", "argue", "miss", "ship", "delay", "expose", or "earn" over soft general verbs.
- Use adjectives only when they add meaning, not sheen.

### 19. Keep emotional texture controlled

- Human writing is not emotionally flat, but it also does not overperform.
- Add feeling through timing, specificity, and point of view.
- Avoid melodrama unless the task genuinely calls for it.

### 20. Keep it restrained

- The best human-like line is often simpler than the first draft.
- Do not show off range when a plain sentence will land better.
- Leave room for the reader to trust the voice.

### 21. Match social context

- Business writing earns trust by stating facts and next steps plainly, without template phrases.
- Public-facing copy should read as if someone chose each word for this product and this reader.
- In commentary, take a position and give its reason. A survey of safe opinions reads as filler.
- Chinese and English should each sound native to their own rhetorical habits.

## Punctuation

### 22. Treat semicolons as an exception

- In ordinary Chinese prose, do not use semicolons by default.
- During the final pass, replace each semicolon with a full stop, comma, colon, or a clearer sentence boundary whenever possible.
- Retain one only for formal quotations, required syntax, or a genuinely complex list where other punctuation would be less clear.
