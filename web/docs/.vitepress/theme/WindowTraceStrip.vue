<script setup lang="ts">
import { computed } from 'vue'
import StepStrip from './StepStrip.vue'

interface Frame {
  l: number
  r: number
  caption: string
  info?: string
}

const props = defineProps<{
  title?: string
  input: Array<string | number>
  frames: Frame[]
}>()

const CELL = 42
const GAP = 4
const PAD_X = 20
const PAD_Y = 32

function cellRect(x: number, y: number, color: string) {
  return `<rect x="${x}" y="${y}" width="${CELL}" height="${CELL}" rx="6" fill="var(--dsa-${color}-soft, #f1f5f9)" stroke="var(--dsa-${color}, #64748b)" stroke-width="1.6"/>`
}
function cellText(x: number, y: number, v: string) {
  return `<text x="${x + CELL / 2}" y="${y + CELL / 2 + 5}" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="15" font-weight="700" fill="var(--dsa-ink, #0f172a)">${v}</text>`
}
function pointerCaret(x: number, y: number, label: string, color: string) {
  const cx = x + CELL / 2
  return `
    <polygon points="${cx - 6},${y} ${cx + 6},${y} ${cx},${y - 7}" fill="var(--dsa-${color}, #2563eb)"/>
    <text x="${cx}" y="${y - 12}" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="11" font-weight="800" fill="var(--dsa-${color}, #2563eb)">${label}</text>
  `
}

function renderSvg(frame: Frame): string {
  const n = props.input.length
  const width = PAD_X * 2 + n * CELL + (n - 1) * GAP
  const height = PAD_Y + CELL + 32
  const yArr = PAD_Y
  const cells = props.input.map((v, i) => {
    const inside = i >= frame.l && i <= frame.r
    const color = inside ? 'primary' : 'neutral'
    const x = PAD_X + i * (CELL + GAP)
    return cellRect(x, yArr, color) + cellText(x, yArr, String(v))
  }).join('')
  const lx = PAD_X + frame.l * (CELL + GAP)
  const rx = PAD_X + frame.r * (CELL + GAP)
  const pointers =
    frame.l === frame.r
      ? pointerCaret(lx, yArr - 2, 'l=r', 'primary')
      : pointerCaret(lx, yArr - 2, 'l', 'primary') + pointerCaret(rx, yArr - 2, 'r', 'primary')
  const info = frame.info
    ? `<text x="${width / 2}" y="${yArr + CELL + 24}" text-anchor="middle" font-family="var(--dsa-font, system-ui)" font-size="12" font-weight="700" fill="var(--vp-c-text-1)">${frame.info}</text>`
    : ''
  return `<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">${cells}${pointers}${info}</svg>`
}

const steps = computed(() =>
  props.frames.map(f => ({ svg: renderSvg(f), caption: f.caption }))
)
</script>

<template>
  <StepStrip :title="title" :steps="steps" />
</template>
