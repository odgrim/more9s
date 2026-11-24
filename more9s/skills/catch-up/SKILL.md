---
name: catch-up
description: "Tell the human what changed since their last message and list everything waiting on them, each item answerable from the reply alone. Use for /catch-up."
disable-model-invocation: true
---

# Catch Up

Assume the human remembers their last message and nothing after it. A notification or a subagent's result isn't their message.

This turn only reads. Check the current state of each PR, CI run, and background task the session touched, and the draft report if there is one. Change no code, start nothing, and post nothing.

Write it the way [wat](../wat/SKILL.md) asks: plain words, and no paths, hashes, or counts the human doesn't need in order to act.

1. Open with one sentence that names what's waiting on the human, or says nothing is.
2. Say what happened, in under a hundred words. Give one line per thing the human asked for: what came of it, and whether it's done, still running, failed, or not checked. Name any problem found and fixed on the way. Leave out work that changed nothing for them.
3. List what's waiting on them. An item is something only the human can do: an ask-first action, a decision the reviewer has to rule on, a choice no experiment can settle, access you don't have. For each one give:
   - the question, as a choice they can answer in a word
   - your recommendation
   - what it changes for the user of the work
   - the evidence behind the recommendation
   - the risk, even when it's low
   - the command that performs it, if it's an action
4. Say in one line what's left that you can do without them.

- Include every waiting item, however many there are. Don't replace the list with a count or a link.
- Work you can still do yourself isn't an item. Never make one up to fill the list.
- Never call something done that's still waiting on the human.
- If nothing happened and nothing is waiting, say so and stop.

## Check

- Could the human answer every item from this reply, without opening anything?
