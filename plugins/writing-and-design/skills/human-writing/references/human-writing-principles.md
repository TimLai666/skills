# Human writing principles

Use these rules to make prose feel written by a person. They follow the order in which you make decisions: what to say, who will read it, how to structure it, how it should sound, and finally punctuation.

## Make it concrete

### 1. Prefer specificity over abstraction

- Replace broad claims with concrete points.
- Use nouns and verbs that name the thing instead of circling around it.
- Cut lines that only announce importance without adding information.

### 2. Do not use abstract adjectives and adverbs

Abstract modifiers can feel descriptive to the writer, but they give the reader no picture of what happened or what makes something good. The reader has to guess. Watch for four forms:

- **AI-invented shorthand that no real person says**, such as「不繞」「最穩」「一直在撐」. These sound punchy to the model but are not how people talk, and the reader cannot even tell what quality is being claimed. This form is the strongest AI tell of the four.
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

### 10. Do not default to setup-and-reveal structures

- 先抑後揚 and 先破後立 start by building up a wrong view, then reveal the real point. Models fall into this pattern easily. When every section starts that way, readers learn to skip the first half of each paragraph.
- Most points are stronger stated directly: lead with the claim, then support it.
- Keep the structure only when the intended reader genuinely holds the misconception and correcting it is the point of the passage. Never invent a strawman just to have something to knock down. Even when justified, use it once in a piece, not as the skeleton of every section.

### 11. Make the point clear

- The reader should be able to tell what the writer thinks or wants them to understand.
- In restrained writing, state the judgment clearly and keep the framing consistent.
- In voiced writing, use opinion, tension, or a light edge when it helps the point.

### 12. Write body text as body text, not as slogans

- Body sentences need a subject, a verb, and a connection to the sentences before and after. A paragraph built from headline-style declarations, such as「效率，從此不同」「一個平台，解決所有問題」, reads like presentation titles pasted together, and the reader cannot find the line of reasoning.
- Headline diction belongs in headings. If a sentence would work unchanged as a slide title, it is probably not doing body-text work.
- State the claim as a full sentence with its reason or consequence attached, then continue the thread into the next sentence.

### 13. Break sterile symmetry

- Do not force every idea into neat triples.
- Do not make every paragraph the same length.
- Let sentence length change with the point. Do not arrange every paragraph into the same pattern.

## Control rhythm and tone

### 14. Vary rhythm on purpose

- Mix short sentences with longer ones.
- Avoid paragraphs where every sentence has the same shape.
- Let emphasis come from contrast, not from constant intensity.

### 15. Choose stronger verbs before adding adjectives

- Fix weak verb choice first.
- Prefer "cut", "argue", "miss", "ship", "delay", "expose", or "earn" over soft general verbs.
- Use adjectives only when they add meaning, not sheen.

### 16. Keep emotional texture controlled

- Human writing is not emotionally flat, but it also does not overperform.
- Add feeling through timing, specificity, and point of view.
- Avoid melodrama unless the task genuinely calls for it.

### 17. Keep it restrained

- The best human-like line is often simpler than the first draft.
- Do not show off range when a plain sentence will land better.
- Leave room for the reader to trust the voice.

### 18. Match social context

- Business writing should feel reliable, not robotic.
- Public-facing copy should feel intentional, not inflated.
- Commentary should sound considered, not generic.
- Chinese and English should each sound native to their own rhetorical habits.

## Punctuation

### 19. Treat semicolons as an exception

- In ordinary Chinese prose, do not use semicolons by default.
- During the final pass, replace each semicolon with a full stop, comma, colon, or a clearer sentence boundary whenever possible.
- Retain one only for formal quotations, required syntax, or a genuinely complex list where other punctuation would be less clear.
