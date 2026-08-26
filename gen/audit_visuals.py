#!/usr/bin/env python3
"""
gen/audit_visuals.py — visual + a11y audit over the 21 pattern chapters.

Report-only. Prints a table of every SVG (fenced ```svg block) and Vue anim
component embed, flagging:

    R  = missing role="img" (screen-reader landmarks)
    A  = missing aria-label / aria-labelledby
    F  = font-size < 11px (unreadable at 1x on 4K displays)
    H  = hard-coded hex color (#rrggbb) instead of --dsa-* token
    W  = fixed pixel width without viewBox (breaks responsive)
    N  = no <text> caption or preceding "How to read it" prose within 100 chars

Also emits SUMMARY counts per category and per chapter.

Not opinionated about which issues to fix — that's for the operator to decide
based on the chapter's editorial priority. This script is the eyes; the hands
are separate.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from collections import Counter

SRC = Path(__file__).parent.parent / 'gen' / 'src'
PATTERNS = [
    '21-sliding-window', '22-two-pointers', '23-fast-slow', '24-prefix-sum',
    '25-hashing', '26-monotonic-stack', '27-binary-search', '28-bs-on-answer',
    '29-top-k-heap', '30-k-way-merge', '31-merge-intervals', '32-sweep-line',
    '33-topological-sort', '34-union-find', '35-greedy', '36-backtracking',
    '37-divide-conquer', '38-dp', '39-trie-pattern', '40-bit-manip',
    '41-quickselect',
]

# Regex to extract each fenced ```svg block plus its trailing readfig caption.
SVG_BLOCK = re.compile(r'^```svg\n(.*?)\n^```', re.MULTILINE | re.DOTALL)
CAPTION_HINT = re.compile(r'<div class="readfig"|<p class="secgoal"|<b>How to read it')


def audit_svg(svg: str) -> list[str]:
    """Return list of one-letter flags for issues in this SVG block."""
    flags = []
    if 'role="img"' not in svg and 'role=\'img\'' not in svg:
        flags.append('R')
    if 'aria-label' not in svg and 'aria-labelledby' not in svg:
        flags.append('A')
    # Look for font-size below 11 (integer or "10.5px")
    font_matches = re.findall(r'font-size\s*=\s*["\']?(\d+(?:\.\d+)?)', svg)
    small_fonts = [f for f in font_matches if float(f) < 11]
    if small_fonts:
        flags.append('F')
    # Hard-coded hex (not in a var() reference)
    # Strip var(--x) references first, then look for #rrggbb / #rgb outside them.
    stripped = re.sub(r'var\([^)]*\)', '', svg)
    if re.search(r'#[0-9a-fA-F]{3,6}\b', stripped):
        flags.append('H')
    # Fixed width without viewBox: literal `width="720"` and no viewBox at all.
    if re.search(r'<svg\b[^>]*\bwidth=', svg) and 'viewBox' not in svg:
        flags.append('W')
    return flags


def audit_chapter(name: str) -> dict:
    """Return per-chapter audit result."""
    text = (SRC / f'{name}.md').read_text(encoding='utf-8')
    svgs = list(SVG_BLOCK.finditer(text))
    result = {'name': name, 'svg_count': len(svgs), 'issues': []}
    for i, m in enumerate(svgs):
        svg = m.group(1)
        flags = audit_svg(svg)
        # Caption check: look at 200 chars AFTER the closing ``` for a caption element
        end = m.end()
        trailing = text[end:end + 300]
        if not CAPTION_HINT.search(trailing):
            flags.append('N')
        if flags:
            result['issues'].append({'idx': i, 'flags': ''.join(sorted(flags))})
    return result


def main() -> int:
    all_results = [audit_chapter(name) for name in PATTERNS]
    print('Visual + a11y audit — 21 pattern chapters')
    print('Flag legend: R=role="img"  A=aria-label  F=small font  H=hard-coded hex  W=fixed width  N=missing caption')
    print()
    print(f'{"Chapter":<24} {"SVGs":>5} {"Issues":>7}  Flags per SVG (idx:flags)')
    print('-' * 100)
    counter: Counter = Counter()
    total_svgs = 0
    total_flagged = 0
    for r in all_results:
        total_svgs += r['svg_count']
        total_flagged += len(r['issues'])
        flag_str = ', '.join(f'{iss["idx"]}:{iss["flags"]}' for iss in r['issues']) or '(clean)'
        # Truncate long strings
        if len(flag_str) > 60:
            flag_str = flag_str[:57] + '...'
        for iss in r['issues']:
            for c in iss['flags']:
                counter[c] += 1
        print(f'{r["name"]:<24} {r["svg_count"]:>5} {len(r["issues"]):>7}  {flag_str}')
    print()
    print('-' * 100)
    print(f'Total: {total_svgs} SVGs, {total_flagged} with issues.')
    print()
    print('Issues by flag:')
    labels = {
        'R': 'missing role="img"',
        'A': 'missing aria-label',
        'F': 'font-size < 11px',
        'H': 'hard-coded hex color',
        'W': 'fixed width without viewBox',
        'N': 'no readfig / caption in next 300 chars',
    }
    for k in 'RAFHWN':
        print(f'  {k}  {labels[k]:<40} {counter[k]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
