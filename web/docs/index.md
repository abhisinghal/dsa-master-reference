---
layout: home

hero:
  name: DSA Master Reference
  text: Zero to Hero for Senior/Staff Interviews
  tagline: Patterns · Invariants · Problems — Java 17, Grokking-style depth, 300+ curated pages
  image:
    src: /hero.svg
    alt: DSA Master Reference
  actions:
    - theme: brand
      text: Get Started
      link: /foundations/roadmap
    - theme: alt
      text: Browse Patterns
      link: /patterns/
    - theme: alt
      text: View on GitHub
      link: https://github.com/abhisinghal/dsa-master-reference

features:
  - icon: 🎯
    title: 21 Core Patterns
    details: Every pattern with story intro, when-to-use, templates, canonical problems, and interview scripts. Sliding Window to Quickselect.
    link: /patterns/
    linkText: Explore patterns
  - icon: 📚
    title: Learning Notes on Every Line
    details: Why <code>Long.MIN_VALUE</code>? Why <code>right >= k-1</code>? Every non-obvious code decision explained bullet-by-bullet.
    link: /patterns/sliding-window
    linkText: See in action
  - icon: 🗺️
    title: 8-Week Roadmap
    details: Pre-flight quiz, weekly cadence (2 canonical + 2 variations + 1 mock), staff-level readiness signals.
    link: /foundations/roadmap
    linkText: See the plan
  - icon: 💡
    title: 20 Java Gotchas
    details: <code>Integer.MIN_VALUE</code> overflow, autoboxing cost, ArrayDeque vs Stack, TreeMap floor/ceiling — the pitfalls that cost interviews.
    link: /foundations/java-gotchas
    linkText: Read gotchas
  - icon: 🎬
    title: Mock Interview Transcripts
    details: Easy (Two Sum), Medium (LRU Cache), Hard (Sliding Window Maximum) — verbatim what a senior candidate says.
    link: /appendix/mock-transcripts
    linkText: Read transcripts
  - icon: ⚠️
    title: 109 Traps Catalog
    details: Every trap callout consolidated in one place for interview-eve revision.
    link: /appendix/traps-catalog
    linkText: Skim traps
---

## Why this book exists

Most DSA references are one of two things: **a textbook** (dense theory, no interview signal) or **a LeetCode grind list** (500 problems, zero pattern recognition). This is neither.

- **Pattern-first** — you learn to *recognize* what family a problem belongs to, then apply the right template.
- **Java-native** — all code is idiomatic Java 17. No Python-style pseudocode.
- **Interview-calibrated** — every problem has a "how would you defend this in an interview" script.
- **Learning notes on every line** — *why* is `Long.MIN_VALUE` the seed and not `0`? *why* `long` and not `int`? Every non-obvious decision is called out.

## What's inside

- **Part I — Foundations**: Java Data Structures primer, complexity model, Java gotchas, debugging DSA code
- **Part II — 21 Core Patterns**: Sliding Window, Two Pointers, Prefix Sum, Binary Search, DP, Backtracking, Union-Find, and more
- **Part III — Data Structures in Depth**: Arrays, Strings, Linked Lists, Trees, Heaps, Trie, Graphs, Segment Tree
- **Part IV — Cheat Sheets & Self-Check**: templates, drills, problem index, mock transcripts, traps catalog

## Also available as PDF

The full 300+ page reference is also available as a PDF (light + dark themes) — [download from Releases](https://github.com/abhisinghal/dsa-master-reference/releases).
