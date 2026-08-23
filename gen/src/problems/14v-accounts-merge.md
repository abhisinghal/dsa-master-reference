# Union-Find — Accounts Merge

*[↗ LeetCode: Accounts Merge](https://leetcode.com/problems/accounts-merge/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/union-find)

<CompanyTags companies="Meta, Amazon, Google" />

Given accounts `[name, email1, email2, …]`, merge accounts sharing any email into one. Return merged accounts with emails sorted.

**Example 1** — Given John/Mary accounts with overlapping emails → merged into deduplicated groups.
**Example 2** — All distinct → unchanged.

**Constraints** — total emails ≤ 30·10³.


<Hints
  hint1="Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?"
  hint2="Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n)."
  hint3="For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
/>
---

<MarkSolved problem-slug="accounts-merge" /> <Bookmark problem-slug="accounts-merge" />

<InterviewTimer problem-slug="accounts-merge" />



## Approach 1 — DFS on email graph

Build graph with emails as nodes, connect emails within the same account. DFS to find components. O(N·α).

## Approach 2 — Union-Find on email index (canonical)

**Insight.** Assign each email an index; union all emails within each account. Group emails by root; attach owner's name.

```java
List<List<String>> accountsMerge(List<List<String>> accounts) {
    Map<String, Integer> emailIdx = new HashMap<>();
    Map<String, String> emailName = new HashMap<>();
    int idx = 0;
    for (List<String> acc : accounts)
        for (int i = 1; i < acc.size(); i++) {
            if (!emailIdx.containsKey(acc.get(i))) emailIdx.put(acc.get(i), idx++);
            emailName.put(acc.get(i), acc.get(0));
        }
    int[] parent = new int[idx];
    for (int i = 0; i < idx; i++) parent[i] = i;
    for (List<String> acc : accounts)
        for (int i = 2; i < acc.size(); i++)
            union(parent, emailIdx.get(acc.get(1)), emailIdx.get(acc.get(i)));
    Map<Integer, TreeSet<String>> groups = new HashMap<>();
    for (var e : emailIdx.entrySet()) {
        int r = find(parent, e.getValue());
        groups.computeIfAbsent(r, k -> new TreeSet<>()).add(e.getKey());
    }
    List<List<String>> out = new ArrayList<>();
    for (var e : groups.entrySet()) {
        List<String> row = new ArrayList<>();
        row.add(emailName.get(e.getValue().first()));
        row.addAll(e.getValue());
        out.add(row);
    }
    return out;
}
int find(int[] p, int x) { return p[x] == x ? x : (p[x] = find(p, p[x])); }
void union(int[] p, int a, int b) { p[find(p, a)] = find(p, b); }
```

**Complexity** — Time **O(N · α(N) · log N)** (sort within group); Space **O(N)**.

---

## Try it yourself

<JavaRunner problem-slug="accounts-merge" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| DFS components | O(N·α) | O(N) | acceptable |
| Union-Find | **O(N·α·log N)** | O(N) | canonical |

## When to use which

- **Dynamic merging of sets by shared attribute** → Union-Find.
- **Static / one-shot** → DFS is fine.
- **"Return count of merged accounts"** → count distinct roots.

<AiCompanion problem-slug="accounts-merge" pattern-hint="union-find" />

## Related problems

- [Number of Provinces](/problems/union-find-number-of-provinces)
- [Redundant Connection](/problems/redundant-connection)
- [Most Stones Removed with Same Row or Column](/problems/most-stones-removed-with-same-row-or-column)

<FeedbackWidget problem-slug="accounts-merge" />

<RelatedProblems problems="min-cost-to-connect-all-points::Min Cost To Connect All Points|connecting-cities-with-minimum-cost::Connecting Cities With Minimum Cost|most-stones-removed-with-same-row-or-column::Most Stones Removed With Same Row Or Column" />
