# Divide & Conquer — Count of Smaller Numbers After Self

*[↗ LeetCode: Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/divide-conquer)

<CompanyTags companies="Google, Amazon, Meta" />

For each index `i`, return the number of `j > i` with `nums[j] < nums[i]`.

**Example 1** — `nums=[5,2,6,1]` → `[2,1,1,0]`
**Example 2** — `nums=[-1]` → `[0]`
**Example 3** — `nums=[-1,-1]` → `[0,0]` (equal, not strictly smaller)

**Constraints** — `1 ≤ n ≤ 10⁵`; values fit in `int`. Brute pair-count is O(n²) = 10¹⁰ ops = TLE. Merge-sort variant is O(n log n) ≈ 1.7·10⁶.


<Hints
  hint1="Can I split the input in half, solve each half, then combine? Combine step is the trick."
  hint2="Merge sort framework: recurse left, recurse right, then merge with the counting/comparison logic on the boundary."
  hint3="For count-of-X-across-boundary, two-pointer walk during the merge step."
/>
---

<MarkSolved problem-slug="divide-conquer-inversions" /> <Bookmark problem-slug="divide-conquer-inversions" />

<InterviewTimer problem-slug="divide-conquer-inversions" />



## Approach 1 — Brute force (nested compare)

**Intuition.** For each `i`, count `nums[j] < nums[i]` for `j > i`.



```java
List<Integer> countSmallerBrute(int[] nums) {
    List<Integer> ans = new ArrayList<>();
    for (int i = 0; i < nums.length; i++) {
        int c = 0;
        for (int j = i + 1; j < nums.length; j++) if (nums[j] < nums[i]) c++;
        ans.add(c);
    }
    return ans;
}
```



**Complexity** — Time **O(n²)**; Space **O(n)** output. TLE at n=10⁵.

---

## Approach 2 — Binary Indexed Tree (BIT) / Fenwick tree

**Insight.** Traverse right to left. At each step, "how many values already seen are less than `nums[i]`?" is a range query on a frequency array. BIT answers in O(log n).

**Preprocess.** Compress values to `[0, m)`.



```java
List<Integer> countSmallerBIT(int[] nums) {
    int n = nums.length;
    int[] sorted = nums.clone();
    Arrays.sort(sorted);
    Map<Integer, Integer> rank = new HashMap<>();
    int r = 0;
    for (int v : sorted) if (!rank.containsKey(v)) rank.put(v, r++);
    int[] bit = new int[r + 1];
    Integer[] ans = new Integer[n];
    for (int i = n - 1; i >= 0; i--) {
        int idx = rank.get(nums[i]);
        ans[i] = query(bit, idx);       // count of values with rank < idx
        update(bit, idx + 1, 1);
    }
    return Arrays.asList(ans);
}
int query(int[] bit, int i) { int s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; }
void update(int[] bit, int i, int d) { for (; i < bit.length; i += i & -i) bit[i] += d; }
```



**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Approach 3 — Merge sort with count of inversions

**Insight.** During a merge sort's merge step: when a right-side element `R[j]` is smaller than a left-side `L[i]`, every remaining `L[i..]` gains a count. Accumulate into a `counts[]` array indexed by original position.



```java
int[] result;
List<Integer> countSmaller(int[] nums) {
    int n = nums.length;
    result = new int[n];
    Integer[] idx = new Integer[n];
    for (int i = 0; i < n; i++) idx[i] = i;
    mergeSort(nums, idx, 0, n - 1);
    List<Integer> out = new ArrayList<>();
    for (int v : result) out.add(v);
    return out;
}
void mergeSort(int[] nums, Integer[] idx, int lo, int hi) {
    if (lo >= hi) return;
    int mid = (lo + hi) / 2;
    mergeSort(nums, idx, lo, mid);
    mergeSort(nums, idx, mid + 1, hi);
    Integer[] tmp = new Integer[hi - lo + 1];
    int i = lo, j = mid + 1, k = 0, rightBelow = 0;
    while (i <= mid && j <= hi) {
        if (nums[idx[j]] < nums[idx[i]]) { rightBelow++; tmp[k++] = idx[j++]; }
        else { result[idx[i]] += rightBelow; tmp[k++] = idx[i++]; }
    }
    while (i <= mid) { result[idx[i]] += rightBelow; tmp[k++] = idx[i++]; }
    while (j <= hi)  tmp[k++] = idx[j++];
    for (int p = 0; p < tmp.length; p++) idx[lo + p] = tmp[p];
}
```



<CodeTrace
  title="Merge-sort inversions — nums=[5,2,6,1]"
  :values="[5,2,6,1]"
  :windowKeys="['i','j']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0, j: 1 }, vars: { pair: "[5,2]", swap: true }, note: "merge [5] and [2]: 5 gt 2 → counts[5]=1", added: [0,1] },
    { pointers: { i: 2, j: 3 }, vars: { pair: "[6,1]", swap: true }, note: "merge [6] and [1]: 6 gt 1 → counts[6]=1", added: [2,3] },
    { pointers: { i: 0, j: 2 }, vars: { L: "[2,5]", R: "[1,6]" }, note: "merge: 2 gt 1 → counts[5]+=2, counts[2]+=1" },
    { pointers: { i: 0, j: 3 }, vars: { result: "[2,1,1,0]" }, note: "final counts array", added: [0] }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="divide-conquer-inversions" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute nested compare | O(n²) | O(n) |
| BIT / Fenwick | **O(n log n)** | O(n) |
| Merge sort | **O(n log n)** | O(n) |

## When to use which

- **You know BIT well** → shorter code, easier to explain.
- **You want to reuse merge sort** → same skeleton solves Reverse Pairs, Count of Range Sum, Global-and-Local Inversions.

<AiCompanion problem-slug="divide-conquer-inversions" pattern-hint="divide & conquer" />

## Related problems (same ladder applies)

- [Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) — `nums[i] > 2 * nums[j]` condition
- [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) — prefix sums + merge sort with range count
- [Global and Local Inversions](https://leetcode.com/problems/global-and-local-inversions/)
- [Sort List](https://leetcode.com/problems/sort-list/) — merge sort on linked list

<FeedbackWidget problem-slug="divide-conquer-inversions" />
