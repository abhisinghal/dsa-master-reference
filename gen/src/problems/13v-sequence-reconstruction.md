# Topological Sort — Sequence Reconstruction

*[↗ LeetCode: Sequence Reconstruction](https://leetcode.com/problems/sequence-reconstruction/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/topological-sort)

Given a target `nums` and a list of `sequences` (subsequences of `nums`), return `true` iff there is exactly ONE topological order consistent with all sequences and it equals `nums`.

**Example** — `nums=[1,2,3], sequences=[[1,2],[1,3]]` → `false` (both [1,2,3] and [1,3,2] work)

---

## Approach 1 — Kahn's with uniqueness check

**Insight.** Build the DAG from `sequences`. Kahn's; at every layer, if the queue has ≥ 2 candidates, the order isn't unique → false. Compare with `nums` element by element.

```java
boolean sequenceReconstruction(int[] nums, List<List<Integer>> sequences) {
    int n = nums.length;
    Map<Integer, Set<Integer>> adj = new HashMap<>();
    int[] indeg = new int[n + 1];
    for (int i = 1; i <= n; i++) adj.put(i, new HashSet<>());
    for (List<Integer> seq : sequences)
        for (int i = 0; i < seq.size() - 1; i++)
            if (adj.get(seq.get(i)).add(seq.get(i + 1))) indeg[seq.get(i + 1)]++;
    Deque<Integer> q = new ArrayDeque<>();
    for (int i = 1; i <= n; i++) if (indeg[i] == 0) q.offer(i);
    int idx = 0;
    while (!q.isEmpty()) {
        if (q.size() > 1) return false;                              // not unique
        int u = q.poll();
        if (u != nums[idx++]) return false;                          // doesn't match target
        for (int v : adj.get(u)) if (--indeg[v] == 0) q.offer(v);
    }
    return idx == n;
}
```

<CodeTrace
  title="Uniqueness check — nums=[1,2,3], sequences=[[1,2],[1,3]]"
  :values="[1,2,3]"
  :windowKeys="['step']"
  :cellWidth="46"
  :steps='[
    { pointers: { step: 0 }, vars: { queue: "[1]", "size": 1 }, note: "start; unique" },
    { pointers: { step: 1 }, vars: { queue: "[2,3]", "size": 2 }, note: "after popping 1: queue has 2 candidates → not unique → false", removed: [1,2] }
  ]'
/>

**Complexity** — Time **O(V + E)**; Space **O(V + E)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Kahn's + uniqueness | **O(V + E)** | O(V + E) |

## Related problems

- [Course Schedule II](/problems/topological-sort-course-schedule) — return any valid order
- [Alien Dictionary](/problems/alien-dictionary) — derive DAG from adjacent pairs
