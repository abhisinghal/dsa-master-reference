---
layout: home

hero:
  name: DSA Master Reference
  text: Zero to Hero for Senior/Staff Interviews
  tagline: Patterns · Invariants · Problems — Java 17, Grokking-style depth, Instant offline reference — 340 pages, searchable PDF
  image:
    src: /dsa-master-reference/hero.svg
    alt: Sliding Window on 9 cells with two overlapping windows
  actions:
    - theme: brand
      text: Get Started
      link: /foundations/roadmap
    - theme: alt
      text: Browse Patterns
      link: /patterns/
    - theme: alt
      text: See it in action
      link: /patterns/hashing#try-it-yourself
    - theme: alt
      text: View on GitHub
      link: https://github.com/abhisinghal/dsa-master-reference

features:
  - icon: /dsa-master-reference/icons/patterns.svg
    title: 21 Core Patterns
    details: Every pattern with story intro, when-to-use, templates, canonical problems, and interview scripts. Sliding Window to Quickselect.
    link: /patterns/
    linkText: Explore patterns
  - icon: /dsa-master-reference/icons/learning.svg
    title: Learning Notes on Every Line
    details: Why <code>Long.MIN_VALUE</code>? Why <code>right >= k-1</code>? Every non-obvious code decision explained bullet-by-bullet.
    link: /patterns/sliding-window
    linkText: See in action
  - icon: /dsa-master-reference/icons/roadmap.svg
    title: 8-Week Roadmap
    details: Pre-flight quiz, weekly cadence (2 canonical + 2 variations + 1 mock), staff-level readiness signals.
    link: /foundations/roadmap
    linkText: See the plan
  - icon: /dsa-master-reference/icons/gotchas.svg
    title: 205 Interactive Problems
    details: Every problem has a Java runner (CheerpJ WASM), progressive hints, company tags, and an AI companion for stuck-on-a-problem help.
    link: /problems/
    linkText: Start solving
  - icon: /dsa-master-reference/icons/mocks.svg
    title: Progressive Hints + AI Companion
    details: 3-level reveal on every problem; AI chat that answers "explain differently", "give me a nudge", "what edge cases?" — never spoils the solution.
    link: /problems/hashing-two-sum
    linkText: Try on Two Sum
  - icon: /dsa-master-reference/icons/traps.svg
    title: 109 Traps + 105 Quiz Questions
    details: Every trap callout in one appendix. 5-question quiz at the end of every pattern chapter — score is saved locally.
    link: /appendix/traps-catalog
    linkText: Skim traps
  - icon: /dsa-master-reference/icons/comparison.svg
    title: How this compares
    details: Side-by-side vs Grokking, NeetCode, TakeUForward, LeetCode Premium. Where this book wins and where it doesn't.
    link: /foundations/vs-competitors
    linkText: See the comparison
---

<div class="screenshot-strip">
  <img src="/mock-screenshots/screenshot-runner.svg" alt="Interactive Java runner" class="screenshot" />
  <img src="/mock-screenshots/screenshot-animation.svg" alt="Sliding window animation" class="screenshot" />
  <img src="/mock-screenshots/screenshot-mobile.svg" alt="Mobile-responsive view" class="screenshot" />
</div>

## Recently updated

<RecentUpdates />

## Built by

<div class="author-bio">
  <img src="https://github.com/abhisinghal.png?size=140" alt="Abhishek Singhal" class="author-avatar" />
  <div class="author-text">
    <h3>Abhishek Singhal</h3>
    <p>Senior Software Engineer. Built this reference over months of solo work while preparing for senior/staff interviews. If you found this useful, connect with me on <a href="https://github.com/abhisinghal">GitHub</a>.</p>
  </div>
</div>

# DSA Master Reference

## Try it before you read it

<div class="try-it-strip">
  <div class="try-it-card">
    <div class="try-it-icon">▶</div>
    <div class="try-it-body">
      <div class="try-it-title">Run Java on any problem — no signup</div>
      <div class="try-it-sub">CheerpJ WASM runtime, in-browser, on 205 problems.</div>
    </div>
  </div>
  <div class="try-it-card">
    <div class="try-it-icon">💡</div>
    <div class="try-it-body">
      <div class="try-it-title">Progressive hints on every page</div>
      <div class="try-it-sub">3 levels of help — general → specific → near-solution.</div>
    </div>
  </div>
  <div class="try-it-card">
    <div class="try-it-icon">✨</div>
    <div class="try-it-body">
      <div class="try-it-title">AI companion per problem</div>
      <div class="try-it-sub">Ask "explain differently", "give me a nudge", "what edge cases?"</div>
    </div>
  </div>
  <div class="try-it-card">
    <div class="try-it-icon">🎯</div>
    <div class="try-it-body">
      <div class="try-it-title">Pattern quizzes with scoring</div>
      <div class="try-it-sub">5 questions per pattern; 105 questions total. Tracks progress.</div>
    </div>
  </div>
</div>

<UserProfile />

<div class="stats-strip">
  <div class="stat">
    <div class="stat-value">338</div>
    <div class="stat-label">Pages (PDF)</div>
  </div>
  <div class="stat">
    <div class="stat-value">21</div>
    <div class="stat-label">Core patterns</div>
  </div>
  <div class="stat">
    <div class="stat-value">205</div>
    <div class="stat-label">Interactive problems</div>
  </div>
  <div class="stat">
    <div class="stat-value">109</div>
    <div class="stat-label">Interview traps</div>
  </div>
  <div class="stat">
    <div class="stat-value">105</div>
    <div class="stat-label">Quiz questions</div>
  </div>
  <div class="stat">
    <div class="stat-value">✨</div>
    <div class="stat-label">AI companion + Java runner on every page</div>
  </div>
</div>

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

## Also available as a searchable offline PDF

For flights, whiteboarding, or interview eve without WiFi. Same content as the website. [Download from Releases](https://github.com/abhisinghal/dsa-master-reference/releases).

<EmailCapture />

<style scoped>
.stats-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  padding: 24px 0;
  margin: 24px 0;
  border-top: 1px solid var(--vp-c-divider);
  border-bottom: 1px solid var(--vp-c-divider);
}
.stat {
  text-align: center;
}
.stat-value {
  font-size: 2em;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  line-height: 1;
}
.stat-label {
  font-size: 0.82em;
  color: var(--vp-c-text-2);
  margin-top: 4px;
}
.try-it-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 12px;
  margin: 24px 0 32px;
}
.try-it-card {
  display: flex;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  transition: transform 0.15s, border-color 0.15s;
}
.try-it-card:hover {
  transform: translateY(-2px);
  border-color: var(--vp-c-brand-1);
}
.try-it-icon {
  font-size: 24px;
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--vp-c-brand-1), var(--vp-c-brand-2));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.try-it-title {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
.try-it-sub {
  font-size: 11.5px;
  color: var(--vp-c-text-2);
  margin-top: 2px;
  line-height: 1.4;
}
.screenshot-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin: 32px 0;
}
.screenshot {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  border: 1px solid var(--vp-c-divider);
}
.author-bio {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px;
  margin: 24px 0;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
}
.author-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 3px solid var(--vp-c-brand-1);
  flex-shrink: 0;
}
.author-text h3 { margin-top: 0; }
.author-text p { margin-bottom: 0; color: var(--vp-c-text-2); }
@media (max-width: 600px) {
  .author-bio { flex-direction: column; text-align: center; }
}
</style>
