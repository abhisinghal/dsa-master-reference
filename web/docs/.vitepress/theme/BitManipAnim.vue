<script setup lang="ts">
/**
 * BitManipAnim.vue — user-driven bit playground.
 *
 * UX: two 16-bit registers A and B. User can:
 *   - click any bit to toggle it (in A or B)
 *   - pick an operator (AND / OR / XOR / SHL / SHR)
 *   - see the resulting register update live, both in binary and decimal
 */
import { computed, ref } from 'vue'

const BITS = 16

const a = ref(new Array(BITS).fill(0) as number[])
const b = ref(new Array(BITS).fill(0) as number[])
type Op = 'AND' | 'OR' | 'XOR' | 'SHL' | 'SHR'
const op = ref<Op>('XOR')

// Seed with some interesting values.
a.value = [0,0,0,0,0,0,0,0, 0,0,1,0,1,1,0,1] // 45
b.value = [0,0,0,0,0,0,0,0, 0,0,0,0,1,0,0,1] // 9

function toggleA(i: number) { const next = [...a.value]; next[i] = next[i] ^ 1; a.value = next }
function toggleB(i: number) { const next = [...b.value]; next[i] = next[i] ^ 1; b.value = next }
function clearA() { a.value = new Array(BITS).fill(0) }
function clearB() { b.value = new Array(BITS).fill(0) }
function randomize() {
  a.value = Array.from({length: BITS}, () => Math.random() < 0.5 ? 1 : 0)
  b.value = Array.from({length: BITS}, () => Math.random() < 0.5 ? 1 : 0)
}

const bitsToInt = (bits: number[]): number => {
  let n = 0
  for (let i = 0; i < bits.length; i++) n = (n << 1) | bits[i]
  return n
}

const intToBits = (n: number): number[] => {
  const bits = new Array(BITS).fill(0)
  for (let i = BITS - 1; i >= 0; i--) {
    bits[i] = n & 1
    n = n >>> 1
  }
  return bits
}

const aInt = computed(() => bitsToInt(a.value))
const bInt = computed(() => bitsToInt(b.value))

const result = computed(() => {
  const A = aInt.value
  const B = bInt.value
  switch (op.value) {
    case 'AND': return A & B
    case 'OR':  return A | B
    case 'XOR': return A ^ B
    case 'SHL': return (A << (B & 15)) & ((1 << BITS) - 1) // shift A by low bits of B
    case 'SHR': return A >>> (B & 15)
  }
})

const resultBits = computed(() => intToBits(result.value))

// For SHL/SHR, the operator label shows shift amount
const opLabel = computed(() => {
  if (op.value === 'SHL') return `A << ${bInt.value & 15}`
  if (op.value === 'SHR') return `A >>> ${bInt.value & 15}`
  return `A ${op.value === 'AND' ? '&' : op.value === 'OR' ? '|' : '^'} B`
})

const bitW = 32
const gap = 4
const totalW = BITS * bitW + (BITS - 1) * gap
const startX = 720 / 2 - totalW / 2

const bitX = (i: number) => startX + i * (bitW + gap)

const idealDecimal = (v: number) => v.toString()
const idealHex = (v: number) => '0x' + v.toString(16).padStart(4, '0').toUpperCase()
</script>

