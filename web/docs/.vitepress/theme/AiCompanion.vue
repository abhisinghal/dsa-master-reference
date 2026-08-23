<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'

/**
 * AI Companion — a chat panel per problem/pattern page.
 *
 * MVP scope:
 * - Pre-baked FAQ-like responses to common prompts ("explain differently",
 *   "give me a hint", "what's the trap here", "walk me through it")
 * - When a real backend/API key is wired later, replace `answer()` with
 *   a fetch to /api/ai (or direct OpenAI/Anthropic client-side call).
 * - Conversation persists in localStorage per problem slug.
 */

const props = defineProps<{
  problemSlug: string
  patternHint?: string
  contextSummary?: string
}>()

interface Msg { role: 'user' | 'ai'; text: string }
const messages = ref<Msg[]>([])
const input = ref('')
const busy = ref(false)
const open = ref(false)
const scroller = ref<HTMLElement | null>(null)

const STORAGE_KEY = computed(() => `dsa-ai-chat:${props.problemSlug}`)

function loadHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY.value)
    if (raw) messages.value = JSON.parse(raw)
  } catch (e) {}
}
loadHistory()

function saveHistory() {
  try { localStorage.setItem(STORAGE_KEY.value, JSON.stringify(messages.value)) } catch (e) {}
}

const suggestions = [
  'Explain the intuition differently',
  'Give me a nudge, not the answer',
  'What edge cases should I test?',
  'Why is this O(n) and not O(n²)?',
  'What is the most common bug here?',
]

function answer(prompt: string): string {
  const q = prompt.toLowerCase()
  const p = props.patternHint || 'this pattern'

  if (/explain|different|analog|simpler|beginner/.test(q)) {
    return `Think of ${p} as a resource-allocation problem. You have a "budget" (window size, prefix sum, heap slot) and you slide it across the input, updating the budget when constraints allow. The invariant is: at any moment, the tracked answer is optimal over everything seen so far. The trick that makes it fast is that you never re-inspect elements you already processed.`
  }
  if (/hint|nudge|stuck|help me/.test(q)) {
    return `Try this: check the *Progressive Hints* panel above — Hint 1 gives you the shape, Hint 2 the key data structure, Hint 3 near-solution. If you still can't make progress, walk the first example on paper: what's the state after processing element 0? Element 1? What must be true for the invariant to hold?`
  }
  if (/edge|corner|test|break/.test(q)) {
    return `Standard edge cases for problems in the ${p} family: (1) empty input, (2) single element, (3) all-same elements, (4) duplicates at boundaries, (5) sorted or reverse-sorted input, (6) the value that makes the constraint exactly binding (e.g., k = n, target = sum). Trace at least the empty and single-element cases before submitting.`
  }
  if (/why|prove|complexity|big o|o\(/.test(q)) {
    return `The complexity claim comes from an amortization argument: each element is processed at most a constant number of times across all iterations of the outer + inner loops combined. Formal statement: total work = Σ (index i visits) ≤ 2n. This is why sliding-window / two-pointer / stack-based approaches consistently hit O(n) despite having nested loop syntax.`
  }
  if (/bug|mistake|common|wrong|pitfall/.test(q)) {
    return `Most-common bugs in this pattern: (1) off-by-one on window boundaries (r-l+1 vs r-l), (2) forgetting to shrink left inside the while loop, (3) integer overflow when summing (use long), (4) not skipping duplicates when the problem demands unique output, (5) initializing sentinel to wrong side (Integer.MIN_VALUE vs 0). Check your loop invariant on the first three inputs by hand.`
  }
  if (/walk|step|through|trace/.test(q)) {
    return `The *Execution Trace* embed above steps through the algorithm on Example 1. Click through the frames to see how (left, right, running_metric) evolve. Pay attention to when the invariant is temporarily broken and when it's restored — that's the boundary of a legitimate "shrink" step.`
  }
  if (/pattern|which|recognize/.test(q)) {
    return `Signals that point to ${p}: (a) the problem talks about contiguous / range / substring, (b) asks for max/min length or count of X, (c) input size is 10⁴-10⁶ suggesting O(n) is the bar, (d) the "brute force" is O(n²) with a nested loop where the inner loop revisits work. If ≥ 2 of those match, this pattern is likely.`
  }
  // Default response
  return `Great question. For "${prompt}" — the key insight for ${p} problems is to define a clear invariant on your window/state, ensure the invariant is easy to check in O(1), and prove that when you extend the boundary the invariant either holds or can be restored by shrinking. If you want to sanity-check a specific approach, paste your code idea and I'll flag anything that might break.`
}

async function send() {
  const text = input.value.trim()
  if (!text || busy.value) return
  input.value = ''
  messages.value.push({ role: 'user', text })
  busy.value = true
  saveHistory()
  await nextTick()
  scrollToBottom()

  // Simulate a small delay for UX
  await new Promise(r => setTimeout(r, 400 + Math.random() * 400))
  const reply = answer(text)
  messages.value.push({ role: 'ai', text: reply })
  busy.value = false
  saveHistory()
  await nextTick()
  scrollToBottom()
}

function sendSuggestion(s: string) {
  input.value = s
  send()
}

function scrollToBottom() {
  if (scroller.value) scroller.value.scrollTop = scroller.value.scrollHeight
}

function clearChat() {
  messages.value = []
  saveHistory()
}
</script>

<template>
  <div class="ai-panel">
    <div class="ai-header">
      <div class="ai-title">
        <span class="ai-icon">✨</span>
        <span>AI Study Companion</span>
        <span class="ai-badge">Beta</span>
      </div>
      <div class="ai-controls">
        <button v-if="messages.length > 0" class="ai-btn ghost" @click="clearChat" title="Clear">Clear</button>
        <button class="ai-btn" @click="open = !open">{{ open ? 'Hide' : 'Open chat' }}</button>
      </div>
    </div>
    <transition name="ai-slide">
      <div v-if="open" class="ai-body">
        <div v-if="messages.length === 0" class="ai-empty">
          <div class="ai-empty-title">Stuck? Ask me anything about this problem.</div>
          <div class="ai-empty-sub">I have access to the pattern, the code, and the traps. Tap a suggestion or type your own.</div>
          <div class="ai-suggestions">
            <button
              v-for="s in suggestions"
              :key="s"
              class="ai-suggest"
              @click="sendSuggestion(s)"
            >{{ s }}</button>
          </div>
        </div>
        <div v-else ref="scroller" class="ai-messages">
          <div v-for="(m, i) in messages" :key="i" :class="['ai-msg', m.role]">
            <div class="ai-msg-avatar">{{ m.role === 'user' ? '🧑' : '✨' }}</div>
            <div class="ai-msg-text">{{ m.text }}</div>
          </div>
          <div v-if="busy" class="ai-msg ai">
            <div class="ai-msg-avatar">✨</div>
            <div class="ai-msg-text ai-thinking">Thinking<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></div>
          </div>
        </div>
        <form class="ai-form" @submit.prevent="send">
          <input
            v-model="input"
            type="text"
            class="ai-input"
            placeholder="Ask a question about this problem…"
            :disabled="busy"
          />
          <button type="submit" class="ai-send" :disabled="!input.trim() || busy">Send</button>
        </form>
        <div class="ai-fine">
          MVP mode: responses use pattern-templated reasoning. Full LLM integration ships in v2.
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.ai-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  margin: 24px 0;
  background: linear-gradient(135deg, rgba(139,92,246,0.05), rgba(59,130,246,0.03));
}
.ai-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  gap: 8px;
  flex-wrap: wrap;
}
.ai-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
.ai-icon { font-size: 18px; }
.ai-badge {
  font-size: 10px;
  padding: 2px 6px;
  background: rgba(139,92,246,0.15);
  color: #8b5cf6;
  border-radius: 999px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.ai-controls { display: flex; gap: 6px; }
.ai-btn {
  padding: 6px 12px;
  border: 1px solid var(--vp-c-brand-1);
  border-radius: 6px;
  background: var(--vp-c-brand-1);
  color: white;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
}
.ai-btn.ghost { background: transparent; color: var(--vp-c-text-1); border-color: var(--vp-c-divider); }
.ai-body { padding: 0 18px 16px; }
.ai-empty {
  text-align: center;
  padding: 20px 12px;
}
.ai-empty-title { font-size: 14px; font-weight: 600; color: var(--vp-c-text-1); }
.ai-empty-sub { font-size: 12px; color: var(--vp-c-text-2); margin-top: 4px; }
.ai-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
  margin-top: 14px;
}
.ai-suggest {
  padding: 6px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}
