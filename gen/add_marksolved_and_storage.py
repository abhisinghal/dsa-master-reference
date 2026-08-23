"""Embed MarkSolved on all problem pages. Add StorageManager to Roadmap."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'
PROBS = SRC / 'problems'


def extract_slug(name: str) -> str:
    return re.sub(r'^\d+v?-', '', name).replace('.md', '')


def add_mark_solved(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<MarkSolved' in text:
        return False
    slug = extract_slug(path.name)
    block = f'<MarkSolved problem-slug="{slug}" />\n\n'
    # Insert after the first `---` separator (right before Approach 1)
    idx = text.find('\n---\n')
    if idx < 0:
        return False
    # Insert after the ---
    insert_at = idx + len('\n---\n')
    text = text[:insert_at] + '\n' + block + text[insert_at:]
    path.write_text(text, encoding='utf-8')
    return True


def add_storage_manager(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<StorageManager' in text:
        return False
    # Insert at top after H1 subtitle
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith('# '):
            # After H1 + any subtitle paragraph
            insert_at = i + 1
            while insert_at < len(lines) and (lines[insert_at].strip() == '' or lines[insert_at].startswith('<p ')):
                insert_at += 1
            block = ['', '<StorageManager />', '']
            new = lines[:insert_at] + block + lines[insert_at:]
            path.write_text('\n'.join(new), encoding='utf-8')
            return True
    return False


def main():
    marked = 0
    for md in sorted(PROBS.iterdir()):
        if md.suffix != '.md' or md.name == '00-index.md':
            continue
        if add_mark_solved(md):
            marked += 1
    print(f'Added MarkSolved to {marked} pages.')

    roadmap = SRC / '03-roadmap.md'
    if roadmap.exists() and add_storage_manager(roadmap):
        print('Added StorageManager to roadmap.')


if __name__ == '__main__':
    main()
