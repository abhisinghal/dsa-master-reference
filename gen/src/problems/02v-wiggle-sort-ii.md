# Two Pointers — Wiggle Sort II

*[↗ LeetCode: Wiggle Sort II](https://leetcode.com/problems/wiggle-sort-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Reorder `nums` so `a[0] < a[1] > a[2] < a[3] …` (strict inequality).

**Example 1** — `nums=[1,5,1,1,6,4]` → `[1,6,1,5,1,4]` (or any valid arrangement)
**Example 2** — `nums=[1,3,2,2,3,1]` → `[2,3,1,3,1,2]`

**Constraints** — `1 ≤ n ≤ 5·10⁴`.

---

## Approach 1 — Sort + interleave (canonical simple)

Sort. Place larger half at odd indices in reverse; smaller half at even indices in reverse. Reverse order avoids adjacent duplicates on boundaries.

```java
void wiggleSort(int[] nums) {
    int[] sorted = nums.clone();
    Arrays.sort(sorted);
    int n = nums.length, mid = (n + 1) / 2, r = n - 1;
    for (int k = 0; k < n; k++)
        nums[k] = (k % 2 == 0) ? sorted[--mid] : sorted[r--];
}
```

<CodeTrace
  title="Sort + interleave (canonical simple)"
  :values="['1', '5', '1', '1', '6', '4']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 3 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 5 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

## Approach 2 — Quickselect median + virtual-index Dutch flag (advanced)

**Insight.** Find median via Quickselect. Use virtual index mapping `A(i) = (2i+1) % (n | 1)` to partition into three groups — larger to odd indices, smaller to even, median centered.

**Complexity** — Time **O(n)** average; Space **O(1)** extra.

Code is subtle — study the classic writeup before an interview.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + interleave | O(n log n) | O(n) | canonical & clear |
| Quickselect + Dutch flag | **O(n)** avg | O(1) | polish |

## When to use which

- **Standard** → sort + interleave.
- **Best asymptotic + O(1) space** → Quickselect + virtual index.
- **Wiggle non-strict** → simple pairwise swaps.

## Related problems

- [Wiggle Sort I](https://leetcode.com/problems/wiggle-sort/)
- [Kth Largest Element in an Array](/problems/quickselect-kth-largest)
- [Sort Colors](https://leetcode.com/problems/sort-colors/) — Dutch partition
