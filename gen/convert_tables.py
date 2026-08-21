"""Convert prose 'Same pattern, new tweaks' sections into 4-column linked tables.
Preserves the intro tagline; each bullet becomes: Variation | The one thing that changes | Time | link.
Also fills in known LeetCode slugs for orphan (link-less) variation names.
"""
import re, os, glob

# Curated slug map for orphan variation names (bold-only, no URL)
SLUG = {
 # arrays / hashing
 "Longest Substring with At Most K Distinct":"longest-substring-with-at-most-k-distinct-characters",
 "Longest Substring with At Most Two Distinct":"longest-substring-with-at-most-two-distinct-characters",
 "Serialize N-ary Tree":"serialize-and-deserialize-n-ary-tree",
 "Maximal Square / Maximal Rectangle":"maximal-rectangle",
 "Valid Palindrome / Valid Palindrome II":"valid-palindrome-ii",
 "Merge Sorted Array (in place, from the back)":"merge-sorted-array",
 "Trapping Rain Water II (2D)":"trapping-rain-water-ii",
 "Replace the Substring for Balanced String":"replace-the-substring-for-balanced-string",
 "Shortest Subarray with Sum ≥ K (negatives allowed)":"shortest-subarray-with-sum-at-least-k",
 "Shortest Subarray with Sum ≥ K (with negatives)":"shortest-subarray-with-sum-at-least-k",
 "Permutation in String / Find All Anagrams":"find-all-anagrams-in-a-string",
 "Substring with Concatenation of All Words":"substring-with-concatenation-of-all-words",
 "Frequency of the Most Frequent Element":"frequency-of-the-most-frequent-element",
 "Find All Numbers Disappeared / Find All Duplicates":"find-all-numbers-disappeared-in-an-array",
 "Remove K Digits / Largest Rectangle variants":"remove-k-digits",
 "Search in Rotated Array II (with duplicates)":"search-in-rotated-sorted-array-ii",
 "Order-Agnostic Binary Search":"binary-search",
 "Split Array Largest Sum / Book Allocation":"split-array-largest-sum",
 "Divide Chocolate / Maximize the Minimum":"divide-chocolate",
 "Kth Element of Two Sorted Arrays":"median-of-two-sorted-arrays",
 "Find K-th Smallest Pair Distance":"find-k-th-smallest-pair-distance",
 "Maximum Subarray (Kadane)":"maximum-subarray",
 "Minimum Number of Platforms":"meeting-rooms-ii",
 "My Calendar II / III":"my-calendar-ii",
 "Subsets II (with duplicates)":"subsets-ii",
 "Combination Sum / Combination Sum II":"combination-sum-ii",
 "Permutations II (with duplicates)":"permutations-ii",
 "Letter Case Permutation":"letter-case-permutation",
 "Number of Reverse Pairs / Global Inversions":"reverse-pairs",
 "Kth Largest Element":"kth-largest-element-in-an-array",
 "Min Cost Climbing Stairs / Paint Fence":"min-cost-climbing-stairs",
 "Coin Change (min coins)":"coin-change",
 "Combination Sum IV (count ordered sequences)":"combination-sum-iv",
 "Unique Paths / Unique Paths II":"unique-paths-ii",
 "Minimum Path Sum / Minimum Falling Path Sum":"minimum-falling-path-sum",
 "Regex / Wildcard Matching":"regular-expression-matching",
 "Minimum Cost to Merge Stones":"minimum-cost-to-merge-stones",
 "Palindrome Partitioning II":"palindrome-partitioning-ii",
 "Best Time to Buy/Sell with Cooldown":"best-time-to-buy-and-sell-stock-with-cooldown",
 "Best Time with Transaction Fee":"best-time-to-buy-and-sell-stock-with-transaction-fee",
 "Best Time with at most k Transactions":"best-time-to-buy-and-sell-stock-iv",
 "Paint House I/II":"paint-house-ii",
 "Number of Ways to Assign (hats/jobs)":"number-of-ways-to-wear-different-hats-to-each-other",
 "Find the Difference / Set Mismatch":"find-the-difference",
 "Sum of All Subset XOR / SOS DP":"sum-of-all-subset-xor-totals",
 "Range Sum/Min/Max Query — Mutable":"range-sum-query-mutable",
 "Range Add + Range Sum":"range-sum-query-mutable",
 "Count of Range Sum / Range Module":"count-of-range-sum",
 "Serialize/Deserialize Binary Tree":"serialize-and-deserialize-binary-tree",
 "Encode/Decode TinyURL":"encode-and-decode-tinyurl",
 "LCA with Parent Pointers":"lowest-common-ancestor-of-a-binary-tree-iii",
 "Distance Between Two Nodes":"lowest-common-ancestor-of-a-binary-tree",
 "Convert BST to Sorted Doubly Linked List":"convert-binary-search-tree-to-sorted-doubly-linked-list",
 "Construct String from Binary Tree":"construct-string-from-binary-tree",
 "Construct from Inorder + Postorder":"construct-binary-tree-from-inorder-and-postorder-traversal",
 "Construct BST from Preorder":"construct-binary-search-tree-from-preorder-traversal",
 "Construct from Preorder + Postorder":"construct-binary-tree-from-preorder-and-postorder-traversal",
 "Convert Sorted Array/List to BST":"convert-sorted-array-to-binary-search-tree",
 "Add and Search Word (wildcard `.`)":"design-add-and-search-words-data-structure",
 "Count Pairs With XOR in a Range":"count-pairs-with-xor-in-a-range",
 "Replace Words / IP routing":"replace-words",
 "Dijkstra with weights ∈ {0,1}":"01-matrix",
 "Negative-cycle detection":"find-if-path-exists-in-graph",
 "All-pairs, small V":"find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance",
 "Connecting Cities With Minimum Cost":"connecting-cities-with-minimum-cost",
 "Optimize Water Distribution in a Village":"optimize-water-distribution-in-a-village",
 "Articulation points":"critical-connections-in-a-network",
 "Strongly Connected Components":"critical-connections-in-a-network",
 "Cracking the Safe":"cracking-the-safe",
 "Modular exponentiation":"super-pow",
 "Matrix exponentiation":"fibonacci-number",
 "Smallest-prime-factor sieve":"count-primes",
 "2D — Range Addition II / stamping a grid":"range-addition-ii",
 # arrays / hashing / other rescue
 "Fraction to Recurring Decimal":"fraction-to-recurring-decimal",
 "Water and Jug Problem":"water-and-jug-problem",
 # keep existing entries below unchanged
 "Two Sum II — Input Array Is Sorted":"two-sum-ii-input-array-is-sorted",
 "3Sum Smaller":"3sum-smaller","Triplets with Smaller Sum":"3sum-smaller",
 "Two-Sum in a BST":"two-sum-iv-input-is-a-bst",
 "Wiggle Sort":"wiggle-sort-ii","Partition (Quicksort step)":"kth-largest-element-in-an-array",
 "Max Stack":"max-stack",
 "Stock Span / Online Stock Span":"online-stock-span",
 "Sliding Window Minimum/Maximum":"sliding-window-maximum",
 # binary search
 "Find Peak Element":"find-peak-element","First Bad Version":"first-bad-version",
 "Search Insert Position":"search-insert-position","Find Right Interval":"find-right-interval",
 "Aggressive Cows / Magnetic Force":"magnetic-force-between-two-balls",
 "Painters Partition":"split-array-largest-sum",
 "Capacity To Ship":"capacity-to-ship-packages-within-d-days",
 "Minimum Number of Days to Make m Bouquets":"minimum-number-of-days-to-make-m-bouquets",
 "Kth Smallest Prime Fraction":"k-th-smallest-prime-fraction",
 "Median of Row-Sorted Matrix":"find-median-in-a-sorted-array-of-integers",
 # greedy
 "Task Scheduler":"task-scheduler","Activity Selection":"non-overlapping-intervals",
 "Partition Labels":"partition-labels",
 # intervals
 "Insert Interval":"insert-interval","Meeting Rooms":"meeting-rooms",
 "My Calendar I":"my-calendar-i","Employee Free Time":"employee-free-time",
 "Car Pooling":"car-pooling",
 "The Skyline Problem":"the-skyline-problem",
 # backtracking
 "Subsets II":"subsets-ii","Permutations II":"permutations-ii",
 "Combination Sum II":"combination-sum-ii","Combination Sum III":"combination-sum-iii",
 "Palindrome Partitioning":"palindrome-partitioning",
 "Generate Parentheses":"generate-parentheses",
 "Letter Combinations of a Phone Number":"letter-combinations-of-a-phone-number",
 "N-Queens II":"n-queens-ii","Sudoku Solver":"sudoku-solver",
 "Word Search II":"word-search-ii",
 # divide & conquer
 "Reverse Pairs":"reverse-pairs","Count of Range Sum":"count-of-range-sum",
 "Sort an Array":"sort-an-array","Kth Largest Element in an Array":"kth-largest-element-in-an-array",
 # DP
 "Climbing Stairs":"climbing-stairs","House Robber II":"house-robber-ii",
 "Delete and Earn":"delete-and-earn","Min Cost Climbing Stairs":"min-cost-climbing-stairs",
 "Paint Fence":"paint-fence",
 "Partition Equal Subset Sum":"partition-equal-subset-sum",
 "Target Sum":"target-sum","Last Stone Weight II":"last-stone-weight-ii",
 "Ones and Zeroes":"ones-and-zeroes",
 "Coin Change 2":"coin-change-ii","Perfect Squares":"perfect-squares",
 "Combination Sum IV":"combination-sum-iv",
 "Unique Paths":"unique-paths","Minimum Path Sum":"minimum-path-sum",
 "Dungeon Game":"dungeon-game","Cherry Pickup II":"cherry-pickup-ii",
 "Longest Increasing Subsequence":"longest-increasing-subsequence",
 "Longest Common Subsequence":"longest-common-subsequence",
 "Edit Distance":"edit-distance","Distinct Subsequences":"distinct-subsequences",
 "Wildcard Matching":"wildcard-matching","Regular Expression Matching":"regular-expression-matching",
 "Matrix Chain Multiplication":"burst-balloons","Burst Balloons":"burst-balloons",
 "Best Time to Buy and Sell Stock":"best-time-to-buy-and-sell-stock",
 "Best Time to Buy and Sell Stock II":"best-time-to-buy-and-sell-stock-ii",
 "Best Time to Buy and Sell Stock III":"best-time-to-buy-and-sell-stock-iii",
 "Best Time to Buy and Sell Stock IV":"best-time-to-buy-and-sell-stock-iv",
 "Stock with Cooldown":"best-time-to-buy-and-sell-stock-with-cooldown",
 "Stock with Transaction Fee":"best-time-to-buy-and-sell-stock-with-transaction-fee",
 "Travelling Salesman":"find-the-shortest-superstring",
 "Partition to K Equal Sum Subsets":"partition-to-k-equal-sum-subsets",
 # bits / segment tree
 "Missing Number":"missing-number","Set Mismatch":"set-mismatch",
 "Find the Difference":"find-the-difference",
 "Single Number II":"single-number-ii","Single Number III":"single-number-iii",
 "Bitwise AND of Numbers Range":"bitwise-and-of-numbers-range",
 "Permutations":"permutations","Beautiful Arrangement":"beautiful-arrangement",
 "Range Sum Query — Mutable":"range-sum-query-mutable",
 "Count of Smaller Numbers After Self":"count-of-smaller-numbers-after-self",
 "Count of Range Sum":"count-of-range-sum",
 # strings
 "Palindromic Substrings":"palindromic-substrings",
 "Longest Palindromic Subsequence":"longest-palindromic-subsequence",
 "Repeated Substring Pattern":"repeated-substring-pattern",
 "Shortest Palindrome":"shortest-palindrome","Rabin–Karp":"repeated-dna-sequences",
 "Serialize and Deserialize":"encode-and-decode-strings",
 # linked list
 "Reverse Nodes in k-Group":"reverse-nodes-in-k-group",
 "Reverse Linked List II":"reverse-linked-list-ii",
 "Rotate List":"rotate-list","Linked List Cycle":"linked-list-cycle",
 "Middle of the Linked List":"middle-of-the-linked-list",
 "Happy Number":"happy-number","Find the Duplicate Number":"find-the-duplicate-number",
 "Copy List with Random Pointer":"copy-list-with-random-pointer",
 "Merge Two Sorted Lists":"merge-two-sorted-lists",
 "Add Two Numbers":"add-two-numbers","Odd Even Linked List":"odd-even-linked-list",
 "Reorder List":"reorder-list","Palindrome Linked List":"palindrome-linked-list",
 "All O`one Data Structure":"all-oone-data-structure",
 # trees
 "Symmetric Tree":"symmetric-tree","Same Tree":"same-tree","Invert Binary Tree":"invert-binary-tree",
 "Binary Tree Right Side View":"binary-tree-right-side-view",
 "Zigzag Level Order":"binary-tree-zigzag-level-order-traversal",
 "Level Order Traversal":"binary-tree-level-order-traversal",
 "Balanced Binary Tree":"balanced-binary-tree","Diameter of Binary Tree":"diameter-of-binary-tree",
 "Binary Tree Maximum Path Sum":"binary-tree-maximum-path-sum",
 "LCA of a BST":"lowest-common-ancestor-of-a-binary-search-tree",
 "LCA of Deepest Leaves":"lowest-common-ancestor-of-deepest-leaves",
 "Kth Smallest in BST":"kth-smallest-element-in-a-bst",
 "Recover BST":"recover-binary-search-tree",
 "Serialize/Deserialize BST":"serialize-and-deserialize-bst",
 "Construct from Postorder + Inorder":"construct-binary-tree-from-inorder-and-postorder-traversal",
 "Path Sum":"path-sum-ii","Longest Univalue Path":"longest-univalue-path",
 "Distribute Coins in Binary Tree":"distribute-coins-in-binary-tree",
 # heaps
 "IPO":"ipo","Reorganize String":"reorganize-string",
 "Sliding Window Median":"sliding-window-median",
 "Kth Smallest Element in a Sorted Matrix":"kth-smallest-element-in-a-sorted-matrix",
 "Find K Pairs with Smallest Sums":"find-k-pairs-with-smallest-sums",
 "Smallest Range Covering Elements from K Lists":"smallest-range-covering-elements-from-k-lists",
 "Ugly Number II":"ugly-number-ii",
 # trie
 "Design Add and Search Words":"design-add-and-search-words-data-structure",
 "Replace Words":"replace-words","Map Sum Pairs":"map-sum-pairs",
 "Longest Word in Dictionary":"longest-word-in-dictionary",
 "Palindrome Pairs":"palindrome-pairs",
 # graphs
 "Surrounded Regions":"surrounded-regions","Pacific Atlantic Water Flow":"pacific-atlantic-water-flow",
 "Word Ladder":"word-ladder","Open the Lock":"open-the-lock",
 "Shortest Path in Binary Matrix":"shortest-path-in-binary-matrix",
 "Alien Dictionary":"alien-dictionary","Parallel Courses":"parallel-courses",
 "Sequence Reconstruction":"sequence-reconstruction",
 "Accounts Merge":"accounts-merge","Redundant Connection":"redundant-connection",
 "Number of Provinces":"number-of-provinces","Graph Valid Tree":"graph-valid-tree",
 "Number of Connected Components in an Undirected Graph":"number-of-connected-components-in-an-undirected-graph",
 "Most Stones Removed":"most-stones-removed-with-same-row-or-column",
 "Regions Cut By Slashes":"regions-cut-by-slashes",
 "Satisfiability of Equality Equations":"satisfiability-of-equality-equations",
 "Network Delay Time":"network-delay-time",
 "Path With Minimum Effort":"path-with-minimum-effort",
 "Swim in Rising Water":"swim-in-rising-water",
 "Is Graph Bipartite / Possible Bipartition":"is-graph-bipartite",
 "Is Graph Bipartite":"is-graph-bipartite",
 "Course Schedule (cycle detect)":"course-schedule",
 "Course Schedule III":"course-schedule-iii",
 "Reconstruct Itinerary":"reconstruct-itinerary",
 "Strongly Connected Components":"critical-connections-in-a-network",
 "Articulation points":"critical-connections-in-a-network",
 "Cracking the Safe":"cracking-the-safe",
 "Valid Arrangement of Pairs":"valid-arrangement-of-pairs",
 "Smallest-prime-factor sieve":"count-primes","Ugly Number II ":"ugly-number-ii",
 # math / design
 "Modular exponentiation":"powx-n","Matrix exponentiation":"fibonacci-number",
 "Fisher–Yates shuffle":"shuffle-an-array",
}

