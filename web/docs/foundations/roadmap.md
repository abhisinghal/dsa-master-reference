# Zero-to-Hero Roadmap


&lt;RoadmapChecklist /&gt;

&lt;StorageManager /&gt;

*A concrete, day-by-day plan a working engineer can actually follow. The book will not teach you if you read it front-to-back like a novel — patterns stick only through **spaced practice** on canonical problems. This chapter tells you exactly what to do on Monday morning.*

## Pre-flight quiz — are you ready for patterns?

Do NOT start Part II until you can answer these ten in under 30 seconds each without looking anything up. If you miss more than two, go finish [Part I](/foundations/java-primer) first.

1. What is the time complexity of `list.contains(x)` when `list` is an `ArrayList<Integer>` of size n? *(O(n) — it's a linear scan.)*
2. What is the amortized cost of `HashMap.put`? What's the worst case? *(O(1) amortized; O(n) worst if every key collides.)*
3. In `ArrayDeque`, which end is `push`/`pop`? Which end is `offer`/`poll`? *(`push`/`pop` = head, LIFO. `offer`/`poll` = tail-in, head-out, FIFO.)*
4. What's `Integer.MIN_VALUE * -1` in Java? *(Still `Integer.MIN_VALUE` — overflow wraps.)*
5. Given `n = 10⁵`, which complexities fit under 1 second? *(O(n), O(n log n), O(n √n). O(n²) is borderline; O(n³) fails.)*
6. What does `(lo + hi) / 2` fail on, and what's the fix? *(Overflow when `lo + hi > Integer.MAX_VALUE`. Use `lo + (hi - lo) / 2`.)*
7. In `TreeMap<Integer,V>`, what does `floorKey(x)` return? *(The greatest key ≤ x, or `null` if none exists.)*
8. What's the difference between `String.equals` and `==`? *(`equals` compares content; `==` compares references. Interned strings can accidentally pass `==`.)*
9. What's the space complexity of a recursive function that recurses `n` times without tail-call optimization? *(O(n) — Java doesn't do TCO; every frame stays on the stack.)*
10. Why is `ArrayDeque` preferred over `Stack` in modern Java? *(`Stack` extends `Vector` which is synchronized; `ArrayDeque` is faster and idiomatic.)*

<Callout kind="key" title="Score interpretation">

9-10: skip Part I, start Part II. 6-8: skim Part I, focus on gaps. ≤ 5: read Part I fully before Part II.

</Callout>

## The three tracks — pick one

Your track depends on your **calendar constraint**, not your skill level. All three land at the same competence — they just spread it differently.

| Track | Weeks | Weekly commitment | For whom |
|---|---|---|---|
| **Sprint** | 4 | 15–20 hrs | Interview in a month; strong Java baseline |
| **Standard** | 8 | 8–10 hrs | Interview in ~two months; want depth without cramming |
| **Marathon** | 12 | 5–7 hrs | Long-horizon prep; also learning fundamentals |

Below I lay out the **Standard 8-week plan** as the default. Sprint compresses each pair of weeks into one; Marathon expands each week into 1.5.

## The weekly cadence — do the same shape every week

Every week (regardless of track), your five practice sessions look like this:

| Session | Duration | What you do |
|---|---|---|
| **Study (Mon)** | 60 min | Read one pattern chapter's story + templates + one canonical problem. **No coding yet.** |
| **Canonical (Tue/Wed)** | 45 min × 2 | Code the week's 2 canonical problems from scratch on a blank editor. Time yourself. |
| **Variations (Thu)** | 45 min | Solve 2 variations of the week's pattern — proves you learned the *idea*, not the specific solution. |
| **Weakness (Fri)** | 60 min | Pick any problem you failed earlier and re-solve it *without looking*. This is where retention actually happens. |
| **Mock (Sat)** | 60 min | Full mock — think aloud, clarify, brute force → optimize → code → verify. Grade yourself with the [interview playbook](/foundations/playbook). |

Sundays are for rest. Retention needs sleep, not extra grinding.

<Callout kind="key" title="The 30% rule">

At least 30% of your weekly hours must go to **problems you've already solved once**. Fresh problems feel productive; **re-solving is where mastery is built**. If you skip re-solving, you'll forget every pattern within 3 weeks of the interview.

</Callout>

## The 8-week Standard Plan

### Week 1 — Foundations you can't skip

- **Read**: `06-java-ds.md` (Java primer). `07-java-gotchas.md`. `10-complexity.md`.
- **Do**: On paper, without an IDE, implement:
  - A stack using an array (grow-when-full)
  - A hash map with open addressing (linear probing)
  - Binary search — the `[lo, hi)` half-open version *only*
