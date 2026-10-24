## Concepts & Mental Models

Recursion turns a problem into a stack of smaller commitments. Backtracking adds one discipline: every frame owns one choice, explores all consequences of that choice, then undoes it before the caller tries the next candidate. The canonical template is **choose → explore → un-choose**.

!!! key "Core invariant"
    At every node, the partial solution is valid with respect to all constraints checked so far. Pruning is safe only when the rejected prefix cannot be extended into a valid full solution.

The search is an implicit **state-space decision tree**: a node is a partial assignment, an edge is a choice, and a leaf is either an accepted solution or a dead end. The call stack is the current root-to-node path; mutable structures such as `path`, `board`, `used`, and constraint sets encode that node.

!!! complexity "Counting backtracking complexity"
    If each level has at most `b` choices and the maximum depth is `d`, the loose bound is **O(b^d)** nodes. Then add validation/copying costs at leaves. Strong pruning reduces the realized tree but not the worst-case decision-space argument.

Pruning preserves completeness when it rejects only prefixes that violate a necessary condition: sum already too large, queen under attack, reused grid cell, non-palindromic segment, duplicate permutation representative. Good backtracking is not “try everything”; it is **try every still-possible valid prefix exactly once**.

---

## Combination Sum

!!! pattern "Pattern: Unbounded combination backtracking · T: O(N^(T/M)) · S: O(T/M) stack"
    **Signals:** choose numbers repeatedly, order does not matter, positive candidates, enumerate all sums to target.

### 1. The Problem

Given distinct positive integers `candidates` and a positive `target`, return every unique combination whose values sum to `target`. A candidate may be used unlimited times. `[2,2,3]` and `[2,3,2]` are the same combination.

### 2. The Intuition

Carry a `start` index. Once we choose candidate `i`, the next level may choose `i` again, but never an index `< i`. That makes every path nondecreasing by candidate index, so each multiset has one canonical representation.

### 3. The Naive Approach

Trying every candidate at every depth generates all permutations of each multiset, then needs a set to deduplicate normalized lists. It wastes exponential work and obscures the real invariant.

### 4. The Key Observation 🔑

!!! key "Key observation"
    Because all candidates are positive, `remaining` only decreases. If sorted `candidates[i] > remaining`, every later candidate also fails. Because order is irrelevant, enforcing nondecreasing candidate indices preserves all combinations exactly once.

### 5. Pattern Recognition

**Signals.** “All combinations,” “reuse allowed,” “sum target,” “duplicates forbidden.” **Shortcut.** Impose a canonical order with `start`. **Related.** Combination Sum II, Subsets, integer partitions, coin-change enumeration.

### 6. The Invariant

At entry to `dfs(start, remaining, path)`, `path` is nondecreasing by candidate index and `sum(path) + remaining == target`. If `remaining >= 0`, the prefix is feasible; the loop considers all valid next indices without allowing a later permutation to go backward.

### 7. Visual Explanation

```diagram
{"type":"recursion","nodes":[{"id":"r","label":"rem=7\n[]","x":3,"y":0},{"id":"a","label":"choose 2\nrem=5","x":1,"y":1},{"id":"b","label":"choose 3\nrem=4","x":3,"y":1},{"id":"c","label":"choose 6\nrem=1","x":5,"y":1},{"id":"d","label":"[2,2]\nrem=3","x":0,"y":2},{"id":"e","label":"[2,3]\nrem=2","x":2,"y":2},{"id":"f","label":"[2,2,3]\nrem=0","x":0,"y":3,"role":"green"},{"id":"x","label":"prune","x":6,"y":2,"role":"red"}],"edges":[{"from":"r","to":"a","label":"2","color":"primary"},{"from":"r","to":"b","label":"3","color":"primary"},{"from":"r","to":"c","label":"6","color":"primary"},{"from":"a","to":"d","label":"2","color":"primary"},{"from":"a","to":"e","label":"3","color":"primary"},{"from":"d","to":"f","label":"3","color":"green"},{"from":"c","to":"x","label":"7 > rem","color":"red","dash":true}]}
```

