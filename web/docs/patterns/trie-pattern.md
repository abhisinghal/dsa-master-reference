# Trie (pattern)


&lt;PatternVideo pattern-name="Trie" duration="8–12 min" /&gt;
&lt;PatternProgress pattern-id="trie" problems="word-search-ii, design-add-and-search-words-data-structure, replace-words, concatenated-words, stream-of-characters, maximum-xor-with-an-element-from-array, count-pairs-with-xor-in-a-range, maximum-genetic-difference-query" /&gt;



**Grokking arc:** The motivating problem is repeated prefix checking against many words or many bit strings. Brute force scans every candidate. **Can we do better?** Share prefixes in a trie so each next character or bit decides whether a whole branch remains possible.

## Why trie patterns exist — the story

A normal string search treats every word like a stranger. If your dictionary is `cat`, `car`, `cart`, and `dog`, and you ask whether the grid path `c → a → r → ...` can become a word, a brute-force checker may compare that prefix against every dictionary entry again and again. A trie changes the conversation: all words that start with `ca` share one hallway, so walking `c`, then `a`, answers "does any target still remain possible?" in O(1) per letter. The moment the hallway ends, you stop exploring.

That shared-prefix idea is why trie questions often pair with another technique. In **Word Search II**, the trie is the dictionary brain and backtracking is the board explorer. The DFS does not ask, "Is this complete path one of 30,000 words?" after every move. It asks, "Does this next letter exist from my current trie node?" If not, the entire branch dies immediately. For board paths like `o → a → x`, and a dictionary containing `oath` but no word beginning `oax`, the trie saves you from exploring every continuation under `x`.

The same idea works when the alphabet is not letters but bits. For maximum XOR, insert numbers as 32-bit paths. Query `5` (`00101` in a tiny 5-bit story) against `3,10,25`: at the highest bit, XOR wants the opposite bit because `1` beats `0` in that position. If the query bit is `0`, prefer a stored `1`; if the query bit is `1`, prefer a stored `0`. With `5` and `25` (`11001`), those opposite choices produce `11100` = 28. You did not compare `5` against every number one by one; the binary trie let you greedily choose the best available partner bit-by-bit in O(32).

The *pattern* chapter is about those applications. For the mechanics of a trie node, `insert`, `search`, and `startsWith`, see the [Trie deep-dive](/data-structures/trie) in Part III.

<Callout kind="key" title="Key Insight">

A trie turns many repeated prefix checks into one shared walk. A binary trie does the same thing for bits: build once, then each query makes 32 greedy choices instead of scanning all prior numbers.

</Callout>

<TrieWalkAnim />

### Recognize by
- *prefix queries against a shared dictionary* — "starts with," "autocomplete," "replace by root," "dictionary path"
- *many target strings tested against the same search space* — especially grid DFS plus a word list
- *XOR-max* wording — "maximum XOR pair," "best XOR under a limit," "count pairs with XOR in range"
- *wildcard or streaming suffix checks* — store words reversed when the query arrives from the end
- *longest/shortest prefix match* — routing tables, root replacement, command dictionaries

### When NOT to use it
- The dictionary is tiny and the strings are short; a linear scan may be clearer and fast enough.
- You need arbitrary substring or suffix search without reversing/preprocessing; tries are prefix-first.
- You only perform one lookup; building the trie may cost more than the lookup it saves.
- Your alphabet is huge and sparse without many shared prefixes; a hash set of full strings may be simpler.
- You need sorted order of complete words more than prefix pruning; a sorted array plus binary search can be enough.

## How to use it — binary-trie template for max-XOR

Use a binary trie when each element is a fixed-width bit string. Java `int` problems usually walk bits `31` down to `0`; if values are guaranteed non-negative under `2^31`, you can still keep 31 or 32 levels and the code stays simple.



```java
class BitNode { BitNode[] child = new BitNode[2]; }

void insert(BitNode root, int x) {
    BitNode cur = root;
    for (int b = 31; b >= 0; b--) {
        int bit = (x >>> b) & 1;
        if (cur.child[bit] == null) cur.child[bit] = new BitNode();
        cur = cur.child[bit];
    }
}

int bestXorAgainst(BitNode root, int x) {
    BitNode cur = root;
    int ans = 0;
    for (int b = 31; b >= 0; b--) {
        int bit = (x >>> b) & 1;
        int want = bit ^ 1;
        if (cur.child[want] != null) {
            ans |= 1 << b;
            cur = cur.child[want];
        } else {
            cur = cur.child[bit];
        }
    }
    return ans;
}
```



