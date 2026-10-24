<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { withBase } from 'vitepress'
import { storage } from './lib/storage'

/*
 * DiagnosticQuiz
 *
 * A 60-question self-diagnostic covering the 12 topic clusters that make
 * up the interview-DSA surface. Honest answers in → a weakness-vector
 * out, with a prioritised "start here" list that links into /map.
 *
 * Scoring design choice: a cluster is marked WEAK if the user got
 * < 60 % right, OK if 60–79 %, STRONG if ≥ 80 %. These thresholds
 * come from "below 60 % is coin-flip territory; above 80 % you can
 * reasonably skip the chapter and skim the templates."
 *
 * Persistence: the latest full result (per-cluster score vector + raw
 * answers) is stored in localStorage under `dsa-diagnostic:latest` via
 * the shared `storage` helper. We never write anything until the user
 * actually reaches the results screen (no half-completed state).
 */

type Cluster =
  | 'complexity'
  | 'arrays-hashing'
  | 'strings-prefix'
  | 'two-ptr-window'
  | 'binary-search'
  | 'stacks-mono'
  | 'trees'
  | 'heaps-topk'
  | 'graphs'
  | 'backtracking'
  | 'dp'
  | 'design-math'

interface Question {
  cluster: Cluster
  q: string
  choices: string[]
  correct: number       // index into choices
  why: string           // one-sentence explanation shown with the answer
  link?: string         // optional deeper-dive chapter
}

const CLUSTER_LABELS: Record<Cluster, string> = {
  'complexity':      'Complexity',
  'arrays-hashing':  'Arrays & Hashing',
  'strings-prefix':  'Strings & Prefix Sum',
  'two-ptr-window':  'Two Pointers & Sliding Window',
  'binary-search':   'Binary Search',
  'stacks-mono':     'Stacks & Monotonic',
  'trees':           'Trees',
  'heaps-topk':      'Heaps, Top-K, K-way Merge',
  'graphs':          'Graphs',
  'backtracking':    'Backtracking',
  'dp':              'Dynamic Programming',
  'design-math':     'Design, Bit & Math',
}

const CLUSTER_CHAPTER: Record<Cluster, string> = {
  'complexity':      '/foundations/complexity',
  'arrays-hashing':  '/data-structures/arrays',
  'strings-prefix':  '/data-structures/strings',
  'two-ptr-window':  '/patterns/two-pointers',
  'binary-search':   '/patterns/binary-search',
  'stacks-mono':     '/patterns/monotonic-stack',
  'trees':           '/data-structures/trees',
  'heaps-topk':      '/patterns/top-k-heap',
  'graphs':          '/data-structures/graphs',
  'backtracking':    '/patterns/backtracking',
  'dp':              '/patterns/dp',
  'design-math':     '/patterns/design',
}

