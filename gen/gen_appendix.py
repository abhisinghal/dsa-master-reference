"""Generate the Practice-Solutions appendix.
- Walks every source file, harvests LC links + their surrounding tweak hint
- Groups by chapter/pattern
- Emits a compact 4-column table: Problem | Pattern | Approach | LC link
- Plus curated deeper walkthroughs for ~30 highest-value variations
"""
import re, os

ROOT = os.path.join(os.path.dirname(__file__), "src")

# Chapter mapping: filename -> (pattern label, anchor).
# Restructured for Part II (patterns) / Part III (data structures) split.
CH = {
 # ---- Part II · The 21 Core Patterns ----
 "21-sliding-window.md":("Sliding Window","#sliding-window"),
 "22-two-pointers.md":("Two Pointers","#two-pointers"),
 "23-fast-slow.md":("Fast / Slow Pointers","#fast-slow-pointers-floyd"),
 "24-prefix-sum.md":("Prefix Sum / Difference Array","#prefix-sum-difference-arrays"),
 "25-hashing.md":("Hashing (pattern)","#hashing"),
 "26-monotonic-stack.md":("Monotonic Stack","#monotonic-stack"),
 "27-binary-search.md":("Binary Search","#binary-search-search-on-answer"),
 "28-bs-on-answer.md":("Binary Search on the Answer","#binary-search-on-the-answer"),
 "29-top-k-heap.md":("Top-K / Heap","#top-k-heap"),
 "30-k-way-merge.md":("K-way Merge","#k-way-merge"),
 "31-merge-intervals.md":("Merge Intervals","#merge-intervals"),
 "32-sweep-line.md":("Sweep Line","#sweep-line"),
 "33-topological-sort.md":("Topological Sort","#topological-sort"),
 "34-union-find.md":("Union-Find (DSU)","#union-find-disjoint-set-union"),
 "35-greedy.md":("Greedy","#greedy"),
 "36-backtracking.md":("Recursion & Backtracking","#recursion-backtracking"),
 "37-divide-conquer.md":("Divide & Conquer","#divide-conquer"),
 "38-dp.md":("Dynamic Programming","#dynamic-programming"),
 "39-trie-pattern.md":("Trie (pattern)","#trie-pattern"),
 "40-bit-manip.md":("Bit Manipulation","#bit-manipulation"),
 "41-quickselect.md":("Quickselect","#quickselect"),
 "42-math.md":("Math & Number Theory","#math-number-theory"),
 "44-design.md":("Design & Randomized","#design-randomized"),
 # ---- Part III · Data Structures ----
 "50-arrays.md":("Arrays (DS)","#arrays"),
 "52-strings.md":("Strings","#strings"),
 "56-linked-lists.md":("Linked Lists","#linked-lists"),
 "58-stacks-queues.md":("Stacks & Queues","#stacks-queues"),
 "60-trees.md":("Trees","#trees"),
 "62-heaps.md":("Heaps (DS)","#heaps-priority-queues"),
 "64-trie.md":("Tries","#tries-prefix-trees"),
 "66-graphs.md":("Graphs","#graphs"),
 "68-segment-fenwick.md":("Segment Tree & Fenwick","#segment-tree-fenwick-tree"),
 # ---- Part II opener ----
 "20-patterns.md":("Pattern Recognition Map","#the-21-core-patterns-recognition-navigation-map"),
}

def clean_name(n):
    n = re.sub(r'^\u2197\s*LeetCode:\s*', '', n)
    return n.strip()

def extract():
    """Returns dict slug -> {name, pattern, anchor, approach, source_file}"""
    out = {}
    for f in sorted(os.listdir(ROOT)):
        if f not in CH: continue
        pattern, anchor = CH[f]
        txt = open(os.path.join(ROOT, f), encoding="utf-8").read()
        # Scan line by line to capture the tweak text near each LC link
        lines = txt.split('\n')
        for i, ln in enumerate(lines):
            for m in re.finditer(r'\[([^\]]+)\]\((https://leetcode\.com/problems/([a-z0-9\-]+))/?\)', ln):
                name = clean_name(m.group(1))
                slug = m.group(3)
                # Extract approach from surrounding context
                approach = None
                # 1) In a table row: | [Name](url) | changes | time |
                if ln.startswith('|') and ' | ' in ln:
                    cells = [c.strip() for c in ln.split('|')[1:-1]]
                    if len(cells) >= 2:
                        approach = cells[1]
                # 2) Prose bullet: - [Name](url) — *tweak:* text.
                if not approach:
                    mm = re.match(r'^\s*-\s*\[[^\]]+\]\([^\)]+\)\s*[\u2014-]\s*\*tweak:\*\s*(.*?)\.?$', ln)
                    if mm: approach = mm.group(1)
                # 3) Practice bullet: line with · separators — take just the pattern label
                if not approach and ' · ' in ln and '**Practice**' in ln:
                    approach = f"See the pattern card for the template."
                # Save the FIRST rich mention (skips citations & second appearances)
                if slug not in out or (approach and not out[slug].get('approach')):
                    out[slug] = {
                     'name': name, 'pattern': pattern, 'anchor': anchor,
                     'approach': approach, 'source': f,
                    }
    return out

