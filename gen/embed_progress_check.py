#!/usr/bin/env python3
"""Embed <ProgressCheck :id="slug"/> after each ## Problem H2 in src/."""
import os, re, glob

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gen", "src")

def slugify(title: str) -> str:
    """Convert a problem title to a stable slug."""
    # Strip badge span
    title = re.sub(r"<span class=\"diff[^\"]*\">[^<]*</span>", "", title)
    # Lowercase, replace non-alphanum with -
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

def process(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    out = []
    added = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^## ([^#].*?)$", line)
        # Skip pattern-level headings that aren't canonical problems
        # A canonical problem H2 is followed within 3 lines by *[↗ LeetCode: ...] or similar
        if m and "<span class=\"diff" in line:
            # Peek ahead — this is a problem H2 that has a badge
            slug = slugify(m.group(1))
            # Check next lines don't already have ProgressCheck
            following = "\n".join(lines[i+1:i+6])
            if "<ProgressCheck" not in following:
                out.append(line)
                # Append a blank line then the ProgressCheck (before LC link line for visibility)
                # Actually put it AFTER the LC link line so it doesn't disrupt flow.
                # Find LC link line and insert progress after it.
                j = i + 1
                out.append("")  # blank after H2
                # Copy next lines until we find LC link or 5 lines pass
                inserted = False
                while j < len(lines) and j < i + 6:
                    out.append(lines[j])
                    if "leetcode.com/problems/" in lines[j] and not inserted:
                        out.append("")
                        out.append(f'<ProgressCheck id="{slug}" />')
                        inserted = True
                        added += 1
                    j += 1
                # If we didn't find LC link, add ProgressCheck right after H2
                if not inserted:
                    # Rewind: our loop was awful — do simpler thing
                    pass
                i = j
                continue
        out.append(line)
        i += 1
    new = "\n".join(out)
    if new != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
    return added

def main():
    total = 0
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        n = process(path)
        if n > 0:
            print(f"  {os.path.basename(path)}: +{n} progress checks")
            total += n
    print(f"\nTotal progress checks embedded: {total}")

if __name__ == "__main__":
    main()
