<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'

type Phase = {
  id: string
  title: string
  subtitle: string
  bullets: string[]
  color: string
  example: string
}

const props = defineProps<{
  problem?: string
  example?: string
  autoplay?: boolean
}>()

const PROBLEM = props.problem || 'Longest Substring Without Repeating Characters'
const EXAMPLE = props.example || 's = "abcabcbb"'

const PHASES: Phase[] = [
  {
    id: 'recognize',
    title: '1. Recognize',
    subtitle: 'What kind of problem is this?',
    bullets: [
      'Signal words: "substring", "longest", "contiguous"',
      'Data: string of characters, need to find a range',
      'Pattern candidate: Sliding Window'
    ],
    color: '#3b82f6',
    example: 'signals → sliding window'
  },
  {
    id: 'model',
    title: '2. Model',
    subtitle: 'What state maintains the invariant?',
    bullets: [
      'Window [l, r] contains only unique characters',
      'Track last-seen index of each character',
      'When s[r] was seen inside window, advance l past it'
    ],
    color: '#8b5cf6',
    example: 'state = (l, r, lastSeen: Map)'
  },
  {
    id: 'verify',
    title: '3. Verify',
    subtitle: 'Trace on the smallest example',
    bullets: [
      's = "abc"  → window grows to full string, answer 3',
      's = "aa"   → r=1: a seen at 0; l jumps to 1; answer 1',
      's = ""     → answer 0 (edge case: empty input)'
    ],
    color: '#06b6d4',
    example: 'trace: "abc"→3, "aa"→1, ""→0'
  },
  {
    id: 'code',
    title: '4. Code',
    subtitle: 'Translate the model to Java',
    bullets: [
      'Loop r from 0 to n-1',
      'On repeat inside window: l = lastSeen[c] + 1',
      'Update lastSeen[c] = r; track max(best, r - l + 1)'
    ],
    color: '#10b981',
    example: 'for(r) { … best = max(best, r-l+1); }'
  },
  {
    id: 'test',
    title: '5. Test',
    subtitle: 'Boundary + edge + adversarial',
    bullets: [
      'Empty string → 0',
      'All identical ("aaaa") → 1',
      'All distinct ("abcdef") → 6',
      'Repeats at boundary ("abba") → 2 (not 3!)'
    ],
    color: '#f59e0b',
    example: '"abba" trap: l cannot go backwards'
  },
  {
    id: 'optimize',
    title: '6. Optimize',
    subtitle: 'Can we do better?',
    bullets: [
      'Already O(n) time — each index touched twice',
      'Space O(σ) — bounded alphabet → O(1)',
      'ASCII-only? Replace HashMap with int[128]',
      'Nothing to save — ship it.'
    ],
    color: '#ef4444',
    example: 'O(n) time · O(σ) space · done'
  }
]

const idx = ref(0)
const playing = ref(props.autoplay ?? false)
let timer: number | null = null

const current = computed(() => PHASES[idx.value])

function next() { idx.value = (idx.value + 1) % PHASES.length }
function prev() { idx.value = (idx.value - 1 + PHASES.length) % PHASES.length }
function jump(i: number) { idx.value = i; pause() }
function toggle() {
  playing.value = !playing.value
  if (playing.value) { schedule() } else { pause() }
}
function schedule() {
  if (timer !== null) window.clearInterval(timer)
  timer = window.setInterval(() => {
    idx.value = (idx.value + 1) % PHASES.length
  }, 3200)
}
function pause() {
  if (timer !== null) { window.clearInterval(timer); timer = null }
  playing.value = false
}
function reset() { idx.value = 0; pause() }

if (props.autoplay) schedule()
onBeforeUnmount(() => { if (timer !== null) window.clearInterval(timer) })

const progressPct = computed(() => ((idx.value + 1) / PHASES.length) * 100)
</script>

