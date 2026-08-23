<script setup>
import { computed } from 'vue'

const props = defineProps({
  patternId: { type: String, required: true }
})

const RELATED = {
  'sliding-window':   [['two-pointers','Two Pointers','Same shrink/expand mechanics'], ['hashing','Hashing','Common frequency-map inner tool'], ['prefix-sum','Prefix Sum','Alternative for static range queries']],
  'two-pointers':     [['sliding-window','Sliding Window','Both move indices with an invariant'], ['sort','Sorting','Enables the classic sorted two-pointer setup'], ['fast-slow','Fast/Slow','Two-pointer variant on linked structures']],
  'fast-slow':        [['two-pointers','Two Pointers','Same family, different step size'], ['linked-lists','Linked Lists','Primary data structure'], ['cycle-detection','Cycle Detection','Floyd is the canonical algorithm']],
  'prefix-sum':       [['sliding-window','Sliding Window','Both do range-sum queries'], ['hashing','Hashing','Prefix + hash unlocks subarray-sum-equals-k'], ['segment-tree','Segment Tree','When queries also need updates']],
  'hashing':          [['sliding-window','Sliding Window','Frequency-map lives in a hash'], ['prefix-sum','Prefix Sum','Sum-to-index maps power subarray tricks'], ['two-sum','Two Sum family','Classic hash-lookup pattern']],
  'binary-search':    [['sorting','Sorting','Requires monotonic input'], ['binary-search-on-answer','Binary Search on Answer','Feasibility-based variant'], ['two-pointers','Two Pointers','Alternate way to narrow a range']],
  'sorting':          [['two-pointers','Two Pointers','Sorted input unlocks the pattern'], ['binary-search','Binary Search','Requires sorted input'], ['quickselect','Quickselect','Partial-sort variant for kth element']],
  'stacks-queues':    [['monotonic-stack','Monotonic Stack','Stack maintaining an invariant'], ['bfs','BFS','Queue-based traversal'], ['dfs','DFS','Stack-based traversal']],
  'monotonic-stack':  [['stacks-queues','Stacks & Queues','Underlying data structure'], ['sliding-window','Sliding Window','Both process elements once left-to-right'], ['next-greater','Next Greater Element family','Canonical use case']],
  'heap':             [['sorting','Sorting','Heap-sort and kth-largest problems'], ['quickselect','Quickselect','Alternative for kth-element'], ['top-k','Top-K family','Canonical use case']],
  'trees':            [['dfs','DFS','Primary traversal on trees'], ['bfs','BFS','Level-order traversal'], ['recursion','Recursion','Trees are naturally recursive']],
  'graphs':           [['bfs','BFS','Shortest path in unweighted graphs'], ['dfs','DFS','Connectivity and cycle detection'], ['union-find','Union Find','Dynamic connectivity']],
  'bfs':              [['dfs','DFS','Complementary graph traversal'], ['graphs','Graphs','Primary use case'], ['topo-sort','Topological Sort','Kahn algorithm uses BFS']],
  'dfs':              [['bfs','BFS','Complementary graph traversal'], ['backtracking','Backtracking','DFS with undo'], ['graphs','Graphs','Primary use case']],
  'topo-sort':        [['graphs','Graphs','DAG-specific graph algorithm'], ['bfs','BFS','Kahn algorithm'], ['dfs','DFS','Post-order variant']],
  'shortest-path':    [['graphs','Graphs','Weighted-graph algorithm family'], ['bfs','BFS','Unweighted shortest path'], ['heap','Heap','Priority queue for Dijkstra']],
  'union-find':       [['graphs','Graphs','Dynamic connectivity queries'], ['mst','MST','Kruskal uses union-find'], ['bfs','BFS','Alternative for static connectivity']],
  'greedy':           [['sorting','Sorting','Greedy often needs sorted input'], ['dp','DP','Both optimize; greedy is a special case'], ['intervals','Intervals','Classic greedy application']],
  'backtracking':     [['dfs','DFS','Backtracking IS DFS with undo'], ['recursion','Recursion','Backtracking is a recursion style'], ['bitmask','Bitmask','State compression for subsets']],
  'divide-conquer':   [['recursion','Recursion','D&C is a recursion pattern'], ['binary-search','Binary Search','Simplest D&C'], ['sorting','Sorting','Merge sort and quicksort']],
  'dp':               [['recursion','Recursion','DP = memoized recursion'], ['greedy','Greedy','Both optimize; DP when greedy fails'], ['bitmask','Bitmask','DP state compression']],
  'knapsack':         [['dp','DP','Parent pattern'], ['greedy','Greedy','Fails for 0/1 knapsack'], ['bitmask','Bitmask','Subset-sum variant']],
  'trie-pattern':     [['strings','Strings','Trie is a prefix structure over strings'], ['hashing','Hashing','Alternative for exact-match lookup'], ['dfs','DFS','Word search on grid uses trie + DFS']],
  'bit-manip':        [['bitmask','Bitmask DP','DP state compression'], ['math','Math','Bitwise arithmetic tricks'], ['hashing','Hashing','XOR replaces hash in some tricks']],
  'quickselect':      [['sorting','Sorting','Partial-sort variant'], ['heap','Heap','Alternative for kth-element'], ['divide-conquer','Divide & Conquer','Partition-based algorithm']],
  'math':             [['bit-manip','Bit Manipulation','Bitwise math tricks'], ['dp','DP','Number-theoretic DP problems'], ['hashing','Hashing','Modular hashing tricks']],
  'design':           [['hashing','Hashing','Fast lookups in designed structures'], ['trees','Trees','LRU + BST hybrid designs'], ['heap','Heap','Priority-queue-based designs']],
  'sweep-line':       [['intervals','Intervals','Same input domain'], ['sorting','Sorting','Sort events first'], ['heap','Heap','Active-event tracking']],
  'intervals':        [['sweep-line','Sweep Line','Same input domain'], ['sorting','Sorting','Sort by start/end'], ['greedy','Greedy','Merge-intervals is greedy']],
}

const items = computed(() => RELATED[props.patternId] || [])
const url = (slug) => `/patterns/${slug}`
</script>

<template>
  <div v-if="items.length" class="rp-panel">
    <div class="rp-title">🔗 Related patterns</div>
    <ul class="rp-list">
      <li v-for="[slug, name, note] in items" :key="slug">
        <a :href="url(slug)" class="rp-link">
          <span class="rp-name">{{ name }}</span>
          <span class="rp-note">{{ note }}</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.rp-panel {
  margin: 1.5rem 0;
  padding: 14px 18px;
  border-left: 3px solid var(--vp-c-brand-1);
  background: var(--vp-c-bg-soft);
  border-radius: 6px;
}
.rp-title {
  font-size: 0.85em;
  font-weight: 700;
  color: var(--vp-c-brand-1);
  letter-spacing: 0.02em;
  margin-bottom: 8px;
}
.rp-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 8px;
}
.rp-list li { margin: 0; }
.rp-link {
  display: flex;
  flex-direction: column;
  padding: 8px 12px;
  border-radius: 5px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  text-decoration: none;
  color: var(--vp-c-text-1);
  transition: border-color 0.15s, transform 0.1s;
}
.rp-link:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-1px);
}
.rp-name {
  font-weight: 600;
  font-size: 0.92em;
  color: var(--vp-c-brand-1);
}
.rp-note {
  font-size: 0.78em;
  color: var(--vp-c-text-2);
  margin-top: 2px;
}
</style>
