<div class="cover">
<h1>DSA MASTER<br/>REFERENCE</h1>
<div class="sub">Patterns · Invariants · Problems</div>
<div class="rule"></div>
<div class="meta">
A high-density reference for senior &amp; staff engineers.<br/>
Pattern recognition · Optimal Java 17 · Correctness reasoning.
</div>
<div class="badge">Enhanced Edition · Java 17 · Revision-Optimized</div>
</div>

<div class="toc" markdown="1">

# How to Use This Book

This is a **recognition-first** reference, not a tutorial. It assumes fluency in Java and programming fundamentals. Every topic opens with a compact **concept model** (recognition signals → core idea → invariant → complexity), followed by a small set of **canonical problems** chosen because each teaches a *distinct* idea, variation, or trap.

**How the book is organized — and the order to learn it**

Think in two layers: **data structures are your vocabulary; patterns are the grammar.** You need the vocabulary before the grammar makes sense — but "vocabulary" means the *mechanics* of each structure (declare, insert, iterate, costs), which is **Part I's Java Data-Structures primer** and needs **zero** pattern knowledge. The chapters named *Arrays &amp; Hashing, Linked Lists, Trees…* in Part III are **not** "learn the structure" sections — they are **collections of pattern problems** grouped by the structure they run on. That single distinction fixes the reading order:

1. **Foundations first (Part I).** Read the Java DS primer for pure mechanics and do the *Easy* structure warm-ups on each container — no patterns required. Skim Complexity.
2. **Patterns next (Part II → the pattern chapters).** This is the real practice. For each pattern: read its card (recognition signals + code template), then work its canonical problems. When a pattern leans on a structure you're rusty on, jump back to that structure's primer section.
3. **Topic chapters as reference.** *Trees, Heaps, Graphs, Tries…* are where the depth lives; you reach them **through** the patterns, not before them.

<Callout kind="key" title="Recommended path:">

primer (mechanics) → patterns (practice) → topic chapters (depth). **Don't** read the topic problem-chapters cold before the patterns — that's exactly the confusion to avoid.

</Callout>

<Callout kind="pat" title="Start here:">

