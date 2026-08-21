<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type NodeId =
  | 'root'
  | 'i1'
  | 'e1'
  | 'i12'
  | 'i1e2'
  | 'e1i2'
  | 'e1e2'
  | 'l123'
  | 'l12'
  | 'l13'
  | 'l1'
  | 'l23'
  | 'l2'
  | 'l3'
  | 'l0'

type TreeNode = { id: NodeId; x: number; y: number; width: number; label: string; leaf?: boolean }
type Edge = { id: string; from: NodeId; to: NodeId; choice: 'include' | 'exclude' }
type Step = { leaf: NodeId; subset: string; path: NodeId[]; undoEdges: string[]; description: string }

const nodes: TreeNode[] = [
  { id: 'root', x: 360, y: 72, width: 50, label: '{}' },
  { id: 'i1', x: 220, y: 118, width: 54, label: '{1}' },
  { id: 'e1', x: 500, y: 118, width: 50, label: '{}' },
  { id: 'i12', x: 130, y: 164, width: 68, label: '{1,2}' },
  { id: 'i1e2', x: 288, y: 164, width: 54, label: '{1}' },
  { id: 'e1i2', x: 432, y: 164, width: 54, label: '{2}' },
  { id: 'e1e2', x: 590, y: 164, width: 50, label: '{}' },
  { id: 'l123', x: 74, y: 216, width: 76, label: '{1,2,3}', leaf: true },
  { id: 'l12', x: 142, y: 216, width: 68, label: '{1,2}', leaf: true },
  { id: 'l13', x: 250, y: 216, width: 68, label: '{1,3}', leaf: true },
  { id: 'l1', x: 318, y: 216, width: 54, label: '{1}', leaf: true },
  { id: 'l23', x: 414, y: 216, width: 68, label: '{2,3}', leaf: true },
  { id: 'l2', x: 482, y: 216, width: 54, label: '{2}', leaf: true },
  { id: 'l3', x: 590, y: 216, width: 54, label: '{3}', leaf: true },
  { id: 'l0', x: 658, y: 216, width: 50, label: '{}', leaf: true }
]

const edges: Edge[] = [
  { id: 'root-i1', from: 'root', to: 'i1', choice: 'include' },
  { id: 'root-e1', from: 'root', to: 'e1', choice: 'exclude' },
  { id: 'i1-i12', from: 'i1', to: 'i12', choice: 'include' },
  { id: 'i1-i1e2', from: 'i1', to: 'i1e2', choice: 'exclude' },
  { id: 'e1-e1i2', from: 'e1', to: 'e1i2', choice: 'include' },
  { id: 'e1-e1e2', from: 'e1', to: 'e1e2', choice: 'exclude' },
  { id: 'i12-l123', from: 'i12', to: 'l123', choice: 'include' },
  { id: 'i12-l12', from: 'i12', to: 'l12', choice: 'exclude' },
  { id: 'i1e2-l13', from: 'i1e2', to: 'l13', choice: 'include' },
  { id: 'i1e2-l1', from: 'i1e2', to: 'l1', choice: 'exclude' },
  { id: 'e1i2-l23', from: 'e1i2', to: 'l23', choice: 'include' },
  { id: 'e1i2-l2', from: 'e1i2', to: 'l2', choice: 'exclude' },
  { id: 'e1e2-l3', from: 'e1e2', to: 'l3', choice: 'include' },
  { id: 'e1e2-l0', from: 'e1e2', to: 'l0', choice: 'exclude' }
]

