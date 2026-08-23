# Trie — Maximum XOR With an Element From Array

*[↗ LeetCode: Maximum XOR With an Element From Array](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

<CompanyTags companies="Google, Amazon" />

Given `nums` and queries `[query_val, max_allowed]`. For each query return the max XOR of `query_val` with any `x ∈ nums` where `x ≤ max_allowed`. Return -1 if no such x.

**Example** — `nums=[0,1,2,3,4], queries=[[3,1],[1,3],[5,6]]` → `[3,3,7]`

**Constraints** — `1 ≤ n ≤ 10⁵`; nums, queries ≤ 10⁵.


<Hints
  hint1="Prefix operations? Word set lookups? Autocomplete?"
  hint2="Each node has ≤ σ children (26 for lowercase). Walk char-by-char; create nodes on insert; check `end` flag on search."
  hint3="For XOR max: binary trie of 32-bit values; walk greedily choosing the opposite bit."
/>
---

## Approach 1 — Linear per query

O(n · Q). TLE.

## Approach 2 — Offline sort + binary trie (canonical)

**Insight.** Sort nums ascending; sort queries by `max_allowed`. Process queries in order, inserting nums into a **binary trie** as they become eligible. For each query, walk the trie greedily choosing the opposite bit.

```java
class Node { Node[] c = new Node[2]; }
int[] maximizeXor(int[] nums, int[][] queries) {
    Arrays.sort(nums);
    Integer[] ord = new Integer[queries.length];
    for (int i = 0; i < queries.length; i++) ord[i] = i;
    Arrays.sort(ord, (a, b) -> queries[a][1] - queries[b][1]);
    int[] ans = new int[queries.length];
    Node root = new Node();
    int idx = 0;
    for (int qi : ord) {
        int v = queries[qi][0], cap = queries[qi][1];
        while (idx < nums.length && nums[idx] <= cap) insert(root, nums[idx++]);
        ans[qi] = idx == 0 ? -1 : maxXor(root, v);
    }
    return ans;
}
void insert(Node root, int x) {
    Node cur = root;
    for (int i = 31; i >= 0; i--) {
        int b = (x >> i) & 1;
        if (cur.c[b] == null) cur.c[b] = new Node();
        cur = cur.c[b];
    }
}
int maxXor(Node root, int v) {
    Node cur = root; int r = 0;
    for (int i = 31; i >= 0; i--) {
        int b = (v >> i) & 1, want = 1 - b;
        if (cur.c[want] != null) { r |= 1 << i; cur = cur.c[want]; }
        else cur = cur.c[b];
    }
    return r;
}
```

<CodeTrace
  title="Linear per query"
  :values="['0', '1', '2', '3', '4']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 4 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O((n + q) · 32 + q log q)**; Space **O(n · 32)**.

---

## Try it yourself

<JavaRunner problem-slug="maximum-xor-with-an-element-from-array" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Linear per query | O(n · Q) | O(1) | TLE |
| Offline sort + binary trie | **O((n+q)·32)** | O(n·32) | canonical |

## When to use which

- **Max XOR queries** → binary trie always.
- **Constraint on element** → offline sort processes queries in order of constraint.
- **Streaming** → online trie without deletion; harder with `≤ max` constraint.

## Related problems

- [Maximum XOR of Two Numbers](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) — offline sibling
- [Count Pairs With XOR in Range](/problems/count-pairs-with-xor-in-a-range)
- [Maximum Genetic Difference Query](/problems/maximum-genetic-difference-query)