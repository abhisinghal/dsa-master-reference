# Hashing — Word Ladder

*[↗ LeetCode: Word Ladder](https://leetcode.com/problems/word-ladder/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/bfs)

<CompanyTags companies="Amazon, Meta, Google" />

Transform `beginWord` → `endWord` by changing one letter at a time; each intermediate must be in dict. Return length.

**Example 1** — `beginWord="hit", endWord="cog", wordList=["hot","dot","dog","lot","log","cog"]` → `5`
**Example 2** — Same words minus "cog" → `0`

**Constraints** — `1 ≤ L ≤ 10`; `1 ≤ #words ≤ 5000`. Brute BFS over all pairs is O(N²·L) = 10¹⁰ ops at N=5·10³, L=10 (TLE). Bidirectional BFS with wildcard-bucket adjacency is O(N·L²·26) = ~10⁶ ops.
<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="word-ladder" /> <Bookmark problem-slug="word-ladder" />

<InterviewTimer problem-slug="word-ladder" />



## Approach 1 — BFS over all pairs

Build edges by comparing every pair. O(N² · L). TLE.

## Approach 2 — Wildcard buckets + BFS (canonical)

**Insight.** For each word, generate patterns like `"h*t"`, `"*ot"`. Words share a bucket iff neighbors. BFS traverses via buckets.

```java
int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> dict = new HashSet<>(wordList);
    if (!dict.contains(endWord)) return 0;
    Map<String, List<String>> buckets = new HashMap<>();
    for (String w : dict)
        for (int i = 0; i < w.length(); i++) {
            String k = w.substring(0, i) + "*" + w.substring(i + 1);
            buckets.computeIfAbsent(k, x -> new ArrayList<>()).add(w);
        }
    Queue<String> q = new ArrayDeque<>();
    Set<String> seen = new HashSet<>();
    q.add(beginWord); seen.add(beginWord);
    int steps = 1;
    while (!q.isEmpty()) {
        for (int sz = q.size(); sz > 0; sz--) {
            String w = q.poll();
            if (w.equals(endWord)) return steps;
            for (int i = 0; i < w.length(); i++) {
                String k = w.substring(0, i) + "*" + w.substring(i + 1);
                for (String nb : buckets.getOrDefault(k, List.of()))
                    if (seen.add(nb)) q.add(nb);
            }
        }
        steps++;
    }
    return 0;
}
```

<CodeTrace
  title="BFS over all pairs"
  :values="['hot', 'dot', 'dog', 'lot', 'log', 'cog']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 3 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 5 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

## Approach 3 — Bidirectional BFS
Expand from both ends until frontiers meet. ~O(2 · b^(d/2)).

**Complexity** — Time **O(N · L²)**; Space **O(N · L²)**.

---

## Try it yourself

<JavaRunner problem-slug="word-ladder" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| All-pair edges | O(N²·L) | O(N²) | TLE |
| Wildcard buckets | **O(N · L²)** | O(N · L²) | canonical |
| Bidirectional | O(√ of above) | same | polish |

## When to use which

- **Shortest transformation** → BFS + wildcards.
- **All paths** → [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) — parent map + DFS.
- **Very deep search** → bidirectional.

<AiCompanion problem-slug="word-ladder" pattern-hint="hashing" />

## Related problems

- [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/)
- [Minimum Genetic Mutation](https://leetcode.com/problems/minimum-genetic-mutation/)
- [Open the Lock](https://leetcode.com/problems/open-the-lock/)

<FeedbackWidget problem-slug="word-ladder" />
