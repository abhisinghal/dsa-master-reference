<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Step = {
  lo: number
  hi: number
  mid: number
  comparison: string
  result: string
  found: boolean
  description: string
}

const values = [1, 3, 5, 7, 9, 11, 13, 15, 17]
const target = 11
const cellWidth = 44
const cellHeight = 44
const gap = 8
const stepX = cellWidth + gap
const startX = 130
const cellY = 82

const steps: Step[] = [
  {
    lo: 0,
    hi: 8,
    mid: 4,
    comparison: '9 < 11',
    result: 'search right half',
    found: false,
    description: 'The middle value 9 is too small, so every value at index 4 or left can be discarded.'
  },
  {
    lo: 5,
    hi: 8,
    mid: 6,
    comparison: '13 > 11',
    result: 'search left half',
    found: false,
    description: 'The middle value 13 is too large, so the target must be left of index 6.'
  },
  {
    lo: 5,
    hi: 5,
    mid: 5,
    comparison: '11 == 11',
    result: 'found target',
    found: true,
    description: 'The active window has collapsed to index 5, where the value equals the target.'
  }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const bracketX = computed(() => startX + currentStep.value.lo * stepX - 6)
const bracketWidth = computed(() => (currentStep.value.hi - currentStep.value.lo + 1) * cellWidth + (currentStep.value.hi - currentStep.value.lo) * gap + 12)
const bracketLabelX = computed(() => bracketX.value + bracketWidth.value / 2)
const stateLabel = computed(
  () => `lo=${currentStep.value.lo}, mid=${currentStep.value.mid}, hi=${currentStep.value.hi}`
)

function cellX(index: number) {
  return startX + index * stepX
}

function inRange(index: number) {
  return index >= currentStep.value.lo && index <= currentStep.value.hi
}

function cellClass(index: number) {
  return {
    'in-range': inRange(index),
    mid: currentStep.value.mid === index,
    found: currentStep.value.found && currentStep.value.mid === index,
    discarded: !inRange(index)
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
  <ClientOnly>
    <div class="anim-card">
      <div class="anim-header">
        <h3>Binary search for target = {{ target }}</h3>
        <span class="counter">Step {{ current + 1 }} / {{ steps.length }}</span>
      </div>

      <svg
        class="anim-svg"
        width="720"
        height="255"
        viewBox="0 0 720 255"
        xmlns="http://www.w3.org/2000/svg"
        font-family="var(--dsa-font)"
        role="img"
        aria-label="Interactive binary search animation"
      >
        <rect x="0" y="0" width="720" height="255" rx="12" fill="var(--dsa-bg)" />

        <text x="360" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="var(--dsa-primary)">
          ordered data lets one comparison discard half the window
        </text>

        <g class="window-outline">
          <rect
            :x="bracketX"
            y="70"
            :width="bracketWidth"
            height="68"
            rx="10"
            fill="none"
            stroke="var(--dsa-primary)"
            stroke-width="var(--dsa-outline-stroke)"
          />
        </g>
        <text
          class="window-label"
          :x="bracketLabelX"
          y="62"
          text-anchor="middle"
          font-size="12"
          font-weight="700"
          fill="var(--dsa-primary)"
        >
          active [{{ currentStep.lo }}, {{ currentStep.hi }}]
        </text>

        <g>
          <g v-for="(value, index) in values" :key="index" class="array-cell" :class="cellClass(index)">
            <rect :x="cellX(index)" :y="cellY" :width="cellWidth" :height="cellHeight" rx="7" />
            <text
              :x="cellX(index) + cellWidth / 2"
              :y="cellY + 28"
              text-anchor="middle"
              font-size="17"
              font-weight="700"
            >
              {{ value }}
            </text>
            <text
              :x="cellX(index) + cellWidth / 2"
              :y="cellY + 62"
              text-anchor="middle"
              font-size="11"
            >
              {{ index }}
            </text>
          </g>
        </g>

        <g class="pointer-labels" font-size="11" font-weight="700" text-anchor="middle">
          <text :x="cellX(currentStep.lo) + cellWidth / 2" y="158" :class="{ active: currentStep.lo === currentStep.mid }">
            lo
          </text>
          <text :x="cellX(currentStep.mid) + cellWidth / 2" y="176" class="active">mid</text>
          <text :x="cellX(currentStep.hi) + cellWidth / 2" y="158" :class="{ active: currentStep.hi === currentStep.mid }">
            hi
          </text>
        </g>

        <g v-if="currentStep.found" class="found-label">
          <rect :x="cellX(currentStep.mid) - 8" y="38" width="60" height="24" rx="8" />
          <text :x="cellX(currentStep.mid) + cellWidth / 2" y="55" text-anchor="middle" font-size="11" font-weight="800">
            FOUND
          </text>
        </g>

        <rect x="214" y="190" width="292" height="42" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" />
        <text x="360" y="207" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">
          {{ stateLabel }} · {{ currentStep.comparison }}
        </text>
        <text x="360" y="225" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">
          {{ currentStep.result }}
        </text>

        <text x="360" y="247" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">
          {{ currentStep.description }}
        </text>
      </svg>

      <p class="anim-caption">
        Track the blue bracket first, then inspect the primary mid cell; each comparison shrinks the candidate range.
      </p>

      <div class="controls" aria-label="Binary search animation controls">
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

.window-outline rect,
.window-label {
  transition:
    x 600ms ease,
    width 600ms ease;
}

.array-cell rect {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    opacity 320ms ease,
    transform 320ms ease;
}

.array-cell text {
  fill: var(--dsa-ink);
}

.array-cell text:last-child {
  fill: var(--dsa-neutral);
}

.array-cell.in-range rect {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary-line);
}

.array-cell.mid rect {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
  stroke-width: var(--dsa-outline-stroke);
  transform: translateY(-3px);
}

.array-cell.found rect {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-outline-stroke);
}

.array-cell.discarded {
  opacity: 0.45;
}

.pointer-labels text {
  fill: var(--dsa-neutral);
}

.pointer-labels text.active {
  fill: var(--dsa-primary);
}

.found-label rect {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
}

.found-label text {
  fill: var(--dsa-success);
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
