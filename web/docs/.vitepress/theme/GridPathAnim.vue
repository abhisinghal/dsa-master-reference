<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Coord = { r: number; c: number }

type Step = {
  cell: Coord | null
  deps?: Coord[]
  formula: string
  description: string
}

type Props = {
  title: string
  rows: number
  cols: number
  dp: number[][]
  fillOrder: Record<string, number>
  steps: Step[]
  pathTrace?: Coord[]
  cellSize?: number
  showArrows?: boolean
  initialValue?: string
}

const props = withDefaults(defineProps<Props>(), {
  pathTrace: () => [],
  cellSize: 44,
  showArrows: true,
  initialValue: ''
})

const gridX = 60
const gridY = 60
const gridWidth = computed(() => props.cols * props.cellSize)
const gridHeight = computed(() => props.rows * props.cellSize)
const svgWidth = computed(() => Math.max(680, gridX + gridWidth.value + 260))
const svgHeight = computed(() => Math.max(260, gridY + gridHeight.value + 90))

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => props.steps[current.value])

const pathSet = computed(() => {
  const s = new Set<string>()
  props.pathTrace.forEach((c) => s.add(`${c.r}-${c.c}`))
  return s
})

function key(r: number, c: number) {
  return `${r}-${c}`
}

function cellX(c: number) {
  return gridX + c * props.cellSize
}

function cellY(r: number) {
  return gridY + r * props.cellSize
}

function isComputed(r: number, c: number) {
  const order = props.fillOrder[key(r, c)]
  if (order === undefined) return false
  const curCell = currentStep.value.cell
  if (!curCell) return order === 0
  const curOrder = props.fillOrder[key(curCell.r, curCell.c)] ?? 0
  return order <= curOrder
}

function cellValue(r: number, c: number) {
  if (!isComputed(r, c)) return props.initialValue
  return props.dp[r]?.[c] ?? ''
}

function isCurrent(r: number, c: number) {
  const cell = currentStep.value.cell
  return Boolean(cell && cell.r === r && cell.c === c)
}

function isDependency(r: number, c: number) {
  return (currentStep.value.deps ?? []).some((d) => d.r === r && d.c === c)
}

function isOnPath(r: number, c: number) {
  return pathSet.value.has(key(r, c))
}

function cellClass(r: number, c: number) {
  return {
    computed: isComputed(r, c),
    current: isCurrent(r, c),
    dependency: isDependency(r, c),
    pending: !isComputed(r, c),
    path: isOnPath(r, c) && isComputed(r, c) && !isCurrent(r, c)
  }
}

const rowIndices = computed(() => Array.from({ length: props.rows }, (_, r) => r))
const colIndices = computed(() => Array.from({ length: props.cols }, (_, c) => c))

const arrows = computed(() => {
  const curCell = currentStep.value.cell
  const deps = currentStep.value.deps ?? []
  if (!curCell || !props.showArrows) return []
  return deps.map((dep) => {
    const fromX = cellX(dep.c) + props.cellSize / 2
    const fromY = cellY(dep.r) + props.cellSize / 2
    const toX = cellX(curCell.c) + props.cellSize / 2
    const toY = cellY(curCell.r) + props.cellSize / 2
    return { fromX, fromY, toX, toY, dep }
  })
})

