# Hashing

Almost every problem starts life as an array, and the single most useful upgrade you can make to an array algorithm is a **hash map**. Here's the pattern to watch for: a brute-force solution says *"for each element, look through all the others"* — that's the O(n²) nested loop. A hash map lets you **remember what you've already seen**, so instead of re-scanning you just ask "have I seen the thing I need?" in O(1). That one swap collapses a whole class of problems from O(n²) down to O(n).

Throughout this chapter you'll meet the same few moves: **complement lookup** (remember values, then ask for the partner), **frequency signatures** (turn a group into a canonical key so equal things land together), and **prefix/suffix products** (carry a running result in from each side).

> [key] **Key Insight** — Whenever a brute force does "for each element, scan the rest" (O(n²)), ask: *can a hash map remember what I've seen so I never rescan?* That single question collapses a huge class of problems to O(n).

### Recognize by
- "pair / triplet summing to target", "any duplicate?", "first non-repeated"
- "group by canonical key" — anagrams, isomorphic strings, group shifted strings
- "seen this before?" — cycle detection in a functional graph (Happy Number), longest consecutive sequence

### When NOT to use it
You need a *contiguous* result (subarray, substring) and the running quantity is monotone — [Sliding Window](#sliding-window) is O(1) extra space vs. the map's O(n). Also skip hashing when the *order* between duplicates matters (hash maps lose it).

---

## Two Sum <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Two Sum](https://leetcode.com/problems/two-sum/)*

<TwoSumStepStrip />

### Try it yourself

Edit the Java code below and click **▶ Run tests** to check it against real examples. Powered by [Judge0](https://ce.judge0.com); your code auto-saves in your browser.

<JavaRunner problemSlug="two-sum" :tests='[{ input: "4\n2 7 11 15\n9", expected: "0 1" }, { input: "2\n3 3\n6", expected: "0 1" }]' />


<ProgressCheck id="two-sum" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-ts-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">Complement lookup turns pair search into O(1)</text>
  <text x="82" y="56" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-neutral)">target = 9</text>

  <g text-anchor="middle">
    <rect x="28" y="84" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="80" y="84" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="132" y="84" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <rect x="184" y="84" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="var(--dsa-cell-stroke)"/>
    <g font-size="17" font-weight="700" fill="var(--dsa-ink)">
      <text x="50" y="112">2</text><text x="102" y="112">7</text><text x="154" y="112">11</text><text x="206" y="112">15</text>
    </g>
    <g font-size="11" fill="var(--dsa-neutral)">
      <text x="50" y="143">0</text><text x="102" y="143">1</text><text x="154" y="143">2</text><text x="206" y="143">3</text>
    </g>
  </g>

  <path d="M72 108 C118 62 222 62 268 96" fill="none" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-ts-primary)"/>
  <text x="169" y="61" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">complement 7 → seen?</text>
  <rect x="260" y="84" width="112" height="72" rx="10" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <text x="316" y="106" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">hash map</text>
  <text x="316" y="132" text-anchor="middle" font-size="15" font-weight="700" fill="var(--dsa-success)">{7→1}</text>
  <rect x="132" y="190" width="136" height="28" rx="9" fill="var(--dsa-success-soft)" stroke="var(--dsa-success-line)" stroke-width="1.6"/>
  <text x="200" y="209" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-success)">return [0,1]</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> For each value, compute the exact partner needed and ask the map in O(1); this trades O(n) space for a one-pass O(n) search.</div>

### Problem
Given an array `nums` and a `target`, return the **indices** of the two entries that add up to `target`. Exactly one pair works, and you can't reuse the same index.

**Constraints:** `2 ≤ nums.length ≤ 10⁴`; the array is **not sorted**; values fit in `int`.

**Example 1:** `nums = [2,7,11,15], target = 9` → `[0,1]` (since `2 + 7 = 9`).

**Example 2:** `nums = [3,3], target = 6` → `[0,1]` (two equal values must be different indices).

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

