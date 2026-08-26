#!/usr/bin/env python3
"""
gen/fix_svg_a11y.py — auto-fix R and A flags from audit_visuals.py.

For every ```svg fenced block in the 21 pattern chapters:
  - If the outer <svg> element lacks role="img", add it.
  - If it lacks aria-label, add one derived from the nearest preceding
    H2/H3 title (or the SVG's own <text> title element).

Idempotent — safe to re-run. Reports counts.
"""
from __future__ import annotations

import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'
PATTERNS = [
    '21-sliding-window', '22-two-pointers', '23-fast-slow', '24-prefix-sum',
    '25-hashing', '26-monotonic-stack', '27-binary-search', '28-bs-on-answer',
    '29-top-k-heap', '30-k-way-merge', '31-merge-intervals', '32-sweep-line',
    '33-topological-sort', '34-union-find', '35-greedy', '36-backtracking',
    '37-divide-conquer', '38-dp', '39-trie-pattern', '40-bit-manip',
    '41-quickselect',
]

SVG_BLOCK = re.compile(r'(^```svg\n)(.*?)(\n^```)', re.MULTILINE | re.DOTALL)


def derive_label(chapter_name: str, preceding_text: str, svg: str) -> str:
    """Best-effort label from preceding H2/H3 title, then SVG's title text, then chapter name."""
    # 1. Nearest preceding H2/H3 in the last 800 chars
    heads = re.findall(r'^#{2,3}\s+(.+?)$', preceding_text[-1200:], re.MULTILINE)
    if heads:
        # Strip HTML entities / markdown syntax
        title = heads[-1].strip()
        title = re.sub(r'<[^>]+>', '', title)
        title = re.sub(r'[*_`]', '', title).strip()
        if title and len(title) < 100:
            return f'Diagram illustrating: {title}'
    # 2. SVG's own font-weight="700" text elements (headings inside the chart)
    heading_text = re.search(r'<text[^>]*font-weight="7\d\d"[^>]*>([^<]{4,100})</text>', svg)
    if heading_text:
        return heading_text.group(1).strip()
    # 3. Fallback: chapter name
    return f'{chapter_name.split("-", 1)[1].replace("-", " ")} diagram'


def fix_svg(chapter_name: str, preceding: str, svg_body: str) -> tuple[str, bool, bool]:
    """Return (fixed_svg_body, added_role, added_aria)."""
    added_role = False
    added_aria = False
    label = derive_label(chapter_name, preceding, svg_body)
    label_esc = label.replace('"', '&quot;')

    # Find the outer <svg ...> opening tag
    m = re.search(r'<svg\b([^>]*)>', svg_body)
    if not m:
        return svg_body, False, False
    open_attrs = m.group(1)

    if 'role=' not in open_attrs:
        open_attrs = ' role="img"' + open_attrs
        added_role = True
    if 'aria-label' not in open_attrs and 'aria-labelledby' not in open_attrs:
        open_attrs = open_attrs + f' aria-label="{label_esc}"'
        added_aria = True

    if not (added_role or added_aria):
        return svg_body, False, False
    new_open = f'<svg{open_attrs}>'
    return svg_body[:m.start()] + new_open + svg_body[m.end():], added_role, added_aria


def process(path: Path, chapter_name: str) -> tuple[int, int]:
    text = path.read_text(encoding='utf-8')
    role_added = 0
    aria_added = 0
    result = []
    last_end = 0
    for m in SVG_BLOCK.finditer(text):
        # Emit content before this block
        result.append(text[last_end:m.start()])
        # Preceding context is text up to this block
        preceding = text[:m.start()]
        opener, body, closer = m.group(1), m.group(2), m.group(3)
        fixed_body, r_added, a_added = fix_svg(chapter_name, preceding, body)
        if r_added: role_added += 1
        if a_added: aria_added += 1
        result.append(opener + fixed_body + closer)
        last_end = m.end()
    result.append(text[last_end:])
    new_text = ''.join(result)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
    return role_added, aria_added


def main() -> int:
    total_role = 0
    total_aria = 0
    for name in PATTERNS:
        r, a = process(SRC / f'{name}.md', name)
        total_role += r
        total_aria += a
        if r or a:
            print(f'  {name:<24} +role={r:>2}  +aria-label={a:>2}')
    print()
    print(f'Total: added role="img" to {total_role} SVGs, aria-label to {total_aria} SVGs.')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
