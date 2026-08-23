# Bit Manipulation — Subsets

*[↗ LeetCode: Subsets](https://leetcode.com/problems/subsets/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/bit-manip)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft, Bloomberg, Apple" /&gt;

Given distinct integers `nums`, return all possible subsets (the power set).

**Example 1** — `nums=[1,2,3]` → `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`
**Example 2** — `nums=[0]` → `[[],[0]]`

**Constraints** — `1 ≤ n ≤ 10`.


&lt;Hints
  hint1="Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k."
  hint2="For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen."
  hint3="For ’find the unique/missing’: XOR the whole array with 0..n; pairs cancel, missing survives."
/&gt;
---

## Approach 1 — Backtracking

Standard include/exclude recursion. O(2ⁿ · n).

## Approach 2 — Iterative expansion

For each element, double the current answer by appending it to every existing subset.



```java
List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    out.add(new ArrayList<>());
    for (int x : nums) {
        int sz = out.size();
        for (int i = 0; i < sz; i++) {
            List<Integer> next = new ArrayList<>(out.get(i));
            next.add(x);
            out.add(next);
        }
    }
    return out;
}
```



## Approach 3 — Bitmask enumeration (canonical)

**Insight.** Each subset corresponds to a bit pattern of length n. Iterate `mask` from 0 to 2ⁿ-1.



```java
List<List<Integer>> subsetsBM(int[] nums) {
    int n = nums.length;
    List<List<Integer>> out = new ArrayList<>();
    for (int mask = 0; mask < 1 << n; mask++) {
        List<Integer> sub = new ArrayList<>();
        for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) sub.add(nums[i]);
        out.add(sub);
    }
    return out;
}
```



<CodeTrace
  title="Bitmask — nums=[1,2,3]"
  :values="['1','2','3']"
  :windowKeys="['mask']"
  :cellWidth="34"
  :steps='[
    { pointers: { mask: 0 }, vars: { bin: "000", subset: "[]" }, note: "" },
    { pointers: { mask: 5 }, vars: { bin: "101", subset: "[1,3]" }, note: "" },
    { pointers: { mask: 7 }, vars: { bin: "111", subset: "[1,2,3]" }, note: "" }
  ]'
/>

**Complexity** — Time **O(2ⁿ · n)**; Space **O(2ⁿ · n)** for output.

---

## Try it yourself

<JavaRunner problem-slug="subsets" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Backtracking | O(2ⁿ · n) | O(n) recursion | canonical |
| Iterative expansion | O(2ⁿ · n) | O(2ⁿ · n) | elegant |
| Bitmask | **O(2ⁿ · n)** | O(2ⁿ · n) | polish |

## When to use which

- **All subsets** → any of the three.
- **All subsets with duplicate elements** → sort + skip; see [Subsets II](/problems/subsets-ii).
- **Only subsets of size k** → recurse with size arg; or DP.

## Related problems

- [Subsets II](/problems/subsets-ii) — with duplicates
- [Combination Sum](https://leetcode.com/problems/combination-sum/)
- [Permutations](/problems/permutations)