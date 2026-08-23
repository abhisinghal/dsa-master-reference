<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  problemSlug: { type: String, required: true }
})

const bookmarked = ref(false)

const KEY = () => `dsa-bookmark:${props.problemSlug}`

onMounted(() => {
  try { bookmarked.value = localStorage.getItem(KEY()) === 'true' } catch (e) {}
})

function toggle() {
  bookmarked.value = !bookmarked.value
  try {
    if (bookmarked.value) {
      localStorage.setItem(KEY(), 'true')
      localStorage.setItem(`${KEY()}:ts`, String(Date.now()))
    } else {
      localStorage.removeItem(KEY())
      localStorage.removeItem(`${KEY()}:ts`)
    }
  } catch (e) {}
}
</script>

<template>
  <button
    :class="['bmk-btn', { active: bookmarked }]"
    @click="toggle"
    :aria-pressed="bookmarked"
    :title="bookmarked ? 'Remove bookmark' : 'Bookmark for later'"
  >
    <svg width="16" height="16" viewBox="0 0 24 24" :fill="bookmarked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
    </svg>
    <span>{{ bookmarked ? 'Bookmarked' : 'Bookmark' }}</span>
  </button>
</template>

<style scoped>
.bmk-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1.5px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  font-size: 0.85em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin: 4px 0;
}
.bmk-btn:hover { border-color: #f59e0b; color: #f59e0b; }
.bmk-btn.active {
  color: #f59e0b;
  border-color: #f59e0b;
  background: rgba(245, 158, 11, 0.08);
}
@media print { .bmk-btn { display: none !important; } }
</style>
