# Divide & Conquer — Global and Local Inversions

*[↗ LeetCode: Global and Local Inversions](https://leetcode.com/problems/global-and-local-inversions/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/divide-conquer)

Return `true` iff the count of **global** inversions (pairs `i < j` with `a[i] > a[j]`) equals the count of **local** inversions (adjacent pairs `a[i] > a[i+1]`).

**Example** — `[1,0,2]` → `true` (1 global = 1 local); `[1,2,0]` → `false` (2 global, 1 local)

---

## Approach 1 — Count both directly

O(n²) for global. TLE.

## Approach 2 — Merge sort to count global

Global count = inversion count via merge sort (O(n log n)); local count is O(n). Compare.

## Approach 3 — Observation trick (O(n))

**Insight.** Every local inversion IS a global inversion, so global ≥ local. They are equal iff no non-adjacent inversion exists — meaning every value `a[i]` is at most 1 position away from its sorted position `i`.

**Rule.** Return `false` if any `|a[i] - i| > 1`.

```java
boolean isIdealPermutation(int[] a) {
    for (int i = 0; i < a.length; i++)
        if (Math.abs(a[i] - i) > 1) return false;
    return true;
}
```

<CodeTrace
  title="Position drift check — [1,0,2]"
  :values="[1,0,2]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { "|a[i]-i|": 1 }, note: "1 vs 0 → drift 1. OK" },
    { pointers: { i: 1 }, vars: { "|a[i]-i|": 1 }, note: "0 vs 1 → drift 1. OK" },
    { pointers: { i: 2 }, vars: { "|a[i]-i|": 0 }, note: "2 vs 2 → OK. answer true", added: [0,1,2] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Direct global (nested) | O(n²) | O(1) |
| Merge sort count | O(n log n) | O(n) |
| Drift check | **O(n)** | **O(1)** |

## Related problems

- [Count of Smaller Numbers After Self](/problems/divide-conquer-inversions) — merge sort framework
- [Reverse Pairs](/problems/reverse-pairs)
