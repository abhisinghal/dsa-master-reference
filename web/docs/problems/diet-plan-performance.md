# Sliding Window — Diet Plan Performance

*[↗ LeetCode: Diet Plan Performance](https://leetcode.com/problems/diet-plan-performance/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/sliding-window)

Fixed window of size `k` over calories. For each window: +1 if sum &gt; upper; −1 if sum &lt; lower; 0 otherwise. Return total score.

**Example 1** — `calories=[1,2,3,4,5], k=1, lower=3, upper=3` → `0`
**Example 2** — `calories=[3,2], k=2, lower=0, upper=1` → `1`
**Example 3** — `calories=[6,5,0,0], k=2, lower=1, upper=5` → `0`

**Constraints** — `1 ≤ n ≤ 10⁵`; `1 ≤ k ≤ n`.


<Hints
  hint1="What does a valid window look like here? Define the invariant on the window contents before writing loops."
  hint2="Grow `right`. When the invariant breaks, shrink `left` until it’s restored. Track the best answer inside the valid region."
  hint3="For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
/>
---

<MarkSolved problem-slug="diet-plan-performance" /> <Bookmark problem-slug="diet-plan-performance" />

<InterviewTimer problem-slug="diet-plan-performance" />



## Approach — Fixed-window running sum (canonical)

**Insight.** Pre-sum first `k`; slide by adding right and subtracting left.



```java
int dietPlanPerformance(int[] cal, int k, int lower, int upper) {
    int sum = 0;
    for (int i = 0; i < k; i++) sum += cal[i];
    int score = 0;
    if (sum > upper) score++;
    else if (sum < lower) score--;
    for (int i = k; i < cal.length; i++) {
        sum += cal[i] - cal[i - k];
        if (sum > upper) score++;
        else if (sum < lower) score--;
    }
    return score;
}
```



<CodeTrace
  title="Fixed window — calories=[6,5,0,0], k=2, lower=1, upper=5"
  :values="['6','5','0','0']"
  :windowKeys="['left','right']"
  :cellWidth="34"
  :steps='[
    { pointers: { left: 0, right: 1 }, vars: { sum: 11, score: 1 }, note: "sum > upper → +1" },
    { pointers: { left: 1, right: 2 }, vars: { sum: 5, score: 1 }, note: "in range" },
    { pointers: { left: 2, right: 3 }, vars: { sum: 0, score: 0 }, note: "sum < lower → -1" }
  ]'
/>

**Complexity** — Time **O(n)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="diet-plan-performance" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Fixed window slide | **O(n)** | O(1) | canonical |

## When to use which

- **Fixed window size + accumulator** → this template.
- **Variable window** → shrink/extend on validity.
- **Return per-window score list** → append instead of accumulating.

<AiCompanion problem-slug="diet-plan-performance" pattern-hint="sliding window" />

## Related problems

- [Maximum Average Subarray I](/problems/maximum-average-subarray-i)
- [Minimum Size Subarray Sum](/problems/minimum-size-subarray-sum)
- [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)

<FeedbackWidget problem-slug="diet-plan-performance" />
