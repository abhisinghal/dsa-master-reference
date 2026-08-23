"""Add missing '## When to use which' section to 9 pages identified in audit."""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'

WHEN_TO_USE = {
    '08v-capacity-to-ship-packages-within-d-days.md': """## When to use which

- **"Min feasible X with monotone predicate"** → BS on answer.
- **Return the split itself** → after BS converges, re-simulate to record boundaries.
- **Very large sums** → use `long` for hi bound.
""",
    '08v-divide-chocolate.md': """## When to use which

- **"Max feasible X with monotone predicate"** → BS on answer with `≥ target` check.
- **Return the splits** → re-simulate after convergence.
- **Bounded values** → tight `[lo, hi]` speeds up.
""",
    '08v-find-k-th-smallest-pair-distance.md': """## When to use which

- **"kth-smallest of computable pair metric"** → BS on answer + count-≤ function.
- **All-pair distinct sums** → same idea.
- **Streaming** → not directly applicable — need offline.
""",
    '08v-kth-smallest-element-in-a-sorted-matrix.md': """## When to use which

- **Sorted matrix kth** → BS on value or min-heap merge.
- **BS on value** is cleaner for max n; heap wins for small n.
- **Kth in unsorted** → Quickselect or heap.
""",
    '08v-median-of-two-sorted-arrays.md': """## When to use which

- **"Median of two sorted"** → BS on smaller array (O(log min)).
- **"Median of k sorted"** → heap or divide-and-conquer.
- **"kth of two sorted"** → same BS with different partition target.
""",
    '08v-minimize-max-distance-to-gas-station.md': """## When to use which

- **"Minimize max after k operations"** → BS on real-valued answer.
- **Discrete answer** → integer BS.
- **Precision** → iterate until `hi - lo < 1e-6`.
""",
    '08v-path-with-minimum-effort.md': """## When to use which

- **"Min max edge on path"** → BS on answer OR Dijkstra with max-of-path metric OR MST.
- **Dijkstra variant** — replace sum with max in relaxation.
- **Streaming edge addition** → Union-Find with sorted edges.
""",
    '08v-split-array-largest-sum.md': """## When to use which

- **"Min largest chunk after splitting"** → BS on answer.
- **DP alternative** → interval DP; slower but returns actual partition.
- **Related: max smallest chunk** → similar BS with `≥` predicate.
""",
    '18v-edit-distance.md': """## When to use which

- **Standard edit distance** → 2D DP.
- **Only insertions allowed** → LCS variant.
- **Return the operations** → track parent choices during DP.
""",
}

changed = 0
for name, block in WHEN_TO_USE.items():
    p = SRC / name
    if not p.exists():
        continue
    text = p.read_text(encoding='utf-8')
    if '## When to use' in text:
        continue
    # Insert before "## Related problems"
    if '## Related problems' in text:
        text = text.replace('## Related problems', block + '\n## Related problems', 1)
    else:
        text = text.rstrip() + '\n\n' + block
    p.write_text(text, encoding='utf-8')
    changed += 1
    print(f'  + {name}')
print(f'Updated {changed}')
