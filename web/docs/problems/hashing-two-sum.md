# Hashing — Two Sum

*[↗ LeetCode: Two Sum](https://leetcode.com/problems/two-sum/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple, Adobe, Bloomberg" /&gt;

Given `nums` and `target`, return indices `[i, j]` such that `nums[i] + nums[j] == target`. Every input has exactly one solution and you may not use the same element twice.

**Example 1** — `nums = [2,7,11,15], target = 9` → `[0, 1]`
**Example 2** — `nums = [3,2,4], target = 6` → `[1, 2]`
**Example 3** — `nums = [3,3], target = 6` → `[0, 1]`

**Constraints** — `2 ≤ n ≤ 10⁴`, `-10⁹ ≤ nums[i], target ≤ 10⁹`.


&lt;Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/&gt;
---

## Approach 1 — Brute force (nested loops)

**Intuition.** Check every pair `(i, j)` with `j > i`. If they sum to target, return them.



```java
int[] twoSumBrute(int[] nums, int target) {
    int n = nums.length;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (nums[i] + nums[j] == target) return new int[]{i, j};
        }
    }
    return new int[0];
}
```



<CodeTrace
  title="Brute force — nums=[2,7,11,15], target=9"
  :values="[2,7,11,15]"
  :windowKeys="['i','j']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0, j: 1 }, vars: { sum: 9 }, note: "2 + 7 = 9. return [0,1]", added: [0,1] }
  ]'
/>

**Complexity** — Time **O(n²)** worst case; Space **O(1)**.

At n=10⁴ the pair count is ~5·10⁷ — passes but slow. At n=10⁶ this fails timeouts.

---

## Approach 2 — Sort + two pointers

**Insight from brute.** The nested loop restates *"does the array contain `target − nums[i]`?"* — a search question. Sorting turns it into a two-pointer sweep at O(n log n).

**Trap** — sorting loses original indices. Keep `(value, original_index)` pairs.



```java
int[] twoSumSort(int[] nums, int target) {
    int n = nums.length;
    int[][] paired = new int[n][2];
    for (int i = 0; i < n; i++) { paired[i][0] = nums[i]; paired[i][1] = i; }
    Arrays.sort(paired, (a, b) -> a[0] - b[0]);
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int sum = paired[lo][0] + paired[hi][0];
        if (sum == target) return new int[]{paired[lo][1], paired[hi][1]};
        if (sum < target) lo++;
        else              hi--;
    }
    return new int[0];
}
```



<CodeTrace
  title="Sort + two pointers — sorted (2,7,11,15), target=9"
  :values="[2,7,11,15]"
  :windowKeys="['lo','hi']"
  :cellWidth="46"
  :steps='[
    { pointers: { lo: 0, hi: 3 }, vars: { sum: 17 }, note: "2 + 15 = 17 gt 9 → hi--" },
    { pointers: { lo: 0, hi: 2 }, vars: { sum: 13 }, note: "2 + 11 = 13 gt 9 → hi--" },
    { pointers: { lo: 0, hi: 1 }, vars: { sum: 9 }, note: "2 + 7 = 9 match → return [0,1]", added: [0,1] }
  ]'
/>

**Complexity** — Time **O(n log n)** (sorting dominates); Space **O(n)** for the paired array.

Better asymptotic than brute, but the sort dominates. Only real win: works on the streaming/sorted variant, and O(1) extra space if in-place-sortable.

---

## Approach 3 — Hash map (one pass)

**Insight from sort+2ptr.** We didn't need the ordering — we needed to answer *"have I seen `target − nums[i]`?"* in O(1). That's a hash map.

Scan once. At each `i`, check if the map already contains the complement `target − nums[i]`; if so, return `[map.get(complement), i]`. Otherwise store `map.put(nums[i], i)`.

**Trap** — check the map *before* inserting. Otherwise `nums=[3,3], target=6` matches the first 3 with itself as `[0,0]`.



```java
int[] twoSumHash(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[0];
}
```



<CodeTrace
  title="Hash map one-pass — nums=[2,7,11,15], target=9"
  :values="[2,7,11,15]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { complement: 7, seen: "{}" }, note: "miss. put seen[2]=0" },
    { pointers: { i: 1 }, vars: { complement: 2, "seen[2]": 0 }, note: "HIT → return [0, 1]", added: [0,1] }
  ]'
/>

**Complexity** — Time **O(n)** amortized; Space **O(n)** for the map.

Optimal. Single scan, O(1) lookup, no sort.

---

## Try it yourself

<JavaRunner problem-slug="hashing-two-sum" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Brute force | O(n²) | O(1) | Baseline — state it, then move on |
| Sort + two pointers | O(n log n) | O(n) or O(1) | Bonus: reuse on the *sorted-input* variant |
| Hash map (one pass) | **O(n)** | O(n) | Expected optimum |

## When to use which

- **Interviewer opens Two Sum cold** → walk brute → hash map. Explain space:time trade explicitly.
- **Input is sorted** → skip the map; use two pointers for O(1) extra space. That's *Two Sum II*.
- **Interviewer probes "what if it's a stream?"** → hash map wins hands-down; two pointers can't handle streaming.
- **Interviewer probes "what if we need all pairs?"** → sort + two pointers; the map only finds the first match.

## Related problems (same ladder applies)

- [Two Sum II — Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) — drop the map, use two pointers on already-sorted input (O(1) space)
- [3Sum](https://leetcode.com/problems/3sum/) — sort, fix pivot i, two-pointer the tail
- [4Sum](https://leetcode.com/problems/4sum/) — sort, fix i and j, two-pointer the tail
- [Two Sum III — Design](https://leetcode.com/problems/two-sum-iii-data-structure-design/) — hash map with counts for the streaming variant
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) — same idea, but hash **prefix sums** instead of raw values