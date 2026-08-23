# Hashing — Two Sum II (Input Array Is Sorted)

*[↗ LeetCode: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Sorted array; return 1-indexed pair summing to target.

**Example 1** — `numbers=[2,7,11,15], target=9` → `[1,2]`
**Example 2** — `numbers=[2,3,4], target=6` → `[1,3]`
**Example 3** — `numbers=[-1,0], target=-1` → `[1,2]`

**Constraints** — `2 ≤ n ≤ 3·10⁴`.

---

## Approach 1 — Hash-map

Ignores sortedness. O(n) time O(n) space.

## Approach 2 — Opposing two-pointer (canonical)

**Insight.** Sum monotone in pointer movement — deterministic.



```java
int[] twoSum(int[] nums, int target) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        int s = nums[l] + nums[r];
        if (s == target) return new int[]{l + 1, r + 1};
        if (s < target) l++; else r--;
    }
    return new int[]{-1, -1};
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Hash map | O(n) | O(n) | works but wastes sort |
| Opposing 2p | **O(n)** | **O(1)** | canonical |

## When to use which

- **Sorted input** → 2p every time.
- **Not sorted** → hash.
- **k-Sum on sorted** → recursion with 2p base.

## Related problems

- [Two Sum](/problems/hashing-two-sum)
- [3Sum](/problems/3sum)
