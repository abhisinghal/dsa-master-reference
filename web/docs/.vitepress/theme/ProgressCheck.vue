<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'

const props = defineProps<{ id: string }>()
const solved = ref(false)

onMounted(() => {
  try {
    const stored = localStorage.getItem('dsa-solved')
    if (stored) solved.value = JSON.parse(stored)[props.id] === true
  } catch (e) {}
})

function toggle() {
  solved.value = !solved.value
  try {
    const stored = localStorage.getItem('dsa-solved')
    const map = stored ? JSON.parse(stored) : {}
    map[props.id] = solved.value
    localStorage.setItem('dsa-solved', JSON.stringify(map))
  } catch (e) {}
}
</script>

<template>
  <label :class="['progress-check', { done: solved }]">
    <input type="checkbox" :checked="solved" @change="toggle" />
    <span class="check-label">
      <span v-if="solved">✅ Solved</span>
      <span v-else>⬜ Mark as solved</span>
    </span>
  </label>
</template>

<style scoped>
.progress-check {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  cursor: pointer;
  font-size: 0.85em;
  font-weight: 500;
  color: var(--vp-c-text-2);
  transition: all 0.15s ease;
  user-select: none;
}
.progress-check:hover {
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
}
.progress-check.done {
  background: rgba(21, 128, 61, 0.08);
  border-color: rgba(21, 128, 61, 0.3);
  color: #15803d;
}
.progress-check input { display: none; }
</style>
