"""Embed PrintButton right after the PatternVideo tag on each pattern chapter."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'

PATTERN_FILES = [
    '21-sliding-window.md', '22-two-pointers.md', '23-fast-slow.md',
    '24-prefix-sum.md', '25-hashing.md', '26-monotonic-stack.md',
    '27-binary-search.md', '28-bs-on-answer.md', '29-top-k-heap.md',
    '30-k-way-merge.md', '31-merge-intervals.md', '32-sweep-line.md',
    '33-topological-sort.md', '34-union-find.md', '35-greedy.md',
    '36-backtracking.md', '37-divide-conquer.md', '38-dp.md',
    '39-trie-pattern.md', '40-bit-manip.md', '41-quickselect.md',
    '42-math.md', '44-design.md',
]


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<PrintButton' in text:
        return False
    # Place it before RelatedPatterns at end of chapter
    if '<RelatedPatterns' in text:
        text = text.replace('<RelatedPatterns', '<PrintButton />\n\n<RelatedPatterns', 1)
    else:
        text = text.rstrip() + '\n\n<PrintButton />\n'
    path.write_text(text, encoding='utf-8')
    return True


def main():
    changed = 0
    for name in PATTERN_FILES:
        p = SRC / name
        if not p.exists():
            print(f'  ! MISSING: {name}')
            continue
        if process(p):
            changed += 1
    print(f'Added PrintButton to {changed}/{len(PATTERN_FILES)} pattern chapters.')


if __name__ == '__main__':
    main()