before your first problem, read **[The Interview Playbook](/foundations/playbook)** — the 6-phase loop (Clarify → Examples → Brute force → Optimize → Code → Verify) that scores you as *senior* — and pick a track in **[Study Plans &amp; Revision Cadence](/foundations/playbook#study-plans)**. Track what you've mastered in the **[Master Problem Index](/appendix/problem-index)**.

</Callout>

<Callout kind="note" title="Prerequisite chain">

a few patterns stack on earlier ones. Learn them in this dependency order: **recursion → backtracking → dynamic programming**; **arrays & hashing → prefix sum → sliding window**; **heaps → Dijkstra & K-way merge**; **stacks → monotonic stack**; **trees → tree-DP & tries**. If a pattern feels impossible, you're usually missing its prerequisite, not the pattern itself.

</Callout>

**Revision passes**

- **Revision pass** — read only the callout boxes: 🔑 Key Insight, 📐 Invariant, ⚠️ Trap, 🔗 Pattern Connection. Each problem is designed to be re-absorbed in under 90 seconds.
- **Interview eve** — read Part II (decision tree + patterns) and Part IV (cheat sheets) only.

**Colour &amp; icon legend** — the callout boxes are colour-coded so you can navigate by eye:

<Callout kind="key" title="Key Insight">

(blue) — the one idea that unlocks the problem.

</Callout>

<Callout kind="inv" title="Invariant">

(amber) — the property held true at every step; the backbone of correctness.

</Callout>

<Callout kind="trap" title="Common Trap">

(red) — the mistake that fails the interview.

</Callout>

<Callout kind="pat" title="Pattern Connection">

(green) — how this generalizes to the larger family.

</Callout>

<Callout kind="def" title="Definition / Key terms">

(teal) — jargon explained; reference material.

</Callout>

<Callout kind="note" title="Note / Trace it">

(grey) — worked walkthroughs and secondary notes. Every "Trace it" callout is paired with an **Execution Trace** — an interactive slider visualization (Play / Prev / Next / Reset + draggable scrubber) that steps through the algorithm frame-by-frame on the example, showing pointer positions, tracked variables, and per-step notes.

</Callout>

Difficulty on practice links is badged too: <span class="diff diff-e">Easy</span> · <span class="diff diff-m">Medium</span> · <span class="diff diff-h">Hard</span>. A thin teal rule under a heading (*"What &amp; why…"*) states that section's purpose in one line.

**Every problem is a self-contained unit** — Problem (statement + constraints + example) → approach → **code first**, then a *Trace it* walkthrough on that code → complexity → traps → variations — so you can drill any one in isolation.

**Code conventions** — modern **Java 17+**: `ArrayDeque` (never `Stack`), `getOrDefault`/`merge`/`computeIfAbsent`, `StringBuilder`, `var` where it aids clarity, `int[]{r,c}` for grid cells, `long` wherever sums can overflow, and half-open intervals `[lo, hi)` for binary search unless noted.

## Syllabus &amp; Chapters

*Every entry below is a link — click any line to jump straight to that section (works in the PDF and the HTML).*

<ol>
<li><a href="#the-interview-playbook">The Interview Playbook — how to drive the room</a></li>
<li><a href="#study-plans-revision-cadence">Study Plans &amp; Revision Cadence</a></li>
<li><a href="#zero-to-hero-roadmap">Zero-to-Hero Roadmap — day-by-day plan</a></li>
<li><a href="#glossary-words-we-use-everywhere">Glossary — Words We Use Everywhere</a></li>
<li class="part">Part I — Foundations</li>
<li><a href="#java-data-structures-a-visual-toolkit">Java Data Structures — A Visual Toolkit (the primer: pure mechanics)</a></li>
<li><a href="#java-dsa-gotchas">Java DSA Gotchas — 20 pitfalls that cost interviews</a></li>
<li><a href="#complexity-amortization-the-cost-model">Complexity, Amortization &amp; the Cost Model</a></li>
<li><a href="#data-structure-operation-costs">Data-Structure Operation Costs (with per-structure revision cards)</a></li>
<li><a href="#debugging-dsa-code">Debugging DSA Code — trace tables, adversarial tests, top-5 bugs</a></li>
<li class="part">Part II — The 21 Core Patterns (algorithmic techniques)</li>
<li><a href="#the-which-pattern-decision-tree">The "Which Pattern?" Decision Tree &amp; Recognition Framework</a></li>
<li><a href="#sliding-window">1. Sliding Window</a></li>
<li><a href="#two-pointers">2. Two Pointers</a></li>
<li><a href="#fast-slow-pointers-floyd">3. Fast / Slow Pointers (Floyd)</a></li>
<li><a href="#prefix-sum-difference-arrays">4. Prefix Sum &amp; Difference Arrays</a></li>
<li><a href="#hashing">5. Hashing (Two Sum, Group Anagrams, Longest Consecutive)</a></li>
<li><a href="#monotonic-stack">6. Monotonic Stack</a></li>
<li><a href="#binary-search-search-on-answer">7. Binary Search</a></li>
<li><a href="#binary-search-on-the-answer">8. Binary Search on the Answer</a></li>
<li><a href="#top-k-heap">9. Top-K / Heap</a></li>
<li><a href="#k-way-merge">10. K-way Merge</a></li>
<li><a href="#merge-intervals">11. Merge Intervals</a></li>
<li><a href="#sweep-line">12. Sweep Line</a></li>
<li><a href="#topological-sort">13. Topological Sort</a></li>
<li><a href="#union-find-disjoint-set-union">14. Union-Find (DSU)</a></li>
<li><a href="#greedy">15. Greedy</a></li>
<li><a href="#recursion-backtracking">16. Recursion &amp; Backtracking</a></li>
<li><a href="#divide-conquer">17. Divide &amp; Conquer</a></li>
<li><a href="#dynamic-programming">18. Dynamic Programming</a></li>
<li><a href="#trie-pattern">19. Trie pattern</a></li>
<li><a href="#bit-manipulation">20. Bit Manipulation &amp; Bitmasking</a></li>
<li><a href="#quickselect">21. Quickselect</a></li>
<li><a href="#math-number-theory">+ Math &amp; Number Theory (fast expo, GCD, sieve)</a></li>
<li><a href="#design-randomized">+ Design &amp; Randomized (O(1) structures, reservoir sampling)</a></li>
<li class="part">Part III — Data Structures in Depth (containers)</li>
<li><a href="#arrays">Arrays (Matrix Mechanics, Cyclic Sort)</a></li>
<li><a href="#strings">Strings</a></li>
<li><a href="#linked-lists">Linked Lists</a></li>
<li><a href="#stacks-queues">Stacks &amp; Queues</a></li>
<li><a href="#trees">Trees (traversal, BST, LCA, diameter, tree DP, serialize, build)</a></li>
<li><a href="#heaps-priority-queues">Heaps (streaming median, gotchas)</a></li>
<li><a href="#tries-prefix-trees">Tries (implement)</a></li>
<li><a href="#graphs">Graphs (BFS, DFS, Dijkstra, Bellman-Ford, MST, bridges/SCC, Eulerian)</a></li>
<li><a href="#segment-tree-fenwick-tree">Segment Tree &amp; Fenwick Tree</a></li>
<li class="part">Part IV — Cheat Sheets &amp; Self-Check</li>
<li><a href="#master-cheat-sheets-templates">Master Cheat Sheets &amp; Templates</a></li>
<li><a href="#appendix-self-check-mastery-drills">Appendix — Self-Check &amp; Mastery Drills</a></li>
<li><a href="#master-problem-index-tracker">Master Problem Index &amp; Tracker (all problems, checkable)</a></li>
<li><a href="#practice-solutions-appendix">Practice Solutions Appendix (~320 variations, hints + walkthroughs)</a></li>
<li><a href="#mock-interview-transcripts">Mock Interview Transcripts — Easy / Medium / Hard walkthroughs</a></li>
<li><a href="#traps-catalog">Traps Catalog — every [trap] callout consolidated for revision</a></li>
</ol>

</div>
