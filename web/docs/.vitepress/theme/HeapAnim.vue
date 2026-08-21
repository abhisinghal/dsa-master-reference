<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Step = {
  heap: number[]
  activeIndex: number | null
  compareIndex: number | null
  swapFrom: number | null
  swapTo: number | null
  description: string
}

type NodePosition = {
  x: number
  y: number
}

const cellWidth = 34
const cellHeight = 30
const arrayStartX = 208
const arrayY = 232
const arrayStep = 38
const nodeRadius = 21
const nodePositions: Record<number, NodePosition> = {
  0: { x: 360, y: 52 },
  1: { x: 220, y: 112 },
  2: { x: 500, y: 112 },
  3: { x: 145, y: 174 },
  4: { x: 295, y: 174 },
  5: { x: 425, y: 174 },
  6: { x: 555, y: 174 },
  7: { x: 635, y: 174 }
}
const edgePairs: [number, number][] = [
  [0, 1],
  [0, 2],
  [1, 3],
  [1, 4],
  [2, 5],
  [2, 6],
  [2, 7]
]

const steps: Step[] = [
  {
    heap: [2, 4, 7, 5, 6, 9, 11],
    activeIndex: null,
    compareIndex: null,
    swapFrom: null,
    swapTo: null,
    description: 'Initial min-heap is valid; every parent is less than or equal to its children.'
  },
  {
    heap: [2, 4, 7, 5, 6, 9, 11, 1],
    activeIndex: 7,
    compareIndex: 2,
    swapFrom: 7,
    swapTo: 2,
    description: 'Insert 1 at the bottom-right slot. Since 1 < 7, it swaps with its parent.'
  },
  {
    heap: [2, 4, 1, 5, 6, 9, 11, 7],
    activeIndex: 2,
    compareIndex: 0,
    swapFrom: 2,
    swapTo: 0,
    description: 'Now 1 is at position 2. Since 1 < 2, it swaps with the root.'
  },
  {
    heap: [1, 4, 2, 5, 6, 9, 11, 7],
    activeIndex: 0,
    compareIndex: null,
    swapFrom: null,
    swapTo: null,
    description: 'The inserted value reaches the root, so the min-heap invariant is restored.'
  }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const visibleNodes = computed(() =>
  currentStep.value.heap.map((value, index) => ({
    index,
    value,
    ...nodePositions[index]
  }))
)
const visibleEdges = computed(() => edgePairs.filter(([, child]) => child < currentStep.value.heap.length))
const stateLabel = computed(() => {
  const step = currentStep.value
  if (step.compareIndex === null || step.activeIndex === null) return 'parent ≤ children'
  return `${step.heap[step.activeIndex]} < ${step.heap[step.compareIndex]} → swap`
})

function arrayX(index: number) {
  return arrayStartX + index * arrayStep
}

function nodeClass(index: number) {
  return {
    active: currentStep.value.activeIndex === index,
    comparing: currentStep.value.compareIndex === index,
    settled: current.value === steps.length - 1 && index === 0
  }
}

function ringClass(index: number) {
  return {
    source: currentStep.value.swapFrom === index,
    destination: currentStep.value.swapTo === index
  }
}

function arrayClass(index: number) {
  return {
    active: currentStep.value.activeIndex === index,
    comparing: currentStep.value.compareIndex === index,
    source: currentStep.value.swapFrom === index,
    destination: currentStep.value.swapTo === index,
    settled: current.value === steps.length - 1 && index === 0
  }
}

function position(index: number) {
  return nodePositions[index]
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
  <ClientOnly>
    <div class="anim-card">
      <div class="anim-header">
        <h3>Min-heap insert: sift 1 upward</h3>
        <span class="counter">Step {{ current + 1 }} / {{ steps.length }}</span>
      </div>

      <svg
        class="anim-svg"
        width="720"
        height="300"
        viewBox="0 0 720 300"
        xmlns="http://www.w3.org/2000/svg"
        font-family="var(--dsa-font)"
        role="img"
        aria-label="Interactive min-heap sift-up animation"
      >
        <defs>
          <marker id="heap-success-arrow" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)" />
          </marker>
          <marker id="heap-danger-arrow" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-danger)" />
          </marker>
        </defs>

        <rect x="0" y="0" width="720" height="300" rx="12" fill="var(--dsa-bg)" />

        <text x="360" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">
          sift-up compares the inserted value with its parent
        </text>
        <rect x="36" y="36" width="130" height="28" rx="9" fill="var(--dsa-warning-soft)" stroke="var(--dsa-warning)" />
        <text x="101" y="55" text-anchor="middle" font-size="12" font-weight="800" fill="var(--dsa-warning)">
          parent ≤ children
        </text>

        <g class="tree-edges">
          <line
            v-for="([parent, child]) in visibleEdges"
            :key="`${parent}-${child}`"
            :x1="position(parent).x"
            :y1="position(parent).y + nodeRadius"
            :x2="position(child).x"
            :y2="position(child).y - nodeRadius"
          />
        </g>

        <g v-if="currentStep.swapFrom !== null && currentStep.swapTo !== null" class="swap-arrows">
          <line
            :x1="position(currentStep.swapFrom).x"
            :y1="position(currentStep.swapFrom).y - nodeRadius"
            :x2="position(currentStep.swapTo).x"
            :y2="position(currentStep.swapTo).y + nodeRadius"
            marker-end="url(#heap-success-arrow)"
          />
          <line
            class="down"
            :x1="position(currentStep.swapTo).x"
            :y1="position(currentStep.swapTo).y + nodeRadius"
            :x2="position(currentStep.swapFrom).x"
            :y2="position(currentStep.swapFrom).y - nodeRadius"
            marker-end="url(#heap-danger-arrow)"
          />
        </g>

        <g text-anchor="middle">
          <g
            v-for="node in visibleNodes"
            :key="node.index"
            class="heap-node"
            :class="nodeClass(node.index)"
            :transform="`translate(${node.x}, ${node.y})`"
          >
            <circle :r="nodeRadius" />
            <circle v-if="currentStep.swapFrom === node.index || currentStep.swapTo === node.index" class="swap-ring" :class="ringClass(node.index)" r="27" />
            <text y="6" font-size="17" font-weight="800">{{ node.value }}</text>
            <text y="38" font-size="10" font-weight="700">{{ node.index }}</text>
          </g>
        </g>

        <rect x="184" y="210" width="352" height="18" rx="8" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" />
        <text x="360" y="223" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">
          {{ stateLabel }}
        </text>

        <g class="heap-array" text-anchor="middle">
          <text x="166" y="252" font-size="12" font-weight="800" fill="var(--dsa-primary)">array</text>
          <g v-for="(value, index) in currentStep.heap" :key="index" class="array-cell" :class="arrayClass(index)">
            <rect :x="arrayX(index)" :y="arrayY" :width="cellWidth" :height="cellHeight" rx="7" />
            <text :x="arrayX(index) + cellWidth / 2" :y="arrayY + 20" font-size="14" font-weight="800">{{ value }}</text>
            <text :x="arrayX(index) + cellWidth / 2" :y="arrayY + 44" font-size="10" font-weight="700">{{ index }}</text>
          </g>
        </g>

        <text x="360" y="292" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">
          {{ currentStep.description }}
        </text>
      </svg>

      <p class="anim-caption">
        The tree shows parent-child order; the array below shows the same heap as contiguous storage.
      </p>

      <div class="controls" aria-label="Heap sift-up animation controls">
        <button type="button" :disabled="current === 0" @click="prev">◀ Prev</button>
        <button type="button" @click="togglePlay">{{ playing ? '⏸ Pause' : '▶ Play' }}</button>
        <button type="button" :disabled="current === steps.length - 1" @click="next">Next ▶</button>
        <button type="button" @click="reset">⟳ Reset</button>
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
}

