# history/

Archived artifacts from earlier iterations of this repository. **None of this is used by the live build.** It is kept for provenance — so that a future reader can understand the evolution of the content and the choices behind the current pipeline.

If you are looking for how the project builds today, read [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## What's here

### `legacy-book-pipeline/`

A complete, parallel book-building system that predates the current `gen/src/ → web/migrate.py → VitePress` pipeline. It produced a standalone paged HTML book (`build/book.html`) from a separate, more terse content tree.

- `src/content/*.md` — 43 chapter files in the first-pass format: MkDocs-style `!!! key` admonitions, strict `{"type":"array",…}` JSON diagram specs, no Vue components. Numbering uses `m01…m15` for modules and `p01…p20` for patterns.
- `src/build.py` + `src/manifest.json` — Markdown → paged HTML build harness driven by the manifest's chapter ordering.
- `src/render_pages.py`, `src/gen_master_md.py`, `src/diagrams.py`, `src/gen_index.py` — support scripts for the above.
- `make.ps1` — Windows PowerShell orchestrator for the legacy pipeline. Hardcodes a developer-machine `session-state` path and is not portable.
- `AUTHORING-legacy.md` — the authoring conventions for the legacy format (admonition tags, 20-section problem template, diagram JSON schema).

The current pipeline is documented in [`CONTRIBUTING.md`](../CONTRIBUTING.md); its source of truth lives in `gen/src/` and uses `> [key] **Title** — body` blockquote callouts plus Vue components, which `web/migrate.py` transforms into the final site content.

### `plan-waves-complete-2026-08-28.md`

The completed-waves status document (originally `plan.md` at repo root). Records the eight-wave content refresh and nine-wave problem-page polish that brought all 205 pages to the "reference-bar" quality. Preserved as a historical record of what shipped and why; it is **not** an active plan.

### `plan-practice-page-rollout-2026-08-22.md`

The earlier practice-page rollout snapshot (originally `plan.old.md` at repo root). Captures the session-c960137b scope before the Wave 1-9 refresh; superseded by the waves plan.

## Why archive instead of delete?

Git history would preserve the files regardless, but keeping them in-tree makes the repository's evolution legible without needing `git log --follow`. The authorial decisions (why Vue components, why story-first openings, why one source tree with a migrator) are easier to understand when the earlier approach is still visible to compare against.

If any file here grows load-bearing on a current workflow, it should be promoted back out of `history/` and documented in `CONTRIBUTING.md`.
