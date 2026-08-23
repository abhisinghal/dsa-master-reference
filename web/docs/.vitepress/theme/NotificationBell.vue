<script setup>
import { ref, onMounted } from 'vue'

const streak = ref(0)
const showBell = ref(false)
const dismissed = ref(false)

const DISMISS_KEY = 'dsa-bell-dismissed-day'

const today = () => new Date().toISOString().slice(0, 10)

function checkTodayActivity() {
  const t = today()
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i) || ''
      if (!k.startsWith('dsa-solved:')) continue
      const v = localStorage.getItem(k)
      if (!v || v === 'true') continue
      try {
        const data = JSON.parse(v)
        if (data.timestamp && new Date(data.timestamp).toISOString().slice(0, 10) === t) {
          return true
        }
      } catch (e) {}
    }
  } catch (e) {}
  return false
}

function loadStreak() {
  try {
    const raw = localStorage.getItem('dsa-streak')
    if (!raw) return 0
    const data = JSON.parse(raw)
    return data.count || 0
  } catch (e) { return 0 }
}

function dismiss() {
  dismissed.value = true
  showBell.value = false
  try { localStorage.setItem(DISMISS_KEY, today()) } catch (e) {}
}

onMounted(() => {
  if (typeof window === 'undefined') return
  setTimeout(() => {
    try {
      const dismissedDay = localStorage.getItem(DISMISS_KEY)
      if (dismissedDay === today()) return
    } catch (e) {}

    streak.value = loadStreak()
    if (streak.value >= 2 && !checkTodayActivity()) {
      showBell.value = true
    }
  }, 2500)
})
</script>

<template>
  <transition name="bell-fade">
    <div v-if="showBell && !dismissed" class="bell-panel" role="alert">
      <button class="bell-close" @click="dismiss" aria-label="Dismiss">×</button>
      <div class="bell-icon">🔔</div>
      <div class="bell-body">
        <div class="bell-title">Keep your {{ streak }}-day streak alive</div>
        <div class="bell-sub">Solve one problem today to extend it.</div>
        <a href="/problems/" class="bell-cta">Pick a problem →</a>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.bell-panel {
  position: fixed;
  left: 24px;
  bottom: 24px;
  max-width: 320px;
  padding: 14px 18px 14px 16px;
  border-radius: 12px;
  background: var(--vp-c-bg);
  border: 1.5px solid #f97316;
  box-shadow: 0 6px 24px rgba(249, 115, 22, 0.25);
  display: flex;
  gap: 12px;
  align-items: flex-start;
  z-index: 999;
}
.bell-icon {
  font-size: 1.5em;
  line-height: 1.1;
}
.bell-body { flex: 1; }
.bell-title {
  font-weight: 700;
  font-size: 0.95em;
  color: var(--vp-c-text-1);
  margin-bottom: 3px;
}
.bell-sub {
  font-size: 0.82em;
  color: var(--vp-c-text-2);
  margin-bottom: 8px;
}
.bell-cta {
  display: inline-block;
  font-size: 0.85em;
  font-weight: 600;
  color: #f97316;
  text-decoration: none;
}
.bell-cta:hover { text-decoration: underline; }
.bell-close {
  position: absolute;
  top: 4px;
  right: 8px;
  background: none;
  border: none;
  font-size: 20px;
  color: var(--vp-c-text-3);
  cursor: pointer;
  line-height: 1;
  padding: 2px 6px;
}
.bell-close:hover { color: var(--vp-c-text-1); }
.bell-fade-enter-active, .bell-fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}
.bell-fade-enter-from, .bell-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
@media print { .bell-panel { display: none !important; } }
</style>
