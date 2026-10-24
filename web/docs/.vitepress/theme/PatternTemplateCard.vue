<script setup lang="ts">
import { withBase } from 'vitepress'
import InvariantProof from './InvariantProof.vue'
import TemplateReveal from './TemplateReveal.vue'

interface Invariant {
  statement: string
  initialization: string
  maintenance: string
  termination: string
}

interface Complexity {
  time: string
  space: string
}

interface Specialization {
  slug: string
  title: string
  href?: string
}

defineProps<{
  slug: string
  title?: string
  language?: string
  code: string
  invariant: Invariant
  complexity: Complexity
  specializations?: Specialization[]
  problemShape?: string
  defaultRevealed?: boolean
}>()

function specHref(spec: Specialization): string {
  if (spec.href) return withBase(spec.href)
  return `#${spec.slug}`
}
</script>

<template>
  <section class="pattern-template-card">
    <header class="ptc-head">
      <span class="ptc-badge">THE template</span>
      <h3 v-if="title" class="ptc-title">{{ title }}</h3>
    </header>

    <TemplateReveal
      :slug="`template:${slug}`"
      :language="language || 'java'"
      :canonical="code"
      :problem-shape="problemShape"
      :default-revealed="defaultRevealed"
    />

    <InvariantProof
      :statement="invariant.statement"
      :initialization="invariant.initialization"
      :maintenance="invariant.maintenance"
      :termination="invariant.termination"
    />

    <div class="ptc-complexity">
      <div class="ptc-cx-cell">
        <span class="ptc-cx-label">Time</span>
        <span class="ptc-cx-value">{{ complexity.time }}</span>
      </div>
      <div class="ptc-cx-cell">
        <span class="ptc-cx-label">Space</span>
        <span class="ptc-cx-value">{{ complexity.space }}</span>
      </div>
    </div>

    <slot name="amortized" />

    <div v-if="specializations && specializations.length" class="ptc-specializations">
      <div class="ptc-sp-label">Specializations in this chapter</div>
      <div class="ptc-sp-chips">
        <a
          v-for="spec in specializations"
          :key="spec.slug"
          :href="specHref(spec)"
          class="ptc-sp-chip"
        >
          {{ spec.title }}
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.pattern-template-card {
  margin: 28px 0;
  padding: 20px;
  background: var(--vp-c-bg-soft);
  border: 2px solid var(--vp-c-brand-1);
  border-radius: 12px;
}
.ptc-head {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 10px;
}
.ptc-badge {
  font-size: 0.72em;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  text-transform: uppercase;
  letter-spacing: 1.2px;
  background: color-mix(in srgb, var(--vp-c-brand-1) 15%, transparent);
  padding: 4px 10px;
  border-radius: 6px;
  flex-shrink: 0;
}
.ptc-title {
  margin: 0;
  font-size: 1.1em;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
.ptc-complexity {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 14px 0;
}
.ptc-cx-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
}
.ptc-cx-label {
  font-size: 0.7em;
  font-weight: 800;
  color: var(--vp-c-text-2);
  text-transform: uppercase;
  letter-spacing: 0.6px;
}
.ptc-cx-value {
  font-family: var(--vp-font-family-mono);
  font-size: 0.95em;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.ptc-specializations {
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px dashed var(--vp-c-divider);
}
.ptc-sp-label {
  font-size: 0.72em;
  font-weight: 800;
  color: var(--vp-c-text-2);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 8px;
}
.ptc-sp-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.ptc-sp-chip {
  display: inline-block;
  padding: 5px 11px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  font-size: 0.82em;
  color: var(--vp-c-text-1);
  text-decoration: none;
  transition: all 0.15s ease;
}
.ptc-sp-chip:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 8%, var(--vp-c-bg));
}
@media (max-width: 480px) {
  .ptc-complexity {
    grid-template-columns: 1fr;
  }
}
</style>
