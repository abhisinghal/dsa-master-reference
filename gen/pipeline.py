#!/usr/bin/env python3
"""
gen/pipeline.py — one-command rebuild of `gen/src/` from scratch.

Runs every idempotent embed / fix / upgrade script in the correct order.
Each script must be safely re-runnable (skip work that is already done);
this orchestrator does not manage state, it just enforces order and
gives operators a single entry point.

Usage:
    python gen/pipeline.py             # run every stage in order
    python gen/pipeline.py --dry-run   # print the plan, don't execute
    python gen/pipeline.py --only fix_component_spacing add_hints
                                       # run only the named stages

Stages are grouped by concern. Ordering rules:
    1. Structural fixes and section additions come first, because later
       widget-embed scripts locate anchors like `<CompanyTags>` or
       `<MarkSolved>` to insert relative to.
    2. Per-page widget embeds come next (Hints, CompanyTags, Bookmark,
       InterviewTimer, MarkSolved, JavaRunner, FeedbackWidget, AiCompanion,
       RelatedProblems).
    3. Chapter-level widget embeds after (PatternProgress, PatternVideo,
       PrintButton, RelatedPatterns).
    4. Cleanup / spacing fixes last.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

GEN_DIR = Path(__file__).parent


# Ordered list of stages. Each entry is (script_name, one-line description).
STAGES: list[tuple[str, str]] = [
    # --- Structural fixes ---
    ('add_when_to_use.py',         'Ensure every pattern chapter has a When-to-use section.'),
    ('add_missing_sections.py',    'Ensure every problem page has Brute/Better/Optimized sections.'),
    ('add_difficulty_badges.py',   'Add Easy/Medium/Hard badges to every problem H2.'),
    ('upgrade_problem_pages.py',   'Bring older problem pages up to the current 7-section layout.'),

    # --- Per-problem widgets ---
    ('add_company_tags.py',        'Curated company tags on 194 problem pages.'),
    ('add_hints.py',               'Progressive 3-hint reveal on every problem.'),
    ('add_marksolved_and_storage.py', 'Mark-solved buttons + storage manager on Roadmap.'),
    ('add_bookmark.py',            'Bookmark pill next to Mark Solved.'),
    ('add_interview_timer.py',     'Interview timer collapsible on every problem.'),
    ('add_java_runner.py',         'CheerpJ Java runner tag on every problem.'),
    ('add_feedback.py',            'Thumbs up/down feedback widget on every problem.'),
    ('add_video_and_ai.py',        'PatternVideo (chapters) + AiCompanion (problems).'),
    ('add_related_problems.py',    'Related-problems widget on every problem.'),
    ('add_codetrace.py',           'CodeTrace step-strip embeds where the source markers exist.'),
    ('embed_progress_check.py',    'Progress-check H3 anchors for the sidebar generator.'),
    ('add_example_previews.py',    'ExamplePreview compact input/output blocks.'),

    # --- Per-chapter widgets ---
    ('add_pattern_progress.py',    'Per-pattern progress bar at top of chapters.'),
    ('add_pattern_quizzes.py',     '5-question quiz at end of every chapter.'),
    ('add_related_patterns.py',    'Related-patterns recommender at end of chapters.'),
    ('add_print_button.py',        'Print-chapter button on chapter pages.'),

    # --- Cleanup / correctness ---
    ('fix_component_spacing.py',   'Ensure blank lines between consecutive component tags.'),
    ('strip_example_previews.py',  'Remove ExamplePreview tags with malformed nested quotes.'),
]


def run_stage(name: str, description: str, *, dry_run: bool) -> bool:
    """Run a single stage. Returns True on success (or dry-run)."""
    script = GEN_DIR / name
    if not script.exists():
        print(f'  SKIP  {name:34}  (file not found)')
        return True
    print(f'  RUN   {name:34}  {description}')
    if dry_run:
        return True
    started = time.monotonic()
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(GEN_DIR),
    )
    elapsed = time.monotonic() - started
    if result.returncode != 0:
        print(f'        FAILED after {elapsed:.1f}s. stderr:')
        for line in result.stderr.strip().splitlines()[-10:]:
            print(f'          {line}')
        return False
    # Print only the LAST line of stdout as a summary (each script prints
    # a one-line result like `Added Bookmark to 205/206 problem pages.`).
    tail = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else '(no output)'
    print(f'        {tail}  [{elapsed:.1f}s]')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true',
                        help='Print the plan without executing.')
    parser.add_argument('--only', nargs='*',
                        help='Run only the named scripts (without .py).')
    args = parser.parse_args()

    stages = STAGES
    if args.only:
        wanted = {name if name.endswith('.py') else name + '.py' for name in args.only}
        stages = [s for s in STAGES if s[0] in wanted]
        missing = wanted - {s[0] for s in stages}
        if missing:
            print(f'ERROR: no such stage(s): {sorted(missing)}', file=sys.stderr)
            return 2

    total = len(stages)
    print(f'gen/pipeline.py — {total} stages{" (dry-run)" if args.dry_run else ""}')
    print()
    failures = 0
    started = time.monotonic()
    for i, (name, description) in enumerate(stages, 1):
        print(f'[{i:2}/{total}]')
        if not run_stage(name, description, dry_run=args.dry_run):
            failures += 1
    elapsed = time.monotonic() - started
    print()
    if failures:
        print(f'FAILED: {failures} stage(s) failed after {elapsed:.1f}s')
        return 1
    print(f'OK: all {total} stages complete in {elapsed:.1f}s')
    return 0


if __name__ == '__main__':
    sys.exit(main())
