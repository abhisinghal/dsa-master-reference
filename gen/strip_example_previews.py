"""Strip existing ExamplePreview embeds before re-running the generator."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'

# Match the preview block: blank line + <ExamplePreview .../> line
STRIP_RE = re.compile(
    r'\n\n<ExamplePreview[^>]*/>\n',
    re.MULTILINE
)

def strip_file(path):
    text = path.read_text(encoding='utf-8')
    new_text, count = STRIP_RE.subn('\n', text)
    if count:
        path.write_text(new_text, encoding='utf-8')
    return count

def main():
    total = 0
    for md in sorted(SRC.rglob('*.md')):
        removed = strip_file(md)
        if removed:
            total += removed
            print(f'  - {md.relative_to(SRC)}: {removed} embeds removed')
    print(f'\nTotal removed: {total}')

if __name__ == '__main__':
    main()
