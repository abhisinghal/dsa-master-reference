<script setup lang="ts">
import DsStateMachine from './DsStateMachine.vue'

const cards = [
  {
    id: 'stack-push',
    title: 'Stack · push',
    subtitle: 'add to top',
    frames: [
      { desc: 'Empty stack.', cells: [], headLabel: 'top' },
      { desc: 'push(3) — grow top.', cells: [{ value: 3, highlight: 'primary' }], headLabel: 'top' },
      { desc: 'push(7) — grow top.', cells: [{ value: 3 }, { value: 7, highlight: 'primary' }], headLabel: 'top' },
      { desc: 'push(1) — grow top.', cells: [{ value: 3 }, { value: 7 }, { value: 1, highlight: 'primary' }], headLabel: 'top', note: 'Amortized O(1) — ArrayDeque doubles capacity when full.' }
    ]
  },
  {
    id: 'stack-pop',
    title: 'Stack · pop',
    subtitle: 'remove from top',
    frames: [
      { desc: 'Stack [3, 7, 1].', cells: [{ value: 3 }, { value: 7 }, { value: 1 }], headLabel: 'top' },
      { desc: 'pop() → 1.', cells: [{ value: 3 }, { value: 7 }, { value: 1, highlight: 'swap' }], headLabel: 'top' },
      { desc: 'Stack now [3, 7].', cells: [{ value: 3 }, { value: 7, highlight: 'done' }], headLabel: 'top', note: 'peek() would return 7 without popping. Always check isEmpty() first.' }
    ]
  },
  {
    id: 'queue-enqueue',
    title: 'Queue · enqueue',
    subtitle: 'add at back',
    frames: [
      { desc: 'Empty queue.', cells: [], headLabel: 'front', tailLabel: 'back' },
      { desc: 'enqueue(A) at back.', cells: [{ value: 'A', highlight: 'primary' }], headLabel: 'front', tailLabel: 'back' },
      { desc: 'enqueue(B) at back.', cells: [{ value: 'A' }, { value: 'B', highlight: 'primary' }], headLabel: 'front', tailLabel: 'back' },
      { desc: 'enqueue(C) at back.', cells: [{ value: 'A' }, { value: 'B' }, { value: 'C', highlight: 'primary' }], headLabel: 'front', tailLabel: 'back', note: 'ArrayDeque backing — offer() is O(1) amortized. Do NOT use LinkedList (cache-hostile).' }
    ]
  },
  {
    id: 'queue-dequeue',
    title: 'Queue · dequeue',
    subtitle: 'remove from front',
    frames: [
      { desc: 'Queue [A, B, C].', cells: [{ value: 'A' }, { value: 'B' }, { value: 'C' }], headLabel: 'front', tailLabel: 'back' },
      { desc: 'poll() → A.', cells: [{ value: 'A', highlight: 'swap' }, { value: 'B' }, { value: 'C' }], headLabel: 'front', tailLabel: 'back' },
      { desc: 'Queue now [B, C].', cells: [{ value: 'B', highlight: 'done' }, { value: 'C' }], headLabel: 'front', tailLabel: 'back', note: 'FIFO — first in, first out. peek() returns front without removing.' }
    ]
  },
  {
    id: 'deque-push-front',
    title: 'Deque · pushFront / pushBack',
    subtitle: 'double-ended access',
    frames: [
      { desc: 'Deque [B, C].', cells: [{ value: 'B' }, { value: 'C' }], headLabel: 'front', tailLabel: 'back' },
      { desc: 'offerFirst(A) → grows at front.', cells: [{ value: 'A', highlight: 'primary' }, { value: 'B' }, { value: 'C' }], headLabel: 'front', tailLabel: 'back' },
      { desc: 'offerLast(D) → grows at back.', cells: [{ value: 'A' }, { value: 'B' }, { value: 'C' }, { value: 'D', highlight: 'primary' }], headLabel: 'front', tailLabel: 'back', note: 'Deque = stack + queue. Both ends O(1). Backing for monotonic-deque and sliding-window-max.' }
    ]
  },
  {
    id: 'monostack',
    title: 'Monotonic Stack · push-with-pop',
    subtitle: 'maintain decreasing order',
    frames: [
      { desc: 'Stack [4, 3] (values, decreasing).', cells: [{ value: 4 }, { value: 3 }], headLabel: 'bottom', tailLabel: 'top' },
      { desc: 'push(5): 5 > top (3) → pop 3.', cells: [{ value: 4 }, { value: 3, highlight: 'swap' }], headLabel: 'bottom', tailLabel: 'top' },
      { desc: '5 > top (4) → pop 4.', cells: [{ value: 4, highlight: 'swap' }], headLabel: 'bottom', tailLabel: 'top' },
      { desc: 'Stack empty → push 5.', cells: [{ value: 5, highlight: 'done' }], headLabel: 'bottom', tailLabel: 'top', note: 'Each element pushed and popped at most once → amortized O(1) per operation.' }
    ]
  }
]
</script>

<template>
  <DsStateMachine title="Stack, Queue &amp; Deque operations" :cards="cards" />
</template>
