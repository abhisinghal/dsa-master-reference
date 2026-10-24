<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  method: 'aggregate' | 'accounting' | 'potential'
  bound: string
  statement?: string
  workedExample?: string
}>()

const open = ref(true)

const methodLabel: Record<string, string> = {
  aggregate: 'Aggregate method',
  accounting: 'Accounting method',
  potential: 'Potential method',
}
</script>

<template>
  <div class="amortized-panel">
    <div class="amortized-head">
      <span class="amortized-badge">Amortized</span>
      <span class="amortized-method">{{ methodLabel[method] }}</span>
      <span class="amortized-bound">{{ bound }}</span>
    </div>
    <div v-if="statement" class="amortized-statement">{{ statement }}</div>
    <button
      class="amortized-toggle"
      type="button"
      :aria-expanded="open"
      @click="open = !open"
    >
      <span class="caret" :class="{ 'caret-open': open }">▸</span>
      {{ open ? 'Hide derivation' : 'Show derivation' }}
    </button>
    <div v-if="open" class="amortized-body">
      <div class="amortized-argument">
        <slot />
      </div>
      <div v-if="workedExample" class="amortized-example">
        <div class="example-label">Worked numeric example</div>
        <pre class="example-pre">{{ workedExample }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.amortized-panel {
  margin: 20px 0;
  padding: 16px 18px;
  background: var(--dsa-warning-soft, color-mix(in srgb, #f59e0b 10%, var(--vp-c-bg-soft)));
  border-left: 3px solid var(--dsa-warning, #f59e0b);
  border-radius: 8px;
}
.amortized-head {
  display: flex;
  gap: 10px;
  align-items: baseline;
  flex-wrap: wrap;
  margin-bottom: 6px;
}
.amortized-badge {
  font-size: 0.68em;
  font-weight: 800;
  color: var(--dsa-warning, #d97706);
  text-transform: uppercase;
  letter-spacing: 1px;
}
.amortized-method {
  font-size: 0.95em;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
.amortized-bound {
  margin-left: auto;
  font-family: var(--vp-font-family-mono);
  font-size: 0.9em;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  padding: 2px 8px;
  border-radius: 5px;
  color: var(--vp-c-text-1);
}
.amortized-statement {
  font-size: 0.95em;
  line-height: 1.5;
  color: var(--vp-c-text-1);
  margin: 4px 0 10px;
}
.amortized-toggle {
  padding: 0;
  background: transparent;
  border: none;
  color: var(--vp-c-text-2);
  font-size: 0.85em;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
}
.amortized-toggle:hover {
  color: var(--vp-c-text-1);
}
.caret {
  display: inline-block;
  transition: transform 0.18s ease;
  font-size: 0.7em;
}
.caret-open {
  transform: rotate(90deg);
}
.amortized-body {
  margin-top: 14px;
}
.amortized-argument {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 14px 16px;
  font-size: 0.92em;
  line-height: 1.6;
}
.amortized-argument :deep(p):first-child {
  margin-top: 0;
}
.amortized-argument :deep(p):last-child {
  margin-bottom: 0;
}
.amortized-example {
  margin-top: 12px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 10px 14px;
}
.example-label {
  font-size: 0.7em;
  font-weight: 800;
  color: var(--dsa-warning, #d97706);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 6px;
}
.example-pre {
  font-family: var(--vp-font-family-mono);
  font-size: 0.82em;
  line-height: 1.5;
  color: var(--vp-c-text-1);
  margin: 0;
  white-space: pre;
  overflow-x: auto;
}
</style>
