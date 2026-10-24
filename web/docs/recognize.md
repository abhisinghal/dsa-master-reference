---
title: Recognition drill
description: Pattern recognition is the first bottleneck in a DSA interview. Train it in isolation.
---

<script setup>
import { ref, onMounted } from 'vue'
import patternsData from './.vitepress/theme/data/patterns.subvariations.json'
import problemsData from './.vitepress/theme/data/recognition.problems.json'

const allPatterns = patternsData
const problemBank = problemsData

const availablePatterns = Object.keys(allPatterns)
  .filter(k => Array.isArray(problemBank[k]) && problemBank[k].length > 0)
  .map(k => ({ slug: k, title: allPatterns[k].title, count: problemBank[k].length }))

const selected = ref(availablePatterns.length ? availablePatterns[0].slug : null)
const started = ref(false)

function startWith(slug) {
  selected.value = slug
  started.value = true
}
</script>

# Recognition drill

Three things determine your interview result on an algorithms question: whether you **recognize** the right pattern, whether you can **code** it under time pressure, and whether you can **debug** it when you make a small mistake. This page trains the first one in isolation — you see a problem statement with the pattern tag hidden, and you guess.

Why in isolation? Because when you work through a pattern's chapter, you already know what pattern it is. The recognition skill never gets exercised. On a cold interview question, the pattern tag is **always** hidden. Drill the skill under that condition.

## Pick a pattern to drill

Each drill is a batch of 10 problems with the pattern tag hidden. The drill reveals the correct pattern (and sub-variation) after each guess, scores you at the end, and remembers your result so you can see progress over time.

<div v-if="availablePatterns.length === 0" style="padding: 20px; background: var(--vp-c-bg-soft); border-radius: 8px;">
  <p>Pattern-level drills are populated as each chapter upgrade lands. For now, try the <a href="/mixed-drill">mixed drill</a> once a few chapters are live.</p>
</div>

<div v-else-if="!started" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; margin: 20px 0;">
  <button
    v-for="p in availablePatterns"
    :key="p.slug"
    type="button"
    style="padding: 12px 14px; background: var(--vp-c-bg-soft); border: 1px solid var(--vp-c-divider); border-radius: 8px; cursor: pointer; text-align: left; font-size: 0.9em; color: var(--vp-c-text-1);"
    @click="startWith(p.slug)"
  >
    <div style="font-weight: 700; margin-bottom: 2px;">{{ p.title }}</div>
    <div style="font-size: 0.78em; color: var(--vp-c-text-2);">{{ p.count }} problems available</div>
  </button>
</div>

<div v-if="started && selected" :key="selected">
  <RecognitionDrill :pattern="selected" :count="10" />
  <p style="margin-top: 12px;">
    <button type="button" @click="started = false" style="padding: 6px 12px; background: transparent; border: 1px solid var(--vp-c-divider); border-radius: 6px; cursor: pointer; font-size: 0.85em;">← Pick a different pattern</button>
    &nbsp;or try the <a href="/mixed-drill">mixed drill</a>.
  </p>
</div>

## How to read your score

- **8-10 correct** — recognition is strong for this pattern. The next bottleneck is implementation fluency; drill cold-solves from the chapter's problem list.
- **5-7 correct** — recognition is forming. Reread the chapter's **When to use** and **When NOT to use** sections, then retake the drill. Pay attention to the distractors; the problems you miss name the shapes you're confusing it with.
- **0-4 correct** — the pattern isn't landing. Reread the chapter's canonical walkthrough and work the sub-variation H3s before retrying.

## This drill does NOT measure

- Whether you can **implement** the pattern under pressure. That's a separate skill — see the chapter's **Blind-solve** blocks (click "Reveal canonical template" only after attempting).
- Whether you'd recognize the pattern inside a disguised problem (compiler bugs, platform limits, ambiguous requirements). Only full-length mock interviews measure that.
- Transfer across patterns under random order. For that, use the [mixed drill](/mixed-drill).

The point of this page is one specific skill: given a problem statement with no tags, name the pattern. Train it until the recognition is reflex.
