# Two Pointers — Intersection of Two Arrays II

*[↗ LeetCode: Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

Return the multi-set intersection (each element appears `min(count_a, count_b)` times).

## Approach 1 — Hash map count

Count nums1, iterate nums2, decrement. **O(n+m)** time, **O(n)** space.

## Approach 2 — Sort + two-pointer

**Insight.** After sorting, walk both arrays; on equal, emit and advance both.

```java
int[] intersect(int[] nums1, int[] nums2) {
    Arrays.sort(nums1); Arrays.sort(nums2);
    List<Integer> out = new ArrayList<>();
    int i = 0, j = 0;
    while (i < nums1.length && j < nums2.length) {
        if (nums1[i] == nums2[j]) { out.add(nums1[i]); i++; j++; }
        else if (nums1[i] < nums2[j]) i++;
        else j++;
    }
    return out.stream().mapToInt(Integer::intValue).toArray();
}
```

**Time O((n+m) log(n+m))**, **Space O(1)** extra.

**Follow-up.** If nums1 is huge and streamed from disk, hash-map on the smaller side. If both sorted, two-pointer is O(1) extra memory.

## Related problems

- [Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays/) — set intersection
- [Merge Sorted Array](/problems/merge-sorted-array) — same two-pointer walk