# The one-line "How to complete" for a variation is derived from the tweak text itself.
def make_time(bullet):
    m = re.search(r'\bO\(([^)]+)\)', bullet)
    return f"O({m.group(1)})" if m else "—"

def make_row(bullet):
    """Parse a bullet like:
      - [Name](url) — *tweak:* description.
      - **Name** — *tweak:* description.
    Returns (name_cell, changes_cell, time_cell).
    """
    b = bullet.strip()
    if b.startswith("- "): b = b[2:]
    # linked?
    m = re.match(r'\[([^\]]+)\]\((https?://[^\)]+)\)\s*[—-]\s*(.*)', b)
    if m:
        name, url, rest = m.group(1), m.group(2), m.group(3)
        name_cell = f"[{name}]({url})"
    else:
        m = re.match(r'\*\*([^*]+)\*\*\s*[—-]\s*(.*)', b)
        if not m:
            return None
        name, rest = m.group(1), m.group(2)
        slug = SLUG.get(name)
        name_cell = f"[{name}](https://leetcode.com/problems/{slug}/)" if slug else f"**{name}**"
    # rest is: *tweak:* description.
    rest = re.sub(r'^\*tweak:\*\s*', '', rest).rstrip(' .')
    time_cell = make_time(rest)
    if time_cell != "—":
        rest = re.sub(r',?\s*O\([^)]+\)\.?$', '', rest).rstrip(' .')
    return name_cell, rest, time_cell

