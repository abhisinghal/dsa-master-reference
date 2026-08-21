## The Pattern

Divide and conquer solves a problem by splitting it into smaller independent subproblems, solving them recursively, and combining their answers. The senior-level question is not just "can I recurse?" but **where the combine cost lives** and whether the recurrence improves on an iterative or DP formulation.

!!! pattern "Recognition signals"
    **Signals:** naturally splittable input, balanced halves, independent subproblems, cross-boundary combine logic, or recurrences like `T(n) = aT(n/b) + f(n)`. Sorting, inversion counting, closest-pair, and many tree algorithms are canonical examples.

```diagram
{"type":"recursion","title":"Balanced divide and conquer with O(n) combine per level","nodes":[{"id":"n","label":"n work: split + combine O(n)","x":3,"y":0,"role":"primary"},{"id":"l","label":"n/2","x":1.5,"y":1,"role":"green"},{"id":"r","label":"n/2","x":4.5,"y":1,"role":"green"},{"id":"ll","label":"n/4","x":0.75,"y":2,"role":"amber"},{"id":"lr","label":"n/4","x":2.25,"y":2,"role":"amber"},{"id":"rl","label":"n/4","x":3.75,"y":2,"role":"amber"},{"id":"rr","label":"n/4","x":5.25,"y":2,"role":"amber"}],"edges":[{"from":"n","to":"l","label":"split","color":"primary"},{"from":"n","to":"r","label":"split","color":"primary"},{"from":"l","to":"ll","label":"","color":"muted"},{"from":"l","to":"lr","label":"","color":"muted"},{"from":"r","to":"rl","label":"","color":"muted"},{"from":"r","to":"rr","label":"","color":"muted"}],"caption":"For merge sort and inversion count, each level totals O(n) combine work across all nodes, giving O(n log n)."}
```

## The Invariant

Each recursive call returns the correct answer for its exact subrange, and the combine step produces the correct answer for the parent using only child answers plus explicitly handled cross-boundary information. No element or pair may be lost at the split; cross-boundary cases belong in combine.

## Template

```java
long solve(int[] a) {
    int[] buffer = new int[a.length];
    return divide(a, buffer, 0, a.length);
}

long divide(int[] a, int[] buffer, int lo, int hi) {
    if (hi - lo <= 1) return 0L;
    int mid = lo + (hi - lo) / 2;
    long left = divide(a, buffer, lo, mid);
    long right = divide(a, buffer, mid, hi);
    long cross = combine(a, buffer, lo, mid, hi);
    return left + right + cross;
}
```

The combine function is where merge sort spends O(length) merging, and where Count Inversions counts pairs crossing `mid`. Reuse buffers rather than allocating at every node.

| recurrence | condition | result | intuition |
|---|---:|---:|---|
| `T(n)=aT(n/b)+f(n)` | `f(n)=O(n^(log_b a - eps))` | `Theta(n^log_b a)` | leaves dominate |
| same | `f(n)=Theta(n^log_b a log^k n)` | `Theta(n^log_b a log^(k+1)n)` | balanced levels |
| same | `f(n)=Omega(n^(log_b a + eps))` plus regularity | `Theta(f(n))` | root/combine dominates |

## Worked Recognition

- **Merge Sort** (Module 15): split into halves, sort both, then merge in O(n). The O(n) combine across O(log n) levels gives O(n log n).
- **Count Inversions** (Module 15): recursively count inversions inside each half; during merge, count cross inversions when a right value precedes remaining left values.
- Binary tree height/diameter: children are independent subproblems; the combine computes parent height and cross-through-root diameter.

## Complexity

!!! complexity "Complexity"
    Use the recurrence, not vibes. Balanced two-way split with O(n) combine is `T(n)=2T(n/2)+O(n)=O(n log n)`. If combine is O(1), it is often O(n) total nodes; if combine is O(n²), divide and conquer may be worse than a direct method. Recursion stack is O(log n) for balanced splits, O(n) for skewed splits.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Forgetting cross-boundary cases, using `mid = (lo + hi) / 2` where overflow is possible, allocating large temporary arrays per call, assuming the Master Theorem applies to uneven or non-polynomial recurrences, or double-counting combine work at every node and every level.

## When NOT to use it

Do not force divide and conquer when subproblems overlap heavily without memoization, when the combine step is more expensive than the original problem, when input is inherently streaming, or when a linear scan invariant is simpler and more robust.
