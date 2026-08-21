<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type NodeId = 'a' | 'b' | 'c' | 'd' | 'root'
type CompressibleNode = Exclude<NodeId, 'root'>
type Step = {
  visiting: NodeId | null
  compressed: CompressibleNode[]
  description: string
}

const nodes: Record<NodeId, { x: number; y: number; label: string }> = {
  a: { x: 92, y: 170, label: 'a' },
  b: { x: 198, y: 130, label: 'b' },
  c: { x: 304, y: 98, label: 'c' },
  d: { x: 410, y: 78, label: 'd' },
  root: { x: 552, y: 78, label: 'root' }
}

const chainParent: Record<CompressibleNode, NodeId> = {
  a: 'b',
  b: 'c',
  c: 'd',
  d: 'root'
}

const steps: Step[] = [
  { visiting: null, compressed: [], description: 'Initial tree: a → b → c → d → root.' },
  { visiting: 'a', compressed: [], description: 'Run find(a): start at a.' },
  { visiting: 'b', compressed: [], description: 'Follow parent[a] to b.' },
  { visiting: 'c', compressed: [], description: 'Follow parent[b] to c.' },
  { visiting: 'd', compressed: [], description: 'Follow parent[c] to d.' },
  { visiting: 'root', compressed: [], description: 'Reach the representative root.' },
  { visiting: 'd', compressed: ['d'], description: 'Return trip: confirm d points directly to root.' },
  { visiting: 'c', compressed: ['d', 'c'], description: 'Compress c so parent[c] = root.' },
  { visiting: 'b', compressed: ['d', 'c', 'b'], description: 'Compress b so parent[b] = root.' },
  { visiting: 'a', compressed: ['d', 'c', 'b', 'a'], description: 'Compress a so parent[a] = root. Future finds are flat.' }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const findPath: NodeId[] = ['a', 'b', 'c', 'd', 'root']
const nonRootNodes: CompressibleNode[] = ['a', 'b', 'c', 'd']

const edges = computed(() =>
  nonRootNodes.map((from) => {
    const compressed = currentStep.value.compressed.includes(from)
    const to = compressed ? 'root' : chainParent[from]
    const active = currentStep.value.visiting === from || currentStep.value.visiting === to
    return {
      from,
      to,
      compressed,
      active,
      ...edgeCoords(from, to)
    }
  })
)

function edgeCoords(fromId: NodeId, toId: NodeId) {
  const from = nodes[fromId]
  const to = nodes[toId]
  const dx = to.x - from.x
  const dy = to.y - from.y
  const length = Math.hypot(dx, dy) || 1
  const startPad = fromId === 'root' ? 30 : 24
  const endPad = toId === 'root' ? 34 : 24

  return {
    x1: from.x + (dx / length) * startPad,
    y1: from.y + (dy / length) * startPad,
    x2: to.x - (dx / length) * endPad,
    y2: to.y - (dy / length) * endPad
  }
}

function parentLabel(node: CompressibleNode) {
  return currentStep.value.compressed.includes(node) ? 'root' : chainParent[node]
}

function nodeClass(node: NodeId) {
  return {
    active: currentStep.value.visiting === node,
    compressed: node !== 'root' && currentStep.value.compressed.includes(node as CompressibleNode)
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
  if (current.value < steps.length - 1) {
    current.value += 1
  } else {
    stop()
  }
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
      height="285"
      viewBox="0 0 720 285"
      xmlns="http://www.w3.org/2000/svg"
      font-family="Segoe UI, Arial, sans-serif"
      role="img"
      aria-label="Interactive union-find path compression animation"
    >
      <defs>
        <marker id="uf-anim-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#2563eb" />
        </marker>
        <marker id="uf-anim-grn" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#16a34a" />
        </marker>
        <filter id="uf-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="285" fill="#fbfcfe" />
      <rect x="22" y="34" width="676" height="206" rx="9" fill="#f8fafc" stroke="#d9dee7" />
      <text x="360" y="61" text-anchor="middle" font-size="14" font-weight="700" fill="#0b1220">
        Path compression during find(a)
      </text>

      <g class="edges">
        <line
          v-for="edge in edges"
          :key="edge.from"
          :class="['parent-edge', { compressed: edge.compressed, active: edge.active }]"
          :x1="edge.x1"
          :y1="edge.y1"
          :x2="edge.x2"
          :y2="edge.y2"
          :marker-end="edge.compressed ? 'url(#uf-anim-grn)' : 'url(#uf-anim-blue)'"
        />
      </g>

      <g filter="url(#uf-anim-shadow)" text-anchor="middle" font-size="14" font-weight="700">
        <g
          v-for="node in nonRootNodes"
          :key="node"
          class="node"
          :class="nodeClass(node)"
          :transform="`translate(${nodes[node].x}, ${nodes[node].y})`"
        >
          <circle r="22" />
          <text y="5">{{ nodes[node].label }}</text>
        </g>

        <g class="node root" :class="nodeClass('root')" :transform="`translate(${nodes.root.x}, ${nodes.root.y})`">
          <rect x="-33" y="-22" width="66" height="44" rx="9" />
          <text y="5">{{ nodes.root.label }}</text>
        </g>
      </g>

      <g class="path-labels" font-size="11" text-anchor="middle">
        <text
          v-for="(node, index) in findPath"
          :key="node"
          :x="120 + index * 120"
          y="224"
          :class="{ active: currentStep.visiting === node }"
        >
          {{ node }}
        </text>
      </g>

      <rect x="80" y="246" width="560" height="26" rx="7" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="360" y="264" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">
        parent[a]={{ parentLabel('a') }} · parent[b]={{ parentLabel('b') }} · parent[c]={{ parentLabel('c') }} ·
        parent[d]={{ parentLabel('d') }}
      </text>

      <text x="360" y="205" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Union-find animation controls">
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

.parent-edge {
  stroke: #2563eb;
  stroke-width: 2.2;
  fill: none;
  opacity: 0.72;
  transition:
    opacity 350ms ease,
    stroke 350ms ease;
}

.parent-edge.active {
  opacity: 1;
  stroke-width: 3;
}

.parent-edge.compressed {
  stroke: #16a34a;
  opacity: 1;
}

.node circle,
.node rect {
  fill: #fff;
  stroke: #93c5fd;
  stroke-width: 1.6;
  transition:
    fill 350ms ease,
    stroke 350ms ease,
    transform 350ms ease;
}

.node text {
  fill: #0b1220;
}

.node.active circle,
.node.active rect {
  fill: #eff6ff;
  stroke: #2563eb;
  stroke-width: 2.4;
}

.node.compressed circle {
  fill: #f0fdf4;
  stroke: #16a34a;
}

.node.root rect {
  fill: #eff6ff;
  stroke: #2563eb;
  stroke-width: 1.8;
}

.path-labels text {
  fill: #94a3b8;
  font-weight: 700;
}

.path-labels text.active {
  fill: #2563eb;
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
