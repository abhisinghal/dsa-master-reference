# Hashing

Almost every problem starts life as an array, and the single most useful upgrade you can make to an array algorithm is a **hash map**. Here's the pattern to watch for: a brute-force solution says *"for each element, look through all the others"* — that's the O(n²) nested loop. A hash map lets you **remember what you've already seen**, so instead of re-scanning you just ask "have I seen the thing I need?" in O(1). That one swap collapses a whole class of problems from O(n²) down to O(n).

Throughout this chapter you'll meet the same few moves: **complement lookup** (remember values, then ask for the partner), **frequency signatures** (turn a group into a canonical key so equal things land together), and **prefix/suffix products** (carry a running result in from each side).

<Callout kind="key" title="Key Insight">

Whenever a brute force does "for each element, scan the rest" (O(n²)), ask: *can a hash map remember what I've seen so I never rescan?* That single question collapses a huge class of problems to O(n).

</Callout>

### Recognize by
- "pair / triplet summing to target", "any duplicate?", "first non-repeated"
- "group by canonical key" — anagrams, isomorphic strings, group shifted strings
- "seen this before?" — cycle detection in a functional graph (Happy Number), longest consecutive sequence

### When NOT to use it
You need a *contiguous* result (subarray, substring) and the running quantity is monotone — [Sliding Window](/patterns/sliding-window) is O(1) extra space vs. the map's O(n). Also skip hashing when the *order* between duplicates matters (hash maps lose it).

---

## Two Sum
*[↗ LeetCode: Two Sum](https://leetcode.com/problems/two-sum/)*

### Problem
Given an array `nums` and a `target`, return the **indices** of the two entries that add up to `target`. Exactly one pair works, and you can't reuse the same index.

**Constraints:** `2 ≤ nums.length ≤ 10⁴`; the array is **not sorted**; values fit in `int`.

**Example 1:** `nums = [2,7,11,15], target = 9` → `[0,1]` (since `2 + 7 = 9`).

**Example 2:** `nums = [3,3], target = 6` → `[0,1]` (two equal values must be different indices).

### Try it yourself

Complete the `Main` class below and click **▶ Run tests**. Your code compiles and runs against the two examples via the Judge0 API. Code auto-saves to your browser.

<JavaRunner
  problemSlug="two-sum"
  :tests='[
    { input: "4\n2 7 11 15\n9", expected: "0 1" },
    { input: "2\n3 3\n6", expected: "0 1" }
  ]'
/>

### Solution — brute force
Nested loop: for each `i`, scan `j > i` for `nums[i] + nums[j] == target`. This is O(n²) time and O(1) space, and it is correct but too slow once `n` reaches `10⁴`. The hash-map optimization avoids the inner scan by remembering values already seen and asking whether the current value's complement has appeared.



```java
int[] twoSumBrute(int[] a, int target) {
    for (int i = 0; i < a.length; i++)
        for (int j = i + 1; j < a.length; j++)
            if (a[i] + a[j] == target) return new int[]{i, j};
    return new int[]{-1, -1};
}
```



**Brute-force cost:** O(n²) time, O(1) space — too slow for n ≥ 10⁴.

### Solution — optimized
The optimized one-pass map stores values already seen. At each index, check whether the exact complement is already behind you; checking before insert prevents using the same index twice.

**Pattern.**
Complement lookup: replace nested search with one-pass hashing.

**Steps.**
1. Create an empty hash map from value → index.
2. Scan the array once. For each `a[i]`, compute `need = target - a[i]`.
3. If `need` is in the map, return `{map[need], i}`.
4. Otherwise `map[a[i]] = i`. Check-then-insert (never the other way — an element would match itself).

**Java.**


```java
int[] twoSum(int[] a, int target) {
    Map<Integer,Integer> seen = new HashMap<>();
    for (int i = 0; i < a.length; i++) {
        Integer j = seen.get(target - a[i]);
        if (j != null) return new int[]{j, i};
        seen.put(a[i], i);
    }
    return new int[]{-1,-1};
}
```



### Time Complexity
Existing summary: Time O(n) · Space O(n).

The scan is O(n) expected time because each element performs one hash lookup and one hash insert on average.

### Space Complexity
Space is O(n) in the worst case because the map may store every prior value before the answer appears.

### Learning notes
- Why `Map<Integer,Integer>`? — we need the partner value and must return its index.
- Why compute `target - a[i]`? — that is the only value that completes the pair.
- Why check before `seen.put`? — otherwise an element could match itself.
- Why use `Integer j`? — `null` cleanly means the complement was absent.
- Why return `{j, i}`? — `j` is the earlier stored index.

