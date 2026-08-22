# Two Pointers — Boats to Save People

*[↗ LeetCode: Boats to Save People](https://leetcode.com/problems/boats-to-save-people/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Each boat carries at most 2 people totaling ≤ `limit`. Minimize number of boats.

---

## Approach 1 — Sort + greedy two-pointer
**Insight.** Sort. Pair the heaviest with the lightest if possible; otherwise the heaviest goes alone.

**Why optimal.** If the heaviest can't pair with the lightest, they can't pair with anyone; sending them alone is forced. If they can pair, pairing with the lightest is at least as good as any other pairing (leaves the strongest remainder).

```java
int numRescueBoats(int[] people, int limit) {
    Arrays.sort(people);
    int l = 0, r = people.length - 1, boats = 0;
    while (l <= r) {
        if (people[l] + people[r] <= limit) l++;
        r--;
        boats++;
    }
    return boats;
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort + greedy two-pointer | O(n log n) | O(1) | primary |

## When to use which

- **Ship this** → Sort + greedy two-pointer (O(n log n), O(1)). The pattern's standard solution.

## Related problems

- [Two Sum II - Input Array Is Sorted](/problems/two-sum-ii-input-array-is-sorted)
- [Assign Cookies](https://leetcode.com/problems/assign-cookies/) — same sort+pair greedy
