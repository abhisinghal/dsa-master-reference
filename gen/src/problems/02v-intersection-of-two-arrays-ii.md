# Two Pointers — Intersection of Two Arrays II

*[↗ LeetCode: Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Meta, Amazon, Google, Uber" />

Return the multi-set intersection (each element appears `min(cnt_a, cnt_b)` times).

**Example 1** — `nums1=[1,2,2,1], nums2=[2,2]` → `[2,2]`
**Example 2** — `nums1=[4,9,5], nums2=[9,4,9,8,4]` → `[4,9]` or `[9,4]`

**Constraints** — `1 ≤ n, m ≤ 1000`.


<Hints
  hint1="Sort first if the input isn’t already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="intersection-of-two-arrays-ii" />

<InterviewTimer problem-slug="intersection-of-two-arrays-ii" />



## Approach 1 — Hash-map count

Count nums1; iterate nums2 decrementing. O(n+m).

## Approach 2 — Sort + two-pointer (canonical for pre-sorted)

**Insight.** After sorting, walk both arrays; on equal emit and advance both.

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

<CodeTrace
  title="Hash-map count"
  :values="['1', '2', '2', '1']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O((n+m) log(n+m))**; Space **O(1)** extra.

---

## Try it yourself

<JavaRunner problem-slug="intersection-of-two-arrays-ii" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Hash count | O(n+m) | O(min) | best if small side fits |
| Sort + 2p | **O((n+m) log)** | O(1) | canonical for sorted / streaming |

## When to use which

- **Presorted input** → 2p.
- **One huge / one small** → hash on smaller.
- **Streamed** → hash on materialized side.

<AiCompanion problem-slug="intersection-of-two-arrays-ii" pattern-hint="two pointers" />

## Related problems

- [Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays/) — set version
- [Merge Sorted Array](/problems/merge-sorted-array)

<FeedbackWidget problem-slug="intersection-of-two-arrays-ii" />