# Curated deeper walk-throughs for the 40 highest-value variation problems.
# Format: slug -> markdown block (numbered steps + optional code)
DEEP = {}

def add(slug, name, pattern, steps, code=None):
    hdr = f"### {name} {{: #{slug} }}\n[\u2197 LeetCode](https://leetcode.com/problems/{slug}/) \u00b7 Pattern: **{pattern}**\n\n"
    body = "\n".join(f"{i+1}. {s}" for i,s in enumerate(steps))
    md = hdr + body
    if code:
        md += f"\n\n```java\n{code}\n```"
    DEEP[slug] = md

add("two-sum-ii-input-array-is-sorted","Two Sum II — Input Array Is Sorted","Two Pointers",[
 "Two indices `lo=0`, `hi=n-1`.",
 "Compute `sum = a[lo] + a[hi]`; if it equals target return `{lo+1, hi+1}` (1-indexed).",
 "If sum is too small, `lo++`; too big, `hi--`. Sortedness guarantees the discarded end can never help.",
 "Terminates when pointers cross \u2014 O(n) time, O(1) space."
], "int lo=0, hi=a.length-1;\nwhile (lo<hi) {\n    int s=a[lo]+a[hi];\n    if (s==target) return new int[]{lo+1, hi+1};\n    if (s<target) lo++; else hi--;\n}\nreturn new int[]{-1,-1};")

add("3sum-closest","3Sum Closest","Two Pointers",[
 "Sort. For each `i`, run two-pointer on `[i+1..n-1]`.",
 "At every step compute `sum = a[i]+a[lo]+a[hi]`; if `abs(sum-target) < best`, update `best`.",
 "Move `lo++` if `sum < target`, else `hi--` \u2014 like standard 3Sum but tracking the closest, not exactly target.",
 "Return `best`. O(n\u00b2) time."
])

add("4sum","4Sum","Two Pointers",[
 "Sort. Two outer loops `i`, `j` (with `i<j`), then two-pointer inner search for the remaining pair.",
 "Skip duplicates at every level: `i>0 && a[i]==a[i-1]`, `j>i+1 && a[j]==a[j-1]`, and after each hit skip `lo`/`hi` duplicates.",
 "Use `long` for the sum to avoid overflow at extreme values.",
 "O(n\u00b3) time."
])

add("valid-anagram","Valid Anagram","Hashing",[
 "Return false if lengths differ.",
 "Bump `count[c]++` for each char in `s`, decrement for each char in `t`.",
 "Return true iff every count is 0 (or every entry in the map is 0).",
 "O(n) time, O(1) space for fixed alphabet."
])

add("maximum-product-subarray","Maximum Product Subarray","1D DP (Kadane variant)",[
 "Track both a running `maxSoFar` and `minSoFar` \u2014 a negative flips them.",
 "At each `x`: `newMax = max(x, x*maxSoFar, x*minSoFar)`; `newMin = min(x, x*maxSoFar, x*minSoFar)`.",
 "Update `best = max(best, newMax)` each step.",
 "O(n) time, O(1) space."
])

add("candy","Candy","Greedy (two-pass)",[
 "Give every child 1 candy.",
 "Left-to-right: if `r[i] > r[i-1]`, set `c[i] = c[i-1] + 1`.",
 "Right-to-left: if `r[i] > r[i+1]`, set `c[i] = max(c[i], c[i+1] + 1)`.",
 "Sum `c`. Two passes because each direction enforces only one side of the constraint. O(n)."
])

