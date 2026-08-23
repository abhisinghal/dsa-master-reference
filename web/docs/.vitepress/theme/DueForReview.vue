<script setup>
import { ref, onMounted } from 'vue'

const dueItems = ref([])
const totalSolved = ref(0)

const REVIEW_DAYS = 7

onMounted(() => {
  if (typeof window === 'undefined') return
  const now = Date.now()
  const cutoff = now - REVIEW_DAYS * 24 * 60 * 60 * 1000
  const items = []
  let solved = 0
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i)
    if (!key || !key.startsWith('dsa-solved:')) continue
    const raw = localStorage.getItem(key)
    if (!raw) continue
    try {
      const data = JSON.parse(raw)
      if (data && data.solved) {
        solved++
        const ts = data.timestamp || 0
        if (ts && ts < cutoff) {
          const slug = key.slice('dsa-solved:'.length)
          items.push({ slug, ts, days: Math.floor((now - ts) / 86400000) })
        }
      }
    } catch (e) {}
  }
  totalSolved.value = solved
  items.sort((a, b) => a.ts - b.ts)
  dueItems.value = items.slice(0, 5)
})

const slugToTitle = (slug) => slug.split('-').map(w => w[0].toUpperCase() + w.slice(1)).join(' ')
const url = (slug) => `/problems/${slug}`
</script>

<template>
  <div v-if="dueItems.length" class="dfr-panel">
    <div class="dfr-title">🔁 Due for review</div>
    <div class="dfr-sub">Spaced repetition: you last solved these {{ REVIEW_DAYS }}+ days ago. Give them another pass.</div>
    <ul class="dfr-list">
      <li v-for="item in dueItems" :key="item.slug">
        <a :href="url(item.slug)" class="dfr-link">
          <span class="dfr-name">{{ slugToTitle(item.slug) }}</span>
          <span class="dfr-days">{{ item.days }}d ago</span>
        </a>
      </li>
    </ul>
  </div>
  <div v-else-if="totalSolved > 0" class="dfr-empty">
    ✅ All {{ totalSolved }} solved problems are within the 7-day recall window. Keep going.
  </div>
</template>

<style scoped>
.dfr-panel {
  margin: 1.5rem 0;
  padding: 14px 18px;
  border: 1px solid var(--vp-c-warning-1, #d97706);
  background: var(--vp-c-warning-soft, rgba(217, 119, 6, 0.08));
  border-radius: 6px;
}
.dfr-title {
  font-size: 0.85em;
  font-weight: 700;
  color: var(--vp-c-warning-1, #d97706);
  letter-spacing: 0.02em;
  margin-bottom: 4px;
}
.dfr-sub {
  font-size: 0.82em;
  color: var(--vp-c-text-2);
  margin-bottom: 10px;
}
.dfr-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.dfr-list li {
  margin: 4px 0;
}
.dfr-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  border-radius: 4px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  text-decoration: none;
  color: var(--vp-c-text-1);
  font-size: 0.9em;
}
.dfr-link:hover {
  border-color: var(--vp-c-warning-1, #d97706);
}
.dfr-name { font-weight: 500; }
.dfr-days { font-size: 0.78em; color: var(--vp-c-text-3); }
.dfr-empty {
  margin: 1rem 0;
  padding: 10px 14px;
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  font-size: 0.88em;
}
</style>
