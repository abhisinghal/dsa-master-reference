<script setup lang="ts">
/**
 * GreedyAnim.vue — user-driven diagram for Coin Change greedy vs. optimal.
 *
 * UX: user picks:
 *   - denominations (a small preset list of coin sets)
 *   - target amount (slider)
 * Component shows:
 *   - greedy trace (largest coin first) — running amount + coin count
 *   - optimal trace via DP
 *   - flags counter-example when greedy fails (e.g. [1,3,4] target 6: greedy=4+1+1=3, optimal=3+3=2)
 */
import { computed, ref } from 'vue'

interface CoinSet { label: string; coins: number[]; note: string }

const coinSets: CoinSet[] = [
  { label: 'US coins (canonical greedy)', coins: [25, 10, 5, 1], note: 'Greedy is optimal here.' },
  { label: '[1, 3, 4] — famous counter-example', coins: [4, 3, 1], note: 'Greedy fails: target 6 → 4+1+1 = 3 coins, optimal is 3+3 = 2 coins.' },
  { label: 'European (1, 2, 5, 10, 20, 50)', coins: [50, 20, 10, 5, 2, 1], note: 'Greedy is optimal here.' },
  { label: '[1, 5, 6, 9]', coins: [9, 6, 5, 1], note: 'Try target 11: greedy=9+1+1=3, optimal=6+5=2.' }
]

const chosenSet = ref(1) // start on the counter-example
const target = ref(6)
const coins = computed(() => coinSets[chosenSet.value].coins) // sorted desc

// Greedy trace
interface GreedyStep { coin: number; used: number; remaining: number }
const greedyTrace = computed<GreedyStep[]>(() => {
  const trace: GreedyStep[] = []
  let remaining = target.value
  for (const c of coins.value) {
    if (c > remaining) continue
    const used = Math.floor(remaining / c)
    if (used === 0) continue
    remaining -= used * c
    trace.push({ coin: c, used, remaining })
    if (remaining === 0) break
  }
  return trace
})
const greedyCount = computed(() => greedyTrace.value.reduce((s, t) => s + t.used, 0))
const greedyReached = computed(() => greedyTrace.value.length === 0 ? target.value === 0 : greedyTrace.value[greedyTrace.value.length - 1].remaining === 0)

// Optimal DP: fewest coins to reach `target`
const optimal = computed(() => {
  const T = target.value
  const dp = new Array(T + 1).fill(Infinity)
  const parent = new Array(T + 1).fill(-1)
  dp[0] = 0
  for (let a = 1; a <= T; a++) {
    for (const c of coins.value) {
      if (c <= a && dp[a - c] + 1 < dp[a]) {
        dp[a] = dp[a - c] + 1
        parent[a] = c
      }
    }
  }
  const path: number[] = []
  if (dp[T] !== Infinity) {
    let cur = T
    while (cur > 0) {
      const c = parent[cur]
      path.push(c)
      cur -= c
    }
  }
  path.sort((a, b) => b - a)
  return { count: dp[T] === Infinity ? -1 : dp[T], path }
})

const greedyMatchesOptimal = computed(() =>
  greedyReached.value && optimal.value.count >= 0 && greedyCount.value === optimal.value.count
)

const failedThisAmount = computed(() =>
  greedyReached.value && optimal.value.count >= 0 && greedyCount.value > optimal.value.count
)

// Layout: coins bar chart across the diagram
const svgW = 720
const svgH = 320
const maxCoinDenom = computed(() => Math.max(...coins.value))
</script>

