<script setup lang="ts">
import { computed, ref } from 'vue'

/**
 * ExamplePreview — a compact "input → output" transformation visual
 * for a single Example line in a problem. Renders a small strip:
 * [input cells]  →  [output cells]  with an optional highlight of
 * which elements were "kept", "chosen", or transformed.
 */

type Cell = {
  value: string | number
  hl?: 'keep' | 'drop' | 'pick' | 'result'
  sub?: string
}

const props = defineProps<{
  title?: string
  input: Cell[] | (string | number)[]
  output: Cell[] | (string | number)[]
  inputLabel?: string
  outputLabel?: string
  operation?: string
  compact?: boolean
}>()

function normalize(cells: Cell[] | (string | number)[]): Cell[] {
  return cells.map(c => typeof c === 'object' && c !== null ? c : { value: c })
}

const input = computed(() => normalize(props.input))
const output = computed(() => normalize(props.output))

function cellClass(c: Cell) {
  if (c.value === '|') return 'ep-sep'
  if (!c.hl) return 'ep-cell'
  return 'ep-cell hl-' + c.hl
}
</script>

<template>
  <div :class="['ep', { compact: props.compact }]">
    <div class="ep-badge">Example Preview</div>
    <div v-if="title" class="ep-title">{{ title }}</div>
    <div class="ep-row">
      <div class="ep-side">
        <div class="ep-label">{{ props.inputLabel || 'Input' }}</div>
        <div class="ep-cells">
          <div v-for="(c, i) in input" :key="'i'+i" :class="cellClass(c)">
            <template v-if="c.value === '|'"></template>
            <template v-else>
              <span class="v">{{ c.value }}</span>
              <span v-if="c.sub" class="s">{{ c.sub }}</span>
            </template>
          </div>
        </div>
      </div>
      <div class="ep-arrow">
        <div class="ep-op">{{ props.operation || '→' }}</div>
      </div>
      <div class="ep-side">
        <div class="ep-label">{{ props.outputLabel || 'Output' }}</div>
        <div class="ep-cells">
          <div v-for="(c, i) in output" :key="'o'+i" :class="cellClass(c)">
            <template v-if="c.value === '|'"></template>
            <template v-else>
              <span class="v">{{ c.value }}</span>
              <span v-if="c.sub" class="s">{{ c.sub }}</span>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ep {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 14px 16px;
  background: var(--vp-c-bg-soft);
  margin: 12px 0 16px;
}
.ep.compact { padding: 10px 12px; }
.ep-badge {
  display: inline-block;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 600;
  margin-bottom: 6px;
}
.ep-title { font-size: 13px; font-weight: 600; color: var(--vp-c-text-1); margin-bottom: 8px; }
.ep-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 12px;
  align-items: center;
}
.ep-side { min-width: 0; }
.ep-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--vp-c-text-3);
  font-weight: 600;
  margin-bottom: 6px;
}
.ep-cells {
  display: flex;
  gap: 3px;
  flex-wrap: wrap;
}
.ep-cell {
  min-width: 30px;
  padding: 4px 6px;
  border: 1.5px solid var(--vp-c-divider);
  border-radius: 5px;
  background: var(--vp-c-bg);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.2s;
}
.ep-cell .v {
  font-family: ui-monospace, monospace;
  font-size: 12px;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.ep-cell .s {
  font-size: 9px;
  color: var(--vp-c-text-3);
  margin-top: 1px;
}
.hl-keep   { border-color: #22c55e; background: rgba(34,197,94,0.10); }
.hl-drop   { border-color: #94a3b8; opacity: 0.45; }
.hl-pick   { border-color: #3b82f6; background: rgba(59,130,246,0.12); box-shadow: 0 0 0 1.5px rgba(59,130,246,0.15); }
.hl-result { border-color: #8b5cf6; background: rgba(139,92,246,0.12); }
.ep-sep {
  width: 8px;
  border: none;
  background: transparent;
  color: var(--vp-c-text-3);
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}
.ep-sep::before {
  content: '';
  display: block;
  width: 1px;
  height: 20px;
  background: var(--vp-c-divider);
}
.ep-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
}
.ep-op {
  font-family: ui-monospace, monospace;
  font-size: 13px;
  color: var(--vp-c-brand-1);
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 4px;
  background: var(--vp-c-brand-soft);
  white-space: nowrap;
}
@media (max-width: 640px) {
  .ep-row { grid-template-columns: 1fr; gap: 8px; }
  .ep-arrow { transform: rotate(90deg); justify-self: center; }
}
</style>
