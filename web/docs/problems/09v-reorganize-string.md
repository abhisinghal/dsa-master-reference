# Top-K / Heap — Reorganize String

*[↗ LeetCode: Reorganize String](https://leetcode.com/problems/reorganize-string/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/top-k-heap)

Given a string `s`, reorganize so no two adjacent characters are the same. Return the string or `""` if impossible.

**Example 1** — `"aab"` → `"aba"`
**Example 2** — `"aaab"` → `""` (impossible: 3 a's cannot alternate with 1 b)

---

## Approach 1 — Greedy with counts (place most-frequent alternating)

**Insight.** If any char has frequency &gt; `(n+1)/2`, it's impossible. Otherwise: place the most-frequent char at even positions (0, 2, 4…) first, then fill the rest.



```java
String reorganizeStringCount(String s) {
    int[] cnt = new int[26];
    for (char c : s.toCharArray()) cnt[c - 'a']++;
    int maxCnt = 0, maxCh = 0;
    for (int i = 0; i < 26; i++) if (cnt[i] > maxCnt) { maxCnt = cnt[i]; maxCh = i; }
    if (maxCnt > (s.length() + 1) / 2) return "";
    char[] result = new char[s.length()];
    int idx = 0;
    while (cnt[maxCh]-- > 0) { result[idx] = (char)('a' + maxCh); idx += 2; }
    for (int c = 0; c < 26; c++)
        while (cnt[c]-- > 0) {
            if (idx >= s.length()) idx = 1;
            result[idx] = (char)('a' + c);
            idx += 2;
        }
    return new String(result);
}
```



**Complexity** — Time **O(n)**; Space **O(1)** (26 alphabet).

## Approach 2 — Max-heap by frequency

**Insight.** At each step, pick the two most-frequent remaining chars — they can't be the same, so placing them next-to-each-other is safe.



```java
String reorganizeString(String s) {
    int[] cnt = new int[26];
    for (char c : s.toCharArray()) cnt[c - 'a']++;
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> b[1] - a[1]);
    for (int i = 0; i < 26; i++) if (cnt[i] > 0) heap.offer(new int[]{i, cnt[i]});
    if (heap.peek()[1] > (s.length() + 1) / 2) return "";
    StringBuilder sb = new StringBuilder();
    while (heap.size() >= 2) {
        int[] a = heap.poll(), b = heap.poll();
        sb.append((char)('a' + a[0])).append((char)('a' + b[0]));
        if (--a[1] > 0) heap.offer(a);
        if (--b[1] > 0) heap.offer(b);
    }
    if (!heap.isEmpty()) sb.append((char)('a' + heap.peek()[0]));
    return sb.toString();
}
```



<CodeTrace
  title="Max-heap — s=&quot;aabbcc&quot;"
  :values="['a','a','b','b','c','c']"
  :windowKeys="['step']"
  :cellWidth="38"
  :steps='[
    { pointers: { step: 0 }, vars: { heap: "[a:2, b:2, c:2]", sb: "" }, note: "seed" },
    { pointers: { step: 1 }, vars: { heap: "[b:2, c:2, a:1]", sb: "ab" }, note: "pop a, b → append", added: [0,2] },
    { pointers: { step: 2 }, vars: { heap: "[a:1, b:1, c:1]", sb: "abcb" }, note: "pop b, c → append", added: [2,4] },
    { pointers: { step: 3 }, vars: { heap: "[b:1]", sb: "abcbac" }, note: "pop a, c → append; b remains", added: [0,5] },
    { pointers: { step: 4 }, vars: { sb: "abcbacb" }, note: "append last b", added: [3] }
  ]'
/>

**Complexity** — Time **O(n log 26) = O(n)**; Space **O(1)** alphabet.

## Complexity summary

| Approach | Time | Space |
|---|---|---|
| Greedy count + place alternating | **O(n)** | O(1) |
| Max-heap by freq | O(n) | O(1) |

## Related problems

- [Rearrange String k Distance Apart](https://leetcode.com/problems/rearrange-string-k-distance-apart/) — same idea, generalized
- [Task Scheduler](/problems/task-scheduler) — cooldown-constrained scheduling
