<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Icon from './Icon.vue'

interface Choice {
  text: string
  correct?: boolean
  explanation?: string
}

interface Question {
  q: string
  choices: Choice[]
}

const props = defineProps<{
  patternId: string
  questions: Question[]
}>()

const currentIdx = ref(0)
const selected = ref<number | null>(null)
const answered = ref<boolean[]>([])
const correctCount = ref(0)
const finished = ref(false)

const STORAGE_KEY = computed(() => `dsa-quiz:${props.patternId}`)

onMounted(() => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY.value)
    if (raw) {
      const state = JSON.parse(raw)
      if (state.finished) {
        finished.value = true
        correctCount.value = state.score || 0
      }
    }
  } catch (e) {}
})

function currentQuestion() {
  return props.questions[currentIdx.value]
}

function correctIndex(): number {
  const q = currentQuestion()
  return q.choices.findIndex(c => c.correct === true)
}

function pick(i: number) {
  if (selected.value !== null) return
  selected.value = i
  if (i === correctIndex()) correctCount.value++
}

function next() {
  answered.value.push(selected.value === correctIndex())
  selected.value = null
  if (currentIdx.value < props.questions.length - 1) {
    currentIdx.value++
  } else {
    finished.value = true
    try {
      localStorage.setItem(STORAGE_KEY.value, JSON.stringify({
        finished: true,
        score: correctCount.value,
        total: props.questions.length,
        ts: Date.now()
      }))
    } catch (e) {}
  }
}

function restart() {
  currentIdx.value = 0
  selected.value = null
  answered.value = []
  correctCount.value = 0
  finished.value = false
  try { localStorage.removeItem(STORAGE_KEY.value) } catch (e) {}
}

const scorePct = computed(() =>
  props.questions.length > 0
    ? Math.round((correctCount.value / props.questions.length) * 100)
    : 0
)

const verdict = computed(() => {
  if (scorePct.value === 100) return { icon: 'target', label: 'Perfect', color: '#15803d' }
  if (scorePct.value >= 67)   return { icon: 'check',  label: 'Solid', color: '#2563eb' }
  if (scorePct.value >= 33)   return { icon: 'zap',    label: 'Half-way — re-read the story section', color: '#b45309' }
  return { icon: 'book', label: 'Come back after re-reading the chapter', color: '#dc2626' }
})
</script>

<template>
  <ClientOnly>
    <div class="quiz">
      <div class="quiz-header">
        <span class="quiz-title"><Icon name="bulb" :size="18" /> Quick check — {{ patternId }} quiz</span>
        <span class="quiz-progress" v-if="!finished">
          Q {{ currentIdx + 1 }} / {{ questions.length }}
        </span>
      </div>

      <!-- In-progress question -->
      <div v-if="!finished" class="quiz-body">
        <div class="quiz-question">{{ currentQuestion().q }}</div>
        <div class="quiz-choices">
          <button
            v-for="(c, i) in currentQuestion().choices"
            :key="i"
            :class="[
              'choice',
              selected === i && correctIndex() === i && 'correct',
              selected === i && correctIndex() !== i && 'incorrect',
              selected !== null && correctIndex() === i && 'correct',
            ]"
            :disabled="selected !== null"
            @click="pick(i)"
          >
            <span class="choice-marker">{{ String.fromCharCode(65 + i) }}</span>
            <span class="choice-text">{{ c.text }}</span>
          </button>
        </div>

        <div v-if="selected !== null" class="quiz-explain">
          <template v-if="currentQuestion().choices[selected]?.explanation">
            <strong v-if="selected === correctIndex()" class="verdict-right"><Icon name="check" :size="15" /> Right — </strong>
            <strong v-else class="verdict-wrong"><Icon name="x" :size="15" /> Not quite. </strong>
            {{ currentQuestion().choices[selected].explanation }}
          </template>
          <template v-else-if="selected === correctIndex()">
            <strong class="verdict-right"><Icon name="check" :size="15" /> Correct.</strong>
          </template>
          <template v-else>
            <strong class="verdict-wrong"><Icon name="x" :size="15" /> Not quite.</strong>
            The correct answer is <strong>{{ String.fromCharCode(65 + correctIndex()) }}</strong>.
            <template v-if="currentQuestion().choices[correctIndex()].explanation">
              — {{ currentQuestion().choices[correctIndex()].explanation }}
            </template>
          </template>
        </div>

        <div v-if="selected !== null" class="quiz-actions">
          <button class="next-btn" @click="next">
            {{ currentIdx === questions.length - 1 ? 'See score →' : 'Next question →' }}
          </button>
        </div>
      </div>

      <!-- Finished screen -->
      <div v-else class="quiz-result">
        <div class="result-icon" :style="{ color: verdict.color }"><Icon :name="verdict.icon" :size="52" /></div>
        <div class="result-score" :style="{ color: verdict.color }">
          {{ correctCount }} / {{ questions.length }}
        </div>
        <div class="result-verdict">{{ verdict.label }}</div>
        <button class="restart-btn" @click="restart">Try again ↻</button>
      </div>
    </div>
  </ClientOnly>
