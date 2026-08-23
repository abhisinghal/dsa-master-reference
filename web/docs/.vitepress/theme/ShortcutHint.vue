<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  hasHints?: boolean
  hasRunner?: boolean
  hasAi?: boolean
}>()

const visible = ref(true)
const STORAGE_KEY = 'dsa-shortcut-hint-shown'

onMounted(() => {
  try {
    if (localStorage.getItem(STORAGE_KEY) === 'true') {
      visible.value = false
    } else {
      // Show for 8 seconds on first visit
      setTimeout(() => {
        visible.value = false
        try { localStorage.setItem(STORAGE_KEY, 'true') } catch (e) {}
      }, 8000)
    }
  } catch (e) {}

  window.addEventListener('keydown', handleKey)
})
onUnmounted(() => window.removeEventListener('keydown', handleKey))

function scrollToId(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function handleKey(e: KeyboardEvent) {
  // Ignore when typing in inputs
  const target = e.target as HTMLElement
  if (target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable)) return
  if (e.key === 'h' || e.key === 'H') {
    // scroll to Hints
    const el = document.querySelector('.hint-panel')
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  } else if (e.key === 'r' || e.key === 'R') {
    const el = document.querySelector('.jr-panel, .java-runner')
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  } else if (e.key === 'a' || e.key === 'A') {
    const el = document.querySelector('.ai-panel')
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }
}

function dismiss() {
  visible.value = false
  try { localStorage.setItem(STORAGE_KEY, 'true') } catch (e) {}
}
</script>

<template>
  <transition name="dbar">
    <div v-if="visible" class="dbar">
      <div class="dbar-content">
        <div class="dbar-title">💡 Quick shortcuts</div>
        <div class="dbar-items">
          <span class="dbar-item"><kbd>H</kbd> Hints</span>
          <span class="dbar-item"><kbd>R</kbd> Run Java</span>
          <span class="dbar-item"><kbd>A</kbd> AI Help</span>
        </div>
      </div>
      <button class="dbar-close" @click="dismiss" aria-label="Dismiss">×</button>
    </div>
  </transition>
</template>

<style scoped>
.dbar {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 100;
  background: linear-gradient(135deg, var(--vp-c-brand-1), var(--vp-c-brand-2));
  color: white;
  padding: 12px 16px;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  display: flex;
  gap: 12px;
  align-items: center;
  max-width: 92vw;
}
.dbar-content { flex: 1; }
.dbar-title { font-size: 12px; font-weight: 700; margin-bottom: 4px; opacity: 0.95; }
.dbar-items { display: flex; gap: 12px; flex-wrap: wrap; }
.dbar-item {
  font-size: 11.5px;
  display: flex;
  gap: 4px;
  align-items: center;
  opacity: 0.95;
}
kbd {
  display: inline-block;
  min-width: 16px;
  padding: 1px 4px;
  background: rgba(255,255,255,0.25);
  border-radius: 3px;
  font-family: ui-monospace, monospace;
  font-size: 10px;
  font-weight: 700;
  text-align: center;
}
.dbar-close {
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.8);
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
  padding: 0;
  width: 22px;
  height: 22px;
}
.dbar-close:hover { color: white; }
.dbar-enter-active, .dbar-leave-active { transition: all 0.3s ease; }
.dbar-enter-from, .dbar-leave-to { transform: translateY(20px); opacity: 0; }
@media (max-width: 600px) {
  .dbar { left: 10px; right: 10px; bottom: 10px; }
}
</style>
