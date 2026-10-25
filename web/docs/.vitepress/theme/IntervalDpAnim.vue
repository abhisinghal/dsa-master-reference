<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Coord = { l: number; r: number }

type SplitRead = { l: number; r: number }

type Step = {
  revealOrder: number
  cell: Coord | null
  splits?: { k: number; left: SplitRead; right: SplitRead; cost: string | number }[]
  formula: string
  result?: string
  description: string
}

type Props = {
  title: string
  n: number
  labels?: (string | number)[]
  dp: (number | string)[][]
  fillOrder: Record<string, number>
  steps: Step[]
  cellSize?: number
}

const props = withDefaults(defineProps<Props>(), {
  labels: () => [],
  cellSize: 54
})

const indices = computed(() => Array.from({ length: props.n }, (_, i) => i))

const tableX = 60
const tableY = 70
const svgWidth = computed(() => Math.max(760, tableX + props.n * props.cellSize + 300))
const svgHeight = computed(() => Math.max(300, tableY + props.n * props.cellSize + 100))

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => props.steps[current.value])

function key(l: number, r: number) {
  return `${l}-${r}`
}

function cellX(r: number) {
  return tableX + r * props.cellSize
}

function cellY(l: number) {
  return tableY + l * props.cellSize
}

function isValid(l: number, r: number) {
  return l <= r
}

function isComputed(l: number, r: number) {
  if (!isValid(l, r)) return false
  const order = props.fillOrder[key(l, r)]
  if (order === undefined) return false
  return order <= currentStep.value.revealOrder
}

function cellValue(l: number, r: number): string | number {
  if (!isValid(l, r)) return ''
  return isComputed(l, r) ? (props.dp[l]?.[r] ?? '') : ''
}

function isCurrent(l: number, r: number) {
  const cell = currentStep.value.cell
  return Boolean(cell && cell.l === l && cell.r === r)
}

function isSplitRead(l: number, r: number) {
  const splits = currentStep.value.splits ?? []
  return splits.some(
    (s) => (s.left.l === l && s.left.r === r) || (s.right.l === l && s.right.r === r)
  )
}

function cellClass(l: number, r: number) {
  if (!isValid(l, r)) return { empty: true }
  return {
    base: l === r && isComputed(l, r),
    computed: isComputed(l, r) && l !== r,
    current: isCurrent(l, r),
    dependency: isSplitRead(l, r) && !isCurrent(l, r),
    pending: !isComputed(l, r)
  }
}

const arrows = computed(() => {
  const cur = currentStep.value.cell
  const splits = currentStep.value.splits ?? []
  if (!cur) return []
  const toX = cellX(cur.r) + props.cellSize / 2
  const toY = cellY(cur.l) + props.cellSize / 2
  return splits.flatMap((s, i) => {
    const colors = ['var(--dsa-info)', 'var(--dsa-warn)', 'var(--dsa-primary)']
    const color = colors[i % colors.length]
    const leftFrom = {
      x: cellX(s.left.r) + props.cellSize / 2,
      y: cellY(s.left.l) + props.cellSize / 2
    }
    const rightFrom = {
      x: cellX(s.right.r) + props.cellSize / 2,
      y: cellY(s.right.l) + props.cellSize / 2
    }
    return [
      { fromX: leftFrom.x, fromY: leftFrom.y, toX, toY, color, splitIdx: i },
      { fromX: rightFrom.x, fromY: rightFrom.y, toX, toY, color, splitIdx: i }
    ]
  })
})