> [key] **Key Insight** — For each `x`, the partner you need is `target - x`. Remember values as you go; check before inserting.

> [inv] **Invariant** — When at index `i`, the map holds every value at indices `< i` with its index.

> [note] **Trace it** — `a=[2,7,11,15], target=9`. At `i=1` (value 7) the partner is `9−7=2`, already stored from `i=0` → return `[0,1]`. No full rescan needed.

> [note] **Interview script** — "I first confirm there is exactly one answer and I should return indices, not values. I start with brute force by checking every pair, which is O(n²) time and O(1) space. I optimize by storing seen values in a hash map and checking `target - a[i]` during one scan, giving O(n) time and O(n) space."


<CodeTrace
  title="Two Sum (hash) — nums=[2,7,11,15], target=9"
  :values="[2,7,11,15]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { need: 7, seen: "{}", hit: "no" }, note: "store seen[2]=0" },
    { pointers: { i: 1 }, vars: { need: 2, seen: "{2:0}", hit: "YES" }, note: "seen[2]=0 → return [0,1]", added: [0,1] }
  ]'
/>

> [trap] **Common Trap** — Inserting into the map **before** the check makes an element match itself. *Example:* `nums=[3,2,4]`, `target=6`. If you `put(3,0)` first, then check for `target-3=3`, you find yourself and emit `(0,0)`. Check first, insert after.

<CodeTrace
  title="Trap — Two Sum matches self: nums=[3,2,4], target=6"
  :values="[3,2,4]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { seen: "{3:0}" }, note: "BUG: put(3,0) first" },
    { pointers: { i: 0 }, vars: { need: 3, hit: "seen[3]=0" }, note: "BUG: check complement 3 → seen[3]=0 → return [0,0] WRONG!", added: [0] },
    { pointers: { i: 0 }, vars: { seen: "{}", need: 3 }, note: "FIX: check first (miss), then insert seen[3]=0" }
  ]'
/>

> [pat] **Pattern Connection** — Hashing. In a *sorted* array the same task becomes **two pointers** in O(1) space; the sorted-vs-unsorted choice recurs throughout.

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

> [pat] **The thread that ties them together** — all of these are *"find elements that combine to a target."* The decision tree is short: **unsorted + exact pair** → hash the complement · **sorted** → two pointers (O(1) space) · **k numbers** → fix `k−2`, two-pointer the last two · **contiguous** → hash prefix sums · **maximize under a bound** → sort + two pointers. Same idea, five faces.

## Group Anagrams <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Group Anagrams](https://leetcode.com/problems/group-anagrams/)*

<ProgressCheck id="group-anagrams" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-ga-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">Canonical keys make equivalent words collide</text>

  <g font-size="13" font-weight="700" text-anchor="middle">
    <rect x="24" y="54" width="58" height="30" rx="8" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="53" y="74" fill="var(--dsa-ink)">eat</text>
    <rect x="24" y="104" width="58" height="30" rx="8" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="53" y="124" fill="var(--dsa-ink)">tea</text>
    <rect x="24" y="154" width="58" height="30" rx="8" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/><text x="53" y="174" fill="var(--dsa-ink)">tan</text>

    <rect x="138" y="54" width="58" height="30" rx="8" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="167" y="74" fill="var(--dsa-success)">aet</text>
    <rect x="138" y="104" width="58" height="30" rx="8" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="167" y="124" fill="var(--dsa-success)">aet</text>
    <rect x="138" y="154" width="58" height="30" rx="8" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" stroke-width="1.6"/><text x="167" y="174" fill="var(--dsa-warning)">ant</text>
  </g>
  <g stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-ga-primary)" fill="none">
    <path d="M84 69 L132 69"/><path d="M84 119 L132 119"/><path d="M84 169 L132 169"/>
  </g>
  <text x="110" y="48" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-neutral)">sort chars</text>

  <rect x="236" y="62" width="134" height="112" rx="10" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <text x="303" y="85" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">hash map</text>
  <text x="303" y="112" text-anchor="middle" font-size="12" fill="var(--dsa-success)">"aet" → [eat, tea]</text>
  <text x="303" y="140" text-anchor="middle" font-size="12" fill="var(--dsa-warning)">"ant" → [tan]</text>
  <path d="M198 69 C220 69 218 96 235 100" fill="none" stroke="var(--dsa-success)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-ga-primary)"/>
  <path d="M198 169 C220 169 218 144 235 140" fill="none" stroke="var(--dsa-warning)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-ga-primary)"/>
  <text x="200" y="225" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">same sorted key → same bucket; different key → different group</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> Each word is transformed into a canonical sorted-character key, and the hash map groups all words with the same key together.</div>

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