```diagram
{"type":"flow","width":520,"box":270,"title":"Combination Sum DFS","steps":[{"type":"start","text":"dfs(start, remaining, path)"},{"type":"decision","text":"remaining == 0?","yes":"no","branch":{"label":"yes","text":"copy path to result","role":"green"}},{"type":"process","text":"for i from start to n-1"},{"type":"decision","text":"candidates[i] <= remaining?","yes":"yes","branch":{"label":"no","text":"break sorted loop","role":"red"}},{"type":"process","text":"choose candidates[i]"},{"type":"process","text":"dfs(i, remaining - candidates[i])"},{"type":"process","text":"undo last choice"},{"type":"end","text":"return"}]}
```

### 8. Algorithm Flow Diagram

The executable skeleton is base case, sorted-loop pruning, choose, recurse with `i` to allow reuse, then undo. Uniqueness is encoded entirely by never recursing to a smaller index.

### 9. Step-by-Step Walkthrough

| path | remaining | next indices | action |
|---|---:|---|---|
| `[]` | 7 | `0..3` | choose 2 |
| `[2]` | 5 | `0..3` | choose 2 |
| `[2,2]` | 3 | `0..3` | choose 3 |
| `[2,2,3]` | 0 | — | accept |
| `[2,3]` | 2 | `1..3` | 3 exceeds remaining, break |
| `[7]` | 0 | — | accept |

### 10. Why It Works

Soundness: a copied path has `remaining == 0`, so it sums to target. Completeness: any valid combination can be sorted by candidate index, and DFS can choose that exact sequence. Uniqueness: the `start` boundary prevents any alternate ordering of the same multiset.

### 11. Java Implementation

```java
import java.util.*;

class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> ans = new ArrayList<>();
        dfs(candidates, target, 0, new ArrayList<>(), ans);
        return ans;
    }

    private void dfs(int[] candidates, int remaining, int start,
                     List<Integer> path, List<List<Integer>> ans) {
        if (remaining == 0) {
            ans.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < candidates.length; i++) {
            int x = candidates[i];
            if (x > remaining) break;
            path.add(x);
            dfs(candidates, remaining - x, i, path, ans);
            path.remove(path.size() - 1);
        }
    }
}
```

### 12. Code Walkthrough

Sorting enables `break`. Passing `i` allows reuse; passing `i + 1` would solve a different problem. `path` is mutated in place and copied only at accepted leaves.

### 13. Complexity

!!! complexity "Complexity"
    With smallest candidate `M` and target `T`, depth is at most `T/M`; branching is at most `N`, giving **O(N^(T/M))** search nodes. Space is **O(T/M)** excluding output.

### 14. Edge Cases

Target equal to a candidate, no possible combination, candidate larger than target, and the positive-candidate precondition. Zero or negative candidates can cause nontermination.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Recursing from index `0` regenerates permutations; recursing with `i + 1` forbids reuse; forgetting `path.remove(...)` corrupts sibling branches.

### 16. Optimization

Sort and break early. Memoizing `(start, remaining)` helps only when reusing suffix combination lists carefully; enumeration is often output-bound.

### 17. Alternatives

DP is better for counting or optimizing coin counts, not for listing combinations. BFS stores many partial paths and has no advantage over DFS.

### 18. Interview Follow-Ups

Combination Sum II uses each index once and skips duplicates at the same depth. Combination Sum III adds fixed cardinality. Count-only variants use DP.

### 19. Variations

Subsets, k-combinations, factor combinations, and integer partitions all use the same canonical-forward recursion.

### 20. Pattern Connection

This is the archetype of **enumerative backtracking with canonical order**: the prefix is valid, pruning is necessary-condition pruning, and accepted leaves are copied.

---

## N-Queens

