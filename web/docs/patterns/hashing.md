# Hashing


<PatternVideo pattern-name="Hashing" duration="8–12 min" />

<PatternProgress pattern-id="hashing" problems="hashing-two-sum, 3sum, two-sum-ii-input-array-is-sorted, two-sum-iii-data-structure-design, valid-anagram, isomorphic-strings, longest-consecutive-sequence, group-shifted-strings, maximum-product-subarray, number-of-islands, word-ladder, candy, subarray-sum-equals-k, top-k-frequent-elements" />

<script setup>
const bareTemplateCode = `# python — one-pass complement lookup
def two_sum(nums, target):
    seen = {}                                 # value → index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:                      # found the partner we saw earlier
            return [seen[need], i]
        seen[x] = i                           # record AFTER checking, so x doesn't match itself
    return [-1, -1]`

const bareInvariant = {
  statement: `At iteration i, \`seen\` holds exactly the values of \`nums[0:i]\` mapped to their indices; if \`seen\` contains \`target - nums[i]\`, that index together with i form a valid pair.`,
  initialization: `Before the loop, \`seen = {}\` is empty and i = 0. The claim "seen holds nums[0:0] = empty" is trivially true.`,
  maintenance: `At iteration i, we query \`seen\` for \`target - nums[i]\`. If present at index j < i, the pair (j, i) sums to target — correct, since nums[j] + nums[i] = (target - nums[i]) + nums[i] = target. If absent, we store nums[i] under index i, extending the invariant to i+1.`,
  termination: `If the loop exits, we scanned every index and never found a partner, so no pair exists. If we found one, we exited early with the correct pair.`
}

const bareComplexity = {
  time: `O(n) average — one pass with O(1) hashmap ops.`,
  space: `O(n) worst case for the hashmap (if no pair exists, every element is stored).`
}

const templateSpecializations = [
  { slug: `two-sum-one-pass-hashmap-easy`, title: `Two Sum (bare mechanic)` },
  { slug: `two-sum-ii-sorted-array-bridges-to-two-pointer-medium`, title: `Two Sum II (sorted)` },
  { slug: `group-anagrams-medium`, title: `Group Anagrams` },
  { slug: `longest-consecutive-sequence-medium`, title: `Longest Consecutive` },
  { slug: `subarray-sum-equals-k-medium`, title: `Subarray Sum K` },
  { slug: `top-k-frequent-elements-medium`, title: `Top K Frequent` }
]

const twoSumIISortedCode = `# python — sorted array; two-pointer is strictly better than hashmap here
def twoSum(numbers, target):
    lo, hi = 0, len(numbers) - 1
    while lo &lt; hi:
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]            # problem is 1-indexed
        if s &lt; target:
            lo += 1                             # too small; biggest-pairable is at hi
        else:
            hi -= 1                             # too big; smallest-pairable is at lo
    return [-1, -1]`

const twoSumIIInvariant = {
  statement: `At every iteration, if a valid pair exists in \`numbers\`, both indices lie within \`[lo, hi]\`.`,
  initialization: `Before the loop, \`lo = 0\`, \`hi = n - 1\`, so every index is in \`[lo, hi]\`.`,
  maintenance: `Case sum < target: \`numbers[lo]\` is the smallest in \`[lo, hi]\` (sorted); paired with the largest it still falls short, so no partner for \`lo\` exists → \`lo++\`. Case sum > target: symmetric for \`hi\`. Case sum == target: valid pair.`,
  termination: `\`hi - lo\` strictly decreases each step. Loop ends when \`lo &gt;= hi\` → no range left; no pair exists.`
}

const groupAnagramsCode = `# python — count-signature hashing
def groupAnagrams(strs):
    buckets = {}
    for s in strs:
        cnt = [0] * 26
        for c in s:
            cnt[ord(c) - ord('a')] += 1
        key = tuple(cnt)                        # tuple is hashable; array is not
        buckets.setdefault(key, []).append(s)
    return list(buckets.values())`

const groupAnagramsInvariant = {
  statement: `After each word \`s\` is processed, every word in \`buckets[key(s)]\` has the same 26-count signature as \`s\`, i.e. is an anagram of \`s\`.`,
  initialization: `Before the loop, \`buckets = {}\` — no claim to maintain.`,
  maintenance: `For each new word \`s\`, we compute its canonical signature (26-count tuple). Two words have the same signature iff they are anagrams. We append \`s\` to the bucket keyed by its signature, preserving the invariant for all buckets.`,
  termination: `All words processed. Each bucket's values list is a complete anagram group.`
}

const longestConsecutiveCode = `# python — hashset + start-only expansion
def longestConsecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:                          # not a run-start; skip
            continue
        cur, length = x, 1
        while cur + 1 in s:
            cur += 1
            length += 1
        best = max(best, length)
    return best`

const longestConsecutiveInvariant = {
  statement: `Each element of \`s\` is traversed by the inner \`while\` loop at most once across the entire algorithm.`,
  initialization: `Before the outer loop, no inner-loop steps have occurred.`,
  maintenance: `The inner loop only runs when \`x - 1 ∉ s\` — i.e. \`x\` is the leftmost element of its consecutive run. For a run of length L starting at \`x\`, the inner loop executes exactly L steps for \`x\` and 0 steps for \`x+1, x+2, ..., x+L-1\` (they fail the start test). Total inner-loop steps across all runs ≤ n.`,
  termination: `Outer loop iterates over every unique element in \`s\`; inner-loop total is O(n). Overall O(n) expected time.`
}

const subarraySumKCode = `# python — prefix-sum frequency map
def subarraySum(nums, k):
    freq = {0: 1}                               # empty prefix sum is "seen" once
    prefix, count = 0, 0
    for x in nums:
        prefix += x
        count += freq.get(prefix - k, 0)        # number of prefixes with sum (prefix - k)
        freq[prefix] = freq.get(prefix, 0) + 1
    return count`