add("spiral-matrix-ii","Spiral Matrix II","Matrix mechanics",[
 "Same layer-by-layer walk as Spiral Matrix, but **write** `1..n\u00b2` into the cells you visit.",
 "Maintain `top`, `bot`, `left`, `right` bounds; after each side, shrink the relevant bound.",
 "Guard bottom-row and left-column with `top <= bot` / `left <= right` for odd `n`.",
 "O(n\u00b2) time, O(1) extra."
])

add("search-a-2d-matrix","Search a 2D Matrix","Binary Search",[
 "Row-major sorted array reshaped as a matrix \u2014 treat as one 1D sorted array of size `m*n`.",
 "Binary-search `lo=0, hi=m*n-1`; map `mid` to `(mid/n, mid%n)`.",
 "Compare `mat[r][c]` to target; standard halving.",
 "O(log(mn)) time."
])

add("search-a-2d-matrix-ii","Search a 2D Matrix II","Two Pointers on a matrix",[
 "Start at the top-right corner `(0, n-1)`.",
 "If `mat[r][c] == target`, done. If `mat[r][c] > target`, `c--` (eliminates a column). Else `r++` (eliminates a row).",
 "Each step drops a row or column, so O(m+n) total.",
 "Bottom-left works symmetrically."
])

add("subarray-sums-divisible-by-k","Subarray Sums Divisible by K","Prefix Sum + Hash",[
 "Prefix sum modulo k \u2014 two prefix sums with the same residue bracket a subarray whose sum is a multiple of k.",
 "Count occurrences of each residue `((prefix % k) + k) % k` (handle negatives).",
 "For each new residue, add its running count to the answer, then increment.",
 "Seed the count map with `{0: 1}` for subarrays that start at index 0. O(n)."
])

add("contiguous-array","Contiguous Array (equal 0s and 1s)","Prefix Sum + Hash",[
 "Map every `0` to `-1` mentally; find the longest subarray with sum 0.",
 "Track running sum; store the **first** index each sum value appeared at.",
 "When you revisit a sum, the subarray between is balanced \u2014 update `best`.",
 "Seed `{0: -1}` so runs starting at index 0 are handled. O(n)."
])

add("range-addition","Range Addition","Difference Array",[
 "Maintain a delta array. For each update `[l, r, val]`, do `diff[l] += val; diff[r+1] -= val`.",
 "After all updates, prefix-sum the delta array to recover the final values.",
 "O(U + n) total, vs O(U\u00b7n) naive."
])

add("valid-palindrome-ii","Valid Palindrome II","Two Pointers",[
 "Standard two-pointer palindrome check.",
 "On the first mismatch, allow one skip: try `s[lo+1..hi]` or `s[lo..hi-1]` \u2014 return true if either is a palindrome.",
 "Only one deletion is allowed, so this branching is sufficient.",
 "O(n) time."
])

add("move-zeroes","Move Zeroes","Two Pointers (write index)",[
 "Keep a `write` index starting at 0.",
 "Scan `read` left-to-right: whenever `a[read] != 0`, set `a[write++] = a[read]`.",
 "After the scan, fill `a[write..n-1]` with 0.",
 "In-place, order-preserving, O(n)."
])

add("fruit-into-baskets","Fruits into Baskets","Sliding Window",[
 "Reduces to *longest subarray with \u2264 2 distinct values*.",
 "Grow `right`; when the map holds > 2 distinct fruits, shrink `left` until back to 2.",
 "Track `best = max(best, right - left + 1)`.",
 "O(n) time, O(1) space (alphabet \u2264 3)."
])

add("longest-substring-with-at-most-k-distinct-characters","Longest Substring with At Most K Distinct","Sliding Window",[
 "Grow `right`, tracking a frequency map.",
 "While `map.size() > k`, shrink `left`: decrement its count; remove key when it hits 0.",
 "Update `best = max(best, right - left + 1)`.",
 "O(n) time, O(k) space."
])

add("find-all-anagrams-in-a-string","Find All Anagrams in a String","Sliding Window (fixed size)",[
 "Build the frequency vector `need[26]` from `p`.",
 "Slide a window of size `|p|` over `s`. Maintain a `have[26]`.",
 "Record `left` in the result whenever `have` equals `need`; increment/decrement bounds each step.",
 "O(|s|) time."
])

add("permutation-in-string","Permutation in String","Sliding Window (fixed size)",[
 "Same as Find All Anagrams, but return `true` on the first match instead of collecting positions.",
 "Fixed window size = `|s1|`; compare counts each shift.",
 "O(|s2|) time."
])

