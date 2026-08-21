<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Step = {
  window: [number, number]
  sum: number
  entering: number | null
  leaving: number | null
  partial?: string
  description: string
}

const values = [1, 3, 2, 6, -1, 4, 1, 8, 2]
const cellWidth = 50
const gap = 6
const stepX = cellWidth + gap
const startX = 10

const steps: Step[] = [
  {
    window: [0, 4],
    sum: 11,
    entering: null,
    leaving: null,
    partial: '1 + 3 + 2 + 6 − 1',
    description: 'Initial fixed-size window covers indices 0..4.'
  },
  {
    window: [0, 4],
    sum: 11,
    entering: null,
    leaving: 0,
    partial: 'old sum = 11',
    description: 'The leftmost value 1 is about to leave.'
  },
  {
    window: [0, 4],
    sum: 10,
    entering: null,
    leaving: 0,
    partial: '11 − 1 = 10',
    description: 'Subtract the leaving value from the running sum.'
  },
  {
    window: [1, 5],
    sum: 10,
    entering: 5,
    leaving: 0,
    partial: 'reuse indices 1..4',
    description: 'Slide the blue window one index to the right.'
  },
  {
    window: [1, 5],
    sum: 14,
    entering: 5,
    leaving: null,
    partial: '10 + 4 = 14',
    description: 'Add the incoming value 4.'
  },
  {
    window: [1, 5],
    sum: 14,
    entering: null,
    leaving: null,
    partial: 'newSum = 11 − 1 + 4',
    description: 'Window 1..5 is ready with sum 14.'
  }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const windowOffset = computed(() => currentStep.value.window[0] * stepX)
const windowLabelX = computed(() => 145 + windowOffset.value)

function inWindow(index: number) {
  const [left, right] = currentStep.value.window
  return index >= left && index <= right
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
      height="245"
      viewBox="0 0 720 245"
      xmlns="http://www.w3.org/2000/svg"
      font-family="Segoe UI, Arial, sans-serif"
      role="img"
      aria-label="Interactive sliding window animation"
    >
      <defs>
        <marker id="sw-anim-red" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#dc2626" />
        </marker>
        <marker id="sw-anim-grn" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#16a34a" />
        </marker>
        <filter id="sw-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="245" fill="#fbfcfe" />

      <text x="360" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="#0b1220">
        Fixed-size window, k = 5
      </text>

      <g class="window-outline" :style="{ transform: `translateX(${windowOffset}px)` }">
        <rect x="6" y="70" width="278" height="52" rx="9" fill="none" stroke="#2563eb" stroke-width="2.8" />
      </g>
      <text
        class="window-label"
        :x="windowLabelX"
        y="62"
        text-anchor="middle"
        font-size="12"
        fill="#2563eb"
        font-weight="700"
      >
        window {{ currentStep.window[0] }}..{{ currentStep.window[1] }} · sum = {{ currentStep.sum }}
      </text>

      <g filter="url(#sw-anim-shadow)">
        <g
          v-for="(value, index) in values"
          :key="index"
          :class="[
            'array-cell',
            {
              'in-window': inWindow(index),
              leaving: currentStep.leaving === index,
              entering: currentStep.entering === index
            }
          ]"
        >
          <rect :x="startX + index * stepX" y="76" width="50" height="40" rx="7" />
          <text :x="startX + index * stepX + 25" y="102" text-anchor="middle" font-size="18" font-weight="700">
            {{ value }}
          </text>
          <text :x="startX + index * stepX + 25" y="134" text-anchor="middle" font-size="11" fill="#94a3b8">
            {{ index }}
          </text>
        </g>
      </g>

      <g v-if="currentStep.leaving !== null" class="annotation leave-note">
        <line
          :x1="startX + currentStep.leaving * stepX + 25"
          y1="172"
          :x2="startX + currentStep.leaving * stepX + 25"
          y2="121"
          stroke="#dc2626"
          stroke-width="2"
          marker-end="url(#sw-anim-red)"
        />
        <text
          :x="startX + currentStep.leaving * stepX + 25"
          y="191"
          text-anchor="middle"
          font-size="11"
          font-weight="700"
          fill="#dc2626"
        >
          − leaves
        </text>
      </g>

      <g v-if="currentStep.entering !== null" class="annotation enter-note">
        <line
          :x1="startX + currentStep.entering * stepX + 25"
          y1="172"
          :x2="startX + currentStep.entering * stepX + 25"
          y2="121"
          stroke="#16a34a"
          stroke-width="2"
          marker-end="url(#sw-anim-grn)"
        />
        <text
          :x="startX + currentStep.entering * stepX + 25"
          y="191"
          text-anchor="middle"
          font-size="11"
          font-weight="700"
          fill="#16a34a"
        >
          + enters
        </text>
      </g>

      <rect x="524" y="74" width="188" height="76" rx="9" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="618" y="98" text-anchor="middle" font-size="12" font-weight="700" fill="#0b1220">
        running sum
      </text>
      <text x="618" y="120" text-anchor="middle" font-size="18" font-weight="800" fill="#2563eb">
        {{ currentStep.sum }}
      </text>
      <text x="618" y="140" text-anchor="middle" font-size="11" fill="#334155">{{ currentStep.partial }}</text>

      <text x="360" y="224" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Sliding window animation controls">
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
  border: 1px solid #d9dee7;
  border-radius: 10px;
  background: #fbfcfe;
}

.anim-svg {
  display: block;
  width: 100%;
  height: auto;
}

.window-outline {
  transition: transform 600ms ease;
}

.window-label {
  transition: x 600ms ease;
}

.array-cell rect {
  fill: #f8fafc;
  stroke: #cbd5e1;
  stroke-width: 1.5;
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    transform 320ms ease;
}

.array-cell.in-window rect {
  fill: #eff6ff;
  stroke: #93c5fd;
}

.array-cell.leaving rect {
  fill: #fef2f2;
  stroke: #dc2626;
  transform: translateY(-3px);
}

.array-cell.entering rect {
  fill: #f0fdf4;
  stroke: #16a34a;
  transform: translateY(-3px);
}

.array-cell text {
  fill: #0b1220;
}

.annotation {
  opacity: 1;
  transition: opacity 250ms ease;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
}

button {
  border: 1px solid #cbd5e1;
  border-radius: 7px;
  padding: 6px 10px;
  background: #fff;
  color: #0b1220;
  font: 600 13px "Segoe UI", Arial, sans-serif;
  cursor: pointer;
}

button:hover:not(:disabled) {
  border-color: #2563eb;
  color: #2563eb;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.counter {
  margin-left: auto;
  color: #5b6472;
  font: 600 13px "Segoe UI", Arial, sans-serif;
}
</style>
