# Binary Search — Standard (Order-agnostic)

*[↗ LeetCode: Binary Search](https://leetcode.com/problems/binary-search/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/binary-search)

Given a sorted array and target, return the index or `-1`. O(log n).

**Example** — `nums=[-1,0,3,5,9,12], target=9` → `4`

---

## Approach 1 — Linear scan

O(n). Trivial baseline.

## Approach 2 — Classic binary search (closed interval)

```java
int search(int[] a, int t) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == t) return mid;
        else if (a[mid] < t) lo = mid + 1;
        else                 hi = mid - 1;
    }
    return -1;
}
```

<CodeTrace
  title="Binary search — target=9 in [-1,0,3,5,9,12]"
  :values="[-1,0,3,5,9,12]"
  :windowKeys="['lo','hi']"
  :cellWidth="42"
  :steps='[
    { pointers: { lo: 0, hi: 5, mid: 2 }, vars: { "a[mid]": 3 }, note: "3 lt 9 → lo = mid+1 = 3" },
    { pointers: { lo: 3, hi: 5, mid: 4 }, vars: { "a[mid]": 9 }, note: "match → return 4", added: [4] }
  ]'
/>

**Complexity** — Time **O(log n)**; Space **O(1)**.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Linear scan | O(n) | O(1) |
| Binary search | **O(log n)** | **O(1)** |

## Related problems

- [Search in Rotated Sorted Array](/problems/binary-search-rotated-sorted)
- [Find First and Last Position of Element](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) — two binary searches
- [Guess Number Higher or Lower](https://leetcode.com/problems/guess-number-higher-or-lower/) — interactive