.anim-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}

.anim-header h3 {
  margin: 0;
  color: var(--dsa-ink);
  font: 700 14px var(--dsa-font);
}

.anim-svg {
  display: block;
  max-width: 100%;
  width: 100%;
  height: auto;
}

.tree-edges line {
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-arrow-stroke);
  transition: stroke 320ms ease;
}

.swap-arrows line {
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-arrow-stroke);
  fill: none;
  opacity: 0.9;
  transition: opacity 320ms ease;
}

.swap-arrows line.down {
  stroke: var(--dsa-danger);
  stroke-dasharray: 5 4;
  opacity: 0.78;
}

.heap-node circle:first-child {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    transform 320ms ease;
}

.heap-node.active circle:first-child {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-outline-stroke);
}

.heap-node.comparing circle:first-child {
  fill: var(--dsa-warning-soft);
  stroke: var(--dsa-warning);
}

.heap-node.settled circle:first-child {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-outline-stroke);
}

.heap-node text {
  fill: var(--dsa-ink);
}

.heap-node text:last-child {
  fill: var(--dsa-neutral);
}

.swap-ring {
  fill: none;
  stroke-width: var(--dsa-outline-stroke);
  stroke-dasharray: 5 4;
}

.swap-ring.source {
  stroke: var(--dsa-danger);
}

.swap-ring.destination {
  stroke: var(--dsa-success);
}

.array-cell rect {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    transform 320ms ease;
}

.array-cell text {
  fill: var(--dsa-ink);
}

.array-cell text:last-child {
  fill: var(--dsa-neutral);
}

.array-cell.active rect {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-outline-stroke);
  transform: translateY(-2px);
}

.array-cell.comparing rect {
  fill: var(--dsa-warning-soft);
  stroke: var(--dsa-warning);
}

.array-cell.source rect {
  stroke: var(--dsa-danger);
}

.array-cell.destination rect,
.array-cell.settled rect {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
}

.anim-caption {
  margin: 8px 0 0;
  color: var(--dsa-neutral);
  font: italic 11.5px var(--dsa-font);
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
  font: 600 13px var(--dsa-font);
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
  color: var(--dsa-neutral);
  font: 600 13px var(--dsa-font);
}
</style>