<template>
  <div class="anim-card">
    <div class="anim-head">
      <h4 class="anim-title">Bit Manipulation — click bits, pick an op</h4>
      <p class="anim-hint">
        Click any bit of register <b>A</b> or <b>B</b> to toggle it.
        For <code>&lt;&lt;</code> and <code>&gt;&gt;&gt;</code>, B's low 4 bits give the shift count.
      </p>
    </div>

    <svg
      class="anim-svg"
      width="720"
      height="360"
      viewBox="0 0 720 360"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="Bit manipulation playground with two 16-bit registers and a result"
    >
      <!-- Register A -->
      <text x="14" y="34" font-size="14" font-weight="700" fill="#0f172a">A</text>
      <text :x="startX + totalW / 2" y="18" text-anchor="middle" font-size="12" fill="#64748b">
        dec {{ idealDecimal(aInt) }} · hex {{ idealHex(aInt) }}
      </text>
      <g v-for="(v, i) in a" :key="'a' + i">
        <rect
          :class="['bit', 'a-bit', { on: v === 1 }]"
          :x="bitX(i)"
          y="30"
          :width="bitW"
          height="32"
          rx="4"
          @click="toggleA(i)"
          role="button"
          :aria-label="'A bit ' + (BITS - 1 - i) + ' = ' + v"
        />
        <text :x="bitX(i) + bitW / 2" y="52" text-anchor="middle" font-size="14" font-weight="700" pointer-events="none">
          {{ v }}
        </text>
        <text :x="bitX(i) + bitW / 2" y="76" text-anchor="middle" font-size="9" fill="#94a3b8">
          {{ BITS - 1 - i }}
        </text>
      </g>

      <!-- Operator badge -->
      <g transform="translate(0, 100)">
        <rect x="300" y="0" width="120" height="30" rx="15" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.2" />
        <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="#2563eb">
          {{ opLabel }}
        </text>
      </g>

      <!-- Register B -->
      <text x="14" y="164" font-size="14" font-weight="700" fill="#0f172a">B</text>
      <text :x="startX + totalW / 2" y="148" text-anchor="middle" font-size="12" fill="#64748b">
        dec {{ idealDecimal(bInt) }} · hex {{ idealHex(bInt) }}
      </text>
      <g v-for="(v, i) in b" :key="'b' + i">
        <rect
          :class="['bit', 'b-bit', { on: v === 1 }]"
          :x="bitX(i)"
          y="160"
          :width="bitW"
          height="32"
          rx="4"
          @click="toggleB(i)"
          role="button"
          :aria-label="'B bit ' + (BITS - 1 - i) + ' = ' + v"
        />
        <text :x="bitX(i) + bitW / 2" y="182" text-anchor="middle" font-size="14" font-weight="700" pointer-events="none">
          {{ v }}
        </text>
      </g>

      <!-- Divider line -->
      <line :x1="startX" y1="220" :x2="startX + totalW" y2="220" stroke="#94a3b8" stroke-width="1.5" />

      <!-- Result -->
      <text x="14" y="264" font-size="14" font-weight="700" fill="#7c3aed">=</text>
      <text :x="startX + totalW / 2" y="246" text-anchor="middle" font-size="13" font-weight="700" fill="#7c3aed">
        result = {{ idealDecimal(result) }} ({{ idealHex(result) }})
      </text>
      <g v-for="(v, i) in resultBits" :key="'r' + i">
        <rect
          :class="['bit', 'r-bit', { on: v === 1 }]"
          :x="bitX(i)"
          y="258"
          :width="bitW"
          height="32"
          rx="4"
        />
        <text :x="bitX(i) + bitW / 2" y="280" text-anchor="middle" font-size="14" font-weight="700" fill="white" pointer-events="none">
          {{ v }}
        </text>
      </g>
      <text
        :x="startX + totalW / 2"
        y="322"
        text-anchor="middle"
        font-size="11"
        fill="#64748b"
      >
        bit 15 → bit 0 (MSB first)
      </text>
    </svg>

    <div class="controls">
      <div class="op-row" role="radiogroup" aria-label="Bitwise operator">
        <button
          v-for="o in (['AND','OR','XOR','SHL','SHR'] as Op[])"
          :key="o"
          :class="['btn op-btn', { active: op === o }]"
          role="radio"
          :aria-checked="op === o"
          @click="op = o"
        >
          {{ o }}
        </button>
      </div>
      <div class="misc-row">
        <button class="btn" @click="clearA">Clear A</button>
        <button class="btn" @click="clearB">Clear B</button>
        <button class="btn" @click="randomize">Random</button>
      </div>
    </div>

    <div class="live" aria-live="polite">
      A = {{ idealDecimal(aInt) }} ({{ idealHex(aInt) }}), B = {{ idealDecimal(bInt) }} ({{ idealHex(bInt) }}),
      {{ opLabel }} = {{ idealDecimal(result) }}
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
.anim-hint code { background: var(--vp-c-bg); padding: 1px 6px; border-radius: 3px; font-size: 12px; }

.anim-svg { display: block; width: 100%; height: auto; max-width: 720px; margin: 8px auto; }

.bit {
  fill: var(--vp-c-bg);
  stroke: #94a3b8;
  stroke-width: 1.2;
  cursor: pointer;
  transition: fill 0.12s, stroke 0.12s;
}
.bit:not(.r-bit) {
  cursor: pointer;
}
.bit.r-bit {
  cursor: default;
}
.bit.on { fill: #2563eb; stroke: #1d4ed8; }
.bit.on ~ text { fill: white; }
.a-bit.on { fill: #2563eb; }
.b-bit.on { fill: #f59e0b; stroke: #d97706; }
.r-bit.on { fill: #7c3aed; stroke: #6d28d9; }
.bit:hover { stroke-width: 2; }
.bit:focus-visible { outline: 2px solid #2563eb; }

.controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}
.op-row, .misc-row { display: flex; gap: 6px; flex-wrap: wrap; }

.btn {
  padding: 6px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
  cursor: pointer;
  font-family: var(--vp-font-family-mono);
}
.btn:hover { border-color: #2563eb; }
.op-btn.active {
  background: #7c3aed;
  border-color: #6d28d9;
  color: white;
}

.live {
  margin-top: 8px;
  font-size: 12px;
  color: var(--vp-c-text-3);
  text-align: center;
  font-family: var(--vp-font-family-mono);
}

@media print { .controls, .live { display: none; } }
</style>
