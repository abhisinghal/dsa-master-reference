<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Phase = 'pick' | 'partition' | 'compare'
type Step = { values: number[]; pivotIndex: number; phase: Phase; description: string; annotation: string }

const target = 3
const pivotValue = 4
const cellWidth = 52
const gap = 12
const startX = 88

const steps: Step[] = [
  {
    values: [3, 7, 8, 1, 5, 4],
    pivotIndex: 5,
    phase: 'pick',
    description: 'Pick pivot 4 while seeking the 3rd smallest value.',
    annotation: 'target rank = 3'
  },
  {
    values: [3, 1, 4, 7, 8, 5],
    pivotIndex: 2,
    phase: 'partition',
    description: 'Partition: values less than 4 move left; the rest stay right.',
    annotation: '2 values < pivot'
  },
  {
    values: [3, 1, 4, 7, 8, 5],
    pivotIndex: 2,
    phase: 'compare',
    description: 'Pivot lands at rank 3, exactly the target rank.',
    annotation: 'pivot rank = 3, target = 3 → done'
  }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const pivotRank = computed(() => currentStep.value.pivotIndex + 1)

function cellX(index: number) {
  return startX + index * (cellWidth + gap)
}

function cellClass(index: number) {
  const step = currentStep.value
  return {
    pivot: index === step.pivotIndex,
    left: step.phase !== 'pick' && index < step.pivotIndex,
    right: step.phase !== 'pick' && index > step.pivotIndex,
    done: step.phase === 'compare' && index === step.pivotIndex
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
  <div class="anim-card">
    <svg
      class="anim-svg"
      width="720"
      height="270"
      viewBox="0 0 720 270"
      xmlns="http://www.w3.org/2000/svg"
      font-family="Segoe UI, Arial, sans-serif"
      role="img"
      aria-label="Interactive quickselect partition animation"
    >
      <defs>
        <marker id="qs-anim-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#2563eb" />
        </marker>
        <filter id="qs-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="270" fill="#fbfcfe" />
      <text x="360" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="#0b1220">
        Quickselect: one partition can finish the rank search
      </text>

      <rect x="62" y="58" width="450" height="112" rx="9" fill="#f8fafc" stroke="#d9dee7" />
      <text x="287" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">
        {{ currentStep.phase === 'pick' ? 'before partition' : 'after partition' }}
      </text>

      <g filter="url(#qs-anim-shadow)">
        <g v-for="(value, index) in currentStep.values" :key="`${index}-${value}`" class="array-cell" :class="cellClass(index)">
          <rect :x="cellX(index)" y="100" width="52" height="42" rx="7" />
          <text :x="cellX(index) + 26" y="127" text-anchor="middle" font-size="18" font-weight="800">
            {{ value }}
          </text>
          <text :x="cellX(index) + 26" y="158" text-anchor="middle" font-size="11" fill="#94a3b8">
            {{ index }}
          </text>
        </g>
      </g>

      <line
        v-if="currentStep.phase !== 'pick'"
        :x1="cellX(currentStep.pivotIndex) - 6"
        y1="92"
        :x2="cellX(currentStep.pivotIndex) - 6"
        y2="155"
        stroke="#2563eb"
        stroke-width="2"
        stroke-dasharray="5 4"
      />
      <text :x="cellX(currentStep.pivotIndex) + 26" y="95" text-anchor="middle" font-size="11" font-weight="700" fill="#2563eb">
        pivot = {{ pivotValue }}
      </text>

      <g v-if="currentStep.phase !== 'pick'" font-size="11" font-weight="700" text-anchor="middle">
        <text x="152" y="190" fill="#2563eb">&lt; pivot region</text>
        <line x1="112" y1="178" x2="224" y2="178" stroke="#2563eb" stroke-width="2" marker-end="url(#qs-anim-blue)" />
        <text x="390" y="190" fill="#5b6472">≥ pivot region</text>
      </g>

      <rect x="536" y="58" width="154" height="112" rx="9" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="613" y="82" text-anchor="middle" font-size="12" font-weight="700" fill="#0b1220">
        rank check
      </text>
      <text x="613" y="108" text-anchor="middle" font-size="13" font-weight="800" :fill="currentStep.phase === 'compare' ? '#16a34a' : '#2563eb'">
        pivot rank = {{ pivotRank }}
      </text>
      <text x="613" y="130" text-anchor="middle" font-size="13" font-weight="800" fill="#5b6472">
        target = {{ target }}
      </text>
      <text x="613" y="152" text-anchor="middle" font-size="11" font-weight="700" :fill="currentStep.phase === 'compare' ? '#16a34a' : '#5b6472'">
        {{ currentStep.annotation }}
      </text>

      <rect x="80" y="214" width="560" height="34" rx="9" :fill="currentStep.phase === 'compare' ? '#f0fdf4' : '#f6f8fb'" stroke="#d9dee7" />
      <text x="360" y="236" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Quickselect animation controls">
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

.array-cell rect {
  fill: #f8fafc;
  stroke: #cbd5e1;
  stroke-width: 1.5;
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    transform 320ms ease;
}

.array-cell text {
  fill: #0b1220;
}

.array-cell.left rect {
  fill: #eff6ff;
  stroke: #2563eb;
}

.array-cell.right rect {
  fill: #f6f8fb;
  stroke: #cbd5e1;
}

.array-cell.pivot rect {
  fill: #fef2f2;
  stroke: #dc2626;
  stroke-width: 2;
  transform: translateY(-4px);
}

.array-cell.done rect {
  fill: #f0fdf4;
  stroke: #16a34a;
  stroke-width: 2.2;
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