</template>

<style scoped>
.quiz {
  margin: 24px 0;
  padding: 20px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
}
.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--vp-c-divider);
}
.quiz-title {
  font-weight: 700;
  color: var(--vp-c-text-1);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.verdict-right { color: #15803d; display: inline-flex; align-items: center; gap: 3px; }
.verdict-wrong { color: #dc2626; display: inline-flex; align-items: center; gap: 3px; }
.result-icon { margin-bottom: 8px; display: flex; justify-content: center; }
.quiz-progress {
  font-size: 0.85em;
  color: var(--vp-c-text-2);
  padding: 3px 10px;
  background: var(--vp-c-bg);
  border-radius: 12px;
}
.quiz-question {
  font-size: 1.02em;
  font-weight: 500;
  margin-bottom: 14px;
  line-height: 1.55;
}
.quiz-choices {
  display: grid;
  gap: 8px;
}
.choice {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  font-size: 0.94em;
  color: var(--vp-c-text-1);
  transition: all 0.15s ease;
}
.choice:hover:not(:disabled) {
  border-color: var(--vp-c-brand-1);
  transform: translateX(2px);
}
.choice:disabled {
  cursor: default;
  opacity: 0.7;
}
.choice.correct {
  background: rgba(21, 128, 61, 0.1);
  border-color: #15803d;
  opacity: 1;
}
.choice.incorrect {
  background: rgba(220, 38, 38, 0.08);
  border-color: #dc2626;
  opacity: 1;
}
.choice-marker {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--vp-c-bg-soft);
  font-weight: 700;
  font-size: 0.82em;
  color: var(--vp-c-text-2);
  flex-shrink: 0;
}
.choice.correct .choice-marker {
  background: #15803d;
  color: white;
}
.choice.incorrect .choice-marker {
  background: #dc2626;
  color: white;
}
.choice-text { flex: 1; }
.quiz-explain {
  margin-top: 14px;
  padding: 12px 14px;
  background: var(--vp-c-bg);
  border-left: 3px solid var(--vp-c-brand-1);
  border-radius: 4px;
  font-size: 0.9em;
  line-height: 1.5;
}
.quiz-actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
.next-btn, .restart-btn {
  padding: 8px 18px;
  border: none;
  background: var(--vp-c-brand-1);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9em;
  transition: background 0.15s ease;
}
.next-btn:hover, .restart-btn:hover {
  background: var(--vp-c-brand-2);
}
.quiz-result {
  text-align: center;
  padding: 20px;
}
.result-score {
  font-size: 2.2em;
  font-weight: 800;
  margin-bottom: 6px;
}
.result-verdict {
  color: var(--vp-c-text-2);
  font-size: 0.95em;
  margin-bottom: 20px;
}
</style>
