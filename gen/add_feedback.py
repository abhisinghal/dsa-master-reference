"""Embed FeedbackWidget at the bottom of every problem page."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'


def extract_slug(name: str) -> str:
    return re.sub(r'^\d+v?-', '', name).replace('.md', '')


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<FeedbackWidget' in text:
        return False
    slug = extract_slug(path.name)
    block = f'\n<FeedbackWidget problem-slug="{slug}" />\n'
    path.write_text(text.rstrip() + '\n' + block, encoding='utf-8')
    return True


def main():
    changed = 0
    for md in sorted(SRC.iterdir()):
        if md.suffix != '.md' or md.name == '00-index.md':
            continue
        if process(md):
            changed += 1
    print(f'Added FeedbackWidget to {changed} pages.')


if __name__ == '__main__':
    main()