<Callout kind="inv" title="Greedy bit invariant">

once you decide a higher XOR bit can be `1`, no later lower bit can compensate for losing it. That is why the MSB-first opposite-bit walk is safe.

</Callout>

## When to use it — trie pattern flavors

| Flavor | Recognizer phrasing | What the trie contributes |
|---|---|---|
| Dictionary-pruned DFS | "find all words on a board", "many target strings" | kills paths as soon as their prefix is absent |
| Shortest/longest prefix | "replace by root", "routing prefix", "autocomplete" | walks one path and stops at the first or deepest useful terminal |
| Wildcard branching | "`?` / `.` can match any letter" | branches only at wildcard positions instead of scanning every word |
| Binary XOR trie | "maximum XOR", "XOR under limit", "count XOR pairs" | chooses opposite bits greedily from most significant to least |
| Streaming suffix query | "does the stream end with any word?" | store reversed words, then walk the recent stream backward |

The important interview move is to name the alphabet. Letter tries branch over characters. Binary tries branch over `0/1` bits. Reversed tries branch over the query from the end. Once you say that out loud, the code becomes a normal walk with a different interpretation of "next edge."

---

## Word Search II (Trie + Backtracking) <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Word Search II](https://leetcode.com/problems/word-search-ii/)*

<ProgressCheck id="word-search-ii-trie-backtracking" />





