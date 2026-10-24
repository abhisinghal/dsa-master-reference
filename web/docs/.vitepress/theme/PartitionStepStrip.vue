<script setup lang="ts">
import { computed } from 'vue'
import StepStrip from './StepStrip.vue'

interface Frame {
  array: Array<string | number>
  i: number
  j: number
  pivot: number
  caption: string
  swap?: boolean
}

const props = defineProps<{
  title?: string
  frames: Frame[]
}>()

const CELL = 40
const GAP = 4
const PAD_X = 20
const PAD_Y = 48

function cellRect(x: number, y: number, color: string) {
  return `<rect x="${x}" y="${y}" width="${CELL}" height="${CELL}" rx="6" fill="var(--dsa-${color}-soft, #f1f5f9)" stroke="var(--dsa-${color}, #64748b)" stroke-width="1.6"/>`
}
function cellText(x: number, y: number, v: string) {
  return `<text x="${x + CELL / 2}" y="${y + CELL / 2 + 5}" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="14" font-weight="700" fill="var(--dsa-ink, #0f172a)">${v}</text>`
}
function pointerLabel(x: number, y: number, label: string, color: string, below = false) {
  const cx = x + CELL / 2
  if (below) {
    return `
      <polygon points="${cx - 5},${y + CELL + 2} ${cx + 5},${y + CELL + 2} ${cx},${y + CELL + 9}" fill="var(--dsa-${color}, #2563eb)"/>
      <text x="${cx}" y="${y + CELL + 24}" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="11" font-weight="800" fill="var(--dsa-${color}, #2563eb)">${label}</text>
    `
  }
  return `
    <polygon points="${cx - 5},${y - 2} ${cx + 5},${y - 2} ${cx},${y - 9}" fill="var(--dsa-${color}, #2563eb)"/>
    <text x="${cx}" y="${y - 14}" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="11" font-weight="800" fill="var(--dsa-${color}, #2563eb)">${label}</text>
  `
}

function renderSvg(frame: Frame): string {
  const n = frame.array.length
  const width = PAD_X * 2 + n * CELL + (n - 1) * GAP
  const height = PAD_Y + CELL + 40
  const yArr = PAD_Y
  const cells = frame.array.map((v, idx) => {
    const color = idx === frame.pivot ? 'warning' : idx === frame.i ? 'primary' : idx === frame.j ? 'info' : idx < frame.i ? 'success' : 'neutral'
    const x = PAD_X + idx * (CELL + GAP)
    return cellRect(x, yArr, color) + cellText(x, yArr, String(v))
  }).join('')
  const iX = PAD_X + frame.i * (CELL + GAP)
  const jX = PAD_X + frame.j * (CELL + GAP)
  const pivotX = PAD_X + frame.pivot * (CELL + GAP)
  const iLabel = pointerLabel(iX, yArr, 'i', 'primary')
  const jLabel = frame.j !== frame.i ? pointerLabel(jX, yArr, 'j', 'info', true) : ''
  const pivotLabel = pointerLabel(pivotX, yArr, 'pivot', 'warning', frame.pivot !== frame.i)
  const header = frame.swap
    ? `<text x="${width / 2}" y="22" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="12" font-weight="800" fill="var(--vp-c-brand-1, #2563eb)">↔ swap</text>`
    : ''
  return `<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">${header}${cells}${iLabel}${jLabel}${pivotLabel}</svg>`
}

const steps = computed(() =>
  props.frames.map(f => ({ svg: renderSvg(f), caption: f.caption }))
)
</script>

<template>
  <StepStrip :title="title" :steps="steps" />
</template>