def convert_section(intro, bullets_block):
    """intro is the tagline (may be blank). bullets_block is the raw bullet text.
    Returns the new markdown to replace them.
    """
    lines = [ln for ln in bullets_block.split('\n') if ln.strip()]
    bullets = [ln for ln in lines if ln.lstrip().startswith('- ')]
    rows=[]
    for b in bullets:
        r = make_row(b)
        if r:
            rows.append(r)
        else:
            rows.append((b, "", "—"))
    if not rows: return None
    out = []
    if intro.strip():
        out.append(intro.rstrip())
        out.append("")
    out.append("| Variation | The one thing that changes | Time |")
    out.append("|---|---|---|")
    for n, ch, t in rows:
        out.append(f"| {n} | {ch} | {t} |")
    return "\n".join(out)

def process_file(path):
    txt = open(path, encoding="utf-8").read()
    orig = txt
    pattern = re.compile(r'(### Same pattern, new tweaks\n\n)(.*?)(?=\n#{1,3}\s|\Z)', re.DOTALL)
    changed = 0
    def repl(m):
        nonlocal changed
        header, body = m.group(1), m.group(2)
        if '| Variation |' in body: return m.group(0)  # already table
        # Split intro (non-bullet lines at top) from bullet block
        segs = body.strip().split('\n')
        intro_lines=[]; i=0
        while i < len(segs) and not segs[i].lstrip().startswith('- '):
            intro_lines.append(segs[i]); i+=1
        intro = "\n".join(intro_lines).strip()
        bullets = "\n".join(segs[i:])
        conv = convert_section(intro, bullets)
        if not conv: return m.group(0)
        changed += 1
        return header + conv + "\n"
    new = pattern.sub(repl, txt)
    if new != orig:
        open(path, "w", encoding="utf-8").write(new)
    return changed

root = os.path.join(os.path.dirname(__file__), "src")
total = 0
for f in sorted(os.listdir(root)):
    if not re.match(r'^(3\d|4\d|5\d|6[0-5]|9\d)-', f): continue
    n = process_file(os.path.join(root, f))
    if n: print(f"{f:25} converted: {n}")
    total += n
print(f"\nTOTAL sections converted: {total}")
