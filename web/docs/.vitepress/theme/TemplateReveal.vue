<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { storage } from './lib/storage'

const props = defineProps<{
  slug: string
  language?: string
  canonical: string
  problemShape?: string
  defaultRevealed?: boolean
}>()

const storageKey = () => `dsa-template-reveal:${props.slug}`

const attempt = ref('')
const revealed = ref(!!props.defaultRevealed)
const everAttempted = ref(false)

onMounted(() => {
  const data = storage.getJson<{
    attempt?: string
    revealed?: boolean
    everAttempted?: boolean
  }>(storageKey(), {})
  if (typeof data.attempt === 'string') attempt.value = data.attempt
  if (data.revealed) revealed.value = true
  if (data.everAttempted) everAttempted.value = true
})

function persist() {
  storage.setJson(storageKey(), {
    attempt: attempt.value,
    revealed: revealed.value,
    everAttempted: everAttempted.value,
  })
}

function onAttemptInput() {
  if (!everAttempted.value && attempt.value.trim().length >= 10) {
    everAttempted.value = true
  }
  persist()
}

function reveal() {
  revealed.value = true
  persist()
}

function hide() {
  revealed.value = false
  persist()
}

function reset() {
  attempt.value = ''
  revealed.value = false
  everAttempted.value = false
  storage.remove(storageKey())
}

const canonicalLines = computed(() => props.canonical.replace(/\n$/, '').split('\n'))
const attemptLines = computed(() => attempt.value.replace(/\n$/, '').split('\n'))

type DiffRow = {
  canonical: string
  attempt: string
  same: boolean
  canonicalIsBlank: boolean
  attemptIsBlank: boolean
}

const diffRows = computed<DiffRow[]>(() => {
  const a = attemptLines.value
  const c = canonicalLines.value
  const n = Math.max(a.length, c.length)
  const rows: DiffRow[] = []
  for (let i = 0; i < n; i++) {
    const aa = a[i] ?? ''
    const cc = c[i] ?? ''
    rows.push({
      canonical: cc,
      attempt: aa,
      same: aa.replace(/\s+$/, '') === cc.replace(/\s+$/, ''),
      canonicalIsBlank: i >= c.length,
      attemptIsBlank: i >= a.length,
    })
  }
  return rows
})

const matchCount = computed(() => diffRows.value.filter(r => r.same).length)
const showDiff = computed(() => revealed.value && attempt.value.trim().length > 0)
</script>

