# DSA Master Reference

A pattern-first Data Structures & Algorithms reference for senior/staff engineering interviews. Java 17-native, Grokking-style depth.

**Live site:** https://abhisinghal.github.io/dsa-master-reference/

## Contents

- **Part I — Foundations**: Java Data Structures primer, complexity model, Java gotchas, debugging DSA code, zero-to-hero roadmap
- **Part II — 21 Core Patterns**: Sliding Window, Two Pointers, Prefix Sum, Binary Search, DP, Backtracking, Union-Find, and 15 more
- **Part III — Data Structures in Depth**: Arrays, Strings, Linked Lists, Trees, Heaps, Trie, Graphs, Segment Tree
- **Part IV — Cheat Sheets & Self-Check**: templates, drills, problem index, mock transcripts, traps catalog

## PDF downloads

The full 300+ page reference is also available as PDF (light + dark themes) in [Releases](https://github.com/abhisinghal/dsa-master-reference/releases).

## Local development

```powershell
cd web
npm install
python migrate.py       # Copy content from ../gen/src2 → docs/
npx vitepress dev docs  # Preview at http://localhost:5173
```

## Building the PDF

```powershell
cd gen
python build2.py        # Generates output8.html from src2/
node render2.js         # Renders DSA_MASTER_REFERENCE8.pdf
node render2.js dark    # Renders DSA_MASTER_REFERENCE8_dark.pdf
```

## Structure

```
gen/                # PDF pipeline (Python + Puppeteer)
├── src/            # Original markdown source (v7 — 295 pages)
├── src2/           # Grokking-restructured source (v8 — target 320+ pages)
├── build.py        # Builds v7 HTML from src/
├── build2.py       # Builds v8 HTML from src2/
├── render.js       # v7 PDF renderer
└── render2.js      # v8 PDF renderer

web/                # VitePress site
├── docs/           # Site content (auto-migrated from gen/src2/)
├── migrate.py      # Content transformation script
└── package.json    # VitePress + deps

snapshots/          # Preservation baselines for rollback
```

## License

MIT
