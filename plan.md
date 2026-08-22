# DSA Master Reference — Live Plan

Last updated: 2026-08-22 (session c960137b).
Live at https://abhisinghal.github.io/dsa-master-reference/ · Repo `abhisinghal/dsa-master-reference` · Latest commit `d1a7683`.

---

## Session complete — all four priorities shipped ✅

### Priority 1 — Finish in-progress work

- **`c2-rss-changelog`** ✅ — `gen-rss.mjs` wired into VitePress buildStart hook; `dist/rss.xml` (4.2 KB, 3 entries) auto-generated on every build; RSS autodiscovery link in head.
- **`a1-token-audit`** ✅ — swept **715 hardcoded hex colors** across 11 gen/src files into `var(--dsa-*)` tokens. Dark-mode consistency guaranteed across all 49 static SVGs.

### Priority 2 — Full CodeTrace coverage

- **`codetrace-coverage-full`** ✅ — **100% coverage: 87/87 Trace-it callouts** now have an **interactive slider** visualization (up from 12% at start of session).
- **CodeTrace.vue redesign** — was a static comic strip, is now a Play/Prev/Next/Reset interactive slider matching FastSlowAnim's UX per your explicit request.

### Priority 3 — Round out Tier-1

- **`a3-embed-anims`** ✅ — 4 more anim components embedded.
- **`a2-more-stepstrips`** ✅ — marked superseded by CodeTrace (same information density).
- **`a4-landing-screenshots`** ✅ — 3 SVG mockups shipped on landing.

### Priority 4 — System design intro chapter

- **`b2-system-design-intro`** ✅ — new **~30 KB** chapter at `gen/src/45-system-design.md`, live at https://abhisinghal.github.io/dsa-master-reference/system-design/. Covers 7-phase interview cadence, latency numbers, CAP/PACELC, sharding, caching, replication, queues, load balancing, rate limiting, 4 flagship case studies (URL shortener, rate limiter, KV store, news feed), trade-off catalog, interview scripts, 30-day prep plan.

### Bonus infra fixes shipped this session

- `migrate.py` `KNOWN_HTML` regex tightened to allow `>` inside quoted attribute values.
- `migrate.py` `transform_svg_fences` strips blank lines inside inline SVGs (fixes prior 7-hour build hang).
- Sweep script auto-fixed 3 files where apostrophes in note strings closed single-quoted `:steps` attributes.
- Sweep script auto-moved orphaned blockquote continuations into their parent Trace-it note.

---

## Final scorecard

**Todos: 27 done, 1 blocked.**

Only remaining item: `add-email-capture-pdf-gate` — blocked on your Buttondown/ConvertKit signup.

## Deferred bigger bets (not in this plan — kept so we don't lose them)

- AI companion chat (multi-day; API-key strategy)
- Auth / accounts / cross-device progress sync (multi-day; backend)
- Community / forum / comments (moderation strategy)
- Mock-interview AI voice mode (multi-week)
- Job board integration
- Mobile app
- Anti-pattern generator per pattern
- Extended mock transcripts (3 → 15)
- Company tracks (Meta / Google / Amazon annotated lists)
- Behavioural interview prep
