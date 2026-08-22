# Fast/Slow — Happy Number

*[↗ LeetCode: Happy Number](https://leetcode.com/problems/happy-number/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/fast-slow)

Starting from `n`, repeatedly replace with the sum of squares of its digits. Return `true` if it reaches `1`; otherwise it enters a cycle → `false`.

**Example 1** — `n=19` → `true` (`19→82→68→100→1`)
**Example 2** — `n=2` → `false` (loops)

---

## Approach 1 — Hash set



```java
boolean isHappyHash(int n) {
    Set<Integer> seen = new HashSet<>();
    while (n != 1 && seen.add(n)) n = next(n);
    return n == 1;
}
int next(int n) { int s = 0; while (n > 0) { int d = n % 10; s += d * d; n /= 10; } return s; }
```



**Complexity** — Time **O(log n)** per step, converges quickly; Space **O(k)** for seen values.

## Approach 2 — Floyd on the digit-square sequence

**Insight.** The sequence `n → next(n) → next(next(n)) → …` is a functional graph. A non-happy number lands in a cycle; a happy number lands at `1` (a fixed point). Floyd detects both — cycle means unhappy, meeting at `1` means happy.



```java
boolean isHappy(int n) {
    int slow = n, fast = n;
    do {
        slow = next(slow);
        fast = next(next(fast));
    } while (slow != fast);
    return slow == 1;
}
```



<CodeTrace
  title="Floyd on happy sequence — n=19 → 82 → 68 → 100 → 1"
  :values="[19,82,68,100,1]"
  :windowKeys="['slow','fast']"
  :cellWidth="46"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: { }, note: "start at 19" },
    { pointers: { slow: 1, fast: 2 }, vars: { }, note: "slow=82, fast=68" },
    { pointers: { slow: 2, fast: 4 }, vars: { }, note: "slow=68, fast=1" },
    { pointers: { slow: 4, fast: 4 }, vars: { }, note: "meet at 1 → happy!", added: [4] }
  ]'
/>

**Complexity** — Time **O(log n)** per next; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Hash set | O(log n) per step | O(k) |
| Floyd | O(log n) per step | **O(1)** |

## Related problems

- [Linked List Cycle](/problems/linked-list-cycle) — same technique on linked list
- [Find the Duplicate Number](/problems/find-the-duplicate-number) — Floyd on `next = nums[i]`
