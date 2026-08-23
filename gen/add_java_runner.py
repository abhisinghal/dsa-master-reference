"""Add JavaRunner (CheerpJ WASM) to every problem page.
Placement: after Approach sections, before "## Complexity summary".
Starter template is a generic Main class with Scanner input.
"""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'


def extract_slug(filename: str) -> str:
    """Remove NN- or NNv- prefix and .md suffix."""
    name = filename.replace('.md', '')
    return re.sub(r'^\d+v?-', '', name)


def build_runner_block(slug: str) -> str:
    """Build a minimal JavaRunner tag."""
    return f'''
## Try it yourself

<JavaRunner problem-slug="{slug}" />

'''


def process(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<JavaRunner' in text:
        return False
    slug = extract_slug(path.name)
    block = build_runner_block(slug)
    # Insert BEFORE "## Complexity summary" if present, else before "## Related problems"
    for anchor in ['## Complexity summary', '## Related problems', '## When to use']:
        idx = text.find(anchor)
        if idx >= 0:
            new_text = text[:idx].rstrip() + '\n\n' + block.strip() + '\n\n' + text[idx:]
            path.write_text(new_text, encoding='utf-8')
            return True
    # Fallback: append at end
    path.write_text(text.rstrip() + '\n\n' + block.strip() + '\n', encoding='utf-8')
    return True


def main():
    changed = 0
    for md in sorted(SRC.iterdir()):
        if md.suffix != '.md' or md.name == '00-index.md':
            continue
        if process(md):
            changed += 1
    print(f'Added JavaRunner to {changed} pages.')


if __name__ == '__main__':
    main()
