<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const progress = ref(0)
let raf = null

const update = () => {
  const scrollTop = window.scrollY || document.documentElement.scrollTop
  const height = document.documentElement.scrollHeight - window.innerHeight
  progress.value = height > 0 ? Math.min(100, (scrollTop / height) * 100) : 0
  raf = null
}

const onScroll = () => {
  if (raf === null) raf = window.requestAnimationFrame(update)
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
  <div class="rpb-track" aria-hidden="true">
    <div class="rpb-fill" :style="{ width: progress + '%' }"></div>
  </div>
</template>

<style scoped>
.rpb-track {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: transparent;
  z-index: 1000;
  pointer-events: none;
}
.rpb-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--vp-c-brand-1), #8b5cf6);
  transition: width 0.05s linear;
  box-shadow: 0 0 6px rgba(37, 99, 235, 0.4);
}
</style>
