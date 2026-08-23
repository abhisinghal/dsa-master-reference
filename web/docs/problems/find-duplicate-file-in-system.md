# Hashing — Find Duplicate File in System

*[↗ LeetCode: Find Duplicate File in System](https://leetcode.com/problems/find-duplicate-file-in-system/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

&lt;CompanyTags companies="Google, Amazon, Dropbox" /&gt;

Given `"dir file1.ext(content) file2.ext(content) …"` strings, group files with identical content.

**Example 1** — Various paths → grouped by content.

**Constraints** — total input ≤ 2·10⁷.


&lt;Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its ’canonical form’ — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For ’first duplicate’, a `HashSet` and single-pass `add()` is enough."
/&gt;
---

&lt;MarkSolved problem-slug="find-duplicate-file-in-system" /&gt;


## Approach — Hash by content (canonical)



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
    for (var g : byContent.values()) if (g.size() > 1) out.add(g);
    return out;
}
```



**Complexity** — Time **O(total input)**; Space **O(total input)**.

## Follow-ups

- **Very large files** → hash by SHA256 of chunks.
- **Filesystem streaming** → compare `(size, sha1(first 1KB), sha256)` triple.
- **Symlinks** → normalize `readlink` before grouping.

---

## Try it yourself

<JavaRunner problem-slug="find-duplicate-file-in-system" />

## Complexity summary

| Approach | Time | Space | Grade |
|---|---|---|---|
| Content hash | **O(N)** | O(N) | canonical |

## When to use which

- **Small files, batch mode** → full content hash.
- **Huge files** → chunked hash + verify collisions.

&lt;AiCompanion problem-slug="find-duplicate-file-in-system" pattern-hint="hashing" /&gt;

## Related problems

- [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — canonical-key style

&lt;FeedbackWidget problem-slug="find-duplicate-file-in-system" /&gt;
