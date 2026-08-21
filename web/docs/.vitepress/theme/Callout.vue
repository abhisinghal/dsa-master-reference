<script setup lang="ts">
defineProps<{ kind: 'key' | 'inv' | 'trap' | 'pat' | 'note' | 'def', title?: string }>()
</script>

<template>
  <div :class="['callout', 'callout-' + kind]">
    <div class="callout-icon">
      <span v-if="kind === 'key'">🔑</span>
      <span v-else-if="kind === 'inv'">📐</span>
      <span v-else-if="kind === 'trap'">⚠️</span>
      <span v-else-if="kind === 'pat'">🔗</span>
      <span v-else-if="kind === 'note'">📝</span>
      <span v-else-if="kind === 'def'">📖</span>
    </div>
    <div class="callout-body">
      <div v-if="title" class="callout-title">{{ title }}</div>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.callout {
  display: flex;
  gap: 12px;
  margin: 14px 0;
  padding: 12px 16px;
  border-left: 4px solid;
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
}
.callout-icon {
  font-size: 1.3em;
  line-height: 1;
  padding-top: 2px;
}
.callout-body { flex: 1; }
.callout-title {
  font-weight: 700;
  margin-bottom: 4px;
}
.callout-body :deep(p) { margin: 4px 0; }
.callout-body :deep(p:last-child) { margin-bottom: 0; }
.callout-body :deep(p:first-child) { margin-top: 0; }
.callout-body :deep(ul), .callout-body :deep(ol) { margin: 4px 0; }

/* Colors per kind */
.callout-key  { border-color: #2563eb; background: rgba(37, 99, 235, 0.08); }
.callout-inv  { border-color: #b45309; background: rgba(180, 83, 9, 0.08); }
.callout-trap { border-color: #dc2626; background: rgba(220, 38, 38, 0.08); }
.callout-pat  { border-color: #15803d; background: rgba(21, 128, 61, 0.08); }
.callout-note { border-color: #64748b; background: rgba(100, 116, 139, 0.08); }
.callout-def  { border-color: #0e7490; background: rgba(14, 116, 144, 0.08); }

.dark .callout { background: rgba(255, 255, 255, 0.03); }
.dark .callout-key  { background: rgba(37, 99, 235, 0.14); }
.dark .callout-inv  { background: rgba(180, 83, 9, 0.14); }
.dark .callout-trap { background: rgba(220, 38, 38, 0.14); }
.dark .callout-pat  { background: rgba(21, 128, 61, 0.14); }
.dark .callout-note { background: rgba(100, 116, 139, 0.16); }
.dark .callout-def  { background: rgba(14, 116, 144, 0.16); }
</style>
