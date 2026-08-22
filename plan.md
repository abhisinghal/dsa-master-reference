# DSA Master Reference — Live Plan

Last updated: 2026-08-22 (session c960137b).
Live at https://abhisinghal.github.io/dsa-master-reference/ · Repo `abhisinghal/dsa-master-reference` · Latest commit `73fa0ae`.

---

## Where we are — honest scorecard

Tier-1 visuals sprint (originally 50–60 h) is **~85% shipped**:

| Batch | Scope | Ship state |
|---|---|---|
| 1. Design tokens | ~30 `--dsa-*` CSS custom properties, light + dark | ✅ 85% (spec-audit of hardcoded hex in older SVGs still open) |
| 2. StepStrip layout | Component + real usage in chapters | ✅ 60% — component live, 1 real usage (Two Sum comic strip in hashing) |
| 3. 30 problem SVGs | Static visual per canonical problem | ✅ 90% — 49 SVGs total across 26 files, covers 30 canonicals |
| 4. Animation components | 8 animated Vue components | ✅ 85% — 15 components exist, 14 pattern chapters embed one |
| 5. Icon system swap | Emojis → SVG icons across the app | ✅ 90% — Icon.vue with 15 lucide-style glyphs, 5 Vue components + 23 markdown files cleaned |

Ancillary CEO-review Wave A/B items (from earlier in this session):
- ✅ CheerpJ browser Java runner (kills Judge0 rate-limit trust issue)
- ✅ Sidebar filter (problems only, no section-heading noise)
- ✅ URL slug normalization (no em-dashes)
- ✅ 100% difficulty-badge coverage
- ✅ Per-pattern quiz component (Quiz.vue, 63 questions across 21 chapters)
- ✅ How-this-compares + Changelog pages
- ✅ Author bio on landing
- ✅ Video callout placeholders (5 patterns)
- ✅ PDF messaging repositioned

Blocked (needs your action, not mine):
- ⏸ Email capture / PDF gate — waiting on your Buttondown or ConvertKit signup + API key.

Critical fix landed this session:
- `migrate.py` `transform_svg_fences()` now strips blank lines inside inline `\`\`\`svg` blocks (root cause of the 7-hour dp.md build hang). Prevents future recurrence for any author-supplied SVG.

---

## The next plan — three tracks, you pick

I've split remaining work into three tracks. Each is independently valuable; you can approve any subset.

### Track A — Close the last 15% of Tier-1 (~4–6 h)

Small, high-consistency work that finishes what we started, no new features:

| # | Item | Effort | Delivers |
|---|---|---|---|
| A1 | Design-token audit of every existing SVG — replace any residual `#hex` with `var(--dsa-*)` | 90 min | Guaranteed dark-mode consistency; no more theme-mismatch cells |
| A2 | 4 more StepStrip wrappers on flagship problems (SlidingWindowStepStrip, HouseRobberStepStrip, BacktrackingSubsetsStepStrip, BinarySearchStepStrip) | 2 h | Signature "Grokking comic-strip" moment on 5 chapters instead of 1 |
| A3 | Embed remaining anims in 7 pattern chapters that would benefit (prefix-sum, k-way-merge, greedy, trees, heaps, trie, segment-fenwick) — reuse existing anim components with new step content, or defer if no fitting component exists | 1.5 h | Anim coverage 14 → 21 of 29 patterns |
| A4 | Landing-page screenshots — take 3 real screenshots (JavaRunner mid-run, sliding-window animation, mobile view) and embed above features grid | 30 min | Landing feels like a product not a docs page |

**Recommendation: yes, do A1 + A4 immediately. A2 + A3 if you want the "wow-per-chapter" density.**

### Track B — Wave C from the CEO review (~15–25 h) — content, not visuals

Content depth that separates a reference from a course:

| # | Item | Effort | Delivers |
|---|---|---|---|
| B1 | Extend mock transcripts from 3 → 15 | 6–8 h | Interview-realism content moat |
| B2 | System design intro chapter (25–35 pages: URL shortener, rate limiter, KV store fundamentals) | 8–10 h | Senior/staff interviews are 50% system design; you have 0 pages |
| B3 | Company tracks (Meta / Google / Amazon annotated lists) | 3–4 h | Buyer motivation for many candidates |
| B4 | Behavioural interview prep (STAR framework, 10 common prompts, sample answers) | 2 h | Rounds out the loop |
| B5 | Anti-pattern generator ("here's how NOT to solve — find the bug") | 2 h per pattern | Unique interview-prep angle no one else does well |

**Recommendation: B2 first (highest single-item lift for senior-target audience). Then B3 for buyer clarity. Defer B1/B4/B5 to a subsequent sprint.**

### Track C — Distribution / audience (~4–8 h + ongoing user work)

The ByteByteGo-CEO items — nothing about content, everything about who reads it:

| # | Item | Effort | Delivers |
|---|---|---|---|
| C1 | Email capture on PDF download (BLOCKED — needs your Buttondown signup) | 1.5 h once you sign up | Newsletter list, retention channel |
| C2 | RSS feed for the changelog page | 30 min | Return-visitor notification |
| C3 | Shareable "money graphics" — square 1200×1200 export of top 5 pattern diagrams with title + logo watermark for LinkedIn/Twitter | 3 h | Social distribution flywheel |
| C4 | 5–10 minute Loom video walkthrough for 1 flagship pattern (Sliding Window) — you record, I write the script and slides | 30 min script + 45 min your recording time | Video is table stakes for 2026 interview prep sites |
| C5 | "Start here" 90-second landing intro video | 45 min | 3–5× conversion lift on cold traffic (documented industry benchmark) |

**Recommendation: C2 today (30 min, no dependency). C1 as soon as you pick a provider. C3–C5 need your recording time.**

---

## What I recommend as your next single decision

**Track A only** (~4–6 h agent time): pick the highest-density, no-dependency work. Finishes what we started. No design decisions required from you.

**Track A + B2** (~14 h agent time): also ships the system-design chapter, which is the single biggest content gap for a senior/staff audience.

**Track A + Track B fully** (~30 h agent time): pushes the product into course-level completeness for the interview-prep niche.

**None of the above — different direction**: tell me what to prioritize and I re-plan.

---

## Blockers waiting on you

1. **Newsletter provider choice** — Buttondown (dev-friendly, $9/mo after 100 subs, generous API), ConvertKit (marketer-friendly, free < 1K), Substack (built-in audience, less API flexibility). Pick one, share the API endpoint + key, and C1 unblocks in 1.5 h.
2. **Video recording** — C4 and C5 need your voice + face. I write the script; you record. No AI can ship this for you.

---

## Deferred bigger bets (not in this plan — mention them so we don't lose them)

- AI companion chat (multi-day; needs API-key strategy)
- Auth / accounts / cross-device progress sync (multi-day; needs backend)
- Community / forum / comments (needs moderation strategy)
- Mock-interview AI voice mode (multi-week)
- Job board integration
- Mobile app (separate project)

These matter — they're what separate a $19 reference from a $99 course from a $399 coaching product. But they're outside the "one sprint" horizon and shouldn't crowd out Track A/B/C decisions today.