const subarraySumKInvariant = {
  statement: `At iteration i, \`freq[p]\` equals the number of prefixes \`nums[0:j+1]\` with sum \`p\` for \`j &lt; i\`; \`count\` holds the total number of subarrays \`nums[j:i]\` with sum k ending before index i.`,
  initialization: `Before the loop, \`freq = {0: 1}\` — the empty prefix has sum 0, counted once. \`prefix = 0\`, \`count = 0\`.`,
  maintenance: `At index i, \`prefix\` becomes the sum of \`nums[0:i+1]\`. A subarray \`nums[j:i+1]\` has sum k iff \`prefix(i+1) - prefix(j) = k\`, i.e. \`prefix(j) = prefix - k\`. \`freq[prefix - k]\` counts how many such j exist (ending-this-step subarrays). Add to \`count\`. Then record the new prefix.`,
  termination: `All n elements processed. \`count\` holds all valid subarray-sum-equals-k combinations.`
}

const topKFrequentCode = `# python — bucket sort by frequency
def topKFrequent(nums, k):
    freq = {}
    for x in nums:
        freq[x] = freq.get(x, 0) + 1
    buckets = [[] for _ in range(len(nums) + 1)]  # index = frequency; max freq ≤ n
    for value, f in freq.items():
        buckets[f].append(value)
    out = []
    for f in range(len(buckets) - 1, 0, -1):      # walk high→low frequency
        for value in buckets[f]:
            out.append(value)
            if len(out) == k:
                return out
    return out`

const topKFrequentInvariant = {
  statement: `After bucketing, \`buckets[f]\` contains every value whose frequency is exactly \`f\`; walking buckets high→low yields values in non-increasing frequency order.`,
  initialization: `Before bucketing, \`buckets[f]\` is empty for all f. After counting \`freq\`, each distinct value has one frequency.`,
  maintenance: `For each \`(value, f)\` in \`freq\`, append \`value\` to \`buckets[f]\`. Buckets partition the distinct values by frequency.`,
  termination: `Walking from the highest-populated bucket downward emits values in decreasing frequency order. Stop after collecting k.`
}

const trapAcode = {
  statement: `Two Sum: putting the current element in the map BEFORE checking for its complement.`,
  bug: `On \`nums = [3, 3]\`, target \`6\`: iteration 0 puts \`{3: 0}\`; iteration 1 looks for \`6 - 3 = 3\`, finds it, returns \`[0, 0]\` — matching index 0 with itself. On \`nums = [3]\`, target \`6\`: same bug returns \`[0, 0]\` instead of "no pair."`,
  fix: `Check first, then insert. Walk the array in order; at each step: query map for \`target - nums[i]\`; if hit, return \`[seen_idx, i]\`; otherwise insert \`nums[i] → i\`. Never swap the order.`
}

const trapBcode = {
  statement: `Mutating a key after inserting into a HashMap (Java/Kotlin specific).`,
  bug: `Using a mutable \`ArrayList\` or \`char[]\` as a key: insert it with hashCode H1; mutate it; now \`map.containsKey(sameObject)\` returns \`false\` because the recomputed hashCode is H2 but the entry is bucketed under H1. The entry is "lost" even though it still exists.`,
  fix: `Keys must be effectively immutable. Prefer \`String\`, \`Integer\`, records, or sealed value types. For composite keys, use \`Map.Entry\` or \`List.of(a, b)\` (immutable list). Never a mutable collection or array as a key.`
}

const trapCcode = {
  statement: `Count-signature collisions without a delimiter in Group Anagrams.`,
  bug: `Building a key by concatenating counts: \`[1, 11]\` and \`[11, 1]\` both stringify to \`"111"\` — distinct letter histograms collide into the same bucket. On input where no word has >= 10 of any letter, you may not notice; on longer inputs, anagram groups get merged incorrectly.`,
  fix: `Use a delimiter: \`"1#11"\` vs \`"11#1"\`. Or in Python use \`tuple(cnt)\` (hashable and compares by element). Or in Java use \`Arrays.toString(cnt)\` which includes separators. The abstract rule: your canonical-form serialization must be injective on the equivalence class.`
}

const quizQuestions = [
  {q: "Time complexity of Two Sum with hash map?", choices: [{text: "O(n²)", correct: false}, {text: "O(n log n)", correct: false}, {text: "O(n) average", correct: true, explanation: "Single pass with O(1) average lookups."}, {text: "O(1)", correct: false}]},
  {q: "Why does Longest Consecutive Sequence achieve O(n) using a HashSet?", choices: [{text: "Only start counting from sequence heads (x where x-1 is absent)", correct: true, explanation: "Each element is visited by an inner extension at most once total."}, {text: "Because HashSet is O(1)", correct: false, explanation: "True but insufficient — without the head check it becomes O(n²)."}, {text: "Because the input is sorted", correct: false, explanation: "It is unsorted; that's the point."}, {text: "Because we sort first", correct: false, explanation: "Sorting would violate the O(n) spec."}]},
  {q: "What is the canonical-key trick for Group Anagrams?", choices: [{text: "Hash each word to a canonical form (sorted chars OR 26-count tuple) and bucket", correct: true, explanation: "Anagrams share the same canonical form; O(n·L) with the 26-count version."}, {text: "Use the string itself as key", correct: false}, {text: "Hash all substrings", correct: false}, {text: "Use Trie", correct: false, explanation: "Possible but heavier than needed."}]},
  {q: "For Subarray Sum Equals K with negatives allowed, why does sliding window FAIL and prefix-sum + hashmap SUCCEED?", choices: [{text: "Sliding window requires monotonic growth of the running sum, which negatives break; the hashmap tracks every prefix sum seen so we can match prefix - k", correct: true, explanation: "Classic distinction: sliding window needs monotonicity; hashmap doesn't."}, {text: "Sliding window is too slow", correct: false, explanation: "The problem is correctness, not speed."}, {text: "Hashmap uses less memory", correct: false, explanation: "It uses more."}, {text: "Negatives aren't allowed", correct: false, explanation: "They are."}]},
  {q: "What is the amortized cost of `HashMap.get()` in Java?", choices: [{text: "O(1)", correct: true, explanation: "Amortized O(1) with a good hash function; adversarial keys can degrade to O(log n) with tree bins."}, {text: "O(log n)", correct: false}, {text: "O(n)", correct: false}, {text: "O(σ)", correct: false}]}
]

