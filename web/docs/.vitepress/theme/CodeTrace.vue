<script setup lang="ts">
/**
 * Interactive execution-trace visualization (slider style).
 * Same data shape as before, but now shows ONE frame at a time with Play/Prev/Next/Reset
 * controls and a step counter — matching FastSlowAnim's UX.
 *
 * Usage:
 *   <CodeTrace
 *     title="Max Average Subarray I trace — nums=[1,12,-5,-6,50,3], k=4"
 *     :values="[1,12,-5,-6,50,3]"
 *     :steps="[
 *       { pointers: { left: 0, right: 3 }, vars: { sum: 2, best: 2 }, note: 'first full window' },
 *       ...
 *     ]"
 *     :windowKeys="['left', 'right']"
 *   />
 */
import { computed, onBeforeUnmount, ref } from 'vue'

interface Step {
  pointers: Record<string, number>
  vars?: Record<string, string | number>
  note?: string
  added?: number[]
  removed?: number[]
}

const props = defineProps<{
  title?: string
  values: (string | number)[]
  steps: Step[]
  windowKeys?: string[]
  cellWidth?: number
}>()

const CELL = props.cellWidth ?? 44
const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

const currentStep = computed(() => props.steps[current.value])

function stop() {
  playing.value = false
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}
function next() {
  if (current.value < props.steps.length - 1) current.value += 1
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
  if (playing.value) { stop(); return }
  if (current.value === props.steps.length - 1) current.value = 0
  playing.value = true
  timer.value = setInterval(next, 1400)
}
onBeforeUnmount(stop)

// --- SVG geometry ---
const n = computed(() => props.values.length)
const svgW = computed(() => 30 + n.value * CELL + 30)
const yCells = 78
const cellH = 40

function cellColor(idx: number): string {
  const s = currentStep.value
  if (s.removed?.includes(idx)) return 'danger'
  if (s.added?.includes(idx)) return 'success'
  if (props.windowKeys) {
    if (props.windowKeys.length >= 2) {
      const a = s.pointers[props.windowKeys[0]]
      const b = s.pointers[props.windowKeys[1]]
      if (a != null && b != null) {
        const lo = Math.min(a, b), hi = Math.max(a, b)
        if (idx >= lo && idx <= hi) return 'primary'
      }
    } else if (props.windowKeys.length === 1) {
      const p = s.pointers[props.windowKeys[0]]
      if (p === idx) return 'primary'
    }
  }
  return 'neutral'
}

function pointerX(idx: number): number { return 30 + idx * CELL + (CELL - 4) / 2 }

const pointerEntries = computed(() =>
  Object.entries(currentStep.value.pointers).filter(([, idx]) => idx >= 0 && idx < n.value)
)
const varEntries = computed(() => Object.entries(currentStep.value.vars ?? {}))
</script>

