<script setup lang="ts">
import DsStateMachine from './DsStateMachine.vue'

const cards = [
  {
    id: 'find-pc',
    title: 'find · path compression',
    subtitle: 'flatten during lookup',
    frames: [
      { desc: 'parent[]: idx→parent. Chain 0→1→2→3 (root 3).', cells: [{ value: 1, label: '0' }, { value: 2, label: '1' }, { value: 3, label: '2' }, { value: 3, label: '3' }] },
      { desc: 'find(0). Walk to root.', cells: [{ value: 1, label: '0', highlight: 'compare' }, { value: 2, label: '1' }, { value: 3, label: '2' }, { value: 3, label: '3' }] },
      { desc: '→ parent[0]=1 → visit 1.', cells: [{ value: 1, label: '0' }, { value: 2, label: '1', highlight: 'compare' }, { value: 3, label: '2' }, { value: 3, label: '3' }] },
      { desc: '→ parent[1]=2 → visit 2.', cells: [{ value: 1, label: '0' }, { value: 2, label: '1' }, { value: 3, label: '2', highlight: 'compare' }, { value: 3, label: '3' }] },
      { desc: 'Reached root 3. Compress: parent[0]=parent[1]=parent[2]=3.', cells: [{ value: 3, label: '0', highlight: 'swap' }, { value: 3, label: '1', highlight: 'swap' }, { value: 3, label: '2', highlight: 'swap' }, { value: 3, label: '3', highlight: 'done' }], note: 'Amortized O(α(n)) per find — effectively constant. Without compression it can degrade to O(n).' }
    ]
  },
  {
    id: 'union-by-rank',
    title: 'union · by rank',
    subtitle: 'smaller tree under larger',
    frames: [
      { desc: 'Two roots: A (rank 2), B (rank 1).', cells: [{ value: 'A', label: 'r=2' }, { value: 'B', label: 'r=1' }] },
      { desc: 'union(A, B). Compare ranks.', cells: [{ value: 'A', label: 'r=2', highlight: 'compare' }, { value: 'B', label: 'r=1', highlight: 'compare' }] },
      { desc: 'rank(A) > rank(B) → attach B under A.', cells: [{ value: 'A', label: 'r=2', highlight: 'primary' }, { value: 'B', label: 'child', highlight: 'swap' }] },
      { desc: 'Rank of A unchanged (only bumps when equal ranks merged).', cells: [{ value: 'A', label: 'r=2', highlight: 'done' }, { value: 'B', label: 'child' }], note: 'Combining path compression + union-by-rank gives O(m·α(n)) for m operations — the classic Tarjan bound.' }
    ]
  },
  {
    id: 'components-scan',
    title: 'components · scan roots',
    subtitle: 'after unions, count distinct roots',
    frames: [
      { desc: 'After unions. parent[]: {0→2, 1→2, 2→2, 3→4, 4→4}.', cells: [{ value: 2, label: '0' }, { value: 2, label: '1' }, { value: 2, label: '2' }, { value: 4, label: '3' }, { value: 4, label: '4' }] },
      { desc: 'find(0)=2 → root.', cells: [{ value: 2, label: '0', highlight: 'primary' }, { value: 2, label: '1' }, { value: 2, label: '2' }, { value: 4, label: '3' }, { value: 4, label: '4' }] },
      { desc: 'find(3)=4 → new root.', cells: [{ value: 2, label: '0' }, { value: 2, label: '1' }, { value: 2, label: '2' }, { value: 4, label: '3', highlight: 'primary' }, { value: 4, label: '4' }] },
      { desc: 'Distinct roots = {2, 4} → 2 components.', cells: [{ value: 2, label: '0' }, { value: 2, label: '1' }, { value: 2, label: '2', highlight: 'done' }, { value: 4, label: '3' }, { value: 4, label: '4', highlight: 'done' }], note: 'Track component count with a size decrement inside union() rather than a post-scan — avoids the extra pass.' }
    ]
  }
]
</script>

<template>
  <DsStateMachine title="Union-Find operations (find with path compression, union by rank)" :cards="cards" />
</template>
