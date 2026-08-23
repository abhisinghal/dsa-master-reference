"""Embed RelatedPatterns at the END of each pattern chapter (before closing appendix if any)."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'

PATTERN_MAP = {
    '21-sliding-window.md':    'sliding-window',
    '22-two-pointers.md':      'two-pointers',
    '23-fast-slow.md':         'fast-slow',
    '24-prefix-sum.md':        'prefix-sum',
    '25-hashing.md':           'hashing',
    '26-monotonic-stack.md':   'monotonic-stack',
    '27-binary-search.md':     'binary-search',
    '28-bs-on-answer.md':      'binary-search',
    '29-top-k-heap.md':        'heap',
    '30-k-way-merge.md':       'heap',
    '31-merge-intervals.md':   'intervals',
    '32-sweep-line.md':        'sweep-line',
    '33-topological-sort.md':  'topo-sort',
    '34-union-find.md':        'union-find',
    '35-greedy.md':            'greedy',
    '36-backtracking.md':      'backtracking',
    '37-divide-conquer.md':    'divide-conquer',
    '38-dp.md':                'dp',
    '39-trie-pattern.md':      'trie-pattern',
    '40-bit-manip.md':         'bit-manip',
    '41-quickselect.md':       'quickselect',
    '42-math.md':              'math',
    '44-design.md':            'design',
}


def process(path: Path, pid: str) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<RelatedPatterns' in text:
        return False
    block = f'\n\n<RelatedPatterns pattern-id="{pid}" />\n'
    # Append at end of file
    text = text.rstrip() + block
    path.write_text(text, encoding='utf-8')
    return True


def main():
    changed = 0
    for name, pid in PATTERN_MAP.items():
        p = SRC / name
        if not p.exists():
            print(f'  ! MISSING: {name}')
            continue
        if process(p, pid):
            changed += 1
    print(f'Added RelatedPatterns to {changed}/{len(PATTERN_MAP)} pattern chapters.')


if __name__ == '__main__':
    main()
