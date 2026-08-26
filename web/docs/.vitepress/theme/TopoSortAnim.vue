<script setup lang="ts">
/**
 * TopoSortAnim.vue — user-driven interactive diagram for Kahn's algorithm.
 *
 * UX: A fixed graph of 6 nodes at fixed positions. User can toggle any edge
 * on / off by clicking. After each edge change:
 *   - indegree table recomputes
 *   - Kahn's algorithm re-runs and produces a topological order (or reports a cycle)
 *   - the visualisation shows the queue state + the emitted order
 *
 * "Step through Kahn" button plays the algorithm one node at a time so the
 * reader can see the queue empty.
 */
import { computed, ref } from 'vue'

interface EdgeKey { from: number; to: number }

const N = 6
const nodes = [
  { id: 0, x: 90,  y: 80  },
  { id: 1, x: 240, y: 60  },
  { id: 2, x: 240, y: 180 },
  { id: 3, x: 390, y: 80  },
  { id: 4, x: 390, y: 200 },
  { id: 5, x: 540, y: 140 }
]

// Adjacency: Set<"from-to"> of directed edges.
const edges = ref<Set<string>>(new Set([
  '0-1', '0-2', '1-3', '2-3', '2-4', '3-5', '4-5'
]))

const edgeKey = (a: number, b: number) => `${a}-${b}`
const hasEdge = (a: number, b: number) => edges.value.has(edgeKey(a, b))

function toggleEdge(from: number, to: number) {
  if (from === to) return
  const k = edgeKey(from, to)
  const next = new Set(edges.value)
  if (next.has(k)) next.delete(k)
  else {
    // Reject if it creates the immediate reverse (a cycle of length 2 is instructive but blocks)
    // Actually — allow all edges. If cycle results, Kahn shows the cycle detection.
    next.add(k)
  }
  edges.value = next
  // Reset step state
  currentStep.value = -1
  autoPlay()
}

// Kahn's algorithm: compute the full sequence of states.
interface State {
  queue: number[]
  emitted: number[]
  indeg: number[]
  poppedNode: number | null
  cycle: boolean
}

const initialState = computed<State>(() => {
  const indeg = new Array(N).fill(0)
  for (const k of edges.value) {
    const [, to] = k.split('-').map(Number)
    indeg[to]++
  }
  const queue = []
  for (let i = 0; i < N; i++) if (indeg[i] === 0) queue.push(i)
  return { queue, emitted: [], indeg, poppedNode: null, cycle: false }
})

const stepStates = computed<State[]>(() => {
  const states: State[] = [
    {
      queue: [...initialState.value.queue],
      emitted: [],
      indeg: [...initialState.value.indeg],
      poppedNode: null,
      cycle: false
    }
  ]

  const indeg = [...initialState.value.indeg]
  const queue = [...initialState.value.queue]
  const emitted: number[] = []

  while (queue.length > 0) {
    const u = queue.shift()!
    emitted.push(u)
    // Snapshot BEFORE relaxing neighbours
    states.push({
      queue: [...queue],
      emitted: [...emitted],
      indeg: [...indeg],
      poppedNode: u,
      cycle: false
    })
    // Relax edges out of u
    for (const k of edges.value) {
      const [from, to] = k.split('-').map(Number)
      if (from === u) {
        indeg[to]--
        if (indeg[to] === 0) queue.push(to)
      }
    }
    // Snapshot AFTER relaxing
    states.push({
      queue: [...queue],
      emitted: [...emitted],
      indeg: [...indeg],
      poppedNode: null,
      cycle: false
    })
  }

  const isCycle = emitted.length < N
  if (isCycle) {
    // Final state with cycle flag
    states.push({
      queue: [],
      emitted: [...emitted],
      indeg: [...indeg],
      poppedNode: null,
      cycle: true
    })
  }
  return states
})

const currentStep = ref(0)
const currentState = computed(() => stepStates.value[currentStep.value] || initialState.value)

let playTimer: ReturnType<typeof setInterval> | null = null

function play() {
  stop()
  currentStep.value = 0
  playTimer = setInterval(() => {
    if (currentStep.value < stepStates.value.length - 1) {
      currentStep.value++
    } else {
      stop()
    }
  }, 900)
}

function stop() {
  if (playTimer) {
    clearInterval(playTimer)
    playTimer = null
  }
}

function autoPlay() {
  currentStep.value = 0
  stop()
}