<Callout kind="key" title="Key Insight">

For each `x`, the partner you need is `target - x`. Remember values as you go; check before inserting.

</Callout>

<Callout kind="inv" title="Invariant">

When at index `i`, the map holds every value at indices `< i` with its index.

</Callout>

<Callout kind="note" title="Trace it">

`a=[2,7,11,15], target=9`. At `i=1` (value 7) the partner is `9−7=2`, already stored from `i=0` → return `[0,1]`. No full rescan needed.

</Callout>

<Callout kind="note" title="Interview script">

"I first confirm there is exactly one answer and I should return indices, not values. I start with brute force by checking every pair, which is O(n²) time and O(1) space. I optimize by storing seen values in a hash map and checking `target - a[i]` during one scan, giving O(n) time and O(n) space."

</Callout>

<Callout kind="trap" title="Common Trap">

Inserting into the map **before** the check makes an element match itself. *Example:* `nums=[3,2,4]`, `target=6`. If you `put(3,0)` first, then check for `target-3=3`, you find yourself and emit `(0,0)`. Check first, insert after.

</Callout>

<Callout kind="pat" title="Pattern Connection">

Hashing. In a *sorted* array the same task becomes **two pointers** in O(1) space; the sorted-vs-unsorted choice recurs throughout.

</Callout>

### Same pattern, new tweaks

Every variation below changes **exactly one** constraint — and that one change dictates the approach. This is the real skill: recognizing which lever moved.

