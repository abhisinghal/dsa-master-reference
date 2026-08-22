# Bit Manipulation — Missing Number

*[↗ LeetCode: Missing Number](https://leetcode.com/problems/missing-number/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Given `nums` containing `n` distinct numbers from `[0, n]`, return the missing one.

**Example** — `nums=[3,0,1]` → `2`

## Approach 1 — Sort or hash set

O(n log n) or O(n) with O(n) space.

## Approach 2 — Gauss sum

Expected sum `n(n+1)/2` minus actual sum.

## Approach 3 — XOR fold

`missing = 0 ^ 1 ^ … ^ n ^ nums[0] ^ … ^ nums[n-1]` — every present index cancels with its own value.



```java
int missingNumber(int[] nums) {
    int x = nums.length;
    for (int i = 0; i < nums.length; i++) x ^= i ^ nums[i];
    return x;
}
```



**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Single Number](/problems/bit-manip-single-number) — XOR canonical
- [Find the Difference](/problems/find-the-difference) — sibling
- [Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)
