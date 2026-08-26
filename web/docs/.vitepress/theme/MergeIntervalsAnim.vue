<script setup lang="ts">
/**
 * MergeIntervalsAnim.vue — user-driven diagram for merge-intervals.
 *
 * UX: 5 intervals rendered as coloured bars on a 0..30 timeline. User can:
 *   - drag either endpoint of any interval to reshape it
 *   - add / remove intervals
 * The merged output re-computes reactively on every change, showing which
 * originals fused together.
 */
import { computed, ref } from 'vue'

interface Interval { start: number; end: number; id: number }

const nextId = ref(6)
const intervals = ref<Interval[]>([
  { id: 1, start: 1,  end: 5  },
  { id: 2, start: 3,  end: 8  },
  { id: 3, start: 12, end: 15 },
  { id: 4, start: 13, end: 20 },
  { id: 5, start: 24, end: 27 }
])

// Merged output: sort by start, sweep left to right, extend on overlap.
const merged = computed(() => {
  const sorted = [...intervals.value].sort((a, b) => a.start - b.start)
  const out: { start: number; end: number; sources: number[] }[] = []
  for (const iv of sorted) {
    const last = out[out.length - 1]
    if (last && iv.start <= last.end) {
      last.end = Math.max(last.end, iv.end)
      last.sources.push(iv.id)
    } else {
      out.push({ start: iv.start, end: iv.end, sources: [iv.id] })
    }
  }
  return out
})

const MIN = 0
const MAX = 30
const SVG_W = 720
const PAD = 40
const scale = (x: number) => PAD + ((x - MIN) / (MAX - MIN)) * (SVG_W - 2 * PAD)

const barY = (idx: number) => 60 + idx * 32
const barH = 22

// Drag logic — pointer-based
type DragTarget = { id: number; edge: 'start' | 'end' | 'body' } | null
const dragTarget = ref<DragTarget>(null)
const dragOrigin = ref<{ x: number; startVal: number; endVal: number } | null>(null)

function beginDrag(iv: Interval, edge: 'start' | 'end' | 'body', e: PointerEvent) {
  ;(e.target as Element).setPointerCapture?.(e.pointerId)
  dragTarget.value = { id: iv.id, edge }
  dragOrigin.value = { x: e.clientX, startVal: iv.start, endVal: iv.end }
  e.preventDefault()
}

function onDrag(e: PointerEvent) {
  if (!dragTarget.value || !dragOrigin.value) return
  const svg = (e.currentTarget as SVGElement)
  const rect = svg.getBoundingClientRect()
  const scaleFactor = (SVG_W - 2 * PAD) / (MAX - MIN)
  const dxSvg = (e.clientX - dragOrigin.value.x) * (SVG_W / rect.width) / scaleFactor
  const iv = intervals.value.find(v => v.id === dragTarget.value!.id)
  if (!iv) return
  if (dragTarget.value.edge === 'start') {
    iv.start = Math.max(MIN, Math.min(iv.end - 1, Math.round(dragOrigin.value.startVal + dxSvg)))
  } else if (dragTarget.value.edge === 'end') {
    iv.end = Math.min(MAX, Math.max(iv.start + 1, Math.round(dragOrigin.value.endVal + dxSvg)))
  } else {
    const width = dragOrigin.value.endVal - dragOrigin.value.startVal
    const newStart = Math.max(MIN, Math.min(MAX - width, Math.round(dragOrigin.value.startVal + dxSvg)))
    iv.start = newStart
    iv.end = newStart + width
  }
}

function endDrag() {
  dragTarget.value = null
  dragOrigin.value = null
}

const palette = ['#2563eb', '#f59e0b', '#7c3aed', '#059669', '#dc2626', '#0891b2', '#db2777']
const colorFor = (id: number) => palette[(id - 1) % palette.length]

function addInterval() {
  const start = Math.floor(Math.random() * 20)
  intervals.value.push({ id: nextId.value++, start, end: start + 2 + Math.floor(Math.random() * 4) })
}

function removeInterval(id: number) {
  intervals.value = intervals.value.filter(v => v.id !== id)
}

function reset() {
  intervals.value = [
    { id: 1, start: 1,  end: 5  },
    { id: 2, start: 3,  end: 8  },
    { id: 3, start: 12, end: 15 },
    { id: 4, start: 13, end: 20 },
    { id: 5, start: 24, end: 27 }
  ]
  nextId.value = 6
}

const contentH = computed(() => Math.max(200, 60 + intervals.value.length * 32 + 100))
</script>

