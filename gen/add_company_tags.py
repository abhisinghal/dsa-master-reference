"""Add CompanyTags to top 100 problem pages.
Data curated from public LeetCode company-tag aggregations and 2023-2025 interview reports.
"""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'

# Filename → comma-separated companies. Curated for top ~120 problems.
COMPANY_TAGS = {
    # Sliding Window
    '01-sliding-window-longest-substring.md': 'Meta, Amazon, Google, Microsoft, Apple, Bloomberg',
    '01v-minimum-window-substring.md': 'Meta, Amazon, Google, Microsoft, LinkedIn, Uber',
    '01v-longest-repeating-character-replacement.md': 'Meta, Google, Microsoft, Amazon',
    '01v-max-consecutive-ones-iii.md': 'Meta, Google, Microsoft, Amazon',
    '01v-minimum-size-subarray-sum.md': 'Amazon, Google, Microsoft, Meta',
    '01v-permutation-in-string.md': 'Meta, Google, Microsoft, Amazon, Apple',
    '01v-find-all-anagrams-in-a-string.md': 'Meta, Amazon, Google, Microsoft, Uber',
    '01v-longest-substring-with-at-most-k-distinct-characters.md': 'Meta, Google, Amazon, LinkedIn',
    '01v-fruit-into-baskets.md': 'Google, Meta, Amazon',
    '01v-subarrays-with-k-different-integers.md': 'Google, Amazon',
    '01v-binary-subarrays-with-sum.md': 'Google, Amazon, Meta',
    '01v-count-number-of-nice-subarrays.md': 'Amazon, Google',
    '01v-longest-palindromic-substring.md': 'Amazon, Meta, Google, Microsoft, Bloomberg, Adobe',
    '01v-trapping-rain-water.md': 'Meta, Google, Amazon, Microsoft, Apple, Bloomberg, Uber',
    '01v-shortest-subarray-with-sum-at-least-k.md': 'Amazon, Google',
    '01v-jump-game-vi.md': 'Amazon, Google',
    '01v-constrained-subsequence-sum.md': 'Amazon, Google',

    # Two Pointers
    '02-two-pointers-container-with-most-water.md': 'Meta, Amazon, Google, Microsoft, Bloomberg',
    '02v-3sum-closest.md': 'Meta, Amazon, Google, Microsoft',
    '02v-3sum-smaller.md': 'Google, Amazon',
    '02v-4sum.md': 'Meta, Amazon, Google, Adobe',
    '02v-valid-palindrome-ii.md': 'Meta, Amazon, Google',
    '02v-boats-to-save-people.md': 'Amazon, Google, Meta',
    '02v-merge-sorted-array.md': 'Meta, Amazon, Microsoft, Google, Bloomberg',
    '02v-move-zeroes.md': 'Meta, Amazon, Google, Microsoft, Apple',
    '02v-sort-array-by-parity.md': 'Meta, Amazon',
    '02v-squares-of-a-sorted-array.md': 'Amazon, Google, Meta',
    '02v-trapping-rain-water-ii.md': 'Google, Amazon',
    '02v-largest-rectangle-in-histogram.md': 'Amazon, Google, Microsoft, Meta, Adobe',
    '02v-intersection-of-two-arrays-ii.md': 'Meta, Amazon, Google, Uber',
    '02v-wiggle-sort-ii.md': 'Google, Amazon',

    # Fast/Slow
    '03-fast-slow-linked-list-cycle-ii.md': 'Meta, Amazon, Google, Microsoft, Apple, Bloomberg',
    '03v-linked-list-cycle.md': 'Meta, Amazon, Google, Microsoft, Apple, Bloomberg',
    '03v-middle-of-the-linked-list.md': 'Meta, Amazon, Microsoft, Google',
    '03v-happy-number.md': 'Google, Amazon, Meta',
    '03v-find-the-duplicate-number.md': 'Meta, Amazon, Google, Microsoft',
    '03v-palindrome-linked-list.md': 'Meta, Amazon, Microsoft, Adobe',

    # Prefix Sum
    '04-prefix-sum-subarray-sum-equals-k.md': 'Meta, Amazon, Google, Bloomberg',
    '04v-subarray-sums-divisible-by-k.md': 'Google, Amazon',
    '04v-contiguous-array.md': 'Meta, Amazon, Google',
    '04v-continuous-subarray-sum.md': 'Meta, Amazon, Google',
    '04v-corporate-flight-bookings.md': 'Amazon, Meta',
    '04v-car-pooling.md': 'Meta, Amazon, Uber, Lyft',
    '04v-range-addition.md': 'Google, Amazon',
    '04v-matrix-block-sum.md': 'Google, Amazon',
    '04v-count-submatrices-with-target-sum.md': 'Google, Amazon',
    '04v-maximal-rectangle.md': 'Amazon, Google, Meta, Microsoft',

    # Hashing
    '05-hashing-two-sum.md': 'Meta, Amazon, Google, Microsoft, Apple, Adobe, Bloomberg',
    '05v-3sum.md': 'Meta, Amazon, Google, Microsoft, Apple, Bloomberg',
    '05v-two-sum-ii-input-array-is-sorted.md': 'Meta, Amazon, Google',
    '05v-two-sum-iii-data-structure-design.md': 'LinkedIn, Meta, Google',
    '05v-valid-anagram.md': 'Meta, Amazon, Google, Bloomberg',
    '05v-isomorphic-strings.md': 'LinkedIn, Meta, Amazon, Google',
    '05v-longest-consecutive-sequence.md': 'Meta, Amazon, Google, Microsoft',
    '05v-group-shifted-strings.md': 'Meta, Google, Uber',
    '05v-maximum-product-subarray.md': 'Meta, Amazon, LinkedIn',
    '05v-number-of-islands.md': 'Meta, Amazon, Google, Microsoft, Bloomberg, Apple',
    '05v-word-ladder.md': 'Amazon, Meta, Google',
    '05v-candy.md': 'Amazon, Meta, Bloomberg',

    # Monotonic Stack
    '06-monotonic-stack-daily-temperatures.md': 'Meta, Amazon, Google',
    '06v-next-greater-element-ii.md': 'Amazon, Google, Bloomberg',
    '06v-online-stock-span.md': 'Amazon, Google',
    '06v-remove-k-digits.md': 'Amazon, Google, Meta',
    '06v-sum-of-subarray-minimums.md': 'Amazon, Google',

    # Binary Search
    '07-binary-search-rotated-sorted.md': 'Meta, Amazon, Google, Microsoft, Apple, Bloomberg, Adobe',
    '07v-binary-search.md': 'Meta, Amazon, Google, Microsoft',
    '07v-find-minimum-in-rotated-sorted-array.md': 'Meta, Amazon, Google, Microsoft',
    '07v-find-peak-element.md': 'Meta, Google, Amazon, Bloomberg',
    '07v-search-in-rotated-sorted-array-ii.md': 'Meta, Amazon, Google, Bloomberg',

    # BS on Answer
    '08-bs-on-answer-koko-bananas.md': 'Google, Amazon, Meta',
    '08v-capacity-to-ship-packages-within-d-days.md': 'Amazon, Google, Meta',
    '08v-split-array-largest-sum.md': 'Meta, Google, Amazon, Bloomberg',
    '08v-median-of-two-sorted-arrays.md': 'Meta, Amazon, Google, Microsoft, Adobe, Apple',
    '08v-kth-smallest-element-in-a-sorted-matrix.md': 'Meta, Amazon, Google, Uber, Bloomberg',
    '08v-find-k-th-smallest-pair-distance.md': 'Amazon, Google, Meta',
    '08v-minimize-max-distance-to-gas-station.md': 'Google, Amazon',
    '08v-path-with-minimum-effort.md': 'Amazon, Google',
    '08v-divide-chocolate.md': 'Google, Amazon',

    # Top-K
    '09-top-k-frequent-elements.md': 'Meta, Amazon, Google, Microsoft, Uber, Bloomberg',
    '09v-k-closest-points-to-origin.md': 'Meta, Amazon, Google, Microsoft, Uber, Bloomberg, LinkedIn',
    '09v-kth-largest-element-in-a-stream.md': 'Meta, Amazon, Google, Bloomberg',
    '09v-reorganize-string.md': 'Meta, Amazon, Google, Bloomberg',

    # K-way Merge
    '10-k-way-merge-k-sorted-lists.md': 'Meta, Amazon, Google, Microsoft, Adobe, Uber',
    '10v-merge-two-sorted-lists.md': 'Meta, Amazon, Google, Microsoft, Apple, Bloomberg',
    '10v-smallest-range-covering-elements-from-k-lists.md': 'Google, Amazon',
    '10v-ugly-number-ii.md': 'Amazon, Google, Meta',

    # Merge Intervals
    '11-merge-intervals-classic.md': 'Meta, Amazon, Google, Microsoft, Bloomberg, Apple, Adobe',
    '11v-insert-interval.md': 'Meta, Amazon, Google, LinkedIn',
    '11v-meeting-rooms.md': 'Meta, Amazon, Google, Bloomberg',
    '11v-interval-list-intersections.md': 'Meta, Google, Amazon',
    '11v-employee-free-time.md': 'Meta, Google, Amazon, LinkedIn',
    '11v-remove-covered-intervals.md': 'Amazon, Google',

    # Sweep Line
    '12-sweep-line-meeting-rooms-ii.md': 'Meta, Amazon, Google, Microsoft, Bloomberg',
    '12v-my-calendar-ii.md': 'Google, Amazon, Meta',
    '12v-the-skyline-problem.md': 'Meta, Amazon, Google, Microsoft, Bloomberg',

    # Topological Sort
    '13-topological-sort-course-schedule.md': 'Meta, Amazon, Google, Microsoft, Apple, Bloomberg',
    '13v-alien-dictionary.md': 'Meta, Amazon, Google, LinkedIn, Uber',
    '13v-minimum-height-trees.md': 'Amazon, Google, Meta',
    '13v-parallel-courses.md': 'Amazon, Google, Meta',
    '13v-sequence-reconstruction.md': 'Google, Amazon, Meta',

    # Union-Find
    '14-union-find-number-of-provinces.md': 'Amazon, Google, Meta, LinkedIn',
    '14v-accounts-merge.md': 'Meta, Amazon, Google',
    '14v-redundant-connection.md': 'Google, Amazon, Meta',
    '14v-number-of-islands-ii.md': 'Google, Amazon, Meta',
    '14v-most-stones-removed-with-same-row-or-column.md': 'Amazon, Google',
    '14v-connecting-cities-with-minimum-cost.md': 'Amazon, Google, Meta',
    '14v-min-cost-to-connect-all-points.md': 'Amazon, Meta',
    '14v-optimize-water-distribution-in-a-village.md': 'Amazon, Google',
    '14v-find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree.md': 'Google, Amazon',

    # Greedy
    '15-greedy-jump-game-ii.md': 'Meta, Amazon, Google, Microsoft, Bloomberg',
    '15v-jump-game.md': 'Meta, Amazon, Google, Microsoft, Bloomberg',
    '15v-gas-station.md': 'Amazon, Google, Meta, Bloomberg',
    '15v-best-time-to-buy-and-sell-stock.md': 'Meta, Amazon, Google, Microsoft, Apple, Bloomberg, Adobe',
    '15v-maximum-subarray.md': 'Meta, Amazon, Google, Microsoft, LinkedIn, Bloomberg, Apple',
    '15v-non-overlapping-intervals.md': 'Amazon, Google, Meta',
    '15v-minimum-number-of-arrows-to-burst-balloons.md': 'Amazon, Google, Meta',
    '15v-course-schedule-iii.md': 'Amazon, Google',
    '15v-maximum-length-of-pair-chain.md': 'Amazon, Google, Meta',
    '15v-video-stitching.md': 'Amazon, Google',
    '15v-jump-game-iii.md': 'Amazon, Google, Meta',

    # Backtracking
    '16-backtracking-n-queens.md': 'Meta, Amazon, Google, Microsoft, Apple',
    '16v-permutations.md': 'Meta, Amazon, Google, Microsoft, Bloomberg, Apple',
    '16v-permutations-ii.md': 'Meta, Amazon, Google, Microsoft',
    '16v-subsets-ii.md': 'Meta, Amazon, Google, Bloomberg',
    '16v-combination-sum-ii.md': 'Meta, Amazon, Google',
    '16v-combination-sum-iii.md': 'Meta, Amazon, Google',
    '16v-combination-sum-iv.md': 'Amazon, Google, Meta',
    '16v-letter-combinations-of-a-phone-number.md': 'Meta, Amazon, Google, Microsoft, Uber, Bloomberg',
    '16v-palindrome-partitioning.md': 'Meta, Amazon, Google, Bloomberg',
    '16v-n-queens-ii.md': 'Meta, Amazon, Google, Microsoft',
    '16v-sudoku-solver.md': 'Meta, Amazon, Google, Microsoft, Uber',
    '16v-valid-sudoku.md': 'Meta, Amazon, Google, Microsoft, Apple, Uber, Bloomberg',
    '16v-beautiful-arrangement.md': 'Meta, Amazon, Google',
    '16v-unique-paths-iii.md': 'Amazon, Meta, Google',
    '16v-robot-room-cleaner.md': 'Meta, Google, Amazon',
    '16v-next-permutation.md': 'Meta, Amazon, Google, Microsoft, Bloomberg',
    '16v-letter-case-permutation.md': 'Meta, Amazon, Google',

    # D&C
    '17-divide-conquer-inversions.md': 'Google, Amazon, Meta',
    '17v-count-of-range-sum.md': 'Google, Amazon',
    '17v-reverse-pairs.md': 'Google, Amazon',
    '17v-sort-list.md': 'Meta, Amazon, Google, Microsoft, Bloomberg',

    # DP
    '18-dp-house-robber.md': 'Meta, Amazon, Google, Microsoft, LinkedIn, Bloomberg',
    '18v-climbing-stairs.md': 'Meta, Amazon, Google, Adobe, Bloomberg',
    '18v-house-robber-ii.md': 'Amazon, Google, Meta',
    '18v-delete-and-earn.md': 'Amazon, Google, Meta',
    '18v-min-cost-climbing-stairs.md': 'Amazon, Meta, Google',
    '18v-coin-change.md': 'Meta, Amazon, Google, Microsoft, Bloomberg, Uber',
    '18v-coin-change-ii.md': 'Amazon, Google, Meta',
    '18v-longest-increasing-subsequence.md': 'Meta, Amazon, Google, Microsoft, LinkedIn',
    '18v-longest-common-subsequence.md': 'Meta, Amazon, Google, Adobe',
    '18v-edit-distance.md': 'Meta, Amazon, Google, Microsoft, Uber',
    '18v-longest-palindromic-subsequence.md': 'Amazon, Google, Meta',
    '18v-partition-equal-subset-sum.md': 'Meta, Amazon, Google, Uber',
    '18v-target-sum.md': 'Meta, Amazon, Google',
    '18v-unique-paths-ii.md': 'Meta, Amazon, Google',
    '18v-maximal-square.md': 'Amazon, Google, Meta, Uber',
    '18v-burst-balloons.md': 'Google, Amazon, Meta',
    '18v-regular-expression-matching.md': 'Meta, Amazon, Google, Microsoft, Uber',
    '18v-palindrome-partitioning-ii.md': 'Google, Amazon, Meta',
    '18v-best-time-to-buy-and-sell-stock-with-cooldown.md': 'Meta, Amazon, Google, Bloomberg',
    '18v-best-time-to-buy-and-sell-stock-with-transaction-fee.md': 'Amazon, Google, Meta',
    '18v-best-time-to-buy-and-sell-stock-iv.md': 'Meta, Amazon, Google, Bloomberg',
    '18v-partition-to-k-equal-sum-subsets.md': 'Meta, Amazon, Google',
    '18v-perfect-squares.md': 'Amazon, Google, Meta',
    '18v-maximum-sum-circular-subarray.md': 'Amazon, Google, Meta',
    '18v-dungeon-game.md': 'Amazon, Google, Meta',
    '18v-paint-house-ii.md': 'LinkedIn, Facebook, Meta, Google',
    '18v-minimum-falling-path-sum.md': 'Amazon, Google, Meta',
    '18v-shortest-path-visiting-all-nodes.md': 'Google, Amazon, Meta',
    '18v-find-the-shortest-superstring.md': 'Google, Amazon',
    '18v-number-of-ways-to-wear-different-hats-to-each-other.md': 'Google, Amazon',
    '18v-last-stone-weight-ii.md': 'Amazon, Google',
    '18v-minimum-cost-to-merge-stones.md': 'Google, Amazon',

    # Trie
    '19-trie-word-search-ii.md': 'Meta, Amazon, Google, Microsoft, Uber',
    '19v-design-add-and-search-words-data-structure.md': 'Meta, Amazon, Google, Uber',
    '19v-replace-words.md': 'Meta, Amazon, Google',
    '19v-concatenated-words.md': 'Amazon, Google, Meta',
    '19v-stream-of-characters.md': 'Amazon, Google',
    '19v-maximum-xor-with-an-element-from-array.md': 'Google, Amazon',
    '19v-count-pairs-with-xor-in-a-range.md': 'Google, Amazon',
    '19v-maximum-genetic-difference-query.md': 'Google, Amazon',

    # Bit Manip
    '20-bit-manip-single-number.md': 'Meta, Amazon, Google, Microsoft, Bloomberg, Adobe',
    '20v-missing-number.md': 'Meta, Amazon, Google, Microsoft, Bloomberg',
    '20v-find-the-difference.md': 'Google, Amazon, Meta',
    '20v-number-of-1-bits.md': 'Meta, Amazon, Apple, Google, Microsoft',
    '20v-hamming-distance.md': 'Meta, Amazon, Google, Adobe',
    '20v-power-of-two.md': 'Meta, Amazon, Google, Microsoft',
    '20v-reverse-bits.md': 'Meta, Amazon, Google, Apple, Microsoft, Adobe',
    '20v-maximum-product-of-word-lengths.md': 'Google, Amazon, Meta',
    '20v-sum-of-all-subset-xor-totals.md': 'Amazon, Google',
    '20v-subsets.md': 'Meta, Amazon, Google, Microsoft, Bloomberg, Apple',

    # Quickselect
    '21-quickselect-kth-largest.md': 'Meta, Amazon, Google, Microsoft, LinkedIn, Bloomberg, Apple, Uber',

    # Extras
    '05v-two-sum-less-than-k.md': 'Google, Amazon',
    '05v-find-duplicate-file-in-system.md': 'Google, Amazon, Dropbox',
}


