# Two Pointers — 3Sum Closest

*[↗ LeetCode: 3Sum Closest](https://leetcode.com/problems/3sum-closest/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Find three numbers whose sum is closest to `target`; return the sum.

---

## Approach 1 — Triple loop O(n³)

---

## Approach 2 — Sort + two-pointer
**Insight.** Sort. For each `i`, use two pointers on `[i+1, n-1]`; move whichever pointer reduces distance to target.



```java
int threeSumClosest(int[] nums, int target) {
    Arrays.sort(nums);
    int best = nums[0] + nums[1] + nums[2];
    for (int i = 0; i < nums.length - 2; i++) {
        int l = i + 1, r = nums.length - 1;
        while (l < r) {
            int s = nums[i] + nums[l] + nums[r];
            if (Math.abs(s - target) < Math.abs(best - target)) best = s;
            if (s < target) l++;
            else if (s > target) r--;
            else return s;
        }
    }
    return best;
}
```



**Complexity** — Time **O(n²)**; Space **O(1)** extra.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Triple loop O(n³) | — | — | baseline |
| Sort + two-pointer | O(n²) | O(1) | optimum |

## When to use which

- **State it for signal** → Triple loop O(n³) (—). Correct baseline; call it out then move on.
- **Ship this** → Sort + two-pointer (O(n²), O(1)). Expected optimum in interview.

## Related problems

- [3Sum](/problems/3sum)
- [3Sum Smaller](/problems/3sum-smaller)
- [4Sum](/problems/4sum)