> [key] **Key Insight** — Anagrams share a canonical form. Use the 26-count signature (O(L)) rather than sorting (O(L log L)) when the alphabet is fixed.

> [note] **Trace it** — `["eat","tea","tan","ate","nat","bat"]`. Count-signatures make `eat/tea/ate` collide, `tan/nat` collide, `bat` alone → `[[eat,tea,ate],[tan,nat],[bat]]`.

> [note] **Interview script** — "I first confirm words are lowercase and group order does not matter. I start with brute force by comparing every pair of words for anagram equality, which is O(n²·L log L) time in the sorting version. I optimize by building one 26-count signature per word and hashing groups by that key, for O(n·L) time and O(n·L) space."


<CodeTrace
  title="Group Anagrams — words indexed 0..5"
  :values="['eat','tea','tan','ate','nat','bat']"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { key: "aet", groups: "{aet:[eat]}" }, note: "start bucket aet" },
    { pointers: { i: 1 }, vars: { key: "aet", groups: "{aet:[eat,tea]}" }, note: "tea joins aet", added: [0,1] },
    { pointers: { i: 2 }, vars: { key: "ant", groups: "{aet,ant:[tan]}" }, note: "new bucket ant" },
    { pointers: { i: 3 }, vars: { key: "aet", groups: "{aet:[eat,tea,ate],ant}" }, note: "ate joins aet", added: [0,1,3] },
    { pointers: { i: 4 }, vars: { key: "ant", groups: "{aet,ant:[tan,nat]}" }, note: "nat joins ant", added: [2,4] },
    { pointers: { i: 5 }, vars: { key: "abt", groups: "{aet,ant,abt:[bat]}" }, note: "bat alone. final 3 groups" }
  ]'
/>

> [trap] **Common Trap** — Building the count key without a delimiter collides distinct histograms. *Example:* counts `[1,11]` and `[11,1]` both stringify to `"111"` and get grouped together. Separate fields — e.g. `"1#11"` vs `"11#1"`.

<TrapTrace title="Building the count key without a delimiter collides distinct histograms" input="[1,11]" bug="counts '[1,11]' and '[11,1]' both stringify to ''111'' and get grouped together. Separate fields — e.g. ''1#11'' vs ''11#1''." fix="See the guidance in the trap description and the code snippet." />

> [pat] **Pattern Connection** — "Signature hashing" also powers Group Shifted Strings and isomorphic-string checks.

### Same pattern, new tweaks

Same move — *"map each item to a canonical key so equivalents collide"* — only the definition of "equivalent" changes:

