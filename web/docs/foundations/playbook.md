# The Interview Playbook
<p class="secgoal"><b>What &amp; why:</b> knowing the algorithm is only half the score. At senior/staff level the other half is <b>how you drive the room</b> — clarifying, narrating tradeoffs, and testing your own code before the interviewer has to. This page is the meta-process to run on <i>every</i> problem, independent of topic.</p>

The strongest candidates rarely produce the cleverest algorithm — they produce the clearest *process*. Interviewers are scoring signal, not just the final answer: did you scope the problem, reason about complexity out loud, choose a structure deliberately, and verify correctness yourself? Run the loop below on every question and those signals emit automatically.

## The 6-Phase Solving Loop

<Callout kind="key" title="The loop">

**C-E-B-O-C-V:** **C**larify → **E**xamples → **B**rute force → **O**ptimize → **C**ode → **V**erify. Spend the first third of the interview *before* writing real code. Silence and a blank screen read as "stuck"; a narrated plan reads as "senior."

</Callout>

| # | Phase | Time | What you actually do | What you say out loud |
|---|---|---|---|---|
| 1 | **Clarify** | 2–3 min | Restate the problem in your words; pin down input size, types, ranges, duplicates, sorted-ness, empties, negatives, mutability, memory limits. | *"So input is up to 10⁵ ints, possibly negative, possibly with duplicates — and I can't mutate the input, right?"* |
| 2 | **Examples** | 1–2 min | Write one normal case **and** the nasty edges (empty, single element, all-equal, overflow). Hand-trace the normal one. | *"Let me make sure I understand with `[3,1,1]` and target 2… and what should empty return?"* |
| 3 | **Brute force** | 1–2 min | State the naive solution and its complexity — *don't* code it. Name the **target** complexity from the input size (see the [complexity heuristic](/foundations/complexity)). | *"Brute force is O(n²) pair-checking. n is 10⁵, so O(n²) ≈ 10¹⁰ is too slow — I need O(n) or O(n log n)."* |
| 4 | **Optimize** | 2–4 min | Route to a pattern via the [decision tree](/patterns/). State the **key insight and invariant before coding**. Get buy-in. | *"Because it's sorted, two converging pointers discard a whole side each step — O(n). The invariant is: the answer, if any, lies between `lo` and `hi`."* |
| 5 | **Code** | 10–15 min | Write clean, named code top-to-bottom. Narrate as you go. Handle the edges you listed in phase 2. | *"I'll guard the empty case first, then…"* |
| 6 | **Verify** | 3–5 min | Dry-run your **example** line by line, then the edges. State final time/space. Offer follow-ups (scale, concurrency, alternate structure). | *"Tracing `[2,7,11]`… returns indices `[0,1]`, correct. Empty → `[]`. Final: O(n) time, O(n) space."* |

<Callout kind="inv" title="Invariant of the loop">

you never write real code you can't already justify. If you can't state the invariant in one sentence (phase 4), you're not ready for phase 5 — go back.

</Callout>

## Reading the signals — trigger → say this

The recognition table (Part II) maps *problem words* → *pattern*. This one maps the same triggers to the **sentence** that shows the interviewer you saw it.

