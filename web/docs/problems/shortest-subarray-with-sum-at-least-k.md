# Sliding Window — Shortest Subarray with Sum at Least K

*[↗ LeetCode: Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/monotonic-stack)

&lt;CompanyTags companies="Amazon, Google" /&gt;

Smallest subarray sum ≥ `k`. **Array may contain negatives.**

**Example 1** — `nums=[1], k=1` → `1`
**Example 2** — `nums=[1,2], k=4` → `-1`
**Example 3** — `nums=[2,-1,2], k=3` → `3`

**Constraints** — `1 ≤ n ≤ 10⁵`; `-10⁵ ≤ nums[i] ≤ 10⁵`.


&lt;Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/&gt;
---

&lt;MarkSolved problem-slug="shortest-subarray-with-sum-at-least-k" /&gt; &lt;Bookmark problem-slug="shortest-subarray-with-sum-at-least-k" /&gt;

&lt;InterviewTimer problem-slug="shortest-subarray-with-sum-at-least-k" /&gt;



## Approach 1 — Sliding window fails

With negatives, sum isn't monotone in window size — can't shrink safely.

## Approach 2 — Prefix sums + monotonic deque (canonical)

**Insight.** Define `P[i]` = prefix sum. Answer = min `j - i` with `P[j] - P[i] ≥ k`. For each `j`, find earliest `i < j` with `P[i] ≤ P[j] - k`.

Maintain a deque of candidate `i` where `P` is increasing:
- **Pop front** while `P[deque.front] ≤ P[j] - k` — record candidate and discard.
- **Pop back** while `P[deque.back] ≥ P[j]` — later smaller prefix dominates.



```java
int shortestSubarray(int[] nums, int k) {
    int n = nums.length;
    long[] P = new long[n + 1];
    for (int i = 0; i < n; i++) P[i + 1] = P[i] + nums[i];
    Deque<Integer> dq = new ArrayDeque<>();
    int best = Integer.MAX_VALUE;
    for (int j = 0; j <= n; j++) {
        while (!dq.isEmpty() && P[j] - P[dq.peekFirst()] >= k)
            best = Math.min(best, j - dq.pollFirst());
        while (!dq.isEmpty() && P[dq.peekLast()] >= P[j]) dq.pollLast();
        dq.offerLast(j);
    }
    return best == Integer.MAX_VALUE ? -1 : best;
}
```



<CodeTrace
  title="Deque on prefix — nums=[2,-1,2], k=3"
  :values="['0','2','1','3']"
  :windowKeys="['j']"
  :cellWidth="34"
  :steps='[
    { pointers: { j: 1 }, vars: { deque: "[0,1]" }, note: "P=[0,2]" },
    { pointers: { j: 2 }, vars: { deque: "[0,2]", pop: 1 }, note: "P[2]=1 < P[1]=2 → pop back" },
    { pointers: { j: 3 }, vars: { deque: "[3]", best: 3 }, note: "P[3]=3, P[3]-P[0]=3 ≥ k → best=3" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="shortest-subarray-with-sum-at-least-k" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Sliding window | fails | — | rejected (negatives) |
| Monotonic deque | **O(n)** | O(n) | canonical |

## When to use which

- **Positives only** → sliding window fine.
- **Negatives allowed** → monotonic deque on prefix sums.
- **"Longest" instead** → different template — deque with reverse condition.

&lt;AiCompanion problem-slug="shortest-subarray-with-sum-at-least-k" pattern-hint="sliding window" /&gt;

## Related problems

- [Minimum Size Subarray Sum](/problems/minimum-size-subarray-sum) — positives only
- [Constrained Subsequence Sum](/problems/constrained-subsequence-sum)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)

&lt;FeedbackWidget problem-slug="shortest-subarray-with-sum-at-least-k" /&gt;

&lt;RelatedProblems problems="binary-subarrays-with-sum::Binary Subarrays With Sum|trapping-rain-water::Trapping Rain Water|fruit-into-baskets::Fruit Into Baskets" /&gt;
