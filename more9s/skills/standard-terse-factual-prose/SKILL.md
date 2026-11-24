---
name: standard-terse-factual-prose
description: "Apply when you're writing anything a human reads: commit messages, PR descriptions, docs, replies. Write so it's understood on the first read, in the fewest words that allow it, and state facts."
disable-model-invocation: true
---

# Terse, Factual Prose

The reader has less context than you and less time.

- Lead with what changes for the reader.
- Give the claim and its evidence. Drop adjectives and filler.
- Label a claim without evidence once: inferred or guess. Don't state it as fact, and don't spread the doubt through the sentence with "might", "should", or "probably".
- If a change makes a comment, doc, or agent instruction untrue, fix or delete it in the same change.
- No em dashes. Use a period, comma, or colon, and vary which. The more9s hook flags them in prose files and code comments. Nothing but this line checks replies, commit messages, and edits a script makes.

## Check

- Delete each sentence in turn. Is anything lost?
