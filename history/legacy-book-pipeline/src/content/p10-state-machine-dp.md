## The Pattern

State-machine DP models each entity state explicitly and updates all states by legal transitions. Instead of asking "what was the last index?", ask "what condition am I in after processing this prefix?" The state names should be semantic: `hold`, `sold`, `rest`; `free`, `cooldown`; `matched`, `unmatched`; `inside`, `outside`.

!!! pattern "Recognition signals"
    **Signals:** actions have cooldowns, fees, mutually exclusive modes, "after doing X you cannot immediately do Y", or the best answer depends on what state the previous step ended in. If the rule reads like an automaton, make the automaton the DP.

```diagram
{"type":"recursion","nodes":[{"id":"rest","label":"rest\nnot holding","x":0,"y":0,"role":"primary"},{"id":"hold","label":"hold\nown stock","x":2.5,"y":0,"role":"amber"},{"id":"sold","label":"sold\ncooldown","x":5,"y":0,"role":"green"}],"edges":[{"from":"rest","to":"hold","label":"buy","color":"amber"},{"from":"hold","to":"sold","label":"sell","color":"green"},{"from":"sold","to":"rest","label":"cool down","color":"primary"},{"from":"rest","to":"rest","label":"skip","color":"muted"},{"from":"hold","to":"hold","label":"skip","color":"muted"}]}
```

## The Invariant

**STATE:** `dpState` is the best value after processing the current prefix and ending in that exact semantic state. For stock cooldown: `hold` = max profit while holding one share, `sold` = max profit if sold today, `rest` = max profit while not holding and not in today's sell state.

**TRANSITION:** every next-state value is the maximum over legal predecessor states plus the action delta. For cooldown: `nextHold = max(hold, rest - price)`, `nextSold = hold + price`, `nextRest = max(rest, sold)`.

**BASE CASE:** initialize only states that are reachable before reading input. For stock cooldown: `hold = -∞`, `sold = -∞`, `rest = 0`; after each price, compute next values from the previous day's snapshot.

## Template

```java
int maxProfitWithCooldown(int[] prices) {
    final int NEG = Integer.MIN_VALUE / 4;
    int hold = NEG;
    int sold = NEG;
    int rest = 0;

    for (int price : prices) {
        int prevHold = hold;
        int prevSold = sold;
        int prevRest = rest;

        hold = Math.max(prevHold, prevRest - price);
        sold = prevHold + price;
        rest = Math.max(prevRest, prevSold);
    }
    return Math.max(rest, sold);
}
```

## Worked Recognition

- **Best Time to Buy/Sell with Cooldown** (Module 12): the word "cooldown" is a state constraint, not a local greedy tweak. `sold` must transition to `rest` before another `buy`.
- **Best Time to Buy/Sell with Fee** (Module 12 family): use `hold` and `cash`; selling pays `price - fee`. The same state-machine frame removes ambiguity about when the fee is charged.
- **House Robber-style exclusion** (Module 12 family): `take` and `skip` are states over a prefix. The transition "take only after skip" is a two-state automaton.

## Complexity

!!! complexity "Complexity"
    **T:** O(n · s · d) conceptually for n positions, s states, and d incoming transitions per state; most interview machines have constant s and d, so O(n). **S:** O(s), usually O(1), by rolling one step because transitions depend only on the previous layer.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Updating states in place without saving the previous snapshot, allowing illegal transitions because the state definition is vague, initializing unreachable states to 0 instead of -∞, or returning a terminal state that still violates the problem (for stock, ending in `hold` is not realized profit).

## When NOT to use it

Do not force a state machine when the decision has no persistent mode. Plain prefix DP, greedy intervals, or graph shortest path may be clearer. If transitions depend on arbitrary history rather than a small finite state, enlarge the state carefully or switch patterns.
