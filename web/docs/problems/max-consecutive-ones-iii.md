# Sliding Window — Max Consecutive Ones III

*[↗ LeetCode: Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sliding-window)

&lt;CompanyTags companies="Meta, Google, Microsoft, Amazon" /&gt;

Given a binary array `nums` and integer `k`, return the maximum length of a subarray containing only 1s after flipping at most `k` zeros.

**Example 1** — `nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2` → `6` (flip the two zeros in the middle group; window `[1,1,1,0,0,1,1,1,1] — no wait — final window `[1,1,1,0,0,1,1,1]` after flipping the middle 0s gives 6 in one run)
**Example 2** — `nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3` → `10`
**Example 3** — `nums = [1,1,1,1], k = 0` → `4`

**Constraints** — `1 ≤ n ≤ 10⁵`; `nums[i] ∈ {0, 1}`; `0 ≤ k ≤ n`.


&lt;Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/&gt;
---

## Approach 1 — Try every subarray

**Intuition.** For each `[i, j]`, count zeros; if `zeros ≤ k`, track length.



```java
int longestOnesBrute(int[] nums, int k) {
    int n = nums.length, best = 0;
    for (int i = 0; i < n; i++) {
        int zeros = 0;
        for (int j = i; j < n; j++) {
            if (nums[j] == 0) zeros++;
            if (zeros <= k) best = Math.max(best, j - i + 1);
            else break;
        }
    }
    return best;
}
```



<CodeTrace
  title="Brute — nums=[1,1,0,0,1,1], k=1"
  :values="['1','1','0','0','1','1']"
  :windowKeys="['i','j']"
  :cellWidth="34"
  :steps='[
    { pointers: { i: 0, j: 2 }, vars: { zeros: 1, best: 3 }, note: "one zero — allowed" },
    { pointers: { i: 0, j: 3 }, vars: { zeros: 2 }, note: "two zeros > k — break" },
    { pointers: { i: 1, j: 4 }, vars: { zeros: 2 }, note: "still two zeros, break early" },
    { pointers: { i: 3, j: 5 }, vars: { zeros: 1, best: 3 }, note: "back to 1 zero; length 3" }
  ]'
/>

**Complexity** — Time **O(n²)**; Space **O(1)**.

---

## Approach 2 — Sliding window with zero counter

**Insight from brute.** Growing `right` never decreases the zero count. Once we exceed `k`, we must shrink `left` past a zero to reduce it.



```java
int longestOnesSlide(int[] nums, int k) {
    int left = 0, zeros = 0, best = 0;
    for (int right = 0; right < nums.length; right++) {
        if (nums[right] == 0) zeros++;
        while (zeros > k) if (nums[left++] == 0) zeros--;
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```



<CodeTrace
  title="Sliding — nums=[1,1,1,0,0,0,1,1,1,1,0], k=2"
  :values="['1','1','1','0','0','0','1','1','1','1','0']"
  :windowKeys="['left','right']"
  :cellWidth="30"
  :steps='[
    { pointers: { left: 0, right: 4 }, vars: { zeros: 2, best: 5 }, note: "window contains 2 zeros ✓" },
    { pointers: { left: 0, right: 5 }, vars: { zeros: 3 }, note: "3rd zero → must shrink" },
    { pointers: { left: 4, right: 5 }, vars: { zeros: 2, best: 5 }, note: "shrunk past two zeros; left=4" },
    { pointers: { left: 5, right: 9 }, vars: { zeros: 1, best: 6 }, note: "extend to [1,1,1,1] plus one zero — new best 6" }
  ]'
/>

**Complexity** — Time **O(n)** — each index enters/leaves window once; Space **O(1)**.

---

## Approach 3 — Non-shrinking window (interview polish)

**Insight from sliding.** For a *maximum-length* answer, we never need to shrink below `best`. We can keep the window size monotonic non-decreasing.



```java
int longestOnes(int[] nums, int k) {
    int left = 0, zeros = 0;
    for (int right = 0; right < nums.length; right++) {
        if (nums[right] == 0) zeros++;
        if (zeros > k) { if (nums[left] == 0) zeros--; left++; }
    }
    return nums.length - left;
}
```



<CodeTrace
  title="Non-shrinking — same nums, k=2"
  :values="['1','1','1','0','0','0','1','1','1','1','0']"
  :windowKeys="['left','right']"
  :cellWidth="30"
  :steps='[
    { pointers: { left: 0, right: 5 }, vars: { zeros: 3 }, note: "3rd zero → slide left by exactly 1" },
    { pointers: { left: 1, right: 5 }, vars: { zeros: 3 }, note: "still invalid — but we do not shrink further; wait for right" },
    { pointers: { left: 1, right: 9 }, vars: { zeros: 3 }, note: "window slides forward; length preserved" },
    { pointers: { left: 5, right: 10 }, vars: { zeros: 3, len: 6 }, note: "final length = n - left = 6" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**. Same asymptotics, one less inner loop.

---

## Try it yourself

<JavaRunner problem-slug="max-consecutive-ones-iii" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Every subarray | O(n²) | O(1) | baseline |
| Sliding window + zero counter | O(n) | O(1) | expected optimum |
| Non-shrinking window | **O(n)** | O(1) | polish — one-pass, no inner while |

## When to use which

- **First pass** — state brute, then jump to sliding-window with zero counter.
- **"Max length" only** → prefer non-shrinking version.
- **"Return the window itself"** → keep the shrinking version and track `(bestL, bestLen)`.
- **"Flip 1s to 0s instead"** → complementary problem — swap semantics.

## Related problems

- [Longest Subarray of 1s After Deleting One Element](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) — `k=1` with deletion
- [Longest Repeating Character Replacement](/problems/longest-repeating-character-replacement) — generalization to arbitrary alphabet
- [Fruit Into Baskets](/problems/fruit-into-baskets) — `k=2` distinct
- [Longest Substring with At Most K Distinct Characters](/problems/longest-substring-with-at-most-k-distinct-characters)