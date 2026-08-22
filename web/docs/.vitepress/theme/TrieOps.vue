<script setup lang="ts">
import DsStateMachine from './DsStateMachine.vue'

const cards = [
  {
    id: 'trie-insert',
    title: 'Trie · insert',
    subtitle: 'walk-or-create per char',
    frames: [
      { desc: 'Empty trie. insert("cat"). Path shown as characters.', cells: [{ value: '·', label: 'root' }] },
      { desc: 'c: no child → create.', cells: [{ value: '·', label: 'root' }, { value: 'c', highlight: 'primary' }] },
      { desc: 'a: no child of c → create.', cells: [{ value: '·', label: 'root' }, { value: 'c' }, { value: 'a', highlight: 'primary' }] },
      { desc: 't: no child of a → create; mark isEnd.', cells: [{ value: '·', label: 'root' }, { value: 'c' }, { value: 'a' }, { value: 't', label: 'end', highlight: 'done' }] },
      { desc: 'insert("car"). c already exists → walk.', cells: [{ value: '·', label: 'root' }, { value: 'c', highlight: 'compare' }, { value: 'a' }, { value: 't', label: 'end' }] },
      { desc: 'a exists → walk.', cells: [{ value: '·', label: 'root' }, { value: 'c' }, { value: 'a', highlight: 'compare' }, { value: 't', label: 'end' }] },
      { desc: 'r: no child → branch off.', cells: [{ value: '·', label: 'root' }, { value: 'c' }, { value: 'a' }, { value: 't', label: 'end' }, { value: 'r', label: 'end', highlight: 'done' }], note: 'O(L) per insert, where L = word length. Sibling branches share the prefix "ca".' }
    ]
  },
  {
    id: 'trie-search',
    title: 'Trie · search',
    subtitle: 'walk char-by-char, check isEnd',
    frames: [
      { desc: 'Trie contains {"cat", "car"}.', cells: [{ value: '·', label: 'root' }, { value: 'c' }, { value: 'a' }, { value: 't', label: 'end' }, { value: 'r', label: 'end' }] },
      { desc: 'search("ca"). Walk c, a.', cells: [{ value: '·', label: 'root' }, { value: 'c', highlight: 'compare' }, { value: 'a', highlight: 'compare' }, { value: 't', label: 'end' }, { value: 'r', label: 'end' }] },
      { desc: 'Reached "a" node. isEnd=false → return false.', cells: [{ value: '·', label: 'root' }, { value: 'c' }, { value: 'a', highlight: 'swap' }, { value: 't', label: 'end' }, { value: 'r', label: 'end' }], note: 'Use startsWith("ca") if you only want prefix existence. contains() checks isEnd at the last node.' }
    ]
  },
  {
    id: 'trie-prefix',
    title: 'Trie · startsWith (prefix)',
    subtitle: 'return true if node exists',
    frames: [
      { desc: 'Trie {"cat", "car"}. startsWith("ca").', cells: [{ value: '·', label: 'root' }, { value: 'c' }, { value: 'a' }, { value: 't', label: 'end' }, { value: 'r', label: 'end' }] },
      { desc: 'Walk c → exists.', cells: [{ value: '·', label: 'root' }, { value: 'c', highlight: 'compare' }, { value: 'a' }, { value: 't', label: 'end' }, { value: 'r', label: 'end' }] },
      { desc: 'Walk a → exists.', cells: [{ value: '·', label: 'root' }, { value: 'c' }, { value: 'a', highlight: 'done' }, { value: 't', label: 'end' }, { value: 'r', label: 'end' }], note: 'Return true. Autocomplete: from this node, DFS/BFS to enumerate all descendants ending words.' }
    ]
  }
]
</script>

<template>
  <DsStateMachine title="Trie operations" :cards="cards" />
</template>
