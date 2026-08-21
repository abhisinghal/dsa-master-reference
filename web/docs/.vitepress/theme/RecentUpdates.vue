<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'

type RecentUpdate = {
  title: string
  url: string
  updated: string
}

const updates = ref<RecentUpdate[]>([])
const loaded = ref(false)

const hasUpdates = computed(() => updates.value.length > 0)

function formatUpdated(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value

  const diffMs = Date.now() - date.getTime()
  const absMs = Math.abs(diffMs)
  const units = [
    { label: 'year', ms: 365 * 24 * 60 * 60 * 1000 },
    { label: 'month', ms: 30 * 24 * 60 * 60 * 1000 },
    { label: 'week', ms: 7 * 24 * 60 * 60 * 1000 },
    { label: 'day', ms: 24 * 60 * 60 * 1000 },
    { label: 'hour', ms: 60 * 60 * 1000 },
    { label: 'minute', ms: 60 * 1000 }
  ]

  const unit = units.find((candidate) => absMs >= candidate.ms)
  if (!unit) return 'Updated just now'

  const amount = Math.round(absMs / unit.ms)
  const label = amount === 1 ? unit.label : `${unit.label}s`
  return diffMs >= 0 ? `Updated ${amount} ${label} ago` : `Updated in ${amount} ${label}`
}

onMounted(async () => {
  try {
    const response = await fetch(withBase('/recent.json'))
    if (!response.ok) return

    const data = await response.json()
    if (Array.isArray(data)) {
      updates.value = data.filter((item) => item?.title && item?.url && item?.updated)
    }
    loaded.value = true
  } catch {
    loaded.value = false
  }
})
</script>

<template>
  <p v-if="!loaded && !hasUpdates" class="recent-placeholder">Loading recent updates...</p>
  <div v-else class="recent-grid">
    <a v-for="item in updates" :key="item.url" class="recent-card" :href="withBase(item.url)">
      <div class="recent-title">{{ item.title }}</div>
      <div class="recent-date">{{ formatUpdated(item.updated) }}</div>
    </a>
  </div>
</template>

<style scoped>
.recent-placeholder {
  color: var(--vp-c-text-2);
}

.recent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin: 16px 0 28px;
}

.recent-card {
  display: block;
  padding: 16px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 14px;
  background: color-mix(in srgb, var(--vp-c-bg-soft) 72%, transparent);
  text-decoration: none;
  transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease;
}

.recent-card:hover {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  transform: translateY(-2px);
}

.recent-title {
  color: var(--vp-c-text-1);
  font-weight: 700;
  line-height: 1.35;
}

.recent-date {
  margin-top: 8px;
  color: var(--vp-c-text-2);
  font-size: 0.9em;
}
</style>
