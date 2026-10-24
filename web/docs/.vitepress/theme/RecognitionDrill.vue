<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { withBase } from 'vitepress'
import { storage } from './lib/storage'
import problemsData from './data/recognition.problems.json'
import patternsData from './data/patterns.subvariations.json'

interface Problem {
  statement: string
  pattern: string
  subVariation?: string
  distractors?: string[]
}

interface PatternMeta {
  slug: string
  title: string
  chapter?: string
  subVariations?: Array<{ slug: string; title: string; difficulty?: string }>
}

const props = defineProps<{
  pattern: string
  count?: number
}>()

const allPatterns = patternsData as unknown as Record<string, PatternMeta>
const problemBank = problemsData as unknown as Record<string, Problem[]> & { _meta?: unknown }

const idx = ref(0)
const guessPattern = ref<string | null>(null)
const guessSubVariation = ref<string | null>(null)
const revealed = ref(false)
const scores = ref<Array<{ patternOk: boolean; subOk: boolean }>>([])
const finished = ref(false)

const storageKey = () => `dsa-recognition:${props.pattern}`

function pickProblems(): Problem[] {
  const n = props.count ?? 10
  if (props.pattern === 'mixed') {
    const pool: Problem[] = []
    for (const key of Object.keys(problemBank)) {
      if (key.startsWith('_')) continue
      const list = problemBank[key] as Problem[] | undefined
      if (Array.isArray(list)) pool.push(...list)
    }
    return shuffle(pool).slice(0, n)
  }
  const list = (problemBank[props.pattern] as Problem[] | undefined) ?? []
  return shuffle(list.slice()).slice(0, n)
}