!!! pattern "Pattern: Constraint-set backtracking · T: O(N!) · S: O(N) auxiliary"
    **Signals:** place one item per row, reject conflicts immediately, output all boards, diagonal constraints.

### 1. The Problem

Place `n` queens on an `n × n` chessboard so no two queens attack each other. Return all distinct board configurations.

### 2. The Intuition

Place exactly one queen per row. Row conflicts vanish by construction; the only live constraints are column, main diagonal, and anti-diagonal. Boolean sets make each safety check O(1).

### 3. The Naive Approach

Try arbitrary squares and validate completed boards by scanning. This explores many placements with duplicate rows and columns and delays obvious conflicts until too late.

### 4. The Key Observation 🔑

!!! key "Key observation"
    With one queen per row, a partial board is valid iff no used column, `row - col` diagonal, or `row + col` diagonal repeats. These constraints are monotonic: an attack cannot be repaired by placing more queens.

### 5. Pattern Recognition

**Signals.** “Place N objects,” “all arrangements,” “constraints between positions.” **Shortcut.** Convert geometry into integer keys: column `c`, diagonal `r - c + n - 1`, anti-diagonal `r + c`. **Related.** Sudoku, graph coloring, permutations with `used[]`.

### 6. The Invariant

Before `dfs(row)`, rows `0..row-1` each contain one queen, no two placed queens attack, and `cols`, `diag1`, `diag2` exactly describe those queens. A failed safety test therefore cannot participate in any completion of this prefix.

### 7. Visual Explanation

```diagram
{"type":"recursion","nodes":[{"id":"r0","label":"row 0","x":3,"y":0},{"id":"c0","label":"Q at (0,0)","x":1,"y":1},{"id":"c1","label":"Q at (0,1)","x":3,"y":1},{"id":"c2","label":"Q at (0,2)","x":5,"y":1},{"id":"p","label":"conflict","x":0,"y":2,"role":"red"},{"id":"r2","label":"row 2 valid","x":3,"y":2},{"id":"sol","label":"4 queens placed","x":3,"y":3,"role":"green"}],"edges":[{"from":"r0","to":"c0","label":"col 0","color":"primary"},{"from":"r0","to":"c1","label":"col 1","color":"primary"},{"from":"r0","to":"c2","label":"col 2","color":"primary"},{"from":"c0","to":"p","label":"attacked","color":"red","dash":true},{"from":"c1","to":"r2","label":"safe","color":"primary"},{"from":"r2","to":"sol","label":"complete","color":"green"}]}
```

```diagram
{"type":"dptable","corner":"","col_head":["0","1","2","3"],"row_head":["0","1","2","3"],"grid":[["Q","×","×","×"],["×","×",".","."],["×",".","×","."],["×",".",".","×"]],"highlights":[[0,0,"green"],[0,1,"red"],[1,0,"red"],[1,1,"red"],[2,2,"red"],[3,3,"red"]],"arrows":[]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":540,"box":280,"title":"N-Queens DFS by row","steps":[{"type":"start","text":"dfs(row)"},{"type":"decision","text":"row == n?","yes":"no","branch":{"label":"yes","text":"emit board","role":"green"}},{"type":"process","text":"for col in 0..n-1"},{"type":"decision","text":"col and diagonals free?","yes":"yes","branch":{"label":"no","text":"skip candidate","role":"red"}},{"type":"process","text":"place Q; mark constraints"},{"type":"process","text":"dfs(row + 1)"},{"type":"process","text":"remove Q; unmark constraints"},{"type":"end","text":"return"}]}
```

### 9. Step-by-Step Walkthrough

For `n = 4`, one solution uses columns `[1,3,0,2]`.

| row | col | occupied columns | `r-c` keys | `r+c` keys |
|---:|---:|---|---|---|
| 0 | 1 | `{1}` | `{-1}` | `{1}` |
| 1 | 3 | `{1,3}` | `{-1,-2}` | `{1,4}` |
| 2 | 0 | `{0,1,3}` | `{-1,-2,2}` | `{1,2,4}` |
| 3 | 2 | `{0,1,2,3}` | `{-1,-2,1,2}` | `{1,2,4,5}` |

