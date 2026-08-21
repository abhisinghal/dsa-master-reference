<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type StepState = 'normal' | 'meeting' | 'reset' | 'entry'

type Step = {
  slow: number
  fast: number
  state: StepState
  description: string
}

type NodePosition = {
  x: number
  y: number
}

const nodePositions: NodePosition[] = [
  { x: 64, y: 116 },
  { x: 144, y: 116 },
  { x: 224, y: 116 },
  { x: 304, y: 116 },
  { x: 384, y: 116 },
  { x: 464, y: 116 },
  { x: 544, y: 116 },
  { x: 624, y: 116 }
]
const links = [
  [0, 1],
  [1, 2],
  [2, 3],
  [3, 4],
  [4, 5],
  [5, 6],
  [6, 7]
] as const
const cycleStart = 3

const steps: Step[] = [
  { slow: 0, fast: 0, state: 'normal', description: 'Start both pointers at the head.' },
  { slow: 1, fast: 2, state: 'normal', description: 'Slow moves one hop; fast moves two.' },
  { slow: 2, fast: 4, state: 'normal', description: 'The fast pointer keeps gaining inside the one-way chain.' },
  { slow: 3, fast: 6, state: 'normal', description: 'Slow enters the cycle at node 3 while fast is deeper in the loop.' },
  { slow: 4, fast: 3, state: 'normal', description: 'Fast wraps 6 → 7 → 3 through the cycle link.' },
  { slow: 5, fast: 5, state: 'meeting', description: 'Meeting point! The pointers collide inside the cycle.' },
  { slow: 0, fast: 5, state: 'reset', description: 'Reset slow to head; keep fast at the meeting point.' },
  { slow: 1, fast: 6, state: 'reset', description: 'Move both one step at a time toward the cycle entry.' },
  { slow: 2, fast: 7, state: 'reset', description: 'Fast is one hop from wrapping back to the entry.' },
  { slow: 3, fast: 3, state: 'entry', description: 'Cycle start found at node 3.' }
]

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => steps[current.value])
const statusText = computed(() => {
  if (currentStep.value.state === 'meeting') return 'Meeting point!'
  if (currentStep.value.state === 'entry') return 'Cycle start = node 3'
  if (currentStep.value.state === 'reset') return 'Entry phase: both move by 1'
  return 'Detection phase: slow +1, fast +2'
})
const statusTone = computed(() => {
  if (currentStep.value.state === 'meeting' || currentStep.value.state === 'entry') return 'var(--dsa-success)'
  if (currentStep.value.state === 'reset') return 'var(--dsa-info)'
  return 'var(--dsa-primary)'
})

function nodeClass(index: number) {
  const step = currentStep.value
  return {
    cycle: index >= cycleStart,
    slow: index === step.slow && step.slow !== step.fast,
    fast: index === step.fast && step.slow !== step.fast,
    meeting: step.state === 'meeting' && index === step.slow,
    entry: step.state === 'entry' && index === cycleStart
  }
}

function nodeX(index: number) {
  return nodePositions[index].x
}

function nodeY(index: number) {
  return nodePositions[index].y
}

function markerX(kind: 'slow' | 'fast') {
  const step = currentStep.value
  const index = kind === 'slow' ? step.slow : step.fast
  const both = step.slow === step.fast
  return nodeX(index) + (both ? (kind === 'slow' ? -8 : 8) : kind === 'slow' ? -7 : 7)
}

