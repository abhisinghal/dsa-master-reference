<script setup>
import { ref, onMounted } from 'vue'

const items = ref([])

const slugToTitle = (slug) => slug.split('-').map(w => {
  if (w.toLowerCase() === 'ii') return 'II'
  if (w.toLowerCase() === 'iii') return 'III'
  if (w.toLowerCase() === 'iv') return 'IV'
  return w[0].toUpperCase() + w.slice(1)
}).join(' ')

const url = (slug) => `/problems/${slug}`

onMounted(() => {
  if (typeof window === 'undefined') return
  const list = []
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i) || ''
      if (k.startsWith('dsa-bookmark:') && !k.endsWith(':ts') && localStorage.getItem(k) === 'true') {
        const slug = k.slice('dsa-bookmark:'.length)
        const tsRaw = localStorage.getItem(`${k}:ts`)
        const ts = tsRaw ? parseInt(tsRaw, 10) : 0
        list.push({ slug, ts })
      }
    }
  } catch (e) {}
  list.sort((a, b) => b.ts - a.ts)
  items.value = list.slice(0, 10)
})

function remove(slug) {
  try {
    localStorage.removeItem(`dsa-bookmark:${slug}`)
    localStorage.removeItem(`dsa-bookmark:${slug}:ts`)
  } catch (e) {}
  items.value = items.value.filter(i => i.slug !== slug)
}
</script>

<template>
  <div v-if="items.length" class="bml-panel">
    <div class="bml-title">🔖 Your bookmarks ({{ items.length }})</div>
    <ul class="bml-list">
      <li v-for="item in items" :key="item.slug">
        <a :href="url(item.slug)" class="bml-link">{{ slugToTitle(item.slug) }}</a>
        <button class="bml-remove" @click="remove(item.slug)" title="Remove bookmark" aria-label="Remove bookmark">×</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.bml-panel {
  margin: 1rem 0;
  padding: 14px 18px;
  border-left: 3px solid #f59e0b;
  background: rgba(245, 158, 11, 0.06);
  border-radius: 6px;
}
.bml-title {
  font-size: 0.85em;
  font-weight: 700;
  color: #d97706;
  margin-bottom: 8px;
}
.bml-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.bml-list li {
  display: flex;
  align-items: center;
  padding: 4px 0;
  border-bottom: 1px solid var(--vp-c-divider);
}
.bml-list li:last-child { border-bottom: none; }
.bml-link {
  flex: 1;
  color: var(--vp-c-text-1);
  text-decoration: none;
  font-size: 0.9em;
}
.bml-link:hover { color: #d97706; }
.bml-remove {
  background: none;
  border: none;
  color: var(--vp-c-text-3);
  font-size: 18px;
  cursor: pointer;
  padding: 0 6px;
}
.bml-remove:hover { color: #ef4444; }
</style>
