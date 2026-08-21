"""Restructure the 21 pattern cards in 20-patterns.md to match the canonical-problem layout
used in 30-arrays-hashing.md (## header, ### Problem, ### Pattern, [key]/[inv] callouts,
SVG visual, ### Steps, ### Java, [trap] Common Trap with Example, ### Practice).
"""
import re, os

# Curated numbered-Steps recipes per pattern (index 1..21)
STEPS = {
 1: [  # Sliding Window
  "Initialize `windowSum = 0` (and any per-char counter you need for the rule).",
  "Iterate `right` from 0 to n-1: add `a[right]` into the window aggregate.",
  "Once `right >= k - 1` (fixed-size) or the rule is satisfied (variable-size), record the answer.",
  "If the window has grown one step past size k (fixed) or the rule is broken (variable), shrink from `left`: undo `a[left]`'s contribution, `left++`.",
  "Each element enters and leaves the window exactly once \u2014 O(n) total."
 ],
 2: [  # Two Pointers
  "Sort the array (mandatory prerequisite \u2014 sortedness makes each move monotone).",
  "Set `lo = 0`, `hi = n - 1`. Loop while `lo < hi`.",
  "Compute the current summary (sum, area, distance) from `a[lo]` and `a[hi]`.",
  "If it matches the target, record. If it's too small, `lo++` (only move that can help). If too big, `hi--`.",
  "If duplicates matter, skip them after each hit to avoid repeated answers."
 ],
 3: [  # Fast/Slow Pointers
  "Start `slow = fast = head`. Loop while `fast != null && fast.next != null`.",
  "Move `slow = slow.next`, `fast = fast.next.next` \u2014 fast moves twice as fast.",
  "For \"has cycle?\": if `slow == fast`, there's a cycle.",
  "For \"cycle start\": after they meet, reset `slow = head`; step both one at a time until they meet again \u2014 that node is the cycle entry.",
  "For \"middle\": when the loop exits, `slow` is at the middle."
 ],
 4: [  # Prefix Sum
  "Build `pre[0] = 0` and `pre[k] = pre[k-1] + a[k-1]` for k = 1..n.",
  "Any range sum `a[l..r]` becomes `pre[r+1] - pre[l]` \u2014 constant time per query.",
  "For \"count subarrays summing to k\": scan the array with a `HashMap<sum, count>` seeded `{0: 1}`; at each running-sum `s`, add `map.getOrDefault(s - k, 0)` to the answer, then `merge(s, 1, +)`.",
  "For the *difference-array* mirror: given many range-add updates, do `diff[l] += v; diff[r+1] -= v`, then prefix-sum once to recover the array."
 ],
 5: [  # Hashing
  "Choose the map/set shape based on the question \u2014 value\u2192index, char\u2192count, or membership set.",
  "Single pass: for each element, first *look up* whether the complement / duplicate / anagram-key is already present.",
  "If found, act on it (return, record, count).",
  "Then insert the current element / update its count.",
  "Order matters \u2014 lookup before insert avoids matching an element with itself."
 ],
 6: [  # Monotonic Stack
  "Decide the direction (left-to-right for \"next greater to the right\") and the monotonicity (decreasing stack for next-greater).",
  "Iterate. While the stack is non-empty and the top's value is \u2264 (or <) the current, pop it.",
  "The moment you pop something, the current index is its \"next greater/smaller.\"",
  "Push the current index. Every index is pushed and popped at most once \u2014 O(n).",
  "For unresolved indices left on the stack at the end, their answer is \"none\" (or a sentinel)."
 ],
 7: [  # Binary Search
  "Choose your interval convention \u2014 `[lo, hi]` closed or `[lo, hi)` half-open \u2014 and stick with it.",
  "Compute `mid = lo + (hi - lo) / 2` (overflow-safe).",
  "Compare `a[mid]` to target. If equal, return. If too small, discard the left half; too big, discard the right.",
  "Update `lo` or `hi` to the appropriate side and repeat until the interval is empty.",
  "For \"first/last true boundary\" variants, prefer half-open: the answer is `lo` at the end."
 ],
 8: [  # Binary Search on the Answer
  "Identify what makes `feasible(x)` **monotone**: as x grows, feasibility flips from false to true (or vice versa) exactly once.",
  "Set `lo`, `hi` from the problem's natural range (e.g. `max(a)` to `sum(a)`).",
  "Binary-search on `lo..hi`: compute `mid`; if `feasible(mid)`, tighten `hi`; else raise `lo`.",
  "Converge to the boundary. `lo` is the smallest (or largest) feasible answer.",
  "The `feasible(x)` predicate itself often runs in O(n) \u2014 giving O(n log range) total."
 ],
 9: [  # Top-K / Heap
  "Choose polarity opposite to what you want: min-heap for k *largest*, max-heap for k *smallest*.",
  "Iterate the input; `heap.offer(x)`.",
  "If `heap.size() > k`, `heap.poll()` \u2014 evicts the worst-of-the-best-k.",
  "After the pass, the heap holds the k target elements. The root is your `k`-th answer.",
  "O(n log k) time and O(k) space \u2014 far cheaper than sorting when k is small."
 ],
 10: [  # K-way Merge
  "Push each list's head into a min-heap of `(value, list-id)`.",
  "Poll the smallest; append its value to the output.",
  "Push the polled node's `next` from the same list (if any) \u2014 keeping the heap fed.",
  "Repeat until the heap is empty.",
  "The heap only ever holds \u2264 k elements \u2014 O(N log k) where N is the total node count."
 ],
 11: [  # Merge Intervals
  "Sort intervals by `start`.",
  "Initialize `out` with the first interval.",
  "For each next interval `cur`: if `cur.start <= last.end`, they overlap \u2014 extend `last.end = max(last.end, cur.end)`.",
  "Otherwise, append `cur` as a new interval.",
  "Return `out`. O(n log n) dominated by the sort."
 ],
 12: [  # Sweep Line
  "Turn each interval `[s, e]` into two events: `(s, +1)` and `(e, -1)`.",
  "Sort all events by time, breaking ties end-before-start (or vice versa depending on semantics).",
  "Sweep: keep a running counter, add each event's delta.",
  "The running maximum of the counter is peak concurrency \u2014 that's usually the answer.",
  "For total-covered-length variants, track sweep intervals `[prev, cur]` where the counter is non-zero."
 ],
 13: [  # Topological Sort
  "Build the adjacency list and `inDegree[]` array from edges.",
  "Enqueue every node with `inDegree == 0`.",
  "Repeat: poll a node, append it to `order`; for each neighbour decrement its in-degree, enqueue when it hits 0.",
  "If `order.size() < V`, a cycle exists \u2014 report \"impossible.\"",
  "Otherwise `order` is a valid topological sort. O(V + E) total."
 ],
 14: [  # Union-Find
  "Initialize `parent[i] = i`, `rank[i] = 0`.",
  "`find(x)`: recurse to the root; on the way back up, set `parent[x] = root` (path compression).",
  "`union(a, b)`: find both roots. If equal, they're already in one set. Else attach the shallower tree under the taller (union by rank).",
  "Iterate edges/queries, calling `union` and `find` as needed.",
  "Amortized nearly O(1) per operation with both optimizations."
 ],
 15: [  # Greedy
  "Sort by the criterion that makes the locally-best choice safe (earliest end time, largest ratio, etc.).",
  "Iterate in that order. At each step, take the greedy choice that doesn't violate constraints so far.",
  "Track the invariant that proves the choice is safe (frontier, running count, running deadline).",
  "Prove the exchange argument mentally: if a different choice at step i beats yours, you can swap without losing global optimality.",
  "If the exchange argument fails, you probably need DP instead."
 ],
 16: [  # Backtracking
  "Frame the search as a decision tree: at each node, enumerate the next choice.",
  "For each choice: **choose** \u2014 apply the choice to state.",
  "**Recurse** into the smaller subproblem.",
  "**Un-choose** \u2014 restore the state exactly, so sibling branches see it fresh.",
  "**Prune** early: as soon as the partial state can't produce a valid full answer, return without recursing."
 ],
 17: [  # Divide & Conquer
  "Base case: return the trivial answer for a size-0 or size-1 subarray.",
  "Split the input in half by index (`mid = (lo + hi) / 2`).",
  "Recurse on both halves, capturing partial answers.",
  "Combine the two halves in O(n) or O(log n) \u2014 this is where the algorithm's cleverness lives.",
  "Master-theorem gives you the total time from the recursion depth and combine cost."
 ],
 18: [  # Dynamic Programming
  "Design the **state**: what parameters uniquely describe a subproblem? (e.g. `dp[i][cap]`).",
  "Write the **transition**: how does one state combine smaller states? (e.g. `dp[i] = min(dp[i-c] + 1)`).",
  "Set **base cases**: values for the smallest sub-states (e.g. `dp[0] = 0`).",
  "Choose an **order** that computes each dependency before the state that needs it (bottom-up) or use memoization (top-down).",
  "Optionally, **compress space** if `dp[i]` uses only `dp[i-1]` (rolling array)."
 ],
 19: [  # Trie
  "Root node holds an empty prefix. Each node has an array of children (size \u03a3, typically 26) and an `isEnd` flag.",
  "`insert(word)`: walk from root; for each char, create the child if absent, descend, and finally set `isEnd = true`.",
  "`search(word)`: walk down; if a child is missing, return false. At the end, return `isEnd`.",
  "`startsWith(prefix)`: same walk as search, but return true unconditionally at the end.",
  "For dictionary+backtracking problems, hang the *word* itself on the terminal node so DFS can emit it in one lookup."
 ],
 20: [  # Bit Manipulation
  "Identify what a single bit represents (membership in a set, parity of a value, presence of a factor).",
  "Choose operations: `&` intersects, `|` unions, `^` toggles/cancels, `<<`/`>>` moves.",
  "For bitmask DP, `dp[mask]` = best answer using the subset represented by `mask` (n \u2264 20 usually).",
  "Enumerate submasks via `for (int s = mask; s > 0; s = (s - 1) & mask)`.",
  "Use `Integer.bitCount(mask)` for popcount, `mask & -mask` for the lowest set bit."
 ],
 21: [  # Quickselect
  "`lo = 0, hi = n - 1`. Loop while `lo <= hi`.",
  "Pick a random pivot (or median-of-three); partition `a[lo..hi]` around it, returning the pivot's final index `p`.",
  "If `p == k`, `a[k]` is the answer.",
  "If `p < k`, recurse (or set `lo = p + 1`) into the right half. If `p > k`, into the left.",
  "Only one side is recursed into per level \u2014 average O(n), worst O(n\u00b2)."
 ],
}

