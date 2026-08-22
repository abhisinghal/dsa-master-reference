# Trie — Count Pairs With XOR in a Range

*[↗ LeetCode: Count Pairs With XOR in a Range](https://leetcode.com/problems/count-pairs-with-xor-in-a-range/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

Count pairs `(i, j)` with `i < j` and `low ≤ nums[i] XOR nums[j] ≤ high`.

**Example 1** — `nums=[1,4,2,7], low=2, high=6` → `6`
**Example 2** — `nums=[9,8,4,2,1], low=5, high=14` → `8`

**Constraints** — `1 ≤ n ≤ 2·10⁴`; `0 ≤ nums[i] ≤ 2·10⁴`.

---

## Approach 1 — All pairs

O(n²). Baseline; borderline TLE.

## Approach 2 — Binary trie with subtree counts (canonical)

**Insight.** `count(≤ high) - count(≤ low - 1)`. For each `nums[i]`, count how many previously-inserted values yield XOR ≤ threshold via a per-bit analysis.

```java
class Node { Node[] c = new Node[2]; int cnt; }
int countPairs(int[] nums, int low, int high) {
    return countLE(nums, high) - countLE(nums, low - 1);
}
int countLE(int[] nums, int t) {
    Node root = new Node();
    int total = 0;
    for (int x : nums) { total += queryLE(root, x, t); insert(root, x); }
    return total;
}
void insert(Node root, int x) {
    Node cur = root;
    for (int i = 15; i >= 0; i--) {
        int b = (x >> i) & 1;
        if (cur.c[b] == null) cur.c[b] = new Node();
        cur = cur.c[b]; cur.cnt++;
    }
}
int queryLE(Node root, int x, int t) {
    Node cur = root; int r = 0;
    for (int i = 15; i >= 0; i--) {
        if (cur == null) return r;
        int xb = (x >> i) & 1, tb = (t >> i) & 1;
        if (tb == 1) {
            if (cur.c[xb] != null) r += cur.c[xb].cnt;
            cur = cur.c[1 - xb];
        } else cur = cur.c[xb];
    }
    if (cur != null) r += cur.cnt;
    return r;
}
```

**Complexity** — Time **O(n · 16)**; Space **O(n · 16)**.

---

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| All pairs | O(n²) | O(1) | baseline |
| Binary trie counting | **O(n · 16)** | O(n · 16) | canonical |

## When to use which

- **XOR count in a range** → binary trie with subtree counts.
- **Fixed range not variable** → single sweep suffices.
- **Streaming** → same trie, insert online.

## Related problems

- [Maximum XOR of Two Numbers](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)
- [Maximum XOR With an Element From Array](/problems/maximum-xor-with-an-element-from-array)
- [Maximum Genetic Difference](/problems/maximum-genetic-difference-query)
