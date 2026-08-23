<script setup lang="ts">
import { ref, onMounted } from 'vue'

/**
 * PageAnalytics — client-side view counter.
 * Increments per-page view counts in localStorage. Data lives on the user's
 * device only (privacy-first). Aggregate stats display at bottom of appendix.
 */

const key = ref('')

onMounted(() => {
  if (typeof window === 'undefined') return
  key.value = window.location.pathname
  try {
    const raw = localStorage.getItem('dsa-page-views') || '{}'
    const map = JSON.parse(raw)
    map[key.value] = (map[key.value] || 0) + 1
    // Also update total
    map['__total__'] = (map['__total__'] || 0) + 1
    map['__last__'] = Date.now()
    localStorage.setItem('dsa-page-views', JSON.stringify(map))
  } catch (e) {}
})
</script>

<template>
  <span style="display:none" data-analytics-page />
</template>
