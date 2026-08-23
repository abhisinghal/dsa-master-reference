<script setup>
import { ref, computed } from 'vue'

const weeks = ref(4)
const level = ref('senior')

const PLANS = {
  1: {
    intro: '1 week = crisis mode. Focus on top-40 patterns you already know 60%.',
    days: [
      { d: 'Day 1', tasks: ['Sliding Window (ch21)', 'Two Pointers (ch22)', '5 canonical problems from each'] },
      { d: 'Day 2', tasks: ['Binary Search + BS on Answer (ch27-28)', 'Hashing (ch25)', 'Practice: koko-bananas, two-sum, 3sum'] },
      { d: 'Day 3', tasks: ['Trees (ch60) + BFS/DFS traversals', 'Practice: level-order, LCA, subtree'] },
      { d: 'Day 4', tasks: ['Graphs + Topo Sort (ch66, ch33)', 'Practice: course-schedule, number-of-islands'] },
      { d: 'Day 5', tasks: ['DP essentials (ch38)', 'Practice: coin-change, LIS, LCS, edit-distance'] },
      { d: 'Day 6', tasks: ['Backtracking (ch36) + Heap (ch29)', 'Traps catalog full read'] },
      { d: 'Day 7', tasks: ['Mock interview × 2 timed', 'Review Interview Day Kit', 'Rest'] },
    ]
  },
  2: {
    intro: '2 weeks = intense but doable. Cover 15 patterns properly.',
    days: [
      { d: 'Week 1', tasks: ['Sliding Window, Two Pointers, Fast/Slow', 'Hashing, Prefix Sum, Binary Search', '~30 canonical problems'] },
      { d: 'Week 2', tasks: ['Trees, Graphs, BFS/DFS, Topo Sort', 'DP, Backtracking, Heap', '2 timed mock interviews', 'Traps catalog + Interview Day Kit'] },
    ]
  },
  4: {
    intro: '4 weeks = sprint. Recommended baseline: works for most senior interviews.',
    days: [
      { d: 'Week 1', tasks: ['Java foundations (ch06-10)', 'Sliding Window + Two Pointers + Hashing', 'One canonical per pattern'] },
      { d: 'Week 2', tasks: ['Binary Search + BS on Answer', 'Fast/Slow + Prefix Sum + Monotonic Stack', 'Heap + Top-K + K-way Merge'] },
      { d: 'Week 3', tasks: ['Trees + BSTs + Trie', 'Graphs + BFS + DFS + Topo + UF', 'Backtracking'] },
      { d: 'Week 4', tasks: ['DP (Grid + Sequence + Interval + Bitmask)', 'Design + Greedy + Divide & Conquer', 'Weekly mocks, traps catalog, day-of kit'] },
    ]
  },
  8: {
    intro: '8 weeks = marathon. Follows the built-in Roadmap chapter 1:1.',
    days: [
      { d: 'Weeks 1-2', tasks: ['Foundations + Arrays + Hashing + Prefix Sum', 'Follow ch03-Roadmap Week 1-2 exactly'] },
      { d: 'Weeks 3-4', tasks: ['Two Pointers + Fast/Slow + Binary Search', 'Stacks + Monotonic + SW Max'] },
      { d: 'Weeks 5-6', tasks: ['Heap + Top-K + K-way', 'Trees + BSTs + Trie'] },
      { d: 'Weeks 7-8', tasks: ['Graphs + BFS + DFS + Topo + UF', 'DP + Backtracking + Design + Mocks'] },
    ]
  },
  12: {
    intro: '12 weeks = luxury. Include system design + behavioral practice.',
    days: [
      { d: 'Weeks 1-4', tasks: ['All Part I foundations + first 10 patterns', 'Book\'s Roadmap chapter Weeks 1-4'] },
      { d: 'Weeks 5-8', tasks: ['Advanced patterns (DP variations, Graphs, Design)', 'System Design intro chapter'] },
      { d: 'Weeks 9-10', tasks: ['Company-specific tracks (Meta/Google/Amazon)', 'Mock interviews weekly'] },
      { d: 'Weeks 11-12', tasks: ['Behavioral prep', 'Traps catalog + Interview Day Kit', 'Rest before onsite'] },
    ]
  },
}

const plan = computed(() => PLANS[weeks.value] || PLANS[4])
</script>

<template>
  <div class="spg-panel">
    <div class="spg-head">
      <div class="spg-title">🗓️ Personalized study plan</div>
      <div class="spg-sub">Tell me your timeline and I'll generate a plan.</div>
    </div>
    <div class="spg-controls">
      <label>
        <span>Weeks until interview</span>
        <select v-model.number="weeks">
          <option :value="1">1 week (crisis)</option>
          <option :value="2">2 weeks</option>
          <option :value="4">4 weeks (recommended)</option>
          <option :value="8">8 weeks</option>
          <option :value="12">12 weeks</option>
        </select>
      </label>
      <label>
        <span>Target level</span>
        <select v-model="level">
          <option value="mid">Mid (L4)</option>
          <option value="senior">Senior (L5)</option>
          <option value="staff">Staff (L6+)</option>
        </select>
      </label>
    </div>
    <div class="spg-plan">
      <div class="spg-intro">{{ plan.intro }}</div>
      <ul class="spg-days">
        <li v-for="(day, idx) in plan.days" :key="idx" class="spg-day">
          <div class="spg-day-label">{{ day.d }}</div>
          <ul class="spg-tasks">
            <li v-for="task in day.tasks" :key="task">→ {{ task }}</li>
          </ul>
        </li>
      </ul>
    </div>
    <div class="spg-cta">
      <a href="/foundations/roadmap" class="spg-link">Open full Roadmap →</a>
    </div>
  </div>
</template>

<style scoped>
.spg-panel {
  margin: 1.5rem 0;
  padding: 20px 22px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.04), rgba(139, 92, 246, 0.04));
  border: 1px solid var(--vp-c-divider);
}
.spg-head { margin-bottom: 12px; }
.spg-title {
  font-weight: 700;
  font-size: 1.05em;
  color: var(--vp-c-brand-1);
}
.spg-sub {
  font-size: 0.85em;
  color: var(--vp-c-text-2);
  margin-top: 2px;
}
.spg-controls {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.spg-controls label {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.82em;
  color: var(--vp-c-text-2);
}
.spg-controls select {
  padding: 6px 10px;
  border-radius: 5px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.9em;
}
.spg-intro {
  font-size: 0.9em;
  color: var(--vp-c-text-1);
  padding: 10px 14px;
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  margin-bottom: 12px;
  font-weight: 500;
}
.spg-days {
  list-style: none;
  padding: 0;
  margin: 0;
}
.spg-day {
  padding: 10px 0;
  border-top: 1px solid var(--vp-c-divider);
}
.spg-day:first-child { border-top: none; }
.spg-day-label {
  font-weight: 700;
  font-size: 0.9em;
  color: var(--vp-c-brand-1);
  margin-bottom: 4px;
}
.spg-tasks {
  list-style: none;
  padding: 0;
  margin: 0;
}
.spg-tasks li {
  font-size: 0.86em;
  color: var(--vp-c-text-2);
  padding: 2px 0;
}
.spg-cta {
  text-align: right;
  margin-top: 12px;
}
.spg-link {
  font-size: 0.88em;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  text-decoration: none;
}
.spg-link:hover { text-decoration: underline; }
</style>
