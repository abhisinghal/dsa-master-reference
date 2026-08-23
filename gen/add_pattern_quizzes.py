"""Add 5-question quizzes to end of each pattern chapter."""
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'

# Pattern chapter filename → (patternId, list of 5 questions).
QUIZZES = {
    '21-sliding-window.md': ('sliding-window', [
        {
            'q': 'Which invariant characterizes a Sliding Window solution?',
            'choices': [
                { 'text': 'The array is sorted', 'correct': False, 'explanation': 'That is Binary Search.' },
                { 'text': 'A monotone-in-window-length property holds', 'correct': True, 'explanation': 'Sliding Window works when validity is monotone: once a window is valid, extending or shrinking preserves the invariant predictably.' },
                { 'text': 'The problem asks for shortest path', 'correct': False, 'explanation': 'That is BFS.' },
                { 'text': 'Recursion is used', 'correct': False, 'explanation': 'Sliding Window is iterative.' },
            ],
        },
        {
            'q': 'For "exactly k distinct" subarray count, what is the standard trick?',
            'choices': [
                { 'text': 'Sort and binary search', 'correct': False },
                { 'text': 'atMost(k) - atMost(k-1)', 'correct': True, 'explanation': 'Direct "exactly k" is hard to slide. `atMost` slides cleanly; subtract to isolate exactly-k.' },
                { 'text': 'Brute force n²', 'correct': False },
                { 'text': 'Hash map of prefixes', 'correct': False, 'explanation': 'That is Prefix Sum family.' },
            ],
        },
        {
            'q': 'Time complexity of the canonical variable-size sliding window template?',
            'choices': [
                { 'text': 'O(n²)', 'correct': False },
                { 'text': 'O(n log n)', 'correct': False },
                { 'text': 'O(n) amortized', 'correct': True, 'explanation': 'Each index enters and leaves the window at most once, so total work is 2n.' },
                { 'text': 'O(σ · n)', 'correct': False, 'explanation': 'Only if you scan the full alphabet each step; canonical uses O(1) per step.' },
            ],
        },
        {
            'q': 'Why does "lazy maxCount" work in Longest Repeating Character Replacement?',
            'choices': [
                { 'text': 'The window can only grow when a strictly-larger max appears — stale maxCount can never inflate the answer', 'correct': True, 'explanation': 'Correctness is preserved because we only accept new bests when a new real max is seen.' },
                { 'text': 'It doesn\'t work — you must recompute max every shrink', 'correct': False },
                { 'text': 'Character frequencies never decrease', 'correct': False },
                { 'text': 'Random luck', 'correct': False },
            ],
        },
        {
            'q': 'For "shortest subarray with sum ≥ k" WITH negatives, why does plain sliding fail?',
            'choices': [
                { 'text': 'Because sums are not monotone in window size once negatives are allowed', 'correct': True, 'explanation': 'Sliding requires that shrinking left strictly decreases the running metric. Negatives break that; use monotonic deque on prefix sums.' },
                { 'text': 'Because k might be too large', 'correct': False },
                { 'text': 'Because the array might be empty', 'correct': False },
                { 'text': 'Because there might be no answer', 'correct': False },
            ],
        },
    ]),

    '22-two-pointers.md': ('two-pointers', [
        {
            'q': 'What pre-condition is usually required before applying Two Pointers?',
            'choices': [
                { 'text': 'The array must be sorted (or have a monotone metric)', 'correct': True, 'explanation': 'Movements rely on knowing which side is provably suboptimal.' },
                { 'text': 'The array must be a permutation of 1..n', 'correct': False },
                { 'text': 'The array must contain only positive integers', 'correct': False },
                { 'text': 'The array size must be a power of 2', 'correct': False },
            ],
        },
        {
            'q': 'In 3Sum, how do you enforce uniqueness of triplets?',
            'choices': [
                { 'text': 'Use a HashSet of sorted triplets', 'correct': False, 'explanation': 'Works but wasteful.' },
                { 'text': 'Skip duplicates at all three levels of pointer movement', 'correct': True, 'explanation': 'Sort + skip at i, l, r ensures each triplet is emitted once.' },
                { 'text': 'Emit only the first found triplet', 'correct': False },
                { 'text': 'Duplicates are impossible after sorting', 'correct': False },
            ],
        },
        {
            'q': 'For Trapping Rain Water, why does the opposing two-pointer work with O(1) extra space?',
            'choices': [
                { 'text': 'The water at pointer p is bounded by the shorter of the two "walls seen so far"', 'correct': True, 'explanation': 'Moving the shorter side is safe because the other side\'s known max bounds it.' },
                { 'text': 'Because heights are integers', 'correct': False },
                { 'text': 'Because there is always a global maximum', 'correct': False },
                { 'text': 'It doesn\'t — you need O(n) leftMax/rightMax arrays', 'correct': False, 'explanation': 'Those work too, but 2p achieves O(1).' },
            ],
        },
        {
            'q': 'What is the complexity of the sort + two-pointer solution for 3Sum?',
            'choices': [
                { 'text': 'O(n)', 'correct': False },
                { 'text': 'O(n log n)', 'correct': False },
                { 'text': 'O(n²)', 'correct': True, 'explanation': 'Sort is O(n log n), then outer loop × inner two-pointer = O(n²), which dominates.' },
                { 'text': 'O(n³)', 'correct': False, 'explanation': 'That is the brute-force triple loop.' },
            ],
        },
        {
            'q': 'For Valid Palindrome II (delete ≤ 1 char), what is the two-pointer strategy on mismatch?',
            'choices': [
                { 'text': 'Skip the character with the higher ASCII value', 'correct': False },
                { 'text': 'Try skipping left OR skipping right; return true iff either remainder is a palindrome', 'correct': True, 'explanation': 'Two choices at the mismatch; test each; each is O(n) but only tried once.' },
                { 'text': 'Give up immediately', 'correct': False },
                { 'text': 'Recurse with k-1 deletion budget', 'correct': False, 'explanation': 'That is the k-deletion generalization.' },
            ],
        },
    ]),

    '23-fast-slow.md': ('fast-slow', [
        {
            'q': 'What does Floyd\'s Tortoise & Hare guarantee?',
            'choices': [
                { 'text': 'Cycle detection in O(1) space if a cycle exists', 'correct': True, 'explanation': 'Two pointers at different speeds always meet inside any cycle.' },
                { 'text': 'The array is sorted', 'correct': False },
                { 'text': 'Cycle length is exactly n', 'correct': False },
                { 'text': 'Constant time detection', 'correct': False, 'explanation': 'It is O(n) time; O(1) space is the win.' },
            ],
        },
        {
            'q': 'After Floyd\'s pointers meet in a cycle, how do you find the entry?',
            'choices': [
                { 'text': 'Reset one pointer to head; walk both at speed 1; they meet at entry', 'correct': True, 'explanation': 'Classic invariant: distance from head to entry = distance from meeting point to entry.' },
                { 'text': 'Sort the linked list', 'correct': False },
                { 'text': 'The meeting point is the entry', 'correct': False, 'explanation': 'It is inside the cycle but not necessarily the entry.' },
                { 'text': 'Cannot be found in O(1) space', 'correct': False },
            ],
        },
        {
            'q': 'For Middle of the Linked List with even length, how do you get the SECOND middle?',
            'choices': [
                { 'text': 'Loop while `fast != null && fast.next != null`', 'correct': True, 'explanation': 'This condition places slow at the second middle for even lengths.' },
                { 'text': 'Loop while `fast.next != null && fast.next.next != null`', 'correct': False, 'explanation': 'That gives the FIRST middle.' },
                { 'text': 'Use a queue', 'correct': False },
                { 'text': 'Two passes over the list', 'correct': False },
            ],
        },
        {
            'q': 'Find the Duplicate Number (array of n+1 ints in [1..n]) — why does Floyd\'s work?',
            'choices': [
                { 'text': '`nums[i]` treated as `next(i)` creates a functional graph; two distinct indices point to the duplicate → cycle entry = duplicate', 'correct': True, 'explanation': 'The pigeonhole guarantees a cycle; the merge-in structure guarantees the entry is the duplicate value.' },
                { 'text': 'It is a linked list already', 'correct': False },
                { 'text': 'By sort', 'correct': False, 'explanation': 'That modifies input, disallowed.' },
                { 'text': 'By XOR trick', 'correct': False, 'explanation': 'That is for missing/single, not duplicate here.' },
            ],
        },
        {
            'q': 'Which of these is NOT a Fast/Slow pattern application?',
            'choices': [
                { 'text': 'Detecting cycle in linked list', 'correct': False },
                { 'text': 'Finding middle of list', 'correct': False },
                { 'text': 'Happy Number', 'correct': False },
                { 'text': 'Longest Common Subsequence', 'correct': True, 'explanation': 'LCS is dynamic programming, not cycle detection.' },
            ],
        },
    ]),

    '24-prefix-sum.md': ('prefix-sum', [
        {
            'q': 'What does `count[preSum - k]` count in Subarray Sum Equals K?',
            'choices': [
                { 'text': 'Number of subarrays ending at current index with sum k', 'correct': True, 'explanation': 'Every earlier prefix with value `preSum - k` gives a valid subarray.' },
                { 'text': 'Total number of elements less than k', 'correct': False },
                { 'text': 'Number of prefixes divisible by k', 'correct': False },
                { 'text': 'Number of distinct values in nums', 'correct': False },
            ],
        },
        {
            'q': 'When using prefix mod k, why initialize `count[0] = 1`?',
            'choices': [
                { 'text': 'To count subarrays starting from index 0', 'correct': True, 'explanation': 'The "prefix sum before index 0" is 0; without this, subarrays sum-to-k starting at 0 are missed.' },
                { 'text': 'To handle negative numbers', 'correct': False },
                { 'text': 'It is required by Java', 'correct': False },
                { 'text': 'To avoid null exceptions', 'correct': False },
            ],
        },
        {
            'q': 'For range-add + point-query, what is the O(1)-per-add data structure?',
            'choices': [
                { 'text': 'Segment tree', 'correct': False, 'explanation': 'Works but O(log n) per op — overkill if only one final scan.' },
                { 'text': 'Difference array (then prefix sum at the end)', 'correct': True, 'explanation': 'O(1) per add; one O(n) prefix sweep to recover values.' },
                { 'text': 'Hash map', 'correct': False },
                { 'text': 'BIT / Fenwick tree', 'correct': False, 'explanation': 'Works but heavier than needed.' },
            ],
        },
        {
            'q': 'In Contiguous Array (equal 0s and 1s), what mapping enables prefix sum?',
            'choices': [
                { 'text': 'Map 0 → -1 and 1 → +1; equal counts iff prefix returns to a prior value', 'correct': True, 'explanation': 'Same prefix twice → the delta is 0 → equal 0s and 1s.' },
                { 'text': 'Sort the array', 'correct': False },
                { 'text': 'Use bitwise XOR', 'correct': False },
                { 'text': 'Impossible in O(n)', 'correct': False },
            ],
        },
        {
            'q': 'Time to answer any 2D rectangle-sum query after O(mn) preprocessing?',
            'choices': [
                { 'text': 'O(1)', 'correct': True, 'explanation': 'Inclusion-exclusion on the 2D prefix table.' },
                { 'text': 'O(log(mn))', 'correct': False },
                { 'text': 'O(m + n)', 'correct': False },
                { 'text': 'O(mn)', 'correct': False },
            ],
        },
    ]),

    '25-hashing.md': ('hashing', [
        {
            'q': 'Time complexity of Two Sum with hash map?',
            'choices': [
                { 'text': 'O(n²)', 'correct': False },
                { 'text': 'O(n log n)', 'correct': False },
                { 'text': 'O(n) average', 'correct': True, 'explanation': 'Single pass with O(1) average lookups.' },
                { 'text': 'O(1)', 'correct': False },
            ],
        },
        {
            'q': 'Why does Longest Consecutive Sequence achieve O(n) using a HashSet?',
            'choices': [
                { 'text': 'Only start counting from sequence heads (x where x-1 is absent)', 'correct': True, 'explanation': 'Each element is visited by an inner extension at most once total.' },
                { 'text': 'Because HashSet is O(1)', 'correct': False, 'explanation': 'True but insufficient — without the head check it becomes O(n²).' },
                { 'text': 'Because the input is sorted', 'correct': False, 'explanation': 'It is unsorted; that\'s the point.' },
                { 'text': 'Because we sort first', 'correct': False, 'explanation': 'Sorting would violate the O(n) spec.' },
            ],
        },
        {
            'q': 'What is the canonical-key trick for Group Anagrams?',
            'choices': [
                { 'text': 'Sort each string; use the sorted form as the hash key', 'correct': True, 'explanation': 'Anagrams share the same sorted form; O(nk log k) total.' },
                { 'text': 'Use the string itself as key', 'correct': False },
                { 'text': 'Hash all substrings', 'correct': False },
                { 'text': 'Use Trie', 'correct': False, 'explanation': 'Possible but heavier than needed.' },
            ],
        },
        {
            'q': 'For Isomorphic Strings, why do you need TWO maps (s→t and t→s)?',
            'choices': [
                { 'text': 'To forbid two source chars mapping to the same target', 'correct': True, 'explanation': 'A bijection requires uniqueness in both directions.' },
                { 'text': 'For performance', 'correct': False },
                { 'text': 'To handle Unicode', 'correct': False },
                { 'text': 'Because one map is not enough memory', 'correct': False },
            ],
        },
        {
            'q': 'What is the amortized cost of `HashMap.get()` in Java?',
            'choices': [
                { 'text': 'O(1)', 'correct': True, 'explanation': 'Amortized O(1) with a good hash function; adversarial keys can degrade to O(log n) with tree bins.' },
                { 'text': 'O(log n)', 'correct': False },
                { 'text': 'O(n)', 'correct': False },
                { 'text': 'O(σ)', 'correct': False },
            ],
        },
    ]),

    '26-monotonic-stack.md': ('monotonic-stack', [
        {
            'q': 'What is the amortized cost per element in a monotonic-stack sweep?',
            'choices': [
                { 'text': 'O(1)', 'correct': True, 'explanation': 'Each element pushed and popped at most once → 2n total operations.' },
                { 'text': 'O(log n)', 'correct': False },
                { 'text': 'O(n)', 'correct': False },
                { 'text': 'O(σ)', 'correct': False },
            ],
        },
        {
            'q': 'For "next greater element", which stack orientation do you maintain?',
            'choices': [
                { 'text': 'Monotonically decreasing from bottom to top', 'correct': True, 'explanation': 'New larger element pops smaller predecessors — those find their answer.' },
                { 'text': 'Monotonically increasing', 'correct': False, 'explanation': 'That is for "next smaller".' },
                { 'text': 'Not monotonic', 'correct': False },
                { 'text': 'Sorted at insertion', 'correct': False },
            ],
        },
        {
            'q': 'Why does Largest Rectangle in Histogram benefit from a "sentinel" bar?',
            'choices': [
                { 'text': 'A trailing height-0 flushes any remaining stack cleanly', 'correct': True, 'explanation': 'Otherwise you need special-case code after the loop.' },
                { 'text': 'To handle negative heights', 'correct': False, 'explanation': 'Heights are non-negative.' },
                { 'text': 'For randomness', 'correct': False },
                { 'text': 'To detect end-of-input', 'correct': False },
            ],
        },
        {
            'q': 'Sum of Subarray Minimums uses "contribution counting". What is the key idea?',
            'choices': [
                { 'text': 'For each element, count how many subarrays it is minimum of (L·R spans)', 'correct': True, 'explanation': 'Turn "for each subarray find min" into "for each element count contributions".' },
                { 'text': 'Sum over all subarrays', 'correct': False, 'explanation': 'That is O(n²).' },
                { 'text': 'Only iterate subarrays of length ≤ log n', 'correct': False },
                { 'text': 'Sort the array first', 'correct': False },
            ],
        },
        {
            'q': 'For Online Stock Span, what does the stack store?',
            'choices': [
                { 'text': '(price, span) pairs', 'correct': True, 'explanation': 'On next price ≥ top, pop and accumulate span.' },
                { 'text': 'Only prices', 'correct': False, 'explanation': 'Would lose the span info.' },
                { 'text': 'Only spans', 'correct': False },
                { 'text': 'All prices ever seen', 'correct': False, 'explanation': 'Would defeat the amortization.' },
            ],
        },
    ]),

    '27-binary-search.md': ('binary-search', [
        {
            'q': 'What is the danger of using `mid = (lo + hi) / 2`?',
            'choices': [
                { 'text': 'Integer overflow when lo + hi > Integer.MAX_VALUE', 'correct': True, 'explanation': 'Use `mid = lo + (hi - lo) / 2` to avoid this.' },
                { 'text': 'Off-by-one error', 'correct': False },
                { 'text': 'Nothing; it\'s always safe', 'correct': False },
                { 'text': 'It divides by zero', 'correct': False },
            ],
        },
        {
            'q': 'In Rotated Sorted Array search, how do you decide which half is sorted?',
            'choices': [
                { 'text': 'Compare `nums[mid]` with `nums[lo]` (or nums[hi])', 'correct': True, 'explanation': 'If `nums[mid] > nums[lo]`, the left half is sorted; else the right half is.' },
                { 'text': 'Always search the left half first', 'correct': False },
                { 'text': 'Random guess', 'correct': False },
                { 'text': 'Sort the array first', 'correct': False, 'explanation': 'Defeats the log n requirement.' },
            ],
        },
        {
            'q': 'For Find Peak Element, which comparison guides the BS?',
            'choices': [
                { 'text': '`nums[mid] < nums[mid+1]` → climb right; else → left', 'correct': True, 'explanation': 'A climbing side must eventually peak (nums[n] = -∞).' },
                { 'text': '`nums[mid] < nums[0]`', 'correct': False },
                { 'text': '`nums[mid] > target`', 'correct': False },
                { 'text': 'Nothing; use linear scan', 'correct': False },
            ],
        },
        {
            'q': 'Half-open BS returns `lo` after the loop. What does `lo` represent?',
            'choices': [
                { 'text': 'The lower_bound: smallest index i with nums[i] ≥ target', 'correct': True, 'explanation': 'Extensible to first-true / first-occurrence variants.' },
                { 'text': 'Always the answer', 'correct': False, 'explanation': 'Not for closed-interval BS.' },
                { 'text': 'The middle of the array', 'correct': False },
                { 'text': 'Nothing; the loop iterates forever', 'correct': False },
            ],
        },
        {
            'q': 'When can binary search NOT be applied?',
            'choices': [
                { 'text': 'When there is no monotonic property', 'correct': True, 'explanation': 'BS requires that you can eliminate half the search space each step, which needs monotonicity.' },
                { 'text': 'When n is large', 'correct': False, 'explanation': 'BS is BEST for large n.' },
                { 'text': 'When elements are integers', 'correct': False },
                { 'text': 'When there are duplicates', 'correct': False, 'explanation': 'Duplicates change some variants but not the general applicability.' },
            ],
        },
    ]),

    '28-bs-on-answer.md': ('bs-on-answer', [
        {
            'q': 'What TWO ingredients are required to apply "Binary Search on the Answer"?',
            'choices': [
                { 'text': 'A monotonic feasibility predicate + bounded answer range', 'correct': True, 'explanation': 'Without monotonicity you can\'t eliminate halves.' },
                { 'text': 'The array must be sorted', 'correct': False, 'explanation': 'The array need not be sorted.' },
                { 'text': 'The answer must be an integer', 'correct': False, 'explanation': 'It can be a real number with epsilon convergence.' },
                { 'text': 'Recursion', 'correct': False },
            ],
        },
        {
            'q': 'For Koko Eating Bananas, what is the feasibility function?',
            'choices': [
                { 'text': 'Given eating speed k, can we finish within h hours?', 'correct': True, 'explanation': 'Monotone: larger k → fewer hours required.' },
                { 'text': 'Is k the smallest pile?', 'correct': False },
                { 'text': 'Is k a divisor of h?', 'correct': False },
                { 'text': 'Is k > max(piles)?', 'correct': False },
            ],
        },
        {
            'q': 'For Split Array Largest Sum, what does `feasible(cap)` check?',
            'choices': [
                { 'text': 'Can we split into ≤ m parts each with sum ≤ cap?', 'correct': True, 'explanation': 'Larger cap → fewer parts needed.' },
                { 'text': 'Is cap ≥ max(nums)?', 'correct': False, 'explanation': 'That is the lower bound of the search, not the check.' },
                { 'text': 'Is cap divisible by m?', 'correct': False },
                { 'text': 'Nothing', 'correct': False },
            ],
        },
        {
            'q': 'What is the total complexity of BS on Answer with an O(n) feasibility check over range [lo, hi]?',
            'choices': [
                { 'text': 'O(n log(hi - lo))', 'correct': True, 'explanation': 'log iterations × O(n) per check.' },
                { 'text': 'O(n²)', 'correct': False },
                { 'text': 'O(log n)', 'correct': False },
                { 'text': 'O(hi - lo)', 'correct': False },
            ],
        },
        {
            'q': 'For real-valued BS on Answer (e.g., minimize max distance to gas station), how do you terminate?',
            'choices': [
                { 'text': 'Iterate until `hi - lo < epsilon` for some small threshold', 'correct': True, 'explanation': 'Integer BS uses `lo < hi`; real-valued uses epsilon convergence.' },
                { 'text': 'Loop 1000 times', 'correct': False, 'explanation': 'Fragile; use epsilon.' },
                { 'text': 'Never — infinite loop', 'correct': False },
                { 'text': 'Cast to int', 'correct': False },
            ],
        },
    ]),

    '29-top-k-heap.md': ('top-k-heap', [
        {
            'q': 'For "k largest", which heap type do you maintain?',
            'choices': [
                { 'text': 'Min-heap of size k', 'correct': True, 'explanation': 'Root is the smallest of the current top-k; poll if new value > root.' },
                { 'text': 'Max-heap of size k', 'correct': False, 'explanation': 'That gives k smallest.' },
                { 'text': 'Min-heap of size n', 'correct': False, 'explanation': 'Wasteful.' },
                { 'text': 'BST of size n', 'correct': False, 'explanation': 'Also works but O(n log n).' },
            ],
        },
        {
            'q': 'Time complexity of maintaining top-k over n elements with a heap?',
            'choices': [
                { 'text': 'O(n log k)', 'correct': True, 'explanation': 'Each of n insertions is O(log k) since heap size ≤ k.' },
                { 'text': 'O(n log n)', 'correct': False, 'explanation': 'That is full sorting.' },
                { 'text': 'O(k log n)', 'correct': False },
                { 'text': 'O(n + k)', 'correct': False },
            ],
        },
        {
            'q': 'For streaming k-th largest, what is the correct API pattern?',
            'choices': [
                { 'text': 'add(v): pq.offer(v); if pq.size() > k: pq.poll(); return pq.peek()', 'correct': True, 'explanation': 'Root of min-heap is the k-th largest.' },
                { 'text': 'Re-sort on every add', 'correct': False, 'explanation': 'O(n log n) per add — too slow.' },
                { 'text': 'Keep only the max', 'correct': False, 'explanation': 'Loses info.' },
                { 'text': 'Use a linked list', 'correct': False },
            ],
        },
        {
            'q': 'Quickselect vs Heap for offline top-k (order-irrelevant): which is asymptotically better on average?',
            'choices': [
                { 'text': 'Quickselect O(n) average', 'correct': True, 'explanation': 'Beats O(n log k) when k is close to n.' },
                { 'text': 'Heap O(n log k)', 'correct': False, 'explanation': 'Heap is safer worst-case but slower on average.' },
                { 'text': 'Both equal', 'correct': False },
                { 'text': 'Merge sort', 'correct': False },
            ],
        },
        {
            'q': 'For Reorganize String, why does the greedy max-heap approach work?',
            'choices': [
                { 'text': 'Always placing the most-frequent remaining character avoids getting stuck', 'correct': True, 'explanation': 'Feasibility check: max count ≤ (n+1)/2.' },
                { 'text': 'Because all letters are unique', 'correct': False },
                { 'text': 'Randomness', 'correct': False },
                { 'text': 'Because heap is fast', 'correct': False, 'explanation': 'Fast, but that\'s not why it\'s CORRECT.' },
            ],
        },
    ]),

    '30-k-way-merge.md': ('k-way-merge', [
        {
            'q': 'For merging k sorted lists into one, what is the heap-based complexity?',
            'choices': [
                { 'text': 'O(N log k) where N = total elements', 'correct': True, 'explanation': 'Heap holds one head per list; O(log k) per pop.' },
                { 'text': 'O(N log N)', 'correct': False, 'explanation': 'Full sort of merged; wastes existing sortedness.' },
                { 'text': 'O(k · N)', 'correct': False, 'explanation': 'Naive round-robin merge.' },
                { 'text': 'O(N)', 'correct': False },
            ],
        },
        {
            'q': 'For Smallest Range Covering k Lists, what does the heap track?',
            'choices': [
                { 'text': 'Current-minimum across all lists (via one pointer per list)', 'correct': True, 'explanation': 'And separately track current-max seen; range = [heapMin, currentMax].' },
                { 'text': 'All possible ranges', 'correct': False, 'explanation': 'Exponential; not needed.' },
                { 'text': 'Only the k smallest values', 'correct': False, 'explanation': 'Different problem.' },
                { 'text': 'Only the k largest values', 'correct': False },
            ],
        },
        {
            'q': 'When does K-way Merge stop for the "smallest range" problem?',
            'choices': [
                { 'text': 'When any one list is exhausted', 'correct': True, 'explanation': 'We can no longer cover that list; done.' },
                { 'text': 'When the heap is empty', 'correct': False, 'explanation': 'That is total exhaustion.' },
                { 'text': 'After N iterations', 'correct': False },
                { 'text': 'Never', 'correct': False },
            ],
        },
        {
            'q': 'For Ugly Number II, why does the 3-pointer approach beat the min-heap?',
            'choices': [
                { 'text': 'It avoids duplicates and the heap overhead — pure O(n)', 'correct': True, 'explanation': 'Three pointers into the growing ugly[] give exact sequence generation.' },
                { 'text': 'It uses less memory', 'correct': False, 'explanation': 'Same memory.' },
                { 'text': 'Heap doesn\'t work', 'correct': False, 'explanation': 'Heap works too, but slower.' },
                { 'text': 'Randomness', 'correct': False },
            ],
        },
        {
            'q': 'Merging two sorted linked lists is best done with:',
            'choices': [
                { 'text': 'Two-pointer merge with a dummy head, in-place re-linking', 'correct': True, 'explanation': 'O(m+n) time, O(1) space (nodes reused).' },
                { 'text': 'Copying to array, sorting, rebuilding', 'correct': False, 'explanation': 'Wastes existing sortedness.' },
                { 'text': 'Heap-based merge', 'correct': False, 'explanation': 'Overkill for k=2.' },
                { 'text': 'Recursion only', 'correct': False, 'explanation': 'Works but O(n) stack.' },
            ],
        },
    ]),

    '31-merge-intervals.md': ('merge-intervals', [
        {
            'q': 'Standard Merge Intervals: sort by what?',
            'choices': [
                { 'text': 'Start ascending', 'correct': True, 'explanation': 'Then walk once and merge on overlap.' },
                { 'text': 'End ascending', 'correct': False, 'explanation': 'Better for activity selection / non-overlap counting.' },
                { 'text': 'Length descending', 'correct': False },
                { 'text': 'Random', 'correct': False },
            ],
        },
        {
            'q': 'For Insert Interval into a pre-sorted list, what is the canonical algorithm?',
            'choices': [
                { 'text': 'Three-phase single pass: copy-before, merge-overlapping, copy-after', 'correct': True, 'explanation': 'O(n) time; no re-sort needed since input is sorted.' },
                { 'text': 'Insert then run full Merge Intervals', 'correct': False, 'explanation': 'Works but O(n log n).' },
                { 'text': 'Sort by end and use greedy', 'correct': False, 'explanation': 'That is Non-overlap Intervals.' },
                { 'text': 'Binary search only', 'correct': False },
            ],
        },
        {
            'q': 'For Remove Covered Intervals, what tie-break at same-start intervals?',
            'choices': [
                { 'text': 'Sort by start asc, end DESC', 'correct': True, 'explanation': 'Ensures the covering interval comes first when starts tie.' },
                { 'text': 'Sort by start asc, end asc', 'correct': False, 'explanation': 'Would mislabel the shorter one as covering.' },
                { 'text': 'No tie-break needed', 'correct': False },
                { 'text': 'Random tie-break', 'correct': False },
            ],
        },
        {
            'q': 'For Meeting Rooms (bool "can attend all"), what is the O(n log n) check?',
            'choices': [
                { 'text': 'Sort by start; verify each start ≥ previous end', 'correct': True, 'explanation': 'Adjacent-check suffices after sorting.' },
                { 'text': 'Full n² pair check', 'correct': False, 'explanation': 'Wasteful.' },
                { 'text': 'Union-Find', 'correct': False },
                { 'text': 'DP', 'correct': False },
            ],
        },
        {
            'q': 'Interval List Intersections (two sorted disjoint lists) is best solved by:',
            'choices': [
                { 'text': 'Two-pointer merge with `[max(starts), min(ends)]` intersection formula', 'correct': True, 'explanation': 'O(n+m) linear pass.' },
                { 'text': 'Sort both then binary search', 'correct': False, 'explanation': 'Already sorted; unnecessary sort.' },
                { 'text': 'Union all then re-detect overlaps', 'correct': False, 'explanation': 'Overkill.' },
                { 'text': 'Recursion', 'correct': False },
            ],
        },
    ]),

    '32-sweep-line.md': ('sweep-line', [
        {
            'q': 'What events do you emit for the classic Meeting Rooms II problem?',
            'choices': [
                { 'text': '(start, +1) and (end, -1)', 'correct': True, 'explanation': 'Sweep time; maintain running count; max is the answer.' },
                { 'text': '(start, meeting)', 'correct': False },
                { 'text': '(start, +1) only', 'correct': False },
                { 'text': 'Interval midpoints', 'correct': False },
            ],
        },
        {
            'q': 'For The Skyline Problem, what data structure processes active heights?',
            'choices': [
                { 'text': 'Max-heap (with lazy removal) or a TreeMap', 'correct': True, 'explanation': 'You need max-active at each event.' },
                { 'text': 'Min-heap', 'correct': False, 'explanation': 'You want max, not min.' },
                { 'text': 'Simple stack', 'correct': False },
                { 'text': 'Queue', 'correct': False },
            ],
        },
        {
            'q': 'In sweep events, why does the tie-break "end before start at same time" matter for Meeting Rooms II?',
            'choices': [
                { 'text': 'A meeting ending exactly when another starts doesn\'t need a new room', 'correct': True, 'explanation': 'End-first tie-break correctly reuses rooms.' },
                { 'text': 'It doesn\'t matter', 'correct': False },
                { 'text': 'For alphabetical ordering', 'correct': False },
                { 'text': 'To avoid duplicates', 'correct': False },
            ],
        },
        {
            'q': 'For My Calendar II (no triple bookings), what is a clean approach?',
            'choices': [
                { 'text': 'Track singles + doubles; on new book check doubles first', 'correct': True, 'explanation': 'Overlap with doubles = triple = reject.' },
                { 'text': 'Sort all events every book', 'correct': False, 'explanation': 'O(n log n) per book.' },
                { 'text': 'Union-Find', 'correct': False },
                { 'text': 'DFS', 'correct': False },
            ],
        },
        {
            'q': 'Sweep Line vs Difference Array: when is Sweep Line preferred?',
            'choices': [
                { 'text': 'When coordinates are unbounded / very sparse', 'correct': True, 'explanation': 'Diff arrays need contiguous integer coords; sweep works on any comparable timestamps.' },
                { 'text': 'When coordinates are 1..n dense', 'correct': False, 'explanation': 'Diff arrays are perfect there.' },
                { 'text': 'Always', 'correct': False },
                { 'text': 'Never', 'correct': False },
            ],
        },
    ]),

    '33-topological-sort.md': ('topological-sort', [
        {
            'q': 'Kahn\'s BFS toposort starts with nodes of what indeg?',
            'choices': [
                { 'text': '0', 'correct': True, 'explanation': 'No incoming edges → no prerequisites.' },
                { 'text': '1', 'correct': False },
                { 'text': 'n-1', 'correct': False },
                { 'text': 'Max indeg', 'correct': False },
            ],
        },
        {
            'q': 'How does Kahn\'s detect a cycle?',
            'choices': [
                { 'text': 'If the emitted count < n, some nodes were never freed → cycle', 'correct': True, 'explanation': 'Cycle nodes always have indeg > 0.' },
                { 'text': 'Timeout', 'correct': False },
                { 'text': 'DFS gives back-edges', 'correct': False, 'explanation': 'That is DFS-based; Kahn is BFS.' },
                { 'text': 'Impossible in linear time', 'correct': False },
            ],
        },
        {
            'q': 'For "unique topological order" check, what do you assert at every BFS step?',
            'choices': [
                { 'text': 'Queue size ≤ 1', 'correct': True, 'explanation': 'Multiple nodes with indeg 0 simultaneously = ambiguous order.' },
                { 'text': 'Queue size ≥ 1', 'correct': False },
                { 'text': 'Queue size == n', 'correct': False },
                { 'text': 'Nothing', 'correct': False },
            ],
        },
        {
            'q': 'For Minimum Height Trees, why does leaf-peeling find the center(s)?',
            'choices': [
                { 'text': 'Tree centers are the innermost nodes after successively removing leaves', 'correct': True, 'explanation': 'At most 2 remain (they are the median(s) of the longest path).' },
                { 'text': 'Random', 'correct': False },
                { 'text': 'By eccentricity computation', 'correct': False, 'explanation': 'Works but O(n²).' },
                { 'text': 'By BFS from root', 'correct': False },
            ],
        },
        {
            'q': 'Alien Dictionary: what edges are added to the precedence graph?',
            'choices': [
                { 'text': 'First differing character between two adjacent words: a[i] → b[i]', 'correct': True, 'explanation': 'That is the sole ordering signal.' },
                { 'text': 'Every char pair', 'correct': False, 'explanation': 'Would over-constrain.' },
                { 'text': 'Random pairs', 'correct': False },
                { 'text': 'Alphabet order edges', 'correct': False, 'explanation': 'Alphabet is unknown.' },
            ],
        },
    ]),

    '34-union-find.md': ('union-find', [
        {
            'q': 'What is the amortized cost of Union-Find operations with path compression + union by rank?',
            'choices': [
                { 'text': 'O(α(n)) — effectively constant', 'correct': True, 'explanation': 'α is inverse Ackermann; ≤ 4 for realistic n.' },
                { 'text': 'O(log n)', 'correct': False, 'explanation': 'Without union by rank.' },
                { 'text': 'O(n)', 'correct': False, 'explanation': 'Without compression, worst case.' },
                { 'text': 'O(1) exactly', 'correct': False, 'explanation': 'Amortized, not worst-case exact.' },
            ],
        },
        {
            'q': 'Path compression during `find(x)` — what does it do?',
            'choices': [
                { 'text': 'Reroots every node on the path directly to the tree\'s root', 'correct': True, 'explanation': 'Flattens the tree, making future finds O(1).' },
                { 'text': 'Deletes the path', 'correct': False },
                { 'text': 'Sorts the tree', 'correct': False },
                { 'text': 'Nothing', 'correct': False },
            ],
        },
        {
            'q': 'For Redundant Connection (undirected), when do you emit the answer?',
            'choices': [
                { 'text': 'The first edge whose endpoints already share a root', 'correct': True, 'explanation': 'Adding it would create a cycle.' },
                { 'text': 'The last edge', 'correct': False, 'explanation': 'Not necessarily.' },
                { 'text': 'The edge with highest weight', 'correct': False, 'explanation': 'Weights not relevant here.' },
                { 'text': 'Any edge', 'correct': False },
            ],
        },
        {
            'q': 'For Kruskal MST, when do you stop?',
            'choices': [
                { 'text': 'After picking n-1 valid edges', 'correct': True, 'explanation': 'That is the count in a spanning tree of n nodes.' },
                { 'text': 'After iterating all edges', 'correct': False, 'explanation': 'Works but wasteful.' },
                { 'text': 'When the smallest edge is > threshold', 'correct': False },
                { 'text': 'Random', 'correct': False },
            ],
        },
        {
            'q': 'For Most Stones Removed with Same Row or Column, what does #components represent?',
            'choices': [
                { 'text': 'Number of stones that must remain — removable = n - #components', 'correct': True, 'explanation': 'One stone per connected component must stay.' },
                { 'text': 'Number of rows used', 'correct': False },
                { 'text': 'Number of removable stones directly', 'correct': False, 'explanation': 'It is n - components, not components itself.' },
                { 'text': 'Nothing', 'correct': False },
            ],
        },
    ]),

    '35-greedy.md': ('greedy', [
        {
            'q': 'What is the risk of a greedy algorithm?',
            'choices': [
                { 'text': 'Local optimum may not equal global optimum', 'correct': True, 'explanation': 'Must prove correctness — usually via exchange argument.' },
                { 'text': 'It is always slow', 'correct': False, 'explanation': 'Greedy is usually fastest.' },
                { 'text': 'Uses too much memory', 'correct': False },
                { 'text': 'Doesn\'t terminate', 'correct': False },
            ],
        },
        {
            'q': 'For Jump Game (reachability), what does the greedy track?',
            'choices': [
                { 'text': 'Farthest index reachable so far', 'correct': True, 'explanation': 'If i > farthest, we\'re stuck.' },
                { 'text': 'Number of jumps used', 'correct': False, 'explanation': 'That is Jump Game II.' },
                { 'text': 'Sum of nums', 'correct': False },
                { 'text': 'Min-heap of jumps', 'correct': False },
            ],
        },
        {
            'q': 'For Course Schedule III, what makes the "regret" greedy correct?',
            'choices': [
                { 'text': 'Sort by deadline; swap out longest past-taken course when infeasible', 'correct': True, 'explanation': 'Preserves feasibility while maximizing count.' },
                { 'text': 'Sort by duration', 'correct': False, 'explanation': 'Doesn\'t enforce deadlines.' },
                { 'text': 'Random', 'correct': False },
                { 'text': 'DP', 'correct': False, 'explanation': 'Works but slower.' },
            ],
        },
        {
            'q': 'For Non-overlapping Intervals (minimum removes), sort by:',
            'choices': [
                { 'text': 'End ascending', 'correct': True, 'explanation': 'Choosing earliest end leaves maximal room — classic activity selection.' },
                { 'text': 'Start ascending', 'correct': False, 'explanation': 'That is Merge Intervals.' },
                { 'text': 'Length descending', 'correct': False },
                { 'text': 'Random', 'correct': False },
            ],
        },
        {
            'q': 'For Gas Station (circular route), what allows the O(n) reset trick?',
            'choices': [
                { 'text': 'If tank < 0 at index i, no start in [candidateStart..i] works — reset to i+1', 'correct': True, 'explanation': 'Any start ≤ i would have failed by i too.' },
                { 'text': 'Sort by cost', 'correct': False },
                { 'text': 'Total sum trick only', 'correct': False, 'explanation': 'Also needed but not the reset itself.' },
                { 'text': 'DP', 'correct': False },
            ],
        },
    ]),

    '36-backtracking.md': ('backtracking', [
        {
            'q': 'What is the key invariant of backtracking?',
            'choices': [
                { 'text': 'On return, state is restored to before the call', 'correct': True, 'explanation': 'Choose → recurse → un-choose is the discipline.' },
                { 'text': 'Global state only', 'correct': False },
                { 'text': 'No recursion allowed', 'correct': False },
                { 'text': 'Purely functional (no mutation)', 'correct': False, 'explanation': 'Mutation is fine as long as undone.' },
            ],
        },
        {
            'q': 'For Permutations II (with duplicates), how do you dedup?',
            'choices': [
                { 'text': 'Sort; skip `nums[i]` if equal to previous AND previous not used', 'correct': True, 'explanation': 'Enforces canonical duplicate order.' },
                { 'text': 'Use a HashSet of results', 'correct': False, 'explanation': 'Works but wasteful.' },
                { 'text': 'Never emit', 'correct': False },
                { 'text': 'Sort output at end', 'correct': False, 'explanation': 'Doesn\'t prevent generation.' },
            ],
        },
        {
            'q': 'For N-Queens II (count), what state accelerates the check?',
            'choices': [
                { 'text': 'Three bitmasks: cols, diag1, diag2', 'correct': True, 'explanation': '`avail = ~(cols | d1 | d2)`; each pick uses `avail & -avail`.' },
                { 'text': 'A 2D boolean board', 'correct': False, 'explanation': 'Works but slower per step.' },
                { 'text': 'A HashSet of coordinates', 'correct': False },
                { 'text': 'DP', 'correct': False },
            ],
        },
        {
            'q': 'For Sudoku Solver, what is the "MRV" heuristic?',
            'choices': [
                { 'text': 'Pick the empty cell with the fewest legal digits next', 'correct': True, 'explanation': 'Minimum Remaining Values — prunes hardest branches first.' },
                { 'text': 'Random ordering', 'correct': False },
                { 'text': 'Top-left first', 'correct': False, 'explanation': 'Works but slow on hard puzzles.' },
                { 'text': 'Left-to-right', 'correct': False },
            ],
        },
        {
            'q': 'What is a common cause of TLE in backtracking?',
            'choices': [
                { 'text': 'Missing pruning (input not sorted, no early-return check)', 'correct': True, 'explanation': 'Aggressive pruning is essential.' },
                { 'text': 'Wrong programming language', 'correct': False },
                { 'text': 'Too many comments', 'correct': False },
                { 'text': 'Using recursion', 'correct': False },
            ],
        },
    ]),

    '37-divide-conquer.md': ('divide-conquer', [
        {
            'q': 'Merge sort merges two halves in O(n). Total complexity?',
            'choices': [
                { 'text': 'O(n log n)', 'correct': True, 'explanation': 'By Master Theorem: T(n) = 2T(n/2) + O(n).' },
                { 'text': 'O(n²)', 'correct': False },
                { 'text': 'O(log n)', 'correct': False },
                { 'text': 'O(n)', 'correct': False },
            ],
        },
        {
            'q': 'For Count Inversions during merge sort, when is the count added?',
            'choices': [
                { 'text': 'When taking from the right half: add (leftRemaining) to the count', 'correct': True, 'explanation': 'Each such take crosses `leftRemaining` inversions.' },
                { 'text': 'At start of merge', 'correct': False },
                { 'text': 'At end of merge', 'correct': False, 'explanation': 'Batch-counting works too but the per-take is standard.' },
                { 'text': 'Never — count separately', 'correct': False },
            ],
        },
        {
            'q': 'For Reverse Pairs (i < j with nums[i] > 2*nums[j]), why long?',
            'choices': [
                { 'text': '2 * nums[j] can overflow int', 'correct': True, 'explanation': 'Cast to long before comparison.' },
                { 'text': 'For readability', 'correct': False },
                { 'text': 'Faster than int', 'correct': False, 'explanation': 'Usually slower.' },
                { 'text': 'Not needed', 'correct': False, 'explanation': 'Overflow bug otherwise.' },
            ],
        },
        {
            'q': 'For Sort List (linked list mergesort), how do you split in O(1) space?',
            'choices': [
                { 'text': 'Fast/slow pointers to find middle; cut the link', 'correct': True, 'explanation': 'Middle split via fast/slow, then merge.' },
                { 'text': 'Copy to array', 'correct': False, 'explanation': 'O(n) space.' },
                { 'text': 'Random split', 'correct': False },
                { 'text': 'Not possible', 'correct': False },
            ],
        },
        {
            'q': 'When would you NOT use divide & conquer?',
            'choices': [
                { 'text': 'When the subproblems aren\'t independent (need shared state)', 'correct': True, 'explanation': 'Then DP or shared-memoization is better.' },
                { 'text': 'When n is large', 'correct': False, 'explanation': 'D&C shines for large n.' },
                { 'text': 'When recursion is banned', 'correct': False, 'explanation': 'You can iterate; possible but ugly.' },
                { 'text': 'Never — always use D&C', 'correct': False },
            ],
        },
    ]),

    '38-dp.md': ('dp', [
        {
            'q': 'What are the FOUR components of a DP formulation?',
            'choices': [
                { 'text': 'State, Transition, Base case, Order', 'correct': True, 'explanation': 'Miss any one and the DP doesn\'t work.' },
                { 'text': 'Array, Loop, If, Return', 'correct': False },
                { 'text': 'Sort, Search, Store', 'correct': False },
                { 'text': 'Just recursion', 'correct': False },
            ],
        },
        {
            'q': 'For 0/1 knapsack DP, why iterate weight DESCENDING?',
            'choices': [
                { 'text': 'To prevent using the same item twice in one iteration', 'correct': True, 'explanation': 'Ascending order would let item[i] extend a state that already included item[i].' },
                { 'text': 'For cache efficiency', 'correct': False },
                { 'text': 'To handle negative weights', 'correct': False },
                { 'text': 'It doesn\'t matter', 'correct': False },
            ],
        },
        {
            'q': 'Coin Change II: count unordered combinations. What is the loop order?',
            'choices': [
                { 'text': 'Outer: coins; Inner: amount', 'correct': True, 'explanation': 'Fixes coin usage order → unordered.' },
                { 'text': 'Outer: amount; Inner: coins', 'correct': False, 'explanation': 'That counts ordered sequences (Combination Sum IV).' },
                { 'text': 'Random', 'correct': False },
                { 'text': 'Nested both', 'correct': False },
            ],
        },
        {
            'q': 'For Burst Balloons, why does "last to burst" (not "first") work?',
            'choices': [
                { 'text': 'The last one\'s neighbors are fixed at the sub-range boundaries', 'correct': True, 'explanation': 'This isolates subproblems into independent intervals.' },
                { 'text': 'Random', 'correct': False },
                { 'text': 'For symmetry', 'correct': False },
                { 'text': 'It doesn\'t work; must use first', 'correct': False, 'explanation': 'First fails — this is the trick.' },
            ],
        },
        {
            'q': 'For Best Time to Buy/Sell Stock IV (k transactions), when does k allow unlimited?',
            'choices': [
                { 'text': 'When k ≥ n/2', 'correct': True, 'explanation': 'You can capture every increasing step → sum of positive diffs.' },
                { 'text': 'k = n', 'correct': False },
                { 'text': 'k = 1', 'correct': False, 'explanation': 'Then O(n) single-tx algorithm.' },
                { 'text': 'Never', 'correct': False },
            ],
        },
    ]),

    '39-trie-pattern.md': ('trie', [
        {
            'q': 'What is the space complexity of a trie storing N words of avg length L over alphabet σ?',
            'choices': [
                { 'text': 'O(N · L · σ) worst case', 'correct': True, 'explanation': 'Each node has ≤ σ child pointers; N·L nodes total.' },
                { 'text': 'O(N)', 'correct': False },
                { 'text': 'O(L)', 'correct': False },
                { 'text': 'O(σ)', 'correct': False },
            ],
        },
        {
            'q': 'Search in a trie for a word of length L costs:',
            'choices': [
                { 'text': 'O(L)', 'correct': True, 'explanation': 'One step per character, regardless of N.' },
                { 'text': 'O(N)', 'correct': False },
                { 'text': 'O(N · L)', 'correct': False },
                { 'text': 'O(σ · L)', 'correct': False, 'explanation': 'Only if scanning all children each step.' },
            ],
        },
        {
            'q': 'For Word Search II, why is Trie + DFS faster than DFS-per-word?',
            'choices': [
                { 'text': 'Shared prefix traversal — each grid cell visits the trie at most O(σ) times', 'correct': True, 'explanation': 'Grid DFS + trie fusion avoids repeated prefix work.' },
                { 'text': 'Sorting', 'correct': False },
                { 'text': 'Randomization', 'correct': False },
                { 'text': 'Not faster', 'correct': False },
            ],
        },
        {
            'q': 'For Stream of Characters (last-suffix match), what modification to the standard trie?',
            'choices': [
                { 'text': 'Insert each dictionary word REVERSED', 'correct': True, 'explanation': 'Then walk backward through the stream — matches end at the newest char.' },
                { 'text': 'Store hash of suffixes', 'correct': False },
                { 'text': 'Use two tries', 'correct': False },
                { 'text': 'Never possible in O(L)', 'correct': False },
            ],
        },
        {
            'q': 'For Maximum XOR Between Numbers, what tree do you build?',
            'choices': [
                { 'text': 'Binary trie of the numbers (bit-by-bit)', 'correct': True, 'explanation': 'Walk from MSB, greedily choosing the opposite bit.' },
                { 'text': 'BST', 'correct': False },
                { 'text': 'Character trie', 'correct': False },
                { 'text': 'Heap', 'correct': False },
            ],
        },
    ]),

    '40-bit-manip.md': ('bit-manip', [
        {
            'q': 'What does `n & (n-1)` do?',
            'choices': [
                { 'text': 'Clears the lowest set bit', 'correct': True, 'explanation': 'Foundation for Kernighan\'s popcount and power-of-2 tests.' },
                { 'text': 'Sets the lowest bit', 'correct': False },
                { 'text': 'Flips all bits', 'correct': False },
                { 'text': 'Nothing', 'correct': False },
            ],
        },
        {
            'q': 'How do you test if n is a power of 2?',
            'choices': [
                { 'text': 'n > 0 && (n & (n-1)) == 0', 'correct': True, 'explanation': 'Exactly one bit set.' },
                { 'text': 'n % 2 == 0', 'correct': False, 'explanation': 'Even, not power of 2.' },
                { 'text': 'n / 2 == 0', 'correct': False },
                { 'text': 'log2(n) is integer', 'correct': False, 'explanation': 'Works but FP-risky.' },
            ],
        },
        {
            'q': 'XOR of all numbers 0..n missing exactly one equals:',
            'choices': [
                { 'text': 'The missing number', 'correct': True, 'explanation': 'Pairs cancel; missing survives.' },
                { 'text': '0', 'correct': False },
                { 'text': 'n', 'correct': False },
                { 'text': 'Sum(0..n) - sum(nums)', 'correct': False, 'explanation': 'That is Gauss sum, works too but overflow risk.' },
            ],
        },
        {
            'q': 'For subset enumeration on n ≤ 20 items, what pattern is used?',
            'choices': [
                { 'text': 'Iterate mask 0..(1<<n)-1; bit i set means item i chosen', 'correct': True, 'explanation': 'Bitmask enumeration; often paired with DP.' },
                { 'text': 'Recursion only', 'correct': False, 'explanation': 'Works but slower.' },
                { 'text': 'Sort', 'correct': False },
                { 'text': 'HashSet', 'correct': False },
            ],
        },
        {
            'q': 'For Maximum Product of Word Lengths, how do you check "no shared letter" in O(1)?',
            'choices': [
                { 'text': '26-bit mask per word; `mask[i] & mask[j] == 0`', 'correct': True, 'explanation': 'Single AND is O(1) regardless of word length.' },
                { 'text': 'Iterate every character', 'correct': False, 'explanation': 'O(L) per pair.' },
                { 'text': 'HashSet intersection', 'correct': False, 'explanation': 'Works but slower.' },
                { 'text': 'Sort both words', 'correct': False },
            ],
        },
    ]),

    '41-quickselect.md': ('quickselect', [
        {
            'q': 'Average complexity of Quickselect for k-th element?',
            'choices': [
                { 'text': 'O(n)', 'correct': True, 'explanation': 'Each partition eliminates a constant fraction of remaining candidates on average.' },
                { 'text': 'O(n log n)', 'correct': False, 'explanation': 'That is full quicksort.' },
                { 'text': 'O(log n)', 'correct': False },
                { 'text': 'O(k)', 'correct': False },
            ],
        },
        {
            'q': 'Worst-case complexity of Quickselect (without randomization)?',
            'choices': [
                { 'text': 'O(n²)', 'correct': True, 'explanation': 'On adversarial inputs / sorted-with-first-pivot.' },
                { 'text': 'O(n log n)', 'correct': False },
                { 'text': 'O(n)', 'correct': False, 'explanation': 'Only with median-of-medians pivot.' },
                { 'text': 'O(log n)', 'correct': False },
            ],
        },
        {
            'q': 'For k-th LARGEST via Quickselect, how do you compute the index?',
            'choices': [
                { 'text': 'Look for index n - k in ascending-sorted order', 'correct': True, 'explanation': 'k-th largest = element at position n-k when sorted ascending.' },
                { 'text': 'Look for index k', 'correct': False, 'explanation': 'That is k-th smallest.' },
                { 'text': 'Random', 'correct': False },
                { 'text': 'Nothing; use max-heap', 'correct': False, 'explanation': 'Works but heavier.' },
            ],
        },
        {
            'q': 'What is Wiggle Sort II\'s O(n) trick using Quickselect?',
            'choices': [
                { 'text': 'Quickselect median, then Dutch flag partition using virtual index mapping', 'correct': True, 'explanation': 'Virtual index `(2i+1) % (n|1)` interleaves ranks correctly.' },
                { 'text': 'Just sort', 'correct': False, 'explanation': 'That is O(n log n).' },
                { 'text': 'Random shuffle', 'correct': False },
                { 'text': 'BFS', 'correct': False },
            ],
        },
        {
            'q': 'What guarantees Quickselect terminates?',
            'choices': [
                { 'text': 'The partition strictly reduces the search size by at least 1 each step', 'correct': True, 'explanation': 'The pivot itself is placed correctly and excluded.' },
                { 'text': 'Random luck', 'correct': False },
                { 'text': 'Recursion depth bound', 'correct': False },
                { 'text': 'Sorted input', 'correct': False },
            ],
        },
    ]),
}


