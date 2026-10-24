---
title: Mixed recognition drill
description: Problems from across all 21 patterns, order randomized, tags hidden. The mastery-level test.
---

# Mixed recognition drill

A single-pattern [recognition drill](/recognize) tells you whether you can spot that pattern inside its own chapter's problem set. A mixed drill tells you something harder: whether you can spot a pattern **when you don't know which chapter the problem came from**. That's the actual interview condition.

Each round pulls 10 problems from the full 21-pattern bank, randomizes the order, and hides the tags. If you have been working from one chapter at a time, this is where you discover whether the recognition has transferred.

<RecognitionDrill pattern="mixed" :count="10" />

## When to come here

- **After finishing a chapter** — to check whether the pattern survived contact with the other 20.
- **Before an interview** — spending 20 minutes on this surfaces exactly which recognitions are still shaky, which chapters to re-skim, which traps you're prone to.
- **During a plateau** — if cold-solving feels slow but you can read any solution and understand it instantly, this is probably why. You can recognize patterns when you're told them; you can't yet recognize them unprompted.

## Why mixed is harder than it looks

Problems from two different patterns often share surface features. "Smallest subarray with sum ≥ S" (sliding-window) and "Minimum capacity to ship in D days" (binary-search on the answer) both start with "find the smallest..." Reading top-down, both look like optimization problems; the recognition cue is deeper — one has a monotone validity predicate over the answer space, the other has a sliding-window invariant that can be maintained incrementally. If you miss the cue, you'll pick the wrong tool and spend 20 minutes going nowhere.

The distractors in this drill are the specific patterns the problem can be mistaken for. If you keep missing in the same direction (always picking X when the answer is Y), that's your highest-leverage study target.

## Caveats

- A high mixed score is **necessary but not sufficient** for interview readiness. Implementation fluency and debugging under pressure are separate axes; mock interviews are where you measure them.
- The problem bank grows as chapter upgrades land — your score shouldn't be compared across weeks until the bank stabilizes. Compare your score to **yourself from last week** on the same bank size.
- Problems rephrase common statements; a question copied verbatim from LeetCode would train memory, not recognition.
