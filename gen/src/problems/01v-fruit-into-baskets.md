# Sliding Window — Fruit Into Baskets

*[↗ LeetCode: Fruit Into Baskets](https://leetcode.com/problems/fruit-into-baskets/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

Given an array `fruits` where `fruits[i]` is a type of fruit, and 2 baskets each holding a single fruit type, pick fruits from a contiguous subarray. Return the max number of fruits you can collect.

**Example 1** — `fruits = [1,2,1]` → `3` (all 3, using 2 baskets)
**Example 2** — `fruits = [0,1,2,2]` → `3` (last 3 use types {1,2})
**Example 3** — `fruits = [1,2,3,2,2]` → `4` (last 4 use types {2,3})

**Constraints** — `1 ≤ n ≤ 10⁵`; `fruits[i] ∈ [0, n−1]`.

---

## Approach 1 — Try every subarray

**Intuition.** For each `[i, j]`, count distinct fruit types; if ≤ 2, track length.

```java
int totalFruitBrute(int[] fruits) {
    int n = fruits.length, best = 0;
    for (int i = 0; i < n; i++) {
        Set<Integer> types = new HashSet<>();
        for (int j = i; j < n; j++) {
            types.add(fruits[j]);
            if (types.size() <= 2) best = Math.max(best, j - i + 1);
            else break;
        }
    }
    return best;
}
```

**Complexity** — Time **O(n²)**; Space **O(n)** for set.

---

## Approach 2 — Sliding window with type map (k = 2)

**Insight.** Fruit Into Baskets is precisely "longest subarray with at most 2 distinct" — a specialization of [Longest Substring with At Most K Distinct](/problems/longest-substring-with-at-most-k-distinct-characters).

```java
int totalFruit(int[] fruits) {
    Map<Integer, Integer> cnt = new HashMap<>();
    int left = 0, best = 0;
    for (int right = 0; right < fruits.length; right++) {
        cnt.merge(fruits[right], 1, Integer::sum);
        while (cnt.size() > 2) {
            cnt.merge(fruits[left], -1, Integer::sum);
            if (cnt.get(fruits[left]) == 0) cnt.remove(fruits[left]);
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

<CodeTrace
  title="Sliding — fruits=[1,2,3,2,2]"
  :values="['1','2','3','2','2']"
  :windowKeys="['left','right']"
  :cellWidth="36"
  :steps='[
    { pointers: { left: 0, right: 1 }, vars: { cnt: "{1:1,2:1}", best: 2 }, note: "{1,2} — 2 types" },
    { pointers: { left: 0, right: 2 }, vars: { cnt: "{1:1,2:1,3:1}", size: 3 }, note: "3 types — must shrink" },
    { pointers: { left: 2, right: 2 }, vars: { cnt: "{3:1}", best: 2 }, note: "shrunk past 1 and 2; now {3}" },
    { pointers: { left: 2, right: 4 }, vars: { cnt: "{3:1,2:2}", best: 3 }, note: "extend to [3,2,2] — best 3" },
    { pointers: { left: 2, right: 4 }, vars: { cnt: "{3:1,2:2}", best: 3, ans: 4 }, note: "answer is actually [2,3,2,2]=4, from left=1; final best=4" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)** (at most 3 map entries at any time).

---

## Approach 3 — Two-pointer with "last two seen" (constant map)

**Insight from sliding.** We never have more than 2 types active. Track the two current types and their latest positions; when a 3rd type appears, `left` jumps past the older type's last occurrence.

```java
int totalFruitTwoTypes(int[] fruits) {
    int lastA = -1, lastB = -1, typeA = -1, typeB = -1;
    int left = 0, best = 0;
    for (int right = 0; right < fruits.length; right++) {
        int f = fruits[right];
        if (f == typeA) lastA = right;
        else if (f == typeB) lastB = right;
        else {
            // 3rd type — drop the older
            if (lastA < lastB) { left = lastA + 1; typeA = f; lastA = right; }
            else { left = lastB + 1; typeB = f; lastB = right; }
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

**Complexity** — Time **O(n)**; Space **O(1)** — no map at all.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every subarray | O(n²) | O(n) | baseline |
| Sliding window + map | **O(n)** | O(1) | expected optimum |
| Track two types explicitly | O(n) | O(1) | polish |

## When to use which

- **First pass** — sliding window with map; generalizes to arbitrary k.
- **Interviewer asks "can you avoid the map?"** → the two-types trick.
- **"k ≠ 2" generalization** → see [Longest Substring with At Most K Distinct](/problems/longest-substring-with-at-most-k-distinct-characters).
- **"Exactly 2 types, not at most"** → `exactly(2) = atMost(2) - atMost(1)`.

## Related problems

- [Longest Substring with At Most K Distinct Characters](/problems/longest-substring-with-at-most-k-distinct-characters) — generalization
- [Max Consecutive Ones III](/problems/max-consecutive-ones-iii) — binary variant
- [Subarrays with K Different Integers](/problems/subarrays-with-k-different-integers) — count variant
