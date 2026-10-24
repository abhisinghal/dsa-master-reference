<script setup lang="ts">
import { ref, computed } from 'vue'
import { withBase } from 'vitepress'

// A node is one chapter (foundation / data structure / pattern).
// `tier` controls the vertical band (0 = top, 5 = bottom); `col` controls
// horizontal position within that band. All coordinates are hand-placed so
// the drawing reads top-to-bottom like a learning path.
type Kind = 'foundation' | 'ds' | 'pattern' | 'advanced'
interface Node {
  id: string
  label: string
  href: string
  kind: Kind
  tier: number
  col: number
  prereqs: string[]
}

const NODES: Node[] = [
  // Tier 0 — the two foundations everything leans on
  { id: 'complexity',       label: 'Complexity',          href: '/foundations/complexity',           kind: 'foundation', tier: 0, col: 2, prereqs: [] },
  { id: 'java-primer',      label: 'Java Primer',         href: '/foundations/java-primer',          kind: 'foundation', tier: 0, col: 5, prereqs: [] },

  // Tier 1 — core data structures you can build everything else from
  { id: 'arrays',           label: 'Arrays',              href: '/data-structures/arrays',           kind: 'ds',         tier: 1, col: 0, prereqs: ['java-primer'] },
  { id: 'strings',          label: 'Strings',             href: '/data-structures/strings',          kind: 'ds',         tier: 1, col: 1.5, prereqs: ['arrays'] },
  { id: 'linked-lists',     label: 'Linked Lists',        href: '/data-structures/linked-lists',     kind: 'ds',         tier: 1, col: 3, prereqs: ['java-primer'] },
  { id: 'hashing',          label: 'Hashing',             href: '/patterns/hashing',                 kind: 'ds',         tier: 1, col: 4.5, prereqs: ['arrays'] },
  { id: 'stacks-queues',    label: 'Stacks & Queues',     href: '/data-structures/stacks-queues',    kind: 'ds',         tier: 1, col: 6, prereqs: ['arrays'] },
  { id: 'bit-manip',        label: 'Bit Manipulation',    href: '/patterns/bit-manip',               kind: 'ds',         tier: 1, col: 7.5, prereqs: ['java-primer'] },

  // Tier 2 — fundamental patterns on top of arrays / strings / lists
  { id: 'two-pointers',     label: 'Two Pointers',        href: '/patterns/two-pointers',            kind: 'pattern',    tier: 2, col: 0, prereqs: ['arrays'] },
  { id: 'sliding-window',   label: 'Sliding Window',      href: '/patterns/sliding-window',          kind: 'pattern',    tier: 2, col: 1.3, prereqs: ['arrays', 'two-pointers'] },
  { id: 'prefix-sum',       label: 'Prefix Sum',          href: '/patterns/prefix-sum',              kind: 'pattern',    tier: 2, col: 2.6, prereqs: ['arrays'] },
  { id: 'binary-search',    label: 'Binary Search',       href: '/patterns/binary-search',           kind: 'pattern',    tier: 2, col: 3.9, prereqs: ['arrays', 'complexity'] },
  { id: 'bs-on-answer',     label: 'BS on Answer',        href: '/patterns/bs-on-answer',            kind: 'pattern',    tier: 2, col: 5.2, prereqs: ['binary-search'] },
  { id: 'fast-slow',        label: 'Fast / Slow',         href: '/patterns/fast-slow',               kind: 'pattern',    tier: 2, col: 6.5, prereqs: ['linked-lists', 'two-pointers'] },
  { id: 'monotonic-stack',  label: 'Monotonic Stack',     href: '/patterns/monotonic-stack',         kind: 'pattern',    tier: 2, col: 7.8, prereqs: ['stacks-queues'] },

  // Tier 3 — compound data structures (built on tier 1)
  { id: 'trees',            label: 'Trees',               href: '/data-structures/trees',            kind: 'ds',         tier: 3, col: 1, prereqs: ['linked-lists'] },
  { id: 'heaps',            label: 'Heaps',               href: '/data-structures/heaps',            kind: 'ds',         tier: 3, col: 2.6, prereqs: ['arrays', 'trees'] },
  { id: 'trie',             label: 'Trie',                href: '/data-structures/trie',             kind: 'ds',         tier: 3, col: 4.2, prereqs: ['trees', 'strings'] },
  { id: 'graphs',           label: 'Graphs',              href: '/data-structures/graphs',           kind: 'ds',         tier: 3, col: 5.8, prereqs: ['linked-lists', 'hashing'] },
  { id: 'segment-fenwick',  label: 'Segment / Fenwick',   href: '/data-structures/segment-fenwick',  kind: 'ds',         tier: 3, col: 7.4, prereqs: ['trees', 'arrays'] },

  // Tier 4 — mid-level patterns that depend on tier 3 structures
  { id: 'merge-intervals',  label: 'Merge Intervals',     href: '/patterns/merge-intervals',         kind: 'pattern',    tier: 4, col: 0, prereqs: ['arrays'] },
  { id: 'sweep-line',       label: 'Sweep Line',          href: '/patterns/sweep-line',              kind: 'pattern',    tier: 4, col: 1.3, prereqs: ['merge-intervals', 'heaps'] },
  { id: 'top-k-heap',       label: 'Top-K / Heap',        href: '/patterns/top-k-heap',              kind: 'pattern',    tier: 4, col: 2.6, prereqs: ['heaps'] },
  { id: 'k-way-merge',      label: 'K-Way Merge',         href: '/patterns/k-way-merge',             kind: 'pattern',    tier: 4, col: 3.9, prereqs: ['heaps'] },
  { id: 'quickselect',      label: 'Quickselect',         href: '/patterns/quickselect',             kind: 'pattern',    tier: 4, col: 5.2, prereqs: ['arrays'] },
  { id: 'trie-pattern',     label: 'Trie Pattern',        href: '/patterns/trie-pattern',            kind: 'pattern',    tier: 4, col: 6.5, prereqs: ['trie'] },
  { id: 'greedy',           label: 'Greedy',              href: '/patterns/greedy',                  kind: 'pattern',    tier: 4, col: 7.8, prereqs: ['complexity'] },

  // Tier 5 — graph + recursion patterns, plus divide & conquer
  { id: 'topological-sort', label: 'Topological Sort',    href: '/patterns/topological-sort',        kind: 'pattern',    tier: 5, col: 0, prereqs: ['graphs'] },
  { id: 'union-find',       label: 'Union Find',          href: '/patterns/union-find',              kind: 'pattern',    tier: 5, col: 1.3, prereqs: ['arrays', 'graphs'] },
  { id: 'backtracking',     label: 'Backtracking',        href: '/patterns/backtracking',            kind: 'pattern',    tier: 5, col: 2.6, prereqs: ['trees'] },
  { id: 'divide-conquer',   label: 'Divide & Conquer',    href: '/patterns/divide-conquer',          kind: 'pattern',    tier: 5, col: 3.9, prereqs: ['complexity'] },
  { id: 'math',             label: 'Math',                href: '/patterns/math',                    kind: 'pattern',    tier: 5, col: 5.2, prereqs: ['bit-manip'] },

  // Tier 6 — the hardest surfaces: DP and the design chapter
  { id: 'dp',               label: 'Dynamic Programming', href: '/patterns/dp',                      kind: 'advanced',   tier: 6, col: 2.6, prereqs: ['backtracking', 'divide-conquer'] },
  { id: 'design',           label: 'Design',              href: '/patterns/design',                  kind: 'advanced',   tier: 6, col: 5.2, prereqs: ['hashing', 'linked-lists', 'heaps'] },
]

