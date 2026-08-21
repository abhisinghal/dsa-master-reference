<div class="part-divider">
<div class="pnum">Part III</div>
<div class="ptitle">Data Structures in Depth</div>
<div class="rule"></div>
<div class="pdesc">The "individual things" the patterns kept pointing to. Arrays, strings, linked lists, stacks &amp; queues, trees, heaps, tries, graphs, and segment/Fenwick trees — each a self-contained deep dive you reach <em>through</em> the patterns, not before them. Use as reference when a pattern lands you on one of these structures.</div>
</div>

# Arrays

Arrays are the workhorse container — most patterns land on them at some point. This chapter collects the **array-specific mechanics** that aren't tied to any single pattern: matrix rotation and traversal, in-place cell overwriting, and the cyclic-sort family that exploits value = index+1 mappings for O(n) time + O(1) space.

For the array-as-a-container Java mechanics (declaration, growth, sorting comparators), see the [primer](#array-int-t) in Part I.

## Matrix Mechanics (in-place grid manipulation)

<p class="secgoal"><b>What &amp; why:</b> a small family that isn't a "pattern" but shows up constantly as a warm-up — the whole game is <b>index arithmetic</b> and doing it <b>in place</b> (O(1) extra space). Master three moves: transpose+reverse (rotate), layer-by-layer traversal (spiral), and first-row/col as marker storage (zeroes).</p>

> [key] **Key Insight** — Almost every matrix trick is "map `(r,c)` to another cell by a formula." Write the formula down before you code: rotate-90°-clockwise sends `(r,c) → (c, n-1-r)`, which is exactly **transpose then reverse each row**.

### Rotate Image (90° clockwise, in place)
*[↗ LeetCode: Rotate Image](https://leetcode.com/problems/rotate-image/)* — **Medium**

**Problem.** Rotate an `n×n` matrix 90° clockwise, **in place** (no second matrix). **Example:** `[[1,2],[3,4]] → [[3,1],[4,2]]`.

```java
void rotate(int[][] m) {
    int n = m.length;
    for (int r = 0; r < n; r++)                 // 1) transpose across the main diagonal
        for (int c = r + 1; c < n; c++) {
            int t = m[r][c]; m[r][c] = m[c][r]; m[c][r] = t;
        }
    for (int[] row : m)                          // 2) reverse each row
        for (int i = 0, j = n - 1; i < j; i++, j--) {
            int t = row[i]; row[i] = row[j]; row[j] = t;
        }
}
```

> [note] **Trace it** — `[[1,2],[3,4]]`. Transpose → `[[1,3],[2,4]]`; reverse each row → `[[3,1],[4,2]]`. Counter-clockwise is the mirror: reverse rows **first**, then transpose (or transpose then reverse each column).

Time O(n²) · Space O(1).

### Spiral Matrix (layer-by-layer traversal)
*[↗ LeetCode: Spiral Matrix](https://leetcode.com/problems/spiral-matrix/)* — **Medium**

**Problem.** Return all elements of an `m×n` matrix in spiral order. **Example:** `[[1,2,3],[4,5,6],[7,8,9]] → [1,2,3,6,9,8,7,4,5]`.

```java
List<Integer> spiralOrder(int[][] a) {
    List<Integer> out = new ArrayList<>();
    int top = 0, bot = a.length - 1, left = 0, right = a[0].length - 1;
    while (top <= bot && left <= right) {
        for (int c = left; c <= right; c++) out.add(a[top][c]);      top++;
        for (int r = top;  r <= bot;   r++) out.add(a[r][right]);    right--;
        if (top <= bot) { for (int c = right; c >= left; c--) out.add(a[bot][c]); bot--; }
        if (left <= right) { for (int r = bot; r >= top; r--) out.add(a[r][left]); left++; }
    }
    return out;
}
```

> [trap] **Common Trap** — Forgetting the two `if` guards before the bottom row and left column. On a single leftover row or column they run again and re-emit cells. The guards check the shrinking bounds haven't crossed.

Time O(m·n) · Space O(1) extra.

### Set Matrix Zeroes (use row 0 / col 0 as markers)
*[↗ LeetCode: Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/)* — **Medium**

**Problem.** If a cell is `0`, set its entire row and column to `0` — **in place, O(1) extra space**. **Trap:** you must record *original* zeros before you start writing, or new zeros trigger more clearing.

```java
void setZeroes(int[][] m) {
    int R = m.length, C = m[0].length;
    boolean col0 = false;
    for (int r = 0; r < R; r++) {
        if (m[r][0] == 0) col0 = true;                 // column 0 needs its own flag
        for (int c = 1; c < C; c++)
            if (m[r][c] == 0) { m[r][0] = 0; m[0][c] = 0; }   // mark in the border
    }
    for (int r = R - 1; r >= 0; r--) {                 // write bottom-up so row 0 survives as marker
        for (int c = C - 1; c >= 1; c--)
            if (m[r][0] == 0 || m[0][c] == 0) m[r][c] = 0;
        if (col0) m[r][0] = 0;
    }
}
```

> [key] **Key Insight** — The naïve O(R·C) extra-space fix stores zero rows/cols in two sets. To reach **O(1)**, reuse the first row and first column *as* those sets — with one extra scalar (`col0`) because cell `(0,0)` would otherwise mean two things.

Time O(R·C) · Space O(1).

> [pat] **Pattern Connection** — "Reuse the input's own border as auxiliary storage" is the space-optimization mindset behind rolling-array DP and in-place linked-list surgery: when you're told **O(1) space**, look for structure you can safely overwrite.

### Same pattern, new tweaks

| Variation | The one move that changes | Time · Space |
|---|---|---|
| [Rotate Image](https://leetcode.com/problems/rotate-image/) | transpose + reverse rows (90° CW) | O(n²) · O(1) |
| [Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) | *write* `1..n²` along the same spiral bounds | O(n²) · O(1) |
| [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | border-as-marker + `col0` flag | O(R·C) · O(1) |
| [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | treat the grid as one sorted array → binary search | O(log mn) · O(1) |
| [Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) | start top-right; go left on bigger, down on smaller | O(m+n) · O(1) |


## Cyclic Sort family (value = index + 1)


Here's a pattern that looks like magic the first time you see it. **When an array contains `n` numbers taken from the range `1..n` (or `0..n-1`), every value has a natural home: the number `v` belongs at index `v-1`.** Cyclic Sort exploits this to sort — and to find missing or duplicate numbers — in **O(n) time and O(1) extra space**, beating both sorting (O(n log n)) and a hash set (O(n) space).

> [key] **The core idea** — Walk the array. At each position, if the number isn't already in its home slot, **swap it to where it belongs**. Because every swap places at least one number correctly, the total number of swaps is at most `n`, so the whole thing is O(n) despite the nested-looking `while`.

### Visual — placing each value at index `value − 1`

```text
 nums = [3, 1, 5, 4, 2]        (numbers 1..5, want value v at index v-1)
 i=0: 3 belongs at idx2 -> swap -> [5,1,3,4,2]
       5 belongs at idx4 -> swap -> [2,1,3,4,5]
       2 belongs at idx1 -> swap -> [1,2,3,4,5]  now nums[0]=1 correct -> i++
 ... every later i already home -> done in O(n)
```

> [inv] **Invariant** — After the pointer advances past index `i`, positions `0..i` hold exactly the values `1..i+1` in order. Each `swap` puts one more value into its final home, so across the whole scan there are ≤ n swaps.

## Cyclic Sort (the base template)
<p class="secgoal"><b>What & why:</b> the in-place template that sorts values from a known range (1..n) by sending each value to its own index. Goal — recognize the "array holds 1..n, find the missing/duplicate" family and solve it in O(n) time, O(1) space.</p>

### Problem
Sort an array that contains every number from `1..n` exactly once, in place, in O(n).

### Java
```java
void cyclicSort(int[] nums) {
    int i = 0;
    while (i < nums.length) {
        int home = nums[i] - 1;              // where nums[i] belongs
        if (nums[i] != nums[home]) swap(nums, i, home);   // put it home
        else i++;                            // already correct (or a duplicate) -> move on
    }
}
void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
```

### Complexity
Time O(n) · Space O(1).

> [trap] **Common Trap** — Advancing `i` after every swap skips values you just placed. *Example:* `nums=[3,1,2]` at `i=0`. Swap `3` to index 2 → `[2,1,3]`. If you `i++`, the fresh `2` at index 0 never gets placed at index 1. Use `while` (not `if`) at each `i`.

> [pat] **Pattern Connection** — Every problem below is this template with a different final step. The unifying idea — *"the value tells you its own index"* — also underlies counting sort and the in-place hashing trick (marking `nums[abs(v)-1]` negative) used in some array problems.

### Same pattern, new tweaks

Cyclic sort's whole family is "place each value at its home, then read off the wrong slots":

| Variation | The one thing that changes | Time |
|---|---|---|
| [Find the Missing Number](https://leetcode.com/problems/missing-number/) | after placing, the first index whose value ≠ index is missing | — |
| [Find All Numbers Disappeared / Find All Duplicates](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/) | scan for *every* wrong slot instead of the first | — |
| [Set Mismatch](https://leetcode.com/problems/set-mismatch/) | the single wrong slot reveals both the duplicated and the missing number | — |
| [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | ignore values outside `1..n`; the answer lies in `1..n+1` | — |

## Find the Missing Number
*[↗ LeetCode: Missing Number](https://leetcode.com/problems/missing-number/)*

### Problem
An array holds `n` distinct numbers from the range `0..n` (so exactly one is missing). Return the missing one. *Example:* `[4,0,3,1]` → `2`.

### How the pattern fits
Place each number at its index (`v` at index `v`, since the range starts at 0). Afterwards, the first index whose value isn't equal to its index reveals the missing number — that slot's rightful owner never showed up.

### Java
```java
int missingNumber(int[] nums) {
    int i = 0, n = nums.length;
    while (i < n) {
        int home = nums[i];
        if (nums[i] < n && nums[i] != nums[home]) swap(nums, i, home);  // in range & not home
        else i++;
    }
    for (i = 0; i < n; i++) if (nums[i] != i) return i;   // first wrong slot
    return n;                                             // all present -> n is missing
}
```

### Complexity
Time O(n) · Space O(1).

> [trap] **Common Trap** — The range is `0..n`, so a value can equal `n` (out of array bounds); guard `nums[i] < n` before swapping or you'll index out of range. (The classic XOR / Gauss-sum solutions also work, but cyclic sort generalizes to the "find *all* missing" variant below, which they don't.)

> [pat] **Pattern Connection** — Sibling of *Missing Number* via XOR (`i ^ nums[i]` over all i) and via the sum formula `n(n+1)/2 − Σnums`. Prefer those for the single-missing case; reach for cyclic sort when you must report **every** missing/duplicate value.

## Find All Missing / All Duplicate Numbers
*[↗ LeetCode: Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)*

### Problem
An array of `n` numbers where each is in `1..n`, but some appear twice and some are missing. Return **all** missing numbers (or all duplicates). *Example:* `[2,3,1,3,3]` → missing `[4,5]`, duplicates `[3]`.

### How the pattern fits
Run cyclic sort. Any index `i` where `nums[i] != i+1` is a "wrong home": index `i` is missing value `i+1`, and the value sitting there (`nums[i]`) is a duplicate.

### Java
```java
List<Integer> findDisappearedNumbers(int[] nums) {
    int i = 0, n = nums.length;
    while (i < n) {
        int home = nums[i] - 1;
        if (nums[i] != nums[home]) swap(nums, i, home);
        else i++;
    }
    List<Integer> missing = new ArrayList<>();
    for (i = 0; i < n; i++) if (nums[i] != i + 1) missing.add(i + 1);   // duplicates = nums[i]
    return missing;
}
```

### Complexity
Time O(n) · Space O(1) (excluding the output list).

> [trap] **Common Trap** — Using `if (nums[i] != nums[home])` is what makes duplicates safe: when the home slot already holds the same value, swapping would loop forever, so you skip and advance instead.

> [pat] **Pattern Connection** — *Find the Duplicate Number* (exactly one duplicate, array **immutable**) can't cyclic-sort in place — that constraint forces the **Fast/Slow Pointers** (Floyd) reframe instead. Recognizing *which constraint you're given* (mutable vs read-only) picks cyclic sort vs Floyd.

## First Missing Positive (Hard)
*[↗ LeetCode: First Missing Positive](https://leetcode.com/problems/first-missing-positive/)*

### Problem
Given an unsorted array (any integers), find the smallest missing **positive** integer in O(n) time and O(1) space. *Example:* `[3,4,-1,1]` → `2`.

### How the pattern fits
The answer must lie in `1..n+1` (with `n` slots, the smallest missing positive can't exceed `n+1`). So ignore non-positives and values `> n`, cyclic-sort the rest into place, then the first slot `i` with `nums[i] != i+1` gives the answer.

### Java
```java
int firstMissingPositive(int[] nums) {
    int i = 0, n = nums.length;
    while (i < n) {
        int home = nums[i] - 1;
        if (nums[i] > 0 && nums[i] <= n && nums[i] != nums[home]) swap(nums, i, home);
        else i++;
    }
    for (i = 0; i < n; i++) if (nums[i] != i + 1) return i + 1;
    return n + 1;                                  // 1..n all present
}
```

### Complexity
Time O(n) · Space O(1).

> [key] **Key Insight** — The bound *"answer ∈ `1..n+1`"* is what lets you ignore everything outside that range and still guarantee correctness: with only `n` positions, values above `n` cannot change which small positive is first missing.

> [trap] **Common Trap** — Trying to place out-of-range values. *Example:* `nums=[3,4,-1,1]`. `-1` and `4` can't fit in `[0..n-1]` (n=4). Guard `1 ≤ v ≤ n` before every swap or you'll IOOBE.

> [pat] **Pattern Connection** — The same "use the array itself as a hash table over `1..n`" idea powers the sign-marking trick (negate `nums[abs(v)-1]`) — an alternative O(1)-space encoding when you may not reorder the array.
