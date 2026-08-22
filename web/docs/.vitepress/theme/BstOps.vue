<script setup lang="ts">
import DsStateMachine from './DsStateMachine.vue'

const cards = [
  {
    id: 'bst-search',
    title: 'BST · search',
    subtitle: 'find in-order traversal, but skip left/right',
    frames: [
      { desc: 'BST in-order: [1, 3, 4, 6, 7, 8, 10, 13, 14].', cells: [{ value: 1 }, { value: 3 }, { value: 4 }, { value: 6 }, { value: 7 }, { value: 8 }, { value: 10 }, { value: 13 }, { value: 14 }] },
      { desc: 'search(6). Start at root (8).', cells: [{ value: 1 }, { value: 3 }, { value: 4 }, { value: 6 }, { value: 7 }, { value: 8, highlight: 'compare' }, { value: 10 }, { value: 13 }, { value: 14 }] },
      { desc: '6 < 8 → go LEFT subtree.', cells: [{ value: 1 }, { value: 3 }, { value: 4, highlight: 'primary' }, { value: 6 }, { value: 7 }, { value: 8 }, { value: 10 }, { value: 13 }, { value: 14 }] },
      { desc: 'At 4: 6 > 4 → go RIGHT subtree.', cells: [{ value: 1 }, { value: 3 }, { value: 4, highlight: 'compare' }, { value: 6, highlight: 'primary' }, { value: 7 }, { value: 8 }, { value: 10 }, { value: 13 }, { value: 14 }] },
      { desc: 'Found 6.', cells: [{ value: 1 }, { value: 3 }, { value: 4 }, { value: 6, highlight: 'done' }, { value: 7 }, { value: 8 }, { value: 10 }, { value: 13 }, { value: 14 }], note: 'O(log n) balanced. O(n) worst — a skewed BST is a linked list.' }
    ]
  },
  {
    id: 'bst-insert',
    title: 'BST · insert',
    subtitle: 'walk-to-leaf, attach',
    frames: [
      { desc: 'Existing tree with in-order [3, 8, 10, 14].', cells: [{ value: 3 }, { value: 8 }, { value: 10 }, { value: 14 }] },
      { desc: 'insert(12). Start at root (10).', cells: [{ value: 3 }, { value: 8 }, { value: 10, highlight: 'compare' }, { value: 14 }] },
      { desc: '12 > 10 → RIGHT.', cells: [{ value: 3 }, { value: 8 }, { value: 10 }, { value: 14, highlight: 'compare' }] },
      { desc: '12 < 14 → LEFT (null) → attach as leaf.', cells: [{ value: 3 }, { value: 8 }, { value: 10 }, { value: 12, highlight: 'primary' }, { value: 14 }] },
      { desc: 'New in-order [3, 8, 10, 12, 14].', cells: [{ value: 3 }, { value: 8 }, { value: 10 }, { value: 12, highlight: 'done' }, { value: 14 }], note: 'O(h). Unbalanced trees degrade to O(n) — use TreeMap/TreeSet in Java for guaranteed O(log n).' }
    ]
  },
  {
    id: 'bst-delete',
    title: 'BST · delete',
    subtitle: '3 cases: leaf, one-child, two-children',
    frames: [
      { desc: 'In-order [1, 3, 4, 6, 7, 8, 10, 13, 14]. delete(8) — root, two children.', cells: [{ value: 1 }, { value: 3 }, { value: 4 }, { value: 6 }, { value: 7 }, { value: 8, highlight: 'primary' }, { value: 10 }, { value: 13 }, { value: 14 }] },
      { desc: 'Find in-order successor: leftmost of right subtree = 10.', cells: [{ value: 1 }, { value: 3 }, { value: 4 }, { value: 6 }, { value: 7 }, { value: 8, highlight: 'compare' }, { value: 10, highlight: 'compare' }, { value: 13 }, { value: 14 }] },
      { desc: 'Copy 10 into node holding 8.', cells: [{ value: 1 }, { value: 3 }, { value: 4 }, { value: 6 }, { value: 7 }, { value: 10, highlight: 'swap' }, { value: 10, highlight: 'swap' }, { value: 13 }, { value: 14 }] },
      { desc: 'Delete original 10 (now a leaf-side case).', cells: [{ value: 1 }, { value: 3 }, { value: 4 }, { value: 6 }, { value: 7 }, { value: 10, highlight: 'done' }, { value: 13 }, { value: 14 }], note: 'Cases: (a) leaf → just null; (b) one child → skip node; (c) two children → replace with in-order successor and recurse.' }
    ]
  },
  {
    id: 'level-order',
    title: 'Binary tree · level-order (BFS)',
    subtitle: 'queue-based traversal',
    frames: [
      { desc: 'Tree = 3 / (9, 20) / (·, ·, 15, 7). Queue: [3].', cells: [{ value: 3, highlight: 'primary' }], headLabel: 'queue' },
      { desc: 'Dequeue 3 → emit; enqueue children 9, 20.', cells: [{ value: 9, highlight: 'primary' }, { value: 20, highlight: 'primary' }], headLabel: 'queue', note: 'Emitted so far: [3]' },
      { desc: 'Dequeue 9 → emit; no children.', cells: [{ value: 20 }], headLabel: 'queue', note: 'Emitted so far: [3, 9]' },
      { desc: 'Dequeue 20 → emit; enqueue 15, 7.', cells: [{ value: 15, highlight: 'primary' }, { value: 7, highlight: 'primary' }], headLabel: 'queue', note: 'Emitted so far: [3, 9, 20]' },
      { desc: 'Drain — emit 15, 7.', cells: [], headLabel: 'queue', note: 'Final order: [3, 9, 20, 15, 7]. For "level-by-level", capture queue.size() at the start of each outer loop iteration.' }
    ]
  }
]
</script>

<template>
  <DsStateMachine title="BST &amp; binary tree operations" :cards="cards" />
</template>
