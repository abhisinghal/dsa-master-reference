# Top-K / Heap — Reorganize String

*[↗ LeetCode: Reorganize String](https://leetcode.com/problems/reorganize-string/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/top-k-heap)

<CompanyTags companies="Meta, Amazon, Google, Bloomberg" />

Given string `s`, rearrange characters so no two adjacent characters are the same. Return the result, or `""` if impossible.

**Example 1** — `s = "aab"` → `"aba"`
**Example 2** — `s = "aaab"` → `""` (a appears too often)
**Example 3** — `s = "vvvlo"` → `"vlvov"` (one valid arrangement)

**Constraints** — `1 ≤ n ≤ 500`. Lowercase English.


<Hints
  hint1="You need the k largest/smallest. Sort is O(n log n). Can you do O(n log k)?"
  hint2="Maintain a heap of size k. Min-heap → k largest at root candidates; max-heap → k smallest."
  hint3="For ’k closest’ or ’k most frequent’, the heap’s comparator holds the distance/frequency metric."
/>
---

## Approach 1 — Try all permutations (backtracking)

O(n!). Baseline; only correct for tiny n.

## Approach 2 — Max-heap by frequency (greedy)

**Insight.** At each step, place the most-frequent remaining char (that isn't the same as the previous placed char). If we ever can't place, return `""`.

**Feasibility check.** Impossible iff some char count > `(n + 1) / 2`.

```java
String reorganizeString(String s) {
    int[] cnt = new int[26];
    for (char c : s.toCharArray()) cnt[c - 'a']++;
    int max = 0, maxIdx = 0;
    for (int i = 0; i < 26; i++) if (cnt[i] > max) { max = cnt[i]; maxIdx = i; }
    if (max > (s.length() + 1) / 2) return "";

    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[1] - a[1]);
    for (int i = 0; i < 26; i++) if (cnt[i] > 0) pq.offer(new int[]{i, cnt[i]});

    StringBuilder sb = new StringBuilder();
    while (pq.size() >= 2) {
        int[] a = pq.poll();
        int[] b = pq.poll();
        sb.append((char) ('a' + a[0]));
        sb.append((char) ('a' + b[0]));
        if (--a[1] > 0) pq.offer(a);
        if (--b[1] > 0) pq.offer(b);
    }
    if (!pq.isEmpty()) sb.append((char) ('a' + pq.peek()[0]));
    return sb.toString();
}
```

<CodeTrace
  title="Max-heap — s='aab'"
  :values="['a','a','b']"
  :windowKeys="['step']"
  :cellWidth="34"
  :steps='[
    { pointers: { step: 0 }, vars: { heap: "[a:2, b:1]" }, note: "counts" },
    { pointers: { step: 1 }, vars: { pop: "a,b", sb: "ab", heap: "[a:1]" }, note: "place a then b" },
    { pointers: { step: 2 }, vars: { sb: "aba" }, note: "one left → append; result aba" }
  ]'
/>

**Complexity** — Time **O(n log σ)**; Space **O(σ)**.

---

## Approach 3 — Bucket placement (O(n) without heap)

**Insight from heap.** Sort chars by frequency; place the most-frequent char at even indices `0, 2, 4, …`, then wrap remaining chars into remaining slots. As long as `max ≤ (n+1)/2` this works.

```java
String reorganizeBucket(String s) {
    int n = s.length();
    int[] cnt = new int[26];
    for (char c : s.toCharArray()) cnt[c - 'a']++;
    int max = 0, letter = 0;
    for (int i = 0; i < 26; i++) if (cnt[i] > max) { max = cnt[i]; letter = i; }
    if (max > (n + 1) / 2) return "";

    char[] out = new char[n];
    int idx = 0;
    // place most-frequent first
    while (cnt[letter]-- > 0) { out[idx] = (char) ('a' + letter); idx += 2; }
    // rest
    for (int i = 0; i < 26; i++) {
        while (cnt[i]-- > 0) {
            if (idx >= n) idx = 1;
            out[idx] = (char) ('a' + i);
            idx += 2;
        }
    }
    return new String(out);
}
```

**Complexity** — Time **O(n + σ)**; Space **O(σ)**.

---

## Try it yourself

<JavaRunner problem-slug="reorganize-string" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Backtracking | O(n!) | O(n) | baseline |
| Max-heap greedy | **O(n log σ)** | O(σ) | canonical |
| Bucket placement | O(n + σ) | O(σ) | polish — no heap |

## When to use which

- **Standard answer** → max-heap greedy.
- **Interviewer asks "no heap?"** → bucket placement.
- **"K-length gap between duplicates"** → this generalizes: [Rearrange String k Distance Apart](https://leetcode.com/problems/rearrange-string-k-distance-apart/).
- **"Task scheduling with cooldown"** → same skeleton; see [Task Scheduler](https://leetcode.com/problems/task-scheduler/).

<AiCompanion problem-slug="reorganize-string" pattern-hint="top-K / heap" />

## Related problems

- [Task Scheduler](https://leetcode.com/problems/task-scheduler/) — same greedy
- [Rearrange String k Distance Apart](https://leetcode.com/problems/rearrange-string-k-distance-apart/) — k-generalization
- [Top K Frequent Elements](/problems/top-k-frequent-elements)