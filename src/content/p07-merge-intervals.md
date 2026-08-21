## The Pattern

Merge Intervals reduces a set of ranges to non-overlapping components. Sort by start time, carry one current interval, and either extend it on overlap or flush it when a gap appears.

!!! pattern "Recognition signals"
    **Signals:** intervals, calendars, reservations, ranges, "overlap", "minimum rooms", "erase overlaps", or "union of ranges." Sorting by start converts global overlap reasoning into a local comparison with the current end.

```diagram
{"type":"intervals","title":"Sorted intervals coalesce left to right","min":0,"max":10,"intervals":[{"start":1,"end":3,"label":"[1,3]","role":"green"},{"start":2,"end":6,"label":"extends to 6","role":"amber"},{"start":8,"end":10,"label":"new component","role":"primary"}],"caption":"Because starts are sorted, an overlap only needs comparison with the current merged end."}
```

## The Invariant

Before reading interval `i`, the output contains finalized, non-overlapping intervals strictly before `current`, and `current` is the union of all processed intervals that overlap its start component. Since later intervals start no earlier than `current.start`, only `interval.start <= current.end` can extend it.

## Template

```java
int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> {
        int byStart = Integer.compare(a[0], b[0]);
        return byStart != 0 ? byStart : Integer.compare(a[1], b[1]);
    });

    List<int[]> merged = new ArrayList<>();
    int start = intervals[0][0];
    int end = intervals[0][1];

    for (int i = 1; i < intervals.length; i++) {
        int s = intervals[i][0], e = intervals[i][1];
        if (s <= end) {
            end = Math.max(end, e);
        } else {
            merged.add(new int[] {start, end});
            start = s;
            end = e;
        }
    }
    merged.add(new int[] {start, end});
    return merged.toArray(new int[merged.size()][]);
}
```

## Worked Recognition

- **Meeting Rooms II** (Modules 10/14): merging tells whether meetings overlap, but the room count needs a min-heap of end times or a sweep line. Same interval ordering, different aggregate.
- **Non-overlapping Intervals** (Module 7): instead of merging, greedily keep the interval with the earliest end when overlaps occur; the invariant is about maximizing survivors.
- Calendar union / log compaction: sorted adjacent or overlapping ranges are coalesced to minimize storage and simplify later membership checks.

## Complexity

!!! complexity "Complexity"
    **T:** O(n log n) from sorting; the scan is O(n). **S:** O(n) for the result, excluding sort implementation details. If input is already sorted by start, the merge scan is O(n).

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Sorting by end for merge-union problems; forgetting to append the final current interval; treating touching intervals incorrectly (`s <= end` merges closed intervals, while half-open `[s,e)` often uses `s < end`); mutating shared interval arrays unexpectedly; or using subtraction in comparators.

## When NOT to use it

Do not use plain merging when the question asks for maximum concurrency, minimum removals, weighted interval profit, or point queries under many updates. Those need sweep line, greedy-by-end, DP, segment trees, or balanced maps.
