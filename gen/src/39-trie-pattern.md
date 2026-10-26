# Trie (pattern)


<PatternVideo pattern-name="Trie" duration="8–12 min" />

<PatternProgress pattern-id="trie" problems="word-search-ii, design-add-and-search-words-data-structure, replace-words, concatenated-words, stream-of-characters, maximum-xor-with-an-element-from-array, count-pairs-with-xor-in-a-range, maximum-genetic-difference-query" />

<script setup>
const theTemplateSpecializations = [
  { slug: `implement-trie-bare-mechanic-medium`, title: `Implement Trie (bare mechanic)` },
  { slug: `word-search-ii-trie-backtracking-hard`, title: `Word Search II (trie + backtracking)` },
  { slug: `replace-words-shortest-prefix-replacement-medium`, title: `Replace Words (shortest-prefix)` },
  { slug: `map-sum-pairs-prefix-sum-over-values-medium`, title: `Map Sum Pairs (prefix-sum over values)` },
  { slug: `search-suggestions-system-autocomplete-top-3-medium`, title: `Search Suggestions (autocomplete top-3)` },
  { slug: `word-break-ii-trie-dp-hard`, title: `Word Break II (trie + DP)` },
  { slug: `maximum-xor-of-two-numbers-binary-trie-medium`, title: `Maximum XOR (binary trie)` },
  { slug: `concatenated-words-dfs-over-trie-hard`, title: `Concatenated Words (DFS over trie)` },
]

const theTemplateCode = `// THE Trie template — 26-way letter trie with explicit end-of-word flag.
// Operations: insert, search (whole word), startsWith (prefix only).
class Trie {
    Trie[] next = new Trie[26];                   // one slot per lowercase letter
    boolean end = false;                           // true at the last node of an inserted word

    void insert(String word) {
        Trie node = this;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (node.next[i] == null) node.next[i] = new Trie();
            node = node.next[i];
        }
        node.end = true;                           // CRITICAL: without this, "app" false-matches "apple"
    }

    boolean search(String word) {
        Trie node = walk(word);
        return node != null && node.end;           // whole word match requires end flag
    }

    boolean startsWith(String prefix) {
        return walk(prefix) != null;               // prefix match: any walkable path
    }

    private Trie walk(String s) {
        Trie node = this;
        for (char c : s.toCharArray()) {
            int i = c - 'a';
            if (node.next[i] == null) return null;
            node = node.next[i];
        }
        return node;
    }
}`

const binaryTrieCode = `// Binary trie — 32-bit path per int, used for max-XOR queries.
// Walk MSB-first; at each bit prefer the OPPOSITE bit to maximize the XOR.
class BinaryTrie {
    BinaryTrie[] next = new BinaryTrie[2];

    void insert(int x) {
        BinaryTrie node = this;
        for (int b = 31; b >= 0; b--) {
            int bit = (x >>> b) & 1;
            if (node.next[bit] == null) node.next[bit] = new BinaryTrie();
            node = node.next[bit];
        }
    }

    int maxXor(int q) {
        BinaryTrie node = this;
        int result = 0;
        for (int b = 31; b >= 0; b--) {
            int bit = (q >>> b) & 1;
            int want = bit ^ 1;                     // XOR wants the opposite bit
            if (node.next[want] != null) {
                result |= (1 << b);
                node = node.next[want];
            } else {
                node = node.next[bit];              // fallback — forced to take same bit
            }
        }
        return result;
    }
}`

const replaceWordsCode = `// Replace Words — insert all roots, then for each word walk until the first terminal.
String replaceWords(List<String> dictionary, String sentence) {
    Trie root = new Trie();
    for (String r : dictionary) root.insert(r);
    String[] words = sentence.split(" ");
    for (int i = 0; i < words.length; i++) {
        Trie node = root;
        StringBuilder shortest = new StringBuilder();
        for (char c : words[i].toCharArray()) {
            int idx = c - 'a';
            if (node.next[idx] == null) break;
            shortest.append(c);
            node = node.next[idx];
            if (node.end) break;                   // first terminal = shortest root
        }
        if (node.end) words[i] = shortest.toString();
    }
    return String.join(" ", words);
}`

const mapSumCode = `// Map Sum Pairs — propagate value-deltas along every prefix node on insert.
// prefix.sum() = sum of all values whose key starts with prefix. O(L) per op.
class MapSum {
    static class Node { Node[] next = new Node[26]; int sum = 0; }
    private final Node root = new Node();
    private final Map<String, Integer> map = new HashMap<>();

    public void insert(String key, int val) {
        int delta = val - map.getOrDefault(key, 0);
        map.put(key, val);
        Node node = root;
        for (char c : key.toCharArray()) {
            int i = c - 'a';
            if (node.next[i] == null) node.next[i] = new Node();
            node = node.next[i];
            node.sum += delta;                     // every prefix node accumulates
        }
    }

    public int sum(String prefix) {
        Node node = root;
        for (char c : prefix.toCharArray()) {
            int i = c - 'a';
            if (node.next[i] == null) return 0;
            node = node.next[i];
        }
        return node.sum;
    }
}`

const searchSuggestionsCode = `// Search Suggestions — at each prefix node, store up to 3 lex-smallest completions.
// Sort products once, then insert; after each character, read the 3 cached suggestions.
List<List<String>> suggestedProducts(String[] products, String searchWord) {
    Arrays.sort(products);
    Trie root = new Trie();
    for (String p : products) root.insert(p);
    List<List<String>> ans = new ArrayList<>();
    Trie node = root;
    boolean dead = false;
    for (char c : searchWord.toCharArray()) {
        if (!dead && node.next[c - 'a'] != null) {
            node = node.next[c - 'a'];
            ans.add(node.top3);                    // cached top-3 at this prefix
        } else {
            dead = true;
            ans.add(Collections.emptyList());
        }
    }
    return ans;
}

class Trie {
    Trie[] next = new Trie[26];
    List<String> top3 = new ArrayList<>();         // sorted; at most 3 words

    void insert(String word) {
        Trie node = this;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (node.next[i] == null) node.next[i] = new Trie();
            node = node.next[i];
            if (node.top3.size() < 3) node.top3.add(word);
        }
    }
}`

