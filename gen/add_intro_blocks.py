"""Ensure every Part II pattern chapter opens with a consistent 4-subsection block:
  ### Recognize by
  ### Why it beats brute force
  ### How it works
  ### When NOT to use it

Where the chapter already has a rich prose intro, that intro remains as the "Why".
This just inserts the missing subsection headings so every chapter has the same
reading rhythm.
"""
import os, re

ROOT = os.path.join(os.path.dirname(__file__), "src")

# per-chapter authored content (filename -> dict with the 4 sections)
INTRO = {
 "23-fast-slow.md": {
   "recognize": [
     "linked-list cycle / \"does this list loop?\"",
     "middle-of-linked-list / nth-from-end",
     "any *functional graph* (each node has one successor) — Happy Number, Find Duplicate",
   ],
   "when_not": (
     "Anything that isn't a single-successor structure. For general graphs (each node has multiple neighbours), use BFS/DFS. For two-pointer *on a sorted array*, "
     "the mechanism is entirely different — that's [Two Pointers](#two-pointers), driven by sortedness, not by a speed differential."
   ),
 },
 "26-monotonic-stack.md": {
   "recognize": [
     "*nearest greater / smaller* element (left or right)",
     "spans, histograms, rectangles bounded by taller / shorter neighbours",
     "\"largest rectangle\", \"trapping rain water\" (stack variant), stock spans, remove-k-digits",
   ],
   "when_not": (
     "You need *farthest* rather than *nearest* — or the comparison isn't a simple ordering. If the \"answer per element\" depends on *aggregating* over a "
     "range instead of picking one boundary, reach for a segment tree or sparse table, not a monotonic stack."
   ),
 },
 "28-bs-on-answer.md": {
   "recognize": [
     "\"minimum X such that…\" / \"maximum X such that…\"",
     "you can *check* a candidate x in linear time but *searching* every x is too slow",
     "phrases like \"minimum capacity to ship in D days\", \"slowest speed to finish\", \"largest minimum gap\"",
   ],
   "when_not": (
     "The feasibility predicate isn't monotone — you can find an x where `feasible(x)` is true but `feasible(x+1)` is false. Then you're not searching a "
     "single flip point; the search space has multiple boundaries and this technique gives the wrong answer."
   ),
 },
 "29-top-k-heap.md": {
   "recognize": [
     "\"k largest / smallest / most frequent\"",
     "\"k closest to origin\", \"kth from data stream\"",
     "you need the k best items but *not* their relative order and *not* the rest of the array sorted",
   ],
   "when_not": (
     "You need the k-th value **once** and don't care about the other k−1 boundary items. **Quickselect** is O(n) average and beats the heap's O(n log k). "
     "Use a heap when the input arrives as a **stream** (you can't Quickselect it) or when you need *all* k boundary items."
   ),
 },
 "30-k-way-merge.md": {
   "recognize": [
     "\"merge k sorted lists / arrays\"",
     "\"smallest range covering elements from k lists\"",
     "\"find k pairs with smallest sums\" (heap of pair candidates)",
   ],
   "when_not": (
     "The k streams aren't sorted individually — a heap over the current fronts is meaningless if the fronts don't represent \"smallest not-yet-emitted\". "
     "Sort each stream first, or use a different approach."
   ),
 },
 "31-merge-intervals.md": {
   "recognize": [
     "*intervals* on a number line — meetings, flights, ranges",
     "\"merge overlapping\", \"insert new interval\", \"non-overlapping intervals\"",
     "the answer needs the intervals themselves (as opposed to just the count of active ones — that's [Sweep Line](#sweep-line))",
   ],
   "when_not": (
     "You need *how many are active at time t?* rather than *which merged into which?* — that's the [Sweep Line](#sweep-line) variant. Also skip this pattern "
     "when intervals live on multiple axes (2-D) — reach for coordinate compression + segment tree."
   ),
 },
 "32-sweep-line.md": {
   "recognize": [
     "*peak concurrency* — \"minimum meeting rooms\"",
     "total coverage / uncovered gap on a number line",
     "\"skyline\" — max height at every x-coordinate (event = building start/end)",
   ],
   "when_not": (
     "You need to *reconstruct which intervals were merged* rather than count activity. Use [Merge Intervals](#merge-intervals) instead. Also, if events arrive "
     "*online* (no chance to sort up front), reach for a TreeMap or segment tree instead of an event-array sweep."
   ),
 },
 "33-topological-sort.md": {
   "recognize": [
     "*directed graph with prerequisites* — \"course schedule\", \"build order\", \"task dependencies\"",
     "\"detect cycle in a DAG\" (cycle iff Kahn's queue empties before emitting all V)",
     "\"alien dictionary\" — infer letter order from ordered word list, then topologically sort",
   ],
   "when_not": (
     "The graph is *undirected* — topological sort is undefined. For \"reach everything from x\" use BFS/DFS. For \"is this graph a DAG?\" use DFS with a 3-colour "
     "visitor. If dependencies come with weights (build times, delays), reach for critical-path DP instead."
   ),
 },
 "34-union-find.md": {
   "recognize": [
     "*dynamic connectivity* — edges arrive over time; answer \"same group?\" as they do",
     "\"count connected components / groups / islands\"",
     "\"redundant connection\" (find the edge that creates a cycle)",
   ],
   "when_not": (
     "You need to *walk* the components (traversal, distances, colouring) — Union-Find only tells you set membership, not adjacency. Also, if you must **remove** "
     "edges (not just add), Union-Find doesn't support that natively — either process events offline in reverse or use link-cut trees."
   ),
 },
 "37-divide-conquer.md": {
   "recognize": [
     "\"solve the halves, combine\" — merge sort family",
     "\"count inversions\" / \"count of smaller after self\" / \"reverse pairs\"",
     "\"closest pair of points\", \"maximum subarray via D&C\" (Kadane's O(n) beats it but D&C teaches the shape)",
   ],
   "when_not": (
     "The two halves *depend on each other* (state flows across the split). Then you can't recurse independently — reach for DP with a state that captures the "
     "cross-half interaction. Also, if the combine step is O(n log n), your total becomes O(n log² n) — check if a single-pass approach exists."
   ),
 },
 "39-trie-pattern.md": {
   "recognize": [
     "*prefix queries against a shared dictionary* — autocomplete, spellcheck, word ladders",
     "*XOR-max* problems (binary trie over bits, greedy walk to the opposite bit)",
     "*wildcard match against many words* — Word Search II combines trie + backtracking",
   ],
   "when_not": (
     "You need suffix matching (not prefix) — use a suffix automaton or reverse the strings and build a prefix trie. Also skip a trie when your \"dictionary\" is "
     "tiny (< ~50 words) — a linear scan is simpler."
   ),
 },
 "41-quickselect.md": {
   "recognize": [
     "\"find the k-th smallest / largest\" — **one-shot** query",
     "median problems where you don't need the sorted array",
     "\"top k\" when you're willing to trade the log-k factor for a linear expected time",
   ],
   "when_not": (
     "You need k-th in a **stream** (no random access) — use a heap. You need the k boundary items in order — use a heap or partial sort. Adversarial inputs "
     "with the same pivot every time degrade to O(n²) — always pick a **random** pivot or use median-of-medians."
   ),
 },
}

TEMPLATE = (
    "### Recognize by\n"
    "{recognize_lines}\n\n"
    "### When NOT to use it\n"
    "{when_not}\n\n"
    "---\n\n"
)

def process_file(fname, info):
    path = os.path.join(ROOT, fname)
    txt = open(path, encoding="utf-8").read()
    # find first H2 boundary (## something)
    m = re.search(r'^## ', txt, re.MULTILINE)
    if not m:
        print(f"  ! no H2 found in {fname}")
        return
    if "### Recognize by" in txt[:m.start()]:
        print(f"  = already has Recognize block: {fname}")
        return
    recognize_lines = "\n".join(f"- {b}" for b in info["recognize"])
    block = TEMPLATE.format(recognize_lines=recognize_lines, when_not=info["when_not"])
    new_txt = txt[:m.start()] + block + txt[m.start():]
    open(path, "w", encoding="utf-8").write(new_txt)
    print(f"  + injected intro block: {fname}")

if __name__ == "__main__":
    for fname, info in INTRO.items():
        process_file(fname, info)
    print(f"\ndone: {len(INTRO)} chapters processed")