<template>
  <figure class="code-trace">
    <div class="code-trace-badge">Execution Trace</div>
    <figcaption v-if="title" class="code-trace-title">{{ title }}</figcaption>

    <div class="code-trace-stage">
      <svg :viewBox="`0 0 ${svgW} 200`" :width="svgW" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" class="code-trace-svg" font-family="var(--dsa-font)">
        <rect x="0" y="0" :width="svgW" height="200" rx="8" fill="var(--dsa-bg)" />

        <!-- Pointer labels + arrows above the cells -->
        <template v-for="([name, idx], k) in pointerEntries" :key="name">
          <text
            :x="pointerX(idx)"
            :y="k % 2 === 0 ? 32 : 20"
            text-anchor="middle"
            font-size="12"
            font-weight="700"
            fill="var(--dsa-primary)"
          >{{ name }}</text>
          <path
            :d="`M${pointerX(idx)},${(k % 2 === 0 ? 36 : 24)} L${pointerX(idx)},${yCells - 4}`"
            stroke="var(--dsa-primary)"
            stroke-width="1.6"
            marker-end="url(#ct-arrow)"
          />
        </template>

        <defs>
          <marker id="ct-arrow" markerWidth="8" markerHeight="8" refX="4" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)" />
          </marker>
        </defs>

        <!-- Cells -->
        <g v-for="(v, idx) in values" :key="idx">
          <rect
            :x="30 + idx * CELL"
            :y="yCells"
            :width="CELL - 4"
            :height="cellH"
            rx="6"
            :fill="`var(--dsa-${cellColor(idx)}-soft)`"
            :stroke="`var(--dsa-${cellColor(idx)})`"
            stroke-width="1.6"
          />
          <text
            :x="30 + idx * CELL + (CELL - 4) / 2"
            :y="yCells + 26"
            text-anchor="middle"
            font-size="14"
            font-weight="700"
            fill="var(--dsa-ink)"
          >{{ v }}</text>
          <text
            :x="30 + idx * CELL + (CELL - 4) / 2"
            :y="yCells + cellH + 14"
            text-anchor="middle"
            font-size="10"
            fill="var(--dsa-neutral)"
          >{{ idx }}</text>
        </g>

        <!-- Variable readouts -->
        <g v-if="varEntries.length">
          <text
            v-for="([name, val], k) in varEntries"
            :key="name"
            :x="30"
            :y="yCells + cellH + 40 + k * 15"
            font-size="12"
            fill="var(--dsa-ink)"
          >
            <tspan font-weight="700" fill="var(--dsa-neutral)">{{ name }}</tspan> = {{ val }}
          </text>
        </g>
      </svg>
    </div>

    <div v-if="currentStep.note" class="code-trace-note">
      <span class="step-tag">Step {{ current + 1 }} / {{ steps.length }}</span>
      <span class="step-note">{{ currentStep.note }}</span>
    </div>

    <div class="code-trace-controls">
      <button @click="prev" :disabled="current === 0" aria-label="Previous step">◀ Prev</button>
      <button @click="togglePlay" class="play-btn" aria-label="Play/Pause">
        {{ playing ? '⏸ Pause' : (current === steps.length - 1 ? '↻ Replay' : '▶ Play') }}
      </button>
      <button @click="next" :disabled="current === steps.length - 1" aria-label="Next step">Next ▶</button>
      <button @click="reset" class="reset-btn" aria-label="Reset">Reset</button>
      <input
        type="range"
        min="0"
        :max="steps.length - 1"
        v-model.number="current"
        @input="stop"
        class="step-slider"
        :aria-valuenow="current"
        :aria-valuemin="0"
        :aria-valuemax="steps.length - 1"
      />
    </div>
  </figure>
</template>

<style scoped>
.code-trace {
  margin: 22px 0;
  padding: 14px 16px 12px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
}
.code-trace-badge {
  display: inline-block;
  font-size: 0.72em;
  font-weight: 700;
  color: var(--dsa-primary, #2563eb);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  padding: 3px 10px;
  background: var(--vp-c-bg);
  border: 1px solid var(--dsa-primary, #2563eb);
  border-radius: 12px;
  margin-bottom: 8px;
}
.code-trace-title {
  font-weight: 700;
  color: var(--vp-c-text-1);
  font-size: 0.92em;
  margin-bottom: 10px;
}
.code-trace-stage {
  display: flex;
  justify-content: center;
  background: var(--vp-c-bg);
  border-radius: 8px;
  padding: 6px;
  overflow-x: auto;
}
.code-trace-svg { max-width: 100%; height: auto; }
.code-trace-note {
  margin-top: 10px;
  padding: 8px 12px;
  background: var(--vp-c-bg);
  border-left: 3px solid var(--dsa-primary, #2563eb);
  border-radius: 4px;
  font-size: 0.9em;
  line-height: 1.4;
  display: flex;
  align-items: baseline;
  gap: 10px;
  flex-wrap: wrap;
}
.step-tag {
  font-size: 0.75em;
  font-weight: 700;
  color: var(--dsa-primary, #2563eb);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  padding: 2px 8px;
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
  flex-shrink: 0;
}
.step-note { flex: 1; color: var(--vp-c-text-1); }
.code-trace-controls {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.code-trace-controls button {
  padding: 5px 12px;
  font-size: 0.85em;
  font-weight: 600;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  border: 1px solid var(--vp-c-divider);
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.12s ease;
}
.code-trace-controls button:hover:not(:disabled) {
  background: var(--vp-c-bg-mute);
  border-color: var(--dsa-primary, #2563eb);
}
.code-trace-controls button:disabled { opacity: 0.4; cursor: not-allowed; }
.play-btn {
  background: var(--dsa-primary, #2563eb) !important;
  color: white !important;
  border-color: var(--dsa-primary, #2563eb) !important;
}
.play-btn:hover:not(:disabled) { filter: brightness(1.08); }
.reset-btn { color: var(--vp-c-text-2) !important; }
.step-slider {
  flex: 1;
  min-width: 100px;
  margin-left: 6px;
  accent-color: var(--dsa-primary, #2563eb);
}

@media (max-width: 540px) {
  .code-trace-controls { justify-content: center; }
  .step-slider { flex-basis: 100%; margin-left: 0; margin-top: 6px; }
}
</style>
