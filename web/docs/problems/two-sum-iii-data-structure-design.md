# Hashing — Two Sum III (Data Structure Design)

*[↗ LeetCode: Two Sum III - Data Structure Design](https://leetcode.com/problems/two-sum-iii-data-structure-design/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

<CompanyTags companies="LinkedIn, Meta, Google" />

Design `TwoSum` supporting `add(x)` and `find(t)`.

**Example 1** —


```
TwoSum ts = new TwoSum();
ts.add(1); ts.add(3); ts.add(5);
ts.find(4);  // true  (1 + 3)
ts.find(7);  // false
```



**Example 2** — Duplicate handling: `add(3); add(3); find(6)` → `true` (uses both 3s).

**Example 3** — Empty: `find(10)` on a fresh TwoSum → `false`.

**Constraints** — up to 10⁴ ops total. Naive O(n²) per-find would give 10⁸ ops; wisely chosen design gives ~10⁴.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its 'canonical form' — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For 'first duplicate', a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="two-sum-iii-data-structure-design" /> <Bookmark problem-slug="two-sum-iii-data-structure-design" />

<InterviewTimer problem-slug="two-sum-iii-data-structure-design" />



## Approach 1 — Fast add, slow find (canonical if adds dominate)

**Insight.** Store counts in a `HashMap`. On `add`, increment count in O(1). On `find`, iterate over each stored value `k` and check whether `t - k` also exists (with duplicate handling for `k == t/2`).



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



**Complexity** — add **O(1)**; find **O(n)**. *In an interview* say "ask the interviewer about the ratio of adds to finds — pick a design accordingly."

## Approach 2 — Fast find, slow add

**Precompute all pairwise sums** into a `HashSet` on `add`. `find = O(1)`, `add = O(n)`.



```java
class TwoSumFastFind {
    List<Integer> nums = new ArrayList<>();
    Set<Integer> sums = new HashSet<>();
    void add(int x) {
        for (int y : nums) sums.add(x + y);
        nums.add(x);
    }
    boolean find(int t) { return sums.contains(t); }
}
```



**Complexity** — add **O(n)**; find **O(1)**. *Say aloud in an interview:* "trade-space-for-time: sums grows to O(n²), fine at 10⁴ ops but explodes at 10⁶."

---

## Try it yourself

<JavaRunner problem-slug="two-sum-iii-data-structure-design" />

## Complexity summary

| Approach | add | find | Grade |
|---|---|---|---|
| **Fast add** | **O(1)** | O(n) | **Canonical when adds dominate** |
| Fast find | O(n) | O(1) | When finds dominate |

## When to use which

- **Ask the interviewer about ratio** — pick the matching design.
- **Balanced** → hybrid or ordered TreeSet.
- **"Stream infinite"** → fast add.

<AiCompanion problem-slug="two-sum-iii-data-structure-design" pattern-hint="hashing" />

## Related problems

- [Two Sum](/problems/hashing-two-sum)

<FeedbackWidget problem-slug="two-sum-iii-data-structure-design" />
