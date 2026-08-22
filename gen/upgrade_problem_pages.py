"""
Upgrade every variation page under gen/src/problems/ to the flagship format:

Flagship structure (from 01-sliding-window-longest-substring.md, 05-hashing-two-sum.md):

  # Pattern — Title
  *[↗ LeetCode: ...](...)* · <span class="diff diff-X">Difficulty</span> · [pattern chapter →](/patterns/xxx)

  <problem paragraph>

  **Example 1** — ...
  **Example 2** — ...
  **Constraints** — ...

  ---

  ## Approach 1 — Brute force ...
  **Intuition.** ...
  ```java ... ```
  <CodeTrace ... />
  **Complexity** — ...

  ---

  ## Approach 2 — ...
  ...

  ## Complexity summary
  | Approach | Time | Space | Interview grade |
  ...

  ## When to use which
  - ...

  ## Related problems
  - ...

This script parses each variation and rewrites it in that shape,
preserving all authored content and adding the missing structural
sections. CodeTrace embeds are inserted after every approach's code
block using a minimal generic 3-frame scaffold based on the example.
"""
import re
import os
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'

# Files to skip (flagship 21 and index)
SKIP = {'00-index.md'}

FLAGSHIP_RE = re.compile(r'^\d\d-')  # NN- (flagship files); we upgrade variations only, but re-run is idempotent


def parse_header(text):
    """Extract H1 title, LC line, problem paragraph up to first ## Approach."""
    lines = text.splitlines()
    out = {'lines': lines, 'h1_i': None, 'lc_i': None, 'problem_start': None, 'first_approach_i': None}
    for i, ln in enumerate(lines):
        if out['h1_i'] is None and ln.startswith('# '):
            out['h1_i'] = i
        elif out['lc_i'] is None and ln.startswith('*[↗ LeetCode:'):
            out['lc_i'] = i
        elif ln.startswith('## Approach') and out['first_approach_i'] is None:
            out['first_approach_i'] = i
            break
    return out


def find_related_section(lines):
    """Find index of '## Related problems' (return -1 if absent)."""
    for i, ln in enumerate(lines):
        if ln.strip().startswith('## Related'):
            return i
    return -1


def extract_approaches(lines, first_approach_i, related_i):
    """Split lines[first_approach_i:related_i] into approach chunks by '## Approach'."""
    end = related_i if related_i >= 0 else len(lines)
    approach_section = lines[first_approach_i:end]
    approaches = []
    current = None
    for ln in approach_section:
        if ln.startswith('## Approach') or ln.startswith('## Optimized'):
            if current is not None:
                approaches.append(current)
            # normalize "## Optimized ..." into "## Approach N ..."
            current = {'header': ln, 'body': []}
        elif current is not None:
            current['body'].append(ln)
    if current is not None:
        approaches.append(current)
    return approaches


def _find_o_expr(text):
    """Find all balanced O(...) expressions in text, handling one level of nested parens.
    Returns list of inner expressions."""
    results = []
    i = 0
    while i < len(text):
        m = re.search(r'O\(', text[i:])
        if not m:
            break
        start = i + m.end()
        depth = 1
        j = start
        while j < len(text) and depth > 0:
            if text[j] == '(':
                depth += 1
            elif text[j] == ')':
                depth -= 1
            j += 1
        if depth == 0:
            results.append(text[start:j-1])
        i = j
    return results


def parse_complexity(body):
    """Extract time and space from a body. Try explicit **Complexity** line first,
    then fall back to any O(...) mentions in the body prose. Handles nested parens."""
    for ln in body:
        if '**Complexity**' in ln:
            # Try to identify Time and Space sections
            time_pos = ln.find('Time')
            space_pos = ln.find('Space')
            t, s = '—', '—'
            if time_pos >= 0:
                seg_end = space_pos if space_pos > time_pos else len(ln)
                exprs = _find_o_expr(ln[time_pos:seg_end])
                if exprs:
                    t = f'O({exprs[0]})'
            if space_pos >= 0:
                exprs = _find_o_expr(ln[space_pos:])
                if exprs:
                    s = f'O({exprs[0]})'
            if t != '—' or s != '—':
                return t, s
    # Fallback: search whole body for O(...) expressions
    body_text = ' '.join(body)
    exprs = _find_o_expr(body_text)
    if not exprs:
        return '—', '—'
    t = f'O({exprs[0]})'
    s = f'O({exprs[1]})' if len(exprs) > 1 else '—'
    return t, s


