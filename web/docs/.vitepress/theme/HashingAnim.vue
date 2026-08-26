<script setup lang="ts">
/**
 * HashingAnim.vue — user-driven interactive diagram for a chained hash table.
 *
 * UX: user types a key and clicks "Insert". Component:
 *   1. Computes h(key) via a small displayed polynomial hash.
 *   2. Highlights the target bucket.
 *   3. Chains the key onto the bucket (linked-list style).
 *   4. If the bucket already has entries, colours it as a collision.
 *   5. User can also "Lookup" a key — the walk down the chain animates.
 *
 * Fixed table size 7 keeps the visualisation compact. The hash is
 *   h(key) = sum(key.charCodeAt(i) * 31^i) mod 7
 * shown live so the reader can predict the bucket.
 */
import { computed, ref } from 'vue'

const TABLE_SIZE = 7
const table = ref<string[][]>(Array.from({ length: TABLE_SIZE }, () => []))
const keyInput = ref('cat')
const lastAction = ref<
  | null
  | { type: 'insert' | 'lookup'; key: string; bucket: number; found?: boolean }
>(null)
const highlightBucket = ref<number | null>(null)
const walkingIdx = ref<number | null>(null) // for lookup animation
let walkTimer: ReturnType<typeof setTimeout> | null = null

function hash(key: string): number {
  let h = 0
  const p = 31
  let pk = 1
  for (let i = 0; i < key.length; i++) {
    h = (h + key.charCodeAt(i) * pk) % TABLE_SIZE
    pk = (pk * p) % TABLE_SIZE
  }
  return ((h % TABLE_SIZE) + TABLE_SIZE) % TABLE_SIZE
}

const currentHash = computed(() => (keyInput.value ? hash(keyInput.value) : null))

function insert() {
  const k = keyInput.value.trim()
  if (!k) return
  const b = hash(k)
  if (!table.value[b].includes(k)) {
    table.value[b].push(k)
  }
  highlightBucket.value = b
  lastAction.value = { type: 'insert', key: k, bucket: b }
  keyInput.value = ''
  setTimeout(() => {
    if (highlightBucket.value === b) highlightBucket.value = null
  }, 1200)
}

function reset() {
  table.value = Array.from({ length: TABLE_SIZE }, () => [])
  lastAction.value = null
  highlightBucket.value = null
  walkingIdx.value = null
  if (walkTimer) clearTimeout(walkTimer)
}

function lookup() {
  const k = keyInput.value.trim()
  if (!k) return
  const b = hash(k)
  highlightBucket.value = b
  walkingIdx.value = 0
  const chain = table.value[b]
  const step = () => {
    if (walkingIdx.value === null) return
    const cur = walkingIdx.value
    if (cur >= chain.length) {
      // Not found
      lastAction.value = { type: 'lookup', key: k, bucket: b, found: false }
      walkingIdx.value = null
      return
    }
    if (chain[cur] === k) {
      lastAction.value = { type: 'lookup', key: k, bucket: b, found: true }
      walkingIdx.value = null
      return
    }
    walkingIdx.value = cur + 1
    walkTimer = setTimeout(step, 350)
  }
  step()
}

const preset = [
  { label: 'Presets: family of collisions', keys: ['cat', 'act', 'tac'] },
  { label: 'Presets: sparse', keys: ['red', 'blue', 'green'] }
]

function loadPreset(keys: string[]) {
  reset()
  for (const k of keys) {
    const b = hash(k)
    table.value[b].push(k)
  }
}

const cellW = 96
const cellH = 44
const startX = 30
const startY = 60
const chainStep = 90

const bucketX = (i: number) => startX
const bucketY = (i: number) => startY + i * (cellH + 10)

const collisionBuckets = computed(() => table.value.map(chain => chain.length > 1))
</script>

