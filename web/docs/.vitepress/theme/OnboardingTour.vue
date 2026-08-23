<script setup lang="ts">
import { ref, onMounted } from 'vue'

const steps = [
  {
    title: 'Welcome!',
    body: 'This is a Java-native DSA reference optimized for senior/staff interviews. Everything runs in your browser — no signup, no server.',
    icon: '👋',
  },
  {
    title: '21 Core Patterns',
    body: 'Start with the pattern chapters (top nav). Each has a story intro, a canonical problem, code with learning notes, and a 5-question quiz.',
    icon: '🎯',
  },
  {
    title: '205 Interactive Problems',
    body: 'Every problem has an in-browser Java runner (CheerpJ), 3 progressive hints, company tags, and an AI companion for stuck-on-a-problem help.',
    icon: '💻',
  },
  {
    title: 'Progress Tracking',
    body: 'Your solved-count, quiz scores, and browsing history are saved to your browser. No account needed.',
    icon: '📊',
  },
  {
    title: 'Keyboard shortcuts',
    body: 'On any problem page, press H for hints, R for runner, A for AI companion. K opens search.',
    icon: '⌨️',
  },
  {
    title: 'You are ready',
    body: 'Suggested first stop: the 8-Week Roadmap. Or dive into any pattern chapter.',
    icon: '🚀',
  },
]

const visible = ref(false)
const step = ref(0)
const STORAGE_KEY = 'dsa-tour-completed'

onMounted(() => {
  try {
    if (localStorage.getItem(STORAGE_KEY) !== 'true') {
      // Delay slightly to avoid layout shift
      setTimeout(() => { visible.value = true }, 1200)
    }
  } catch (e) {}
})

function next() {
  if (step.value < steps.length - 1) step.value++
  else finish()
}
function prev() { if (step.value > 0) step.value-- }
function finish() {
  visible.value = false
  try { localStorage.setItem(STORAGE_KEY, 'true') } catch (e) {}
}
function open() {
  visible.value = true
  step.value = 0
}
defineExpose({ open })
</script>

<template>
  <transition name="tour">
    <div v-if="visible" class="tour-overlay" @click.self="finish">
      <div class="tour-card">
        <button class="tour-close" @click="finish" aria-label="Close">×</button>
        <div class="tour-icon">{{ steps[step].icon }}</div>
        <h3 class="tour-title">{{ steps[step].title }}</h3>
        <p class="tour-body">{{ steps[step].body }}</p>
        <div class="tour-dots">
          <span
            v-for="(_, i) in steps"
            :key="i"
            :class="['dot', { active: i === step, done: i < step }]"
          ></span>
        </div>
        <div class="tour-nav">
          <button v-if="step > 0" class="tour-btn ghost" @click="prev">Back</button>
          <button v-else class="tour-btn ghost" @click="finish">Skip</button>
          <button class="tour-btn primary" @click="next">
            {{ step === steps.length - 1 ? 'Start exploring' : 'Next' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.tour-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.55);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.tour-card {
  position: relative;
  background: var(--vp-c-bg);
  border-radius: 16px;
  padding: 32px 32px 24px;
  max-width: 460px;
  width: 100%;
  box-shadow: 0 24px 60px rgba(0,0,0,0.35);
  text-align: center;
}
.tour-close {
  position: absolute;
  top: 12px;
  right: 14px;
  background: transparent;
  border: none;
  color: var(--vp-c-text-3);
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
.tour-close:hover { background: var(--vp-c-divider); color: var(--vp-c-text-1); }
.tour-icon { font-size: 48px; margin-bottom: 12px; }
.tour-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin: 0 0 8px;
}
.tour-body {
  font-size: 14px;
  color: var(--vp-c-text-2);
  line-height: 1.5;
  margin: 0 0 20px;
}
.tour-dots {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-bottom: 20px;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--vp-c-divider);
  transition: all 0.2s;
}
.dot.active { background: var(--vp-c-brand-1); width: 24px; border-radius: 4px; }
.dot.done { background: var(--vp-c-brand-2); }
.tour-nav {
  display: flex;
  gap: 8px;
  justify-content: center;
}
.tour-btn {
  padding: 10px 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.tour-btn.ghost { background: transparent; }
.tour-btn.primary {
  background: var(--vp-c-brand-1);
  color: white;
  border-color: var(--vp-c-brand-1);
}
.tour-btn.primary:hover { background: var(--vp-c-brand-2); }
.tour-btn.ghost:hover { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); }
.tour-enter-active, .tour-leave-active { transition: opacity 0.25s ease; }
.tour-enter-from, .tour-leave-to { opacity: 0; }
</style>
