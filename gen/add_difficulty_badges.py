#!/usr/bin/env python3
"""Wave 1 bulk edits on src/:
  - Add difficulty badges (Easy/Medium/Hard) to problem H2s based on LC slug lookup.
  - Add <ProgressCheck :id="slug"/> after each ## Problem H2.
  - Prev/next frontmatter isn't set here — VitePress auto-detects from sidebar order.
"""
import os, re, glob

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gen", "src")

# Curated LC difficulty lookup — from most common canonical problems.
# Easy=e, Medium=m, Hard=h.
LC_DIFFICULTY = {
    # Sliding Window
    "maximum-average-subarray-i": "e",
    "minimum-size-subarray-sum": "m",
    "longest-substring-without-repeating-characters": "m",
    "minimum-window-substring": "h",
    "longest-repeating-character-replacement": "m",
    "sliding-window-maximum": "h",
    "subarray-product-less-than-k": "m",
    "subarrays-with-k-different-integers": "h",
    "permutation-in-string": "m",
    "find-all-anagrams-in-a-string": "m",
    "max-consecutive-ones-iii": "m",
    "fruit-into-baskets": "m",
    "longest-substring-with-at-most-k-distinct-characters": "m",
    # Two Pointers
    "3sum": "m",
    "container-with-most-water": "m",
    "trapping-rain-water": "h",
    "squares-of-a-sorted-array": "e",
    "sort-colors": "m",
    "3sum-closest": "m",
    "4sum": "m",
    "remove-duplicates-from-sorted-array": "e",
    "valid-palindrome": "e",
    # Fast/Slow
    "linked-list-cycle": "e",
    "linked-list-cycle-ii": "m",
    "middle-of-the-linked-list": "e",
    "happy-number": "e",
    "find-the-duplicate-number": "m",
    # Prefix Sum
    "range-sum-query-immutable": "e",
    "range-sum-query-2d-immutable": "m",
    "subarray-sum-equals-k": "m",
    "contiguous-array": "m",
    "product-of-array-except-self": "m",
    # Hashing
    "two-sum": "e",
    "group-anagrams": "m",
    "longest-consecutive-sequence": "m",
    "top-k-frequent-elements": "m",
    "valid-anagram": "e",
    # Monotonic Stack
    "daily-temperatures": "m",
    "next-greater-element-i": "e",
    "next-greater-element-ii": "m",
    "largest-rectangle-in-histogram": "h",
    "trapping-rain-water": "h",
    # Binary Search
    "binary-search": "e",
    "search-in-rotated-sorted-array": "m",
    "find-first-and-last-position-of-element-in-sorted-array": "m",
    "search-a-2d-matrix": "m",
    "find-peak-element": "m",
    "median-of-two-sorted-arrays": "h",
    # BS on Answer
    "koko-eating-bananas": "m",
    "capacity-to-ship-packages-within-d-days": "m",
    "split-array-largest-sum": "h",
    "aggressive-cows": "m",
    "magnetic-force-between-two-balls": "m",
    # Top K / Heap
    "kth-largest-element-in-an-array": "m",
    "kth-largest-element-in-a-stream": "e",
    "k-closest-points-to-origin": "m",
    "find-median-from-data-stream": "h",
    # K-way Merge
    "merge-k-sorted-lists": "h",
    "kth-smallest-element-in-a-sorted-matrix": "m",
    "smallest-range-covering-elements-from-k-lists": "h",
    # Merge Intervals
    "merge-intervals": "m",
    "insert-interval": "m",
    "non-overlapping-intervals": "m",
    "meeting-rooms": "e",
    "meeting-rooms-ii": "m",
    # Sweep Line
    "the-skyline-problem": "h",
    "car-pooling": "m",
    "corporate-flight-bookings": "m",
    "employee-free-time": "h",
    # Topo Sort
    "course-schedule": "m",
    "course-schedule-ii": "m",
    "alien-dictionary": "h",
    "minimum-height-trees": "m",
    # Union Find
    "number-of-provinces": "m",
    "number-of-islands": "m",
    "redundant-connection": "m",
    "accounts-merge": "m",
    # Greedy
    "jump-game": "m",
    "jump-game-ii": "m",
    "gas-station": "m",
    "task-scheduler": "m",
    "partition-labels": "m",
    "candy": "h",
    # Backtracking
    "subsets": "m",
    "permutations": "m",
    "combination-sum": "m",
    "combination-sum-ii": "m",
    "word-search": "m",
    "n-queens": "h",
    "sudoku-solver": "h",
    "letter-combinations-of-a-phone-number": "m",
    "generate-parentheses": "m",
    "restore-ip-addresses": "m",
    # Divide & Conquer
    "count-of-smaller-numbers-after-self": "h",
    "reverse-pairs": "h",
    # DP
    "climbing-stairs": "e",
    "house-robber": "m",
    "coin-change": "m",
    "longest-increasing-subsequence": "m",
    "longest-common-subsequence": "m",
    "edit-distance": "h",
    "maximum-subarray": "m",
    "maximum-product-subarray": "m",
    "word-break": "m",
    "unique-paths": "m",
    "unique-paths-ii": "m",
    "minimum-path-sum": "m",
    "partition-equal-subset-sum": "m",
    "partition-to-k-equal-sum-subsets": "m",
    "burst-balloons": "h",
    "best-time-to-buy-and-sell-stock": "e",
    "best-time-to-buy-and-sell-stock-with-cooldown": "m",
    # Trie
    "implement-trie-prefix-tree": "m",
    "design-add-and-search-words-data-structure": "m",
    "word-search-ii": "h",
    "maximum-xor-of-two-numbers-in-an-array": "m",
    # Bit Manip
    "single-number": "e",
    "single-number-ii": "m",
    "counting-bits": "e",
    "reverse-bits": "e",
    "number-of-1-bits": "e",
    "missing-number": "e",
    "sum-of-two-integers": "m",
    # Quickselect
    # Math
    "powx-n": "m",
    "sqrtx": "e",
    "count-primes": "m",
    "greatest-common-divisor-of-strings": "e",
    # Design
    "lru-cache": "m",
    "lfu-cache": "h",
    "insert-delete-getrandom-o1": "m",
    "linked-list-random-node": "m",
    "min-stack": "m",
    # Arrays
    "rotate-image": "m",
    "spiral-matrix": "m",
    "set-matrix-zeroes": "m",
    "first-missing-positive": "h",
    "find-all-numbers-disappeared-in-an-array": "e",
    "next-permutation": "m",
    # Strings
    "reverse-string": "e",
    "reverse-words-in-a-string": "m",
    "encode-and-decode-strings": "m",
    "valid-parentheses": "e",
    "palindromic-substrings": "m",
    "longest-palindromic-substring": "m",
    # Linked Lists
    "reverse-linked-list": "e",
    "merge-two-sorted-lists": "e",
    "add-two-numbers": "m",
    "remove-nth-node-from-end-of-list": "m",
    "palindrome-linked-list": "e",
    "copy-list-with-random-pointer": "m",
    "reverse-nodes-in-k-group": "h",
    # Stacks/Queues
    "min-stack": "m",
    # Trees
    "invert-binary-tree": "e",
    "maximum-depth-of-binary-tree": "e",
    "same-tree": "e",
    "symmetric-tree": "e",
    "binary-tree-level-order-traversal": "m",
    "diameter-of-binary-tree": "e",
    "validate-binary-search-tree": "m",
    "kth-smallest-element-in-a-bst": "m",
    "lowest-common-ancestor-of-a-binary-tree": "m",
    "lowest-common-ancestor-of-a-binary-search-tree": "m",
    "binary-tree-maximum-path-sum": "h",
    "serialize-and-deserialize-binary-tree": "h",
    "construct-binary-tree-from-preorder-and-inorder-traversal": "m",
    "binary-tree-right-side-view": "m",
    "house-robber-iii": "m",
    # Graphs
    "clone-graph": "m",
    "rotting-oranges": "m",
    "pacific-atlantic-water-flow": "m",
    "word-ladder": "h",
    "network-delay-time": "m",
    "cheapest-flights-within-k-stops": "m",
    "min-cost-to-connect-all-points": "m",
    "swim-in-rising-water": "h",
    "critical-connections-in-a-network": "h",
    "reconstruct-itinerary": "h",
    # Segment Tree / Fenwick
    "range-sum-query-mutable": "m",
}

