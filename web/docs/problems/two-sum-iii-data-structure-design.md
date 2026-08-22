# Hashing — Two Sum III (Data Structure Design)

*[↗ LeetCode: Two Sum III - Data Structure Design](https://leetcode.com/problems/two-sum-iii-data-structure-design/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

Design `TwoSum` supporting `add(x)` and `find(target)` (any pair summing to target).

---

## Approach 1 — Fast add, slow find
Store a count map. `find(t)` iterates keys, checks `t - k`. Handles duplicates via `count[k] > 1` for `k == t/2`.



```java
class TwoSum {
    Map<Integer, Integer> cnt = new HashMap<>();
    void add(int x) { cnt.merge(x, 1, Integer::sum); }
    boolean find(int t) {
        for (int k : cnt.keySet()) {
            int need = t - k;
            if (k == need) { if (cnt.get(k) >= 2) return true; }
            else if (cnt.containsKey(need)) return true;
        }
        return false;
    }
}
```



**add O(1)**, **find O(n)**.

---

## Approach 2 — Fast find, slow add
Precompute all pair sums into a set on `add`. `find` = O(1). `add` becomes O(n). Use when find ≫ add.

**Interview reasoning.** Ask about frequency of ops. If adds dominate, choose Approach 1; if finds dominate, choose Approach 2.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Fast add, slow find | O(1) | O(n) | baseline |
| Fast find, slow add | O(1) | O(n) | optimum |

## When to use which

- **State it for signal** → Fast add, slow find (O(1)). Correct baseline; call it out then move on.
- **Ship this** → Fast find, slow add (O(1), O(n)). Expected optimum in interview.

## Related problems

- [Two Sum](/problems/hashing-two-sum) — offline sibling
