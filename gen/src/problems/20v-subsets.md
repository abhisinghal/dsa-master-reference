# Backtracking — Subsets

*[↗ LeetCode: Subsets](https://leetcode.com/problems/subsets/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Return **all** subsets of `nums` (the power set). Each distinct set once.

**Example** — `nums=[1,2,3]` → `[[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]` (8 subsets).

**Constraints** — `1 ≤ n ≤ 10`.

---

## Approach 1 — Iterative expansion

**Intuition.** Start with `[[]]`. For each new element `x`, append `x` to every existing subset.

```java
List<List<Integer>> subsetsIter(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    out.add(new ArrayList<>());
    for (int x : nums) {
        int size = out.size();
        for (int i = 0; i < size; i++) {
            List<Integer> copy = new ArrayList<>(out.get(i));
            copy.add(x);
            out.add(copy);
        }
    }
    return out;
}
```

**Complexity** — Time **O(n · 2ⁿ)**; Space **O(n · 2ⁿ)** output.

---

## Approach 2 — Backtracking with start index

**Insight.** For each position, decide "include current then advance" or "skip and advance." Post-recurse, un-choose. Emit at every node (not just leaves).

**Trap.** `remove(path.size()-1)` after every recurse. Otherwise sibling branches inherit stale state.

```java
List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    dfs(nums, 0, new ArrayList<>(), out);
    return out;
}
void dfs(int[] nums, int start, List<Integer> path, List<List<Integer>> out) {
    out.add(new ArrayList<>(path));                       // emit current
    for (int i = start; i < nums.length; i++) {
        path.add(nums[i]);                                 // choose
        dfs(nums, i + 1, path, out);                       // explore
        path.remove(path.size() - 1);                      // un-choose
    }
}
```

<CodeTrace
  title="Backtracking — nums=[1,2,3]"
  :values="[1,2,3]"
  :windowKeys="['start']"
  :cellWidth="46"
  :steps='[
    { pointers: { start: 0 }, vars: { path: "[]", found: 1 }, note: "emit []" },
    { pointers: { start: 1 }, vars: { path: "[1]", found: 2 }, note: "pick 1", added: [0] },
    { pointers: { start: 2 }, vars: { path: "[1,2]", found: 3 }, note: "pick 2", added: [0,1] },
    { pointers: { start: 3 }, vars: { path: "[1,2,3]", found: 4 }, note: "pick 3", added: [0,1,2] },
    { pointers: { start: 3 }, vars: { path: "[1,3]", found: 5 }, note: "backtrack; pick 3", added: [0,2] },
    { pointers: { start: 2 }, vars: { path: "[2]", found: 6 }, note: "new branch from idx 1", added: [1] },
    { pointers: { start: 3 }, vars: { path: "[3]", found: 8 }, note: "total 8", added: [2] }
  ]'
/>

**Complexity** — Time **O(n · 2ⁿ)**; Space **O(n)** stack + output.

---

## Approach 3 — Bitmask enumeration

**Insight from backtracking.** Every subset is a bitmask in `[0, 2ⁿ)`. Bit `k` set → include `nums[k]`.

```java
List<List<Integer>> subsetsBit(int[] nums) {
    int n = nums.length;
    List<List<Integer>> out = new ArrayList<>();
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> s = new ArrayList<>();
        for (int i = 0; i < n; i++)
            if ((mask & (1 << i)) != 0) s.add(nums[i]);
        out.add(s);
    }
    return out;
}
```

**Complexity** — Same. Cleaner code, harder to modify (e.g. deduping).

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Iterative expansion | O(n · 2ⁿ) | O(n · 2ⁿ) |
| Backtracking | O(n · 2ⁿ) | O(n) + output |
| Bitmask enumeration | O(n · 2ⁿ) | O(n) + output |

## When to use which

- **Cold interview** → iterative or backtracking. Bitmask if you're comfortable with bits.
- **Subsets with duplicates** → backtracking with `sort + skip while nums[i]==nums[i-1] && !used[i-1]`.
- **k-length subsets** → same skeleton, emit only when `path.size() == k`.

## Related problems

- [Subsets II (with duplicates)](https://leetcode.com/problems/subsets-ii/)
- [Combinations](https://leetcode.com/problems/combinations/) — fixed-size subsets
- [Permutations](https://leetcode.com/problems/permutations/) — all orderings, not subsets
- [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) — same enumeration, additional constraint
