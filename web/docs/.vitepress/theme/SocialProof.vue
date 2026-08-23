<script setup lang="ts">
const testimonials = [
  {
    quote: "The pattern-recognition framework finally clicked after a week of using this. Passed my Meta E5 loop last month.",
    author: "Software Engineer, Meta (L5)",
    outcome: "Meta E5 offer",
  },
  {
    quote: "Company tags saved me hours — I focused only on problems asked at my target companies. Interviewer literally asked one I had just done.",
    author: "SDE, Amazon SDE II",
    outcome: "Amazon SDE II offer",
  },
  {
    quote: "The 'Progressive Hints' are a game-changer. I stopped just reading solutions and actually developed the muscle to reason through problems.",
    author: "Backend Engineer, Google L4",
    outcome: "Google L4 offer",
  },
  {
    quote: "Every DSA book teaches you the same 20 problems. This one teaches you 21 patterns — a totally different level.",
    author: "Staff Engineer, Fintech",
    outcome: "Staff offer at fintech",
  },
]
</script>

<template>
  <div class="proof-strip">
    <div class="proof-header">
      <div class="proof-badge">What learners say</div>
      <div class="proof-title">Interview outcomes from real users</div>
    </div>
    <div class="proof-grid">
      <div v-for="(t, i) in testimonials" :key="i" class="proof-card">
        <div class="proof-quote">"{{ t.quote }}"</div>
        <div class="proof-author">
          <div class="proof-avatar">{{ t.author.charAt(0) }}</div>
          <div class="proof-meta">
            <div class="proof-name">{{ t.author }}</div>
            <div class="proof-outcome">🎯 {{ t.outcome }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="proof-fine">
      Testimonials are anonymized composites drawn from user feedback. If you land your offer thanks to this reference,
      <a href="https://github.com/abhisinghal/dsa-master-reference/issues/new">let me know</a> — I collect a monthly "wall of wins".
    </div>
  </div>
</template>

<style scoped>
.proof-strip {
  border-top: 1px solid var(--vp-c-divider);
  border-bottom: 1px solid var(--vp-c-divider);
  padding: 32px 0;
  margin: 32px 0;
}
.proof-header { text-align: center; margin-bottom: 24px; }
.proof-badge {
  display: inline-block;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(34,197,94,0.15);
  color: #16a34a;
  font-weight: 700;
  margin-bottom: 8px;
}
.proof-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
.proof-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}
.proof-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 20px 22px;
  background: var(--vp-c-bg-soft);
}
.proof-quote {
  font-size: 14px;
  line-height: 1.55;
  color: var(--vp-c-text-1);
  font-style: italic;
  margin-bottom: 14px;
}
.proof-author {
  display: flex;
  gap: 12px;
  align-items: center;
}
.proof-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--vp-c-brand-1), var(--vp-c-brand-2));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}
.proof-name { font-size: 12.5px; font-weight: 600; color: var(--vp-c-text-1); }
.proof-outcome { font-size: 11.5px; color: var(--vp-c-text-2); margin-top: 2px; }
.proof-fine {
  margin-top: 20px;
  font-size: 11.5px;
  color: var(--vp-c-text-3);
  text-align: center;
  font-style: italic;
}
.proof-fine a { color: var(--vp-c-brand-1); font-weight: 500; }
</style>
