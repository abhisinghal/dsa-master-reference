# Hashing — Two Sum II (Input Array Is Sorted)

*[↗ LeetCode: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Meta, Amazon, Google" />

Sorted array; return 1-indexed pair summing to target.

**Example 1** — `numbers=[2,7,11,15], target=9` → `[1,2]`
**Example 2** — `numbers=[2,3,4], target=6` → `[1,3]`
**Example 3** — `numbers=[-1,0], target=-1` → `[1,2]`

**Constraints** — `2 ≤ n ≤ 3·10⁴`.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="two-sum-ii-input-array-is-sorted" />

<InterviewTimer problem-slug="two-sum-ii-input-array-is-sorted" />



## Approach 1 — Hash-map

Ignores sortedness. O(n) time O(n) space.

## Approach 2 — Opposing two-pointer (canonical)

**Insight.** Sum monotone in pointer movement — deterministic.

```java
int[] twoSum(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        int s = nums[l] + nums[r];
        if (s == target) return new int[]{l + 1, r + 1};
        if (s < target) l++; else r--;
    }
    return new int[]{-1, -1};
}
```

<CodeTrace
  title="Hash-map"
  :values="['2', '7', '11', '15']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="two-sum-ii-input-array-is-sorted" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Hash map | O(n) | O(n) | works but wastes sort |
| Opposing 2p | **O(n)** | **O(1)** | canonical |

## When to use which

- **Sorted input** → 2p every time.
- **Not sorted** → hash.
- **k-Sum on sorted** → recursion with 2p base.

<AiCompanion problem-slug="two-sum-ii-input-array-is-sorted" pattern-hint="hashing" />

## Related problems

- [Two Sum](/problems/hashing-two-sum)
- [3Sum](/problems/3sum)

<FeedbackWidget problem-slug="two-sum-ii-input-array-is-sorted" />

<RelatedProblems problems="hashing-two-sum::Hashing Two Sum|3sum::3sum|valid-anagram::Valid Anagram" />
