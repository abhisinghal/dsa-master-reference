<script setup>
function doPrint() {
  if (typeof window !== 'undefined') window.print()
}
</script>

<template>
  <button class="print-btn" @click="doPrint" title="Print this chapter">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="6 9 6 2 18 2 18 9"></polyline>
      <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
      <rect x="6" y="14" width="12" height="8"></rect>
    </svg>
    <span>Print chapter</span>
  </button>
</template>

<style scoped>
.print-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  font-size: 0.82em;
  font-weight: 500;
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
  margin: 8px 0;
}
.print-btn:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
@media print { .print-btn { display: none !important; } }
</style>