add("find-all-numbers-disappeared-in-an-array","Find All Numbers Disappeared in an Array","Cyclic Sort / index-marking",[
 "In-place: for each `v = |a[i]|`, mark `a[v-1] = -|a[v-1]|` to record that `v` was seen.",
 "After the pass, positive entries mark indices whose value never appeared \u2014 add `i+1` to the result.",
 "O(n) time, O(1) extra."
])

add("find-the-duplicate-number","Find the Duplicate Number","Fast/Slow Pointers (Floyd)",[
 "Treat `nums` as a functional graph: `next(i) = nums[i]`. A duplicate value guarantees a cycle.",
 "Phase 1: advance `slow = nums[slow]`, `fast = nums[nums[fast]]` until they meet.",
 "Phase 2: reset `slow = 0`; move both one step at a time until they meet again \u2014 that's the cycle start = duplicate.",
 "O(n) time, O(1) space."
])

add("next-greater-element-i","Next Greater Element I","Monotonic Stack",[
 "Compute NGE for each value in `nums2` using a decreasing stack; store `value \u2192 next-greater` in a map.",
 "For each query in `nums1`, look it up in the map (default `-1`).",
 "O(n + m) time."
])

add("online-stock-span","Online Stock Span","Monotonic Stack",[
 "Keep a stack of `(price, span)` pairs, decreasing by price.",
 "On `next(price)`: pop and accumulate `span` while the top's price \u2264 current. Push `(price, span)`.",
 "Each pushed pair is popped at most once \u2014 amortized O(1) per query."
])

add("find-peak-element","Find Peak Element","Binary Search on the shape",[
 "`nums[-1] = nums[n] = -\u221e` conceptually.",
 "At `mid`: if `a[mid] > a[mid+1]`, a peak is on the left half (including `mid`); else on the right.",
 "Halve until `lo == hi`. O(log n)."
])

add("capacity-to-ship-packages-within-d-days","Capacity To Ship Packages Within D Days","Binary Search on Answer",[
 "Range: `lo = max(weights)`, `hi = sum(weights)`.",
 "`feasible(cap)`: sweep, add to current day's load; if it would exceed `cap`, start a new day; return `days <= D`.",
 "Binary-search the smallest feasible `cap`. O(n log sum)."
])

add("magnetic-force-between-two-balls","Aggressive Cows / Magnetic Force","Binary Search on Answer",[
 "Sort positions. Range `lo=1`, `hi=max-min`.",
 "`feasible(d)`: greedily place balls at positions \u2265 last + d; feasible iff you place all m.",
 "Binary-search the largest feasible `d`. O(n log range)."
])

add("kth-smallest-element-in-a-sorted-matrix","Kth Smallest Element in a Sorted Matrix","Binary Search on Value",[
 "Range `lo=mat[0][0]`, `hi=mat[n-1][n-1]`.",
 "`count(v)` \u2014 count entries \u2264 v by walking from bottom-left in O(n) (down if \u2264, else left).",
 "Binary-search smallest `v` with `count(v) \u2265 k`. O(n log range)."
])

add("insert-interval","Insert Interval","Intervals",[
 "Emit all intervals ending before `newStart` (no overlap, left side).",
 "Merge every interval overlapping `new` \u2014 grow `newStart = min`, `newEnd = max`.",
 "Emit the merged `new`, then emit the rest.",
 "O(n) with one pass."
])

add("meeting-rooms","Meeting Rooms","Intervals",[
 "Sort by start time.",
 "Return false as soon as `a[i].start < a[i-1].end`.",
 "Otherwise true. O(n log n)."
])

add("my-calendar-i","My Calendar I","Intervals / TreeMap",[
 "Store bookings in a TreeMap keyed by start.",
 "For a new `[s,e)`: check `floorKey(s)` and `ceilingKey(s)` \u2014 conflict iff their intervals overlap `[s,e)`.",
 "Insert on success. O(log n) per booking."
])

add("subsets-ii","Subsets II","Backtracking (dedup by sort + skip)",[
 "Sort. Standard subsets template with `start` index.",
 "Inside the for-loop: if `i > start && a[i] == a[i-1]` skip \u2014 prevents same-level twins.",
 "Record a *copy* of the path at every node.",
 "O(2\u207f) subsets."
])