<div class="svg-figure">
<svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 720 260" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="720" height="260" rx="12" fill="var(--dsa-bg)"/>
  <text x="360" y="24" text-anchor="middle" font-family="var(--dsa-font)" font-size="13" font-weight="700" fill="var(--dsa-primary)">Trie of {"cat","car","cop"} + DFS on grid emits "car"</text>
  <g font-family="var(--dsa-font)" text-anchor="middle" font-size="14" font-weight="700" fill="var(--dsa-ink)">
    <circle cx="120" cy="70" r="16" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="120" y="75" font-size="11" fill="var(--dsa-neutral)">root</text>
    <circle cx="120" cy="125" r="16" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="120" y="130">c</text>
    <circle cx="80" cy="175" r="16" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="80" y="180">a</text>
    <circle cx="170" cy="175" r="16" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="170" y="180">o</text>
    <circle cx="50" cy="225" r="16" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="50" y="230">t</text>
    <circle cx="110" cy="225" r="16" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="2.2"/><text x="110" y="230">r*</text>
    <circle cx="170" cy="225" r="16" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="170" y="230">p</text>
    <path d="M120,86 L120,109" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" fill="none"/>
    <path d="M110,138 L90,161" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" fill="none"/>
    <path d="M130,138 L160,161" stroke="var(--dsa-neutral)" stroke-width="1.5" fill="none"/>
    <path d="M75,190 L54,212" stroke="var(--dsa-neutral)" stroke-width="1.5" fill="none"/>
    <path d="M88,190 L104,212" stroke="var(--dsa-success)" stroke-width="var(--dsa-arrow-stroke)" fill="none"/>
    <path d="M170,190 L170,212" stroke="var(--dsa-neutral)" stroke-width="1.5" fill="none"/>
  </g>
  <g font-family="var(--dsa-font)" text-anchor="middle">
    <text x="450" y="52" font-size="12" font-weight="700" fill="var(--dsa-neutral)">grid</text>
    <g font-size="15" font-weight="700" fill="var(--dsa-ink)">
      <rect x="360" y="66" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="382" y="94">c</text>
      <rect x="410" y="66" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="432" y="94">a</text>
      <rect x="460" y="66" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="2.2"/><text x="482" y="94">r</text>
      <rect x="510" y="66" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="532" y="94">z</text>
      <rect x="360" y="116" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="382" y="144">o</text>
      <rect x="410" y="116" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="432" y="144">p</text>
      <rect x="460" y="116" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="482" y="144">t</text>
      <rect x="510" y="116" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="532" y="144">s</text>
    </g>
    <path d="M404,88 L410,88" stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" fill="none" marker-end="url(#tw-ar)"/>
    <path d="M454,88 L460,88" stroke="var(--dsa-success)" stroke-width="var(--dsa-arrow-stroke)" fill="none" marker-end="url(#tw-ar)"/>
    <defs>
      <marker id="tw-ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-success)"/></marker>
    </defs>
    <rect x="600" y="80" width="94" height="60" rx="10" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="2.4"/>
    <text x="647" y="106" font-family="var(--dsa-font)" font-size="12" font-weight="700" fill="var(--dsa-success)">found</text>
    <text x="647" y="128" font-family="var(--dsa-font)" font-size="16" font-weight="700" fill="var(--dsa-ink)">"car"</text>
  </g>
  <text x="360" y="238" text-anchor="middle" font-family="var(--dsa-font)" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">DFS walks the grid; the trie prunes any prefix not in the dictionary.</text>
</svg>
</div>




### Problem
Given a grid of letters and a dictionary, return **all dictionary words** that can be traced through **adjacent** cells (up/down/left/right), never reusing a cell within one word.

**Constraints:** grid up to `12×12`; up to `3·10⁴` words.

**Example 1:** grid with words `["oath","pea","eat","rain"]` → the traceable ones (e.g. `["oath","eat"]`).

&lt;ExamplePreview compact :input="['"oath"', '"pea"', '"eat"', '"rain"']" :output="['"oath"', '"eat"']" /&gt;

**Example 2:** Board `[["a"]]`, words `["a","b"]` → `["a"]`.

&lt;ExamplePreview compact :input="['[["a"]]']" :output="['"a"', '"b"']" /&gt;

### Solution — brute force
The straightforward approach is: for every word, run the single-word Word Search DFS over the board. That is easy to explain but terrible at scale because common prefixes are re-explored for every word.



```text
for each word in words:
    for each cell in board:
        run DFS trying to spell exactly this word
        if found, add it and stop searching this word
```



If there are `W` words, average length `L`, and `R·C` cells, the worst case is roughly O(W·R·C·4^L). The trie solution pays O(total characters) once, then shares all prefix work across the dictionary.

**Baseline complexity:** O(W·R·C·4^L) worst case and O(L) recursion space per word search.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
Insert all words into a trie, then DFS the grid once, walking the trie in lockstep — pruning every branch that leaves the trie.

<Callout kind="key" title="Key Insight">

With many query words, testing each independently is wasteful. The trie lets one grid DFS test *all* words at once: you only continue into a cell if the current character exists as a trie edge. Mark found words at terminal nodes.

</Callout>

<Callout kind="inv" title="Invariant">

The DFS position in the grid and the node in the trie always spell the same string; leaving the trie means no word can be completed down this path.

</Callout>

#### Java (core)


```java
List<String> findWords(char[][] board, String[] words) {
    Node root = buildTrie(words);
    List<String> res = new ArrayList<>();
    for (int r = 0; r < board.length; r++)
        for (int c = 0; c < board[0].length; c++)
            dfs(board, r, c, root, res);
    return res;
}
void dfs(char[][] b, int r, int c, Node node, List<String> res) {
    if (r < 0 || c < 0 || r >= b.length || c >= b[0].length) return;
    char ch = b[r][c];
    if (ch == '#') return;
    Node nxt = node.next[ch - 'a'];
    if (nxt == null) return;                 // prune: prefix not in any word
    if (nxt.word != null) { res.add(nxt.word); nxt.word = null; }  // dedup found
    b[r][c] = '#';                           // mark visited
    dfs(b, r+1, c, nxt, res); dfs(b, r-1, c, nxt, res);
    dfs(b, r, c+1, nxt, res); dfs(b, r, c-1, nxt, res);
    b[r][c] = ch;                            // restore
}
```



<Callout kind="note" title="Trace it">

words `["oath","pea","eat","rain"]` on a letter grid. Start from `o`: the trie has child `o`, then `a`, then `t`, then `h`, so that path can reach the terminal word `"oath"`. Start from a path like `o → a → x`: after `oa`, there is no `x` child, so the DFS returns immediately. You are not checking four words separately; one prefix walk prunes the whole dictionary.

</Callout>

<CodeTrace
  title="Word Search II — DFS pruned by trie for word 'oath'"
  :values="['o','a','t','h']"
  :windowKeys="['depth']"
  :cellWidth="42"
  :steps='[
    { pointers: { depth: 0 }, vars: { grid_cell: "(0,0)=o", trie_node: "root→o" }, note: "start. child o exists → dive", added: [0] },
    { pointers: { depth: 1 }, vars: { grid_cell: "(0,1)=a", trie_node: "o→a" }, note: "child a exists", added: [0,1] },
    { pointers: { depth: 2 }, vars: { grid_cell: "(1,1)=t", trie_node: "a→t" }, note: "child t exists", added: [0,1,2] },
    { pointers: { depth: 3 }, vars: { grid_cell: "(1,0)=h (END)", trie_node: "t→h★" }, note: "trie marks `oath` complete → collect", added: [0,1,2,3] },
    { pointers: { depth: 2 }, vars: { grid_cell: "(1,1)→x", trie_node: "a→x?" }, note: "alt branch: no x child → prune whole subtree" }
  ]'
