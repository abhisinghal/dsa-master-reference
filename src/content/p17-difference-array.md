## The Pattern

A difference array turns many range additions into boundary edits. Instead of touching every `a[i]` for `l <= i <= r`, record only the slope changes: `diff[l] += v` starts adding `v`, and `diff[r + 1] -= v` stops it. One prefix-sum pass reconstructs the final array.

!!! pattern "Recognition signals"
    **Signals:** offline range increments, many updates before any query, "add value to every index in [l,r]", bookings over numbered seats/flights, or constraints where `updates * rangeLength` is too large. If all updates are known before answers are needed, boundary deltas beat repeated writes.

```diagram
{"type":"array","title":"Range add [l,r] by writing only boundaries","values":["0","+v","0","0","-v","0"],"index":[0,"l",2,"r","r+1",5],"highlights":{"1":"green","4":"red"},"pointers":[{"name":"start add","index":1,"color":"green","side":"top"},{"name":"stop after r","index":4,"color":"red","side":"bottom"}],"caption":"diff[l] += v turns the contribution on; diff[r+1] -= v turns it off before the next position."}
```

```diagram
{"type":"array","title":"Prefix sum reconstructs the applied update","values":[0,"v","v","v",0,0],"index":[0,"l",2,"r","r+1",5],"highlights":{"1":"green","2":"green","3":"green","4":"muted"},"brackets":[{"from":1,"to":3,"label":"range receives +v","color":"green","row":0}],"caption":"Running sum over diff materializes the final contribution at each index."}
```

## The Invariant

After processing any set of updates, `diff[i]` stores the net change to the running value that begins exactly at index `i`. Therefore the prefix sum `running += diff[i]` equals the total contribution of every update whose left boundary has been seen and whose right boundary has not yet been passed.

## Template

```java
int[] applyRangeAdds(int n, int[][] updates) {
    long[] diff = new long[n + 1];
    for (int[] u : updates) {
        int l = u[0], r = u[1], v = u[2];
        diff[l] += v;
        if (r + 1 < n) diff[r + 1] -= v;
    }

    int[] ans = new int[n];
    long running = 0;
    for (int i = 0; i < n; i++) {
        running += diff[i];
        ans[i] = Math.toIntExact(running);
    }
    return ans;
}
```

For a 2D rectangle add, update the four corners of a `(rows + 1) x (cols + 1)` diff grid: `+v` at top-left and bottom-right-after, `-v` at top-right-after and bottom-left-after; then take 2D prefix sums.

## Worked Recognition

- **Range Addition** (Module 14): each update is exactly `diff[start] += inc`, `diff[end + 1] -= inc`; the answer is produced once at the end.
- **Corporate Flight Bookings** (Module 14): bookings add seats over consecutive flight numbers. Convert 1-based flight ranges to 0-based boundaries and prefix once.
- Batched quota/traffic adjustments: if queries ask only for the final state after all policy windows, a difference array is simpler and faster than a segment tree.

## Complexity

!!! complexity "Complexity"
    **T:** O(u + n) for `u` updates and one reconstruction pass, instead of O(total covered length). **S:** O(n) for the diff array; use `long` when accumulated deltas can overflow `int`.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Forgetting the `r + 1` boundary guard; mixing inclusive ranges with half-open APIs; returning the diff array without prefix reconstruction; allocating only `n` slots and then writing `diff[n]`; or using `int` when many large updates accumulate.

## When NOT to use it

Do not use a plain difference array when queries and updates are interleaved online, when you need range minimum/maximum during updates, or when coordinates are huge and sparse without compression. Use a Fenwick tree, segment tree, ordered map, or coordinate compression instead.