def find_lc_slug(text_after_h2: str) -> str | None:
    """Find LC slug from the *[↗ LeetCode: Name](https://leetcode.com/problems/slug/)* line right after H2."""
    m = re.search(r"https://leetcode\.com/problems/([a-z0-9-]+)/?", text_after_h2)
    return m.group(1) if m else None

def process_file(path: str) -> tuple[int, int]:
    """Process one markdown file. Returns (badges_added, progress_added)."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    out = []
    badges = 0
    progress = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        # Match H2 problem headings (not already-badged)
        m = re.match(r"^(## )([^#\n<].*?)$", line)
        if m and "<span class=\"diff" not in line and i + 3 < len(lines):
            # Look ahead for LC link in next 2 lines
            following = "\n".join(lines[i:i+3])
            slug = find_lc_slug(following)
            if slug and slug in LC_DIFFICULTY:
                diff = LC_DIFFICULTY[slug]
                diff_label = {"e": "Easy", "m": "Medium", "h": "Hard"}[diff]
                new_h2 = f'{m.group(1)}{m.group(2)} <span class="diff diff-{diff}">{diff_label}</span>'
                out.append(new_h2)
                badges += 1
                i += 1
                continue
        out.append(line)
        i += 1

    new_content = "\n".join(out)
    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    return badges, progress

def main():
    total_badges = 0
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        b, p = process_file(path)
        if b > 0:
            print(f"  {os.path.basename(path)}: +{b} badges")
            total_badges += b
    print(f"\nTotal difficulty badges added: {total_badges}")

if __name__ == "__main__":
    main()
