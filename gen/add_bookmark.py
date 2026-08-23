"""Embed Bookmark button right after MarkSolved on each problem page."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'


def strip_prefix(stem: str) -> str:
    return re.sub(r'^\d+v?-', '', stem)


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<Bookmark ' in text or '<Bookmark\n' in text:
        return False
    slug = strip_prefix(path.stem)
    tag = f'<Bookmark problem-slug="{slug}" />'
    m = re.search(r'<MarkSolved[^>]*/>', text)
    if not m:
        return False
    # Insert immediately after MarkSolved tag (before InterviewTimer which lives after it)
    text = text[:m.end()] + ' ' + tag + text[m.end():]
    path.write_text(text, encoding='utf-8')
    return True


def main():
    changed = 0
    total = 0
    for p in SRC.glob('*.md'):
        if p.stem in {'00-index'}:
            continue
        total += 1
        if process(p):
            changed += 1
    print(f'Added Bookmark to {changed}/{total} problem pages.')


if __name__ == '__main__':
    main()