const twoSumSolvePrompt = `Given an array of integers and a target, return the indices of the two numbers that add up to target. Exactly one solution exists; you may not use the same element twice. O(n) average.`
const twoSumIISolvePrompt = `Given a SORTED array and a target, return 1-indexed indices of two numbers summing to target. O(n) time, O(1) space (don't use the hashmap trick here).`
const groupAnagramsSolvePrompt = `Group words that are anagrams of each other. Return the groups in any order.`
const longestConsecutiveSolvePrompt = `Given an unsorted array, find the length of the longest run of consecutive integers. O(n) expected.`
const subarraySumKSolvePrompt = `Given an integer array (possibly with negatives) and target k, return the count of contiguous subarrays whose sum equals k.`
const topKFrequentSolvePrompt = `Given an integer array, return the k most frequent elements. Required: better than O(n log n). Example: \`[1,1,1,2,2,3], k=2\` → \`[1, 2]\`.`
</script>

## Why hashing exists — the story

You get an interview question you've seen before: **Two Sum**. Given `nums = [2, 7, 11, 15]` and `target = 9`, return the indices of the two numbers that add up to 9. Easy. You write two nested loops. Every pair. Return `[0, 1]`. Done.

The interviewer nods, then says: *"Great. Now `n = 10⁷`."*

Your O(n²) solution is now **5 × 10¹³ operations** — about 20 minutes at 40M ops/sec. The interviewer will not wait 20 minutes. And here's the maddening part: for each `nums[i]`, you know *exactly* what number you need — it's `target - nums[i]`. You don't need to *scan* for it; you need to *look it up*. Scanning is what makes the loop O(n²). Lookup is what turns it O(n).

The idea that makes lookup fast is a **hash table**: a data structure that maps keys to values with **average O(1)** insert and lookup — no scanning, no comparing, no sorting. Give it a key, get back the value in constant time. For Two Sum, walk the array once; at each `nums[i]` ask *"have I seen `target - nums[i]` already?"* If yes, return. If no, remember `nums[i]` and continue. One pass. **20 minutes → 100 milliseconds.** A twelve-thousand-times speedup for four lines of code.

But hash tables are more than just fast Two Sum. Anywhere a brute-force says *"for each element, look through all the others"*, a hash map lets you swap that inner scan for a lookup. Group anagrams? Instead of comparing every pair, hash each word to a canonical fingerprint and bucket. Longest consecutive sequence? Instead of sorting, dump into a set and expand only from the "start" of each run. Streak detection, frequency counting, complement lookup, cycle detection in a functional graph — hashing is the single most productive tool in a competitive programmer's toolbox.

The catch, and it's a real one: hash tables can **degrade to O(n)** per operation if the hash function is bad or an adversary crafts colliding keys. Understanding when this happens — and how Java's `HashMap` mitigates it — is the difference between a candidate who says *"hashing"* and one who says *"HashMap with treeified buckets past 8 collisions, average O(1), worst-case O(log n)."*

## The bare mechanic — simplest working example

Two Sum on `nums = [2, 7, 11, 15]`, target `9`:

| i | nums[i] | need = target − nums[i] | seen before? | seen after step |
|---|---|---|---|---|
| 0 | 2 | 7 | no | `{2: 0}` |
| 1 | 7 | 2 | **yes → [0, 1]** | — |

The whole pattern is **check first, then insert**. Insertion before the check would allow element 0 to match itself (`seen = {2: 0}` → at i=1 we'd query for 7, miss; but on `[3,3]` with target 6 we'd query for 3, find index 0, and return `[0, 0]`).





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Two Sum bare mechanic">
  <rect x="0" y="0" width="400" height="180" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">one pass; check first, then insert</text>
  <g text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-ink)">
    <rect x="40" y="56" width="50" height="30" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="65" y="76">2</text>
    <rect x="98" y="56" width="50" height="30" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="2"/><text x="123" y="76">7</text>
    <rect x="156" y="56" width="50" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="181" y="76">11</text>
    <rect x="214" y="56" width="50" height="30" rx="6" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)"/><text x="239" y="76">15</text>
  </g>
  <rect x="280" y="52" width="100" height="90" rx="8" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)" stroke-width="1.6"/>
  <text x="330" y="72" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-ink)">seen</text>
  <text x="330" y="100" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">2 → 0</text>
  <text x="200" y="128" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">at i=1: need=9-7=2 ∈ seen → return [0, 1]</text>
  <text x="200" y="158" text-anchor="middle" font-size="10" font-style="italic" fill="var(--dsa-neutral)">O(n) time, O(n) space</text>
</svg>
</div>




<PatternTemplateCard
  slug="hashing-bare"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  problemShape="walk once; at each step query hashmap for complement, then insert"
  defaultRevealed />

<HashingAnim />

## When to use it — recognition signals

