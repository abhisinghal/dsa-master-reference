# Monotonic Stack — Remove K Digits

*[↗ LeetCode: Remove K Digits](https://leetcode.com/problems/remove-k-digits/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

Given a numeric string `num` and integer `k`, remove exactly `k` digits so the resulting number is smallest. Return the string (no leading zeros).

**Example 1** — `num="1432219", k=3` → `"1219"`
**Example 2** — `num="10200", k=1` → `"200"` (leading zeros stripped)

---

## Approach 1 — Brute (try all C(n,k) removals)

**Complexity** — TLE fast.

## Approach 2 — Greedy with monotonic increasing stack

**Insight.** From left to right, keep digits in a **non-decreasing** stack. When today's digit breaks the invariant, pop the top (as long as we still have removals remaining). Any digit that makes the number bigger by "coming before a smaller one" should go.

**Trap.** After the scan, if `k > 0`, chop the last `k` digits (they must be the largest remaining — since the stack is non-decreasing, biggest are at the end).

```java
String removeKdigits(String num, int k) {
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : num.toCharArray()) {
        while (k > 0 && !stack.isEmpty() && stack.peek() > c) { stack.pop(); k--; }
        stack.push(c);
    }
    while (k-- > 0 && !stack.isEmpty()) stack.pop();
    StringBuilder sb = new StringBuilder();
    for (char c : stack) sb.append(c);
    sb.reverse();
    int i = 0;
    while (i < sb.length() && sb.charAt(i) == '0') i++;                 // strip leading 0
    String out = sb.substring(i);
    return out.isEmpty() ? "0" : out;
}
```

<CodeTrace
  title="Greedy stack — num=&quot;1432219&quot;, k=3"
  :values="['1','4','3','2','2','1','9']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { stack: "[1]", k: 3 }, note: "push 1" },
    { pointers: { i: 1 }, vars: { stack: "[1,4]", k: 3 }, note: "push 4 (1 le 4)" },
    { pointers: { i: 2 }, vars: { stack: "[1,3]", k: 2 }, note: "3 lt 4 → pop 4 (k→2), push 3", removed: [1] },
    { pointers: { i: 3 }, vars: { stack: "[1,2]", k: 1 }, note: "2 lt 3 → pop 3 (k→1)", removed: [2] },
    { pointers: { i: 5 }, vars: { stack: "[1,1]", k: 0 }, note: "1 lt 2 → pop 2, push 1. k=0 → stop popping", removed: [4] },
    { pointers: { i: 6 }, vars: { stack: "[1,1,9]", answer: "1219" }, note: "final. answer 1219", added: [0,5,6] }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute all removals | O(C(n,k) · n) | O(n) |
| Greedy monotonic stack | **O(n)** | O(n) |

## Related problems

- [Smallest Subsequence of Distinct Characters](https://leetcode.com/problems/smallest-subsequence-of-distinct-characters/) — same greedy stack + count constraint
- [132 Pattern](https://leetcode.com/problems/132-pattern/) — monotonic stack with a `k` companion
- [Create Maximum Number](https://leetcode.com/problems/create-maximum-number/) — two-array variant
