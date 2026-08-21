<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type NodeId = 'root' | 'c' | 'a' | 't' | 'r'
type EdgeId = 'root-c' | 'c-a' | 'a-t' | 'a-r'
type Step = {
  operation: string
  word: string
  visibleNodes: NodeId[]
  visibleEdges: EdgeId[]
  activePath: EdgeId[]
  addedNodes: NodeId[]
  addedEdges: EdgeId[]
  current: NodeId
  failedFrom?: NodeId
  failedChar?: string
  missingEnd?: NodeId
  result: string
  description: string
}

type TrieNode = { id: NodeId; x: number; y: number; label: string; terminal?: boolean }
type TrieEdge = { id: EdgeId; from: NodeId; to: NodeId; label: string }

const nodes: Record<NodeId, TrieNode> = {
  root: { id: 'root', x: 360, y: 54, label: 'root' },
  c: { id: 'c', x: 360, y: 108, label: 'c' },
  a: { id: 'a', x: 360, y: 162, label: 'a' },
  t: { id: 't', x: 270, y: 228, label: 't', terminal: true },
  r: { id: 'r', x: 450, y: 228, label: 'r', terminal: true }
}

const edges: TrieEdge[] = [
  { id: 'root-c', from: 'root', to: 'c', label: 'c' },
  { id: 'c-a', from: 'c', to: 'a', label: 'a' },
  { id: 'a-t', from: 'a', to: 't', label: 't' },
  { id: 'a-r', from: 'a', to: 'r', label: 'r' }
]

const steps: Step[] = [
  {
    operation: 'insert',
    word: 'cat',
    visibleNodes: ['root'],
    visibleEdges: [],
    activePath: [],
    addedNodes: [],
    addedEdges: [],
    current: 'root',
    result: 'start at root',
    description: 'Begin insert("cat") with only the root node in the trie.'
  },
  {
    operation: 'insert',
    word: 'cat',
    visibleNodes: ['root', 'c'],
    visibleEdges: ['root-c'],
    activePath: ['root-c'],
    addedNodes: ['c'],
    addedEdges: ['root-c'],
    current: 'c',
    result: 'add c',
    description: 'No c edge exists from root, so create root → c.'
  },
  {
    operation: 'insert',
    word: 'cat',
    visibleNodes: ['root', 'c', 'a'],
    visibleEdges: ['root-c', 'c-a'],
    activePath: ['root-c', 'c-a'],
    addedNodes: ['a'],
    addedEdges: ['c-a'],
    current: 'a',
    result: 'add a',
    description: 'Continue the word by adding c → a.'
  },
  {
    operation: 'insert',
    word: 'cat',
    visibleNodes: ['root', 'c', 'a', 't'],
    visibleEdges: ['root-c', 'c-a', 'a-t'],
    activePath: ['root-c', 'c-a', 'a-t'],
    addedNodes: ['t'],
    addedEdges: ['a-t'],
    current: 't',
    result: 'mark t★',
    description: 'Add t and mark it as an end-of-word node for "cat".'
  },
  {
    operation: 'insert',
    word: 'car',
    visibleNodes: ['root', 'c', 'a', 't'],
    visibleEdges: ['root-c', 'c-a', 'a-t'],
    activePath: ['root-c', 'c-a'],
    addedNodes: [],
    addedEdges: [],
    current: 'a',
    result: 'reuse c → a',
    description: 'Insert("car") shares the existing c and a prefix.'
  },
  {
    operation: 'insert',
    word: 'car',
    visibleNodes: ['root', 'c', 'a', 't', 'r'],
    visibleEdges: ['root-c', 'c-a', 'a-t', 'a-r'],
    activePath: ['root-c', 'c-a', 'a-r'],
    addedNodes: ['r'],
    addedEdges: ['a-r'],
    current: 'r',
    result: 'add r★',
    description: 'Branch from a to r and mark r as another terminal word.'
  },
  {
    operation: 'search',
    word: 'cars',
    visibleNodes: ['root', 'c', 'a', 't', 'r'],
    visibleEdges: ['root-c', 'c-a', 'a-t', 'a-r'],
    activePath: ['root-c', 'c-a', 'a-r'],
    addedNodes: [],
    addedEdges: [],
    current: 'r',
    result: 'matched car',
    description: 'Search("cars") walks root → c → a → r, but one letter remains.'
  },
  {
    operation: 'search',
    word: 'cars',
    visibleNodes: ['root', 'c', 'a', 't', 'r'],
    visibleEdges: ['root-c', 'c-a', 'a-t', 'a-r'],
    activePath: ['root-c', 'c-a', 'a-r'],
    addedNodes: [],
    addedEdges: [],
    current: 'r',
    failedFrom: 'r',
    failedChar: 's',
    result: 'false: missing s',
    description: 'The r node has no s child, so "cars" is not in the trie.'
  },
  {
    operation: 'search',
    word: 'ca',
    visibleNodes: ['root', 'c', 'a', 't', 'r'],
    visibleEdges: ['root-c', 'c-a', 'a-t', 'a-r'],
    activePath: ['root-c', 'c-a'],
    addedNodes: [],
    addedEdges: [],
    current: 'a',
    result: 'walked ca',
    description: 'Search("ca") can follow c and a without missing an edge.'
  },
  {
    operation: 'search',
    word: 'ca',
    visibleNodes: ['root', 'c', 'a', 't', 'r'],
    visibleEdges: ['root-c', 'c-a', 'a-t', 'a-r'],
    activePath: ['root-c', 'c-a'],
    addedNodes: [],
    addedEdges: [],
    current: 'a',
    missingEnd: 'a',
    result: 'false: no ★',
    description: 'The input is exhausted at a, but a is not an end-of-word node.'
  }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])

