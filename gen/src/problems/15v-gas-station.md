# Greedy — Gas Station

*[↗ LeetCode: Gas Station](https://leetcode.com/problems/gas-station/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/greedy)

Circular route: at station `i` you gain `gas[i]`, pay `cost[i]` to reach `i+1`. Return start index that completes the loop, or `-1`.

**Example 1** — `gas=[1,2,3,4,5], cost=[3,4,5,1,2]` → `3`
**Example 2** — `gas=[2,3,4], cost=[3,4,3]` → `-1`

**Constraints** — `1 ≤ n ≤ 10⁵`.

---

## Approach 1 — Try each start with simulation

O(n²). TLE.

## Approach 2 — Single pass total + local reset (canonical)

**Insight.**
1. If `Σgas < Σcost`, impossible.
2. Walk once: track running `tank`. When `tank < 0` at `i`, no start in `[startCandidate..i]` works → reset `startCandidate = i+1`, `tank = 0`.

```java
int canCompleteCircuit(int[] gas, int[] cost) {
    int total = 0, tank = 0, start = 0;
    for (int i = 0; i < gas.length; i++) {
        int d = gas[i] - cost[i];
        total += d; tank += d;
        if (tank < 0) { start = i + 1; tank = 0; }
    }
    return total < 0 ? -1 : start;
}
```

<CodeTrace
  title="Reset — gas=[1,2,3,4,5], cost=[3,4,5,1,2]"
  :values="['-2','-2','-2','3','3']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 2 }, vars: { tank: -6 }, note: "reset; start=3" },
    { pointers: { i: 4 }, vars: { tank: 6, total: 0 }, note: "return 3" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Simulate | O(n²) | O(1) | TLE |
| Total + reset | **O(n)** | O(1) | canonical |

## When to use which

- **Circular feasibility problem with cost/gain** → total + reset.
- **Multiple valid starts** → all indices past all resets are valid.
- **Two-direction travel** → separate check for each.

## Related problems

- [Candy](/problems/candy) — two-sweep sibling
- [Best Sightseeing Pair](https://leetcode.com/problems/best-sightseeing-pair/)