<template>
  <div class="anim-card">
    <div class="anim-head">
      <h4 class="anim-title">Merge Intervals — drag any endpoint, watch the union reshape</h4>
      <p class="anim-hint">
        Sort by start, sweep left to right, extend the last merged interval on overlap.
        Same-coloured merged bar = fused originals.
      </p>
    </div>

    <svg
      class="anim-svg"
      :width="SVG_W"
      :height="contentH"
      :viewBox="`0 0 ${SVG_W} ${contentH}`"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="Merge intervals diagram: input on top, merged output on bottom"
      @pointermove="onDrag"
      @pointerup="endDrag"
      @pointercancel="endDrag"
    >
      <!-- Axis -->
      <line :x1="PAD" :y1="40" :x2="SVG_W - PAD" :y2="40" stroke="#94a3b8" stroke-width="1.2" />
      <g v-for="tick in MAX / 5 + 1" :key="'tick' + tick">
        <line :x1="scale((tick - 1) * 5)" :y1="36" :x2="scale((tick - 1) * 5)" :y2="44" stroke="#94a3b8" stroke-width="1" />
        <text :x="scale((tick - 1) * 5)" y="30" text-anchor="middle" font-size="10" fill="#64748b">
          {{ (tick - 1) * 5 }}
        </text>
      </g>

      <text x="14" y="60" font-size="12" font-weight="700" fill="#475569">input</text>

      <!-- Input intervals -->
      <g v-for="(iv, idx) in intervals" :key="iv.id">
        <rect
          class="iv-bar"
          :x="scale(iv.start)"
          :y="barY(idx)"
          :width="scale(iv.end) - scale(iv.start)"
          :height="barH"
          :fill="colorFor(iv.id)"
          fill-opacity="0.85"
          rx="4"
          @pointerdown="beginDrag(iv, 'body', $event)"
        />
        <!-- Left handle -->
        <rect
          class="handle"
          :x="scale(iv.start) - 6"
          :y="barY(idx) - 2"
          :width="12"
          :height="barH + 4"
          rx="3"
          @pointerdown="beginDrag(iv, 'start', $event)"
        />
        <!-- Right handle -->
        <rect
          class="handle"
          :x="scale(iv.end) - 6"
          :y="barY(idx) - 2"
          :width="12"
          :height="barH + 4"
          rx="3"
          @pointerdown="beginDrag(iv, 'end', $event)"
        />
        <text
          :x="scale(iv.start) + 4"
          :y="barY(idx) + barH / 2 + 4"
          font-size="11"
          font-weight="700"
          fill="#ffffff"
        >
          [{{ iv.start }}, {{ iv.end }}]
        </text>
        <text
          class="rm-btn"
          :x="SVG_W - PAD + 6"
          :y="barY(idx) + barH / 2 + 4"
          font-size="14"
          fill="#dc2626"
          @click="removeInterval(iv.id)"
          role="button"
          aria-label="Remove interval"
        >×</text>
      </g>

      <!-- Divider before merged output -->
      <line
        :x1="PAD"
        :y1="60 + intervals.length * 32 + 8"
        :x2="SVG_W - PAD"
        :y2="60 + intervals.length * 32 + 8"
        stroke="#e2e8f0"
        stroke-width="1"
        stroke-dasharray="4 4"
      />

      <text x="14" :y="60 + intervals.length * 32 + 40" font-size="12" font-weight="700" fill="#475569">merged</text>

      <!-- Merged output -->
      <g v-for="(m, mi) in merged" :key="'m' + mi">
        <rect
          :x="scale(m.start)"
          :y="60 + intervals.length * 32 + 28"
          :width="scale(m.end) - scale(m.start)"
          height="26"
          rx="5"
          fill="#16a34a"
          fill-opacity="0.85"
        />
        <text
          :x="scale(m.start) + 4"
          :y="60 + intervals.length * 32 + 46"
          font-size="11"
          font-weight="700"
          fill="#ffffff"
        >
          [{{ m.start }}, {{ m.end }}]
        </text>
        <text
          :x="scale(m.start) + (scale(m.end) - scale(m.start)) / 2"
          :y="60 + intervals.length * 32 + 76"
          text-anchor="middle"
          font-size="10"
          fill="#64748b"
        >
          from {{ m.sources.map(s => '#' + s).join(', ') }}
        </text>
      </g>
    </svg>

    <div class="controls">
      <button class="btn primary" @click="addInterval">+ Add interval</button>
      <button class="btn" @click="reset">Reset</button>
      <span class="tally">
        {{ intervals.length }} input → {{ merged.length }} merged
      </span>
    </div>

    <div class="live" aria-live="polite">
      Drag any endpoint or the body of an interval to reshape it. The merged result updates instantly.
    </div>
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

.anim-svg { display: block; width: 100%; height: auto; max-width: 720px; margin: 8px auto; touch-action: none; user-select: none; }

.iv-bar { cursor: grab; transition: fill-opacity 0.15s; }
.iv-bar:hover { fill-opacity: 1; }
.iv-bar:active { cursor: grabbing; }

.handle { fill: rgba(255,255,255,0.001); cursor: ew-resize; }
.handle:hover { fill: rgba(37, 99, 235, 0.35); }

.rm-btn { cursor: pointer; font-weight: 700; }
.rm-btn:hover { fill: #b91c1c; }

.controls {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 8px;
  flex-wrap: wrap;
}
.btn {
  padding: 6px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
  cursor: pointer;
}
.btn:hover { border-color: #2563eb; }
.btn.primary { background: #2563eb; color: white; border-color: #2563eb; }
.btn.primary:hover { background: #1d4ed8; }
.tally {
  font-size: 12px;
  color: var(--vp-c-text-2);
  margin-left: auto;
}

.live {
  margin-top: 6px;
  font-size: 12px;
  color: var(--vp-c-text-3);
  text-align: center;
}

@media (prefers-reduced-motion: reduce) {
  .iv-bar { transition: none; }
}

@media print { .controls, .live { display: none; } }
</style>
