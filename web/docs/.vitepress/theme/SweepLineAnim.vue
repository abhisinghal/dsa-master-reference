<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type EventPoint = {
  time: number
  delta: 1 | -1
  label: string
}

type Interval = {
  label: string
  start: number
  end: number
  y: number
  color: 'blue' | 'green' | 'red'
}

type Step = {
  eventIndex: number
  count: number
  description: string
}

const events: EventPoint[] = [
  { time: 1, delta: 1, label: '+1 at 1' },
  { time: 2, delta: 1, label: '+1 at 2' },
  { time: 4, delta: -1, label: '-1 at 4' },
  { time: 5, delta: 1, label: '+1 at 5' },
  { time: 6, delta: -1, label: '-1 at 6' },
  { time: 8, delta: -1, label: '-1 at 8' }
]

const intervals: Interval[] = [
  { label: '[1,4]', start: 1, end: 4, y: 74, color: 'blue' },
  { label: '[2,6]', start: 2, end: 6, y: 108, color: 'green' },
  { label: '[5,8]', start: 5, end: 8, y: 142, color: 'red' }
]

const steps: Step[] = [
  { eventIndex: 0, count: 1, description: 'Start [1,4]: active count becomes 1.' },
  { eventIndex: 1, count: 2, description: 'Start [2,6]: two intervals overlap.' },
  { eventIndex: 2, count: 1, description: 'End [1,4]: one interval remains active.' },
  { eventIndex: 3, count: 2, description: 'Start [5,8]: overlap rises back to 2.' },
  { eventIndex: 4, count: 1, description: 'End [2,6]: only [5,8] is active.' },
  { eventIndex: 5, count: 0, description: 'End [5,8]: the sweep finishes with count 0.' }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const currentEvent = computed(() => events[currentStep.value.eventIndex])
const sweepX = computed(() => timeX(currentEvent.value.time))

function timeX(time: number) {
  return 88 + (time - 1) * 76
}

function isActive(interval: Interval) {
  const time = currentEvent.value.time
  return interval.start <= time && time < interval.end
}

function intervalClass(interval: Interval) {
  return {
    active: isActive(interval),
    blue: interval.color === 'blue',
    green: interval.color === 'green',
    red: interval.color === 'red'
  }
}

function eventClass(index: number) {
  return {
    current: index === currentStep.value.eventIndex,
    past: index < currentStep.value.eventIndex,
    start: events[index].delta > 0,
    end: events[index].delta < 0
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
      height="285"
      viewBox="0 0 720 285"
      xmlns="http://www.w3.org/2000/svg"
      font-family="Segoe UI, Arial, sans-serif"
      role="img"
      aria-label="Interactive sweep line animation"
    >
      <defs>
        <marker id="sweep-anim-blue" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#2563eb" />
        </marker>
        <filter id="sweep-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="285" fill="#fbfcfe" />
      <text x="360" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="#0b1220">
        Sweep sorted interval events from left to right
      </text>

      <line x1="88" y1="186" x2="640" y2="186" stroke="#2563eb" stroke-width="2" marker-end="url(#sweep-anim-blue)" />
      <g font-size="11" text-anchor="middle" fill="#5b6472">
        <text v-for="time in [1, 2, 3, 4, 5, 6, 7, 8]" :key="time" :x="timeX(time)" y="206">
          {{ time }}
        </text>
      </g>

      <g filter="url(#sweep-anim-shadow)">
        <g v-for="interval in intervals" :key="interval.label" class="interval" :class="intervalClass(interval)">
          <rect :x="timeX(interval.start)" :y="interval.y" :width="timeX(interval.end) - timeX(interval.start)" height="20" rx="9" />
          <text :x="timeX(interval.start) - 12" :y="interval.y + 15" text-anchor="end" font-size="12" font-weight="700">
            {{ interval.label }}
          </text>
        </g>
      </g>

      <g class="events" font-size="11" font-weight="700" text-anchor="middle">
        <g v-for="(event, index) in events" :key="event.label" class="event" :class="eventClass(index)">
          <circle :cx="timeX(event.time)" cy="186" r="6" />
          <text :x="timeX(event.time)" y="232">{{ event.label }}</text>
        </g>
      </g>

      <line class="sweep-line" :x1="sweepX" y1="52" :x2="sweepX" y2="218" />
      <text class="sweep-label" :x="sweepX + 12" y="62" font-size="11" font-weight="700">
        t={{ currentEvent.time }}
      </text>

      <rect x="520" y="68" width="150" height="82" rx="9" fill="#f6f8fb" stroke="#d9dee7" />
      <text x="595" y="92" text-anchor="middle" font-size="12" font-weight="700" fill="#0b1220">
        running count
      </text>
      <text x="595" y="122" text-anchor="middle" font-size="26" font-weight="800" fill="#2563eb">
        {{ currentStep.count }}
      </text>
      <text x="595" y="141" text-anchor="middle" font-size="11" font-weight="700" fill="#5b6472">
        {{ currentEvent.label }}
      </text>

      <text x="360" y="266" text-anchor="middle" font-size="12" font-weight="700" fill="#5b6472">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Sweep line animation controls">
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

.interval rect {
  fill: #f8fafc;
  stroke: #cbd5e1;
  stroke-width: 1.5;
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    transform 320ms ease;
}

.interval text {
  fill: #0b1220;
}

.interval.active rect {
  transform: translateY(-3px);
}

.interval.active.blue rect {
  fill: #eff6ff;
  stroke: #2563eb;
  stroke-width: 1.8;
}

.interval.active.green rect {
  fill: #f0fdf4;
  stroke: #16a34a;
  stroke-width: 1.8;
}

.interval.active.red rect {
  fill: #fef2f2;
  stroke: #dc2626;
  stroke-width: 1.8;
}

.event circle {
  fill: #fff;
  stroke: #cbd5e1;
  stroke-width: 1.6;
  transition:
    fill 300ms ease,
    stroke 300ms ease,
    transform 300ms ease;
}

.event text {
  fill: #5b6472;
}

.event.start.current circle,
.event.start.past circle {
  fill: #f0fdf4;
  stroke: #16a34a;
}

.event.end.current circle,
.event.end.past circle {
  fill: #fef2f2;
  stroke: #dc2626;
}

.event.current circle {
  transform: translateY(-4px);
  stroke-width: 2.4;
}

.event.current text {
  fill: #2563eb;
}

.sweep-line {
  stroke: #2563eb;
  stroke-width: 2.8;
  stroke-dasharray: 6 5;
  transition: x1 600ms ease, x2 600ms ease;
}

.sweep-label {
  fill: #2563eb;
  transition: x 600ms ease;
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
