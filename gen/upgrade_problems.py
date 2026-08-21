"""Insert `### Steps` (numbered recipe) and, for multi-failure-mode problems,
`### Common Mistakes` (bulleted, plural) into a curated set of high-value canonical problems.

Steps are inserted right BEFORE `### Java` (so reader sees the recipe, then the code).
Common Mistakes are inserted right AFTER the existing `[trap]` callout (which stays as the primary trap).
"""
import re, os

ROOT = os.path.join(os.path.dirname(__file__), "src")

# problem-title -> (steps: List[str], common_mistakes: Optional[List[str]])
UPGRADES = {

 "Two Sum": (
   ["Create an empty hash map from value \u2192 index.",
    "Scan the array once. For each `a[i]`, compute `need = target - a[i]`.",
    "If `need` is in the map, return `{map[need], i}`.",
    "Otherwise `map[a[i]] = i`. Check-then-insert (never the other way \u2014 an element would match itself)."],
   None),

 "3Sum": (
   ["Sort the array \u2014 sortedness lets us prune and two-pointer.",
    "Loop `i` over each element as the outer pivot. Skip duplicate pivots: `if (i > 0 && a[i] == a[i-1]) continue;`.",
    "For each pivot, set `lo = i+1`, `hi = n-1`; hunt pairs summing to `-a[i]`.",
    "If `s < 0` \u2192 `lo++`; if `s > 0` \u2192 `hi--`; if `s == 0` \u2192 record the triplet.",
    "After a hit, skip duplicates on **both** pointers before advancing: `while (a[lo]==a[lo+1]) lo++;` and mirror for `hi`.",
    "Break early when `a[i] > 0` \u2014 no positive triple sums to zero."],
   ["**Missing any of the three duplicate-skips** \u2014 pivot, `lo`, `hi`. All three are required.",
    "**Advancing `lo`/`hi` before skipping duplicates** \u2014 do the skip on the value you just consumed, then advance.",
    "**Using `long` for the sum** unnecessary here (constraints keep it within `int`), but confirm when values approach `10\u2079`.",
    "**Not sorting first** breaks the two-pointer discard argument \u2014 the whole approach collapses to O(n\u00b3)."]),

 "Trapping Rain Water": (
   ["Two pointers `lo=0, hi=n-1`; carry `leftMax = 0`, `rightMax = 0`.",
    "At each step, compare `heights[lo]` vs `heights[hi]`. The **shorter** side bounds the water.",
    "If `heights[lo] < heights[hi]`: if `heights[lo] >= leftMax`, update `leftMax`; else add `leftMax - heights[lo]` to the answer. Advance `lo++`.",
    "Symmetric on the right side: advance `hi--`.",
    "Loop until `lo >= hi`. Every cell contributes at most once \u2014 O(n) time, O(1) space."],
   ["**Local maxima vs global**: water above a cell depends on the global bounding walls, not on the nearest peak.",
    "**Wrong side advances**: only move the pointer on the shorter side \u2014 that's the one whose water level is determined.",
    "**Missing the `>= leftMax` check**: without it, you subtract on `leftMax = heights[lo]` and get negative contributions.",
    "**Stack-based alternative**: also O(n) but uses O(n) space; two-pointer is O(1)."]),

 "Search in Rotated Sorted Array": (
   ["Binary-search with a twist: at every `mid`, decide **which half is sorted**, then check if `target` falls in it.",
    "`mid = lo + (hi - lo) / 2`. If `a[mid] == target`, return `mid`.",
    "If `a[lo] <= a[mid]` \u2014 left half `[lo..mid]` is sorted. If `a[lo] <= target < a[mid]` \u2192 `hi = mid - 1`; else `lo = mid + 1`.",
    "Otherwise the right half `[mid..hi]` is sorted. If `a[mid] < target <= a[hi]` \u2192 `lo = mid + 1`; else `hi = mid - 1`.",
    "Loop while `lo <= hi`; return `-1` if not found."],
   ["**Strict vs inclusive** on the sorted-half test \u2014 use `a[lo] <= a[mid]` so a length-1 left half is treated as sorted.",
    "**Comparing target inclusively on the wrong endpoint** \u2014 the target-in-range checks must match the sorted-half boundary.",
    "**Overflow on `(lo+hi)/2`** for large indices \u2014 use `lo + (hi-lo)/2`.",
    "**Assumes no duplicates**; with duplicates (LC 81), shrink both ends when `a[lo]==a[mid]==a[hi]`."]),

 "N-Queens (constraint occupancy)": (
   ["Represent the board as a `queens[N]` array where `queens[row] = col`.",
    "Maintain three bit-sets: `cols`, `antiDiag` (keyed by `row - col + N`), `mainDiag` (keyed by `row + col`).",
    "Recurse row by row. For each `col`, if all three bitsets say the cell is free, place and recurse.",
    "On return, un-set the three bits (backtrack).",
    "When `row == N`, translate `queens[]` into the string board and record it.",
    "O(N!) time \u2014 the branching factor shrinks fast due to the three constraints."],
   ["**Wrong diagonal keys**: anti-diagonal `row - col` (offset by `N` for non-negative), main diagonal `row + col`. Swapping them rejects valid boards.",
    "**Placing before checking**: check all three occupancy bits *first*, then place.",
    "**Forgetting to undo** any of the three bits on return.",
    "**Copying the board on every step** \u2014 mutate in place, snapshot only on success."]),

 "Dijkstra (weighted shortest path, non-negative)": (
   ["Initialize `dist[]` to `\u221e` except `dist[src] = 0`.",
    "Min-heap of `{node, distance}`. Offer `{src, 0}`.",
    "Pop the top. If its `d > dist[u]`, it's a **stale** entry \u2014 skip.",
    "Otherwise, relax each outgoing edge `(u, v, w)`: if `d + w < dist[v]`, update and push `{v, d+w}`.",
    "Continue until the heap is empty. Distances are final on first pop (since edges are non-negative).",
    "Time O(E log V) with lazy deletion."],
   ["**Skipping the stale-pop guard**: without `if (d > dist[u]) continue;`, popped-then-updated nodes re-relax with wrong distances.",
    "**Using it with negative edges**: greedy assumption breaks \u2014 use Bellman\u2013Ford instead.",
    "**Storing `{node}` alone**: you need the distance in the heap for lazy deletion (Java has no decrease-key).",
    "**Overflow on `d + w`**: for large edge weights, widen the accumulator to `long`.",
    "**Undirected forgotten**: add both `(u, v, w)` and `(v, u, w)` to the adjacency list."]),

 "Median of Two Sorted Arrays (Partition Binary Search)": (
   ["Ensure `nums1` is the shorter array (swap if not) \u2014 keeps the binary-search range small.",
    "Binary-search `i` over `[0, m]`; set `j = (m + n + 1) / 2 - i`.",
    "Boundary values: `L1 = i > 0 ? nums1[i-1] : -\u221e`; `R1 = i < m ? nums1[i] : +\u221e`. Symmetric for `L2, R2`.",
    "If `L1 <= R2 && L2 <= R1` \u2014 partition is correct.",
    "If `L1 > R2` \u2014 `i` is too big; shrink `hi = i - 1`. Else `lo = i + 1`.",
    "Once partitioned: odd total \u2192 `max(L1, L2)`; even \u2192 `(max(L1,L2) + min(R1,R2)) / 2.0`."],
   ["**Not shortening the shorter array first** \u2014 the binary search range should be the smaller of `m`, `n`.",
    "**Off-by-one in the left-half size** \u2014 use `(m + n + 1) / 2` so the median lives on the left when odd.",
    "**Missing the `\u00b1\u221e` sentinels** for empty halves \u2014 use `Integer.MIN/MAX_VALUE`.",
    "**Averaging as ints** for even-total median \u2014 divide by `2.0` (return `double`)."]),

 "LRU Cache (Design)": (
   ["Combine `HashMap<Key, Node>` + a doubly-linked list; the list keeps recency (front = MRU, back = LRU).",
    "Add dummy `head` and `tail` sentinels to eliminate edge cases in linking.",
    "`get(key)`: if absent \u2192 `-1`. Else unlink the node and re-insert at the front; return its value.",
    "`put(key, value)`: if the key exists, update value and move to front. Otherwise, allocate a node, insert at front, `map.put`.",
    "If `map.size() > capacity`, evict `tail.prev` \u2014 unlink it and `map.remove` its key.",
    "Alternatively, extend `LinkedHashMap` with `accessOrder=true` and override `removeEldestEntry`."],
   ["**Not updating recency on `get`** \u2014 the whole point of LRU is that `get` is a mutation.",
    "**Forgetting head/tail sentinels** \u2014 you'll write null-checks in five places instead of zero.",
    "**Evicting before the size actually exceeds capacity** \u2014 evict only *after* inserting, only if `size > cap`.",
    "**Using the wrong map key on eviction** \u2014 remove the node's key from the map, not the node itself.",
    "**Not extending `LinkedHashMap` correctly** \u2014 must call `super(capacity, 0.75f, true)` and override `removeEldestEntry`."]),

 "Course Schedule (Topological Sort)": (
   ["Build the adjacency list `graph[prereq] \u2192 [course]` and an `inDegree[]` counter.",
    "Enqueue every node with `inDegree == 0` \u2014 they can start immediately.",
    "Repeatedly pop, add to the order, and decrement each neighbour's in-degree. Enqueue neighbours whose in-degree hits 0.",
    "After the loop, if `order.size() < V` \u2014 there was a cycle \u2192 return `[]` (or `false` for the boolean variant).",
    "Otherwise return the order. O(V + E) time."],
   ["**Edge direction reversed**: `prereq \u2192 course`, not `course \u2192 prereq`. Reverse it and cycle detection breaks.",
    "**Not detecting the cycle**: if `order.size() < V` at the end, report impossible \u2014 don't return a partial order.",
    "**Building the graph off `numCourses` instead of the max node index**: initialize adjacency for all `numCourses` even if some are isolated.",
    "**DFS variant needs 3-state marking**: unvisited / in-progress / done \u2014 a back-edge into an in-progress node is the cycle."]),

 "Merge Intervals": (
   ["Sort the intervals by `start` \u2014 O(n log n) prerequisite for the linear sweep.",
    "Initialize `out` with the first interval.",
    "For each subsequent interval `cur`: if `cur.start <= last.end` \u2014 they overlap or touch; update `last.end = max(last.end, cur.end)`.",
    "Otherwise \u2014 push `cur` as a new interval.",
    "Return `out`. O(n log n) total."],
   ["**Touching vs overlapping**: `[1,2]` and `[2,3]` are treated as overlapping on LC Merge Intervals; `<=` is correct here.",
    "**Sorting by end** would break the merging invariant \u2014 sort by start.",
    "**Mutating input intervals** may cause bugs when the interviewer's harness reuses them \u2014 push copies.",
    "**Comparator overflow**: use `Integer.compare(a[0], b[0])`, not `a[0] - b[0]`, for large starts."]),

 "Longest Substring Without Repeating Characters": (
   ["Maintain a `left` pointer and a map (or `int[128]`) from char \u2192 its last-seen index.",
    "Scan `right` left to right. If `s[right]` was seen and its last index >= `left`, clamp: `left = lastIndex[s[right]] + 1`.",
    "Update `lastIndex[s[right]] = right`.",
    "Update `best = max(best, right - left + 1)` each step.",
    "O(n) time, O(alphabet) space."],
   ["**Not clamping `left`** on the previous-index bump \u2014 `left = max(left, prev + 1)` is required.",
    "**Restarting `left` from prev+1 unconditionally** \u2014 you'll move `left` backwards on old-but-now-outside occurrences.",
    "**Off-by-one on window size**: `right - left + 1`, not `right - left`.",
    "**Alphabet assumption**: full unicode needs a `HashMap`, not `int[128]`."]),

 "Sliding Window Maximum (Monotonic Deque)": (
   ["Deque holds **indices**, front-to-back non-increasing in value.",
    "For each `i`: while the back's value `<= nums[i]`, pop it \u2014 it can't be the max of any future window.",
    "Push `i`.",
    "If the front's index has fallen out of the window (`<= i - k`), pop it.",
    "When `i >= k - 1`, record `nums[dq.peekFirst()]` as the current window max.",
    "O(n) amortized \u2014 each index enters and leaves the deque at most once."],
   ["**Storing values, not indices** \u2014 you can't detect front-of-window expiry.",
    "**Wrong pop direction**: `<= nums[i]` (strictly weaker or equal) keeps the deque non-increasing.",
    "**Recording the max too early** (before the first full window forms) \u2014 wait until `i >= k - 1`.",
    "**Using `LinkedList` instead of `ArrayDeque`** \u2014 slower and higher memory."]),
}

