# Trie — Count Pairs With XOR in a Range

*[↗ LeetCode: Count Pairs With XOR in a Range](https://leetcode.com/problems/count-pairs-with-xor-in-a-range/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

Count pairs `(i, j)` with `low ≤ nums[i] XOR nums[j] ≤ high`.

---

## Approach 1 — Binary trie counting
**Insight.** `count(≤ high) - count(≤ low - 1)`. For each nums[i], walk the trie counting how many previously-inserted nums produce `XOR ≤ threshold` using bit-by-bit analysis. Trie stores subtree counts.

```java
class Node { Node[] ch = new Node[2]; int cnt; }
int countPairs(int[] nums, int low, int high) {
    return countLE(nums, high) - countLE(nums, low - 1);
}
int countLE(int[] nums, int threshold) {
    Node root = new Node();
    int total = 0;
    for (int x : nums) {
        total += queryLE(root, x, threshold);
        insert(root, x);
    }
    return total;
}
void insert(Node root, int x) {
    Node cur = root;
    for (int i = 15; i >= 0; i--) {
        int b = (x >> i) & 1;
        if (cur.ch[b] == null) cur.ch[b] = new Node();
        cur = cur.ch[b];
        cur.cnt++;
    }
}
int queryLE(Node root, int x, int t) {
    Node cur = root;
    int result = 0;
    for (int i = 15; i >= 0; i--) {
        if (cur == null) return result;
        int xb = (x >> i) & 1, tb = (t >> i) & 1;
        if (tb == 1) {
            if (cur.ch[xb] != null) result += cur.ch[xb].cnt;
            cur = cur.ch[1 - xb];
        } else {
            cur = cur.ch[xb];
        }
    }
    if (cur != null) result += cur.cnt;
    return result;
}
```

**Complexity** — Time **O(n · 16)**; Space **O(n · 16)**.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Binary trie counting | O(n · 16) | O(n · 16) | primary |

## When to use which

- **Ship this** → Binary trie counting (O(n · 16), O(n · 16)). The pattern's standard solution.

## Related problems

- [Maximum XOR of Two Numbers](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)
- [Maximum XOR With an Element From Array](/problems/maximum-xor-with-an-element-from-array)
