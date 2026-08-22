<script setup lang="ts">
/**
 * Generic execution-trace visualization.
 * Shows an array with per-iteration state: pointer positions, tracked variables, per-step note.
 * Renders as a horizontal step-strip of small frames — one frame per iteration.
 *
 * Usage:
 *   <CodeTrace
 *     title="Max Average Subarray I trace — nums=[1,12,-5,-6,50,3], k=4"
 *     :values="['1','12','-5','-6','50','3']"
 *     :steps="[
 *       { pointers: { left:0, right:3 }, vars:{ sum:'2', best:'2' }, note:'first full window' },
 *       ...
 *     ]"
 *     :windowKeys="['left','right']"
 *   />
 */
interface Step {
  pointers: Record<string, number>       // e.g. { left: 0, right: 3, i: 1 }
  vars?: Record<string, string | number> // e.g. { sum: 2, best: 2 }
  note?: string
  /** Optional: array of cell indices to color as "just added" (green). */
  added?: number[]
  /** Optional: array of cell indices to color as "just removed" (red). */
  removed?: number[]
}

const props = defineProps<{
  title?: string
  values: (string | number)[]
  steps: Step[]
  /** Names of pointers that together define the "current window" — those cells will be highlighted. */
  windowKeys?: string[]
  /** Pixel width of each cell (default 30 — narrower than main SVGs to fit many cells per step). */
  cellWidth?: number
}>()

const CELL = props.cellWidth ?? 30

function frameSvg(step: Step) {
  const n = props.values.length
  const svgWidth = 20 + n * CELL + 20
  const yCells = 44
  const cellHeight = 30

  // determine highlighted range if windowKeys provided
  let inWindow = new Set<number>()
  if (props.windowKeys && props.windowKeys.length >= 2) {
    const a = step.pointers[props.windowKeys[0]]
    const b = step.pointers[props.windowKeys[1]]
    if (a != null && b != null) {
      const lo = Math.min(a, b), hi = Math.max(a, b)
      for (let k = lo; k <= hi; k++) inWindow.add(k)
    }
  } else if (props.windowKeys && props.windowKeys.length === 1) {
    // single pointer — just highlight that cell
    const p = step.pointers[props.windowKeys[0]]
    if (p != null) inWindow.add(p)
  }

  const addedSet = new Set(step.added ?? [])
  const removedSet = new Set(step.removed ?? [])

  const cells = props.values.map((v, idx) => {
    const x = 20 + idx * CELL
    let color = 'neutral'
    if (removedSet.has(idx)) color = 'danger'
    else if (addedSet.has(idx)) color = 'success'
    else if (inWindow.has(idx)) color = 'primary'
    return `<rect x="${x}" y="${yCells}" width="${CELL - 2}" height="${cellHeight}" rx="4"
      fill="var(--dsa-${color}-soft)" stroke="var(--dsa-${color})" stroke-width="1.3"/>
      <text x="${x + (CELL - 2) / 2}" y="${yCells + 20}" text-anchor="middle"
        font-family="var(--dsa-font)" font-size="12" font-weight="700" fill="var(--dsa-ink)">${v}</text>
      <text x="${x + (CELL - 2) / 2}" y="${yCells + cellHeight + 12}" text-anchor="middle"
        font-family="var(--dsa-font)" font-size="9" fill="var(--dsa-neutral)">${idx}</text>`
  }).join('')

  // pointer labels — draw above the cells
  const pointerEntries = Object.entries(step.pointers)
  const pointerLabels = pointerEntries.map(([name, idx], k) => {
    if (idx < 0 || idx >= n) return ''
    const x = 20 + idx * CELL + (CELL - 2) / 2
    // alternate labels above/below to avoid overlap
    const yLabel = 30 - (k % 2) * 12
    const yArrow = 40
    return `<text x="${x}" y="${yLabel}" text-anchor="middle" font-family="var(--dsa-font)"
      font-size="10" font-weight="700" fill="var(--dsa-primary)">${name}</text>
      <path d="M${x},${yArrow - 2} L${x - 3},${yArrow - 8} L${x + 3},${yArrow - 8} Z"
        fill="var(--dsa-primary)"/>`
  }).join('')

  // vars block below
  const varEntries = step.vars ? Object.entries(step.vars) : []
  const varLines = varEntries.map(([name, val], k) => {
    return `<text x="20" y="${100 + k * 14}" font-family="var(--dsa-font)"
      font-size="11" fill="var(--dsa-ink)"><tspan font-weight="700"
      fill="var(--dsa-neutral)">${name}</tspan> = ${val}</text>`
  }).join('')

  const note = step.note
    ? `<text x="${svgWidth / 2}" y="${100 + varEntries.length * 14 + 14}"
       text-anchor="middle" font-family="var(--dsa-font)" font-size="10"
       font-style="italic" fill="var(--dsa-neutral)">${step.note}</text>`
    : ''

  const svgHeight = 100 + varEntries.length * 14 + (step.note ? 24 : 6)

  return `<svg viewBox="0 0 ${svgWidth} ${svgHeight}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <rect x="0" y="0" width="${svgWidth}" height="${svgHeight}" rx="6" fill="var(--dsa-bg)"/>
    ${pointerLabels}
    ${cells}
    ${varLines}
    ${note}
  </svg>`
}
</script>

<template>
  <figure class="code-trace">
    <figcaption v-if="title" class="code-trace-title">{{ title }}</figcaption>
    <div class="code-trace-track">
      <div v-for="(step, i) in steps" :key="i" class="code-trace-step">
        <div class="code-trace-step-index">Step {{ i + 1 }}</div>
        <div class="code-trace-svg" v-html="frameSvg(step)"></div>
      </div>
    </div>
  </figure>
</template>

<style scoped>
.code-trace {
  margin: 20px 0;
  padding: 14px 16px 16px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
}
.code-trace-title {
  font-weight: 700;
  color: var(--vp-c-text-1);
  font-size: 0.92em;
  margin-bottom: 12px;
}
.code-trace-track {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 10px;
}
.code-trace-step {
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.code-trace-step-index {
  font-size: 0.7em;
  font-weight: 700;
  color: var(--dsa-primary, #2563eb);
  text-transform: uppercase;
  letter-spacing: 0.6px;
}
.code-trace-svg {
  display: flex;
  justify-content: center;
}
.code-trace-svg :deep(svg) {
  max-width: 100%;
  height: auto;
}

@media (max-width: 540px) {
  .code-trace-track {
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    overflow-x: auto;
    padding-bottom: 6px;
  }
}
</style>
