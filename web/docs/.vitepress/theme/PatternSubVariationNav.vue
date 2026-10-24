<script setup lang="ts">
import { computed } from 'vue'
import patternsData from './data/patterns.subvariations.json'

interface SubVariation {
  slug: string
  title: string
  difficulty?: string
}

interface PatternMeta {
  slug: string
  title: string
  subVariations?: SubVariation[]
}

const props = defineProps<{
  pattern: string
}>()

const allPatterns = patternsData as unknown as Record<string, PatternMeta>

const meta = computed<PatternMeta | null>(() => allPatterns[props.pattern] ?? null)
const subs = computed<SubVariation[]>(() => meta.value?.subVariations ?? [])

function difficultyClass(d?: string): string {
  if (d === 'easy') return 'nav-diff nav-diff-e'
  if (d === 'medium') return 'nav-diff nav-diff-m'
  if (d === 'hard') return 'nav-diff nav-diff-h'
  return 'nav-diff'
}
function difficultyLabel(d?: string): string {
  if (d === 'easy') return 'E'
  if (d === 'medium') return 'M'
  if (d === 'hard') return 'H'
  return ''
}
</script>

<template>
  <nav v-if="subs.length" class="sub-nav" :aria-label="`Sub-variations of ${meta?.title ?? pattern}`">
    <div class="sub-nav-head">
      <span class="sub-nav-badge">{{ subs.length }} sub-variations</span>
      <span class="sub-nav-title">This chapter covers {{ meta?.title }}'s full range</span>
    </div>
    <ol class="sub-nav-list">
      <li v-for="(sv, i) in subs" :key="sv.slug" class="sub-nav-item">
        <a :href="`#${sv.slug}`" class="sub-nav-link">
          <span class="sub-nav-num">{{ i + 1 }}</span>
          <span class="sub-nav-title-row">{{ sv.title }}</span>
          <span v-if="sv.difficulty" :class="difficultyClass(sv.difficulty)">
            {{ difficultyLabel(sv.difficulty) }}
          </span>
        </a>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.sub-nav {
  margin: 20px 0;
  padding: 14px 16px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-left: 3px solid var(--vp-c-brand-1);
  border-radius: 8px;
}
.sub-nav-head {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 10px;
}
.sub-nav-badge {
  font-size: 0.7em;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  text-transform: uppercase;
  letter-spacing: 1px;
  background: color-mix(in srgb, var(--vp-c-brand-1) 15%, transparent);
  padding: 3px 10px;
  border-radius: 5px;
}
.sub-nav-title {
  font-size: 0.88em;
  color: var(--vp-c-text-2);
}
.sub-nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 4px;
}
@media (min-width: 720px) {
  .sub-nav-list {
    grid-template-columns: 1fr 1fr;
  }
}
.sub-nav-item {
  margin: 0;
}
.sub-nav-link {
  display: grid;
  grid-template-columns: 22px 1fr auto;
  align-items: center;
  gap: 10px;
  padding: 7px 10px;
  border-radius: 6px;
  text-decoration: none;
  color: var(--vp-c-text-1);
  font-size: 0.9em;
}
.sub-nav-link:hover {
  background: var(--vp-c-bg);
  color: var(--vp-c-brand-1);
}
.sub-nav-num {
  font-family: var(--vp-font-family-mono);
  font-size: 0.78em;
  color: var(--vp-c-text-3);
  font-weight: 700;
}
.nav-diff {
  font-size: 0.68em;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 10px;
  letter-spacing: 0.5px;
}
.nav-diff-e {
  background: color-mix(in srgb, #10b981 20%, transparent);
  color: #047857;
}
.nav-diff-m {
  background: color-mix(in srgb, #f59e0b 25%, transparent);
  color: #b45309;
}
.nav-diff-h {
  background: color-mix(in srgb, #ef4444 20%, transparent);
  color: #b91c1c;
}
:root.dark .nav-diff-e { color: #6ee7b7; }
:root.dark .nav-diff-m { color: #fcd34d; }
:root.dark .nav-diff-h { color: #fca5a5; }
</style>
