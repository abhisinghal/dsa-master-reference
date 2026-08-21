<script setup lang="ts">
interface Step {
  svg: string    // raw inline SVG markup
  caption: string
}

defineProps<{
  title?: string
  steps: Step[]
}>()
</script>

<template>
  <figure class="step-strip">
    <figcaption v-if="title" class="step-strip-title">{{ title }}</figcaption>
    <div class="step-strip-track">
      <div v-for="(s, i) in steps" :key="i" class="step-cell">
        <div class="step-index">Step {{ i + 1 }}</div>
        <div class="step-svg" v-html="s.svg"></div>
        <div class="step-caption">{{ s.caption }}</div>
      </div>
    </div>
  </figure>
</template>

<style scoped>
.step-strip {
  margin: 24px 0;
  padding: 16px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  overflow: hidden;
}
.step-strip-title {
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 14px;
  padding: 0 4px;
  font-size: 0.95em;
}
.step-strip-track {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}
.step-cell {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.step-index {
  font-size: 0.72em;
  font-weight: 700;
  color: var(--dsa-primary, #2563eb);
  text-transform: uppercase;
  letter-spacing: 0.6px;
}
.step-svg {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
.step-svg :deep(svg) {
  max-width: 100%;
  height: auto;
}
.step-caption {
  font-size: 0.85em;
  line-height: 1.4;
  color: var(--vp-c-text-2);
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 8px;
  margin-top: 4px;
}

/* Horizontally scrollable on very narrow viewports */
@media (max-width: 480px) {
  .step-strip-track {
    grid-template-columns: repeat(4, 220px);
    overflow-x: auto;
    padding-bottom: 6px;
    scroll-snap-type: x mandatory;
  }
  .step-cell {
    scroll-snap-align: start;
  }
}
</style>
