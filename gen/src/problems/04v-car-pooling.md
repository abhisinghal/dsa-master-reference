# Prefix Sum — Car Pooling

*[↗ LeetCode: Car Pooling](https://leetcode.com/problems/car-pooling/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

Given trips `[numPassengers, from, to]` and car `capacity`, return `true` iff you can carry all passengers without exceeding capacity.

**Example** — `trips=[[2,1,5],[3,3,7]], capacity=4` → `false`

## Approach — Difference array

**Insight.** Same as Corporate Flight Bookings — `+num` at `from`, `-num` at `to`. Then prefix scan; if any prefix > capacity, false.

```java
boolean carPooling(int[][] trips, int capacity) {
    int[] diff = new int[1001];
    for (int[] t : trips) { diff[t[1]] += t[0]; diff[t[2]] -= t[0]; }
    int run = 0;
    for (int c : diff) { run += c; if (run > capacity) return false; }
    return true;
}
```

**Complexity** — Time **O(n + max)**; Space **O(max)**.

## Related problems

- [Corporate Flight Bookings](/problems/corporate-flight-bookings) — sibling
- [Range Addition](/problems/range-addition)
- [Meeting Rooms II](/problems/sweep-line-meeting-rooms-ii) — related but with heap
