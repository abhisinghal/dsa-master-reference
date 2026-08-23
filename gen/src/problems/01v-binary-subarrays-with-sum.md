# Sliding Window — Binary Subarrays With Sum

*[↗ LeetCode: Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

<CompanyTags companies="Google, Amazon, Meta" />

Given a binary array `nums` and integer `goal`, return the number of non-empty contiguous subarrays with sum equal to `goal`.

**Example 1** — `nums = [1,0,1,0,1], goal = 2` → `4` (subarrays: `[1,0,1]`, `[1,0,1,0]`, `[0,1,0,1]`, `[1,0,1]`)
**Example 2** — `nums = [0,0,0,0,0], goal = 0` → `15` (every subarray sums to 0)
**Example 3** — `nums = [1,1,1], goal = 3` → `1`

**Constraints** — `1 ≤ n ≤ 3 · 10⁴`; `nums[i] ∈ {0, 1}`; `0 ≤ goal ≤ n`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="binary-subarrays-with-sum" /> <Bookmark problem-slug="binary-subarrays-with-sum" />

<InterviewTimer problem-slug="binary-subarrays-with-sum" />



## Approach 1 — Every subarray

**Intuition.** For each `[i, j]`, sum bits; increment on match.

```java
int numSubarraysWithSumBrute(int[] nums, int goal) {
    int n = nums.length, count = 0;
    for (int i = 0; i < n; i++) {
        int s = 0;
        for (int j = i; j < n; j++) {
            s += nums[j];
            if (s == goal) count++;
            else if (s > goal) break;
        }
    }
    return count;
}
```

**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 2 — Prefix-sum hash map (works with any integers)

**Insight from brute.** Precompute prefix sums. Subarray `[i, j]` has sum `goal` iff `pref[j+1] - pref[i] = goal` → count for each `j`, how many earlier prefixes equal `pref[j+1] - goal`. Same recipe as [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k).

```java
int numSubarraysWithSumPS(int[] nums, int goal) {
    Map<Integer, Integer> cnt = new HashMap<>();
    cnt.put(0, 1);
    int pref = 0, res = 0;
    for (int x : nums) {
        pref += x;
        res += cnt.getOrDefault(pref - goal, 0);
        cnt.merge(pref, 1, Integer::sum);
    }
    return res;
}
```

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Approach 3 — `atMost(goal) − atMost(goal−1)` sliding window

**Insight from prefix-sum.** With **non-negative** integers, sums are monotone in window size — a plain sliding-window computes `atMost(goal)` in O(n) and O(1) space. Subtract `atMost(goal-1)` to get "exactly goal".

```java
int numSubarraysWithSum(int[] nums, int goal) {
    return atMost(nums, goal) - atMost(nums, goal - 1);
}
int atMost(int[] nums, int goal) {
    if (goal < 0) return 0;
    int left = 0, sum = 0, res = 0;
    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];
        while (sum > goal) sum -= nums[left++];
        res += right - left + 1;
    }
    return res;
}
```

<CodeTrace
  title="atMost(goal=2) — nums=[1,0,1,0,1]"
  :values="['1','0','1','0','1']"
  :windowKeys="['left','right']"
  :cellWidth="36"
  :steps='[
    { pointers: { left: 0, right: 1 }, vars: { sum: 1, res: 3 }, note: "subarrays ending at 0 and 1 all valid" },
    { pointers: { left: 0, right: 2 }, vars: { sum: 2, res: 6 }, note: "sum=2 ≤ goal — count 3 more" },
    { pointers: { left: 0, right: 4 }, vars: { sum: 3 }, note: "sum=3 > 2 → shrink" },
    { pointers: { left: 3, right: 4 }, vars: { sum: 1, res: 12 }, note: "final atMost(2)=12; atMost(1)=8 → answer 4" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="binary-subarrays-with-sum" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every subarray | O(n²) | O(1) | baseline |
| Prefix-sum hash map | O(n) | O(n) | works even for negatives |
| Two `atMost` windows | **O(n)** | **O(1)** | optimum for non-negatives |

## When to use which

- **Binary / non-negative array + exact sum** → `atMost` sliding trick.
- **Arbitrary integers (negatives allowed)** → prefix-sum hash map — sliding window breaks.
- **Longest / shortest subarray with sum X (not count)** → different template — see [Minimum Size Subarray Sum](/problems/minimum-size-subarray-sum).
- **Return subarrays themselves** → prefix-sum + track indices, or DP; loses O(n).

<AiCompanion problem-slug="binary-subarrays-with-sum" pattern-hint="sliding window" />

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k) — arbitrary integers
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers) — same `atMost` trick
- [Count Number of Nice Subarrays](/problems/count-number-of-nice-subarrays) — same trick with odd counts

<FeedbackWidget problem-slug="binary-subarrays-with-sum" />

<RelatedProblems problems="fruit-into-baskets::Fruit Into Baskets|longest-substring-with-at-most-k-distinct-characters::Longest Substring With At Most K Distinct Characters|subarray-product-less-than-k::Subarray Product Less Than K" />