- **Canonical**: [Two Sum](https://leetcode.com/problems/two-sum/), [Valid Anagram](https://leetcode.com/problems/valid-anagram/) — with both brute-force **and** optimized versions and complexity for each.
- **Weekend mock**: Two Sum, aloud, timed. Grade yourself: did you propose brute force first? Did you state complexity before coding?

### Week 2 — Arrays, Hashing, Prefix Sum

- **Patterns**: Chapters 21 (Sliding Window — read the whole thing), 25 (Hashing), 24 (Prefix Sum).
- **Canonical**: [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/), [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/).
- **Variations**: [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/), [Group Anagrams](https://leetcode.com/problems/group-anagrams/).
- **Trap to internalize**: `HashMap.get(k)` returns `null` if absent — not `0`. Use `getOrDefault` or `merge`.

### Week 3 — Two Pointers, Fast/Slow, Binary Search

- **Patterns**: 22 (Two Pointers), 23 (Fast/Slow), 27 (Binary Search), 28 (BS on Answer).
- **Canonical**: [3Sum](https://leetcode.com/problems/3sum/), [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/).
- **Variations**: [Container With Most Water](https://leetcode.com/problems/container-with-most-water/), [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/), [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/).
- **Focus**: Binary Search's boundary conventions. Pick `[lo, hi)` half-open and stick with it. All the off-by-ones vanish.

### Week 4 — Stacks, Queues, Monotonic Stack, Sliding Window Max

- **Patterns**: 26 (Monotonic Stack), and revisit 21 for Sliding Window Maximum (monotonic deque).
- **Data structure**: 58 (Stacks & Queues).
- **Canonical**: [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/), [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/).
- **Variations**: [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/), [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) (both mono-stack and two-pointer solutions).
- **Interview mindset**: A stack solving a problem often means **"for each item, find the next greater/smaller."** Recognize this signal instantly.

### Week 5 — Heaps, Top-K, K-way Merge, Quickselect

- **Patterns**: 29 (Top-K/Heap), 30 (K-way Merge), 41 (Quickselect).
- **Data structure**: 62 (Heaps).
- **Canonical**: [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/), [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/).
- **Variations**: [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/), [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) (solve twice — once with heap, once with quickselect).
- **Focus**: When to reach for a heap vs. sort vs. quickselect — the "one-shot vs streaming" question.

### Week 6 — Trees, BSTs, Trie

- **Patterns**: 39 (Trie).
- **Data structures**: 60 (Trees), 64 (Trie).
- **Canonical**: [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/), [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/), [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/).
- **Variations**: [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/), [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/), [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/).
- **Interview mindset**: For trees, ask two questions at each node: *what do I need from my children?* (post-order return) and *what did my parent give me?* (pre-order context). Everything else is variations on those.

### Week 7 — Graphs, BFS/DFS, Topo Sort, Union-Find

- **Patterns**: 33 (Topological Sort), 34 (Union-Find), 66 (Graphs).
- **Canonical**: [Number of Islands](https://leetcode.com/problems/number-of-islands/), [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/), [Number of Provinces](https://leetcode.com/problems/number-of-provinces/).
- **Variations**: [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/), [Network Delay Time](https://leetcode.com/problems/network-delay-time/) (Dijkstra), [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) (MST).
- **Focus**: Choose your representation before you write a line. Adjacency list for sparse graphs, adjacency matrix only when V ≤ 500 and dense.

### Week 8 — DP, Backtracking, Design

- **Patterns**: 36 (Backtracking), 38 (Dynamic Programming), 44 (Design).
- **Canonical**: [House Robber](https://leetcode.com/problems/house-robber/), [Coin Change](https://leetcode.com/problems/coin-change/), [LRU Cache](https://leetcode.com/problems/lru-cache/), [Subsets](https://leetcode.com/problems/subsets/).
- **Variations**: [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/), [Edit Distance](https://leetcode.com/problems/edit-distance/), [N-Queens](https://leetcode.com/problems/n-queens/), [Word Search II](https://leetcode.com/problems/word-search-ii/) (Trie + backtracking).
- **Focus**: DP state design. If you can't name what a `dp[i]` cell *means* in one sentence, you can't code it. Spend as much time on the definition as on the transition.

### Weeks 9–10 (Sprint = W3-4; Marathon = spread across weeks 9-14)

**Retention consolidation.** No new patterns. Re-solve everything.

- **Monday**: Re-solve one problem from every pattern you learned (that's 21 problems in ~5 hrs — you'll be fast now).
- **Tuesday–Thursday**: One mock interview per day, unseen problems from LeetCode top-100.
- **Friday**: Grade all three mocks against the [interview playbook rubric](/foundations/playbook). Fix your weakest phase.

### Weeks 11–12 (final push, or first two weeks of Marathon closing)

**System design overlay + hard problems.**

- **System design**: 1 hour daily. Not covered here — see Alex Xu / DDIA — but the DSA patterns you learned show up (LRU cache, consistent hashing, rate limiter).
- **Hard problems**: [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/), [Serialize/Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/), [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/), [Word Break II](https://leetcode.com/problems/word-break-ii/), [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/), [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/), [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/).
- **Interview eve**: Only read Part II (patterns) and Part IV (cheat sheets). No new problems in the final 48 hours.

## What "you're ready" looks like

Sign one is easy: **you recognize the pattern in under 30 seconds.** But that's not sufficient. All three of these must be true:

1. **Recognition** — You read a problem and, within 30 seconds, you can name the pattern and often the exact template you'll use.
2. **Communication** — You can walk through your solution aloud without freezing, and you naturally propose brute-force before optimized. You know the complexity of every step *before* you write it.
3. **Recovery** — When your first idea doesn't work, you don't panic. You state what changed, propose an alternative, and move on. This is the difference between senior and mid-level.

If any of the three is missing, keep drilling. The book has enough material for another full pass.

<Callout kind="pat" title="Anti-pattern to avoid">

Grinding 500 LeetCode problems without a plan. Volume without spacing doesn't build recognition. **60 canonical problems drilled 3× each** beats 500 problems solved once. That's the entire premise of this book.

</Callout>

## Signs you're ready for **staff-level** (not just senior)

Passing a senior interview requires the three above. Staff adds three more:

4. **Decomposition** — You can turn a fuzzy real-world problem ("build me a rate limiter") into concrete data-structure choices with tradeoffs you can defend.
5. **Approximation** — You know when the "optimal" answer isn't worth it. Bloom filter instead of hash set (memory), quickselect instead of sort (need only k-th), sampling instead of full scan.
6. **Systems eye** — You spot when a DSA problem is really a systems problem. "Design a top-K feed" isn't `PriorityQueue`; it's count-min sketch + heavy hitters + heap merge — and you'd never fit that on a whiteboard, so you narrate the tradeoff.

If you hit staff signal in the first 20 minutes of an interview, expect harder problems. The book helps here but real staff interviews test judgment as much as code.

## Common mistakes on this roadmap

- **"I'll skip the pre-flight quiz."** Do the quiz. If you can't answer autoboxing / overflow / `ArrayDeque`, you'll waste hours debugging Java specifics that have nothing to do with the algorithm. The quiz takes 5 minutes.
- **"I'll do 10 problems this weekend and catch up."** Retention is a function of *spacing*, not *volume*. Ten problems in a weekend are forgotten by Wednesday. Two problems per day for five days aren't.
- **"I'll skip the mocks — I'll do them when I feel ready."** You'll never feel ready. The whole point of the mock is to expose what you don't yet have. Do them from Week 1.
- **"I'll just read the book."** Reading builds recognition; **only writing code builds recall**. The plan asks for 2 canonical + 2 variations + 1 re-solve per week for a reason.
- **"I'll skip re-solving problems I already got right."** This is *the* single biggest mistake. See "30% rule" above. Retention decays exponentially without re-exposure.

## What to do when you're stuck

Every serious engineer gets stuck. Here's the escalation order — do NOT skip steps.

1. **Re-read the problem statement.** Half of stuck-ness is misread constraints (n ≤ 10⁵ vs 10⁷ changes everything).
2. **State an example.** Pick the smallest input the problem allows. Trace what the answer should be by hand.
3. **State the brute force.** Even if it's O(n³) — say it out loud. This unlocks the "optimize what?" question.
4. **Look at what the input is *shaped* like.** Sorted? → binary search / two pointers. Overlapping ranges? → merge intervals. Prefix / suffix? → prefix sum. Contiguous? → sliding window.
5. **Read only the pattern's Recognize-by callout** in this book — not the code. If it clicks, close the book and code it.
6. **Look at the code template** — but *not* the specific problem's solution.
7. **Look at the solution.** Now: close everything, re-solve from a blank editor 24 hours later. If you can't, you didn't learn — you copied.

Discipline in step 7 is the single biggest predictor of interview success.