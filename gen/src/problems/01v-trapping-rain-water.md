# Sliding Window — Trapping Rain Water

*[↗ LeetCode: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Meta, Google, Amazon, Microsoft, Apple, Bloomberg, Uber" />

Given `n` non-negative integers representing an elevation map, compute how much water it traps after raining.

**Example 1** — `height=[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`
**Example 2** — `height=[4,2,0,3,2,5]` → `9`

**Constraints** — `1 ≤ n ≤ 2·10⁴`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="trapping-rain-water" />


## Approach 1 — Precompute leftMax, rightMax

For each i, water = `min(leftMax[i], rightMax[i]) - h[i]`. **O(n)** time, **O(n)** space.

## Approach 2 — Opposing two-pointer (canonical)

**Insight.** Move whichever pointer has the smaller wall — the water level there is bounded by the smaller *known* max.

```java
int trap(int[] h) {
    int l = 0, r = h.length - 1, lMax = 0, rMax = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            lMax = Math.max(lMax, h[l]);
            water += lMax - h[l];
            l++;
        } else {
            rMax = Math.max(rMax, h[r]);
            water += rMax - h[r];
            r--;
        }
    }
    return water;
}
```

<CodeTrace
  title="Two-pointer — height=[0,1,0,2,1,0,1,3,2,1,2,1]"
  :values="['0','1','0','2','1','0','1','3','2','1','2','1']"
  :windowKeys="['l','r']"
  :cellWidth="26"
  :steps='[
    { pointers: { l: 2, r: 11 }, vars: { lMax: 1, water: 1 }, note: "trapped 1 at idx 2" },
    { pointers: { l: 5, r: 11 }, vars: { lMax: 2, water: 4 }, note: "accumulating" },
    { pointers: { l: 7, r: 11 }, vars: { lMax: 3, water: 6 }, note: "final = 6" }
  ]'
/>

## Approach 3 — Monotonic decreasing stack

Push indices while heights decrease; on rise, pop the "bottom" and compute water in the pocket. Same O(n).

**Complexity** — Time **O(n)**; Space **O(1)** for 2p, **O(n)** for arrays/stack.

---

## Try it yourself

<JavaRunner problem-slug="trapping-rain-water" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| leftMax + rightMax arrays | O(n) | O(n) | first-pass answer |
| Opposing 2p | **O(n)** | **O(1)** | canonical |
| Monotonic stack | O(n) | O(n) | teaching link |

## When to use which

- **Standard** → opposing 2p (elegant, O(1) space).
- **Interviewer wants explicit reasoning** → precompute arrays.
- **2D grid** → [Trapping Rain Water II](/problems/trapping-rain-water-ii) — min-heap.

<AiCompanion problem-slug="trapping-rain-water" pattern-hint="sliding window" />

## Related problems

- [Trapping Rain Water II](/problems/trapping-rain-water-ii)
- [Container With Most Water](/problems/two-pointers-container-with-most-water)
- [Largest Rectangle in Histogram](/problems/largest-rectangle-in-histogram)

<FeedbackWidget problem-slug="trapping-rain-water" />
