"""
Add missing Constraints lines to BS-on-Answer pages, flagship pages, and other pages
identified in the audit. Also add missing Examples where missing.
"""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'

# Manual fix map: filename -> {'examples': [...], 'constraints': '...'}
FIXES = {
    '08v-capacity-to-ship-packages-within-d-days.md': {
        'constraints': '**Constraints** — `1 ≤ days ≤ n ≤ 5·10⁴`; `1 ≤ weights[i] ≤ 500`.'
    },
    '08v-divide-chocolate.md': {
        'constraints': '**Constraints** — `1 ≤ k+1 ≤ n ≤ 10⁴`; `1 ≤ sweetness[i] ≤ 10⁵`.'
    },
    '08v-find-k-th-smallest-pair-distance.md': {
        'constraints': '**Constraints** — `n·(n-1)/2 ≥ k ≥ 1`; `2 ≤ n ≤ 10⁴`.'
    },
    '08v-kth-smallest-element-in-a-sorted-matrix.md': {
        'constraints': '**Constraints** — `1 ≤ n ≤ 300`; `1 ≤ k ≤ n²`.'
    },
    '08v-median-of-two-sorted-arrays.md': {
        'constraints': '**Constraints** — `0 ≤ n, m ≤ 1000`; total ≥ 1.'
    },
    '08v-minimize-max-distance-to-gas-station.md': {
        'constraints': '**Constraints** — `10 ≤ stations.length ≤ 2000`; `0 ≤ stations[i] ≤ 10⁸`.'
    },
    '08v-path-with-minimum-effort.md': {
        'constraints': '**Constraints** — `1 ≤ m, n ≤ 100`; `0 ≤ height[i][j] ≤ 10⁶`.'
    },
    '08v-split-array-largest-sum.md': {
        'constraints': '**Constraints** — `1 ≤ m ≤ n ≤ 1000`; `0 ≤ nums[i] ≤ 10⁶`.'
    },
    '12-sweep-line-meeting-rooms-ii.md': {
        'constraints': '**Constraints** — `1 ≤ n ≤ 10⁴`; `0 ≤ start < end ≤ 10⁶`.'
    },
    '18-dp-house-robber.md': {
        'constraints': '**Constraints** — `1 ≤ n ≤ 100`; `0 ≤ nums[i] ≤ 400`.'
    },
    '18v-edit-distance.md': {
        'constraints': '**Constraints** — `0 ≤ m, n ≤ 500`.'
    },
    '18v-best-time-to-buy-and-sell-stock-iv.md': {
        'examples': ['**Example 1** — `k=2, prices=[2,4,1]` → `2`', '**Example 2** — `k=2, prices=[3,2,6,5,0,3]` → `7`']
    },
    '18v-dungeon-game.md': {
        'examples': ['**Example 1** — `dungeon=[[-2,-3,3],[-5,-10,1],[10,30,-5]]` → `7`', '**Example 2** — `dungeon=[[0]]` → `1`']
    },
    '18v-find-the-shortest-superstring.md': {
        'examples': ['**Example 1** — `words=["alex","loves","leetcode"]` → `"alexlovesleetcode"`', '**Example 2** — `words=["catg","ctaagt","gcta","ttca","atgcatc"]` → `"gctaagttcatgcatc"`']
    },
    '18v-number-of-ways-to-wear-different-hats-to-each-other.md': {
        'examples': ['**Example 1** — `hats=[[3,4],[4,5],[5]]` → `1`', '**Example 2** — `hats=[[3,5,1],[3,5]]` → `4`', '**Example 3** — `hats=[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]` → `24`']
    },
    '18v-paint-house-ii.md': {
        'examples': ['**Example 1** — `costs=[[1,5,3],[2,9,4]]` → `5`', '**Example 2** — `costs=[[1,3],[2,4]]` → `5`']
    },
    '18v-shortest-path-visiting-all-nodes.md': {
        'examples': ['**Example 1** — `graph=[[1,2,3],[0],[0],[0]]` → `4`', '**Example 2** — `graph=[[1],[0,2,4],[1,3,4],[2],[1,2]]` → `4`']
    },
    '19v-maximum-genetic-difference-query.md': {
        'examples': ['**Example 1** — `parents=[-1,0,1,1], queries=[[0,2],[3,2],[2,5]]` → `[2,3,7]`']
    },
    '16v-robot-room-cleaner.md': {
        'examples': ['**Example 1** — Room modeled as grid with obstacles; robot at `(row, col)`. Robot cleans every reachable cell.']
    },
    '16v-unique-paths-iii.md': {
        'examples': ['**Example 1** — `grid=[[1,0,0,0],[0,0,0,0],[0,0,2,-1]]` → `2`', '**Example 2** — `grid=[[1,0,0,0],[0,0,0,0],[0,0,0,2]]` → `4`', '**Example 3** — `grid=[[0,1],[2,0]]` → `0`']
    },
    '16v-valid-sudoku.md': {
        'examples': ['**Example 1** — Standard partially-filled 9×9 board → `true`', '**Example 2** — Same as 1 but with two `8`s in same column → `false`']
    },
}


def insert_after_paragraph(text, insertion):
    """Insert `insertion` block after the problem paragraph but before ## or ---."""
    lines = text.splitlines()
    # Find first line that's a heading (##) or separator (---)
    for i, ln in enumerate(lines):
        if ln.startswith('##') or ln.strip() == '---':
            # Insert before this line, with blank separator
            new = lines[:i] + insertion.splitlines() + [''] + lines[i:]
            return '\n'.join(new)
    return text + '\n\n' + insertion


def add_constraints(text, constraints_line):
    if '**Constraints**' in text:
        return text
    # Find right position: after examples or right before first ##
    lines = text.splitlines()
    # Find last **Example line
    last_example = -1
    for i, ln in enumerate(lines):
        if ln.startswith('**Example'):
            last_example = i
    if last_example >= 0:
        # Insert after last example line + blank
        new = lines[:last_example + 1] + ['', constraints_line] + lines[last_example + 1:]
    else:
        # Insert before first ## or ---
        for i, ln in enumerate(lines):
            if ln.startswith('##') or ln.strip() == '---':
                new = lines[:i] + [constraints_line, ''] + lines[i:]
                break
        else:
            return text
    return '\n'.join(new)


def add_examples(text, examples_list):
    if '**Example' in text:
        return text
    lines = text.splitlines()
    # Find the LC link line, then problem paragraph, then insert examples before ## or ---
    for i, ln in enumerate(lines):
        if ln.startswith('##') or ln.strip() == '---':
            # Back up to find previous non-empty line (end of problem para)
            j = i - 1
            while j > 0 and lines[j].strip() == '':
                j -= 1
            block = [''] + examples_list
            new = lines[:j + 1] + block + [''] + lines[i:]
            return '\n'.join(new)
    return text


def process():
    changed = 0
    for name, fixes in FIXES.items():
        p = SRC / name
        if not p.exists():
            print(f'  ! missing {name}')
            continue
        text = p.read_text(encoding='utf-8')
        original = text
        if 'examples' in fixes and '**Example' not in text:
            text = add_examples(text, fixes['examples'])
        if 'constraints' in fixes and '**Constraints**' not in text:
            text = add_constraints(text, fixes['constraints'])
        if text != original:
            p.write_text(text, encoding='utf-8')
            changed += 1
            print(f'  + {name}')
    print(f'Total updated: {changed}')


if __name__ == '__main__':
    process()
