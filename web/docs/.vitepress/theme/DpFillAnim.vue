<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type CellCoord = { i: number; j: number }
type Step = {
  revealBase: boolean
  revealOrder: number
  cell: CellCoord | null
  deps: CellCoord[]
  formula: string
  result: string
  description: string
}

const xChars = ['', 'A', 'G', 'C', 'A', 'T']
const yChars = ['', 'G', 'A', 'C']
const colIndices = [0, 1, 2, 3, 4, 5]
const rowIndices = [0, 1, 2, 3]
const cellSize = 40
const tableX = 236
const tableY = 86

const dp = [
  [0, 0, 0, 0],
  [0, 0, 1, 1],
  [0, 1, 1, 1],
  [0, 1, 1, 2],
  [0, 1, 2, 2],
  [0, 1, 2, 2]
]

const fillOrder = new Map<string, number>([
  ['1-1', 1],
  ['1-2', 2],
  ['1-3', 3],
  ['2-1', 4],
  ['2-2', 5],
  ['2-3', 6],
  ['3-1', 7],
  ['3-2', 8],
  ['3-3', 9],
  ['4-1', 10],
  ['4-2', 11],
  ['4-3', 12],
  ['5-1', 13],
  ['5-2', 14],
  ['5-3', 15]
])

const matchCells = new Set(['1-2', '2-1', '3-3', '4-2'])