const QS: Question[] = [
  // --- C1: complexity ---
  { cluster: 'complexity', q: 'What is the amortized cost of HashMap.put, and its worst case?',
    choices: ['O(1) / O(1)', 'O(1) / O(n)', 'O(log n) / O(n)', 'O(n) / O(n²)'],
    correct: 1,
    why: 'Amortised O(1) across resizes; worst-case O(n) when every key collides into one bucket (Java 17 switches to a tree for long chains, reducing worst case to O(log n), but older/pre-treeify codebases are still cited as O(n)).' },
  { cluster: 'complexity', q: 'For n = 10⁵, which of these complexities does NOT comfortably fit under one second?',
    choices: ['O(n log n)', 'O(n √n)', 'O(n²)', 'O(n)'],
    correct: 2,
    why: 'n² at n = 10⁵ is 10¹⁰ ops — roughly 100 seconds on a modern CPU. The others all come in under 1 s.' },
  { cluster: 'complexity', q: 'A recursive function recurses n deep in Java (no tail-call optimisation). Space complexity?',
    choices: ['O(1)', 'O(log n)', 'O(n)', 'O(n²)'],
    correct: 2,
    why: 'Each call keeps its frame on the JVM stack; Java does not do TCO, so n frames = O(n) space.' },
  { cluster: 'complexity', q: 'Rank from slowest to fastest growth: n², n log n, n √n, n log log n.',
    choices: [
      'n² > n √n > n log n > n log log n',
      'n² > n log n > n √n > n log log n',
      'n √n > n² > n log n > n log log n',
      'n² > n log log n > n √n > n log n',
    ], correct: 0,
    why: 'For large n: n² (10¹⁰) > n √n (≈3·10⁷) > n log n (≈1.7·10⁶) > n log log n (≈4·10⁵).' },
  { cluster: 'complexity', q: 'Which is NOT a safe simplification?',
    choices: [
      'O(n) + O(n log n) = O(n log n)',
      'O(2ⁿ) + O(n⁵) = O(2ⁿ)',
      'O(n²) + O(n²) = O(n²)',
      'O(log n²) = O(n log n)',
    ], correct: 3,
    why: 'log(n²) = 2 log n = O(log n), NOT O(n log n). Classic error.' },

  // --- C2: arrays-hashing ---
  { cluster: 'arrays-hashing', q: 'HashMap.get(k) returns null if the key is absent. What is the most common bug this creates?',
    choices: [
      'NullPointerException when auto-unboxing to a primitive',
      'ClassCastException',
      'ConcurrentModificationException',
      'ArrayIndexOutOfBoundsException',
    ], correct: 0,
    why: 'map.getOrDefault(k, 0) or map.get(k) == null guards are the right fix — a direct int x = map.get(k) throws NPE on absent keys.' },
  { cluster: 'arrays-hashing', q: 'For "find any pair in an unsorted array that sums to target", the fastest single-pass solution uses…',
    choices: ['Sort + two pointers', 'HashSet (seen so far)', 'Nested loops', 'Sort + binary search'],
    correct: 1,
    why: 'HashSet in a single pass gives O(n) time, O(n) space with no sort cost. Two-pointers requires sort → O(n log n).' },
  { cluster: 'arrays-hashing', q: 'LinkedHashMap preserves insertion order. Which problem is the single best fit for it?',
    choices: ['Two Sum', 'LRU Cache', 'Group Anagrams', 'Longest Consecutive Sequence'],
    correct: 1,
    why: 'LRU needs O(1) get/put plus access-order enumeration — exactly what LinkedHashMap (with accessOrder=true) gives you for free.' },
  { cluster: 'arrays-hashing', q: 'To "count occurrences of each element", which is cleanest in Java?',
    choices: ['Nested loops with counter', 'map.merge(k, 1, Integer::sum)', 'HashSet with resize-on-collision', 'Arrays.sort then scan'],
    correct: 1,
    why: 'merge is designed for exactly this — atomic read-modify-write with a default, no null handling needed.' },
  { cluster: 'arrays-hashing', q: 'For a 10⁶-element array, "find any element with majority (> n/2 count)" has an O(n) time, O(1) space algorithm. Its name?',
    choices: ['Floyd cycle detection', 'Boyer-Moore majority vote', 'Kadane\'s algorithm', 'Dutch National Flag'],
    correct: 1,
    why: 'Boyer-Moore keeps one candidate + one count; the majority element (if it exists) survives.' },

  // --- C3: strings-prefix ---
  { cluster: 'strings-prefix', q: '"Count subarrays with sum = k, nums may be negative." Which pattern wins?',
    choices: ['Sliding window', 'Prefix sum + hashmap', 'Two pointers', 'Divide & conquer'],
    correct: 1,
    why: 'Negative values break sliding window monotonicity. Prefix sum + hashmap gives O(n) by counting how many earlier prefix sums equal (currentSum − k).' },
  { cluster: 'strings-prefix', q: 'For "longest palindromic substring, n ≤ 1000", the two canonical approaches are "expand around center" and "Manacher". Both reach what time?',
    choices: ['O(n³) and O(n²)', 'O(n²) and O(n)', 'O(n²) and O(n log n)', 'O(n log n) and O(n)'],
    correct: 1,
    why: 'Expand-around-center is O(n²); Manacher reduces to O(n) by reusing palindrome information.' },
  { cluster: 'strings-prefix', q: 'prefix[r+1] − prefix[l] gives you the sum of…',
    choices: ['Elements at indices l to r−1', 'Elements at indices l to r inclusive', 'Elements at indices l+1 to r', 'Elements at indices l to r+1'],
    correct: 1,
    why: 'Standard convention: prefix[0] = 0, prefix[i] = sum of first i elements. Then prefix[r+1] − prefix[l] = elements l..r inclusive.' },
  { cluster: 'strings-prefix', q: 'Rabin-Karp rolling hash: the biggest trap is…',
    choices: [
      'Overflow during the hash update',
      'Hash collisions requiring verification',
      'Case sensitivity',
      'Unicode normalization',
    ], correct: 1,
    why: 'A hash match does NOT guarantee an actual match. You MUST compare the strings on a hash hit, or you ship a bug.' },
  { cluster: 'strings-prefix', q: 'To check if two strings are rotations of each other (e.g. "waterbottle" and "erbottlewat"), the one-liner is…',
    choices: [
      '(s1 + s1).contains(s2) with length check',
      'sort both and compare',
      'XOR the characters',
      's1.equals(new StringBuilder(s2).reverse().toString())',
    ], correct: 0,
    why: 'Every rotation of s1 appears as a substring of s1+s1. One contains() call, O(n) with the right matcher.' },

  // --- C4: two-ptr-window ---
  { cluster: 'two-ptr-window', q: 'Sorted array, find a pair summing to target. The right algorithm?',
    choices: ['Hash set', 'Two pointers from both ends', 'Binary search for complement', 'Nested loop'],
    correct: 1,
    why: 'Sorted + find pair → opposite-end two pointers in O(n), O(1) extra space. Hash set works but wastes the sort.' },
  { cluster: 'two-ptr-window', q: '"Longest substring with at most K distinct characters." Which pattern?',
    choices: ['Two pointers (opposite ends)', 'Sliding window with hashmap', 'Prefix sum + hashmap', 'Monotonic deque'],
    correct: 1,
    why: 'Classic sliding window: expand right, shrink left while map.size() > K, track the max window length.' },
  { cluster: 'two-ptr-window', q: 'Sliding window FAILS on "longest subarray with sum ≥ k" when values can be negative. Why?',
    choices: [
      'Negative values break monotonicity of the window sum',
      'Window sum can overflow',
      'Hashmaps don\'t support negatives',
      'The window never shrinks correctly',
    ], correct: 0,
    why: 'Window sum is no longer monotone when values can be negative — shrinking the window might INCREASE the sum. Sliding window loses the "when invalid, shrink to make valid" guarantee.' },
  { cluster: 'two-ptr-window', q: 'Dutch National Flag (3-way partition using lo/mid/hi): when a[mid] == 2, you swap and…',
    choices: ['Advance mid', 'Advance hi only (don\'t advance mid)', 'Reset lo = mid', 'Advance both mid and hi'],
    correct: 1,
    why: 'The swapped-in value from hi is unknown — must re-examine it. Only hi−−.' },
  { cluster: 'two-ptr-window', q: '"Minimum window substring (contains all chars of T)" — what makes it harder than fixed-size sliding window?',
    choices: [
      'Window length is variable and condition is "contains",not "sum"',
      'Requires sorting first',
      'Doesn\'t fit in O(n)',
      'Needs a priority queue',
    ], correct: 0,
    why: 'Both bounds move independently and the validity predicate is a multiset-coverage check, not a single comparator. Still O(n) with a frequency hashmap + a "matched" counter.' },

  // --- C5: binary-search ---
  { cluster: 'binary-search', q: 'mid = (lo + hi) / 2 has what bug, and the fix?',
    choices: [
      'Division by zero; use (lo + hi) >> 1',
      'Integer overflow; use lo + (hi − lo) / 2',
      'Rounding error; cast to double',
      'None, it is correct',
    ], correct: 1,
    why: 'If lo + hi > Integer.MAX_VALUE, you wrap to a negative mid. Famous JDK bug fixed by Google in 2006.' },
  { cluster: 'binary-search', q: 'For "find the smallest value v such that P(v) is true" using parametric binary search, which bound convention has the fewest off-by-ones?',
    choices: [
      '[lo, hi] closed',
      '[lo, hi) half-open (lo inclusive, hi exclusive)',
      '(lo, hi) open',
      '(lo, hi] half-open',
    ], correct: 1,
    why: 'Half-open [lo, hi) with answer = lo at termination is the convention that reads most cleanly and has the simplest proof.' },
  { cluster: 'binary-search', q: '"Minimum eating speed K to finish all bananas in H hours." Which pattern?',
    choices: ['Sliding window', 'Binary search on answer', 'Greedy', 'DP'],
    correct: 1,
    why: 'The feasibility predicate "can finish at speed K" is monotone in K — classic BS-on-answer. Search space is [1, max(piles)].' },
  { cluster: 'binary-search', q: 'Binary search on a rotated sorted array needs what extra check per iteration?',
    choices: [
      'Which half is monotonically sorted',
      'Whether the midpoint equals the pivot',
      'Whether lo == 0',
      'The parity of the array length',
    ], correct: 0,
    why: 'Compare a[lo] with a[mid]: one half is sorted. Check if target lies in the sorted half, then recurse accordingly.' },
  { cluster: 'binary-search', q: 'Binary search\'s O(log n) breaks when…',
    choices: [
      'Array access is not O(1) (e.g. on a linked list)',
      'The array contains duplicates',
      'The search target is at the midpoint',
      'The array is large',
    ], correct: 0,
    why: 'Linked list traversal to index is O(n), killing the log-factor speedup. Binary search is for random-access structures.' },

  // --- C6: stacks-mono ---
  { cluster: 'stacks-mono', q: 'In modern Java, prefer ArrayDeque over Stack because…',
    choices: [
      'Stack is deprecated',
      'Stack extends Vector and is synchronized (slower, legacy)',
      'ArrayDeque has more methods',
      'Stack lacks peek()',
    ], correct: 1,
    why: 'Stack inherits Vector\'s synchronisation. ArrayDeque is faster, idiomatic, and the official recommendation.' },
  { cluster: 'stacks-mono', q: '"Next greater element to the right" family of problems — the right data structure?',
    choices: ['BST', 'Priority queue', 'Monotonic (decreasing) stack', 'Hashmap'],
    correct: 2,
    why: 'A monotonic decreasing stack: pop until the top is greater than current; the top (or absent) is the next greater element.' },
  { cluster: 'stacks-mono', q: '"Largest rectangle in histogram" — what invariant does the monotonic stack maintain?',
    choices: [
      'Indices of heights in strictly increasing order',
      'Heights only; indices irrelevant',
      'Indices in decreasing order',
      'Pairs (height, count)',
    ], correct: 0,
    why: 'Stack holds indices whose heights are strictly increasing. When current is lower, pop and compute area with the just-popped bar as the limiting height.' },
  { cluster: 'stacks-mono', q: 'Monotonic stack vs monotonic deque — the deque is used when…',
    choices: [
      'You need the max/min of a sliding window of fixed size',
      'You need O(1) random access',
      'You need to process elements in reverse',
      'Memory is scarce',
    ], correct: 0,
    why: 'The deque permits removal from BOTH ends — pop stale indices from the front, maintain monotonicity by popping from the back. Perfect for "max in window of size K".' },
  { cluster: 'stacks-mono', q: 'For "longest valid parentheses substring", a stack-based solution pushes…',
    choices: [
      'The character \'(\'',
      'Indices (never the characters)',
      'Pairs (index, char)',
      'Only matched pairs',
    ], correct: 1,
    why: 'Push indices. On \')\' pop; if stack empty, push current index as new base. Max distance between top-of-stack and current = longest valid run ending here.' },

  // --- C7: trees ---
  { cluster: 'trees', q: 'BST operations are O(log n) on average but O(?) in the worst case, when?',
    choices: [
      'O(n), when the tree degenerates into a linked list (sorted inserts)',
      'O(n log n), with alternating inserts',
      'O(√n), with balanced inserts',
      'O(log² n), always',
    ], correct: 0,
    why: 'An unbalanced BST (e.g. inserting a sorted sequence) becomes a linked list — height = n, every operation O(n). Use a self-balancing BST (TreeMap) in Java to guarantee O(log n).' },
  { cluster: 'trees', q: 'Which traversal visits BST nodes in SORTED order?',
    choices: ['Preorder', 'Inorder', 'Postorder', 'Level-order'],
    correct: 1,
    why: 'Inorder (left, node, right) on a BST yields values in ascending order. This is the defining property.' },
  { cluster: 'trees', q: '"Lowest common ancestor of nodes p and q in a binary tree" — the recursion returns…',
    choices: [
      'The depth of the LCA',
      'A boolean: "found in subtree?"',
      'The LCA node when both p and q are found below; else propagates whichever was found',
      'A list of all ancestors',
    ], correct: 2,
    why: 'Classic shape: if either side returns non-null for both p and q, the current node IS the LCA; otherwise bubble up whichever one you found.' },
  { cluster: 'trees', q: 'For serialize/deserialize of a BT, the standard trap is…',
    choices: [
      'Null children get skipped, making the tree unreconstructable',
      'Int values overflow',
      'Recursion depth',
      'Hashing collisions',
    ], correct: 0,
    why: 'Nulls MUST be emitted (e.g. as "#") during serialize, otherwise shape is lost and deserialize can\'t distinguish "1,2" from "1,null,2".' },
  { cluster: 'trees', q: '"Diameter of a binary tree": at each node, the diameter candidate is max(left_depth + right_depth + 1). Why +1?',
    choices: [
      'To include the current node in the path count',
      'To avoid off-by-one on empty trees',
      'Historical convention',
      'It\'s not needed; +0 is correct',
    ], correct: 0,
    why: 'If "diameter" counts nodes on the path (not edges), the current node is one of them. Some problem variants count edges — then it is left_depth + right_depth (no +1).' },

  // --- C8: heaps-topk ---
  { cluster: 'heaps-topk', q: '"Top K frequent elements, n = 10⁶, K ≤ 10". Fastest?',
    choices: [
      'Sort by frequency O(n log n)',
      'Heap of size K: O(n log K)',
      'Quickselect: O(n) average',
      'Bucket by frequency: O(n)',
    ], correct: 3,
    why: 'Frequency ≤ n, so bucket[freq] = list — O(n) worst-case. Quickselect gives O(n) average but worst O(n²). Heap of size K is O(n log K), fine but strictly worse than buckets for this constraint.' },
  { cluster: 'heaps-topk', q: 'The heap-of-size-K streaming pattern (offer+poll) beats sort-and-take because…',
    choices: [
      'It works on infinite streams; sort does not',
      'It is cache-friendlier',
      'It uses less memory even for finite inputs',
      'Both can run concurrently',
    ], correct: 0,
    why: 'Sort needs the whole input in memory. Heap-of-K keeps only K elements, so it fits in RAM for arbitrarily long streams.' },
  { cluster: 'heaps-topk', q: '"Find median from a data stream" — the right structure?',
    choices: [
      'Single sorted ArrayList (insertion sort)',
      'Two heaps: max-heap of lower half, min-heap of upper half',
      'TreeSet',
      'HashMap of counts',
    ], correct: 1,
    why: 'Two balanced heaps give O(log n) insert and O(1) median: top of max-heap (odd total) or average of both tops (even total).' },
  { cluster: 'heaps-topk', q: '"Merge K sorted lists of total N elements". Complexity with a min-heap of size K?',
    choices: ['O(N)', 'O(N log K)', 'O(N²)', 'O(N × K)'],
    correct: 1,
    why: 'Each of N elements enters and exits the K-sized heap once; each op is O(log K).' },
  { cluster: 'heaps-topk', q: 'Java PriorityQueue comparator (a, b) -> a - b has what bug?',
    choices: [
      'None, it\'s idiomatic',
      'Overflow when a < 0 and b > 0, giving wrong order',
      'Breaks when values are equal',
      'Only works on primitive int, not Integer',
    ], correct: 1,
    why: 'For a = Integer.MIN_VALUE and b positive, a − b overflows to a positive number — wrong order. Use Integer.compare(a, b).' },

  // --- C9: graphs ---
  { cluster: 'graphs', q: 'Shortest path in an UNWEIGHTED graph — algorithm?',
    choices: ['Dijkstra', 'BFS from the source', 'DFS with pruning', 'Bellman-Ford'],
    correct: 1,
    why: 'BFS explores by layers; the first time we reach a node, that layer IS the shortest edge-count distance. O(V + E).' },
  { cluster: 'graphs', q: '"Course Schedule II (ordering)." What signals a cycle in Kahn\'s algorithm?',
    choices: [
      'An unvisited node remains at the end',
      'The queue becomes empty before all nodes are output',
      'Negative edge weights',
      'An edge pointing to the source',
    ], correct: 1,
    why: 'If after processing all queued zero-in-degree nodes, output size < V, remaining nodes are on a cycle. Return [] / false.' },
  { cluster: 'graphs', q: 'Union-Find with path compression + union by rank — amortised complexity per op?',
    choices: ['O(log n)', 'O(1)', 'O(α(n)), effectively constant', 'O(log* n)'],
    correct: 2,
    why: 'Tarjan 1975 proved α(n) (the inverse Ackermann) amortised bound. For any practical n, α(n) ≤ 4.' },
  { cluster: 'graphs', q: 'Dijkstra fails when the graph has…',
    choices: [
      'Cycles',
      'Disconnected components',
      'Negative edge weights',
      'Multiple edges between the same pair',
    ], correct: 2,
    why: 'Dijkstra\'s greedy "settle the current closest node forever" assumes no negative edges can shorten the path later. Use Bellman-Ford instead.' },
  { cluster: 'graphs', q: '"Number of islands in a grid." Which approach is INCORRECT?',
    choices: ['DFS flood fill', 'BFS flood fill', 'Union-Find', 'Binary search'],
    correct: 3,
    why: 'Binary search needs a monotone/orderable space — grid connectivity has neither.' },

  // --- C10: backtracking ---
  { cluster: 'backtracking', q: 'Finding "any one solution" vs "all solutions" differs in which part of the backtracking template?',
    choices: [
      'The pruning predicate',
      'Whether the recursive call returns early on success',
      'The base case',
      'The state representation',
    ], correct: 1,
    why: 'For "any", returning true from the recursion stops exploration immediately. For "all", we accumulate and continue searching sibling branches.' },
  { cluster: 'backtracking', q: '"N-Queens" uses three boolean sets (column, diagonal, anti-diagonal). Why does that beat naïve brute force?',
    choices: [
      'Prunes O(N²) wasted checks per node',
      'Prunes entire subtrees whose current partial placement already conflicts',
      'It reduces memory, not time',
      'It\'s equivalent — just stylistic',
    ], correct: 1,
    why: 'Any placement that violates a constraint at depth d prunes an entire O(N^(n−d)) subtree. The sets give O(1) conflict checks.' },
  { cluster: 'backtracking', q: 'The two best moments to prune in backtracking are…',
    choices: [
      'At every recursive call and at leaves',
      'Before recursion (infeasibility) and after accepting an element (bound-driven)',
      'Only at the base case',
      'Never — pruning complicates the logic',
    ], correct: 1,
    why: 'Pre-call prune skips doomed branches entirely; post-accept bound prune (e.g. for optimisation) cuts branches that can\'t improve the running best.' },
  { cluster: 'backtracking', q: 'For "permutations of nums with duplicates", avoid duplicate outputs by…',
    choices: [
      'Using a HashSet of result strings',
      'Sorting then skipping used[i-1] == false && nums[i] == nums[i-1]',
      'Running quicksort on the output',
      'Taking only unique nums',
    ], correct: 1,
    why: 'The canonical trick: sort, then at each depth skip a duplicate only if the previous equal value was NOT used in the current branch (i.e. we are starting a new branch with an equal duplicate — that branch was already generated).' },
  { cluster: 'backtracking', q: 'Backtracking often TLEs even when "O(n!) is fine on paper." The usual culprit?',
    choices: [
      'Allocating a new List/Map at every recursive call instead of mutating + undoing',
      'Using recursion instead of iteration',
      'Not using parallelism',
      'JIT warmup',
    ], correct: 0,
    why: 'The hidden constant per node matters. choose/explore/un-choose on a shared mutable state is dramatically faster than copying state at each node.' },

  // --- C11: dp ---
  { cluster: 'dp', q: 'When designing a DP, what is the single most important question to answer FIRST?',
    choices: [
      'Memoize or tabulate?',
      'Top-down or bottom-up?',
      'What exactly does dp[i] (or dp[i][j]) MEAN, in one sentence?',
      'Which language to implement in?',
    ], correct: 2,
    why: 'If you can\'t state the subproblem definition in one sentence, you can\'t write a transition that is correct. Everything else follows from the definition.' },
  { cluster: 'dp', q: '"Minimum coins to make amount N" — what is dp[i]?',
    choices: [
      'Number of ways to make amount i',
      'Minimum coins to make amount i',
      'Set of coins used for amount i',
      'Largest coin ≤ i',
    ], correct: 1,
    why: 'dp[i] = min across all coins c of (dp[i − c] + 1), with dp[0] = 0 and dp[< 0] = ∞. Answer at dp[N].' },
  { cluster: 'dp', q: '0-1 knapsack vs unbounded knapsack: the key difference is in the loop order over what?',
    choices: [
      'Items (outer) and capacity (inner)',
      'Capacity direction: 0-1 iterates capacity DECREASING (large→small); unbounded iterates INCREASING',
      'Whether to use recursion',
      'Whether to sort items first',
    ], correct: 1,
    why: 'In the 1-D roll of 0-1 knapsack, iterating capacity high→low prevents an item from being counted twice. Unbounded knapsack iterates low→high because reuse IS allowed.' },
  { cluster: 'dp', q: '"Edit distance between s and t." The three transitions (insert, delete, substitute) correspond to…',
    choices: [
      'dp[i][j-1]+1, dp[i-1][j]+1, dp[i-1][j-1]+1',
      'dp[i][j+1]+1, dp[i+1][j]+1, dp[i+1][j+1]+1',
      'dp[i-1][j-1], dp[i][j-1], dp[i-1][j]',
      'All three use the same transition',
    ], correct: 0,
    why: 'Reading as "edit s[0..i) into t[0..j)": insert char from t = dp[i][j-1]+1; delete char from s = dp[i-1][j]+1; substitute = dp[i-1][j-1] + (s[i-1] == t[j-1] ? 0 : 1).' },
  { cluster: 'dp', q: 'Dropping a dimension via rolling array is safe when…',
    choices: [
      'The transition only reads from the previous row (or last K rows)',
      'The grid is sparse',
      'The DP is top-down',
      'The DP is NP-hard',
    ], correct: 0,
    why: 'If dp[i] depends only on dp[i-1] (or a bounded window), you can keep just those rows and reuse the array — O(W) space instead of O(N×W).' },

  // --- C12: design-math ---
  { cluster: 'design-math', q: 'LRU cache: which two structures combine, and why?',
    choices: [
      'Array + hashmap, for compact storage',
      'Hashmap (O(1) lookup) + doubly linked list (O(1) move-to-front and evict-tail)',
      'TreeMap + heap',
      'Linked list only, iterating on each op',
    ], correct: 1,
    why: 'Hashmap gives O(1) key→node. Doubly linked list gives O(1) splice (remove and re-insert at head). Together: O(1) get, put, and eviction.' },
  { cluster: 'design-math', q: 'x & (x − 1) evaluates to…',
    choices: [
      'x with its lowest set bit cleared',
      'x shifted right by 1',
      'x negated',
      'The sign bit of x',
    ], correct: 0,
    why: 'Classic Kernighan trick. Repeatedly applying x = x & (x-1) counts set bits in O(number of set bits), not O(32).' },
  { cluster: 'design-math', q: 'n & -n isolates…',
    choices: [
      'The highest set bit',
      'The lowest set bit (as a bitmask)',
      'All even-position bits',
      'The sign bit',
    ], correct: 1,
    why: 'In two\'s complement, -n = ~n + 1 flips bits above the lowest 1 and preserves it. ANDing gives just that lowest bit.' },
  { cluster: 'design-math', q: 'Reservoir sampling with reservoir size 1 over a stream of unknown length: on the k-th element, probability of including it in the sample?',
    choices: ['1/n (n = total length)', '1/k', '1/(k+1)', '1/2'],
    correct: 1,
    why: 'Keep element k with probability 1/k. By induction, every element ends up with uniform probability 1/n at the end.' },
  { cluster: 'design-math', q: '"Find the single number in an array where all others appear twice." Fastest?',
    choices: [
      'HashSet add/remove',
      'XOR all elements',
      'Sort then scan',
      'Count with HashMap',
    ], correct: 1,
    why: 'XOR is associative + commutative + a^a = 0 + a^0 = a. The pairs cancel; the single value remains. O(n) time, O(1) space.' },
]

