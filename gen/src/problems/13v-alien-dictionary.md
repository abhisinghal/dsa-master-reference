# Topological Sort — Alien Dictionary

*[↗ LeetCode: Alien Dictionary](https://leetcode.com/problems/alien-dictionary/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/topological-sort)

<CompanyTags companies="Meta, Amazon, Google, LinkedIn, Uber" />

Given words sorted alphabetically in an alien language, return the character order. Return `""` if impossible.

**Example 1** — `words=["wrt","wrf","er","ett","rftt"]` → `"wertf"`
**Example 2** — `words=["z","x"]` → `"zx"`
**Example 3** — `words=["z","x","z"]` → `""` (cycle)

**Constraints** — `1 ≤ words.length ≤ 100`; `1 ≤ words[i].length ≤ 100`; lowercase English.


<Hints
  hint1="Directed graph? Prerequisites? You need topological order."
  hint2="Kahn’s BFS: start from nodes with indeg 0; when you pop, decrement neighbors’ indeg; add new zeros."
  hint3="For ’layers/semesters’, process one full BFS layer per timestep. For ’unique order?’, check queue size ≤ 1 at every step."
/>
---

<MarkSolved problem-slug="alien-dictionary" />

<InterviewTimer problem-slug="alien-dictionary" />



## Approach 1 — Trial-and-error permutation

Try every char ordering. O(26!). Absurd baseline.

## Approach 2 — Build precedence graph + Kahn's BFS toposort (canonical)

**Insight.** From each adjacent pair `(a, b)` in the sorted list, find the first differing char — this is a directed edge `a[i] → b[i]`. Then topological sort the graph. Return `""` if there's a cycle OR if `b` is a strict prefix of `a` (invalid ordering).

```java
String alienOrder(String[] words) {
    Map<Character, Set<Character>> g = new HashMap<>();
    Map<Character, Integer> indeg = new HashMap<>();
    for (String w : words) for (char c : w.toCharArray()) indeg.putIfAbsent(c, 0);
    for (int i = 0; i + 1 < words.length; i++) {
        String a = words[i], b = words[i+1];
        if (a.length() > b.length() && a.startsWith(b)) return "";
        for (int j = 0; j < Math.min(a.length(), b.length()); j++) {
            if (a.charAt(j) != b.charAt(j)) {
                g.computeIfAbsent(a.charAt(j), k -> new HashSet<>());
                if (g.get(a.charAt(j)).add(b.charAt(j))) indeg.merge(b.charAt(j), 1, Integer::sum);
                break;
            }
        }
    }
    Queue<Character> q = new ArrayDeque<>();
    for (var e : indeg.entrySet()) if (e.getValue() == 0) q.offer(e.getKey());
    StringBuilder sb = new StringBuilder();
    while (!q.isEmpty()) {
        char c = q.poll();
        sb.append(c);
        for (char nxt : g.getOrDefault(c, Set.of()))
            if (indeg.merge(nxt, -1, Integer::sum) == 0) q.offer(nxt);
    }
    return sb.length() == indeg.size() ? sb.toString() : "";
}
```

<CodeTrace
  title="Toposort — words=['wrt','wrf','er','ett','rftt']"
  :values="['w','e','r','t','f']"
  :windowKeys="['step']"
  :cellWidth="30"
  :steps='[
    { pointers: { step: 0 }, vars: { edges: "w→e, r→t, t→f, e→r" }, note: "extracted from adjacent pairs" },
    { pointers: { step: 1 }, vars: { indeg: "w:0,e:1,r:1,t:1,f:1" }, note: "" },
    { pointers: { step: 2 }, vars: { order: "wertf" }, note: "BFS toposort" }
  ]'
/>

**Complexity** — Time **O(C)** where C = total characters; Space **O(1)** (bounded alphabet).

---

## Try it yourself

<JavaRunner problem-slug="alien-dictionary" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Trial-and-error | O(26!) | O(1) | trivia |
| Kahn's BFS toposort | **O(C)** | **O(1)** | canonical |

## When to use which

- **"Any valid order"** → Kahn's BFS.
- **"Lex-smallest topological order"** → replace queue with min-heap.
- **DFS-based alternative** → recursion + reverse post-order; same complexity.

<AiCompanion problem-slug="alien-dictionary" pattern-hint="topological sort" />

## Related problems

- [Course Schedule](/problems/topological-sort-course-schedule)
- [Sequence Reconstruction](/problems/sequence-reconstruction)
- [Parallel Courses](/problems/parallel-courses)

<FeedbackWidget problem-slug="alien-dictionary" />

<RelatedProblems problems="course-schedule::Course Schedule|sequence-reconstruction::Sequence Reconstruction|parallel-courses::Parallel Courses" />
