"""Embed <PatternVideo /> at the top of each pattern chapter and <AiCompanion /> on every problem page."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'
PROBS = SRC / 'problems'

# Pattern chapter -> pattern name
PATTERNS = [
    ('21-sliding-window.md', 'Sliding Window'),
    ('22-two-pointers.md', 'Two Pointers'),
    ('23-fast-slow.md', 'Fast & Slow Pointers'),
    ('24-prefix-sum.md', 'Prefix Sum'),
    ('25-hashing.md', 'Hashing'),
    ('26-monotonic-stack.md', 'Monotonic Stack'),
    ('27-binary-search.md', 'Binary Search'),
    ('28-bs-on-answer.md', 'Binary Search on the Answer'),
    ('29-top-k-heap.md', 'Top-K / Heap'),
    ('30-k-way-merge.md', 'K-way Merge'),
    ('31-merge-intervals.md', 'Merge Intervals'),
    ('32-sweep-line.md', 'Sweep Line'),
    ('33-topological-sort.md', 'Topological Sort'),
    ('34-union-find.md', 'Union-Find'),
    ('35-greedy.md', 'Greedy'),
    ('36-backtracking.md', 'Backtracking'),
    ('37-divide-conquer.md', 'Divide & Conquer'),
    ('38-dp.md', 'Dynamic Programming'),
    ('39-trie-pattern.md', 'Trie'),
    ('40-bit-manip.md', 'Bit Manipulation'),
    ('41-quickselect.md', 'Quickselect'),
]


def add_video_to_pattern(path: Path, name: str) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<PatternVideo' in text:
        return False
    block = f'\n<PatternVideo pattern-name="{name}" duration="8–12 min" />\n\n'
    # Insert after the H1 title (first line starting with `# `)
    lines = text.splitlines(keepends=False)
    for i, ln in enumerate(lines):
        if ln.startswith('# ') and i > 0:
            # Assume H1 is at index 0 usually; but be defensive
            pass
        if ln.startswith('# '):
            # Insert after the H1 and its optional subtitle paragraph
            insert_at = i + 1
            # Skip blank line, secgoal paragraph (`<p class="secgoal"...>`), then blank line
            while insert_at < len(lines) and (
                lines[insert_at].strip() == '' or lines[insert_at].startswith('<p class="secgoal"')
            ):
                insert_at += 1
            new_lines = lines[:insert_at] + [block.rstrip()] + [''] + lines[insert_at:]
            path.write_text('\n'.join(new_lines), encoding='utf-8')
            return True
    return False


def slug_of(name: str) -> str:
    return re.sub(r'^\d+v?-', '', name).replace('.md', '')


PATTERN_HINTS = {
    '01': 'sliding window', '02': 'two pointers', '03': 'fast/slow pointers',
    '04': 'prefix sum', '05': 'hashing', '06': 'monotonic stack',
    '07': 'binary search', '08': 'binary search on answer',
    '09': 'top-K / heap', '10': 'k-way merge',
    '11': 'merge intervals', '12': 'sweep line',
    '13': 'topological sort', '14': 'union-find',
    '15': 'greedy', '16': 'backtracking',
    '17': 'divide & conquer', '18': 'dynamic programming',
    '19': 'trie', '20': 'bit manipulation', '21': 'quickselect',
}


def add_ai_to_problem(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<AiCompanion' in text:
        return False
    prefix = path.name[:2]
    hint = PATTERN_HINTS.get(prefix, 'this pattern')
    slug = slug_of(path.name)
    block = f'<AiCompanion problem-slug="{slug}" pattern-hint="{hint}" />\n'
    # Insert BEFORE "## Related problems" if present, else at end
    for anchor in ['## Related problems']:
        idx = text.find(anchor)
        if idx >= 0:
            text = text[:idx].rstrip() + '\n\n' + block + '\n' + text[idx:]
            path.write_text(text, encoding='utf-8')
            return True
    # Fallback: append
    path.write_text(text.rstrip() + '\n\n' + block, encoding='utf-8')
    return True


def main():
    v = 0
    for name, pname in PATTERNS:
        p = SRC / name
        if p.exists() and add_video_to_pattern(p, pname):
            v += 1
    print(f'Added PatternVideo to {v}/{len(PATTERNS)} pattern chapters.')
    a = 0
    for md in sorted(PROBS.iterdir()):
        if md.suffix != '.md' or md.name == '00-index.md':
            continue
        if add_ai_to_problem(md):
            a += 1
    print(f'Added AiCompanion to {a} problem pages.')


if __name__ == '__main__':
    main()
