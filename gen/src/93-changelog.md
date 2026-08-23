# Changelog

*Reverse-chronological list of substantive reader-facing changes since project inception. Skips typos, merge commits, and internal-only cleanup unless it changes what readers see.*

This changelog is curated from the `gen/src/` git history plus recent reader-facing additions. Entries are grouped by what a reader actually experiences.

## November 2026 — CEO plan execution

### 2026-11 — Round 20: Behavioral Interview Crash Course
- New Behavioral Crash Course appendix chapter (STAR + 6 archetypes + 15 canonical questions).
- Appendix sidebar now surfaces Interview Day Kit and Behavioral Crash Course explicitly.

### 2026-11 — Round 19: Personalized Study Plan Generator
- Landing has a Study Plan Generator: pick 1/2/4/8/12 weeks and target level (mid/senior/staff) → get a curated week-by-week plan referencing book chapters.

### 2026-11 — Round 18: Interactive Roadmap checklist
- Roadmap chapter now has clickable weekly checkboxes with a live progress bar (locally persisted).

### 2026-11 — Round 17: Bookmarks
- Bookmark button on every problem page (amber pill next to Mark Solved).
- Landing shows your top 10 bookmarks, sorted newest-first.

### 2026-11 — Round 16: Interview Timer
- Interview Timer collapsible panel on all 205 problem pages — start/pause/reset and save your best time per problem.
- Target-time hints for Medium (20-25 min) and Hard (30-40 min).

### 2026-11 — Round 15: Streak notification bell + print button
- Bottom-left notification bell nudges you to solve today when your streak is at risk (per-day dismiss).
- Every pattern chapter has a "Print chapter" button for offline reference.

### 2026-11 — Round 14: Custom 404 + Problem Stats
- Dedicated 404 page with 6 suggested links (patterns / roadmap / all problems / Meta track / traps / day kit) instead of the default VitePress 404.
- Problem index shows your solved / total / percentage with a live progress bar.

### 2026-11 — Round 13: Reading progress + Back to top
- Fixed gradient progress bar at the top of every page tracking scroll position.
- Floating back-to-top button appears after 400px of scroll.

### 2026-11 — Round 12: Related Problems widget
- Each problem page now recommends 3 sibling problems from the same pattern for lateral browsing.

### 2026-11 — Round 11: Spaced repetition (Due For Review)
- Landing surfaces up to 5 problems you last solved 7+ days ago — a targeted spaced-repetition list.
- Mark Solved now stores solve timestamps (backward-compatible with older `'true'` values).

### 2026-11 — Round 10: Related Patterns + RSS refresh
- Every pattern chapter now recommends 3 conceptually related patterns.
- RSS feed refreshed with entries for all recent releases.

### 2026-11 — Round 9: Interview Day Kit + print-friendly styles
- New Interview Day Kit page — 24-hour countdown checklist with emergency mode.
- Landing gained two new feature cards: Company Tracks (Meta / Google / Amazon) and Interview Day Kit.
- Print CSS added: interactive overlays hidden, hints and code traces stay visible when printing.

### 2026-11 — Round 8: Company Tracks
- New Meta / Google / Amazon track pages with 4-week problem sequences and level-by-level focus.
- Company Tracks dropdown added to the top navigation.

### 2026-11 — Round 7: Streaks + Share buttons
- Added a StreakTracker on the landing showing consecutive-day activity with fire-emoji tiers.
- Added ShareButtons using the Web Share API plus Twitter and LinkedIn quick-share.

### 2026-11 — Round 6: Social proof + support
- Landing gained a Social Proof panel with 4 anonymized composite testimonials.
- Added a Support panel with GitHub Sponsors and Buy Me a Coffee links (monetization Path 1 = free + newsletter/sponsors).

### 2026-11 — Round 5: Mark solved + storage manager
- Every problem page now has a Mark Solved button (with confetti) that syncs with the pattern progress bar.
- Roadmap now has a Storage Manager to export/import/clear all local progress as JSON.

### 2026-11 — Round 4: Onboarding tour + page analytics
- First-time visitors see a 6-step onboarding tour highlighting hints, runner, and AI companion.
- Privacy-first client-side page-view counter (no external tracking).

### 2026-11 — Round 3: Feedback + keyboard shortcuts
- Thumbs up/down + free-text feedback widget on all 205 problem pages.
- Floating keyboard-shortcut hint panel (H = hints, R = runner, A = AI companion).

### 2026-11 — Round 2: Per-pattern progress bar
- Each of the 21 pattern chapters now shows a live progress bar combining solved problems and quiz scores.
- Landing feature grid refreshed to lead with AI Companion, Hints, and Quizzes.

### 2026-11 — Round 1: Landing polish + user profile
- Added a "Try it before you read it" strip on the landing.
- User Profile card with solved count now displayed prominently.
- Newsletter capture and AI chat now have dismiss + 30-day expiry.

### 2026-11 — Wave C: AI companion + pattern videos
- Added an AI Companion chat panel to all 205 problem pages (pattern-templated MVP responses; wired to swap in a real LLM).
- Added a Pattern Video placeholder to all 21 pattern chapters (YouTube/Loom-ready with a "coming soon" fallback).

### 2026-11 — Wave B: User accounts + email capture
- Local User Profile with solved-count badge (localStorage-only; ready for future cross-device auth).
- Email capture on the landing with local dismiss/success states (backend integration pending user signup).

### 2026-11 — Wave A: Hints, company tags, quizzes, Java runner
- Progressive 3-hint reveal system on all 205 problem pages.
- Company tags (Meta / Google / Amazon and 60+ others) on 194 problem pages.
- Every one of the 21 pattern chapters now ends with a 5-question quiz (105 questions total).
- Interactive Java runner (CheerpJ WASM in-browser) embedded on all 205 problem pages — no server needed.

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
