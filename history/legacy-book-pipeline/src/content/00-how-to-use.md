## How to Use This Book

This is a **reference and training manual**, not a beginner tutorial. It assumes you already write production Java fluently and want to build one specific skill: **seeing the pattern inside an unfamiliar problem fast enough to solve it under interview pressure.**

Every chapter is engineered around a single conviction:

!!! key "The thesis of this book"
    You do not pass senior/staff algorithm interviews by memorizing solutions. You pass them by recognizing that *this new problem is a disguised instance of a pattern you already understand*, then re-deriving the algorithm from its invariant. Memory fails under stress; derivation does not.

### The three layers

The book has three layers, and you should read them differently.

| Layer | What it contains | How to read it |
|---|---|---|
| **Part I — Modules** | The 15 core data-structure & algorithm families | Read linearly the first time. Build the mental models. |
| **Part II — Patterns** | 20 cross-cutting patterns (sliding window, monotonic stack, binary search on answer, \u2026) | Read after Part I. This is where recognition is trained. |
| **Part III — Interview Mastering** | Decision trees, comparison matrices, and master indexes | Use as a lookup during revision and mock interviews. |

### The problem template

Every canonical problem is dissected with the same 20-part editorial template. You will quickly learn to skim to the section you need:

!!! pattern "Anatomy of a problem entry"
    **Problem \u2192 Intuition \u2192 Naive \u2192 Why naive fails \u2192 Key Observation \ud83d\udd11 \u2192 Pattern Recognition \u2192 Invariant \u2192 Visual \u2192 Flow diagram \u2192 Walkthrough \u2192 Why it works \u2192 Java \u2192 Code walkthrough \u2192 Complexity \u2192 Edge cases \u2192 Common mistakes \u2192 Optimization \u2192 Alternatives \u2192 Follow-ups \u2192 Variations \u2192 Pattern connection.**

The **Key Observation** box is the single most important paragraph in each entry. If you remember nothing else from a problem, remember that.

### How to actually drill

1. **Cover the solution.** Read only *The Problem* and *The Intuition*, then close the book and attempt it.
2. **Diff your reasoning against the Key Observation.** Most failures are a missing observation, not a coding bug.
3. **Reconstruct the invariant out loud.** If you can state the invariant, you can rebuild the code.
4. **Revisit via the pattern, not the problem.** A week later, open the *Pattern \u2192 Problems Index* and re-solve from the pattern name alone.

!!! tip "Interview signal"
    In a real interview, narrate the pattern-recognition step explicitly: \u201cThe fact that the array is sorted and we want a pair summing to a target is the two-pointers signal.\u201d Interviewers score *how* you navigate to the solution, not just the final code.

### Notation & conventions

- Complexity is written as **T:** (time) and **S:** (space) badges near each solution.
- Java is modern and interview-ready: `ArrayDeque` over `Stack`, overflow-safe comparators, `long` where products can overflow, `int[]{r,c}` for grid coordinates.
- Diagrams are generated deterministically from data, so a pointer at index `i` in a figure is exactly the `i` in the adjacent code.

!!! warning "This book optimizes for transfer, not coverage"
    We deliberately spend more space on *why an approach generalizes* than on cataloguing every LeetCode variant. Ten deeply understood patterns beat a hundred memorized solutions.
