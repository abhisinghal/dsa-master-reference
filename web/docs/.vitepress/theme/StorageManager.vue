<script setup lang="ts">
import { ref, onMounted } from 'vue'

/**
 * StorageManager — export/import all localStorage-tracked progress.
 * Users can save their data locally (JSON) and restore across browsers
 * or devices without needing an account.
 */

const stats = ref({ solved: 0, quiz: 0, feedback: 0, views: 0 })
const message = ref('')

function refresh() {
  try {
    let solved = 0, quiz = 0, feedback = 0
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i) || ''
      if (k.startsWith('dsa-solved:')) {
        const v = localStorage.getItem(k)
        if (v === 'true') { solved++ }
        else { try { if (JSON.parse(v).solved) solved++ } catch (e) {} }
      }
      else if (k.startsWith('dsa-quiz:')) quiz++
      else if (k.startsWith('dsa-feedback:')) feedback++
    }
    let views = 0
    try {
      const raw = localStorage.getItem('dsa-page-views')
      if (raw) views = JSON.parse(raw).__total__ || 0
    } catch (e) {}
    stats.value = { solved, quiz, feedback, views }
  } catch (e) {}
}
onMounted(refresh)

function exportData() {
  try {
    const dump: Record<string, string> = {}
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i) || ''
      if (k.startsWith('dsa-')) dump[k] = localStorage.getItem(k) || ''
    }
    const blob = new Blob([JSON.stringify({ version: 1, exportedAt: new Date().toISOString(), data: dump }, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `dsa-master-reference-progress-${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    URL.revokeObjectURL(url)
    message.value = 'Downloaded backup file.'
    setTimeout(() => { message.value = '' }, 3000)
  } catch (e) {
    message.value = 'Export failed.'
  }
}

function importData(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (ev) => {
    try {
      const parsed = JSON.parse(ev.target?.result as string)
      const data = parsed.data || {}
      for (const [k, v] of Object.entries(data)) {
        if (k.startsWith('dsa-')) localStorage.setItem(k, v as string)
      }
      message.value = `Imported ${Object.keys(data).length} items.`
      refresh()
      setTimeout(() => { message.value = '' }, 3000)
    } catch (e) {
      message.value = 'Import failed — invalid JSON.'
    }
  }
  reader.readAsText(file)
  target.value = ''
}

function clearAll() {
  if (!confirm('Clear ALL local progress? This cannot be undone.')) return
  try {
    const keys: string[] = []
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i) || ''
      if (k.startsWith('dsa-')) keys.push(k)
    }
    keys.forEach(k => localStorage.removeItem(k))
    refresh()
    message.value = `Cleared ${keys.length} local items.`
    setTimeout(() => { message.value = '' }, 3000)
  } catch (e) {}
}
</script>

<template>
  <div class="sm-panel">
    <div class="sm-header">
      <div class="sm-badge">Your Progress</div>
      <div class="sm-title">Local Data Manager</div>
    </div>
    <div class="sm-stats">
      <div class="sm-stat"><div class="v">{{ stats.solved }}</div><div class="l">Solved</div></div>
      <div class="sm-stat"><div class="v">{{ stats.quiz }}</div><div class="l">Quizzes</div></div>
      <div class="sm-stat"><div class="v">{{ stats.feedback }}</div><div class="l">Feedback</div></div>
      <div class="sm-stat"><div class="v">{{ stats.views }}</div><div class="l">Page views</div></div>
    </div>
    <div class="sm-actions">
      <button class="sm-btn primary" @click="exportData">↓ Export (JSON)</button>
      <label class="sm-btn ghost">
        ↑ Import
        <input type="file" accept="application/json" @change="importData" style="display:none" />
      </label>
      <button class="sm-btn danger" @click="clearAll">Clear all</button>
    </div>
    <div v-if="message" class="sm-msg">{{ message }}</div>
    <div class="sm-fine">
      All progress is stored in your browser. Nothing is sent to a server. Export to move between devices.
    </div>
  </div>
</template>

<style scoped>
.sm-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 20px 24px;
  margin: 24px 0;
  background: var(--vp-c-bg-soft);
}
.sm-header { margin-bottom: 14px; }
.sm-badge {
  display: inline-block;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 700;
  margin-bottom: 6px;
}
.sm-title { font-size: 16px; font-weight: 700; color: var(--vp-c-text-1); }
.sm-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: 8px;
  margin-bottom: 14px;
}
.sm-stat {
  text-align: center;
  padding: 10px 4px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}
.sm-stat .v { font-size: 20px; font-weight: 800; color: var(--vp-c-brand-1); }
.sm-stat .l { font-size: 10.5px; color: var(--vp-c-text-3); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }
.sm-actions { display: flex; gap: 6px; flex-wrap: wrap; }
.sm-btn {
  padding: 8px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.sm-btn.primary { background: var(--vp-c-brand-1); color: white; border-color: var(--vp-c-brand-1); }
.sm-btn.primary:hover { background: var(--vp-c-brand-2); }
.sm-btn.ghost:hover { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); }
.sm-btn.danger { color: #dc2626; border-color: rgba(220,38,38,0.4); }
.sm-btn.danger:hover { background: rgba(220,38,38,0.08); border-color: #dc2626; }
.sm-msg {
  margin-top: 10px;
  font-size: 12.5px;
  color: #16a34a;
  font-weight: 500;
}
.sm-fine {
  font-size: 11px;
  color: var(--vp-c-text-3);
  margin-top: 10px;
  font-style: italic;
}
</style>
