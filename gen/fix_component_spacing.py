"""Fix consecutive Vue component tags by ensuring blank lines between them.

When two block-level Vue component tags (self-closing like <Comp ... />) appear
on adjacent lines with no blank line between, VitePress/markdown-it wraps them
in a <p> and renders them as escaped literal text.

This script scans gen/src/**.md and inserts a blank line between any pair of
consecutive self-closing block tags.
"""
import re
from pathlib import Path

SRC_DIRS = [
    Path(__file__).parent.parent / 'gen' / 'src',
    Path(__file__).parent.parent / 'gen' / 'src' / 'problems',
]

# Component names we've added that are self-closing block tags.
BLOCK_COMPS = [
    'PatternVideo', 'PatternProgress', 'CompanyTags', 'Hints', 'JavaRunner',
    'MarkSolved', 'Bookmark', 'InterviewTimer', 'AiCompanion', 'FeedbackWidget',
    'RelatedProblems', 'RelatedPatterns', 'PrintButton', 'DueForReview',
    'BookmarksList', 'StudyPlanGenerator', 'RoadmapChecklist', 'ProblemStats',
    'StreakTracker', 'UserProfile', 'SocialProof', 'SupportPanel', 'ShareButtons',
    'EmailCapture', 'StorageManager',
]

# Match a self-closing tag on its own line.
LINE_TAG = re.compile(
    r'^(?P<indent>[ \t]*)<(?P<name>' + '|'.join(BLOCK_COMPS) + r')(?P<attrs>\s[^>]*)?/>[ \t]*$'
)


def fix_text(text: str) -> tuple[str, int]:
    """Return (fixed_text, count_of_fixes). Ensures blank line between adjacent block-tag lines."""
    lines = text.split('\n')
    out = []
    fixes = 0
    for i, line in enumerate(lines):
        out.append(line)
        if i + 1 >= len(lines):
            continue
        curr_match = LINE_TAG.match(line)
        next_line = lines[i + 1]
        next_match = LINE_TAG.match(next_line)
        # Also handle case where next line is text starting with `<Comp ... />`
        # even if it doesn't span the full line pattern.
        if curr_match and next_match:
            # Both are block tags; ensure a blank between them.
            out.append('')
            fixes += 1
        elif curr_match and next_line.strip().startswith('<') and any(
            next_line.lstrip().startswith(f'<{c}') for c in BLOCK_COMPS
        ):
            out.append('')
            fixes += 1
    return '\n'.join(out), fixes


def main():
    total_fixes = 0
    files_changed = 0
    for src_dir in SRC_DIRS:
        if not src_dir.exists():
            continue
        for md in src_dir.glob('*.md'):
            text = md.read_text(encoding='utf-8')
            fixed, fixes = fix_text(text)
            if fixes > 0 and fixed != text:
                md.write_text(fixed, encoding='utf-8')
                files_changed += 1
                total_fixes += fixes
    print(f'Fixed {total_fixes} adjacencies across {files_changed} files.')


if __name__ == '__main__':
    main()