function stepBack() { stop(); currentStep.value = Math.max(0, currentStep.value - 1) }
function stepFwd()  { stop(); currentStep.value = Math.min(stepStates.value.length - 1, currentStep.value + 1) }
function reset() {
  edges.value = new Set(['0-1', '0-2', '1-3', '2-3', '2-4', '3-5', '4-5'])
  currentStep.value = 0
}

const orderText = computed(() => currentState.value.emitted.join(' → ') || '(empty)')
const queueText = computed(() => currentState.value.queue.join(', ') || '(empty)')

const isEmitted = (id: number) => currentState.value.emitted.includes(id)
const isInQueue = (id: number) => currentState.value.queue.includes(id)
const isPopped  = (id: number) => currentState.value.poppedNode === id
</script>

<template>
  <div class="anim-card">
    <div class="anim-head">
      <h4 class="anim-title">Topological Sort (Kahn) — click an edge to toggle, then step through</h4>
      <p class="anim-hint">
        Click any pair of nodes to add or remove that directed edge. Kahn's algorithm re-runs; step
        through to watch the queue drain. If the graph has a cycle, Kahn stops early and reports it.
      </p>
    </div>

    <svg
      class="anim-svg"
      width="720"
      height="280"
      viewBox="0 0 720 280"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="Topological sort with Kahn's algorithm on 6 nodes"
    >
      <defs>
        <marker id="ts-arrow" markerWidth="10" markerHeight="10" refX="12" refY="3" orient="auto">
          <path d="M0,0 L8,3 L0,6 Z" fill="#64748b" />
        </marker>
        <marker id="ts-arrow-active" markerWidth="10" markerHeight="10" refX="12" refY="3" orient="auto">
          <path d="M0,0 L8,3 L0,6 Z" fill="#2563eb" />
        </marker>
      </defs>

      <!-- Toggleable edge candidates: all node pairs (undirected click, becomes directed low->high) -->
      <!-- We render only the ACTIVE edges as arrows; a small hit-target on the midpoint enables toggle -->
      <g v-for="k in Array.from(edges)" :key="k">
        <template v-for="parts in [k.split('-').map(Number)]" :key="parts.join('-') + '-line'">
          <line
            :x1="nodes[parts[0]].x"
            :y1="nodes[parts[0]].y"
            :x2="nodes[parts[1]].x"
            :y2="nodes[parts[1]].y"
            stroke="#64748b"
            stroke-width="2"
            marker-end="url(#ts-arrow)"
            :class="{ 'edge-active': isPopped(parts[0]) || isEmitted(parts[0]) }"
          />
        </template>
      </g>

      <!-- Nodes -->
      <g v-for="n in nodes" :key="'n' + n.id" @click.stop>
        <circle
          :cx="n.x"
          :cy="n.y"
          r="22"
          :class="[
            'node',
            {
              emitted: isEmitted(n.id),
              queued: isInQueue(n.id) && !isEmitted(n.id),
              popped: isPopped(n.id),
              zero: currentState.indeg[n.id] === 0 && !isEmitted(n.id)
            }
          ]"
        />
        <text :x="n.x" :y="n.y + 5" text-anchor="middle" font-size="15" font-weight="700">{{ n.id }}</text>
        <text :x="n.x" :y="n.y - 32" text-anchor="middle" font-size="10" fill="#64748b">
          indeg = {{ currentState.indeg[n.id] }}
        </text>
      </g>

      <!-- Cycle overlay -->
      <g v-if="currentState.cycle">
        <rect x="20" y="240" width="680" height="30" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="1.4" />
        <text x="360" y="260" text-anchor="middle" font-size="13" font-weight="700" fill="#991b1b">
          Cycle detected — {{ N - currentState.emitted.length }} nodes remain with positive indegree.
        </text>
      </g>
    </svg>

    <!-- Edge toggle matrix -->
    <details class="edge-panel">
      <summary>Toggle edges (click any cell)</summary>
      <table class="edge-matrix" role="grid" aria-label="Edge adjacency matrix">
        <thead>
          <tr>
            <th></th>
            <th v-for="n in nodes" :key="'h' + n.id">{{ n.id }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="from in nodes" :key="'r' + from.id">
            <th>{{ from.id }} →</th>
            <td v-for="to in nodes" :key="'c' + from.id + '-' + to.id">
              <button
                v-if="from.id !== to.id"
                :class="['edge-cell', { on: hasEdge(from.id, to.id) }]"
                :aria-pressed="hasEdge(from.id, to.id)"
                :aria-label="'Edge ' + from.id + ' to ' + to.id"
                @click="toggleEdge(from.id, to.id)"
              />
              <span v-else class="diag">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </details>

    <div class="controls">
      <button class="btn" @click="stepBack" :disabled="currentStep === 0">◀ Prev</button>
      <button class="btn primary" @click="play">▶ Play</button>
      <button class="btn" @click="stepFwd" :disabled="currentStep >= stepStates.length - 1">Next ▶</button>
      <button class="btn" @click="reset">Reset</button>
      <span class="step">Step {{ currentStep + 1 }} / {{ stepStates.length }}</span>
    </div>

    <div class="state-panels">
      <div class="state-panel queue-panel">
        <div class="state-label">Queue</div>
        <div class="state-value">[{{ queueText }}]</div>
      </div>
      <div class="state-panel order-panel">
        <div class="state-label">Emitted order</div>
        <div class="state-value">{{ orderText }}</div>
      </div>
    </div>

    <div class="live" aria-live="polite">
      <template v-if="currentState.cycle">Cycle detected — Kahn stopped early.</template>
      <template v-else-if="currentState.emitted.length === N">Complete: {{ N }} nodes emitted.</template>
      <template v-else>{{ currentState.emitted.length }} / {{ N }} emitted.</template>
    </div>
  </div>
</template>

<style scoped>
.anim-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 16px;
  margin: 20px 0;
}
.anim-head { margin-bottom: 12px; }
.anim-title { margin: 0 0 4px; font-size: 15px; font-weight: 700; color: var(--vp-c-text-1); }
.anim-hint { margin: 0; font-size: 13px; color: var(--vp-c-text-2); }