### 10. Why It Works

Soundness: emitted boards have one queen per row and no repeated column or diagonal, so no two queens attack. Completeness: in any valid solution, the solution's column at each row passes the constraint tests under its prefix, so DFS keeps that branch. Pruning only removes attacked squares.

### 11. Java Implementation

```java
import java.util.*;

class Solution {
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> ans = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');
        boolean[] cols = new boolean[n];
        boolean[] diag1 = new boolean[2 * n - 1];
        boolean[] diag2 = new boolean[2 * n - 1];
        dfs(0, board, cols, diag1, diag2, ans);
        return ans;
    }

    private void dfs(int row, char[][] board, boolean[] cols,
                     boolean[] diag1, boolean[] diag2,
                     List<List<String>> ans) {
        int n = board.length;
        if (row == n) {
            ans.add(toBoard(board));
            return;
        }
        for (int col = 0; col < n; col++) {
            int d1 = row - col + n - 1;
            int d2 = row + col;
            if (cols[col] || diag1[d1] || diag2[d2]) continue;
            board[row][col] = 'Q';
            cols[col] = diag1[d1] = diag2[d2] = true;
            dfs(row + 1, board, cols, diag1, diag2, ans);
            cols[col] = diag1[d1] = diag2[d2] = false;
            board[row][col] = '.';
        }
    }

    private List<String> toBoard(char[][] board) {
        List<String> rows = new ArrayList<>(board.length);
        for (char[] row : board) rows.add(new String(row));
        return rows;
    }
}
```

### 12. Code Walkthrough

`row` is depth. The board is for output; the boolean arrays are the legality oracle. The shift `+ n - 1` maps negative main-diagonal keys into array indices.

### 13. Complexity

!!! complexity "Complexity"
    Column choices shrink like a permutation, so a standard bound is **O(N!)** nodes with O(1) safety checks. Emitting each solution costs O(N²). Auxiliary constraints and stack are **O(N)**; the mutable board is O(N²).

### 14. Edge Cases

`n = 1` has one board. `n = 2` and `n = 3` have no solution. For large `n`, output size dominates.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Mixing up diagonal formulas, forgetting the `+ n - 1` shift, or failing to unmark exactly the constraints just marked. Emitting `Arrays.toString(row)` instead of `new String(row)` also produces the wrong board format.

### 16. Optimization

Bitmasks can enumerate legal columns with `available = ~(cols | diag1 | diag2) & mask`, improving constants for counting. Boolean arrays remain clearer for board generation.

### 17. Alternatives

Permuting columns first removes column conflicts but delays diagonal pruning. Exact-cover/SAT formulations are elegant but unnecessary in a coding interview unless generalized constraints are requested.

### 18. Interview Follow-Ups

Count solutions only, stop after one solution, support blocked squares, or implement a bitmask solver.

### 19. Variations

N-Rooks removes diagonals; bishop placement keeps only diagonals; Sudoku generalizes the same constraint-set idea.

### 20. Pattern Connection

N-Queens is a canonical valid-prefix search. Every deeper node is legal by construction, and every pruned branch violates a necessary constraint.

---

## Word Search (grid DFS + backtrack)

!!! pattern "Pattern: Grid path backtracking · T: O(MN·4^L) · S: O(L) stack"
    **Signals:** grid path, orthogonal moves, cannot reuse a cell, existence rather than all paths.

### 1. The Problem

Given an `m × n` board of characters and a word, determine whether the word can be constructed from sequentially adjacent horizontal/vertical cells. A cell may not be reused in the same path.

### 2. The Intuition

Start from every cell that could match the first character. At word index `k`, the next recursive state must be an unvisited neighbor matching `word[k+1]`. Mark the current cell visited, explore, then restore it.

### 3. The Naive Approach

