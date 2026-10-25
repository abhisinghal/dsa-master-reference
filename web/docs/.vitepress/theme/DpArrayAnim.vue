<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Step = {
  revealOrder: number
  cell: number | null
  deps?: number[]
  formula: string
  result?: string
  description: string
}

type Props = {
  title: string
  length: number
  dp: (number | string)[]
  labels?: (number | string)[]
  fillOrder: Record<string, number>
  baseCells?: number[]
  highlightCells?: number[]
  steps: Step[]
  cellSize?: number
  showIndex?: boolean
  initialValue?: string
  transitionLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  labels: () => [],
  baseCells: () => [],
  highlightCells: () => [],
  cellSize: 52,
  showIndex: true,
  initialValue: '',
  transitionLabel: 'transition'
})

const baseSet = computed(() => new Set(props.baseCells))
const highlightSet = computed(() => new Set(props.highlightCells))

const indices = computed(() => Array.from({ length: props.length }, (_, i) => i))

const arrayX = 40
const arrayY = 90
const svgWidth = computed(() => Math.max(760, arrayX + props.length * props.cellSize + 260))
const svgHeight = 260

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => props.steps[current.value])

function cellX(i: number) {
  return arrayX + i * props.cellSize
}

function isComputed(i: number) {
  const order = props.fillOrder[String(i)]
  if (order === undefined) return false
  return order <= currentStep.value.revealOrder
}

function cellValue(i: number) {
  if (!isComputed(i)) return props.initialValue
  return props.dp[i] ?? ''
}

function isCurrent(i: number) {
  return currentStep.value.cell === i
}

function isDependency(i: number) {
  return (currentStep.value.deps ?? []).includes(i)
}

function cellClass(i: number) {
  return {
    base: baseSet.value.has(i) && isComputed(i),
    computed: isComputed(i) && !baseSet.value.has(i),
    highlight: highlightSet.value.has(i) && isComputed(i) && !isCurrent(i),
    current: isCurrent(i),
    dependency: isDependency(i),
    pending: !isComputed(i)
  }
}

const arrows = computed(() => {
  const curCell = currentStep.value.cell
  const deps = currentStep.value.deps ?? []
  if (curCell === null) return []
  return deps.map((depIdx) => {
    const fromX = cellX(depIdx) + props.cellSize / 2
    const fromY = arrayY - 6
    const toX = cellX(curCell) + props.cellSize / 2
    const toY = arrayY - 6
    const midX = (fromX + toX) / 2
    const archHeight = Math.min(50, 18 + Math.abs(depIdx - curCell) * 10)
    const midY = arrayY - archHeight
    return { path: `M ${fromX} ${fromY} Q ${midX} ${midY}, ${toX} ${toY}` }
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
  timer.value = setInterval(next, 1300)
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
        :aria-label="`1D DP array animation: ${title}`"
      >
        <defs>
          <marker
            id="dparr-arrowhead"
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

        <g class="arrows">
          <path
            v-for="(a, idx) in arrows"
            :key="`arrow-${idx}`"
            :d="a.path"
            class="arrow-line"
            marker-end="url(#dparr-arrowhead)"
          />
        </g>

        <g v-if="showIndex" class="index-labels" text-anchor="middle">
          <text
            v-for="i in indices"
            :key="`idx-${i}`"
            :x="cellX(i) + cellSize / 2"
            :y="arrayY - 56"
          >
            {{ labels[i] !== undefined ? labels[i] : i }}
          </text>
        </g>

        <g class="dp-array">
          <g
            v-for="i in indices"
            :key="`cell-${i}`"
            class="dp-cell"
            :class="cellClass(i)"
            :transform="`translate(${cellX(i)}, ${arrayY})`"
          >
            <rect :width="cellSize" :height="cellSize" rx="7" />
            <text :x="cellSize / 2" :y="cellSize / 2 + 7" text-anchor="middle">{{ cellValue(i) }}</text>
          </g>
        </g>

        <g class="formula-panel">
          <rect :x="svgWidth - 230" y="78" width="210" height="130" rx="10" />
          <text :x="svgWidth - 125" y="104" text-anchor="middle" class="panel-heading">{{ transitionLabel }}</text>
          <text v-if="currentStep.result" :x="svgWidth - 125" y="132" text-anchor="middle" class="formula-text">{{ currentStep.result }}</text>
          <text :x="svgWidth - 125" y="158" text-anchor="middle" class="formula-text">{{ currentStep.formula }}</text>
          <text :x="svgWidth - 125" y="188" text-anchor="middle" class="hint-text">arcs show reads</text>
        </g>

        <g class="legend" text-anchor="start">
          <rect x="40" :y="arrayY + cellSize + 20" width="16" height="16" rx="4" class="legend-current" />
          <text x="63" :y="arrayY + cellSize + 33">current</text>
          <rect x="150" :y="arrayY + cellSize + 20" width="16" height="16" rx="4" class="legend-read" />
          <text x="173" :y="arrayY + cellSize + 33">dependency</text>
          <rect x="280" :y="arrayY + cellSize + 20" width="16" height="16" rx="4" class="legend-highlight" />
          <text x="303" :y="arrayY + cellSize + 33">highlight</text>
        </g>
      </svg>

      <p class="caption">{{ currentStep.description }}</p>

      <div class="controls" aria-label="1D DP array animation controls">
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

.index-labels text {
  fill: var(--dsa-neutral);
  font-family: var(--dsa-font);
  font-size: var(--dsa-caption-size);
  font-weight: 700;
}

.dp-cell rect {
  fill: var(--dsa-bg);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 280ms ease,
    opacity 280ms ease,
    stroke 280ms ease,
    stroke-dasharray 280ms ease;
}

.dp-cell text {
  fill: var(--dsa-ink);
  font-family: var(--dsa-font);
  font-size: var(--dsa-value-size);
  font-weight: 800;
}

.dp-cell.pending rect { opacity: 0.38; }
.dp-cell.base rect { fill: var(--dsa-neutral-soft); }
.dp-cell.computed rect { fill: var(--dsa-bg); }

.dp-cell.highlight rect {
  fill: var(--dsa-success);
  stroke: var(--dsa-success);
}

.dp-cell.highlight text { fill: var(--dsa-bg); }

.dp-cell.dependency rect {
  stroke: var(--dsa-info);
  stroke-width: 2.6px;
  stroke-dasharray: 5 3;
}

.dp-cell.current rect {
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

.legend-highlight {
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