function stop() {
  playing.value = false
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

function next() {
  if (current.value < props.steps.length - 1) {
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
  if (current.value === props.steps.length - 1) current.value = 0
  playing.value = true
  timer.value = setInterval(next, 1400)
}

onBeforeUnmount(stop)
</script>

<template>
  <ClientOnly>
    <div class="anim-card">
      <div class="anim-title">{{ title }}</div>
      <svg
        class="anim-svg"
        :width="svgWidth"
        :height="svgHeight"
        :viewBox="`0 0 ${svgWidth} ${svgHeight}`"
        xmlns="http://www.w3.org/2000/svg"
        font-family="var(--dsa-font)"
        role="img"
        :aria-label="`Grid DP animation: ${title}`"
      >
        <defs>
          <marker
            id="grid-arrowhead"
            viewBox="0 0 10 10"
            refX="9"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 0 L 10 5 L 0 10 z" class="arrowhead" />
          </marker>
        </defs>

        <rect x="0" y="0" :width="svgWidth" :height="svgHeight" rx="12" class="surface" />

        <g class="grid">
          <g v-for="r in rowIndices" :key="`row-${r}`">
            <g
              v-for="c in colIndices"
              :key="`cell-${r}-${c}`"
              class="grid-cell"
              :class="cellClass(r, c)"
              :transform="`translate(${cellX(c)}, ${cellY(r)})`"
            >
              <rect :width="cellSize" :height="cellSize" rx="7" />
              <text :x="cellSize / 2" :y="cellSize / 2 + 6" text-anchor="middle">{{ cellValue(r, c) }}</text>
            </g>
          </g>
        </g>

        <g class="arrows">
          <line
            v-for="(a, idx) in arrows"
            :key="`arrow-${idx}`"
            :x1="a.fromX"
            :y1="a.fromY"
            :x2="a.toX"
            :y2="a.toY"
            marker-end="url(#grid-arrowhead)"
            class="arrow-line"
          />
        </g>

        <g class="formula-panel">
          <rect :x="svgWidth - 230" y="60" width="210" height="130" rx="10" />
          <text :x="svgWidth - 125" y="86" text-anchor="middle" class="panel-heading">transition</text>
          <text :x="svgWidth - 125" y="118" text-anchor="middle" class="formula-text">{{ currentStep.formula }}</text>
          <text :x="svgWidth - 125" y="170" text-anchor="middle" class="hint-text">arrows show reads</text>
        </g>

        <g class="legend" text-anchor="start">
          <rect :x="svgWidth - 230" :y="svgHeight - 90" width="16" height="16" rx="4" class="legend-current" />
          <text :x="svgWidth - 207" :y="svgHeight - 77">current</text>
          <rect :x="svgWidth - 230" :y="svgHeight - 64" width="16" height="16" rx="4" class="legend-read" />
          <text :x="svgWidth - 207" :y="svgHeight - 51">dependency</text>
          <rect :x="svgWidth - 230" :y="svgHeight - 38" width="16" height="16" rx="4" class="legend-path" />
          <text :x="svgWidth - 207" :y="svgHeight - 25">path</text>
        </g>
      </svg>

      <p class="caption">{{ currentStep.description }}</p>

      <div class="controls" aria-label="Grid DP animation controls">
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
  max-width: 820px;
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

.surface { fill: var(--dsa-bg); }

.formula-panel rect {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
}

.panel-heading {
  fill: var(--dsa-primary);
  font-family: var(--dsa-font);
  font-size: var(--dsa-label-size);
  font-weight: 800;
  text-transform: uppercase;
}

.formula-text {
  fill: var(--dsa-ink);
  font-family: var(--dsa-font);
  font-size: var(--dsa-label-size);
  font-weight: 700;
}

.hint-text {
  fill: var(--dsa-neutral);
  font-family: var(--dsa-font);
  font-size: var(--dsa-caption-size);
}

.legend text {
  fill: var(--dsa-neutral);
  font-family: var(--dsa-font);
  font-size: var(--dsa-caption-size);
}

.grid-cell rect {
  fill: var(--dsa-bg);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 280ms ease,
    opacity 280ms ease,
    stroke 280ms ease,
    stroke-dasharray 280ms ease;
}

.grid-cell text {
  fill: var(--dsa-ink);
  font-family: var(--dsa-font);
  font-size: var(--dsa-value-size);
  font-weight: 800;
}

.grid-cell.pending rect { opacity: 0.38; }
.grid-cell.computed rect { fill: var(--dsa-bg); }

.grid-cell.path rect {
  fill: var(--dsa-success);
  stroke: var(--dsa-success);
}

.grid-cell.path text { fill: var(--dsa-bg); }

.grid-cell.dependency rect {
  stroke: var(--dsa-info);
  stroke-width: 2.6px;
  stroke-dasharray: 5 3;
}

.grid-cell.current rect {
  stroke: var(--dsa-primary);
  stroke-width: 3px;
}

.arrow-line {
  stroke: var(--dsa-info);
  stroke-width: 2;
  fill: none;
  opacity: 0.85;
}

.arrowhead { fill: var(--dsa-info); }

.legend-current {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-cell-stroke);
}

.legend-read {
  fill: var(--dsa-bg);
  stroke: var(--dsa-info);
  stroke-width: var(--dsa-cell-stroke);
  stroke-dasharray: 5 3;
}

.legend-path {
  fill: var(--dsa-success);
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-cell-stroke);
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
