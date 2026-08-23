# DP — Delete and Earn

*[↗ LeetCode: Delete and Earn](https://leetcode.com/problems/delete-and-earn/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/dp)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Delete `x` to earn `x` points; also removes all `x-1` and `x+1`. Max points.

**Example 1** — `nums=[3,4,2]` → `6`
**Example 2** — `nums=[2,2,3,3,3,4]` → `9`

**Constraints** — `1 ≤ n ≤ 2·10⁴`.


&lt;Hints
  hint1="What is the state? What are the transitions? What’s the base case?"
  hint2="Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling."
  hint3="For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
/&gt;
---

## Approach — Reduce to House Robber (canonical)

**Insight.** Bucket totals: `points[v] = v · count(v)`. Picking `v` forbids `v±1` — exactly House Robber on `points[]`.



```java
int deleteAndEarn(int[] nums) {
    int max = 0;
    for (int x : nums) max = Math.max(max, x);
    int[] points = new int[max + 1];
    for (int x : nums) points[x] += x;
    int prev = 0, curr = 0;
    for (int v = 0; v <= max; v++) {
        int t = Math.max(curr, prev + points[v]);
        prev = curr; curr = t;
    }
    return curr;
}
```



<CodeTrace
  title="Reduce to House Robber (canonical)"
  :values="['3', '4', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 2 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n + max)**; Space **O(max)**.

---

## Try it yourself

<JavaRunner problem-slug="delete-and-earn" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Reduce to House Robber | **O(n + max)** | O(max) | canonical |

## When to use which

- **"Adjacent-value taboo"** → reduce to House Robber.
- **Sparse values** → skip zeros; use TreeMap.

## Related problems

- [House Robber](/problems/dp-house-robber)
- [House Robber II](/problems/house-robber-ii)