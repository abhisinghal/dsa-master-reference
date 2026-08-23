# Two Pointers — 4Sum

*[↗ LeetCode: 4Sum](https://leetcode.com/problems/4sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Meta, Amazon, Google, Adobe" />

Given an integer array `nums` and integer `target`, return all unique quadruplets `[a, b, c, d]` with `a + b + c + d == target`.

**Example 1** — `nums = [1,0,-1,0,-2,2], target = 0` → `[[-2,-1,1,2], [-2,0,0,2], [-1,0,0,1]]`
**Example 2** — `nums = [2,2,2,2,2], target = 8` → `[[2,2,2,2]]`
**Example 3** — `nums = [1000000000,1000000000,1000000000,1000000000], target = -294967296` → `[]` (overflow trap — use `long`)

**Constraints** — `1 ≤ n ≤ 200`; `-10⁹ ≤ nums[i], target ≤ 10⁹`.


<Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="4sum" />

<InterviewTimer problem-slug="4sum" />



## Approach 1 — Quadruple loop + set for dedup

**Intuition.** Enumerate every `(i, j, k, l)`; check sum; sort quadruplet, put in set.

```java
List<List<Integer>> fourSumBrute(int[] nums, int target) {
    Set<List<Integer>> set = new HashSet<>();
    Arrays.sort(nums);
    int n = nums.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            for (int k = j + 1; k < n; k++)
                for (int l = k + 1; l < n; l++)
                    if ((long) nums[i] + nums[j] + nums[k] + nums[l] == target)
                        set.add(Arrays.asList(nums[i], nums[j], nums[k], nums[l]));
    return new ArrayList<>(set);
}
```

**Complexity** — Time **O(n⁴)**; Space **O(#quadruplets)**.

---

## Approach 2 — Two nested loops + inner two-pointer (canonical)

**Insight from brute.** Sort. Fix `i` and `j`; run two pointers on `[j+1, n-1]` targeting `t - nums[i] - nums[j]`. Skip duplicates at all four levels.

**Trap** — **overflow**: sums can exceed `Integer.MAX_VALUE`. Use `long` for the running sum.

```java
List<List<Integer>> fourSum(int[] nums, int target) {
    Arrays.sort(nums);
    List<List<Integer>> out = new ArrayList<>();
    int n = nums.length;
    for (int i = 0; i < n - 3; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        for (int j = i + 1; j < n - 2; j++) {
            if (j > i + 1 && nums[j] == nums[j - 1]) continue;
            int l = j + 1, r = n - 1;
            while (l < r) {
                long s = (long) nums[i] + nums[j] + nums[l] + nums[r];
                if (s == target) {
                    out.add(Arrays.asList(nums[i], nums[j], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++; r--;
                } else if (s < target) l++;
                else r--;
            }
        }
    }
    return out;
}
```

<CodeTrace
  title="4-sum — nums=[1,0,-1,0,-2,2] sorted=[-2,-1,0,0,1,2], target=0"
  :values="['-2','-1','0','0','1','2']"
  :windowKeys="['i','j','l','r']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, j: 1, l: 2, r: 5 }, vars: { sum: -1 }, note: "-2-1+0+2=-1 < 0 → l++" },
    { pointers: { i: 0, j: 1, l: 4, r: 5 }, vars: { sum: 0, out: "[-2,-1,1,2]" }, note: "emit; then l++, r--" },
    { pointers: { i: 0, j: 2, l: 3, r: 5 }, vars: { sum: 0, out: "[-2,0,0,2]" }, note: "j++ finds another triplet" },
    { pointers: { i: 1, j: 2, l: 3, r: 4 }, vars: { sum: 0, out: "[-1,0,0,1]" }, note: "final" }
  ]'
/>

**Complexity** — Time **O(n³)**; Space **O(1)** extra.

---

## Approach 3 — Generalized `kSum` recursion

**Insight from above.** Recurse on `k`: at `k = 2` run two-pointer. Same complexity `O(n^(k-1))`, cleaner code for larger `k`.

```java
List<List<Integer>> kSum(int[] nums, long target, int start, int k) {
    List<List<Integer>> out = new ArrayList<>();
    if (k == 2) {
        int l = start, r = nums.length - 1;
        while (l < r) {
            long s = (long) nums[l] + nums[r];
            if (s == target) {
                out.add(new ArrayList<>(Arrays.asList(nums[l], nums[r])));
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++; r--;
            } else if (s < target) l++; else r--;
        }
        return out;
    }
    for (int i = start; i <= nums.length - k; i++) {
        if (i > start && nums[i] == nums[i - 1]) continue;
        for (List<Integer> sub : kSum(nums, target - nums[i], i + 1, k - 1)) {
            List<Integer> quad = new ArrayList<>();
            quad.add(nums[i]);
            quad.addAll(sub);
            out.add(quad);
        }
    }
    return out;
}
```

**Complexity** — Time **O(n^(k-1))**; Space **O(k)** recursion.

---

## Try it yourself

<JavaRunner problem-slug="4sum" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Quadruple loop | O(n⁴) | O(#quads) | baseline |
| Two loops + inner 2p | **O(n³)** | O(1) | canonical answer |
| Generalized kSum recursion | O(n^(k−1)) | O(k) | polish — extensible |

## When to use which

- **Standard 4-sum** → two loops + inner two-pointer.
- **kSum for arbitrary k** → recursive kSum with 2Sum base case.
- **4Sum II** ("`a[i] + b[j] + c[k] + d[l] == 0` from four arrays") → hash-map on `(a+b)` vs `-(c+d)` — different technique, O(n²).
- **Overflow** — always cast to `long` when values can be `±10⁹`.

<AiCompanion problem-slug="4sum" pattern-hint="two pointers" />

## Related problems

- [3Sum](/problems/3sum) — one fewer nested loop
- [3Sum Closest](/problems/3sum-closest) — closest sum variant
- [4Sum II](https://leetcode.com/problems/4sum-ii/) — hash-based, splits into halves
- [Two Sum](/problems/hashing-two-sum)

<FeedbackWidget problem-slug="4sum" />

<RelatedProblems problems="valid-palindrome-ii::Valid Palindrome II|container-with-most-water::Container With Most Water|merge-sorted-array::Merge Sorted Array" />