.anim-svg { display: block; width: 100%; height: auto; max-width: 720px; margin: 8px auto; }

.node {
  fill: var(--vp-c-bg);
  stroke: #94a3b8;
  stroke-width: 1.6;
  transition: fill 0.15s, stroke 0.15s, stroke-width 0.15s;
}
.node.zero { stroke: #16a34a; stroke-width: 2; }
.node.queued { fill: #dbeafe; stroke: #2563eb; stroke-width: 2; }
.node.popped { fill: #fde68a; stroke: #d97706; stroke-width: 2.4; }
.node.emitted { fill: #dcfce7; stroke: #16a34a; stroke-width: 1.6; }

.edge-panel {
  margin-top: 10px;
  padding: 10px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}
.edge-panel summary {
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: var(--vp-c-text-2);
}
.edge-matrix { margin-top: 10px; border-collapse: collapse; font-size: 12px; margin-left: auto; margin-right: auto; }
.edge-matrix th { font-weight: 600; padding: 4px 6px; color: var(--vp-c-text-2); }
.edge-matrix td { padding: 2px; text-align: center; }
.edge-cell {
  width: 26px; height: 26px; border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  cursor: pointer;
}
.edge-cell:hover { border-color: #2563eb; }
.edge-cell.on { background: #2563eb; border-color: #1d4ed8; }
.diag { color: var(--vp-c-text-3); font-size: 12px; }

.controls {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 10px;
  flex-wrap: wrap;
}
.btn {
  padding: 6px 12px; border: 1px solid var(--vp-c-divider); border-radius: 6px;
  background: var(--vp-c-bg); color: var(--vp-c-text-1); font-size: 13px; cursor: pointer;
}
.btn:hover:not(:disabled) { border-color: #2563eb; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn.primary { background: #2563eb; color: white; border-color: #2563eb; }
.btn.primary:hover { background: #1d4ed8; }
.step { margin-left: auto; font-size: 12px; color: var(--vp-c-text-2); font-family: var(--vp-font-family-mono); }

.state-panels {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 10px;
  margin-top: 10px;
}
.state-panel {
  padding: 10px 14px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}
.queue-panel { border-left: 3px solid #2563eb; }
.order-panel { border-left: 3px solid #16a34a; }
.state-label { font-size: 11px; font-weight: 700; color: var(--vp-c-text-2); letter-spacing: 0.02em; text-transform: uppercase; margin-bottom: 4px; }
.state-value { font-size: 14px; font-family: var(--vp-font-family-mono); color: var(--vp-c-text-1); font-weight: 600; }

.live { margin-top: 8px; font-size: 12px; color: var(--vp-c-text-3); text-align: center; }

@media (prefers-reduced-motion: reduce) {
  .node { transition: none; }
}
@media print { .controls, .edge-panel, .live { display: none; } }
</style>
