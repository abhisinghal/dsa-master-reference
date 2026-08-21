#!/usr/bin/env python3
# Build combined markdown -> styled HTML for the DSA Master Reference.
import re, glob, os, html, sys
import markdown
from pygments import highlight
from pygments.lexers import JavaLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, "src")
THEME = (sys.argv[1].lower() if len(sys.argv) > 1 else "light")
DARK = THEME == "dark"
OUT_MD = r"C:\Users\absinghal\Downloads\Int\DSA_MASTER_REFERENCE.md"

# 1. Concatenate sources in sorted order
files = sorted(glob.glob(os.path.join(SRC, "*.md")))
parts = []
for f in files:
    with open(f, encoding="utf-8") as fh:
        parts.append(fh.read().rstrip() + "\n")
combined = "\n\n".join(parts)

with open(OUT_MD, "w", encoding="utf-8") as fh:
    fh.write(combined)

# 2. Protect fenced code blocks with placeholders
blocks = []
def stash(m):
    lang = (m.group(1) or "text").strip().lower()
    code = m.group(2)
    idx = len(blocks)
    blocks.append((lang, code))
    return f"\n\n@@CODEBLOCK_{idx}@@\n\n"

fence_re = re.compile(r"^```([A-Za-z0-9_+-]*)\n(.*?)\n^```", re.DOTALL | re.MULTILINE)
protected = fence_re.sub(stash, combined)

# 2b. Protect callouts: lines like "> [key] text" or "[key] text" -> standalone styled boxes
callouts = []
_inline = markdown.Markdown(extensions=["attr_list"])
def stash_callout(m):
    tag = m.group(1)
    text = m.group(2).strip()
    inner = _inline.reset().convert(text)
    idx = len(callouts)
    callouts.append(f'<blockquote class="{tag}">{inner}</blockquote>')
    return f"\n\n@@CALLOUT_{idx}@@\n\n"

callout_re = re.compile(r"^>?\s*\[(key|inv|trap|pat|note|def)\]\s+(.*)$", re.MULTILINE)
protected = callout_re.sub(stash_callout, protected)

# 3. Convert markdown to HTML
md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "attr_list", "sane_lists"])
body = md.convert(protected)

# 4. Render code blocks
fmt = HtmlFormatter(nowrap=True, noclasses=True, style="material")
def render_block(lang, code):
    if lang in ("java",):
        hl = highlight(code, JavaLexer(), fmt)
        return f'<pre class="code"><code>{hl}</code></pre>'
    if lang == "mermaid":
        return f'<div class="mermaid">{html.escape(code)}</div>'
    if lang == "svg":
        return f'<div class="svgfig">{code}</div>'      # raw inline SVG, not escaped
    if lang in ("python","py","js","javascript","cpp","c"):
        try:
            lx = get_lexer_by_name(lang)
            hl = highlight(code, lx, fmt)
            return f'<pre class="code"><code>{hl}</code></pre>'
        except Exception:
            pass
    return f'<pre class="diagram">{html.escape(code)}</pre>'

def sub_block(m):
    idx = int(m.group(1))
    lang, code = blocks[idx]
    return render_block(lang, code)

body = re.sub(r"<p>\s*@@CODEBLOCK_(\d+)@@\s*</p>", sub_block, body)
body = re.sub(r"@@CODEBLOCK_(\d+)@@", sub_block, body)

# 5. Substitute callout placeholders
def sub_callout(m):
    return callouts[int(m.group(1))]
body = re.sub(r"<p>\s*@@CALLOUT_(\d+)@@\s*</p>", sub_callout, body)
body = re.sub(r"@@CALLOUT_(\d+)@@", sub_callout, body)

# 5b. External links open in a new tab
body = re.sub(
    r'<a href="(https?://[^"]+)">',
    r'<a href="\1" target="_blank" rel="noopener">',
    body
)

# 6. Load CSS
with open(os.path.join(ROOT, "style.css"), encoding="utf-8") as fh:
    css = fh.read()
if DARK:
    with open(os.path.join(ROOT, "style-dark.css"), encoding="utf-8") as fh:
        css += "\n/* ===== DARK ===== */\n" + fh.read()

# 7. Assemble final HTML
html_doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>DSA Master Reference</title>
<style>{css}</style></head><body>
{body}
<script src="mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: false,
    theme: 'base',
    themeVariables: {{ primaryColor:'#eef5ff', primaryBorderColor:'#2563eb', primaryTextColor:'#0b1220', lineColor:'#5b6472', fontSize:'13px', fontFamily:'Segoe UI, Arial, sans-serif' }},
    flowchart: {{ curve: 'basis', htmlLabels: true, nodeSpacing: 28, rankSpacing: 34 }}
  }});
</script>
</body></html>"""

out_html = os.path.join(ROOT, "output_dark.html" if DARK else "output.html")
with open(out_html, "w", encoding="utf-8") as fh:
    fh.write(html_doc)

# Count code blocks + report
print(f"HTML written ({'dark' if DARK else 'light'}): {out_html} | code blocks: {len(blocks)} | bytes: {len(html_doc)}")
