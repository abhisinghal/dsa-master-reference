# Sliding Window — Count Number of Nice Subarrays

*[↗ LeetCode: Count Number of Nice Subarrays](https://leetcode.com/problems/count-number-of-nice-subarrays/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

<CompanyTags companies="Amazon, Google" />

Given an array `nums` and integer `k`, return the number of contiguous subarrays containing exactly `k` odd numbers.

**Example 1** — `nums = [1,1,2,1,1], k = 3` → `2`
**Example 2** — `nums = [2,4,6], k = 1` → `0`
**Example 3** — `nums = [2,2,2,1,2,2,1,2,2,2], k = 2` → `16`

**Constraints** — `1 ≤ n ≤ 5 · 10⁴`; `1 ≤ nums[i] ≤ 10⁵`; `1 ≤ k ≤ n`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="count-number-of-nice-subarrays" />

<InterviewTimer problem-slug="count-number-of-nice-subarrays" />



## Approach 1 — Every subarray

**Intuition.** For each `[i, j]`, count odd numbers.

```java
int numberOfSubarraysBrute(int[] nums, int k) {
    int n = nums.length, count = 0;
    for (int i = 0; i < n; i++) {
        int odd = 0;
        for (int j = i; j < n; j++) {
            if (nums[j] % 2 == 1) odd++;
            if (odd == k) count++;
            else if (odd > k) break;
        }
    }
    return count;
}
```

**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 2 — Reduce to Binary Subarrays With Sum

**Insight from brute.** Map `odd → 1`, `even → 0`. Now the problem is: count subarrays with **sum exactly k** on a binary array — which is exactly [Binary Subarrays With Sum](/problems/binary-subarrays-with-sum). Use the `atMost` trick.

```java
int numberOfSubarrays(int[] nums, int k) {
    return atMost(nums, k) - atMost(nums, k - 1);
}
int atMost(int[] nums, int k) {
    if (k < 0) return 0;
    int left = 0, odd = 0, res = 0;
    for (int right = 0; right < nums.length; right++) {
        if (nums[right] % 2 == 1) odd++;
        while (odd > k) if (nums[left++] % 2 == 1) odd--;
        res += right - left + 1;
    }
    return res;
}
```

<CodeTrace
  title="atMost(k=3) — nums=[1,1,2,1,1]"
  :values="['1','1','2','1','1']"
  :windowKeys="['left','right']"
  :cellWidth="36"
  :steps='[
    { pointers: { left: 0, right: 2 }, vars: { odd: 2, res: 6 }, note: "up to 3 subarrays end at 2 (odd=2 ≤ 3)" },
    { pointers: { left: 0, right: 3 }, vars: { odd: 3, res: 10 }, note: "odd=3 ≤ 3 — 4 subarrays end here" },
    { pointers: { left: 0, right: 4 }, vars: { odd: 4 }, note: "odd=4 > 3 → shrink" },
    { pointers: { left: 1, right: 4 }, vars: { odd: 3, res: 14 }, note: "shrunk past first 1; atMost(3)=14" }
  ]'
/>

Then `atMost(3) - atMost(2) = 14 - 12 = 2`.

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Approach 3 — Count-of-prefix-sums with prefix map (O(n) space)

**Insight.** Prefix-count of odd numbers up to index `i`. Subarray `[i+1, j]` has k odd iff `oddPref[j+1] - oddPref[i] = k`. Same hash-map trick as [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k).

```java
int numberOfSubarraysPS(int[] nums, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    cnt.put(0, 1);
    int odd = 0, res = 0;
    for (int x : nums) {
        odd += x & 1;
        res += cnt.getOrDefault(odd - k, 0);
        cnt.merge(odd, 1, Integer::sum);
    }
    return res;
}
```

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="count-number-of-nice-subarrays" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every subarray | O(n²) | O(1) | baseline |
| Two `atMost` windows | **O(n)** | **O(1)** | optimum |
| Prefix hash map | O(n) | O(n) | acceptable — same as SSEqK |

## When to use which

- **"Exactly k of X" over non-negative counts** → `atMost` trick.
- **Arbitrary values (negatives, etc.)** → prefix + hash map (works for any).
- **"At most k"** → single sliding window.
- **"Return the subarrays"** → prefix + indices; loses O(1) space.

<AiCompanion problem-slug="count-number-of-nice-subarrays" pattern-hint="sliding window" />

## Related problems

- [Binary Subarrays With Sum](/problems/binary-subarrays-with-sum) — identical mechanics
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers) — same atMost pattern for distinct count
- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k) — hash-map sibling

<FeedbackWidget problem-slug="count-number-of-nice-subarrays" />

<RelatedProblems problems="subarray-product-less-than-k::Subarray Product Less Than K|minimum-window-substring::Minimum Window Substring|find-all-anagrams-in-a-string::Find All Anagrams In A String" />
