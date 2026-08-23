<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const props = defineProps({
  problemSlug: { type: String, required: true }
})

const running = ref(false)
const seconds = ref(0)
const bestSeconds = ref(null)
let interval = null

const fmt = (s) => {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
}

const display = computed(() => fmt(seconds.value))
const bestDisplay = computed(() => bestSeconds.value ? fmt(bestSeconds.value) : '—')

const bestKey = () => `dsa-timer-best:${props.problemSlug}`

onMounted(() => {
  if (typeof window === 'undefined') return
  try {
    const raw = localStorage.getItem(bestKey())
    if (raw) bestSeconds.value = parseInt(raw, 10) || null
  } catch (e) {}
})

onUnmounted(() => { if (interval) clearInterval(interval) })

function start() {
  if (running.value) return
  running.value = true
  interval = setInterval(() => { seconds.value++ }, 1000)
}

function pause() {
  running.value = false
  if (interval) { clearInterval(interval); interval = null }
}

function reset() {
  pause()
  seconds.value = 0
}

function saveBest() {
  pause()
  if (seconds.value === 0) return
  if (!bestSeconds.value || seconds.value < bestSeconds.value) {
    bestSeconds.value = seconds.value
    try { localStorage.setItem(bestKey(), String(seconds.value)) } catch (e) {}
  }
}
</script>

<template>
  <details class="timer-panel">
    <summary class="timer-summary">
      <span class="timer-icon">⏱️</span>
      <span class="timer-label">Interview timer</span>
      <span class="timer-clock" :class="{ running }">{{ display }}</span>
      <span class="timer-best" v-if="bestSeconds">best {{ bestDisplay }}</span>
    </summary>
    <div class="timer-body">
      <div class="timer-help">Practice under interview pressure. Start when you begin reading; stop when you finish. Save best only when you had a full working solution.</div>
      <div class="timer-controls">
        <button v-if="!running" class="tbtn tbtn-start" @click="start">▶ Start</button>
        <button v-else class="tbtn tbtn-pause" @click="pause">⏸ Pause</button>
        <button class="tbtn tbtn-reset" @click="reset">↺ Reset</button>
        <button class="tbtn tbtn-save" @click="saveBest" :disabled="seconds === 0">💾 Save as best</button>
      </div>
      <div class="timer-note">Target for interview: Medium = 20-25 min · Hard = 30-40 min · Best time persists on this device only.</div>
    </div>
  </details>
</template>

<style scoped>
.timer-panel {
  margin: 1rem 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
}
.timer-summary {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
  list-style: none;
  font-weight: 600;
  font-size: 0.92em;
}
.timer-summary::-webkit-details-marker { display: none; }
.timer-icon { font-size: 1.1em; }
.timer-label { color: var(--vp-c-text-1); }
.timer-clock {
  font-family: var(--vp-font-family-mono);
  font-size: 1em;
  color: var(--vp-c-text-2);
  padding: 3px 8px;
  border-radius: 4px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
}
.timer-clock.running {
  color: #f97316;
  border-color: #f97316;
  animation: pulse 1s ease-in-out infinite;
}
@keyframes pulse {
  50% { box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.15); }
}
.timer-best {
  font-size: 0.75em;
  color: #22c55e;
  font-weight: 500;
  margin-left: auto;
}
.timer-body { padding: 0 14px 14px; }
.timer-help {
  font-size: 0.82em;
  color: var(--vp-c-text-2);
  margin-bottom: 10px;
}
.timer-controls {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.tbtn {
  padding: 6px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.85em;
  font-weight: 500;
  cursor: pointer;
  transition: border-color 0.15s;
}
.tbtn:hover:not(:disabled) { border-color: var(--vp-c-brand-1); }
.tbtn:disabled { opacity: 0.5; cursor: not-allowed; }
.tbtn-start { color: #22c55e; border-color: #22c55e; }
.tbtn-pause { color: #f97316; border-color: #f97316; }
.timer-note {
  font-size: 0.75em;
  color: var(--vp-c-text-3);
}
@media print { .timer-panel { display: none !important; } }
</style>
