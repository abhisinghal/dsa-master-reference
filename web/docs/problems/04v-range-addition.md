# Prefix Sum — Range Addition

*[↗ LeetCode: Range Addition](https://leetcode.com/problems/range-addition/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/prefix-sum)

Given array size `n` and `updates=[start, end, val]`, apply all as range add and return final array.

**Example** — `n=5, [[1,3,2],[2,4,3],[0,2,-2]]` → `[-2,0,3,5,3]`

## Approach — Difference array + one prefix pass



```java
int[] getModifiedArray(int n, int[][] updates) {
    int[] diff = new int[n + 1];
    for (int[] u : updates) { diff[u[0]] += u[2]; diff[u[1] + 1] -= u[2]; }
    int[] out = new int[n];
    int run = 0;
    for (int i = 0; i < n; i++) { run += diff[i]; out[i] = run; }
    return out;
}
```



**Complexity** — Time **O(n + updates)**; Space **O(n)**.

## Related problems

- [Corporate Flight Bookings](/problems/corporate-flight-bookings)
- [Car Pooling](/problems/car-pooling)
- [Range Addition II](/problems/range-addition-ii)