def to_quiz_block(pattern_id: str, questions: list) -> str:
    """Build the Vue Quiz component block."""
    # Build JS array of questions using single-quoted attribute syntax
    import json
    q_json = json.dumps(questions, ensure_ascii=False)
    # Escape single quotes in the JSON so it fits in a single-quoted attribute
    q_attr = q_json.replace("'", "\u2019")
    return f'''## Check your understanding

<Quiz
  pattern-id="{pattern_id}"
  :questions='{q_attr}'
/>

'''


def append_quiz(path: Path, pattern_id: str, questions: list) -> bool:
    """Replace any existing <Quiz>...</Quiz> block (or "## Check your understanding" section) with the new one."""
    import re as _re
    text = path.read_text(encoding='utf-8')
    new_block = to_quiz_block(pattern_id, questions)
    # Strategy: find the FIRST occurrence of "<Quiz" and remove from that point to end of the Quiz self-closing tag
    quiz_match = _re.search(r'^## Check your understanding\s*$', text, _re.MULTILINE)
    if quiz_match:
        # Remove everything from "## Check your understanding" to end of file
        text = text[:quiz_match.start()].rstrip() + '\n\n'
    elif '<Quiz' in text:
        # No H2 wrapping; find and remove just the Quiz tag
        m = _re.search(r'<Quiz[^>]*?/>|<Quiz.*?</Quiz>', text, _re.DOTALL)
        if m:
            text = text[:m.start()].rstrip() + '\n\n' + text[m.end():].lstrip()
    text = text.rstrip() + '\n\n' + new_block.rstrip() + '\n'
    path.write_text(text, encoding='utf-8')
    return True


def main():
    changed = 0
    for name, (pid, qs) in QUIZZES.items():
        p = SRC / name
        if not p.exists():
            print(f'  ! MISSING: {name}')
            continue
        if append_quiz(p, pid, qs):
            changed += 1
            print(f'  + {name} ({len(qs)} Q)')
    print(f'\nAdded quizzes to {changed}/{len(QUIZZES)} pattern chapters.')


if __name__ == '__main__':
    main()
