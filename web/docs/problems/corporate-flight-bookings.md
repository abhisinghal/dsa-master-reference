# Prefix Sum — Corporate Flight Bookings

*[↗ LeetCode: Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

&lt;CompanyTags companies="Amazon, Meta" /&gt;

Given `n` flights and bookings `[first, last, seats]`, return an array where index `i` = total seats booked on flight `i+1`.

**Example 1** — `bookings=[[1,2,10],[2,3,20],[2,5,25]], n=5` → `[10,55,45,25,25]`
**Example 2** — `bookings=[[1,2,10],[2,2,15]], n=2` → `[10,25]`
**Example 3** — `bookings=[[1,1,5]], n=3` → `[5,0,0]`

**Constraints** — `1 ≤ n ≤ 2·10⁴`; `1 ≤ bookings.length ≤ 2·10⁴`.


&lt;Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/&gt;
---

## Approach 1 — Direct fill

For each booking, add `seats` to every index in `[first-1, last-1]`. **O(n · m)**.

## Approach 2 — Difference array (canonical)

**Insight.** Range-add on many disjoint queries is O(1) per query on a **difference array**: `+seats` at `first-1`, `-seats` at `last`. Prefix sum recovers the totals.



```java
int[] corpFlightBookings(int[][] bookings, int n) {
    int[] diff = new int[n + 1];
    for (int[] b : bookings) {
        diff[b[0] - 1] += b[2];
        diff[b[1]] -= b[2];
    }
    for (int i = 1; i < n; i++) diff[i] += diff[i - 1];
    return Arrays.copyOf(diff, n);
}
```



<CodeTrace
  title="Diff array — bookings=[[1,2,10],[2,3,20],[2,5,25]], n=5"
  :values="['0','0','0','0','0']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { diff: "[10,20+25,-10,-20,25,-25]" }, note: "record deltas" },
    { pointers: { i: 1 }, vars: { pref: "[10,55,45,25,25]" }, note: "prefix sum reveals totals" }
  ]'
/>

**Complexity** — Time **O(n + m)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="corporate-flight-bookings" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Direct fill | O(n·m) | O(n) | baseline |
| Difference array | **O(n+m)** | O(n) | optimum |

## When to use which

- **Many range-add queries, one final read** → difference array + one prefix sum.
- **Queries interleaved with reads** → segment tree with lazy propagation.
- **Range assignment (not add)** → different structure — sweep line or seg tree.

## Related problems

- [Car Pooling](/problems/car-pooling) — identical idea with capacity check
- [Range Addition](/problems/range-addition) — the primitive
- [Range Addition II](/problems/range-addition-ii)