const wordBreakIICode = `// Word Break II — trie prunes dictionary lookups during DFS over sentence splits.
List<String> wordBreak(String s, List<String> wordDict) {
    Trie root = new Trie();
    for (String w : wordDict) root.insert(w);
    List<String> ans = new ArrayList<>();
    dfs(s, 0, root, new ArrayList<>(), ans);
    return ans;
}

void dfs(String s, int i, Trie root, List<String> path, List<String> ans) {
    if (i == s.length()) { ans.add(String.join(" ", path)); return; }
    Trie node = root;
    StringBuilder sb = new StringBuilder();
    for (int j = i; j < s.length(); j++) {
        int idx = s.charAt(j) - 'a';
        if (node.next[idx] == null) return;        // prune: no word starts with this prefix
        node = node.next[idx];
        sb.append(s.charAt(j));
        if (node.end) {
            path.add(sb.toString());
            dfs(s, j + 1, root, path, ans);
            path.remove(path.size() - 1);
        }
    }
}`

const concatenatedWordsCode = `// Concatenated Words — a word is "concatenated" iff it can be split into >=2
// shorter dictionary words. DFS over the trie with memoization on split points.
List<String> findAllConcatenatedWordsInADict(String[] words) {
    Arrays.sort(words, Comparator.comparingInt(String::length));
    Trie root = new Trie();
    List<String> ans = new ArrayList<>();
    for (String w : words) {
        if (!w.isEmpty() && canBuild(w, 0, root, 0)) ans.add(w);
        root.insert(w);                            // insert AFTER checking (ordered by length)
    }
    return ans;
}

boolean canBuild(String w, int i, Trie root, int parts) {
    if (i == w.length()) return parts >= 1;        // >=1 completed part + the final part = >=2 pieces
    Trie node = root;
    for (int j = i; j < w.length(); j++) {
        int idx = w.charAt(j) - 'a';
        if (node.next[idx] == null) return false;
        node = node.next[idx];
        if (node.end && canBuild(w, j + 1, root, parts + 1)) return true;
    }
    return false;
}`

const trap1Bug = `Insert ["apple"] then search("app"). Walking "app" doesn't hit null, so a buggy search returns true. But "app" was never inserted — it's just a prefix of "apple". The dictionary is corrupted silently.`
const trap1Fix = `Every node needs an explicit boolean "end" field; insert() sets it true on the last node; search() returns walked-to-non-null && end. startsWith() keeps the no-end-check behavior. The flag's existence is the whole mechanism for distinguishing prefix from whole-word match.`

const trap2Bug = `Board where "cat" can be spelled starting from two different cells. Without dedup, the output contains ["cat", "cat"] — the grader rejects it. Also happens when the same path is explored in both directions during a bidirectional sweep.`
const trap2Fix = `After collecting a word, mutate the trie: set the terminal node's end = false (effectively "uninstalling" it from future finds). Alternative: collect into a Set<String> and dedupe. The trie-mutation approach is faster because future paths that would have reached this terminal get pruned.`

const trap3Bug = `A buggy insert iterates b from 0 to 31. The trie now paths LSB-first. maxXor() still prefers opposite bits, but each "opposite" is at a tiny place value. On nums=[3, 10, 5] a query of 25 may return 7 instead of 28.`
const trap3Fix = `Always iterate MSB-first: for (int b = 31; b >= 0; b--). Bit 31 contributes 2^31 to the XOR — more than all lower bits combined. The greedy opposite-bit choice at the MSB dominates every subsequent decision.`

const trieInvariant = {
  statement: `At every point: (1) every inserted word corresponds to a path from root ending at a node with end == true, (2) a lookup walking the path returns the correct answer iff the end flag is checked, (3) the branching factor at every node is at most |alphabet|.`,
  initialization: `Before any insertion: root is an empty node with all next[i] == null and end == false. The invariant holds vacuously (no inserted words).`,
  maintenance: `insert(word): walks the path, creating missing child nodes along the way; sets end = true on the last node. Previously-inserted words are undisturbed because the shared-prefix walk reuses existing branches. search(word): walks the same path and verifies end == true at the terminal — distinguishing full-word match from mere-prefix match. startsWith(prefix): just verifies the walk doesn't hit null.`,
  termination: `For any sequence of inserts and queries: insert(w) ensures w is henceforth findable; search(w) returns true iff w has been inserted; startsWith(p) returns true iff some inserted word starts with p.`,
}

const trieComplexity = { time: `O(L) per op where L is the word/prefix length — independent of #stored words`, space: `O(sum of unique prefix characters) — shared prefixes cost once; worst case O(alphabet × total chars)` }

const mastery5 = [
  {
    q: `Why does a trie need an explicit "end-of-word" flag on nodes?`,
    choices: [
      { text: `To distinguish full-word matches from mere-prefix matches — otherwise 'app' falsely matches when only 'apple' was inserted`, correct: true, explanation: `Without the flag, search() has no way to know whether the walk ended at a real word or just a prefix of one. insert() sets end=true; search() verifies it.` },
      { text: `To free memory on delete`, correct: false, explanation: `That's a separate optimization and doesn't require the flag's existence.` },
      { text: `For sorted iteration`, correct: false, explanation: `Lex order comes from branch iteration, not the end flag.` },
      { text: `To speed up startsWith`, correct: false, explanation: `startsWith doesn't check end — it only verifies walkability.` },
    ],
  },
  {
    q: `For Maximum XOR with a binary trie, why walk bits MSB-first and prefer the OPPOSITE bit at each step?`,
    choices: [
      { text: `Each higher-order bit contributes more to the XOR value than all lower-order bits combined, so grabbing opposite-bit at the MSB maximizes the result greedily`, correct: true, explanation: `Bit 31 is worth 2^31 ≥ 2^30 + 2^29 + ... + 2^0 + 1. Setting bit 31 to 1 (opposite choice if possible) outweighs any future bit choices.` },
      { text: `MSB-first makes the trie smaller`, correct: false, explanation: `Trie size depends only on inserted values' bit patterns.` },
      { text: `To support signed integers`, correct: false, explanation: `Using unsigned right shift >>> handles signedness independently.` },
      { text: `Random choice`, correct: false },
    ],
  },
  {
    q: `For Word Search II (trie + DFS board), what's the TRIE-side optimization that makes the algorithm fast?`,
    choices: [
      { text: `A missing trie child at the current letter kills the entire DFS branch — no further board exploration needed`, correct: true, explanation: `This is the core of the trie-prunes-DFS idea. If 'oax' has no trie continuation, every path extending 'oax' can be abandoned, saving exponential work.` },
      { text: `The trie sorts the dictionary`, correct: false },
      { text: `The trie dedupes words`, correct: false, explanation: `Dedup is a benefit but not THE speedup — pruning is.` },
      { text: `The trie supports O(1) random access`, correct: false },
    ],
  },
  {
    q: `In Search Suggestions System, where are the top-3 lex-smallest completions stored for O(1) retrieval?`,
    choices: [
      { text: `In a top3 list CACHED on each trie node, populated at insert time after sorting the input`, correct: true, explanation: `Sort products once; walk each product through the trie; at every node visited, append the word if top3.size() < 3. At query time, read the cached list per prefix letter.` },
      { text: `In a single global sorted array`, correct: false },
      { text: `In a hash map keyed by prefix`, correct: false, explanation: `Possible but wastes space — the trie already encodes prefixes.` },
      { text: `Computed via DFS at query time`, correct: false, explanation: `Correct but slow — defeats the preprocess advantage.` },
    ],
  },
  {
    q: `For Concatenated Words, why sort the input by length before processing?`,
    choices: [
      { text: `A concatenated word is built from SHORTER dictionary words — processing short-first ensures smaller pieces are already in the trie when we check a longer word`, correct: true, explanation: `By length-ascending order, when we check canBuild(w), every piece shorter than |w| has already been inserted. The check becomes "can this longer word be split into pieces already present?"` },
      { text: `For deterministic output`, correct: false, explanation: `Final answer can still be sorted later; this isn't why.` },
      { text: `To avoid duplicates`, correct: false },
      { text: `For better cache performance`, correct: false },
    ],
  },
]
</script>

