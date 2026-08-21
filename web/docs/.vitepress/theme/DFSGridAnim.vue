<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Cell = {
  row: number
  col: number
  obstacle?: boolean
}

type Step = {
  visited: Cell[]
  active: Cell
  backtracked: Cell[]
  blocked?: Cell
  path?: Cell[]
  status: string[]
  caption: string
}

const gridSize = 4
const cellSize = 30
const gap = 4
const gridX = 42
const gridY = 58
const step = cellSize + gap

const obstacles: Cell[] = [
  { row: 1, col: 1 },
  { row: 2, col: 2 }
]

const start: Cell = { row: 0, col: 0 }
const target: Cell = { row: 3, col: 3 }

function sameCell(a: Cell, b: Cell) {
  return a.row === b.row && a.col === b.col
}

function contains(cells: Cell[], cell: Cell) {
  return cells.some((candidate) => sameCell(candidate, cell))
}

function c(row: number, col: number): Cell {
  return { row, col }
}

const visit1 = [c(0, 0)]
const visit2 = [...visit1, c(0, 1)]
const visit3 = [...visit2, c(0, 2)]
const visit4 = [...visit3, c(0, 3)]
const visit5 = [...visit4, c(1, 3)]
const visit6 = [...visit5, c(1, 2)]
const visit7 = [...visit6, c(2, 3)]
const visit8 = [...visit7, c(3, 3)]
const deadBranch = [c(1, 2)]
const finalPath = [c(0, 0), c(0, 1), c(0, 2), c(0, 3), c(1, 3), c(2, 3), c(3, 3)]

const steps: Step[] = [
  {
    visited: visit1,
    active: c(0, 0),
    backtracked: [],
    status: ['visit #1 at (0,0)', 'try right first'],
    caption: 'step 1: start at (0,0); DFS marks before exploring neighbours.'
  },
  {
    visited: visit2,
    active: c(0, 1),
    backtracked: [],
    status: ['at (0,0)', 'try right → (0,1)'],
    caption: 'step 2: right is open, so (0,1) becomes visit #2.'
  },
  {
    visited: visit3,
    active: c(0, 2),
    backtracked: [],
    status: ['at (0,1)', 'try right → (0,2)'],
    caption: 'step 3: keep following the right-first branch to visit #3.'
  },
  {
    visited: visit4,
    active: c(0, 3),
    backtracked: [],
    status: ['at (0,2)', 'try right → (0,3)'],
    caption: 'step 4: the top row branch reaches visit #4 at the edge.'
  },
  {
    visited: visit5,
    active: c(1, 3),
    backtracked: [],
    status: ['at (0,3)', 'try down → (1,3)'],
    caption: 'step 5: right is outside, so DFS descends to visit #5.'
  },
  {
    visited: visit6,
    active: c(1, 2),
    backtracked: [],
    status: ['at (1,3)', 'try left → (1,2)'],
    caption: 'step 6: the left turn explores a side branch as visit #6.'
  },
  {
    visited: visit6,
    active: c(1, 2),
    backtracked: [],
    blocked: c(1, 1),
    status: ['at (1,2)', 'try left → obstacle'],
    caption: 'step 7: hit obstacle at (1,1); this neighbour is skipped.'
  },
  {
    visited: visit6,
    active: c(1, 2),
    backtracked: deadBranch,
    blocked: c(2, 2),
    status: ['try down → obstacle', 'no moves; backtrack'],
    caption: 'step 8: (2,2) is blocked too, so (1,2) fades as a dead branch.'
  },
  {
    visited: visit7,
    active: c(2, 3),
    backtracked: deadBranch,
    status: ['back at (1,3)', 'try down → (2,3)'],
    caption: 'step 9: after backtracking, DFS resumes and visits (2,3) as #7.'
  },
  {
    visited: visit7,
    active: c(2, 3),
    backtracked: deadBranch,
    blocked: c(2, 2),
    status: ['at (2,3)', 'try left → obstacle'],
    caption: 'step 10: another obstacle check keeps the search on the open corridor.'
  },
  {
    visited: visit8,
    active: c(3, 3),
    backtracked: deadBranch,
    path: finalPath,
    status: ['try down → target', 'path found'],
    caption: 'step 11: target (3,3) is found; the successful DFS path turns primary.'
  }
]

const cells: Cell[] = Array.from({ length: gridSize * gridSize }, (_, index) => {
  const row = Math.floor(index / gridSize)
  const col = index % gridSize
  return { row, col, obstacle: contains(obstacles, { row, col }) }
})

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])

function cellX(cell: Cell) {
  return gridX + cell.col * step
}

function cellY(cell: Cell) {
  return gridY + cell.row * step
}

function isVisited(cell: Cell) {
  return contains(currentStep.value.visited, cell)
}

function isActive(cell: Cell) {
  return sameCell(currentStep.value.active, cell)
}

function isBacktracked(cell: Cell) {
  return contains(currentStep.value.backtracked, cell)
}

function isBlocked(cell: Cell) {
  return currentStep.value.blocked ? sameCell(currentStep.value.blocked, cell) : false
}

function inPath(cell: Cell) {
  return currentStep.value.path ? contains(currentStep.value.path, cell) : false
}

function isStart(cell: Cell) {
  return sameCell(start, cell)
}

