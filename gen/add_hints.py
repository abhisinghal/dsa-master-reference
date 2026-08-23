"""Add Hints component to every problem page.
Uses pattern-specific hint templates keyed by the pattern number prefix.
Each page gets 3 progressive hints: general → specific → almost-solution.
"""
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / 'gen' / 'src' / 'problems'

# Pattern-keyed hint bank. Keys: 2-digit pattern number.
HINTS_BY_PATTERN = {
    '01': (  # Sliding Window
        "What does a valid window look like here? Define the invariant on the window contents before writing loops.",
        "Grow `right`. When the invariant breaks, shrink `left` until it's restored. Track the best answer inside the valid region.",
        "For counts, maintain a `have`/`need` counter to avoid O(σ) re-comparison at every step."
    ),
    '02': (  # Two Pointers
        "Sort first if the input isn't already ordered. Two pointers rely on monotonicity.",
        "Place one pointer at each end. Move the one whose side is provably suboptimal for the target.",
        "Skip duplicates at both boundaries when emitting results to avoid repeated triplets/pairs."
    ),
    '03': (  # Fast/Slow
        "Two pointers moving at different speeds detect cycles without extra memory.",
        "Slow steps 1, Fast steps 2. If they ever meet, there's a cycle. If Fast hits null, no cycle.",
        "For cycle entry (Floyd's Tortoise): after meeting, reset one pointer to head; walk both at speed 1; meet at entry."
    ),
    '04': (  # Prefix Sum
        "Ask: can I answer `sum(i, j)` in O(1) given a preprocessed structure?",
        "Prefix sums let you compute range sums as `pref[j+1] - pref[i]`. For 'count subarrays with property X on sum', use a hash-map of prefix sums.",
        "For '≥ 2 length' or 'divisible by k' variants, store first occurrence and check remainders."
    ),
    '05': (  # Hashing
        "What can you look up in O(1)? Complement, canonical key, or seen-before?",
        "Map each element to its 'canonical form' — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems.",
        "For 'first duplicate', a `HashSet` and single-pass `add()` is enough."
    ),
    '06': (  # Monotonic Stack
        "What element does each `i` 'see' looking left or right? Nearest greater? Nearest smaller?",
        "Maintain a stack that's monotonic in one direction. When the new element breaks monotonicity, pop and answer for popped items.",
        "Contribution counting: instead of 'for each subarray find X', ask 'for each element, how many subarrays does it contribute to?'"
    ),
    '07': (  # Binary Search
        "The input has a monotonic property somewhere — sorted, or piecewise-sorted.",
        "Use half-open `[lo, hi)` template. Invariant: answer lives in `[lo, hi)` throughout. Return `lo`.",
        "For rotated arrays: one half is always sorted — compare mid with lo (or hi) to detect which side."
    ),
    '08': (  # BS on Answer
        "Can I write a `feasible(x)` check that returns true iff answer ≤ x (or ≥ x)?",
        "If `feasible` is monotonic in x, binary search over the answer space `[lo, hi]`. Range: min possible value to max possible value.",
        "The feasibility check is O(n); total complexity is O(n log range)."
    ),
    '09': (  # Top-K / Heap
        "You need the k largest/smallest. Sort is O(n log n). Can you do O(n log k)?",
        "Maintain a heap of size k. Min-heap → k largest at root candidates; max-heap → k smallest.",
        "For 'k closest' or 'k most frequent', the heap's comparator holds the distance/frequency metric."
    ),
    '10': (  # K-way Merge
        "You have k sorted sequences. Which element is globally next?",
        "Min-heap of size k, one head per list. Pop smallest, emit, push its successor from the same list.",
        "For 'smallest range covering k lists', track max-in-heap; window is [minInHeap, maxSeen]."
    ),
    '11': (  # Merge Intervals
        "Sort by start (or end, depending on the question).",
        "Walk once; each interval either extends the current chunk (overlap) or starts a new one.",
        "For 'insert' or 'intersect', use the same sweep with a merge/intersection rule at overlaps."
    ),
    '12': (  # Sweep Line
        "Turn events into `(time, +1/-1)` pairs. What's the 'active count' or 'max concurrent'?",
        "Sort events by time; break ties consistently (end before start for 'meetings', or vice versa).",
        "Sweep; maintain a running count/set. Max active gives room count; drops give free slots."
    ),
    '13': (  # Topological Sort
        "Directed graph? Prerequisites? You need topological order.",
        "Kahn's BFS: start from nodes with indeg 0; when you pop, decrement neighbors' indeg; add new zeros.",
        "For 'layers/semesters', process one full BFS layer per timestep. For 'unique order?', check queue size ≤ 1 at every step."
    ),
    '14': (  # Union-Find
        "Are you grouping things by shared property? Adjacent lands, same friend circle, connected components?",
        "Union-Find: `find(x)` returns root; `union(a, b)` merges. Path compression + union by rank gives α(n).",
        "For MST (min-cost connect all): Kruskal sorts edges, unions if disjoint, stops at n−1 edges."
    ),
    '15': (  # Greedy
        "Is there a local rule that provably gives global optimum? (Exchange argument.)",
        "Sort by the greedy criterion (deadline / end / cost). Iterate; make the locally best choice.",
        "If greedy fails, DP is likely needed. But prove greedy's correctness before writing it."
    ),
    '16': (  # Backtracking
        "You're exploring a decision tree. What's the state at each depth? What choices are available?",
        "Recursive DFS. On each call: check base case, then for each choice, mutate state, recurse, undo.",
        "Prune aggressively: sort input, skip duplicates at the same depth, and cut branches when partial sum/state exceeds target."
    ),
    '17': (  # Divide & Conquer
        "Can I split the input in half, solve each half, then combine? Combine step is the trick.",
        "Merge sort framework: recurse left, recurse right, then merge with the counting/comparison logic on the boundary.",
        "For count-of-X-across-boundary, two-pointer walk during the merge step."
    ),
    '18': (  # DP
        "What is the state? What are the transitions? What's the base case?",
        "Write recurrence first: `dp[i] = f(dp[i-1], dp[i-2], …)`. Then convert top-down memo → bottom-up table → 1D rolling.",
        "For grid: `dp[i][j] = min/max/sum of neighbors + weight`. For interval: iterate lengths, split by k."
    ),
    '19': (  # Trie
        "Prefix operations? Word set lookups? Autocomplete?",
        "Each node has ≤ σ children (26 for lowercase). Walk char-by-char; create nodes on insert; check `end` flag on search.",
        "For XOR max: binary trie of 32-bit values; walk greedily choosing the opposite bit."
    ),
    '20': (  # Bit Manipulation
        "Is there a bit-level trick? XOR cancels duplicates, `n & (n-1)` clears the lowest bit, `n | (1 << k)` sets bit k.",
        "For subset problems: iterate `mask` from 0 to 2ⁿ−1; bit `i` set means element `i` chosen.",
        "For 'find the unique/missing': XOR the whole array with 0..n; pairs cancel, missing survives."
    ),
    '21': (  # Quickselect
        "You want the k-th element but not the sorted order. Sort is O(n log n) — can you do O(n) average?",
        "Quickselect: pick a pivot, partition, recurse into the side containing index k.",
        "Randomize pivot to avoid O(n²) worst case. Worst-case O(n) via median-of-medians (rarely worth it in interviews)."
    ),
}


