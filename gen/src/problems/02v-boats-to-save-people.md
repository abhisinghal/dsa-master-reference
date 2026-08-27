# Two Pointers — Boats to Save People

*[↗ LeetCode: Boats to Save People](https://leetcode.com/problems/boats-to-save-people/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Amazon, Google, Meta" />

Each boat carries ≤ 2 people totaling ≤ `limit`. Minimize boats.

**Example 1** — `people=[1,2], limit=3` → `1`
**Example 2** — `people=[3,2,2,1], limit=3` → `3`
**Example 3** — `people=[3,5,3,4], limit=5` → `4`

**Constraints** — `1 ≤ n ≤ 5·10⁴`. Brute enumeration of all pairings is `(n/2)! ≈ 10²⁰⁰⁰⁰` — impossible. Sort + two-pointer greedy is O(n log n).


<Hints
  hint1="Sort first if the input isn't already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="boats-to-save-people" /> <Bookmark problem-slug="boats-to-save-people" />

<InterviewTimer problem-slug="boats-to-save-people" />



## Approach 1 — Brute enumerate pairings (reference)

**Intuition.** For each way to partition people into groups of 1 or 2 (each ≤ limit), count boats. Return the minimum.

**Complexity** — Time **O((n/2)!)** partitions. At n=10 that's 3,628,800 — feasible but stops there. Just state this for completeness. *In an interview* say "there's a greedy exchange argument that gives O(n log n)."

---

## Approach 2 — Sort + greedy two-pointer (canonical)

**Insight.** Sort. Pair the heaviest with the lightest if they fit; otherwise the heaviest goes alone.

**Why optimal — exchange argument.** If the heaviest person can't share with the lightest available, they can't share with anyone (everyone else is at least as heavy as the lightest). So the heaviest is *forced* into a boat alone or with the lightest — no other choice can help.

```java
int numRescueBoats(int[] people, int limit) {
    Arrays.sort(people);
    int l = 0, r = people.length - 1, boats = 0;
    while (l <= r) {
        if (people[l] + people[r] <= limit) l++;
        r--; boats++;
    }
    return boats;
}
```

<CodeTrace
  title="Sort + greedy two-pointer (canonical)"
  :values="['1', '2']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 1 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 1 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(1)**. *Say aloud in an interview:* "same 'heaviest + lightest' exchange argument as fair-pairing problems in Balanced Load Assignment and Sum-of-Pairs Minimization."

---

## Try it yourself

<JavaRunner problem-slug="boats-to-save-people" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Brute pairings | O((n/2)!) | O(n) | Reference; dies past n=12 |
| **Sort + greedy 2p** | **O(n log n)** | O(1) | **Canonical** |

## When to use which

- **"Pair heaviest + lightest greedy"** → applies to boats, task scheduling, item packing.
- **"3+ per boat"** → generalizes with DP or different greedy.

<AiCompanion problem-slug="boats-to-save-people" pattern-hint="two pointers" />

## Related problems

- [Two Sum II](/problems/two-sum-ii-input-array-is-sorted)
- [Assign Cookies](https://leetcode.com/problems/assign-cookies/)

<FeedbackWidget problem-slug="boats-to-save-people" />

<RelatedProblems problems="squares-of-a-sorted-array::Squares Of A Sorted Array|valid-palindrome-ii::Valid Palindrome II|sort-array-by-parity::Sort Array By Parity" />