add("permutations-ii","Permutations II","Backtracking (dedup by used[] rule)",[
 "Sort. Use `used[i]` to track picked indices.",
 "Skip when `i > 0 && a[i] == a[i-1] && !used[i-1]` \u2014 enforces first-copy-first ordering.",
 "Recurse when `path.size() == n`.",
 "O(n\u00b7n!) time."
])

add("combination-sum-ii","Combination Sum II","Backtracking (each element once + dedup)",[
 "Sort. Standard combination template with `start`.",
 "At each `i`: skip if `i > start && a[i] == a[i-1]` (dedup at level).",
 "Recurse with `i+1` (no reuse). Break when `a[i] > remaining` (pruning).",
 "Exponential in worst case."
])

add("palindrome-partitioning","Palindrome Partitioning","Backtracking + palindrome check",[
 "DFS the split points. At each recursion, try every next-cut position `end`.",
 "If `s[start..end]` is a palindrome, add and recurse from `end+1`.",
 "Precompute an `isPal[i][j]` DP for O(1) palindrome test.",
 "Exponential in worst case."
])

add("generate-parentheses","Generate Parentheses","Backtracking (constrained)",[
 "Track `open`, `close` counters starting at 0.",
 "Add `(` if `open < n`. Add `)` if `close < open`.",
 "When `open + close == 2n`, record the string.",
 "Catalan-number many outputs."
])

add("word-break","Word Break","1D DP",[
 "`dp[i]` = can we split `s[0..i-1]` into dictionary words.",
 "`dp[0] = true`; for each `i`, try every `j < i` \u2014 `dp[i] = dp[j] && s[j..i-1] \u2208 dict`.",
 "Use a `HashSet` for O(1) lookups.",
 "O(n\u00b2\u00b7L) time."
])

add("longest-increasing-subsequence","Longest Increasing Subsequence","Patience DP",[
 "Maintain a `tails` list where `tails[k]` = smallest tail of an LIS of length `k+1`.",
 "For each `x`, binary-search the first `tails[i] >= x` and set `tails[i] = x`; if none, append.",
 "Answer = `tails.size()`.",
 "O(n log n)."
])

add("coin-change","Coin Change","Unbounded knapsack DP",[
 "`dp[i]` = min coins summing to `i`; init `dp[0]=0`, others `amount+1` (sentinel).",
 "For each `i` from 1 to amount, for each coin `c \u2264 i`: `dp[i] = min(dp[i], dp[i-c]+1)`.",
 "Return `dp[amount] > amount ? -1 : dp[amount]`.",
 "O(amount \u00b7 coins)."
])

add("unique-paths","Unique Paths","Grid DP",[
 "`dp[i][j] = dp[i-1][j] + dp[i][j-1]`; first row/col all 1s.",
 "Collapse to a 1D row updated left-to-right \u2014 O(n) space.",
 "Answer at `dp[m-1][n-1]`.",
 "O(m\u00b7n)."
])

add("edit-distance","Edit Distance","Subsequence DP",[
 "`dp[i][j]` = edits from `s1[0..i-1]` to `s2[0..j-1]`.",
 "Match: `dp[i-1][j-1]`. Else: `1 + min(insert dp[i][j-1], delete dp[i-1][j], replace dp[i-1][j-1])`.",
 "Bases: empty prefix = length of the other.",
 "O(m\u00b7n)."
])

add("best-time-to-buy-and-sell-stock","Best Time to Buy and Sell Stock","1-pass DP",[
 "Track `minSoFar = min(minSoFar, price[i])`.",
 "Track `best = max(best, price[i] - minSoFar)`.",
 "O(n) time, O(1) space."
])

add("best-time-to-buy-and-sell-stock-with-cooldown","Stock with Cooldown","State-Machine DP",[
 "Three states: `hold`, `sold`, `rest`. Transitions:",
 "`hold' = max(hold, rest - price)` (buy today).",
 "`sold' = hold + price` (sell today).",
 "`rest' = max(rest, sold)` (do nothing).",
 "Answer = `max(sold, rest)`. O(n) time, O(1) space."
])

add("missing-number","Missing Number","XOR / Gauss sum",[
 "XOR trick: `xor(0..n) ^ xor(nums)` \u2014 all pairs cancel, missing survives.",
 "Or sum trick: `n(n+1)/2 - sum(nums)`.",
 "O(n) time, O(1) space."
])

