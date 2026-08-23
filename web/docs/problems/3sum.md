# Hashing — 3Sum

*[↗ LeetCode: 3Sum](https://leetcode.com/problems/3sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Apple, Bloomberg" /&gt;

Given an integer array `nums`, return all **unique** triplets `[nums[i], nums[j], nums[k]]` with `i < j < k` and `nums[i] + nums[j] + nums[k] == 0`.

**Example 1** — `nums = [-1,0,1,2,-1,-4]` → `[[-1,-1,2], [-1,0,1]]`
**Example 2** — `nums = [0,1,1]` → `[]`
**Example 3** — `nums = [0,0,0]` → `[[0,0,0]]`

**Constraints** — `3 ≤ n ≤ 3000`; `-10⁵ ≤ nums[i] ≤ 10⁵`.


&lt;Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/&gt;
---

## Approach 1 — Triple nested loop + set for dedup

**Intuition.** Enumerate every `(i, j, k)`; check sum; add sorted triplet to a set to remove duplicates.



```java
List<List<Integer>> threeSumBrute(int[] nums) {
    Set<List<Integer>> set = new HashSet<>();
    int n = nums.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            for (int k = j + 1; k < n; k++)
                if (nums[i] + nums[j] + nums[k] == 0) {
                    List<Integer> t = Arrays.asList(nums[i], nums[j], nums[k]);
                    Collections.sort(t);
                    set.add(t);
                }
    return new ArrayList<>(set);
}
```



**Complexity** — Time **O(n³)**; Space **O(#triplets)**.

At n=3000 this is 2.7·10¹⁰ ops — TLE.

---

## Approach 2 — Fix `i`, hash-map inner two-sum

**Insight from brute.** For each `i`, run a hash-based Two Sum on `nums[i+1..]` targeting `-nums[i]`.



```java
List<List<Integer>> threeSumHash(int[] nums) {
    Arrays.sort(nums);
    Set<List<Integer>> set = new HashSet<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        Set<Integer> seen = new HashSet<>();
        for (int j = i + 1; j < nums.length; j++) {
            int need = -nums[i] - nums[j];
            if (seen.contains(need))
                set.add(Arrays.asList(nums[i], need, nums[j]));
            seen.add(nums[j]);
        }
    }
    return new ArrayList<>(set);
}
```



**Complexity** — Time **O(n²)**; Space **O(n)**.

---

## Approach 3 — Sort + two-pointer (canonical)

**Insight from hash.** After sorting, the inner two-sum is a converging two-pointer — no extra hash needed. Skip duplicates at all three levels to emit unique triplets naturally.

**Trap** — `i > 0 && nums[i] == nums[i-1]` skips duplicate anchors. **Inside** the while loop: after emitting a valid triplet, advance both `l` and `r` past all duplicates.



```java
List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> out = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (nums[i] > 0) break;                             // no chance of sum 0
        if (i > 0 && nums[i] == nums[i - 1]) continue;      // dedup anchor
        int l = i + 1, r = nums.length - 1;
        while (l < r) {
            int s = nums[i] + nums[l] + nums[r];
            if (s == 0) {
                out.add(Arrays.asList(nums[i], nums[l], nums[r]));
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++; r--;
            } else if (s < 0) l++;
            else r--;
        }
    }
    return out;
}
```



<CodeTrace
  title="Sort + 2p — nums=[-1,0,1,2,-1,-4] sorted=[-4,-1,-1,0,1,2]"
  :values="['-4','-1','-1','0','1','2']"
  :windowKeys="['i','l','r']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, l: 1, r: 5 }, vars: { sum: -3 }, note: "i=-4: -4+-1+2=-3 < 0 → l++" },
    { pointers: { i: 1, l: 2, r: 5 }, vars: { sum: 0, out: "[-1,-1,2]" }, note: "i=-1: emit; skip dup at l" },
    { pointers: { i: 1, l: 3, r: 4 }, vars: { sum: 0, out: "[-1,0,1]" }, note: "l++, r--; s=0 → emit second triplet" },
    { pointers: { i: 3, l: 4, r: 5 }, vars: { sum: 3 }, note: "i=0: 0+1+2=3 > 0 → r--; then i=1 breaks" }
  ]'
/>

**Complexity** — Time **O(n²)** — outer O(n) × inner O(n); Space **O(1)** extra (not counting output).

---

## Try it yourself

<JavaRunner problem-slug="3sum" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Triple loop + set | O(n³) | O(#triplets) | baseline; TLE at n=3000 |
| Fix i + inner hash Two Sum | O(n²) | O(n) | correct; needs dedup |
| Sort + two-pointer | **O(n²)** | O(1) | canonical answer |

## When to use which

- **Standard interview answer** → sort + two-pointer.
- **"Streaming triplets, no sort allowed"** → hash-based approach.
- **"Return count only, not triplets"** → same skeleton, replace list with counter.
- **"Sum to arbitrary target t, not 0"** → same algorithm; replace `-nums[i]` with `t - nums[i]`.

## Related problems

- [3Sum Closest](/problems/3sum-closest) — minimize `|sum - target|`
- [3Sum Smaller](/problems/3sum-smaller) — count triplets with sum &lt; target
- [4Sum](/problems/4sum) — one more nested loop
- [Two Sum](/problems/hashing-two-sum) — the seed