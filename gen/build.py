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
OUT_MD = r"C:\Users\absinghal\Downloads\Int\DSA_MASTER_REFERENCE7.md"

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

# 3. Markdown -> HTML
md = markdown.Markdown(extensions=["tables", "attr_list", "sane_lists", "md_in_html", "toc"],
                       extension_configs={"toc": {"toc_depth": "1-2"}})
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
body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
# # INJECTED-SOLUTION-JUMPS
_LC_TO_ANCHOR = {
    'best-time-to-buy-and-sell-stock-with-cooldown': 'state-machine-dp-stock-trading-with-cooldown',
    'burst-balloons': 'interval-dp-matrix-chain-burst-balloons',
    'coin-change': 'coin-change-unbounded-min-count',
    'combination-sum': 'combination-sum-reuse-pruning',
    'construct-binary-tree-from-preorder-and-inorder-traversal': 'construct-tree-from-traversals',
    'count-of-smaller-numbers-after-self': 'merge-sort-count-of-smaller-numbers-after-self',
    'count-primes': 'sieve-of-eratosthenes-count-primes',
    'counting-bits': 'counting-bits-dp-on-bits',
    'course-schedule-ii': 'course-schedule-topological-sort',
    'diameter-of-binary-tree': 'maximum-depth-balanced-diameter-post-order-aggregation',
    'edit-distance': 'subsequence-dp-lis-lcs-edit-distance',
    'encode-and-decode-strings': 'encode-and-decode-strings-length-prefixing',
    'find-all-numbers-disappeared-in-an-array': 'find-all-missing-all-duplicate-numbers',
    'find-median-from-data-stream': 'find-median-from-data-stream-two-heaps',
    'first-missing-positive': 'first-missing-positive-hard',
    'gas-station': 'gas-station-prefix-balance-greedy',
    'greatest-common-divisor-of-strings': 'euclids-algorithm-gcd-lcm',
    'house-robber': '1d-dp-climbing-stairs-house-robber',
    'house-robber-iii': 'tree-dp-house-robber-iii',
    'implement-trie-prefix-tree': 'implement-trie',
    'insert-delete-getrandom-o1': 'insert-delete-getrandom-o1',
    'jump-game-ii': 'jump-game-ii-farthest-reach-greedy',
    'kth-largest-element-in-an-array': 'quickselect-kth-largest-element',
    'linked-list-random-node': 'reservoir-sampling-uniform-pick-from-a-stream',
    'longest-palindromic-substring': 'longest-palindromic-substring-expand-around-center',
    'lowest-common-ancestor-of-a-binary-tree': 'lowest-common-ancestor',
    'lru-cache': 'lru-cache-design',
    'maximum-subarray': 'maximum-subarray-kadane-the-running-optimum-dp',
    'maximum-xor-of-two-numbers-in-an-array': 'maximum-xor-of-two-numbers-binary-trie',
    'meeting-rooms-ii': 'meeting-rooms-ii-minimum-concurrent-intervals',
    'merge-intervals': 'merge-intervals',
    'merge-k-sorted-lists': 'merge-two-k-sorted-lists',
    'min-cost-to-connect-all-points': 'minimum-spanning-tree-kruskal-union-find',
    'min-stack': 'min-stack-o1-minimum',
    'missing-number': 'find-the-missing-number',
    'n-queens': 'n-queens-constraint-occupancy',
    'non-overlapping-intervals': 'non-overlapping-intervals-interval-scheduling',
    'number-of-provinces': 'union-find-disjoint-set-union',
    'palindrome-linked-list': 'reorder-palindrome-via-split-reverse-merge',
    'partition-equal-subset-sum': '01-knapsack-subset-sum-family',
    'partition-to-k-equal-sum-subsets': 'bitmask-dp-travelling-salesman-assignment',
    'permutations': 'permutations-the-used-template',
    'powx-n': 'fast-binary-exponentiation-powx-n',
    'reverse-linked-list': 'reverse-a-linked-list',
    'serialize-and-deserialize-binary-tree': 'serialize-deserialize-structure-encoding',
    'single-number': 'single-number-i-ii-iii-xor',
    'subsets': 'subsets-combinations-the-start-index-template',
    'task-scheduler': 'task-scheduler-activity-selection-sort-driven-greedy',
    'unique-paths': 'grid-dp-unique-paths-minimum-path-sum',
    'valid-parentheses': 'valid-parentheses',
    'validate-binary-search-tree': 'validate-bst-bst-operations',
    'word-search': 'word-search-grid-backtracking',
    'word-search-ii': 'word-search-ii-trie-backtracking'
}
def _inject_solution_jumps(html):
    import re
    # Only jump to anchors that actually exist in the HTML.
    existing_ids = set(re.findall(r'id="([^"]+)"', html))
    LC_RE = re.compile(r'(<a href=")(https://leetcode\.com/problems/([a-z0-9\-]+)/?)("[^>]*>)([^<]+)</a>')
    def repl(m):
        pre1, url, slug, pre2, name = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        anchor = _LC_TO_ANCHOR.get(slug, slug)
        if anchor not in existing_ids:
            return m.group(0)  # no in-PDF target — leave the link untouched
        jump = ' <a class="soljump" href="#' + anchor + '" title="Jump to solution in this PDF">↩️</a>'
        return pre1 + url + pre2 + name + '</a>' + jump
    return LC_RE.sub(repl, html)

body = _inject_solution_jumps(body)



# 5c. Difficulty badges (Easy / Medium / Hard authored as **bold**)
body = body.replace('<strong>Easy</strong>',   '<span class="diff diff-e">Easy</span>')
body = body.replace('<strong>Medium</strong>', '<span class="diff diff-m">Medium</span>')
body = body.replace('<strong>Hard</strong>',   '<span class="diff diff-h">Hard</span>')

# 6. Wrap with template
with open(os.path.join(ROOT, "style.css"), encoding="utf-8") as fh:
    css = fh.read()
if DARK:
    with open(os.path.join(ROOT, "style-dark.css"), encoding="utf-8") as fh:
        css += "\n/* ===== DARK ===== */\n" + fh.read()

mermaid_theme = "base"
mermaid_vars = ("{ primaryColor:'#eef5ff', primaryBorderColor:'#2563eb', primaryTextColor:'#0b1220', "
                "lineColor:'#5b6472', fontSize:'13px', fontFamily:'Segoe UI, Arial, sans-serif' }")

htmlout = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<style>{css}</style></head><body>
{body}
<script src="mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: false,
    theme: '{mermaid_theme}',
    themeVariables: {mermaid_vars},
    flowchart: {{ curve: 'basis', htmlLabels: true, nodeSpacing: 28, rankSpacing: 34 }}
  }});
</script>
</body></html>"""

out = os.path.join(ROOT, "output_dark.html" if DARK else "output.html")
with open(out, "w", encoding="utf-8") as fh:
    fh.write(htmlout)
print(f"HTML written ({THEME}):", out, "| code blocks:", len(blocks), "| bytes:", len(htmlout))
