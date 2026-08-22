#!/usr/bin/env python3
# Migrate gen/src/*.md into web/docs/ VitePress structure.
# Transforms:
#   > [key] **Title** — body            ->  <Callout kind="key" title="Title">body</Callout>
#   > [tag] body                        ->  <Callout kind="tag">body</Callout>
# Preserves fenced code blocks (no transformation inside them).
import os, re, shutil, glob, unicodedata

# Compute paths relative to this script
_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(_HERE, "..", "gen", "src"))
DST = os.path.abspath(os.path.join(_HERE, "docs"))

# File slug mapping (source -> destination path relative to DST)
MAPPING = {
    "00-front.md":              "foundations/how-to-use.md",
    "01-playbook.md":           "foundations/playbook.md",
    "02-glossary.md":           "foundations/glossary.md",
    "03-roadmap.md":            "foundations/roadmap.md",
    "04-part1.md":              None,  # section divider, skip
    "06-java-ds.md":            "foundations/java-primer.md",
    "07-java-gotchas.md":       "foundations/java-gotchas.md",
    "09-vs-competitors.md":     "foundations/vs-competitors.md",
    "10-complexity.md":         "foundations/complexity.md",
    "11-debugging.md":          "foundations/debugging.md",
    "20-patterns.md":           "patterns/index.md",
    "21-sliding-window.md":     "patterns/sliding-window.md",
    "22-two-pointers.md":       "patterns/two-pointers.md",
    "23-fast-slow.md":          "patterns/fast-slow.md",
    "24-prefix-sum.md":         "patterns/prefix-sum.md",
    "25-hashing.md":            "patterns/hashing.md",
    "26-monotonic-stack.md":    "patterns/monotonic-stack.md",
    "27-binary-search.md":      "patterns/binary-search.md",
    "28-bs-on-answer.md":       "patterns/bs-on-answer.md",
    "29-top-k-heap.md":         "patterns/top-k-heap.md",
    "30-k-way-merge.md":        "patterns/k-way-merge.md",
    "31-merge-intervals.md":    "patterns/merge-intervals.md",
    "32-sweep-line.md":         "patterns/sweep-line.md",
    "33-topological-sort.md":   "patterns/topological-sort.md",
    "34-union-find.md":         "patterns/union-find.md",
    "35-greedy.md":             "patterns/greedy.md",
    "36-backtracking.md":       "patterns/backtracking.md",
    "37-divide-conquer.md":     "patterns/divide-conquer.md",
    "38-dp.md":                 "patterns/dp.md",
    "39-trie-pattern.md":       "patterns/trie-pattern.md",
    "40-bit-manip.md":          "patterns/bit-manip.md",
    "41-quickselect.md":        "patterns/quickselect.md",
    "42-math.md":               "patterns/math.md",
    "44-design.md":             "patterns/design.md",
    "45-system-design.md":      "system-design/index.md",
    "50-arrays.md":             "data-structures/arrays.md",
    "52-strings.md":            "data-structures/strings.md",
    "56-linked-lists.md":       "data-structures/linked-lists.md",
    "58-stacks-queues.md":      "data-structures/stacks-queues.md",
    "60-trees.md":              "data-structures/trees.md",
    "62-heaps.md":              "data-structures/heaps.md",
    "64-trie.md":               "data-structures/trie.md",
    "66-graphs.md":             "data-structures/graphs.md",
    "68-segment-fenwick.md":    "data-structures/segment-fenwick.md",
    "90-cheatsheets.md":        "appendix/cheatsheets.md",
    "93-changelog.md":          "appendix/changelog.md",
    "95-self-check.md":         "appendix/self-check.md",
    "96-problem-index.md":      "appendix/problem-index.md",
    "97-practice-solutions.md": "appendix/practice-solutions.md",
    "98-mock-transcripts.md":   "appendix/mock-transcripts.md",
    "99-traps-catalog.md":      "appendix/traps-catalog.md",
}

# In-book anchor rewrites — old fragment -> new URL
# These need to be updated because chapters now live at different URL paths
def slugify_anchor(value: str) -> str:
    """Match the VitePress heading slug policy used by docs/.vitepress/config.mts."""
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[—–→·]", "-", value)
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return re.sub(r"^(\d)", r"_\1", value)

