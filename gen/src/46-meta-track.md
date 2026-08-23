# Meta / Facebook Interview Kit

<PatternVideo pattern-name="Meta Interview Kit" duration="prep video coming soon" />

Meta's coding interviews at E4–E6 rely heavily on **Sliding Window**, **DFS/BFS on graphs**, **Trees**, and **DP** — with a strong preference for problems that test *invariant reasoning*, not memorized templates.

## What Meta actually asks (based on public reports)

| Level | Focus areas |
|---|---|
| **E4 (SDE II)** | Two-pointer, hashing, tree traversal, medium DP |
| **E5 (Senior)** | Interval merging, monotonic stack, graph shortest path, hard DP |
| **E6 (Staff+)** | Design + algorithm, system-scale trade-offs, hard interval / stream problems |

## Recommended problem sequence

Solve in this order — each builds on the previous.

### Week 1 — Foundations
1. [Two Sum](/problems/hashing-two-sum) — hashing baseline
2. [Longest Substring Without Repeating Characters](/problems/sliding-window-longest-substring) — sliding window seed
3. [Container With Most Water](/problems/container-with-most-water) — two pointers
4. [3Sum](/problems/3sum) — sort + 2p

### Week 2 — Trees + Graphs
5. [Number of Islands](/problems/number-of-islands) — DFS / UF
6. [Course Schedule](/problems/course-schedule) — topo sort
7. [Word Ladder](/problems/word-ladder) — BFS
8. [Alien Dictionary](/problems/alien-dictionary) — Meta favorite

### Week 3 — DP + Intervals
9. [House Robber](/problems/house-robber) — DP entry
10. [Merge Intervals](/problems/merge-intervals-classic) — Meta favorite
11. [Meeting Rooms II](/problems/meeting-rooms-ii) — sweep line
12. [Best Time to Buy and Sell Stock](/problems/best-time-to-buy-and-sell-stock) — greedy DP

### Week 4 — Harder
13. [Trapping Rain Water](/problems/trapping-rain-water) — 2p / stack
14. [Regular Expression Matching](/problems/regular-expression-matching) — DP
15. [Word Search II](/problems/word-search-ii) — trie + DFS
16. [Serialize and Deserialize Binary Tree](/patterns/dp) — tree

## What Meta interviewers care about (per public reports)

- **Clarify first.** Don't code until you've asked about input size, duplicates, null.
- **Talk through complexity BEFORE coding.** State target big-O and why.
- **Test the sample.** Trace input by hand at the end.
- **Handle edge cases proactively.** Empty, single element, all-same, adversarial.

<SocialProof />

<EmailCapture />

<Callout kind="pat" title="Data disclaimer">
Meta interview kits are curated from public interview reports and blog posts. This is not from Meta insider knowledge. Individual mileage varies.
</Callout>
