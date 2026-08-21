<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type NodeId = 'root' | 'left' | 'right' | 'l0' | 'l1' | 'r0' | 'r1' | 'r10' | 'r11'
type TreeNode = { id: NodeId; x: number; y: number; width: number; label: string }
type Edge = { from: NodeId; to: NodeId }
type Step = {
  active: NodeId[]
  solved: NodeId[]
  labels: Partial<Record<NodeId, string>>
  direction: 'down' | 'up'
  description: string
}

const nodes: TreeNode[] = [
  { id: 'root', x: 360, y: 48, width: 144, label: '[3,1,4,1,5]' },
  { id: 'left', x: 220, y: 100, width: 86, label: '[3,1]' },
  { id: 'right', x: 500, y: 100, width: 104, label: '[4,1,5]' },
  { id: 'l0', x: 160, y: 154, width: 46, label: '[3]' },
  { id: 'l1', x: 280, y: 154, width: 46, label: '[1]' },
  { id: 'r0', x: 432, y: 154, width: 46, label: '[4]' },
  { id: 'r1', x: 570, y: 154, width: 76, label: '[1,5]' },
  { id: 'r10', x: 535, y: 208, width: 46, label: '[1]' },
  { id: 'r11', x: 625, y: 208, width: 46, label: '[5]' }
]

const edges: Edge[] = [
  { from: 'root', to: 'left' },
  { from: 'root', to: 'right' },
  { from: 'left', to: 'l0' },
  { from: 'left', to: 'l1' },
  { from: 'right', to: 'r0' },
  { from: 'right', to: 'r1' },
  { from: 'r1', to: 'r10' },
  { from: 'r1', to: 'r11' }
]

const steps: Step[] = [
  { active: ['root'], solved: [], labels: {}, direction: 'down', description: 'Split the full array into left and right halves.' },
  { active: ['left', 'right'], solved: [], labels: {}, direction: 'down', description: 'Recursively split each half.' },
  {
    active: ['l0', 'l1', 'r0', 'r10', 'r11'],
    solved: ['l0', 'l1', 'r0', 'r10', 'r11'],
    labels: {},
    direction: 'down',
    description: 'Base cases: every leaf is already sorted.'
  },
  {
    active: ['left', 'r1'],
    solved: ['l0', 'l1', 'r0', 'r10', 'r11', 'left', 'r1'],
    labels: { left: '[1,3]', r1: '[1,5]' },
    direction: 'up',
    description: 'Merge leaf pairs: [3]+[1] → [1,3] and [1]+[5] → [1,5].'
  },
  {
    active: ['right'],
    solved: ['l0', 'l1', 'r0', 'r10', 'r11', 'left', 'r1', 'right'],
    labels: { left: '[1,3]', r1: '[1,5]', right: '[1,4,5]' },
    direction: 'up',
    description: 'Merge [4] with [1,5] to form sorted right half [1,4,5].'
  },
  {
    active: ['root'],
    solved: ['l0', 'l1', 'r0', 'r10', 'r11', 'left', 'r1', 'right', 'root'],
    labels: { left: '[1,3]', r1: '[1,5]', right: '[1,4,5]', root: '[1,1,3,4,5]' },
    direction: 'up',
    description: 'Final merge combines sorted halves into [1,1,3,4,5].'
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

function labelFor(node: TreeNode) {
  return currentStep.value.labels[node.id] ?? node.label
}

function nodeClass(node: TreeNode) {
  return {
    active: currentStep.value.active.includes(node.id),
    solved: currentStep.value.solved.includes(node.id),
    root: node.id === 'root'
  }
}

function edgeClass(edge: Edge) {
  const step = currentStep.value
  return {
    active: step.active.includes(edge.from) || step.active.includes(edge.to),
    solved: step.solved.includes(edge.from) && step.solved.includes(edge.to),
    upward: step.direction === 'up'
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
      height="315"
      viewBox="0 0 720 315"
      xmlns="http://www.w3.org/2000/svg"
      font-family="Segoe UI, Arial, sans-serif"
      role="img"
      aria-label="Interactive divide and conquer merge sort animation"
    >
      <defs>
        <marker id="dc-anim-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#2563eb" />
        </marker>
        <marker id="dc-anim-green" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#16a34a" />
        </marker>
        <filter id="dc-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="315" fill="#fbfcfe" />
      <text x="360" y="26" text-anchor="middle" font-size="14" font-weight="700" fill="#0b1220">
        Merge sort: split down, merge up
      </text>

      <g class="edges">
        <line
          v-for="edge in edges"
          :key="`${edge.from}-${edge.to}`"
          :class="edgeClass(edge)"
          :x1="nodeById[edge.from].x"
          :y1="nodeById[edge.from].y + 17"
          :x2="nodeById[edge.to].x"
          :y2="nodeById[edge.to].y - 17"
          :marker-end="edgeClass(edge).solved ? 'url(#dc-anim-green)' : 'url(#dc-anim-blue)'"
        />
      </g>

      <g filter="url(#dc-anim-shadow)" text-anchor="middle" font-weight="700">
        <g v-for="node in nodes" :key="node.id" class="tree-node" :class="nodeClass(node)">
          <rect :x="node.x - node.width / 2" :y="node.y - 17" :width="node.width" height="34" rx="7" />
          <text :x="node.x" :y="node.y + 5" font-size="12">{{ labelFor(node) }}</text>
        </g>
      </g>

      <rect x="42" y="244" width="166" height="40" rx="9" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="125" y="260" text-anchor="middle" font-size="11" font-weight="700" fill="#5b6472">
        current direction
      </text>
      <text x="125" y="277" text-anchor="middle" font-size="13" font-weight="800" :fill="currentStep.direction === 'down' ? '#2563eb' : '#16a34a'">
        {{ currentStep.direction === 'down' ? 'split ↓' : 'merge ↑' }}
      </text>

      <rect x="250" y="244" width="420" height="40" rx="9" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="460" y="268" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Divide and conquer animation controls">
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
  stroke-width: 1.6;
  transition:
    opacity 320ms ease,
    stroke 320ms ease,
    stroke-width 320ms ease;
}

.edges line.active {
  stroke: #2563eb;
  stroke-width: 2.4;
}

.edges line.solved {
  stroke: #16a34a;
}

.edges line.upward {
  stroke-dasharray: 5 4;
}

.tree-node rect {
  fill: #f8fafc;
  stroke: #cbd5e1;
  stroke-width: 1.5;
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    transform 320ms ease;
}

.tree-node text {
  fill: #0b1220;
}

.tree-node.root rect {
  fill: #eff6ff;
  stroke: #93c5fd;
}

.tree-node.solved rect {
  fill: #f0fdf4;
  stroke: #16a34a;
}

.tree-node.active rect {
  fill: #eff6ff;
  stroke: #2563eb;
  stroke-width: 2.3;
  transform: translateY(-3px);
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
