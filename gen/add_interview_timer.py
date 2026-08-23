"""Embed InterviewTimer on each problem page right after CompanyTags (or after H1 if CompanyTags absent)."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'


def strip_prefix(stem: str) -> str:
    return re.sub(r'^\d+v?-', '', stem)


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<InterviewTimer' in text:
        return False
    slug = strip_prefix(path.stem)
    tag = f'<InterviewTimer problem-slug="{slug}" />'

    # Prefer: after <MarkSolved ... />
    m = re.search(r'<MarkSolved[^>]*/>', text)
    if m:
        text = text[:m.end()] + '\n\n' + tag + '\n' + text[m.end():]
    else:
        # Fallback: after <CompanyTags ... />
        m = re.search(r'<CompanyTags[^>]*/>', text)
        if m:
            text = text[:m.end()] + '\n\n' + tag + '\n' + text[m.end():]
        else:
            # Fallback: after H1
            m = re.search(r'^# .+$', text, re.MULTILINE)
            if not m:
                return False
            text = text[:m.end()] + '\n\n' + tag + '\n' + text[m.end():]
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
    print(f'Added InterviewTimer to {changed}/{total} problem pages.')


if __name__ == '__main__':
    main()