// Index for O(1) lookup
const BY_ID = new Map(NODES.map(n => [n.id, n]))

// Grid geometry — one coordinate frame; viewBox uses it directly.
const COL_W = 150
const ROW_H = 110
const PAD_X = 40
const PAD_Y = 30
const NODE_W = 128
const NODE_H = 56
const WIDTH = 9 * COL_W + 2 * PAD_X
const HEIGHT = 7 * ROW_H + 2 * PAD_Y

function nodeX(n: Node): number {
  return PAD_X + n.col * COL_W + (COL_W - NODE_W) / 2
}
function nodeY(n: Node): number {
  return PAD_Y + n.tier * ROW_H
}
function nodeCX(n: Node): number { return nodeX(n) + NODE_W / 2 }
function nodeCY(n: Node): number { return nodeY(n) + NODE_H / 2 }

const hovered = ref<string | null>(null)

// All ancestors of a node (its prereqs transitively).
function ancestors(id: string): Set<string> {
  const out = new Set<string>()
  const stack: string[] = [id]
  while (stack.length) {
    const curr = stack.pop()!
    const node = BY_ID.get(curr)
    if (!node) continue
    for (const p of node.prereqs) {
      if (!out.has(p)) { out.add(p); stack.push(p) }
    }
  }
  return out
}