function shuffle<T>(arr: T[]): T[] {
  const a = arr.slice()
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

const problems = ref<Problem[]>([])

onMounted(() => {
  problems.value = pickProblems()
})

const current = computed<Problem | null>(() => problems.value[idx.value] ?? null)

const patternChoices = computed<string[]>(() => {
  const c = current.value
  if (!c) return []
  const set = new Set<string>()
  set.add(c.pattern)
  for (const d of c.distractors ?? []) set.add(d)
  while (set.size < 4) {
    const keys = Object.keys(allPatterns)
    const k = keys[Math.floor(Math.random() * keys.length)]
    set.add(k)
  }
  return shuffle(Array.from(set)).slice(0, 4)
})

const correctPattern = computed(() => current.value?.pattern ?? '')
const correctSubVariation = computed(() => current.value?.subVariation ?? '')

const subChoices = computed<Array<{ slug: string; title: string }>>(() => {
  if (!guessPattern.value) return []
  const meta = allPatterns[guessPattern.value]
  return meta?.subVariations ?? []
})

const patternTitle = (slug: string): string => allPatterns[slug]?.title ?? slug
const subTitle = (patternSlug: string, subSlug: string): string => {
  const meta = allPatterns[patternSlug]
  return meta?.subVariations?.find(s => s.slug === subSlug)?.title ?? subSlug
}
const patternHref = (slug: string): string => {
  const chapter = allPatterns[slug]?.chapter
  return chapter ? withBase(chapter) : withBase('/')
}

function selectPattern(p: string) {
  if (revealed.value) return
  guessPattern.value = p
  guessSubVariation.value = null
}

function selectSub(sub: string) {
  if (revealed.value) return
  guessSubVariation.value = sub
}

function reveal() {
  if (revealed.value) return
  revealed.value = true
  const patternOk = guessPattern.value === correctPattern.value
  const subOk = correctSubVariation.value
    ? guessSubVariation.value === correctSubVariation.value
    : true
  scores.value.push({ patternOk, subOk })
}

function next() {
  if (idx.value < problems.value.length - 1) {
    idx.value++
    guessPattern.value = null
    guessSubVariation.value = null
    revealed.value = false
  } else {
    finishDrill()
  }
}

function finishDrill() {
  finished.value = true
  const result = {
    at: Date.now(),
    pattern: props.pattern,
    scores: scores.value,
    total: problems.value.length,
    patternCorrect: scores.value.filter(s => s.patternOk).length,
    subCorrect: scores.value.filter(s => s.subOk).length,
  }
  storage.setJson(storageKey(), result)
}

function restart() {
  idx.value = 0
  guessPattern.value = null
  guessSubVariation.value = null
  revealed.value = false
  scores.value = []
  finished.value = false
  problems.value = pickProblems()
}

const patternCorrect = computed(() => scores.value.filter(s => s.patternOk).length)
const subCorrect = computed(() => scores.value.filter(s => s.subOk).length)
const total = computed(() => problems.value.length)
</script>

<template>
  <div v-if="problems.length === 0" class="rd rd-empty">
    <p>
      No recognition problems are available for
      <strong>{{ pattern === 'mixed' ? 'mixed drill' : patternTitle(pattern) }}</strong>
      yet. These are populated as each chapter upgrade lands.
    </p>
  </div>

  <div v-else-if="finished" class="rd rd-finished">
    <div class="rd-score-head">
      <div class="rd-score-big">
        <span class="rd-score-num">{{ patternCorrect }}</span>
        <span class="rd-score-den">/ {{ total }}</span>
      </div>
      <div class="rd-score-lbl">patterns correctly recognized</div>
    </div>
    <div class="rd-score-sub">
      Sub-variation accuracy: <strong>{{ subCorrect }} / {{ total }}</strong>
    </div>
    <div class="rd-score-actions">
      <button class="rd-btn rd-btn-primary" type="button" @click="restart">Try another set</button>
      <a
        v-if="pattern !== 'mixed'"
        class="rd-btn"
        :href="withBase('/mixed-drill')"
      >Mix with all 21 patterns</a>
    </div>
  </div>

  <div v-else class="rd">
    <div class="rd-head">
      <span class="rd-badge">Recognition drill</span>
      <span class="rd-progress">Problem {{ idx + 1 }} of {{ total }}</span>
      <span v-if="pattern !== 'mixed'" class="rd-scope">
        Pattern locked in: <strong>{{ patternTitle(pattern) }}</strong> family
      </span>
      <span v-else class="rd-scope rd-mixed">
        Mixed — any of the 21 patterns
      </span>
    </div>

    <div class="rd-statement">
      <div class="rd-statement-label">Problem statement</div>
      <p>{{ current?.statement }}</p>
    </div>

    <div class="rd-q">
      <div class="rd-q-label">Which pattern applies?</div>
      <div class="rd-choices">
        <button
          v-for="p in patternChoices"
          :key="p"
          type="button"
          class="rd-choice"
          :class="{
            'rd-choice-selected': guessPattern === p && !revealed,
            'rd-choice-correct': revealed && p === correctPattern,
            'rd-choice-wrong': revealed && guessPattern === p && p !== correctPattern,
          }"
          :disabled="revealed"
          @click="selectPattern(p)"
        >
          {{ patternTitle(p) }}
        </button>
      </div>
    </div>

    <div v-if="guessPattern && subChoices.length" class="rd-q">
      <div class="rd-q-label">
        Which sub-variation of {{ patternTitle(guessPattern) }}?
      </div>
      <div class="rd-choices rd-choices-sub">
        <button
          v-for="sub in subChoices"
          :key="sub.slug"
          type="button"
          class="rd-choice rd-choice-sub"
          :class="{
            'rd-choice-selected': guessSubVariation === sub.slug && !revealed,
            'rd-choice-correct': revealed && sub.slug === correctSubVariation,
            'rd-choice-wrong': revealed && guessSubVariation === sub.slug && sub.slug !== correctSubVariation,
          }"
          :disabled="revealed"
          @click="selectSub(sub.slug)"
        >
          {{ sub.title }}
        </button>
      </div>
    </div>

    <div class="rd-actions">
      <button
        v-if="!revealed"
        class="rd-btn rd-btn-primary"
        type="button"
        :disabled="!guessPattern"
        @click="reveal"
      >
        Reveal
      </button>
      <button v-else class="rd-btn rd-btn-primary" type="button" @click="next">
        {{ idx < total - 1 ? 'Next problem' : 'See results' }}
      </button>
    </div>

    <div v-if="revealed && current" class="rd-reveal">
      <div class="rd-reveal-row" :class="{ 'rd-reveal-ok': guessPattern === correctPattern }">
        <span class="rd-reveal-lbl">Correct pattern:</span>
        <a :href="patternHref(correctPattern)" class="rd-reveal-val">
          {{ patternTitle(correctPattern) }}
        </a>
      </div>
      <div v-if="correctSubVariation" class="rd-reveal-row" :class="{ 'rd-reveal-ok': guessSubVariation === correctSubVariation }">
        <span class="rd-reveal-lbl">Sub-variation:</span>
        <span class="rd-reveal-val">{{ subTitle(correctPattern, correctSubVariation) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rd {
  margin: 24px 0;
  padding: 20px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
}
.rd-empty p {
  margin: 0;
  color: var(--vp-c-text-2);
  font-size: 0.9em;
  line-height: 1.5;
}
.rd-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 10px 14px;
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--vp-c-divider);
}
.rd-badge {
  font-size: 0.7em;
  font-weight: 800;
  color: var(--vp-c-brand-1);
  text-transform: uppercase;
  letter-spacing: 1px;
  background: color-mix(in srgb, var(--vp-c-brand-1) 15%, transparent);
  padding: 3px 10px;
  border-radius: 5px;
}
.rd-progress {
  font-size: 0.82em;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
.rd-scope {
  font-size: 0.8em;
  color: var(--vp-c-text-2);
}
.rd-mixed {
  color: var(--vp-c-brand-1);
}
.rd-statement {
  margin-bottom: 16px;
}
.rd-statement-label, .rd-q-label {
  font-size: 0.7em;
  font-weight: 800;
  color: var(--vp-c-text-2);
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 6px;
}
.rd-statement p {
  margin: 0;
  font-size: 0.95em;
  line-height: 1.55;
  color: var(--vp-c-text-1);
}
.rd-q {
  margin: 14px 0;
}
.rd-choices {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.rd-choices-sub {
  grid-template-columns: 1fr;
}
@media (min-width: 720px) {
  .rd-choices-sub {
    grid-template-columns: 1fr 1fr;
  }
}
.rd-choice {
  padding: 10px 14px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 7px;
  font-size: 0.88em;
  color: var(--vp-c-text-1);
  text-align: left;
  cursor: pointer;
  transition: all 0.15s ease;
}
.rd-choice:hover:not(:disabled) {
  border-color: var(--vp-c-brand-1);
}
.rd-choice:disabled {
  cursor: default;
}
.rd-choice-selected {
  border-color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 10%, var(--vp-c-bg));
}
.rd-choice-correct {
  border-color: #10b981;
  background: color-mix(in srgb, #10b981 15%, var(--vp-c-bg));
  color: var(--vp-c-text-1);
  font-weight: 600;
}
.rd-choice-wrong {
  border-color: #ef4444;
  background: color-mix(in srgb, #ef4444 10%, var(--vp-c-bg));
  color: var(--vp-c-text-1);
}
.rd-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}
.rd-btn {
  padding: 8px 16px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  font-size: 0.88em;
  font-weight: 600;
  color: var(--vp-c-text-1);
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
}
.rd-btn:hover:not(:disabled) {
  border-color: var(--vp-c-brand-1);
}
.rd-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.rd-btn-primary {
  background: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  color: #fff;
}
.rd-btn-primary:hover:not(:disabled) {
  background: var(--vp-c-brand-2);
  border-color: var(--vp-c-brand-2);
}
.rd-reveal {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px dashed var(--vp-c-divider);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.rd-reveal-row {
  display: flex;
  gap: 10px;
  font-size: 0.88em;
}
.rd-reveal-lbl {
  color: var(--vp-c-text-2);
  font-weight: 700;
  min-width: 120px;
}
.rd-reveal-val {
  color: var(--vp-c-text-1);
  font-weight: 600;
  text-decoration: none;
}
.rd-reveal-val:hover {
  color: var(--vp-c-brand-1);
}
.rd-reveal-ok .rd-reveal-val {
  color: #10b981;
}

.rd-finished {
  margin: 24px 0;
  padding: 32px 20px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  text-align: center;
}
.rd-score-head {
  margin-bottom: 10px;
}
.rd-score-big {
  display: inline-flex;
  align-items: baseline;
  gap: 4px;
  color: var(--vp-c-brand-1);
  font-weight: 800;
}
.rd-score-num {
  font-size: 3em;
  line-height: 1;
}
.rd-score-den {
  font-size: 1.4em;
  color: var(--vp-c-text-2);
}
.rd-score-lbl {
  margin-top: 4px;
  font-size: 0.9em;
  color: var(--vp-c-text-2);
}
.rd-score-sub {
  font-size: 0.95em;
  color: var(--vp-c-text-1);
  margin: 10px 0 20px;
}
.rd-score-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
