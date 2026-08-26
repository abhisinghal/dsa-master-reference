<script setup lang="ts">
/**
 * PrefixSumAnim.vue — user-driven interactive diagram for the prefix-sum pattern.
 *
 * UX: the user drags two sliders (l and r) to pick a range. The diagram
 * visualizes:
 *   - the source array cells
 *   - the prefix-sum array pre[] with pre[i] = sum of a[0..i-1]
 *   - the two cells pre[r+1] and pre[l] involved in the O(1) subtraction
 *   - the running answer sum(l..r) = pre[r+1] - pre[l]
 *
 * Meets the systemexpert reference bar: user changes the input, diagram morphs.
 * Not a timeline playback.
 */
import { computed, ref } from 'vue'

const values = [3, 1, 4, 1, 5, 9, 2, 6]
const n = values.length

// Prefix sums: pre[i] = sum of values[0..i-1], length n+1.
const pre = computed(() => {
  const arr = new Array(n + 1).fill(0)
  for (let i = 0; i < n; i++) arr[i + 1] = arr[i] + values[i]
  return arr
})

// User-controlled range [l, r], both inclusive.
const l = ref(1)
const r = ref(4)

// Ensure l <= r always.
const setL = (v: number) => {
  const clamped = Math.max(0, Math.min(n - 1, v))
  l.value = clamped
  if (r.value < l.value) r.value = l.value
}
const setR = (v: number) => {
  const clamped = Math.max(0, Math.min(n - 1, v))
  r.value = clamped
  if (l.value > r.value) l.value = r.value
}

const rangeSum = computed(() => pre.value[r.value + 1] - pre.value[l.value])
const rangeSumNaive = computed(() => {
  let s = 0
  for (let i = l.value; i <= r.value; i++) s += values[i]
  return s
})

const cellW = 60
const gap = 6
const startX = 40
const rowATop = 66     // source array
const rowPreTop = 152  // prefix array

// The prefix cells directly involved in the subtraction: pre[r+1] and pre[l].
const preRightIdx = computed(() => r.value + 1)
const preLeftIdx = computed(() => l.value)

const cellX = (i: number) => startX + i * (cellW + gap)

const inRange = (i: number) => i >= l.value && i <= r.value
const isPreLeft = (i: number) => i === preLeftIdx.value
const isPreRight = (i: number) => i === preRightIdx.value

const ariaLive = computed(() =>
  `Range [${l.value}, ${r.value}]. sum = pre[${preRightIdx.value}] − pre[${preLeftIdx.value}] = ${pre.value[preRightIdx.value]} − ${pre.value[preLeftIdx.value]} = ${rangeSum.value}.`
)
</script>

