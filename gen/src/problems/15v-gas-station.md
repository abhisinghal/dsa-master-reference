# Greedy — Gas Station

*[↗ LeetCode: Gas Station](https://leetcode.com/problems/gas-station/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Circular route: at station `i` you gain `gas[i]`, pay `cost[i]` to reach `i+1`. Find start index that completes the loop, or -1.

## Approach 1 — Brute force try each start

O(n²).

## Approach 2 — Single pass total + local reset

**Insight.**
1. If `sum(gas) < sum(cost)`, impossible.
2. Otherwise, a solution exists. Walk once: if running `tank < 0` at station `i`, no start in `[startCandidate..i]` works — reset `startCandidate = i+1`, `tank = 0`.

**Why the reset is safe.** If start `s ∈ [startCandidate..i]` failed at some later index, it failed before we reset. Any start after `i` starts fresh with tank 0.

```java
int canCompleteCircuit(int[] gas, int[] cost) {
    int total = 0, tank = 0, start = 0;
    for (int i = 0; i < gas.length; i++) {
        int diff = gas[i] - cost[i];
        total += diff;
        tank += diff;
        if (tank < 0) { start = i + 1; tank = 0; }
    }
    return total < 0 ? -1 : start;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Candy](/problems/candy) — two-sweep sibling
- [Best Sightseeing Pair](https://leetcode.com/problems/best-sightseeing-pair/)