# What the pattern "solves" — used to build ### Problem and Example
PROBLEM_INTRO = {
 1: ("*Find the max sum of every contiguous subarray of size `k`.*",
     "The brute force re-computes each window from scratch \u2192 O(n\u00b7k). Neighbouring windows overlap in k\u22121 elements, so slide instead \u2014 add the entering element and drop the leaving one.",
     "`a = [4, 2, 1, 7, 8, 3]`, `k = 3` \u2192 max window `[7, 8, 3]` with sum **18**."),
 2: ("*In a sorted array, find two numbers that sum to `target`.*",
     "Checking every pair is O(n\u00b2). Sortedness lets you start with the widest pair and close in: too big \u2192 move `hi` left; too small \u2192 move `lo` right.",
     "`a = [1, 3, 5, 6, 8, 11]`, `target = 9` \u2192 indices `(1, 3)` because `3 + 6 = 9`."),
 3: ("*Given a linked list, does it contain a cycle? If so, where does the cycle start?*",
     "Store every visited node in a set \u2014 O(n) space. Or move two pointers at different speeds; if there's a cycle they must meet inside it. Simple algebra then locates the cycle entry.",
     "List `3 \u2192 2 \u2192 0 \u2192 -4 \u2192 (back to 2)` \u2192 slow and fast collide at `-4`; reset slow to head, walk one step each \u2192 they meet at `2` = cycle start."),
 4: ("*Answer many `sum(a[l..r])` queries fast, and \u2014 harder \u2014 count subarrays whose sum equals `k` even with negatives.*",
     "Precompute `pre[k] = sum of the first k elements`. Any range sum is one subtraction: `pre[r+1] - pre[l]`. For \"= k\" with negatives, pair prefix sums with a hash map.",
     "`a = [3, 1, 4, 1, 5]` \u2192 `pre = [0, 3, 4, 8, 9, 14]`; `sum(1..3) = pre[4] - pre[1] = 9 - 3 = 6`."),
 5: ("*Find two numbers in an unsorted array that sum to `target` \u2014 in O(n).*",
     "The nested-loop scan is O(n\u00b2). A hash map trades O(n) memory for O(1) recall of every value already seen, collapsing the search to one pass.",
     "`a = [3, 2, 4]`, `target = 6` \u2192 at index 2 (value `4`), map contains `2` (index 1) \u2192 answer `(1, 2)`."),
 6: ("*For each element, find the **next greater element** to its right.*",
     "Scanning forward from each index is O(n\u00b2). Keep a stack of *indices whose answer is still unknown*, monotonically decreasing in value; when a bigger element arrives, it resolves every pending index below it in one sweep.",
     "`a = [2, 1, 2, 4, 3]` \u2192 next-greater = `[4, 2, 4, -1, -1]`. Each index is pushed once and popped once."),
 7: ("*Locate a target value in a **sorted** array.*",
     "A linear scan is O(n). Because the array is ordered, one comparison at the midpoint eliminates half the remaining range \u2192 O(log n).",
     "`a = [1, 3, 5, 7, 9, 11, 13]`, `target = 9` \u2192 mid \u2192 `7 < 9` (right half) \u2192 mid \u2192 `11 > 9` (left) \u2192 mid \u2192 `9` \u2713 in 3 steps."),
 8: ("*Find the smallest speed / capacity / value at which some feasibility test succeeds.*",
     "Try every candidate \u2192 O(range \u00b7 n). If `feasible(x)` is monotone (false...false, then true...true), binary-search the boundary.",
     "Koko eating bananas: `piles = [3, 6, 7, 11]`, hours `h = 8` \u2192 speeds 1..3 fail, 4 works \u2192 answer `4`."),
 9: ("*Return the **k largest** elements of an array.*",
     "Sorting all n is O(n log n). Keep a min-heap capped at size k: push each element, pop the smallest when size exceeds k. The heap always holds the current top k \u2192 O(n log k).",
     "`a = [4, 1, 7, 3, 8, 5]`, k = 3 \u2192 heap ends up as `{5, 7, 8}`; root `5` is the 3rd-largest."),
 10: ("*Merge k sorted lists into one sorted list.*",
      "Concatenate-then-sort is O(N log N). Put each list's head into a min-heap; repeatedly pop the smallest and push its list's `next`. The heap holds \u2264 k items \u2192 O(N log k).",
      "Lists `A = [1, 4], B = [1, 3], C = [2, 6]` \u2192 merged output `[1, 1, 2, 3, 4, 6]`."),
 11: ("*Given a collection of `[start, end]` intervals, merge every pair that overlaps.*",
      "Comparing every pair is O(n\u00b2). Sort by `start` and sweep left to right: an interval either extends the current running one, or starts a new one.",
      "Input `[[1, 3], [2, 6], [8, 10], [15, 18]]` \u2192 merged `[[1, 6], [8, 10], [15, 18]]`."),
 12: ("*Given a set of meetings, what is the **peak** number that overlap at any point in time?*",
      "Comparing every pair of intervals is O(n\u00b2). Convert each interval to two events (+1 at start, \u22121 at end), sort, sweep \u2014 the running counter's max is the peak.",
      "Meetings `[[0, 30], [5, 10], [15, 20]]` \u2192 peak concurrency `2` \u2192 **2** rooms needed."),
 13: ("*Given tasks with prerequisites (a DAG), return an order that respects them.*",
      "Guess-and-verify is exponential. Kahn's algorithm: repeatedly emit a node whose prerequisites are all done; if you can't finish, a cycle exists.",
      "Prerequisites `0 \u2192 1, 0 \u2192 2, 1 \u2192 3, 2 \u2192 3` \u2192 a valid order is `[0, 1, 2, 3]`."),
 14: ("*Answer \"same group?\" as edges arrive dynamically \u2014 count the number of groups.*",
      "BFS from each node per query is O(V + E) per call. Union-Find maintains parent pointers; each `find` and `union` is amortized near-O(1) with path compression + union by rank.",
      "Nodes 0..4 with edges `(0,1), (2,3), (1,3)` \u2192 sets `{0, 1, 2, 3}` and `{4}` \u2192 **2** components."),
 15: ("*Reach the last index in the fewest jumps possible.*",
      "Trying every jump length recursively is exponential. Extend a \"reachable frontier\" as you scan; jump only when you hit the current frontier's end, then reset it.",
      "`nums = [2, 3, 1, 1, 4]` \u2192 minimum jumps = **2** (`0 \u2192 1 \u2192 4`)."),
 16: ("*Generate **every subset** of an array of distinct values.*",
      "Nested loops don't scale beyond a fixed depth. Walk a decision tree: at each element, branch into \"include it\" and \"skip it\", and un-choose on the way back up so sibling branches stay clean.",
      "`nums = [1, 2, 3]` \u2192 8 subsets `[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]`."),
 17: ("*Sort an array with a recursive split-then-combine strategy (merge sort).*",
      "Nested loops give O(n\u00b2). Split into halves, sort each recursively (O(log n) levels), then merge the sorted halves in O(n) \u2192 O(n log n).",
      "`a = [5, 2, 4, 1]` \u2192 split to `[5, 2]` and `[4, 1]` \u2192 sort to `[2, 5]` and `[1, 4]` \u2192 merge to `[1, 2, 4, 5]`."),
 18: ("*Count the ways to climb `n` stairs, taking 1 or 2 steps at a time.*",
      "Recursion `f(n) = f(n-1) + f(n-2)` re-solves the same subproblems exponentially. Write each answer down once and reuse it \u2192 O(n).",
      "`n = 5` \u2192 `dp = [1, 1, 2, 3, 5, 8]` \u2192 **8** ways."),
 19: ("*Store a dictionary and answer \"does any word start with this prefix?\" in O(L).*",
      "Comparing against every word is O(N\u00b7L). A trie shares prefix nodes, so a lookup follows the path of L characters \u2014 independent of dictionary size.",
      "Insert `cat`, `car`, `dog` \u2192 the prefix `ca` occupies a single path shared by `cat` and `car`."),
 20: ("*Given an array where every element appears twice except one, find the loner.*",
      "Counting with a hash map is O(n) time and O(n) space. XOR is associative and self-inverse (`x ^ x = 0`), so XOR-ing every value cancels the pairs and leaves the loner \u2014 O(1) space.",
      "`a = [4, 1, 2, 1, 2]` \u2192 `4 ^ 1 ^ 2 ^ 1 ^ 2 = 4`. The loner is **4**."),
 21: ("*Return the `k`-th smallest element of an unsorted array \u2014 without fully sorting.*",
      "Sorting is O(n log n). Partition around a pivot so it lands at its final sorted index `p`; if `p == k`, you're done \u2014 recurse only into the side that contains rank `k`.",
      "`a = [7, 2, 1, 8, 4, 5]`, k = 4 (2nd-largest) \u2192 pivot 5 \u2192 answer 7."),
}

