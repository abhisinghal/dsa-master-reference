<script setup>
import { ref, computed, onMounted } from 'vue'

const weeks = [
  { id: 1, label: 'W1 — Foundations' },
  { id: 2, label: 'W2 — Arrays / Hashing / Prefix Sum' },
  { id: 3, label: 'W3 — Two Pointers / Binary Search' },
  { id: 4, label: 'W4 — Stacks / Monotonic / SW Max' },
  { id: 5, label: 'W5 — Heaps / Top-K / K-way Merge' },
  { id: 6, label: 'W6 — Trees / BSTs / Trie' },
  { id: 7, label: 'W7 — Graphs / BFS-DFS / Topo / UF' },
  { id: 8, label: 'W8 — DP / Backtracking / Design' },
  { id: 9, label: 'W9-10 — Rehearsal' },
  { id: 11, label: 'W11-12 — Final push' },
]

const done = ref(new Set())

const KEY = 'dsa-roadmap-done'

onMounted(() => {
  if (typeof window === 'undefined') return
  try {
    const raw = localStorage.getItem(KEY)
    if (raw) done.value = new Set(JSON.parse(raw))
  } catch (e) {}
})

function toggle(id) {
  const next = new Set(done.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  done.value = next
  try { localStorage.setItem(KEY, JSON.stringify([...next])) } catch (e) {}
}

const progress = computed(() => Math.round((done.value.size / weeks.length) * 100))
</script>

<template>
  <div class="rc-panel">
    <div class="rc-head">
      <div class="rc-title">📅 My roadmap progress</div>
      <div class="rc-count">{{ done.size }} / {{ weeks.length }} weeks · {{ progress }}%</div>
    </div>
    <div class="rc-bar-wrap">
      <div class="rc-bar" :style="{ width: progress + '%' }"></div>
    </div>
    <ul class="rc-list">
      <li
        v-for="w in weeks"
        :key="w.id"
        :class="['rc-week', { done: done.has(w.id) }]"
        @click="toggle(w.id)"
      >
        <span class="rc-check">{{ done.has(w.id) ? '✓' : '☐' }}</span>
        <span class="rc-label">{{ w.label }}</span>
      </li>
    </ul>
    <div class="rc-hint">Click a week to toggle done. Progress persists on this device.</div>
  </div>
</template>

<style scoped>
.rc-panel {
  margin: 1.5rem 0;
  padding: 16px 20px;
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
}
.rc-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
}
.rc-title {
  font-weight: 700;
  font-size: 0.95em;
  color: var(--vp-c-brand-1);
}
.rc-count {
  font-size: 0.82em;
  color: var(--vp-c-text-2);
}
.rc-bar-wrap {
  height: 6px;
  background: var(--vp-c-divider);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 14px;
}
.rc-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--vp-c-brand-1), #22c55e);
  transition: width 0.4s ease;
}
.rc-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 6px;
}
.rc-week {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  cursor: pointer;
  transition: all 0.15s;
  font-size: 0.88em;
}
.rc-week:hover { border-color: var(--vp-c-brand-1); }
.rc-week.done {
  background: rgba(34, 197, 94, 0.08);
  border-color: #22c55e;
  color: var(--vp-c-text-2);
}
.rc-check {
  font-weight: 700;
  color: var(--vp-c-brand-1);
  min-width: 16px;
}
.rc-week.done .rc-check { color: #22c55e; }
.rc-week.done .rc-label { text-decoration: line-through; }
.rc-hint {
  margin-top: 10px;
  font-size: 0.75em;
  color: var(--vp-c-text-3);
  text-align: center;
}
</style>
