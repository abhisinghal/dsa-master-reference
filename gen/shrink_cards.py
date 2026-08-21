"""Shrink the 21 pattern cards in 20-patterns.md back to their 30-second-refresher role
(as promised in the front matter). For each card 2..21:
 - Add a '📖 Full write-up' cross-link to the corresponding Part III chapter section
 - Remove the ### Steps block (numbered recipes belong in Part III canonicals)
 - Collapse ### Problem, ### Pattern, ### Complexity subheadings into prose
 - Keep: recognition tagline, one Example, one visualization SVG, one template Java,
   [inv]/[trap] callouts, ### Practice link list.
"""
import re, os

ROOT = os.path.join(os.path.dirname(__file__), "src")

# Card # -> (Part III anchor slug, human-readable chapter name)
PART3 = {
 1: ("sliding-window", "Sliding Window"),
 2: ("two-pointers", "Two Pointers"),
 3: ("linked-lists", "Linked Lists"),
 4: ("prefix-sum-difference-arrays", "Prefix Sum & Difference Arrays"),
 5: ("arrays-hashing", "Arrays & Hashing"),
 6: ("stacks-queues-monotonic-stack", "Stacks & Monotonic Stack"),
 7: ("binary-search-search-on-answer", "Binary Search & Search-on-Answer"),
 8: ("binary-search-search-on-answer", "Binary Search & Search-on-Answer"),
 9: ("heaps-priority-queues", "Heaps"),
 10: ("heaps-priority-queues", "Heaps · K-way Merge"),
 11: ("intervals-sweep-line", "Intervals & Sweep Line"),
 12: ("intervals-sweep-line", "Intervals & Sweep Line"),
 13: ("graphs", "Graphs · Topological Sort"),
 14: ("graphs", "Graphs · Union-Find"),
 15: ("greedy", "Greedy"),
 16: ("recursion-backtracking", "Recursion & Backtracking"),
 17: ("divide-conquer-quickselect", "Divide & Conquer"),
 18: ("dynamic-programming", "Dynamic Programming"),
 19: ("tries-prefix-trees", "Tries"),
 20: ("bit-manipulation", "Bit Manipulation & Bitmasking"),
 21: ("divide-conquer-quickselect", "Divide & Conquer · Quickselect"),
}

def shrink_card(num, header, body):
    """body is the text between '## N. Name' and the next '## ' header."""
    slug, name = PART3[num]

    # 1. Extract the Recognition tagline
    recog_m = re.search(r'^\*Recognition\s*[\u2014-]\s*(.*?)\.?\*$', body, re.MULTILINE)
    recog = recog_m.group(1).strip() if recog_m else None

    # 2. Extract example line (typically "**Example.** ..." or "**Example:** ...")
    example_m = re.search(r'^\*\*Example\.\*\*\s*(.*?)$', body, re.MULTILINE)
    if not example_m:
        example_m = re.search(r'^\*\*Example:\*\*\s*(.*?)$', body, re.MULTILINE)
    example = example_m.group(1).strip() if example_m else None

    # 3. Extract Problem prose (short — the second paragraph after Problem heading)
    prob_m = re.search(r'^### Problem\n(?:(?!^###)(?!^\*\*Example).)+', body, re.DOTALL | re.MULTILINE)
    prob = None
    if prob_m:
        prob_text = prob_m.group(0).split('\n', 1)[1].strip()
        # Keep the first non-empty line (typically an italic problem statement)
        for line in prob_text.split('\n\n'):
            if line.strip():
                prob = line.strip()
                break

    # 4. Extract Pattern prose (one paragraph)
    pat_m = re.search(r'^### Pattern\n((?:(?!^###)(?!^\*\*Template).)+?)(?=\n(?:```|>|###)|\Z)', body, re.DOTALL | re.MULTILINE)
    pat = pat_m.group(1).strip() if pat_m else None

    # 5. Extract invariant/trap callouts (single-line format)
    inv_m = re.search(r'^> \[inv\][^\n]+', body, re.MULTILINE)
    inv = inv_m.group(0) if inv_m else None
    trap_m = re.search(r'^> \[trap\][^\n]+', body, re.MULTILINE)
    trap = trap_m.group(0) if trap_m else None

    # 6. Extract SVG block(s) — keep them
    svg_ms = re.findall(r'```svg\n.*?\n```(?:\n<div class="figcap">.*?</div>)?', body, re.DOTALL)

    # 7. Extract the FIRST Java template block (the one with template label if present)
    java_m = re.search(r'(?:^\*\*Template\s*[\u2014-][^\n]+\*\*\n)?```java\n(.*?)\n```', body, re.DOTALL | re.MULTILINE)
    java_code = java_m.group(1) if java_m else None
    # Also try the ### Java (template ...) form
    if not java_code:
        java_m = re.search(r'### Java[^\n]*\n```java\n(.*?)\n```', body, re.DOTALL)
        java_code = java_m.group(1) if java_m else None

    # 8. Extract Complexity line (single line after ### Complexity)
    comp_m = re.search(r'^### Complexity\n([^\n]+)', body, re.MULTILINE)
    complexity = comp_m.group(1).strip() if comp_m else None

    # 9. Extract Practice bullet list
    prac_m = re.search(r'### Practice\n((?:^- .+\n?)+)', body, re.MULTILINE)
    practice = prac_m.group(1).rstrip() if prac_m else None

    # ---- Rebuild ----
    out = [header, ""]
    if recog:
        out.append(f"*Recognition — {recog}.*")
        out.append("")
    out.append(f'<div class="see-full">📖 <b>Full write-up</b> — the "why / when / how / when-not" story lives in <a href="#{slug}">Part III · {name}</a>. This card is a 30-second refresher.</div>')
    out.append("")
    if prob or pat:
        out.append("### Idea (in one line)")
        # Prefer Pattern prose as the idea (it's usually the punch line); fall back to Problem
        idea = pat or prob
        # Collapse newlines
        idea = re.sub(r'\s+', ' ', idea).strip()
        out.append(idea)
        out.append("")
    if example:
        out.append(f"**Example.** {example}")
        out.append("")
    if inv:
        out.append(inv); out.append("")
    if trap:
        out.append(trap); out.append("")
    for svg in svg_ms[:1]:                  # keep only the FIRST svg — the primary viz
        out.append(svg); out.append("")
    if java_code:
        out.append("### Template")
        out.append("```java")
        out.append(java_code)
        out.append("```")
        if complexity:
            out.append(f"*{complexity}*")
        out.append("")
    if practice:
        out.append("### Practice")
        out.append(practice)
        out.append("")
    return "\n".join(out)

def process():
    path = os.path.join(ROOT, "20-patterns.md")
    txt = open(path, encoding="utf-8").read()
    # Split at ## N. markers
    parts = re.split(r'(?m)^(## (\d+)\. [^\n]+)$', txt)
    # parts: [pre, header1, num1, body1, header2, num2, body2, ...]
    out = [parts[0]]
    i = 1
    changed = 0
    while i < len(parts):
        header = parts[i]
        num = int(parts[i+1])
        body = parts[i+2] if i+2 < len(parts) else ""
        if num in PART3 and num != 1:       # #1 already manually shrunk
            new_body = shrink_card(num, header, body)
            out.append(new_body)
            changed += 1
        else:
            out.append(header + body)
        i += 3
    open(path, "w", encoding="utf-8").write("".join(out))
    return changed

if __name__ == "__main__":
    n = process()
    print(f"cards shrunk to refresher form: {n}")
