# Two Pointers — 3Sum

*[↗ LeetCode: 3Sum](https://leetcode.com/problems/3sum/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

Return all **unique triplets** `(a, b, c)` in `nums` that sum to 0.

**Example** — `nums=[-1,0,1,2,-1,-4]` → `[[-1,-1,2], [-1,0,1]]`

**Constraints** — `3 ≤ n ≤ 3000`; `-10⁵ ≤ nums[i] ≤ 10⁵`.

---

## Approach 1 — Brute force (all triplets)

**Intuition.** Three nested loops; dedup via a set of sorted triplets.

```java
List<List<Integer>> threeSumBrute(int[] a) {
    int n = a.length;
    Set<List<Integer>> seen = new HashSet<>();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            for (int k = j + 1; k < n; k++)
                if (a[i] + a[j] + a[k] == 0) {
                    List<Integer> t = Arrays.asList(a[i], a[j], a[k]);
                    Collections.sort(t);
                    seen.add(t);
                }
    return new ArrayList<>(seen);
}
```

**Complexity** — Time **O(n³)**; Space **O(#triplets)**. At n=3000 → 2.7·10¹⁰. TLE.

---

## Approach 2 — Hashing per pair

**Insight from brute.** Fix `i`; then it's "does the remaining array contain `-a[i] - a[j]` for some `j > i`?" — a Two Sum on the tail.

```java
List<List<Integer>> threeSumHash(int[] a) {
    Arrays.sort(a);
    Set<List<Integer>> seen = new HashSet<>();
    for (int i = 0; i < a.length; i++) {
        Set<Integer> map = new HashSet<>();
        for (int j = i + 1; j < a.length; j++) {
            int c = -a[i] - a[j];
            if (map.contains(c)) seen.add(Arrays.asList(a[i], c, a[j]));
            map.add(a[j]);
        }
    }
    return new ArrayList<>(seen);
}
```

**Complexity** — Time **O(n²)**; Space **O(n)** per iteration. Faster but still needs the dedup set.

---

## Approach 3 — Sort + two pointers (canonical)

**Insight from hashing.** After sorting, for each pivot `i`, apply **two pointers** on the tail — no set, O(1) space besides output. **Skip duplicates** at all three positions (`i`, `lo`, `hi`) to dedup while sorted.

**Trap.** Skipping only the pivot dedup isn't enough — after a hit, the same `lo`/`hi` values can produce duplicates on the next iteration.

```java
List<List<Integer>> threeSum(int[] a) {
    Arrays.sort(a);
    List<List<Integer>> out = new ArrayList<>();
    int n = a.length;
    for (int i = 0; i < n - 2; i++) {
        if (a[i] > 0) break;                    // no way to sum to 0
        if (i > 0 && a[i] == a[i - 1]) continue; // skip dup pivot
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            int s = a[i] + a[lo] + a[hi];
            if (s == 0) {
                out.add(Arrays.asList(a[i], a[lo], a[hi]));
                while (lo < hi && a[lo] == a[lo + 1]) lo++;   // skip dup lo
                while (lo < hi && a[hi] == a[hi - 1]) hi--;   // skip dup hi
                lo++; hi--;
            } else if (s < 0) lo++;
            else              hi--;
        }
    }
    return out;
}
```

<CodeTrace
  title="Sort + two pointers — sorted [-4,-1,-1,0,1,2]"
  :values="[-4,-1,-1,0,1,2]"
  :windowKeys="['lo','hi']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0, lo: 1, hi: 5 }, vars: { pivot: -4, need: 4 }, note: "no valid pair in tail" },
    { pointers: { i: 1, lo: 2, hi: 5 }, vars: { pivot: -1, sum: 0 }, note: "-1+-1+2=0 → [-1,-1,2]", added: [1,2,5] },
    { pointers: { i: 1, lo: 3, hi: 4 }, vars: { pivot: -1, sum: 0 }, note: "-1+0+1=0 → [-1,0,1]", added: [1,3,4] },
    { pointers: { i: 2 }, vars: { skip: "dup" }, note: "skip pivot dup (-1 again)" }
  ]'
/>

**Complexity** — Time **O(n²)** (sort O(n log n) + scan O(n²)); Space **O(1)** aside from output.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute nested triple | O(n³) | O(#triplets) |
| Hashing per pair | O(n²) | O(n) per iter |
| Sort + two pointers | **O(n²)** | **O(1)** |

## When to use which

- **Cold interview** → brute → sort+2ptr with the three-skip discipline.
- **k-Sum family** → fix `k−2` indices, two-pointer the last two.

## Related problems (same ladder applies)

- [3Sum Closest](https://leetcode.com/problems/3sum-closest/) — same skeleton, track `abs(sum - target)`
- [4Sum](https://leetcode.com/problems/4sum/) — fix i and j, two-pointer the rest
- [3Sum Smaller](https://leetcode.com/problems/3sum-smaller/) — count triplets with sum ≤ target
