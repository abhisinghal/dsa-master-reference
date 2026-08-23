"""Embed RelatedProblems on each problem page.

Uses pattern grouping from add_pattern_progress.py PATTERN_PROBLEMS.
For each problem, finds 3 sibling problems from same pattern.
"""
import re
import random
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'

# Reuse the exact list from add_pattern_progress.py (kept in sync manually).
PATTERN_GROUPS = {
    'sliding-window': [
        'sliding-window-longest-substring', 'minimum-window-substring',
        'longest-repeating-character-replacement', 'max-consecutive-ones-iii',
        'minimum-size-subarray-sum', 'permutation-in-string',
        'find-all-anagrams-in-a-string', 'longest-substring-with-at-most-k-distinct-characters',
        'fruit-into-baskets', 'subarrays-with-k-different-integers',
        'binary-subarrays-with-sum', 'count-number-of-nice-subarrays',
        'subarray-product-less-than-k', 'number-of-substrings-containing-all-three-characters',
        'longest-palindromic-substring', 'trapping-rain-water',
        'shortest-subarray-with-sum-at-least-k',
    ],
    'two-pointers': [
        'container-with-most-water', '3sum-closest', '3sum-smaller', '4sum',
        'valid-palindrome-ii', 'boats-to-save-people', 'merge-sorted-array',
        'move-zeroes', 'sort-array-by-parity', 'squares-of-a-sorted-array',
    ],
    'fast-slow': [
        'fast-slow-linked-list-cycle-ii', 'linked-list-cycle',
        'middle-of-the-linked-list', 'happy-number',
        'find-the-duplicate-number', 'palindrome-linked-list',
    ],
    'prefix-sum': [
        'prefix-sum-subarray-sum-equals-k', 'subarray-sums-divisible-by-k',
        'contiguous-array', 'continuous-subarray-sum', 'corporate-flight-bookings',
        'car-pooling', 'range-addition',
    ],
    'hashing': [
        'hashing-two-sum', '3sum', 'two-sum-ii-input-array-is-sorted',
        'valid-anagram', 'isomorphic-strings',
        'longest-consecutive-sequence', 'group-shifted-strings',
    ],
    'monotonic-stack': [
        'monotonic-stack-daily-temperatures', 'next-greater-element-ii',
        'online-stock-span', 'remove-k-digits', 'sum-of-subarray-minimums',
    ],
    'binary-search': [
        'binary-search-rotated-sorted', 'binary-search',
        'find-minimum-in-rotated-sorted-array', 'find-peak-element',
        'search-in-rotated-sorted-array-ii',
        'koko-bananas', 'capacity-to-ship-packages-within-d-days',
        'split-array-largest-sum', 'median-of-two-sorted-arrays',
    ],
    'top-k-heap': [
        'top-k-frequent-elements', 'k-closest-points-to-origin',
        'kth-largest-element-in-a-stream', 'reorganize-string',
        'k-way-merge-k-sorted-lists', 'merge-two-sorted-lists',
        'smallest-range-covering-elements-from-k-lists', 'ugly-number-ii',
    ],
    'intervals': [
        'merge-intervals-classic', 'insert-interval', 'meeting-rooms',
        'interval-list-intersections', 'employee-free-time', 'remove-covered-intervals',
        'meeting-rooms-ii', 'my-calendar-ii', 'the-skyline-problem',
    ],
    'topological-sort': [
        'course-schedule', 'alien-dictionary', 'minimum-height-trees',
        'parallel-courses', 'sequence-reconstruction',
    ],
    'union-find': [
        'number-of-provinces', 'accounts-merge', 'redundant-connection',
        'number-of-islands-ii', 'most-stones-removed-with-same-row-or-column',
        'connecting-cities-with-minimum-cost', 'min-cost-to-connect-all-points',
    ],
    'greedy': [
        'jump-game-ii', 'jump-game', 'gas-station', 'best-time-to-buy-and-sell-stock',
        'maximum-subarray', 'non-overlapping-intervals',
        'minimum-number-of-arrows-to-burst-balloons', 'course-schedule-iii',
    ],
    'backtracking': [
        'n-queens', 'permutations', 'permutations-ii', 'subsets-ii',
        'combination-sum-ii', 'combination-sum-iii', 'combination-sum-iv',
        'letter-combinations-of-a-phone-number', 'palindrome-partitioning',
        'n-queens-ii', 'sudoku-solver', 'beautiful-arrangement',
    ],
    'divide-conquer': [
        'inversions', 'count-of-range-sum', 'reverse-pairs',
        'global-and-local-inversions', 'sort-list',
    ],
    'dp': [
        'house-robber', 'climbing-stairs', 'house-robber-ii', 'delete-and-earn',
        'min-cost-climbing-stairs', 'coin-change', 'coin-change-ii',
        'longest-increasing-subsequence', 'longest-common-subsequence',
        'edit-distance', 'longest-palindromic-subsequence',
        'partition-equal-subset-sum', 'target-sum', 'unique-paths-ii',
        'maximal-square', 'burst-balloons', 'regular-expression-matching',
        'palindrome-partitioning-ii',
    ],
    'trie': [
        'word-search-ii', 'design-add-and-search-words-data-structure',
        'replace-words', 'concatenated-words', 'stream-of-characters',
        'trie-word-search-ii',
    ],
    'bit-manip': [
        'single-number', 'missing-number', 'find-the-difference',
        'number-of-1-bits', 'hamming-distance', 'power-of-two',
        'reverse-bits', 'maximum-product-of-word-lengths',
    ],
}


def slug_to_title(slug: str) -> str:
    """slug-with-dashes -> Slug With Dashes"""
    words = []
    for w in slug.split('-'):
        if w.lower() in {'ii', 'iii', 'iv', 'k', 'i'}:
            words.append(w.upper())
        elif w.isdigit():
            words.append(w)
        else:
            words.append(w[:1].upper() + w[1:])
    return ' '.join(words)


def get_related(slug: str) -> list:
    """Return list of (slug, title) for up to 3 siblings from same pattern."""
    for pattern, siblings in PATTERN_GROUPS.items():
        if slug in siblings:
            others = [s for s in siblings if s != slug]
            random.seed(hash(slug))
            picks = random.sample(others, min(3, len(others)))
            return [(p, slug_to_title(p)) for p in picks]
    return []


def strip_prefix(stem: str) -> str:
    """Strip NN- or NNv- prefix from filename stem."""
    return re.sub(r'^\d+v?-', '', stem)


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<RelatedProblems' in text:
        return False
    slug = strip_prefix(path.stem)
    related = get_related(slug)
    if not related:
        return False
    joined = '|'.join(f'{s}::{t}' for s, t in related)
    block = f'\n\n<RelatedProblems problems="{joined}" />\n'
    text = text.rstrip() + block
    path.write_text(text, encoding='utf-8')
    return True


def main():
    changed = 0
    total = 0
    for p in SRC.glob('*.md'):
        total += 1
        if process(p):
            changed += 1
    print(f'Added RelatedProblems to {changed}/{total} problem pages.')


if __name__ == '__main__':
    main()