Generate every length-`L` grid walk and compare its string to the word. This stores path strings and explores branches that mismatch immediately. Backtracking validates one character per level.

### 4. The Key Observation 🔑

!!! key "Key observation"
    A prefix path is valid exactly when it spells `word[0..k]` and contains no repeated cells. A character mismatch, boundary exit, or revisit can be pruned because no extension can repair it.

### 5. Pattern Recognition

**Signals.** “Grid,” “path,” “cannot reuse,” “four directions.” **Shortcut.** Use the board itself as visited by writing a sentinel and restoring it. **Related.** Maze DFS, Boggle, Word Search II with a trie.

### 6. The Invariant

At entry to `dfs(r,c,k)`, previously marked cells form a simple path spelling `word[0..k-1]`. If `(r,c)` is in bounds, unvisited, and equals `word[k]`, choosing it extends a valid prefix.

### 7. Visual Explanation

```diagram
{"type":"recursion","nodes":[{"id":"a","label":"A(0,0)\nk=0","x":3,"y":0},{"id":"b","label":"B(0,1)\nk=1","x":2,"y":1},{"id":"x","label":"mismatch","x":4,"y":1,"role":"red"},{"id":"c","label":"C(0,2)\nk=2","x":2,"y":2},{"id":"d","label":"C(1,2)\nk=3","x":2,"y":3},{"id":"e","label":"E(2,2)\nk=4","x":2,"y":4},{"id":"f","label":"D(2,1)\nk=5","x":2,"y":5,"role":"green"}],"edges":[{"from":"a","to":"b","label":"right","color":"primary"},{"from":"a","to":"x","label":"left/up","color":"red","dash":true},{"from":"b","to":"c","label":"right","color":"primary"},{"from":"c","to":"d","label":"down","color":"primary"},{"from":"d","to":"e","label":"down","color":"primary"},{"from":"e","to":"f","label":"left","color":"green"}]}
```

```diagram
{"type":"dptable","corner":"","col_head":["0","1","2","3"],"row_head":["0","1","2"],"grid":[["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],"highlights":[[0,0,"green"],[0,1,"green"],[0,2,"green"],[1,2,"green"],[2,2,"green"],[2,1,"green"]],"arrows":[{"from":[0,0],"to":[0,1],"color":"green"},{"from":[0,1],"to":[0,2],"color":"green"},{"from":[0,2],"to":[1,2],"color":"green"},{"from":[1,2],"to":[2,2],"color":"green"},{"from":[2,2],"to":[2,1],"color":"green"}]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":540,"box":285,"title":"Word Search DFS","steps":[{"type":"start","text":"for each cell"},{"type":"decision","text":"dfs(r,c,0) true?","yes":"yes","branch":{"label":"no","text":"try next start","role":"primary"}},{"type":"end","text":"return true"},{"type":"process","text":"dfs checks bounds, visited, char"},{"type":"process","text":"mark cell visited"},{"type":"process","text":"search four neighbors"},{"type":"process","text":"restore cell"},{"type":"end","text":"return found"}]}
```

### 9. Step-by-Step Walkthrough

For `ABCCED`, the path is `(0,0) → (0,1) → (0,2) → (1,2) → (2,2) → (2,1)`.

| index | char | cell | reason branch survives |
|---:|---|---|---|
| 0 | A | `(0,0)` | start matches |
| 1 | B | `(0,1)` | unvisited neighbor |
| 2 | C | `(0,2)` | unvisited neighbor |
| 3 | C | `(1,2)` | unvisited neighbor |
| 4 | E | `(2,2)` | unvisited neighbor |
| 5 | D | `(2,1)` | final char matched |

### 10. Why It Works

Soundness: true is returned only after matching every character in order, and visited marking prevents reuse. Completeness: any valid path starts at a cell considered by the outer loop, and each next cell is among the four recursive moves.

### 11. Java Implementation

