<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

type TestCase = { input: string; expected: string }
type TestResult = { pass: boolean; input: string; expected: string; actual: string }
type CheerpJRunMain = (className: string, classPath: string, ...args: string[]) => Promise<number>

declare global {
  interface Window {
    cheerpjInit?: (options?: { status?: 'splash' | 'none' | 'default'; version?: number }) => Promise<void>
    cheerpjRunMain?: CheerpJRunMain
    cheerpOSAddStringFile?: (path: string, data: string | Uint8Array) => void
    cheerpjAddStringFile?: (path: string, data: string | Uint8Array) => void
    cjFileBlob?: (path: string) => Promise<Blob>
  }
}

const props = defineProps<{
  problemSlug: string
  starter?: string
  tests?: TestCase[]
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
const isRuntimeLoading = ref(false)
const runtimeReady = ref(false)
const runtimeError = ref('')
const output = ref('')
const testResults = ref<TestResult[]>([])
let cheerpjInitPromise: Promise<void> | null = null

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
  runtimeError.value = ''
  testResults.value = []
}

async function initCheerpJ() {
  if (runtimeReady.value) return
  if (typeof window === 'undefined' || !window.cheerpjInit) {
    throw new Error('CheerpJ runtime failed to load. Please refresh the page and try again.')
  }

  isRuntimeLoading.value = true
  runtimeError.value = ''
  output.value = 'Loading Java runtime...'
  try {
    cheerpjInitPromise ||= window.cheerpjInit({ status: 'none', version: 17 })
    await cheerpjInitPromise
    runtimeReady.value = true
  } catch (e: any) {
    runtimeError.value = `Runner temporarily unavailable: ${e?.message || 'CheerpJ initialization failed'}`
    throw e
  } finally {
    isRuntimeLoading.value = false
  }
}

function addStringFile(path: string, data: string) {
  const addFile = window.cheerpOSAddStringFile || window.cheerpjAddStringFile
  if (!addFile) throw new Error('CheerpJ file API is not available.')
  addFile(path, data)
}

async function readCheerpJFile(path: string) {
  if (!window.cjFileBlob) throw new Error('CheerpJ file read API is not available.')
  return await (await window.cjFileBlob(path)).text()
}

