# Two Pointers — Boats to Save People

*[↗ LeetCode: Boats to Save People](https://leetcode.com/problems/boats-to-save-people/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/two-pointers)

&lt;CompanyTags companies="Amazon, Google, Meta" /&gt;

Each boat carries ≤ 2 people totaling ≤ `limit`. Minimize boats.

**Example 1** — `people=[1,2], limit=3` → `1`
**Example 2** — `people=[3,2,2,1], limit=3` → `3`
**Example 3** — `people=[3,5,3,4], limit=5` → `4`

**Constraints** — `1 ≤ n ≤ 5·10⁴`.


&lt;Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/&gt;
---

&lt;MarkSolved problem-slug="boats-to-save-people" /&gt; &lt;Bookmark problem-slug="boats-to-save-people" /&gt;

&lt;InterviewTimer problem-slug="boats-to-save-people" /&gt;



## Approach — Sort + greedy two-pointer (canonical)

**Insight.** Sort. Pair heaviest with lightest if possible; otherwise heaviest goes alone.

**Why optimal.** If heaviest can't pair with lightest, they can't pair with anyone.



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

**Complexity** — Time **O(n log n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="boats-to-save-people" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sort + greedy | **O(n log n)** | O(1) | canonical |

## When to use which

- **"Pair heaviest + lightest greedy"** → applies to boats, task scheduling, item packing.
- **"3+ per boat"** → generalizes with DP or different greedy.

&lt;AiCompanion problem-slug="boats-to-save-people" pattern-hint="two pointers" /&gt;

## Related problems

- [Two Sum II](/problems/two-sum-ii-input-array-is-sorted)
- [Assign Cookies](https://leetcode.com/problems/assign-cookies/)

&lt;FeedbackWidget problem-slug="boats-to-save-people" /&gt;

&lt;RelatedProblems problems="squares-of-a-sorted-array::Squares Of A Sorted Array|valid-palindrome-ii::Valid Palindrome II|sort-array-by-parity::Sort Array By Parity" /&gt;