ANCHOR_MAP = {
    "sliding-window":               "/patterns/sliding-window",
    "two-pointers":                 "/patterns/two-pointers",
    "fast-slow-pointers-floyd":     "/patterns/fast-slow",
    "prefix-sum-difference-arrays": "/patterns/prefix-sum",
    "hashing":                      "/patterns/hashing",
    "monotonic-stack":              "/patterns/monotonic-stack",
    "binary-search-search-on-answer": "/patterns/binary-search",
    "binary-search-on-the-answer":  "/patterns/bs-on-answer",
    "top-k-heap":                   "/patterns/top-k-heap",
    "k-way-merge":                  "/patterns/k-way-merge",
    "merge-intervals":              "/patterns/merge-intervals",
    "sweep-line":                   "/patterns/sweep-line",
    "topological-sort":             "/patterns/topological-sort",
    "union-find-disjoint-set-union": "/patterns/union-find",
    "greedy":                       "/patterns/greedy",
    "recursion-backtracking":       "/patterns/backtracking",
    "divide-conquer":               "/patterns/divide-conquer",
    "dynamic-programming":          "/patterns/dp",
    "trie-pattern":                 "/patterns/trie-pattern",
    "bit-manipulation":             "/patterns/bit-manip",
    "quickselect":                  "/patterns/quickselect",
    "math-number-theory":           "/patterns/math",
    "design-randomized":            "/patterns/design",
    "arrays":                       "/data-structures/arrays",
    "strings":                      "/data-structures/strings",
    "linked-lists":                 "/data-structures/linked-lists",
    "stacks-queues":                "/data-structures/stacks-queues",
    "trees":                        "/data-structures/trees",
    "heaps-priority-queues":        "/data-structures/heaps",
    "tries-prefix-trees":           "/data-structures/trie",
    "graphs":                       "/data-structures/graphs",
    "segment-tree-fenwick-tree":    "/data-structures/segment-fenwick",
    "the-interview-playbook":       "/foundations/playbook",
    "study-plans-revision-cadence": "/foundations/playbook#study-plans",
    "zero-to-hero-roadmap":         "/foundations/roadmap",
    "glossary-words-we-use-everywhere": "/foundations/glossary",
    "java-data-structures-a-visual-toolkit": "/foundations/java-primer",
    "java-dsa-gotchas":             "/foundations/java-gotchas",
    "complexity-amortization-the-cost-model": "/foundations/complexity",
    "debugging-dsa-code":           "/foundations/debugging",
    "the-which-pattern-decision-tree": "/patterns/",
    "master-cheat-sheets-templates": "/appendix/cheatsheets",
    "appendix-self-check-mastery-drills": "/appendix/self-check",
    "master-problem-index-tracker":   "/appendix/problem-index",
    "practice-solutions-appendix":    "/appendix/practice-solutions",
    "mock-interview-transcripts":     "/appendix/mock-transcripts",
    "traps-catalog":                  "/appendix/traps-catalog",
}

