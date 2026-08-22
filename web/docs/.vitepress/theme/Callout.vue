<script setup lang="ts">
import Icon from './Icon.vue'
defineProps<{ kind: 'key' | 'inv' | 'trap' | 'pat' | 'note' | 'def', title?: string }>()

const iconByKind: Record<string, string> = {
  key: 'key',
  inv: 'ruler',
  trap: 'alert',
  pat: 'link',
  note: 'pencil',
  def: 'book',
}
</script>

<template>
  <div :class="['callout', 'callout-' + kind]">
    <div class="callout-icon">
      <Icon :name="iconByKind[kind]" :size="20" />
    </div>
    <div class="callout-body">
      <div v-if="title" class="callout-title">{{ title }}</div>
      <slot />
    </div>
  </div>
</template>

<style scoped>
/* 2026-08 dark contrast audit: dark callout borders/background tints now pair with the AA-safe theme link/text colors. */
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
  line-height: 1;
  padding-top: 2px;
  display: flex;
  align-items: flex-start;
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

/* Colors per kind — icons inherit border color via currentColor. */
.callout-key  { border-color: #2563eb; background: rgba(37, 99, 235, 0.08); color: #2563eb; }
.callout-inv  { border-color: #b45309; background: rgba(180, 83, 9, 0.08);  color: #b45309; }
.callout-trap { border-color: #dc2626; background: rgba(220, 38, 38, 0.08); color: #dc2626; }
.callout-pat  { border-color: #15803d; background: rgba(21, 128, 61, 0.08); color: #15803d; }
.callout-note { border-color: #64748b; background: rgba(100, 116, 139, 0.08); color: #64748b; }
.callout-def  { border-color: #0e7490; background: rgba(14, 116, 144, 0.08); color: #0e7490; }
/* Keep body text at normal color; only the icon inherits the tinted color. */
.callout .callout-body { color: var(--vp-c-text-1); }
.callout .callout-title { color: var(--vp-c-text-1); }

.dark .callout { background: rgba(255, 255, 255, 0.03); }
.dark .callout-key  { border-color: #93c5fd; background: rgba(59, 130, 246, 0.16); color: #93c5fd; }
.dark .callout-inv  { border-color: #fcd34d; background: rgba(245, 158, 11, 0.15); color: #fcd34d; }
.dark .callout-trap { border-color: #fca5a5; background: rgba(239, 68, 68, 0.15);  color: #fca5a5; }
.dark .callout-pat  { border-color: #86efac; background: rgba(34, 197, 94, 0.15);  color: #86efac; }
.dark .callout-note { border-color: #cbd5e1; background: rgba(148, 163, 184, 0.16); color: #cbd5e1; }
.dark .callout-def  { border-color: #67e8f9; background: rgba(6, 182, 212, 0.15);  color: #67e8f9; }
.dark .callout .callout-body { color: var(--vp-c-text-1); }
.dark .callout .callout-title { color: var(--vp-c-text-1); }
</style>