function markerY(kind: 'slow' | 'fast') {
  const step = currentStep.value
  const index = kind === 'slow' ? step.slow : step.fast
  return nodeY(index) - 10
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
      font-family="var(--dsa-font)"
      role="img"
      aria-label="Interactive fast slow pointers cycle detection animation"
    >
      <defs>
        <marker id="fs-anim-neutral" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-neutral)" />
        </marker>
        <marker id="fs-anim-warning" markerWidth="9" markerHeight="9" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-warning)" />
        </marker>
        <filter id="fs-anim-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="var(--dsa-neutral-line)" flood-opacity="0.5" />
        </filter>
      </defs>

      <rect x="0" y="0" width="720" height="300" rx="12" fill="var(--dsa-bg)" />
      <text x="360" y="30" text-anchor="middle" font-size="14" font-weight="700" fill="var(--dsa-primary)">
        Floyd cycle detection — 7 links back to 3
      </text>

      <g class="links">
        <line
          v-for="([from, to], index) in links"
          :key="index"
          :x1="nodeX(from) + 22"
          :y1="nodeY(from)"
          :x2="nodeX(to) - 22"
          :y2="nodeY(to)"
          stroke="var(--dsa-neutral)"
          stroke-width="var(--dsa-arrow-stroke)"
          marker-end="url(#fs-anim-neutral)"
        />
        <path
          d="M 624 140 C 590 222, 346 222, 304 140"
          fill="none"
          stroke="var(--dsa-warning)"
          stroke-width="var(--dsa-arrow-stroke)"
          stroke-dasharray="6 5"
          marker-end="url(#fs-anim-warning)"
        />
        <text x="464" y="236" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-warning)">
          cycle link: 7 → 3
        </text>
      </g>

      <g filter="url(#fs-anim-shadow)">
        <g v-for="(_, index) in nodePositions" :key="index" class="node" :class="nodeClass(index)">
          <circle :cx="nodeX(index)" :cy="nodeY(index)" r="22" />
          <text :x="nodeX(index)" :y="nodeY(index) + 6" text-anchor="middle" font-size="17" font-weight="800">
            {{ index }}
          </text>
        </g>
      </g>

      <g class="marker marker-slow" :style="{ transform: `translate(${markerX('slow')}px, ${markerY('slow')}px)` }">
        <circle cx="0" cy="0" r="7" fill="var(--dsa-primary)" stroke="var(--dsa-bg)" stroke-width="2" />
      </g>
      <g class="marker marker-fast" :style="{ transform: `translate(${markerX('fast')}px, ${markerY('fast')}px)` }">
        <circle cx="0" cy="0" r="7" fill="var(--dsa-success)" stroke="var(--dsa-bg)" stroke-width="2" />
      </g>

      <g class="legend" font-size="12" font-weight="700">
        <circle cx="260" cy="58" r="6" fill="var(--dsa-primary)" />
        <text x="274" y="62" fill="var(--dsa-primary)">slow</text>
        <circle cx="344" cy="58" r="6" fill="var(--dsa-success)" />
        <text x="358" y="62" fill="var(--dsa-success)">fast</text>
      </g>

      <rect x="238" y="188" width="244" height="58" rx="9" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" />
      <text x="360" y="211" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-ink)">
        slow={{ currentStep.slow }}, fast={{ currentStep.fast }}
      </text>
      <text x="360" y="233" text-anchor="middle" font-size="13" font-weight="800" :fill="statusTone">
        {{ statusText }}
      </text>

      <text x="360" y="282" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-neutral)">
        {{ currentStep.description }}
      </text>
    </svg>

    <div class="controls" aria-label="Fast slow pointers animation controls">
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

.node circle {
  fill: var(--dsa-neutral-soft);
  stroke: var(--dsa-neutral-line);
  stroke-width: var(--dsa-cell-stroke);
  transition:
    fill 320ms ease,
    stroke 320ms ease,
    stroke-width 320ms ease;
}

.node.cycle circle {
  stroke: var(--dsa-warning-line);
}

.node.slow circle {
  fill: var(--dsa-primary-soft);
  stroke: var(--dsa-primary);
}

.node.fast circle {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
}

.node.meeting circle,
.node.entry circle {
  fill: var(--dsa-success-soft);
  stroke: var(--dsa-success);
  stroke-width: var(--dsa-outline-stroke);
}

.node text {
  fill: var(--dsa-ink);
}

.marker {
  transition: transform 600ms ease;
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
