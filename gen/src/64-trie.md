# Tries (Prefix Trees)

## Why tries exist — the story

A trie exists because dictionaries waste work when words share beginnings. Imagine inserting `app`, `apple`, `apply`, and `bat`. A hash set can tell you whether `apple` is a complete word, but it cannot naturally answer "does anything start with `appl`?" unless you precompute prefixes or scan many words. A trie stores the shared prefix once: `a → p → p → l` is one hallway, and both `apple` and `apply` branch only at the final letter.

Trace a tiny lookup. Insert `app` first: create nodes `a`, `p`, `p`, then mark the last node as a word. Insert `apple`: walk the existing `a → p → p`, then add `l → e` and mark `e`. Now `search("app")` is true because the third node has the word flag. `startsWith("ap")` is true because the path exists even though the `p` at depth 2 is not a complete word. `search("ap")` is false because a prefix is not automatically a word. That one flag is the difference between "path exists" and "word ends here."

The main implementation choice is how each node stores children. For lowercase English, `Node[] next = new Node[26]` is fast and simple: index `c - 'a'` directly. But if your alphabet is Unicode, file paths, arbitrary bytes, or only a few children per node, an array can waste memory. A `HashMap<Character, Node>` stores only existing edges, at the cost of hashing and more object overhead per edge. This Part III chapter is about those internals: node layout, operations, memory tradeoffs, and clean Java skeletons. The trie pattern chapter shows higher-level applications like Word Search II and binary XOR tries.

> [key] **Key Insight** — A trie separates two questions: "can I walk this prefix?" and "is this prefix a complete stored word?" The path answers the first; the terminal flag answers the second.

### Recognize by
- `insert`, `search`, `startsWith` API requirements
- repeated prefix queries against a stable dictionary
- autocomplete, command lookup, root-word replacement, or namespace/path matching
- wildcard search where `.` or `*` branches through possible children
- counting how many words share a prefix, requiring counters on nodes
- lexicographic collection of words under a prefix


<TrieWalkAnim />


### When NOT to use it
- You only need exact membership; `HashSet<String>` is simpler and usually faster.
- You need suffix or substring queries; reverse the strings or use a suffix-specific structure.
- The dictionary is small and memory matters more than asymptotic prefix time.
- The alphabet is huge and dense arrays would waste most child slots.
- You need sorted range queries over whole words; a sorted list or `TreeSet` may be easier.

## How to use it — standard node and skeleton

Start with the lowercase `a-z` version. It is the one most LeetCode trie problems expect and the one easiest to code correctly under interview pressure.

```java
class TrieNode {
    TrieNode[] next = new TrieNode[26];
    boolean isWord;
}

TrieNode root = new TrieNode();

void insert(String word) {
    TrieNode cur = root;
    for (char ch : word.toCharArray()) {
        int i = ch - 'a';
        if (cur.next[i] == null) cur.next[i] = new TrieNode();
        cur = cur.next[i];
    }
    cur.isWord = true;
}

TrieNode walk(String s) {
    TrieNode cur = root;
    for (char ch : s.toCharArray()) {
        int i = ch - 'a';
        if (cur.next[i] == null) return null;
        cur = cur.next[i];
    }
    return cur;
}
```

Then implement `search(word)` as `walk(word) != null && node.isWord`, and `startsWith(prefix)` as `walk(prefix) != null`.

> [inv] **Implementation invariant** — every edge corresponds to exactly one character, and the node reached after consuming a string represents that exact prefix. `isWord` is independent of whether the node has children.

### Root node mental model

The root does not represent a real character; it represents the empty prefix. That detail removes a lot of off-by-one confusion. After reading zero characters, you are at root. After reading one character, you are at the node for that one-character prefix. After reading all characters of `word`, the current node is exactly where the terminal flag belongs.

This also explains empty-string behavior. Most LeetCode trie problems do not insert empty strings, but a production trie can support them by setting `root.word = true`. Then `search("")` checks the root flag, while `startsWith("")` is true because every word starts with the empty prefix. You usually do not need this in interviews, but the model helps you reason cleanly.

