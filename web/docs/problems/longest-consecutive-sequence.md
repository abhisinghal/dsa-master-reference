# Hashing — Longest Consecutive Sequence

*[↗ LeetCode: Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

&lt;CompanyTags companies="Meta, Amazon, Google, Microsoft" /&gt;

Given an unsorted integer array `nums`, return the length of the longest **consecutive** elements sequence. Must run in **O(n)** time.

**Example 1** — `nums = [100,4,200,1,3,2]` → `4` (`[1,2,3,4]`)
**Example 2** — `nums = [0,3,7,2,5,8,4,6,0,1]` → `9` (`[0..8]`)
**Example 3** — `nums = []` → `0`

**Constraints** — `0 ≤ n ≤ 10⁵`; `-10⁹ ≤ nums[i] ≤ 10⁹`.


&lt;Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/&gt;
---

## Approach 1 — Sort, then walk

**Intuition.** Sort. Walk pairwise; increment a running length on each `+1` step; break otherwise. Skip duplicates.



```java
int longestConsecutiveSort(int[] nums) {
    if (nums.length == 0) return 0;
    int[] a = nums.clone();
    Arrays.sort(a);
    int best = 1, run = 1;
    for (int i = 1; i < a.length; i++) {
        if (a[i] == a[i - 1]) continue;
        if (a[i] == a[i - 1] + 1) run++;
        else run = 1;
        best = Math.max(best, run);
    }
    return best;
}
```



**Complexity** — Time **O(n log n)**; Space **O(n)** clone. Rejected by the spec (needs O(n)).

---

## Approach 2 — Set + only start from sequence heads

**Insight from sort.** Put all nums into a `HashSet`. For each element, only *start* counting a run if `x - 1` is **not** in the set (making `x` a sequence head). Then extend forward. Every element is visited by the inner extension at most once — total **O(n)**.

**Trap** — without the "head" check, an element in the middle of a long run walks the entire run each time → O(n²) worst case.



```java
int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int x : nums) set.add(x);
    int best = 0;
    for (int x : set) {
        if (set.contains(x - 1)) continue;   // not a head
        int len = 1;
        while (set.contains(x + len)) len++;
        best = Math.max(best, len);
    }
    return best;
}
```



<CodeTrace
  title="Set + heads — nums=[100,4,200,1,3,2]"
  :values="['1','2','3','4','100','200']"
  :windowKeys="['x','len']"
  :cellWidth="34"
  :steps='[
    { pointers: { x: 0, len: 1 }, vars: { head: "1 (no 0 in set)", }, note: "x=1 is head; start len=1" },
    { pointers: { x: 0, len: 4 }, vars: { extend: "1→2→3→4" }, note: "extend forward while x+len exists; len=4" },
    { pointers: { x: 4, len: 1 }, vars: { head: "100" }, note: "x=100 is a head (no 99); alone, len=1" },
    { pointers: { x: 5, len: 1 }, vars: { head: "200", best: 4 }, note: "final best=4" }
  ]'
/>

**Complexity** — Time **O(n)** amortized; Space **O(n)**.

---

## Approach 3 — Union-Find (extendable variant)

**Insight.** Union `x` with `x-1` and `x+1` whenever both exist in the set. The largest component gives the answer. Same **O(n · α(n))** ≈ O(n).



```java
int longestConsecutiveUF(int[] nums) {
    Map<Integer, Integer> parent = new HashMap<>(), rank = new HashMap<>();
    for (int x : nums) if (!parent.containsKey(x)) { parent.put(x, x); rank.put(x, 1); }
    for (int x : nums) {
        if (parent.containsKey(x - 1)) union(parent, rank, x, x - 1);
        if (parent.containsKey(x + 1)) union(parent, rank, x, x + 1);
    }
    return rank.values().stream().max(Integer::compareTo).orElse(0);
}
int find(Map<Integer,Integer> p, int x) { return p.get(x) == x ? x : (p.put(x, find(p, p.get(x))) == null ? x : find(p, p.get(x))); }
void union(Map<Integer,Integer> p, Map<Integer,Integer> r, int a, int b) {
    int ra = find(p, a), rb = find(p, b);
    if (ra == rb) return;
    if (r.get(ra) < r.get(rb)) { int t = ra; ra = rb; rb = t; }
    p.put(rb, ra); r.merge(ra, r.get(rb), Integer::sum);
}
```



**Complexity** — Time **O(n · α(n))**; Space **O(n)**. Handy for streaming inputs where "add" operations must extend runs.

---

## Try it yourself

<JavaRunner problem-slug="longest-consecutive-sequence" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Sort + walk | O(n log n) | O(n) | rejected by spec |
| Set + heads | **O(n)** | O(n) | canonical answer |
| Union-Find | O(n · α(n)) | O(n) | polish; streaming variant |

## When to use which

- **Standard interview answer** → set + heads.
- **Streaming input** ("insert one number at a time, query longest run") → Union-Find with per-insert union.
- **"Return the actual sequence"** → track the head and length of the best run; slice.
- **"Longest arithmetic progression"** — different problem (DP).

&lt;AiCompanion problem-slug="longest-consecutive-sequence" pattern-hint="hashing" /&gt;

## Related problems

- [Number of Islands](/problems/number-of-islands) — same "connected component" mindset
- [Longest Substring Without Repeating Characters](/problems/sliding-window-longest-substring) — sliding-window sibling
- [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — hash-key grouping