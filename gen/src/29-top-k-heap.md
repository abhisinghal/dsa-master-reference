# Top-K / Heap

## Why top-k heaps exist — the story

Imagine you are watching a live scoreboard with millions of scores, but the product manager only cares about the top 10. Sorting every score every time would be silly: rank 11 through rank 1,000,000 do not matter. The Top-K heap pattern exists because you can keep a tiny "VIP room" of size `k` instead of arranging the whole crowd. Every new candidate enters the room briefly; if the room is too full, you kick out the worst person currently inside. At the end, the room contains exactly the best `k` candidates.

<HeapAnim />

Use a concrete example: find the 3 largest numbers in `[7, 1, 9, 3, 10, 2, 8]`. Keep a min-heap of size 3. Read `7,1,9` → heap has `{1,7,9}`. Read `3` → heap becomes `{1,3,7,9}`, too large, so remove the smallest `1`; room is `{3,7,9}`. Read `10` → remove `3`; room is `{7,9,10}`. Read `2` → remove `2` immediately. Read `8` → remove `7`; final room is `{8,9,10}`. Notice the heap root is not the answer to "largest"; it is the weakest of the winners, the one easiest to evict.

The brute-force walk-through is full sorting: arrange everyone, then take the first `k`. Can we do better? Yes, because the exact order of the rejected `n-k` items does not matter. Keep only the current boundary set.

That opposite-polarity idea is the whole trick. For k largest, use a min-heap. For k smallest, use a max-heap. For k most frequent, use a min-heap ordered by frequency. The heap is not there to sort everything; it is there to maintain a moving boundary between "still in the top k" and "not good enough."

> [key] **Key Insight** — For k *largest*, use a **min**-heap (its root is the worst-of-the-best, cheap to evict). For k *smallest*, use a **max**-heap. Polarity is always the opposite of the goal.

## When to use it — boundary items without sorting

Top-K heap is the interview pattern for "I need a small elite set from a large input." It is especially strong when `k` is much smaller than `n`, when the input is streaming, or when the final order of the selected items does not matter.

### Recognize by
- "k largest", "k smallest", "top k", "bottom k"
- "k most frequent", "k least frequent", "most common words"
- "k closest to origin" or "nearest k elements" where the ranking key is computed from each item
- "kth largest in a stream" where values arrive over time and you must answer after each add
- "return any order" or "relative order among the top k does not matter"
- constraints like `n = 10^5` and `k` small enough that O(n log k) is attractive

### When NOT to use it
You need the k-th value **once** and don't care about the other k−1 boundary items. **Quickselect** is O(n) average and beats the heap's O(n log k). Use a heap when the input arrives as a **stream** (you can't Quickselect it) or when you need *all* k boundary items.

Also avoid a heap when you need the complete sorted order of all values; then sorting is simpler and honest. If the key range is tiny or bounded, bucket sort can beat the heap: for frequencies from 0 to n, buckets often give O(n). If `k` is close to `n`, O(n log k) becomes close to O(n log n), so the benefit shrinks.

## How to use it — template

```java
PriorityQueue<Item> heap = new PriorityQueue<>((a, b) -> compareWorstFirst(a, b));
for (Item item : items) {
    heap.offer(item);
    if (heap.size() > k) {
        heap.poll();        // remove the worst of the kept items
    }
}
List<Item> answer = new ArrayList<>();
while (!heap.isEmpty()) {
    answer.add(heap.poll());
}
return answer;
```

Fill in `compareWorstFirst` based on what "worst among the winners" means. For k largest, the smallest value is worst, so Java's default min-heap works. For k smallest, the largest value is worst, so reverse the comparator. For k most frequent, the lowest frequency is worst, so order by `freq.get(x)`. The loop invariant is simple: after processing any prefix of the input, the heap contains the best `k` items from that prefix, or all items if fewer than `k` have appeared.

---

## Kth Largest / Top K Frequent <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/)*

<ProgressCheck id="kth-largest-top-k-frequent" />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg" font-family="var(--dsa-font)">
  <defs>
    <marker id="ar-topk-success" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/>
    </marker>
    <marker id="ar-topk-danger" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-danger)"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="28" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-primary)">keep only the current top k boundary</text>

  <rect x="31" y="92" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/>
  <text x="53" y="120" text-anchor="middle" font-size="17" font-weight="700" fill="var(--dsa-ink)">12</text>
  <text x="53" y="153" text-anchor="middle" font-size="11.5" fill="var(--dsa-success)">incoming</text>
  <line x1="80" y1="114" x2="137" y2="114" stroke="var(--dsa-success)" stroke-width="2" marker-end="url(#ar-topk-success)"/>
  <text x="105" y="101" text-anchor="middle" font-size="11" font-weight="700" fill="var(--dsa-success)">larger</text>

  <line x1="200" y1="95" x2="164" y2="138" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <line x1="200" y1="95" x2="236" y2="138" stroke="var(--dsa-neutral)" stroke-width="2"/>
  <circle cx="200" cy="76" r="22" fill="var(--dsa-danger-soft)" stroke="var(--dsa-danger)" stroke-width="1.6"/>
  <circle cx="158" cy="158" r="22" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <circle cx="242" cy="158" r="22" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/>
  <g text-anchor="middle" font-size="17" font-weight="700" fill="var(--dsa-ink)">
    <text x="200" y="82">5</text><text x="158" y="164">8</text><text x="242" y="164">10</text>
  </g>
  <text x="200" y="42" text-anchor="middle" font-size="12" font-weight="700" fill="var(--dsa-danger)">root = smallest kept</text>
  <path d="M200 104 C206 121, 220 124, 258 105" fill="none" stroke="var(--dsa-danger)" stroke-width="2" marker-end="url(#ar-topk-danger)"/>
  <text x="294" y="108" font-size="11.5" font-weight="700" fill="var(--dsa-danger)">evict root</text>
  <text x="200" y="210" text-anchor="middle" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">size-k min-heap keeps k largest at O(n log k)</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> The heap stores only k candidates; its root is the weakest kept item, so a stronger incoming value replaces it and everything smaller can be ignored.</div>

