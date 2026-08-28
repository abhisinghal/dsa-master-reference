# Hashing — Two Sum Less Than K

*[↗ LeetCode: Two Sum Less Than K](https://leetcode.com/problems/two-sum-less-than-k/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Google, Amazon" />

Return max sum `< k` from any pair, or `-1`.

**Example 1** — `nums=[34,23,1,24,75,33,54,8], k=60` → `58`
**Example 2** — `nums=[10,20,30], k=15` → `-1` (no pair fits under k)
**Example 3** — `nums=[1,2,3,4,5], k=100` → `9` (4+5)

**Constraints** — `1 ≤ n ≤ 100`. Brute is O(n²) = 10⁴ — passes easily here, but the sort+2p is cleaner and generalises to n=10⁵. Brute nested loop is O(n²) = 10⁶ ops at n=10³. Sort + two-pointer is O(n log n) = 10⁴ ops with cache-friendly pass.
<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its 'canonical form' — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For 'first duplicate', a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="two-sum-less-than-k" /> <Bookmark problem-slug="two-sum-less-than-k" />

<InterviewTimer problem-slug="two-sum-less-than-k" />



## Approach 1 — Brute pair enumeration

**Intuition.** Try every pair. Track max sum below k.



```java
int twoSumLessThanKBrute(int[] nums, int k) {
    int best = -1;
    for (int i = 0; i < nums.length; i++)
        for (int j = i + 1; j < nums.length; j++) {
            int s = nums[i] + nums[j];
            if (s < k) best = Math.max(best, s);
        }
    return best;
}
```



**Complexity** — Time **O(n²)**; Space **O(1)**. Fine at n=100. Fails at n=10⁵. *In an interview* say "with sort, this becomes O(n log n) via two pointers."

---

## Approach 2 — Sort + two pointer (canonical)

**Insight.** Sort. `l`, `r` from ends: if `sum < k`, this is a candidate — record it, then advance `l` to try a larger sum. If `sum ≥ k`, retreat `r` to make room.



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

**Complexity** — Time **O(n log n)**; Space **O(1)**. *Say aloud in an interview:* "same monotone-scan template as 3Sum Smaller and Container With Most Water."

**Bucket variant** — since values ≤ 1000, bucket-count then two-pointer over buckets → O(n + 1000) time.

---

## Try it yourself

<JavaRunner problem-slug="two-sum-less-than-k" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute pair | O(n²) | O(1) | Fine at n≤100 |
| **Sort + 2p** | **O(n log n)** | O(1) | **Canonical** |
| Bucket count | O(n + V) | O(V) | Best if V small |

## When to use which

- **Standard** → sort + 2p.
- **Bounded values** → bucket count for O(n).
- **"≤ k" or "≥ k"** → symmetric variants.

<AiCompanion problem-slug="two-sum-less-than-k" pattern-hint="hashing" />

## Related problems

- [Two Sum II](/problems/two-sum-ii-input-array-is-sorted)
- [3Sum Smaller](/problems/3sum-smaller)

<FeedbackWidget problem-slug="two-sum-less-than-k" />
