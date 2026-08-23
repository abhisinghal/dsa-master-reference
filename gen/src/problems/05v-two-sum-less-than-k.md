# Hashing — Two Sum Less Than K

*[↗ LeetCode: Two Sum Less Than K](https://leetcode.com/problems/two-sum-less-than-k/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Google, Amazon" />

Return max sum `< k` from any pair, or `-1`.

**Example 1** — `nums=[34,23,1,24,75,33,54,8], k=60` → `58`
**Example 2** — `nums=[10,20,30], k=15` → `-1`

**Constraints** — `1 ≤ n ≤ 100`.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/>
---

## Approach — Sort + two pointer (canonical)

**Insight.** Sort. `l`, `r` from ends: if `sum < k`, record and advance `l`; else retreat `r`.

```java
int twoSumLessThanK(int[] nums, int k) {
    Arrays.sort(nums);
    int l = 0, r = nums.length - 1, best = -1;
    while (l < r) {
        int s = nums[l] + nums[r];
        if (s < k) { best = Math.max(best, s); l++; }
        else r--;
    }
    return best;
}
```

<CodeTrace
  title="Sort + two pointer (canonical)"
  :values="['34', '23', '1', '24', '75', '33', '54', '8']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 4 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 7 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**.

**Bucket variant** — since values ≤ 1000, bucket-count then two-pointer over buckets → O(n + 1000) time.

---

## Try it yourself

<JavaRunner problem-slug="two-sum-less-than-k" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + 2p | **O(n log n)** | O(1) | canonical |
| Bucket count | O(n + V) | O(V) | best if V small |

## When to use which

- **Standard** → sort + 2p.
- **Bounded values** → bucket count for O(n).
- **"≤ k" or "≥ k"** → symmetric variants.

## Related problems

- [Two Sum II](/problems/two-sum-ii-input-array-is-sorted)
- [3Sum Smaller](/problems/3sum-smaller)