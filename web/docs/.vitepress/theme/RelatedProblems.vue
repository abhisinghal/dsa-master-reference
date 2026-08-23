<script setup>
const props = defineProps({
  problems: { type: String, required: true }
})
const list = props.problems.split('|').map(entry => {
  const [slug, title] = entry.split('::')
  return { slug, title }
}).filter(p => p.slug && p.title)
const url = (slug) => `/problems/${slug}`
</script>

<template>
  <div v-if="list.length" class="rprob-panel">
    <div class="rprob-title">📚 Related problems</div>
    <ul class="rprob-list">
      <li v-for="p in list" :key="p.slug">
        <a :href="url(p.slug)" class="rprob-link">→ {{ p.title }}</a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.rprob-panel {
  margin: 1.5rem 0;
  padding: 12px 16px;
  border-left: 3px solid #8b5cf6;
  background: rgba(139, 92, 246, 0.06);
  border-radius: 6px;
}
.rprob-title {
  font-size: 0.85em;
  font-weight: 700;
  color: #7c3aed;
  letter-spacing: 0.02em;
  margin-bottom: 6px;
}
.rprob-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.rprob-list li { margin: 3px 0; }
.rprob-link {
  color: var(--vp-c-text-1);
  text-decoration: none;
  font-size: 0.9em;
}
.rprob-link:hover {
  color: #7c3aed;
  text-decoration: underline;
}
</style>