```java
class Solution {
    private static final int[][] DIRS = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    public boolean exist(char[][] board, String word) {
        if (word.length() > board.length * board[0].length) return false;
        for (int r = 0; r < board.length; r++) {
            for (int c = 0; c < board[0].length; c++) {
                if (dfs(board, word, r, c, 0)) return true;
            }
        }
        return false;
    }

    private boolean dfs(char[][] board, String word, int r, int c, int k) {
        if (k == word.length()) return true;
        if (r < 0 || r == board.length || c < 0 || c == board[0].length) return false;
        if (board[r][c] != word.charAt(k)) return false;

        char saved = board[r][c];
        board[r][c] = '#';
        for (int[] d : DIRS) {
            if (dfs(board, word, r + d[0], c + d[1], k + 1)) {
                board[r][c] = saved;
                return true;
            }
        }
        board[r][c] = saved;
        return false;
    }
}
```

### 12. Code Walkthrough

The base case means all previous characters matched. Bounds and character checks occur before mutation. The sentinel encodes visited for the active path; if `'#'` may appear in the board, use `boolean[][] visited`.

### 13. Complexity

!!! complexity "Complexity"
    There are `M·N` starts. The first step has up to 4 directions, later steps at most 3 useful directions because the previous cell is visited. Bound: **O(MN·4^L)**, refined to **O(MN·3^(L-1))**. Space is **O(L)**.

### 14. Edge Cases

Word longer than cell count, one-character words, repeated letters requiring visited state, and boards containing the sentinel character.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Forgetting to restore the cell before returning, marking visited after recursion, or using one global visited set that is not undone between starts.

### 16. Optimization

Count board characters and reject impossible words. Reverse the word when the last character is rarer than the first to reduce starting points.

### 17. Alternatives

Use a separate `visited` matrix when mutation is undesirable. For many words, build a trie and DFS once over shared prefixes.

### 18. Interview Follow-Ups

Return coordinates, support diagonal moves, count all matching paths, or solve Word Search II.

### 19. Variations

Boggle, maze simple paths, Hamiltonian grid paths, and island DFS with reversible state all share this active-path invariant.

### 20. Pattern Connection

This is valid-prefix DFS on a grid: the prefix already spells the word prefix and is simple. Every pruned branch violates adjacency, character equality, or no-reuse.

---

## Palindrome Partitioning

!!! pattern "Pattern: Prefix partition backtracking · T: O(N·2^N) · S: O(N) stack"
    **Signals:** split a string into all valid segmentations, validate each chosen substring, output all partitions.

### 1. Problem

Given a string `s`, return all ways to partition it so every substring in the partition is a palindrome.

### 2. Key Observation

!!! key "Key observation"
    At index `start`, every valid answer chooses one palindromic prefix `s[start..end]`, then partitions the suffix. A non-palindromic prefix can be pruned because later cuts cannot change its internal characters.

### 3. Invariant

At entry to `dfs(start)`, `path` contains palindromic substrings whose concatenation is exactly `s[0..start-1]`. Thus `start == s.length()` means `path` is a complete valid partition.

### 4. Diagram

```diagram
{"type":"recursion","nodes":[{"id":"r","label":"start 0\n[]","x":3,"y":0},{"id":"a","label":"a","x":1,"y":1},{"id":"aa","label":"aa","x":4,"y":1},{"id":"ab","label":"ab prune","x":6,"y":1,"role":"red"},{"id":"a2","label":"a | a","x":1,"y":2},{"id":"b1","label":"a | a | b","x":1,"y":3,"role":"green"},{"id":"b2","label":"aa | b","x":4,"y":2,"role":"green"}],"edges":[{"from":"r","to":"a","label":"pal","color":"primary"},{"from":"r","to":"aa","label":"pal","color":"primary"},{"from":"r","to":"ab","label":"not pal","color":"red","dash":true},{"from":"a","to":"a2","label":"pal","color":"primary"},{"from":"a2","to":"b1","label":"pal","color":"green"},{"from":"aa","to":"b2","label":"pal","color":"green"}]}
```

