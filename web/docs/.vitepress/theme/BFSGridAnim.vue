<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Cell = {
  row: number
  col: number
  dist: number
}

type Step = {
  distance: number
  queue: Cell[]
  caption: string
}

const gridSize = 5
const cellSize = 30
const gap = 4
const gridX = 34
const gridY = 58
const step = cellSize + gap

const cells: Cell[] = Array.from({ length: gridSize * gridSize }, (_, index) => {
  const row = Math.floor(index / gridSize)
  const col = index % gridSize
  return { row, col, dist: row + col }
})

function frontier(distance: number) {
  return cells.filter((cell) => cell.dist === distance)
}

const steps: Step[] = [0, 1, 2, 3, 4].map((distance) => {
  const queue = frontier(distance)
  return {
    distance,
    queue,
    caption:
      distance === 0
        ? 'distance 0 source — (0,0) starts the BFS queue.'
        : `distance ${distance} wave — ${queue.length} cells reached${distance === 4 ? '; the ripple keeps spreading.' : '.'}`
  }
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

function queueX(index: number) {
  return 264 + (index % 2) * 108
}

function queueY(index: number) {
  return 94 + Math.floor(index / 2) * 34
}

function isReached(cell: Cell) {
  return cell.dist <= currentStep.value.distance
}

function cellClass(cell: Cell) {
  return {
    source: cell.dist === 0 && isReached(cell),
    active: cell.dist === currentStep.value.distance && currentStep.value.distance !== 0,
    reached: cell.dist < currentStep.value.distance,
    pending: !isReached(cell)
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
        <h3>BFS on a 5×5 grid</h3>
        <span class="counter">Step {{ current + 1 }} / {{ steps.length }}</span>
      </div>

      <svg
        class="anim-svg"
        viewBox="0 0 520 245"
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-label="BFS distance layers spreading across a five by five grid"
      >
        <rect class="svg-bg" x="0" y="0" width="520" height="245" rx="12" />

        <text class="svg-title" x="119" y="28" text-anchor="middle">layers = shortest distance</text>
        <text class="queue-title" x="352" y="28" text-anchor="middle">queue grows by frontier</text>

        <g class="grid" text-anchor="middle">
          <g v-for="cell in cells" :key="`${cell.row}-${cell.col}`" class="grid-cell" :class="cellClass(cell)">
            <rect :x="cellX(cell)" :y="cellY(cell)" :width="cellSize" :height="cellSize" rx="6" />
            <text
              v-if="isReached(cell)"
              :x="cellX(cell) + cellSize / 2"
              :y="cellY(cell) + 20"
              class="distance-label"
            >
              {{ cell.dist }}
            </text>
            <text v-else :x="cellX(cell) + cellSize / 2" :y="cellY(cell) + 20" class="dot-label">·</text>
          </g>
        </g>

        <rect class="queue-panel" x="238" y="52" width="244" height="146" rx="10" />
        <text class="queue-heading" x="258" y="75">queue: [</text>
        <g v-for="(cell, index) in currentStep.queue" :key="`q-${cell.row}-${cell.col}`" class="queue-chip">
          <rect :x="queueX(index)" :y="queueY(index)" width="84" height="24" rx="7" />
          <text :x="queueX(index) + 42" :y="queueY(index) + 16" text-anchor="middle">({{ cell.row }},{{ cell.col }})</text>
        </g>
        <text class="queue-heading" x="258" y="184">]</text>

        <g class="legend" text-anchor="start">
          <rect x="42" y="207" width="12" height="12" rx="3" class="legend-source" />
          <text x="60" y="217">source</text>
          <rect x="124" y="207" width="12" height="12" rx="3" class="legend-frontier" />
          <text x="142" y="217">fresh wave</text>
          <rect x="232" y="207" width="12" height="12" rx="3" class="legend-reached" />
          <text x="250" y="217">already reached</text>
        </g>
      </svg>

      <p class="caption">{{ currentStep.caption }}</p>

      <div class="controls" aria-label="BFS grid animation controls">
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
.queue-title {
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

.grid-cell.pending rect {
  opacity: 0.72;
}

.grid-cell.reached rect {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary-line);
}

.grid-cell.source rect {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-outline-stroke);
}

.grid-cell.active rect {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-outline-stroke);
  transform: translateY(-2px);
}

.distance-label,
.dot-label {
  fill: var(--dsa-ink);
  font: 800 13px var(--dsa-font);
}

.dot-label {
  fill: var(--dsa-neutral);
}

.queue-panel {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
}

.queue-heading {
  fill: var(--dsa-ink);
  font: 800 13px var(--dsa-font);
}

.queue-chip rect {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 320ms ease,
    stroke 320ms ease;
}

.queue-chip text,
.legend text {
  fill: var(--dsa-ink);
  font: 700 12px var(--dsa-font);
}

.legend-source {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
}

.legend-frontier {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
}

.legend-reached {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary-line);
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