### Problem
Return the **k most frequent** elements of an array (or, in the sibling, the kth largest). The order among the top-k doesn't matter.

**Constraints:** `1 ≤ n ≤ 10⁵`; `1 ≤ k ≤ #distinct`; beat a full O(n log n) sort.

**Example 1:** `nums = [1,1,1,2,2,3], k = 2` → `[1,2]`.

**Example 2:** `nums = [1], k = 1` → `[1]`.

### Solution — brute force
First count frequencies. The brute-force way is then to sort all distinct values by decreasing frequency and take the first `k`.

```text
freq = count each number
items = all distinct numbers
sort items by freq descending
return first k items
```

```java
int[] topKFrequentBrute(int[] nums, int k) {
    Map<Integer,Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    List<Integer> keys = new ArrayList<>(freq.keySet());
    keys.sort((a, b) -> freq.get(b) - freq.get(a));
    int[] res = new int[k];
    for (int i = 0; i < k; i++) res[i] = keys.get(i);
    return res;
}
```

This is perfectly acceptable as a baseline: O(n) to count, O(m log m) to sort `m` distinct values, and O(m) space. It becomes wasteful when `m` is large and `k` is small, because sorting rank 5000 versus rank 5001 does not help you return the top 10. The heap version avoids fully ordering the losers.

O(n + m log m) time, O(m) space, where `m` is the number of distinct values — wasteful when k is tiny.

### Solution — optimized
Size-k min-heap; evict the smallest whenever the heap exceeds k.

The heap stores distinct numbers, not array indices and not `(number, frequency)` pairs. The comparator looks up each number's count in the frequency map. Because this is a min-heap by frequency, `poll()` removes the least frequent number among the currently kept candidates. After all distinct values have been processed, only the k most frequent can survive.

> [inv] **Invariant** — After each key from `freq.keySet()` is processed, `pq` contains the k highest-frequency keys seen so far. If more than k keys have been offered, the lowest-frequency survivor has already been evicted.

The optimized Java counts once, then keeps a heap of only `k` surviving keys. The root is deliberately the weakest survivor, so overflow beyond size `k` evicts the least useful candidate immediately.

```java
int[] topKFrequent(int[] nums, int k) {
    Map<Integer,Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    PriorityQueue<Integer> pq =                    // min-heap by frequency
        new PriorityQueue<>((a, b) -> freq.get(a) - freq.get(b));
    for (int key : freq.keySet()) {
        pq.offer(key);
        if (pq.size() > k) pq.poll();              // drop least frequent
    }
    int[] res = new int[k];
    for (int i = k - 1; i >= 0; i--) res[i] = pq.poll();
    return res;
}
```

> [note] **Trace it** — `nums=[1,1,1,2,2,3], k=2`.

<CodeTrace
  title="Top K Frequent — nums=[1,1,1,2,2,3], k=2"
  :values="[1,1,1,2,2,3]"
  :windowKeys="['i']"
  :cellWidth="38"
  :steps='[
    { pointers: { i: 5 }, vars: { freq: "{1:3, 2:2, 3:1}", heap: "[]" }, note: "count all frequencies" },
    { pointers: { i: 0 }, vars: { heap: "[(3,1)]" }, note: "push 1 (freq 3)" },
    { pointers: { i: 0 }, vars: { heap: "[(2,2),(3,1)]" }, note: "push 2 (freq 2). heap size = k=2" },
    { pointers: { i: 0 }, vars: { heap: "[(2,2),(3,1)]" }, note: "3 has freq 1 lt min(2) → skip. result [1,2]", added: [0,3] }
  ]'
