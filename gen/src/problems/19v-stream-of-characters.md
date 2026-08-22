# Trie — Stream of Characters

*[↗ LeetCode: Stream of Characters](https://leetcode.com/problems/stream-of-characters/)* · <span class="diff diff-h">Hard</span> · [pattern chapter →](/patterns/trie-pattern)

Streaming interface: after each `query(c)`, return true iff any word in the dictionary matches a **suffix** of the stream so far.

## Approach — Trie of REVERSED words, walk stream in reverse

**Insight.** Checking "does any word end at position i in the stream?" = "does any *reversed word* start at position i and read backwards?". Insert reversed words into the trie; on each query, walk backward through the buffered stream.

```java
class StreamChecker {
    static class Node { Map<Character, Node> ch = new HashMap<>(); boolean end; }
    Node root = new Node();
    StringBuilder stream = new StringBuilder();
    public StreamChecker(String[] words) {
        for (String w : words) {
            Node cur = root;
            for (int i = w.length() - 1; i >= 0; i--) cur = cur.ch.computeIfAbsent(w.charAt(i), k -> new Node());
            cur.end = true;
        }
    }
    public boolean query(char c) {
        stream.append(c);
        Node cur = root;
        for (int i = stream.length() - 1; i >= 0; i--) {
            cur = cur.ch.get(stream.charAt(i));
            if (cur == null) return false;
            if (cur.end) return true;
        }
        return false;
    }
}
```

**Complexity** — Time **O(max_word_len)** per query; Space **O(D)** for dictionary.

## Related problems

- [Word Search II](/problems/trie-word-search-ii)
- [Design Add and Search Words](/problems/design-add-and-search-words-data-structure)
