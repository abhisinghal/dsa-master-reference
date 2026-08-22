<script setup lang="ts">
import { useData } from 'vitepress'
import { computed } from 'vue'
import Icon from './Icon.vue'

const { page } = useData()

// Word count from page content — approximate.
const readingMinutes = computed(() => {
  const html = page.value?.frontmatter?.description || ''
  const words = (html.match(/\b\w+\b/g) || []).length
  // Fallback: 5 min minimum; use 220 wpm
  return Math.max(1, Math.round(words / 220))
})
</script>

<template>
  <span class="reading-time" v-if="readingMinutes > 0">
    <Icon name="clock" :size="14" /> ~{{ readingMinutes }} min read
  </span>
</template>

<style scoped>
.reading-time {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  font-size: 0.78em;
  font-weight: 500;
  margin-left: 8px;
  vertical-align: middle;
}
</style>
