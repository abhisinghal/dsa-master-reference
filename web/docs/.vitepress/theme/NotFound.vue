<script setup>
const suggestions = [
  { icon: '🎯', label: 'Start with patterns', href: '/patterns/' },
  { icon: '🗺️', label: 'Roadmap', href: '/foundations/roadmap' },
  { icon: '📚', label: 'All problems', href: '/problems/' },
  { icon: '🏢', label: 'Company tracks — Meta', href: '/tracks/meta' },
  { icon: '⚠️', label: 'Traps catalog', href: '/appendix/traps-catalog' },
  { icon: '📅', label: 'Interview day kit', href: '/appendix/interview-day-kit' },
]
</script>

<template>
  <div class="nf-wrap">
    <div class="nf-code">404</div>
    <div class="nf-title">This page doesn't exist</div>
    <div class="nf-sub">The URL you tried isn't in the reference. Might be a stale bookmark or a typo. Try one of these instead:</div>
    <ul class="nf-links">
      <li v-for="s in suggestions" :key="s.href">
        <a :href="s.href" class="nf-link">
          <span class="nf-icon">{{ s.icon }}</span>
          <span class="nf-label">{{ s.label }}</span>
        </a>
      </li>
    </ul>
    <div class="nf-tip">💡 Tip: press <kbd>/</kbd> or click the search icon to find any page.</div>
  </div>
</template>

<style scoped>
.nf-wrap {
  max-width: 620px;
  margin: 80px auto;
  padding: 30px;
  text-align: center;
}
.nf-code {
  font-size: 96px;
  font-weight: 900;
  color: var(--vp-c-brand-1);
  line-height: 1;
  letter-spacing: -3px;
  margin-bottom: 10px;
}
.nf-title {
  font-size: 1.7em;
  font-weight: 700;
  margin-bottom: 8px;
}
.nf-sub {
  color: var(--vp-c-text-2);
  margin-bottom: 24px;
  font-size: 0.95em;
}
.nf-links {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
  text-align: left;
}
.nf-links li { margin: 0; }
.nf-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  text-decoration: none;
  color: var(--vp-c-text-1);
  transition: border-color 0.15s, transform 0.1s;
}
.nf-link:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-1px);
}
.nf-icon { font-size: 1.2em; }
.nf-label { font-weight: 500; font-size: 0.92em; }
.nf-tip {
  font-size: 0.88em;
  color: var(--vp-c-text-2);
  padding: 12px 16px;
  border-radius: 8px;
  background: var(--vp-c-brand-soft);
}
.nf-tip kbd {
  background: var(--vp-c-bg);
  padding: 1px 6px;
  border-radius: 3px;
  border: 1px solid var(--vp-c-divider);
  font-family: var(--vp-font-family-mono);
  font-size: 0.9em;
}
</style>
