"""Generate t3-indexes.md: curated indexes + auto-extracted Master Problem Index."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "src" / "content"
manifest = json.loads((ROOT / "src" / "manifest.json").read_text(encoding="utf-8"))

H2 = re.compile(r"^##\s+(?!#)(.+)$", re.M)
SKIP = {"concepts & mental models", "the dp thought process"}
rows = []
for item in manifest["items"]:
    if item.get("type") != "chapter":
        continue
    cid = item["id"]
    if not re.match(r"m\d\d", cid):
        continue
    f = CONTENT / item["file"]
    if not f.exists():
        continue
    for m in H2.finditer(f.read_text(encoding="utf-8")):
        title = re.sub(r"\s*\([^)]*\)\s*$", "", m.group(1).strip())
        if title.lower() in SKIP:
            continue
        rows.append((title, item["title"]))
rows.sort(key=lambda r: r[0].lower())

problem_table = ["| Problem | Module |", "|---|---|"]
for t, mod in rows:
    problem_table.append(f"| {t} | {mod} |")
problem_table = "\n".join(problem_table)

CURATED = r"""## How to Use These Indexes

Revision is a lookup problem. When a friend names a random problem, you should recall its
pattern in seconds; when an interviewer describes a scenario, you should map its signals to a
technique. These indexes train both directions.

## Pattern to Problems

The fastest revision drill: cover the right column, read a pattern, and reconstruct its problems
from memory.

| Pattern | Representative problems |
|---|---|
| Sliding Window | Longest Substring Without Repeating Characters, Minimum Window Substring, Sliding Window Maximum |
| Two Pointers | Dutch National Flag, Two Sum (sorted), Palindrome checks, Reorder List |
| Fast & Slow Pointers | Linked List Cycle, Find Cycle Start, Middle of List, Palindrome Linked List, Happy Number |
| Monotonic Stack | Daily Temperatures, Next Greater Element, Largest Rectangle in Histogram |
| Binary Search | Binary Search, Search in Rotated Sorted Array, Find Minimum in Rotated Array, Search a 2D Matrix |
| Binary Search on Answer | Koko Eating Bananas, Capacity to Ship Packages, Book Allocation, Median of Two Sorted Arrays |
| Top-K / Heap | Kth Largest Element, Top K Frequent Elements, Merge K Sorted Lists, Find Median from Data Stream |
| Merge Intervals / Sweep | Meeting Rooms II, Non-overlapping Intervals, Corporate Flight Bookings |
| Topological Sort | Course Schedule, Alien Dictionary |
| Union-Find | Number of Connected Components, Accounts Merge, Kruskal's MST |
| BFS / DFS on graphs | Number of Islands, Clone Graph, Rotting Oranges, Word Ladder |
| Shortest Path | Dijkstra / Network Delay Time, Cheapest Flights Within K Stops |
| Prefix Sum + HashMap | Subarray Sum Equals K, Product of Array Except Self |
| Difference Array | Range Addition, Corporate Flight Bookings |
| 1D DP | Climbing Stairs, House Robber, Decode Ways |
| Knapsack DP | 0/1 Knapsack, Partition Equal Subset Sum, Coin Change, Coin Change II |
| Grid DP | Unique Paths, Minimum Path Sum, Edit Distance, Longest Common Subsequence |
| Sequence DP | Longest Increasing Subsequence, Longest Common Subsequence |
| Interval DP | Burst Balloons, Matrix Chain Multiplication |
| State-Machine DP | Best Time to Buy/Sell Stock with Cooldown |
| Tree DP | House Robber III, Binary Tree Maximum Path Sum, Diameter of Binary Tree |
| Backtracking | N-Queens, Combination Sum, Word Search, Palindrome Partitioning, Permutations II, Sudoku Solver |
| Tries | Implement Trie, Word Search II |
| Bitmasking | Power Set, Single Number family, subset enumeration |
| Divide & Conquer | Merge Sort, Count Inversions |
| Quickselect | Kth Largest Element, k-th order statistic |
| XOR tricks | Single Number, Missing Number |

## Data Structure to Problems

| Data structure | Problems where it is the key choice |
|---|---|
| HashMap / HashSet | Two Sum, Subarray Sum Equals K, Longest Consecutive Sequence, Group Anagrams, LRU Cache |
| Stack (ArrayDeque) | Valid Parentheses, Daily Temperatures, Largest Rectangle, Min Stack |
| Deque | Sliding Window Maximum |
| Heap (PriorityQueue) | Top K Frequent, Merge K Sorted Lists, Find Median from Data Stream, Meeting Rooms II, Dijkstra |
| BST / TreeMap | Kth Smallest in BST, Validate BST, ordered range queries |
| Trie | Implement Trie, Word Search II |
| Union-Find | Number of Connected Components, Accounts Merge, Kruskal |
| Doubly Linked List + Map | LRU Cache |
| Prefix / Difference array | Range Sum Query, Range Addition, Corporate Flight Bookings |
| Monotonic stack/deque | Next Greater Element, Histogram, Sliding Window Maximum |
| Segment Tree / Fenwick | Range Sum Query (mutable), Count of Range Sums |

## Complexity to Algorithm

| Target complexity | Techniques that hit it |
|---|---|
| O(1) space over a scan | XOR accumulation, two pointers, Kadane, running counters |
| O(log n) | binary search, balanced BST, heap push/pop |
| O(n) | sliding window, prefix sums, monotonic stack, BFS/DFS, quickselect (expected), counting sort |
| O(n log n) | comparison sort, heap of n, merge sort, sort-then-sweep, LIS (patience) |
| O(n k) / O(n W) | knapsack, coin change, edit distance, grid DP |
| O(V + E) | graph traversal, topological sort |
| O(E log V) | Dijkstra, Prim, Kruskal |
| Exponential / factorial | subset/permutation backtracking, bitmask DP |

## Interview Follow-Up to Technique

| If the interviewer adds... | Reach for... |
|---|---|
| "...now stream the input / unbounded data" | heap of size k, reservoir sampling, two-heaps median |
| "...now the array can contain negatives" | prefix-sum + hashmap instead of sliding window |
| "...now support updates between queries" | Fenwick / segment tree instead of a static prefix array |
| "...now k appears three times except one" | per-bit modular counting instead of plain XOR |
| "...now return all solutions, not just one" | backtracking instead of greedy/DP-value |
| "...now edges have weights" | Dijkstra instead of BFS |
| "...now weights can be negative" | Bellman-Ford instead of Dijkstra |
| "...reduce the O(n) extra space" | rolling-array DP, in-place marking, bit tricks |

## Master Problem Index

Every canonical problem in Part I, alphabetized, with its home module.

"""

out = CURATED + problem_table + "\n"
(CONTENT / "t3-indexes.md").write_text(out, encoding="utf-8")
print(f"wrote t3-indexes.md with {len(rows)} indexed problems")
