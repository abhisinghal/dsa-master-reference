# Prefix Sum — Count Submatrices with Target Sum

*[↗ LeetCode: Count Submatrices with Target Sum](https://leetcode.com/problems/count-submatrices-that-sum-to-target/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/prefix-sum)

Given matrix and integer `target`, count submatrices whose sum equals `target`.

**Example 1** — `mat=[[0,1,0],[1,1,1],[0,1,0]], target=0` → `4`
**Example 2** — `mat=[[1,-1],[-1,1]], target=0` → `5`
**Example 3** — `mat=[[904]], target=0` → `0`

**Constraints** — `1 ≤ m, n ≤ 100`; `-1000 ≤ mat[i][j] ≤ 1000`.

---

## Approach 1 — Enumerate every submatrix

O(m²·n²·mn). TLE.

## Approach 2 — Row-collapse + 1D subarray-sum trick (canonical)

**Insight.** Fix a top row `r1` and bottom row `r2`. Collapse the strip into a 1D array `col[j] = Σ mat[r1..r2][j]`. Now count subarrays of `col` summing to `target` — [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k) template. Iterate over all `(r1, r2)`.



```java
int numSubmatrixSumTarget(int[][] mat, int target) {
    int m = mat.length, n = mat[0].length, count = 0;
    for (int r1 = 0; r1 < m; r1++) {
        int[] col = new int[n];
        for (int r2 = r1; r2 < m; r2++) {
            for (int j = 0; j < n; j++) col[j] += mat[r2][j];
            // subarray sum = target in col
            Map<Integer, Integer> cnt = new HashMap<>();
            cnt.put(0, 1);
            int pref = 0;
            for (int j = 0; j < n; j++) {
                pref += col[j];
                count += cnt.getOrDefault(pref - target, 0);
                cnt.merge(pref, 1, Integer::sum);
            }
        }
    }
    return count;
}
```



**Complexity** — Time **O(m²·n)**; Space **O(n)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| All submatrices | O(m³·n²) | O(1) | baseline |
| Row-collapse + 1D SSEqK | **O(m²·n)** | O(n) | canonical |

## When to use which

- **2D sum problems reducible to 1D fixed-row-strip** → row collapse.
- **Faster on `m > n`** → transpose and collapse the smaller dimension outer.
- **"Max sum submatrix ≤ K"** → similar collapse + Kadane variant with TreeSet.

## Related problems

- [Subarray Sum Equals K](/problems/prefix-sum-subarray-sum-equals-k)
- [Max Sum of Rectangle No Larger Than K](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/)
- [Maximum Sum Rectangle](/problems/maximum-subarray) — 1D Kadane sibling