// -- state --
type Phase = 'intro' | 'quiz' | 'results'
const phase = ref<Phase>('intro')
const idx = ref(0)
const answers = ref<(number | null)[]>(QS.map(() => null))
const revealed = ref<boolean[]>(QS.map(() => false))

const current = computed(() => QS[idx.value])
const total = QS.length

function pickAnswer(i: number) {
  if (revealed.value[idx.value]) return
  answers.value[idx.value] = i
  revealed.value[idx.value] = true
}

function next() {
  if (idx.value < total - 1) {
    idx.value++
  } else {
    finish()
  }
}
function prev() { if (idx.value > 0) idx.value-- }

const scores = computed(() => {
  // per-cluster: { right, total, pct }
  const buckets: Record<Cluster, { right: number; total: number }> = {} as any
  for (const c of Object.keys(CLUSTER_LABELS) as Cluster[]) buckets[c] = { right: 0, total: 0 }
  QS.forEach((q, i) => {
    buckets[q.cluster].total++
    if (answers.value[i] === q.correct) buckets[q.cluster].right++
  })
  return (Object.keys(buckets) as Cluster[]).map(c => ({
    cluster: c,
    label: CLUSTER_LABELS[c],
    chapter: CLUSTER_CHAPTER[c],
    right: buckets[c].right,
    total: buckets[c].total,
    pct: Math.round(100 * buckets[c].right / buckets[c].total),
  }))
})

