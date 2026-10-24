<script setup lang="ts">
import { computed } from 'vue'
import StepStrip from './StepStrip.vue'

interface Frame {
  lo: number
  hi: number
  mid: number
  verdict: 'go-left' | 'go-right' | 'found'
  caption: string
}

const props = defineProps<{
  title?: string
  input: Array<string | number>
  target?: string | number
  frames: Frame[]
}>()

const CELL = 40
const GAP = 4
const PAD_X = 20
const PAD_Y = 44

function cellRect(x: number, y: number, color: string, dashed = false) {
  const dash = dashed ? ` stroke-dasharray="4 3"` : ''
  return `<rect x="${x}" y="${y}" width="${CELL}" height="${CELL}" rx="6" fill="var(--dsa-${color}-soft, #f1f5f9)" stroke="var(--dsa-${color}, #64748b)" stroke-width="1.6"${dash}/>`
}
function cellText(x: number, y: number, v: string, muted = false) {
  const fill = muted ? 'var(--vp-c-text-3, #94a3b8)' : 'var(--dsa-ink, #0f172a)'
  return `<text x="${x + CELL / 2}" y="${y + CELL / 2 + 5}" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="14" font-weight="700" fill="${fill}">${v}</text>`
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
  const n = props.input.length
  const width = PAD_X * 2 + n * CELL + (n - 1) * GAP
  const height = PAD_Y + CELL + 40
  const yArr = PAD_Y
  const cells = props.input.map((v, i) => {
    const inRange = i >= frame.lo && i <= frame.hi
    const isMid = i === frame.mid
    const color = frame.verdict === 'found' && isMid ? 'success' : isMid ? 'warning' : inRange ? 'primary' : 'neutral'
    const x = PAD_X + i * (CELL + GAP)
    return cellRect(x, yArr, color, !inRange) + cellText(x, yArr, String(v), !inRange)
  }).join('')
  const loX = PAD_X + frame.lo * (CELL + GAP)
  const midX = PAD_X + frame.mid * (CELL + GAP)
  const hiX = PAD_X + frame.hi * (CELL + GAP)
  const upperLabels =
    frame.lo === frame.hi && frame.lo === frame.mid
      ? pointerLabel(loX, yArr, 'lo=hi=mid', 'primary')
      : pointerLabel(loX, yArr, 'lo', 'primary') + (frame.hi !== frame.lo ? pointerLabel(hiX, yArr, 'hi', 'primary') : '')
  const midLabel = (frame.mid !== frame.lo && frame.mid !== frame.hi)
    ? pointerLabel(midX, yArr, 'mid', 'warning', true)
    : (frame.lo !== frame.hi ? pointerLabel(midX, yArr, 'mid', 'warning', true) : '')
  const target = props.target !== undefined
    ? `<text x="${width / 2}" y="20" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="11.5" font-weight="700" fill="var(--vp-c-text-1)">target = ${props.target}</text>`
    : ''
  return `<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">${target}${cells}${upperLabels}${midLabel}</svg>`
}

const steps = computed(() =>
  props.frames.map(f => ({ svg: renderSvg(f), caption: f.caption }))
)
</script>

<template>
  <StepStrip :title="title" :steps="steps" />
</template>