function isNodeVisible(node: NodeId) {
  return currentStep.value.visibleNodes.includes(node)
}

function isEdgeVisible(edge: EdgeId) {
  return currentStep.value.visibleEdges.includes(edge)
}

function isEdgeActive(edge: EdgeId) {
  return currentStep.value.activePath.includes(edge)
}

function isEdgeAdded(edge: EdgeId) {
  return currentStep.value.addedEdges.includes(edge)
}

function isNodeAdded(node: NodeId) {
  return currentStep.value.addedNodes.includes(node)
}

function isCurrent(node: NodeId) {
  return currentStep.value.current === node
}

function isMissingEnd(node: NodeId) {
  return currentStep.value.missingEnd === node
}

function edgeMidpoint(edge: TrieEdge) {
  const from = nodes[edge.from]
  const to = nodes[edge.to]
  return {
    x: (from.x + to.x) / 2,
    y: (from.y + to.y) / 2
  }
}

function edgeClass(edge: EdgeId) {
  return {
    active: isEdgeActive(edge),
    added: isEdgeAdded(edge)
  }
}

function nodeClass(node: NodeId) {
  return {
    current: isCurrent(node),
    added: isNodeAdded(node),
    terminal: Boolean(nodes[node].terminal),
    'missing-end': isMissingEnd(node)
  }
}

function failLine() {
  const from = nodes[currentStep.value.failedFrom ?? 'r']
  return {
    x1: from.x + 24,
    y1: from.y,
    x2: from.x + 96,
    y2: from.y,
    labelX: from.x + 64,
    labelY: from.y - 10
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
  timer.value = setInterval(next, 1250)
}

onBeforeUnmount(stop)
</script>

<template>
  <ClientOnly>
    <div class="anim-card">
      <div class="anim-title">Trie insert/search walk</div>
      <svg
        class="anim-svg"
        width="720"
        height="300"
        viewBox="0 0 720 300"
        xmlns="http://www.w3.org/2000/svg"
        font-family="var(--dsa-font)"
        role="img"
        aria-label="Interactive trie insertion and search animation"
      >
        <rect x="0" y="0" width="720" height="300" rx="12" class="surface" />

        <g class="status-panel">
          <rect x="24" y="42" width="190" height="92" rx="10" />
          <text x="119" y="68" text-anchor="middle" class="panel-heading">{{ currentStep.operation }}</text>
          <text x="119" y="98" text-anchor="middle" class="word-text">"{{ currentStep.word }}"</text>
          <text x="119" y="121" text-anchor="middle" class="result-text">{{ currentStep.result }}</text>
        </g>

        <g class="edges">
          <g v-for="edge in edges" :key="edge.id" v-show="isEdgeVisible(edge.id)">
            <line
              :class="['trie-edge', edgeClass(edge.id)]"
              :x1="nodes[edge.from].x"
              :y1="nodes[edge.from].y + 23"
              :x2="nodes[edge.to].x"
              :y2="nodes[edge.to].y - 23"
            />
            <rect
              :x="edgeMidpoint(edge).x - 12"
              :y="edgeMidpoint(edge).y - 12"
              width="24"
              height="20"
              rx="7"
              class="edge-label-bg"
            />
            <text :x="edgeMidpoint(edge).x" :y="edgeMidpoint(edge).y + 3" text-anchor="middle" class="edge-label">
              {{ edge.label }}
            </text>
          </g>
        </g>

        <g v-if="currentStep.failedFrom && currentStep.failedChar" class="failed-step">
          <line
            :x1="failLine().x1"
            :y1="failLine().y1"
            :x2="failLine().x2"
            :y2="failLine().y2"
          />
          <text :x="failLine().labelX" :y="failLine().labelY" text-anchor="middle">
            no '{{ currentStep.failedChar }}'
          </text>
        </g>

        <g class="nodes" text-anchor="middle">
          <g
            v-for="node in Object.values(nodes)"
            :key="node.id"
            v-show="isNodeVisible(node.id)"
            class="trie-node"
            :class="nodeClass(node.id)"
            :transform="`translate(${node.x}, ${node.y})`"
          >
            <circle r="22" />
            <text y="5" class="node-label">{{ node.label }}</text>
            <text v-if="node.terminal" x="25" y="-16" class="star">★</text>
            <text v-if="isMissingEnd(node.id)" x="0" y="41" class="missing-label">no ★</text>
          </g>
        </g>

        <g class="legend" text-anchor="start">
          <rect x="506" y="48" width="16" height="16" rx="4" class="legend-current" />
          <text x="529" y="61">current node</text>
          <rect x="506" y="76" width="16" height="16" rx="4" class="legend-terminal" />
          <text x="529" y="89">end marker ★</text>
          <line x1="506" y1="111" x2="522" y2="111" class="legend-fail" />
          <text x="529" y="115">failed continuation</text>
        </g>

        <text x="360" y="282" text-anchor="middle" class="svg-caption">
          A search succeeds only if every edge exists and the final node has ★.
        </text>
      </svg>

      <p class="caption">{{ currentStep.description }}</p>

      <div class="controls" aria-label="Trie walk animation controls">
        <button type="button" :disabled="current === 0" @click="prev">◀ Prev</button>
        <button type="button" @click="togglePlay">{{ playing ? '⏸ Pause' : '▶ Play' }}</button>
        <button type="button" :disabled="current === steps.length - 1" @click="next">Next ▶</button>
        <button type="button" @click="reset">⟳ Reset</button>
        <span class="counter">Step {{ current + 1 }} / {{ steps.length }}</span>
      </div>
    </div>
  </ClientOnly>
</template>

<style scoped>
.anim-card {
  max-width: 720px;
  margin: 18px 0;
  padding: 12px;
  border: 1px solid var(--dsa-neutral-line);
  border-radius: 10px;
  background: var(--dsa-bg);
  color: var(--dsa-ink);
}

.anim-title {
  margin-bottom: 8px;
  color: var(--dsa-primary);
  font-family: var(--dsa-font);
  font-size: 14px;
  font-weight: 800;
  text-align: center;
}

.anim-svg {
  display: block;
  width: 100%;
  height: auto;
}

.surface {
  fill: var(--dsa-bg);
}

.status-panel rect {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
}

.panel-heading,
.word-text,
.result-text,
.edge-label,
.node-label,
.star,
.missing-label,
.legend text,
.failed-step text,
.svg-caption {
  font-family: var(--dsa-font);
}

.panel-heading {
  fill: var(--dsa-primary);
  font-size: var(--dsa-label-size);
  font-weight: 800;
  text-transform: uppercase;
}

.word-text {
  fill: var(--dsa-ink);
  font-size: 20px;
  font-weight: 800;
}

.result-text,
.legend text,
.svg-caption {
  fill: var(--dsa-neutral);
  font-size: var(--dsa-caption-size);
  font-weight: 700;
}

.trie-edge {
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-arrow-stroke);
  transition:
    opacity 260ms ease,
    stroke 260ms ease,
    stroke-width 260ms ease;
}