/>

#### Same pattern, new tweaks
| Variation | The one thing that changes | Time |
|---|---|---|
| - **Word Search** (single word) — *tweak:* plain grid DFS, no trie needed. |  | — |
| [Concatenated Words](https://leetcode.com/problems/concatenated-words/) | a trie of all words + DFS to test whether a word is built from shorter ones | — |
| [Stream of Characters](https://leetcode.com/problems/stream-of-characters/) | store words *reversed* in a trie and match the incoming stream from the back | — |
| [Replace Words](https://leetcode.com/problems/replace-words/) | stop at the shortest terminal prefix instead of collecting all terminals | — |
| [Add and Search Word](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | wildcard `.` branches into all children at that depth | — |

<Callout kind="trap" title="Common Trap">

Re-adding a word for every path that reaches it. *Example:* board has multiple paths spelling `"cat"` from the same trie leaf. Without clearing `node.word` after the first find (or using a `Set<String>` result), you emit `"cat"` multiple times.

</Callout>

<TrapTrace title="Re-adding a word for every path that reaches it" input="'cat'" bug="board has multiple paths spelling ''cat'' from the same trie leaf. Without clearing 'node.word' after the first find (or using a 'SetltStringgt' result), you emit ''cat'' multiple times." fix="See the guidance in the trap description and the code snippet." />

<Callout kind="note" title="Interview script">

"I would not search each word independently because the dictionary has up to 30,000 words and many share prefixes. I build a trie once, then do board DFS while carrying the current trie node. If the next board letter is not a trie child, no dictionary word can continue, so I prune that branch. When I hit a terminal node, I record the word and clear it to avoid duplicates."

</Callout>

<Callout kind="pat" title="Pattern Connection">

"Drive a backtracking search with a trie to prune multiple targets simultaneously" is a hallmark staff-level combination of two structures.

</Callout>

### Time Complexity
Time O(R·C·4^L) worst but trie-pruned in practice · Space O(total chars).

Worst-case O(R·C·4^L), but trie prefix pruning avoids repeating work for shared dictionary prefixes.


### Space Complexity
O(totalChars) for the trie plus O(L) recursion stack; result output extra.

### Learning notes
- Why `buildTrie(words)` first? — it shares all dictionary prefixes before the board DFS begins.
- Why carry `Node node` in DFS? — the grid path and trie path must advance together.
- Why `nxt == null` returns immediately? — no dictionary word has this prefix, so every continuation is impossible.
- Why `nxt.word = null` after adding? — it deduplicates a word found through multiple paths.
- Why mark `b[r][c] = '#'` and restore? — one path cannot reuse a cell, but sibling paths need the original board.

## Maximum XOR of Two Numbers (Binary Trie) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)*

<ProgressCheck id="maximum-xor-of-two-numbers-binary-trie" />

### Problem
Given an array, find the **maximum XOR** obtainable from any two elements.

**Constraints:** `1 ≤ n ≤ 2·10⁵`; values `0 … 2³¹−1`; aim to beat O(n²).

**Example 1:** `[3,10,5,25,2,8]` → `28` (`5 XOR 25`).

&lt;ExamplePreview compact :input="['3', '10', '5', '25', '2', '8']" :output="['28']" /&gt;

**Example 2:** `[0]` → `0` because the only possible pair value with itself is zero.

&lt;ExamplePreview compact :input="['0']" :output="['0']" /&gt;

### Solution — brute force
The brute-force version checks every pair. It is a good correctness baseline and a terrible final answer for `n = 2·10^5`.



```java
int findMaximumXORBrute(int[] nums) {
    int best = 0;
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            best = Math.max(best, nums[i] ^ nums[j]);
        }
    }
    return best;
}
```



That is O(n²) time and O(1) space. The optimized version keeps the same "best partner" idea but finds the partner by walking a trie of bits, so each number costs only 32 decisions.

One subtle choice: many solutions insert all numbers first and then query all numbers, as below. You can also insert numbers one at a time and query only against previously inserted numbers to avoid pairing a value with itself. For maximum XOR of two numbers, pairing with itself gives XOR 0, so it never incorrectly beats a positive answer; the all-first version is simpler.

**Baseline complexity:** O(n²) time and O(1) space.

### Solution — optimized
The optimized solution keeps the original Java intact and explains the pattern that removes the brute-force bottleneck.

#### Pattern
Insert numbers bit-by-bit (MSB→LSB) into a binary trie; for each number, greedily walk toward the *opposite* bit to maximize XOR.

<Callout kind="key" title="Key Insight">

To maximize XOR, at each bit prefer the branch with the complementary bit (they differ → contributes `1` at that position). A binary trie makes this greedy choice O(32) per query.

</Callout>

#### Java (sketch)


```java
class BinTrie { BinTrie[] c = new BinTrie[2]; }
int findMaximumXOR(int[] nums) {
    BinTrie root = new BinTrie();
    for (int x : nums) {                       // insert
        BinTrie n = root;
        for (int b = 31; b >= 0; b--) {
            int bit = (x >> b) & 1;
            if (n.c[bit] == null) n.c[bit] = new BinTrie();
            n = n.c[bit];
        }
    }
    int best = 0;
    for (int x : nums) {                        // query best partner
        BinTrie n = root; int cur = 0;
        for (int b = 31; b >= 0; b--) {
            int bit = (x >> b) & 1, want = bit ^ 1;
            if (n.c[want] != null) { cur |= (1 << b); n = n.c[want]; }
            else n = n.c[bit];
        }
        best = Math.max(best, cur);
    }
    return best;
}
```



<Callout kind="note" title="Trace it">

Use 5-bit versions for readability: `5 = 00101`, `25 = 11001`. Querying `5`, the trie first wants `1` at the 16s bit and can take `25`'s branch, so the XOR gets a high `1`. It next wants `1` at the 8s bit and again follows `25`. Later bits contribute as available. The final path gives `00101 XOR 11001 = 11100` = `28`, better than any pair in `[3,10,5,25,2,8]`.

</Callout>

<CodeTrace
  title="Maximum XOR — query 5 vs trie of [3,10,5,25,2,8], 5-bit"
  :values="[1,6,8,4]"
  :windowKeys="['bit']"
  :cellWidth="42"
  :steps='[
    { pointers: { bit: 0 }, vars: { want: "1 (16s)", have_choice: "0 or 1", pick: 1 }, note: "query bit=0 → want 1 → trie has → take 25 branch", added: [0] },
    { pointers: { bit: 1 }, vars: { want: "1 (8s)", pick: 1 }, note: "query bit=0 → want 1 → 25 branch continues (25=11001)", added: [0,1] },
    { pointers: { bit: 2 }, vars: { want: "0 (4s)", pick: 0 }, note: "query bit=1 → want 0 → 25 continues (bit 4)", added: [0,1] },
    { pointers: { bit: 3 }, vars: { want: "0 (2s)", pick: 0 }, note: "query bit=0 → want 0 → but 25 has 0 → 25 (bit 3 of 11001 = 0)", added: [0,1,2] },
    { pointers: { bit: 4 }, vars: { want: "0 (1s)", pick: 1 }, note: "query bit=1 → want 0 → 25 has 1 → XOR bit set. total = 11100 = 28", added: [0,1,2,3] }
  ]'
/>

#### Why MSB-first matters
XOR is a number, not just a count of different bits. A `1` in the 16s place beats any combination of lower bits. That is why the trie walk starts from bit 31 and commits greedily. If the opposite branch exists at a high bit, take it. Even if that later forces weaker low bits, the high bit already dominates.

For a tiny 4-bit example, compare possible XORs for query `0101`. A partner beginning with `1...` gives a leading XOR bit `1`, producing at least `1000` (8). A partner beginning with `0...` leaves that bit `0`, so the best it can do is `0111` (7). No later choice can recover the lost high bit. This is the same logic as choosing the lexicographically larger binary string when maximizing a number.

#### Same pattern, new tweaks
| Variation | The one thing that changes | Time |
|---|---|---|
| [Maximum XOR With an Element From Array](https://leetcode.com/problems/maximum-xor-with-an-element-from-array/) | answer queries offline, sorting by the value bound and inserting numbers as they become allowed | O((n+q)·32) |
| [Count Pairs With XOR in a Range](https://leetcode.com/problems/count-pairs-with-xor-in-a-range/) | store subtree counts in the binary trie and count paths whose XOR is `< limit`, then subtract | O(n·32) |
| [Maximum Genetic Difference Query](https://leetcode.com/problems/maximum-genetic-difference-query/) | add/remove ancestors in a binary trie during tree DFS | O((n+q)·32) |
| [Replace Words / IP routing](https://leetcode.com/problems/replace-words/) | the same longest-prefix idea, but over characters or address bits instead of XOR greed | — |

<Callout kind="trap" title="Common Trap">

Comparing bits in the wrong direction. *Example:* numbers `[3,10,5,25]` — XOR-max hunt greedily wants the **opposite** bit at each level from the query. Insert MSB-first; at each level, walk the child whose bit differs from the current bit (fall back if that branch doesn't exist).

</Callout>

<TrapTrace title="Comparing bits in the wrong direction" input="[3,10,5,25]" bug="numbers '[3,10,5,25]' — XOR-max hunt greedily wants the **opposite** bit at each level from the query" fix="Insert MSB-first; at each level, walk the child whose bit differs from the current bit (fall back if that branch doesn't exist)." />

<Callout kind="note" title="Interview script">

"Brute force compares every pair, but XOR is decided from the highest bit downward. I insert every number into a binary trie and, for each query number, prefer the opposite bit at each level. If the opposite branch exists, that bit of the answer becomes 1; otherwise I take the same-bit branch. The width is constant at 32, so the total time is O(n)."

</Callout>

<Callout kind="pat" title="Pattern Connection">

Binary tries also answer *Maximum XOR With an Element From Array* (offline with a value bound) and range-XOR counting (store subtree counts). It is the bitwise cousin of prefix-tree search: different alphabet, same shared-path idea.

</Callout>

### Time Complexity
Time O(n·32) · Space O(n·32).

O(n·32), which is O(n) for fixed-width Java integers.


### Space Complexity
O(n·32) trie nodes in the worst case.

### Learning notes
- Why walk bits from 31 down to 0? — higher XOR bits dominate every combination of lower bits.
- Why `want = bit ^ 1`? — XOR gets a 1 exactly when the two bits differ.
- Why set `cur |= (1 << b)` only when `want` exists? — that bit can be made 1 only if an opposite branch is available.
- Why insert all numbers first? — each query can choose among every potential partner in the array.
- Why pairing with itself is harmless here? — self-XOR is 0, which cannot beat a positive maximum pair.

---

## Check your understanding

<Quiz
  pattern-id="trie"
  :questions='[{"q": "What is the space complexity of a trie storing N words of avg length L over alphabet σ?", "choices": [{"text": "O(N · L · σ) worst case", "correct": true, "explanation": "Each node has ≤ σ child pointers; N·L nodes total."}, {"text": "O(N)", "correct": false}, {"text": "O(L)", "correct": false}, {"text": "O(σ)", "correct": false}]}, {"q": "Search in a trie for a word of length L costs:", "choices": [{"text": "O(L)", "correct": true, "explanation": "One step per character, regardless of N."}, {"text": "O(N)", "correct": false}, {"text": "O(N · L)", "correct": false}, {"text": "O(σ · L)", "correct": false, "explanation": "Only if scanning all children each step."}]}, {"q": "For Word Search II, why is Trie + DFS faster than DFS-per-word?", "choices": [{"text": "Shared prefix traversal — each grid cell visits the trie at most O(σ) times", "correct": true, "explanation": "Grid DFS + trie fusion avoids repeated prefix work."}, {"text": "Sorting", "correct": false}, {"text": "Randomization", "correct": false}, {"text": "Not faster", "correct": false}]}, {"q": "For Stream of Characters (last-suffix match), what modification to the standard trie?", "choices": [{"text": "Insert each dictionary word REVERSED", "correct": true, "explanation": "Then walk backward through the stream — matches end at the newest char."}, {"text": "Store hash of suffixes", "correct": false}, {"text": "Use two tries", "correct": false}, {"text": "Never possible in O(L)", "correct": false}]}, {"q": "For Maximum XOR Between Numbers, what tree do you build?", "choices": [{"text": "Binary trie of the numbers (bit-by-bit)", "correct": true, "explanation": "Walk from MSB, greedily choosing the opposite bit."}, {"text": "BST", "correct": false}, {"text": "Character trie", "correct": false}, {"text": "Heap", "correct": false}]}]'
/>

&lt;RelatedPatterns pattern-id="trie-pattern" /&gt;
