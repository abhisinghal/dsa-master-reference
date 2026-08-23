# Backtracking — Next Permutation

*[↗ LeetCode: Next Permutation](https://leetcode.com/problems/next-permutation/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg" />

Rearrange nums to the next lexicographic permutation in-place. If none, sort ascending.

**Example 1** — `nums=[1,2,3]` → `[1,3,2]`
**Example 2** — `nums=[3,2,1]` → `[1,2,3]`

**Constraints** — `1 ≤ n ≤ 100`.


<Hints
  hint1="You’re exploring a decision tree. What’s the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

## Approach — Classic algorithm (canonical)

**Steps.**
1. Scan from right; find first `i` with `nums[i] < nums[i+1]` (pivot). If none, reverse whole array.
2. Scan from right; find first `j` with `nums[j] > nums[i]`. Swap.
3. Reverse suffix from `i+1` to end (was decreasing → becomes increasing = smallest larger permutation).

```java
void nextPermutation(int[] nums) {
    int n = nums.length, i = n - 2;
    while (i >= 0 && nums[i] >= nums[i + 1]) i--;
    if (i >= 0) {
        int j = n - 1;
        while (nums[j] <= nums[i]) j--;
        swap(nums, i, j);
    }
    reverse(nums, i + 1, n - 1);
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
void reverse(int[] a, int l, int r) { while (l < r) swap(a, l++, r--); }
```

<CodeTrace
  title="Classic algorithm (canonical)"
  :values="['1', '2', '3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="next-permutation" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Classic 3-step | **O(n)** | O(1) | canonical |

## When to use which

- **Standard next-perm** → this algorithm.
- **Previous permutation** → mirror the steps (scan for decreasing gap, etc).
- **Kth permutation** → factorial-number system.

## Related problems

- [Permutations](/problems/permutations)
- [Permutation Sequence](https://leetcode.com/problems/permutation-sequence/)