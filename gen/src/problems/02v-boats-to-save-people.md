# Two Pointers — Boats to Save People

*[↗ LeetCode: Boats to Save People](https://leetcode.com/problems/boats-to-save-people/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Each boat carries ≤ 2 people totaling ≤ `limit`. Minimize boats.

**Example 1** — `people=[1,2], limit=3` → `1`
**Example 2** — `people=[3,2,2,1], limit=3` → `3`
**Example 3** — `people=[3,5,3,4], limit=5` → `4`

**Constraints** — `1 ≤ n ≤ 5·10⁴`.

---

## Approach — Sort + greedy two-pointer (canonical)

**Insight.** Sort. Pair heaviest with lightest if possible; otherwise heaviest goes alone.

**Why optimal.** If heaviest can't pair with lightest, they can't pair with anyone.

```java
int numRescueBoats(int[] people, int limit) {
    Arrays.sort(people);
    int l = 0, r = people.length - 1, boats = 0;
    while (l <= r) {
        if (people[l] + people[r] <= limit) l++;
        r--; boats++;
    }
    return boats;
}
```

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + greedy | **O(n log n)** | O(1) | canonical |

## When to use which

- **"Pair heaviest + lightest greedy"** → applies to boats, task scheduling, item packing.
- **"3+ per boat"** → generalizes with DP or different greedy.

## Related problems

- [Two Sum II](/problems/two-sum-ii-input-array-is-sorted)
- [Assign Cookies](https://leetcode.com/problems/assign-cookies/)
