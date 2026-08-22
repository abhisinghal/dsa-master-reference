# Two Pointers

Instead of checking every pair with two nested loops (that's O(n²)), you keep **two indices** and move them cleverly so each step rules out a whole batch of pairs at once. The trick almost always leans on the array being **sorted** — that order is what tells you *which* pointer to move.

<TwoPointersAnim />

Say the array is sorted and you want two numbers that add up to a target. Put one pointer at each end and look at their sum:

- too **big**? the large end is the culprit — move the right pointer **left** to a smaller value.
- too **small**? move the left pointer **right** to a bigger value.
- **just right**? you found the pair.

Every move discards a number you've *proven* can't help, so you sweep the array once — O(n) instead of O(n²).

```svg
<svg width="720" height="200" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">
  <defs>
    <marker id="tp-g" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#16a34a"/></marker>
    <marker id="tp-r" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#dc2626"/></marker>
    <filter id="tp-s" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5"/></filter>
  </defs>
  <rect x="0" y="0" width="720" height="200" fill="#fbfcfe"/>
  <text x="20" y="28" font-size="13" font-weight="700" fill="#2563eb">sorted array — find two numbers summing to 9</text>

  <g filter="url(#tp-s)">
    <rect x="18"  y="54" width="54" height="42" rx="7" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.6"/>
    <rect x="82"  y="54" width="54" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="146" y="54" width="54" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="210" y="54" width="54" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="274" y="54" width="54" height="42" rx="7" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="338" y="54" width="54" height="42" rx="7" fill="#fef2f2" stroke="#dc2626" stroke-width="1.6"/>
  </g>
  <g font-size="19" font-weight="700" fill="#0b1220" text-anchor="middle">
    <text x="45"  y="82">1</text><text x="109" y="82">3</text><text x="173" y="82">5</text>
    <text x="237" y="82">6</text><text x="301" y="82">8</text><text x="365" y="82">11</text>
  </g>
  <g font-size="11" fill="#94a3b8" text-anchor="middle">
    <text x="45" y="112">0</text><text x="109" y="112">1</text><text x="173" y="112">2</text>
    <text x="237" y="112">3</text><text x="301" y="112">4</text><text x="365" y="112">5</text>
  </g>

  <line x1="45"  y1="150" x2="45"  y2="100" stroke="#16a34a" stroke-width="2" marker-end="url(#tp-g)"/>
  <text x="45"  y="168" text-anchor="middle" font-size="12" font-weight="700" fill="#16a34a">lo</text>
  <line x1="365" y1="150" x2="365" y2="100" stroke="#dc2626" stroke-width="2" marker-end="url(#tp-r)"/>
  <text x="365" y="168" text-anchor="middle" font-size="12" font-weight="700" fill="#dc2626">hi</text>

  <rect x="440" y="52" width="264" height="92" rx="9" fill="#f6f8fb" stroke="#d9dee7"/>
  <text x="456" y="76" font-size="13" font-weight="700" fill="#0b1220">a[lo] + a[hi] = 1 + 11 = 12</text>
  <text x="456" y="100" font-size="13" fill="#dc2626">12 &gt; 9  →  too big, move hi ◀ left</text>
  <text x="456" y="124" font-size="12" fill="#334155">(now 1 + 8 = 9  ✓  found it)</text>
</svg>
```
<div class="readfig"><b>How to read it:</b> The green <b>lo</b> pointer starts at the smallest value, the red <b>hi</b> at the largest. Their sum here is 12, which overshoots 9 — and since everything to the left of <b>hi</b> is smaller, the only way to shrink the sum is to pull <b>hi</b> inward. One step later, <code>1 + 8 = 9</code>. Each move permanently eliminates one number, so the two pointers meet in the middle after a single O(n) sweep.</div>

There are three flavours of this idea: **converging** (from both ends, like above), **same-direction** (a fast reader and a slow writer, for in-place compaction), and **partition** (the Dutch-flag three-way split).

> [key] **Key Insight** — On a *sorted* array, if `a[lo]+a[hi]` is too big, no pair using `hi` can be smaller, so `hi--` discards a whole column safely. Each step eliminates one row or column of the pair matrix ⇒ O(n).

### Recognize by
- sorted array + "find pair / triplet summing to X"
- "partition" / "in-place two-value split" — Dutch National Flag, Sort Colors
- palindrome check, container-with-most-water, trapping rain water (two-pointer variant)

### When NOT to use it
The array **isn't sorted** and you can't afford to sort it (O(n log n) prep) — try a hash-map approach instead. Or the problem needs a *contiguous window* rather than a boundary discard — that's [Sliding Window](#sliding-window).

---

## 3Sum <span class="diff diff-m">Medium</span>

*[↗ LeetCode: 3Sum](https://leetcode.com/problems/3sum/)*

<ProgressCheck id="3sum" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-3sum-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
    <marker id="ar-3sum-success" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/></marker>
    <marker id="ar-3sum-danger" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-danger)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">Sort, fix one value, two-pointer the rest</text>

  <g text-anchor="middle">
    <rect x="44" y="82" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="96" y="82" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="148" y="82" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="200" y="82" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="252" y="82" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="304" y="82" width="44" height="44" rx="7" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="var(--dsa-cell-stroke)"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="66" y="110">-4</text><text x="118" y="110">-1</text><text x="170" y="110">-1</text>
      <text x="222" y="110">0</text><text x="274" y="110">1</text><text x="326" y="110">2</text>
    </g>
    <g font-size="11" fill="var(--dsa-neutral)">
      <text x="66" y="141">0</text><text x="118" y="141">1</text><text x="170" y="141">2</text>
      <text x="222" y="141">3</text><text x="274" y="141">4</text><text x="326" y="141">5</text>
    </g>
  </g>

  <line x1="118" y1="54" x2="118" y2="79" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-3sum-primary)"/>
  <text x="118" y="48" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">i fixed</text>
  <line x1="170" y1="174" x2="170" y2="130" stroke="var(--dsa-success)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-3sum-success)"/>
  <text x="170" y="193" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">left</text>
  <line x1="326" y1="174" x2="326" y2="130" stroke="var(--dsa-danger)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-3sum-danger)"/>
  <text x="326" y="193" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-danger)">right</text>

  <rect x="62" y="210" width="276" height="24" rx="8" fill="var(--dsa-success-soft)" stroke="var(--dsa-success-line)" stroke-width="1.6"/>
  <text x="200" y="227" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">sum = -1 + -1 + 2 = 0 → hit!</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> Once <code>i</code> is fixed, the sorted suffix is a two-sum problem; move <code>left</code>/<code>right</code> until the triple hits zero, then skip duplicates.</div>

