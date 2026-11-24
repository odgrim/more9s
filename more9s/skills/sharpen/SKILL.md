---
name: sharpen
description: "Rewrites a prompt so it asks for what an expert would do, without making the task bigger. Use for /sharpen."
argument-hint: "[the prompt to sharpen]"
disable-model-invocation: true
---

# Sharpen

The human wants a deeper version of their task, not a larger one. With no argument, the prompt is their last request.

Answer these four first, briefly:

1. What would someone expert in this field do here that the prompt doesn't ask for?
2. What primary material would they start from, where the prompt points at a summary of it?
3. Which methods and tools would they use, by name?
4. What would show the result is right, other than the human or the agent saying so?

Then rewrite the prompt to ask for that. The rewritten prompt:

- keeps the original goal and adds no new deliverable
- names the material, the methods, and the check from the answers above
- asks for any choice an experiment can settle to be settled by a prototype, with a recommendation from what was observed
- leaves a choice of product or preference to the human, and says which ones those are

Give the four answers and the rewritten prompt, and stop. Don't start the task.