| Variation | "Equivalent" means… | So the key is… |
|---|---|---|
| [Group Shifted Strings](https://leetcode.com/problems/group-shifted-strings/) | same **shift pattern** (`"abc"`≡`"bcd"`) | the sequence of gaps between consecutive letters (mod 26) |
| [Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/) | same **structure** (`"egg"`≡`"add"`) | the first-occurrence-position pattern (`"egg"` → `0,1,1`) |
| [Find Duplicate File in System](https://leetcode.com/problems/find-duplicate-file-in-system/) | same **content** | the file's content string |
| [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | two strings, not a whole group | compare the two 26-count signatures directly |

## Product of Array Except Self <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)*

<ProgressCheck id="product-of-array-except-self" />

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

> [key] **Key Insight** — `answer[i] = (∏ left of i) × (∏ right of i)`. Two sweeps; carry the running product in the output array to hit O(1) extra space.

> [inv] **Invariant** — After the left sweep, `out[i]` holds the product of all elements strictly left of `i`; the right sweep multiplies in the running right product.

> [note] **Trace it** — `[1,2,3,4]`. Left-products `[1,1,2,6]`, then multiply each by the running right-product → `[24,12,8,6]`. Position 0 = 2·3·4, position 3 = 1·2·3.

> [note] **Interview script** — "I first confirm division is disallowed and zeros may appear, so total-product division is not safe. I start with brute force by multiplying all other entries for every index, which is O(n²) time and O(1) extra space. I optimize with prefix and suffix products in two sweeps, giving O(n) time and O(1) extra space besides the output."


<CodeTrace
  title="Product of Array Except Self — nums=[1,2,3,4]"
  :values="[1,2,3,4]"
  :windowKeys="['i']"
  :cellWidth="42"
  :steps='[
    { pointers: { i: 0 }, vars: { left: 1, res: "[1,_,_,_]" }, note: "res[0]=1 (product of nothing left of 0)", added: [0] },
    { pointers: { i: 1 }, vars: { left: 1, res: "[1,1,_,_]" }, note: "res[1]=1 (nums[0]=1)", added: [1] },
    { pointers: { i: 2 }, vars: { left: 2, res: "[1,1,2,_]" }, note: "res[2]=1*2=2", added: [2] },
    { pointers: { i: 3 }, vars: { left: 6, res: "[1,1,2,6]" }, note: "res[3]=1*2*3=6 — left pass done", added: [3] },
    { pointers: { i: 3 }, vars: { right: 1, res: "[1,1,2,6]" }, note: "right pass, i=3: no change (right=1)" },
    { pointers: { i: 2 }, vars: { right: 4, res: "[1,1,8,6]" }, note: "res[2] *= 4 → 8", added: [2] },
    { pointers: { i: 1 }, vars: { right: 12, res: "[1,12,8,6]" }, note: "res[1] *= 12 → 12", added: [1] },
    { pointers: { i: 0 }, vars: { right: 24, res: "[24,12,8,6]" }, note: "res[0] *= 24 → final [24,12,8,6]", added: [0] }
  ]'
/>

> [trap] **Common Trap** — Reaching for division. *Example:* `nums=[1,2,0,4]` — dividing the total product by each element blows up at the zero. The prefix/suffix product is division-free and zero-safe.

<TrapTrace title="Reaching for division" input="nums=[1,2,0,4]" bug="'nums=[1,2,0,4]' — dividing the total product by each element blows up at the zero. The prefix/suffix product is division-free and zero-safe." fix="See the guidance in the trap description and the code snippet." />

> [pat] **Pattern Connection** — Prefix/suffix aggregation — the same skeleton as Trapping Rain Water (prefix/suffix max) and candy-distribution problems.

### Same pattern, new tweaks

Same skeleton — *combine a running result from the left with one from the right* — only the aggregate changes:

| Variation | The one thing that changes | So the aggregate is… | Time · Space |
|---|---|---|---|
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | water is bounded by the shorter wall | running **max** from each side; water = `min(L,R) − height` | O(n) · O(1) |
| [Candy](https://leetcode.com/problems/candy/) | each child must beat both neighbours | two passes (L→R then R→L), take the **max** requirement | O(n) · O(n) |
| [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | a negative flips sign | track running **max *and* min** so a sign-flip can become the new best | O(n) · O(1) |

## Longest Consecutive Sequence <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)*

<ProgressCheck id="longest-consecutive-sequence" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-lcs-success" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">Only start a streak at the left edge</text>

  <rect x="22" y="54" width="356" height="76" rx="12" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/>
  <text x="44" y="78" font-size="12" font-weight="700" fill="var(--dsa-neutral)">set</text>
  <g text-anchor="middle" font-size="14" font-weight="700">
    <rect x="70" y="70" width="52" height="32" rx="8" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="96" y="91" fill="var(--dsa-ink)">100</text>
    <rect x="132" y="70" width="38" height="32" rx="8" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="151" y="91" fill="var(--dsa-success)">4</text>
    <rect x="180" y="70" width="52" height="32" rx="8" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="206" y="91" fill="var(--dsa-ink)">200</text>
    <rect x="242" y="70" width="38" height="32" rx="8" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="261" y="91" fill="var(--dsa-primary)">1</text>
    <rect x="290" y="70" width="38" height="32" rx="8" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="309" y="91" fill="var(--dsa-success)">3</text>
    <rect x="338" y="70" width="32" height="32" rx="8" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="354" y="91" fill="var(--dsa-success)">2</text>
  </g>

  <text x="96" y="156" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-danger)">0 absent</text>
  <path d="M118 152 C150 140 205 140 242 152" fill="none" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" stroke-dasharray="6 4"/>
  <g text-anchor="middle" font-size="17" font-weight="700">
    <circle cx="110" cy="186" r="19" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="110" y="192" fill="var(--dsa-primary)">1</text>
    <circle cx="170" cy="186" r="19" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="170" y="192" fill="var(--dsa-success)">2</text>
    <circle cx="230" cy="186" r="19" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="230" y="192" fill="var(--dsa-success)">3</text>
    <circle cx="290" cy="186" r="19" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="290" y="192" fill="var(--dsa-success)">4</text>
  </g>
  <g stroke="var(--dsa-success)" stroke-width="var(--dsa-arrow-stroke)" marker-end="url(#ar-lcs-success)" fill="none">
    <path d="M129 186 L148 186"/><path d="M189 186 L208 186"/><path d="M249 186 L268 186"/>
  </g>
  <rect x="132" y="214" width="136" height="24" rx="8" fill="var(--dsa-success-soft)" stroke="var(--dsa-success-line)" stroke-width="1.6"/>
  <text x="200" y="231" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">streak length = 4</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> Start counting only when <code>x - 1</code> is absent; then walking <b>1→2→3→4</b> counts each run once instead of restarting inside it.</div>

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

> [key] **Key Insight** — Put all numbers in a set. A number `x` begins a run **iff** `x-1` is absent. Only then walk `x, x+1, …`. Each number is visited at most twice → O(n).

> [inv] **Invariant** — Inner `while` extends only from true run-starts, so total inner steps ≤ n across the whole outer loop.

> [note] **Trace it** — `[100,4,200,1,3,2]`. Only `1` and `100` and `200` are run-starts (their predecessor is absent). From `1` walk `1,2,3,4` → length **4**; the others give length 1.

> [note] **Interview script** — "I first confirm the array is unsorted, duplicates may exist, and the target is the length of the longest consecutive run. I start with brute force by trying to extend a run from every value with repeated searches, which is O(n²) time. I optimize by putting values in a set and expanding only when `x - 1` is absent, giving O(n) time and O(n) space."


<CodeTrace
  title="Longest Consecutive Sequence — nums=[100,4,200,1,3,2]"
  :values="[100,4,200,1,3,2]"
  :windowKeys="['i']"
  :cellWidth="38"
  :steps='[
    { pointers: { i: 0 }, vars: { val: 100, "99 in set": "no", start: "yes", run: 1, best: 1 }, note: "100 is a run-start, but 101 not present" },
    { pointers: { i: 1 }, vars: { val: 4, "3 in set": "yes", start: "no" }, note: "4 not a run-start — skip" },
    { pointers: { i: 2 }, vars: { val: 200, "199 in set": "no", start: "yes", run: 1, best: 1 }, note: "200 alone" },
    { pointers: { i: 3 }, vars: { val: 1, "0 in set": "no", start: "yes", run: 4, best: 4 }, note: "walk 1→2→3→4 — best=4", added: [3,5,4,1] },
    { pointers: { i: 4 }, vars: { val: 3, "2 in set": "yes", start: "no" }, note: "skip (mid-run)" },
    { pointers: { i: 5 }, vars: { val: 2, "1 in set": "yes", start: "no" }, note: "skip. final best = 4" }
  ]'
/>

> [trap] **Common Trap** — Omitting the `x-1` guard makes it O(n²). *Example:* `nums=[1,2,3,4]` — without the guard you walk the run from 1, then from 2, then from 3, then from 4 → 4+3+2+1 steps. Only start from values whose predecessor is absent.

<CodeTrace
  title="Trap — Longest Consecutive without x-1 guard: nums=[1,2,3,4]"
  :values="[1,2,3,4]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 0 }, vars: { walks: "1→2→3→4", steps: 4 }, note: "BUG: from 1 walks 4 steps" },
    { pointers: { i: 1 }, vars: { walks: "2→3→4", steps: 3 }, note: "BUG: from 2 walks again → O(n²)" },
    { pointers: { i: 2 }, vars: { walks: "3→4", steps: 2 }, note: "BUG: from 3 walks again" },
    { pointers: { i: 3 }, vars: { walks: "4", steps: 1 }, note: "total 10 steps for n=4" },
    { pointers: { i: 1 }, vars: { "check x-1": "yes → skip" }, note: "FIX: skip if x-1 present. only run-starts walk. O(n)" }
  ]'
/>

> [pat] **Pattern Connection** — "Start from the boundary" recurs in grid/graph flood-fill and interval merging: identify canonical entry points to avoid redundant work.

### Same pattern, new tweaks

Same skeleton — *put everything in a set, then only start work from a canonical entry point* to avoid redundant re-scans:

| Variation | The one thing that changes | Canonical "start" is… | Time |
|---|---|---|---|
| [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 1-D runs of integers | a number `x` whose predecessor `x−1` is absent | O(n) |
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | 2-D grid connectivity | any unvisited land cell (flood it once) | O(R·C) |
| [Word Ladder](https://leetcode.com/problems/word-ladder/) | words linked by 1-letter edits | dedup words in a set so each transform is explored once | O(N·L²) |

---

## Check your understanding

<Quiz patternId="hashing" :questions='[
  {
    "q": "In Two Sum, why check the complement before inserting the current value?",
    "choices": [
      {
        "text": "To keep indices sorted"
      },
      {
        "text": "To avoid matching the element with itself",
        "correct": true,
        "explanation": "Exactly. Insert-first can falsely pair one value with its own index."
      },
      {
        "text": "To reduce memory to O(1)"
      },
      {
        "text": "To support duplicate targets only"
      }
    ]
  },
  {
    "q": "For grouping lowercase anagrams, which key avoids sorting every word?",
    "choices": [
      {
        "text": "Raw word length only"
      },
      {
        "text": "First and last character"
      },
      {
        "text": "Delimited 26-count signature",
        "correct": true,
        "explanation": "Yes. Fixed alphabet counts give O(L) keys, and delimiters prevent collisions."
      },
      {
        "text": "Random hash seed"
      }
    ]
  },
  {
    "q": "What guard keeps Longest Consecutive Sequence linear?",
    "choices": [
      {
        "text": "Start only when x minus one is absent",
        "correct": true,
        "explanation": "Correct. Only run starts walk forward, so each number is visited a constant number of times."
      },
      {
        "text": "Walk forward from every number",
        "explanation": "That repeats the same run and can become O(n squared)."
      },
      {
        "text": "Sort the values first"
      },
      {
        "text": "Use a max heap"
      }
    ]
  }
]' />
