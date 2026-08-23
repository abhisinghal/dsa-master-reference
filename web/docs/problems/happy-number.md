# Fast &amp; Slow — Happy Number

*[↗ LeetCode: Happy Number](https://leetcode.com/problems/happy-number/)* · <span class="diff diff-e">Easy</span> · [pattern chapter →](/patterns/fast-slow)

<CompanyTags companies="Google, Amazon, Meta" />

A "happy number" transformation repeatedly replaces `n` by the sum of the squares of its digits. `n` is happy iff this sequence eventually reaches `1`. Return `true` if `n` is happy.

**Example 1** — `n = 19` → `true` (`1² + 9² = 82 → 8² + 2² = 68 → … → 1`)
**Example 2** — `n = 2` → `false` (enters a cycle `4 → 16 → 37 → …`)
**Example 3** — `n = 1` → `true`

**Constraints** — `1 ≤ n ≤ 2³¹ − 1`.


<Hints
  hint1="Two pointers moving at different speeds detect cycles without extra memory."
  hint2="Slow steps 1, Fast steps 2. If they ever meet, there’s a cycle. If Fast hits null, no cycle."
  hint3="For cycle entry (Floyd’s Tortoise): after meeting, reset one pointer to head; walk both at speed 1; meet at entry."
/>
---

<MarkSolved problem-slug="happy-number" /> <Bookmark problem-slug="happy-number" />

<InterviewTimer problem-slug="happy-number" />



## Approach 1 — Hash set of seen values

**Intuition.** Iterate transformation; if we revisit a value, we're in a cycle → not happy. If we hit 1, happy.



```java
boolean isHappyHash(int n) {
    Set<Integer> seen = new HashSet<>();
    while (n != 1 && seen.add(n)) n = next(n);
    return n == 1;
}
int next(int n) {
    int s = 0;
    while (n > 0) { int d = n % 10; s += d * d; n /= 10; }
    return s;
}
```



**Complexity** — Time **O(log n · k)** where k = # iterations (bounded — see below); Space **O(k)**.

---

## Approach 2 — Floyd's tortoise/hare

**Insight from hash.** The sequence is a functional graph — it must eventually cycle. Detect cycles with two pointers moving at different speeds. If `slow` ever equals `fast` at value `1`, happy; otherwise cycle.

**Why bounded.** For 32-bit ints, the max digit-square-sum is `9² · 10 = 810` — the sequence stays under a few hundred within a couple of steps.



```java
boolean isHappy(int n) {
    int slow = n, fast = n;
    do {
        slow = next(slow);
        fast = next(next(fast));
    } while (slow != fast);
    return slow == 1;
}
int next(int n) {
    int s = 0;
    while (n > 0) { int d = n % 10; s += d * d; n /= 10; }
    return s;
}
```



<CodeTrace
  title="Floyd — n=19"
  :values="['19','82','68','100','1']"
  :windowKeys="['slow','fast']"
  :cellWidth="34"
  :steps='[
    { pointers: { slow: 0, fast: 0 }, vars: { slowVal: 19, fastVal: 19 }, note: "start" },
    { pointers: { slow: 1, fast: 2 }, vars: { slowVal: 82, fastVal: 68 }, note: "slow next=82; fast next.next=68" },
    { pointers: { slow: 2, fast: 4 }, vars: { slowVal: 68, fastVal: 1 }, note: "fast reaches 1" },
    { pointers: { slow: 4, fast: 4 }, vars: { slowVal: 1, fastVal: 1 }, note: "slow catches up; both=1 → happy" }
  ]'
/>

**Complexity** — Time **O(log n · k)**; Space **O(1)**.

---

## Approach 3 — Known unhappy cycle short-circuit (interview trick)

**Insight from Floyd.** Every unhappy number's cycle contains `4`. Just check `n == 1 || n == 4`.



```java
boolean isHappyCycle(int n) {
    while (n != 1 && n != 4) n = next(n);
    return n == 1;
}
```



Small proof: iterate 1..810; every trajectory either reaches 1 or hits `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4`.

**Complexity** — Time **O(log n · k)**; Space **O(1)**.

---

## Try it yourself

<JavaRunner problem-slug="happy-number" />

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Hash set | O(log n · k) | O(k) | correct baseline |
| Floyd's cycle detection | **O(log n · k)** | **O(1)** | pattern-recognition win |
| "Contains 4" short-circuit | O(log n · k) | O(1) | trivia; skip in interview |

## When to use which

- **Interview** → Floyd's — teaches the pattern.
- **Production** → hash set is cleaner, memory bounded by ~250 states.
- **"Return the cycle values"** → hash-set version already records them.
- **Generalization** ("happy in base b") → Floyd's still applies; the "4" trick doesn't.

<AiCompanion problem-slug="happy-number" pattern-hint="fast/slow pointers" />

## Related problems

- [Linked List Cycle](/problems/linked-list-cycle) — same detection
- [Linked List Cycle II](/problems/fast-slow-linked-list-cycle-ii) — same on lists
- [Find the Duplicate Number](/problems/find-the-duplicate-number) — cycle on implicit function

<FeedbackWidget problem-slug="happy-number" />

<RelatedProblems problems="linked-list-cycle::Linked List Cycle|middle-of-the-linked-list::Middle Of The Linked List|find-the-duplicate-number::Find The Duplicate Number" />
