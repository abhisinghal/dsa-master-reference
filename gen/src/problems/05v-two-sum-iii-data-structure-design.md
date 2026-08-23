# Hashing — Two Sum III (Data Structure Design)

*[↗ LeetCode: Two Sum III - Data Structure Design](https://leetcode.com/problems/two-sum-iii-data-structure-design/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/hashing)

<CompanyTags companies="LinkedIn, Meta, Google" />

Design `TwoSum` supporting `add(x)` and `find(t)`.

**Example** —
```
TwoSum ts = new TwoSum();
ts.add(1); ts.add(3); ts.add(5);
ts.find(4);  // true
ts.find(7);  // false
```

**Constraints** — up to 10⁴ ops.


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="two-sum-iii-data-structure-design" /> <Bookmark problem-slug="two-sum-iii-data-structure-design" />

<InterviewTimer problem-slug="two-sum-iii-data-structure-design" />



## Approach 1 — Fast add, slow find (canonical if adds dominate)

Store counts; on `find`, iterate keys checking `t - k`. Handle duplicates.

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

**add O(1); find O(n).**

## Approach 2 — Fast find, slow add

Precompute all pairwise sums into a set on `add`. `find` = O(1). `add` = O(n).

---

## Try it yourself

<JavaRunner problem-slug="two-sum-iii-data-structure-design" />

## Complexity summary

| Approach | add | find | Grade |
|---|---|---|---|
| Fast add | O(1) | O(n) | adds dominate |
| Fast find | O(n) | O(1) | finds dominate |

## When to use which

- **Ask the interviewer about ratio** — pick the matching design.
- **Balanced** → hybrid or ordered TreeSet.
- **"Stream infinite"** → fast add.

<AiCompanion problem-slug="two-sum-iii-data-structure-design" pattern-hint="hashing" />

## Related problems

- [Two Sum](/problems/hashing-two-sum)

<FeedbackWidget problem-slug="two-sum-iii-data-structure-design" />