<template>
  <div class="pb-viz">
    <div class="pb-badge">Interactive · 6-Phase Playbook</div>
    <div class="pb-header">
      <div>
        <div class="pb-problem">{{ PROBLEM }}</div>
        <div class="pb-example"><code>{{ EXAMPLE }}</code></div>
      </div>
      <div class="pb-controls">
        <button @click="reset" title="Reset">↺</button>
        <button @click="prev" title="Previous">‹</button>
        <button @click="toggle" :title="playing ? 'Pause' : 'Play'">
          {{ playing ? '⏸' : '▶' }}
        </button>
        <button @click="next" title="Next">›</button>
      </div>
    </div>

    <div class="pb-progressTrack">
      <div class="pb-progressBar" :style="{ width: progressPct + '%', background: current.color }"></div>
    </div>

    <div class="pb-strip">
      <button
        v-for="(p, i) in PHASES"
        :key="p.id"
        :class="['pb-tab', { active: i === idx, done: i < idx }]"
        :style="{ '--phase-color': p.color }"
        @click="jump(i)"
      >
        <div class="pb-tabIndex">{{ i + 1 }}</div>
        <div class="pb-tabTitle">{{ p.title.replace(/^\d+\.\s*/, '') }}</div>
      </button>
    </div>

    <div class="pb-panel" :style="{ borderColor: current.color }">
      <div class="pb-panelHead" :style="{ background: current.color }">
        <span class="pb-panelTitle">{{ current.title }}</span>
        <span class="pb-panelSub">— {{ current.subtitle }}</span>
      </div>
      <ul class="pb-bullets">
        <li v-for="b in current.bullets" :key="b">{{ b }}</li>
      </ul>
      <div class="pb-exampleBox">
        <span class="pb-exLabel">Working artefact</span>
        <code>{{ current.example }}</code>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pb-viz {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 20px;
  background: var(--vp-c-bg-soft);
  margin: 24px 0;
}
.pb-badge {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-weight: 600;
  margin-bottom: 12px;
}
.pb-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.pb-problem { font-size: 16px; font-weight: 700; color: var(--vp-c-text-1); }
.pb-example { font-size: 12px; color: var(--vp-c-text-2); margin-top: 4px; }
.pb-example code {
  background: var(--vp-c-bg); padding: 2px 6px; border-radius: 4px;
  font-family: ui-monospace, monospace;
}
.pb-controls { display: flex; gap: 6px; }
.pb-controls button {
  width: 32px; height: 32px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  font-size: 14px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.pb-controls button:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.pb-progressTrack {
  height: 4px;
  background: var(--vp-c-bg);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 16px;
}
.pb-progressBar { height: 100%; transition: width 0.3s ease, background 0.3s ease; }
.pb-strip {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 6px;
  margin-bottom: 18px;
}
.pb-tab {
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  border-radius: 8px;
  padding: 8px 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  --phase-color: #64748b;
}
.pb-tab:hover {
  border-color: var(--phase-color);
  transform: translateY(-1px);
}
.pb-tab.active {
  border-color: var(--phase-color);
  background: color-mix(in oklab, var(--phase-color) 12%, var(--vp-c-bg));
  box-shadow: 0 2px 8px color-mix(in oklab, var(--phase-color) 20%, transparent);
}
.pb-tab.done {
  border-color: color-mix(in oklab, var(--phase-color) 50%, var(--vp-c-divider));
  opacity: 0.9;
}
.pb-tabIndex {
  width: 22px; height: 22px;
  border-radius: 50%;
  background: var(--phase-color);
  color: white;
  font-size: 11px;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.pb-tab.done .pb-tabIndex::after { content: '✓'; }
.pb-tab.done .pb-tabIndex { font-size: 0; }
.pb-tab.done .pb-tabIndex::after { font-size: 12px; }
.pb-tabTitle {
  font-size: 11px;
  font-weight: 600;
  color: var(--vp-c-text-2);
  text-align: center;
}
.pb-tab.active .pb-tabTitle { color: var(--vp-c-text-1); }
.pb-panel {
  border: 2px solid;
  border-radius: 10px;
  overflow: hidden;
  transition: border-color 0.3s;
}
.pb-panelHead {
  padding: 10px 14px;
  color: white;
  font-weight: 600;
  transition: background 0.3s;
}
.pb-panelTitle { font-size: 14px; }
.pb-panelSub { font-size: 13px; opacity: 0.9; font-weight: 400; }
.pb-bullets {
  margin: 0; padding: 14px 20px 6px 34px;
  list-style: disc;
}
.pb-bullets li {
  font-size: 14px;
  color: var(--vp-c-text-1);
  margin-bottom: 6px;
  line-height: 1.45;
}
.pb-exampleBox {
  margin: 6px 14px 14px 14px;
  padding: 10px 12px;
  background: var(--vp-c-bg);
  border: 1px dashed var(--vp-c-divider);
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.pb-exLabel {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--vp-c-text-3);
  font-weight: 600;
  white-space: nowrap;
}
.pb-exampleBox code {
  font-family: ui-monospace, monospace;
  font-size: 12px;
  color: var(--vp-c-text-1);
  background: transparent;
}
@media (max-width: 640px) {
  .pb-strip { grid-template-columns: repeat(3, 1fr); }
}
</style>