const highlightSet = computed(() => {
  if (!hovered.value) return null
  const set = ancestors(hovered.value)
  set.add(hovered.value)
  return set
})

function isLit(id: string): boolean {
  if (!highlightSet.value) return true
  return highlightSet.value.has(id)
}

function edgeLit(fromId: string, toId: string): boolean {
  if (!highlightSet.value) return true
  return highlightSet.value.has(fromId) && highlightSet.value.has(toId)
}

// Flatten (from, to) edges — one edge per prereq relationship.
const EDGES = NODES.flatMap(n => n.prereqs.map(p => ({ from: p, to: n.id })))

function colorForKind(k: Kind): string {
  switch (k) {
    case 'foundation': return 'var(--dsa-neutral-soft, #e2e8f0)'
    case 'ds':         return 'var(--dsa-info-soft, #dbeafe)'
    case 'pattern':    return 'var(--dsa-primary-soft, #e0e7ff)'
    case 'advanced':   return 'var(--dsa-warning-soft, #fef3c7)'
  }
}
function strokeForKind(k: Kind): string {
  switch (k) {
    case 'foundation': return 'var(--dsa-neutral-line, #94a3b8)'
    case 'ds':         return 'var(--dsa-info, #2563eb)'
    case 'pattern':    return 'var(--dsa-primary, #4f46e5)'
    case 'advanced':   return 'var(--dsa-warning, #d97706)'
  }
}
</script>

