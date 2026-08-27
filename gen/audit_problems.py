#!/usr/bin/env python3
"""
gen/audit_problems.py — score all 206 problem pages against the reference-bar checklist.

For each page scores presence of:
  P  problem statement (LC link)
  E  >= 2 examples
  H  Hints widget
  N  >= 2 approaches (numbered)
  D  drama numbers in prose
  I  interview commentary in italics
  C  complexity summary table
  W  "When to use" section
  R  related-problems section
  A  >= 5 widgets embedded

Score 0-10, higher is closer to reference-bar quality.
Categorises STAR (>=7), OK (4-6), GAP (<=3).
"""
from __future__ import annotations
import re
from pathlib import Path
from collections import Counter

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'
WIDGETS = ['Hints', 'MarkSolved', 'Bookmark', 'InterviewTimer', 'JavaRunner', 'AiCompanion', 'FeedbackWidget']


def score_page(page: Path) -> dict:
    text = page.read_text(encoding='utf-8')
    flags = {}
    flags['P'] = 'leetcode.com/problems' in text
    flags['E'] = len(re.findall(r'\*\*Example\s*\d', text)) >= 2
    flags['H'] = '<Hints' in text
    flags['N'] = len(re.findall(r'##\s*Approach\s*\d', text)) >= 2
    dramatic = (
        re.search(r'\b1[0-9]\^[6-9]', text) or
        re.search(r'10[\u2076\u2077\u2078\u2079\u00b9]', text) or
        re.search(r'\b10\^[6-9]', text) or
        re.search(r'\b\d+\s*(?:min|sec|hour|day|year|billion|trillion)', text, re.IGNORECASE)
    )
    flags['D'] = bool(dramatic)
    commentary = re.search(
        r'\*[^*]*(?:interview|say (?:this |the )?(?:out |aloud)|out loud|In an interview|Interview commentary|voice out)[^*]*\*',
        text, re.IGNORECASE
    )
    flags['I'] = bool(commentary)
    flags['C'] = bool(re.search(r'##\s*Complexity\s*(?:summary|ladder)', text))
    flags['W'] = bool(re.search(r'##\s*When to use', text))
    flags['R'] = bool(re.search(r'##\s*Related (?:problems|patterns)', text)) or '<RelatedProblems' in text
    widgets_present = sum(1 for w in WIDGETS if f'<{w}' in text)
    flags['A'] = widgets_present >= 5
    total = sum(1 for v in flags.values() if v)
    return {'name': page.stem, 'score': total, 'flags': flags, 'widgets': widgets_present}


def bucket(score: int) -> str:
    if score >= 7: return 'STAR'
    if score >= 4: return 'OK'
    return 'GAP'


def main() -> int:
    pages = sorted([p for p in SRC.glob('*.md') if p.stem != '00-index'])
    results = [score_page(p) for p in pages]

    print(f'Audit: {len(pages)} problem pages')
    print()

    grouped: dict[str, list[dict]] = {}
    for r in results:
        m = re.match(r'^(\d+)v?-', r['name'])
        prefix = m.group(1) if m else '??'
        grouped.setdefault(prefix, []).append(r)

    print(f'{"Family":<8} {"Total":>6} {"STAR":>5} {"OK":>5} {"GAP":>5}  Median')
    print('-' * 60)
    for prefix in sorted(grouped.keys(), key=lambda x: int(x)):
        pgs = grouped[prefix]
        b = Counter(bucket(r['score']) for r in pgs)
        med = sorted(r['score'] for r in pgs)[len(pgs) // 2]
        print(f'{prefix:<8} {len(pgs):>6} {b["STAR"]:>5} {b["OK"]:>5} {b["GAP"]:>5}  {med}')

    all_b = Counter(bucket(r['score']) for r in results)
    print()
    print(f'Overall: {all_b["STAR"]} STAR, {all_b["OK"]} OK, {all_b["GAP"]} GAP')
    print()

    labels = {
        'P': 'problem+LC', 'E': '>=2 examples', 'H': 'Hints', 'N': '>=2 approaches',
        'D': 'drama numbers', 'I': 'interview commentary', 'C': 'complexity table',
        'W': 'when-to-use', 'R': 'related problems', 'A': '>=5 widgets'
    }
    fc: Counter = Counter()
    for r in results:
        for k, v in r['flags'].items():
            if v:
                fc[k] += 1
    print('Feature coverage:')
    for k in 'PEHNDICWRA':
        print(f'  {k}  {labels[k]:<25} {fc[k]:>3}/{len(results)}  ({100*fc[k]/len(results):>4.0f}%)')

    print()
    print('Top-15 weakest pages:')
    for r in sorted(results, key=lambda x: x['score'])[:15]:
        missing = ''.join(k for k, v in r['flags'].items() if not v)
        print(f'  {r["score"]:>2}  {r["name"]:<50}  missing:{missing}')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
