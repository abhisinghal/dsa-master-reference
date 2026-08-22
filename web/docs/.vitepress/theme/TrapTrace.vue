<script setup lang="ts">
/**
 * Simplified TrapTrace — 2-frame interactive slider for "buggy vs fixed" execution.
 * Faster to embed than full CodeTrace for the 60+ Trap Examples.
 *
 * Usage:
 *   <TrapTrace
 *     title="Two Sum matches self"
 *     input="nums=[3,2,4], target=6"
 *     bug="If you put(3,0) first, then check for complement 3, seen[3]=0 already — return [0,0]. Same element twice!"
 *     fix="Check the map first (miss), then insert seen[3]=0. Next iteration finds the correct partner."
 *   />
 */
import { computed, onBeforeUnmount, ref } from 'vue'

const props = defineProps<{
  title?: string
  input?: string
  bug: string
  fix: string
}>()

const steps = computed(() => [
  { label: 'Buggy', color: 'danger', note: props.bug },
  { label: 'Fixed', color: 'success', note: props.fix }
])

const current = ref(0)
const playing = ref(false)
const timer = ref<ReturnType<typeof setInterval> | null>(null)

function stop() {
  playing.value = false
  if (timer.value) { clearInterval(timer.value); timer.value = null }
}
function next() {
  if (current.value < steps.value.length - 1) current.value += 1
  else stop()
}
function prev() { stop(); current.value = Math.max(0, current.value - 1) }
function reset() { stop(); current.value = 0 }
function togglePlay() {
  if (playing.value) { stop(); return }
  if (current.value === steps.value.length - 1) current.value = 0
  playing.value = true
  timer.value = setInterval(next, 2000)
}
onBeforeUnmount(stop)

const currentStep = computed(() => steps.value[current.value])
</script>

<template>
  <figure class="trap-trace">
    <div class="trap-trace-badge">Execution Trace · Trap</div>
    <figcaption v-if="title" class="trap-trace-title">{{ title }}</figcaption>

    <div class="trap-trace-stage" :class="`stage-${currentStep.color}`">
      <div class="trap-trace-frame-label">
        <span :class="`label label-${currentStep.color}`">{{ currentStep.label }}</span>
        <span v-if="input" class="input-echo">Input: {{ input }}</span>
      </div>
      <div class="trap-trace-note">{{ currentStep.note }}</div>
    </div>

    <div class="trap-trace-controls">
      <button @click="prev" :disabled="current === 0">◀ Prev</button>
      <button @click="togglePlay" class="play-btn">
        {{ playing ? '⏸ Pause' : (current === steps.length - 1 ? '↻ Replay' : '▶ Play') }}
      </button>
      <button @click="next" :disabled="current === steps.length - 1">Next ▶</button>
      <button @click="reset" class="reset-btn">Reset</button>
      <input
        type="range" min="0" :max="steps.length - 1"
        v-model.number="current" @input="stop" class="step-slider"
      />
      <span class="step-idx">{{ current + 1 }} / {{ steps.length }}</span>
    </div>
  </figure>
</template>

<style scoped>
.trap-trace {
  margin: 22px 0;
  padding: 14px 16px 12px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
}
.trap-trace-badge {
  display: inline-block;
  font-size: 0.72em;
  font-weight: 700;
  color: var(--dsa-danger, #dc2626);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  padding: 3px 10px;
  background: var(--vp-c-bg);
  border: 1px solid var(--dsa-danger, #dc2626);
  border-radius: 12px;
  margin-bottom: 8px;
}
.trap-trace-title {
  font-weight: 700;
  color: var(--vp-c-text-1);
  font-size: 0.92em;
  margin-bottom: 10px;
}
.trap-trace-stage {
  background: var(--vp-c-bg);
  border-radius: 8px;
  padding: 14px 16px;
  border-left: 4px solid;
  transition: border-color 0.25s ease;
}
.stage-danger { border-left-color: var(--dsa-danger, #dc2626); }
.stage-success { border-left-color: var(--dsa-success, #15803d); }
.trap-trace-frame-label {
  display: flex;
  align-items: baseline;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.label {
  font-size: 0.72em;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  padding: 3px 10px;
  border-radius: 12px;
}
.label-danger { background: var(--vp-c-bg-soft); color: var(--dsa-danger, #dc2626); border: 1px solid var(--dsa-danger, #dc2626); }
.label-success { background: var(--vp-c-bg-soft); color: var(--dsa-success, #15803d); border: 1px solid var(--dsa-success, #15803d); }
.input-echo {
  font-size: 0.85em;
  color: var(--vp-c-text-2);
  font-family: var(--vp-font-family-mono);
}
.trap-trace-note {
  font-size: 0.92em;
  color: var(--vp-c-text-1);
  line-height: 1.5;
}
.trap-trace-controls {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.trap-trace-controls button {
  padding: 5px 12px;
  font-size: 0.85em;
  font-weight: 600;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  border: 1px solid var(--vp-c-divider);
  border-radius: 5px;
  cursor: pointer;
}
.trap-trace-controls button:disabled { opacity: 0.4; cursor: not-allowed; }
.play-btn {
  background: var(--dsa-primary, #2563eb) !important;
  color: white !important;
  border-color: var(--dsa-primary, #2563eb) !important;
}
.reset-btn { color: var(--vp-c-text-2) !important; }
.step-slider {
  flex: 1;
  min-width: 80px;
  margin-left: 6px;
  accent-color: var(--dsa-primary, #2563eb);
}
.step-idx {
  font-size: 0.8em;
  color: var(--vp-c-text-2);
  min-width: 32px;
  text-align: right;
}

@media (max-width: 540px) {
  .trap-trace-controls { justify-content: center; }
  .step-slider { flex-basis: 100%; margin-left: 0; }
}
</style>