| Variation | The one thing that changes | So the approach becomes… | Time · Space |
|---|---|---|---|
| [Two Sum II — sorted input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | the array is **already sorted** | drop the map — converge two pointers from both ends (sum too small → `lo++`; too big → `hi--`) | O(n) · **O(1)** |
| [3Sum](https://leetcode.com/problems/3sum/) | need **three** numbers summing to 0, no duplicate triplets | sort; fix `a[i]`, then two-pointer the rest for `−a[i]`; skip equal values to dedupe | O(n²) · O(1) |
| [4Sum](https://leetcode.com/problems/4sum/) | **four** numbers summing to `target` | sort; fix two indices with nested loops, two-pointer the remaining pair | O(n³) · O(1) |
| [Two Sum III — design](https://leetcode.com/problems/two-sum-iii-data-structure-design/) | numbers **arrive over time**, many `find` queries | keep a running frequency map; `add` O(1), `find(t)` checks each key `k` for `t−k` | O(1) add · O(n) find |
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | want a **contiguous subarray** summing to k | hash **prefix sums**, not raw values: a subarray sums to k iff two prefixes differ by k | O(n) · O(n) |
| [Two Sum Less Than K](https://leetcode.com/problems/two-sum-less-than-k/) | largest pair sum strictly **&lt; K** | sort + two pointers, recording the best sum seen below K | O(n log n) · O(1) |

<Callout kind="pat" title="The thread that ties them together">

all of these are *"find elements that combine to a target."* The decision tree is short: **unsorted + exact pair** → hash the complement · **sorted** → two pointers (O(1) space) · **k numbers** → fix `k−2`, two-pointer the last two · **contiguous** → hash prefix sums · **maximize under a bound** → sort + two pointers. Same idea, five faces.

</Callout>

## Group Anagrams
*[↗ LeetCode: Group Anagrams](https://leetcode.com/problems/group-anagrams/)*

### Problem
Given a list of words, bucket together the ones that are **anagrams** of each other (same letters, any order). Return the groups in any order.

**Constraints:** up to `10⁴` words, lowercase `a–z`; total characters up to ~10⁵.

**Example 1:** `["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"],["tan","nat"],["bat"]]`.

**Example 2:** `["", "b"]` → `[[""],["b"]]` (empty string has the all-zero signature).

### Solution — brute force
Brute force compares each word against every other word by sorting both words or counting letters and checking equality. That can reach O(n²·L log L) time with a visited array, which is correct but wasteful because each group comparison repeats work. The optimized version computes one canonical signature per word and uses it as a hash-map key, so all anagrams land in the same bucket immediately.



```java
List<List<String>> groupAnagramsBrute(String[] strs) {
    boolean[] used = new boolean[strs.length];
    List<List<String>> ans = new ArrayList<>();
    for (int i = 0; i < strs.length; i++) {
        if (used[i]) continue;
        List<String> group = new ArrayList<>();
        for (int j = i; j < strs.length; j++) {
            if (!used[j] && sameLetters(strs[i], strs[j])) { used[j] = true; group.add(strs[j]); }
        }
        ans.add(group);
    }
    return ans;
}
boolean sameLetters(String a, String b) {
    if (a.length() != b.length()) return false;
    int[] cnt = new int[26];
    for (char c : a.toCharArray()) cnt[c - 'a']++;
    for (char c : b.toCharArray()) if (--cnt[c - 'a'] < 0) return false;
    return true;
}
```



**Brute-force cost:** O(n²·L) or O(n²·L log L) depending on the comparison helper, plus output space — too slow for n ≥ 10⁴.

### Solution — optimized
Compute one canonical signature per word, then let the hash map gather equal signatures into the same list. This avoids comparing every word pair repeatedly.

**Pattern.**
Canonical-key hashing: map each item to a signature so equivalents collide.

**Java.**


```java
List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        int[] cnt = new int[26];
        for (char c : s.toCharArray()) cnt[c - 'a']++;
        StringBuilder key = new StringBuilder();
        for (int c : cnt) key.append(c).append('#');   // delimiter avoids 1,11 vs 11,1 collision
        groups.computeIfAbsent(key.toString(), k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```



### Time Complexity
Existing summary: Time O(n·L) · Space O(n·L).

The optimized method is O(n·L) because every character of every word is counted once, and building the 26-count key is constant-size per word for lowercase English letters.

### Space Complexity
Space is O(n·L) for the grouped output plus hash keys/lists; each input string is placed into exactly one bucket.

### Learning notes
- Why `int[] cnt = new int[26]`? — lowercase a–z gives a fixed frequency vector.
- Why `c - 'a'`? — it maps letters to indices 0 through 25.
- Why build a `StringBuilder` key? — arrays do not compare by contents as map keys.
- Why append `#` delimiter? — it prevents count-collision strings like `1,11` vs `11,1`.
- Why `computeIfAbsent`? — it creates the bucket exactly once.

<Callout kind="key" title="Key Insight">

Anagrams share a canonical form. Use the 26-count signature (O(L)) rather than sorting (O(L log L)) when the alphabet is fixed.

</Callout>

<Callout kind="note" title="Trace it">

`["eat","tea","tan","ate","nat","bat"]`. Count-signatures make `eat/tea/ate` collide, `tan/nat` collide, `bat` alone → `[[eat,tea,ate],[tan,nat],[bat]]`.

</Callout>

<Callout kind="note" title="Interview script">

"I first confirm words are lowercase and group order does not matter. I start with brute force by comparing every pair of words for anagram equality, which is O(n²·L log L) time in the sorting version. I optimize by building one 26-count signature per word and hashing groups by that key, for O(n·L) time and O(n·L) space."

</Callout>

<Callout kind="trap" title="Common Trap">

Building the count key without a delimiter collides distinct histograms. *Example:* counts `[1,11]` and `[11,1]` both stringify to `"111"` and get grouped together. Separate fields — e.g. `"1#11"` vs `"11#1"`.

</Callout>

<Callout kind="pat" title="Pattern Connection">

"Signature hashing" also powers Group Shifted Strings and isomorphic-string checks.

</Callout>

### Same pattern, new tweaks

Same move — *"map each item to a canonical key so equivalents collide"* — only the definition of "equivalent" changes:

| Variation | "Equivalent" means… | So the key is… |
|---|---|---|
| [Group Shifted Strings](https://leetcode.com/problems/group-shifted-strings/) | same **shift pattern** (`"abc"`≡`"bcd"`) | the sequence of gaps between consecutive letters (mod 26) |
| [Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/) | same **structure** (`"egg"`≡`"add"`) | the first-occurrence-position pattern (`"egg"` → `0,1,1`) |
| [Find Duplicate File in System](https://leetcode.com/problems/find-duplicate-file-in-system/) | same **content** | the file's content string |
| [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | two strings, not a whole group | compare the two 26-count signatures directly |

## Product of Array Except Self
*[↗ LeetCode: Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)*

### Problem
Return an array where `answer[i]` is the product of **every element except** `nums[i]` — **without using division**, in O(n) time.

**Constraints:** `2 ≤ n ≤ 10⁵`; the full product fits in a 32-bit int; division is disallowed (and would break on zeros anyway).

**Example 1:** `nums = [1,2,3,4]` → `[24,12,8,6]` (e.g. position 0 = 2·3·4).

**Example 2:** `nums = [-1,1,0,-3,3]` → `[0,0,9,0,0]` (one zero makes only the zero position nonzero).

### Solution — brute force
Brute force builds each `answer[i]` by multiplying every element except index `i`. That is O(n²) time and O(1) extra space beyond the output, and division is not allowed anyway. The optimized idea precomputes the product to the left and the product to the right of each index; the Java code stores the left product in the output, then multiplies in a running right product.



```java
int[] productExceptSelfBrute(int[] a) {
    int[] out = new int[a.length];
    for (int i = 0; i < a.length; i++) {
        int product = 1;
        for (int j = 0; j < a.length; j++) if (i != j) product *= a[j];
        out[i] = product;
    }
    return out;
}
```



**Brute-force cost:** O(n²) time, O(1) extra space beyond output — too slow for n ≥ 10⁴.

### Solution — optimized
The optimized method splits the answer into left product and right product. It writes all left products into `out`, then walks from the right multiplying in the product of elements after each index.

**Pattern.**
Prefix × suffix without division.

**Java.**


```java
int[] productExceptSelf(int[] a) {
    int n = a.length; int[] out = new int[n];
    out[0] = 1;
    for (int i = 1; i < n; i++) out[i] = out[i-1] * a[i-1];   // prefix
    int right = 1;
    for (int i = n - 1; i >= 0; i--) { out[i] *= right; right *= a[i]; }  // suffix
    return out;
}
```



### Time Complexity
Existing summary: Time O(n) · Space O(1) extra (output aside).

The algorithm is O(n) because it performs one left-to-right pass and one right-to-left pass, with constant work per index.

### Space Complexity
Extra space is O(1) excluding the required output array: `out` stores the answer, and `right` is the only additional running aggregate.

### Learning notes
- Why set `out[0] = 1`? — there are no elements to the left of index 0.
- Why start the prefix loop at `i = 1`? — `out[i]` depends on `out[i-1] * a[i-1]`.
- Why walk from `n - 1` down? — that accumulates the product strictly to the right.
- Why multiply `out[i] *= right` before `right *= a[i]`? — `a[i]` itself must be excluded.
- Why no division? — zeros make division unsafe and the prompt disallows it.

<Callout kind="key" title="Key Insight">

`answer[i] = (∏ left of i) × (∏ right of i)`. Two sweeps; carry the running product in the output array to hit O(1) extra space.

</Callout>

<Callout kind="inv" title="Invariant">

After the left sweep, `out[i]` holds the product of all elements strictly left of `i`; the right sweep multiplies in the running right product.

</Callout>

<Callout kind="note" title="Trace it">

`[1,2,3,4]`. Left-products `[1,1,2,6]`, then multiply each by the running right-product → `[24,12,8,6]`. Position 0 = 2·3·4, position 3 = 1·2·3.

</Callout>

<Callout kind="note" title="Interview script">

"I first confirm division is disallowed and zeros may appear, so total-product division is not safe. I start with brute force by multiplying all other entries for every index, which is O(n²) time and O(1) extra space. I optimize with prefix and suffix products in two sweeps, giving O(n) time and O(1) extra space besides the output."

</Callout>

<Callout kind="trap" title="Common Trap">

Reaching for division. *Example:* `nums=[1,2,0,4]` — dividing the total product by each element blows up at the zero. The prefix/suffix product is division-free and zero-safe.

</Callout>

<Callout kind="pat" title="Pattern Connection">

Prefix/suffix aggregation — the same skeleton as Trapping Rain Water (prefix/suffix max) and candy-distribution problems.

</Callout>

### Same pattern, new tweaks

Same skeleton — *combine a running result from the left with one from the right* — only the aggregate changes:

| Variation | The one thing that changes | So the aggregate is… | Time · Space |
|---|---|---|---|
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | water is bounded by the shorter wall | running **max** from each side; water = `min(L,R) − height` | O(n) · O(1) |
| [Candy](https://leetcode.com/problems/candy/) | each child must beat both neighbours | two passes (L→R then R→L), take the **max** requirement | O(n) · O(n) |
| [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | a negative flips sign | track running **max *and* min** so a sign-flip can become the new best | O(n) · O(1) |

## Longest Consecutive Sequence
*[↗ LeetCode: Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)*

### Problem
Given an **unsorted** array, find the length of the longest run of **consecutive integers** (like 1,2,3,4) — in O(n), so sorting (O(n log n)) is off the table.

**Constraints:** `0 ≤ n ≤ 10⁵`; values span the full int range; duplicates may appear.

**Example 1:** `nums = [100,4,200,1,3,2]` → `4` (the run `1,2,3,4`).

**Example 2:** `nums = []` → `0` (no numbers means no run).

### Solution — brute force
Brute force can start from every number and repeatedly search the array for the next value `x + 1`. With a linear search each step, a run like `1..n` degenerates to O(n²) time, though it uses only O(1) extra space. Sorting is O(n log n), but the target is O(n), so the optimized set method starts only at true run beginnings and walks each number at most once.



```java
int longestConsecutiveBrute(int[] nums) {
    int best = 0;
    for (int x : nums) {
        int len = 1, cur = x;
        while (contains(nums, cur + 1)) { cur++; len++; }
        best = Math.max(best, len);
    }
    return best;
}
boolean contains(int[] nums, int target) {
    for (int x : nums) if (x == target) return true;
    return false;
}
```



**Brute-force cost:** O(n²) time with repeated linear searches, O(1) space — too slow for n ≥ 10⁴.

### Solution — optimized
The set gives O(1) membership checks, but the real optimization is starting only at sequence beginnings. If `x - 1` exists, `x` belongs to a run that will be counted from an earlier value.

**Pattern.**
Hash set + "only start counting from a sequence's left end."

**Java.**


```java
int longestConsecutive(int[] nums) {
    Set<Integer> set = new HashSet<>();
    for (int x : nums) set.add(x);
    int best = 0;
    for (int x : set) {
        if (set.contains(x - 1)) continue;      // not a run start
        int cur = x, len = 1;
        while (set.contains(cur + 1)) { cur++; len++; }
        best = Math.max(best, len);
    }
    return best;
}
```



### Time Complexity
Existing summary: Time O(n) · Space O(n).

Expected time is O(n): building the set scans all numbers once, and the inner while walks each consecutive value only when starting from the run boundary.

### Space Complexity
Space is O(n) because the hash set stores the distinct input values; duplicates collapse into one set entry.

### Learning notes
- Why build a `HashSet` first? — membership checks become expected O(1).
- Why iterate over `set`, not `nums`? — duplicates should not restart the same run.
- Why `if (set.contains(x - 1)) continue`? — only the left boundary should expand a run.
- Why initialize `len = 1`? — a run start counts itself.
- Why `best` starts at 0? — empty input should return 0.

<Callout kind="key" title="Key Insight">

Put all numbers in a set. A number `x` begins a run **iff** `x-1` is absent. Only then walk `x, x+1, …`. Each number is visited at most twice → O(n).

</Callout>

<Callout kind="inv" title="Invariant">

Inner `while` extends only from true run-starts, so total inner steps ≤ n across the whole outer loop.

</Callout>

<Callout kind="note" title="Trace it">

`[100,4,200,1,3,2]`. Only `1` and `100` and `200` are run-starts (their predecessor is absent). From `1` walk `1,2,3,4` → length **4**; the others give length 1.

</Callout>

<Callout kind="note" title="Interview script">

"I first confirm the array is unsorted, duplicates may exist, and the target is the length of the longest consecutive run. I start with brute force by trying to extend a run from every value with repeated searches, which is O(n²) time. I optimize by putting values in a set and expanding only when `x - 1` is absent, giving O(n) time and O(n) space."

</Callout>

<Callout kind="trap" title="Common Trap">

Omitting the `x-1` guard makes it O(n²). *Example:* `nums=[1,2,3,4]` — without the guard you walk the run from 1, then from 2, then from 3, then from 4 → 4+3+2+1 steps. Only start from values whose predecessor is absent.

</Callout>

<Callout kind="pat" title="Pattern Connection">

"Start from the boundary" recurs in grid/graph flood-fill and interval merging: identify canonical entry points to avoid redundant work.

</Callout>

### Same pattern, new tweaks

Same skeleton — *put everything in a set, then only start work from a canonical entry point* to avoid redundant re-scans:

| Variation | The one thing that changes | Canonical "start" is… | Time |
|---|---|---|---|
| [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 1-D runs of integers | a number `x` whose predecessor `x−1` is absent | O(n) |
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | 2-D grid connectivity | any unvisited land cell (flood it once) | O(R·C) |
| [Word Ladder](https://leetcode.com/problems/word-ladder/) | words linked by 1-letter edits | dedup words in a set so each transform is explored once | O(N·L²) |
