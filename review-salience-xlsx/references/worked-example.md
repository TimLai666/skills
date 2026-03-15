# Worked Example — Safety Eyewear (923 reviews, 30 attributes)

Use this file to calibrate scoring intuition. The scores here are from a
semantic reading pass (Claude as scorer) on Amazon safety-eyewear reviews
spanning English, French, Spanish, Italian, and German.

---

## Corpus

8 products, 923 valid reviews (body length > 15 chars), no language filtering.

| Product | Count | Key use context |
|---------|-------|----------------|
| B00080FKIO | 115 | Shooting, airsoft, military (EN/FR/ES/IT/DE) |
| B007W7X1UK | 46 | Machine shop, OR, COVID PPE |
| B00X69LVKK | 37 | Military, tactical, everyday |
| B016KZ2APQ | 249 | Pickleball, factory, healthcare |
| B07GB8Y11G | 194 | Outdoor, sport, pickleball |
| B08GKPC599 | 208 | Healthcare, lab, pickleball |
| B0B15BXZ94 | 42 | Pickleball (sport-specific) |
| B0BQHBHNQF | 32 | Welding class, dental lab, pickleball |

---

## Scoring calibration examples

### Score = 0 (not mentioned)

> "Great for every day wear, been wearing these everyday for at least a year and I'm on my second pair"

- `s07` (impact protection) = 0 — no mention of ballistic or impact testing
- `s12` (ear-muff compatibility) = 0 — no hearing protection context
- `s13` (community identity) = 0 — no professional/military language

### Score = 3–4 (indirect or ambiguous)

> "Fogs up playing airsoft"

- `s02` (anti-fog) = 6 — clear complaint, single-sentence but unambiguous
- `s25` (scene adaptability) = 4 — airsoft is implied context, not elaborated

> "Die Brille passt, sitz bequem, der Preis ist ok."  
> (DE: The glasses fit, sit comfortably, the price is ok.)

- `s23` (all-day comfort) = 5 — "bequem" (comfortable) is clear
- `s28` (price-value) = 4 — "Preis ist ok" is neutral, not praising or criticising

### Score = 5–6 (clearly mentioned)

> "I work in an operating room and i am scrubbed in for 6+ hours a day. These glasses are comfy and looked and functioned great for the first 3 weeks. However i bought two pairs and the protective coating started to wear off of them after only 3 weeks of use. Some of the coating flaked off into my eye."

- `s05` (lens clarity durability) = 7 — coating failure is the central complaint, described vividly
- `s17` (team/workplace use) = 5 — bought two pairs, workplace context
- `s23` (all-day comfort) = 6 — "6+ hours a day" is explicit
- `s25` (scene adaptability) = 5 — OR context stated

### Score = 7 (strongly emphasised)

> "Buyer beware! You will only receive 1 color of lense. I give 3 stars and not 5 because of the fact that the product is deceptively advertised to make you think you are getting 3 sets."

- `s20` (ad honesty) = 7 — "deceptively advertised" is the entire purpose of the review

> "LITERALLY SCRATCHED WHEN I RECEIVED THEM!! This was probably my worst purchase ever."

- `s08` (scratch resistance) = 7 — capitalised emphasis, strongest possible negative signal

---

## Score distribution from this corpus

| Score | Count | % of all cells |
|-------|-------|---------------|
| 0 | 25,287 | 91.3% |
| 1 | 0 | 0.0% |
| 2 | 29 | 0.1% |
| 3 | 41 | 0.1% |
| 4 | 340 | 1.2% |
| 5 | 1,668 | 6.0% |
| 6 | 264 | 1.0% |
| 7 | 61 | 0.2% |

**Key observation:** 91 % of cells are 0. Most reviews mention only 2–5
attributes. Scores of 1 are nearly absent because reviews rarely make partial
references — they either say something clearly (5+) or don't say it (0).
Score 4 appears for ambiguous statements like "price is ok" or implied context.

---

## Average attributes mentioned per review

| Product | Mean non-zero attrs/review |
|---------|--------------------------|
| B0B15BXZ94 (pickleball-specific) | 4.4 |
| B00080FKIO (Wiley X, multi-context) | 3.5 |
| B0BQHBHNQF (lab/dental) | 3.3 |
| B007W7X1UK (Bollé) | 2.9 |
| B08GKPC599 (NoCry healthcare) | 2.7 |
| B07GB8Y11G (NoCry general) | 2.2 |
| B016KZ2APQ (3M) | 1.9 |

Short, complaint-focused reviews (3M corpus) produce lower attribute density
than detailed sport-use reviews (Impactable pickleball corpus).

---

## Cross-language scoring notes

- **Italian** "poco resistenti ai graffi" → `s08` = 6 (scratch resistance, clearly negative)
- **Spanish** "no se empañan" → `s02` = 5 (no fogging, clearly positive)
- **French** "ne bue pas au début (une semaine) et après rien à faire, on y voit plus rien" → `s02` = 7 (fog resistance collapses after one week — vivid, emphasis-worthy)
- **German** "beschlägt kaum" → `s02` = 4 (barely fogs — mild positive, not strong enough for 5)

Treat all languages identically. Do not assign lower confidence to non-English
reviews when scoring.
