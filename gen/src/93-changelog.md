# Changelog

*Reverse-chronological list of substantive reader-facing changes since project inception. Skips typos, merge commits, and internal-only cleanup unless it changes what readers see.*

This changelog is curated from the `gen/src/` git history plus the current Wave B reader-facing additions. The raw source history currently has two content commits on 2026-08-21, so the entries below group those commits by what a reader actually experiences.

## August 2026

### 2026-08-21 — Wave B1+B3 reader navigation additions
- New "How this book compares" page versus Grokking, NeetCode, TakeUForward, and LeetCode Premium.
- New public changelog page so readers can see substantive project changes without reading git history.
- Landing page now links directly to the comparison page.
- Foundations sidebar now exposes the comparison page near the Java foundations chapters.
- Appendix sidebar now exposes the changelog.

### 2026-08-21 — Content consolidation and Grokking-style expansion
- Consolidated the repository to the latest `gen/src/` content source.
- Expanded all 21 pattern chapters with a more consistent mentor-style rhythm.
- Strengthened pattern chapters with recognition cues, when-not-to-use guidance, canonical problems, traps, and interview framing.
- Large chapter updates landed across Sliding Window, Two Pointers, Dynamic Programming, Backtracking, Graphs, Trees, Arrays, Strings, and the remaining pattern/data-structure chapters.
- Preserved the Java-native focus while making the problem explanations more self-contained.

### 2026-08-21 — Initial public site, PDF pipeline, and appendix set
- Initial VitePress site and GitHub Actions deployment pipeline added.
- PDF pipeline added for the offline reference format.
- 21 core pattern chapters introduced, from Sliding Window through Quickselect, plus bonus Math and Design chapters.
- Java Data Structures Primer, Java DSA Gotchas, Complexity Model, Debugging DSA Code, and Zero-to-Hero Roadmap added as foundations.
- Data-structure deep dives added for arrays, strings, linked lists, stacks/queues, trees, heaps, tries, graphs, and segment/Fenwick trees.
- Appendix chapters added: cheat sheets, self-check drills, master problem index, practice solutions, mock interview transcripts, and traps catalog.
- Java 17 is the default implementation language throughout the reference.

### Earlier 2026 — Baseline reference scope
- Core idea established: pattern-first DSA prep for senior/staff interviews.
- Java-native explanations and templates chosen over language-agnostic pseudocode.
- Problem chapters organized around brute force → optimized reasoning → trace → complexity → traps.
- Callout vocabulary introduced for key ideas, invariants, traps, pattern connections, notes, and definitions.