function makeJavaIdentifier(prefix: string) {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`
}

function normalizeUserMain(source: string, userClassName: string) {
  return source
    .replace(/^\s*package\s+[^;]+;\s*/gm, '')
    .replace(/\bMain\b/g, userClassName)
    .replace(new RegExp(`public\\s+class\\s+${userClassName}\\b`), `class ${userClassName}`)
}

function extractImports(source: string) {
  const imports = source.match(/^\s*import\s+[^;]+;\s*$/gm) || []
  const body = source.replace(/^\s*import\s+[^;]+;\s*$/gm, '').trim()
  return { imports: Array.from(new Set(imports.map(i => i.trim()))), body }
}

function buildRunnerSource(runnerClassName: string, userClassName: string) {
  const normalized = normalizeUserMain(code.value, userClassName)
  const { imports, body } = extractImports(normalized)
  return `${imports.join('\n')}
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;

public class ${runnerClassName} {
    public static void main(String[] args) throws Exception {
        String inputPath = args[0];
        String outputPath = args[1];
        byte[] inputBytes = Files.readAllBytes(Paths.get(inputPath));
        InputStream previousIn = System.in;
        PrintStream previousOut = System.out;
        PrintStream previousErr = System.err;
        ByteArrayOutputStream stdout = new ByteArrayOutputStream();
        ByteArrayOutputStream stderr = new ByteArrayOutputStream();
        PrintStream captureOut = new PrintStream(stdout, true, "UTF-8");
        PrintStream captureErr = new PrintStream(stderr, true, "UTF-8");
        Throwable failure = null;

        try {
            System.setIn(new ByteArrayInputStream(inputBytes));
            System.setOut(captureOut);
            System.setErr(captureErr);
            ${userClassName}.main(new String[0]);
        } catch (Throwable t) {
            failure = t;
        } finally {
            captureOut.flush();
            captureErr.flush();
            System.setIn(previousIn);
            System.setOut(previousOut);
            System.setErr(previousErr);
        }

        String result = stdout.toString("UTF-8");
        String err = stderr.toString("UTF-8");
        if (failure != null) {
            StringWriter sw = new StringWriter();
            failure.printStackTrace(new PrintWriter(sw));
            result = (result + (err.isEmpty() ? "" : "\n[stderr]\n" + err) + "\n[error]\n" + sw.toString()).trim();
        }
        Files.write(Paths.get(outputPath), result.getBytes(StandardCharsets.UTF_8));
    }
}

${body}
`
}

async function compileRunner(sourcePath: string) {
  if (!window.cheerpjRunMain) throw new Error('CheerpJ execution API is not available.')
  const args = ['-encoding', 'UTF-8', '-d', '/files', sourcePath]
  const attempts: Array<[string, string]> = [
    ['com.sun.tools.javac.Main', ''],
    ['com.sun.tools.javac.Main', '/app/tools.jar']
  ]

  let lastError = ''
  for (const [className, classPath] of attempts) {
    try {
      const exitCode = await window.cheerpjRunMain(className, classPath, ...args)
      if (exitCode === 0) return
      lastError = `javac exited with code ${exitCode}`
    } catch (e: any) {
      lastError = e?.message || String(e)
    }
  }

  throw new Error(`Compilation failed in the browser runtime. ${lastError}`)
}

async function runTests() {
  if (!props.tests || props.tests.length === 0) {
    output.value = 'No test cases defined for this problem yet — use "Save" to persist your code.'
    return
  }
  isRunning.value = true
  testResults.value = []

  try {
    await initCheerpJ()
    if (!window.cheerpjRunMain) throw new Error('CheerpJ execution API is not available.')

    output.value = 'Compiling and running in your browser...'
    const runnerClassName = makeJavaIdentifier('DsaRunner')
    const userClassName = makeJavaIdentifier('DsaUserMain')
    const sourcePath = `/str/${runnerClassName}.java`
    addStringFile(sourcePath, buildRunnerSource(runnerClassName, userClassName))
    await compileRunner(sourcePath)

    for (const [index, test] of props.tests.entries()) {
      const inputPath = `/str/${runnerClassName}_input_${index}.txt`
      const outputPath = `/files/${runnerClassName}_output_${index}.txt`
      addStringFile(inputPath, test.input)
      const exitCode = await window.cheerpjRunMain(runnerClassName, '/files', inputPath, outputPath)
      const actual = exitCode === 0
        ? (await readCheerpJFile(outputPath)).trim()
        : `Program exited with code ${exitCode}`
      const expected = test.expected.trim()
      testResults.value.push({
        pass: actual === expected,
        input: test.input,
        expected,
        actual: actual || 'no output'
      })
    }

    const passed = testResults.value.filter(r => r.pass).length
    output.value = `${passed} / ${testResults.value.length} tests passed`
  } catch (e: any) {
    runtimeError.value = `Runner temporarily unavailable: ${e?.message || 'Java runtime error'}`
    output.value = `${runtimeError.value}. Please try again later.`
  } finally {
    isRunning.value = false
    isRuntimeLoading.value = false
  }
}
</script>

<template>
  <ClientOnly>
    <div class="code-runner">
      <div class="runner-header">
        <span class="runner-title">💻 Try it — Java editor</span>
        <div class="runner-controls">
          <button @click="save" :disabled="isRunning || isRuntimeLoading">💾 Save</button>
          <button @click="reset" :disabled="isRunning || isRuntimeLoading">⟳ Reset</button>
          <button @click="runTests" :disabled="isRunning || isRuntimeLoading" class="run-btn">
            {{ isRuntimeLoading ? '⏳ Loading Java runtime...' : isRunning ? '⏳ Running...' : '▶ Run tests' }}
          </button>
        </div>
      </div>
      <textarea v-model="code" class="editor" spellcheck="false"></textarea>
      <div v-if="isRuntimeLoading" class="runner-status">
        <span class="spinner" aria-hidden="true"></span>
        Loading Java runtime...
      </div>
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
        Powered by <a href="https://cheerpj.com" target="_blank" rel="noopener">CheerpJ WASM</a> — Java runs locally in your browser after a one-time runtime download.
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
.runner-status,
.runner-output {
  padding: 10px 14px;
  background: var(--vp-c-bg-soft);
  border-bottom: 1px solid var(--vp-c-divider);
  font-family: monospace;
  font-size: 0.85em;
}
.runner-status {
  display: flex;
  align-items: center;
  gap: 8px;
}
.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--vp-c-divider);
  border-top-color: var(--vp-c-brand-1);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
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

@media (max-width: 640px) {
  .runner-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  .runner-controls {
    justify-content: space-between;
  }
  .editor {
    height: 240px;
    font-size: 12px;
    padding: 10px 12px;
  }
  .test-detail code {
    word-break: break-all;
  }
}
</style>
