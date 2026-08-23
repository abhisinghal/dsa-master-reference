<script setup lang="ts">
const props = defineProps<{
  compact?: boolean
}>()
</script>

<template>
  <div :class="['support-panel', { compact }]">
    <div class="support-content">
      <div class="support-icon">☕</div>
      <div class="support-text">
        <div class="support-title">Free forever. Support keeps it that way.</div>
        <div class="support-sub">
          If this reference helped land your offer, buy me a coffee. It funds the next batch of pattern videos.
        </div>
      </div>
    </div>
    <div class="support-actions">
      <a
        href="https://github.com/sponsors/abhisinghal"
        target="_blank"
        rel="noopener"
        class="support-btn primary"
      >
        <span class="btn-icon">💖</span>
        Sponsor on GitHub
      </a>
      <a
        href="https://buymeacoffee.com/abhisinghal"
        target="_blank"
        rel="noopener"
        class="support-btn secondary"
      >
        <span class="btn-icon">☕</span>
        Buy me a coffee
      </a>
    </div>
  </div>
</template>

<style scoped>
.support-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 22px 24px;
  margin: 28px 0;
  background: linear-gradient(135deg, rgba(245,158,11,0.06), rgba(239,68,68,0.03));
  display: flex;
  gap: 20px;
  align-items: center;
  flex-wrap: wrap;
}
.support-panel.compact {
  padding: 14px 18px;
  margin: 14px 0;
}
.support-content {
  display: flex;
  gap: 14px;
  align-items: center;
  flex: 1;
  min-width: 260px;
}
.support-icon { font-size: 34px; }
.support-title { font-size: 15px; font-weight: 700; color: var(--vp-c-text-1); }
.support-sub { font-size: 12.5px; color: var(--vp-c-text-2); margin-top: 3px; line-height: 1.45; }
.support-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.support-btn {
  padding: 8px 16px;
  border: 1px solid;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s;
  display: inline-flex;
  gap: 6px;
  align-items: center;
}
.support-btn.primary {
  background: #ec4899;
  color: white;
  border-color: #ec4899;
}
.support-btn.primary:hover { background: #db2777; border-color: #db2777; }
.support-btn.secondary {
  background: #f59e0b;
  color: white;
  border-color: #f59e0b;
}
.support-btn.secondary:hover { background: #d97706; border-color: #d97706; }
.btn-icon { font-size: 15px; }
</style>
