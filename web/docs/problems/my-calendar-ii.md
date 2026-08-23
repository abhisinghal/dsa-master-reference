# Sweep Line — My Calendar II

*[↗ LeetCode: My Calendar II](https://leetcode.com/problems/my-calendar-ii/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/sweep-line)

&lt;CompanyTags companies="Google, Amazon, Meta" /&gt;

Design `MyCalendarTwo`. `book(start, end)` returns `true` iff the new event can be added without causing a **triple** overlap.

**Example 1** —


```
MyCalendarTwo c = new MyCalendarTwo();
c.book(10, 20); // true
c.book(50, 60); // true
c.book(10, 40); // true (double, allowed)
c.book(5, 15);  // false (would make triple at [10,15))
c.book(5, 10);  // true
c.book(25, 55); // true
```



**Constraints** — `≤ 1000` `book` calls; `0 ≤ start < end ≤ 10⁹`.


&lt;Hints
  hint1="Turn events into `(time, +1/-1)` pairs. What’s the ’active count’ or ’max concurrent’?"
  hint2="Sort events by time; break ties consistently (end before start for ’meetings’, or vice versa)."
  hint3="Sweep; maintain a running count/set. Max active gives room count; drops give free slots."
/&gt;
---

## Approach 1 — Track singles + doubles

**Insight.** Maintain a list of single-booked intervals and double-booked intervals. On `book`:
- If overlap with **doubles** → triple → return false.
- Else compute overlaps with singles and add them as new doubles; add new event to singles.



```java
class MyCalendarTwo {
    List<int[]> singles = new ArrayList<>();
    List<int[]> doubles = new ArrayList<>();
    public boolean book(int s, int e) {
        for (int[] d : doubles) if (s < d[1] && d[0] < e) return false;
        for (int[] sg : singles)
            if (s < sg[1] && sg[0] < e)
                doubles.add(new int[]{Math.max(s, sg[0]), Math.min(e, sg[1])});
        singles.add(new int[]{s, e});
        return true;
    }
}
```



**Complexity** — Time **O(n)** per `book`; Space **O(n)**.

---

## Approach 2 — Difference-map sweep

**Insight.** Maintain a `TreeMap<Integer, Integer>` of deltas. `book(s, e)` tentatively `+1` at s, `-1` at e; sweep to find running count; if any &gt; 2, rollback.



```java
class MyCalendarTwo2 {
    TreeMap<Integer, Integer> map = new TreeMap<>();
    public boolean book(int s, int e) {
        map.merge(s, 1, Integer::sum);
        map.merge(e, -1, Integer::sum);
        int active = 0;
        for (int d : map.values()) {
            active += d;
            if (active >= 3) {
                map.merge(s, -1, Integer::sum);
                map.merge(e, 1, Integer::sum);
                if (map.get(s) == 0) map.remove(s);
                if (map.get(e) == 0) map.remove(e);
                return false;
            }
        }
        return true;
    }
}
```



**Complexity** — Time **O(n log n)** per `book`; Space **O(n)**.

---

## Try it yourself

<JavaRunner problem-slug="my-calendar-ii" />

## Complexity summary

| Approach | Time / book | Space | Grade |
|---|---|---|---|
| Two-list tracking | O(n) | O(n) | canonical |
| Delta-map sweep | O(n log n) | O(n) | generalizes to k-book |

## When to use which

- **My Calendar II specifically** → two-list.
- **"My Calendar k"** (no k-th overlap) → delta map + threshold.
- **Streaming with heavy queries** → segment tree with lazy prop.

&lt;AiCompanion problem-slug="my-calendar-ii" pattern-hint="sweep line" /&gt;

## Related problems

- [My Calendar I](https://leetcode.com/problems/my-calendar-i/) — no double
- [My Calendar III](https://leetcode.com/problems/my-calendar-iii/) — return current max concurrency
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii)