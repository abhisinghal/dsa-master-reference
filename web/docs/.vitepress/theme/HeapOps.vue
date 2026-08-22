<script setup lang="ts">
import DsStateMachine from './DsStateMachine.vue'

const cards = [
  {
    id: 'sift-up',
    title: 'insert · sift-up',
    subtitle: 'min-heap insert',
    frames: [
      { desc: 'Heap [2, 4, 7, 5, 6, 9, 11] (array form).', cells: [{ value: 2 }, { value: 4 }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }, { value: 11 }] },
      { desc: 'insert(1): append at index 7.', cells: [{ value: 2 }, { value: 4 }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }, { value: 11 }, { value: 1, highlight: 'primary' }] },
      { desc: '1 < parent(4) → swap.', cells: [{ value: 2 }, { value: 4, highlight: 'compare' }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }, { value: 11 }, { value: 1, highlight: 'compare' }] },
      { desc: 'After swap.', cells: [{ value: 2 }, { value: 1, highlight: 'swap' }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }, { value: 11 }, { value: 4 }] },
      { desc: '1 < parent(2) → swap.', cells: [{ value: 2, highlight: 'compare' }, { value: 1, highlight: 'compare' }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }, { value: 11 }, { value: 4 }] },
      { desc: 'Root updated → heap valid.', cells: [{ value: 1, highlight: 'done' }, { value: 2 }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }, { value: 11 }, { value: 4 }], note: 'O(log n) — each swap halves distance to root. parent(i) = (i-1)/2.' }
    ]
  },
  {
    id: 'sift-down',
    title: 'extract-min · sift-down',
    subtitle: 'remove root, restore heap',
    frames: [
      { desc: 'Heap [1, 2, 7, 5, 6, 9, 11].', cells: [{ value: 1 }, { value: 2 }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }, { value: 11 }] },
      { desc: 'extractMin → save 1; move last (11) to root.', cells: [{ value: 11, highlight: 'primary' }, { value: 2 }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }] },
      { desc: 'Compare with children (2, 7); min is 2.', cells: [{ value: 11, highlight: 'compare' }, { value: 2, highlight: 'compare' }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }] },
      { desc: '11 > 2 → swap.', cells: [{ value: 2, highlight: 'swap' }, { value: 11, highlight: 'swap' }, { value: 7 }, { value: 5 }, { value: 6 }, { value: 9 }] },
      { desc: 'Compare 11 with children (5, 6); min is 5.', cells: [{ value: 2 }, { value: 11, highlight: 'compare' }, { value: 7 }, { value: 5, highlight: 'compare' }, { value: 6 }, { value: 9 }] },
      { desc: '11 > 5 → swap.', cells: [{ value: 2 }, { value: 5, highlight: 'swap' }, { value: 7 }, { value: 11, highlight: 'swap' }, { value: 6 }, { value: 9 }] },
      { desc: '11 has no children (leaf); done.', cells: [{ value: 2 }, { value: 5 }, { value: 7 }, { value: 11, highlight: 'done' }, { value: 6 }, { value: 9 }], note: 'O(log n). Always sift with the SMALLER child (min-heap) or LARGER (max-heap).' }
    ]
  },
  {
    id: 'heapify',
    title: 'heapify · bulk build',
    subtitle: 'array → heap in O(n)',
    frames: [
      { desc: 'Random array [9, 4, 7, 1, 5, 3].', cells: [{ value: 9 }, { value: 4 }, { value: 7 }, { value: 1 }, { value: 5 }, { value: 3 }] },
      { desc: 'Start at last non-leaf: index (n/2 - 1) = 2.', cells: [{ value: 9 }, { value: 4 }, { value: 7, highlight: 'primary' }, { value: 1 }, { value: 5 }, { value: 3 }] },
      { desc: 'sift-down 7 with child 3 → swap.', cells: [{ value: 9 }, { value: 4 }, { value: 3, highlight: 'swap' }, { value: 1 }, { value: 5 }, { value: 7 }] },
      { desc: 'i=1: sift-down 4 with min child 1 → swap.', cells: [{ value: 9 }, { value: 1, highlight: 'swap' }, { value: 3 }, { value: 4, highlight: 'swap' }, { value: 5 }, { value: 7 }] },
      { desc: 'i=0: sift-down 9 with min child 1 → swap.', cells: [{ value: 1, highlight: 'swap' }, { value: 9, highlight: 'swap' }, { value: 3 }, { value: 4 }, { value: 5 }, { value: 7 }] },
      { desc: 'sift 9 with min child 4 → swap.', cells: [{ value: 1 }, { value: 4, highlight: 'swap' }, { value: 3 }, { value: 9, highlight: 'swap' }, { value: 5 }, { value: 7 }] },
      { desc: 'Heap valid.', cells: [{ value: 1, highlight: 'done' }, { value: 4 }, { value: 3 }, { value: 9 }, { value: 5 }, { value: 7 }], note: 'Bulk heapify is O(n), not O(n log n) — deeper nodes get shorter sifts. Never insert one-by-one into an empty heap.' }
    ]
  }
]
</script>

<template>
  <DsStateMachine title="Heap operations (sift-up, sift-down, heapify)" :cards="cards" />
</template>
