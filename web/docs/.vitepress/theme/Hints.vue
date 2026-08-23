<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  hint1: string
  hint2?: string
  hint3?: string
}>()

const revealed = ref(0)

function reveal() {
  const max = props.hint3 ? 3 : props.hint2 ? 2 : 1
  if (revealed.value < max) revealed.value++
}
function hide() { revealed.value = 0 }

const hints = () => [props.hint1, props.hint2, props.hint3].filter(Boolean) as string[]
</script>

<template>
  <div class="hint-panel">
    <div class="hint-header">
      <div class="hint-badge">Progressive Hints</div>
      <div class="hint-controls">
        <button v-if="revealed > 0" class="hint-btn" @click="hide" title="Hide">↺</button>
        <button
          v-if="revealed < hints().length"
          class="hint-btn primary"
          @click="reveal"
        >
          {{ revealed === 0 ? 'Show Hint 1' : `Show Hint ${revealed + 1}` }}
        </button>
        <span v-else class="hint-done">All hints shown</span>
      </div>
    </div>
    <div v-if="revealed >= 1" class="hint-item">
      <span class="hint-num">1</span>
      <div class="hint-text">{{ props.hint1 }}</div>
    </div>
    <div v-if="revealed >= 2 && props.hint2" class="hint-item">
      <span class="hint-num">2</span>
      <div class="hint-text">{{ props.hint2 }}</div>
    </div>
    <div v-if="revealed >= 3 && props.hint3" class="hint-item">
      <span class="hint-num">3</span>
      <div class="hint-text">{{ props.hint3 }}</div>
    </div>
    <div v-if="revealed === 0" class="hint-nudge">
      Try to solve it yourself first. Reveal hints only when stuck — each hint is progressively more specific.
    </div>
  </div>
</template>

<style scoped>
.hint-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 16px;
  margin: 20px 0;
  background: linear-gradient(135deg, rgba(250,204,21,0.06), rgba(59,130,246,0.03));
}
.hint-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.hint-badge {
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(250,204,21,0.15);
  color: #ca8a04;
  font-weight: 700;
}
:global(.dark) .hint-badge {
  background: rgba(250,204,21,0.18);
  color: #fbbf24;
}
.hint-controls {
  display: flex;
  gap: 6px;
  align-items: center;
}
.hint-btn {
  padding: 6px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.hint-btn:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.hint-btn.primary {
  background: var(--vp-c-brand-1);
  color: white;
  border-color: var(--vp-c-brand-1);
}
.hint-btn.primary:hover {
  background: var(--vp-c-brand-2);
  color: white;
}
.hint-done {
  font-size: 12px;
  color: var(--vp-c-text-3);
  font-style: italic;
}
.hint-item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 10px 12px;
  margin-top: 8px;
  background: var(--vp-c-bg);
  border-left: 3px solid #f59e0b;
  border-radius: 4px;
}
.hint-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #f59e0b;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}
.hint-text {
  font-size: 13.5px;
  line-height: 1.5;
  color: var(--vp-c-text-1);
}
.hint-nudge {
  font-size: 12px;
  color: var(--vp-c-text-3);
  font-style: italic;
  padding: 6px 4px;
}
</style>
