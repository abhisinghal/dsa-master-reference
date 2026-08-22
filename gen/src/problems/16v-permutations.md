# Backtracking — Permutations

*[↗ LeetCode: Permutations](https://leetcode.com/problems/permutations/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/backtracking)

Return **all permutations** of `nums` (all values distinct).

**Example** — `nums=[1,2,3]` → `[[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]`

**Constraints** — `1 ≤ n ≤ 6`; values distinct.

---

## Approach 1 — Insert-into-every-position

**Intuition.** Start with `[[]]`. For each new element, insert it at every position in every existing permutation.

```java
List<List<Integer>> permuteIter(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    out.add(new ArrayList<>());
    for (int x : nums) {
        List<List<Integer>> next = new ArrayList<>();
        for (List<Integer> p : out)
            for (int i = 0; i <= p.size(); i++) {
                List<Integer> copy = new ArrayList<>(p);
                copy.add(i, x);
                next.add(copy);
            }
        out = next;
    }
    return out;
}
```

**Complexity** — Time **O(n · n!)**; Space **O(n · n!)** output.

---

## Approach 2 — Backtracking with `used[]` (canonical)

**Insight.** DFS through positions 0..n-1; at each, pick any not-yet-used value.

```java
List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    dfs(nums, new boolean[nums.length], new ArrayList<>(), out);
    return out;
}
void dfs(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> out) {
    if (path.size() == nums.length) { out.add(new ArrayList<>(path)); return; }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        used[i] = true; path.add(nums[i]);
        dfs(nums, used, path, out);
        used[i] = false; path.remove(path.size() - 1);
    }
}
```

<CodeTrace
  title="Backtracking — nums=[1,2,3]"
  :values="[1,2,3]"
  :windowKeys="['pos']"
  :cellWidth="46"
  :steps='[
    { pointers: { pos: 0 }, vars: { path: "[1]" }, note: "pos 0: pick 1", added: [0] },
    { pointers: { pos: 1 }, vars: { path: "[1,2]" }, note: "pos 1: pick 2", added: [0,1] },
    { pointers: { pos: 2 }, vars: { path: "[1,2,3]" }, note: "emit 123", added: [0,1,2] },
    { pointers: { pos: 1 }, vars: { path: "[1,3]" }, note: "backtrack; pick 3", added: [0,2] },
    { pointers: { pos: 0 }, vars: { path: "[2]" }, note: "backtrack to pos 0; pick 2", added: [1] },
    { pointers: { pos: 0 }, vars: { path: "[3]" }, note: "and pick 3. 6 total", added: [2] }
  ]'
/>

**Complexity** — Time **O(n · n!)**; Space **O(n)** stack + output.

---

## Approach 3 — Swap-in-place (O(1) extra beyond output)

**Insight.** Instead of `used[]`, swap the pivot value with each `i ≥ pos`, recurse on `pos+1`, then swap back.

```java
List<List<Integer>> permuteSwap(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    swap(0, nums, out);
    return out;
}
void swap(int pos, int[] a, List<List<Integer>> out) {
    if (pos == a.length) {
        List<Integer> copy = new ArrayList<>();
        for (int x : a) copy.add(x);
        out.add(copy);
        return;
    }
    for (int i = pos; i < a.length; i++) {
        int t = a[pos]; a[pos] = a[i]; a[i] = t;
        swap(pos + 1, a, out);
        t = a[pos]; a[pos] = a[i]; a[i] = t;
    }
}
```

**Complexity** — Same as backtracking; no `used[]` array.

---

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Insert-into-every-position | O(n · n!) | O(n · n!) |
| Backtracking with `used[]` | **O(n · n!)** | O(n) + output |
| Swap-in-place | **O(n · n!)** | O(1) + output |

## When to use which

- **Cold interview** → backtracking with `used[]` — easiest to explain.
- **Space-conscious** → swap-in-place.
- **With duplicates** → sort + skip via `if (i > pos && used[i-1]) continue`.

## Related problems

- [Permutations II (with duplicates)](https://leetcode.com/problems/permutations-ii/)
- [Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/)
- [Next Permutation](https://leetcode.com/problems/next-permutation/) — in-place next lexicographic
- [Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/) — permutations with divisibility constraint