<template>
  <figure class="prereq-graph">
    <figcaption class="prereq-caption">
      <strong>How the chapters depend on each other.</strong>
      Hover a chapter to light up every prerequisite that leads to it.
      Click any chapter to open it.
    </figcaption>

    <div class="prereq-legend">
      <span><i class="sw foundation"></i> Foundation</span>
      <span><i class="sw ds"></i> Data Structure</span>
      <span><i class="sw pattern"></i> Pattern</span>
      <span><i class="sw advanced"></i> Advanced</span>
    </div>

    <div class="prereq-svg-wrap">
      <svg
        :viewBox="`0 0 ${WIDTH} ${HEIGHT}`"
        preserveAspectRatio="xMidYMid meet"
        role="img"
        aria-label="Prerequisite dependency graph of all chapters"
      >
        <!-- Arrowhead marker -->
        <defs>
          <marker id="prereq-arrow" viewBox="0 0 10 10" refX="9" refY="5"
                  markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
          </marker>
        </defs>

        <!-- Edges first so nodes sit on top -->
        <g class="edges" stroke-linecap="round">
          <line
            v-for="e in EDGES"
            :key="`${e.from}->${e.to}`"
            :x1="nodeCX(BY_ID.get(e.from)!)"
            :y1="nodeY(BY_ID.get(e.from)!) + NODE_H"
            :x2="nodeCX(BY_ID.get(e.to)!)"
            :y2="nodeY(BY_ID.get(e.to)!)"
            :class="{ dim: !edgeLit(e.from, e.to), lit: edgeLit(e.from, e.to) && hovered !== null }"
            marker-end="url(#prereq-arrow)"
          />
        </g>

        <!-- Nodes -->
        <g class="nodes">
          <a
            v-for="n in NODES"
            :key="n.id"
            :href="withBase(n.href)"
            @mouseenter="hovered = n.id"
            @mouseleave="hovered = null"
            @focus="hovered = n.id"
            @blur="hovered = null"
          >
            <rect
              :x="nodeX(n)"
              :y="nodeY(n)"
              :width="NODE_W"
              :height="NODE_H"
              rx="10"
              :fill="colorForKind(n.kind)"
              :stroke="strokeForKind(n.kind)"
              stroke-width="1.6"
              :class="{ dim: !isLit(n.id), lit: isLit(n.id) && hovered !== null }"
            />
            <text
              :x="nodeCX(n)"
              :y="nodeCY(n) + 4"
              text-anchor="middle"
              font-size="13"
              font-weight="600"
              :class="{ dim: !isLit(n.id) }"
            >{{ n.label }}</text>
          </a>
        </g>
      </svg>
    </div>
  </figure>
</template>

<style scoped>
.prereq-graph {
  margin: 1.5rem 0;
}
.prereq-caption {
  font-size: 0.95rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.75rem;
}
.prereq-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.75rem;
}
.prereq-legend .sw {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 3px;
  margin-right: 0.3rem;
  vertical-align: -2px;
  border: 1px solid var(--vp-c-divider);
}
.prereq-legend .sw.foundation { background: var(--dsa-neutral-soft, #e2e8f0); }
.prereq-legend .sw.ds         { background: var(--dsa-info-soft, #dbeafe); }
.prereq-legend .sw.pattern    { background: var(--dsa-primary-soft, #e0e7ff); }
.prereq-legend .sw.advanced   { background: var(--dsa-warning-soft, #fef3c7); }

.prereq-svg-wrap {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 0.5rem;
  background: var(--vp-c-bg-soft);
}
.prereq-svg-wrap svg {
  width: 100%;
  height: auto;
  min-width: 760px; /* keeps labels readable on phones; wrapper scrolls */
  display: block;
}

/* Edges */
.edges line {
  stroke: var(--vp-c-text-3);
  stroke-width: 1.4;
  color: var(--vp-c-text-3);   /* for marker fill (currentColor) */
  transition: opacity 160ms ease, stroke 160ms ease;
}
.edges line.dim { opacity: 0.14; }
.edges line.lit {
  stroke: var(--vp-c-brand-1, #4f46e5);
  color: var(--vp-c-brand-1, #4f46e5);
  stroke-width: 2;
}

/* Nodes */
.nodes a { cursor: pointer; }
.nodes rect {
  transition: opacity 160ms ease, stroke-width 160ms ease, filter 160ms ease;
}
.nodes rect.dim  { opacity: 0.3; }
.nodes rect.lit  { stroke-width: 2.4; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.15)); }
.nodes text {
  fill: var(--vp-c-text-1);
  pointer-events: none;
  transition: opacity 160ms ease;
}
.nodes text.dim { opacity: 0.35; }
.nodes a:hover rect:not(.dim) { stroke-width: 2.4; }
.nodes a:focus-visible { outline: 2px solid var(--vp-c-brand-1, #4f46e5); outline-offset: 2px; }

/* Dark-mode-friendly tweak: boost edge contrast a touch */
.dark .edges line { stroke: var(--vp-c-text-2); color: var(--vp-c-text-2); }
.dark .edges line.dim { opacity: 0.18; }
</style>
