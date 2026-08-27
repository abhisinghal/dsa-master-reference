# Hashing — Find Duplicate File in System

*[↗ LeetCode: Find Duplicate File in System](https://leetcode.com/problems/find-duplicate-file-in-system/)* · <span class="diff diff-m">Medium</span> · [pattern chapter →](/patterns/hashing)

<CompanyTags companies="Google, Amazon, Dropbox" />

Given `"dir file1.ext(content) file2.ext(content) …"` strings, group files with identical content.

**Example 1** — `paths=["root/a 1.txt(abcd) 2.txt(efgh)","root/c 3.txt(abcd) 4.txt(efgh)"]` → `[["root/a/1.txt","root/c/3.txt"],["root/a/2.txt","root/c/4.txt"]]`
**Example 2** — `paths=["root/a 1.txt(abcd) 2.txt(efgh)"]` → `[]` (no duplicates)
**Example 3** — `paths=["a 1(x) 2(x)","b 3(x)"]` → `[["a/1","a/2","b/3"]]` (three files, same content)

**Constraints** — total input ≤ 2·10⁷ chars. Brute pairwise content comparison is O(N²) where N = total input size = 4·10¹⁴ — universe-age. Hash by content is O(N).


<Hints
  hint1="What can you look up in O(1)? Complement, canonical key, or seen-before?"
  hint2="Map each element to its 'canonical form' — sorted string for anagrams, letter-diff pattern for shifts, prefix sum for range problems."
  hint3="For 'first duplicate', a `HashSet` and single-pass `add()` is enough."
/>
---

<MarkSolved problem-slug="find-duplicate-file-in-system" /> <Bookmark problem-slug="find-duplicate-file-in-system" />

<InterviewTimer problem-slug="find-duplicate-file-in-system" />



## Approach 1 — Brute pairwise content comparison

**Intuition.** Parse every file into `(path, content)`. Compare every pair.

**Complexity** — Time **O(F² · L)** where F = file count, L = avg content length; Space **O(F)**. TLE past F=10⁴. *In an interview* say "hash the content once, group by hash → O(N)."

---

## Approach 2 — Hash by content (canonical)

**Insight.** Parse once; for each file, compute a canonical key = content string. Insert into `Map<content, List<path>>`. Extract groups with size &gt; 1.



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



**Complexity** — Time **O(total input)**; Space **O(total input)**. *Say aloud in an interview:* "canonical-key hashing — same pattern as Group Anagrams (sort key), Group Shifted Strings (diff key), Group Isomorphic (first-index key)."

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
| Pairwise compare | O(F² · L) | O(F) | Reference; TLE past 10⁴ files |
| **Content hash** | **O(N)** | O(N) | **Canonical** |

## When to use which

- **Small files, batch mode** → full content hash.
- **Huge files** → chunked hash + verify collisions.

<AiCompanion problem-slug="find-duplicate-file-in-system" pattern-hint="hashing" />

## Related problems

- [Group Anagrams](https://leetcode.com/problems/group-anagrams/) — canonical-key style

<FeedbackWidget problem-slug="find-duplicate-file-in-system" />