add("counting-bits","Counting Bits","DP on bits",[
 "`bits[i] = bits[i >> 1] + (i & 1)` reuses the answer for `i/2`.",
 "Fill 0..n in one pass.",
 "O(n) time."
])

add("range-sum-query-mutable","Range Sum Query — Mutable","Fenwick Tree",[
 "Build 1-indexed BIT: `for each i, tree[i] = sum of the last i&-i values`.",
 "`update(i, delta)`: walk `i += i & -i` while `i \u2264 n`, adding delta.",
 "`sum(i)`: walk `i -= i & -i` while `i > 0`, accumulating.",
 "Query `[l,r]` = `sum(r) - sum(l-1)`. O(log n) each op."
])

add("reverse-nodes-in-k-group","Reverse Nodes in k-Group","Linked List",[
 "Advance a pointer k steps; if fewer than k remain, return without reversing.",
 "Reverse the k-node block in place (standard three-pointer reverse).",
 "Wire the tail of the reversed block to the recursive result of the rest.",
 "O(n) time, O(1) space (iterative)."
])

add("copy-list-with-random-pointer","Copy List with Random Pointer","Hashing on nodes",[
 "First pass: `Map<Node,Node>` from original to a fresh clone with same `val`.",
 "Second pass: for each original `u`, set `map[u].next = map[u.next]` and `map[u].random = map[u.random]`.",
 "Return `map[head]`. O(n) time and space (or O(1) with interleaved-copy trick)."
])

add("binary-tree-right-side-view","Binary Tree Right Side View","BFS (last of each level)",[
 "BFS with a level size. Push root, then for each level dequeue `size` nodes.",
 "The last one you dequeue in the level is visible \u2014 record its value.",
 "Push children in normal order.",
 "O(n) time."
])

add("kth-smallest-element-in-a-bst","Kth Smallest Element in a BST","In-order traversal",[
 "In-order visit gives sorted order for a BST.",
 "Iterative in-order (stack): push lefts, pop-visit-descend-right; decrement k on each visit.",
 "Return the value when k hits 0.",
 "O(H + k) time."
])

add("k-closest-points-to-origin","K Closest Points to Origin","Top-K Heap or Quickselect",[
 "Max-heap of size k on squared distance. For each point, offer; if size > k, poll (evict the farthest).",
 "Heap ends with the k closest. Or use Quickselect for O(n) average.",
 "O(n log k) time."
])

add("word-ladder","Word Ladder","BFS",[
 "Put every word into a set (dedup + O(1) lookup).",
 "BFS from `beginWord`; at each pop, generate every 1-letter variant, if in set, enqueue and remove from set.",
 "Distance += 1 per level; return when you dequeue `endWord`.",
 "O(N\u00b7L\u00b7\u03a3) time."
])

add("pacific-atlantic-water-flow","Pacific Atlantic Water Flow","Multi-source BFS/DFS",[
 "Two `visited` grids: `pac`, `atl`.",
 "BFS/DFS **from** every edge cell of each ocean, but only step to neighbours **not lower** (reverse-flow).",
 "Result cells are those visited by both `pac` and `atl`.",
 "O(m\u00b7n) time."
])

add("network-delay-time","Network Delay Time","Dijkstra",[
 "Standard Dijkstra from `k`.",
 "If any distance stays `\u221e`, return `-1`.",
 "Otherwise return `max(dist)`.",
 "O(E log V)."
])

add("number-of-provinces","Number of Provinces","Union-Find",[
 "For each `(i, j)` with `M[i][j] == 1`, `union(i, j)`.",
 "Count distinct `find(i)` values.",
 "O(n\u00b2 \u03b1(n))."
])

add("critical-connections-in-a-network","Critical Connections in a Network","Tarjan low-link",[
 "DFS assigning `disc[u]` (discovery time) and `low[u]` (earliest reachable via one back-edge).",
 "For a tree edge `u \u2192 v`, recurse then set `low[u] = min(low[u], low[v])`.",
 "If `low[v] > disc[u]`, edge `(u,v)` is a bridge.",
 "Skip the direct parent edge to avoid a false back-edge. O(V+E)."
])

add("shuffle-an-array","Shuffle an Array (Fisher\u2013Yates)","Randomized",[
 "Copy the array to a mutable buffer.",
 "For `i` from `n-1` down to `1`: swap `buf[i]` with `buf[rnd.nextInt(i+1)]`.",
 "Every permutation has equal probability by induction.",
 "O(n) per shuffle."
])

