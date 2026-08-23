<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

/**
 * StreakTracker — counts consecutive days of practice.
 * "Practice" defined as: solving any problem OR taking any quiz OR
 * marking any progress within a 24-hour window.
 */

const streak = ref(0)
const lastDay = ref('')
const longest = ref(0)

const KEY = 'dsa-streak'

function todayKey(): string {
  const d = new Date()
  return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`
}

onMounted(() => {
  try {
    const raw = localStorage.getItem(KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      const today = todayKey()
      const yesterdayD = new Date()
      yesterdayD.setDate(yesterdayD.getDate() - 1)
      const yKey = `${yesterdayD.getFullYear()}-${yesterdayD.getMonth() + 1}-${yesterdayD.getDate()}`
      if (parsed.lastDay === today) {
        // Same day: no change
        streak.value = parsed.streak || 1
      } else if (parsed.lastDay === yKey) {
        // Consecutive day: increment
        streak.value = (parsed.streak || 0) + 1
      } else {
        // Broken streak
        streak.value = 1
      }
      longest.value = Math.max(parsed.longest || 0, streak.value)
      lastDay.value = today
      localStorage.setItem(KEY, JSON.stringify({
        streak: streak.value,
        longest: longest.value,
        lastDay: today,
      }))
    } else {
      streak.value = 1
      longest.value = 1
      lastDay.value = todayKey()
      localStorage.setItem(KEY, JSON.stringify({
        streak: 1,
        longest: 1,
        lastDay: lastDay.value,
      }))
    }
  } catch (e) {}
})

const flame = computed(() => {
  if (streak.value >= 30) return '🔥🔥🔥'
  if (streak.value >= 14) return '🔥🔥'
  if (streak.value >= 3) return '🔥'
  return '⭐'
})

const message = computed(() => {
  if (streak.value >= 30) return "Legendary streak. Keep going."
  if (streak.value >= 14) return "Two-week momentum. You're building the habit."
  if (streak.value >= 7) return "One week in. Consistency compounds."
  if (streak.value >= 3) return "Three days in a row. Nice."
  if (streak.value >= 1) return "Day 1. Come back tomorrow."
  return ""
})
</script>

<template>
  <div class="streak-panel">
    <div class="streak-icon">{{ flame }}</div>
    <div class="streak-body">
      <div class="streak-label">Practice streak</div>
      <div class="streak-value">{{ streak }} <span class="unit">{{ streak === 1 ? 'day' : 'days' }}</span></div>
      <div class="streak-msg">{{ message }}</div>
    </div>
    <div v-if="longest > streak" class="streak-longest">
      <div class="longest-label">Longest</div>
      <div class="longest-value">{{ longest }} days</div>
    </div>
  </div>
</template>

<style scoped>
.streak-panel {
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 16px 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(245,158,11,0.06), rgba(239,68,68,0.03));
  margin: 20px 0;
}
.streak-icon { font-size: 34px; flex-shrink: 0; }
.streak-body { flex: 1; }
.streak-label {
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--vp-c-text-3);
  font-weight: 600;
}
.streak-value {
  font-size: 22px;
  font-weight: 800;
  color: var(--vp-c-text-1);
  line-height: 1.1;
  margin-top: 3px;
}
.streak-value .unit {
  font-size: 12.5px;
  font-weight: 500;
  color: var(--vp-c-text-2);
}
.streak-msg { font-size: 12px; color: var(--vp-c-text-2); margin-top: 4px; }
.streak-longest {
  text-align: right;
  padding-left: 12px;
  border-left: 1px solid var(--vp-c-divider);
}
.longest-label { font-size: 10.5px; color: var(--vp-c-text-3); text-transform: uppercase; letter-spacing: 0.05em; }
.longest-value { font-size: 15px; font-weight: 700; color: var(--vp-c-text-1); }
</style>
