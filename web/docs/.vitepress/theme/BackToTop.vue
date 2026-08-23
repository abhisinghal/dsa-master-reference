<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const visible = ref(false)
let raf = null

const update = () => {
  visible.value = (window.scrollY || document.documentElement.scrollTop) > 400
  raf = null
}
const onScroll = () => { if (raf === null) raf = window.requestAnimationFrame(update) }

const scrollTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  if (typeof window === 'undefined') return
  window.addEventListener('scroll', onScroll, { passive: true })
  update()
})

onUnmounted(() => {
  if (typeof window !== 'undefined') window.removeEventListener('scroll', onScroll)
})
</script>

<template>
  <transition name="btt-fade">
    <button
      v-if="visible"
      class="btt-btn"
      @click="scrollTop"
      aria-label="Back to top"
      title="Back to top"
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
      </svg>
    </button>
  </transition>
</template>

<style scoped>
.btt-btn {
  position: fixed;
  right: 24px;
  bottom: 90px;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 1.5px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
  z-index: 999;
  transition: transform 0.15s, border-color 0.15s;
}
.btt-btn:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  transform: translateY(-2px);
}
.btt-fade-enter-active, .btt-fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.btt-fade-enter-from, .btt-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
@media print { .btt-btn { display: none !important; } }
</style>
