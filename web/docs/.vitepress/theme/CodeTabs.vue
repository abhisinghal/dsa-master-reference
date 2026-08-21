<script setup lang="ts">
import { ref, computed, useSlots, VNode } from 'vue'

const slots = useSlots()

// Detect which slots have content: java, python, js, cpp
const availableLangs = computed(() => {
  const langs: { key: string, label: string }[] = []
  if (slots.java) langs.push({ key: 'java', label: 'Java' })
  if (slots.python) langs.push({ key: 'python', label: 'Python' })
  if (slots.js) langs.push({ key: 'js', label: 'JavaScript' })
  if (slots.cpp) langs.push({ key: 'cpp', label: 'C++' })
  return langs
})

const active = ref(availableLangs.value[0]?.key || 'java')
</script>

<template>
  <div class="code-tabs">
    <div class="code-tabs-header" v-if="availableLangs.length > 1">
      <button
        v-for="lang in availableLangs"
        :key="lang.key"
        :class="['tab', { active: active === lang.key }]"
        @click="active = lang.key">
        {{ lang.label }}
      </button>
    </div>
    <div class="code-tabs-panel">
      <template v-for="lang in availableLangs" :key="lang.key">
        <div v-show="active === lang.key">
          <slot :name="lang.key" />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.code-tabs {
  margin: 12px 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}
.code-tabs-header {
  display: flex;
  background: var(--vp-c-bg-soft);
  border-bottom: 1px solid var(--vp-c-divider);
}
.tab {
  padding: 6px 14px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 0.88em;
  font-weight: 500;
  color: var(--vp-c-text-2);
  border-bottom: 2px solid transparent;
  transition: all 0.15s ease;
}
.tab:hover { color: var(--vp-c-text-1); }
.tab.active {
  color: var(--vp-c-brand-1);
  border-bottom-color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
}
.code-tabs-panel :deep(div[class*='language-']) {
  margin: 0 !important;
  border-radius: 0 !important;
  border: none !important;
}
</style>
