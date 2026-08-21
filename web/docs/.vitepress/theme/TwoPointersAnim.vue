<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type PointerMove = 'left' | 'right' | null

type Step = {
  left: number
  right: number
  sum: number
  comparison: string
  move: PointerMove
  found: boolean
  description: string
}

const values = [-4, -1, 0, 1, 3, 5, 8]
const target = 2
const cellWidth = 44
const gap = 12
const startX = 170
const cellY = 104
const stepX = cellWidth + gap

const steps: Step[] = [
  {
    left: 0,
    right: 6,
    sum: 4,
    comparison: '4 > 2',
    move: 'right',
    found: false,
    description: '-4 + 8 = 4 is too large, so shrink the sum by moving right left.'
  },
  {
    left: 0,
    right: 5,
    sum: 1,
    comparison: '1 < 2',
    move: 'left',
    found: false,
    description: '-4 + 5 = 1 is too small, so grow the sum by moving left right.'
  },
  {
    left: 1,
    right: 5,
    sum: 4,
    comparison: '4 > 2',
    move: 'right',
    found: false,
    description: '-1 + 5 = 4 is too large, so move right left again.'
  },
  {
    left: 1,
    right: 4,
    sum: 2,
    comparison: '2 = 2',
    move: null,
    found: true,
    description: 'Match found: [-1, 3] reaches the target exactly.'
  }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const resultTone = computed(() => {
  if (currentStep.value.found) return 'var(--dsa-success)'
  return currentStep.value.move === 'right' ? 'var(--dsa-danger)' : 'var(--dsa-primary)'
})

function cellX(index: number) {
  return startX + index * stepX
}

function pointerX(index: number) {
  return cellX(index) + cellWidth / 2
}

function cellClass(index: number) {
  const step = currentStep.value
  return {
    left: !step.found && index === step.left,
    right: !step.found && index === step.right,
    found: step.found && (index === step.left || index === step.right)
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
  <div class="anim-card">
    <svg
      class="anim-svg"
      width="720"
      height="260"
      viewBox="0 0 720 260"
      xmlns="http://www.w3.org/2000/svg"
      font-family="var(--dsa-font)"
      role="img"
      aria-label="Interactive two pointers target sum animation"
    >
      <defs>
        <marker id="tp-anim-primary" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)" />
        </marker>
        <marker id="tp-anim-success" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)" />
        </marker>
        <filter id="tp-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="var(--dsa-neutral-line)" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="260" rx="12" fill="var(--dsa-bg)" />
      <text x="360" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--dsa-primary)">
        Two pointers walk — target = {{ target }}
      </text>

      <g
        class="pointer pointer-left"
        :style="{ transform: `translateX(${pointerX(currentStep.left)}px)` }"
      >
        <text x="0" y="58" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">
          left
        </text>
        <line
          x1="0"
          y1="64"
          x2="0"
          y2="96"
          stroke="var(--dsa-primary)"
          stroke-width="var(--dsa-arrow-stroke)"
          marker-end="url(#tp-anim-primary)"
        />
      </g>

      <g
        class="pointer pointer-right"
        :style="{ transform: `translateX(${pointerX(currentStep.right)}px)` }"
      >
        <text x="0" y="58" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-success)">
          right
        </text>
        <line
          x1="0"
          y1="64"
          x2="0"
          y2="96"
          stroke="var(--dsa-success)"
          stroke-width="var(--dsa-arrow-stroke)"
          marker-end="url(#tp-anim-success)"
        />
      </g>

      <g filter="url(#tp-anim-shadow)">
        <g v-for="(value, index) in values" :key="index" class="array-cell" :class="cellClass(index)">
          <rect :x="cellX(index)" :y="cellY" :width="cellWidth" height="44" rx="7" />
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
            class="index-label"
            :x="cellX(index) + cellWidth / 2"
            :y="cellY + 62"
            text-anchor="middle"
            font-size="11"
          >
            {{ index }}
          </text>
        </g>
      </g>

      <rect x="226" y="180" width="268" height="52" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" />
      <text x="360" y="201" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">
        sum = {{ values[currentStep.left] }} + {{ values[currentStep.right] }} = {{ currentStep.sum }}
      </text>
      <text x="360" y="222" text-anchor="middle" font-size="13" font-weight="800" :fill="resultTone">
        {{ currentStep.found ? 'Found: [-1, 3]' : `${currentStep.comparison} → move ${currentStep.move}` }}
      </text>

      <text x="360" y="250" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-neutral)">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Two pointers animation controls">
      <button type="button" :disabled="current === 0" @click="prev">◀ Prev</button>
      <button type="button" @click="togglePlay">{{ playing ? '⏸ Pause' : '▶ Play' }}</button>
      <button type="button" :disabled="current === steps.length - 1" @click="next">Next ▶</button>
      <button type="button" @click="reset">⟳ Reset</button>
      <span class="counter">Step {{ current + 1 }} / {{ steps.length }}</span>
    </div>
  </div>
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

.anim-svg {
  display: block;
  width: 100%;
  height: auto;
}

.pointer {
  transition: transform 600ms ease;
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

.array-cell.left rect {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
  transform: translateY(-3px);
}

.array-cell.right rect {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
  transform: translateY(-3px);
}

.array-cell.found rect {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-outline-stroke);
  transform: translateY(-3px);
}

.array-cell text {
  fill: var(--dsa-ink);
}

.array-cell .index-label {
  fill: var(--dsa-neutral);
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
  margin-left: auto;
  color: var(--dsa-neutral);
  font: 600 13px var(--dsa-font);
}
</style>
