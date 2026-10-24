---
title: Prerequisite Map
description: A dependency graph of every chapter — see which topics you need to master first.
---

# Prerequisite Map

A chapter rarely stands alone. Dynamic programming is a wall if you have not internalised recursion and backtracking; graphs stop making sense without a mental model of adjacency and a working hashing habit; segment trees expect you to be fluent with both arrays and trees. The graph below shows those dependencies as a single picture, so you can plan a study path that always lands on ground you already stand on.

Each node is a chapter. An arrow from **A → B** means *A is a prerequisite for B* — not a hard gate, but a "if you are new to B and A looks unfamiliar, start there instead."

<PrerequisiteGraph />

## How to use this map

- **If you're starting fresh** — begin with the two foundation chapters (Complexity, Java Primer), then walk down tier by tier. The vertical ordering is the recommended first-pass path.
- **If you failed a specific chapter** — hover it. The highlighted ancestry is exactly the set of chapters whose absence most commonly causes the fail. Re-read any you're shaky on, then come back.
- **If you're preparing for a specific interview** — pick the four or five hardest chapters on the company's track (Meta / Google / Amazon), hover each, and union the highlighted sets. That union is your minimum study surface.

## The four kinds of nodes

| Kind | What it means | How to approach |
|---|---|---|
| **Foundation** | The cost model + the language primer | Not optional. Everything above these assumes you own them. |
| **Data Structure** | A container with a contract: operations and their complexities | Learn the operations and their invariants before any pattern that uses the structure. |
| **Pattern** | A reusable solution shape — "when I see X, I reach for Y" | Each pattern teaches you to *recognize* a problem class in under 30 seconds. |
| **Advanced** | DP and Design — synthesis chapters that lean on many others | Only attempt once the ancestry chain is comfortable. |

## Where this map does *not* capture dependency

The graph deliberately shows the **most load-bearing** prerequisites, not every tangential one. For instance:

- Sliding Window benefits from Hashing (frequency tables), but it does not *require* it — you can learn the pattern on numeric constraints first. The graph does not draw that edge.
- Union Find can be learned without Graphs (it starts as pure array manipulation), but every interview-grade use of it is on graph connectivity problems. The graph draws that edge because the practical dependency matters more than the theoretical minimum.

When in doubt about where to go next, follow the arrows and trust that the author who built the chapter above you probably assumed you'd read the one below first.