| When you hear / see… | Say this | Route to |
|---|---|---|
| "sorted array", "pair that sums to" | *"Sorted lets me converge two pointers in O(n)."* | [Two Pointers](#the-21-core-patterns-recognition-navigation-map) |
| "contiguous subarray / substring", "window" | *"This is a sliding window; I'll grow right and shrink left on the rule."* | [Sliding Window](#the-21-core-patterns-recognition-navigation-map) |
| "top K", "K largest / closest", "median of stream" | *"A size-K heap keeps the boundary element at the root — O(n log K)."* | [Top-K / Heap](#the-21-core-patterns-recognition-navigation-map) |
| "minimum / maximum feasible X", monotone predicate | *"I can binary-search the answer: feasibility forms a boundary."* | [Binary Search on Answer](#the-21-core-patterns-recognition-navigation-map) |
| "number of ways", "min/max cost", overlapping subproblems | *"State, transition, base, order — this is DP."* | [Dynamic Programming](#the-21-core-patterns-recognition-navigation-map) |
| "prerequisites", "build order", "cycle?" | *"Directed graph → topological sort; if I can't emit all nodes, there's a cycle."* | [Topological Sort](#the-21-core-patterns-recognition-navigation-map) |
| "connected", "groups", "is X reachable from Y" | *"Union-Find for connectivity, or flood-fill if I must walk it."* | [Union-Find](#the-21-core-patterns-recognition-navigation-map) |
| "n ≤ 20", "visit every subset/permutation" | *"Small n screams bitmask DP or backtracking over states."* | [Backtracking](#the-21-core-patterns-recognition-navigation-map) |

## Senior &amp; staff differentiators

<Callout kind="pat" title="What separates a hire from a strong hire">

at L5+/staff, the bar isn't "solved it." It's these:

</Callout>

- **Drive tradeoffs unprompted.** *"Heap is O(n log K); Quickselect is O(n) average but destroys input and is O(n²) worst-case — which matters here?"*
- **Ask about scale before choosing.** 10³ vs 10⁹ elements changes everything: in-memory sort vs external, `int` vs `long`, exact vs approximate.
- **State complexity for every solution, including the brute force** — time *and* space. Never leave it implicit.
- **Name the alternative you rejected and why.** Shows breadth and deliberate choice, not luck.
- **Test your own code.** Dry-run before the interviewer asks. Volunteer the edge cases. This single habit most separates senior from mid.
- **Talk about production.** Overflow (`long`), thread-safety, what breaks at 100× scale, how you'd unit-test it.

## Red flags that fail strong candidates

<Callout kind="trap" title="Avoid these — they read as &quot;not senior&quot;">

silent coding with no narration; jumping to code before stating an approach; claiming a complexity you can't defend; never considering the empty/single/overflow case; and — the most common — *not noticing your own bug* on a trivial input the interviewer then has to point out.

</Callout>

# Study Plans &amp; Revision Cadence
<p class="secgoal"><b>What &amp; why:</b> this book is a reference, not a schedule. Pick a track below by how much runway you have, and use the spaced-repetition table so what you learn actually sticks to the interview date.</p>

## Pick your track

<Callout kind="key" title="How to choose">

all three tracks follow the same order — **Foundations → Patterns → Depth** — they differ only in how many canonical problems per pattern you drill. Depth beats breadth: 3 problems you can reproduce cold beat 12 you half-remember.

</Callout>

| | **2-Week Sprint** (interview imminent) | **4-Week Standard** | **8-Week Mastery** |
|---|---|---|---|
| **Days 1–2** | Skim Part I primer + Complexity; memorize the [decision tree](/patterns/). | Part I in full; do the *Easy* structure warm-ups. | Part I in full + re-implement each structure from scratch once. |
| **Core** | 1 canonical problem per pattern (the **Canonical** one on each card). | 2–3 problems per pattern; every card's template from memory. | All canonical problems + the *variation* links; write your own variations. |
| **Data structures** | Read Part IV callouts only. | Work Trees / Graphs / Heaps fully. | Part IV in full + segment tree / trie / union-find by hand. |
| **Daily volume** | 6–8 problems | 4–5 problems | 3–4 problems, deeper |
| **Last 2 days** | Part II + Part V cheat sheets; the [self-check drills](/appendix/self-check). | Mock interviews using the [6-phase loop](/foundations/playbook). | Timed mocks + re-drill every problem you missed. |

## Spaced-repetition schedule

You forget ~70% of a freshly-learned solution within a week unless you re-touch it. Don't re-solve from scratch each time — re-touch at *increasing* intervals, spending less each pass.

| Pass | When | What you do (≈ time per problem) |
|---|---|---|
| **Learn** | Day 0 | Solve it, or read + understand the solution fully. Note the pattern + invariant. (15–25 min) |
| **Reinforce** | Day +1 | From the problem name alone, re-derive the approach and code it. (8–12 min) |
| **Recall** | Day +3 | Read only the 🔑/📐/⚠️ callouts; state the invariant and the trap from memory. (2–3 min) |
| **Retain** | Day +7 | Re-code the template cold; if you stall, mark it for another cycle. (5–8 min) |
| **Cement** | Day +21 | Recognition only: given a *disguised* prompt, name the pattern in &lt;30 s. (1 min) |
| **Interview eve** | Last night | Read Part II (patterns) + Part V (cheat sheets) end-to-end. No new problems. |

## The daily loop

<Callout kind="note" title="A good study session">

(1) **warm up** by naming the pattern for 3 problems you've seen. (2) **Learn** 1–2 new problems with the 6-phase loop, out loud, as if interviewing. (3) **Review** yesterday's problems cold. (4) **Log misses** — every problem you couldn't reproduce goes back into the Day+1 bucket. Track them in the [Problem Index](/appendix/problem-index) checklist.

</Callout>