def get_pattern_prefix(filename: str) -> str:
    """Extract 2-digit pattern number."""
    m = re.match(r'^(\d{2})', filename)
    return m.group(1) if m else ''


def escape_for_attr(s: str) -> str:
    """Escape a string for use in a HTML double-quoted attribute."""
    return s.replace('"', '&quot;').replace("'", "\u2019").replace('\n', ' ')


def build_hints_block(pattern: str) -> str:
    hints = HINTS_BY_PATTERN.get(pattern)
    if not hints:
        return ''
    h1, h2, h3 = hints
    return (
        f'<Hints\n'
        f'  hint1="{escape_for_attr(h1)}"\n'
        f'  hint2="{escape_for_attr(h2)}"\n'
        f'  hint3="{escape_for_attr(h3)}"\n'
        f'/>\n'
    )


def process_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    if '<Hints' in text:
        return False
    pattern = get_pattern_prefix(path.name)
    if not pattern:
        return False
    block = build_hints_block(pattern)
    if not block:
        return False
    # Insert AFTER the constraints line (or after examples if no constraints), BEFORE the first `---`.
    # Strategy: find first `---` separator; insert block above it with blank spacing.
    idx = text.find('\n---\n')
    if idx < 0:
        return False
    new_text = text[:idx + 1] + '\n' + block + text[idx + 1:]
    path.write_text(new_text, encoding='utf-8')
    return True


def main():
    changed = 0
    skipped = 0
    for md in sorted(SRC.iterdir()):
        if md.suffix != '.md' or md.name == '00-index.md':
            continue
        try:
            if process_file(md):
                changed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f'  ! {md.name}: {e}')
    print(f'Added Hints to {changed} pages; skipped {skipped}.')


if __name__ == '__main__':
    main()