**Grokking arc:** The motivating problem is repeated prefix checking against many words or many bit strings. Brute force scans every candidate. **Can we do better?** Share prefixes in a trie so each next character or bit decides whether a whole branch remains possible.

## Why trie patterns exist — the story

A normal string search treats every word like a stranger. If your dictionary is `cat`, `car`, `cart`, and `dog`, and you ask whether the grid path `c → a → r → ...` can become a word, a brute-force checker may compare that prefix against every dictionary entry again and again. A trie changes the conversation: all words that start with `ca` share one hallway, so walking `c`, then `a`, answers "does any target still remain possible?" in O(1) per letter. The moment the hallway ends, you stop exploring.

That shared-prefix idea is why trie questions often pair with another technique. In **Word Search II**, the trie is the dictionary brain and backtracking is the board explorer. The DFS does not ask, "Is this complete path one of 30,000 words?" after every move. It asks, "Does this next letter exist from my current trie node?" If not, the entire branch dies immediately. For board paths like `o → a → x`, and a dictionary containing `oath` but no word beginning `oax`, the trie saves you from exploring every continuation under `x`.

The same idea works when the alphabet is not letters but bits. For maximum XOR, insert numbers as 32-bit paths. Query `5` (`00101` in a tiny 5-bit story) against `3,10,25`: at the highest bit, XOR wants the opposite bit because `1` beats `0` in that position. If the query bit is `0`, prefer a stored `1`; if the query bit is `1`, prefer a stored `0`. With `5` and `25` (`11001`), those opposite choices produce `11100` = 28. You did not compare `5` against every number one by one; the binary trie let you greedily choose the best available partner bit-by-bit in O(32).

