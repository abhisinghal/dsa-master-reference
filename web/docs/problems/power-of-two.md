# Bit Manipulation — Power of Two

*[↗ LeetCode: Power of Two](https://leetcode.com/problems/power-of-two/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/bit-manip)

Return true iff `n` is a positive power of two.

---

## Approach 1 — Divide by 2
O(log n).

---

## Approach 2 — `n & (n-1) == 0`
**Insight.** A power of two has exactly one bit set. `n & (n-1)` clears the lowest set bit — result 0 iff there was only one.



```java
boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```



**Trap.** Guard `n > 0`: for `n=0`, `0 & -1 == 0` would falsely return true. For negative n, the two's-complement pattern also has one set-like bit form; excluding is required.

**Complexity** — Time **O(1)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Divide by 2 | O(log n) | — | baseline |
| `n & (n-1) == 0` | O(1) | O(1) | optimum |

## When to use which

- **State it for signal** → Divide by 2 (O(log n)). Correct baseline; call it out then move on.
- **Ship this** → `n & (n-1) == 0` (O(1), O(1)). Expected optimum in interview.

## Related problems

- [Power of Three](https://leetcode.com/problems/power-of-three/) — no bit trick, use `1162261467 % n == 0`
- [Power of Four](https://leetcode.com/problems/power-of-four/) — power of two AND set bit at even position
