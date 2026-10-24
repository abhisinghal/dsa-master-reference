<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  statement: string
  initialization: string
  maintenance: string
  termination: string
  defaultOpen?: boolean
}>()

const open = ref(false)
</script>

<template>
  <div class="invariant-proof">
    <div class="invariant-head">
      <span class="invariant-badge">Invariant</span>
      <span class="invariant-statement">{{ statement }}</span>
    </div>
    <button
      class="invariant-toggle"
      type="button"
      :aria-expanded="open || !!defaultOpen"
      @click="open = !open"
    >
      <span class="caret" :class="{ 'caret-open': open || defaultOpen }">▸</span>
      {{ (open || defaultOpen) ? 'Hide proof' : 'Show proof (init · maintenance · termination)' }}
    </button>
    <div v-if="open || defaultOpen" class="invariant-body">
      <div class="proof-strip">
        <div class="proof-cell">
          <div class="proof-label">Initialization</div>
          <div class="proof-text">{{ initialization }}</div>
        </div>
        <div class="proof-cell">
          <div class="proof-label">Maintenance</div>
          <div class="proof-text">{{ maintenance }}</div>
        </div>
        <div class="proof-cell">
          <div class="proof-label">Termination</div>
          <div class="proof-text">{{ termination }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.invariant-proof {
  margin: 18px 0;
  padding: 14px 16px;
  background: var(--dsa-info-soft, color-mix(in srgb, var(--vp-c-brand-1) 10%, var(--vp-c-bg-soft)));
  border-left: 3px solid var(--dsa-info, var(--vp-c-brand-1));
  border-radius: 8px;
}
.invariant-head {
  display: flex;
  gap: 10px;
  align-items: baseline;
  flex-wrap: wrap;
}
.invariant-badge {
  font-size: 0.68em;
  font-weight: 800;
  color: var(--dsa-info, var(--vp-c-brand-1));
  text-transform: uppercase;
  letter-spacing: 1px;
}
.invariant-statement {
  font-weight: 600;
  color: var(--vp-c-text-1);
  line-height: 1.5;
}
.invariant-toggle {
  margin-top: 10px;
  padding: 0;
  background: transparent;
  border: none;
  color: var(--vp-c-text-2);
  font-size: 0.85em;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
}
.invariant-toggle:hover {
  color: var(--vp-c-text-1);
}
.caret {
  display: inline-block;
  transition: transform 0.18s ease;
  font-size: 0.7em;
}
.caret-open {
  transform: rotate(90deg);
}
.invariant-body {
  margin-top: 12px;
}
.proof-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
@media (max-width: 600px) {
  .proof-strip {
    grid-template-columns: 1fr;
  }
}
.proof-cell {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 10px 12px;
}
.proof-label {
  font-size: 0.7em;
  font-weight: 800;
  color: var(--dsa-info, var(--vp-c-brand-1));
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 6px;
}
.proof-text {
  font-size: 0.9em;
  line-height: 1.5;
  color: var(--vp-c-text-1);
}
</style>