/>
### Time Complexity
O(n + m log k), often written O(n log k) when `m ≤ n`. Counting scans all n values, and each of the `m` distinct keys costs O(log k) in the heap.

### Space Complexity
O(n), because the frequency map may store all n values when every value is distinct; the heap itself stores only O(k).

More precisely, counting costs O(n), and heap operations cost O(m log k), where `m` is the number of distinct values. The frequency map can hold up to O(n) entries. The heap itself holds O(k) entries, but the total auxiliary space is still O(n) because of the map.

> [trap] **Common Trap** — Wrong heap polarity. *Example:* the *k-th largest* with a **max**-heap of all n elements costs O(n log n) — wasteful. A **min**-heap of size k evicts the smallest; the root is your answer in O(n log k).

<CodeTrace
  title="Trap — Heap polarity: k-th largest of nums=[3,1,5,2,4], k=2"
  :values="[3,1,5,2,4]"
  :windowKeys="['i']"
  :cellWidth="46"
  :steps='[
    { pointers: { i: 4 }, vars: { max_heap: "[5,4,3,2,1]", cost: "O(n log n)" }, note: "BUG: max-heap of all 5 → build + pop 2 for 2nd largest = 4. wasteful" },
    { pointers: { i: 4 }, vars: { min_heap: "[4,5]", size: 2, cost: "O(n log k)" }, note: "FIX: min-heap capped at k=2. root=4 = 2nd largest", added: [4] }
  ]'
/>

> [note] **Interview script** — First, I'd count each number because frequency is the ranking key. The brute force is to sort all distinct numbers by frequency and take the first k, which is O(n + m log m). Since we only need k winners, I'll keep a min-heap of size k ordered by frequency and evict the least frequent whenever the heap grows too large. That gives O(n + m log k) time and O(n) space, and the output order can be arbitrary because the problem allows it.

> [pat] **Pattern Connection** — *K Closest Points to Origin* is identical with a max-heap of size k keyed on distance; bucket sort by frequency gives O(n) when the key range is bounded.

### Learning notes
- Why count first? — frequency is the ranking key, so the heap cannot compare numbers until counts exist.
- Why store just the key in the heap? — the `freq` map already holds the count; duplicating pairs is unnecessary here.
- Why a **min-heap** for "most frequent"? — the least frequent survivor is the next one to evict.
- Why `if (pq.size() > k) pq.poll()`? — allowing one temporary extra item lets each candidate compete before eviction.
- Why fill `res` from right to left? — repeated `poll()` returns lower-frequency survivors first.
- Why not sort all keys? — sorting orders every loser too; the heap only maintains the top-k boundary.
- Why mention `Integer.compare`? — subtraction comparators can overflow when values or counts are extreme.

#### Choosing between heap, sort, bucket, and quickselect
A useful interview move is to name the trade-off instead of pretending the heap is always best. Full sorting is shortest to code and good when `n` is small or when the final order matters. A size-k heap is best when k is small, the stream may not fit in memory, or you need to update answers incrementally. Bucket sort is excellent for frequencies because frequency is an integer from 1 to n; create buckets where bucket `f` stores all values with frequency `f`, then read from high frequency down until k values are collected. Quickselect is attractive for one-shot selection when you can mutate the array of candidates and do not need streaming behavior.

For Top K Frequent specifically, the heap solution is a reliable general answer because it does not depend on a small value range and is easy to adapt to words, points, pairs, or custom objects. If the interviewer asks for strict O(n), discuss buckets after presenting the heap.

#### Comparator details in Java
Java's `PriorityQueue` is a min-heap according to the comparator. That means the "smallest" item by comparator comes out first. For top-k largest, you intentionally define "smallest" as the item you are most willing to discard. In the existing code, `(a, b) -> freq.get(a) - freq.get(b)` puts lower-frequency numbers first.

In production code, `Integer.compare(freq.get(a), freq.get(b))` avoids overflow. The chapter keeps the compile-tested solution unchanged, but in an interview you can mention `Integer.compare` if counts or values can be extreme. For tie-breaking, add a secondary comparison only if the problem requires deterministic ordering; otherwise, extra tie logic is unnecessary.

#### Heap polarity exercises

When you are under interview pressure, decide heap polarity with one sentence: **the root should be the next thing I would throw away.** If you want k largest numbers, the smallest kept number is the next thing to throw away, so the root must be small: min-heap. If you want k smallest numbers, the largest kept number is the next thing to throw away, so the root must be large: max-heap. If you want k closest points, the farthest kept point is the next thing to throw away, so use a max-heap by distance. If you want k most frequent words, the least frequent kept word is the next thing to throw away, so use a min-heap by frequency.

