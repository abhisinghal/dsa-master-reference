# Hashing — 3Sum

*[↗ LeetCode: 3Sum](https://leetcode.com/problems/3sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

Find all unique triplets summing to 0.

---

## Approach 1 — Triple loop + set for dedup
O(n³).

---

## Approach 2 — Sort + two-pointer
**Insight.** Sort. Fix `i`; two pointers on `[i+1, n-1]` search for `-nums[i]`. Skip duplicates at all 3 levels to avoid emitting repeats.



```java
List<List<Integer>> threeSum(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> out = new ArrayList<>();
    for (int i = 0; i < nums.length - 2; i++) {
        if (nums[i] > 0) break;
        if (i > 0 && nums[i] == nums[i - 1]) continue;
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



**Complexity** — Time **O(n²)**; Space **O(1)** extra.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Triple loop + set for dedup | O(n³) | — | baseline |
| Sort + two-pointer | O(n²) | O(1) | optimum |

## When to use which

- **State it for signal** → Triple loop + set for dedup (O(n³)). Correct baseline; call it out then move on.
- **Ship this** → Sort + two-pointer (O(n²), O(1)). Expected optimum in interview.

## Related problems

- [3Sum Closest](/problems/3sum-closest)
- [3Sum Smaller](/problems/3sum-smaller)
- [4Sum](/problems/4sum)
- [Two Sum](/problems/hashing-two-sum) — the seed