## Node layout choices

| Layout | Best for | Tradeoff |
|---|---|---|
| `Node[26]` | lowercase `a-z`, many operations, predictable alphabet | fastest indexing, but 26 references per node even when sparse |
| `HashMap<Character, Node>` | large/sparse alphabets, Unicode-ish inputs, file paths | stores only real edges, but each lookup hashes and allocates more objects |
| `TreeMap<Character, Node>` | need children in sorted order while traversing | ordered, but O(log alphabet) per edge |
| compressed trie/radix tree | long chains with few branches | saves nodes, harder to implement in interviews |

> [note] **Rule of thumb** — In interviews, use the 26-array when constraints say lowercase English. Mention the map version if the interviewer changes the alphabet.

### Array-backed vs map-backed by example

Suppose you insert `ant`, `and`, and `as`. At the root, only child `a` is used. Under `a`, two children are used: `n` and `s`. Under `an`, two children are used: `t` and `d`. With `Node[26]`, each of those nodes still owns 26 references, most of them null. That is fine for LeetCode constraints because indexing is simple and fast. In a dictionary with millions of sparse Unicode keys, those null slots become expensive.

A map-backed node changes only the child access:

```java
class MapNode {
    Map<Character, MapNode> next = new HashMap<>();
    boolean word;
}

void insert(MapNode root, String w) {
    MapNode cur = root;
    for (char c : w.toCharArray()) {
        cur = cur.next.computeIfAbsent(c, k -> new MapNode());
    }
    cur.word = true;
}
```

Use this version when the alphabet is unknown or sparse. The algorithmic idea is identical: walk the edge for each character, create it if inserting, and mark the final node.

---

## Implement Trie <span class="diff diff-m">Medium</span>


*[↗ LeetCode: Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)*

<ProgressCheck id="implement-trie" />

<TrieOps />

```svg
<svg viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="trie-ar" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--dsa-primary)"/>
    </marker>
  </defs>
  <rect x="0" y="0" width="400" height="250" rx="12" fill="var(--dsa-bg)"/>
  <text x="200" y="24" text-anchor="middle" font-family="var(--dsa-font)" font-size="13" font-weight="700" fill="var(--dsa-primary)">shared prefix: c → a branches to t* and r*</text>
  <g stroke="var(--dsa-primary)" stroke-width="var(--dsa-arrow-stroke)" fill="none" marker-end="url(#trie-ar)">
    <line x1="86" y1="122" x2="124" y2="122"/><line x1="168" y1="122" x2="206" y2="122"/>
    <line x1="250" y1="112" x2="286" y2="84"/><line x1="250" y1="132" x2="286" y2="160"/>
  </g>
  <g font-family="var(--dsa-font)" font-size="12" font-weight="700" text-anchor="middle" fill="var(--dsa-neutral)">
    <text x="105" y="112">c</text><text x="187" y="112">a</text><text x="268" y="88">t</text><text x="268" y="158">r</text>
  </g>
  <g font-family="var(--dsa-font)" text-anchor="middle" font-size="17" font-weight="700" fill="var(--dsa-ink)">
    <rect x="42" y="100" width="44" height="44" rx="7" fill="var(--dsa-neutral-soft)" stroke="var(--dsa-neutral-line)" stroke-width="1.6"/><text x="64" y="127" font-size="11">root</text>
    <rect x="124" y="100" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="146" y="128">c</text>
    <rect x="206" y="100" width="44" height="44" rx="7" fill="var(--dsa-primary-soft)" stroke="var(--dsa-primary)" stroke-width="1.6"/><text x="228" y="128">a</text>
    <rect x="286" y="58" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="308" y="86">t</text>
    <rect x="286" y="142" width="44" height="44" rx="7" fill="var(--dsa-success-soft)" stroke="var(--dsa-success)" stroke-width="1.6"/><text x="308" y="170">r</text>
  </g>
  <g font-family="var(--dsa-font)" font-size="17" font-weight="700" text-anchor="middle" fill="var(--dsa-success)">
    <text x="336" y="72">*</text><text x="336" y="156">*</text>
  </g>
  <text x="200" y="220" text-anchor="middle" font-family="var(--dsa-font)" font-size="11.5" font-style="italic" fill="var(--dsa-neutral)">search(cat) and search(car) reuse the same c,a walk.</text>
</svg>
```

