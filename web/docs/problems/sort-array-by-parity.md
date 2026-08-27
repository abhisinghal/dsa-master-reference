# Two Pointers — Sort Array By Parity

*[↗ LeetCode: Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/two-pointers)

<CompanyTags companies="Meta, Amazon" />

Rearrange so all even values come before all odd. Any valid partition accepted.

**Example 1** — `nums=[3,1,2,4]` → `[2,4,3,1]` or `[4,2,3,1]` etc.
**Example 2** — `nums=[0]` → `[0]`
**Example 3** — `nums=[1,3,5,2,4]` → `[2,4,5,3,1]` or `[4,2,3,5,1]`

**Constraints** — `1 ≤ n ≤ 5000`. Brute allocation + copy is O(n) time + O(n) space. Two-pointer in-place is O(n) time + O(1) space.


<Hints
  hint1="Sort first if the input isn't already ordered. Two pointers rely on monotonicity."
  hint2="Place one pointer at each end. Move the one whose side is provably suboptimal for the target."
  hint3="Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
/>
---

<MarkSolved problem-slug="sort-array-by-parity" /> <Bookmark problem-slug="sort-array-by-parity" />

<InterviewTimer problem-slug="sort-array-by-parity" />



## Approach 1 — Two-pass allocation

**Intuition.** Walk once collecting evens, then once collecting odds. Concatenate.



```java
int[] sortArrayByParityBrute(int[] nums) {
    int[] res = new int[nums.length];
    int idx = 0;
    for (int x : nums) if (x % 2 == 0) res[idx++] = x;
    for (int x : nums) if (x % 2 == 1) res[idx++] = x;
    return res;
}
```



**Complexity** — Time **O(n)**; Space **O(n)**. Correct, but allocates a new array. *In an interview* say "in-place with two pointers → O(1) extra space."

---

## Approach 2 — Opposing pointers + swap (canonical)

**Insight.** `l` from left seeks first odd; `r` from right seeks first even; swap; repeat until they meet. In-place, O(n), O(1) extra space.



```java
int[] sortArrayByParity(int[] nums) {
    int l = 0, r = nums.length - 1;
    while (l < r) {
        if (nums[l] % 2 == 0) l++;
        else if (nums[r] % 2 == 1) r--;
        else { int t = nums[l]; nums[l++] = nums[r]; nums[r--] = t; }
    }
    return nums;
}
```



<CodeTrace
  title="Opposing pointers + swap (canonical)"
  :values="['3', '1', '2', '4']"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0 }, vars: { phase: "start" }, note: "Initialize scan." },
    { pointers: { i: 2 }, vars: { phase: "midway" }, note: "Midway through processing." },
    { pointers: { i: 3 }, vars: { phase: "done" }, note: "Return the answer." }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. *Say aloud in an interview:* "same in-place partition template as Dutch National Flag and Move Zeroes."

**Trap** — for stable ordering (preserving relative order), use slow/fast writer instead.

---

## Try it yourself

<JavaRunner problem-slug="sort-array-by-parity" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Two-pass allocation | O(n) | O(n) | Fine baseline |
| **Opposing 2p in-place** | **O(n)** | **O(1)** | **Canonical** |

## When to use which

- **"Any valid partition"** → opposing 2p.
- **"Stable ordering"** → slow/fast writer + zero-fill (order-preserving).
- **Three-way partition** → Dutch national flag.

<AiCompanion problem-slug="sort-array-by-parity" pattern-hint="two pointers" />

## Related problems

- [Sort Colors](https://leetcode.com/problems/sort-colors/) — 3-way
- [Move Zeroes](/problems/move-zeroes)

<FeedbackWidget problem-slug="sort-array-by-parity" />

<RelatedProblems problems="valid-palindrome-ii::Valid Palindrome II|container-with-most-water::Container With Most Water|4sum::4sum" />