Try this quick table before coding:

| Goal | Worst survivor | Heap at root |
|---|---|---|
| k largest values | smallest value among the kept k | min-heap |
| k smallest values | largest value among the kept k | max-heap |
| k closest points | largest distance among the kept k | max-heap |
| k most frequent | smallest frequency among the kept k | min-heap |
| k least frequent | largest frequency among the kept k | max-heap |

This table prevents the most common reversal bug. The heap is not a trophy case where the best item sits on top. It is a door guard; the root is the easiest item to remove when a better candidate arrives.

#### Streaming vs batch thinking

Top-K heap is the natural streaming answer because it never needs to see the future. After processing the first 100 numbers, the heap already contains the top k among those 100. After the 101st number, one `offer` and maybe one `poll` restores the same invariant. That is why *Kth Largest Element in a Stream* stores the heap as object state and returns `pq.peek()` after each `add`.

Quickselect cannot do that. Quickselect needs a closed array to partition; when a new number arrives, the previous partition work may no longer line up with the new rank. If an interviewer asks, \"What if numbers arrive continuously?\" switch from Quickselect to heap immediately. If they ask, \"What if this is one offline query and k is large?\" Quickselect becomes attractive.

#### Tie handling and output order

Many top-k problems say \"return the answer in any order.\" That permission matters. The heap output order is usually from worst survivor to best survivor because repeated `poll()` removes the comparator-minimum. The existing solution fills the result from right to left so higher-frequency values tend to appear earlier, but the LeetCode problem does not require a sorted top-k list.

If a problem requires deterministic ties, bake the tie-breaker into the comparator. For words, you might sort by frequency ascending but reverse lexicographic order for the min-heap so that the lexicographically worse word is evicted first. For points, equal distances might not need tie-breaking at all. Never add tie rules that the prompt does not ask for; they make comparators harder to reason about and can accidentally evict the wrong item.

#### Testing checklist

Run these small cases mentally before trusting the code:

| Case | Expected lesson |
|---|---|
| `nums=[1], k=1` | heap and result handle the smallest input |
| `nums=[1,2,3], k=3` | no distinct key should be evicted permanently |
| `nums=[1,1,2,2], k=1` | ties are acceptable unless prompt specifies order |
| `nums=[1,1,1,2,3], k=2` | a low-frequency late key should be offered then immediately evicted |
| all values distinct | any k values are valid for top-k frequent because all frequencies tie |

### Same pattern, new tweaks

"Keep only the best `k` in a size-`k` heap of the opposite polarity" transfers straight across:

| Variation | The one thing that changes | Time |
|---|---|---|
| [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | a **max**-heap of size k keyed on squared distance; the farthest current winner is easiest to evict | O(n log k) |
| [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | heap keyed on frequency, or bucket by frequency for O(n) when you want the linear variant | O(n log k) |
| [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | treat each row as a sorted stream and use a min-heap for k-way merge | O(k log n) |
| [Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | keep a size-k **min**-heap alive across `add` calls; root is always the running kth largest | O(log k) per add |
| [Reorganize String](https://leetcode.com/problems/reorganize-string/) | use a max-heap because you repeatedly need the currently most frequent remaining character, not a bounded top-k set | O(n log alphabet) |

---

## Check your understanding

<Quiz patternId="top-k-heap" :questions='[
  {
    "q": "For the k-th largest element in a stream, which heap should be maintained?",
    "choices": [
      {
        "text": "Size-k min heap",
        "correct": true,
        "explanation": "Yes. The root is the worst of the best k values, so it is the running k-th largest."
      },
      {
        "text": "Size-k max heap"
      },
      {
        "text": "Heap containing all values"
      },
      {
        "text": "No heap, only sorting"
      }
    ]
  },
  {
    "q": "What is the usual time and space for scanning n values with a size-k heap?",
    "choices": [
      {
        "text": "O(n log k) time, O(k) space",
        "correct": true,
        "explanation": "Correct. Each candidate costs a heap operation bounded by k."
      },
      {
        "text": "O(n squared) time, O(1) space"
      },
      {
        "text": "O(log n) time, O(n) space"
      },
      {
        "text": "O(k log n) time, O(n) space"
      }
    ]
  },
  {
    "q": "When is bounded top-k heap usually not the best final step?",
    "choices": [
      {
        "text": "k is much smaller than n"
      },
      {
        "text": "Only the threshold value matters"
      },
      {
        "text": "You need the entire output globally sorted",
        "correct": true,
        "explanation": "Right. A bounded heap selects candidates; it does not directly produce a fully sorted list."
      },
      {
        "text": "The stream arrives online"
      }
    ]
  }
]' />
