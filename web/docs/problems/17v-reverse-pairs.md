# Divide & Conquer — Reverse Pairs

*[↗ LeetCode: Reverse Pairs](https://leetcode.com/problems/reverse-pairs/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/divide-conquer)

Count pairs `(i, j)` with `i < j` and `nums[i] > 2 * nums[j]`.

**Example 1** — `nums=[1,3,2,3,1]` → `2`
**Example 2** — `nums=[2,4,3,5,1]` → `3`

---

## Approach 1 — Brute nested count

O(n²). TLE at n=5·10⁴.

## Approach 2 — Merge sort with pair-count step

**Insight.** During merge, both halves are sorted. For each `L[i]`, count `R[j]` with `L[i] > 2*R[j]` via a monotone scan. Then merge as usual.



```java
int count;
int reversePairs(int[] a) {
    count = 0;
    mergeSort(a, 0, a.length - 1);
    return count;
}
void mergeSort(int[] a, int lo, int hi) {
    if (lo >= hi) return;
    int mid = (lo + hi) / 2;
    mergeSort(a, lo, mid);
    mergeSort(a, mid + 1, hi);
    // count pairs across halves
    int j = mid + 1;
    for (int i = lo; i <= mid; i++) {
        while (j <= hi && a[i] > 2L * a[j]) j++;
        count += j - (mid + 1);
    }
    // merge
    int[] tmp = new int[hi - lo + 1];
    int p = lo, q = mid + 1, k = 0;
    while (p <= mid && q <= hi) tmp[k++] = a[p] <= a[q] ? a[p++] : a[q++];
    while (p <= mid) tmp[k++] = a[p++];
    while (q <= hi)  tmp[k++] = a[q++];
    for (int i = 0; i < tmp.length; i++) a[lo + i] = tmp[i];
}
```



<CodeTrace
  title="Merge sort count — [2,4,3,5,1]"
  :values="[2,4,3,5,1]"
  :windowKeys="['step']"
  :cellWidth="42"
  :steps='[
    { pointers: { step: 0 }, vars: { L: "[2,4]", R: "[3]", pairs: 0 }, note: "merge [2,4] and [3]: no 2*3=6 lt L. 0 pairs" },
    { pointers: { step: 1 }, vars: { L: "[5]", R: "[1]", pairs: 1 }, note: "5 gt 2*1=2 → 1 pair" },
    { pointers: { step: 2 }, vars: { L: "[2,3,4]", R: "[1,5]", pairs: 3 }, note: "cross-half: 2,3,4 each vs 1 → 3 more? actually 2 gt 2? 2 gt 2 false; 3 gt 2 → yes; 4 gt 2 → yes. total = 1+2 = 3", added: [0] }
  ]'
/>

**Complexity** — Time **O(n log n)**; Space **O(n)**.

## Alternative — Binary Indexed Tree (Fenwick)

Compress values; walk right to left; at each `nums[i]`, query count of already-seen with value &lt; `nums[i]/2`. **O(n log n)** as well.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute | O(n²) | O(1) |
| Merge sort + count | **O(n log n)** | O(n) |
| Fenwick tree | O(n log n) | O(n) |

## Related problems

- [Count of Smaller Numbers After Self](/problems/divide-conquer-inversions) — same merge-sort framework
- [Count of Range Sum](/problems/count-of-range-sum) — prefix-sum + merge sort
- [Number of Inversions](https://leetcode.com/problems/global-and-local-inversions/)
