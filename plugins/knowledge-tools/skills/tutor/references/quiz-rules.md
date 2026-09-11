# Quiz Design Rules

## Zero-Hint Policy (CRITICAL)

Every question must be answerable ONLY by someone who actually knows the material.

1. **Option descriptions**: NEVER reveal correctness
   - BAD: `label: "stderr"`, `description: "Error output stream used by Cloud Run for error classification"`
   - GOOD: `label: "stderr"`, `description: "Standard error stream"`

2. **No "(Recommended)" tag** on any option

3. **Randomize** correct answer position — never always first or last

4. **Question phrasing**: Ask about behavior/purpose/output, don't hint at the answer
   - BAD: "Which error stream does error() use?"
   - GOOD: "Where does error() method output go?"

5. **Plausible distractors**: Wrong options must be real concepts from the domain, representing common misconceptions

## Question Types

1. **Factual recall**: "What HTTP status code is returned when...?"
2. **Conceptual understanding**: "Why does the system use X pattern?"
3. **Behavioral prediction**: "What happens when X fails?"
4. **Comparison/distinction**: "What is the difference between X and Y?"
5. **Debugging scenario**: "Given this error, what is the most likely cause?"

## Difficulty Balancing

- Diagnostic: easy 40%, medium 40%, hard 20%
- Weak-area drill: medium 30%, hard 70%
- Review: all levels evenly

## Drilling Unresolved Concepts

When targeting 🔴 concepts from concept files:
- Do NOT repeat the exact same question — rephrase in a new context
- Test the same underlying knowledge from a different angle
- E.g., if user confused "400 vs 422", ask a scenario question where they must choose the correct status code for a new situation

## Quiz Presentation

- Four questions per round, four options each, single-select.
- Use an available question tool only when it supports neutral quiz choices and its usage rules permit quizzes. Follow its actual limits; if needed, split the four-question round across calls.
- Do not use a tool that requires recommending or preselecting an answer. If no suitable tool is available, present the four questions in ordinary text with A–D options and wait for the user's answers.
- Keep labels and descriptions neutral. Do not reveal answers through selection defaults, descriptions or answer-shaped response examples.
- Short headers such as "Q1. Topic" are useful when supported; follow the actual tool's length limit.

After the user answers, return to the main skill's Grade & Explain and Update
Files phases. Those phases define the concept and dashboard update procedure;
use the language selected at the start of the session.
