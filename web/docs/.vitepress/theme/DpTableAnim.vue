<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type CellCoord = { i: number; j: number }

type Step = {
  revealBase?: boolean
  revealOrder: number
  cell: CellCoord | null
  deps?: CellCoord[]
  formula: string
  result: string
  description: string
}

type Props = {
  title: string
  xChars: string[]
  yChars: string[]
  dp: number[][]
  fillOrder: Record<string, number>
  matchCells?: string[]
  steps: Step[]
  showCompare?: boolean
  compareLabel?: string
  transitionLabel?: string
  cellSize?: number
}

const props = withDefaults(defineProps<Props>(), {
  matchCells: () => [],
  showCompare: true,
  compareLabel: 'compare',
  transitionLabel: 'transition',
  cellSize: 40
})

const matchSet = computed(() => new Set(props.matchCells))

const colIndices = computed(() => Array.from({ length: props.xChars.length }, (_, i) => i))
const rowIndices = computed(() => Array.from({ length: props.yChars.length }, (_, j) => j))

const tableX = computed(() => (props.showCompare ? 236 : 60))
const tableY = 86
const tableWidth = computed(() => props.xChars.length * props.cellSize)
const tableHeight = computed(() => props.yChars.length * props.cellSize)

const svgWidth = computed(() => Math.max(720, tableX.value + tableWidth.value + 220))

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => props.steps[current.value])
const compared = computed(() => {
  const cell = currentStep.value.cell
  if (!cell) return null
  return { left: props.xChars[cell.i] ?? '', right: props.yChars[cell.j] ?? '' }
})

function key(i: number, j: number) {
  return `${i}-${j}`
}

function cellX(i: number) {
  return tableX.value + i * props.cellSize
}

function cellY(j: number) {
  return tableY + j * props.cellSize
}

function isBase(i: number, j: number) {
  return i === 0 || j === 0
}

function isComputed(i: number, j: number) {
  if (isBase(i, j)) return currentStep.value.revealBase !== false
  const order = props.fillOrder[key(i, j)]
  return order !== undefined && order <= currentStep.value.revealOrder
}

function cellValue(i: number, j: number): string | number {
  return isComputed(i, j) ? props.dp[i]?.[j] ?? '' : ''
}

function isCurrent(i: number, j: number) {
  const cell = currentStep.value.cell
  return Boolean(cell && cell.i === i && cell.j === j)
}

function isDependency(i: number, j: number) {
  return (currentStep.value.deps ?? []).some((dep) => dep.i === i && dep.j === j)
}

function isMatch(i: number, j: number) {
  return isComputed(i, j) && matchSet.value.has(key(i, j))
}