<template>
  <div class="anim-card">
    <div class="anim-head">
      <h4 class="anim-title">Prefix Sum — one subtraction answers any range</h4>
      <p class="anim-hint">Drag the sliders to pick a range <code>[l, r]</code>. Watch how <code>pre[r+1] − pre[l]</code> collapses to O(1).</p>
    </div>

    <svg
      class="anim-svg"
      width="720"
      height="260"
      viewBox="0 0 720 260"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      :aria-label="'Prefix sum diagram, ' + ariaLive"
    >
      <defs>
        <filter id="ps-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.45" />
        </filter>
      </defs>

      <!-- Row A: source array a[] -->
      <text x="14" :y="rowATop + 26" font-size="12" font-weight="700" fill="#475569">a[]</text>
      <g filter="url(#ps-shadow)">
        <g v-for="(v, i) in values" :key="'a' + i" :class="['cell', 'a-cell', { 'in-range': inRange(i) }]">
          <rect :x="cellX(i)" :y="rowATop" :width="cellW" height="42" rx="7" />
          <text :x="cellX(i) + cellW / 2" :y="rowATop + 26" text-anchor="middle" font-size="17" font-weight="700">{{ v }}</text>
        </g>
      </g>
      <g v-for="i in n" :key="'ai' + i">
        <text :x="cellX(i - 1) + cellW / 2" :y="rowATop + 58" text-anchor="middle" font-size="10" fill="#94a3b8">
          {{ i - 1 }}
        </text>
      </g>

      <!-- Row Pre: prefix array pre[] with n+1 slots -->
      <text x="14" :y="rowPreTop + 26" font-size="12" font-weight="700" fill="#475569">pre[]</text>
      <g filter="url(#ps-shadow)">
        <g
          v-for="(v, i) in pre"
          :key="'p' + i"
          :class="['cell', 'p-cell', { 'pre-right': isPreRight(i), 'pre-left': isPreLeft(i) }]"
        >
          <rect :x="cellX(i)" :y="rowPreTop" :width="cellW" height="42" rx="7" />
          <text :x="cellX(i) + cellW / 2" :y="rowPreTop + 26" text-anchor="middle" font-size="16" font-weight="700">{{ v }}</text>
        </g>
      </g>
      <g v-for="i in (n + 1)" :key="'pi' + i">
        <text :x="cellX(i - 1) + cellW / 2" :y="rowPreTop + 58" text-anchor="middle" font-size="10" fill="#94a3b8">
          {{ i - 1 }}
        </text>
      </g>

      <!-- The subtraction formula, rendered live -->
      <g class="formula" transform="translate(0, 232)">
        <text x="14" y="14" font-size="13" fill="#475569" font-weight="600">sum(l..r) =</text>
        <text x="120" y="14" font-size="14" fill="#2563eb" font-weight="700">
          pre[{{ preRightIdx }}] − pre[{{ preLeftIdx }}]
        </text>
        <text x="285" y="14" font-size="14" fill="#475569">=</text>
        <text x="300" y="14" font-size="14" fill="#0f172a" font-weight="700">
          {{ pre[preRightIdx] }} − {{ pre[preLeftIdx] }}
        </text>
        <text x="380" y="14" font-size="14" fill="#475569">=</text>
        <text x="395" y="14" font-size="15" fill="#16a34a" font-weight="800">
          {{ rangeSum }}
        </text>
        <text x="440" y="14" font-size="12" fill="#94a3b8">
          (naive sum over l..r = {{ rangeSumNaive }})
        </text>
      </g>
    </svg>

    <div class="controls" role="group" aria-label="Range selection controls">
      <div class="ctrl">
        <label for="ps-l">l = {{ l }}</label>
        <input
          id="ps-l"
          type="range"
          min="0"
          :max="n - 1"
          :value="l"
          @input="setL(($event.target as HTMLInputElement).valueAsNumber)"
        />
      </div>
      <div class="ctrl">
        <label for="ps-r">r = {{ r }}</label>
        <input
          id="ps-r"
          type="range"
          min="0"
          :max="n - 1"
          :value="r"
          @input="setR(($event.target as HTMLInputElement).valueAsNumber)"
        />
      </div>
    </div>

    <div class="live" aria-live="polite">{{ ariaLive }}</div>
  </div>
</template>

<style scoped>
.anim-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 16px;
  margin: 20px 0;
}
.anim-head { margin-bottom: 12px; }
.anim-title { margin: 0 0 4px; font-size: 15px; font-weight: 700; color: var(--vp-c-text-1); }
.anim-hint { margin: 0; font-size: 13px; color: var(--vp-c-text-2); }
.anim-hint code { background: var(--vp-c-bg); padding: 1px 6px; border-radius: 3px; font-size: 12px; }

.anim-svg { display: block; width: 100%; height: auto; max-width: 720px; margin: 8px auto; }

.cell rect { fill: var(--vp-c-bg); stroke: #94a3b8; stroke-width: 1.4; transition: fill 0.15s, stroke 0.15s, stroke-width 0.15s; }
.cell text { fill: var(--vp-c-text-1); }

.a-cell.in-range rect { fill: #dbeafe; stroke: #2563eb; stroke-width: 1.8; }
.p-cell.pre-right rect { fill: #dcfce7; stroke: #16a34a; stroke-width: 2.2; }
.p-cell.pre-left rect { fill: #fee2e2; stroke: #dc2626; stroke-width: 2.2; }

.controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 8px;
}
.ctrl { display: flex; flex-direction: column; gap: 4px; }
.ctrl label { font-size: 12px; font-weight: 600; color: var(--vp-c-text-2); }
.ctrl input[type='range'] { width: 100%; accent-color: #2563eb; }
.ctrl input[type='range']:focus-visible { outline: 2px solid #2563eb; outline-offset: 3px; border-radius: 4px; }

.live {
  margin-top: 6px;
  font-size: 12px;
  color: var(--vp-c-text-3);
  text-align: center;
  min-height: 16px;
}

@media (prefers-reduced-motion: reduce) {
  .cell rect { transition: none; }
}

@media print { .controls, .live { display: none; } }
</style>
