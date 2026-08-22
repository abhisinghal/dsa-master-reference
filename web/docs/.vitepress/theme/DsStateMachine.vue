<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

/**
 * DsStateMachine — data-structure operation animator.
 * Accepts a curated list of "op cards", each a small keyframe sequence.
 * Renders a tab-switcher; each tab is a step slider with visual state.
 */

type Highlight = 'primary' | 'compare' | 'swap' | 'done'
type Cell = {
  value: string | number
  key?: string | number
  highlight?: Highlight
  label?: string
}
type Frame = {
  desc: string
  cells: Cell[]       // linear cells (arrays / heap array / stack / queue)
  headLabel?: string  // caption e.g. "front", "top", "root"
  tailLabel?: string
  note?: string
}
type OpCard = {
  id: string
  title: string
  subtitle: string
  frames: Frame[]
}

const props = defineProps<{
  title?: string
  cards: OpCard[]
  defaultCard?: string
}>()

const activeId = ref(props.defaultCard || props.cards[0]?.id || '')
const active = computed(() => props.cards.find(c => c.id === activeId.value) || props.cards[0])
const step = ref(0)
const playing = ref(false)
let timer: number | null = null

const frame = computed(() => active.value.frames[step.value])
const maxStep = computed(() => active.value.frames.length - 1)

function selectCard(id: string) {
  activeId.value = id
  step.value = 0
  pause()
}

function next() {
  if (step.value >= maxStep.value) { pause(); return }
  step.value++
}
function prev() {
  if (step.value > 0) step.value--
}
function reset() { step.value = 0; pause() }
function toggle() {
  playing.value = !playing.value
  if (playing.value) schedule()
  else pause()
}
function schedule() {
  if (timer !== null) window.clearInterval(timer)
  timer = window.setInterval(() => {
    if (step.value >= maxStep.value) { pause(); return }
    step.value++
  }, 1400)
}
function pause() {
  if (timer !== null) { window.clearInterval(timer); timer = null }
  playing.value = false
}
onBeforeUnmount(() => { if (timer !== null) window.clearInterval(timer) })

function cellClass(c: Cell): string {
  const base = 'cell'
  if (!c.highlight) return base
  return base + ' hl-' + c.highlight
}
</script>

<template>
  <div class="ds-viz">
    <div class="ds-badge">Interactive · Data-Structure Operation</div>
    <div v-if="title" class="ds-title">{{ title }}</div>

    <div class="ds-tabs">
      <button
        v-for="c in cards"
        :key="c.id"
        :class="['ds-tab', { active: c.id === activeId }]"
        @click="selectCard(c.id)"
      >
        <div class="ds-tabTitle">{{ c.title }}</div>
        <div class="ds-tabSub">{{ c.subtitle }}</div>
      </button>
    </div>

    <div class="ds-stage" v-if="frame">
      <div class="ds-caption">
        <span class="ds-stepNo">Step {{ step + 1 }} / {{ active.frames.length }}</span>
        <span class="ds-desc">{{ frame.desc }}</span>
      </div>
      <div class="ds-row">
        <span v-if="frame.headLabel" class="ds-endLabel">{{ frame.headLabel }} →</span>
        <div class="ds-cells">
          <div
            v-for="(c, i) in frame.cells"
            :key="c.key !== undefined ? c.key : i"
            :class="cellClass(c)"
          >
            <div class="cellValue">{{ c.value }}</div>
            <div v-if="c.label" class="cellLabel">{{ c.label }}</div>
          </div>
        </div>
        <span v-if="frame.tailLabel" class="ds-endLabel">← {{ frame.tailLabel }}</span>
      </div>
      <div v-if="frame.note" class="ds-note">{{ frame.note }}</div>
    </div>

    <div class="ds-controls">
      <button @click="reset" title="Reset">↺</button>
      <button @click="prev" :disabled="step === 0">‹ Prev</button>
      <button @click="toggle">{{ playing ? '⏸ Pause' : '▶ Play' }}</button>
      <button @click="next" :disabled="step >= maxStep">Next ›</button>
      <div class="ds-scrubber">
        <input
          type="range"
          :min="0"
          :max="maxStep"
          v-model.number="step"
          class="ds-slider"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.ds-viz {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 20px;
  background: var(--vp-c-bg-soft);
  margin: 24px 0;
}
.ds-badge {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 600;
  margin-bottom: 8px;
}
.ds-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 14px;
}
.ds-tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}
.ds-tab {
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s;
}
.ds-tab:hover { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); }
.ds-tab.active {
  background: var(--vp-c-brand-1);
  color: white;
  border-color: var(--vp-c-brand-1);
}
.ds-tabTitle { font-size: 13px; font-weight: 600; }
.ds-tabSub { font-size: 11px; opacity: 0.85; margin-top: 2px; }
.ds-stage {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 16px;
  min-height: 120px;
  margin-bottom: 12px;
}
.ds-caption {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.ds-stepNo {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--vp-c-brand-1);
  font-weight: 700;
}
.ds-desc {
  font-size: 13px;
  color: var(--vp-c-text-1);
}
.ds-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.ds-endLabel {
  font-size: 11px;
  color: var(--vp-c-text-3);
  font-style: italic;
  font-family: ui-monospace, monospace;
}
.ds-cells {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
.cell {
  min-width: 38px;
  height: 42px;
  padding: 0 8px;
  border: 2px solid var(--vp-c-divider);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--vp-c-bg-soft);
  transition: all 0.25s;
  position: relative;
}
.cellValue {
  font-family: ui-monospace, monospace;
  font-size: 14px;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.cellLabel {
  font-size: 9px;
  color: var(--vp-c-text-3);
  margin-top: 1px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.hl-primary {
  border-color: #3b82f6;
  background: rgba(59,130,246,0.12);
  box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
}
.hl-compare {
  border-color: #f59e0b;
  background: rgba(245,158,11,0.12);
}
.hl-swap {
  border-color: #8b5cf6;
  background: rgba(139,92,246,0.15);
  animation: swap-flash 0.6s ease;
}
.hl-done {
  border-color: #22c55e;
  background: rgba(34,197,94,0.12);
}
@keyframes swap-flash {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.06); }
}
.ds-note {
  margin-top: 12px;
  padding: 8px 10px;
  background: var(--vp-c-bg-soft);
  border-left: 3px solid var(--vp-c-brand-1);
  border-radius: 4px;
  font-size: 12px;
  color: var(--vp-c-text-2);
  font-style: italic;
}
.ds-controls {
  display: flex;
  gap: 6px;
  align-items: center;
  flex-wrap: wrap;
}
.ds-controls button {
  padding: 6px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.ds-controls button:hover:not(:disabled) {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.ds-controls button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.ds-scrubber { flex: 1; min-width: 120px; }
.ds-slider {
  width: 100%;
  accent-color: var(--vp-c-brand-1);
}
</style>
