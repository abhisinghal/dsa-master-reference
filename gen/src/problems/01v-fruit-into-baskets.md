# Sliding Window — Fruit Into Baskets

*[↗ LeetCode: Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Longest subarray with at most 2 distinct values.

## Approach — Sliding window (k = 2)

**Insight.** Special case of "at most k distinct" with k = 2. Same template.

```java
int totalFruit(int[] fruits) {
    Map<Integer, Integer> cnt = new HashMap<>();
    int l = 0, best = 0;
    for (int r = 0; r < fruits.length; r++) {
        cnt.merge(fruits[r], 1, Integer::sum);
        while (cnt.size() > 2) {
            cnt.merge(fruits[l], -1, Integer::sum);
            if (cnt.get(fruits[l]) == 0) cnt.remove(fruits[l]);
            l++;
        }
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```

**Complexity** — Time **O(n)**; Space **O(1)**.

## Related problems

- [Longest Substring With At Most K Distinct](/problems/longest-substring-with-at-most-k-distinct)
- [Max Consecutive Ones III](/problems/max-consecutive-ones-iii)