def parse_card(header, body):
    """Extract the pieces of a card."""
    d = {'header': header.strip(),
         'signals': None, 'howitworks': None, 'invariant': None, 'complexity': None,
         'canonical': None, 'practice': None, 'trap': None,
         'svg': '', 'figcap': '', 'template_label': None, 'java': ''}
    # Bullet extraction
    for m in re.finditer(r'^\s*-\s*\*\*(Signals|How it works[^*]*|Invariant|Complexity|Canonical|Practice|Trap)\*\*\s*(?:\([^)]*\))?\s*[\u2014-]\s*(.*?)(?=\n\s*-\s*\*\*|\n\n|\Z)', body, re.MULTILINE | re.DOTALL):
        label = m.group(1); content = m.group(2).strip()
        if label.startswith('Signals'): d['signals'] = content
        elif label.startswith('How it works'): d['howitworks'] = content
        elif label == 'Invariant': d['invariant'] = content
        elif label == 'Complexity': d['complexity'] = content
        elif label == 'Canonical': d['canonical'] = content
        elif label == 'Practice': d['practice'] = content
        elif label == 'Trap': d['trap'] = content
    # SVG block
    m = re.search(r'```svg\n(.*?)\n```', body, re.DOTALL)
    if m: d['svg'] = m.group(0)
    m = re.search(r'<div class="figcap">(.*?)</div>', body, re.DOTALL)
    if m: d['figcap'] = m.group(0)
    # Template label + java
    m = re.search(r'\*\*Template\s*[\u2014-]\s*(.+?)\*\*\n```java\n(.*?)\n```', body, re.DOTALL)
    if m:
        d['template_label'] = m.group(1).strip()
        d['java'] = m.group(2)
    return d

