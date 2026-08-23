# Prefix Sum — Maximal Rectangle

*[↗ LeetCode: Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/monotonic-stack)

<CompanyTags companies="Amazon, Google, Meta, Microsoft" />

Given a binary matrix, find the largest rectangle containing only `1`s.

**Example 1** — `mat=[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]` → `6`
**Example 2** — `mat=[["0"]]` → `0`
**Example 3** — `mat=[["1"]]` → `1`

**Constraints** — `1 ≤ m, n ≤ 200`; entries `'0'`/`'1'`.


<Hints
  hint1="Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?"
  hint2="Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For ’count subarrays with property X on sum’, use a hash-map of prefix sums."
  hint3="For ’≥ 2 length’ or ’divisible by k’ variants, store first occurrence and check remainders."
/>
---

## Approach 1 — Every submatrix

O(m³·n³). TLE.

## Approach 2 — Row heights + Largest Rectangle in Histogram (canonical)

**Insight.** For each row `i`, build heights[j] = number of consecutive 1s ending at `mat[i][j]`. Then apply [Largest Rectangle in Histogram](/problems/largest-rectangle-in-histogram) to that heights array. Max across all rows.

```java
int maximalRectangle(char[][] mat) {
    if (mat.length == 0) return 0;
    int m = mat.length, n = mat[0].length, best = 0;
    int[] h = new int[n];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) h[j] = mat[i][j] == '1' ? h[j] + 1 : 0;
        best = Math.max(best, largestRect(h));
    }
    return best;
}
int largestRect(int[] h) {
    Deque<Integer> st = new ArrayDeque<>();
    int best = 0, n = h.length;
    for (int i = 0; i <= n; i++) {
        int val = i == n ? 0 : h[i];
        while (!st.isEmpty() && h[st.peek()] > val) {
            int t = st.pop();
            int w = st.isEmpty() ? i : i - st.peek() - 1;
            best = Math.max(best, h[t] * w);
        }
        st.push(i);
    }
    return best;
}
```

<CodeTrace
  title="Row heights sweep"
  :values="['1','0','1','0','0']"
  :windowKeys="['row']"
  :cellWidth="30"
  :steps='[
    { pointers: { row: 0 }, vars: { h: "[1,0,1,0,0]", rectMax: 1 }, note: "" },
    { pointers: { row: 2 }, vars: { h: "[3,1,3,2,2]", rectMax: 6 }, note: "widest at row 2" }
  ]'
/>

**Complexity** — Time **O(m·n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="maximal-rectangle" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Enumerate submatrices | O(m³·n³) | O(1) | baseline |
| Rows + histogram stack | **O(m·n)** | O(n) | canonical |

## When to use which

- **Binary matrix, largest rectangle of 1s** → row-height + histogram stack.
- **Only squares** → simpler DP (see [Maximal Square](/problems/maximal-square)).
- **"Count submatrices with X"** → row-collapse + 1D template.

## Related problems

- [Largest Rectangle in Histogram](/problems/largest-rectangle-in-histogram) — the primitive
- [Maximal Square](/problems/maximal-square)
- [Count Submatrices with Target Sum](/problems/count-submatrices-with-target-sum)