The *pattern* chapter is about those applications. For the mechanics of a trie node, `insert`, `search`, and `startsWith`, see the [Trie deep-dive](#tries-prefix-trees) in Part III.

> [key] **Key Insight** — A trie turns many repeated prefix checks into one shared walk. A binary trie does the same thing for bits: build once, then each query makes 32 greedy choices instead of scanning all prior numbers.

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

## When to use it — trie pattern flavors

| Flavor | Recognizer phrasing | What the trie contributes |
|---|---|---|
| Dictionary-pruned DFS | "find all words on a board", "many target strings" | kills paths as soon as their prefix is absent |
| Shortest/longest prefix | "replace by root", "routing prefix", "autocomplete" | walks one path and stops at the first or deepest useful terminal |
| Wildcard branching | "`?` / `.` can match any letter" | branches only at wildcard positions instead of scanning every word |
| Binary XOR trie | "maximum XOR", "XOR under limit", "count XOR pairs" | chooses opposite bits greedily from most significant to least |
| Streaming suffix query | "does the stream end with any word?" | store reversed words, then walk the recent stream backward |

The important interview move is to name the alphabet. Letter tries branch over characters. Binary tries branch over `0/1` bits. Reversed tries branch over the query from the end. Once you say that out loud, the code becomes a normal walk with a different interpretation of "next edge."

## THE template

Every Trie-pattern problem is a specialization of **"walk a path through the trie, one character (or bit) at a time; branch when the problem demands wildcards or multiple roots."** Four parameters distinguish the sub-variations: the alphabet (26 letters vs. 2 bits vs. Unicode), what each node caches (end flag, sum, top-k list), whether queries branch (wildcards) or walk greedily (max-XOR), and whether the trie partners with another algorithm (backtracking, DP).

<PatternTemplateCard
  slug="trie-letter-template"
  title="26-way letter trie — THE template"
  language="java"
  :code="theTemplateCode"
  :invariant="trieInvariant"
  :complexity="trieComplexity"
  :specializations="theTemplateSpecializations"
/>

**Binary trie variant** (32-bit path per int for max-XOR queries):

<TemplateReveal
  slug="binary-trie"
  language="java"
  :canonical="binaryTrieCode"
/>

## Traps & gotchas

<TrapTrace
  title="Trap 1 — Forgetting the end-of-word flag"
  :bug="trap1Bug"
  :fix="trap1Fix"
/>

<TrapTrace
  title="Trap 2 — Word Search II emitting the same word twice"
  :bug="trap2Bug"
  :fix="trap2Fix"
/>

<TrapTrace
  title="Trap 3 — Binary-trie bit order reversed (LSB-first)"
  :bug="trap3Bug"
  :fix="trap3Fix"
/>

## History — de la Briandais 1959, Fredkin 1960, Google's first index

The trie data structure was invented by **René de la Briandais** in 1959 as a compact way to store dictionaries in punch-card memory. **Edward Fredkin** independently rediscovered and named it in 1960: *"trie"* from "re**trie**val" (Fredkin insisted it should be pronounced "tree," but nobody listened; the standard pronunciation is "try").

Google's **first web search index (1996-1998)** was a trie of URL prefixes — that's how it did `startsWith` queries so cheaply while other search engines lagged. The **Judy Array** (2000s) was Doug Baskins' cache-aware trie variant for the Cray-1 supercomputer. Modern applications:

- **Autocomplete** everywhere — from your terminal shell (`bash` completion) to Google Search's dropdown.
- **IP routing tables** — every packet routing table on the internet is a Patricia trie (compressed trie) on IP address bit prefixes. Cisco's ASIC hardware performs the walk in one clock cycle.
- **Ethereum's state tree** is a Merkle Patricia trie — cryptographically verifiable trie of account states.
- **Bioinformatics** — suffix tries (Aho-Corasick, 1975) find all occurrences of multiple patterns in DNA sequences.

When you mention *"we could compress single-child chains with a Patricia trie"* in an interview, you're citing a data structure Cisco routers use to move billions of packets per second.

## Sub-variations of the template

<PatternSubVariationNav pattern="trie-pattern" />

The sub-variations walk the template through eight canonical uses — bare mechanic, trie-pruned backtracking on a grid, shortest-prefix root replacement, prefix-sum over values, cached top-k autocomplete, trie + DP sentence split, binary-trie max-XOR, and trie + length-ordered DFS for concatenated words. Each uses the same walk-the-path kernel; what changes is what the node caches and how the walk partners with another algorithm.

### Implement Trie (bare mechanic) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/)*

The simplest instance. Build a trie supporting `insert(word)`, `search(word)`, `startsWith(prefix)`. The whole mechanism is a 26-way array of children per node plus an explicit `end` flag to distinguish word-match from prefix-match.

> [inv] **Invariant** — At every point: inserted words correspond to root-to-end-marked paths; `search` finds a word iff the walk reaches a node with `end == true`; `startsWith` succeeds iff the walk is non-null.

> [key] **Blind-solve prompt** — *Before revealing:* without peeking, write the three operations. Why does `search` need to check `end == true` but `startsWith` doesn't?

<TemplateReveal
  slug="implement-trie"
  language="java"
  :canonical="theTemplateCode"
/>

**Trace** on `insert("apple")`, `insert("app")`, `search("app")`, `startsWith("app")`, `search("appl")`:

| op | trie state | result |
|---|---|---|
| insert("apple") | root→a→p→p→l→e(end) | — |
| insert("app") | root→a→p→p(end)→l→e(end) | — |
| search("app") | walk reaches p-with-end=true | **true** |
| startsWith("app") | walk reaches p (non-null) | **true** |
| search("appl") | walk reaches l (end=false) | **false** |

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **The core structure**: each node holds `children[26]` (or `HashMap<Character, Node>` for non-ASCII) + `end: boolean`. Three operations are all O(L) walks where L = word length.
- **Why `end` is non-negotiable**: `search("app")` must return `false` when only `"apple"` was inserted. Without the `end` flag, `search` can't distinguish word-match from prefix-match. `startsWith` doesn't need it (any non-null walk succeeds).
- **Array vs. HashMap children**: `Node[26]` for lowercase English (fast, 26×8B = 208B per node idle). `HashMap<Character, Node>` for unicode or when branching is sparse (slower, more memory per child but no idle slots).
- **Alternative encoding — the compressed trie (radix tree)**: each edge stores a *substring*, not one char. Memory-optimal for sparse tries. More complex insert/search; prefer the plain trie unless memory bites.
- **Space**: O(ALPHABET · total_chars_in_dict) worst case. For N words of average length L on a 26-letter alphabet: ~26 · N · L bytes.
- **Siblings: Design Add and Search Words Data Structure (`.` wildcard = DFS over all children), Longest Common Prefix (trie or sort-and-compare).**

</details>

### Replace Words (shortest-prefix replacement) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Replace Words](https://leetcode.com/problems/replace-words/)*

Given a list of "root" words and a sentence, replace every word in the sentence by the SHORTEST root that is a prefix of it (if any). The trie insight: walking a word down the trie, the **first** terminal we hit is the shortest root — stop immediately.

> [inv] **Invariant** — When walking word `w` from root, the first node with `end == true` is the shortest-prefix root of `w` (if any such root exists); any longer root would require continuing past this terminal.

<TemplateReveal
  slug="replace-words"
  language="java"
  :canonical="replaceWordsCode"
/>

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **The trie insight: shortest-prefix root is the FIRST terminal on the walk.** Walk the word; stop as soon as `node.end == true`; return the walked prefix. No need to continue past it.
- **If no terminal is hit** (walk ends because the next child is null, or the word ends with no `end` seen) → the word has no root replacement; keep it unchanged.
- **Why not a HashSet of roots?** Then you'd test every prefix of each word → O(L²) per word. The trie walks each word once in O(L).
- **Preprocess once**: insert all roots into the trie before scanning the sentence. Build cost is O(sum of root lengths); per-word query is O(word length).
- **Edge case**: if the input sentence has words separated by multiple spaces or has leading/trailing whitespace, split on whitespace cautiously — the LeetCode variant assumes single-space-separated.
- **Siblings: Longest Common Prefix (trie or sort-and-compare), Longest Word in Dictionary (trie + BFS by length).**

</details>

### Map Sum Pairs (prefix-sum over values) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Map Sum Pairs](https://leetcode.com/problems/map-sum-pairs/)*

Design `MapSum` with `insert(key, val)` and `sum(prefix)` returning the sum of values of all stored keys that start with `prefix`. The trick: **propagate value-deltas along every prefix node on insert**. Each node caches the sum of all values whose key passes through it; `sum(prefix)` is a plain O(L) walk.

> [key] **Why delta?** If `insert("apple", 3)` runs then later `insert("apple", 5)`, we want sum("app") to be 5 (overwrite), not 8 (accumulate). Tracking `delta = new_val - old_val` and adding delta at each prefix node handles both insert and update uniformly.

<TemplateReveal
  slug="map-sum-pairs"
  language="java"
  :canonical="mapSumCode"
/>

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Each node caches the running sum of values of ALL keys that pass through it.** `sum(prefix)` is then an O(L) walk — one node lookup per prefix char.
- **The DELTA pattern for updates**: on `insert(key, val)`, compute `delta = val - oldValueIfAny`, then walk the key adding `delta` at every node. Handles both "new key" (delta = val - 0 = val) and "overwrite" (delta = new - old) uniformly.
- **Keep an auxiliary `HashMap<String, Integer>` of key→value** to look up `oldValueIfAny` in O(1). Without it, you'd need to walk the trie to find the old value — still O(L) but less direct.
- **Why NOT walk + sum children at query time?** That would be O(prefix_subtree_size) per `sum` — potentially O(N·L). The cached per-node sum turns every `sum` into O(L).
- **Doesn't support DELETE efficiently in this form** — you'd need to track per-node contributor counts to prune. For insert-only workloads, this is optimal.
- **Siblings: Range Sum on Prefix (same idea, different query shape), Design File System (trie keyed by path components, store value at terminal only).**

</details>

### Search Suggestions System (autocomplete top-3) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/)*

Given a product list and a search word, after each typed character return up to 3 lex-smallest completions. Preprocess: **sort products once**, then insert each into the trie; each node caches the first 3 words that pass through it (which are the 3 lex-smallest, by sort order). Query is O(L) — just read the cached list per prefix character.

> [inv] **Invariant** — Because insertion order is sorted, the first 3 words that visit any node are the 3 lex-smallest completions of that prefix. `top3` becomes authoritative at insert time.

<TemplateReveal
  slug="search-suggestions"
  language="java"
  :canonical="searchSuggestionsCode"
/>

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Sort products LEX ONCE before trie insertion.** Then the first 3 words that visit any node are guaranteed to be the 3 lex-smallest completions of its prefix (because insertion is in lex order).
- **Cache top-3 per node at insert time** — a `List<String>` of max size 3. If a 4th word visits, drop it. Query becomes O(L): walk L prefix chars, read the cached top-3 at each stop.
- **Alternative without trie: sort + binary search**. For each prefix, binary-search the sorted array for the first match, take up to 3 contiguous entries. O(L log N) per character typed, no preprocessing of a trie. Simpler but each query is slightly slower.
- **If the prefix walk falls off the trie** (null child), all remaining characters have no suggestions — return empty lists for those positions.
- **Memory**: O(sum of lengths + 3·N) for the trie + top-3 cache. For 10⁴ products of length 15, ~150K chars + 30K cached pointers.
- **Siblings: Design In-Memory File System (prefix tree keyed by path), Autocomplete System (persist frequency, use min-heap over top-k instead of lex-sorted list).**

</details>

### Word Break II (trie + DP) <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Word Break II](https://leetcode.com/problems/word-break-ii/)*

Return all ways to segment `s` into space-separated dictionary words. DFS over split points, backed by a trie: a missing child kills the entire branch of the DFS. Add memoization on `(i, parts)` for an extra constant-factor speedup if needed.

<TemplateReveal
  slug="word-break-ii"
  language="java"
  :canonical="wordBreakIICode"
/>

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **The move: DFS over split points, backed by a trie.** At each split position `i`, walk the trie from the root; whenever `node.end == true`, treat `s[0..i]` as a word and recurse on `s[i+1..]`. The trie prunes any branch whose extension isn't in the dictionary.
- **Memoize by starting index `i`**: `memo[i] = all possible segmentations of s[i..]`. Multiple parent splits can reach the same suffix; without memo this is exponential.
- **Output size is exponential in worst case** — `s = "aaaa...a"`, dict = `{"a", "aa", ...}` yields 2^n segmentations. Memoization doesn't help *time* in the worst case because we have to emit every answer; it helps *computation reuse*.
- **If only counting (Word Break I)** or only testing feasibility, scalar DP suffices: `dp[i] = ∃ word in dict ending at i AND dp[i - |word|]`. O(n²) time, O(n) space. Trie compresses the dictionary scan to O(longest word).
- **Why trie over HashSet?** HashSet forces re-hashing every candidate substring (O(L) per candidate). Trie walks character-by-character, so you test all prefixes in O(L) total.
- **Siblings: Word Break (feasibility only), Palindrome Partitioning II (same shape, palindrome constraint via Manacher or expand-around-center).**

</details>

### Concatenated Words (DFS over trie) <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Concatenated Words](https://leetcode.com/problems/concatenated-words/)*

Return all words that can be built by concatenating ≥ 2 shorter words from the same list. Sort by length first; **check-then-insert**, so when we check `w`, only strictly shorter words are in the trie. The DFS tries every split point; a word is "concatenated" iff recursion succeeds with ≥ 2 parts.

> [key] **Why length-sorted?** A concatenated word's pieces are all strictly shorter than the whole. By length-ascending order, every piece needed for `canBuild(w)` is already in the trie.

<TemplateReveal
  slug="concatenated-words"
  language="java"
  :canonical="concatenatedWordsCode"
/>

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- **Sort words by length ASCENDING before processing.** Then when checking whether word `w` is concatenated, every shorter word (and only shorter words) is already in the trie — exactly the pieces that could compose `w`.
- **Check-then-insert**: for each `w` in length order, try `canBuild(w, 0, 0_parts)`. If buildable with ≥ 2 parts, add `w` to results. Then insert `w` into the trie (so longer words can use `w` as a piece).
- **The DFS**: walk the trie from the root; at each `node.end`, recurse on the suffix with `parts + 1`. Need `parts ≥ 2` at the end (one word trivially matches itself).
- **If the input is unsorted and you can't pre-sort**: the alternative is to insert every word into the trie upfront, then for each word mark its terminal and check-with-exclusion. Clumsier.
- **Why not DP on words?** `dp[i] = can s[i..] be built` works, but you still need the trie-walk inside the DP to find next-split positions efficiently. The trie is doing the hard work either way.
- **Siblings: Longest Word in Dictionary (BFS over trie by length, check parents are all in dict), Word Break II (segment one string vs. test every word for self-concatenation).**

</details>

<details>
<summary><strong>Pedagogical: the 3-approach ladder for Word Search II (hash set → naive DFS → trie-pruned DFS)</strong></summary>

#### Canonical problem walkthrough — Word Search II

**Problem** ([↗ LeetCode](https://leetcode.com/problems/word-search-ii/)): Given an `m × n` board of characters and a list of `words`, return **all words** in the list that can be constructed from letters of sequentially adjacent cells. A cell may not be used more than once in a single word.

### Approach 1 — Word Search I per word

For each word, run the O(m·n · 4^L) DFS from every cell.

```java
List<String> findWordsBrute(char[][] board, String[] words) {
    List<String> res = new ArrayList<>();
    for (String w : words) {
        boolean found = false;
        for (int r = 0; r < board.length && !found; r++)
            for (int c = 0; c < board[0].length && !found; c++)
                if (dfs(board, r, c, w, 0)) { res.add(w); found = true; }
    }
    return res;
}

boolean dfs(char[][] b, int r, int c, String w, int i) {
    if (i == w.length()) return true;
    if (r < 0 || r >= b.length || c < 0 || c >= b[0].length || b[r][c] != w.charAt(i)) return false;
    char tmp = b[r][c]; b[r][c] = '#';
    boolean ok = dfs(b,r+1,c,w,i+1) || dfs(b,r-1,c,w,i+1) || dfs(b,r,c+1,w,i+1) || dfs(b,r,c-1,w,i+1);
    b[r][c] = tmp;
    return ok;
}
```

**Complexity:** O(k · m · n · 4^L) where k = number of words. For 10⁴ words on a 15×15 board, this TLEs immediately.

### Approach 2 — Trie of dictionary + single board DFS

Build a trie of all words. From each board cell, DFS **once**, walking the trie in parallel. The trie prunes: if the current cell's letter doesn't extend the trie path, the entire branch dies immediately.

```java
class Trie {
    Trie[] next = new Trie[26];
    String word = null;               // stored at terminals for direct collection
}

List<String> findWords(char[][] board, String[] words) {
    Trie root = new Trie();
    for (String w : words) {
        Trie node = root;
        for (char c : w.toCharArray()) {
            int i = c - 'a';
            if (node.next[i] == null) node.next[i] = new Trie();
            node = node.next[i];
        }
        node.word = w;
    }
    List<String> res = new ArrayList<>();
    for (int r = 0; r < board.length; r++)
        for (int c = 0; c < board[0].length; c++)
            dfs(board, r, c, root, res);
    return res;
}

void dfs(char[][] b, int r, int c, Trie node, List<String> res) {
    if (r < 0 || r >= b.length || c < 0 || c >= b[0].length) return;
    char ch = b[r][c];
    if (ch == '#' || node.next[ch - 'a'] == null) return;
    node = node.next[ch - 'a'];
    if (node.word != null) { res.add(node.word); node.word = null; }   // dedupe
    b[r][c] = '#';
    dfs(b, r+1, c, node, res);
    dfs(b, r-1, c, node, res);
    dfs(b, r, c+1, node, res);
    dfs(b, r, c-1, node, res);
    b[r][c] = ch;
}
```

**Complexity:** O(m · n · 4^L) where L is longest word. Dictionary-size factor eliminated — the trie prunes.

**Interview commentary:**
- *"Brute force is O(k · 4^L) — for 10⁴ words it TLEs."*
- *"Trie shares prefixes so one board DFS finds all words simultaneously. The trie prunes any branch not represented in the dictionary."*
- *"Store `word` at the terminal instead of a boolean — makes collection O(1). Set to null after collecting to avoid duplicates."*
- *"Standard mark-unmark backtracking on the board; the trie navigation is separate."*

### Approach 3 — Trie + prune empty branches

Optimize by removing trie nodes after all words in that subtree are found. Ensures the trie shrinks as we work, so later cells have less to explore.

Marginal improvement — mentioned as a follow-up in interviews, rarely coded.

#### Complexity ladder

| Approach | Time | Space | When |
|---|---|---|---|
| DFS per word | O(k · m · n · 4^L) | O(L) | Reference / k ≤ 10 |
| **Trie + single DFS** | **O(m · n · 4^L)** | **O(dictionary chars)** | **Interview default** |
| Trie with pruning | Slightly better in practice | O(dictionary chars) | Contest / large k |

</details>

### Word Search II (Trie + Backtracking) <span class="diff diff-h">Hard</span>

*[↗ LeetCode: Word Search II](https://leetcode.com/problems/word-search-ii/)*

<ProgressCheck id="word-search-ii-trie-backtracking" />

```svg
<svg role="img" viewBox="0 0 720 260" xmlns="http://www.w3.org/2000/svg" aria-label="Diagram illustrating: Word Search II (Trie + Backtracking) Hard">
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
```
<div class="readfig"><b>How to read it:</b> The grid on the left holds the letters; the trie on the right holds all dictionary words. A DFS walk starts from every grid cell and follows adjacent cells one step at a time. At each step it also walks the trie — if the current letter isn't a trie edge from the current node, the entire branch is dead. When the DFS reaches a trie node marked "end of word," it emits that word (e.g. <code>car</code>).</div>

### Problem
Given a grid of letters and a dictionary, return **all dictionary words** that can be traced through **adjacent** cells (up/down/left/right), never reusing a cell within one word.

**Constraints:** grid up to `12×12`; up to `3·10⁴` words.

**Example 1:** grid with words `["oath","pea","eat","rain"]` → the traceable ones (e.g. `["oath","eat"]`).

**Example 2:** Board `[["a"]]`, words `["a","b"]` → `["a"]`.

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

> [key] **Key Insight** — With many query words, testing each independently is wasteful. The trie lets one grid DFS test *all* words at once: you only continue into a cell if the current character exists as a trie edge. Mark found words at terminal nodes.

> [inv] **Invariant** — The DFS position in the grid and the node in the trie always spell the same string; leaving the trie means no word can be completed down this path.

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

> [note] **Trace it** — words `["oath","pea","eat","rain"]` on a letter grid. Start from `o`: the trie has child `o`, then `a`, then `t`, then `h`, so that path can reach the terminal word `"oath"`. Start from a path like `o → a → x`: after `oa`, there is no `x` child, so the DFS returns immediately. You are not checking four words separately; one prefix walk prunes the whole dictionary.

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

> [trap] **Common Trap** — Re-adding a word for every path that reaches it. *Example:* board has multiple paths spelling `"cat"` from the same trie leaf. Without clearing `node.word` after the first find (or using a `Set<String>` result), you emit `"cat"` multiple times.

<TrapTrace title="Re-adding a word for every path that reaches it" input="'cat'" bug="board has multiple paths spelling ''cat'' from the same trie leaf. Without clearing 'node.word' after the first find (or using a 'SetltStringgt' result), you emit ''cat'' multiple times." fix="See the guidance in the trap description and the code snippet." />

> [note] **Interview script** — "I would not search each word independently because the dictionary has up to 30,000 words and many share prefixes. I build a trie once, then do board DFS while carrying the current trie node. If the next board letter is not a trie child, no dictionary word can continue, so I prune that branch. When I hit a terminal node, I record the word and clear it to avoid duplicates."

> [pat] **Pattern Connection** — "Drive a backtracking search with a trie to prune multiple targets simultaneously" is a hallmark staff-level combination of two structures.

### Time Complexity
Time O(R·C·4^L) worst but trie-pruned in practice · Space O(total chars).

Worst-case O(R·C·4^L), but trie prefix pruning avoids repeating work for shared dictionary prefixes.


### Space Complexity
O(totalChars) for the trie plus O(L) recursion stack; result output extra.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- Why `buildTrie(words)` first? — it shares all dictionary prefixes before the board DFS begins.
- Why carry `Node node` in DFS? — the grid path and trie path must advance together.
- Why `nxt == null` returns immediately? — no dictionary word has this prefix, so every continuation is impossible.
- Why `nxt.word = null` after adding? — it deduplicates a word found through multiple paths.
- Why mark `b[r][c] = '#'` and restore? — one path cannot reuse a cell, but sibling paths need the original board.

</details>

### Maximum XOR of Two Numbers (Binary Trie) <span class="diff diff-m">Medium</span>

*[↗ LeetCode: Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)*

<ProgressCheck id="maximum-xor-of-two-numbers-binary-trie" />

### Problem
Given an array, find the **maximum XOR** obtainable from any two elements.

**Constraints:** `1 ≤ n ≤ 2·10⁵`; values `0 … 2³¹−1`; aim to beat O(n²).

**Example 1:** `[3,10,5,25,2,8]` → `28` (`5 XOR 25`).

<ExamplePreview compact :input="['3', '10', '5', '25', '2', '8']" :output="['28']" />

**Example 2:** `[0]` → `0` because the only possible pair value with itself is zero.

<ExamplePreview compact :input="['0']" :output="['0']" />

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

> [key] **Key Insight** — To maximize XOR, at each bit prefer the branch with the complementary bit (they differ → contributes `1` at that position). A binary trie makes this greedy choice O(32) per query.

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

> [note] **Trace it** — Use 5-bit versions for readability: `5 = 00101`, `25 = 11001`. Querying `5`, the trie first wants `1` at the 16s bit and can take `25`'s branch, so the XOR gets a high `1`. It next wants `1` at the 8s bit and again follows `25`. Later bits contribute as available. The final path gives `00101 XOR 11001 = 11100` = `28`, better than any pair in `[3,10,5,25,2,8]`.

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

> [trap] **Common Trap** — Comparing bits in the wrong direction. *Example:* numbers `[3,10,5,25]` — XOR-max hunt greedily wants the **opposite** bit at each level from the query. Insert MSB-first; at each level, walk the child whose bit differs from the current bit (fall back if that branch doesn't exist).

<TrapTrace title="Comparing bits in the wrong direction" input="[3,10,5,25]" bug="numbers '[3,10,5,25]' — XOR-max hunt greedily wants the **opposite** bit at each level from the query" fix="Insert MSB-first; at each level, walk the child whose bit differs from the current bit (fall back if that branch doesn't exist)." />

> [note] **Interview script** — "Brute force compares every pair, but XOR is decided from the highest bit downward. I insert every number into a binary trie and, for each query number, prefer the opposite bit at each level. If the opposite branch exists, that bit of the answer becomes 1; otherwise I take the same-bit branch. The width is constant at 32, so the total time is O(n)."

> [pat] **Pattern Connection** — Binary tries also answer *Maximum XOR With an Element From Array* (offline with a value bound) and range-XOR counting (store subtree counts). It is the bitwise cousin of prefix-tree search: different alphabet, same shared-path idea.

### Time Complexity
Time O(n·32) · Space O(n·32).

O(n·32), which is O(n) for fixed-width Java integers.


### Space Complexity
O(n·32) trie nodes in the worst case.

<details class="learnings">
<summary><strong>Learnings — points to remember</strong></summary>

- Why walk bits from 31 down to 0? — higher XOR bits dominate every combination of lower bits.
- Why `want = bit ^ 1`? — XOR gets a 1 exactly when the two bits differ.
- Why set `cur |= (1 << b)` only when `want` exists? — that bit can be made 1 only if an opposite branch is available.
- Why insert all numbers first? — each query can choose among every potential partner in the array.
- Why pairing with itself is harmless here? — self-XOR is 0, which cannot beat a positive maximum pair.

</details>

## In the wild — `java.util.jar.JarFile` manifest trie & Cisco IP routing

**`java.util.jar.JarFile`** uses a trie internally to accelerate manifest lookups when verifying signed JARs. Entries are indexed by their path (`META-INF/MANIFEST.MF`, `META-INF/VERSIONS/9/foo.class`), stored in a shared-prefix trie keyed on path segments. Looking up any entry is O(path length) regardless of jar size.

```java
/* java.base/share/classes/java/util/jar/JarFile.java — paraphrased */
class JarVerifier {
    /* The trie maps path-prefixes to code-signer sets, enabling
       O(L) lookup during verifyMultiRelease(). Without the trie,
       each lookup would scan all entries O(n). For a jar with
       10k entries, that's a 100x speedup on verification. */
}
```

**Four more real-world trie sightings:**

1. **Cisco IP routing tables** are **Patricia tries** (compressed trie / radix tree) over IP address bit prefixes. Each router has one trie per routing table; the ASIC walks the trie in one clock cycle per bit.
2. **Ethereum's state tree** is a **Merkle Patricia trie** — each node also stores a cryptographic hash of its subtree, enabling O(log n) proof-of-inclusion for any account state.
3. **Bash/Zsh tab-completion** uses an in-memory trie of filesystem paths and command names, walked once per keystroke to generate suggestions.
4. **Aho-Corasick string matching** (used by `grep -F` and most antivirus pattern matchers) builds a trie of patterns, augmented with "failure links" that generalize KMP to multiple patterns simultaneously.

## False friends — when "prefix lookup" doesn't want a trie

Tries are the right answer for exactly one access pattern: *shared-prefix retrieval*. These lookalikes have different access patterns and want different structures.

- **Exact-match lookup, no prefix queries** — `HashSet<String>` is faster (one hash) and uses less memory (no per-character node overhead). Only switch to trie when prefix / wildcard / streaming semantics matter.
- **Substring or suffix search** — tries are prefix-first. Use **suffix automaton**, **suffix array**, or **Aho-Corasick** for substring queries. Reversing the inserted strings lets you do suffix queries, but only in the simplest cases.
- **Range queries over whole words** — `TreeMap<String, V>` / `TreeSet<String>` supports `subMap(from, to)` in O(log n), cleaner than DFS over trie subtrees.
- **Massive alphabet (Unicode)** — 26-pointer arrays explode. Use `HashMap<Character, Node>` per node (sparse) or a **ternary search tree** (3 pointers per node, 10× memory savings).
- **Memory-critical with lots of duplicate suffixes** — **DAWG / DAFSA** merges equivalent suffixes, cutting memory 10-100× for English word lists.
- **Just one or two lookups** — the trie build cost (O(total characters)) is wasted. Linear scan is fine.

### Visual 1: HashSet wins on exact-match-only lookup

The entire point of a trie is prefix sharing. If you never query prefixes, you're paying for machinery you don't use:

```text
   Words = ["apple", "application", "banana", "cat"]

   Trie structure (26-children arrays per node):
     root
     ├── a → p → p → l → e$                             5 nodes, 5 arrays of 26 slots = 130 slots
     │             → l → i → c → a → t → i → o → n$     7 more nodes, 7 × 26 = 182 slots
     ├── b → a → n → a → n → a$                         6 nodes, 156 slots
     └── c → a → t$                                     3 nodes, 78 slots

     total: ~500 slots × 4 bytes each = 2 KB
     per-lookup: walk up to 11 chars, 11 pointer dereferences

   HashSet<String>:
     stores 4 strings as string objects
     total: ~200 bytes (hash + metadata)
     per-lookup: one hashCode + one equals, ~15 chars touched

   10x more memory for the trie, more pointer-chasing per lookup — in exchange
   for prefix queries you aren't making.
```

The decision: do any queries actually use prefixes? "Does this word exist" is exact match (HashSet). "Does any inserted word start with ‛app'?" is a prefix query (trie wins). "Return all words with prefix ‛app'" definitely needs the trie — HashSet would need a full scan.

### Visual 2: substring search isn't a trie problem

A trie indexes prefixes of inserted strings. Substring search needs the dual — suffixes of a single long text:

```text
   Problem: given text "banana", search for substring "nan"

   Trie of ["banana"]:
     root → b → a → n → a → n → a$
     To find "nan" we'd need to START the walk mid-trie. The trie's
     structure anchors every path at the root.

   Suffix automaton / suffix array of "banana":
     stores all suffixes "banana", "anana", "nana", "ana", "na", "a"
     indexed by the first character, searchable in O(|pattern|) or O(|pattern| log n)
     "nan" lookup: finds the suffix "nana" starting at position 2, match!

   Alternative — Aho-Corasick for multiple patterns at once:
     builds a trie of pattern words with failure links (KMP-style)
     scans the text once, reports every match of every pattern
     this is "grep -F" with multiple needles.
```

The signal: are you looking for the pattern as a *prefix of inserted keys*, or as a *substring inside a single haystack*? Trie answers the first; suffix structures answer the second. A quick hack when `|pattern| × |patterns|` is small: reverse the strings and build a trie — that answers "is this a *suffix* of some inserted key", a weak form of substring search. For general substring, you need the real tool.

## Recognition drill

<RecognitionDrill pattern="trie-pattern" :count="10" />

## Advanced — follow-ups and failure modes

<details>
<summary><strong>What if the alphabet is huge (Unicode, 1M+ code points)?</strong></summary>

A 1M-pointer array per node is absurd — most slots are empty. Three alternatives:
1. **`HashMap<Character, Node>` per node** — only allocates pointers that are actually used. Memory becomes O(sum of distinct chars encountered); CPU is O(L) with a hash per step instead of array index.
2. **Ternary Search Tree** (TST, Bentley-Sedgewick 1997) — 3 pointers per node (`lo`, `mid`, `hi`) representing a BST of children. 10× memory savings; comparable O(L log σ) query time.
3. **Compressed trie / Patricia / Radix tree** — collapse single-child chains into edges labeled with substrings. 2-10× node savings on sparse dictionaries.
</details>

<details>
<summary><strong>What if you need to DELETE words?</strong></summary>

Walk the path; set `end = false` on the terminal. If you want to actually reclaim memory, walk back up the path removing child pointers that no longer lead to any `end == true` node. O(L) time; usually not worth coding unless memory is tight.

For a dynamic dictionary with heavy deletes, a **DAWG** doesn't support deletion natively (merged suffixes become shared, so deleting one word may affect others). Rebuild the DAWG periodically, or stick with a plain trie.
</details>

<details>
<summary><strong>What if queries interleave: "insert, search, insert, search..." on a massive stream?</strong></summary>

Plain trie supports this directly — each op is O(L). Memory grows O(total distinct chars). For bounded memory on an infinite stream, use **LRU cache + trie** or **Bloom filter + trie fallback**: the Bloom filter answers negative queries in O(1); the trie resolves positives.

A **persistent trie** (functional data structure) answers "what was in the trie at time t?" by keeping version pointers. Each insert creates O(L) new nodes but shares the rest.
</details>

<details>
<summary><strong>What if the "word" is actually a sequence of integers, not characters?</strong></summary>

The trie structure is unchanged — just the alphabet differs. For a sequence of 32-bit ints, each node has `HashMap<Integer, Node>`. Common application: **n-gram language models** store sequences of word IDs; frequency and probability live at the terminals.

A **suffix array / suffix automaton** is often a better fit for integer-sequence substring queries — they handle any alphabet in O(n log n) build and O(m) query.
</details>

<details>
<summary><strong>What if you need to answer "longest common prefix of all stored words"?</strong></summary>

Walk from root; follow the single child while this node is not a terminal and has exactly one child. The deepest such node's path is the longest common prefix. O(L) where L is the LCP length.

For the related "longest common substring over all stored words," use a **generalized suffix tree / automaton** — a classical O(sum of lengths) algorithm.
</details>

### Breaking point

Trie **stops being optimal** when:
- The dictionary has only a few short words (hash set is simpler, faster).
- You need exact-match lookup only (hash wins on memory and CPU).
- You need substring/suffix search (use suffix array/automaton).
- Memory is critically tight and alphabet is large (TST, DAWG, Patricia).
- Queries require range or sorted iteration (`TreeMap` is cleaner).
- The input is a one-shot lookup — build cost dominates query cost.

### Three cross-pattern problems

- [Stream of Characters (1032)](https://leetcode.com/problems/stream-of-characters/) — trie over REVERSED words + walk the stream backward. Trie meets streaming.
- [Design Add and Search Words Data Structure (211)](https://leetcode.com/problems/design-add-and-search-words-data-structure/) — trie with wildcard `.` matching via branched DFS. Trie meets backtracking.
- [Palindrome Pairs (336)](https://leetcode.com/problems/palindrome-pairs/) — trie of reversed words + palindrome-check at each walk step. Trie meets string manipulation.

---

## Check your understanding

<Quiz pattern-id="trie" :questions="mastery5" />

<PrintButton />

<RelatedPatterns pattern-id="trie-pattern" />
