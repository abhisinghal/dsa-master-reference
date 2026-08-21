<script setup lang="ts">
import { useRoute } from 'vitepress'
import { computed } from 'vue'

const route = useRoute()

const LABELS: Record<string, string> = {
  'patterns': 'Patterns',
  'data-structures': 'Data Structures',
  'foundations': 'Foundations',
  'appendix': 'Appendix',
  'sliding-window': 'Sliding Window',
  'two-pointers': 'Two Pointers',
  'fast-slow': 'Fast/Slow Pointers',
  'prefix-sum': 'Prefix Sum',
  'hashing': 'Hashing',
  'monotonic-stack': 'Monotonic Stack',
  'binary-search': 'Binary Search',
  'bs-on-answer': 'Binary Search on Answer',
  'top-k-heap': 'Top-K / Heap',
  'k-way-merge': 'K-way Merge',
  'merge-intervals': 'Merge Intervals',
  'sweep-line': 'Sweep Line',
  'topological-sort': 'Topological Sort',
  'union-find': 'Union-Find',
  'greedy': 'Greedy',
  'backtracking': 'Backtracking',
  'divide-conquer': 'Divide & Conquer',
  'dp': 'Dynamic Programming',
  'trie-pattern': 'Trie Pattern',
  'bit-manip': 'Bit Manipulation',
  'quickselect': 'Quickselect',
  'math': 'Math',
  'design': 'Design',
  'arrays': 'Arrays',
  'strings': 'Strings',
  'linked-lists': 'Linked Lists',
  'stacks-queues': 'Stacks & Queues',
  'trees': 'Trees',
  'heaps': 'Heaps',
  'trie': 'Trie',
  'graphs': 'Graphs',
  'segment-fenwick': 'Segment / Fenwick Tree',
  'roadmap': 'Roadmap',
  'playbook': 'Playbook',
  'glossary': 'Glossary',
  'how-to-use': 'How to Use',
  'java-primer': 'Java Primer',
  'java-gotchas': 'Java Gotchas',
  'complexity': 'Complexity',
  'debugging': 'Debugging',
  'cheatsheets': 'Cheat Sheets',
  'self-check': 'Self-Check',
  'problem-index': 'Problem Index',
  'practice-solutions': 'Practice Solutions',
  'mock-transcripts': 'Mock Transcripts',
  'traps-catalog': 'Traps Catalog'
}

function titleize(s: string): string {
  if (LABELS[s]) return LABELS[s]
  return s.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
}

const crumbs = computed(() => {
  const p = route.path.replace(/^\/dsa-master-reference/, '').replace(/\.html$/, '').replace(/\/$/, '')
  if (!p || p === '/') return []
  const parts = p.split('/').filter(Boolean)
  const items: Array<{ text: string; href: string | null }> = [{ text: 'Home', href: '/' }]
  let current = ''
  for (let i = 0; i < parts.length; i++) {
    current += '/' + parts[i]
    const isLast = i === parts.length - 1
    items.push({
      text: titleize(parts[i]),
      href: isLast ? null : current
    })
  }
  return items
})
</script>

<template>
  <nav v-if="crumbs.length > 1" class="breadcrumbs" aria-label="Breadcrumb">
    <ol>
      <li v-for="(c, i) in crumbs" :key="i">
        <a v-if="c.href" :href="`/dsa-master-reference${c.href}`">{{ c.text }}</a>
        <span v-else class="current" aria-current="page">{{ c.text }}</span>
        <span v-if="i < crumbs.length - 1" class="sep">›</span>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.breadcrumbs {
  margin: 12px 0 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--vp-c-divider);
  font-size: 0.85em;
}
.breadcrumbs ol {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0;
}
.breadcrumbs li {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0;
}
.breadcrumbs a {
  color: var(--vp-c-text-2);
  text-decoration: none;
  transition: color 0.15s ease;
}
.breadcrumbs a:hover {
  color: var(--vp-c-brand-1);
}
.breadcrumbs .current {
  color: var(--vp-c-text-1);
  font-weight: 500;
}
.breadcrumbs .sep {
  color: var(--vp-c-text-3);
  padding: 0 6px;
}
</style>