def extract_example_values(problem_lines):
    """Try to parse the first Example line into a JS array of cell values.
    Return `values` list or None."""
    for ln in problem_lines:
        m = re.match(r'^\*\*Example\b.*?—.*?`([^`]+)`\s*→\s*`([^`]+)`', ln)
        if m:
            inp_raw = m.group(1)
            # If contains '=', pick RHS of first array-looking arg
            arr_match = re.search(r'\[([^\[\]]*)\]', inp_raw)
            if arr_match:
                raw_items = [x.strip() for x in arr_match.group(1).split(',') if x.strip()]
                # Strip surrounding quotes and any characters that break HTML attr / JS single-quoted string
                items = []
                for it in raw_items:
                    it = it.strip('"').strip("'")
                    it = it.replace('"', '').replace("'", '')
                    if it:
                        items.append(it)
                if 1 <= len(items) <= 12:
                    return items
            # String literal
            str_match = re.match(r'^"([^"]{1,12})"$', inp_raw.strip())
            if str_match:
                return list(str_match.group(1))
    return None


def approach_short_label(header):
    """Strip '## Approach N — ' or '## Optimized — ' prefix; normalize; return short label."""
    # Strip any '## ' prefix
    h = header.lstrip('#').strip()
    # Strip 'Approach N — ' or 'Approach N. ' or 'Optimized — '
    h = re.sub(r'^Approach\s*\d*\s*[—:.]\s*', '', h)
    h = re.sub(r'^Optimized\s*[—:.]\s*', '', h)
    # Collapse double em-dashes
    h = re.sub(r'\s*—\s*—\s*', ' — ', h)
    return h.strip()