def apply_to_file(path):
    txt = open(path, encoding="utf-8").read()
    orig = txt
    parts = re.split(r'(?m)^(## .+)$', txt)
    rebuilt = [parts[0]]
    changed_titles = []
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i+1] if i+1 < len(parts) else ''
        title = header[3:].strip().replace('&amp;','&')
        up = UPGRADES.get(title)
        if up:
            steps, mistakes = up
            # Insert Steps block right BEFORE ### Java
            steps_block = "### Steps\n" + "\n".join(f"{i+1}. {s}" for i,s in enumerate(steps)) + "\n\n"
            # Only add if not already present
            if "### Steps\n" not in body:
                java_re = re.compile(r'\n### Java', re.MULTILINE)
                m = java_re.search(body)
                if m:
                    body = body[:m.start()] + "\n" + steps_block + body[m.start()+1:]
            # Insert Common Mistakes block right AFTER the [trap] callout
            if mistakes and "### Common Mistakes" not in body:
                trap_re = re.compile(r'(> \[trap\] \*\*Common Trap\*\* \u2014 [^\n]+)\n')
                m = trap_re.search(body)
                if m:
                    cm_block = "\n### Common Mistakes\n" + "\n".join(f"- {mi}" for mi in mistakes) + "\n"
                    body = body[:m.end()] + cm_block + body[m.end():]
            changed_titles.append(title)
        rebuilt.append(header); rebuilt.append(body)
    new_txt = "".join(rebuilt)
    if new_txt != orig:
        open(path, "w", encoding="utf-8").write(new_txt)
    return changed_titles

if __name__ == "__main__":
    all_touched = []
    for f in sorted(os.listdir(ROOT)):
        if not re.match(r'^(3\d|4\d|5\d|6[0-5])-', f): continue
        touched = apply_to_file(os.path.join(ROOT, f))
        for t in touched: all_touched.append((f, t))
    print(f"upgraded {len(all_touched)} problem sections:")
    for f, t in all_touched: print(f"  {f} \u2192 {t}")
    # Which curated keys never matched a title?
    matched = set(t for _, t in all_touched)
    for key in UPGRADES:
        if key not in matched:
            print(f"  ! not matched: {key}")