def build_card(idx, d):
    """Emit the new H3-subsection format matching Arrays & Hashing."""
    problem_stmt, approach, example = PROBLEM_INTRO.get(idx, ("", "", ""))
    steps = STEPS.get(idx, [])
    header = d['header']
    if not header.startswith('##'):
        header = f"## {idx}. {header}"
    lines = []
    lines.append(header)
    lines.append("")
    # Recognition tagline (mirrors *[↗ LeetCode: ...]* in canonical problems)
    if d['signals']:
        # Strip trailing period, keep content
        sig = d['signals'].rstrip('.')
        lines.append(f"*Recognition \u2014 {sig}.*")
        lines.append("")
    # ### Problem
    lines.append("### Problem")
    if problem_stmt:
        lines.append(problem_stmt)
        lines.append("")
    if example:
        lines.append(f"**Example.** {example}")
        lines.append("")
    # ### Pattern (the how-it-works)
    lines.append("### Pattern")
    if approach:
        lines.append(approach)
    elif d['howitworks']:
        lines.append(d['howitworks'])
    lines.append("")
    # [inv] callout
    if d['invariant']:
        lines.append(f"> [inv] **Invariant** \u2014 {d['invariant']}")
        lines.append("")
    # SVG
    if d['svg']:
        lines.append(d['svg'])
        if d['figcap']:
            lines.append(d['figcap'])
        lines.append("")
    # ### Steps
    if steps:
        lines.append("### Steps")
        for i, s in enumerate(steps, 1):
            lines.append(f"{i}. {s}")
        lines.append("")
    # ### Java
    tmpl_label = d.get('template_label') or "template"
    lines.append(f"### Java (template \u2014 *{tmpl_label}*)")
    lines.append("```java")
    lines.append(d['java'])
    lines.append("```")
    lines.append("")
    # Complexity
    if d['complexity']:
        lines.append("### Complexity")
        lines.append(d['complexity'])
        lines.append("")
    # Trap
    if d['trap']:
        lines.append(f"> [trap] **Common Trap** \u2014 {d['trap']}")
        lines.append("")
    # Practice
    if d['practice']:
        lines.append("### Practice")
        # If Practice contains multiple links separated by ·, one bullet per link
        practice_str = d['practice'].strip()
        items = re.split(r'\s*\u00b7\s*', practice_str)
        for it in items:
            lines.append(f"- {it}")
        lines.append("")
    return "\n".join(lines)

