# Two Pointers — Move Zeroes

*[↗ LeetCode: Move Zeroes](https://leetcode.com/problems/move-zeroes/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple" />

Move all zeros to end preserving order of non-zeros. In-place.

**Example 1** — `nums=[0,1,0,3,12]` → `[1,3,12,0,0]`
**Example 2** — `nums=[0]` → `[0]`

**Constraints** — `1 ≤ n ≤ 10⁴`.


<Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="move-zeroes" />

<InterviewTimer problem-slug="move-zeroes" />



## Approach 1 — Two-pass write

Copy non-zeros forward; zero-fill tail.

## Approach 2 — Slow/fast write pointer (canonical)

**Insight.** One pointer for read, one for the next slot to write.

```java
void moveZeroes(int[] nums) {
    int w = 0;
    for (int r = 0; r < nums.length; r++)
        if (nums[r] != 0) nums[w++] = nums[r];
    while (w < nums.length) nums[w++] = 0;
}
```

<CodeTrace
  title="Two-pass write"
  :values="['0', '1', '0', '3', '12']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 4 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

## Approach 3 — Swap on the fly (fewer writes)

Use when array is mostly zeros — each non-zero causes one swap.

```java
void moveZeroesSwap(int[] nums) {
    int w = 0;
    for (int r = 0; r < nums.length; r++)
        if (nums[r] != 0) { int t = nums[r]; nums[r] = nums[w]; nums[w++] = t; }
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="move-zeroes" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two-pass | O(n) | O(1) | baseline |
| Slow/fast writer | **O(n)** | O(1) | canonical |
| Swap-in-place | O(n) | O(1) | fewer writes |

## When to use which

- **Standard** → slow/fast.
- **Minimize writes** (SSD wear, etc.) → swap variant.
- **Removes / partition** → same template family.

<AiCompanion problem-slug="move-zeroes" pattern-hint="two pointers" />

## Related problems

- [Remove Element](https://leetcode.com/problems/remove-element/)
- [Sort Array By Parity](/problems/sort-array-by-parity)

<FeedbackWidget problem-slug="move-zeroes" />

<RelatedProblems problems="4sum::4sum|container-with-most-water::Container With Most Water|squares-of-a-sorted-array::Squares Of A Sorted Array" />
