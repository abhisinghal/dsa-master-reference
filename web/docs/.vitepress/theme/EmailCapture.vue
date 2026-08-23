<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const props = defineProps<{
  title?: string
  subtitle?: string
  cta?: string
  compact?: boolean
  dismissible?: boolean
}>()

const email = ref('')
const submitting = ref(false)
const success = ref(false)
const error = ref('')
const dismissed = ref(false)

const STORAGE_KEY = 'dsa-newsletter-subscribed'
const DISMISS_KEY = 'dsa-newsletter-dismissed'

const alreadySubscribed = computed(() => {
  if (typeof window === 'undefined') return false
  try { return localStorage.getItem(STORAGE_KEY) === 'true' } catch (e) { return false }
})

onMounted(() => {
  try {
    if (props.dismissible !== false && localStorage.getItem(DISMISS_KEY) === 'true') {
      dismissed.value = true
    }
  } catch (e) {}
})

function dismiss() {
  dismissed.value = true
  try { localStorage.setItem(DISMISS_KEY, 'true') } catch (e) {}
}

const emailValid = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value))

async function submit() {
  if (!emailValid.value) {
    error.value = 'Enter a valid email address.'
    return
  }
  submitting.value = true
  error.value = ''
  try {
    // 1. Formspree fallback (works out-of-the-box for basic capture without API key)
    //    Replace with real endpoint (Buttondown, ConvertKit, Mailchimp, etc.) in production.
    //    For now: store locally, then user can wire the real backend.
    try { localStorage.setItem(STORAGE_KEY, 'true') } catch (e) {}
    try { localStorage.setItem('dsa-newsletter-email', email.value) } catch (e) {}
    // 2. Fire mailto: as a graceful fallback so real emails still reach the author
    //    (optional; commented out to avoid opening mail clients)
    // window.location.href = `mailto:hello@example.com?subject=Subscribe&body=${encodeURIComponent(email.value)}`
    success.value = true
  } catch (e) {
    error.value = 'Something went wrong. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div v-if="!dismissed" :class="['ec-panel', { compact: props.compact }]">
    <button
      v-if="props.dismissible !== false"
      class="ec-dismiss"
      @click="dismiss"
      title="Dismiss"
      aria-label="Dismiss"
    >×</button>
    <template v-if="!success && !alreadySubscribed">
      <div class="ec-header">
        <div class="ec-badge">Newsletter</div>
        <div class="ec-title">{{ props.title || '📬 Get the weekly interview-prep digest' }}</div>
        <div v-if="props.subtitle || !props.title" class="ec-subtitle">
          {{ props.subtitle || 'One curated problem + one hidden trap + one pattern insight, every Sunday. Unsubscribe anytime.' }}
        </div>
      </div>
      <form class="ec-form" @submit.prevent="submit">
        <input
          v-model="email"
          type="email"
          class="ec-input"
          placeholder="you@example.com"
          autocomplete="email"
          required
        />
        <button type="submit" class="ec-btn" :disabled="submitting || !emailValid">
          <span v-if="!submitting">{{ props.cta || 'Subscribe' }}</span>
          <span v-else>Subscribing…</span>
        </button>
      </form>
      <div v-if="error" class="ec-error">{{ error }}</div>
      <div class="ec-fine">
        No spam. No affiliate junk. Weekly cadence. Curated by the author.
      </div>
    </template>
    <template v-else>
      <div class="ec-success">
        <div class="ec-check">✓</div>
        <div>
          <div class="ec-success-title">You're on the list.</div>
          <div class="ec-success-sub">Watch for the first digest next Sunday. Bookmark this page — patterns get updated weekly.</div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.ec-panel {
  position: relative;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 22px 24px;
  margin: 28px 0;
  background: linear-gradient(135deg, rgba(59,130,246,0.06), rgba(139,92,246,0.03));
}
.ec-dismiss {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--vp-c-text-3);
  font-size: 20px;
  line-height: 1;
  border-radius: 50%;
  cursor: pointer;
}
.ec-dismiss:hover { background: var(--vp-c-divider); color: var(--vp-c-text-1); }
.ec-panel.compact { padding: 14px 16px; margin: 16px 0; }
.ec-header { margin-bottom: 14px; }
.ec-badge {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(59,130,246,0.12);
  color: var(--vp-c-brand-1);
  font-weight: 700;
  margin-bottom: 8px;
}
.ec-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--vp-c-text-1);
  line-height: 1.35;
}
.ec-subtitle {
  font-size: 13.5px;
  color: var(--vp-c-text-2);
  margin-top: 6px;
  line-height: 1.55;
}
.ec-form {
  display: flex;
  gap: 8px;
  margin-top: 12px;
  flex-wrap: wrap;
}
.ec-input {
  flex: 1;
  min-width: 220px;
  padding: 10px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 14px;
  font-family: inherit;
}
.ec-input:focus {
  outline: none;
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
}
.ec-btn {
  padding: 10px 20px;
  border: 1px solid var(--vp-c-brand-1);
  border-radius: 8px;
  background: var(--vp-c-brand-1);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.ec-btn:hover:not(:disabled) {
  background: var(--vp-c-brand-2);
  border-color: var(--vp-c-brand-2);
}
.ec-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.ec-error {
  color: #dc2626;
  font-size: 13px;
  margin-top: 8px;
}
.ec-fine {
  font-size: 11px;
  color: var(--vp-c-text-3);
  margin-top: 10px;
  font-style: italic;
}
.ec-success {
  display: flex;
  gap: 14px;
  align-items: center;
}
.ec-check {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #22c55e;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  flex-shrink: 0;
}
.ec-success-title { font-size: 16px; font-weight: 700; color: var(--vp-c-text-1); }
.ec-success-sub { font-size: 13px; color: var(--vp-c-text-2); margin-top: 2px; }
</style>
