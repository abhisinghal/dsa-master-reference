<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  title?: string
}>()

const copied = ref(false)
const shared = ref(false)

async function share() {
  const url = typeof window !== 'undefined' ? window.location.href : ''
  const title = props.title || 'DSA Master Reference'
  // Try native Web Share first
  if (typeof navigator !== 'undefined' && (navigator as any).share) {
    try {
      await (navigator as any).share({ title, url })
      shared.value = true
      setTimeout(() => shared.value = false, 2000)
      return
    } catch (e) {
      // User cancelled or error — fall through
    }
  }
  // Fallback: copy to clipboard
  try {
    await navigator.clipboard.writeText(url)
    copied.value = true
    setTimeout(() => copied.value = false, 2000)
  } catch (e) {}
}

function twitterShare() {
  const url = encodeURIComponent(window.location.href)
  const text = encodeURIComponent(`${props.title || 'DSA Master Reference'} — a solid Java DSA interview prep resource`)
  window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank', 'noopener')
}

function linkedInShare() {
  const url = encodeURIComponent(window.location.href)
  window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank', 'noopener')
}
</script>

<template>
  <div class="share-row">
    <span class="share-label">Share</span>
    <button class="share-btn" @click="share" :title="copied ? 'Copied!' : 'Copy link'">
      <span v-if="copied">✓ Copied</span>
      <span v-else-if="shared">✓ Shared</span>
      <span v-else>🔗 Link</span>
    </button>
    <button class="share-btn" @click="twitterShare" title="Share to Twitter/X">𝕏</button>
    <button class="share-btn" @click="linkedInShare" title="Share to LinkedIn">in</button>
  </div>
</template>

<style scoped>
.share-row {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 12px 0;
}
.share-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--vp-c-text-3);
  font-weight: 600;
  margin-right: 4px;
}
.share-btn {
  padding: 5px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  min-width: 32px;
}
.share-btn:hover { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); }
</style>