<div class="readfig"><b>How to read it:</b> each edge = one char; end-of-word flag on terminal nodes.</div>

### Problem

Implement a trie supporting `insert(word)`, `search(word)` (exact word), and `startsWith(prefix)`.

**Constraints:** up to `3·10⁴` calls; lowercase `a–z`; each call O(word length).

**Example:** insert `"apple"`; then `search("apple")` → true, `search("app")` → false, `startsWith("app")` → true.

**Example 1:** insert("apple"), search("apple") -> true, search("app") -> false.

**Example 2:** startsWith("app") -> true after inserting "apple".

### Solution — brute force

The simplest design stores every inserted word in a `HashSet<String>`. `insert` and `search` are easy, but `startsWith(prefix)` must scan all words unless you also store every possible prefix.

```java
class TrieBrute {
    Set<String> words = new HashSet<>();
    void insert(String w) { words.add(w); }
    boolean search(String w) { return words.contains(w); }
    boolean startsWith(String p) {
        for (String w : words) if (w.startsWith(p)) return true;
        return false;
    }
}
```

This gives average O(L) exact search but O(numberOfWords · prefixLength) prefix checks. A trie makes both exact and prefix lookup O(L), where `L` is the query length.

You could precompute every prefix in a second hash set: insert `apple` and also store `a`, `ap`, `app`, `appl`, `apple`. Then `startsWith` becomes O(L), but memory becomes the total number of prefixes, and you still cannot easily enumerate completions under a prefix. A trie is the structured version of that prefix set: it shares prefix objects instead of storing each prefix string separately.

### Solution — optimized

**Pattern:**
Walk one character at a time from the root. Create missing nodes during insertion; reject immediately during lookup when an edge is missing. Exact search checks the terminal flag; prefix search only checks path existence.

**Operation behavior:**
| Operation | Missing edge means | Final node requirement |
|---|---|---|
| `insert(word)` | create the child and continue | set `word = true` |
| `search(word)` | return false immediately | final node must have `word = true` |
| `startsWith(prefix)` | return false immediately | path existence is enough |

Keep this table in mind when coding. The loops are almost identical; only the missing-edge behavior and the final check differ. A common clean implementation is to put the shared walking logic in a private helper, as the solution below does.

**Java:**
```java
class Trie {
    private static class Node {
        Node[] next = new Node[26];
        boolean word;
    }
    private final Node root = new Node();

    public void insert(String w) {
        Node cur = root;
        for (char c : w.toCharArray()) {
            int i = c - 'a';
            if (cur.next[i] == null) cur.next[i] = new Node();
            cur = cur.next[i];
        }
        cur.word = true;
    }
    public boolean search(String w)      { Node n = walk(w); return n != null && n.word; }
    public boolean startsWith(String p)  { return walk(p) != null; }

    private Node walk(String s) {
        Node cur = root;
        for (char c : s.toCharArray()) {
            cur = cur.next[c - 'a'];
            if (cur == null) return null;
        }
        return cur;
    }
}
```

> [note] **Trace it** — Insert `"app"` and `"apple"`. The second insertion reuses the nodes for `a`, first `p`, and second `p`, then creates `l` and `e`. `search("app")` walks three edges and returns true because that node's `word` flag is set. `search("ap")` walks two edges but returns false because the prefix node is not a word. `startsWith("appl")` walks four edges and returns true because the path exists.