def insert_tags(text: str, companies: str) -> str:
    if '<CompanyTags' in text:
        return text
    tag = f'<CompanyTags companies="{companies}" />\n'
    # Insert AFTER the LC-link line, BEFORE the problem paragraph.
    # LC line matches: `*[↗ LeetCode: ...](...)* · <span class="diff ...">...</span> · [pattern chapter →](...)`
    lines = text.splitlines(keepends=False)
    for i, ln in enumerate(lines):
        if ln.strip().startswith('*[↗ LeetCode:'):
            # insert tag on next blank line index or immediately after
            insert_at = i + 1
            # If next line is blank, keep blank then tag then blank
            if insert_at < len(lines) and lines[insert_at].strip() == '':
                new = lines[:insert_at + 1] + [tag.rstrip(), ''] + lines[insert_at + 1:]
            else:
                new = lines[:insert_at] + ['', tag.rstrip(), ''] + lines[insert_at:]
            return '\n'.join(new)
    return text


def main():
    changed = 0
    missing = 0
    for name, companies in COMPANY_TAGS.items():
        p = SRC / name
        if not p.exists():
            missing += 1
            print(f'  ! MISSING: {name}')
            continue
        text = p.read_text(encoding='utf-8')
        new_text = insert_tags(text, companies)
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            changed += 1
    print(f'Added CompanyTags to {changed}/{len(COMPANY_TAGS)} pages ({missing} missing).')


if __name__ == '__main__':
    main()
