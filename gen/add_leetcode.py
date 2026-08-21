import glob, os
SRC = os.path.join(os.path.dirname(__file__), "src")
# (substring to find in a lowercased "## heading" line, slug, display name)
M = [
 ("two sum","two-sum","Two Sum"),
 ("group anagrams","group-anagrams","Group Anagrams"),
 ("product of array except self","product-of-array-except-self","Product of Array Except Self"),
 ("longest consecutive","longest-consecutive-sequence","Longest Consecutive Sequence"),
 ("subarray sum equals k","subarray-sum-equals-k","Subarray Sum Equals K"),
 ("difference array","corporate-flight-bookings","Corporate Flight Bookings"),
 ("2d prefix","range-sum-query-2d-immutable","Range Sum Query 2D"),
 ("3sum","3sum","3Sum"),
 ("container with most water","container-with-most-water","Container With Most Water"),
 ("squaring a sorted array","squares-of-a-sorted-array","Squares of a Sorted Array"),
 ("sort colors","sort-colors","Sort Colors"),
 ("trapping rain water","trapping-rain-water","Trapping Rain Water"),
 ("smallest subarray with sum","minimum-size-subarray-sum","Minimum Size Subarray Sum"),
 ("longest substring without repeating","longest-substring-without-repeating-characters","Longest Substring Without Repeating Characters"),
 ("minimum window substring","minimum-window-substring","Minimum Window Substring"),
 ("longest repeating character replacement","longest-repeating-character-replacement","Longest Repeating Character Replacement"),
 ("sliding window maximum","sliding-window-maximum","Sliding Window Maximum"),
 ("find the missing number","missing-number","Missing Number"),
 ("find all missing","find-all-numbers-disappeared-in-an-array","Find All Numbers Disappeared in an Array"),
 ("first missing positive","first-missing-positive","First Missing Positive"),
 ("longest palindromic substring","longest-palindromic-substring","Longest Palindromic Substring"),
 ("encode and decode strings","encode-and-decode-strings","Encode and Decode Strings"),
 ("reverse a linked list","reverse-linked-list","Reverse Linked List"),
 ("linked list cycle ii","linked-list-cycle-ii","Linked List Cycle II"),
 ("merge two / k sorted","merge-k-sorted-lists","Merge k Sorted Lists"),
 ("reorder / palindrome","palindrome-linked-list","Palindrome Linked List"),
 ("lru cache","lru-cache","LRU Cache"),
 ("valid parentheses","valid-parentheses","Valid Parentheses"),
 ("daily temperatures","daily-temperatures","Daily Temperatures"),
 ("largest rectangle","largest-rectangle-in-histogram","Largest Rectangle in Histogram"),
 ("min stack","min-stack","Min Stack"),
 ("search in rotated","search-in-rotated-sorted-array","Search in Rotated Sorted Array"),
 ("koko eating bananas","koko-eating-bananas","Koko Eating Bananas"),
 ("split array largest sum","split-array-largest-sum","Split Array Largest Sum"),
 ("median of two sorted arrays","median-of-two-sorted-arrays","Median of Two Sorted Arrays"),
 ("jump game ii","jump-game-ii","Jump Game II"),
 ("gas station","gas-station","Gas Station"),
 ("task scheduler","task-scheduler","Task Scheduler"),
 ("merge intervals","merge-intervals","Merge Intervals"),
 ("meeting rooms ii","meeting-rooms-ii","Meeting Rooms II"),
 ("non-overlapping intervals","non-overlapping-intervals","Non-overlapping Intervals"),
 ("subsets &amp; combinations","subsets","Subsets"),
 ("permutations","permutations","Permutations"),
 ("combination sum","combination-sum","Combination Sum"),
 ("n-queens","n-queens","N-Queens"),
 ("word search (grid","word-search","Word Search"),
 ("merge sort &amp; count","count-of-smaller-numbers-after-self","Count of Smaller Numbers After Self"),
 ("quickselect","kth-largest-element-in-an-array","Kth Largest Element in an Array"),
 ("maximum depth, balanced, diameter","diameter-of-binary-tree","Diameter of Binary Tree"),
 ("lowest common ancestor","lowest-common-ancestor-of-a-binary-tree","Lowest Common Ancestor of a Binary Tree"),
 ("validate bst","validate-binary-search-tree","Validate Binary Search Tree"),
 ("serialize / deserialize","serialize-and-deserialize-binary-tree","Serialize and Deserialize Binary Tree"),
 ("construct tree from traversals","construct-binary-tree-from-preorder-and-inorder-traversal","Construct Binary Tree from Preorder and Inorder"),
 ("tree dp (house robber iii)","house-robber-iii","House Robber III"),
 ("kth largest / top k","top-k-frequent-elements","Top K Frequent Elements"),
 ("find median from data stream","find-median-from-data-stream","Find Median from Data Stream"),
 ("implement trie","implement-trie-prefix-tree","Implement Trie (Prefix Tree)"),
 ("word search ii","word-search-ii","Word Search II"),
 ("maximum xor of two numbers","maximum-xor-of-two-numbers-in-an-array","Maximum XOR of Two Numbers in an Array"),
 ("number of islands","number-of-islands","Number of Islands"),
 ("rotting oranges","rotting-oranges","Rotting Oranges"),
 ("course schedule","course-schedule-ii","Course Schedule II"),
 ("dijkstra","network-delay-time","Network Delay Time"),
 ("minimum spanning tree","min-cost-to-connect-all-points","Min Cost to Connect All Points"),
 ("union-find (disjoint set","number-of-provinces","Number of Provinces"),
 ("clone graph","clone-graph","Clone Graph"),
 ("1d dp","house-robber","House Robber"),
 ("0/1 knapsack","partition-equal-subset-sum","Partition Equal Subset Sum"),
 ("coin change","coin-change","Coin Change"),
 ("grid dp","unique-paths","Unique Paths"),
 ("subsequence dp","edit-distance","Edit Distance"),
 ("interval dp","burst-balloons","Burst Balloons"),
 ("state-machine dp","best-time-to-buy-and-sell-stock-with-cooldown","Best Time to Buy and Sell Stock with Cooldown"),
 ("bitmask dp","partition-to-k-equal-sum-subsets","Partition to K Equal Sum Subsets"),
 ("single number","single-number","Single Number"),
 ("counting bits","counting-bits","Counting Bits"),
 ("subset generation via masks","subsets","Subsets"),
 ("fenwick tree","range-sum-query-mutable","Range Sum Query - Mutable"),
 ("segment tree (range","range-sum-query-mutable","Range Sum Query - Mutable"),
]

def find(headline):
    for sub, slug, disp in M:
        if sub in headline:
            return slug, disp
    return None

total = 0
for f in sorted(glob.glob(os.path.join(SRC, "*.md"))):
    lines = open(f, encoding="utf-8").read().split("\n")
    out = []
    inserted = 0
    for i, ln in enumerate(lines):
        out.append(ln)
        if ln.startswith("## "):
            hit = find(ln.lower())
            # already has a link right below?
            nxt = lines[i+1] if i+1 < len(lines) else ""
            nxt2 = lines[i+2] if i+2 < len(lines) else ""
            if hit and "leetcode.com" not in nxt and "leetcode.com" not in nxt2:
                slug, disp = hit
                out.append(f"*[\u2197 LeetCode: {disp}](https://leetcode.com/problems/{slug}/)*")
                inserted += 1
    if inserted:
        open(f, "w", encoding="utf-8").write("\n".join(out))
        print(os.path.basename(f), "->", inserted, "links")
        total += inserted
print("TOTAL links inserted:", total)
