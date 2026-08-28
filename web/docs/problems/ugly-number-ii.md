# K-way Merge — Ugly Number II

*[↗ LeetCode: Ugly Number II](https://leetcode.com/problems/ugly-number-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/k-way-merge)

<CompanyTags companies="Amazon, Google, Meta" />

An **ugly number** has only 2, 3, or 5 as prime factors. `1` is ugly by convention. Return the `n`-th ugly number.

**Example 1** — `n = 10` → `12` (sequence `1, 2, 3, 4, 5, 6, 8, 9, 10, 12`)
**Example 2** — `n = 1` → `1`
**Example 3** — `n = 11` → `15`

**Constraints** — `1 ≤ n ≤ 1690`. Brute checks every integer for 2/3/5-only factorisation — O(N·log N) where N = the 1690th ugly number ≈ 2·10⁹ (dies past 1 min). Three-pointer merge from {2,3,5} is O(n) = 10³ ops = &lt;1 microsec, scales to 10⁶ queries/sec.
<Hints
  hint1="You have k sorted sequences. Which element is globally next?"
  hint2="Min-heap of size k, one head per list. Pop smallest, emit, push its successor from the same list."
  hint3="For ’smallest range covering k lists’, track max-in-heap; window is [minInHeap, maxSeen]."
/>
---

<MarkSolved problem-slug="ugly-number-ii" /> <Bookmark problem-slug="ugly-number-ii" />

<InterviewTimer problem-slug="ugly-number-ii" />



## Approach 1 — Test each candidate

**Intuition.** For each integer, divide by 2, 3, 5 repeatedly; if it reduces to 1, it's ugly.

**Complexity** — Time up to **O(n · answer log answer)** — too slow.

---

## Approach 2 — Min-heap merge of 3 streams

**Insight.** Every ugly number `u > 1` is `2·u'` or `3·u'` or `5·u'` where `u'` is a smaller ugly number. So the sequence is the sorted merge of three streams: `{2·u_i}`, `{3·u_i}`, `{5·u_i}`.

- Push `1` into heap; track seen set for dedup.
- Pop `x` (n-th pop = answer). Push `2x, 3x, 5x` if unseen.



```java
int nthUglyNumberHeap(int n) {
    PriorityQueue<Long> pq = new PriorityQueue<>();
    Set<Long> seen = new HashSet<>();
    pq.offer(1L); seen.add(1L);
    long ans = 1;
    int[] primes = {2, 3, 5};
    for (int i = 0; i < n; i++) {
        ans = pq.poll();
        for (int p : primes) {
            long next = ans * p;
            if (seen.add(next)) pq.offer(next);
        }
    }
    return (int) ans;
}
```



**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Approach 3 — Three pointers (canonical O(n))

**Insight from heap.** Instead of a heap + seen set, maintain three indices `i2, i3, i5` into the growing ugly array. Next ugly = `min(ugly[i2]*2, ugly[i3]*3, ugly[i5]*5)`. Advance whichever pointer(s) produced the minimum — **all of them** if tied — to skip duplicates.



```java
int nthUglyNumber(int n) {
    int[] ugly = new int[n];
    ugly[0] = 1;
    int i2 = 0, i3 = 0, i5 = 0;
    for (int i = 1; i < n; i++) {
        int next2 = ugly[i2] * 2, next3 = ugly[i3] * 3, next5 = ugly[i5] * 5;
        int next = Math.min(next2, Math.min(next3, next5));
        ugly[i] = next;
        if (next == next2) i2++;
        if (next == next3) i3++;
        if (next == next5) i5++;
    }
    return ugly[n - 1];
}
```



<CodeTrace
  title="3-pointer — first few ugly numbers"
  :values="['1','2','3','4','5','6','8','9','10','12']"
  :windowKeys="['i2','i3','i5']"
  :cellWidth="30"
  :steps='[
    { pointers: { i2: 0, i3: 0, i5: 0 }, vars: { candidates: "2,3,5", pick: 2 }, note: "ugly[1]=2; i2++" },
    { pointers: { i2: 1, i3: 0, i5: 0 }, vars: { candidates: "4,3,5", pick: 3 }, note: "ugly[2]=3; i3++" },
    { pointers: { i2: 1, i3: 1, i5: 0 }, vars: { candidates: "4,6,5", pick: 4 }, note: "ugly[3]=4; i2++" },
    { pointers: { i2: 2, i3: 1, i5: 0 }, vars: { candidates: "6,6,5", pick: 5 }, note: "ugly[4]=5; i5++" },
    { pointers: { i2: 2, i3: 1, i5: 1 }, vars: { candidates: "6,6,10", pick: 6 }, note: "ugly[5]=6; both i2 and i3 advance" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)** for the array.

---

## Try it yourself

<JavaRunner problem-slug="ugly-number-ii" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Test each integer | very slow | O(1) | baseline |
| Min-heap merge | O(n log n) | O(n) | correct, uses heap pattern |
| Three-pointer merge | **O(n)** | **O(n)** | canonical answer |

## When to use which

- **Standard** → three-pointer merge.
- **"With k primes, not just {2,3,5}"** → generalize to k pointers; O(nk).
- **"Super ugly numbers"** → same, with `primes[]` given; min-heap gets simpler than k pointers.
- **"nth prime" or "smallest k of type X"** → same merge template if `x` is a closed set.

<AiCompanion problem-slug="ugly-number-ii" pattern-hint="k-way merge" />

## Related problems

- [Super Ugly Number](https://leetcode.com/problems/super-ugly-number/) — k-primes generalization
- [Merge k Sorted Lists](/problems/k-way-merge-k-sorted-lists) — the pattern seed
- [Perfect Squares](/problems/perfect-squares) — DP alternative

<FeedbackWidget problem-slug="ugly-number-ii" />

<RelatedProblems problems="reorganize-string::Reorganize String|kth-largest-element-in-a-stream::Kth Largest Element In A Stream|smallest-range-covering-elements-from-k-lists::Smallest Range Covering Elements From K Lists" />
