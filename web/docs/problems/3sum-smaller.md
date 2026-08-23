# Two Pointers — 3Sum Smaller

*[↗ LeetCode: 3Sum Smaller](https://leetcode.com/problems/3sum-smaller/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Count triplets `(i, j, k)` with `i < j < k` and `nums[i] + nums[j] + nums[k] < target`.

**Example 1** — `nums=[-2,0,1,3], target=2` → `2`
**Example 2** — `nums=[], target=0` → `0`

**Constraints** — `0 ≤ n ≤ 3500`.

---

## Approach 1 — Triple loop

O(n³).

## Approach 2 — Sort + counting two-pointer (canonical)

**Insight.** After sorting, for each `i` and left pointer `l`, if `nums[i]+nums[l]+nums[r] < target`, then **every** `k` in `(l, r]` also satisfies it — add `r - l`.



```java
int threeSumSmaller(int[] nums, int target) {
    Arrays.sort(nums);
    int count = 0;
    for (int i = 0; i < nums.length - 2; i++) {
        int l = i + 1, r = nums.length - 1;
        while (l < r) {
            if (nums[i] + nums[l] + nums[r] < target) { count += r - l; l++; }
            else r--;
        }
    }
    return count;
}
```



**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Triple loop | O(n³) | O(1) | baseline |
| Sort + counting | **O(n²)** | O(1) | canonical |

## When to use which

- **"Count triplets &lt; target"** → sort + counting shortcut.
- **"Return the triplets"** → enumerate; loses O(1).

## Related problems

- [3Sum](/problems/3sum)
- [3Sum Closest](/problems/3sum-closest)
