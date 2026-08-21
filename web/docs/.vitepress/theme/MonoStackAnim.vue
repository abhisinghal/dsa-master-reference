<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Step = {
  current: number | null
  stack: number[]
  popping: number | null
  pushing: number | null
  description: string
}

const values = [3, 1, 4, 1, 5, 9]
const cellWidth = 50
const gap = 12
const sourceX = 138
const stackX = 98
const stackBottom = 225
const stackCellHeight = 34
const stackGap = 8

const steps: Step[] = [
  { current: null, stack: [], popping: null, pushing: null, description: 'Start with an empty decreasing stack.' },
  { current: 0, stack: [0], popping: null, pushing: 0, description: 'Push 3: it becomes the bottom and top.' },
  { current: 1, stack: [0, 1], popping: null, pushing: 1, description: 'Push 1 because it is smaller than the top 3.' },
  { current: 2, stack: [0], popping: 1, pushing: null, description: '4 arrives; pop 1 because 1 < 4.' },
  { current: 2, stack: [], popping: 0, pushing: null, description: 'Continue popping: 3 < 4, so 3 is resolved too.' },
  { current: 2, stack: [2], popping: null, pushing: 2, description: 'Push 4 as the new unresolved top.' },
  { current: 3, stack: [2, 3], popping: null, pushing: 3, description: 'Push 1 because the stack remains decreasing.' },
  { current: 4, stack: [2], popping: 3, pushing: null, description: '5 arrives; pop 1 because 1 < 5.' },
  { current: 4, stack: [], popping: 2, pushing: null, description: 'Pop 4 because 4 < 5.' },
  { current: 4, stack: [4], popping: null, pushing: 4, description: 'Push 5 as the new top.' },
  { current: 5, stack: [], popping: 4, pushing: null, description: '9 arrives; pop 5 because 5 < 9.' },
  { current: 5, stack: [5], popping: null, pushing: 5, description: 'Push 9. Every smaller previous value has been resolved.' }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const stackItems = computed(() => {
  const step = currentStep.value
  const items = step.stack.map((index) => ({
    index,
    value: values[index],
    state: step.pushing === index ? 'push' : 'normal'
  }))

  if (step.popping !== null) {
    items.push({
      index: step.popping,
      value: values[step.popping],
      state: 'pop'
    })
  }

  return items
})

function sourceCellX(index: number) {
  return sourceX + index * (cellWidth + gap)
}

function stackCellY(position: number) {
  return stackBottom - (position + 1) * stackCellHeight - position * stackGap
}

function sourceClass(index: number) {
  return {
    current: currentStep.value.current === index,
    processed: currentStep.value.current !== null && index < currentStep.value.current,
    pushing: currentStep.value.pushing === index
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
      height="300"
      viewBox="0 0 720 300"
      xmlns="http://www.w3.org/2000/svg"
      font-family="Segoe UI, Arial, sans-serif"
      role="img"
      aria-label="Interactive monotonic stack animation"
    >
      <defs>
        <marker id="ms-anim-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#2563eb" />
        </marker>
        <filter id="ms-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="300" fill="#fbfcfe" />
      <text x="360" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="#0b1220">
        Monotonic decreasing stack
      </text>

      <g filter="url(#ms-anim-shadow)">
        <g
          v-for="(value, index) in values"
          :key="index"
          class="source-cell"
          :class="sourceClass(index)"
        >
          <rect :x="sourceCellX(index)" y="54" width="50" height="40" rx="7" />
          <text :x="sourceCellX(index) + 25" y="80" text-anchor="middle" font-size="18" font-weight="700">
            {{ value }}
          </text>
          <text :x="sourceCellX(index) + 25" y="108" text-anchor="middle" font-size="11" fill="#94a3b8">
            i={{ index }}
          </text>
        </g>
      </g>

      <rect x="48" y="120" width="220" height="130" rx="9" fill="#f8fafc" stroke="#d9dee7" />
      <text x="158" y="144" text-anchor="middle" font-size="12" font-weight="700" fill="#2563eb">
        stack: bottom → top
      </text>
      <text v-if="stackItems.length === 0" x="158" y="190" text-anchor="middle" font-size="13" fill="#5b6472">
        empty
      </text>

      <g filter="url(#ms-anim-shadow)">
        <g
          v-for="(item, position) in stackItems"
          :key="item.index"
          class="stack-item"
          :class="item.state"
          :style="{ transform: `translateY(${item.state === 'pop' ? -10 : 0}px)` }"
        >
          <rect :x="stackX" :y="stackCellY(position)" width="120" height="34" rx="7" />
          <text :x="stackX + 60" :y="stackCellY(position) + 22" text-anchor="middle" font-size="17" font-weight="800">
            {{ item.value }}
          </text>
          <text :x="stackX + 137" :y="stackCellY(position) + 22" font-size="11" fill="#5b6472">
            index {{ item.index }}
          </text>
        </g>
      </g>

      <g v-if="currentStep.current !== null" class="incoming">
        <line
          :x1="sourceCellX(currentStep.current) + 25"
          y1="120"
          x2="280"
          y2="176"
          stroke="#2563eb"
          stroke-width="2"
          stroke-dasharray="5 4"
          marker-end="url(#ms-anim-blue)"
        />
        <text x="390" y="136" text-anchor="middle" font-size="12" font-weight="700" fill="#0b1220">
          current = {{ values[currentStep.current] }}
        </text>
      </g>

      <rect x="334" y="158" width="318" height="78" rx="9" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="493" y="184" text-anchor="middle" font-size="12" font-weight="700" fill="#0b1220">
        rule
      </text>
      <text x="493" y="206" text-anchor="middle" font-size="13" fill="#334155">
        while top &lt; current: pop; then push current
      </text>
      <text x="360" y="274" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Monotonic stack animation controls">
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

.source-cell rect,
.stack-item rect {
  transition:
    fill 300ms ease,
    stroke 300ms ease,
    opacity 300ms ease,
    transform 300ms ease;
}

.source-cell rect {
  fill: #f8fafc;
  stroke: #cbd5e1;
  stroke-width: 1.5;
}

.source-cell.processed rect {
  fill: #eff6ff;
  stroke: #93c5fd;
}

.source-cell.current rect {
  fill: #f0fdf4;
  stroke: #16a34a;
  stroke-width: 1.7;
}

.source-cell.pushing rect {
  transform: translateY(-3px);
}

.source-cell text,
.stack-item text {
  fill: #0b1220;
}

.stack-item {
  transition:
    opacity 350ms ease,
    transform 350ms ease;
}

.stack-item rect {
  fill: #eff6ff;
  stroke: #93c5fd;
  stroke-width: 1.5;
}

.stack-item.push rect {
  fill: #f0fdf4;
  stroke: #16a34a;
  stroke-width: 1.7;
}

.stack-item.pop {
  opacity: 0.45;
}

.stack-item.pop rect {
  fill: #fef2f2;
  stroke: #dc2626;
  stroke-width: 1.7;
}

.incoming {
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
