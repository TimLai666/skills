# Human writing principles

Use these rules to make prose feel written, not generated. They are grouped in the order the decisions come up while writing: what to say, who is reading, how to structure it, how it sounds, and finally punctuation.

## Make it concrete

### 1. Prefer specificity over abstraction

- Replace broad claims with concrete points.
- Use nouns and verbs that name the thing instead of circling around it.
- Cut lines that only announce importance without adding information.

### 2. Do not use abstract adjectives and adverbs

Abstract modifiers only feel descriptive to the writer. The reader gets no picture, no idea what happened or how good "good" is, and can only fill the blank with their own guess. Watch for four forms:

- **AI-invented shorthand that no real person says**, such as「不繞」「最穩」「一直在撐」. These sound punchy to the model but are not how people talk, and the reader cannot even tell what quality is being claimed. This form is the strongest AI tell of the four.
- **Impression summaries**, such as「很好」「很棒」「非常愉快」. They report the writer's feeling about the thing instead of the thing, so the picture in the writer's head never reaches the reader.
- **Ambiguous abstractions**, such as「彈性」「完善」or "robust", "seamless". Every reader decodes them differently, so the writer thinks the point is made while each reader understands something else.
- **Ornate stacked modifiers**, such as「深刻地」「優雅地」「淋漓盡致」. They perform style without adding content. If deleting the word loses no information, it was empty.

In every case, rewrite the sentence to show the thing itself, in words a real person would say: what happened, how much, compared to what, what it looks like in use, or what it lets the reader do. If nothing concrete is known, delete the modifier and let the plain statement stand. Never invent a number or detail just to replace a banned word.

The test for "concrete" is whether the reader can replay the scene or operation in their head, not whether the sentence contains a number.「結帳從五步縮成兩步」still fails: the reader does not know what the five steps were, so the number is just another summary. Concrete means the reader could walk through it:「以前在購物網站下單，每次都要重打一遍地址。改版後登入會員，結帳頁直接帶出上次的地址，按送出就完成了」.

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

### 6. Avoid unexplained niche vocabulary

- Prefer common words over niche terms, jargon, project shorthand, and author-created labels.
- If a term such as「剪刀差」is necessary, explain it in plain language at first use. Otherwise, directly describe the difference or consequence it refers to.
- Do not treat a familiar term within one field as familiar to every reader.

### 7. Remove unexplained figurative language

- Keep a metaphor only when the reader can tell what it refers to and what it means in the situation.
- Replace vague images such as「漏過去」with the concrete missing data, action, location, or consequence.

## Structure the argument straight

### 8. Do not default to setup-and-reveal structures

- 先抑後揚 and 先破後立 — first putting something down or building up a wrong view, then revealing the real point — is a default rhetorical reflex of models, not of people. When every section opens by knocking something over, the whole text runs on one visible formula, and the reader learns to skip the first half of every paragraph.
- Most points are stronger stated directly: lead with the claim, then support it.
- Keep the structure only when the intended reader genuinely holds the misconception and correcting it is the point of the passage. Never invent a strawman just to have something to knock down. Even when justified, use it once in a piece, not as the skeleton of every section.

### 9. Sound like someone is making a point

- Give the prose a center of gravity.
- In restrained writing, this means clear judgment and stable framing.
- In voiced writing, this can include opinion, tension, or a light edge.

## Control rhythm and tone

### 10. Vary rhythm on purpose

- Mix short sentences with longer ones.
- Avoid paragraphs where every sentence has the same shape.
- Let emphasis come from contrast, not from constant intensity.

### 11. Break sterile symmetry

- Do not force every idea into neat triples.
- Do not make every paragraph the same length.
- Allow one sharp sentence, one longer turn, one quiet sentence when useful.

### 12. Write body text as body text, not as slogans

- Body sentences need a subject, a verb, and a connection to the sentences before and after. A paragraph built from headline-style declarations, such as「效率，從此不同」「一個平台，解決所有問題」, reads like presentation titles pasted together, and the reader cannot find the line of reasoning.
- Headline diction belongs in headings. If a sentence would work unchanged as a slide title, it is probably not doing body-text work.
- State the claim as a full sentence with its reason or consequence attached, then continue the thread into the next sentence.

### 13. Choose stronger verbs before adding adjectives

- Fix weak verb choice first.
- Prefer "cut", "argue", "miss", "ship", "delay", "expose", or "earn" over soft general verbs.
- Use adjectives only when they add meaning, not sheen.

### 14. Keep emotional texture controlled

- Human writing is not emotionally flat, but it also does not overperform.
- Add feeling through timing, specificity, and point of view.
- Avoid melodrama unless the task genuinely calls for it.

### 15. Use restraint as a feature

- The best human-like line is often simpler than the first draft.
- Do not show off range when a plain sentence will land better.
- Leave room for the reader to trust the voice.

### 16. Match social context

- Business writing should feel reliable, not robotic.
- Public-facing copy should feel intentional, not inflated.
- Commentary should sound considered, not generic.
- Chinese and English should each sound native to their own rhetorical habits.

## Punctuation

### 17. Treat semicolons as an exception

- In ordinary Chinese prose, do not use semicolons by default.
- During the final pass, replace each semicolon with a full stop, comma, colon, or a clearer sentence boundary whenever possible.
- Retain one only for formal quotations, required syntax, or a genuinely complex list where other punctuation would be less clear.
