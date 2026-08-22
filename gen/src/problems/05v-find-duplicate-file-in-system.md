# Hashing — Find Duplicate File in System

*[↗ LeetCode: Find Duplicate File in System](https://leetcode.com/problems/find-duplicate-file-in-system/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

Given a list of `"dir file1.ext(content) file2.ext(content) …"` strings, group files with identical content.

---

## Approach 1 — Hash by content
```java
List<List<String>> findDuplicate(String[] paths) {
    Map<String, List<String>> byContent = new HashMap<>();
    for (String line : paths) {
        String[] parts = line.split(" ");
        String dir = parts[0];
        for (int i = 1; i < parts.length; i++) {
            int lp = parts[i].indexOf('(');
            String name = parts[i].substring(0, lp);
            String content = parts[i].substring(lp + 1, parts[i].length() - 1);
            byContent.computeIfAbsent(content, k -> new ArrayList<>()).add(dir + "/" + name);
        }
    }
    List<List<String>> out = new ArrayList<>();
    for (List<String> g : byContent.values()) if (g.size() > 1) out.add(g);
    return out;
}
```

**Complexity** — Time **O(total input size)**; Space **O(total input size)**.

## Follow-ups

- **Very large files:** hash a rolling checksum (MD5/SHA1) instead of full content; compare buckets by re-hashing suspects fully.
- **Filesystem streaming:** compare (size, first-1KB, sha256) triple to avoid touching non-collisions.
- **Symlinks:** normalize `readlink` before grouping.

---

## Complexity summary

| Approach | Time | Space | Interview grade |
|---|---|---|---|
| Hash by content | O(total input size) | O(total input size) | primary |

## When to use which

- **Ship this** → Hash by content (O(total input size), O(total input size)). The pattern's standard solution.

## Related problems

- [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — same canonical-key style
