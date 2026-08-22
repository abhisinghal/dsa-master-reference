<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{
  title?: string
  defaultN?: number
  hiddenClasses?: string[]
}>()

type Complexity = {
  id: string
  label: string
  fn: (n: number) => number
  color: string
  order: number
}

const ALL: Complexity[] = [
  { id: 'o1',    label: 'O(1)',        fn: () => 1,                   color: '#22c55e', order: 0 },
  { id: 'ologn', label: 'O(log n)',    fn: (n) => Math.log2(Math.max(1, n)), color: '#06b6d4', order: 1 },
  { id: 'osqrt', label: 'O(√n)',       fn: (n) => Math.sqrt(n),       color: '#0ea5e9', order: 2 },
  { id: 'on',    label: 'O(n)',        fn: (n) => n,                  color: '#3b82f6', order: 3 },
  { id: 'onlogn',label: 'O(n log n)',  fn: (n) => n * Math.log2(Math.max(1, n)), color: '#8b5cf6', order: 4 },
  { id: 'on2',   label: 'O(n²)',       fn: (n) => n * n,              color: '#f59e0b', order: 5 },
  { id: 'o2n',   label: 'O(2ⁿ)',       fn: (n) => Math.pow(2, Math.min(n, 30)), color: '#ef4444', order: 6 },
  { id: 'onfact',label: 'O(n!)',       fn: (n) => factorial(Math.min(n, 15)), color: '#dc2626', order: 7 }
]

function factorial(n: number): number {
  let r = 1
  for (let i = 2; i <= n; i++) r *= i
  return r
}

const hidden = new Set(props.hiddenClasses || ['onfact'])
const active = computed(() => ALL.filter(c => !hidden.has(c.id)))

const n = ref(props.defaultN ?? 32)
const budget = ref<'op' | 'ms'>('op')
const opsPerMs = 1_000_000

function formatOps(x: number): string {
  if (!isFinite(x)) return '∞'
  if (x < 1) return x.toFixed(2)
  if (x < 1000) return Math.round(x).toString()
  if (x < 1e6) return (x / 1000).toFixed(1) + 'k'
  if (x < 1e9) return (x / 1e6).toFixed(1) + 'M'
  if (x < 1e12) return (x / 1e9).toFixed(1) + 'B'
  if (x < 1e15) return (x / 1e12).toFixed(1) + 'T'
  return x.toExponential(1)
}

function formatTime(ops: number): string {
  const ms = ops / opsPerMs
  if (ms < 0.001) return '< 1µs'
  if (ms < 1) return (ms * 1000).toFixed(0) + 'µs'
  if (ms < 1000) return ms.toFixed(1) + 'ms'
  if (ms < 60_000) return (ms / 1000).toFixed(1) + 's'
  if (ms < 3_600_000) return (ms / 60_000).toFixed(1) + 'min'
  if (ms < 86_400_000) return (ms / 3_600_000).toFixed(1) + 'h'
  if (ms < 31_536_000_000) return (ms / 86_400_000).toFixed(1) + ' days'
  const years = ms / 31_536_000_000
  if (years > 1e12) return years.toExponential(1) + ' years'
  if (years > 1e9) return (years / 1e9).toFixed(1) + 'B years'
  if (years > 1e6) return (years / 1e6).toFixed(1) + 'M years'
  if (years > 1000) return (years / 1000).toFixed(1) + 'k years'
  return years.toFixed(1) + ' years'
}

const rows = computed(() =>
  active.value.map(c => {
    const ops = c.fn(n.value)
    return {
      ...c,
      ops,
      display: budget.value === 'op' ? formatOps(ops) : formatTime(ops)
    }
  })
)

const maxOps = computed(() => rows.value.reduce((m, r) => Math.max(m, isFinite(r.ops) ? r.ops : 0), 1))
function barWidth(ops: number): number {
  if (!isFinite(ops) || ops <= 0) return 0
  const logMax = Math.log10(maxOps.value + 1)
  const logOps = Math.log10(ops + 1)
  return Math.max(1.5, (logOps / logMax) * 100)
}

const presets = [
  { label: 'n = 10', v: 10 },
  { label: 'n = 100', v: 100 },
  { label: 'n = 1k', v: 1000 },
  { label: 'n = 10k', v: 10000 },
  { label: 'n = 100k', v: 100000 },
  { label: 'n = 1M', v: 1_000_000 }
]

