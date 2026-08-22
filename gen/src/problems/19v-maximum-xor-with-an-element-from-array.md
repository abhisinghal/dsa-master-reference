# Trie — Maximum XOR With an Element From Array

*[↗ LeetCode: Maximum XOR With an Element From Array](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

Given `nums` and queries `[query_val, max_allowed]`, for each query return `max XOR(query_val, x)` where `x ∈ nums` and `x ≤ max_allowed`, or `-1` if none.

---

## Approach 1 — Sort + offline queries + binary trie
**Insight.** Sort nums and queries by their upper bound. Process queries in order, inserting new nums into a **binary trie** as their values become eligible. For each query, walk the trie greedily choosing the opposite bit.

```java
class Node { Node[] ch = new Node[2]; }
int[] maximizeXor(int[] nums, int[][] queries) {
    Arrays.sort(nums);
    Integer[] order = new Integer[queries.length];
    for (int i = 0; i < queries.length; i++) order[i] = i;
    Arrays.sort(order, (a, b) -> queries[a][1] - queries[b][1]);
    int[] out = new int[queries.length];
    Node root = new Node();
    int idx = 0;
    for (int qi : order) {
        int v = queries[qi][0], cap = queries[qi][1];
        while (idx < nums.length && nums[idx] <= cap) insert(root, nums[idx++]);
        if (idx == 0) { out[qi] = -1; continue; }
        out[qi] = maxXor(root, v);
    }
    return out;
}
void insert(Node root, int x) {
    Node cur = root;
    for (int i = 31; i >= 0; i--) {
        int b = (x >> i) & 1;
        if (cur.ch[b] == null) cur.ch[b] = new Node();
        cur = cur.ch[b];
    }
}
int maxXor(Node root, int v) {
    Node cur = root;
    int result = 0;
    for (int i = 31; i >= 0; i--) {
        int b = (v >> i) & 1, want = 1 - b;
        if (cur.ch[want] != null) { result |= 1 << i; cur = cur.ch[want]; }
        else cur = cur.ch[b];
    }
    return result;
}
```

**Complexity** — Time **O((n + q) · 32 + q log q)**; Space **O(n · 32)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort + offline queries + binary trie | O((n + q) · 32 + q log q) | O(n · 32) | primary |

## When to use which

- **Ship this** → Sort + offline queries + binary trie (O((n + q) · 32 + q log q), O(n · 32)). The pattern's standard solution.

## Related problems

- [Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) — offline sibling
- [Count Pairs With XOR in a Range](/problems/count-pairs-with-xor-in-a-range)