def transform_callouts(text: str) -> str:
    """Transform > [tag] **Title** — body ... blockquote lines into <Callout>."""
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^>\s*\[(key|inv|trap|pat|note|def)\]\s+(.*)$", line)
        if m:
            tag = m.group(1)
            first_body = m.group(2)
            # Gather subsequent > lines
            body_lines = [first_body]
            j = i + 1
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                extra = re.sub(r"^>\s?", "", lines[j])
                body_lines.append(extra)
                j += 1
            # Parse first_body: does it start with **Title** — body?
            title_match = re.match(r"\*\*([^*]+)\*\*\s*[—–-]\s*(.*)$", first_body)
            if title_match:
                title = title_match.group(1).strip()
                body_lines[0] = title_match.group(2)
            else:
                # try to grab just the leading **Title**
                bare_title = re.match(r"\*\*([^*]+)\*\*\s*(.*)$", first_body)
                if bare_title:
                    title = bare_title.group(1).strip()
                    body_lines[0] = bare_title.group(2)
                else:
                    title = None
            body = "\n".join(body_lines).strip()

            # Escape bare < and > OUTSIDE of inline code and HTML tags.
            # Vue's SFC parser trips on `high.size() > low.size()` in prose.
            body = escape_lt_gt_in_prose(body)

            if title:
                title_esc = title.replace('"', '&quot;')
                # Also escape < > in title (rare, but safe)
                title_esc = title_esc.replace('<', '&lt;').replace('>', '&gt;')
                out.append(f'<Callout kind="{tag}" title="{title_esc}">\n\n{body}\n\n</Callout>')
            else:
                out.append(f'<Callout kind="{tag}">\n\n{body}\n\n</Callout>')
            i = j
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def escape_lt_gt_in_prose(body: str) -> str:
    """Replace bare < and > characters with HTML entities in prose only.
    Skips: inline code (backticks) and known-good HTML/Vue tags.
    """
    # First stash inline-code spans (backtick pairs) into placeholders
    codes = []
    def stash_code(m):
        codes.append(m.group(0))
        return f"\x00CODE{len(codes)-1}\x01"
    body = re.sub(r"`[^`\n]*`", stash_code, body)

    # Now protect known-good HTML/Vue tags (which may span backticks; but we already stashed those)
    # Attribute matcher allows > inside single- or double-quoted values, so multi-line Vue
    # components with rich :prop='[...>...]' payloads survive the prose-escape pass intact.
    ATTR = r"(?:\s+(?:'[^']*'|\"[^\"]*\"|[^\"'/>\s])+)*"
    KNOWN_HTML = re.compile(
        r"</?(a|b|i|u|em|strong|span|div|p|br|hr|img|code|pre|kbd|sub|sup|"
        r"h[1-6]|ul|ol|li|table|thead|tbody|tr|th|td|blockquote|small|"
        r"details|summary|figure|figcaption|dl|dt|dd|"
        r"Callout|CodeTabs|ProgressCheck|JavaRunner|Breadcrumbs|ReadingTime|"
        r"RecentUpdates|Quiz|StepStrip|TwoSumStepStrip|CodeTrace|Icon|"
        r"SlidingWindowAnim|MonoStackAnim|UnionFindAnim|SweepLineAnim|"
        r"DivideConquerAnim|QuickselectAnim|BacktrackingAnim|"
        r"TwoPointersAnim|FastSlowAnim|BinarySearchAnim|HeapAnim|"
        r"BFSGridAnim|DFSGridAnim|DpFillAnim|TrieWalkAnim|"
        r"ClientOnly|slot|script|style|template)"
        rf"{ATTR}\s*/?>",
        re.IGNORECASE | re.DOTALL
    )
    tag_slots = []
    def stash_tag(m):
        tag_slots.append(m.group(0))
        return f"\x00TAG{len(tag_slots)-1}\x01"
    body = KNOWN_HTML.sub(stash_tag, body)

    # Now escape all remaining < and >
    body = body.replace("<", "&lt;").replace(">", "&gt;")

    # Restore protected tags
    body = re.sub(r"\x00TAG(\d+)\x01", lambda m: tag_slots[int(m.group(1))], body)
    # Restore inline code
    body = re.sub(r"\x00CODE(\d+)\x01", lambda m: codes[int(m.group(1))], body)
    return body

def transform_anchors(text: str) -> str:
    """Rewrite #anchor-slug in-book links to new VitePress URLs."""
    # Match [text](#slug) links
    def sub(m):
        text_part = m.group(1)
        slug = m.group(2)
        normalized_slug = slugify_anchor(slug)
        new_url = ANCHOR_MAP.get(slug) or ANCHOR_MAP.get(normalized_slug)
        if new_url:
            return f"[{text_part}]({new_url})"
        if normalized_slug != slug:
            return f"[{text_part}](#{normalized_slug})"
        return m.group(0)  # unchanged
    return re.sub(r"\[([^\]]+)\]\(#([^)]+)\)", sub, text)

def preserve_code_blocks(text: str) -> tuple:
    """Extract fenced code blocks AND svg divs, replace with placeholders."""
    blocks = []
    def stash(m):
        idx = len(blocks)
        blocks.append(m.group(0))
        return f"\n\n@@CODE{idx}@@\n\n"
    # Stash fenced code blocks
    text = re.sub(r"^```[a-zA-Z]*\n.*?\n^```\s*$", stash, text, flags=re.MULTILINE | re.DOTALL)
    # Stash raw SVG divs produced by transform_svg_fences
    text = re.sub(r"<div class=\"svg-figure\">.*?</div>", stash, text, flags=re.DOTALL)
    return text, blocks