const sortedScores = computed(() =>
  [...scores.value].sort((a, b) => a.pct - b.pct)
)

// Study order = weakest first, filtered to WEAK + OK
const studyOrder = computed(() =>
  sortedScores.value.filter(s => s.pct < 80)
)

function verdict(pct: number): 'weak' | 'ok' | 'strong' {
  if (pct < 60) return 'weak'
  if (pct < 80) return 'ok'
  return 'strong'
}

function finish() {
  phase.value = 'results'
  // persist
  storage.setJson('dsa-diagnostic:latest', {
    at: Date.now(),
    answers: answers.value,
    scores: scores.value,
  })
}

function restart() {
  phase.value = 'intro'
  idx.value = 0
  answers.value = QS.map(() => null)
  revealed.value = QS.map(() => false)
}

function start() {
  phase.value = 'quiz'
  idx.value = 0
}

// restore prior result if any
onMounted(() => {
  const prev = storage.getJson<{ scores?: any[]; at?: number } | null>('dsa-diagnostic:latest', null)
  if (prev && prev.scores) {
    // show results-only view by default; let user choose to retake
  }
})
const hasPrior = computed(() => {
  const prev = storage.getJson<{ at?: number } | null>('dsa-diagnostic:latest', null)
  return !!(prev && prev.at)
})
function viewPrior() {
  const prev = storage.getJson<any>('dsa-diagnostic:latest', null)
  if (prev && prev.answers) {
    answers.value = prev.answers
    revealed.value = prev.answers.map((a: number | null) => a !== null)
    phase.value = 'results'
  }
}