def build_codetrace(values, approach_label, is_first, approach_idx):
    """Build a minimal CodeTrace embed for an approach."""
    if not values:
        return ''
    # Represent values as JS-array string with single quotes
    def js_array(items):
        return '[' + ', '.join(f"'{str(v)}'" for v in items) + ']'
    n = len(values)
    mid = max(0, n // 2 - 1)
    last = max(0, n - 1)
    # generic frame set — use double quotes for string values to avoid clashing with outer single-quoted :steps
    if is_first:
        steps = f"""[
    {{ pointers: {{ i: 0 }}, vars: {{ phase: "start" }}, note: "Initialize; scan begins." }},
    {{ pointers: {{ i: {mid} }}, vars: {{ phase: "midway" }}, note: "Midway through the scan." }},
    {{ pointers: {{ i: {last} }}, vars: {{ phase: "done" }}, note: "All positions considered — return the answer." }}
  ]"""
        window_keys = "['i']"
    else:
        steps = f"""[
    {{ pointers: {{ l: 0, r: 0 }}, vars: {{ phase: "start" }}, note: "Both pointers at the start." }},
    {{ pointers: {{ l: 0, r: {mid} }}, vars: {{ phase: "extend" }}, note: "Right pointer extends; maintain the invariant." }},
    {{ pointers: {{ l: {mid}, r: {last} }}, vars: {{ phase: "finalize" }}, note: "Window converged; produce the answer." }}
  ]"""
        window_keys = "['l','r']"

    # Sanitize title — no double quotes; ensure single-line
    title = re.sub(r'\s+', ' ', approach_label).replace('"', "'")
    return f"""
<CodeTrace
  title="{title}"
  :values="{js_array(values)}"
  :windowKeys="{window_keys}"
  :cellWidth="34"
  :steps='{steps}'
/>
"""


def rebuild_page(text):
    """Return upgraded text (or original if not a variation-style page)."""
    if '## Complexity summary' in text:
        # already upgraded
        return text
    hdr = parse_header(text)
    lines = hdr['lines']
    if hdr['h1_i'] is None or hdr['lc_i'] is None or hdr['first_approach_i'] is None:
        return text  # can't safely upgrade
    # Preamble = h1 + LC line + blank + problem paragraph up to first_approach
    preamble = lines[hdr['h1_i']:hdr['first_approach_i']]

    related_i = find_related_section(lines)
    approaches = extract_approaches(lines, hdr['first_approach_i'], related_i)
    if not approaches:
        return text
    related_block = []
    if related_i >= 0:
        related_block = lines[related_i:]

    # Parse example values from preamble
    values = extract_example_values(preamble)

    # Rebuild
    out = []
    # Preamble (strip trailing blanks)
    while preamble and preamble[-1].strip() == '':
        preamble.pop()
    out.extend(preamble)
    out.append('')
    out.append('---')
    out.append('')

    # Approaches with separators + CodeTrace
    complexity_rows = []
    for idx, ap in enumerate(approaches):
        label = approach_short_label(ap['header'])
        # Rewrite header to consistent "## Approach N — Title" if not already
        header_m = re.match(r'^## Approach\s*(\d+)?\s*(?:—\s*(.*))?$', ap['header'])
        if header_m and header_m.group(1):
            new_header = ap['header']
        else:
            # normalize
            new_header = f'## Approach {idx+1} — {label}'
        out.append(new_header)
        # body: strip surrounding blank lines
        body = list(ap['body'])
        while body and body[0].strip() == '':
            body.pop(0)
        while body and body[-1].strip() == '':
            body.pop()
        # If body has a Java code block, insert CodeTrace right after it
        # Find end of first ```java...``` block
        java_end = -1
        in_java = False
        for i, bl in enumerate(body):
            if bl.strip().startswith('```java'):
                in_java = True
            elif in_java and bl.strip() == '```':
                java_end = i
                break
        new_body = list(body)
        if java_end >= 0 and values:
            ct = build_codetrace(values, label, is_first=(idx == 0), approach_idx=idx).rstrip()
            insert = ['', ct, '']
            new_body = new_body[:java_end+1] + insert + new_body[java_end+1:]
        out.extend(new_body)
        # Collect complexity
        t, s = parse_complexity(body)
        n_approaches = len(approaches)
        if n_approaches == 1:
            grade = 'primary'
        elif idx == 0:
            grade = 'baseline'
        elif idx == n_approaches - 1:
            grade = 'optimum'
        else:
            grade = 'improved'
        complexity_rows.append((label, t, s, grade))
        out.append('')
        out.append('---')
        out.append('')

    # Complexity summary table
    out.append('## Complexity summary')
    out.append('')
    out.append('| Approach | Time | Space | Interview grade |')
    out.append('|---|---|---|---|')
    for label, t, s, grade in complexity_rows:
        # shorten labels
        short = label if len(label) < 45 else label[:42] + '…'
        out.append(f'| {short} | {t} | {s} | {grade} |')
    out.append('')

    # When to use which
    out.append('## When to use which')
    out.append('')
    n = len(complexity_rows)
    for idx, (label, t, s, grade) in enumerate(complexity_rows):
        if n == 1:
            out.append(f'- **Ship this** → {label} ({t}, {s}). The pattern\'s standard solution.')
        elif idx == 0:
            out.append(f'- **State it for signal** → {label} ({t}). Correct baseline; call it out then move on.')
        elif idx == n - 1:
            out.append(f'- **Ship this** → {label} ({t}, {s}). Expected optimum in interview.')
        else:
            out.append(f'- **Intermediate refinement** → {label} ({t}).')
    out.append('')

    # Related problems block (preserved)
    if related_block:
        # ensure blank line separation
        out.extend(related_block)
    else:
        out.append('## Related problems')
        out.append('')
        out.append('- See the [pattern chapter](/patterns/) for the family tree.')

    # Trim trailing blank lines and add single trailing newline
    while out and out[-1].strip() == '':
        out.pop()
    return '\n'.join(out) + '\n'


def process_file(path):
    text = path.read_text(encoding='utf-8')
    new_text = rebuild_page(text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        return True
    return False


def main():
    changed = 0
    skipped = 0
    for md in sorted(SRC.iterdir()):
        if md.suffix != '.md' or md.name in SKIP:
            continue
        # Only upgrade variations (NNv-) — flagships (NN-) already in target format
        if not re.match(r'^\d+v-', md.name):
            skipped += 1
            continue
        try:
            if process_file(md):
                changed += 1
        except Exception as e:
            print(f'  ! {md.name}: {e}')
    print(f'Upgraded {changed} variation pages; skipped {skipped} flagships/other.')


if __name__ == '__main__':
    main()
