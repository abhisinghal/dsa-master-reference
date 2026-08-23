# Contributing to DSA Master Reference

Thanks for looking under the hood. This document exists because the site grew
organically over 22+ ship rounds and the internal conventions are not obvious
from a first read of the code.

If you touch any of the following areas, please skim the relevant section
below first — it will save you the exact bug I fixed in Round 22 (spoiler:
20 components silently rendered as escaped raw text on 200+ pages because
their names were missing from a hand-maintained regex whitelist).

---

## Repository layout

```
gen/                    Authoring pipeline. Source markdown + Python scripts.
  src/                  The source-of-truth markdown (edit this, not web/docs).
  add_*.py              Idempotent embed scripts (one widget per script).
  fix_*.py              Idempotent normalizer scripts.
  pipeline.py           One-command orchestrator for all the above.
web/                    VitePress site.
  docs/                 VitePress content root (auto-generated from gen/src).
    .vitepress/
      config.mts        Site config, nav, sidebar.
      theme/            68+ Vue components + slot-layout override.
        index.ts        Component registrations + Layout slot mounts.
        lib/storage.ts  The single localStorage wrapper. Use this, never
                        the raw browser API.
        *.vue           Everything else.
  migrate.py            gen/src → docs migrator. Runs KNOWN_HTML escape logic.
  tests/                Playwright smoke suite.
    baseline.smoke.ts   The escaped-tag class of bug is caught here.
.github/workflows/      CI: deploy on push to main, smoke on PR.
```

## How the build actually works

```
gen/src/*.md
    │
    │ gen/pipeline.py (optional; only when regenerating widget embeds)
    ▼
gen/src/*.md          (annotated with <Component /> tags)
    │
    │ web/migrate.py  (escapes prose, preserves code fences,
    │                  auto-derives Vue component whitelist from
    │                  theme/index.ts)
    ▼
web/docs/**/*.md
    │
    │ vitepress build
    ▼
web/docs/.vitepress/dist/**/*.html
    │
    │ deploy.yml
    ▼
GitHub Pages
```

### The critical KNOWN_HTML gotcha

`web/migrate.py` HTML-escapes every `<Tag>` in prose that is *not* in its
`KNOWN_HTML` whitelist, because otherwise Vue trips on things like
`i < n` in prose. Since Round 22, that whitelist is **auto-derived** by
scanning `theme/index.ts` for `app.component('Name', ...)` calls. **You
only need to worry about it if you register a component in some other way.**

If you write a new component, register it via `app.component('MyThing', MyThing)`
in `theme/index.ts` and the migrator will pick it up automatically.

## Adding a new Vue component — 6-step checklist

1. Create `theme/MyThing.vue`.
2. Import + register in `theme/index.ts` via
   `app.component('MyThing', MyThing)`.
3. If it does local persistence, use `../lib/storage.ts` — never
   `localStorage.setItem` directly.
4. If it needs to appear on many pages automatically, write
   `gen/add_my_thing.py` and add it to the ordered `STAGES` list in
   `gen/pipeline.py`.
5. Add a smoke assertion in `web/tests/baseline.smoke.ts` — either extend
   `COMPONENTS_MUST_NOT_ESCAPE` (mandatory) or add a targeted
   `expect(page.locator('.my-thing')).toBeVisible()`.
6. Run locally: `cd web && python migrate.py && npx vitepress build docs`
   then `npm run test:smoke`. Both must be green.

## Adding a new problem page

1. Write `gen/src/problems/NN-<slug>.md` (see any existing problem for the
   canonical 7-section shape).
2. Optionally include `<CompanyTags>`, `<Hints>`, `<MarkSolved>`,
   `<Bookmark>`, `<InterviewTimer>`, `<JavaRunner>`, `<AiCompanion>`,
   `<FeedbackWidget>`, `<RelatedProblems>` embeds — or run
   `python gen/pipeline.py --only add_company_tags add_hints ...` and let
   the embed scripts do it.
3. Rebuild and commit.

## Adding a new chapter page

1. Write `gen/src/NN-<slug>.md`.
2. Add a mapping entry in `web/migrate.py`'s `MAPPING` dict.
3. Add a sidebar entry in `web/docs/.vitepress/config.mts`.
4. Rebuild and commit.

## Code style

- Vue components: prefer `<script setup lang="ts">` and typed `defineProps`.
- Storage access: `import { storage } from '../lib/storage'`, never
  `window.localStorage`.
- New components should be under 300 lines. Extract shared primitives.
- CSS: scoped to the component. Global tokens live in `theme/style.css`
  as `--dsa-*` and `--vp-*` variables.

## Running things locally

```bash
cd web
npm ci                              # install once
python migrate.py                   # regenerate docs/ from gen/src/
npm run docs:dev                    # local dev server with HMR
npm run docs:build                  # production build (~1-2 min)
npm run docs:preview                # serve the built dist
npm run test:smoke                  # Playwright smoke suite (needs preview)
python gen/pipeline.py              # re-run all widget embeds
python gen/pipeline.py --dry-run    # inspect the stage plan
python gen/pipeline.py --only add_hints add_bookmark   # subset
```

## Commits

- Small, single-topic commits.
- Every commit that touches user-visible surface should build cleanly.
- CI runs smoke tests on PRs; passing is required.

## Content authoring

- Source markdown lives in `gen/src/`. Never edit `web/docs/*.md` directly —
  the migrator overwrites those.
- Prose can contain `<` and `>` freely; the migrator escapes them safely.
- Vue components in markdown must be **on their own line**, with a **blank
  line before and after**. `fix_component_spacing.py` will normalize this
  for you, but writing it correctly the first time is cheaper.
- Fenced code blocks (```java, ```text, etc.) are preserved verbatim — put
  raw `<`, `>`, and quotes inside them without escaping.

## Environment variables

Copy `.env.example` to `.env` and fill in only the services you use.
Nothing is required for a local build — every integration has a
localStorage-only fallback.

## What broke last time and why

The story of Round 22 is documented at the top of `web/migrate.py`. TL;DR:
if you add a Vue component and its name isn't in the escape-logic whitelist,
it silently renders as `&lt;YourThing /&gt;` — as text, on every page that
uses it. The whitelist is now auto-derived, but the failure mode still
exists for any component registered outside `theme/index.ts`. A Playwright
smoke test now catches this before merge.
