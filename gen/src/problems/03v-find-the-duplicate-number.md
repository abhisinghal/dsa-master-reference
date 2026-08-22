# Fast &amp; Slow — Find the Duplicate Number

*[↗ LeetCode: Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/fast-slow)

Given an array `nums` of `n + 1` integers where each is in `[1, n]`, there is exactly one duplicate. Return it. **Constraints**: don't modify `nums`; use **O(1)** extra space.

**Example 1** — `nums = [1,3,4,2,2]` → `2`
**Example 2** — `nums = [3,1,3,4,2]` → `3`
**Example 3** — `nums = [1,1]` → `1`

**Constraints** — `1 ≤ n ≤ 10⁵`; `1 ≤ nums[i] ≤ n`.

---

## Approach 1 — Sort

O(n log n) time, O(1) if sort in place — but modifies input (disallowed).

## Approach 2 — Hash set

O(n) time, O(n) space — disallowed by spec.

## Approach 3 — Binary search on value

**Intuition.** Binary search on `[1, n]` for the duplicate. For mid `m`, count how many nums are ≤ m. If count > m, duplicate is in `[1, m]`; else `[m+1, n]`.

```java
int findDuplicateBS(int[] nums) {
    int lo = 1, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int cnt = 0;
        for (int x : nums) if (x <= mid) cnt++;
        if (cnt > mid) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Approach 4 — Floyd's tortoise/hare on implicit list (canonical)

**Insight.** Treat `nums[i]` as "next(i)". Since every value is in `[1, n]` and there are `n+1` positions, this functional graph *must* contain a cycle, and the cycle **entry** is the duplicate value.

**Why entry = duplicate.** Two different indices `i1 ≠ i2` both point to the duplicate → the duplicate is the "merge point" of two paths in the functional graph, i.e., the cycle entry.

Same Floyd's algorithm as [Linked List Cycle II](/problems/fast-slow-linked-list-cycle-ii): find meeting point; reset one pointer to start; walk both at speed 1; they meet at the cycle entry.

```java
int findDuplicate(int[] nums) {
    int slow = nums[0], fast = nums[0];
    do { slow = nums[slow]; fast = nums[nums[fast]]; } while (slow != fast);
    slow = nums[0];
    while (slow != fast) { slow = nums[slow]; fast = nums[fast]; }
    return slow;
}
```

<CodeTrace
  title="Floyd — nums=[1,3,4,2,2]"
  :values="['1','3','4','2','2']"
  :windowKeys="['slow','fast']"
  :cellWidth="38"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: { s: 1, f: 1 }, note: "both at nums[0]=1" },
    { pointers: { slow: 1, fast: 2 }, vars: { s: 3, f: 4 }, note: "slow one step, fast two" },
    { pointers: { slow: 2, fast: 2 }, vars: { s: 4, f: 2 }, note: "wait — trace this carefully" },
    { pointers: { slow: 3, fast: 3 }, vars: { s: 2, f: 2, met: true }, note: "meeting point; reset slow to 0" },
    { pointers: { slow: 3, fast: 3 }, vars: { entry: 2 }, note: "walk both at speed 1 → meet at 2 = duplicate" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort | O(n log n) | O(1) | modifies input |
| Hash set | O(n) | O(n) | violates space limit |
| Binary search on value | O(n log n) | O(1) | acceptable |
| Floyd's on implicit list | **O(n)** | **O(1)** | canonical for the constraints |

## When to use which

- **Constraint: don't modify + O(1) space** → Floyd's.
- **"Multiple duplicates possible"** → hash-based counting or bit manipulation.
- **"Return every duplicate"** → mark visited via `nums[abs(v)-1] *= -1` (modifies input).
- **Generalization: "smallest missing positive"** → different problem (in-place index marking).

## Related problems

- [Linked List Cycle II](/problems/fast-slow-linked-list-cycle-ii) — same Floyd's algorithm
- [Missing Number](/problems/missing-number) — one missing, all distinct — XOR trick
- [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) — index-marking