.trie-edge.active {
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-outline-stroke);
}

.trie-edge.added {
  stroke: var(--dsa-success);
}

.edge-label-bg {
  fill: var(--dsa-bg);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
}

.edge-label {
  fill: var(--dsa-ink);
  font-size: var(--dsa-label-size);
  font-weight: 800;
}

.trie-node circle {
  fill: var(--dsa-bg);
  stroke: var(--dsa-info-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 280ms ease,
    stroke 280ms ease,
    stroke-width 280ms ease;
}

.trie-node.added circle {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
}

.trie-node.current circle {
  fill: var(--dsa-primary);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-outline-stroke);
}

.trie-node.missing-end circle {
  stroke: var(--dsa-warning);
  stroke-dasharray: 5 3;
  stroke-width: 3px;
}

.node-label {
  fill: var(--dsa-ink);
  font-size: var(--dsa-label-size);
  font-weight: 800;
}

.trie-node.current .node-label {
  fill: var(--dsa-bg);
}

.star {
  fill: var(--dsa-success);
  font-size: 18px;
  font-weight: 900;
}

.missing-label {
  fill: var(--dsa-warning);
  font-size: var(--dsa-caption-size);
  font-weight: 800;
}

.failed-step line {
  stroke: var(--dsa-danger);
  stroke-width: var(--dsa-arrow-stroke);
  stroke-dasharray: 6 4;
}

.failed-step text {
  fill: var(--dsa-danger);
  font-size: var(--dsa-label-size);
  font-weight: 800;
}

.legend-current {
  fill: var(--dsa-primary);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-cell-stroke);
}

.legend-terminal {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-cell-stroke);
}

.legend-fail {
  stroke: var(--dsa-danger);
  stroke-width: var(--dsa-arrow-stroke);
  stroke-dasharray: 6 4;
}

.caption {
  margin: 10px 2px 0;
  color: var(--dsa-neutral);
  font-family: var(--dsa-font);
  font-size: 13px;
  font-weight: 700;
  text-align: center;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
}

button {
  border: 1px solid var(--dsa-neutral-line);
  border-radius: 7px;
  padding: 6px 10px;
  background: var(--dsa-bg);
  color: var(--dsa-ink);
  font-family: var(--dsa-font);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

button:hover:not(:disabled) {
  border-color: var(--dsa-primary);
  color: var(--dsa-primary);
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.counter {
  margin-left: auto;
  color: var(--dsa-neutral);
  font-family: var(--dsa-font);
  font-size: 13px;
  font-weight: 700;
}
</style>