### 5. Java

```java
import java.util.*;

class Solution {
    public List<List<String>> partition(String s) {
        List<List<String>> ans = new ArrayList<>();
        dfs(s, 0, new ArrayList<>(), ans);
        return ans;
    }

    private void dfs(String s, int start, List<String> path, List<List<String>> ans) {
        if (start == s.length()) {
            ans.add(new ArrayList<>(path));
            return;
        }
        for (int end = start; end < s.length(); end++) {
            if (!isPalindrome(s, start, end)) continue;
            path.add(s.substring(start, end + 1));
            dfs(s, end + 1, path, ans);
            path.remove(path.size() - 1);
        }
    }

    private boolean isPalindrome(String s, int lo, int hi) {
        while (lo < hi) {
            if (s.charAt(lo++) != s.charAt(hi--)) return false;
        }
        return true;
    }
}
```

### 6. Complexity

!!! complexity "Complexity"
    There are `2^(N-1)` cut patterns. Palindrome checks and substring copies give the usual **O(N·2^N)** bound. Recursion/path space is **O(N)** excluding output; a precomputed palindrome table makes checks O(1) at O(N²) space.

### 7. Common Pitfall

Do not validate the whole partition only at the leaf; that loses pruning. Also avoid reusing the mutable `path` object in `ans` without copying it.

### 8. Pattern Connection

This is Combination Sum over string prefixes: choose a valid next segment, recurse on the suffix, undo. The valid-prefix invariant makes non-palindromic-prefix pruning complete.

---

## Permutations II (dedup with used[] / sorted skip)

!!! pattern "Pattern: Deduplicated permutation backtracking · T: O(N!·N) · S: O(N) stack"
    **Signals:** generate permutations with duplicate values, avoid duplicate output, maintain `used[]`.

### 1. Problem

Given an integer array that may contain duplicates, return all unique permutations.

### 2. Key Observation

!!! key "Key observation"
    Sort first. At one recursion depth, equal values are interchangeable; choosing a later copy before the earlier unused copy creates a duplicate representative. The skip rule `i > 0 && nums[i] == nums[i - 1] && !used[i - 1]` keeps only the canonical branch.

### 3. Invariant

At entry to `dfs`, `path` is a length-`depth` permutation prefix built from exactly indices whose `used[i]` is true. Duplicate equal values are consumed in stable index order whenever both choices are available at the same depth.

### 4. Diagram

```diagram
{"type":"recursion","nodes":[{"id":"r","label":"[]","x":3,"y":0},{"id":"a1","label":"choose 1a","x":1,"y":1},{"id":"a2","label":"choose 1b","x":5,"y":1,"role":"red"},{"id":"b","label":"[1,1]","x":0,"y":2},{"id":"c","label":"[1,2]","x":2,"y":2},{"id":"sol1","label":"[1,1,2]","x":0,"y":3,"role":"green"},{"id":"sol2","label":"[1,2,1]","x":2,"y":3,"role":"green"}],"edges":[{"from":"r","to":"a1","label":"use first 1","color":"primary"},{"from":"r","to":"a2","label":"skip duplicate","color":"red","dash":true},{"from":"a1","to":"b","label":"1b","color":"primary"},{"from":"a1","to":"c","label":"2","color":"primary"},{"from":"b","to":"sol1","label":"2","color":"green"},{"from":"c","to":"sol2","label":"1b","color":"green"}]}
```

### 5. Java

```java
import java.util.*;

class Solution {
    public List<List<Integer>> permuteUnique(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> ans = new ArrayList<>();
        dfs(nums, new boolean[nums.length], new ArrayList<>(), ans);
        return ans;
    }

    private void dfs(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> ans) {
        if (path.size() == nums.length) {
            ans.add(new ArrayList<>(path));
            return;
        }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;
            used[i] = true;
            path.add(nums[i]);
            dfs(nums, used, path, ans);
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }
}
```

