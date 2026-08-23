<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const props = defineProps<{
  patternId: string
  problems: string  // Comma-separated slugs
}>()

const solved = ref<Set<string>>(new Set())
const quizScore = ref(0)
const quizTotal = ref(0)

function refresh() {
  const set = new Set<string>()
  try {
    for (const slug of props.problems.split(',').map(s => s.trim()).filter(Boolean)) {
      if (localStorage.getItem(`dsa-solved:${slug}`) === 'true') set.add(slug)
    }
    solved.value = set
    // Quiz score
    const q = localStorage.getItem(`dsa-quiz:${props.patternId}`)
    if (q) {
      const parsed = JSON.parse(q)
      if (parsed.finished) {
        quizScore.value = parsed.score || 0
        quizTotal.value = parsed.total || 5
      }
    }
  } catch (e) {}
}

onMounted(refresh)

const problemList = computed(() => props.problems.split(',').map(s => s.trim()).filter(Boolean))
const solvedCount = computed(() => solved.value.size)
const totalCount = computed(() => problemList.value.length)
const percent = computed(() => totalCount.value === 0 ? 0 : Math.round(100 * solvedCount.value / totalCount.value))

const status = computed(() => {
  const solvedPct = percent.value
  const quizDone = quizTotal.value > 0
  if (solvedPct === 100 && quizDone && quizScore.value >= 4) return 'mastered'
  if (solvedPct >= 50) return 'in-progress'
  if (solvedPct > 0) return 'started'
  return 'not-started'
})

const statusLabel = computed(() => ({
  'not-started': 'Not started',
  'started': 'Started',
  'in-progress': 'In progress',
  'mastered': 'Mastered ✓',
})[status.value])
</script>

<template>
  <div :class="['pp-panel', 'status-' + status]">
    <div class="pp-header">
      <div class="pp-badge">Pattern Progress</div>
      <div class="pp-status">{{ statusLabel }}</div>
    </div>
    <div class="pp-bar-wrap">
      <div class="pp-bar-track">
        <div class="pp-bar-fill" :style="{ width: percent + '%' }"></div>
      </div>
      <div class="pp-percent">{{ percent }}%</div>
    </div>
    <div class="pp-meta">
      <div class="pp-meta-item">
        <span class="pp-meta-label">Problems solved</span>
        <span class="pp-meta-value">{{ solvedCount }} / {{ totalCount }}</span>
      </div>
      <div class="pp-meta-item">
        <span class="pp-meta-label">Quiz score</span>
        <span class="pp-meta-value">
          <template v-if="quizTotal > 0">{{ quizScore }} / {{ quizTotal }}</template>
          <template v-else>Not taken</template>
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pp-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 16px 20px;
  margin: 20px 0;
  background: var(--vp-c-bg-soft);
}
.pp-panel.status-mastered { border-color: #22c55e; background: rgba(34,197,94,0.05); }
.pp-panel.status-in-progress { border-color: #3b82f6; background: rgba(59,130,246,0.04); }
.pp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  flex-wrap: wrap;
  gap: 8px;
}
.pp-badge {
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 700;
}
.pp-status {
  font-size: 13px;
  color: var(--vp-c-text-2);
  font-weight: 600;
}
.pp-panel.status-mastered .pp-status { color: #16a34a; }
.pp-bar-wrap {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 10px;
}
.pp-bar-track {
  flex: 1;
  height: 10px;
  background: var(--vp-c-divider);
  border-radius: 5px;
  overflow: hidden;
}
.pp-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--vp-c-brand-1), var(--vp-c-brand-2));
  transition: width 0.4s ease;
  border-radius: 5px;
}
.pp-panel.status-mastered .pp-bar-fill {
  background: linear-gradient(90deg, #22c55e, #16a34a);
}
.pp-percent {
  font-size: 14px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  min-width: 44px;
  text-align: right;
}
.pp-meta {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}
.pp-meta-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.pp-meta-label {
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--vp-c-text-3);
  font-weight: 600;
}
.pp-meta-value {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--vp-c-text-1);
  font-family: ui-monospace, monospace;
}
</style>
