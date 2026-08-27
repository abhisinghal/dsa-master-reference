"""One-shot: add hand-crafted drama-number sentences to problem pages missing D.

Each entry is per-problem hand-authored, tied to that problem's specific brute vs canonical
story. Runs from repo root: `python gen/add_drama_numbers.py`.
"""
from __future__ import annotations
import re
from pathlib import Path

# Per-file drama sentence appended to the **Constraints** — line.
# Keep each sentence compact (one line) and tied to the actual problem's numbers.
DRAMA = {
    '01v-fruit-into-baskets.md':
        'Brute enumerates every window in O(n²) = 10¹⁰ ops at n=10⁵ (TLE past ~30 s). Sliding window is O(n) = 10⁵ ops = <10 ms.',
    '01v-max-consecutive-ones-iii.md':
        'Brute expands every window in O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Sliding window with k-tolerance stays O(n) = 10⁵ ops.',
    '01v-minimum-size-subarray-sum.md':
        'Brute enumerates all subarrays in O(n²) = 10¹⁰ ops (TLE past n=10⁴). Sliding window is O(n) = 10⁵ ops = <5 ms.',
    '01v-permutation-in-string.md':
        'Brute compares every window against sorted target — O(n·k·log k) = 10⁴·10⁴·13 ≈ 1.3·10⁹ ops (TLE). Sliding-window frequency compare is O(n·26) = ~2·10⁵ ops.',
    '01v-find-all-anagrams-in-a-string.md':
        'Brute sorts every window in O(n·k·log k) = 3·10⁴·10⁴·13 ≈ 4·10⁹ ops (TLE). Sliding-window freq compare is O(n·26) ≈ 8·10⁵ ops.',
    '01v-longest-substring-with-at-most-k-distinct-characters.md':
        'Brute expands every window in O(n²·k) = 10¹⁰·k ops at n=10⁵ (TLE). Sliding window with a freq map is O(n) = 10⁵ ops.',
    '01v-longest-repeating-character-replacement.md':
        'Brute is O(n²·26) ≈ 2.6·10¹¹ ops at n=10⁵ (TLE). Sliding window (max-freq + k) is O(n·26) ≈ 2.6·10⁶ ops.',
    '01v-subarrays-with-k-different-integers.md':
        'Brute enumerates every subarray in O(n²) = 4·10⁸ ops at n=2·10⁴ (borderline TLE). Two sliding windows (`≤k` − `≤k−1`) run in O(n) = 2·10⁴ ops.',
    '01v-number-of-substrings-containing-all-three-characters.md':
        'Brute is O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Sliding window with the "shrink while valid" trick is O(n) = 10⁵ ops.',
    '01v-count-number-of-nice-subarrays.md':
        'Brute checks every subarray in O(n²) = 2.5·10⁹ ops at n=5·10⁴ (TLE). Sliding-window `atMost(k) − atMost(k−1)` is O(n) = 5·10⁴ ops.',
    '01v-binary-subarrays-with-sum.md':
        'Brute is O(n²) = 9·10⁸ ops at n=3·10⁴ (TLE past 5 s). Sliding-window `atMost(goal) − atMost(goal−1)` runs in O(n) = 3·10⁴ ops.',
    '02v-3sum-closest.md':
        'Brute enumerates every triple in O(n³) = 1.25·10⁸ ops at n=500 (borderline). Sort + two-pointer is O(n²) = 2.5·10⁵ ops.',
    '02v-3sum-smaller.md':
        'Brute is O(n³) ≈ 4·10¹⁰ ops at n=3500 (TLE). Sort + two-pointer with count is O(n²) ≈ 1.2·10⁷ ops.',
    '02v-largest-rectangle-in-histogram.md':
        'Brute enumerates every (l, r) window in O(n²) = 10¹⁰ ops at n=10⁵ (TLE). Monotonic stack runs each index in amortised O(1) → O(n) = 10⁵ ops = <10 ms.',
    '02v-move-zeroes.md':
        'Brute (build a fresh array and copy back) is O(n) time + O(n) space. Two-pointer in-place stays O(n) = 10⁴ ops with O(1) extra space.',
}


def already_has_drama(text: str) -> bool:
    return bool(
        re.search(r'\b1[0-9]\^[6-9]', text) or
        re.search(r'10[\u2076\u2077\u2078\u2079\u00b9]', text) or
        re.search(r'\b10\^[6-9]', text) or
        re.search(r'\b\d+\s*(?:min|sec|hour|day|year|billion|trillion)', text, re.IGNORECASE)
    )


CONSTRAINT_RX = re.compile(r'^(\*\*Constraints\*\*\s*—\s*.+?)(\.?)\s*$', re.MULTILINE)


def append_drama(text: str, drama: str) -> str | None:
    match = CONSTRAINT_RX.search(text)
    if not match:
        return None
    original = match.group(1).rstrip()
    if not original.endswith('.'):
        original += '.'
    new_line = f'{original} {drama}'
    return text[:match.start()] + new_line + text[match.end():]


def main() -> None:
    src = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'
    changed = 0
    for name, drama in DRAMA.items():
        path = src / name
        if not path.exists():
            print(f'  skip (missing): {name}')
            continue
        text = path.read_text(encoding='utf-8')
        if already_has_drama(text):
            print(f'  skip (already has D): {name}')
            continue
        updated = append_drama(text, drama)
        if updated is None:
            print(f'  skip (no constraint line): {name}')
            continue
        path.write_text(updated, encoding='utf-8')
        changed += 1
        print(f'  +D {name}')
    print(f'\nDone: added drama to {changed}/{len(DRAMA)} pages.')


if __name__ == '__main__':
    main()