function cellClass(i: number, j: number) {
  return {
    base: isBase(i, j) && isComputed(i, j),
    computed: isComputed(i, j) && !isBase(i, j),
    match: isMatch(i, j),
    current: isCurrent(i, j),
    dependency: isDependency(i, j),
    pending: !isComputed(i, j)
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
        height="300"
        :viewBox="`0 0 ${svgWidth} 300`"
        xmlns="http://www.w3.org/2000/svg"
        font-family="var(--dsa-font)"
        role="img"
        :aria-label="`Interactive dynamic programming table animation for ${title}`"
      >
        <rect x="0" y="0" :width="svgWidth" height="300" rx="12" class="surface" />

        <g v-if="showCompare" class="compare-panel">
          <rect x="22" y="48" width="184" height="104" rx="10" />
          <text x="114" y="73" text-anchor="middle" class="panel-heading">{{ compareLabel }}</text>
          <template v-if="compared">
            <rect x="54" y="88" width="42" height="42" rx="8" class="char-box" />
            <rect x="132" y="88" width="42" height="42" rx="8" class="char-box" />
            <text x="75" y="116" text-anchor="middle" class="char-value">{{ compared.left }}</text>
            <text x="114" y="115" text-anchor="middle" class="versus">vs</text>
            <text x="153" y="116" text-anchor="middle" class="char-value">{{ compared.right }}</text>
          </template>
          <text v-else x="114" y="112" text-anchor="middle" class="base-label">base row + column</text>
        </g>

        <g class="table-labels" text-anchor="middle">
          <text
            v-for="i in colIndices"
            :key="`x-${i}`"
            :x="cellX(i) + cellSize / 2"
            y="76"
          >
            {{ i === 0 ? 'ε' : xChars[i] }}
          </text>
          <text
            v-for="j in rowIndices"
            :key="`y-${j}`"
            :x="tableX - 16"
            :y="cellY(j) + 25"
          >
            {{ j === 0 ? 'ε' : yChars[j] }}
          </text>
        </g>

        <g class="dp-grid">
          <g
            v-for="j in rowIndices"
            :key="`row-${j}`"
          >
            <g
              v-for="i in colIndices"
              :key="`cell-${i}-${j}`"
              class="dp-cell"
              :class="cellClass(i, j)"
              :transform="`translate(${cellX(i)}, ${cellY(j)})`"
            >
              <rect :width="cellSize" :height="cellSize" rx="7" />
              <text :x="cellSize / 2" :y="cellSize / 2 + 6" text-anchor="middle">{{ cellValue(i, j) }}</text>
            </g>
          </g>
        </g>

        <g class="formula-panel">
          <rect :x="svgWidth - 214" y="70" width="190" height="116" rx="10" />
          <text :x="svgWidth - 119" y="96" text-anchor="middle" class="panel-heading">{{ transitionLabel }}</text>
          <text :x="svgWidth - 119" y="124" text-anchor="middle" class="formula-text">{{ currentStep.result }}</text>
          <text :x="svgWidth - 119" y="150" text-anchor="middle" class="formula-text">{{ currentStep.formula }}</text>
          <text :x="svgWidth - 119" y="171" text-anchor="middle" class="hint-text">dashed cells are reads</text>
        </g>

        <g class="legend" text-anchor="start">
          <rect x="30" y="188" width="16" height="16" rx="4" class="legend-current" />
          <text x="53" y="201">current</text>
          <rect x="30" y="214" width="16" height="16" rx="4" class="legend-read" />
          <text x="53" y="227">dependency</text>
          <rect x="30" y="240" width="16" height="16" rx="4" class="legend-match" />
          <text x="53" y="253">match</text>
        </g>

        <text :x="svgWidth / 2" y="282" text-anchor="middle" class="svg-caption">
          Fill states only after their diagonal, top, or left dependencies are known.
        </text>
      </svg>

      <p class="caption">{{ currentStep.description }}</p>

      <div class="controls" aria-label="Dynamic programming table animation controls">
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

.compare-panel rect,
.formula-panel rect {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
}

.panel-heading,
.base-label,
.formula-text,
.hint-text,
.legend text,
.svg-caption { font-family: var(--dsa-font); }

.panel-heading {
  fill: var(--dsa-primary);
  font-size: var(--dsa-label-size);
  font-weight: 800;
  text-transform: uppercase;
}

.char-box {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-cell-stroke);
}

.char-value {
  fill: var(--dsa-primary);
  font-size: 22px;
  font-weight: 800;
}

.versus,
.base-label,
.hint-text,
.legend text,
.svg-caption { fill: var(--dsa-neutral); }

.versus {
  font-size: var(--dsa-label-size);
  font-weight: 800;
}

.base-label,
.formula-text {
  font-size: var(--dsa-label-size);
  font-weight: 700;
}

.formula-text { fill: var(--dsa-ink); }

.hint-text,
.legend text,
.svg-caption { font-size: var(--dsa-caption-size); }

.table-labels text {
  fill: var(--dsa-neutral);
  font-family: var(--dsa-font);
  font-size: var(--dsa-label-size);
  font-weight: 800;
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

.dp-cell.match rect {
  fill: var(--dsa-success);
  stroke: var(--dsa-success);
}

.dp-cell.match text { fill: var(--dsa-bg); }

.dp-cell.dependency rect {
  stroke: var(--dsa-info);
  stroke-width: 2.6px;
  stroke-dasharray: 5 3;
}

.dp-cell.current rect {
  stroke: var(--dsa-primary);
  stroke-width: 3px;
  stroke-dasharray: none;
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

.legend-match {
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
