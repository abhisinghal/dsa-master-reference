"""Add generic CodeTrace embeds to pages missing them, using parsed Example values."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'


def parse_example_values(text):
    """Try to extract cell values from first Example line."""
    m = re.search(r'^\*\*Example\b.*?—.*?`([^`]+)`\s*→\s*`([^`]+)`', text, re.MULTILINE)
    if not m:
        return None
    inp_raw = m.group(1)
    # Multi-arg? Pick first array-looking arg
    arr_match = re.search(r'\[([^\[\]]*)\]', inp_raw)
    if arr_match:
        raw_items = [x.strip() for x in arr_match.group(1).split(',') if x.strip()]
        items = []
        for it in raw_items:
            it = it.strip('"').strip("'").strip()
            it = it.replace('"', '').replace("'", '')
            if it:
                items.append(it)
        if 1 <= len(items) <= 12:
            return items
    # Single quoted string
    str_match = re.search(r'"([^"]{1,12})"', inp_raw)
    if str_match:
        return list(str_match.group(1))
    return None


def build_code_trace(values, approach_label):
    """Build a generic 3-frame CodeTrace based on values."""
    def js(items):
        return '[' + ', '.join(f"'{v}'" for v in items) + ']'
    n = len(values)
    mid = max(0, n // 2)
    last = max(0, n - 1)
    safe_label = approach_label.replace("'", " ").replace('"', ' ').replace('—', '-')
    if len(safe_label) > 60:
        safe_label = safe_label[:57] + '...'
    return f"""
<CodeTrace
  title="{safe_label}"
  :values="{js(values)}"
  :windowKeys="['i']"
  :cellWidth="34"
  :steps='[
    {{ pointers: {{ i: 0 }}, vars: {{ phase: "start" }}, note: "Initialize scan." }},
    {{ pointers: {{ i: {mid} }}, vars: {{ phase: "midway" }}, note: "Midway through processing." }},
    {{ pointers: {{ i: {last} }}, vars: {{ phase: "done" }}, note: "Return the answer." }}
  ]'
/>
"""


def find_first_approach_and_code(text):
    """Find the first Java code block within a ## Approach section. Return (approach_label, insert_pos)."""
    # Find first ## Approach header
    approach_match = re.search(r'^(## Approach [^\n]+|## [^\n]*Approach[^\n]*)$', text, re.MULTILINE)
    if not approach_match:
        return None, None
    header = approach_match.group(1)
    header_end = approach_match.end()
    # Find first ```java...``` after that
    code_start = text.find('```java', header_end)
    if code_start < 0:
        return None, None
    code_end = text.find('```', code_start + 7)
    if code_end < 0:
        return None, None
    code_end_line_end = text.find('\n', code_end)
    if code_end_line_end < 0:
        code_end_line_end = code_end + 3
    label = header.strip('#').strip()
    label = re.sub(r'^Approach\s*\d*\s*[—:.\-]\s*', '', label).strip()
    return label, code_end_line_end + 1


def process_file(path):
    text = path.read_text(encoding='utf-8')
    if '<CodeTrace' in text:
        return False
    values = parse_example_values(text)
    if not values:
        return False
    label, insert_pos = find_first_approach_and_code(text)
    if label is None:
        return False
    trace = build_code_trace(values, label)
    new_text = text[:insert_pos] + trace + text[insert_pos:]
    path.write_text(new_text, encoding='utf-8')
    return True


def main():
    changed = 0
    skipped = 0
    for md in sorted(SRC.iterdir()):
        if md.suffix != '.md' or md.name == '00-index.md':
            continue
        try:
            if process_file(md):
                changed += 1
                print(f'  + {md.name}')
            else:
                skipped += 1
        except Exception as e:
            print(f'  ! {md.name}: {e}')
    print(f'\nAdded CodeTrace to {changed} pages; skipped {skipped}')


if __name__ == '__main__':
    main()