- **"Pair / triplet / quadruple summing to target"** — complement lookup. Two Sum, 3Sum (hash-based variant), 4Sum.
- **"Any duplicate?" / "first non-repeated"** — hash set membership; hash map with counts.
- **"Group by some property"** — anagrams (sorted-string key), isomorphic strings (pattern signature), group shifted strings (relative-offset signature).
- **"Streak / longest consecutive run"** — dump values into a `HashSet`, then expand from each element that starts a run.
- **"Have I visited this state?"** — cycle detection in a functional graph (Happy Number), state deduplication in BFS.
- **"Subarray with sum / count property" when values can be negative** — prefix-sum + hashmap (sliding window fails when the running sum isn't monotone).
- **"Top k frequent"** — hashmap for counts, then bucket-sort by frequency or heap by count.
- **"Random access on arbitrary-shaped keys"** — arrays only key by integer; hash maps key by anything with `hashCode` + `equals`.

## History — Dumey's 1956 memo at IBM

The hash-table idea was first written down in an internal IBM memo by **Arnold Dumey in 1956**, titled *"Indexing for rapid random-access memory systems."* Dumey proposed dividing the address space into "buckets" indexed by a key's remainder modulo a prime — the exact structure every modern hash table still uses. The technique was formalized by **Wesley Peterson** in 1957 and became a standard entry in Knuth's *Sorting and Searching* (1973).

Java's `HashMap` (1998, JDK 1.2) used **separate chaining** — collisions live in a linked list. In **JDK 8 (2014)**, Josh Bloch and Doug Lea rewrote it to **treeify buckets that exceed 8 collisions**, capping worst-case from O(n) to O(log n). This mitigates hash-flooding DoS attacks that had plagued HashMap-based web services since 2011.

Google's **BigTable** (2006), **Redis** (2009), and **Memcached** (2003) are all — at their core — massive distributed hash tables. Every time you use a `Map` in Java, you're calling a subroutine invented in a 1956 memo.

## THE template

Six sub-variations, one skeleton. The specialization chip row jumps to each.

<PatternTemplateCard
  slug="hashing-canonical"
  title="Hashing canonical pattern"
  language="python"
  :code="bareTemplateCode"
  :invariant="bareInvariant"
  :complexity="bareComplexity"
  :specializations="templateSpecializations"
  problemShape="choose a key, choose a value, walk input once; ask hashmap a question per element" />

## Sub-variations of the template

<PatternSubVariationNav pattern="hashing" />

### Two Sum (one-pass hashmap) <span class="diff diff-e">Easy</span>

*[↗ LeetCode: Two Sum](https://leetcode.com/problems/two-sum/)*

<ProgressCheck id="two-sum-one-pass-hashmap" />

The bare mechanic as its own problem. Walk the array once; at each index, query the hashmap for the complement and insert if not found.

<InvariantProof
  :statement="bareInvariant.statement"
  :initialization="bareInvariant.initialization"
  :maintenance="bareInvariant.maintenance"
  :termination="bareInvariant.termination" />

<Callout kind="key" title="Blind-solve first:">

{{ twoSumSolvePrompt }}

</Callout>

<TemplateReveal
  slug="two-sum-one-pass"
  language="python"
  :canonical="bareTemplateCode"
  problemShape="one-pass hashmap: check complement, then insert" />

**Trace** on `nums = [2, 7, 11, 15]`, target 9: at i=0 insert `{2: 0}`; at i=1 need 2 ∈ map → return `[0, 1]`.

**Complexity ladder:**

| Approach | Time | Space | When |
|---|---|---|---|
| Brute force (nested loops) | O(n²) | O(1) | reference / very small n |
| Sort + two pointers | O(n log n) | O(n) | if sort already needed |
| **HashMap one-pass** | **O(n) avg** | **O(n)** | **interview default** |

Related siblings: **3Sum / 4Sum** (fix outer indices, two-pointer the inner pair — see Two Pointers chapter); **Two Sum III: Data Structure Design** (counter-based for streaming add + find).

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **One-pass "check then store"** is the recipe: for each `nums[i]`, ask the map for `target - nums[i]` BEFORE adding `nums[i]`. Order matters — storing first would admit `[3, 3], target = 6` as a false "same index twice" match.
- **Return INDICES, not values.** The problem specifies ordered index pairs; store `(value → index)` and retrieve the stored index when the complement hits.
- **O(n) time, O(n) space.** The space trade is why this beats sort-then-two-pointer when the original indices matter (sorting destroys them).
- **No sort = no two-pointer** on this problem. The sister problem (Two Sum II — sorted input) switches to two-pointer with O(1) space; different problem, different template.
- **The engine for 3Sum / 4Sum** — fix the outer indices, reduce to Two Sum on the remaining range. In practice sort + two-pointer wins for k-Sum because of dedup; hashing is still correct, just more awkward.
- **Streaming variant (Two Sum III)** uses a frequency counter instead of index map — handles add + find separately with better amortized cost under many queries.

</details>

---

### Two Sum II (sorted array → bridges to two-pointer) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)*

<Callout kind="key" title="The twist:">

when the input is sorted, the hashmap approach is strictly worse than two-pointer. Hashmap: O(n) time, **O(n) space**. Two-pointer: O(n) time, **O(1) space**. Sortedness is the handoff: Hashing's "complement lookup" becomes Two-Pointers' "discard a side."

</Callout>

<InvariantProof
  :statement="twoSumIIInvariant.statement"
  :initialization="twoSumIIInvariant.initialization"
  :maintenance="twoSumIIInvariant.maintenance"
  :termination="twoSumIIInvariant.termination" />

<Callout kind="key" title="Blind-solve first:">

{{ twoSumIISolvePrompt }}

</Callout>

<TemplateReveal
  slug="two-sum-ii-sorted"
  language="python"
  :canonical="twoSumIISortedCode"
  problemShape="sorted array → opposite-end two-pointer sweep → O(1) space" />

**Trace** on `numbers = [2, 7, 11, 15]`, target 9: lo=0, hi=3 (sum 17 &gt; 9) → hi--; lo=0, hi=2 (sum 13 &gt; 9) → hi--; lo=0, hi=1 (sum 9 = 9) → return `[1, 2]` (1-indexed).

**Why this problem lives in the hashing chapter at all:** interviewers often ask "what if the array is sorted?" as a follow-up to Two Sum. Say out loud: "the hashmap still works but is wasteful — sortedness unlocks two-pointer for O(1) space." Interviewers love the pattern-bridge recognition.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Sorted input unlocks two-pointer; drop the hashmap.** Opposite-end sweep gets O(n) time, O(1) space — the hashmap still works but costs O(n) space you don't need.
- **The pattern bridge is the point of this problem.** Say it out loud in an interview: "the hashmap works, but sortedness lets me use two-pointer for O(1) space."
- **Return 1-INDEXED indices.** LC Two Sum II specifies 1-based output; off-by-one here is the easiest way to lose the problem.
- **Direction rule: `sum < target` → `left++`, `sum > target` → `right--`.** Each move strictly discards a candidate — the proof that one pass is sufficient.
- **DO NOT re-sort if the input is already sorted.** Sorting is O(n log n) and the problem gave you the gift of sortedness; using it costs you a complexity tier for no benefit.
- **Original-index requirement forbids sorting from scratch.** If the problem demands original indices AND the input is not sorted, you must use hashing (Two Sum I); two-pointer would lose the mapping.

</details>

---

### Group Anagrams <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Group Anagrams](https://leetcode.com/problems/group-anagrams/)*

<ProgressCheck id="group-anagrams" />

<Callout kind="key" title="The twist:">

every anagram equivalence class has a canonical form. Hash each word to its canonical form; words with the same form land in the same bucket. The two canonical forms (sorted-string vs 26-count) trade different constants.

</Callout>

<InvariantProof
  :statement="groupAnagramsInvariant.statement"
  :initialization="groupAnagramsInvariant.initialization"
  :maintenance="groupAnagramsInvariant.maintenance"
  :termination="groupAnagramsInvariant.termination" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 220" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Group Anagrams canonical-key">
  <defs>
    <marker id="ar-ga-primary" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/></marker>
  </defs>
  <rect x="0" y="0" width="400" height="220" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">canonical key → equivalence class bucket</text>
  <g font-size="12" font-weight="700" text-anchor="middle" fill="var(--dsa-ink)">
    <rect x="24" y="48" width="58" height="28" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="53" y="66">eat</text>
    <rect x="24" y="92" width="58" height="28" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="53" y="110">tea</text>
    <rect x="24" y="136" width="58" height="28" rx="6" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)"/><text x="53" y="154">tan</text>
    <rect x="138" y="48" width="58" height="28" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="167" y="66">aet</text>
    <rect x="138" y="92" width="58" height="28" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="167" y="110">aet</text>
    <rect x="138" y="136" width="58" height="28" rx="6" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)"/><text x="167" y="154">ant</text>
  </g>
  <g stroke="var(--dsa-primary)" stroke-width="1.6" marker-end="url(#ar-ga-primary)" fill="none">
    <path d="M84 62 L132 62"/><path d="M84 106 L132 106"/><path d="M84 150 L132 150"/>
  </g>
  <rect x="236" y="56" width="134" height="100" rx="10" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral)" stroke-width="1.6"/>
  <text x="303" y="76" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-ink)">buckets</text>
  <text x="303" y="100" text-anchor="middle" font-size="11" fill="var(--dsa-success)">aet → [eat, tea]</text>
  <text x="303" y="128" text-anchor="middle" font-size="11" fill="var(--dsa-warning)">ant → [tan]</text>
  <text x="200" y="190" text-anchor="middle" font-size="10" font-style="italic" fill="var(--dsa-neutral)">sorted-chars key = O(L log L); 26-count key = O(L)</text>