const steps: Step[] = [
  {
    leaf: 'l123',
    subset: '{1,2,3}',
    path: ['root', 'i1', 'i12', 'l123'],
    undoEdges: [],
    description: 'Include 1, include 2, include 3; record the first leaf.'
  },
  {
    leaf: 'l12',
    subset: '{1,2}',
    path: ['root', 'i1', 'i12', 'l12'],
    undoEdges: ['i12-l123'],
    description: 'Undo choice 3, then exclude it to visit {1,2}.'
  },
  {
    leaf: 'l13',
    subset: '{1,3}',
    path: ['root', 'i1', 'i1e2', 'l13'],
    undoEdges: ['i12-l12', 'i1-i12'],
    description: 'Backtrack from 2, exclude it, then include 3.'
  },
  {
    leaf: 'l1',
    subset: '{1}',
    path: ['root', 'i1', 'i1e2', 'l1'],
    undoEdges: ['i1e2-l13'],
    description: 'Undo 3 to record the sibling subset {1}.'
  },
  {
    leaf: 'l23',
    subset: '{2,3}',
    path: ['root', 'e1', 'e1i2', 'l23'],
    undoEdges: ['i1e2-l1', 'root-i1'],
    description: 'Backtrack past 1, exclude it, then include 2 and 3.'
  },
  {
    leaf: 'l2',
    subset: '{2}',
    path: ['root', 'e1', 'e1i2', 'l2'],
    undoEdges: ['e1i2-l23'],
    description: 'Undo 3 again to visit {2}.'
  },
  {
    leaf: 'l3',
    subset: '{3}',
    path: ['root', 'e1', 'e1e2', 'l3'],
    undoEdges: ['e1i2-l2', 'e1-e1i2'],
    description: 'Backtrack from 2, exclude it, then include 3.'
  },
  {
    leaf: 'l0',
    subset: '{}',
    path: ['root', 'e1', 'e1e2', 'l0'],
    undoEdges: ['e1e2-l3'],
    description: 'Undo 3 and finish with the empty subset.'
  }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const nodeById = computed(() =>
  nodes.reduce(
    (acc, node) => {
      acc[node.id] = node
      return acc
    },
    {} as Record<NodeId, TreeNode>
  )
)

function isPathEdge(edge: Edge) {
  const path = currentStep.value.path
  return path.some((node, index) => node === edge.from && path[index + 1] === edge.to)
}

function edgeClass(edge: Edge) {
  return {
    active: isPathEdge(edge),
    undo: currentStep.value.undoEdges.includes(edge.id),
    include: edge.choice === 'include',
    exclude: edge.choice === 'exclude'
  }
}

function nodeClass(node: TreeNode) {
  return {
    active: currentStep.value.path.includes(node.id),
    leaf: node.leaf,
    current: currentStep.value.leaf === node.id
  }
}

function stop() {
  playing.value = false
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

function next() {
  if (current.value < steps.length - 1) current.value += 1
  else stop()
}

function prev() {
  stop()
  current.value = Math.max(0, current.value - 1)
}

function reset() {
  stop()
  current.value = 0
}

function togglePlay() {
  if (playing.value) {
    stop()
    return
  }
  if (current.value === steps.length - 1) current.value = 0
  playing.value = true
  timer.value = setInterval(next, 1200)
}

onBeforeUnmount(stop)
</script>

<template>
  <div class="anim-card">
    <svg
      class="anim-svg"
      width="720"
      height="330"
      viewBox="0 0 720 330"
      xmlns="http://www.w3.org/2000/svg"
      font-family="Segoe UI, Arial, sans-serif"
      role="img"
      aria-label="Interactive backtracking subset animation"
    >
      <defs>
        <marker id="bt-anim-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#2563eb" />
        </marker>
        <marker id="bt-anim-green" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#16a34a" />
        </marker>
        <marker id="bt-anim-red" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#dc2626" />
        </marker>
        <filter id="bt-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="330" fill="#fbfcfe" />
      <text x="360" y="26" text-anchor="middle" font-size="14" font-weight="700" fill="#0b1220">
        Subsets of [1,2,3]: choose → recurse → undo
      </text>

      <rect x="244" y="42" width="232" height="30" rx="9" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="360" y="62" text-anchor="middle" font-size="13" font-weight="800" fill="#2563eb">
        current subset = {{ currentStep.subset }}
      </text>

      <g class="edges">
        <line
          v-for="edge in edges"
          :key="edge.id"
          :class="edgeClass(edge)"
          :x1="nodeById[edge.from].x"
          :y1="nodeById[edge.from].y + 16"
          :x2="nodeById[edge.to].x"
          :y2="nodeById[edge.to].y - 16"
          :marker-end="edgeClass(edge).undo ? 'url(#bt-anim-red)' : edgeClass(edge).include ? 'url(#bt-anim-green)' : 'url(#bt-anim-blue)'"
        />
      </g>

      <g filter="url(#bt-anim-shadow)" text-anchor="middle" font-weight="700">
        <g v-for="node in nodes" :key="node.id" class="tree-node" :class="nodeClass(node)">
          <rect :x="node.x - node.width / 2" :y="node.y - 15" :width="node.width" height="30" rx="7" />
          <text :x="node.x" :y="node.y + 5" :font-size="node.leaf ? 10.5 : 12">{{ node.label }}</text>
        </g>
      </g>

      <g font-size="10" font-weight="700" text-anchor="middle">
        <text x="286" y="101" fill="#16a34a">include 1</text>
        <text x="435" y="101" fill="#5b6472">exclude 1</text>
        <text x="173" y="148" fill="#16a34a">include 2</text>
        <text x="254" y="148" fill="#5b6472">exclude 2</text>
        <text x="466" y="148" fill="#16a34a">include 2</text>
        <text x="548" y="148" fill="#5b6472">exclude 2</text>
      </g>

      <g v-if="currentStep.undoEdges.length" class="undo-note">
        <path d="M92,252 C128,282 210,286 256,260" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#bt-anim-red)" />
        <text x="210" y="295" text-anchor="middle" font-size="11" font-weight="700" fill="#dc2626">
          undo choice
        </text>
      </g>

      <rect x="82" y="302" width="556" height="22" rx="7" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="360" y="317" text-anchor="middle" font-size="11" font-weight="700" fill="#5b6472">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Backtracking animation controls">
      <button type="button" :disabled="current === 0" @click="prev">◀ Prev</button>
      <button type="button" @click="togglePlay">{{ playing ? '⏸ Pause' : '▶ Play' }}</button>
      <button type="button" :disabled="current === steps.length - 1" @click="next">Next ▶</button>
      <button type="button" @click="reset">⟳ Reset</button>
      <span class="counter">Step {{ current + 1 }} / {{ steps.length }}</span>
    </div>
  </div>
</template>

<style scoped>
.anim-card {
  max-width: 720px;
  margin: 18px 0;
  padding: 12px;
  border: 1px solid #d9dee7;
  border-radius: 10px;
  background: #fbfcfe;
}

.anim-svg {
  display: block;
  width: 100%;
  height: auto;
}

.edges line {
  stroke: #cbd5e1;
  stroke-width: 1.5;
  opacity: 0.75;
  transition:
    opacity 320ms ease,
    stroke 320ms ease,
    stroke-width 320ms ease;
}

.edges line.include.active {
  stroke: #16a34a;
  stroke-width: 2.5;
  opacity: 1;
}

.edges line.exclude.active {
  stroke: #2563eb;
  stroke-width: 2.5;
  opacity: 1;
}

.edges line.undo {
  stroke: #dc2626;
  stroke-dasharray: 6 4;
  stroke-width: 2.5;
  opacity: 0.75;
}

.tree-node rect {
  fill: #f8fafc;
  stroke: #cbd5e1;
  stroke-width: 1.4;
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    transform 320ms ease;
}

.tree-node text {
  fill: #0b1220;
}

.tree-node.active rect {
  fill: #eff6ff;
  stroke: #2563eb;
  stroke-width: 2;
}

.tree-node.current rect {
  fill: #f0fdf4;
  stroke: #16a34a;
  stroke-width: 2.3;
  transform: translateY(-3px);
}

.tree-node.leaf:not(.current) rect {
  fill: #fff;
}

.undo-note {
  transition: opacity 250ms ease;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
}

button {
  border: 1px solid #cbd5e1;
  border-radius: 7px;
  padding: 6px 10px;
  background: #fff;
  color: #0b1220;
  font: 600 13px "Segoe UI", Arial, sans-serif;
  cursor: pointer;
}

button:hover:not(:disabled) {
  border-color: #2563eb;
  color: #2563eb;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.counter {
  margin-left: auto;
  color: #5b6472;
  font: 600 13px "Segoe UI", Arial, sans-serif;
}
</style>