<template>
  <div class="anim-card">
    <div class="anim-head">
      <h4 class="anim-title">Greedy Coin Change — when it works, and when it doesn't</h4>
      <p class="anim-hint">
        Greedy = "always take the biggest coin that fits." Sometimes optimal, sometimes not.
        Pick a coin set and target; watch greedy trace vs. the DP-optimal answer.
      </p>
    </div>

    <svg
      class="anim-svg"
      :width="svgW"
      :height="svgH"
      :viewBox="`0 0 ${svgW} ${svgH}`"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="Greedy vs optimal coin change trace"
    >
      <!-- Target header -->
      <text x="30" y="30" font-size="14" font-weight="700" fill="#0f172a">
        Target: {{ target }}
      </text>
      <text x="30" y="50" font-size="12" fill="#64748b">Coin set: [{{ coins.join(', ') }}]</text>

      <!-- Greedy trace -->
      <g transform="translate(0, 70)">
        <text x="30" y="15" font-size="12" font-weight="700" :fill="failedThisAmount ? '#dc2626' : '#16a34a'">
          Greedy trace ({{ greedyReached ? greedyCount + ' coins' : 'failed to reach ' + target }})
        </text>
        <g v-for="(step, i) in greedyTrace" :key="'g' + i" :transform="`translate(${30 + i * 140}, 30)`">
          <rect width="120" height="60" rx="7" :class="['coin-box', { 'wasteful': failedThisAmount && i >= optimal.count }]" />
          <text x="60" y="24" text-anchor="middle" font-size="11" fill="#64748b">
            take {{ step.used }} × {{ step.coin }}
          </text>
          <text x="60" y="44" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">
            remaining {{ step.remaining }}
          </text>
        </g>
      </g>

      <!-- Optimal comparison -->
      <g transform="translate(0, 200)">
        <text x="30" y="15" font-size="12" font-weight="700" fill="#7c3aed">
          Optimal ({{ optimal.count === -1 ? 'impossible' : optimal.count + ' coins' }})
        </text>
        <g v-if="optimal.count > 0" v-for="(c, i) in optimal.path" :key="'o' + i" :transform="`translate(${30 + i * 65}, 30)`">
          <rect width="55" height="55" rx="10" class="coin-optimal" />
          <text x="27.5" y="35" text-anchor="middle" font-size="16" font-weight="700" fill="white">{{ c }}</text>
        </g>
        <text v-if="optimal.count === -1" x="40" y="45" font-size="13" fill="#dc2626" font-weight="600">
          Target {{ target }} cannot be formed with these coins.
        </text>
      </g>

      <!-- Verdict banner -->
      <g v-if="failedThisAmount" transform="translate(0, 290)">
        <rect x="20" y="0" :width="svgW - 40" height="24" rx="5" fill="#fee2e2" stroke="#dc2626" stroke-width="1.2" />
        <text :x="svgW / 2" y="17" text-anchor="middle" font-size="12" font-weight="700" fill="#991b1b">
          ⚠ Greedy suboptimal here — uses {{ greedyCount }} coins vs. optimal {{ optimal.count }}.
        </text>
      </g>
      <g v-else-if="greedyMatchesOptimal && optimal.count > 0" transform="translate(0, 290)">
        <rect x="20" y="0" :width="svgW - 40" height="24" rx="5" fill="#dcfce7" stroke="#16a34a" stroke-width="1.2" />
        <text :x="svgW / 2" y="17" text-anchor="middle" font-size="12" font-weight="700" fill="#166534">
          ✓ Greedy is optimal here ({{ greedyCount }} = {{ optimal.count }} coins).
        </text>
      </g>
    </svg>

    <div class="controls">
      <label class="coin-picker">
        Coin set:
        <select v-model.number="chosenSet">
          <option v-for="(s, i) in coinSets" :key="i" :value="i">{{ s.label }}</option>
        </select>
      </label>
      <label class="target-picker">
        Target: <b>{{ target }}</b>
        <input type="range" min="1" max="30" v-model.number="target" />
      </label>
    </div>

    <div class="live" aria-live="polite">
      {{ coinSets[chosenSet].note }}
    </div>
  </div>
</template>

<style scoped>
.anim-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 16px;
  margin: 20px 0;
}
.anim-head { margin-bottom: 12px; }
.anim-title { margin: 0 0 4px; font-size: 15px; font-weight: 700; color: var(--vp-c-text-1); }
.anim-hint { margin: 0; font-size: 13px; color: var(--vp-c-text-2); }

.anim-svg { display: block; width: 100%; height: auto; max-width: 720px; margin: 8px auto; }

.coin-box { fill: #dbeafe; stroke: #2563eb; stroke-width: 1.6; }
.coin-box.wasteful { fill: #fee2e2; stroke: #dc2626; stroke-width: 1.8; }
.coin-optimal { fill: #7c3aed; stroke: #6d28d9; stroke-width: 1.6; }

.controls {
  display: flex;
  gap: 20px;
  align-items: center;
  margin-top: 10px;
  flex-wrap: wrap;
}
.coin-picker, .target-picker {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 13px;
  color: var(--vp-c-text-2);
}
.coin-picker select {
  padding: 4px 8px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 5px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 13px;
}
.target-picker input[type="range"] { width: 200px; accent-color: #2563eb; }

.live {
  margin-top: 8px;
  font-size: 12px;
  color: var(--vp-c-text-3);
  text-align: center;
  padding: 6px;
  background: var(--vp-c-bg);
  border-radius: 6px;
  font-style: italic;
}

@media print { .controls, .live { display: none; } }
</style>