### Problem
Find **all unique triplets** `(a, b, c)` in the array with `a + b + c = 0`. The output must contain no duplicate triplets.

**Constraints:** `3 ≤ n ≤ 3000`; values fit in `int`; the array is unsorted (you'll sort it first).

**Example 1:** `[-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`.

**Example 2:** `[0,0,0,0]` → `[[0,0,0]]` (many duplicates, one unique triplet).

### Solution — brute force
Brute force is three nested loops over `i < j < k`, checking every triplet and putting sorted triplets into a set to avoid duplicates. That is O(n³) time plus output/dedup space, and it times out quickly at `n = 3000`. Sorting first lets us fix one value and replace the inner pair scan with two pointers, cutting the search to O(n²) while still skipping duplicates deterministically.

```java
List<List<Integer>> threeSumBrute(int[] a) {
    Set<List<Integer>> seen = new HashSet<>();
    for (int i = 0; i < a.length; i++)
        for (int j = i + 1; j < a.length; j++)
            for (int k = j + 1; k < a.length; k++)
                if (a[i] + a[j] + a[k] == 0) {
                    List<Integer> t = Arrays.asList(a[i], a[j], a[k]);
                    Collections.sort(t);
                    seen.add(t);
                }
    return new ArrayList<>(seen);
}
```

**Brute-force cost:** O(n³) time plus dedup/output space — too slow for n ≥ 10⁴.

### Solution — optimized
Sorting turns the inner two-number search into a monotone two-pointer scan. Fix one pivot, search for its negated complement, and skip equal values so the same triplet is emitted once.

**Pattern.**
Sort, fix one element, converge two pointers for the remaining pair; skip duplicates at every level.

**Steps.**
1. Sort the array — sortedness lets us prune and two-pointer.
2. Loop `i` over each element as the outer pivot. Skip duplicate pivots: `if (i > 0 && a[i] == a[i-1]) continue;`.
3. For each pivot, set `lo = i+1`, `hi = n-1`; hunt pairs summing to `-a[i]`.
4. If `s < 0` → `lo++`; if `s > 0` → `hi--`; if `s == 0` → record the triplet.
5. After a hit, skip duplicates on **both** pointers before advancing: `while (a[lo]==a[lo+1]) lo++;` and mirror for `hi`.
6. Break early when `a[i] > 0` — no positive triple sums to zero.

**Java.**
```java
List<List<Integer>> threeSum(int[] a) {
    Arrays.sort(a);
    List<List<Integer>> res = new ArrayList<>();
    for (int i = 0; i < a.length - 2; i++) {
        if (i > 0 && a[i] == a[i-1]) continue;               // skip dup pivot
        if (a[i] > 0) break;                                  // smallest already positive
        int lo = i + 1, hi = a.length - 1;
        while (lo < hi) {
            int s = a[i] + a[lo] + a[hi];
            if (s == 0) {
                res.add(List.of(a[i], a[lo], a[hi]));
                while (lo < hi && a[lo] == a[lo+1]) lo++;      // skip dup
                while (lo < hi && a[hi] == a[hi-1]) hi--;
                lo++; hi--;
            } else if (s < 0) lo++;
            else hi--;
        }
    }
    return res;
}
```

### Time Complexity
Existing summary: Time O(n²) · Space O(1) (excluding output/sort).

Sorting costs O(n log n), then each pivot runs a linear two-pointer scan over the suffix, giving O(n²) total; O(n²) dominates the sort for large n.

### Space Complexity
Extra space is O(1) excluding the output and sort implementation, because the algorithm uses only indices and the result list required by the problem.

### Learning notes
- Why sort first? — without sorted order, `lo++`/`hi--` cannot safely discard ranges.
- Why skip duplicate pivots? — the same first value would generate the same triplets again.
- Why `if (a[i] > 0) break`? — after sorting, three positive numbers cannot sum to zero.
- Why set `lo = i + 1`? — each triplet uses indices after the fixed pivot.
- Why skip duplicates after a hit? — equal `lo` or `hi` values would re-emit the same triplet.

> [inv] **Invariant** — For fixed `i`, `[lo,hi]` brackets all unexplored pairs summing toward `-a[i]`; sortedness makes each move monotone.

> [note] **Trace it** — `[-1,0,1,2,-1,-4]` sorts to `[-4,-1,-1,0,1,2]`. Fix `-1`, then two pointers on the rest find `0+1` and `-1+2` → triplets `[-1,0,1]` and `[-1,-1,2]`.

> [note] **Interview script** — "I first confirm the output needs unique triplets and the input is unsorted, so sorting is allowed. I start with brute force by checking all triples and deduping them, which is O(n³) time and too slow. I optimize by sorting, fixing one pivot, and two-pointering the remaining pair with duplicate skips for O(n²) time and O(1) extra space excluding output."

> [trap] **Common Trap** — Missing any of the three duplicate-skips yields repeated triplets. *Example:* `nums=[-1,-1,-1,2]`. Without skipping duplicate pivots you emit `[-1,-1,2]` twice (once per `-1` as pivot); without skipping `lo`/`hi` after a hit, `[0,0,0,0]` emits `[0,0,0]` multiple times.

> [pat] **Pattern Connection** — Generalizes to k-Sum by recursion (fix outer indices, two-pointer the base case). 4Sum = one more loop.

### Common Mistakes

- **Missing any of the three duplicate-skips** — pivot, `lo`, `hi`. All three are required.
- **Advancing `lo`/`hi` before skipping duplicates** — do the skip on the value you just consumed, then advance.
- **Using `long` for the sum** unnecessary here (constraints keep it within `int`), but confirm when values approach `10⁹`.
- **Not sorting first** breaks the two-pointer discard argument — the whole approach collapses to O(n³).

### Same pattern, new tweaks

Sort once, then let two converging pointers do the work — the target and the counting change, the skeleton doesn't:

| Variation | The one thing that changes | Time |
|---|---|---|
| [3Sum Closest](https://leetcode.com/problems/3sum-closest/) | instead of hunting for exactly 0, track the sum closest to `target` as the pointers move | — |
| [3Sum Smaller](https://leetcode.com/problems/3sum-smaller/) | count triplets with sum `< target`; when `a[lo]+a[hi] < target`, *all* `hi−lo` pairs qualify at once, so add them in one shot | — |
| [4Sum](https://leetcode.com/problems/4sum/) | add one more outer loop, then two-pointer the inner pair (skip duplicates at every level) | — |
| [Triplets with Smaller Sum](https://leetcode.com/problems/3sum-smaller/) | same batch-counting trick as 3Sum Smaller | — |

## Container With Most Water <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Container With Most Water](https://leetcode.com/problems/container-with-most-water/)*

<ProgressCheck id="container-with-most-water" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-cwm-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">Start widest; move the shorter wall</text>

  <rect x="46" y="151" width="304" height="11" rx="4" fill="var(--dsa-primary-soft)" stroke="var(--dsa-info)" stroke-width="1.6" opacity="0.85"/>
  <line x1="46" y1="162" x2="350" y2="162" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <g text-anchor="middle">
    <rect x="35" y="151" width="22" height="11" rx="4" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
    <rect x="73" y="74" width="22" height="88" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="111" y="96" width="22" height="66" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="149" y="140" width="22" height="22" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="187" y="107" width="22" height="55" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="225" y="118" width="22" height="44" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="263" y="74" width="22" height="88" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="301" y="129" width="22" height="33" rx="4" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
    <rect x="339" y="85" width="22" height="77" rx="4" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
    <g font-size="11" font-weight="700" fill="var(--dsa-ink)">
      <text x="46" y="181">1</text><text x="84" y="181">8</text><text x="122" y="181">6</text><text x="160" y="181">2</text><text x="198" y="181">5</text>
      <text x="236" y="181">4</text><text x="274" y="181">8</text><text x="312" y="181">3</text><text x="350" y="181">7</text>
    </g>
  </g>

  <line x1="46" y1="212" x2="46" y2="166" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-cwm-primary)"/>
  <text x="46" y="231" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">left</text>
  <line x1="350" y1="212" x2="350" y2="166" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-cwm-primary)"/>
  <text x="350" y="231" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">right</text>
  <text x="200" y="207" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--dsa-neutral)">area = min(1,7) × 8 = 8. Move shorter (left) to maximize.</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> The water level is capped by the shorter wall, so with width shrinking each step, only moving the shorter pointer can possibly improve the area.</div>

### Problem
Each element is the height of a vertical wall. Pick the two walls that (with the x-axis) hold the **most water** — area `= min(h[i], h[j]) × (j − i)`.

**Constraints:** `2 ≤ n ≤ 10⁵`; heights `≥ 0`.

**Example 1:** `[1,8,6,2,5,4,8,3,7]` → `49`.

**Example 2:** `[1,1]` → `1` (the only pair has width 1 and height 1).

### Solution — brute force
Brute force checks every pair of walls `(i, j)`, computes `min(h[i], h[j]) * (j - i)`, and keeps the largest area. It is easy to reason about and uses O(1) space, but it is O(n²) time because there are all-pairs choices. The optimized two-pointer version keeps the widest container first and moves only the shorter wall, because moving the taller wall cannot raise the limiting height.

```java
int maxAreaBrute(int[] h) {
    int best = 0;
    for (int i = 0; i < h.length; i++)
        for (int j = i + 1; j < h.length; j++)
            best = Math.max(best, Math.min(h[i], h[j]) * (j - i));
    return best;
}
```

**Brute-force cost:** O(n²) time, O(1) space — too slow for n ≥ 10⁴.

### Solution — optimized
Start with the maximum width and greedily discard the shorter wall. Since width only shrinks, the only possible improvement is finding a taller limiting wall on the short side.

**Pattern.**
Converging pointers; move the **shorter** wall — the only move that can increase area.

**Java.**
```java
int maxArea(int[] h) {
    int l = 0, r = h.length - 1, best = 0;
    while (l < r) {
        best = Math.max(best, Math.min(h[l], h[r]) * (r - l));
        if (h[l] < h[r]) l++; else r--;
    }
    return best;
}
```

### Time Complexity
Existing summary: Time O(n) · Space O(1).

The optimized loop is O(n) because each iteration moves exactly one pointer inward, so there are at most n−1 area checks.

### Space Complexity
Space is O(1) because the method stores two pointers and one best area, with no auxiliary arrays.

### Learning notes
- Why start at both ends? — that gives the largest possible width first.
- Why `Math.min(h[l], h[r])`? — water height is capped by the shorter wall.
- Why multiply by `(r - l)`? — width is the distance between chosen indices.
- Why move the shorter side? — moving the taller side shrinks width without improving the cap.
- Why `while (l < r)`? — a container needs two distinct walls.

> [key] **Key Insight** — Area = `min(h[l],h[r]) × (r−l)`. Width shrinks each step, so only raising the limiting height can help; moving the taller wall can never improve.

> [note] **Trace it** — `[1,8,6,2,5,4,8,3,7]`. Widest pair `8@idx1` and `7@idx8` give `min(8,7)×7 = 49` — the max. Moving the taller side could only shrink width without raising the limiting height.

> [note] **Interview script** — "I first confirm we need the maximum area from two vertical lines and width is index distance. I start with brute force by testing every pair, which is O(n²) time and O(1) space. I optimize with two pointers at the ends, moving the shorter wall each step, for O(n) time and O(1) space."

> [trap] **Common Trap** — Moving the taller wall can never help. *Example:* `heights=[1,8,6,2,5,4,8,3,7]`, `lo=0(h=1), hi=8(h=7)`. Moving `hi` inward shrinks width and can't raise the min (already `1`). Move the shorter wall — the only move that can improve area.

> [pat] **Pattern Connection** — Greedy converging pointers. Contrast with Trapping Rain Water, which *accumulates* water rather than maximizing a single span.

### Same pattern, new tweaks

Two pointers closing in from the ends, always moving the one that can't hurt you:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | instead of maximizing one span, accumulate water per bar using the smaller of the two running maxes | — |
| [Valid Palindrome / Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) | compare from both ends inward; II allows one mismatch (try skipping either side) | — |
| [Boats to Save People](https://leetcode.com/problems/boats-to-save-people/) | sort, then pair the lightest with the heaviest that still fits — a converging-pointer greedy | — |

## Squaring a Sorted Array <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Squares of a Sorted Array](https://leetcode.com/problems/squares-of-a-sorted-array/)*

<ProgressCheck id="squaring-a-sorted-array" />

### Problem
Given a **sorted** array that may contain negatives, return the squares of every number, also in **sorted** order — in O(n).

**Constraints:** `1 ≤ n ≤ 10⁴`; input sorted ascending; negatives allowed (their squares can be the largest).

**Example 1:** `[-4,-1,0,3,10]` → `[0,1,9,16,100]`.

**Example 2:** `[-3,-2,-1]` → `[1,4,9]` (all negatives reverse after squaring).

### Solution — brute force
Brute force squares every element, then sorts the squared values. That is correct because sorting restores the lost order after negatives become positive, but it costs O(n log n) time and O(n) output space. The sorted input still gives structure: the largest remaining square must be at the left or right end, so the optimized method fills the output array from back to front in one pass.

```java
int[] sortedSquaresBrute(int[] a) {
    int[] res = new int[a.length];
    for (int i = 0; i < a.length; i++) res[i] = a[i] * a[i];
    Arrays.sort(res);
    return res;
}
```

**Brute-force cost:** O(n log n) time, O(n) space for output — slower than the required O(n) pass.

### Solution — optimized
Sorted input means the largest absolute value is always at one of the ends. Compare both ends, place the larger square at the back, and shrink the side you used.

**Pattern.**
A sorted array may contain negatives, whose squares are large. Merge from **both ends inward** — the biggest square is always at one of the two ends.

**Java.**
```java
int[] sortedSquares(int[] a) {
    int n = a.length, left = 0, right = n - 1;
    int[] res = new int[n];
    for (int pos = n - 1; pos >= 0; pos--) {   // fill largest-first, back to front
        int ls = a[left] * a[left], rs = a[right] * a[right];
        if (ls > rs) { res[pos] = ls; left++; }
        else         { res[pos] = rs; right--; }
    }
    return res;
}
```

### Time Complexity
Existing summary: Time O(n) · Space O(n) (output).

The optimized pass is O(n) because `pos` fills exactly n slots and each step consumes either `left` or `right` once.

### Space Complexity
Space is O(n) for the required output array. Apart from `res`, the algorithm uses only a few integer pointers.

### Learning notes
- Why compare end squares? — the largest remaining square must be at an extreme.
- Why fill from `n - 1` downward? — we discover squares largest to smallest.
- Why move `left++` when `ls > rs`? — that value has been placed and cannot be reused.
- Why `else` for ties? — either equal square is fine.
- Why not square in place and return? — negatives make squared order unsorted.

> [key] **Key Insight** — After squaring, the array is no longer sorted (e.g. `[-4,-1,0,3]` → `[16,1,0,9]`). But the largest square must come from the most-negative or most-positive value — i.e. an **end**. So compare the two ends, take the larger square, and fill the result **back to front**.

> [inv] **Invariant** — `[left, right]` still spans every element whose square hasn't been placed; `pos` marks the next slot to fill from the right, so the output is built in descending square order.

> [note] **Trace it** — `[-4,-1,0,3,10]`. Compare ends: `(-4)²=16` vs `10²=100` → take 100, then 16, 9, 1, 0; fill the output back-to-front → `[0,1,9,16,100]`.

> [note] **Interview script** — "I first confirm the input is already sorted but may contain negatives, so squared order can break. I start with brute force by squaring everything and sorting, which is O(n log n) time and O(n) space. I optimize by comparing absolute extremes with two pointers and filling from the end, giving O(n) time and O(n) output space."

> [trap] **Common Trap** — Squaring in place, then sorting. *Example:* `nums=[-4,-1,0,3,10]` → squared `[16,1,0,9,100]` still needs a sort (O(n log n)). Two pointers from the ends fill an output array from the back in O(n).

> [pat] **Pattern Connection** — "Merge from both ends because the extreme is at an end" is the same converging-pointer idea as Container With Most Water, and mirrors the merge step of merge sort operating on a fold-point.

### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Sort Transformed Array](https://leetcode.com/problems/squares-of-a-sorted-array/) | after applying `ax²+bx+c` the extremes are at the ends (if `a>0`) or middle (if `a<0`); merge accordingly | — |
| [Merge Sorted Array (in place, from the back)](https://leetcode.com/problems/merge-sorted-array/) | fill from the largest end so you never overwrite unmerged values | — |
| [Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/) | sort both, then two pointers advancing the smaller side | — |

## Sort Colors (Dutch National Flag) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Sort Colors](https://leetcode.com/problems/sort-colors/)*

<ProgressCheck id="sort-colors-dutch-national-flag" />

### Problem
Sort an array of `0`s, `1`s, and `2`s **in place** in a single pass (the Dutch-national-flag problem) — no library sort.

**Constraints:** `1 ≤ n ≤ 300`; values ∈ {0,1,2}; O(1) extra space, one pass.

**Example 1:** `[2,0,2,1,1,0]` → `[0,0,1,1,2,2]`.

**Example 2:** `[0]` → `[0]` (already sorted single bucket).

### Solution — brute force
Brute force can count how many `0`s, `1`s, and `2`s appear, then overwrite the array with that many of each value. That is O(n) time and O(1) space, but it uses two passes; a comparison sort would be O(n log n) and unnecessary. The Dutch National Flag optimization keeps three regions and partitions in one pass, which is the version to present when the interviewer asks for one-pass in-place sorting.

```java
void sortColorsBrute(int[] a) {
    int[] cnt = new int[3];
    for (int x : a) cnt[x]++;
    int idx = 0;
    for (int color = 0; color < 3; color++)
        while (cnt[color]-- > 0) a[idx++] = color;
}
```

**Brute-force cost:** O(n) time and O(1) space, but two passes; a library sort is O(n log n). The one-pass requirement motivates Dutch National Flag.

### Solution — optimized
The optimized partition keeps three regions: confirmed 0s, confirmed 1s, confirmed 2s, and an unknown middle. Each swap grows one confirmed region without needing a second pass.

**Pattern.**
Three-way partition in one pass with three pointers `low, mid, high`.

**Java.**
```java
void sortColors(int[] a) {
    int low = 0, mid = 0, high = a.length - 1;
    while (mid <= high) {
        if (a[mid] == 0)      swap(a, low++, mid++);
        else if (a[mid] == 1) mid++;
        else                  swap(a, mid, high--);   // 2: don't advance mid
    }
}
void swap(int[] a, int i, int j){ int t=a[i]; a[i]=a[j]; a[j]=t; }
```

### Time Complexity
Existing summary: Time O(n) · Space O(1).

The loop is O(n) because `mid` moves right or `high` moves left every iteration, and each element is classified a constant number of times.

### Space Complexity
Space is O(1) because sorting happens in-place with three pointers and a constant-size swap temp.

### Learning notes
- Why `low`, `mid`, `high`? — they mark 0-region, unknown-region, and 2-region boundaries.
- Why advance both after swapping a 0? — the swapped-in value from `low` is already processed.
- Why only `mid++` for a 1? — 1 belongs in the middle region.
- Why not advance `mid` after swapping a 2? — the incoming right-side value is unexamined.
- Why `mid <= high`? — the unknown region includes both endpoints.

> [inv] **Invariant** — `[0,low)`=0s, `[low,mid)`=1s, `(high,n)`=2s; `[mid,high]` unprocessed. The three regions only grow.

> [note] **Trace it** — `[2,0,2,1,1,0]`. `mid` walks forward: 0s swap down to `low`, 2s swap up to `high`, 1s stay → `[0,0,1,1,2,2]` in a single sweep.

> [note] **Interview script** — "I first confirm the only values are 0, 1, and 2 and the array must be sorted in place. I start with brute force as counting buckets or library sort, which is O(n) in two passes or O(n log n) with sort. I optimize with `low`, `mid`, and `high` regions so one scan partitions the array in O(n) time and O(1) space."

> [trap] **Common Trap** — Advancing `mid` after swapping with `high` skips an unexamined value. *Example:* `[2,0,2]`, `mid=1`. Swap `a[mid]` with `a[high]` → `[2,0,2]` (a `2` moves in at `mid`). If you `mid++`, you miss re-evaluating that new value. Advance `mid` only when you swapped with `low` or saw a `1`.

> [pat] **Pattern Connection** — Partitioning is the core of Quickselect/quicksort; the same 3-way scheme handles duplicate-heavy pivots (3-way quicksort).

### Same pattern, new tweaks

"Sweep once, swapping items into buckets by category" generalizes the Dutch-flag idea:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | two categories (nonzero vs zero); a single write-pointer packs nonzeros to the front | — |
| [Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/) | partition into evens then odds with two pointers | — |
| [Wiggle Sort](https://leetcode.com/problems/wiggle-sort-ii/) | partition around the median, then interleave the two halves | — |
| [Partition (Quicksort step)](https://leetcode.com/problems/kth-largest-element-in-an-array/) | the same in-place split around a pivot that powers Quickselect | — |

## Trapping Rain Water <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/)*

<ProgressCheck id="trapping-rain-water" />

### Problem
Each bar has width 1; compute how much **rain water** is trapped between the bars after it rains.

**Constraints:** `1 ≤ n ≤ 2·10⁴`; heights `≥ 0`; target O(n) time, O(1) space.

**Example 1:** `[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`.

**Example 2:** `[4,2,0,3,2,5]` → `9` (global side walls matter, not nearest bars).

### Solution — brute force
Brute force computes water at each index by scanning left for the tallest wall and scanning right for the tallest wall, then adding `min(leftMax, rightMax) - height[i]`. That is correct but costs O(n²) time and O(1) space. Precomputing prefix/suffix maxima gives O(n) time with O(n) space; the shown two-pointer version compresses those maxima into two running values for O(1) extra space.

```java
int trapBrute(int[] h) {
    int water = 0;
    for (int i = 0; i < h.length; i++) {
        int leftMax = 0, rightMax = 0;
        for (int l = i; l >= 0; l--) leftMax = Math.max(leftMax, h[l]);
        for (int r = i; r < h.length; r++) rightMax = Math.max(rightMax, h[r]);
        water += Math.min(leftMax, rightMax) - h[i];
    }
    return water;
}
```

**Brute-force cost:** O(n²) time, O(1) space — too slow for n ≥ 10⁴.

### Solution — optimized
The optimized two-pointer version keeps the best wall seen from each side. Whichever side has the smaller current height can be resolved now, because a sufficient opposite wall exists on the other side.

**Pattern.**
Two pointers tracking `leftMax`/`rightMax`; water over a bar is bounded by the smaller side's running max.

**Steps.**
1. Two pointers `lo=0, hi=n-1`; carry `leftMax = 0`, `rightMax = 0`.
2. At each step, compare `heights[lo]` vs `heights[hi]`. The **shorter** side bounds the water.
3. If `heights[lo] < heights[hi]`: if `heights[lo] >= leftMax`, update `leftMax`; else add `leftMax - heights[lo]` to the answer. Advance `lo++`.
4. Symmetric on the right side: advance `hi--`.
5. Loop until `lo >= hi`. Every cell contributes at most once — O(n) time, O(1) space.

**Java.**
```java
int trap(int[] h) {
    int l = 0, r = h.length - 1, lMax = 0, rMax = 0, water = 0;
    while (l < r) {
        if (h[l] < h[r]) {
            lMax = Math.max(lMax, h[l]);
            water += lMax - h[l];
            l++;
        } else {
            rMax = Math.max(rMax, h[r]);
            water += rMax - h[r];
            r--;
        }
    }
    return water;
}
```

### Time Complexity
Existing summary: Time O(n) · Space O(1).

The algorithm is O(n) because each iteration moves either `l` or `r` inward, so every bar is processed once.

### Space Complexity
Space is O(1) because only two pointers, two running maxima, and the water total are stored.

### Learning notes
- Why keep `lMax` and `rMax`? — water depends on the best boundary seen from each side.
- Why compare `h[l] < h[r]`? — the shorter side is safe to resolve now.
- Why update max before adding water? — a new wall traps zero water at itself.
- Why `water += lMax - h[l]`? — that is the fill level above the left bar.
- Why not use nearest peaks? — trapped water uses global maxima, not local neighbors.

> [key] **Key Insight** — Water above `i` = `min(maxLeft, maxRight) − h[i]`. Advance from the side with the smaller max, because that side's bound is fixed regardless of what lies beyond.

> [inv] **Invariant** — If `leftMax ≤ rightMax`, the water at `left` depends only on `leftMax` (a taller-or-equal wall is guaranteed on the right).

> [note] **Trace it** — `[0,1,0,2,1,0,1,3,2,1,2,1]` traps **6** units. Over the `0` at index 2, water rises to `min(leftMax=1, rightMax=3)=1`, so 1 unit sits there; summing every bar gives 6.

> [note] **Interview script** — "I first confirm each bar has width one and water over a bar depends on the smaller boundary wall. I start with brute force by scanning left and right from every index, which is O(n²) time and O(1) space. I optimize by carrying `leftMax` and `rightMax` with two pointers, so each bar is processed once in O(n) time and O(1) space."

> [trap] **Common Trap** — Local vs global boundaries. *Example:* `heights=[4,2,0,3,2,5]`. Water above index 3 (h=3) is bounded by the global `4` on the left and `5` on the right — not by 3. Track running max from each side (or the shorter side with two pointers).

> [pat] **Pattern Connection** — Also solvable with a monotonic (decreasing) stack that resolves trapped basins between bars — a good cross-check of the two viewpoints.

### Common Mistakes

- **Local maxima vs global**: water above a cell depends on the global bounding walls, not on the nearest peak.
- **Wrong side advances**: only move the pointer on the shorter side — that's the one whose water level is determined.
- **Missing the `>= leftMax` check**: without it, you subtract on `leftMax = heights[lo]` and get negative contributions.
- **Stack-based alternative**: also O(n) but uses O(n) space; two-pointer is O(1).

### Same pattern, new tweaks

"Water/area is bounded by the smaller enclosing wall" shows up in a few disguises:

| Variation | The one thing that changes | Time |
|---|---|---|
| [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | maximize a single span instead of summing trapped water; move the shorter wall | — |
| [Trapping Rain Water II (2D)](https://leetcode.com/problems/trapping-rain-water-ii/) | the "walls" are a whole grid boundary, so process cells outward from the lowest border using a min-heap | — |
| [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | the dual "peak" view — a monotonic stack finds how far each bar extends | — |

---

## Check your understanding

<Quiz patternId="two-pointers" :questions='[
  {
    "q": "In sorted two-sum, the current sum is too large. Which pointer move is justified?",
    "choices": [
      {
        "text": "Move lo right"
      },
      {
        "text": "Move hi left",
        "correct": true,
        "explanation": "Yes. With a sorted array, lowering the larger endpoint discards an entire impossible column."
      },
      {
        "text": "Move both pointers"
      },
      {
        "text": "Restart from the middle"
      }
    ]
  },
  {
    "q": "In Container With Most Water, which wall should move after evaluating an area?",
    "choices": [
      {
        "text": "Always move the taller wall",
        "explanation": "Moving the taller wall only shrinks width without improving the limiting height."
      },
      {
        "text": "Always move both walls"
      },
      {
        "text": "Move the shorter wall",
        "correct": true,
        "explanation": "Right. Only replacing the limiting shorter wall can possibly improve the area."
      },
      {
        "text": "Move a random wall"
      }
    ]
  },
  {
    "q": "In Dutch National Flag, after swapping a 2 with high, why should mid not advance immediately?",
    "choices": [
      {
        "text": "The swapped-in value is unexamined",
        "correct": true,
        "explanation": "Exactly. The value from high could be 0, 1, or 2 and must be processed at mid."
      },
      {
        "text": "high must move right"
      },
      {
        "text": "The array becomes unsorted"
      },
      {
        "text": "mid should reset to zero"
      }
    ]
  }
]' />