<CodeTrace
  title="Implement Trie — insert 'app', 'apple'; then queries"
  :values="['a','p','p','l','e']"
  :windowKeys="['depth']"
  :cellWidth="42"
  :steps='[
    { pointers: { depth: 0 }, vars: { op: "insert app", path: "a", word: false }, note: "create a node", added: [0] },
    { pointers: { depth: 1 }, vars: { op: "insert app", path: "a→p", word: false }, note: "create p", added: [0,1] },
    { pointers: { depth: 2 }, vars: { op: "insert app", path: "a→p→p ★", word: true }, note: "mark end-of-word", added: [0,1,2] },
    { pointers: { depth: 3 }, vars: { op: "insert apple", path: "a→p→p→l", word: false }, note: "reuse first 3 nodes, create l", added: [0,1,2,3] },
    { pointers: { depth: 4 }, vars: { op: "insert apple", path: "l→e ★" }, note: "create e, mark end", added: [0,1,2,3,4] },
    { pointers: { depth: 1 }, vars: { op: "search ap", found: false }, note: "walks 2 edges but no ★ → false" },
    { pointers: { depth: 3 }, vars: { op: "startsWith appl", found: true }, note: "path exists → true" }
  ]'
/>

### Time Complexity

O(L) per insert/search/startsWith.

Original summary: Insert/search/prefix O(L) · Space O(total chars × alphabet).

### Space Complexity

O(total inserted characters * alphabet factor) in the worst case.

> [trap] **Common Trap** — `isEnd` only on leaves. *Example:* insert `"car"` then `"cars"`. If you only mark `s` as end, `search("car")` returns false. `isEnd` marks a **word boundary**, independent of children — set it on `r` too.

<TrapTrace title="'isEnd' only on leaves" input="'car'" bug="insert ''car'' then ''cars''. If you only mark 's' as end, 'search('car')' returns false. 'isEnd' marks a **word boundary**, independent of children — set it on 'r' too." fix="See the guidance in the trap description and the code snippet." />

> [trap] **Alphabet Trap** — The `c - 'a'` index assumes lowercase English. If input can contain uppercase, digits, hyphens, or Unicode, normalize first or switch to a map-backed node.

> [note] **Interview script** — "I will store a root node whose children represent the next character. Insert creates missing children and marks the final node as a complete word. Search walks the same path and also checks the final flag, while `startsWith` only needs the path to exist. Because each operation touches one node per character, the time is O(length of input)."

> [pat] **Pattern Connection** — Adding a `count` per node supports *count words with prefix*; a wildcard `.` in search (*Add and Search Word*) branches over all children at that position (DFS on the trie). The pattern chapter uses this same structure as a component inside larger algorithms.

### Learning notes

- Why array children? Lowercase-only alphabets make arrays 3-5x faster than maps.
- Why isEnd? Prefixes and full words differ.
- Why root has no char? It represents empty prefix.
- Why c-'a'? Compact 0..25 index.
- Why trie over HashSet? Prefix queries avoid scanning words.

#### Same pattern, new tweaks