const answeredCount = computed(() => answers.value.filter(a => a !== null).length)
const progressPct = computed(() => Math.round(100 * (idx.value + 1) / total))
</script>

<template>
  <section class="diag">
    <!-- INTRO -->
    <div v-if="phase === 'intro'" class="diag-card">
      <h3>Diagnostic — where should you spend study time?</h3>
      <p>
        Sixty questions across the twelve topic clusters that make up the DSA interview surface.
        It takes about 15 minutes. Answer honestly — the output tells you which chapters to open first,
        not which ones you can skip. One correct choice per question; the explanation shows after you pick.
      </p>
      <ul class="scoring-rubric">
        <li><strong class="pct weak">&lt; 60 %</strong> on a cluster → WEAK: open the chapter.</li>
        <li><strong class="pct ok">60–79 %</strong> → OK: skim the chapter's templates and traps.</li>
        <li><strong class="pct strong">≥ 80 %</strong> → STRONG: skip the chapter for now; practise the hard problems.</li>
      </ul>
      <div class="actions">
        <button class="btn primary" @click="start">Start the diagnostic</button>
        <button v-if="hasPrior" class="btn ghost" @click="viewPrior">View my last result</button>
      </div>
    </div>

    <!-- QUIZ -->
    <div v-else-if="phase === 'quiz'" class="diag-card">
      <div class="progress-wrap" role="status" :aria-label="`Question ${idx + 1} of ${total}`">
        <div class="progress-bar"><div class="progress-fill" :style="{ width: `${progressPct}%` }"></div></div>
        <div class="progress-text">
          <span>Q {{ idx + 1 }} / {{ total }}</span>
          <span class="cluster-tag">{{ CLUSTER_LABELS[current.cluster] }}</span>
          <span class="answered">{{ answeredCount }} answered</span>
        </div>
      </div>

      <h3 class="q-text">{{ current.q }}</h3>

      <div class="choices">
        <button
          v-for="(c, i) in current.choices"
          :key="i"
          class="choice"
          :class="{
            selected: answers[idx] === i,
            correct: revealed[idx] && i === current.correct,
            wrong: revealed[idx] && answers[idx] === i && i !== current.correct,
            disabled: revealed[idx] && answers[idx] !== i && i !== current.correct,
          }"
          :disabled="revealed[idx]"
          @click="pickAnswer(i)"
        >
          <span class="letter">{{ String.fromCharCode(65 + i) }}</span>
          <span class="text">{{ c }}</span>
        </button>
      </div>

      <div v-if="revealed[idx]" class="why">
        <strong>Why:</strong> {{ current.why }}
      </div>

      <div class="actions">
        <button class="btn ghost" @click="prev" :disabled="idx === 0">Back</button>
        <button class="btn primary" @click="next" :disabled="!revealed[idx]">
          {{ idx === total - 1 ? 'See results' : 'Next' }}
        </button>
      </div>
    </div>

    <!-- RESULTS -->
    <div v-else class="diag-card">
      <h3>Your weakness map</h3>
      <p>
        {{ studyOrder.length === 0
          ? 'Clean sweep — every cluster scored ≥ 80 %. Move to hard problems and mocks.'
          : `${studyOrder.length} of 12 clusters need work. Open them in the order below — strict weakest-first.` }}
      </p>

      <div class="scores-grid">
        <div
          v-for="s in sortedScores"
          :key="s.cluster"
          class="score-row"
          :class="verdict(s.pct)"
        >
          <div class="score-label">
            <a :href="withBase(s.chapter)">{{ s.label }}</a>
          </div>
          <div class="score-bar-wrap">
            <div class="score-bar" :style="{ width: `${s.pct}%` }"></div>
          </div>
          <div class="score-numbers">
            <span class="pct">{{ s.pct }}%</span>
            <span class="raw">{{ s.right }} / {{ s.total }}</span>
          </div>
          <div class="score-verdict">
            {{ verdict(s.pct) === 'weak' ? 'WEAK' : verdict(s.pct) === 'ok' ? 'OK' : 'STRONG' }}
          </div>
        </div>
      </div>

      <div v-if="studyOrder.length > 0" class="rec">
        <h4>Recommended study order</h4>
        <ol>
          <li v-for="(s, i) in studyOrder" :key="s.cluster">
            <strong>{{ i + 1 }}.</strong>
            <a :href="withBase(s.chapter)">{{ s.label }}</a>
            <span class="rec-pct">({{ s.pct }}%)</span>
          </li>
        </ol>
        <p class="rec-note">
          See the <a :href="withBase('/map')">prerequisite map</a> before you start — if the chapter at the top of this list has unmet prereqs, start with those first.
        </p>
      </div>

      <div class="actions">
        <button class="btn primary" @click="restart">Retake</button>
        <a class="btn ghost" :href="withBase('/map')">Open the prerequisite map</a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.diag { margin: 1.5rem 0; }
