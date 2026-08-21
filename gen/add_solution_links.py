"""Add stable in-PDF anchors to every appendix table row (id = LC slug),
and post-process build.py's HTML to append a compact `↩ solution` jump-link
after every LeetCode link that has a same-PDF target.

We add anchors two ways:
1. Every appendix table row keyed by LC slug gets an inline `<a id="slug"></a>` in the Problem cell.
2. Every canonical problem heading in Part III/IV gets a stable id based on its LC slug
   (via `{: #slug }` attr_list syntax) so LC-to-canonical jumps work too.
"""
import re, os

ROOT = os.path.join(os.path.dirname(__file__), "src")

def add_anchors_to_appendix():
    """In 97-practice-solutions.md, prepend `<a id="slug"></a>` inside every
    `| [Name](https://leetcode.com/problems/slug/) …` row.
    Also, the walkthrough headings already have `{: #slug }` attributes.
    """
    path = os.path.join(ROOT, "97-practice-solutions.md")
    txt = open(path, encoding="utf-8").read()
    # Row pattern: | [Name](https://leetcode.com/problems/slug/) [maybe · walkthrough] | Approach |
    def rewrite(m):
        prefix, name, slug, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
        # If already has an anchor, skip
        if f'id="{slug}"' in prefix + name + suffix:
            return m.group(0)
        # Prepend inline anchor
        return f'| <a id="{slug}"></a>[{name}](https://leetcode.com/problems/{slug}/){suffix}'
    new = re.sub(
        r'^\| (\s*)\[([^\]]+)\]\(https://leetcode\.com/problems/([a-z0-9\-]+)/\)([^|\n]*)',
        rewrite, txt, flags=re.MULTILINE)
    if new != txt:
        open(path, "w", encoding="utf-8").write(new)
        return "appendix anchors added"
    return "appendix anchors: already present"

def build_slug_map():
    """Return dict: LC slug -> in-PDF anchor for solution jump.
    Slugify like python-markdown's toc: lowercase, strip HTML entities like `&amp;`, keep only word chars + hyphens.
    """
    slug_map = {}
    for f in sorted(os.listdir(ROOT)):
        if not re.match(r'^(3\d|4\d|5\d|6[0-5])-', f): continue
        path = os.path.join(ROOT, f)
        lines = open(path, encoding="utf-8").read().split('\n')
        i = 0
        while i < len(lines):
            m = re.match(r'^## (.+?)\s*$', lines[i])
            if m:
                title = m.group(1).strip()
                # Match python-markdown's slug: strip &amp; entities and other HTML entities
                s = title.replace('&amp;', '').replace('&', '')
                s = re.sub(r'[^\w\s-]', '', s.lower())
                s = re.sub(r'[\s_]+', '-', s).strip('-')
                # Collapse consecutive hyphens
                s = re.sub(r'-+', '-', s)
                for j in range(i, min(i+5, len(lines))):
                    for mm in re.finditer(r'https://leetcode\.com/problems/([a-z0-9\-]+)', lines[j]):
                        lc = mm.group(1)
                        if lc not in slug_map:
                            slug_map[lc] = s
                    if re.match(r'^#{1,3}\s', lines[j]) and j > i:
                        break
            i += 1
    return slug_map

def update_build_py_postprocess(slug_map):
    """Inject a post-processor into build.py that, right after markdown->HTML, wraps every
    external LC link with an in-PDF ↩ solution jump when the LC slug is in slug_map.
    """
    build_py = os.path.join(os.path.dirname(__file__), "build.py")
    src = open(build_py, encoding="utf-8").read()
    marker = "# INJECTED-SOLUTION-JUMPS"
    lit = "{\n" + ",\n".join(f'    {slug!r}: {anchor!r}' for slug, anchor in sorted(slug_map.items())) + "\n}"
    # Use plain string concatenation, not f-strings, to avoid brace collisions.
    inject_template = '''
# %MARKER%
_LC_TO_ANCHOR = %LITERAL%
def _inject_solution_jumps(html):
    import re
    # Only jump to anchors that actually exist in the HTML.
    existing_ids = set(re.findall(r'id="([^"]+)"', html))
    LC_RE = re.compile(r'(<a href=")(https://leetcode\\.com/problems/([a-z0-9\\-]+)/?)("[^>]*>)([^<]+)</a>')
    def repl(m):
        pre1, url, slug, pre2, name = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        anchor = _LC_TO_ANCHOR.get(slug, slug)
        if anchor not in existing_ids:
            return m.group(0)  # no in-PDF target — leave the link untouched
        jump = ' <a class="soljump" href="#' + anchor + '" title="Jump to solution in this PDF">\u21a9\ufe0f</a>'
        return pre1 + url + pre2 + name + '</a>' + jump
    return LC_RE.sub(repl, html)
'''.replace("%MARKER%", marker).replace("%LITERAL%", lit)
    call = "\nbody = _inject_solution_jumps(body)\n"
    if marker not in src:
        target = 'body = re.sub(r\'<a href="(https?://[^"]+)"\', r\'<a href="\\1" target="_blank" rel="noopener"\', body)'
        if target in src:
            src = src.replace(target, target + inject_template + call)
        else:
            print("!! could not find external-link rewrite anchor in build.py")
            return "build.py: injection point not found"
    else:
        src = re.sub(r'_LC_TO_ANCHOR = \{[\s\S]*?\n\}', f'_LC_TO_ANCHOR = {lit}', src, count=1)
    open(build_py, "w", encoding="utf-8").write(src)
    return f"build.py updated with {len(slug_map)} canonical LC->anchor mappings"

def add_style_rule():
    """Add a `.soljump` style rule to style.css + style-dark.css."""
    for fname in ("style.css", "style-dark.css"):
        p = os.path.join(os.path.dirname(__file__), fname)
        css = open(p, encoding="utf-8").read()
        if ".soljump" in css: continue
        rule = "\n/* In-PDF solution jump link — appended after external LC links */\n" \
               ".soljump { font-size: 0.72em; text-decoration: none; padding: 0 2px; " \
               "border-radius: 3px; background: #eef5ff; color: #2563eb; " \
               "margin-left: 2px; vertical-align: super; }\n" \
               ".soljump:hover { background: #dbeafe; }\n"
        if fname == "style-dark.css":
            rule = "\n.soljump { background: rgba(59,130,246,.18); color: #7ab7f5; }\n"
        open(p, "w", encoding="utf-8").write(css + rule)
    return "styles added"

if __name__ == "__main__":
    print(add_anchors_to_appendix())
    slug_map = build_slug_map()
    print(f"canonical LC->anchor mappings: {len(slug_map)}")
    print(update_build_py_postprocess(slug_map))
    print(add_style_rule())