add("random-pick-with-weight","Random Pick with Weight","Prefix Sum + Binary Search",[
 "Build a prefix sum of weights.",
 "For each pick, generate `r = rnd.nextInt(total) + 1`.",
 "Binary-search the smallest index whose prefix sum \u2265 r.",
 "O(n) build, O(log n) per pick."
])

def generate():
    data = extract()
    # Filter out the canonical problems that are titled "\u2197 LeetCode:" (they ARE the section)
    canonical = {s for s, e in data.items() if e['name'].startswith('\u2197')}
    variations = {s: e for s, e in data.items() if s not in canonical}
    # Group by pattern
    by_pat = {}
    for s, e in variations.items():
        by_pat.setdefault(e['pattern'], []).append((s, e))
    # Emit markdown
    lines = []
    lines.append("# Practice Solutions Appendix")
    lines.append('<p class="secgoal"><b>What &amp; why:</b> every practice / variation problem referenced anywhere in this book, in one place, with a compact <b>Approach</b> hint that gets you unstuck without spoiling the solve. Click through to LeetCode; jump to the corresponding pattern chapter for the full template.</p>')
    lines.append("")
    lines.append("> [key] **How to use it** \u2014 attempt each problem from its pattern card first. If you stall, read only the Approach cell (2\u20133 lines). The 40+ hardest variations have a full numbered-steps walkthrough below the tables.")
    lines.append("")
    lines.append(f"**{sum(len(v) for v in by_pat.values())}** practice / variation problems indexed across **{len(by_pat)}** pattern areas \u2014 this is the one place to check when you want a hint. For the full write-up on a *canonical* problem, use the [Master Problem Index](#master-problem-index-tracker) to jump straight to its section.")
    lines.append("")
    # Table per pattern. Order: patterns first (Part II), then DS (Part III).
    pattern_order = [
      "Sliding Window","Two Pointers","Fast / Slow Pointers","Prefix Sum / Difference Array",
      "Hashing (pattern)","Monotonic Stack","Binary Search","Binary Search on the Answer",
      "Top-K / Heap","K-way Merge","Merge Intervals","Sweep Line","Topological Sort",
      "Union-Find (DSU)","Greedy","Recursion & Backtracking","Divide & Conquer",
      "Dynamic Programming","Trie (pattern)","Bit Manipulation","Quickselect",
      "Math & Number Theory","Design & Randomized",
      # Part III
      "Arrays (DS)","Strings","Linked Lists","Stacks & Queues","Trees","Heaps (DS)",
      "Tries","Graphs","Segment Tree & Fenwick",
      # Fallback opener
      "Pattern Recognition Map",
    ]
    for pat in pattern_order:
        entries = by_pat.get(pat, [])
        if not entries: continue
        # dedupe
        seen_slug=set(); dedup=[]
        for s,e in entries:
            if s in seen_slug: continue
            seen_slug.add(s); dedup.append((s,e))
        # sort by name
        dedup.sort(key=lambda x: x[1]['name'].lower())
        _, anchor = ("", by_pat[pat][0][1]['anchor'])
        lines.append(f"\n## [{pat}]({anchor})\n")
        lines.append("| Problem | Approach hint |")
        lines.append("|---|---|")
        for s, e in dedup:
            hint = e.get('approach') or "See the pattern chapter for the template."
            hint = hint[:180]
            deep_link = f" \u00b7 [\u21e9 walkthrough](#{s})" if s in DEEP else ""
            lines.append(f"| [{e['name']}](https://leetcode.com/problems/{s}/){deep_link} | {hint} |")
    # Deep walkthroughs
    if DEEP:
        lines.append("\n## Full Walkthroughs \u2014 numbered steps + code\n")
        lines.append("<p class=\"secgoal\"><b>What &amp; why:</b> the ~50 highest-value variations where a step-by-step recipe pays off. Each has an explicit approach, numbered steps, and (where useful) a compact Java sketch.</p>\n")
        for slug in sorted(DEEP.keys()):
            lines.append(DEEP[slug])
            lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    md = generate()
    out = os.path.join(ROOT, "97-practice-solutions.md")
    open(out, "w", encoding="utf-8").write(md)
    print(f"wrote {out} \u2014 {len(md)} chars, {md.count(chr(10))} lines")