def process(path):
    txt = open(path, encoding="utf-8").read()
    # Split just the 21 cards region: between "## The 21 Core Patterns" (h2)
    # and next h1/h2 (which starts a different section).
    parts = re.split(r'(?m)^(## \d+\. )', txt)
    # parts[0] = everything before card 1; parts[1] = '## 1. '; parts[2] = card1 body up to next '## N. '; ...
    if len(parts) < 3: return 0
    out = [parts[0]]
    card_count = 0
    # After first '## N. ' marker
    idx = 1
    while idx < len(parts):
        marker = parts[idx]  # '## N. '
        body = parts[idx + 1] if idx + 1 < len(parts) else ""
        # Extract card number
        num_m = re.match(r'## (\d+)\. ', marker)
        num = int(num_m.group(1)) if num_m else None
        # The body starts with the pattern name up to the newline (which is on the same "line" as marker in split), 
        # but with our regex '## \d+\. ' the name is at start of `body`. Let's split first line as name.
        first_nl = body.find('\n')
        name = body[:first_nl].strip() if first_nl >= 0 else body.strip()
        rest = body[first_nl:] if first_nl >= 0 else ""
        header_full = f"## {num}. {name}"
        # Find the end of THIS card: the next occurrence of '## N. ' pattern in the split arrangement is handled by our split
        d = parse_card(header_full, rest)
        d['header'] = header_full
        new_card = build_card(num, d)
        out.append(new_card + "\n")
        card_count += 1
        idx += 2
    new_txt = "".join(out)
    open(path, "w", encoding="utf-8").write(new_txt)
    return card_count

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), "src")
    n = process(os.path.join(root, "20-patterns.md"))
    print(f"restructured {n} cards")
