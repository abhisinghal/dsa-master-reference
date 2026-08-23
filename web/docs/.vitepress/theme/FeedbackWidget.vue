<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  problemSlug: string
}>()

const feedback = ref<'helpful' | 'not-helpful' | null>(null)
const submitted = ref(false)
const showTextarea = ref(false)
const detail = ref('')
const success = ref(false)

const STORAGE_KEY = `dsa-feedback:${props.problemSlug}`

function loadPrev() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      feedback.value = parsed.rating
      submitted.value = true
    }
  } catch (e) {}
}
loadPrev()

function rate(v: 'helpful' | 'not-helpful') {
  feedback.value = v
  if (v === 'not-helpful') {
    showTextarea.value = true
  } else {
    submit()
  }
}

function submit() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      rating: feedback.value,
      detail: detail.value,
      ts: Date.now(),
    }))
  } catch (e) {}
  submitted.value = true
  success.value = true
  setTimeout(() => { success.value = false }, 2500)
}
</script>

<template>
  <div class="fb-panel">
    <div v-if="!submitted" class="fb-prompt">
      <div class="fb-text">Was this page helpful?</div>
      <div class="fb-buttons">
        <button class="fb-btn" @click="rate('helpful')" title="Yes">👍 Yes</button>
        <button class="fb-btn" @click="rate('not-helpful')" title="Could be better">👎 Could be better</button>
      </div>
    </div>
    <div v-else-if="showTextarea && !success" class="fb-detail">
      <label class="fb-label">What could we improve?</label>
      <textarea
        v-model="detail"
        class="fb-textarea"
        rows="3"
        placeholder="Missing content, incorrect code, unclear explanation, …"
      ></textarea>
      <div class="fb-actions">
        <button class="fb-submit" @click="submit">Send feedback</button>
        <button class="fb-skip" @click="submit">Skip</button>
      </div>
    </div>
    <div v-else class="fb-thanks">
      <span class="fb-check">✓</span> Thanks — noted locally. Weekly review incorporates all feedback.
    </div>
  </div>
</template>

<style scoped>
.fb-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 12px 18px;
  margin: 24px 0;
  background: var(--vp-c-bg-soft);
}
.fb-prompt {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}
.fb-text { font-size: 13.5px; color: var(--vp-c-text-1); font-weight: 500; }
.fb-buttons { display: flex; gap: 8px; }
.fb-btn {
  padding: 6px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 12.5px;
  cursor: pointer;
  transition: all 0.15s;
}
.fb-btn:hover { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); }
.fb-detail { display: flex; flex-direction: column; gap: 8px; }
.fb-label { font-size: 12px; color: var(--vp-c-text-2); font-weight: 500; }
.fb-textarea {
  padding: 8px 10px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
  font-family: inherit;
  resize: vertical;
  min-height: 60px;
}
.fb-textarea:focus { outline: none; border-color: var(--vp-c-brand-1); }
.fb-actions { display: flex; gap: 6px; }
.fb-submit {
  padding: 6px 14px;
  border: 1px solid var(--vp-c-brand-1);
  border-radius: 6px;
  background: var(--vp-c-brand-1);
  color: white;
  font-size: 12.5px;
  cursor: pointer;
}
.fb-skip {
  padding: 6px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: transparent;
  color: var(--vp-c-text-2);
  font-size: 12.5px;
  cursor: pointer;
}
.fb-thanks {
  font-size: 13px;
  color: var(--vp-c-text-2);
  display: flex;
  align-items: center;
  gap: 8px;
}
.fb-check {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #22c55e;
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
}
</style>
