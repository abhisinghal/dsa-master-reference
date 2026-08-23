<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{
  problemSlug: string
}>()

const solved = ref(false)
const showConfetti = ref(false)

onMounted(() => {
  try {
    const raw = localStorage.getItem(`dsa-solved:${props.problemSlug}`)
    if (!raw) { solved.value = false; return }
    // Backward compatibility: old format was the literal string 'true'.
    if (raw === 'true') { solved.value = true; return }
    try {
      const data = JSON.parse(raw)
      solved.value = !!(data && data.solved)
    } catch (e) { solved.value = false }
  } catch (e) {}
})

function toggle() {
  solved.value = !solved.value
  try {
    if (solved.value) {
      localStorage.setItem(`dsa-solved:${props.problemSlug}`, JSON.stringify({ solved: true, timestamp: Date.now() }))
      showConfetti.value = true
      setTimeout(() => { showConfetti.value = false }, 1500)
    } else {
      localStorage.removeItem(`dsa-solved:${props.problemSlug}`)
    }
  } catch (e) {}
  // Broadcast for other listeners (progress bars, etc.)
  window.dispatchEvent(new CustomEvent('dsa-solved-toggled', { detail: { slug: props.problemSlug, solved: solved.value } }))
}
</script>

<template>
  <div class="mark-panel">
    <button
      :class="['mark-btn', { solved }]"
      @click="toggle"
      :aria-pressed="solved"
    >
      <span class="mark-icon">{{ solved ? '✓' : '☐' }}</span>
      <span class="mark-label">{{ solved ? 'Marked as solved' : 'Mark as solved' }}</span>
    </button>
    <div v-if="showConfetti" class="confetti" aria-hidden="true">
      <span class="c">✨</span><span class="c">🎉</span><span class="c">✨</span>
    </div>
  </div>
</template>

<style scoped>
.mark-panel {
  position: relative;
  margin: 16px 0;
  display: inline-flex;
}
.mark-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: 1.5px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.mark-btn:hover { border-color: var(--vp-c-brand-1); }
.mark-btn.solved {
  background: #22c55e;
  border-color: #22c55e;
  color: white;
}
.mark-btn.solved:hover {
  background: #16a34a;
  border-color: #16a34a;
}
.mark-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
}
.mark-btn:not(.solved) .mark-icon {
  background: transparent;
  border: 1.5px solid var(--vp-c-divider);
}
.confetti {
  position: absolute;
  inset: 0;
  pointer-events: none;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
  animation: pop 1.5s ease-out forwards;
}
.confetti .c { font-size: 20px; }
@keyframes pop {
  0% { transform: scale(0.5) translateY(0); opacity: 0; }
  30% { transform: scale(1) translateY(-20px); opacity: 1; }
  100% { transform: scale(0.8) translateY(-60px); opacity: 0; }
}
</style>
