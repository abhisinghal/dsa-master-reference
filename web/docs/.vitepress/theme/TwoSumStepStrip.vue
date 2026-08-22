<script setup lang="ts">
import StepStrip from './StepStrip.vue'

const cellRect = (x: number, y: number, color: string) =>
  `<rect x="${x}" y="${y}" width="44" height="44" rx="7" fill="var(--dsa-${color}-soft)" stroke="var(--dsa-${color})" stroke-width="1.6"/>`
const cellText = (x: number, y: number, value: string) =>
  `<text x="${x + 22}" y="${y + 28}" text-anchor="middle" font-family="var(--dsa-font)" font-size="17" font-weight="700" fill="var(--dsa-ink)">${value}</text>`

function frame(i: number, values: string[], primaryIdx: number, successIdx: number | null, mapEntries: string[]) {
  const yArr = 40
  const cells = values.map((v, idx) => {
    const color = idx === successIdx ? 'success' : idx === primaryIdx ? 'primary' : 'neutral'
    const x = 24 + idx * 52
    return cellRect(x, yArr, color) + cellText(x, yArr, v)
  }).join('')
  const idxLabels = values.map((_, idx) => {
    const x = 24 + idx * 52 + 22
    return `<text x="${x}" y="${yArr + 62}" text-anchor="middle" font-family="var(--dsa-font)" font-size="11" fill="var(--dsa-neutral)">${idx}</text>`
  }).join('')
  const mapBox = mapEntries.length
    ? `<rect x="24" y="130" width="200" height="${20 + 18 * mapEntries.length}" rx="8" fill="var(--dsa-info-soft)" stroke="var(--dsa-info)" stroke-width="1.4"/>
       <text x="34" y="150" font-family="var(--dsa-font)" font-size="11" font-weight="700" fill="var(--dsa-info)">seen{value→index}</text>
       ${mapEntries.map((e, i) => `<text x="42" y="${168 + i * 18}" font-family="var(--dsa-font)" font-size="12" fill="var(--dsa-ink)">${e}</text>`).join('')}`
    : `<rect x="24" y="130" width="200" height="38" rx="8" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.4" stroke-dasharray="4 3"/>
       <text x="124" y="154" text-anchor="middle" font-family="var(--dsa-font)" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">empty</text>`
  return `<svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
    <text x="120" y="24" text-anchor="middle" font-family="var(--dsa-font)" font-size="12" font-weight="700" fill="var(--dsa-primary)">i=${i}</text>
    ${cells}${idxLabels}${mapBox}
  </svg>`
}

const steps = [
  {
    svg: frame(0, ['2', '7', '11', '15'], 0, null, []),
    caption: 'i=0, x=2. target-x = 7. Map empty → miss. Store seen[2]=0.'
  },
  {
    svg: frame(1, ['2', '7', '11', '15'], 1, 0, ['2 → 0']),
    caption: 'i=1, x=7. target-x = 2. seen[2]=0 → HIT. Return [0,1].'
  },
  {
    svg: frame(2, ['2', '7', '11', '15'], 2, null, ['2 → 0', '7 → 1']),
    caption: '(unused) If we hadn\'t hit at i=1: i=2, x=11, target-x = −2. Miss. Store seen[11]=2.'
  },
  {
    svg: frame(3, ['2', '7', '11', '15'], 3, null, ['2 → 0', '7 → 1', '11 → 2']),
    caption: '(unused) i=3, x=15, target-x = −6. Miss. The invariant: any pair summing to target is caught the moment the second element is scanned.'
  }
]
</script>

<template>
  <StepStrip
    title="Two Sum comic strip — target=9, one pass, O(n) time O(n) space"
    :steps="steps"
  />
</template>