<template>
  <div class="template-reveal" :class="{ 'is-revealed': revealed }">
    <div class="tr-head">
      <span class="tr-badge">Blind-solve</span>
      <span v-if="problemShape" class="tr-problem">{{ problemShape }}</span>
      <span class="tr-spacer"></span>
      <span v-if="everAttempted && !revealed" class="tr-status">Attempt saved</span>
      <span v-if="revealed && everAttempted" class="tr-status tr-status-match">
        {{ matchCount }} / {{ diffRows.length }} lines match
      </span>
    </div>

    <div v-if="!revealed" class="tr-attempt">
      <label :for="`tr-${slug}`" class="tr-label">
        Type the template from memory. (Encouraged, not required — click reveal when ready.)
      </label>
      <textarea
        :id="`tr-${slug}`"
        v-model="attempt"
        class="tr-textarea"
        :placeholder="`// your attempt in ${language || 'Java'}…`"
        spellcheck="false"
        rows="8"
        @input="onAttemptInput"
      ></textarea>
      <div class="tr-actions">
        <button class="tr-btn tr-btn-primary" type="button" @click="reveal">
          Reveal canonical template
        </button>
        <button v-if="attempt.length > 0" class="tr-btn" type="button" @click="reset">
          Clear
        </button>
      </div>
    </div>

    <div v-if="revealed" class="tr-revealed">
      <div class="tr-canonical">
        <div class="tr-canon-head">
          <span class="tr-canon-label">Canonical template</span>
          <button class="tr-btn tr-btn-ghost" type="button" @click="hide">Hide</button>
        </div>
        <pre class="tr-canon-pre"><code>{{ canonical }}</code></pre>
      </div>

      <div v-if="showDiff" class="tr-diff">
        <div class="tr-diff-head">
          <span class="tr-diff-label">Your attempt vs canonical, line-by-line</span>
        </div>
        <div class="tr-diff-rows">
          <div
            v-for="(row, i) in diffRows"
            :key="i"
            class="tr-diff-row"
            :class="{
              'tr-row-same': row.same,
              'tr-row-diff': !row.same,
              'tr-row-missing': row.attemptIsBlank,
              'tr-row-extra': row.canonicalIsBlank,
            }"
          >
            <span class="tr-ln">{{ i + 1 }}</span>
            <span class="tr-side tr-attempt-side"><code>{{ row.attempt || '·' }}</code></span>
            <span class="tr-sep">│</span>
            <span class="tr-side tr-canon-side"><code>{{ row.canonical || '·' }}</code></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.template-reveal {
  margin: 20px 0;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  overflow: hidden;
}
.tr-head {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: var(--vp-c-bg);
  border-bottom: 1px solid var(--vp-c-divider);
  font-size: 0.85em;
}
.tr-badge {
  font-size: 0.7em;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  text-transform: uppercase;
  letter-spacing: 1px;
  background: color-mix(in srgb, var(--vp-c-brand-1) 15%, transparent);
  padding: 3px 8px;
  border-radius: 5px;
}
.tr-problem {
  color: var(--vp-c-text-2);
  font-style: italic;
}
.tr-spacer { flex: 1; }
.tr-status {
  font-size: 0.78em;
  color: var(--vp-c-text-2);
  font-weight: 600;
}
.tr-status-match {
  color: var(--vp-c-brand-1);
}
.tr-attempt {
  padding: 14px;
}
.tr-label {
  display: block;
  font-size: 0.85em;
  color: var(--vp-c-text-2);
  margin-bottom: 8px;
}
.tr-textarea {
  width: 100%;
  font-family: var(--vp-font-family-mono);
  font-size: 0.85em;
  line-height: 1.5;
  padding: 10px 12px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  color: var(--vp-c-text-1);
  box-sizing: border-box;
  resize: vertical;
  min-height: 120px;
}
.tr-textarea:focus {
  outline: none;
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--vp-c-brand-1) 25%, transparent);
}
.tr-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}
.tr-btn {
  padding: 7px 14px;
  border-radius: 6px;
  font-size: 0.85em;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  transition: all 0.15s ease;
}
.tr-btn:hover {
  border-color: var(--vp-c-brand-1);
}
.tr-btn-primary {
  background: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  color: #fff;
}
.tr-btn-primary:hover {
  background: var(--vp-c-brand-2);
  border-color: var(--vp-c-brand-2);
}
.tr-btn-ghost {
  background: transparent;
  color: var(--vp-c-text-2);
  padding: 4px 10px;
  font-size: 0.78em;
}
.tr-revealed {
  padding: 0;
}
.tr-canonical {
  background: var(--vp-c-bg);
}
.tr-canon-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 14px;
  border-bottom: 1px solid var(--vp-c-divider);
}
.tr-canon-label {
  font-size: 0.72em;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  text-transform: uppercase;
  letter-spacing: 0.6px;
}
.tr-canon-pre {
  margin: 0;
  padding: 14px;
  font-family: var(--vp-font-family-mono);
  font-size: 0.85em;
  line-height: 1.55;
  color: var(--vp-c-text-1);
  overflow-x: auto;
  background: var(--vp-c-bg);
}
.tr-diff {
  border-top: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
}
.tr-diff-head {
  padding: 8px 14px;
  border-bottom: 1px solid var(--vp-c-divider);
}
.tr-diff-label {
  font-size: 0.72em;
  font-weight: 800;
  color: var(--vp-c-text-2);
  text-transform: uppercase;
  letter-spacing: 0.6px;
}
.tr-diff-rows {
  font-family: var(--vp-font-family-mono);
  font-size: 0.78em;
  line-height: 1.5;
  padding: 8px 0;
}
.tr-diff-row {
  display: grid;
  grid-template-columns: 36px 1fr 14px 1fr;
  align-items: baseline;
  padding: 2px 14px;
}
.tr-diff-row.tr-row-same {
  color: var(--vp-c-text-2);
}
.tr-diff-row.tr-row-diff {
  background: color-mix(in srgb, #f59e0b 10%, transparent);
}
.tr-diff-row.tr-row-missing .tr-attempt-side {
  color: color-mix(in srgb, #ef4444 70%, var(--vp-c-text-1));
}
.tr-diff-row.tr-row-extra .tr-canon-side {
  opacity: 0.6;
}
.tr-ln {
  color: var(--vp-c-text-3);
  text-align: right;
  padding-right: 10px;
  user-select: none;
}
.tr-side {
  white-space: pre;
  overflow-x: hidden;
  text-overflow: ellipsis;
}
.tr-sep {
  color: var(--vp-c-divider);
  text-align: center;
}
@media (max-width: 640px) {
  .tr-diff-row {
    grid-template-columns: 28px 1fr;
    grid-template-rows: auto auto;
    gap: 2px 0;
  }
  .tr-sep { display: none; }
  .tr-canon-side {
    grid-column: 2;
    grid-row: 2;
    color: var(--vp-c-brand-1);
    border-top: 1px dashed var(--vp-c-divider);
    padding-top: 2px;
  }
}
</style>
