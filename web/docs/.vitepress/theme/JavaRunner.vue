<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const props = defineProps<{
  problemSlug: string
  starter?: string
  tests?: Array<{ input: string; expected: string }>
}>()

const defaultStarter = props.starter || `import java.util.*;

public class Main {
    public static void main(String[] args) {
        // Read input from System.in, print result to System.out
        Scanner sc = new Scanner(System.in);
        // Your code here
    }
}`

const code = ref(defaultStarter)
const isRunning = ref(false)
const output = ref('')
const testResults = ref<Array<{ pass: boolean; input: string; expected: string; actual: string }>>([])

const STORAGE_KEY = computed(() => `dsa-code:${props.problemSlug}`)

onMounted(() => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY.value)
    if (saved) code.value = saved
  } catch (e) {}
})

function save() {
  try {
    localStorage.setItem(STORAGE_KEY.value, code.value)
    output.value = '✓ Saved to browser storage.'
  } catch (e) {
    output.value = 'Failed to save.'
  }
}

function reset() {
  code.value = defaultStarter
  try { localStorage.removeItem(STORAGE_KEY.value) } catch (e) {}
  output.value = 'Reset to starter code.'
  testResults.value = []
}

async function runTests() {
  if (!props.tests || props.tests.length === 0) {
    output.value = 'No test cases defined for this problem yet — use "Save" to persist your code.'
    return
  }
  isRunning.value = true
  output.value = 'Compiling and running via Judge0...'
  testResults.value = []

  try {
    for (const test of props.tests) {
      const response = await fetch('https://ce.judge0.com/submissions?base64_encoded=false&wait=true', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          language_id: 62,
          source_code: code.value,
          stdin: test.input,
          expected_output: test.expected,
          cpu_time_limit: 5
        })
      })
      const result = await response.json()
      const actual = (result.stdout || '').trim()
      const expected = test.expected.trim()
      testResults.value.push({
        pass: actual === expected,
        input: test.input,
        expected,
        actual: actual || result.compile_output || result.stderr || 'no output'
      })
    }
    const passed = testResults.value.filter(r => r.pass).length
    output.value = `${passed} / ${testResults.value.length} tests passed`
  } catch (e: any) {
    output.value = `Error: ${e.message}`
  } finally {
    isRunning.value = false
  }
}
</script>

<template>
  <ClientOnly>
    <div class="code-runner">
      <div class="runner-header">
        <span class="runner-title">💻 Try it — Java editor</span>
        <div class="runner-controls">
          <button @click="save" :disabled="isRunning">💾 Save</button>
          <button @click="reset" :disabled="isRunning">⟳ Reset</button>
          <button @click="runTests" :disabled="isRunning" class="run-btn">
            {{ isRunning ? '⏳ Running...' : '▶ Run tests' }}
          </button>
        </div>
      </div>
      <textarea v-model="code" class="editor" spellcheck="false"></textarea>
      <div v-if="output" class="runner-output">{{ output }}</div>
      <div v-if="testResults.length > 0" class="test-results">
        <div v-for="(r, i) in testResults" :key="i" :class="['test-row', r.pass ? 'pass' : 'fail']">
          <div class="test-header">
            <span>{{ r.pass ? '✅' : '❌' }} Test {{ i + 1 }}</span>
            <span v-if="!r.pass" class="fail-label">FAILED</span>
          </div>
          <div v-if="!r.pass" class="test-detail">
            <div><strong>Input:</strong> <code>{{ r.input }}</code></div>
            <div><strong>Expected:</strong> <code>{{ r.expected }}</code></div>
            <div><strong>Got:</strong> <code>{{ r.actual }}</code></div>
          </div>
        </div>
      </div>
      <div class="runner-note">
        Powered by <a href="https://ce.judge0.com" target="_blank" rel="noopener">Judge0</a> — free public Java compilation API.
        Code auto-saves to your browser only.
      </div>
    </div>
  </ClientOnly>
</template>

<style scoped>
.code-runner {
  margin: 20px 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  overflow: hidden;
  background: var(--vp-c-bg);
}
.runner-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: var(--vp-c-bg-soft);
  border-bottom: 1px solid var(--vp-c-divider);
}
.runner-title { font-size: 0.9em; font-weight: 700; color: var(--vp-c-text-1); }
.runner-controls { display: flex; gap: 6px; }
.runner-controls button {
  padding: 5px 12px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.82em;
  font-weight: 500;
  color: var(--vp-c-text-1);
  transition: all 0.15s ease;
}
.runner-controls button:hover:not(:disabled) {
  background: var(--vp-c-bg-mute);
  border-color: var(--vp-c-brand-1);
}
.runner-controls button:disabled { opacity: 0.5; cursor: not-allowed; }
.run-btn {
  background: var(--vp-c-brand-1) !important;
  color: white !important;
  border-color: var(--vp-c-brand-1) !important;
}
.run-btn:hover:not(:disabled) { background: var(--vp-c-brand-2) !important; }
.editor {
  width: 100%;
  height: 300px;
  padding: 12px 16px;
  border: none;
  border-bottom: 1px solid var(--vp-c-divider);
  background: #1e293b;
  color: #e2e8f0;
  font-family: "JetBrains Mono", "Cascadia Code", Consolas, monospace;
  font-size: 13px;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  tab-size: 4;
}
.editor:focus { border-bottom-color: var(--vp-c-brand-1); }
.runner-output {
  padding: 10px 14px;
  background: var(--vp-c-bg-soft);
  border-bottom: 1px solid var(--vp-c-divider);
  font-family: monospace;
  font-size: 0.85em;
}
.test-results { padding: 0; }
.test-row {
  padding: 10px 14px;
  border-bottom: 1px solid var(--vp-c-divider);
  font-size: 0.85em;
}
.test-row.pass { background: rgba(21, 128, 61, 0.05); }
.test-row.fail { background: rgba(220, 38, 38, 0.05); }
.test-header {
  display: flex;
  justify-content: space-between;
  font-weight: 500;
}
.fail-label { color: #dc2626; font-weight: 700; }
.test-detail {
  margin-top: 6px;
  padding-left: 22px;
  font-family: monospace;
  font-size: 0.85em;
  color: var(--vp-c-text-2);
}
.test-detail code {
  background: var(--vp-c-bg-mute);
  padding: 1px 5px;
  border-radius: 3px;
}
.runner-note {
  padding: 8px 14px;
  font-size: 0.76em;
  color: var(--vp-c-text-3);
  background: var(--vp-c-bg-soft);
}
.runner-note a { color: var(--vp-c-brand-1); }
</style>
