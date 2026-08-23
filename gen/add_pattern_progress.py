"""Embed PatternProgress at top of each pattern chapter (after PatternVideo)."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'

# Pattern chapter -> (pattern_id, list of problem slugs used in that chapter)
PATTERN_PROBLEMS = {
    '21-sliding-window.md': ('sliding-window', [
        'sliding-window-longest-substring', 'minimum-window-substring',
        'longest-repeating-character-replacement', 'max-consecutive-ones-iii',
        'minimum-size-subarray-sum', 'permutation-in-string',
        'find-all-anagrams-in-a-string', 'longest-substring-with-at-most-k-distinct-characters',
        'fruit-into-baskets', 'subarrays-with-k-different-integers',
        'binary-subarrays-with-sum', 'count-number-of-nice-subarrays',
        'subarray-product-less-than-k', 'number-of-substrings-containing-all-three-characters',
        'longest-palindromic-substring', 'trapping-rain-water',
        'shortest-subarray-with-sum-at-least-k', 'jump-game-vi',
        'constrained-subsequence-sum', 'diet-plan-performance',
        'maximum-average-subarray-i', 'minimum-window-subsequence',
        'replace-the-substring-for-balanced-string', 'get-equal-substrings-within-budget',
        'substring-with-concatenation-of-all-words', 'frequency-of-the-most-frequent-element',
    ]),
    '22-two-pointers.md': ('two-pointers', [
        'container-with-most-water', '3sum-closest', '3sum-smaller', '4sum',
        'valid-palindrome-ii', 'boats-to-save-people', 'merge-sorted-array',
        'move-zeroes', 'sort-array-by-parity', 'squares-of-a-sorted-array',
        'trapping-rain-water-ii', 'largest-rectangle-in-histogram',
        'intersection-of-two-arrays-ii', 'wiggle-sort-ii',
    ]),
    '23-fast-slow.md': ('fast-slow', [
        'fast-slow-linked-list-cycle-ii', 'linked-list-cycle',
        'middle-of-the-linked-list', 'happy-number',
        'find-the-duplicate-number', 'palindrome-linked-list',
    ]),
    '24-prefix-sum.md': ('prefix-sum', [
        'prefix-sum-subarray-sum-equals-k', 'subarray-sums-divisible-by-k',
        'contiguous-array', 'continuous-subarray-sum', 'corporate-flight-bookings',
        'car-pooling', 'range-addition', 'matrix-block-sum',
        'count-submatrices-with-target-sum', 'maximal-rectangle',
    ]),
    '25-hashing.md': ('hashing', [
        'hashing-two-sum', '3sum', 'two-sum-ii-input-array-is-sorted',
        'two-sum-iii-data-structure-design', 'valid-anagram', 'isomorphic-strings',
        'longest-consecutive-sequence', 'group-shifted-strings',
        'maximum-product-subarray', 'number-of-islands', 'word-ladder', 'candy',
    ]),
    '26-monotonic-stack.md': ('monotonic-stack', [
        'monotonic-stack-daily-temperatures', 'next-greater-element-ii',
        'online-stock-span', 'remove-k-digits', 'sum-of-subarray-minimums',
    ]),
    '27-binary-search.md': ('binary-search', [
        'binary-search-rotated-sorted', 'binary-search',
        'find-minimum-in-rotated-sorted-array', 'find-peak-element',
        'search-in-rotated-sorted-array-ii',
    ]),
    '28-bs-on-answer.md': ('bs-on-answer', [
        'koko-bananas', 'capacity-to-ship-packages-within-d-days',
        'split-array-largest-sum', 'median-of-two-sorted-arrays',
        'kth-smallest-element-in-a-sorted-matrix', 'find-k-th-smallest-pair-distance',
        'minimize-max-distance-to-gas-station', 'path-with-minimum-effort',
        'divide-chocolate',
    ]),
    '29-top-k-heap.md': ('top-k-heap', [
        'top-k-frequent-elements', 'k-closest-points-to-origin',
        'kth-largest-element-in-a-stream', 'reorganize-string',
    ]),
    '30-k-way-merge.md': ('k-way-merge', [
        'k-way-merge-k-sorted-lists', 'merge-two-sorted-lists',
        'smallest-range-covering-elements-from-k-lists', 'ugly-number-ii',
    ]),
    '31-merge-intervals.md': ('merge-intervals', [
        'merge-intervals-classic', 'insert-interval', 'meeting-rooms',
        'interval-list-intersections', 'employee-free-time', 'remove-covered-intervals',
    ]),
    '32-sweep-line.md': ('sweep-line', [
        'meeting-rooms-ii', 'my-calendar-ii', 'the-skyline-problem',
    ]),
    '33-topological-sort.md': ('topological-sort', [
        'course-schedule', 'alien-dictionary', 'minimum-height-trees',
        'parallel-courses', 'sequence-reconstruction',
    ]),
    '34-union-find.md': ('union-find', [
        'number-of-provinces', 'accounts-merge', 'redundant-connection',
        'number-of-islands-ii', 'most-stones-removed-with-same-row-or-column',
        'connecting-cities-with-minimum-cost', 'min-cost-to-connect-all-points',
        'optimize-water-distribution-in-a-village',
        'find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree',
    ]),
    '35-greedy.md': ('greedy', [
        'jump-game-ii', 'jump-game', 'gas-station', 'best-time-to-buy-and-sell-stock',
        'maximum-subarray', 'non-overlapping-intervals',
        'minimum-number-of-arrows-to-burst-balloons', 'course-schedule-iii',
        'maximum-length-of-pair-chain', 'video-stitching', 'jump-game-iii',
    ]),
    '36-backtracking.md': ('backtracking', [
        'n-queens', 'permutations', 'permutations-ii', 'subsets-ii',
        'combination-sum-ii', 'combination-sum-iii', 'combination-sum-iv',
        'letter-combinations-of-a-phone-number', 'palindrome-partitioning',
        'n-queens-ii', 'sudoku-solver', 'valid-sudoku', 'beautiful-arrangement',
        'unique-paths-iii', 'robot-room-cleaner', 'next-permutation',
        'letter-case-permutation',
    ]),
    '37-divide-conquer.md': ('divide-conquer', [
        'inversions', 'count-of-range-sum', 'reverse-pairs',
        'global-and-local-inversions', 'sort-list',
    ]),
    '38-dp.md': ('dp', [
        'house-robber', 'climbing-stairs', 'house-robber-ii', 'delete-and-earn',
        'min-cost-climbing-stairs', 'coin-change', 'coin-change-ii',
        'longest-increasing-subsequence', 'longest-common-subsequence',
        'edit-distance', 'longest-palindromic-subsequence',
        'partition-equal-subset-sum', 'target-sum', 'unique-paths-ii',
        'maximal-square', 'burst-balloons', 'regular-expression-matching',
        'palindrome-partitioning-ii', 'best-time-to-buy-and-sell-stock-with-cooldown',
        'best-time-to-buy-and-sell-stock-with-transaction-fee',
        'best-time-to-buy-and-sell-stock-iv', 'partition-to-k-equal-sum-subsets',
        'perfect-squares', 'maximum-sum-circular-subarray', 'dungeon-game',
        'paint-house-ii', 'minimum-falling-path-sum', 'shortest-path-visiting-all-nodes',
        'find-the-shortest-superstring', 'number-of-ways-to-wear-different-hats-to-each-other',
        'last-stone-weight-ii', 'minimum-cost-to-merge-stones',
    ]),
    '39-trie-pattern.md': ('trie', [
        'word-search-ii', 'design-add-and-search-words-data-structure',
        'replace-words', 'concatenated-words', 'stream-of-characters',
        'maximum-xor-with-an-element-from-array', 'count-pairs-with-xor-in-a-range',
        'maximum-genetic-difference-query',
    ]),
    '40-bit-manip.md': ('bit-manip', [
        'single-number', 'missing-number', 'find-the-difference',
        'number-of-1-bits', 'hamming-distance', 'power-of-two',
        'reverse-bits', 'maximum-product-of-word-lengths',
        'sum-of-all-subset-xor-totals', 'subsets',
    ]),
    '41-quickselect.md': ('quickselect', ['kth-largest']),
}


def process(path: Path, pid: str, slugs: list) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<PatternProgress' in text:
        return False
    slugs_str = ', '.join(slugs)
    block = f'\n<PatternProgress pattern-id="{pid}" problems="{slugs_str}" />\n\n'
    # Insert AFTER <PatternVideo... /> (which was added at top)
    m = re.search(r'<PatternVideo[^>]*/>', text)
    if m:
        text = text[:m.end()] + block + text[m.end():]
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    changed = 0
    for name, (pid, slugs) in PATTERN_PROBLEMS.items():
        p = SRC / name
        if not p.exists():
            print(f'  ! MISSING: {name}')
            continue
        if process(p, pid, slugs):
            changed += 1
    print(f'Added PatternProgress to {changed}/{len(PATTERN_PROBLEMS)} pattern chapters.')


if __name__ == '__main__':
    main()