const steps: Step[] = [
  {
    revealBase: true,
    revealOrder: 0,
    cell: null,
    deps: [],
    formula: 'dp[0][*] = 0 and dp[*][0] = 0',
    result: 'Base cases ready',
    description: 'Initialize the empty-prefix row and column to zero.'
  },
  {
    revealBase: true,
    revealOrder: 1,
    cell: { i: 1, j: 1 },
    deps: [
      { i: 0, j: 1 },
      { i: 1, j: 0 }
    ],
    formula: 'max(dp[0][1], dp[1][0]) = 0',
    result: 'A vs G: miss',
    description: 'A and G differ, so carry the best value from top or left.'
  },
  {
    revealBase: true,
    revealOrder: 2,
    cell: { i: 1, j: 2 },
    deps: [{ i: 0, j: 1 }],
    formula: 'dp[0][1] + 1 = 1',
    result: 'A vs A: match',
    description: 'Matching characters extend the diagonal subproblem by one.'
  },
  {
    revealBase: true,
    revealOrder: 3,
    cell: { i: 1, j: 3 },
    deps: [
      { i: 0, j: 3 },
      { i: 1, j: 2 }
    ],
    formula: 'max(dp[0][3], dp[1][2]) = 1',
    result: 'A vs C: miss',
    description: 'A does not match C, so the previous A/A match remains best.'
  },
  {
    revealBase: true,
    revealOrder: 4,
    cell: { i: 2, j: 1 },
    deps: [{ i: 1, j: 0 }],
    formula: 'dp[1][0] + 1 = 1',
    result: 'G vs G: match',
    description: 'The G match starts another length-one subsequence.'
  },
  {
    revealBase: true,
    revealOrder: 5,
    cell: { i: 2, j: 2 },
    deps: [
      { i: 1, j: 2 },
      { i: 2, j: 1 }
    ],
    formula: 'max(dp[1][2], dp[2][1]) = 1',
    result: 'G vs A: miss',
    description: 'On a miss, choose the stronger of dropping G or dropping A.'
  },
  {
    revealBase: true,
    revealOrder: 9,
    cell: { i: 3, j: 3 },
    deps: [{ i: 2, j: 2 }],
    formula: 'dp[2][2] + 1 = 2',
    result: 'C vs C: match',
    description: 'After a few misses, C matches C and raises the best length to two.'
  },
  {
    revealBase: true,
    revealOrder: 11,
    cell: { i: 4, j: 2 },
    deps: [{ i: 3, j: 1 }],
    formula: 'dp[3][1] + 1 = 2',
    result: 'A vs A: match',
    description: 'A later A match also reaches length two, such as GA.'
  },
  {
    revealBase: true,
    revealOrder: 15,
    cell: { i: 5, j: 3 },
    deps: [
      { i: 4, j: 3 },
      { i: 5, j: 2 }
    ],
    formula: 'max(dp[4][3], dp[5][2]) = 2',
    result: 'T vs C: miss',
    description: 'Final answer: dp[5][3] = 2, so the LCS length is 2.'
  }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const compared = computed(() => {
  const cell = currentStep.value.cell
  if (!cell) return null
  return { left: xChars[cell.i], right: yChars[cell.j] }
})

function key(i: number, j: number) {
  return `${i}-${j}`
}

function cellX(i: number) {
  return tableX + i * cellSize
}

function cellY(j: number) {
  return tableY + j * cellSize
}

function isBase(i: number, j: number) {
  return i === 0 || j === 0
}

function isComputed(i: number, j: number) {
  if (isBase(i, j)) return currentStep.value.revealBase
  const order = fillOrder.get(key(i, j))
  return order !== undefined && order <= currentStep.value.revealOrder
}

function cellValue(i: number, j: number) {
  return isComputed(i, j) ? dp[i][j] : ''
}

function isCurrent(i: number, j: number) {
  const cell = currentStep.value.cell
  return Boolean(cell && cell.i === i && cell.j === j)
}

function isDependency(i: number, j: number) {
  return currentStep.value.deps.some((dep) => dep.i === i && dep.j === j)
}

function isMatch(i: number, j: number) {
  return isComputed(i, j) && matchCells.has(key(i, j))
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
  timer.value = setInterval(next, 1300)
}

onBeforeUnmount(stop)
</script>

<template>
  <ClientOnly>
    <div class="anim-card">
      <div class="anim-title">LCS tabulation: AGCAT × GAC</div>
      <svg
        class="anim-svg"
        width="720"
        height="300"
        viewBox="0 0 720 300"
        xmlns="http://www.w3.org/2000/svg"
        font-family="var(--dsa-font)"
        role="img"
        aria-label="Interactive dynamic programming table fill animation for longest common subsequence"
      >
        <rect x="0" y="0" width="720" height="300" rx="12" class="surface" />

        <g class="compare-panel">
          <rect x="22" y="48" width="184" height="104" rx="10" />
          <text x="114" y="73" text-anchor="middle" class="panel-heading">compare</text>
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
            x="220"
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
              <rect width="40" height="40" rx="7" />
              <text x="20" y="26" text-anchor="middle">{{ cellValue(i, j) }}</text>
            </g>
          </g>
        </g>

        <g class="formula-panel">
          <rect x="506" y="70" width="190" height="116" rx="10" />
          <text x="601" y="96" text-anchor="middle" class="panel-heading">transition</text>
          <text x="601" y="124" text-anchor="middle" class="formula-text">{{ currentStep.result }}</text>
          <text x="601" y="150" text-anchor="middle" class="formula-text">{{ currentStep.formula }}</text>
          <text x="601" y="171" text-anchor="middle" class="hint-text">dashed cells are reads</text>
        </g>

        <g class="legend" text-anchor="start">
          <rect x="30" y="188" width="16" height="16" rx="4" class="legend-current" />
          <text x="53" y="201">current</text>
          <rect x="30" y="214" width="16" height="16" rx="4" class="legend-read" />
          <text x="53" y="227">dependency</text>
          <rect x="30" y="240" width="16" height="16" rx="4" class="legend-match" />
          <text x="53" y="253">match</text>
        </g>

        <text x="360" y="282" text-anchor="middle" class="svg-caption">
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
.svg-caption {
  font-family: var(--dsa-font);
}

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
.svg-caption {
  fill: var(--dsa-neutral);
}

.versus {
  font-size: var(--dsa-label-size);
  font-weight: 800;
}

.base-label,
.formula-text {
  font-size: var(--dsa-label-size);
  font-weight: 700;
}

.formula-text {
  fill: var(--dsa-ink);
}

.hint-text,
.legend text,
.svg-caption {
  font-size: var(--dsa-caption-size);
}

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

.dp-cell.pending rect {
  opacity: 0.38;
}

.dp-cell.base rect {
  fill: var(--dsa-neutral-soft);
}

.dp-cell.computed rect {
  fill: var(--dsa-bg);
}

.dp-cell.match rect {
  fill: var(--dsa-success);
  stroke: var(--dsa-success);
}

.dp-cell.match text {
  fill: var(--dsa-bg);
}

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