</svg>
</div>




<Callout kind="key" title="Blind-solve first:">

{{ groupAnagramsSolvePrompt }}

</Callout>

<TemplateReveal
  slug="group-anagrams"
  language="python"
  :canonical="groupAnagramsCode"
  problemShape="canonical-key hashing: 26-count tuple as the equivalence-class fingerprint" />

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

**Related siblings:** *Isomorphic Strings* (first-occurrence position pattern as key); *Group Shifted Strings* (gap sequence mod 26); *Find Duplicate File* (file content as key).

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Group-by canonical form.** For each string, compute an equivalence-class key — sorted letters, or a 26-length count tuple — and bucket by that key. All anagrams of each other land in the same bucket.
- **Count-tuple key beats sort for long strings.** Sorting is O(k log k) per string; counting is O(k). For strings up to length 100, the difference is noise; for very long strings or bioinformatics-scale inputs, the counter wins.
- **Serialize the count tuple for hashmap keys.** In Java, `Arrays.hashCode(int[])` + `Arrays.equals` on wrapped-int arrays — or convert to a `String.valueOf(new String(char[26]))` with char-encoded counts. The tuple being hashable is the whole point.
- **O(N × k) time (counting) or O(N × k log k) time (sorting)** where N = strings, k = max length. Space is O(N × k) for the output groups.
- **Return the groups in any order unless the problem specifies.** Hashmap iteration order is not guaranteed; LeetCode marks the problem as order-independent.
- **The template generalizes.** Isomorphic Strings = first-occurrence position tuple as key; Group Shifted Strings = gap-sequence-mod-26 as key; Find Duplicate File = file-content as key. Same recipe: identify the equivalence class and hash it.

</details>

---

### Longest Consecutive Sequence <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/)*

<ProgressCheck id="longest-consecutive-sequence" />

<Callout kind="key" title="The twist:">

hashset gives O(1) membership. But the real trick is **only starting a run at its left end** (where `x - 1` is absent). Without this guard, you re-walk every run from every element → O(n²). With it, each element is visited at most once by the inner loop → O(n).

</Callout>

<InvariantProof
  :statement="longestConsecutiveInvariant.statement"
  :initialization="longestConsecutiveInvariant.initialization"
  :maintenance="longestConsecutiveInvariant.maintenance"
  :termination="longestConsecutiveInvariant.termination" />

<Callout kind="key" title="Blind-solve first:">

{{ longestConsecutiveSolvePrompt }}

</Callout>

<TemplateReveal
  slug="longest-consecutive-sequence"
  language="python"
  :canonical="longestConsecutiveCode"
  problemShape="hashset membership + expand-from-left-end-only" />

<CodeTrace
  title="Longest Consecutive — nums=[100,4,200,1,3,2]"
  :values="[100,4,200,1,3,2]"
  :windowKeys="['x']"
  :cellWidth="38"
  :steps='[
    { pointers: { x: 100 }, vars: { "99 in set": "no", start: "yes", run: 1, best: 1 }, note: "100 is run-start but 101 absent" },
    { pointers: { x: 4 }, vars: { "3 in set": "yes", start: "no" }, note: "4 not a run-start — skip" },
    { pointers: { x: 200 }, vars: { "199 in set": "no", start: "yes", run: 1, best: 1 }, note: "200 alone" },
    { pointers: { x: 1 }, vars: { "0 in set": "no", start: "yes", run: 4, best: 4 }, note: "walk 1→2→3→4 — best=4", added: [3,5,4,1] },
    { pointers: { x: 3 }, vars: { "2 in set": "yes", start: "no" }, note: "skip (mid-run)" },
    { pointers: { x: 2 }, vars: { "1 in set": "yes", start: "no" }, note: "skip. final = 4" }
  ]'
