## The Pattern

A trie stores strings by shared prefixes. Each node represents a prefix, `children[26]` follows the next lowercase character, and `isEnd` distinguishes a complete word from a mere prefix. The shape turns prefix queries from repeated substring/hash work into one character walk.

!!! pattern "Recognition signals"
    You need `insert`, exact lookup, prefix lookup, dictionary pruning during DFS, autocomplete-style enumeration, or many queries over a mostly stable word set.

```diagram
{"type":"tree","values":["","c","d","a","o",null,null,"t","r","g"],"highlights":{"7":"green","8":"green","9":"green"},"edge_highlights":[[0,1],[0,2],[1,3],[1,4],[3,7],[3,8],[4,9]],"labels":{"0":"root","1":"c","2":"d","3":"a","4":"o","7":"t*","8":"r*","9":"g*"}}
```

## The Invariant

After inserting a word, every prefix of that word exists as a path from the root, and only the terminal node has `isEnd = true`. During search, after consuming `i` characters, the current node represents exactly `word.substring(0, i)`; a missing child proves no stored word has that prefix.

## Template

```java
final class Trie {
    private static final class Node {
        Node[] child = new Node[26];
        boolean isEnd;
    }

    private final Node root = new Node();

    void insert(String word) {
        Node cur = root;
        for (char ch : word.toCharArray()) {
            int idx = ch - 'a';
            if (cur.child[idx] == null) cur.child[idx] = new Node();
            cur = cur.child[idx];
        }
        cur.isEnd = true;
    }

    boolean search(String word) {
        Node node = walk(word);
        return node != null && node.isEnd;
    }

    boolean startsWith(String prefix) {
        return walk(prefix) != null;
    }

    private Node walk(String s) {
        Node cur = root;
        for (char ch : s.toCharArray()) {
            int idx = ch - 'a';
            if (idx < 0 || idx >= 26 || cur.child[idx] == null) return null;
            cur = cur.child[idx];
        }
        return cur;
    }
}
```

## Worked Recognition

- **Implement Trie (Module 13)**: the direct pattern. `insert`, `search`, and `startsWith` are all O(L), where L is the query length, independent of dictionary size after the structure is built.
- **Word Search II (Module 13)**: combine a trie with grid DFS. DFS carries the trie node; if the next board character has no child, prune the entire branch before building strings or probing a hash set.
- **Word Search (Module 6)** contrast: a single target word needs only backtracking. A trie becomes valuable when the grid is searched against many words sharing prefixes.

## Complexity

!!! complexity "Complexity"
    **T:** `insert`, `search`, and `startsWith` are O(L). Building a dictionary is O(total characters). Trie-guided grid DFS is bounded by board DFS but heavily pruned by missing prefixes. **S:** O(total trie nodes), at most O(total characters · alphabet references).

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Confusing prefix existence with word existence, forgetting `isEnd`, allocating `HashMap` children when a fixed `Node[26]` is faster and simpler for lowercase English, or failing to de-duplicate found words in trie + DFS solutions.

## When NOT to use it

Avoid tries for one-off exact lookups where `HashSet<String>` is enough, for huge Unicode alphabets without compression, or when memory is tighter than query latency. A trie pays for shared prefixes; no sharing means many nodes.
