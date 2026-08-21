# Practice Solutions Appendix
<p class="secgoal"><b>What &amp; why:</b> every practice / variation problem referenced anywhere in this book, in one place, with a compact <b>Approach</b> hint that gets you unstuck without spoiling the solve. Click through to LeetCode; jump to the corresponding pattern chapter for the full template.</p>

<Callout kind="key" title="How to use it">

attempt each problem from its pattern card first. If you stall, read only the Approach cell (2–3 lines). The 40+ hardest variations have a full numbered-steps walkthrough below the tables.

</Callout>

**316** practice / variation problems indexed across **31** pattern areas — this is the one place to check when you want a hint. For the full write-up on a *canonical* problem, use the [Master Problem Index](/appendix/problem-index) to jump straight to its section.


## [Sliding Window](/patterns/sliding-window)

| Problem | Approach hint |
|---|---|
| <a id="binary-subarrays-with-sum"></a>[Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/) | same trick, "sum = S" over a 0/1 array |
| <a id="constrained-subsequence-sum"></a>[Constrained Subsequence Sum](https://leetcode.com/problems/constrained-subsequence-sum/) | same windowed-max of a `dp` array, with the window being the allowed gap `k` |
| <a id="count-number-of-nice-subarrays"></a>[Count Number of Nice Subarrays](https://leetcode.com/problems/count-number-of-nice-subarrays/) | same trick, "K odd numbers" as the count |
| <a id="diet-plan-performance"></a>[Diet Plan Performance](https://leetcode.com/problems/diet-plan-performance/) | classify each window by sum thresholds; sum score |
| <a id="find-all-anagrams-in-a-string"></a>[Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/) · [⇩ walkthrough](#find-all-anagrams-in-a-string) | slide a **char-count vector**; record `left` when it matches `need[]` |
| <a id="frequency-of-the-most-frequent-element"></a>[Frequency of the Most Frequent Element](https://leetcode.com/problems/frequency-of-the-most-frequent-element/) | sort, then window where `windowLen·max − windowSum ≤ k` operations |
| <a id="fruit-into-baskets"></a>[Fruits into Baskets](https://leetcode.com/problems/fruit-into-baskets/) · [⇩ walkthrough](#fruit-into-baskets) | it's literally "at most **2** distinct" dressed up as picking fruit into two baskets |
| <a id="get-equal-substrings-within-budget"></a>[Get Equal Substrings Within Budget](https://leetcode.com/problems/get-equal-substrings-within-budget/) | shrink when the total change-cost inside the window exceeds the budget |
| <a id="jump-game-vi"></a>[Jump Game VI](https://leetcode.com/problems/jump-game-vi/) | the deque holds the best `dp` value reachable within the jump range; front = best score to jump from |
| <a id="longest-palindromic-substring"></a>[Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Adding a char at the right can turn a valid palindrome into an invalid one — but also into a *larger* valid one. Non-monotone. |
| <a id="longest-repeating-character-replacement"></a>[Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | the window is valid while `windowLen − countOfMostFrequentChar ≤ K` (you may replace up to `K` of the minority) |
| <a id="subarrays-with-k-different-integers"></a>[Longest Substring with **exactly** K distinct](https://leetcode.com/problems/subarrays-with-k-different-integers/) | Exactly-K validity isn't monotone: a window with 3 distinct isn't "valid" for K=2 nor for K=4. |
| <a id="longest-substring-with-at-most-k-distinct-characters"></a>[Longest Substring with At Most K Distinct](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) · [⇩ walkthrough](#longest-substring-with-at-most-k-distinct-characters) | allow up to `K` different characters instead of zero repeats; shrink while the distinct-count exceeds `K` (track counts in a small map) |
| <a id="longest-substring-without-repeating-characters"></a>[Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | See the pattern chapter for the template. |
| <a id="max-consecutive-ones-iii"></a>[Max Consecutive Ones III](https://leetcode.com/problems/max-consecutive-ones-iii/) | over a 0/1 array, shrink only when the number of zeros in the window exceeds `K` (you may flip `K` zeros) |
| <a id="maximum-average-subarray-i"></a>[Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | plain sum, divide by k at the end |
| <a id="maximum-subarray"></a>[Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | The "rule" here is "which subarray has max sum?" — there's no growing/shrinking validity, only a *choice*: keep extending or restart. |
| <a id="minimum-size-subarray-sum"></a>[Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/) | this exact shape (positive values, sum ≥ target) |
| <a id="minimum-window-subsequence"></a>[Minimum Window Subsequence](https://leetcode.com/problems/minimum-window-subsequence/) | the target must appear in order (not just as a multiset), so track progress through the pattern instead of counts |
| <a id="minimum-window-substring"></a>[Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | validity is "covers all required characters," tracked with a have/need counter |
| <a id="number-of-substrings-containing-all-three-characters"></a>[Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/) | count from the *shrinking* side: `count += left` at each valid `right` |
| <a id="permutation-in-string"></a>[Permutation in String](https://leetcode.com/problems/permutation-in-string/) · [⇩ walkthrough](#permutation-in-string) | same as above; return true on the first match |
| <a id="replace-the-substring-for-balanced-string"></a>[Replace the Substring for Balanced String](https://leetcode.com/problems/replace-the-substring-for-balanced-string/) | shrink while the outside-window counts are already balanced |
| <a id="shortest-subarray-with-sum-at-least-k"></a>[Shortest Subarray with Sum ≥ K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/) | Same reason — negatives break the shortest-variable shrink rule. |
| <a id="subarray-product-less-than-k"></a>[Subarray Product Less Than K](https://leetcode.com/problems/subarray-product-less-than-k/) | The product argument (`product /= a[left]` restores validity) assumes strictly-positive integers. Zeros make the product 0 permanently; negatives flip the inequality direction. |
| <a id="subarray-sum-equals-k"></a>[Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | Adding a negative can lower the running sum below K after it was above → *invalid can become valid again by growing*. Extension test fails. |
| <a id="substring-with-concatenation-of-all-words"></a>[Substring with Concatenation of All Words](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) | the "characters" are whole words of equal length |
| <a id="trapping-rain-water"></a>[Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Water at each index depends on the max on **both** sides — not on a window that slides in one direction. |

## [Two Pointers](/patterns/two-pointers)

| Problem | Approach hint |
|---|---|
| <a id="3sum-closest"></a>[3Sum Closest](https://leetcode.com/problems/3sum-closest/) · [⇩ walkthrough](#_3sum-closest) | instead of hunting for exactly 0, track the sum closest to `target` as the pointers move |
| <a id="3sum-smaller"></a>[3Sum Smaller](https://leetcode.com/problems/3sum-smaller/) | count triplets with sum `< target`; when `a[lo]+a[hi] < target`, *all* `hi−lo` pairs qualify at once, so add them in one shot |
| <a id="4sum"></a>[4Sum](https://leetcode.com/problems/4sum/) · [⇩ walkthrough](#_4sum) | add one more outer loop, then two-pointer the inner pair (skip duplicates at every level) |
| <a id="boats-to-save-people"></a>[Boats to Save People](https://leetcode.com/problems/boats-to-save-people/) | sort, then pair the lightest with the heaviest that still fits — a converging-pointer greedy |
| <a id="container-with-most-water"></a>[Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | maximize a single span instead of summing trapped water; move the shorter wall |
| <a id="intersection-of-two-arrays-ii"></a>[Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/) | sort both, then two pointers advancing the smaller side |
| <a id="largest-rectangle-in-histogram"></a>[Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | the dual "peak" view — a monotonic stack finds how far each bar extends |
| <a id="merge-sorted-array"></a>[Merge Sorted Array (in place, from the back)](https://leetcode.com/problems/merge-sorted-array/) | fill from the largest end so you never overwrite unmerged values |
| <a id="move-zeroes"></a>[Move Zeroes](https://leetcode.com/problems/move-zeroes/) · [⇩ walkthrough](#move-zeroes) | two categories (nonzero vs zero); a single write-pointer packs nonzeros to the front |
| <a id="kth-largest-element-in-an-array"></a>[Partition (Quicksort step)](https://leetcode.com/problems/kth-largest-element-in-an-array/) | the same in-place split around a pivot that powers Quickselect |
| <a id="sort-array-by-parity"></a>[Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/) | partition into evens then odds with two pointers |
| <a id="sort-colors"></a>[Sort Colors](https://leetcode.com/problems/sort-colors/) | See the pattern chapter for the template. |
| <a id="squares-of-a-sorted-array"></a>[Sort Transformed Array](https://leetcode.com/problems/squares-of-a-sorted-array/) | after applying `ax²+bx+c` the extremes are at the ends (if `a>0`) or middle (if `a<0`); merge accordingly |
| <a id="trapping-rain-water-ii"></a>[Trapping Rain Water II (2D)](https://leetcode.com/problems/trapping-rain-water-ii/) | the "walls" are a whole grid boundary, so process cells outward from the lowest border using a min-heap |
| <a id="valid-palindrome-ii"></a>[Valid Palindrome / Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/) · [⇩ walkthrough](#valid-palindrome-ii) | compare from both ends inward; II allows one mismatch (try skipping either side) |
| <a id="wiggle-sort-ii"></a>[Wiggle Sort](https://leetcode.com/problems/wiggle-sort-ii/) | partition around the median, then interleave the two halves |

## [Fast / Slow Pointers](/patterns/fast-slow)

| Problem | Approach hint |
|---|---|
| <a id="find-the-duplicate-number"></a>[Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) · [⇩ walkthrough](#find-the-duplicate-number) | treat `nums[i]` as the next pointer and find the cycle entry |
| <a id="happy-number"></a>[Happy Number](https://leetcode.com/problems/happy-number/) | the "next" step is the sum of squared digits; a cycle means it's not happy |
| <a id="linked-list-cycle"></a>[Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | stop as soon as fast meets slow (detection only) |
| <a id="linked-list-cycle-ii"></a>[Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | See the pattern chapter for the template. |
| <a id="middle-of-the-linked-list"></a>[Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | fast moves 2×, slow 1× → slow lands on the middle |

## [Prefix Sum / Difference Array](/patterns/prefix-sum)

| Problem | Approach hint |
|---|---|
| <a id="range-addition-ii"></a>[2D — Range Addition II / stamping a grid](https://leetcode.com/problems/range-addition-ii/) | a 2D difference array marks the four corners of each rectangle |
| <a id="car-pooling"></a>[Car Pooling](https://leetcode.com/problems/car-pooling/) | a difference array over the *timeline* of pick-ups (+) and drop-offs (−); check capacity never overflows |
| <a id="contiguous-array"></a>[Contiguous Array (equal 0s and 1s)](https://leetcode.com/problems/contiguous-array/) · [⇩ walkthrough](#contiguous-array) | treat 0 as −1; a subarray is balanced when two prefixes are equal |
| <a id="continuous-subarray-sum"></a>[Continuous Subarray Sum (multiple of k)](https://leetcode.com/problems/continuous-subarray-sum/) | same `mod k` bucketing, but store the earliest index to enforce a length ≥ 2 |
| <a id="corporate-flight-bookings"></a>[Corporate Flight Bookings](https://leetcode.com/problems/corporate-flight-bookings/) | +seats at `first`, −seats after `last`; one sweep gives per-flight totals |
| <a id="count-submatrices-with-target-sum"></a>[Count Submatrices With Target Sum](https://leetcode.com/problems/count-submatrices-with-target-sum/) | fix a pair of rows, collapse columns to 1D prefix sums, then reuse the "subarray sum = k" hash-map count |
| <a id="matrix-block-sum"></a>[Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/) | answer each cell as the sum of a `k`-radius block using the same four-corner formula |
| <a id="maximal-rectangle"></a>[Maximal Square / Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | combine per-row prefix counts with a histogram/DP to bound the largest all-ones region |
| <a id="range-addition"></a>[Range Addition](https://leetcode.com/problems/range-addition/) · [⇩ walkthrough](#range-addition) | the canonical form — apply many `[l, r] += v` in O(1) each, reconstruct once |
| <a id="range-sum-query-2d-immutable"></a>[Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d-immutable/) | See the pattern chapter for the template. |
| <a id="subarray-sums-divisible-by-k"></a>[Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/) · [⇩ walkthrough](#subarray-sums-divisible-by-k) | key the map on `pre mod k` instead of the raw prefix |

## [Hashing (pattern)](/patterns/hashing)

| Problem | Approach hint |
|---|---|
| <a id="3sum"></a>[3Sum](https://leetcode.com/problems/3sum/) | need **three** numbers summing to 0, no duplicate triplets |
| <a id="candy"></a>[Candy](https://leetcode.com/problems/candy/) · [⇩ walkthrough](#candy) | each child must beat both neighbours |
| <a id="find-duplicate-file-in-system"></a>[Find Duplicate File in System](https://leetcode.com/problems/find-duplicate-file-in-system/) | same **content** |
| <a id="group-anagrams"></a>[Group Anagrams](https://leetcode.com/problems/group-anagrams/) | See the pattern chapter for the template. |
| <a id="group-shifted-strings"></a>[Group Shifted Strings](https://leetcode.com/problems/group-shifted-strings/) | same **shift pattern** (`"abc"`≡`"bcd"`) |
| <a id="isomorphic-strings"></a>[Isomorphic Strings](https://leetcode.com/problems/isomorphic-strings/) | same **structure** (`"egg"`≡`"add"`) |
| <a id="longest-consecutive-sequence"></a>[Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | 1-D runs of integers |
| <a id="maximum-product-subarray"></a>[Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) · [⇩ walkthrough](#maximum-product-subarray) | a negative flips sign |
| <a id="number-of-islands"></a>[Number of Islands](https://leetcode.com/problems/number-of-islands/) | 2-D grid connectivity |
| <a id="product-of-array-except-self"></a>[Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | See the pattern chapter for the template. |
| <a id="two-sum"></a>[Two Sum](https://leetcode.com/problems/two-sum/) | See the pattern chapter for the template. |
| <a id="two-sum-ii-input-array-is-sorted"></a>[Two Sum II — sorted input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · [⇩ walkthrough](#two-sum-ii-input-array-is-sorted) | the array is **already sorted** |
| <a id="two-sum-iii-data-structure-design"></a>[Two Sum III — design](https://leetcode.com/problems/two-sum-iii-data-structure-design/) | numbers **arrive over time**, many `find` queries |
| <a id="two-sum-less-than-k"></a>[Two Sum Less Than K](https://leetcode.com/problems/two-sum-less-than-k/) | largest pair sum strictly **&lt; K** |
| <a id="valid-anagram"></a>[Valid Anagram](https://leetcode.com/problems/valid-anagram/) · [⇩ walkthrough](#valid-anagram) | two strings, not a whole group |
| <a id="word-ladder"></a>[Word Ladder](https://leetcode.com/problems/word-ladder/) · [⇩ walkthrough](#word-ladder) | words linked by 1-letter edits |

## [Monotonic Stack](/patterns/monotonic-stack)

| Problem | Approach hint |
|---|---|
| <a id="daily-temperatures"></a>[Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | See the pattern chapter for the template. |
| <a id="next-greater-element-ii"></a>[Next Greater Element II (circular)](https://leetcode.com/problems/next-greater-element-ii/) | iterate the array twice (`i % n`) so wrap-around neighbours are considered |
| <a id="online-stock-span"></a>[Online Stock Span](https://leetcode.com/problems/online-stock-span/) · [⇩ walkthrough](#online-stock-span) | streaming version — push `(price, span)` and collapse spans of smaller prices as they arrive |
| <a id="remove-k-digits"></a>[Remove K Digits / Largest Rectangle variants](https://leetcode.com/problems/remove-k-digits/) | a monotonic stack that greedily pops to keep the sequence as small/large as possible |
| <a id="sum-of-subarray-minimums"></a>[Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | each element contributes `min × (countLeft × countRight)`; the monotonic stack gives those boundary counts |

## [Binary Search](/patterns/binary-search)

| Problem | Approach hint |
|---|---|
| <a id="find-minimum-in-rotated-sorted-array"></a>[Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | no target; steer toward the unsorted half, which is where the rotation point (the minimum) hides |
| <a id="find-peak-element"></a>[Find Peak Element](https://leetcode.com/problems/find-peak-element/) · [⇩ walkthrough](#find-peak-element) | no sorted array at all — just move toward the larger neighbour; you're guaranteed to climb to a peak |
| <a id="binary-search"></a>[Order-Agnostic Binary Search](https://leetcode.com/problems/binary-search/) | first peek at the ends to detect ascending vs descending, then flip the comparison accordingly |
| <a id="search-in-rotated-sorted-array-ii"></a>[Search in Rotated Array II (with duplicates)](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) | when `a[lo] == a[mid] == a[hi]` you can't tell which half is sorted, so shrink both ends by one (worst case degrades to O(n)) |
| <a id="search-in-rotated-sorted-array"></a>[Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | See the pattern chapter for the template. |

## [Binary Search on the Answer](/patterns/bs-on-answer)

| Problem | Approach hint |
|---|---|
| <a id="capacity-to-ship-packages-within-d-days"></a>[Capacity to Ship Packages in D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) · [⇩ walkthrough](#capacity-to-ship-packages-within-d-days) | guess a ship capacity; feasibility = "can we finish in ≤ D days at this capacity?" |
| <a id="divide-chocolate"></a>[Divide Chocolate / Maximize the Minimum](https://leetcode.com/problems/divide-chocolate/) | flip it — maximize the smallest piece, so `feasible(x)` = "can make ≥ k pieces each ≥ x." |
| <a id="find-k-th-smallest-pair-distance"></a>[Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/) | binary-search the distance; feasibility counts pairs within it via a sliding window |
| <a id="koko-eating-bananas"></a>[Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | guess a speed; feasibility = "finishes within H hours?" |
| <a id="median-of-two-sorted-arrays"></a>[Kth Element of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | the general form — binary-search a partition so `k` elements sit on the left |
| <a id="kth-smallest-element-in-a-sorted-matrix"></a>[Median of a Row-wise Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) · [⇩ walkthrough](#kth-smallest-element-in-a-sorted-matrix) | binary-search the value and count how many are ≤ mid |
| <a id="minimize-max-distance-to-gas-station"></a>[Minimize Max Distance to Gas Station](https://leetcode.com/problems/minimize-max-distance-to-gas-station/) | guess a distance; feasibility counts how many stations you'd have to add (works on real numbers, so fix an iteration count or epsilon) |
| <a id="path-with-minimum-effort"></a>[Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | binary-search the max allowed step height; feasibility is a BFS/DFS connectivity check |
| <a id="split-array-largest-sum"></a>[Split Array Largest Sum / Book Allocation](https://leetcode.com/problems/split-array-largest-sum/) | guess a max segment sum; feasibility = "≤ m parts needed?" |

## [Top-K / Heap](/patterns/top-k-heap)

| Problem | Approach hint |
|---|---|
| <a id="k-closest-points-to-origin"></a>[K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) · [⇩ walkthrough](#k-closest-points-to-origin) | a **max**-heap of size k keyed on distance; the farthest of your current best sits on top, ready to be evicted |
| <a id="kth-largest-element-in-a-stream"></a>[Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | keep a size-k **min**-heap alive across `add` calls; its root is always the running kth largest |
| <a id="top-k-frequent-elements"></a>[Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | heap keyed on frequency (or, for O(n), bucket by frequency and read the top buckets) |

## [K-way Merge](/patterns/k-way-merge)

| Problem | Approach hint |
|---|---|
| <a id="add-two-numbers"></a>[Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | walk both lists together carrying a digit, building the result node by node |
| <a id="merge-k-sorted-lists"></a>[Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | a min-heap of the `k` current heads yields the global next-smallest |
| <a id="merge-two-sorted-lists"></a>[Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | the base case — a dummy-head splice, no heap needed |
| <a id="smallest-range-covering-elements-from-k-lists"></a>[Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/) | the range spans the heap min and the running max of tops |
| <a id="sort-list"></a>[Sort List](https://leetcode.com/problems/sort-list/) | merge sort *on a list* — split by fast/slow, recurse, then merge two halves |
| <a id="ugly-number-ii"></a>[Ugly Number II / Super Ugly Number](https://leetcode.com/problems/ugly-number-ii/) | the streams are the sequence multiplied by each prime factor |

## [Merge Intervals](/patterns/merge-intervals)

| Problem | Approach hint |
|---|---|
| <a id="employee-free-time"></a>[Employee Free Time](https://leetcode.com/problems/employee-free-time/) | merge everyone's busy intervals; the gaps between merged blocks are the free time |
| <a id="insert-interval"></a>[Insert Interval](https://leetcode.com/problems/insert-interval/) · [⇩ walkthrough](#insert-interval) | three phases — copy intervals before, merge those overlapping the new one, copy the rest |
| <a id="interval-list-intersections"></a>[Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/) | two pointers; each overlap is `[max(starts), min(ends)]` |
| <a id="merge-intervals"></a>[Merge Intervals](https://leetcode.com/problems/merge-intervals/) | See the pattern chapter for the template. |
| <a id="remove-covered-intervals"></a>[Remove Covered Intervals](https://leetcode.com/problems/remove-covered-intervals/) | sort by start (then end desc) and count intervals not swallowed by a previous one |

## [Sweep Line](/patterns/sweep-line)

| Problem | Approach hint |
|---|---|
| <a id="meeting-rooms-ii"></a>[Minimum Number of Platforms](https://leetcode.com/problems/meeting-rooms-ii/) | peak of simultaneously-present trains |
| <a id="my-calendar-ii"></a>[My Calendar II / III](https://leetcode.com/problems/my-calendar-ii/) | a `TreeMap` of +1/−1 deltas; the max running prefix is the max overlap |
| <a id="the-skyline-problem"></a>[The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) | sweep x-coordinates with a max-heap of active building heights |

## [Topological Sort](/patterns/topological-sort)

| Problem | Approach hint |
|---|---|
| <a id="alien-dictionary"></a>[Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) | build edges by comparing adjacent words' first differing character, then topo-sort the alphabet |
| <a id="course-schedule-ii"></a>[Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | emit the actual order, not just "is it possible?" |
| <a id="minimum-height-trees"></a>[Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) | peel leaves layer by layer on an undirected tree; the last 1–2 remaining are the centroids |
| <a id="parallel-courses"></a>[Parallel Courses](https://leetcode.com/problems/parallel-courses/) | count the number of Kahn "waves" — that's the minimum number of semesters |

## [Union-Find (DSU)](/patterns/union-find)

| Problem | Approach hint |
|---|---|
| <a id="accounts-merge"></a>[Accounts Merge](https://leetcode.com/problems/accounts-merge/) | union accounts that share any email, then group emails by root |
| <a id="connecting-cities-with-minimum-cost"></a>[Connecting Cities With Minimum Cost](https://leetcode.com/problems/connecting-cities-with-minimum-cost/) | plain Kruskal on the given edge list; return −1 if it stays disconnected |
| <a id="find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree"></a>[Find Critical and Pseudo-Critical Edges](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/) | rerun MST forcing each edge in / leaving it out to classify it |
| <a id="min-cost-to-connect-all-points"></a>[Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) | the graph is implicit — every pair of points is an edge weighted by Manhattan distance |
| <a id="most-stones-removed-with-same-row-or-column"></a>[Most Stones Removed](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/) | union stones sharing a row or column; removable = total − components |
| <a id="number-of-islands-ii"></a>[Number of Islands II](https://leetcode.com/problems/number-of-islands-ii/) | online — union each newly added land cell with its neighbours, tracking the component count |
| <a id="number-of-provinces"></a>[Number of Provinces](https://leetcode.com/problems/number-of-provinces/) · [⇩ walkthrough](#number-of-provinces) | union adjacent friends; the answer is the count of distinct roots |
| <a id="optimize-water-distribution-in-a-village"></a>[Optimize Water Distribution in a Village](https://leetcode.com/problems/optimize-water-distribution-in-a-village/) | model each well as an edge from a virtual node 0, then run MST |
| <a id="redundant-connection"></a>[Redundant Connection](https://leetcode.com/problems/redundant-connection/) | the answer is the first edge whose two endpoints are *already* connected |

## [Greedy](/patterns/greedy)

| Problem | Approach hint |
|---|---|
| <a id="best-time-to-buy-and-sell-stock"></a>[Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) · [⇩ walkthrough](#best-time-to-buy-and-sell-stock) | track the min price so far and the best profit against it |
| <a id="course-schedule-iii"></a>[Course Schedule III](https://leetcode.com/problems/course-schedule-iii/) | sort by deadline; greedily take courses, dropping the longest with a max-heap when you overrun |
| <a id="gas-station"></a>[Gas Station](https://leetcode.com/problems/gas-station/) | reset the start to `i+1` when the tank dips below 0, with a global feasibility gate |
| <a id="jump-game"></a>[Jump Game I](https://leetcode.com/problems/jump-game/) | just track the farthest reachable index; return whether it reaches the end |
| <a id="jump-game-ii"></a>[Jump Game II](https://leetcode.com/problems/jump-game-ii/) | See the pattern chapter for the template. |
| <a id="jump-game-iii"></a>[Jump Game III](https://leetcode.com/problems/jump-game-iii/) | actual BFS/DFS since you can jump both directions by `arr[i]` |
| <a id="maximum-length-of-pair-chain"></a>[Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) | the same earliest-finish chain, counting length |
| <a id="minimum-number-of-arrows-to-burst-balloons"></a>[Minimum Number of Arrows](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | the interval-cover cousin (sort by end) |
| <a id="non-overlapping-intervals"></a>[Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | removals = total − (max non-overlapping kept) |
| <a id="task-scheduler"></a>[Task Scheduler](https://leetcode.com/problems/task-scheduler/) | See the pattern chapter for the template. |
| <a id="video-stitching"></a>[Video Stitching / Minimum Number of Taps](https://leetcode.com/problems/video-stitching/) | the same "cover the line in fewest intervals" farthest-reach greedy |

## [Recursion & Backtracking](/patterns/backtracking)

| Problem | Approach hint |
|---|---|
| <a id="beautiful-arrangement"></a>[Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/) | place numbers `1..n` where position `i` must divide (or be divided by) the value |
| <a id="combination-sum"></a>[Combination Sum](https://leetcode.com/problems/combination-sum/) | See the pattern chapter for the template. |
| <a id="combination-sum-ii"></a>[Combination Sum / Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) · [⇩ walkthrough](#combination-sum-ii) | carry a remaining-target budget; allow reuse by recursing with the same `i` (unbounded) or forbid it with `i+1` (each item once) |
| <a id="combination-sum-iii"></a>[Combination Sum III](https://leetcode.com/problems/combination-sum-iii/) | exactly `k` numbers drawn from `1..9` summing to `n` |
| <a id="combination-sum-iv"></a>[Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) | it *counts ordered* ways → drop backtracking for a 1-D DP (`dp[t] += dp[t-num]`) |
| <a id="letter-case-permutation"></a>[Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/) | at each letter, branch into lower/upper case |
| <a id="letter-combinations-of-a-phone-number"></a>[Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | the "constraint" is just the digit→letters map; place one letter per position |
| <a id="n-queens"></a>[N-Queens](https://leetcode.com/problems/n-queens/) | See the pattern chapter for the template. |
| <a id="n-queens-ii"></a>[N-Queens II](https://leetcode.com/problems/n-queens-ii/) | just *count* the valid placements instead of listing boards |
| <a id="next-permutation"></a>[Next Permutation](https://leetcode.com/problems/next-permutation/) | in-place — find the pivot, swap with its next-larger suffix element, reverse the suffix |
| <a id="palindrome-partitioning"></a>[Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) · [⇩ walkthrough](#palindrome-partitioning) | a "choice" is a prefix that happens to be a palindrome; recurse on the rest |
| <a id="permutations"></a>[Permutations](https://leetcode.com/problems/permutations/) | order matters, so drop the `start` index and instead track a `used[]` array, scanning all positions each level |
| <a id="permutations-ii"></a>[Permutations II (with duplicates)](https://leetcode.com/problems/permutations-ii/) · [⇩ walkthrough](#permutations-ii) | sort, then skip `i>0 && a[i]==a[i-1] && !used[i-1]` to avoid duplicate orderings |
| <a id="robot-room-cleaner"></a>[Robot Room Cleaner](https://leetcode.com/problems/robot-room-cleaner/) | same visited-set DFS, but you only know relative moves (turn/forward) |
| <a id="subsets-ii"></a>[Subsets II (with duplicates)](https://leetcode.com/problems/subsets-ii/) · [⇩ walkthrough](#subsets-ii) | sort first, then skip equal siblings (`i > start && a[i] == a[i-1]`) so you don't emit the same subset twice |
| <a id="sudoku-solver"></a>[Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) | three occupancy sets (row, column, 3×3 box); place a digit, recurse, undo |
| <a id="unique-paths-iii"></a>[Unique Paths III](https://leetcode.com/problems/unique-paths-iii/) | backtrack across the grid, requiring you visit *every* empty cell exactly once |
| <a id="valid-sudoku"></a>[Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) | no search at all — only check the occupancy sets for conflicts |
| <a id="word-search"></a>[Word Search](https://leetcode.com/problems/word-search/) | See the pattern chapter for the template. |
| <a id="word-search-ii"></a>[Word Search II](https://leetcode.com/problems/word-search-ii/) | many target words → back the grid DFS with a **Trie** so all words are pruned at once |

## [Divide & Conquer](/patterns/divide-conquer)

| Problem | Approach hint |
|---|---|
| <a id="count-of-range-sum"></a>[Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) | run merge sort over the **prefix sums**, counting sums in `[lower, upper]` |
| <a id="count-of-smaller-numbers-after-self"></a>[Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | count how many right-half elements slot in before each left element |
| <a id="reverse-pairs"></a>[Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | before merging, count pairs with `a[i] > 2·a[j]` |

## [Dynamic Programming](/patterns/dp)

| Problem | Approach hint |
|---|---|
| <a id="best-time-to-buy-and-sell-stock-with-cooldown"></a>[Best Time to Buy/Sell with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) · [⇩ walkthrough](#best-time-to-buy-and-sell-stock-with-cooldown) | states `hold / sold / rest`; selling forces a rest day |
| <a id="best-time-to-buy-and-sell-stock-iv"></a>[Best Time with at most k Transactions](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) | add a transaction-count dimension to the state |
| <a id="best-time-to-buy-and-sell-stock-with-transaction-fee"></a>[Best Time with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) | subtract the fee on each sell transition |
| <a id="climbing-stairs"></a>[Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | `dp[i] = dp[i-1] + dp[i-2]` (count ways, no conflict) |
| <a id="coin-change"></a>[Coin Change (min coins)](https://leetcode.com/problems/coin-change/) · [⇩ walkthrough](#coin-change) | unbounded items → loop capacity **upward**, take `min(dp[w], dp[w-coin]+1)` |
| <a id="coin-change-ii"></a>[Coin Change II (count ways)](https://leetcode.com/problems/coin-change-ii/) | `dp[a] += dp[a−coin]`, with **coins in the outer loop** so each combination is counted once (order ignored) |
| <a id="delete-and-earn"></a>[Delete and Earn](https://leetcode.com/problems/delete-and-earn/) | bucket the array by value, then it's House Robber over `value × count` |
| <a id="dungeon-game"></a>[Dungeon Game](https://leetcode.com/problems/dungeon-game/) | fill the grid **backwards** from the goal, because required health propagates in reverse |
| <a id="edit-distance"></a>[Edit Distance](https://leetcode.com/problems/edit-distance/) · [⇩ walkthrough](#edit-distance) | mismatch costs `1 + min(insert, delete, replace)` |
| <a id="house-robber"></a>[House Robber](https://leetcode.com/problems/house-robber/) | See the pattern chapter for the template. |
| <a id="house-robber-ii"></a>[House Robber II](https://leetcode.com/problems/house-robber-ii/) | houses in a circle → run the linear DP twice (exclude first, exclude last) and take the max |
| <a id="last-stone-weight-ii"></a>[Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/) | minimize ` |
| <a id="longest-common-subsequence"></a>[Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | match → `dp[i-1][j-1]+1`, else `max(dp[i-1][j], dp[i][j-1])` |
| <a id="longest-increasing-subsequence"></a>[Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) · [⇩ walkthrough](#longest-increasing-subsequence) | single sequence → patience sorting with binary search for |
| <a id="longest-palindromic-subsequence"></a>[Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | LCS of `s` and `reverse(s)` |
| <a id="burst-balloons"></a>[Matrix Chain Multiplication](https://leetcode.com/problems/burst-balloons/) | `k` is the last multiplication point; cost combines the two sub-products |
| <a id="maximal-square"></a>[Maximal Square](https://leetcode.com/problems/maximal-square/) | `dp = min(up, left, up-left) + 1` for the largest all-ones square |
| <a id="maximum-sum-circular-subarray"></a>[Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) | answer = max(normal Kadane, total − **min**-subarray) |
| <a id="min-cost-climbing-stairs"></a>[Min Cost Climbing Stairs / Paint Fence](https://leetcode.com/problems/min-cost-climbing-stairs/) | the same 1-D recurrence with a per-step cost or an adjacency constraint |
| <a id="minimum-cost-to-merge-stones"></a>[Minimum Cost to Merge Stones](https://leetcode.com/problems/minimum-cost-to-merge-stones/) | merge in groups of `k`; the split respects `(len-1) % (k-1)` |
| <a id="minimum-falling-path-sum"></a>[Minimum Path Sum / Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/) | **min** of the neighbours plus the cell |
| <a id="number-of-ways-to-wear-different-hats-to-each-other"></a>[Number of Ways to Assign (hats/jobs)](https://leetcode.com/problems/number-of-ways-to-wear-different-hats-to-each-other/) | iterate the mask of assigned people, adding one compatible assignment at a time |
| <a id="paint-house-ii"></a>[Paint House I/II](https://leetcode.com/problems/paint-house-ii/) | the state is the last colour used; the transition forbids repeating it |
| <a id="palindrome-partitioning-ii"></a>[Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/) | min cuts via an interval palindrome table |
| <a id="partition-equal-subset-sum"></a>[Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | target = `sum/2`; the boolean knapsack asks if it's reachable |
| <a id="partition-to-k-equal-sum-subsets"></a>[Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) | track the used-element mask plus the current bucket's remaining capacity |
| <a id="perfect-squares"></a>[Perfect Squares](https://leetcode.com/problems/perfect-squares/) | the "coins" are the square numbers `1, 4, 9, 16, …`; minimize the count |
| <a id="regular-expression-matching"></a>[Regex / Wildcard Matching](https://leetcode.com/problems/regular-expression-matching/) | the same grid, with `*` allowing "skip" or "repeat" transitions |
| <a id="shortest-path-visiting-all-nodes"></a>[Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | BFS over `(node, mask)` states — shortest walk covering every node |
| <a id="target-sum"></a>[Target Sum](https://leetcode.com/problems/target-sum/) | assigning ± signs reduces to "subset summing to `(sum+target)/2`" → count instead of boolean |
| <a id="find-the-shortest-superstring"></a>[Travelling Salesman](https://leetcode.com/problems/find-the-shortest-superstring/) | `dp[mask][i]` = cheapest route visiting `mask`, ending at `i` |
| <a id="unique-paths"></a>[Unique Paths](https://leetcode.com/problems/unique-paths/) · [⇩ walkthrough](#unique-paths) | See the pattern chapter for the template. |
| <a id="unique-paths-ii"></a>[Unique Paths / Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | **add** the two neighbours to count paths (obstacles set the cell to 0) |

## [Trie (pattern)](/patterns/trie-pattern)

| Problem | Approach hint |
|---|---|
| <a id="concatenated-words"></a>[Concatenated Words](https://leetcode.com/problems/concatenated-words/) | a trie of all words + DFS to test whether a word is built from shorter ones |
| <a id="count-pairs-with-xor-in-a-range"></a>[Count Pairs With XOR in a Range](https://leetcode.com/problems/count-pairs-with-xor-in-a-range/) | store subtree counts in the binary trie and count paths whose XOR falls in `[low, high]` |
| <a id="maximum-xor-of-two-numbers-in-an-array"></a>[Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) | See the pattern chapter for the template. |
| <a id="maximum-xor-with-an-element-from-array"></a>[Maximum XOR With an Element From Array](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/) | answer queries offline, sorting by the value bound and inserting numbers as they become allowed |
| <a id="replace-words"></a>[Replace Words / IP routing](https://leetcode.com/problems/replace-words/) | the same MSB-first bit walk used for longest-prefix matching |
| <a id="stream-of-characters"></a>[Stream of Characters](https://leetcode.com/problems/stream-of-characters/) | store words *reversed* in a trie and match the incoming stream from the back |

## [Bit Manipulation](/patterns/bit-manip)

| Problem | Approach hint |
|---|---|
| <a id="counting-bits"></a>[Counting Bits](https://leetcode.com/problems/counting-bits/) · [⇩ walkthrough](#counting-bits) | See the pattern chapter for the template. |
| <a id="find-the-difference"></a>[Find the Difference / Set Mismatch](https://leetcode.com/problems/find-the-difference/) | XOR the two collections so shared characters cancel, leaving the odd one out |
| <a id="hamming-distance"></a>[Hamming Distance](https://leetcode.com/problems/hamming-distance/) | `Integer.bitCount(a ^ b)` — count differing bits |
| <a id="maximum-product-of-word-lengths"></a>[Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/) | encode each word's letters as a 26-bit mask; two words share no letter iff `maskA & maskB == 0` |
| <a id="missing-number"></a>[Missing Number](https://leetcode.com/problems/missing-number/) · [⇩ walkthrough](#missing-number) | XOR all indices `0..n` with all values; the survivor is the missing one |
| <a id="number-of-1-bits"></a>[Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | Brian Kernighan's `x &= x - 1` clears the lowest set bit each step |
| <a id="power-of-two"></a>[Power of Two](https://leetcode.com/problems/power-of-two/) | `x > 0 && (x & (x-1)) == 0` |
| <a id="reverse-bits"></a>[Reverse Bits](https://leetcode.com/problems/reverse-bits/) | shift bits out of one int and into another, one position at a time |
| <a id="single-number"></a>[Single Number](https://leetcode.com/problems/single-number/) | See the pattern chapter for the template. |
| <a id="subsets"></a>[Subsets](https://leetcode.com/problems/subsets/) | loop masks `0 .. 2ⁿ-1`; bit `i` set means element `i` is included |
| <a id="sum-of-all-subset-xor-totals"></a>[Sum of All Subset XOR / SOS DP](https://leetcode.com/problems/sum-of-all-subset-xor-totals/) | enumerate submasks with `for (s = m; s > 0; s = (s-1) & m)` |

## [Math & Number Theory](/patterns/math)

| Problem | Approach hint |
|---|---|
| <a id="count-primes"></a>[Count Primes](https://leetcode.com/problems/count-primes/) | count marks left unmarked |
| <a id="fraction-to-recurring-decimal"></a>[Fraction to Recurring Decimal](https://leetcode.com/problems/fraction-to-recurring-decimal/) | track remainders to find the repeating cycle |
| <a id="greatest-common-divisor-of-strings"></a>[GCD of Strings](https://leetcode.com/problems/greatest-common-divisor-of-strings/) | GCD of lengths; verify `s+t == t+s` |
| <a id="fibonacci-number"></a>[Matrix exponentiation](https://leetcode.com/problems/fibonacci-number/) | base is a matrix → nth Fibonacci / linear recurrence |
| <a id="powx-n"></a>[Pow(x, n)](https://leetcode.com/problems/powx-n/) | real base, handle negative exponent |
| <a id="super-pow"></a>[Super Pow](https://leetcode.com/problems/super-pow/) | huge exponent as a digit array, mod 1337 |
| <a id="water-and-jug-problem"></a>[Water and Jug Problem](https://leetcode.com/problems/water-and-jug-problem/) | feasible iff `target % gcd(x,y) == 0` (Bézout) |

## [Design & Randomized](/patterns/design)

| Problem | Approach hint |
|---|---|
| <a id="insert-delete-getrandom-o1"></a>[Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | map value→index + swap-with-last |
| <a id="linked-list-random-node"></a>[Linked List Random Node](https://leetcode.com/problems/linked-list-random-node/) | single reservoir of size 1 |
| <a id="lru-cache"></a>[LRU Cache](https://leetcode.com/problems/lru-cache/) | map + doubly-linked list for recency |
| <a id="random-pick-index"></a>[Random Pick Index](https://leetcode.com/problems/random-pick-index/) | reservoir over indices matching a target |
| <a id="random-pick-with-weight"></a>[Random Pick with Weight](https://leetcode.com/problems/random-pick-with-weight/) · [⇩ walkthrough](#random-pick-with-weight) | prefix-sum array + binary search |
| <a id="shuffle-an-array"></a>[Shuffle an Array](https://leetcode.com/problems/shuffle-an-array/) · [⇩ walkthrough](#shuffle-an-array) | Fisher–Yates: swap i with random ≤ i |
| <a id="insert-delete-getrandom-o1-duplicates-allowed"></a>[… Duplicates allowed](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/) | map value→**set** of indices |

## [Arrays (DS)](/data-structures/arrays)

| Problem | Approach hint |
|---|---|
| <a id="find-all-numbers-disappeared-in-an-array"></a>[Find All Numbers Disappeared / Find All Duplicates](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/) · [⇩ walkthrough](#find-all-numbers-disappeared-in-an-array) | scan for *every* wrong slot instead of the first |
| <a id="first-missing-positive"></a>[First Missing Positive](https://leetcode.com/problems/first-missing-positive/) | ignore values outside `1..n`; the answer lies in `1..n+1` |
| <a id="rotate-image"></a>[Rotate Image](https://leetcode.com/problems/rotate-image/) | transpose + reverse rows (90° CW) |
| <a id="search-a-2d-matrix"></a>[Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) · [⇩ walkthrough](#search-a-2d-matrix) | treat the grid as one sorted array → binary search |
| <a id="search-a-2d-matrix-ii"></a>[Search a 2D Matrix II](https://leetcode.com/problems/search-a-2d-matrix-ii/) · [⇩ walkthrough](#search-a-2d-matrix-ii) | start top-right; go left on bigger, down on smaller |
| <a id="set-matrix-zeroes"></a>[Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | border-as-marker + `col0` flag |
| <a id="set-mismatch"></a>[Set Mismatch](https://leetcode.com/problems/set-mismatch/) | the single wrong slot reveals both the duplicated and the missing number |
| <a id="spiral-matrix"></a>[Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | See the pattern chapter for the template. |
| <a id="spiral-matrix-ii"></a>[Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) · [⇩ walkthrough](#spiral-matrix-ii) | *write* `1..n²` along the same spiral bounds |

## [Strings](/data-structures/strings)

| Problem | Approach hint |
|---|---|
| <a id="encode-and-decode-strings"></a>[Encode and Decode Strings](https://leetcode.com/problems/encode-and-decode-strings/) | See the pattern chapter for the template. |
| <a id="encode-and-decode-tinyurl"></a>[Encode/Decode TinyURL](https://leetcode.com/problems/encode-and-decode-tinyurl/) | map long↔short with a counter or base-62 id instead of embedding the payload |
| <a id="palindromic-substrings"></a>[Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | count every successful expansion instead of keeping only the longest |
| <a id="serialize-and-deserialize-n-ary-tree"></a>[Serialize N-ary Tree](https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/) | prefix each node with its child count so the parser knows when to stop |
| <a id="serialize-and-deserialize-binary-tree"></a>[Serialize/Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | pre-order with `#` null markers makes the traversal reversible |
| <a id="shortest-palindrome"></a>[Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/) | use the KMP failure function on `s + '#' + reverse(s)` to find the longest palindromic prefix |

## [Linked Lists](/data-structures/linked-lists)

| Problem | Approach hint |
|---|---|
| <a id="all-oone-data-structure"></a>[All O`one Data Structure](https://leetcode.com/problems/all-oone-data-structure/) | buckets of equal-count keys threaded in a doubly linked list for O(1) min/max |
| <a id="design-browser-history"></a>[Design Browser History](https://leetcode.com/problems/design-browser-history/) | a doubly linked list of pages with back/forward pointers |
| <a id="lfu-cache"></a>[LFU Cache](https://leetcode.com/problems/lfu-cache/) | add frequency buckets (a map from frequency → ordered list) alongside the key map |
| <a id="palindrome-linked-list"></a>[Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | reverse the second half and compare it against the first |
| <a id="reorder-list"></a>[Reorder List](https://leetcode.com/problems/reorder-list/) | reverse the second half, then interleave it with the first |
| <a id="reverse-linked-list"></a>[Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | See the pattern chapter for the template. |
| <a id="reverse-linked-list-ii"></a>[Reverse Linked List II (sublist)](https://leetcode.com/problems/reverse-linked-list-ii/) | reverse only the nodes in `[left, right]`, then stitch the ends back |
| <a id="reverse-nodes-in-k-group"></a>[Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) · [⇩ walkthrough](#reverse-nodes-in-k-group) | reverse each block of `k` and reconnect blocks (leave a trailing remainder as-is) |
| <a id="rotate-list"></a>[Rotate List](https://leetcode.com/problems/rotate-list/) | find the new tail `k` from the end, then relink into a rotation |
| <a id="swap-nodes-in-pairs"></a>[Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) | the `k = 2` special case |

## [Stacks & Queues](/data-structures/stacks-queues)

| Problem | Approach hint |
|---|---|
| <a id="basic-calculator"></a>[Basic Calculator I/II](https://leetcode.com/problems/basic-calculator/) | push running values and signs; resolve on operators and closing brackets |
| <a id="decode-string"></a>[Decode String](https://leetcode.com/problems/decode-string/) | push `(repeatCount, prefix)` on `[`, pop and expand on `]` |
| <a id="longest-valid-parentheses"></a>[Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | keep a stack of indices to measure the length of each valid span |
| <a id="max-stack"></a>[Max Stack](https://leetcode.com/problems/max-stack/) | track a running max per entry (or a second stack) for O(1) `peekMax` |
| <a id="minimum-remove-to-make-valid-parentheses"></a>[Min Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/) | push indices of unmatched `(`; drop leftovers at the end |
| <a id="min-stack"></a>[Min Stack](https://leetcode.com/problems/min-stack/) | See the pattern chapter for the template. |
| <a id="sliding-window-maximum"></a>[Sliding Window Minimum/Maximum](https://leetcode.com/problems/sliding-window-maximum/) | the queue version — a monotonic deque holding candidate extremes |
| <a id="valid-parentheses"></a>[Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | See the pattern chapter for the template. |

## [Trees](/data-structures/trees)

| Problem | Approach hint |
|---|---|
| <a id="average-of-levels-in-binary-tree"></a>[Average of Levels](https://leetcode.com/problems/average-of-levels-in-binary-tree/) | sum ÷ count for each level |
| <a id="balanced-binary-tree"></a>[Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/) | return height, but short-circuit with `-1` the moment a subtree is unbalanced |
| <a id="binary-tree-cameras"></a>[Binary Tree Cameras](https://leetcode.com/problems/binary-tree-cameras/) | return a 3-state (has-camera / covered / needs-cover) and place cameras greedily from the leaves up |
| <a id="binary-tree-maximum-path-sum"></a>[Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | return the best single branch, but update the global with left+node+right (clamp negative branches to 0) |
| <a id="construct-binary-tree-from-preorder-and-inorder-traversal"></a>[Construct Binary Tree from Preorder and Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | See the pattern chapter for the template. |
| <a id="construct-binary-search-tree-from-preorder-traversal"></a>[Construct BST from Preorder](https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/) | no inorder needed — split children using value bounds |
| <a id="construct-binary-tree-from-inorder-and-postorder-traversal"></a>[Construct from Inorder + Postorder](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) | consume postorder from the **back**, building the right subtree before the left |
| <a id="construct-binary-tree-from-preorder-and-postorder-traversal"></a>[Construct from Preorder + Postorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-postorder-traversal/) | works only for *full* trees; the second preorder value marks the left subtree's root |
| <a id="construct-string-from-binary-tree"></a>[Construct String from Binary Tree](https://leetcode.com/problems/construct-string-from-binary-tree/) | parenthesised encoding `1(2)(3)` that stays reversible |
| <a id="convert-binary-search-tree-to-sorted-doubly-linked-list"></a>[Convert BST to Sorted Doubly Linked List](https://leetcode.com/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/) | thread `prev`/`next` pointers as you visit in order |
| <a id="convert-sorted-array-to-binary-search-tree"></a>[Convert Sorted Array/List to BST](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) | the middle element is the root → balanced BST |
| <a id="diameter-of-n-ary-tree"></a>[Diameter of an N-ary Tree](https://leetcode.com/problems/diameter-of-n-ary-tree/) | combine the two largest child depths instead of left/right |
| <a id="diameter-of-binary-tree"></a>[Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) | See the pattern chapter for the template. |
| <a id="lowest-common-ancestor-of-a-binary-tree"></a>[Distance Between Two Nodes](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | `depth(p) + depth(q) − 2·depth(lca)` |
| <a id="distribute-coins-in-binary-tree"></a>[Distribute Coins in Binary Tree](https://leetcode.com/problems/distribute-coins-in-binary-tree/) | return each subtree's surplus/deficit; sum ` |
| <a id="find-duplicate-subtrees"></a>[Find Duplicate Subtrees](https://leetcode.com/problems/find-duplicate-subtrees/) | serialize every subtree to a string, hash them, and report repeats |
| <a id="house-robber-iii"></a>[House Robber III](https://leetcode.com/problems/house-robber-iii/) | return `{rob, skip}`; robbing a node forbids robbing its children |
| <a id="kth-smallest-element-in-a-bst"></a>[Kth Smallest in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) · [⇩ walkthrough](#kth-smallest-element-in-a-bst) | do an in-order walk and stop after the kth node |
| <a id="lowest-common-ancestor-of-a-binary-search-tree"></a>[LCA of a BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | use the ordering — descend left/right until the two targets split, no full search |
| <a id="lowest-common-ancestor-of-deepest-leaves"></a>[LCA of Deepest Leaves](https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/) | return `(depth, node)` upward and keep the node whose subtree holds the deepest leaves |
| <a id="lowest-common-ancestor-of-a-binary-tree-iii"></a>[LCA with Parent Pointers](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree-iii/) | walk up both ancestor chains and align lengths (like linked-list intersection) |
| <a id="longest-univalue-path"></a>[Longest Univalue Path](https://leetcode.com/problems/longest-univalue-path/) | extend a branch only through children with the same value |
| <a id="longest-zigzag-path-in-a-binary-tree"></a>[Longest ZigZag Path](https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/) | return `{leftLen, rightLen}` and update a global maximum |
| <a id="minimum-depth-of-binary-tree"></a>[Minimum Depth](https://leetcode.com/problems/minimum-depth-of-binary-tree/) | return as soon as you hit the first leaf (BFS finds it earliest) |
| <a id="range-sum-of-bst"></a>[Range Sum of BST](https://leetcode.com/problems/range-sum-of-bst/) | prune whole subtrees that fall entirely outside `[low, high]` |
| <a id="recover-binary-search-tree"></a>[Recover BST](https://leetcode.com/problems/recover-binary-search-tree/) | the in-order sequence has exactly two out-of-order nodes; find and swap them |
| <a id="binary-tree-right-side-view"></a>[Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) · [⇩ walkthrough](#binary-tree-right-side-view) | keep the last node of each level |
| <a id="serialize-and-deserialize-bst"></a>[Serialize/Deserialize BST](https://leetcode.com/problems/serialize-and-deserialize-bst/) | no null markers needed — rebuild using value bounds since it's ordered |
| <a id="validate-binary-search-tree"></a>[Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/) | See the pattern chapter for the template. |
| <a id="binary-tree-zigzag-level-order-traversal"></a>[Zigzag Level Order](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | reverse the collected list on alternate levels |

## [Heaps (DS)](/data-structures/heaps)

| Problem | Approach hint |
|---|---|
| <a id="find-median-from-data-stream"></a>[Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | the base case — balance the two heaps on every insert |
| <a id="ipo"></a>[IPO / Maximize Capital](https://leetcode.com/problems/ipo/) | a min-heap unlocks projects you can afford, a max-heap picks the most profitable of those |
| <a id="sliding-window-median"></a>[Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) | add lazy deletion so the element leaving the window is discarded from whichever heap holds it |

## [Tries](/data-structures/trie)

| Problem | Approach hint |
|---|---|
| <a id="design-add-and-search-words-data-structure"></a>[Add and Search Word (wildcard `.`)](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | on a `.`, recurse into *all* children at that position (DFS instead of a single step) |
| <a id="implement-trie-prefix-tree"></a>[Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | See the pattern chapter for the template. |
| <a id="longest-word-in-dictionary"></a>[Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/) | accept a word only if every one of its prefixes is also a stored word |
| <a id="map-sum-pairs"></a>[Map Sum Pairs](https://leetcode.com/problems/map-sum-pairs/) | store a value at each terminal and sum the values in the subtree under a prefix |

## [Graphs](/data-structures/graphs)

| Problem | Approach hint |
|---|---|
| <a id="01-matrix"></a>[01 Matrix](https://leetcode.com/problems/01-matrix/) | sources are all the 0-cells; each 1-cell gets its distance to the nearest 0 |
| <a id="find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance"></a>[All-pairs, small V](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/) | switch to **Floyd–Warshall** — `dp[i][j] = min(dp[i][j], dp[i][k]+dp[k][j])` |
| <a id="as-far-from-land-as-possible"></a>[As Far From Land as Possible](https://leetcode.com/problems/as-far-from-land-as-possible/) | sources are all land cells; the answer is the last water cell reached (max distance) |
| <a id="cheapest-flights-within-k-stops"></a>[Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | add a stop-budget dimension, or run Bellman–Ford for exactly `K+1` rounds |
| <a id="clone-graph"></a>[Clone Graph](https://leetcode.com/problems/clone-graph/) | a `Map<Node,Node>` original→copy doubles as the visited set; wire neighbours on first visit |
| <a id="course-schedule"></a>[Course Schedule (cycle detect)](https://leetcode.com/problems/course-schedule/) | the map stores a 3-colour state (unvisited / in-progress / done) to catch back-edges |
| <a id="cracking-the-safe"></a>[Cracking the Safe](https://leetcode.com/problems/cracking-the-safe/) | Eulerian circuit on a de Bruijn graph |
| <a id="critical-connections-in-a-network"></a>[Critical Connections](https://leetcode.com/problems/critical-connections-in-a-network/) · [⇩ walkthrough](#critical-connections-in-a-network) | bridge test `low[v] > disc[u]` |
| <a id="evaluate-division"></a>[Evaluate Division](https://leetcode.com/problems/evaluate-division/) | a weighted DFS where the map carries the running product along the path |
| <a id="is-graph-bipartite"></a>[Is Graph Bipartite / Possible Bipartition](https://leetcode.com/problems/is-graph-bipartite/) | the map stores a 2-colouring; a same-colour neighbour means an odd cycle |
| <a id="max-area-of-island"></a>[Max Area of Island](https://leetcode.com/problems/max-area-of-island/) | have the flood return the cells it sank, and keep the maximum instead of a count |
| <a id="find-if-path-exists-in-graph"></a>[Negative-cycle detection](https://leetcode.com/problems/find-if-path-exists-in-graph/) | run the extra `V`-th pass; a relaxation ⇒ cycle |
| <a id="network-delay-time"></a>[Network Delay Time](https://leetcode.com/problems/network-delay-time/) · [⇩ walkthrough](#network-delay-time) | the answer is the max of all shortest distances from the source |
| <a id="number-of-closed-islands"></a>[Number of Closed Islands](https://leetcode.com/problems/number-of-closed-islands/) | same island count, but discard any component that touches the border |
| <a id="pacific-atlantic-water-flow"></a>[Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) · [⇩ walkthrough](#pacific-atlantic-water-flow) | flood **inward from each ocean's edge**, then take the intersection of the two reachable sets |
| <a id="reconstruct-itinerary"></a>[Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) | lexical tie-break via a per-node min-heap |
| <a id="rotting-oranges"></a>[Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | seed the queue with *all* rotten cells and run a multi-source BFS, counting layers = minutes |
| <a id="shortest-bridge"></a>[Shortest Bridge](https://leetcode.com/problems/shortest-bridge/) | flood one island first, then multi-source BFS outward until you hit the second |
| <a id="surrounded-regions"></a>[Surrounded Regions](https://leetcode.com/problems/surrounded-regions/) | first flood the safe cells inward **from the borders**, then flip everything else |
| <a id="swim-in-rising-water"></a>[Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) | minimize the maximum cell height along a path (same min-of-max relaxation) |
| <a id="valid-arrangement-of-pairs"></a>[Valid Arrangement of Pairs](https://leetcode.com/problems/valid-arrangement-of-pairs/) | pick a start with `out−in = 1`; Hierholzer |
| <a id="walls-and-gates"></a>[Walls and Gates](https://leetcode.com/problems/walls-and-gates/) | sources are all the gates; fill each room with its distance to the closest gate |

## [Segment Tree & Fenwick](/data-structures/segment-fenwick)

| Problem | Approach hint |
|---|---|
| <a id="range-sum-query-mutable"></a>[Range Sum Query — Mutable](https://leetcode.com/problems/range-sum-query-mutable/) · [⇩ walkthrough](#range-sum-query-mutable) | the canonical use — update one index, query any prefix/range |

## Full Walkthroughs — numbered steps + code

<p class="secgoal"><b>What &amp; why:</b> the ~50 highest-value variations where a step-by-step recipe pays off. Each has an explicit approach, numbered steps, and (where useful) a compact Java sketch.</p>

### 3Sum Closest
[↗ LeetCode](https://leetcode.com/problems/3sum-closest/) · Pattern: **Two Pointers**

1. Sort. For each `i`, run two-pointer on `[i+1..n-1]`.
2. At every step compute `sum = a[i]+a[lo]+a[hi]`; if `abs(sum-target) < best`, update `best`.
3. Move `lo++` if `sum < target`, else `hi--` — like standard 3Sum but tracking the closest, not exactly target.
4. Return `best`. O(n²) time.

### 4Sum
[↗ LeetCode](https://leetcode.com/problems/4sum/) · Pattern: **Two Pointers**

1. Sort. Two outer loops `i`, `j` (with `i<j`), then two-pointer inner search for the remaining pair.
2. Skip duplicates at every level: `i>0 && a[i]==a[i-1]`, `j>i+1 && a[j]==a[j-1]`, and after each hit skip `lo`/`hi` duplicates.
3. Use `long` for the sum to avoid overflow at extreme values.
4. O(n³) time.

### Best Time to Buy and Sell Stock
[↗ LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) · Pattern: **1-pass DP**

1. Track `minSoFar = min(minSoFar, price[i])`.
2. Track `best = max(best, price[i] - minSoFar)`.
3. O(n) time, O(1) space.

### Stock with Cooldown
[↗ LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) · Pattern: **State-Machine DP**

1. Three states: `hold`, `sold`, `rest`. Transitions:
2. `hold' = max(hold, rest - price)` (buy today).
3. `sold' = hold + price` (sell today).
4. `rest' = max(rest, sold)` (do nothing).
5. Answer = `max(sold, rest)`. O(n) time, O(1) space.

### Binary Tree Right Side View
[↗ LeetCode](https://leetcode.com/problems/binary-tree-right-side-view/) · Pattern: **BFS (last of each level)**

1. BFS with a level size. Push root, then for each level dequeue `size` nodes.
2. The last one you dequeue in the level is visible — record its value.
3. Push children in normal order.
4. O(n) time.

### Candy
[↗ LeetCode](https://leetcode.com/problems/candy/) · Pattern: **Greedy (two-pass)**

1. Give every child 1 candy.
2. Left-to-right: if `r[i] > r[i-1]`, set `c[i] = c[i-1] + 1`.
3. Right-to-left: if `r[i] > r[i+1]`, set `c[i] = max(c[i], c[i+1] + 1)`.
4. Sum `c`. Two passes because each direction enforces only one side of the constraint. O(n).

### Capacity To Ship Packages Within D Days
[↗ LeetCode](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) · Pattern: **Binary Search on Answer**

1. Range: `lo = max(weights)`, `hi = sum(weights)`.
2. `feasible(cap)`: sweep, add to current day's load; if it would exceed `cap`, start a new day; return `days <= D`.
3. Binary-search the smallest feasible `cap`. O(n log sum).

### Coin Change
[↗ LeetCode](https://leetcode.com/problems/coin-change/) · Pattern: **Unbounded knapsack DP**

1. `dp[i]` = min coins summing to `i`; init `dp[0]=0`, others `amount+1` (sentinel).
2. For each `i` from 1 to amount, for each coin `c ≤ i`: `dp[i] = min(dp[i], dp[i-c]+1)`.
3. Return `dp[amount] > amount ? -1 : dp[amount]`.
4. O(amount · coins).

### Combination Sum II
[↗ LeetCode](https://leetcode.com/problems/combination-sum-ii/) · Pattern: **Backtracking (each element once + dedup)**

1. Sort. Standard combination template with `start`.
2. At each `i`: skip if `i > start && a[i] == a[i-1]` (dedup at level).
3. Recurse with `i+1` (no reuse). Break when `a[i] > remaining` (pruning).
4. Exponential in worst case.

### Contiguous Array (equal 0s and 1s)
[↗ LeetCode](https://leetcode.com/problems/contiguous-array/) · Pattern: **Prefix Sum + Hash**

1. Map every `0` to `-1` mentally; find the longest subarray with sum 0.
2. Track running sum; store the **first** index each sum value appeared at.
3. When you revisit a sum, the subarray between is balanced — update `best`.
4. Seed `{0: -1}` so runs starting at index 0 are handled. O(n).

### Copy List with Random Pointer
[↗ LeetCode](https://leetcode.com/problems/copy-list-with-random-pointer/) · Pattern: **Hashing on nodes**

1. First pass: `Map<Node,Node>` from original to a fresh clone with same `val`.
2. Second pass: for each original `u`, set `map[u].next = map[u.next]` and `map[u].random = map[u.random]`.
3. Return `map[head]`. O(n) time and space (or O(1) with interleaved-copy trick).

### Counting Bits
[↗ LeetCode](https://leetcode.com/problems/counting-bits/) · Pattern: **DP on bits**

1. `bits[i] = bits[i >> 1] + (i & 1)` reuses the answer for `i/2`.
2. Fill 0..n in one pass.
3. O(n) time.

### Critical Connections in a Network
[↗ LeetCode](https://leetcode.com/problems/critical-connections-in-a-network/) · Pattern: **Tarjan low-link**

1. DFS assigning `disc[u]` (discovery time) and `low[u]` (earliest reachable via one back-edge).
2. For a tree edge `u → v`, recurse then set `low[u] = min(low[u], low[v])`.
3. If `low[v] > disc[u]`, edge `(u,v)` is a bridge.
4. Skip the direct parent edge to avoid a false back-edge. O(V+E).

### Edit Distance
[↗ LeetCode](https://leetcode.com/problems/edit-distance/) · Pattern: **Subsequence DP**

1. `dp[i][j]` = edits from `s1[0..i-1]` to `s2[0..j-1]`.
2. Match: `dp[i-1][j-1]`. Else: `1 + min(insert dp[i][j-1], delete dp[i-1][j], replace dp[i-1][j-1])`.
3. Bases: empty prefix = length of the other.
4. O(m·n).

### Find All Anagrams in a String
[↗ LeetCode](https://leetcode.com/problems/find-all-anagrams-in-a-string/) · Pattern: **Sliding Window (fixed size)**

1. Build the frequency vector `need[26]` from `p`.
2. Slide a window of size `|p|` over `s`. Maintain a `have[26]`.
3. Record `left` in the result whenever `have` equals `need`; increment/decrement bounds each step.
4. O(|s|) time.

### Find All Numbers Disappeared in an Array
[↗ LeetCode](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/) · Pattern: **Cyclic Sort / index-marking**

1. In-place: for each `v = |a[i]|`, mark `a[v-1] = -|a[v-1]|` to record that `v` was seen.
2. After the pass, positive entries mark indices whose value never appeared — add `i+1` to the result.
3. O(n) time, O(1) extra.

### Find Peak Element
[↗ LeetCode](https://leetcode.com/problems/find-peak-element/) · Pattern: **Binary Search on the shape**

1. `nums[-1] = nums[n] = -∞` conceptually.
2. At `mid`: if `a[mid] > a[mid+1]`, a peak is on the left half (including `mid`); else on the right.
3. Halve until `lo == hi`. O(log n).

### Find the Duplicate Number
[↗ LeetCode](https://leetcode.com/problems/find-the-duplicate-number/) · Pattern: **Fast/Slow Pointers (Floyd)**

1. Treat `nums` as a functional graph: `next(i) = nums[i]`. A duplicate value guarantees a cycle.
2. Phase 1: advance `slow = nums[slow]`, `fast = nums[nums[fast]]` until they meet.
3. Phase 2: reset `slow = 0`; move both one step at a time until they meet again — that's the cycle start = duplicate.
4. O(n) time, O(1) space.

### Fruits into Baskets
[↗ LeetCode](https://leetcode.com/problems/fruit-into-baskets/) · Pattern: **Sliding Window**

1. Reduces to *longest subarray with ≤ 2 distinct values*.
2. Grow `right`; when the map holds &gt; 2 distinct fruits, shrink `left` until back to 2.
3. Track `best = max(best, right - left + 1)`.
4. O(n) time, O(1) space (alphabet ≤ 3).

### Generate Parentheses
[↗ LeetCode](https://leetcode.com/problems/generate-parentheses/) · Pattern: **Backtracking (constrained)**

1. Track `open`, `close` counters starting at 0.
2. Add `(` if `open < n`. Add `)` if `close < open`.
3. When `open + close == 2n`, record the string.
4. Catalan-number many outputs.

### Insert Interval
[↗ LeetCode](https://leetcode.com/problems/insert-interval/) · Pattern: **Intervals**

1. Emit all intervals ending before `newStart` (no overlap, left side).
2. Merge every interval overlapping `new` — grow `newStart = min`, `newEnd = max`.
3. Emit the merged `new`, then emit the rest.
4. O(n) with one pass.

### K Closest Points to Origin
[↗ LeetCode](https://leetcode.com/problems/k-closest-points-to-origin/) · Pattern: **Top-K Heap or Quickselect**

1. Max-heap of size k on squared distance. For each point, offer; if size &gt; k, poll (evict the farthest).
2. Heap ends with the k closest. Or use Quickselect for O(n) average.
3. O(n log k) time.

### Kth Smallest Element in a BST
[↗ LeetCode](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) · Pattern: **In-order traversal**

1. In-order visit gives sorted order for a BST.
2. Iterative in-order (stack): push lefts, pop-visit-descend-right; decrement k on each visit.
3. Return the value when k hits 0.
4. O(H + k) time.

### Kth Smallest Element in a Sorted Matrix
[↗ LeetCode](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) · Pattern: **Binary Search on Value**

1. Range `lo=mat[0][0]`, `hi=mat[n-1][n-1]`.
2. `count(v)` — count entries ≤ v by walking from bottom-left in O(n) (down if ≤, else left).
3. Binary-search smallest `v` with `count(v) ≥ k`. O(n log range).

### Longest Increasing Subsequence
[↗ LeetCode](https://leetcode.com/problems/longest-increasing-subsequence/) · Pattern: **Patience DP**

1. Maintain a `tails` list where `tails[k]` = smallest tail of an LIS of length `k+1`.
2. For each `x`, binary-search the first `tails[i] >= x` and set `tails[i] = x`; if none, append.
3. Answer = `tails.size()`.
4. O(n log n).

### Longest Substring with At Most K Distinct
[↗ LeetCode](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/) · Pattern: **Sliding Window**

1. Grow `right`, tracking a frequency map.
2. While `map.size() > k`, shrink `left`: decrement its count; remove key when it hits 0.
3. Update `best = max(best, right - left + 1)`.
4. O(n) time, O(k) space.

### Aggressive Cows / Magnetic Force
[↗ LeetCode](https://leetcode.com/problems/magnetic-force-between-two-balls/) · Pattern: **Binary Search on Answer**

1. Sort positions. Range `lo=1`, `hi=max-min`.
2. `feasible(d)`: greedily place balls at positions ≥ last + d; feasible iff you place all m.
3. Binary-search the largest feasible `d`. O(n log range).

### Maximum Product Subarray
[↗ LeetCode](https://leetcode.com/problems/maximum-product-subarray/) · Pattern: **1D DP (Kadane variant)**

1. Track both a running `maxSoFar` and `minSoFar` — a negative flips them.
2. At each `x`: `newMax = max(x, x*maxSoFar, x*minSoFar)`; `newMin = min(x, x*maxSoFar, x*minSoFar)`.
3. Update `best = max(best, newMax)` each step.
4. O(n) time, O(1) space.

### Meeting Rooms
[↗ LeetCode](https://leetcode.com/problems/meeting-rooms/) · Pattern: **Intervals**

1. Sort by start time.
2. Return false as soon as `a[i].start < a[i-1].end`.
3. Otherwise true. O(n log n).

### Missing Number
[↗ LeetCode](https://leetcode.com/problems/missing-number/) · Pattern: **XOR / Gauss sum**

1. XOR trick: `xor(0..n) ^ xor(nums)` — all pairs cancel, missing survives.
2. Or sum trick: `n(n+1)/2 - sum(nums)`.
3. O(n) time, O(1) space.

### Move Zeroes
[↗ LeetCode](https://leetcode.com/problems/move-zeroes/) · Pattern: **Two Pointers (write index)**

1. Keep a `write` index starting at 0.
2. Scan `read` left-to-right: whenever `a[read] != 0`, set `a[write++] = a[read]`.
3. After the scan, fill `a[write..n-1]` with 0.
4. In-place, order-preserving, O(n).

### My Calendar I
[↗ LeetCode](https://leetcode.com/problems/my-calendar-i/) · Pattern: **Intervals / TreeMap**

1. Store bookings in a TreeMap keyed by start.
2. For a new `[s,e)`: check `floorKey(s)` and `ceilingKey(s)` — conflict iff their intervals overlap `[s,e)`.
3. Insert on success. O(log n) per booking.

### Network Delay Time
[↗ LeetCode](https://leetcode.com/problems/network-delay-time/) · Pattern: **Dijkstra**

1. Standard Dijkstra from `k`.
2. If any distance stays `∞`, return `-1`.
3. Otherwise return `max(dist)`.
4. O(E log V).

### Next Greater Element I
[↗ LeetCode](https://leetcode.com/problems/next-greater-element-i/) · Pattern: **Monotonic Stack**

1. Compute NGE for each value in `nums2` using a decreasing stack; store `value → next-greater` in a map.
2. For each query in `nums1`, look it up in the map (default `-1`).
3. O(n + m) time.

### Number of Provinces
[↗ LeetCode](https://leetcode.com/problems/number-of-provinces/) · Pattern: **Union-Find**

1. For each `(i, j)` with `M[i][j] == 1`, `union(i, j)`.
2. Count distinct `find(i)` values.
3. O(n² α(n)).

### Online Stock Span
[↗ LeetCode](https://leetcode.com/problems/online-stock-span/) · Pattern: **Monotonic Stack**

1. Keep a stack of `(price, span)` pairs, decreasing by price.
2. On `next(price)`: pop and accumulate `span` while the top's price ≤ current. Push `(price, span)`.
3. Each pushed pair is popped at most once — amortized O(1) per query.

### Pacific Atlantic Water Flow
[↗ LeetCode](https://leetcode.com/problems/pacific-atlantic-water-flow/) · Pattern: **Multi-source BFS/DFS**

1. Two `visited` grids: `pac`, `atl`.
2. BFS/DFS **from** every edge cell of each ocean, but only step to neighbours **not lower** (reverse-flow).
3. Result cells are those visited by both `pac` and `atl`.
4. O(m·n) time.

### Palindrome Partitioning
[↗ LeetCode](https://leetcode.com/problems/palindrome-partitioning/) · Pattern: **Backtracking + palindrome check**

1. DFS the split points. At each recursion, try every next-cut position `end`.
2. If `s[start..end]` is a palindrome, add and recurse from `end+1`.
3. Precompute an `isPal[i][j]` DP for O(1) palindrome test.
4. Exponential in worst case.

### Permutation in String
[↗ LeetCode](https://leetcode.com/problems/permutation-in-string/) · Pattern: **Sliding Window (fixed size)**

1. Same as Find All Anagrams, but return `true` on the first match instead of collecting positions.
2. Fixed window size = `|s1|`; compare counts each shift.
3. O(|s2|) time.

### Permutations II
[↗ LeetCode](https://leetcode.com/problems/permutations-ii/) · Pattern: **Backtracking (dedup by used[] rule)**

1. Sort. Use `used[i]` to track picked indices.
2. Skip when `i > 0 && a[i] == a[i-1] && !used[i-1]` — enforces first-copy-first ordering.
3. Recurse when `path.size() == n`.
4. O(n·n!) time.

### Random Pick with Weight
[↗ LeetCode](https://leetcode.com/problems/random-pick-with-weight/) · Pattern: **Prefix Sum + Binary Search**

1. Build a prefix sum of weights.
2. For each pick, generate `r = rnd.nextInt(total) + 1`.
3. Binary-search the smallest index whose prefix sum ≥ r.
4. O(n) build, O(log n) per pick.

### Range Addition
[↗ LeetCode](https://leetcode.com/problems/range-addition/) · Pattern: **Difference Array**

1. Maintain a delta array. For each update `[l, r, val]`, do `diff[l] += val; diff[r+1] -= val`.
2. After all updates, prefix-sum the delta array to recover the final values.
3. O(U + n) total, vs O(U·n) naive.

### Range Sum Query — Mutable
[↗ LeetCode](https://leetcode.com/problems/range-sum-query-mutable/) · Pattern: **Fenwick Tree**

1. Build 1-indexed BIT: `for each i, tree[i] = sum of the last i&-i values`.
2. `update(i, delta)`: walk `i += i & -i` while `i ≤ n`, adding delta.
3. `sum(i)`: walk `i -= i & -i` while `i > 0`, accumulating.
4. Query `[l,r]` = `sum(r) - sum(l-1)`. O(log n) each op.

### Reverse Nodes in k-Group
[↗ LeetCode](https://leetcode.com/problems/reverse-nodes-in-k-group/) · Pattern: **Linked List**

1. Advance a pointer k steps; if fewer than k remain, return without reversing.
2. Reverse the k-node block in place (standard three-pointer reverse).
3. Wire the tail of the reversed block to the recursive result of the rest.
4. O(n) time, O(1) space (iterative).

### Search a 2D Matrix
[↗ LeetCode](https://leetcode.com/problems/search-a-2d-matrix/) · Pattern: **Binary Search**

1. Row-major sorted array reshaped as a matrix — treat as one 1D sorted array of size `m*n`.
2. Binary-search `lo=0, hi=m*n-1`; map `mid` to `(mid/n, mid%n)`.
3. Compare `mat[r][c]` to target; standard halving.
4. O(log(mn)) time.

### Search a 2D Matrix II
[↗ LeetCode](https://leetcode.com/problems/search-a-2d-matrix-ii/) · Pattern: **Two Pointers on a matrix**

1. Start at the top-right corner `(0, n-1)`.
2. If `mat[r][c] == target`, done. If `mat[r][c] > target`, `c--` (eliminates a column). Else `r++` (eliminates a row).
3. Each step drops a row or column, so O(m+n) total.
4. Bottom-left works symmetrically.

### Shuffle an Array (Fisher–Yates)
[↗ LeetCode](https://leetcode.com/problems/shuffle-an-array/) · Pattern: **Randomized**

1. Copy the array to a mutable buffer.
2. For `i` from `n-1` down to `1`: swap `buf[i]` with `buf[rnd.nextInt(i+1)]`.
3. Every permutation has equal probability by induction.
4. O(n) per shuffle.

### Spiral Matrix II
[↗ LeetCode](https://leetcode.com/problems/spiral-matrix-ii/) · Pattern: **Matrix mechanics**

1. Same layer-by-layer walk as Spiral Matrix, but **write** `1..n²` into the cells you visit.
2. Maintain `top`, `bot`, `left`, `right` bounds; after each side, shrink the relevant bound.
3. Guard bottom-row and left-column with `top <= bot` / `left <= right` for odd `n`.
4. O(n²) time, O(1) extra.

### Subarray Sums Divisible by K
[↗ LeetCode](https://leetcode.com/problems/subarray-sums-divisible-by-k/) · Pattern: **Prefix Sum + Hash**

1. Prefix sum modulo k — two prefix sums with the same residue bracket a subarray whose sum is a multiple of k.
2. Count occurrences of each residue `((prefix % k) + k) % k` (handle negatives).
3. For each new residue, add its running count to the answer, then increment.
4. Seed the count map with `{0: 1}` for subarrays that start at index 0. O(n).

### Subsets II
[↗ LeetCode](https://leetcode.com/problems/subsets-ii/) · Pattern: **Backtracking (dedup by sort + skip)**

1. Sort. Standard subsets template with `start` index.
2. Inside the for-loop: if `i > start && a[i] == a[i-1]` skip — prevents same-level twins.
3. Record a *copy* of the path at every node.
4. O(2ⁿ) subsets.

### Two Sum II — Input Array Is Sorted
[↗ LeetCode](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) · Pattern: **Two Pointers**

1. Two indices `lo=0`, `hi=n-1`.
2. Compute `sum = a[lo] + a[hi]`; if it equals target return `{lo+1, hi+1}` (1-indexed).
3. If sum is too small, `lo++`; too big, `hi--`. Sortedness guarantees the discarded end can never help.
4. Terminates when pointers cross — O(n) time, O(1) space.



```java
int lo=0, hi=a.length-1;
while (lo<hi) {
    int s=a[lo]+a[hi];
    if (s==target) return new int[]{lo+1, hi+1};
    if (s<target) lo++; else hi--;
}
return new int[]{-1,-1};
```



### Unique Paths
[↗ LeetCode](https://leetcode.com/problems/unique-paths/) · Pattern: **Grid DP**

1. `dp[i][j] = dp[i-1][j] + dp[i][j-1]`; first row/col all 1s.
2. Collapse to a 1D row updated left-to-right — O(n) space.
3. Answer at `dp[m-1][n-1]`.
4. O(m·n).

### Valid Anagram
[↗ LeetCode](https://leetcode.com/problems/valid-anagram/) · Pattern: **Hashing**

1. Return false if lengths differ.
2. Bump `count[c]++` for each char in `s`, decrement for each char in `t`.
3. Return true iff every count is 0 (or every entry in the map is 0).
4. O(n) time, O(1) space for fixed alphabet.

### Valid Palindrome II
[↗ LeetCode](https://leetcode.com/problems/valid-palindrome-ii/) · Pattern: **Two Pointers**

1. Standard two-pointer palindrome check.
2. On the first mismatch, allow one skip: try `s[lo+1..hi]` or `s[lo..hi-1]` — return true if either is a palindrome.
3. Only one deletion is allowed, so this branching is sufficient.
4. O(n) time.

### Word Break
[↗ LeetCode](https://leetcode.com/problems/word-break/) · Pattern: **1D DP**

1. `dp[i]` = can we split `s[0..i-1]` into dictionary words.
2. `dp[0] = true`; for each `i`, try every `j < i` — `dp[i] = dp[j] && s[j..i-1] ∈ dict`.
3. Use a `HashSet` for O(1) lookups.
4. O(n²·L) time.

### Word Ladder
[↗ LeetCode](https://leetcode.com/problems/word-ladder/) · Pattern: **BFS**

1. Put every word into a set (dedup + O(1) lookup).
2. BFS from `beginWord`; at each pop, generate every 1-letter variant, if in set, enqueue and remove from set.
3. Distance += 1 per level; return when you dequeue `endWord`.
4. O(N·L·Σ) time.
