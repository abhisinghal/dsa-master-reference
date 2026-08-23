# Hashing — Maximum Product Subarray

*[↗ LeetCode: Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

<CompanyTags companies="Meta, Amazon, LinkedIn" />

Return max product of a contiguous subarray.

**Example 1** — `nums=[2,3,-2,4]` → `6`
**Example 2** — `nums=[-2,0,-1]` → `0`

**Constraints** — `1 ≤ n ≤ 2·10⁴`.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/>
---

## Approach 1 — Try every subarray

O(n²). Baseline.

## Approach 2 — Track min and max ending at i (canonical)

**Insight.** A negative flips min ↔ max on the next step. Maintain both.

```java
int maxProduct(int[] nums) {
    int maxE = nums[0], minE = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        int nMax = Math.max(x, Math.max(maxE * x, minE * x));
        int nMin = Math.min(x, Math.min(maxE * x, minE * x));
        maxE = nMax; minE = nMin;
        best = Math.max(best, maxE);
    }
    return best;
}
```

<CodeTrace
  title="Min/Max — nums=[2,3,-2,4]"
  :values="['2','3','-2','4']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { maxE: 2, minE: 2 }, note: "" },
    { pointers: { i: 1 }, vars: { maxE: 6, minE: 3, best: 6 }, note: "" },
    { pointers: { i: 2 }, vars: { maxE: -2, minE: -12 }, note: "flip" },
    { pointers: { i: 3 }, vars: { maxE: 4, best: 6 }, note: "" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="maximum-product-subarray" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| All subarrays | O(n²) | O(1) | baseline |
| Min/Max tracking | **O(n)** | O(1) | canonical |

## When to use which

- **"Product with negatives"** → track both.
- **"Only positives"** → simple running product.
- **"Return the subarray"** → track indices.

<AiCompanion problem-slug="maximum-product-subarray" pattern-hint="hashing" />

## Related problems

- [Maximum Subarray (Kadane)](/problems/maximum-subarray)
- [Maximum Sum Circular Subarray](/problems/maximum-sum-circular-subarray)