### 6. Complexity

!!! complexity "Complexity"
    In the all-distinct case there are `N!` leaves and each copy costs O(N), so **T: O(N!·N)**. With duplicates, leaves reduce to `N! / Π(freq[v]!)`. Stack, `used`, and `path` are **O(N)** excluding output.

### 7. Common Pitfall

The skip condition must test `!used[i - 1]`, not `used[i - 1]`. We skip the later duplicate only when its earlier twin is available in the same decision layer.

### 8. Pattern Connection

This is symmetry pruning. The partial permutation is valid at every node, and the sorted-skip rule removes only duplicate index representations, never a distinct value sequence.

---

## Sudoku Solver

!!! pattern "Pattern: Constraint propagation backtracking · T: O(9^E) · S: O(E) stack"
    **Signals:** fill empty cells, row/column/box constraints, mutate board in place, stop after one solution.

### 1. Problem

Given a partially filled `9 × 9` Sudoku board, fill empty cells `'.'` so every row, column, and `3 × 3` box contains digits `1..9` without repetition. The input is assumed to have a valid solution.

### 2. Key Observation

!!! key "Key observation"
    A digit is legal for `(r,c)` iff it is unused in row `r`, column `c`, and box `(r / 3) * 3 + c / 3`. These constraints are monotonic under placement, so illegal digits can be pruned before recursion.

### 3. Invariant

Before solving cell index `pos`, every filled cell satisfies Sudoku constraints, and row/column/box masks exactly reflect the board. Choosing a digit sets one bit in each mask; undo clears those same bits.

### 4. Diagram

```diagram
{"type":"dptable","corner":"","col_head":["0","1","2","3","4","5","6","7","8"],"row_head":["0","1","2","3","4","5","6","7","8"],"grid":[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]],"highlights":[[0,2,"green"],[0,0,"amber"],[0,1,"amber"],[0,4,"amber"],[1,2,"red"],[2,2,"red"]],"arrows":[]}
```

### 5. Java

```java
class Solution {
    public void solveSudoku(char[][] board) {
        int[] rows = new int[9], cols = new int[9], boxes = new int[9];
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] == '.') continue;
                int bit = 1 << (board[r][c] - '1');
                rows[r] |= bit;
                cols[c] |= bit;
                boxes[box(r, c)] |= bit;
            }
        }
        solve(board, rows, cols, boxes, 0);
    }

    private boolean solve(char[][] board, int[] rows, int[] cols, int[] boxes, int pos) {
        if (pos == 81) return true;
        int r = pos / 9, c = pos % 9;
        if (board[r][c] != '.') return solve(board, rows, cols, boxes, pos + 1);

        int b = box(r, c);
        int used = rows[r] | cols[c] | boxes[b];
        for (int d = 0; d < 9; d++) {
            int bit = 1 << d;
            if ((used & bit) != 0) continue;
            board[r][c] = (char) ('1' + d);
            rows[r] |= bit;
            cols[c] |= bit;
            boxes[b] |= bit;
            if (solve(board, rows, cols, boxes, pos + 1)) return true;
            rows[r] ^= bit;
            cols[c] ^= bit;
            boxes[b] ^= bit;
            board[r][c] = '.';
        }
        return false;
    }

    private int box(int r, int c) {
        return (r / 3) * 3 + c / 3;
    }
}
```

### 6. Complexity

!!! complexity "Complexity"
    With `E` empty cells, the crude bound is **O(9^E)**. Constraint masks reduce the practical branching factor to legal candidates per cell. Space is **O(E)** recursion plus O(1) masks for 27 units.

### 7. Common Pitfall

Undo must clear exactly the bit placed by this frame. XOR is safe here only because the bit was known absent before placement and no descendant returns through this undo after keeping the solution.

### 8. Pattern Connection

Sudoku is N-Queens with more domains: each empty cell is a variable, each digit is a choice, and row/column/box masks keep the partial board valid at every node.
