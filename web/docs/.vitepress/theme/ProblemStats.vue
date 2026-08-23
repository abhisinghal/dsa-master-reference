<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  total: { type: Number, default: 205 }
})

const solved = ref(0)
const loaded = ref(false)

onMounted(() => {
  if (typeof window === 'undefined') return
  let n = 0
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i) || ''
      if (!k.startsWith('dsa-solved:')) continue
      const v = localStorage.getItem(k)
      if (v === 'true') { n++; continue }
      try { if (JSON.parse(v).solved) n++ } catch (e) {}
    }
  } catch (e) {}
  solved.value = n
  loaded.value = true
})
</script>

<template>
  <div class="ps-panel">
    <div class="ps-row">
      <div class="ps-stat">
        <div class="ps-val">{{ loaded ? solved : '—' }}</div>
        <div class="ps-lbl">Solved by you</div>
      </div>
      <div class="ps-stat">
        <div class="ps-val">{{ total }}</div>
        <div class="ps-lbl">Total problems</div>
      </div>
      <div class="ps-stat">
        <div class="ps-val">{{ loaded ? Math.round((solved / total) * 100) + '%' : '—' }}</div>
        <div class="ps-lbl">Overall progress</div>
      </div>
    </div>
    <div class="ps-bar-wrap">
      <div class="ps-bar" :style="{ width: (loaded ? (solved / total) * 100 : 0) + '%' }"></div>
    </div>
    <div v-if="loaded && solved > 0" class="ps-tip">
      💡 Come back after a few days — the <a href="/">Due For Review</a> panel on the landing surfaces problems worth revisiting.
    </div>
  </div>
</template>

<style scoped>
.ps-panel {
  margin: 1.5rem 0;
  padding: 18px 22px;
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
}
.ps-row {
  display: flex;
  justify-content: space-around;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}
.ps-stat { text-align: center; min-width: 90px; }
.ps-val {
  font-size: 1.8em;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  line-height: 1;
}
.ps-lbl {
  font-size: 0.78em;
  color: var(--vp-c-text-2);
  margin-top: 4px;
}
.ps-bar-wrap {
  height: 6px;
  background: var(--vp-c-divider);
  border-radius: 3px;
  overflow: hidden;
}
.ps-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--vp-c-brand-1), #22c55e);
  transition: width 0.4s ease;
}
.ps-tip {
  margin-top: 10px;
  font-size: 0.85em;
  color: var(--vp-c-text-2);
  text-align: center;
}
</style>
