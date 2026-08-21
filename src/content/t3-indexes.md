## How to Use These Indexes

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

| Problem | Module |
|---|---|
| Accounts Merge | Tries & Advanced Data Structures |
| Activity Selection / Non-overlapping Intervals | Greedy Algorithms |
| Alien Dictionary | Graphs |
| Best Time to Buy/Sell Stock with Cooldown | Dynamic Programming |
| Binary Search | Binary Search |
| Binary Tree Maximum Path Sum | Trees |
| Binary Tree Traversals | Trees |
| Book Allocation / Split Array Largest Sum | Binary Search |
| Burst Balloons | Dynamic Programming |
| Capacity to Ship Packages Within D Days | Binary Search |
| Cheapest Flights Within K Stops | Graphs |
| Climbing Stairs & House Robber | Dynamic Programming |
| Clone Graph | Graphs |
| Coin Change | Dynamic Programming |
| Coin Change II (count ways) & Partition Equal Subset Sum & 0/1 Knapsack | Dynamic Programming |
| Combination Sum | Recursion & Backtracking |
| Construct Binary Tree from Preorder and Inorder | Trees |
| Corporate Flight Bookings | Prefix Sum / Difference Array / Sweep Line |
| Count Inversions | Divide & Conquer / Selection |
| Course Schedule / Topological Sort | Graphs |
| Daily Temperatures | Stacks & Queues |
| Decode Ways | Dynamic Programming |
| Diameter of Binary Tree | Trees |
| Dijkstra's Algorithm / Network Delay Time | Graphs |
| Dutch National Flag | Arrays & Hashing |
| Edit Distance | Dynamic Programming |
| Find Median from Data Stream | Heaps / Priority Queues |
| Find Minimum in Rotated Sorted Array | Binary Search |
| Fractional Knapsack | Greedy Algorithms |
| Gas Station | Greedy Algorithms |
| Group Anagrams | Strings |
| House Robber III | Dynamic Programming |
| Implement Trie | Tries & Advanced Data Structures |
| Interval Scheduling / Minimum Number of Arrows / Meeting-room Style Greedy | Greedy Algorithms |
| Jump Game II | Greedy Algorithms |
| Kadane's Algorithm | Arrays & Hashing |
| KMP / Knuth-Morris-Pratt | Strings |
| Koko Eating Bananas | Binary Search |
| Kruskal's MST (with union-find) and Prim's MST | Graphs |
| Kth Largest Element | Divide & Conquer / Selection |
| Kth Largest Element in an Array | Heaps / Priority Queues |
| Kth Smallest Element in a BST | Trees |
| Largest Rectangle in Histogram | Stacks & Queues |
| Level Order Traversal | Trees |
| Linked List Cycle Detection (Floyd's) + Find Cycle Start | Linked Lists |
| Longest Common Subsequence | Dynamic Programming |
| Longest Consecutive Sequence | Arrays & Hashing |
| Longest Increasing Subsequence | Dynamic Programming |
| Longest Palindromic Substring | Strings |
| Longest Substring Without Repeating Characters | Strings |
| Lowest Common Ancestor | Trees |
| LRU Cache | Linked Lists |
| Maximum Product Subarray | Arrays & Hashing |
| Median of Two Sorted Arrays | Binary Search |
| Meeting Rooms II | Heaps / Priority Queues |
| Meeting Rooms II via Sweep Line | Prefix Sum / Difference Array / Sweep Line |
| Merge K Sorted Lists | Heaps / Priority Queues |
| Merge Sort | Divide & Conquer / Selection |
| Merge Two Sorted Lists | Linked Lists |
| Min Stack | Stacks & Queues |
| Minimum Window Substring | Strings |
| N-Queens | Recursion & Backtracking |
| Next Greater Element I/II | Stacks & Queues |
| Number of Islands | Graphs |
| Palindrome Linked List | Linked Lists |
| Palindrome Partitioning | Recursion & Backtracking |
| Permutations II | Recursion & Backtracking |
| Prefix Sum | Prefix Sum / Difference Array / Sweep Line |
| Product of Array Except Self | Arrays & Hashing |
| Quickselect | Divide & Conquer / Selection |
| Rabin-Karp | Strings |
| Range Addition / Difference Array | Prefix Sum / Difference Array / Sweep Line |
| Reorder List | Linked Lists |
| Reverse Linked List | Linked Lists |
| Reverse Linked List II | Linked Lists |
| Rotting Oranges | Graphs |
| Search a 2D Matrix | Binary Search |
| Search in Rotated Sorted Array | Binary Search |
| Segment Tree for Range Sum Query | Tries & Advanced Data Structures |
| Serialize and Deserialize Binary Tree | Trees |
| Single Number | Bit Manipulation & Math |
| Sliding Window Maximum | Stacks & Queues |
| Subarray Sum Equals K | Arrays & Hashing |
| Subarray Sum Equals K | Prefix Sum / Difference Array / Sweep Line |
| Sudoku Solver | Recursion & Backtracking |
| Top K Frequent Elements | Heaps / Priority Queues |
| Union-Find / Disjoint Set Union | Tries & Advanced Data Structures |
| Unique Paths & Minimum Path Sum | Dynamic Programming |
| Valid Parentheses | Stacks & Queues |
| Validate Binary Search Tree | Trees |
| Word Ladder | Graphs |
| Word Search | Recursion & Backtracking |
| Word Search II | Tries & Advanced Data Structures |
