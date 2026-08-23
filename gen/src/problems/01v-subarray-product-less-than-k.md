# Sliding Window — Subarray Product Less Than K

*[↗ LeetCode: Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Given a positive-int array `nums` and integer `k`, return the number of contiguous subarrays whose product is strictly less than `k`.

**Example 1** — `nums = [10,5,2,6], k = 100` → `8` (subarrays: `[10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6]`)
**Example 2** — `nums = [1,2,3], k = 0` → `0` (no positive product can be `< 0`)
**Example 3** — `nums = [1,1,1], k = 2` → `6`

**Constraints** — `1 ≤ n ≤ 3 · 10⁴`; `1 ≤ nums[i] ≤ 1000`; `0 ≤ k ≤ 10⁶`. **All values positive.**


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

## Approach 1 — Every subarray

**Intuition.** For each `[i, j]`, compute product; if `< k`, increment.

```java
int numSubarrayProductLessThanKBrute(int[] nums, int k) {
    int n = nums.length, count = 0;
    for (int i = 0; i < n; i++) {
        long prod = 1;
        for (int j = i; j < n; j++) {
            prod *= nums[j];
            if (prod < k) count++;
            else break;
        }
    }
    return count;
}
```

**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 2 — Sliding window with running product

**Insight from brute.** Products are monotone with positive values. Extend `right`; shrink `left` while `prod ≥ k`. Every subarray ending at `right` with left ∈ `[currLeft, right]` contributes `(right - left + 1)` new subarrays.

**Trap** — Early-return `k ≤ 1`: no product of positives is `< 1`.

```java
int numSubarrayProductLessThanK(int[] nums, int k) {
    if (k <= 1) return 0;
    long prod = 1;
    int count = 0, left = 0;
    for (int right = 0; right < nums.length; right++) {
        prod *= nums[right];
        while (prod >= k) prod /= nums[left++];
        count += right - left + 1;
    }
    return count;
}
```

<CodeTrace
  title="Sliding — nums=[10,5,2,6], k=100"
  :values="['10','5','2','6']"
  :windowKeys="['left','right']"
  :cellWidth="36"
  :steps='[
    { pointers: { left: 0, right: 1 }, vars: { prod: 50, count: 3 }, note: "[10], [5], [10,5]" },
    { pointers: { left: 0, right: 2 }, vars: { prod: 100 }, note: "prod=100 ≥ 100 → shrink" },
    { pointers: { left: 1, right: 2 }, vars: { prod: 10, count: 5 }, note: "[5], [2], [5,2] added — count=5" },
    { pointers: { left: 1, right: 3 }, vars: { prod: 60, count: 8 }, note: "[6], [2,6], [5,2,6] — count=8" }
  ]'
/>

**Complexity** — Time **O(n)** — each index enters/leaves once; Space **O(1)**.

---

## Approach 3 — Prefix log-sum + binary search (interview polish)

**Insight from sliding.** Log-transforms products into sums: `log(prod) = Σ log(nums[i])`. Now the problem becomes "count sublists with prefix-log-sum difference < log k" — solvable via binary search on the prefix array. Rarely needed in practice, but shows the sum-log-product bridge.

**Complexity** — Time **O(n log n)**; Space **O(n)**. Suboptimal — the sliding window wins.

---

## Try it yourself

<JavaRunner problem-slug="subarray-product-less-than-k" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every subarray | O(n²) | O(1) | baseline |
| Sliding window | **O(n)** | O(1) | expected optimum |
| Log + prefix + BS | O(n log n) | O(n) | curiosity — sum-log-product bridge |

## When to use which

- **Standard answer** → sliding window.
- **"What if nums[i] can be 0?"** → sliding breaks (0 zeros the product); split by zeros or use the log-sum + BS approach with `log(0) = -∞`.
- **"What if nums[i] can be negative?"** → both products and logs break; needs sign-tracking (see [Maximum Product Subarray](/problems/maximum-product-subarray)).
- **"Return the subarrays themselves"** → enumerate during the slide; loses the compact O(n) counting.

<AiCompanion problem-slug="subarray-product-less-than-k" pattern-hint="sliding window" />

## Related problems

- [Maximum Product Subarray](/problems/maximum-product-subarray) — signed variant
- [Binary Subarrays With Sum](/problems/binary-subarrays-with-sum) — sibling with `atMost` trick
- [Count Number of Nice Subarrays](/problems/count-number-of-nice-subarrays) — sibling
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers)

<FeedbackWidget problem-slug="subarray-product-less-than-k" />