const splitLines = computed(() => currentStep.value.splits ?? [])

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
  timer.value = setInterval(next, 1600)
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
        :aria-label="`Interval DP triangular table animation: ${title}`"
      >
        <defs>
          <marker
            id="interval-arrowhead"
            viewBox="0 0 10 10"
            refX="9"
            refY="5"
            markerWidth="5.5"
            markerHeight="5.5"
            orient="auto-start-reverse"
          >
            <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
          </marker>
        </defs>

        <rect x="0" y="0" :width="svgWidth" :height="svgHeight" rx="12" class="surface" />

        <g class="axis-labels" text-anchor="middle">
          <text x="30" :y="tableY - 30" class="axis-caption">l ↓</text>
          <text :x="tableX - 24" :y="tableY - 30" class="axis-caption">r →</text>
          <text
            v-for="r in indices"
            :key="`r-${r}`"
            :x="cellX(r) + cellSize / 2"
            :y="tableY - 10"
            class="axis-label"
          >
            {{ labels[r] !== undefined ? labels[r] : r }}
          </text>
          <text
            v-for="l in indices"
            :key="`l-${l}`"
            :x="tableX - 14"
            :y="cellY(l) + cellSize / 2 + 5"
            class="axis-label"
            text-anchor="end"
          >
            {{ labels[l] !== undefined ? labels[l] : l }}
          </text>
        </g>

        <g class="grid">
          <template v-for="l in indices" :key="`row-${l}`">
            <g
              v-for="r in indices"
              :key="`cell-${l}-${r}`"
              class="dp-cell"
              :class="cellClass(l, r)"
              :transform="`translate(${cellX(r)}, ${cellY(l)})`"
            >
              <rect v-if="isValid(l, r)" :width="cellSize" :height="cellSize" rx="7" />
              <text v-if="isValid(l, r)" :x="cellSize / 2" :y="cellSize / 2 + 7" text-anchor="middle">{{ cellValue(l, r) }}</text>
            </g>
          </template>
        </g>

        <g class="arrows">
          <line
            v-for="(a, idx) in arrows"
            :key="`arrow-${idx}`"
            :x1="a.fromX"
            :y1="a.fromY"
            :x2="a.toX"
            :y2="a.toY"
            :style="`color: ${a.color}; stroke: ${a.color};`"
            marker-end="url(#interval-arrowhead)"
            class="arrow-line"
          />
        </g>

        <g class="formula-panel">
          <rect :x="svgWidth - 270" y="60" width="250" :height="splitLines.length ? 60 + splitLines.length * 22 : 110" rx="10" />
          <text :x="svgWidth - 145" y="86" text-anchor="middle" class="panel-heading">transition</text>
          <text :x="svgWidth - 145" y="112" text-anchor="middle" class="formula-text">{{ currentStep.formula }}</text>
          <text
            v-for="(s, idx) in splitLines"
            :key="`split-${idx}`"
            :x="svgWidth - 258"
            :y="140 + idx * 22"
            class="split-line"
          >
            k={{ s.k }} → {{ s.cost }}
          </text>
          <text v-if="currentStep.result" :x="svgWidth - 145" :y="140 + splitLines.length * 22 + 20" text-anchor="middle" class="result-text">
            {{ currentStep.result }}
          </text>
        </g>

        <g class="legend" text-anchor="start">
          <rect x="30" :y="svgHeight - 68" width="16" height="16" rx="4" class="legend-current" />
          <text x="53" :y="svgHeight - 55">current</text>
          <rect x="140" :y="svgHeight - 68" width="16" height="16" rx="4" class="legend-read" />
          <text x="163" :y="svgHeight - 55">split read</text>
          <rect x="260" :y="svgHeight - 68" width="16" height="16" rx="4" class="legend-base" />
          <text x="283" :y="svgHeight - 55">base (l=r)</text>
        </g>

        <text :x="svgWidth / 2" :y="svgHeight - 20" text-anchor="middle" class="svg-caption">
          Fill order is by diagonal: all length-1 intervals, then length-2, then length-3 …
        </text>
      </svg>

      <p class="caption">{{ currentStep.description }}</p>

      <div class="controls" aria-label="Interval DP animation controls">
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
  max-width: 860px;
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

.axis-caption,
.axis-label {
  font-family: var(--dsa-font);
  font-weight: 800;
}

.axis-caption {
  fill: var(--dsa-primary);
  font-size: var(--dsa-label-size);
}

.axis-label {
  fill: var(--dsa-neutral);
  font-size: var(--dsa-label-size);
}

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

.split-line {
  fill: var(--dsa-ink);
  font-family: var(--dsa-font);
  font-size: 13px;
  font-weight: 700;
}

.result-text {
  fill: var(--dsa-primary);
  font-family: var(--dsa-font);
  font-size: 13px;
  font-weight: 800;
}

.legend text,
.svg-caption {
  fill: var(--dsa-neutral);
  font-family: var(--dsa-font);
  font-size: var(--dsa-caption-size);
}

.dp-cell rect {
  fill: var(--dsa-bg);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 280ms ease,
    opacity 280ms ease,
    stroke 280ms ease;
}

.dp-cell text {
  fill: var(--dsa-ink);
  font-family: var(--dsa-font);
  font-size: var(--dsa-value-size);
  font-weight: 800;
}

.dp-cell.pending rect { opacity: 0.3; }
.dp-cell.base rect { fill: var(--dsa-success-soft); stroke: var(--dsa-success); }
.dp-cell.computed rect { fill: var(--dsa-bg); }

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
  stroke-width: 2;
  fill: none;
  opacity: 0.8;
}

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

.legend-base {
  fill: var(--dsa-success-soft);
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