def restore_code_blocks(text: str, blocks: list) -> str:
    def sub(m):
        idx = int(m.group(1))
        return blocks[idx]
    return re.sub(r"@@CODE(\d+)@@", sub, text)

def transform_svg_fences(text: str) -> str:
    """Convert ```svg ... ``` blocks into raw inline HTML div — VitePress markdown+shiki
    doesn't handle svg language well; direct HTML wrapping renders correctly.
    Also strips fixed width/height attrs from the outer <svg> to let CSS enforce max-width: 100%."""
    def sub(m):
        svg = m.group(1)
        # Strip fixed width/height on the outer <svg> so CSS can scale it responsively.
        # Keep viewBox — that gives the browser aspect ratio.
        svg = re.sub(
            r"(<svg\b[^>]*)\s+width=\"[^\"]*\"",
            r"\1",
            svg,
            count=1
        )
        svg = re.sub(
            r"(<svg\b[^>]*)\s+height=\"[^\"]*\"",
            r"\1",
            svg,
            count=1
        )
        # Ensure preserveAspectRatio is set for consistent scaling
        if "preserveAspectRatio=" not in svg:
            svg = re.sub(
                r"(<svg\b)",
                r'\1 preserveAspectRatio="xMidYMid meet"',
                svg,
                count=1
            )
        # CRITICAL: strip blank lines inside the SVG — markdown-it treats a blank line
        # inside a raw HTML block as a terminator, causing the closing </div> to become
        # an orphan and the Vue SFC parser to fail with "Element is missing end tag".
        svg = re.sub(r"\n\s*\n", "\n", svg)
        return f"\n\n<div class=\"svg-figure\">\n{svg}\n</div>\n\n"
    return re.sub(r"^```svg\n(.*?)\n^```\s*$", sub, text, flags=re.MULTILINE | re.DOTALL)

def transform_file(src_path: str) -> str:
    with open(src_path, encoding="utf-8") as f:
        text = f.read()

    # 0. Convert ```svg blocks to raw HTML (must happen before code-block protection)
    text = transform_svg_fences(text)

    # 1. Protect fenced code blocks
    text, blocks = preserve_code_blocks(text)

    # 2. Strip Kramdown-style {: #id } attribute lists from headings
    text = re.sub(r"^(#{1,6}\s+.*?)\s*\{:\s*#[^}]+\}\s*$", r"\1", text, flags=re.MULTILINE)

    # 3. Transform callouts
    text = transform_callouts(text)

    # 4. Escape < and > in the ENTIRE prose (outside code blocks / known HTML tags)
    text = escape_lt_gt_in_prose(text)

    # 5. Transform anchors
    text = transform_anchors(text)

    # 6. Self-close void HTML tags for Vue's XHTML parser (bare <br> -> <br/>, etc.)
    for void in ("br", "hr", "img", "input", "meta", "link", "wbr"):
        text = re.sub(rf"<{void}(\s[^>]*)?>", lambda m: f"<{void}{m.group(1) or ''}/>", text, flags=re.IGNORECASE)

    # 7. Restore fenced code blocks
    text = restore_code_blocks(text, blocks)

    return text

def main():
    print(f"Migrating {SRC} -> {DST}")
    migrated = 0
    for src_name, dst_rel in MAPPING.items():
        if dst_rel is None:
            continue
        src_path = os.path.join(SRC, src_name)
        if not os.path.exists(src_path):
            print(f"  MISS: {src_name}")
            continue
        dst_path = os.path.join(DST, dst_rel)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        transformed = transform_file(src_path)
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(transformed)
        print(f"  {src_name} -> {dst_rel}")
        migrated += 1
    print(f"\nMigrated {migrated} files.")

    # Also create landing pages for patterns/ and data-structures/ if missing
    for sub, title in [("patterns", "The 21 Core Patterns"), ("data-structures", "Data Structures in Depth"), ("appendix", "Appendix"), ("foundations", "Foundations")]:
        idx = os.path.join(DST, sub, "index.md")
        if not os.path.exists(idx):
            with open(idx, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\nSelect a section from the sidebar to begin.\n")

if __name__ == "__main__":
    main()
