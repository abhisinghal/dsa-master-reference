# Sliding Window — Trapping Rain Water

*[↗ LeetCode: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/two-pointers)

Given heights, compute total water trapped.

## Approach 1 — Precompute leftMax, rightMax

For each i, water = min(leftMax[i], rightMax[i]) - h[i]. **O(n)** time, **O(n)** space.

## Approach 2 — Opposing two-pointer, no arrays

**Insight.** Move whichever pointer has the smaller wall — the water level at that pointer is bounded by whichever *known* max is smaller.



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



**Complexity** — Time **O(n)**; Space **O(1)**.

## Approach 3 — Monotonic decreasing stack

Push indices while heights decrease; on rise, pop the "bottom" and compute water in the pocket bounded by new top and current bar. Same **O(n)**, different mental model — useful teaching link to Largest Rectangle.

## Related problems

- [Trapping Rain Water II](/problems/trapping-rain-water-ii) — 2D min-heap
- [Container With Most Water](/problems/two-pointers-container-with-most-water)
- [Largest Rectangle in Histogram](/problems/largest-rectangle-in-histogram)
