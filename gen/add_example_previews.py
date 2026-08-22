"""
Auto-embed ExamplePreview components after **Example 1:** and **Example 2:** lines
in every gen/src markdown file. Parses common Example line formats:
  **Example 1:** `nums = [1,2,3], target = 4` → `[0,1]`
  **Example 1:** `"abcabcbb"` → `3` (the substring `"abc"`)
  **Example 1:** on `[[3,1],[2,4]]`, `sumRegion(0,0,1,1) = 10` (...)

Skips lines that can't be safely parsed. Preserves the original example line
and inserts the <ExamplePreview /> immediately after.
"""
import re
import os
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src'

EXAMPLE_RE = re.compile(
    r'^(\*\*Example \d+:\*\*.*?)$',
    re.MULTILINE
)

# Extract "input → output" backticks; support multiple formats
BACKTICK_RE = re.compile(r'`([^`]+)`')

def parse_array(s):
    """Parse simple 1D array like [1,2,3] or [a,b,c]. Return list of str, or None."""
    s = s.strip()
    m = re.match(r'^\[([^\[\]]*)\]$', s)
    if not m:
        return None
    inner = m.group(1).strip()
    if not inner:
        return []
    items = [x.strip() for x in inner.split(',')]
    if len(items) > 12:
        return None
    return items

def parse_string(s):
    """Parse "abc" → list of chars."""
    s = s.strip()
    m = re.match(r'^"([^"]*)"$', s)
    if not m:
        return None
    val = m.group(1)
    if len(val) > 15:
        return None
    return list(val)

def parse_scalar(s):
    """Parse a bare int/float/name. Return single-element list."""
    s = s.strip()
    if re.match(r'^-?\d+(\.\d+)?$', s):
        return [s]
    if re.match(r'^-?\d+(\.\d+)?%?$', s):
        return [s]
    return None

def parse_value(raw):
    """Try to parse a code span value to a list of display cells.
    Handles multi-argument inputs like 'nums = [1,2,3], target = 4'.
    """
    # If it looks like a multi-arg (has comma outside brackets AND has = somewhere)
    if '=' in raw and re.search(r'\][^\[]*,', raw):
        # split on commas not inside brackets
        parts = []
        depth = 0
        buf = ''
        for ch in raw:
            if ch in '[(':
                depth += 1
                buf += ch
            elif ch in '])':
                depth -= 1
                buf += ch
            elif ch == ',' and depth == 0:
                parts.append(buf.strip())
                buf = ''
            else:
                buf += ch
        if buf.strip():
            parts.append(buf.strip())
        # For each part, parse its value; concat labels
        merged = []
        for p in parts:
            v = parse_single_value(p)
            if v is None:
                return None
            merged.extend(v)
            if p != parts[-1]:
                merged.append('|')  # separator
        return merged if merged else None
    return parse_single_value(raw)

def parse_single_value(raw):
    """Parse a single argument (may still have LHS assignment)."""
    if '=' in raw:
        rhs = raw.split('=', 1)[1].strip()
    else:
        rhs = raw.strip()
    a = parse_array(rhs)
    if a is not None:
        return a
    s = parse_string(rhs)
    if s is not None:
        return s
    v = parse_scalar(rhs)
    if v is not None:
        return v
    if len(rhs) <= 12:
        return [rhs]
    return None

def build_preview(input_cells, output_cells):
    """Build the <ExamplePreview> tag string."""
    def js_arr(cells):
        parts = []
        for c in cells:
            parts.append(f"'{str(c).replace(chr(39), chr(92)+chr(39))}'")
        return '[' + ', '.join(parts) + ']'
    return (
        f"<ExamplePreview compact "
        f":input=\"{js_arr(input_cells)}\" "
        f":output=\"{js_arr(output_cells)}\" />"
    )

def process_line(line):
    """
    If line matches an Example, extract first two backtick groups as
    input and output, generate an ExamplePreview embed.
    Returns embed line or None to skip.
    """
    ticks = BACKTICK_RE.findall(line)
    if len(ticks) < 2:
        return None
    inp_raw, out_raw = ticks[0], ticks[1]
    inp = parse_value(inp_raw)
    out = parse_value(out_raw)
    if inp is None or out is None:
        return None
    if not inp or not out:
        return None
    return build_preview(inp, out)

def process_file(path):
    text = path.read_text(encoding='utf-8')
    if '<ExamplePreview' in text:
        # already processed
        return 0
    lines = text.splitlines(keepends=False)
    out_lines = []
    added = 0
    for i, ln in enumerate(lines):
        out_lines.append(ln)
        if re.match(r'^\*\*Example \d+:\*\*', ln):
            embed = process_line(ln)
            if embed:
                # insert with blank line separators
                out_lines.append('')
                out_lines.append(embed)
                added += 1
    if added:
        # preserve trailing newline behavior
        new_text = '\n'.join(out_lines) + ('\n' if text.endswith('\n') else '')
        path.write_text(new_text, encoding='utf-8')
    return added

def main():
    total = 0
    files_touched = 0
    for md in sorted(SRC.rglob('*.md')):
        try:
            added = process_file(md)
        except Exception as e:
            print(f'  ! {md.name}: {e}')
            continue
        if added:
            files_touched += 1
            total += added
            print(f'  + {md.relative_to(SRC)}: {added} previews')
    print(f'\nTotal: {total} previews across {files_touched} files')

if __name__ == '__main__':
    main()
