# Empty-context review

A reader who took no part in the writing reads the finished document and reports what cannot be understood without the conversation that produced it.

## When to run it

Run it for a specification, article or report that is delivered as a document of its own, after the [final checklist](./final-checklist.md) passes and before delivery. A specification that another agent will implement from is the first case to cover.

Do not run it for a conversational reply, a short message, code, or a small edit to an existing document.

When the environment cannot start a reader that is isolated from this conversation, do not run it. Check the two context items in the final checklist again yourself, and say at delivery that no independent reader checked the document.

## The reader

- Use a subagent or a separate session that did not take part in writing the document and has not seen an earlier version of it or an earlier review of it.
- Start it without this conversation: turn off any option that passes the conversation or session history to it.
- The reader does not modify any file.

## What the reader is given

Give the reader only:

- who the target readers are and what they read the document for
- the complete text of the document
- the material the target readers can actually obtain with it, such as cited documents and attachments

Do not give the reader the conversation, the writing plan, the reasons for revisions, the reading you intend, or the answers from an earlier review. Do not ask for knowledge beyond what the target readers are assumed to have.

## What the reader returns

1. The main point of the document in the reader's own words. For a specification, also the required behavior and the acceptance criteria. For a report, also the main conclusions and what each one rests on.
2. An itemized list of the places it cannot understand, the places that can be read in more than one way, and the information that is missing. Each item gives the paragraph, page or line, and the smallest fix.

The reader does not fill a gap by guessing. When it finds no problem, it says so.

## After the reader returns

- Compare the reader's restatement with what the document is meant to say. A difference is a finding even when the reader listed no problem.
- Check each item against the document and fix the ones that depend on context the target readers do not have. Prefer a clearer structure, a clearer name, or deleting unrelated content. Add explanation only when those do not solve it.
- After fixing, run the review again with a new reader. Do not reuse the previous reader and do not pass it the previous report.
- At delivery, state what the reader confirmed, what gaps remain, and what could not be checked.

This review covers whether the document can be understood. It does not check facts, test results or correctness.
