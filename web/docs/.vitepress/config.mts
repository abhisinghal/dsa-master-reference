import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { generateRecentUpdates } from './gen-recent.mjs'
import { generateChangelogRss } from './gen-rss.mjs'
import generatedSidebar from './sidebar.generated.json'

type SidebarChapter = {
  items?: { text: string; link: string }[]
}

const sidebarData = generatedSidebar as {
  patterns: Record<string, SidebarChapter>
  dataStructures: Record<string, SidebarChapter>
}

const rCombining = /[\u0300-\u036F]/g
const rAsciiSeparators = /[—–→·]/g
const rNonAsciiSlugChar = /[^a-z0-9]+/g

function slugifyHeading(str: string) {
  return str
    .normalize('NFKD')
    .replace(rCombining, '')
    .toLowerCase()
    .replace(rAsciiSeparators, '-')
    .replace(rNonAsciiSlugChar, '-')
    .replace(/-{2,}/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/^(\d)/, '_$1')
}

function nestedPattern(text: string, slug: string) {
  const items = sidebarData.patterns[slug]?.items ?? []
  return items.length
    ? { text, link: `/patterns/${slug}`, collapsed: true, items }
    : { text, link: `/patterns/${slug}` }
}

function nestedDataStructure(text: string, slug: string) {
  const items = sidebarData.dataStructures[slug]?.items ?? []
  return items.length
    ? { text, link: `/data-structures/${slug}`, collapsed: true, items }
    : { text, link: `/data-structures/${slug}` }
}

