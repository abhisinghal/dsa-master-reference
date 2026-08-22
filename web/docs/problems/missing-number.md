# Bit Manipulation — Missing Number

*[↗ LeetCode: Missing Number](https://leetcode.com/problems/missing-number/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Given `nums` containing `n` distinct numbers from `[0, n]`, return the missing one.

**Example** — `nums=[3,0,1]` → `2`

---

## Approach 1 — Sort or hash set
O(n log n) or O(n) with O(n) space.

---

## Approach 2 — Gauss sum
Expected sum `n(n+1)/2` minus actual sum.

---

## Approach 3 — XOR fold
`missing = 0 ^ 1 ^ … ^ n ^ nums[0] ^ … ^ nums[n-1]` — every present index cancels with its own value.



```java
int missingNumber(int[] nums) {
    int x = nums.length;
    for (int i = 0; i < nums.length; i++) x ^= i ^ nums[i];
    return x;
}
```




<CodeTrace
  title="XOR fold"
  :values="['3', '0', '1']"
  :windowKeys="['l','r']"
  :cellWidth="34"
  :steps='[
    { pointers: { l: 0, r: 0 }, vars: { phase: "start" }, note: "Both pointers at the start." },
    { pointers: { l: 0, r: 0 }, vars: { phase: "extend" }, note: "Right pointer extends; maintain the invariant." },
    { pointers: { l: 0, r: 2 }, vars: { phase: "finalize" }, note: "Window converged; produce the answer." }
  ]'
/>


**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort or hash set | O(n log n) | O(n) | baseline |
| Gauss sum | — | — | improved |
| XOR fold | O(n) | O(1) | optimum |

## When to use which

- **State it for signal** → Sort or hash set (O(n log n)). Correct baseline; call it out then move on.
- **Intermediate refinement** → Gauss sum (—).
- **Ship this** → XOR fold (O(n), O(1)). Expected optimum in interview.

## Related problems

- [Single Number](/problems/bit-manip-single-number) — XOR canonical
- [Find the Difference](/problems/find-the-difference) — sibling
- [Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)