.diag-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 1.5rem;
}
.diag-card h3 { margin-top: 0; }

.actions {
  margin-top: 1.25rem;
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.btn {
  padding: 0.6rem 1.1rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  text-decoration: none;
  display: inline-block;
  font-size: 0.95rem;
}
.btn.primary {
  background: var(--vp-c-brand-1, #4f46e5);
  color: white;
  border-color: transparent;
}
.btn.primary:disabled { opacity: 0.4; cursor: not-allowed; }
.btn.ghost:disabled { opacity: 0.4; cursor: not-allowed; }

.scoring-rubric {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
}
.scoring-rubric li {
  padding: 0.35rem 0;
  font-size: 0.95rem;
}
.scoring-rubric .pct {
  display: inline-block;
  min-width: 4.5rem;
  padding: 2px 6px;
  border-radius: 4px;
  text-align: center;
  margin-right: 0.5rem;
}
.pct.weak   { background: color-mix(in srgb, #ef4444 20%, transparent); color: #ef4444; }
.pct.ok     { background: color-mix(in srgb, #f59e0b 20%, transparent); color: #f59e0b; }
.pct.strong { background: color-mix(in srgb, #22c55e 20%, transparent); color: #22c55e; }

/* progress bar */
.progress-wrap { margin-bottom: 1rem; }
.progress-bar {
  width: 100%;
  height: 6px;
  background: var(--vp-c-divider);
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: var(--vp-c-brand-1, #4f46e5);
  transition: width 180ms ease;
}
.progress-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  margin-top: 0.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}
.cluster-tag {
  padding: 2px 10px;
  border-radius: 20px;
  background: var(--vp-c-brand-soft, rgba(79, 70, 229, 0.1));
  color: var(--vp-c-brand-1, #4f46e5);
  font-weight: 600;
}

.q-text {
  margin: 0.75rem 0 1rem;
  font-size: 1.1rem;
  line-height: 1.5;
}

.choices {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.choice {
  display: flex;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1.5px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  text-align: left;
  font-size: 0.95rem;
  transition: all 120ms ease;
}
.choice:hover:not(:disabled):not(.correct):not(.wrong) {
  border-color: var(--vp-c-brand-1, #4f46e5);
  background: var(--vp-c-bg-soft);
}
.choice .letter {
  font-weight: 700;
  color: var(--vp-c-text-2);
  flex-shrink: 0;
}
.choice.selected { border-color: var(--vp-c-brand-1, #4f46e5); }
.choice.correct {
  border-color: #22c55e;
  background: color-mix(in srgb, #22c55e 10%, transparent);
}
.choice.wrong {
  border-color: #ef4444;
  background: color-mix(in srgb, #ef4444 10%, transparent);
}
.choice.disabled { opacity: 0.5; cursor: default; }

.why {
  margin-top: 1rem;
  padding: 0.9rem 1rem;
  background: var(--vp-c-bg);
  border-left: 3px solid var(--vp-c-brand-1, #4f46e5);
  border-radius: 4px;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* results */
.scores-grid { margin: 1rem 0; }
.score-row {
  display: grid;
  grid-template-columns: 220px 1fr 90px 70px;
  gap: 0.75rem;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--vp-c-divider);
}
.score-label a { color: var(--vp-c-text-1); font-weight: 600; }
.score-label a:hover { color: var(--vp-c-brand-1, #4f46e5); }
.score-bar-wrap {
  background: var(--vp-c-divider);
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}
.score-bar {
  height: 100%;
  background: var(--vp-c-brand-1, #4f46e5);
}
.score-row.weak   .score-bar { background: #ef4444; }
.score-row.ok     .score-bar { background: #f59e0b; }
.score-row.strong .score-bar { background: #22c55e; }
.score-numbers { font-size: 0.9rem; display: flex; flex-direction: column; align-items: flex-end; }
.score-numbers .pct { font-weight: 700; }
.score-numbers .raw { color: var(--vp-c-text-2); font-size: 0.8rem; }
.score-verdict {
  font-size: 0.7rem;
  font-weight: 700;
  text-align: center;
  padding: 3px 6px;
  border-radius: 4px;
  letter-spacing: 0.5px;
}
.score-row.weak   .score-verdict { background: color-mix(in srgb, #ef4444 20%, transparent); color: #ef4444; }
.score-row.ok     .score-verdict { background: color-mix(in srgb, #f59e0b 20%, transparent); color: #f59e0b; }
.score-row.strong .score-verdict { background: color-mix(in srgb, #22c55e 20%, transparent); color: #22c55e; }

.rec { margin-top: 1.5rem; }
.rec h4 { margin: 0 0 0.5rem; }
.rec ol { padding-left: 1.2rem; }
.rec li { padding: 0.2rem 0; }
.rec-pct { color: var(--vp-c-text-2); font-size: 0.85rem; margin-left: 0.3rem; }
.rec-note {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: var(--vp-c-bg);
  border-radius: 6px;
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
}

@media (max-width: 600px) {
  .score-row { grid-template-columns: 1fr 60px; grid-template-areas: 'label verdict' 'bar bar' 'nums nums'; gap: 0.3rem; padding: 0.75rem 0; }
  .score-label   { grid-area: label; }
  .score-bar-wrap{ grid-area: bar; }
  .score-numbers { grid-area: nums; flex-direction: row; justify-content: space-between; }
  .score-verdict { grid-area: verdict; }
}
</style>