function feasibility(ops: number): { verdict: string; className: string } {
  const ms = ops / opsPerMs
  if (ms < 100) return { verdict: 'instant', className: 'verdict-good' }
  if (ms < 1000) return { verdict: 'ok', className: 'verdict-ok' }
  if (ms < 60_000) return { verdict: 'slow', className: 'verdict-warn' }
  return { verdict: 'infeasible', className: 'verdict-bad' }
}
</script>

<template>
  <div class="cx-viz">
    <div class="cx-badge">Interactive · Complexity Playground</div>
    <div class="cx-title">{{ props.title || 'How input size becomes runtime' }}</div>

    <div class="cx-controls">
      <div class="cx-sliderRow">
        <label class="cx-label">Input size <code>n</code></label>
        <input type="range" :min="1" :max="1000000" step="1" v-model.number="n" class="cx-slider" />
        <input type="number" :min="1" :max="10000000" v-model.number="n" class="cx-numInput" />
      </div>

      <div class="cx-presets">
        <button
          v-for="p in presets"
          :key="p.v"
          @click="n = p.v"
          :class="['cx-preset', { active: n === p.v }]"
        >{{ p.label }}</button>
      </div>

      <div class="cx-modeRow">
        <span class="cx-label">Show as</span>
        <div class="cx-modeButtons">
          <button :class="['cx-mode', { active: budget === 'op' }]" @click="budget = 'op'">operations</button>
          <button :class="['cx-mode', { active: budget === 'ms' }]" @click="budget = 'ms'">wall time (10⁶ ops/ms)</button>
        </div>
      </div>
    </div>

    <div class="cx-chart">
      <div v-for="r in rows" :key="r.id" class="cx-row">
        <div class="cx-rowLabel" :style="{ color: r.color }">{{ r.label }}</div>
        <div class="cx-barTrack">
          <div class="cx-bar" :style="{ width: barWidth(r.ops) + '%', background: r.color }"></div>
          <span class="cx-barValue">{{ r.display }}</span>
        </div>
        <div v-if="budget === 'ms'" :class="['cx-verdict', feasibility(r.ops).className]">
          {{ feasibility(r.ops).verdict }}
        </div>
      </div>
    </div>

    <div class="cx-legend">
      <span>Bars use log-scale to keep every class visible when n is large.</span>
    </div>
  </div>
</template>

<style scoped>
.cx-viz {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 20px;
  background: var(--vp-c-bg-soft);
  margin: 24px 0;
  font-family: system-ui, -apple-system, sans-serif;
}
.cx-badge {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 600;
  margin-bottom: 6px;
}
.cx-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 18px;
}
.cx-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}
.cx-sliderRow {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.cx-label {
  font-size: 13px;
  color: var(--vp-c-text-2);
  font-weight: 500;
  min-width: 90px;
}
.cx-slider {
  flex: 1;
  min-width: 180px;
  accent-color: var(--vp-c-brand-1);
}
.cx-numInput {
  width: 100px;
  padding: 4px 8px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-family: ui-monospace, monospace;
  font-size: 13px;
}
.cx-presets, .cx-modeButtons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.cx-modeRow {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.cx-preset, .cx-mode {
  padding: 5px 10px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.cx-preset:hover, .cx-mode:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.cx-preset.active, .cx-mode.active {
  background: var(--vp-c-brand-1);
  color: white;
  border-color: var(--vp-c-brand-1);
}
.cx-chart {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.cx-row {
  display: grid;
  grid-template-columns: 90px 1fr auto;
  gap: 10px;
  align-items: center;
}
.cx-rowLabel {
  font-family: ui-monospace, monospace;
  font-weight: 600;
  font-size: 13px;
  text-align: right;
}
.cx-barTrack {
  position: relative;
  height: 28px;
  background: var(--vp-c-bg);
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
  overflow: hidden;
}
.cx-bar {
  height: 100%;
  border-radius: 3px 0 0 3px;
  transition: width 0.3s ease;
  opacity: 0.85;
}
.cx-barValue {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-family: ui-monospace, monospace;
  font-size: 12px;
  color: var(--vp-c-text-1);
  font-weight: 600;
  text-shadow: 0 0 4px var(--vp-c-bg);
}
.cx-verdict {
  padding: 3px 9px;
  font-size: 11px;
  border-radius: 999px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.verdict-good { background: rgba(34,197,94,0.15); color: #16a34a; }
.verdict-ok   { background: rgba(6,182,212,0.15); color: #0891b2; }
.verdict-warn { background: rgba(245,158,11,0.15); color: #d97706; }
.verdict-bad  { background: rgba(239,68,68,0.15); color: #dc2626; }
.cx-legend {
  margin-top: 14px;
  font-size: 11px;
  color: var(--vp-c-text-3);
  font-style: italic;
}
</style>