/>

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Only start counting from a RUN'S HEAD.** `x` is a run-head iff `x - 1` is NOT in the set — otherwise some earlier element already triggered the count and this x is in the middle of a run.
- **Set, not list — O(1) membership.** The whole algorithm pivots on fast "is x in the set?" checks; a list would make it O(n²) and defeat the purpose.
- **O(n) time amortized.** The outer loop is O(n), and the inner while-walk visits each element in at most ONE run — total inner work across all iterations is O(n).
- **Sort would be O(n log n) — accept the hashing trade-off.** The point of this problem is to show that an unsorted array can be processed in O(n) with O(n) space; sort is the simpler but strictly-dominated alternative.
- **Deduplicate first via Set.** Repeats would cause the inner while to loop over the same values; building a HashSet from the input is the natural O(n) dedup step.
- **Union-Find also works** (merge adjacent values, track component size) at same O(n) complexity. Pick hashing for shorter code; pick Union-Find if the problem has more structure (adding one at a time with online queries).

</details>

---

### Subarray Sum Equals K <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)*

<Callout kind="key" title="The twist:">

values can be **negative**, so sliding window FAILS (the running sum isn't monotone — shrinking the window can increase OR decrease it, so there's no safe advance rule). Instead, carry a **prefix sum + frequency map**: a subarray `nums[j:i+1]` sums to k iff `prefix(i+1) - prefix(j) = k`, so count how many prior prefixes had sum `prefix - k`.

</Callout>

<InvariantProof
  :statement="subarraySumKInvariant.statement"
  :initialization="subarraySumKInvariant.initialization"
  :maintenance="subarraySumKInvariant.maintenance"
  :termination="subarraySumKInvariant.termination" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" role="img" viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)" aria-label="Subarray Sum K prefix-sum map">
  <rect x="0" y="0" width="400" height="180" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">nums = [1, 1, 1], k = 2 → 2 subarrays</text>
  <g font-size="12" fill="var(--dsa-ink)" text-anchor="middle">
    <rect x="60" y="48" width="60" height="30" rx="6" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)"/><text x="90" y="68">prefix=1</text>
    <rect x="140" y="48" width="60" height="30" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="170" y="68">prefix=2</text>
    <rect x="220" y="48" width="60" height="30" rx="6" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)"/><text x="250" y="68">prefix=3</text>
  </g>
  <text x="60" y="100" font-size="10" fill="var(--dsa-neutral)">i=0: look for 1-2=-1 (0 found); add prefix=1</text>
  <text x="60" y="118" font-size="10" fill="var(--dsa-neutral)">i=1: look for 2-2=0 (1 found) → count=1</text>
  <text x="60" y="136" font-size="10" fill="var(--dsa-neutral)">i=2: look for 3-2=1 (1 found) → count=2</text>
  <text x="200" y="166" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">final count = 2</text>
</svg>
</div>




<Callout kind="key" title="Blind-solve first:">

{{ subarraySumKSolvePrompt }}

</Callout>

<TemplateReveal
  slug="subarray-sum-equals-k"
  language="python"
  :canonical="subarraySumKCode"
  problemShape="prefix sum + frequency map; count prefixes with sum (prefix - k)" />

**Trace** on `nums = [1, 1, 1]`, k = 2:
- Start: `freq = {0: 1}`, prefix = 0, count = 0.
- i=0: prefix = 1; look for `1 - 2 = -1` in freq → 0 found; `freq = {0: 1, 1: 1}`.
- i=1: prefix = 2; look for `2 - 2 = 0` in freq → 1 found → count = 1; `freq = {0: 1, 1: 1, 2: 1}`.
- i=2: prefix = 3; look for `3 - 2 = 1` in freq → 1 found → count = 2.
- Return 2.

**Why `freq = {0: 1}` initial?** It handles the case where the subarray starts at index 0 — the "empty prefix" has sum 0, so a prefix equal to k alone counts as one valid subarray.

**Related siblings:** *Continuous Subarray Sum* (prefix sums modulo k); *Subarray Sums Divisible by K* (modular residue classes as keys); *Contiguous Array* with equal 0s and 1s (map +1/-1 then count where `prefix = 0` repeats).

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Prefix-sum + hashmap turns O(n²) into O(n).** `count[prefix - k]` tells you how many prior prefixes make a subarray summing to k ending at the current index. Running total of those counts is the answer.
- **Seed `count.put(0, 1)` for the empty prefix.** Without it, subarrays that start at index 0 are dropped — the fencepost that gets missed on first-pass solutions.
- **Store PREFIX FREQUENCIES, not indices.** Multiple prior prefixes can share the same sum value and each contributes its own valid subarray; a single-index map would under-count.
- **Add to count AFTER querying.** The current prefix should only be visible to FUTURE endings; querying first ensures you aren't matching a subarray against itself.
- **DO NOT use sliding window here.** Negatives in the array break monotonicity under shrink, so the window template is wrong (even though "find subarrays summing to K" sounds like a window problem). This is why the chapter puts it under hashing, not sliding window.
- **The template generalizes to Continuous Subarray Sum (prefix mod k), Subarray Sums Divisible by K (residue classes), Contiguous Array (map +1/-1 and look for prefix == 0 repeats).**

</details>

---

### Top K Frequent Elements <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)*

<Callout kind="key" title="The twist:">

frequencies are bounded by `n`, so bucket-sort by frequency gives O(n) — strictly better than the common O(n log k) heap solution. Hashmap counts; array of lists indexed by frequency sorts; walk high→low until k collected.

</Callout>

<InvariantProof
  :statement="topKFrequentInvariant.statement"
  :initialization="topKFrequentInvariant.initialization"
  :maintenance="topKFrequentInvariant.maintenance"
  :termination="topKFrequentInvariant.termination" />

<Callout kind="key" title="Blind-solve first:">