export default withMermaid(defineConfig({
  base: '/dsa-master-reference/',
  title: 'DSA Master Reference',
  description: 'Patterns, invariants, and problems for senior/staff DSA interviews (Java 17)',
  cleanUrls: true,
  ignoreDeadLinks: true,
  sitemap: {
    hostname: 'https://abhisinghal.github.io/dsa-master-reference/'
  },
  head: [
    ['link', { rel: 'icon', href: '/dsa-master-reference/favicon.svg' }],
    ['link', { rel: 'alternate', type: 'application/rss+xml', title: 'DSA Master Reference changelog', href: '/dsa-master-reference/rss.xml' }],
    ['meta', { name: 'theme-color', content: '#2563eb' }],
    ['script', { src: 'https://cjrtnc.leaningtech.com/3.0/cj3loader.js' }]
  ],
  markdown: {
    lineNumbers: true,
    anchor: {
      slugify: slugifyHeading
    },
    theme: {
      light: 'github-light',
      dark: 'github-dark-high-contrast'
    }
  },
  vite: {
    plugins: [
      {
        name: 'generate-recent-updates',
        apply: 'build',
        buildStart() {
          generateRecentUpdates()
          generateChangelogRss()
        }
      }
    ]
  },
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Roadmap', link: '/foundations/roadmap' },
      { text: 'Patterns', link: '/patterns/' },
      { text: 'Data Structures', link: '/data-structures/' },
      { text: 'Practice', link: '/problems/' },
      { text: 'System Design', link: '/system-design/' },
      { text: 'Cheat sheets', link: '/appendix/cheatsheets' },
      { text: 'PDF', link: 'https://github.com/abhisinghal/dsa-master-reference/releases' }
    ],
    sidebar: {
      '/foundations/': [
        {
          text: 'Foundations',
          items: [
            { text: 'How to Use This Book', link: '/foundations/how-to-use' },
            { text: 'Interview Playbook', link: '/foundations/playbook' },
            { text: 'Zero-to-Hero Roadmap', link: '/foundations/roadmap' },
            { text: 'Glossary', link: '/foundations/glossary' },
            { text: 'Java Data Structures Primer', link: '/foundations/java-primer' },
            { text: 'Java DSA Gotchas', link: '/foundations/java-gotchas' },
            { text: 'How this compares', link: '/foundations/vs-competitors' },
            { text: 'Complexity Model', link: '/foundations/complexity' },
            { text: 'Debugging DSA Code', link: '/foundations/debugging' }
          ]
        }
      ],
      '/patterns/': [
        {
          text: 'The 21 Core Patterns',
          items: [
            { text: 'Overview', link: '/patterns/' },
            nestedPattern('1. Sliding Window', 'sliding-window'),
            nestedPattern('2. Two Pointers', 'two-pointers'),
            nestedPattern('3. Fast/Slow Pointers', 'fast-slow'),
            nestedPattern('4. Prefix Sum', 'prefix-sum'),
            nestedPattern('5. Hashing', 'hashing'),
            nestedPattern('6. Monotonic Stack', 'monotonic-stack'),
            nestedPattern('7. Binary Search', 'binary-search'),
            nestedPattern('8. Binary Search on Answer', 'bs-on-answer'),
            nestedPattern('9. Top-K / Heap', 'top-k-heap'),
            nestedPattern('10. K-way Merge', 'k-way-merge'),
            nestedPattern('11. Merge Intervals', 'merge-intervals'),
            nestedPattern('12. Sweep Line', 'sweep-line'),
            nestedPattern('13. Topological Sort', 'topological-sort'),
            nestedPattern('14. Union-Find', 'union-find'),
            nestedPattern('15. Greedy', 'greedy'),
            nestedPattern('16. Backtracking', 'backtracking'),
            nestedPattern('17. Divide & Conquer', 'divide-conquer'),
            nestedPattern('18. Dynamic Programming', 'dp'),
            nestedPattern('19. Trie Pattern', 'trie-pattern'),
            nestedPattern('20. Bit Manipulation', 'bit-manip'),
            nestedPattern('21. Quickselect', 'quickselect'),
            nestedPattern('Bonus: Math & Number Theory', 'math'),
            nestedPattern('Bonus: Design', 'design')
          ]
        }
      ],
      '/data-structures/': [
        {
          text: 'Part III — Data Structures in Depth',
          items: [
            { text: 'Overview', link: '/data-structures/' },
            nestedDataStructure('Arrays', 'arrays'),
            nestedDataStructure('Strings', 'strings'),
            nestedDataStructure('Linked Lists', 'linked-lists'),
            nestedDataStructure('Stacks & Queues', 'stacks-queues'),
            nestedDataStructure('Trees', 'trees'),
            nestedDataStructure('Heaps', 'heaps'),
            nestedDataStructure('Trie', 'trie'),
            nestedDataStructure('Graphs', 'graphs'),
            nestedDataStructure('Segment / Fenwick Tree', 'segment-fenwick')
          ]
        }
      ],
      '/system-design/': [
        {
          text: 'Part IV — System Design',
          items: [
            { text: 'Fundamentals', link: '/system-design/' }
          ]
        }
      ],
      '/problems/': [
        {
          text: 'Practice — Multi-Approach Deep Dives',
          items: [
            { text: 'Overview', link: '/problems/' }
          ]
        },
        {
          text: '1. Sliding Window',
          collapsed: true,
          items: [
            { text: 'Longest Substring Without Repeating Characters', link: '/problems/sliding-window-longest-substring' },
            { text: 'Binary Subarrays With Sum', link: '/problems/binary-subarrays-with-sum' },
            { text: 'Constrained Subsequence Sum', link: '/problems/constrained-subsequence-sum' },
            { text: 'Count Number of Nice Subarrays', link: '/problems/count-number-of-nice-subarrays' },
            { text: 'Diet Plan Performance', link: '/problems/diet-plan-performance' },
            { text: 'Find All Anagrams in a String', link: '/problems/find-all-anagrams-in-a-string' },
            { text: 'Frequency of the Most Frequent Element', link: '/problems/frequency-of-the-most-frequent-element' },
            { text: 'Fruits into Baskets', link: '/problems/fruit-into-baskets' },
            { text: 'Get Equal Substrings Within Budget', link: '/problems/get-equal-substrings-within-budget' },
            { text: 'Jump Game VI', link: '/problems/jump-game-vi' },
            { text: 'Longest Palindromic Substring', link: '/problems/longest-palindromic-substring' },
            { text: 'Longest Repeating Character Replacement', link: '/problems/longest-repeating-character-replacement' },
            { text: 'Longest Substring with At Most K Distinct', link: '/problems/longest-substring-with-at-most-k-distinct-characters' },
            { text: 'Max Consecutive Ones III', link: '/problems/max-consecutive-ones-iii' },
            { text: 'Maximum Average Subarray I', link: '/problems/maximum-average-subarray-i' },
            { text: 'Minimum Size Subarray Sum', link: '/problems/minimum-size-subarray-sum' },
            { text: 'Minimum Window Subsequence', link: '/problems/minimum-window-subsequence' },
            { text: 'Minimum Window Substring', link: '/problems/minimum-window-substring' },
            { text: 'Number of Substrings Containing All Three Characters', link: '/problems/number-of-substrings-containing-all-three-characters' },
            { text: 'Permutation in String', link: '/problems/permutation-in-string' },
            { text: 'Replace the Substring for Balanced String', link: '/problems/replace-the-substring-for-balanced-string' },
            { text: 'Shortest Subarray with Sum ≥ K (negatives allowed)', link: '/problems/shortest-subarray-with-sum-at-least-k' },
            { text: 'Subarray Product Less Than K', link: '/problems/subarray-product-less-than-k' },
            { text: 'Longest Substring with **exactly** K distinct', link: '/problems/subarrays-with-k-different-integers' },
            { text: 'Substring with Concatenation of All Words', link: '/problems/substring-with-concatenation-of-all-words' },
            { text: 'Trapping Rain Water', link: '/problems/trapping-rain-water' }
          ]
        },
        {
          text: '2. Two Pointers',
          collapsed: true,
          items: [
            { text: 'Container With Most Water', link: '/problems/two-pointers-container-with-most-water' },
            { text: '3Sum Closest', link: '/problems/3sum-closest' },
            { text: '3Sum Smaller', link: '/problems/3sum-smaller' },
            { text: '4Sum', link: '/problems/4sum' },
            { text: 'Boats to Save People', link: '/problems/boats-to-save-people' },
            { text: 'Intersection of Two Arrays II', link: '/problems/intersection-of-two-arrays-ii' },
            { text: 'Largest Rectangle in Histogram', link: '/problems/largest-rectangle-in-histogram' },
            { text: 'Merge Sorted Array (in place, from the back)', link: '/problems/merge-sorted-array' },
            { text: 'Move Zeroes', link: '/problems/move-zeroes' },
            { text: 'Sort Array By Parity', link: '/problems/sort-array-by-parity' },
            { text: 'Sort Transformed Array', link: '/problems/squares-of-a-sorted-array' },
            { text: 'Trapping Rain Water II (2D)', link: '/problems/trapping-rain-water-ii' },
            { text: 'Valid Palindrome / Valid Palindrome II', link: '/problems/valid-palindrome-ii' },
            { text: 'Wiggle Sort', link: '/problems/wiggle-sort-ii' }
          ]
        },
        {
          text: '3. Fast/Slow',
          collapsed: true,
          items: [
            { text: 'Linked List Cycle II', link: '/problems/fast-slow-linked-list-cycle-ii' },
            { text: 'Find the Duplicate Number', link: '/problems/find-the-duplicate-number' },
            { text: 'Happy Number', link: '/problems/happy-number' },
            { text: 'Linked List Cycle', link: '/problems/linked-list-cycle' },
            { text: 'Middle of the Linked List', link: '/problems/middle-of-the-linked-list' },
            { text: 'Palindrome Linked List', link: '/problems/palindrome-linked-list' }
          ]
        },
        {
          text: '4. Prefix Sum',
          collapsed: true,
          items: [
            { text: 'Subarray Sum Equals K', link: '/problems/prefix-sum-subarray-sum-equals-k' },
            { text: 'Car Pooling', link: '/problems/car-pooling' },
            { text: 'Contiguous Array (equal 0s and 1s)', link: '/problems/contiguous-array' },
            { text: 'Continuous Subarray Sum (multiple of k)', link: '/problems/continuous-subarray-sum' },
            { text: 'Corporate Flight Bookings', link: '/problems/corporate-flight-bookings' },
            { text: 'Count Submatrices With Target Sum', link: '/problems/count-submatrices-with-target-sum' },
            { text: 'Matrix Block Sum', link: '/problems/matrix-block-sum' },
            { text: 'Maximal Square / Maximal Rectangle', link: '/problems/maximal-rectangle' },
            { text: '2D — Range Addition II / stamping a grid', link: '/problems/range-addition-ii' },
            { text: 'Range Addition', link: '/problems/range-addition' },
            { text: 'Subarray Sums Divisible by K', link: '/problems/subarray-sums-divisible-by-k' }
          ]
        },
        {
          text: '5. Hashing',
          collapsed: true,
          items: [
            { text: 'Two Sum', link: '/problems/hashing-two-sum' },
            { text: '3Sum', link: '/problems/3sum' },
            { text: 'Candy', link: '/problems/candy' },
            { text: 'Find Duplicate File in System', link: '/problems/find-duplicate-file-in-system' },
            { text: 'Group Shifted Strings', link: '/problems/group-shifted-strings' },
            { text: 'Isomorphic Strings', link: '/problems/isomorphic-strings' },
            { text: 'Longest Consecutive Sequence', link: '/problems/longest-consecutive-sequence' },
            { text: 'Maximum Product Subarray', link: '/problems/maximum-product-subarray' },
            { text: 'Number of Islands', link: '/problems/number-of-islands' },
            { text: 'Two Sum II — sorted input', link: '/problems/two-sum-ii-input-array-is-sorted' },
            { text: 'Two Sum III — design', link: '/problems/two-sum-iii-data-structure-design' },
            { text: 'Two Sum Less Than K', link: '/problems/two-sum-less-than-k' },
            { text: 'Valid Anagram', link: '/problems/valid-anagram' },
            { text: 'Word Ladder', link: '/problems/word-ladder' }
          ]
        },
        {
          text: '6. Monotonic Stack',
          collapsed: true,
          items: [
            { text: 'Daily Temperatures', link: '/problems/monotonic-stack-daily-temperatures' },
            { text: 'Next Greater Element II (circular)', link: '/problems/next-greater-element-ii' },
            { text: 'Online Stock Span', link: '/problems/online-stock-span' },
            { text: 'Remove K Digits / Largest Rectangle variants', link: '/problems/remove-k-digits' },
            { text: 'Sum of Subarray Minimums', link: '/problems/sum-of-subarray-minimums' }
          ]
        },
        {
          text: '7. Binary Search',
          collapsed: true,
          items: [
            { text: 'Search in Rotated Sorted Array', link: '/problems/binary-search-rotated-sorted' },
            { text: 'Order-Agnostic Binary Search', link: '/problems/binary-search' },
            { text: 'Find Minimum in Rotated Sorted Array', link: '/problems/find-minimum-in-rotated-sorted-array' },
            { text: 'Find Peak Element', link: '/problems/find-peak-element' },
            { text: 'Search in Rotated Array II (with duplicates)', link: '/problems/search-in-rotated-sorted-array-ii' }
          ]
        },
        {
          text: '8. BS on Answer',
          collapsed: true,
          items: [
            { text: 'Koko Eating Bananas', link: '/problems/bs-on-answer-koko-bananas' },
            { text: 'Capacity to Ship Packages in D Days', link: '/problems/capacity-to-ship-packages-within-d-days' },
            { text: 'Divide Chocolate / Maximize the Minimum', link: '/problems/divide-chocolate' },
            { text: 'Find K-th Smallest Pair Distance', link: '/problems/find-k-th-smallest-pair-distance' },
            { text: 'Median of a Row-wise Sorted Matrix', link: '/problems/kth-smallest-element-in-a-sorted-matrix' },
            { text: 'Kth Element of Two Sorted Arrays', link: '/problems/median-of-two-sorted-arrays' },
            { text: 'Minimize Max Distance to Gas Station', link: '/problems/minimize-max-distance-to-gas-station' },
            { text: 'Path With Minimum Effort', link: '/problems/path-with-minimum-effort' },
            { text: 'Split Array Largest Sum / Book Allocation', link: '/problems/split-array-largest-sum' }
          ]
        },
        {
          text: '9. Top-K / Heap',
          collapsed: true,
          items: [
            { text: 'Top K Frequent Elements', link: '/problems/top-k-frequent-elements' },
            { text: 'K Closest Points to Origin', link: '/problems/k-closest-points-to-origin' },
            { text: 'Kth Largest Element in a Stream', link: '/problems/kth-largest-element-in-a-stream' },
            { text: 'Reorganize String', link: '/problems/reorganize-string' }
          ]
        },
        {
          text: '10. K-way Merge',
          collapsed: true,
          items: [
            { text: 'Merge k Sorted Lists', link: '/problems/k-way-merge-k-sorted-lists' },
            { text: 'Merge Two Sorted Lists', link: '/problems/merge-two-sorted-lists' },
            { text: 'Smallest Range Covering Elements from K Lists', link: '/problems/smallest-range-covering-elements-from-k-lists' },
            { text: 'Ugly Number II / Super Ugly Number', link: '/problems/ugly-number-ii' }
          ]
        },
        {
          text: '11. Merge Intervals',
          collapsed: true,
          items: [
            { text: 'Merge Intervals', link: '/problems/merge-intervals-classic' },
            { text: 'Employee Free Time', link: '/problems/employee-free-time' },
            { text: 'Insert Interval', link: '/problems/insert-interval' },
            { text: 'Interval List Intersections', link: '/problems/interval-list-intersections' },
            { text: 'Meeting Rooms', link: '/problems/meeting-rooms' },
            { text: 'Remove Covered Intervals', link: '/problems/remove-covered-intervals' }
          ]
        },
        {
          text: '12. Sweep Line',
          collapsed: true,
          items: [
            { text: 'Meeting Rooms II', link: '/problems/sweep-line-meeting-rooms-ii' },
            { text: 'My Calendar II / III', link: '/problems/my-calendar-ii' },
            { text: 'The Skyline Problem', link: '/problems/the-skyline-problem' }
          ]
        },
        {
          text: '13. Topological Sort',
          collapsed: true,
          items: [
            { text: 'Course Schedule II', link: '/problems/topological-sort-course-schedule' },
            { text: 'Alien Dictionary', link: '/problems/alien-dictionary' },
            { text: 'Minimum Height Trees', link: '/problems/minimum-height-trees' },
            { text: 'Parallel Courses', link: '/problems/parallel-courses' },
            { text: 'Sequence Reconstruction', link: '/problems/sequence-reconstruction' }
          ]
        },
        {
          text: '14. Union-Find',
          collapsed: true,
          items: [
            { text: 'Number of Provinces', link: '/problems/union-find-number-of-provinces' },
            { text: 'Accounts Merge', link: '/problems/accounts-merge' },
            { text: 'Connecting Cities With Minimum Cost', link: '/problems/connecting-cities-with-minimum-cost' },
            { text: 'Find Critical and Pseudo-Critical Edges', link: '/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree' },
            { text: 'Min Cost to Connect All Points', link: '/problems/min-cost-to-connect-all-points' },
            { text: 'Most Stones Removed', link: '/problems/most-stones-removed-with-same-row-or-column' },
            { text: 'Number of Islands II', link: '/problems/number-of-islands-ii' },
            { text: 'Optimize Water Distribution in a Village', link: '/problems/optimize-water-distribution-in-a-village' },
            { text: 'Redundant Connection', link: '/problems/redundant-connection' }
          ]
        },
        {
          text: '15. Greedy',
          collapsed: true,
          items: [
            { text: 'Jump Game II', link: '/problems/greedy-jump-game-ii' },
            { text: 'Best Time to Buy and Sell Stock', link: '/problems/best-time-to-buy-and-sell-stock' },
            { text: 'Course Schedule III', link: '/problems/course-schedule-iii' },
            { text: 'Gas Station', link: '/problems/gas-station' },
            { text: 'Jump Game III', link: '/problems/jump-game-iii' },
            { text: 'Jump Game I', link: '/problems/jump-game' },
            { text: 'Maximum Length of Pair Chain', link: '/problems/maximum-length-of-pair-chain' },
            { text: 'Maximum Subarray (Kadane)', link: '/problems/maximum-subarray' },
            { text: 'Minimum Number of Arrows', link: '/problems/minimum-number-of-arrows-to-burst-balloons' },
            { text: 'Non-overlapping Intervals', link: '/problems/non-overlapping-intervals' },
            { text: 'Video Stitching / Minimum Number of Taps', link: '/problems/video-stitching' }
          ]
        },
        {
          text: '16. Backtracking',
          collapsed: true,
          items: [
            { text: 'N-Queens', link: '/problems/backtracking-n-queens' },
            { text: 'Beautiful Arrangement', link: '/problems/beautiful-arrangement' },
            { text: 'Combination Sum / Combination Sum II', link: '/problems/combination-sum-ii' },
            { text: 'Combination Sum III', link: '/problems/combination-sum-iii' },
            { text: 'Combination Sum IV', link: '/problems/combination-sum-iv' },
            { text: 'Letter Case Permutation', link: '/problems/letter-case-permutation' },
            { text: 'Letter Combinations of a Phone Number', link: '/problems/letter-combinations-of-a-phone-number' },
            { text: 'N-Queens II', link: '/problems/n-queens-ii' },
            { text: 'Next Permutation', link: '/problems/next-permutation' },
            { text: 'Palindrome Partitioning', link: '/problems/palindrome-partitioning' },
            { text: 'Permutations II (with duplicates)', link: '/problems/permutations-ii' },
            { text: 'Permutations', link: '/problems/permutations' },
            { text: 'Robot Room Cleaner', link: '/problems/robot-room-cleaner' },
            { text: 'Subsets II (with duplicates)', link: '/problems/subsets-ii' },
            { text: 'Sudoku Solver', link: '/problems/sudoku-solver' },
            { text: 'Unique Paths III', link: '/problems/unique-paths-iii' },
            { text: 'Valid Sudoku', link: '/problems/valid-sudoku' }
          ]
        },
        {
          text: '17. Divide & Conquer',
          collapsed: true,
          items: [
            { text: 'Count of Smaller Numbers After Self', link: '/problems/divide-conquer-inversions' },
            { text: 'Count of Range Sum', link: '/problems/count-of-range-sum' },
            { text: 'Global and Local Inversions', link: '/problems/global-and-local-inversions' },
            { text: 'Reverse Pairs', link: '/problems/reverse-pairs' },
            { text: 'Sort List', link: '/problems/sort-list' }
          ]
        },
        {
          text: '18. Dynamic Programming',
          collapsed: true,
          items: [
            { text: 'House Robber', link: '/problems/dp-house-robber' },
            { text: 'Best Time with at most k Transactions', link: '/problems/best-time-to-buy-and-sell-stock-iv' },
            { text: 'Best Time to Buy/Sell with Cooldown', link: '/problems/best-time-to-buy-and-sell-stock-with-cooldown' },
            { text: 'Best Time with Transaction Fee', link: '/problems/best-time-to-buy-and-sell-stock-with-transaction-fee' },
            { text: 'Matrix Chain Multiplication', link: '/problems/burst-balloons' },
            { text: 'Climbing Stairs', link: '/problems/climbing-stairs' },
            { text: 'Coin Change II (count ways)', link: '/problems/coin-change-ii' },
            { text: 'Coin Change (min coins)', link: '/problems/coin-change' },
            { text: 'Delete and Earn', link: '/problems/delete-and-earn' },
            { text: 'Dungeon Game', link: '/problems/dungeon-game' },
            { text: 'Edit Distance', link: '/problems/edit-distance' },
            { text: 'Travelling Salesman', link: '/problems/find-the-shortest-superstring' },
            { text: 'House Robber II', link: '/problems/house-robber-ii' },
            { text: 'Last Stone Weight II', link: '/problems/last-stone-weight-ii' },
            { text: 'Longest Common Subsequence', link: '/problems/longest-common-subsequence' },
            { text: 'Longest Increasing Subsequence', link: '/problems/longest-increasing-subsequence' },
            { text: 'Longest Palindromic Subsequence', link: '/problems/longest-palindromic-subsequence' },
            { text: 'Maximal Square', link: '/problems/maximal-square' },
            { text: 'Maximum Sum Circular Subarray', link: '/problems/maximum-sum-circular-subarray' },
            { text: 'Min Cost Climbing Stairs / Paint Fence', link: '/problems/min-cost-climbing-stairs' },
            { text: 'Minimum Cost to Merge Stones', link: '/problems/minimum-cost-to-merge-stones' },
            { text: 'Minimum Path Sum / Minimum Falling Path Sum', link: '/problems/minimum-falling-path-sum' },
            { text: 'Number of Ways to Assign (hats/jobs)', link: '/problems/number-of-ways-to-wear-different-hats-to-each-other' },
            { text: 'Paint House I/II', link: '/problems/paint-house-ii' },
            { text: 'Palindrome Partitioning II', link: '/problems/palindrome-partitioning-ii' },
            { text: 'Partition Equal Subset Sum', link: '/problems/partition-equal-subset-sum' },
            { text: 'Partition to K Equal Sum Subsets', link: '/problems/partition-to-k-equal-sum-subsets' },
            { text: 'Perfect Squares', link: '/problems/perfect-squares' },
            { text: 'Regex / Wildcard Matching', link: '/problems/regular-expression-matching' },
            { text: 'Shortest Path Visiting All Nodes', link: '/problems/shortest-path-visiting-all-nodes' },
            { text: 'Target Sum', link: '/problems/target-sum' },
            { text: 'Unique Paths / Unique Paths II', link: '/problems/unique-paths-ii' }
          ]
        },
        {
          text: '19. Trie',
          collapsed: true,
          items: [
            { text: 'Word Search II', link: '/problems/trie-word-search-ii' },
            { text: 'Concatenated Words', link: '/problems/concatenated-words' },
            { text: 'Count Pairs With XOR in a Range', link: '/problems/count-pairs-with-xor-in-a-range' },
            { text: 'Add and Search Word', link: '/problems/design-add-and-search-words-data-structure' },
            { text: 'Maximum Genetic Difference Query', link: '/problems/maximum-genetic-difference-query' },
            { text: 'Maximum XOR With an Element From Array', link: '/problems/maximum-xor-with-an-element-from-array' },
            { text: 'Replace Words', link: '/problems/replace-words' },
            { text: 'Stream of Characters', link: '/problems/stream-of-characters' }
          ]
        },
        {
          text: '20. Bit Manipulation',
          collapsed: true,
          items: [
            { text: 'Single Number', link: '/problems/bit-manip-single-number' },
            { text: 'Find the Difference / Set Mismatch', link: '/problems/find-the-difference' },
            { text: 'Hamming Distance', link: '/problems/hamming-distance' },
            { text: 'Maximum Product of Word Lengths', link: '/problems/maximum-product-of-word-lengths' },
            { text: 'Missing Number', link: '/problems/missing-number' },
            { text: 'Number of 1 Bits', link: '/problems/number-of-1-bits' },
            { text: 'Power of Two', link: '/problems/power-of-two' },
            { text: 'Reverse Bits', link: '/problems/reverse-bits' },
            { text: 'Subsets', link: '/problems/subsets' },
            { text: 'Sum of All Subset XOR / SOS DP', link: '/problems/sum-of-all-subset-xor-totals' }
          ]
        },
        {
          text: '21. Quickselect',
          collapsed: true,
          items: [
            { text: 'Kth Largest Element in an Array', link: '/problems/quickselect-kth-largest' }
          ]
        }
      ],
      '/appendix/': [
        {
          text: 'Appendix',
          items: [
            { text: 'Cheat Sheets & Templates', link: '/appendix/cheatsheets' },
            { text: 'Self-Check & Drills', link: '/appendix/self-check' },
            { text: 'Master Problem Index', link: '/appendix/problem-index' },
            { text: 'Practice Solutions', link: '/appendix/practice-solutions' },
            { text: 'Mock Interview Transcripts', link: '/appendix/mock-transcripts' },
            { text: 'Traps Catalog', link: '/appendix/traps-catalog' },
            { text: 'Changelog', link: '/appendix/changelog' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/abhisinghal/dsa-master-reference' }
    ],
    footer: {
      message: 'Released under MIT license.',
      copyright: 'Copyright © 2026 Abhishek Singhal'
    },
    search: {
      provider: 'local'
    },
    outline: 2
  }
}))