.ai-suggest:hover { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); }
.ai-messages {
  max-height: 380px;
  overflow-y: auto;
  padding: 8px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.ai-msg {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--vp-c-bg);
}
.ai-msg.user { border-left: 3px solid var(--vp-c-brand-1); }
.ai-msg.ai { border-left: 3px solid #8b5cf6; }
.ai-msg-avatar { font-size: 20px; flex-shrink: 0; }
.ai-msg-text {
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--vp-c-text-1);
  white-space: pre-wrap;
}
.ai-thinking { color: var(--vp-c-text-3); }
.ai-thinking .dot {
  display: inline-block;
  animation: bounce 1.4s infinite;
}
.ai-thinking .dot:nth-child(2) { animation-delay: 0.2s; }
.ai-thinking .dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}
.ai-form {
  display: flex;
  gap: 6px;
  margin-top: 12px;
}
.ai-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
  font-family: inherit;
}
.ai-input:focus {
  outline: none;
  border-color: var(--vp-c-brand-1);
}
.ai-send {
  padding: 8px 16px;
  border: 1px solid var(--vp-c-brand-1);
  background: var(--vp-c-brand-1);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
}
.ai-send:disabled { opacity: 0.4; cursor: not-allowed; }
.ai-fine {
  font-size: 10.5px;
  color: var(--vp-c-text-3);
  margin-top: 8px;
  font-style: italic;
  text-align: center;
}
.ai-slide-enter-active, .ai-slide-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}
.ai-slide-enter-from, .ai-slide-leave-to { max-height: 0; opacity: 0; }
.ai-slide-enter-to, .ai-slide-leave-from { max-height: 800px; opacity: 1; }
</style>
