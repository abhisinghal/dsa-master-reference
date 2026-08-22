# Hashing — Word Ladder

*[↗ LeetCode: Word Ladder](https://leetcode.com/problems/word-ladder/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/bfs)

Transform `beginWord` → `endWord` by changing one letter at a time; each intermediate must be in dict. Return length (or 0).

---

## Approach 1 — BFS over full word graph
Naïvely, edges are all word pairs differing in 1 char → **O(N² · L)** to build.

---

## Approach 2 — BFS via wildcard-key hashing
**Insight.** For each word, generate `L` patterns like `"h*t"`, `"*ot"` and bucket words by pattern. Two words are neighbors iff they share a wildcard bucket. Traversal touches each pattern once.

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

---

## Approach 3 — Bidirectional BFS
Expand from both ends; stop when frontiers meet. Roughly halves the exponent → O(2 · b^(d/2)).

**Complexity** — Time **O(N · L²)**; Space **O(N · L²)** for buckets.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| BFS over full word graph | O(N² · L) | — | baseline |
| BFS via wildcard-key hashing | — | — | improved |
| Bidirectional BFS | O(N · L²) | O(N · L²) | optimum |

## When to use which

- **State it for signal** → BFS over full word graph (O(N² · L)). Correct baseline; call it out then move on.
- **Intermediate refinement** → BFS via wildcard-key hashing (—).
- **Ship this** → Bidirectional BFS (O(N · L²), O(N · L²)). Expected optimum in interview.

## Related problems

- [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) — return all paths, needs parent map + DFS reconstruct
- [Minimum Genetic Mutation](https://leetcode.com/problems/minimum-genetic-mutation/) — same pattern
