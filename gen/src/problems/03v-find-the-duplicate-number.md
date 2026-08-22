# Fast/Slow — Find the Duplicate Number

*[↗ LeetCode: Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/fast-slow)

Given `nums` of length `n+1` with values in `[1, n]`, exactly one value appears more than once. Return it. **O(1) space** required (nums cannot be modified).

**Example** — `nums=[1,3,4,2,2]` → `2`

---

## Approach 1 — Sort

```java
int findDuplicateSort(int[] a) {
    Arrays.sort(a);                                        // NOT allowed by follow-up (modifies input)
    for (int i = 1; i < a.length; i++) if (a[i] == a[i - 1]) return a[i];
    return -1;
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)** but modifies input.

## Approach 2 — Hash set

**Complexity** — Time **O(n)**; Space **O(n)**. Fails the O(1) bar.

## Approach 3 — Floyd on the "next=nums[i]" functional graph

**Insight.** Treat the array as a linked list where `next(i) = nums[i]`. Since the domain is `[1..n]` and the length is `n+1`, at least two indices map to the same value → there's a cycle. The cycle entry IS the duplicate.

```java
int findDuplicate(int[] a) {
    int slow = a[0], fast = a[0];
    do { slow = a[slow]; fast = a[a[fast]]; } while (slow != fast);
    slow = a[0];
    while (slow != fast) { slow = a[slow]; fast = a[fast]; }
    return slow;
}
```

<CodeTrace
  title="Floyd on next=nums[i] — nums=[1,3,4,2,2]"
  :values="[1,3,4,2,2]"
  :windowKeys="['slow','fast']"
  :cellWidth="42"
  :steps='[
    { pointers: { slow: 1, fast: 1 }, vars: { }, note: "start slow=fast=nums[0]=1" },
    { pointers: { slow: 3, fast: 2 }, vars: { }, note: "slow=nums[1]=3, fast=nums[nums[1]]=nums[3]=2" },
    { pointers: { slow: 2, fast: 3 }, vars: { }, note: "slow=nums[3]=2, fast=nums[nums[2]]=nums[4]=2, then nums[2]=4… careful trace" },
    { pointers: { slow: 2, fast: 2 }, vars: { }, note: "meeting → cycle proven", added: [2] },
    { pointers: { slow: 2, fast: 2 }, vars: { phase: "entry" }, note: "reset slow=nums[0]=1; walk both 1x → meet at 2 = duplicate", added: [2] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Optimal.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Sort | O(n log n) | O(1) modifies |
| Hash set | O(n) | O(n) |
| Floyd | **O(n)** | **O(1)** |

## Related problems

- [Linked List Cycle II](/problems/fast-slow-linked-list-cycle-ii) — same algorithm on an explicit linked list
- [Missing Number](https://leetcode.com/problems/missing-number/) — XOR or Gauss sum
- [Set Mismatch](https://leetcode.com/problems/set-mismatch/) — find duplicate + missing