<template>
  <div class="anim-card">
    <div class="anim-head">
      <h4 class="anim-title">Hashing — one lookup instead of a scan</h4>
      <p class="anim-hint">
        Type a key and press <b>Insert</b> or <b>Lookup</b>. The hash function is
        <code>h(k) = Σ k[i] × 31<sup>i</sup> mod 7</code>. Same hash → same bucket → collision (chained).
      </p>
    </div>

    <svg
      class="anim-svg"
      width="720"
      height="400"
      viewBox="0 0 720 400"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="Hash table with 7 buckets, chained collisions"
    >
      <defs>
        <filter id="ha-shadow" x="-10%" y="-10%" width="120%" height="140%">
          <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#94a3b8" flood-opacity="0.45" />
        </filter>
        <marker id="ha-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8" />
        </marker>
      </defs>

      <!-- Buckets -->
      <text x="30" y="30" font-size="14" font-weight="700" fill="#0f172a">Buckets (0..6)</text>
      <g v-for="i in TABLE_SIZE" :key="'b' + i" filter="url(#ha-shadow)">
        <g
          :class="[
            'bucket',
            {
              highlight: highlightBucket === (i - 1),
              collision: collisionBuckets[i - 1]
            }
          ]"
        >
          <rect :x="bucketX(i - 1)" :y="bucketY(i - 1)" :width="cellW" :height="cellH" rx="6" />
          <text :x="bucketX(i - 1) - 8" :y="bucketY(i - 1) + cellH / 2 + 5" text-anchor="end" font-size="12" fill="#475569" font-weight="700">
            {{ i - 1 }}
          </text>
          <text
            v-if="table[i - 1].length === 0"
            :x="bucketX(i - 1) + cellW / 2"
            :y="bucketY(i - 1) + cellH / 2 + 5"
            text-anchor="middle"
            font-size="12"
            fill="#94a3b8"
            font-style="italic"
          >
            empty
          </text>
        </g>
      </g>

      <!-- Chained keys per bucket -->
      <g v-for="(chain, bIdx) in table" :key="'chain' + bIdx">
        <template v-for="(key, kIdx) in chain" :key="'k' + bIdx + '-' + kIdx">
          <!-- Arrow from prev to this cell -->
          <line
            :x1="bucketX(bIdx) + cellW + (kIdx === 0 ? 0 : kIdx * chainStep - cellW / 2 + 10)"
            :y1="bucketY(bIdx) + cellH / 2"
            :x2="bucketX(bIdx) + cellW + kIdx * chainStep + 2"
            :y2="bucketY(bIdx) + cellH / 2"
            stroke="#94a3b8"
            stroke-width="1.6"
            marker-end="url(#ha-arrow)"
          />
          <g
            :class="[
              'chain-node',
              { walking: walkingIdx === kIdx && highlightBucket === bIdx }
            ]"
          >
            <rect
              :x="bucketX(bIdx) + cellW + kIdx * chainStep + 8"
              :y="bucketY(bIdx) + 4"
              :width="70"
              :height="cellH - 8"
              rx="6"
            />
            <text
              :x="bucketX(bIdx) + cellW + kIdx * chainStep + 8 + 35"
              :y="bucketY(bIdx) + cellH / 2 + 5"
              text-anchor="middle"
              font-size="13"
              font-weight="600"
            >
              {{ key }}
            </text>
          </g>
        </template>
      </g>
    </svg>

    <div class="controls" role="group" aria-label="Hash table controls">
      <input
        v-model="keyInput"
        type="text"
        maxlength="8"
        placeholder="Type a key…"
        class="key-input"
        aria-label="Key to insert or lookup"
        @keyup.enter="insert"
      />
      <button class="btn primary" @click="insert" :disabled="!keyInput.trim()">
        Insert
      </button>
      <button class="btn" @click="lookup" :disabled="!keyInput.trim()">Lookup</button>
      <button class="btn" @click="reset" aria-label="Clear the table">Reset</button>
      <div class="hash-display" v-if="keyInput">
        h(<code>{{ keyInput }}</code>) = <b>{{ currentHash }}</b>
      </div>
    </div>

    <div class="preset-row">
      <button v-for="p in preset" :key="p.label" class="chip" @click="loadPreset(p.keys)">
        {{ p.label }}
      </button>
    </div>

    <div class="live" aria-live="polite">
      <template v-if="lastAction?.type === 'insert'">
        Inserted <b>{{ lastAction.key }}</b> into bucket {{ lastAction.bucket }}.
        {{ table[lastAction.bucket].length > 1 ? 'Collision — chained.' : 'Empty bucket.' }}
      </template>
      <template v-else-if="lastAction?.type === 'lookup'">
        Looked up <b>{{ lastAction.key }}</b> in bucket {{ lastAction.bucket }}:
        {{ lastAction.found ? 'found' : 'not found' }}.
      </template>
      <template v-else>Try inserting <code>cat</code>, <code>act</code>, <code>tac</code> — same hash, same bucket, chain grows.</template>
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

.bucket rect { fill: var(--vp-c-bg); stroke: #94a3b8; stroke-width: 1.4; transition: fill 0.15s, stroke 0.15s; }
.bucket text { fill: var(--vp-c-text-1); }
.bucket.highlight rect { fill: #dbeafe; stroke: #2563eb; stroke-width: 2.4; }
.bucket.collision rect { stroke: #f59e0b; stroke-width: 1.8; }
.bucket.collision.highlight rect { fill: #fef3c7; stroke: #d97706; stroke-width: 2.4; }

.chain-node rect { fill: var(--vp-c-bg); stroke: #64748b; stroke-width: 1.4; transition: fill 0.2s, stroke 0.2s; }
.chain-node text { fill: var(--vp-c-text-1); }
.chain-node.walking rect { fill: #ede9fe; stroke: #7c3aed; stroke-width: 2; }

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-top: 8px;
}
.key-input {
  padding: 6px 10px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
  width: 140px;
  font-family: var(--vp-font-family-mono);
}
.key-input:focus-visible { outline: 2px solid #2563eb; outline-offset: 2px; }
.btn {
  padding: 6px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
  cursor: pointer;
  transition: border-color 0.15s;
}
.btn:hover:not(:disabled) { border-color: #2563eb; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.btn.primary { background: #2563eb; color: white; border-color: #2563eb; }
.btn.primary:hover:not(:disabled) { background: #1d4ed8; }

.hash-display {
  font-size: 13px;
  color: var(--vp-c-text-2);
  padding: 4px 10px;
  background: var(--vp-c-bg);
  border-radius: 4px;
  border: 1px solid var(--vp-c-divider);
  font-family: var(--vp-font-family-mono);
}
.hash-display code {
  background: transparent;
  color: #2563eb;
  padding: 0;
  font-weight: 700;
}

.preset-row {
  margin-top: 8px;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.chip {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  cursor: pointer;
}
.chip:hover { color: #2563eb; border-color: #2563eb; }

.live {
  margin-top: 8px;
  font-size: 12px;
  color: var(--vp-c-text-3);
  text-align: center;
  min-height: 16px;
}
.live code { background: var(--vp-c-bg); padding: 0 4px; border-radius: 3px; }

@media (prefers-reduced-motion: reduce) {
  .bucket rect, .chain-node rect { transition: none; }
}

@media print { .controls, .preset-row, .live { display: none; } }
</style>
