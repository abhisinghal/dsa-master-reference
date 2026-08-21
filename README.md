# DSA Master Reference

A pattern-first Data Structures & Algorithms reference for senior/staff engineering interviews. Java 17-native, Grokking-style depth, 340+ pages.

**Live site:** https://abhisinghal.github.io/dsa-master-reference/

## Contents

- **Part I — Foundations** (`foundations/`): Java Data Structures primer, complexity model, Java gotchas, debugging DSA code, zero-to-hero roadmap
- **Part II — 21 Core Patterns** (`patterns/`): Sliding Window, Two Pointers, Prefix Sum, Binary Search, DP, Backtracking, Union-Find, and 15 more
- **Part III — Data Structures in Depth** (`data-structures/`): Arrays, Strings, Linked Lists, Trees, Heaps, Trie, Graphs, Segment Tree
- **Part IV — Cheat Sheets & Self-Check** (`appendix/`): templates, drills, problem index, mock transcripts, traps catalog

## Interactive features

- ✅ **Interactive Java runner** on 7 canonical problems (Two Sum, Longest Substring, Binary Search, Coin Change, Max Subarray, Reverse Linked List, Valid Parentheses) — powered by [Judge0](https://ce.judge0.com)
- ✅ **7 animated SVG walkthroughs** — Sliding Window, Monotonic Stack, Union-Find, Sweep Line, Divide & Conquer, Quickselect, Backtracking — with play/pause/step controls
- ✅ **Progress tracker** — mark problems as solved (localStorage-backed, per-pattern solved-count badge in sidebar)
- ✅ **Difficulty badges** on every canonical problem (Easy / Medium / Hard)
- ✅ **Recently updated** section on landing page
- ✅ **Print CSS** — Ctrl+P produces a clean PDF from any page
- ✅ **Search** — VitePress local full-text search
- ✅ **Dark mode** — WCAG AA contrast-audited

## PDF downloads

The full 340-page reference is also available as a PDF (light + dark themes) — [download from Releases](https://github.com/abhisinghal/dsa-master-reference/releases).

## Repository layout

```
.github/workflows/     # GitHub Actions — auto-deploy VitePress site to Pages
gen/                   # PDF pipeline (Python + Puppeteer)
├── src/               # Chapter markdown source (48 files)
├── build.py           # Markdown → styled HTML
├── render.js          # HTML → PDF (light + dark)
├── style.css          # Print styling
├── style-dark.css
├── mermaid.min.js     # Mermaid runtime for diagrams
├── execute_book_solutions.py  # Java compile-and-run harness for canonical solutions
├── add_difficulty_badges.py   # Bulk badge injection for problem H2s
├── add_java_runners.py        # Bulk <JavaRunner> embed for top problems
└── embed_progress_check.py    # Bulk <ProgressCheck> embed after problem H2s

web/                   # VitePress site
├── docs/              # Site content (auto-generated from ../gen/src via migrate.py)
│   ├── .vitepress/    # VitePress config, theme, plugins
│   ├── foundations/   # Roadmap, playbook, Java primer, gotchas, debugging
│   ├── patterns/      # 21 core patterns + math + design
│   ├── data-structures/ # Arrays, strings, lists, trees, heaps, trie, graphs, segtree
│   ├── appendix/      # Cheatsheets, self-check, problem index, mocks, traps
│   └── public/        # Static assets (favicon, hero SVG, robots.txt)
├── migrate.py         # Transforms gen/src markdown → docs/ (Vue callouts, SVG figures)
└── package.json       # VitePress + mermaid deps
```

## Local development

### Preview the website

```powershell
cd web
npm install
python migrate.py       # Copy content from ../gen/src → docs/
npx vitepress dev docs  # Preview at http://localhost:5173
```

### Build the PDF

```powershell
cd gen
python build.py         # Light HTML
python build.py dark    # Dark HTML
node render.js          # Render DSA_MASTER_REFERENCE.pdf
node render.js dark     # Render DSA_MASTER_REFERENCE_dark.pdf
```

### Validate Java solutions

```powershell
cd gen
python execute_book_solutions.py    # Compiles + runs 18 canonical Java solutions
```

## License

MIT
