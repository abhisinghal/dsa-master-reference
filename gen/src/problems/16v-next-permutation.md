# Backtracking — Next Permutation

*[↗ LeetCode: Next Permutation](https://leetcode.com/problems/next-permutation/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

<CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg" />

Rearrange nums to the next lexicographic permutation in-place. If none, sort ascending.

**Example 1** — `nums=[1,2,3]` → `[1,3,2]`
**Example 2** — `nums=[3,2,1]` → `[1,2,3]` (last perm → wrap to first)
**Example 3** — `nums=[1,1,5]` → `[1,5,1]`

**Constraints** — `1 ≤ n ≤ 100`. Brute enumerate all n! permutations + sort + look up next is O(n! · n log n) — 100! is beyond universe. Classic in-place algorithm is O(n).


<Hints
  hint1="You're exploring a decision tree. What's the state at each depth? What choices are available?"
  hint2="Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo."
  hint3="Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
/>
---

<MarkSolved problem-slug="next-permutation" /> <Bookmark problem-slug="next-permutation" />

<InterviewTimer problem-slug="next-permutation" />



## Approach 1 — Enumerate all n! permutations

**Intuition.** Generate all permutations in lex order (or sort them). Find the current one. Return the next.

**Complexity** — Time **O(n! · n)**; Space **O(n! · n)**. Beyond n=10. *In an interview* say "there's a beautiful O(n) in-place algorithm — pivot-swap-reverse."

---

## Approach 2 — Classic algorithm (canonical)

**Insight — 3-step pivot-swap-reverse:**
1. Scan from right; find first `i` with `nums[i] < nums[i+1]` (**pivot**). If none, whole array is decreasing → reverse to ascending.
2. Scan from right; find first `j` with `nums[j] > nums[i]`. **Swap** `i` and `j`.
3. **Reverse** suffix from `i+1` to end (was decreasing → becomes increasing = smallest larger permutation).

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

**Complexity** — Time **O(n)**; Space **O(1)**. *Say aloud in an interview:* "same pattern in `std::next_permutation` in the C++ standard library, and `itertools.permutations`'s iterative production."

---

## Try it yourself

<JavaRunner problem-slug="next-permutation" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Enumerate all perms | O(n! · n) | O(n! · n) | Reference; fails past n=10 |
| **Classic 3-step** | **O(n)** | O(1) | **Canonical** |

## When to use which

- **Standard next-perm** → this algorithm.
- **Previous permutation** → mirror the steps (scan for decreasing gap, etc).
- **Kth permutation** → factorial-number system.

<AiCompanion problem-slug="next-permutation" pattern-hint="backtracking" />

## Related problems

- [Permutations](/problems/permutations)
- [Permutation Sequence](https://leetcode.com/problems/permutation-sequence/)

<FeedbackWidget problem-slug="next-permutation" />