| Variation | The one thing that changes | Time |
|---|---|---|
| [Add and Search Word (wildcard `.`)](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | on a `.`, recurse into *all* children at that position (DFS instead of a single step) | O(26^wildcards · L) |
| [Replace Words](https://leetcode.com/problems/replace-words/) | walk the trie while scanning each word and stop at the shortest root prefix | O(total sentence chars) |
| [Map Sum Pairs](https://leetcode.com/problems/map-sum-pairs/) | store a value at each terminal and maintain prefix sums or subtree traversal | O(L) update/query with sums |
| [Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/) | accept a word only if every one of its prefixes is also a stored word | O(total chars) |
| [Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/) | keep top suggestions under each prefix, or DFS children in sorted order | O(total chars + output) |

## Implementation upgrades you can mention

For counting prefixes, add two counters: `pass` increments on every node you pass during insert, and `end` increments at the terminal node. Then `countWordsStartingWith(prefix)` returns `walk(prefix).pass`, and `countWordsEqualTo(word)` returns `walk(word).end`. For deletion, decrement along the path and optionally prune nodes whose `pass` becomes zero. The important part is to only delete when the word exists; otherwise counters go negative and future prefix queries lie.

```java
class CountNode {
    CountNode[] next = new CountNode[26];
    int pass, end;
}

void insert(CountNode root, String w) {
    CountNode cur = root;
    cur.pass++;
    for (char c : w.toCharArray()) {
        int i = c - 'a';
        if (cur.next[i] == null) cur.next[i] = new CountNode();
        cur = cur.next[i];
        cur.pass++;
    }
    cur.end++;
}
```

Trace `insert("app")`, `insert("apple")`: the nodes for `a`, `p`, `p` have `pass = 2`, the terminal node for `app` has `end = 1`, and the terminal node for `apple` has `end = 1`. A prefix count for `app` returns 2, while an exact count for `app` returns 1.

For memory-heavy dictionaries, switch from `Node[26]` to `Map<Character, Node>`. The code shape stays the same, but `cur.next[i]` becomes `cur.children.get(ch)` and missing child creation uses `computeIfAbsent`. This is slower per character but can save a lot of empty references when most nodes have one or two children.

For lexicographic output, DFS children from `'a'` to `'z'`. With the array layout, that order is natural. With a `HashMap`, you must sort keys or use `TreeMap` if ordered traversal is part of the API.

### Deletion and pruning

Deletion is where many otherwise-correct trie implementations break. There are two different meanings of "delete." If duplicates are not allowed, deleting `word` only needs to clear the terminal flag, and optionally remove dead nodes. If duplicates are allowed, deletion decrements `end` at the terminal node and `pass` along the path. You should not physically remove a node if another word still passes through it.

Example: insert `car` and `cart`, then delete `cart`. The nodes `c → a → r` must remain because `car` is still a word. Only the `t` child can be pruned. If you delete the whole path backward without checking whether nodes have children or terminal counts, `search("car")` breaks.

> [trap] **Deletion Trap** — Never prune a node just because the deleted word used it. Prune only when no word ends there and no child remains, or when a maintained `pass` count drops to zero.

### Testing checklist

Before you trust a trie implementation, run a tiny set of overlapping words:

```text
insert app
insert apple
search app        -> true
search ap         -> false
startsWith ap     -> true
startsWith apple  -> true
search apples     -> false
```

Then test sibling branches: insert `bat` and `bad`; both should survive. Finally test character assumptions: if the input includes `A` or `-`, the array index `c - 'a'` is invalid unless you normalize.

### Space analysis without hand-waving

Trie space is often written as O(total characters), but the constant matters. With an array node, each node carries 26 references plus a boolean. If 10,000 words share the prefix `inter`, those five nodes are shared and the trie saves repeated prefix storage. If 10,000 random strings share almost no prefixes, the trie can have nearly one node per character and many empty child slots.

That does not make tries bad; it tells you when to choose the layout. For lowercase interview constraints, the fixed array is predictable and avoids hashing. For a large alphabet, use a map. For a memory-sensitive system with long single-child chains, consider a compressed trie that stores edge labels like `"ation"` instead of one node per character. You rarely implement that in a LeetCode interview, but mentioning it shows you understand the engineering tradeoff.

### Keeping this chapter distinct from trie patterns

This chapter answers \"how is the data structure built?\" The pattern chapter answers \"where do I plug it into a larger algorithm?\" Word Search II, XOR tries, and stream suffix matching all rely on the same internals shown here, but their difficulty comes from combining the trie with DFS, greedy bit walking, or online queries. If you can implement `walk` confidently, those pattern problems become compositions instead of brand-new ideas.

> [key] **Final mental model** — A trie is not magic compression and it is not always smaller than a set. It buys predictable prefix-time by paying for nodes along shared paths. Use it when prefix behavior is the product requirement, not just because strings are present.
