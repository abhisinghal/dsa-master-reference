# Monotonic Stack — Daily Temperatures

*[↗ LeetCode: Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/monotonic-stack)

<CompanyTags companies="Meta, Amazon, Google" />

Given `temps`, return `answer` where `answer[i]` is the number of days until a warmer temperature (or 0 if none).

**Example 1** — `temps=[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`
**Example 2** — `temps=[30,40,50,60]` → `[1,1,1,0]`

**Constraints** — `1 ≤ n ≤ 10⁵`; `30 ≤ temps[i] ≤ 100`.


<Hints
  hint1="What element does each `i` ’see’ looking left or right? Nearest greater? Nearest smaller?"
  hint2="Maintain a stack that’s monotonic in one direction. When the new element breaks monotonicity, pop and answer for popped items."
  hint3="Contribution counting: instead of ’for each subarray find X’, ask ’for each element, how many subarrays does it contribute to?’"
/>
---

## Approach 1 — Brute force (nested scan)

**Intuition.** For each day `i`, scan forward until a warmer day.

```java
int[] dailyTemperaturesBrute(int[] t) {
    int n = t.length;
    int[] ans = new int[n];
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (t[j] > t[i]) { ans[i] = j - i; break; }
    return ans;
}
```

**Complexity** — Time **O(n²)** worst case (strictly decreasing input); Space **O(1)** aside from output.

---

## Approach 2 — Right-to-left with next-greater cache

**Insight from brute.** After computing `ans[i+1]`, many days beyond `i+1` are known — we can jump over them.

Walk right-to-left. For day `i`, start at `j = i+1`. If `t[j] ≤ t[i]`, jump forward by `ans[j]` (the known distance to a warmer day). Repeat until a warmer day is found or we fall off.

```java
int[] dailyTemperaturesRTL(int[] t) {
    int n = t.length;
    int[] ans = new int[n];
    for (int i = n - 2; i >= 0; i--) {
        int j = i + 1;
        while (j < n && t[j] <= t[i]) {
            if (ans[j] == 0) { j = n; break; }
            j += ans[j];
        }
        if (j < n) ans[i] = j - i;
    }
    return ans;
}
```

**Complexity** — Time **O(n)** amortized (jumps skip regions of ≤); Space **O(1)** output only.

Slick but non-obvious. The stack version below is easier to reason about — and interviewer-preferred.

---

## Approach 3 — Monotonic decreasing stack (indices)

**Insight from RTL cache.** The RTL solution is really doing a *monotonic decreasing* traversal from the right. A stack-based left-to-right pass captures the same idea more explicitly.

Push indices onto a decreasing stack. When `t[i]` beats the top, that top's answer is `i − top`. Pop and repeat.

**Trap.** Store **indices**, not temperatures — you need `i - top` for the answer.

```java
int[] dailyTemperatures(int[] t) {
    int n = t.length;
    int[] ans = new int[n];
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && t[stack.peek()] < t[i]) {
            int idx = stack.pop();
            ans[idx] = i - idx;
        }
        stack.push(i);
    }
    return ans;
}
```

<CodeTrace
  title="Monotonic stack — temps=[73,74,75,71,69,72,76,73]"
  :values="[73,74,75,71,69,72,76,73]"
  :windowKeys="['i']"
  :cellWidth="32"
  :steps='[
    { pointers: { i: 0 }, vars: { stack: "[0]", ans: "[0,0,0,0,0,0,0,0]" }, note: "push 0" },
    { pointers: { i: 1 }, vars: { stack: "[1]", ans: "[1,0,0,0,0,0,0,0]" }, note: "74 pops 73 → ans[0]=1", added: [0] },
    { pointers: { i: 2 }, vars: { stack: "[2]", ans: "[1,1,0,0,0,0,0,0]" }, note: "75 pops 74 → ans[1]=1", added: [1] },
    { pointers: { i: 3 }, vars: { stack: "[2,3]", ans: "[1,1,0,0,0,0,0,0]" }, note: "71 pushes (cooler)" },
    { pointers: { i: 5 }, vars: { stack: "[2,5]", ans: "[1,1,0,2,1,0,0,0]" }, note: "72 pops 69,71 → ans[4]=1, ans[3]=2", added: [3,4] },
    { pointers: { i: 6 }, vars: { stack: "[6]", ans: "[1,1,4,2,1,1,0,0]" }, note: "76 pops 72,75 → ans[5]=1, ans[2]=4", added: [2,5] },
    { pointers: { i: 7 }, vars: { stack: "[6,7]", ans: "[1,1,4,2,1,1,0,0]" }, note: "final" }
  ]'
/>

**Complexity** — Time **O(n)** (each index pushed + popped at most once); Space **O(n)** for the stack.

---

## Try it yourself

<JavaRunner problem-slug="monotonic-stack-daily-temperatures" />

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(1) |
| RTL with cache jump | O(n) amortized | O(1) |
| Monotonic stack | **O(n)** | O(n) |

## When to use which

- **Cold interview** → brute → stack. RTL is smart but hard to explain fast.
- **"Next greater element" family** → always monotonic stack. Once you see the pattern (`while stack.top < current: pop and record`), the whole family is solved by adjusting the comparator.

## Related problems (same ladder applies)

- [Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) — circular array; walk 2n times, `i%n`
- [Online Stock Span](https://leetcode.com/problems/online-stock-span/) — same skeleton, streaming input
- [Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) — monotonic stack + contribution technique
- [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) — closest-smaller-both-sides via one stack