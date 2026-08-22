# Hashing — Longest Consecutive Sequence

*[↗ LeetCode: Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

Given unsorted `nums`, return length of longest run of consecutive integers. **O(n).**

## Approach 1 — Sort

O(n log n). Rejected by spec.

## Approach 2 — Set + only start from sequence heads

**Insight.** Put all nums in a `HashSet`. Iterate; **only start counting from `x` if `x - 1` is absent** (so `x` is a sequence head). Then extend forward. Each element is visited by the inner loop at most once → O(n) total.



```java
int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int x : nums) set.add(x);
    int best = 0;
    for (int x : set) {
        if (set.contains(x - 1)) continue;
        int len = 1;
        while (set.contains(x + len)) len++;
        best = Math.max(best, len);
    }
    return best;
}
```



**Complexity** — Time **O(n)** average; Space **O(n)**.

**Trap.** Without the "sequence head" check, you'd re-walk the same run n times → O(n²).

**Union-Find alternative.** Union x with x±1 whenever both present; track max component size.

## Related problems

- [Longest Substring Without Repeating Characters](/problems/sliding-window-longest-substring)
- [Number of Islands](/problems/number-of-islands) — same "connected component" mindset
