# Authoring Guide — DSA Master Reference

This guide defines the **exact conventions** every content Markdown file must follow so the
book renders consistently. The build extracts fenced ` ```diagram ` and code blocks, renders
SVG + Pygments, converts Markdown (with admonitions/tables), and assembles a paged PDF.

## File & headings

- One Markdown file per module/pattern in `src/content/`, e.g. `m03-binary-search.md`.
- **Do NOT repeat the module/chapter title as a heading** — the chapter opener prints it.
  Begin with a `## Concepts & Mental Models` section (the conceptual intro) then problems.
- **Each canonical problem is a `## H2`** (its title). Use `### H3` for the numbered template
  sections, `#### H4` sparingly.
- Keep `##` problem titles unique across the whole book.

## Admonition callouts (use liberally, 1–3 per problem)

```
!!! key "Key observation"
    One tight paragraph. This is the most important box.
```

Types → visual role: `key` (blue), `warning` (amber), `complexity` (purple),
`pattern` (cyan), `tip` (green), `pitfall` (red), `note` (grey).
Put the **complexity** of each solution in a `!!! complexity` box using `**T:**`/`**S:**`.
Start each problem with a pattern badge box:

```
!!! pattern "Pattern: Two Pointers · T: O(n) · S: O(1)"
    **Signals:** sorted array, pair/triple summing to target, in-place partition.
```

## Code

Use fenced ` ```java ` blocks. Modern, interview-ready Java:
`ArrayDeque` over `Stack`, `PriorityQueue` with safe comparators (no `a-b` overflow —
use `Integer.compare`), `long` where products/sums overflow, `int[]{r,c}` for grid coords,
`map.getOrDefault(...)`, `StringBuilder`, `s.toCharArray()`. Comment only non-obvious lines.
Use ` ```text ` for pseudocode / plain output (no language label shown).

## Diagrams — fenced ```diagram with a JSON spec

Every major algorithm needs ≥1 diagram; every canonical problem needs a **visual walkthrough**
and a **flow diagram**. Specs are strict JSON (double quotes, no trailing commas). Types:

**array** / **pointers**: `values`, `index`, `highlights{idx:role}`,
`pointers[{name,index,color,side}]`, `brackets[{from,to,label,color,row}]`, `caption`.
roles: `amber green red purple primary accent muted panel dark`.

**flow**: `width`,`box`,`title`,`steps[]` with step `type` in `start end process io decision`;
a `decision` may add `branch:{label,text,role}` (role `green`/`primary`/`red`) and `yes`.
`\n` splits lines in text.

**dptable**/**grid**: `col_head`,`row_head`,`corner`,`grid[[..]]` (null/"" empty),
`highlights[[r,c,role]]`, `arrows[{from:[r,c],to:[r,c],color}]`.

**tree**: `values` level-order (null missing), `highlights{i:role}`, `edge_highlights[[i,j]]`,
`labels{i:"txt"}`.

**recursion**: `nodes[{id,label,x,y,role}]`, `edges[{from,to,label,color,dash}]` (x=col,y=level).

**linkedlist**: `values`, `pointers[{name,index}]`, `cycle_to`, `doubly`.

**stack**/**queue**: `items` bottom→top (or `orient:"horizontal"`), `highlights`, `top_label`.

**intervals**: `min`,`max`,`intervals[{start,end,label,role}]`.

**searchspace**: `values`,`lo`,`mid`,`hi`,`eliminated[]`,`target`.

**graph**: `directed`, `nodes[{id,x,y,role,label}]`, `edges[{from,to,w,color,dash,directed}]`
(x,y in ~0..6 grid units).

**bars**: `values`, `highlights{i:role}`.

## The problem template (canonical problems)

`### H3` sections: 1 Problem · 2 Intuition · 3 Naive · 4 Key Observation (a `!!! key` box) ·
5 Pattern Recognition (Signals/Shortcut/Related) · 6 Invariant · 7 Visual Explanation (diagram) ·
8 Algorithm Flow Diagram (diagram) · 9 Walkthrough (table/diagram) · 10 Why It Works · 11 Java ·
12 Code Walkthrough · 13 Complexity (`!!! complexity`) · 14 Edge Cases · 15 Common Mistakes
(`!!! pitfall`) · 16 Optimization · 17 Alternatives · 18 Interview Follow-Ups · 19 Variations ·
20 Pattern Connection. Secondary problems may use a condensed 6–8 section treatment.

## Unicode

Write real characters (— · → ⊕) or `\uXXXX` escapes — the build decodes both. Do not put
`\uXXXX` inside inline `code` spans.