function isTarget(cell: Cell) {
  return sameCell(target, cell)
}

function visitNumber(cell: Cell) {
  const index = currentStep.value.visited.findIndex((visitedCell) => sameCell(visitedCell, cell))
  return index === -1 ? null : index + 1
}

function cellLabel(cell: Cell) {
  const number = visitNumber(cell)
  if (number !== null) return String(number)
  if (cell.obstacle) return '×'
  if (isStart(cell)) return 'S'
  if (isTarget(cell)) return 'T'
  return ''
}

function cellClass(cell: Cell) {
  return {
    obstacle: cell.obstacle,
    visited: isVisited(cell),
    active: isActive(cell),
    backtracked: isBacktracked(cell),
    blocked: isBlocked(cell),
    path: inPath(cell),
    start: isStart(cell),
    target: isTarget(cell)
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
  <ClientOnly>
    <div class="anim-card">
      <div class="anim-header">
        <h3>DFS on a 4×4 grid</h3>
        <span class="counter">Step {{ current + 1 }} / {{ steps.length }}</span>
      </div>

      <svg
        class="anim-svg"
        viewBox="0 0 520 245"
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-label="DFS visits, backtracks, and finds a target in a four by four grid"
      >
        <rect class="svg-bg" x="0" y="0" width="520" height="245" rx="12" />

        <text class="svg-title" x="111" y="28" text-anchor="middle">right-first DFS trace</text>
        <text class="status-title" x="352" y="28" text-anchor="middle">current decision</text>

        <g class="grid" text-anchor="middle">
          <g v-for="cell in cells" :key="`${cell.row}-${cell.col}`" class="grid-cell" :class="cellClass(cell)">
            <rect :x="cellX(cell)" :y="cellY(cell)" :width="cellSize" :height="cellSize" rx="6" />
            <text :x="cellX(cell) + cellSize / 2" :y="cellY(cell) + 20" class="cell-label">
              {{ cellLabel(cell) }}
            </text>
          </g>
        </g>

        <rect class="status-panel" x="220" y="52" width="262" height="126" rx="10" />
        <text class="direction-order" x="352" y="77" text-anchor="middle">try order: right → left → down → up</text>
        <g class="status-lines">
          <text v-for="(line, index) in currentStep.status" :key="line" x="352" :y="110 + index * 24" text-anchor="middle">
            {{ line }}
          </text>
        </g>

        <g class="legend" text-anchor="start">
          <rect x="42" y="207" width="12" height="12" rx="3" class="legend-path" />
          <text x="60" y="217">found path</text>
          <rect x="150" y="207" width="12" height="12" rx="3" class="legend-backtrack" />
          <text x="168" y="217">backtracked</text>
          <rect x="280" y="207" width="12" height="12" rx="3" class="legend-obstacle" />
          <text x="298" y="217">obstacle</text>
        </g>
      </svg>

      <p class="caption">{{ currentStep.caption }}</p>

      <div class="controls" aria-label="DFS grid animation controls">
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
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.anim-header h3 {
  margin: 0;
  color: var(--dsa-ink);
  font: 800 15px var(--dsa-font);
}

.counter {
  margin-left: auto;
  color: var(--dsa-neutral);
  font: 600 13px var(--dsa-font);
  white-space: nowrap;
}

.anim-svg {
  display: block;
  width: 100%;
  height: auto;
}

.svg-bg {
  fill: var(--dsa-bg);
}

.svg-title,
.status-title {
  fill: var(--dsa-primary);
  font: 700 var(--dsa-label-size) var(--dsa-font);
}

.grid-cell rect {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    transform 320ms ease,
    opacity 320ms ease;
}

.grid-cell.start:not(.visited) rect {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
}

.grid-cell.target:not(.visited) rect {
  fill: var(--dsa-warning-soft);
  stroke: var(--dsa-warning);
}

.grid-cell.obstacle rect {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral);
  stroke-width: var(--dsa-outline-stroke);
}

.grid-cell.visited rect {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
}

.grid-cell.active rect {
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-outline-stroke);
  transform: translateY(-2px);
}

.grid-cell.blocked rect {
  fill: var(--dsa-danger-soft);
  stroke: var(--dsa-danger);
  stroke-width: var(--dsa-outline-stroke);
}

.grid-cell.backtracked rect {
  fill: var(--dsa-danger-soft);
  stroke: var(--dsa-danger-line);
  opacity: 0.58;
  transform: translateY(0);
}

.grid-cell.path rect {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-outline-stroke);
  opacity: 1;
}

.cell-label {
  fill: var(--dsa-ink);
  font: 800 13px var(--dsa-font);
}

.status-panel {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
}

.direction-order {
  fill: var(--dsa-neutral);
  font: 800 12px var(--dsa-font);
}

.status-lines text {
  fill: var(--dsa-ink);
  font: 800 16px var(--dsa-font);
}

.legend text {
  fill: var(--dsa-ink);
  font: 700 12px var(--dsa-font);
}

.legend-path {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
}

.legend-backtrack {
  fill: var(--dsa-danger-soft);
  stroke: var(--dsa-danger);
}

.legend-obstacle {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral);
}

.caption {
  margin: 10px 2px 0;
  color: var(--dsa-neutral);
  font: 700 var(--dsa-caption-size) var(--dsa-font);
  font-style: italic;
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
</style>