{{ topKFrequentSolvePrompt }}

</Callout>

<TemplateReveal
  slug="top-k-frequent-elements"
  language="python"
  :canonical="topKFrequentCode"
  problemShape="count with hashmap, bucket-sort by frequency, walk high→low until k collected" />

**Trace** on `nums = [1, 1, 1, 2, 2, 3]`, k = 2:
- freq = `{1: 3, 2: 2, 3: 1}`.
- buckets (size n+1=7): `[[], [3], [2], [1], [], [], []]` (index = frequency).
- Walk from f=6 down: f=6..4 empty; f=3 → `[1]` out=`[1]`; f=2 → `[2]` out=`[1, 2]` → k reached.
- Return `[1, 2]`.

**Comparison with the heap-based solution:** Heap gives O(n log k) time, O(k) space — strictly better when k ≪ n. Bucket sort gives O(n) time, O(n) space. If k is close to n, bucket sort wins. Interviewers often ask for "better than O(n log n)" — both qualify.

**Related siblings:** *Sort Characters by Frequency* (same bucket trick, output characters by descending frequency); *K Closest Points to Origin* (heap of k, bucket sort doesn't apply because distances are continuous).

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Bucket sort by frequency gives O(n), beating heap's O(n log k).** Frequencies are bounded by `n`, so an array of n+1 buckets stores all possible counts; walk from the back for descending order and take k.
- **Count first, then bucket, then collect.** Three O(n) passes compose to one O(n) algorithm — don't fuse them to avoid rewriting the counter.
- **Heap of size k is the "obvious" alternative.** O(n log k) — add every element, pop when size exceeds k. Pick heap when you need streaming / arrival-order processing; pick bucket sort for offline batch.
- **QuickSelect is the third option.** O(n) average, O(n²) worst — partition on frequency, recurse into the half containing the top-k boundary. Shines when k is small and you can mutate; harder to reason about than bucket sort.
- **Return in any order unless the problem specifies.** LeetCode's problem is order-agnostic; many implementations output descending-frequency by convention.
- **Bucket sort does NOT work when the key space is continuous** (K-Closest-Points, where distances are floats) — fall back to heap or QuickSelect there.

</details>

---

## Traps & gotchas

<TrapTrace
  :title="trapAcode.statement"
  :bug="trapAcode.bug"
  :fix="trapAcode.fix" />

<TrapTrace
  :title="trapBcode.statement"
  :bug="trapBcode.bug"
  :fix="trapBcode.fix" />

<TrapTrace
  :title="trapCcode.statement"
  :bug="trapCcode.bug"
  :fix="trapCcode.fix" />

## In the wild — JDK 8 HashMap tree-ification

Before JDK 8 (2014), Java's `java.util.HashMap` used **separate chaining**: each bucket was a singly-linked list, so a bucket with 1000 colliding keys cost O(1000) per lookup. This became a security problem in 2011 when hash-flooding DoS attacks against web services (which key HTTP headers, form parameters, and cookies by name into HashMap) could force worst-case O(n²) processing just by sending many colliding keys.

JDK 8's fix, implemented by **Doug Lea** and documented in `src/share/classes/java/util/HashMap.java`:



```java
// From HashMap.java, trimmed for clarity:
static final int TREEIFY_THRESHOLD = 8;        // bucket > 8 → convert to tree
static final int UNTREEIFY_THRESHOLD = 6;      // tree ≤ 6 → back to linked list

// Tree bins require the key to implement Comparable; otherwise fallback to list
// and hope that System.identityHashCode spreads collisions enough.
```



Once a bucket exceeds 8 entries, it morphs into a red-black tree keyed by hash-and-then-comparable. Lookup within that bucket drops from O(bucket size) to O(log(bucket size)). This caps `HashMap.get()` worst case at **O(log n) regardless of hash function quality**. The hash-flooding attack class is dead.

Other named production uses of hashing:
- **Redis** keys-and-values store: open-addressing hash with incremental rehashing (so a huge rehash doesn't block the single-threaded event loop).
- **PostgreSQL hash joins**: build a hash table from the smaller side, probe with the larger. Falls back to merge join if the hash table doesn't fit in `work_mem`.
- **Git's object store** (`.git/objects/`): SHA-1 content-addressable storage — a hash maps content to filename.
- **Google BigTable / Spanner / Bigtable's shard key**: hash of the row key spreads load across tablet servers.
- **Chrome's cookie jar**: `(domain, name)` tuple hashed into a map; the LRU eviction when the jar is full uses this map's iteration order.

## When NOT to use it

HashMap feels like a universal "O(1) lookup" hammer; here's where it's the wrong tool.

- **Keyspace is a small dense integer range** — arrays are faster. Counting sort, radix sort, and array-indexed lookups beat HashMap for ASCII-character-frequency problems.
- **You need ordered iteration or range queries** — hash maps are unordered by contract. Use `TreeMap` (O(log n) but ordered) or maintain a parallel sorted structure.
- **Memory is tight** — HashMap entries are ~48 bytes each (hash int, key ref, value ref, next ref). A primitive `int[]` beats it 100× on memory.
- **You need worst-case O(1)** — hash maps are *average* O(1), *worst-case* O(n) if all keys collide. For adversarial contexts use `TreeMap` (O(log n) worst-case) or cryptographically strong hashing.
- **The comparison you want isn't equality** — hashing keys by equality doesn't help "find the closest match" or "range query." Use a BST or interval tree.

### Visual 1: array beats HashMap on a small dense keyspace

Counting ASCII character frequencies over `n = 10⁶` chars — HashMap vs `int[128]`:



```text
   HashMap<Character, Integer> freq:
     per char: hashCode(Character) → bucket → chain walk → autobox int → unbox → put
     per op: ~50-80 ns   (10⁶ chars × 70 ns ≈ 70 ms)
     memory: ~60 bytes per unique key   (~128 keys × 60 B ≈ 8 KB; HashMap overhead on top)

   int[128] arr:
     per char: arr[c]++      (bounds check + load + add + store)
     per op: ~1-2 ns         (10⁶ chars × 1.5 ns ≈ 1.5 ms)
     memory: 128 × 4 bytes = 512 B
```



~40× faster, ~16× less memory. The HashMap is doing a hash + collision check + autoboxing on every op — all unnecessary when the key space is `0..127`. The rule: **if the key is a small dense integer, index it directly**. The warning sign: typing `HashMap<Integer, …>` where the integers have a known bounded range.

### Visual 2: HashMap worst-case O(n) under adversarial input

Imagine an attacker who knows your hash function. They send `n` keys that all collide:



```text
   HashMap<String, Int>.put(key, value):

   Average case:                                      Adversarial case:
     bucket = hash(key) % capacity                      every key hashes to bucket 0
     chain in bucket is length 1 (amortized)            chain in bucket 0 is length n
     put = O(1)                                         put = O(n)

   10⁵ puts, each O(n):   10¹⁰ ops   →  ~30 seconds, likely timeout
```



This is the famous "HashMap collision DoS" vulnerability — in 2011 a Java/PHP/Python disclosure showed web servers could be DoS'd with ~1 MB of crafted POST params. Java 8+ fixes it partially by tree-ifying chains of ≥ 8 (chain → red-black tree, worst-case O(log n)) but requires the keys to be `Comparable`. For *provably* bounded worst-case, use `TreeMap` (O(log n) guaranteed) or a cryptographic hash the adversary can't invert.

### Visual 3: closest-match isn't an equality query

HashMap only answers "exact match". For "closest key ≤ k" you need an ordered structure:



```text
   data = { 10 → 'A', 25 → 'B', 50 → 'C', 100 → 'D' }

   Query: "value for the largest key ≤ 42"
   Expected answer: 'B' (key 25)

   HashMap approach:
     map.get(42)       → null, no exact match
     linear scan all keys, find the largest ≤ 42       O(n)       ✗ slow

   TreeMap approach:
     map.floorEntry(42)       → (25, 'B')             O(log n)   ✓ clean
```



The whole point of a hash map is to lose the ordering so you can achieve average O(1). If you need to come back to the ordering, you need a different structure. TreeMap/TreeSet (Java), `std::map` (C++), SortedDict (Python's `sortedcontainers`) all give O(log n) for ordered queries while still giving O(log n) for `put` and `remove`.

## Recognition drill

<RecognitionDrill pattern="hashing" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><b>What if memory is tight and keys are small integers?</b></summary>

Use a primitive int array as a counting map. `int[] cnt = new int[maxValue + 1]` with `cnt[x]++` for each `x` is 4 bytes per cell vs. HashMap's ~48 bytes per entry. For `maxValue = 10⁶`, that's 4 MB vs. 48 MB. For dense keys, this is a 10× memory win.

If keys are sparse but still small (e.g. values up to `10⁹` but you only see 10⁴ of them), coordinate compression (chapter 32 sweep-line discussion) brings them into dense range.
</details>

<details>
<summary><b>What if you need ordered iteration?</b></summary>

Switch to `TreeMap` (Java) or `std::map` (C++): O(log n) ops but ordered. Or use `LinkedHashMap` (Java) if you only need insertion-order iteration — same O(1) average ops, slight constant-factor memory overhead for the doubly-linked-list pointers.

Use case: LRU cache — `LinkedHashMap` with `accessOrder: true` and `removeEldestEntry` override gives you an LRU in 5 lines of code.
</details>

<details>
<summary><b>What if you need worst-case O(1) and can't tolerate O(log n) tails?</b></summary>

Use **cuckoo hashing** (two hash functions, two tables; each key is one of two possible slots). Lookup is strictly O(1) worst case. Insert is amortized O(1) but with occasional O(n) rebuild on cycle detection. Used in: router hardware tables, DPDK networking fast paths, some database indexes.

For cryptographic contexts, use a **universal hash family** (e.g. SipHash — the default in Rust's `HashMap`) so adversaries can't predict hashes without the random seed.
</details>

<details>
<summary><b>What if the "equivalence class" is harder to canonicalize?</b></summary>

The canonical-key trick depends on being able to compute a cheap, injective fingerprint. When this fails:
- **Graph isomorphism**: no known polynomial-time canonical form; use subgraph signatures + hashmap of candidates, confirm by VF2 or similar.
- **Floating-point equivalence** under precision: hash the rounded form; put a tolerance ε into the comparison; be careful about `-0.0 == 0.0` and `NaN != NaN` in Java.
- **Serialized state** of a complex object (used in BFS visited-set): write a canonical serializer; make sure field order is deterministic. A classic BFS bug is "visited keeps growing because every state looks different due to HashMap iteration order."
</details>

<details>
<summary><b>Breaking point — when hashing stops being enough.</b></summary>

- **Range queries** on keys ("how many keys in [a, b]"): switch to `TreeMap` or segment tree.
- **k-NN** on hashable keys (closest match): switch to space partitioning (kd-tree) or LSH (locality-sensitive hashing).
- **Approximate counting at huge scale** (how many distinct users today): switch to HyperLogLog — probabilistic, uses 2 KB regardless of cardinality, 2% error.
- **Set intersection on huge sets**: Bloom filter + verification pass; or sorted-merge if the sets are already sorted.
- **Multi-threaded hashmap under contention**: `ConcurrentHashMap` (Java) with its segment-based locking, or lock-free `CLHM`. Plain `HashMap` crashes under concurrent writes (JDK 7 could even infinite-loop on resize).
</details>

### Cross-pattern problems

| Problem | Primary pattern | What hashing contributes |
|---|---|---|
| [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | sliding window | hashmap of last-seen-index per char lets the left pointer jump |
| [Clone Graph](https://leetcode.com/problems/clone-graph/) | BFS/DFS | `original → clone` hashmap for memoization and cycle handling |
| [Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) | prefix sum + binary search | precompute prefix-sum array; binary search; hashing a lookup only matters when weights are keyed by name |

## Related patterns + Check your understanding

<RelatedPatterns pattern-id="hashing" />

<Quiz
  pattern-id="hashing"
  :questions="quizQuestions" />

<PrintButton />
