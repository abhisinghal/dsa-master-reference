#!/usr/bin/env python3
"""Stitch all chapter sources into a single editable DSA_MASTER_REFERENCE2.md."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "src" / "content"
manifest = json.loads((ROOT / "src" / "manifest.json").read_text(encoding="utf-8"))

out = []
out.append(f"# {manifest['title']}\n")
out.append("> Senior / Staff Interview Edition — a pattern-first field guide to "
           "Data Structures & Algorithms in Java.\n")
out.append("> \n")
out.append("> This file is the concatenated editable source. It is generated from the "
           "per-chapter Markdown in `src/content/` (the true source of truth) and is "
           "rendered to `DSA_MASTER_REFERENCE2.pdf` by the build pipeline. "
           "Fenced ```diagram blocks are rendered to SVG at build time.\n")

for item in manifest["items"]:
    if item["type"] == "part":
        out.append(f"\n\n---\n\n# {item['label']} — {item['title']}\n")
        if item.get("subtitle"):
            out.append(f"*{item['subtitle']}*\n")
    elif item["type"] == "chapter":
        f = CONTENT / item["file"]
        if not f.exists():
            continue
        out.append(f"\n\n---\n\n# {item.get('kicker','')} — {item['title']}\n")
        if item.get("subtitle"):
            out.append(f"*{item['subtitle']}*\n")
        out.append("")
        out.append(f.read_text(encoding="utf-8"))

(ROOT / "DSA_MASTER_REFERENCE2.md").write_text("\n".join(out), encoding="utf-8")
size = (ROOT / "DSA_MASTER_REFERENCE2.md").stat().st_size
print(f"wrote DSA_MASTER_REFERENCE2.md ({size//1024} KB)")
