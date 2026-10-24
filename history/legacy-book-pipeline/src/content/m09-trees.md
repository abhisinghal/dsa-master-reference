## Concepts & Mental Models

Trees reward one mental model: **solve for the children, then combine at the parent**. A node is not an isolated record; it is the root of a smaller problem. Write the helper contract before code: what fact does this subtree return to its parent, and what answer, if any, is accumulated globally?

!!! key "Recursive contract first"
    Tree recursion becomes senior-level when the return value is precise: height, validity under bounds, one-branch gain, built subtree root, or a token stream position. If the best answer may be completed entirely inside a child or through the current node, separate the **returned contribution** from the **global answer**.

| Traversal | Order | Natural when |
|---|---|---|
| Preorder | node → left → right | clone/serialize root-first, consume root-first input |
| Inorder | left → node → right | BST sorted order, kth/range queries |
| Postorder | left → right → node | height, diameter, max path, deletion |
| Level order | breadth by depth | shortest depth, views, completeness, per-level output |

A BST invariant is **range-based**, not just parent-child comparison: all nodes in the left subtree must be `< node.val`, all nodes in the right subtree `> node.val`, and ancestor bounds continue to apply deep below.

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

---

## Binary Tree Traversals (recursive + iterative + Morris note)

!!! pattern "Pattern: Tree Traversal · T: O(n) · S: O(h) recursive / O(n) worst-case"
    **Signals:** visit every node, output order matters, or recursive DFS must become an explicit stack.

### 1. Problem

Return binary-tree values in preorder, inorder, postorder, and level order. The real interview task is choosing the traversal whose visit timing matches the computation, then implementing it recursively or iteratively without losing the invariant.

### 2. Intuition

DFS has three visit slots around child calls: before left, between children, and after right. BFS visits by distance from root. Iterative DFS is the recursive call stack made explicit; Morris traversal temporarily threads predecessor links to remove the stack for inorder/preorder.

### 3. Naive

Repeatedly searching for the "next" node or reconstructing parent paths makes traversal O(nh). A correct traversal touches each node O(1) times.

### 4. Key Observation

!!! key "Key observation"
    Place `visit(node)` before both child calls for preorder, between them for inorder, and after them for postorder. The iterative versions preserve exactly the same suspended work on a stack.

### 5. Pattern Recognition

**Signals.** Need all nodes with no pruning; ordering is the output. **Shortcut.** BST sorted order implies inorder; parent needs both child summaries implies postorder. **Related.** Serialization, kth smallest, expression evaluation, DFS graph templates.

### 6. Invariant

Recursive invariant: when `dfs(node)` returns, every node in that subtree has been appended exactly once in the promised order. Iterative inorder invariant: the stack contains ancestors whose left subtrees have been fully descended but whose own values are not yet emitted.

### 7. Visual Explanation

```diagram
{"type":"tree","values":[1,2,3,4,5,null,6],"labels":{"0":"1 pre1 in4 post6","1":"2 pre2 in2 post3","2":"3 pre5 in5 post5","3":"4 pre3 in1 post1","4":"5 pre4 in3 post2","6":"6 pre6 in6 post4"},"highlights":{"0":"primary","1":"amber","2":"green","3":"muted","4":"muted","6":"muted"}}
```

```diagram
{"type":"tree","values":[1,2,3,4,5,null,6],"labels":{"0":"level1","1":"level2","2":"level3","3":"level4","4":"level5","6":"level6"},"highlights":{"0":"primary","1":"amber","2":"amber","3":"green","4":"green","6":"green"}}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"flow","width":440,"box":270,"title":"DFS visit slots","steps":[{"type":"start","text":"dfs(node)"},{"type":"decision","text":"node == null?","yes":"return"},{"type":"process","text":"preorder visit slot"},{"type":"process","text":"dfs(left)"},{"type":"process","text":"inorder visit slot"},{"type":"process","text":"dfs(right)"},{"type":"process","text":"postorder visit slot"},{"type":"end","text":"return"}]}
```

### 9. Walkthrough

| traversal | output |
|---|---|
| preorder | `1, 2, 4, 5, 3, 6` |
| inorder | `4, 2, 5, 1, 3, 6` |
| postorder | `4, 5, 2, 6, 3, 1` |
| level order | `1, 2, 3, 4, 5, 6` |

### 10. Why It Works

Each edge is traversed down and back once. The recursive placement of the visit creates the ordering; the iterative stack stores the same frames that recursion would have stored implicitly.

### 11. Java

```java
import java.util.*;

class Traversals {
    List<Integer> preorder(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        pre(root, out);
        return out;
    }
    private void pre(TreeNode node, List<Integer> out) {
        if (node == null) return;
        out.add(node.val);
        pre(node.left, out);
        pre(node.right, out);
    }

    List<Integer> inorder(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        in(root, out);
        return out;
    }
    private void in(TreeNode node, List<Integer> out) {
        if (node == null) return;
        in(node.left, out);
        out.add(node.val);
        in(node.right, out);
    }

    List<Integer> postorder(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        post(root, out);
        return out;
    }
    private void post(TreeNode node, List<Integer> out) {
        if (node == null) return;
        post(node.left, out);
        post(node.right, out);
        out.add(node.val);
    }

    List<Integer> preorderIterative(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        if (root == null) return out;
        Deque<TreeNode> st = new ArrayDeque<>();
        st.push(root);
        while (!st.isEmpty()) {
            TreeNode node = st.pop();
            out.add(node.val);
            if (node.right != null) st.push(node.right);
            if (node.left != null) st.push(node.left);
        }
        return out;
    }

    List<Integer> inorderIterative(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        Deque<TreeNode> st = new ArrayDeque<>();
        TreeNode cur = root;
        while (cur != null || !st.isEmpty()) {
            while (cur != null) {
                st.push(cur);
                cur = cur.left;
            }
            cur = st.pop();
            out.add(cur.val);
            cur = cur.right;
        }
        return out;
    }

    List<Integer> postorderIterative(TreeNode root) {
        LinkedList<Integer> out = new LinkedList<>();
        if (root == null) return out;
        Deque<TreeNode> st = new ArrayDeque<>();
        st.push(root);
        while (!st.isEmpty()) {
            TreeNode node = st.pop();
            out.addFirst(node.val);
            if (node.left != null) st.push(node.left);
            if (node.right != null) st.push(node.right);
        }
        return out;
    }
}
```

### 12. Code Walkthrough

Recursive methods differ only by the `out.add` slot. Iterative preorder pushes right before left because a stack reverses order. Iterative inorder descends the left spine, then visits the nearest pending ancestor. Iterative postorder emits node-right-left in reverse by adding to the front.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(h) for recursion or explicit DFS stack, O(n) worst-case on skewed trees; BFS is O(w) by maximum width. Morris inorder/preorder can reduce auxiliary space to O(1) by temporary threading.

### 14. Edge Cases

Empty tree returns an empty list. Single-node trees produce the same output for every traversal. Skewed trees can overflow Java recursion in production-scale inputs.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Pushing left before right in iterative preorder, using legacy `Stack`, pushing null into `ArrayDeque`, or reversing preorder directly for postorder without swapping child order.

### 16. Optimization

Morris traversal creates a temporary right thread from each inorder predecessor to the current node, visits without a stack, and restores the pointer. Use it only when mutation during traversal is acceptable and restoration is guaranteed.

### 17. Alternatives

A `(node, visited)` color stack gives a uniform iterative template for all DFS orders. Parent-pointer traversal works only if parent links exist.

### 18. Interview Follow-Ups

Build a lazy BST iterator, traverse without recursion, add zigzag level order, or describe why Morris is unsafe on immutable/shared trees.

### 19. Variations

Boundary traversal, vertical order, N-ary traversals, and expression-tree evaluation are all state-augmented traversals.

### 20. Pattern Connection

Traversal is the substrate for tree DP, BST order statistics, serialization, and reconstruction. Pick the order based on when the parent has enough information to act.

---

## Level Order Traversal (BFS)

!!! pattern "Pattern: Breadth-First Search · T: O(n) · S: O(w)"
    **Signals:** process by depth, preserve left-to-right order, compute a per-level result.

### Problem

Return `List<List<Integer>>`, grouping node values by depth from the root.

### Key Observation

!!! key "Key observation"
    At the start of each outer loop, `queue.size()` is exactly the number of nodes on the current level. Process exactly that many nodes, appending their children for the next level.

### Invariant

Before each level loop, the queue contains one complete level in left-to-right order. After `size` pops, it contains the next level.

### Diagram

```diagram
{"type":"tree","values":[3,9,20,null,null,15,7],"labels":{"0":"level 0","1":"level 1","2":"level 1","5":"level 2","6":"level 2"},"highlights":{"0":"primary","1":"amber","2":"amber","5":"green","6":"green"}}
```

### Java

```java
List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> ans = new ArrayList<>();
    if (root == null) return ans;
    Deque<TreeNode> q = new ArrayDeque<>();
    q.offer(root);
    while (!q.isEmpty()) {
        int size = q.size();
        List<Integer> level = new ArrayList<>(size);
        for (int i = 0; i < size; i++) {
            TreeNode node = q.poll();
            level.add(node.val);
            if (node.left != null) q.offer(node.left);
            if (node.right != null) q.offer(node.right);
        }
        ans.add(level);
    }
    return ans;
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(w), maximum tree width; O(n) worst-case.

### Pattern Connection

Level-size BFS drives right-side view, zigzag traversal, minimum depth, averages by level, and completeness checks.

---

## Validate Binary Search Tree

!!! pattern "Pattern: DFS with Bounds · T: O(n) · S: O(h)"
    **Signals:** validate BST, ancestor constraints matter, duplicates policy must be explicit.

### Problem

Return whether a binary tree satisfies the strict BST invariant: every node in a left subtree is smaller than the ancestor root, and every node in a right subtree is larger.

### Key Observation

!!! key "Key observation"
    Local child checks miss deep violations. Pass the allowed open interval `(low, high)` downward and require every node to satisfy it.

### Invariant

`valid(node, low, high)` returns true iff every value in `node`'s subtree lies strictly inside `(low, high)` and both children satisfy their tightened intervals.

### Diagram

```diagram
{"type":"tree","values":[5,1,7,null,null,3,8],"labels":{"0":"5 (-∞,+∞)","1":"1 (-∞,5)","2":"7 (5,+∞)","5":"3 violates (5,7)","6":"8 (7,+∞)"},"highlights":{"0":"primary","2":"amber","5":"red"}}
```

### Java

```java
boolean isValidBST(TreeNode root) {
    return valid(root, Long.MIN_VALUE, Long.MAX_VALUE);
}

private boolean valid(TreeNode node, long low, long high) {
    if (node == null) return true;
    if (node.val <= low || node.val >= high) return false;
    return valid(node.left, low, node.val) && valid(node.right, node.val, high);
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(h) recursion depth.

### Pattern Connection

This is range-propagation DFS, reused in BST search ranges, constructing BST from preorder, and validating serialized constraints.

---

## Lowest Common Ancestor (BST and general binary tree)

!!! pattern "Pattern: Divergence / Postorder Search · T: O(h) BST, O(n) general · S: O(h)"
    **Signals:** two targets, first shared ancestor, paths diverge from root or child hits bubble upward.

### 1. Problem

Given a tree and two existing nodes `p` and `q`, return their lowest common ancestor: the deepest node whose subtree contains both, allowing a node to be its own ancestor. Solve the ordered BST case and the arbitrary binary-tree case.

### 2. Intuition

In a BST, values tell whether both targets lie left, both right, or split at the current node. In a general tree, no ordering exists; each subtree reports whether it found either target or an already completed LCA.

### 3. Naive

Build root-to-node paths for both targets, then scan until they diverge. It is correct, but it stores O(h) to O(n) path state and obscures the cleaner recursive signal.

### 4. Key Observation

!!! key "Key observation"
    General helper contract: return `null` if this subtree contains neither target; otherwise return the found target or the completed LCA. If left and right both return non-null, the current node is the lowest meeting point.

### 5. Pattern Recognition

**Signals.** "Lowest ancestor", "first common node", targets are nodes not merely values. **Shortcut.** BST uses value divergence; general tree uses postorder hit aggregation. **Related.** Distance between nodes, LCA of deepest leaves, subtree contains target.

### 6. Invariant

After both child calls return, `left` and `right` faithfully summarize target presence or an LCA inside each child subtree. If both are non-null, no descendant can contain both targets because they are split across children.

### 7. Visual Explanation

```diagram
{"type":"tree","values":[6,2,8,0,4,7,9,null,null,3,5],"labels":{"0":"6 = LCA","1":"p=2","2":"q=8","3":"0","4":"4","5":"7","6":"9","9":"3","10":"5"},"highlights":{"0":"green","1":"primary","2":"primary"},"edge_highlights":[[0,1],[0,2]]}
```

```diagram
{"type":"tree","values":[3,5,1,6,2,0,8,null,null,7,4],"labels":{"0":"3 = LCA","1":"p=5","2":"q=1","3":"6","4":"2","5":"0","6":"8","9":"7","10":"4"},"highlights":{"0":"green","1":"primary","2":"primary"},"edge_highlights":[[0,1],[0,2]]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"recursion","nodes":[{"id":"n","label":"node","x":2,"y":0,"role":"primary"},{"id":"l","label":"left result","x":1,"y":1,"role":"amber"},{"id":"r","label":"right result","x":3,"y":1,"role":"amber"},{"id":"b","label":"both hit → node","x":2,"y":2,"role":"green"},{"id":"o","label":"one hit → bubble up","x":4,"y":2,"role":"muted"}],"edges":[{"from":"n","to":"l","label":"dfs(left)","color":"dark"},{"from":"n","to":"r","label":"dfs(right)","color":"dark"},{"from":"l","to":"b","label":"hit","color":"green"},{"from":"r","to":"b","label":"hit","color":"green"},{"from":"r","to":"o","label":"single side","color":"amber","dash":true}]}
```

### 9. Walkthrough

For `p=5`, `q=1`, root `3` receives non-null results from both children and returns itself. For `p=5`, `q=4`, node `5` matches `p`; because targets are guaranteed present, returning `5` is correct—the ancestor target is the LCA.

### 10. Why It Works

Postorder lets descendants claim an LCA before ancestors. When targets split across the current node's children, the current node is the first possible common ancestor on both paths. When only one side returns a hit, bubbling it upward preserves the only possible answer found so far.

### 11. Java

```java
class LowestCommonAncestor {
    TreeNode lowestCommonAncestorBST(TreeNode root, TreeNode p, TreeNode q) {
        int a = p.val, b = q.val;
        TreeNode cur = root;
        while (cur != null) {
            if (a < cur.val && b < cur.val) cur = cur.left;
            else if (a > cur.val && b > cur.val) cur = cur.right;
            else return cur;
        }
        return null;
    }

    TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) return root;
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        if (left != null && right != null) return root;
        return left != null ? left : right;
    }
}
```

### 12. Code Walkthrough

The BST version descends until both values no longer choose the same side. The general version uses object identity, not value equality. Its return value is simultaneously a presence signal and, once complete, the final LCA.

### 13. Complexity

!!! complexity "Complexity"
    **BST:** T O(h), S O(1). **General:** T O(n), S O(h). Height is O(log n) balanced and O(n) skewed.

### 14. Edge Cases

If one node is ancestor of the other, return that ancestor. Duplicate values are safe only in the object-identity general-tree version. If nodes may be absent, return a tuple with found counts.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Comparing values in the general tree, assuming a BST when the input is not ordered, or forgetting the absent-node variant where returning a single found target is insufficient.

### 16. Optimization

BST LCA is already O(1) space iteratively. For many static-tree queries, preprocess depth and binary-lifting ancestors, or use Euler tour + RMQ.

### 17. Alternatives

Root-to-node paths are easy but allocate. Parent pointers allow walking ancestors with a set. Tarjan offline LCA handles batched queries.

### 18. Interview Follow-Ups

Handle missing nodes, N-ary trees, multiple target nodes, or repeated queries. The general bubbling pattern extends to all children.

### 19. Variations

Distance between two nodes, smallest subtree containing all deepest nodes, and LCA of multiple nodes all reuse postorder aggregation.

### 20. Pattern Connection

LCA is child-signal aggregation: children return constrained facts, while the parent decides whether a cross-child structure has been completed.

---

## Diameter of Binary Tree

!!! pattern "Pattern: Tree DP · T: O(n) · S: O(h)"
    **Signals:** longest path between any two nodes, answer may pass through a node using both children.

### Problem

Return the number of edges on the longest path between any two nodes in a binary tree.

### Key Observation

!!! key "Key observation"
    The helper returns height upward, but the global answer considers `leftHeight + rightHeight` at every node as the best path turning through that node.

### Invariant

`height(node)` returns node-count height. After it returns, `best` has considered every diameter whose highest turning point lies in `node`'s subtree.

### Diagram

```diagram
{"type":"tree","values":[1,2,3,4,5],"labels":{"0":"through=3 edges","1":"2","2":"3","3":"4","4":"5"},"highlights":{"0":"green","3":"primary","4":"primary","2":"primary"},"edge_highlights":[[3,1],[1,0],[0,2]]}
```

### Java

```java
class Diameter {
    private int best;

    int diameterOfBinaryTree(TreeNode root) {
        best = 0;
        height(root);
        return best;
    }

    private int height(TreeNode node) {
        if (node == null) return 0;
        int left = height(node.left);
        int right = height(node.right);
        best = Math.max(best, left + right);
        return 1 + Math.max(left, right);
    }
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(h) recursion depth.

### Pattern Connection

Diameter is maximum path sum without weights. It teaches the split between the upward contribution and the through-node global candidate.

---

## Binary Tree Maximum Path Sum

!!! pattern "Pattern: Tree DP · T: O(n) · S: O(h)"
    **Signals:** maximum path anywhere, negative values, path may start and end at arbitrary nodes.

### 1. Problem

Given a non-empty binary tree with possibly negative values, return the maximum sum of any connected path with no repeated node. The path does not need to pass through the root or end at leaves.

### 2. Intuition

A parent can extend only one child branch; two branches would fork. But the best completed path may turn at the current node and use both children. Therefore return a **single-branch gain** upward and update a global **through-node** answer locally.

### 3. Naive

Enumerating all node pairs and computing path sums is O(n²) or worse. Every valid path has one highest turning node, so one postorder traversal can evaluate all candidates.

### 4. Key Observation

!!! key "Key observation"
    `gain(node)` returns the maximum sum of a path that starts at `node` and goes downward through at most one child. The global candidate is `node.val + max(0,leftGain) + max(0,rightGain)`, allowed to use both sides because it is not returned upward.

### 5. Pattern Recognition

**Signals.** "Path anywhere", negatives, no repeated node. **Shortcut.** If returning both child branches would be illegal for the parent, return one branch and track the two-branch answer globally. **Related.** Diameter, longest univalue path, leaf-to-leaf max path.

### 6. Invariant

After `gain(node)` returns, `best` is the maximum path sum fully contained in `node`'s subtree, and the return value is the best extendable one-branch path beginning at `node`.

### 7. Visual Explanation

```diagram
{"type":"tree","values":[-10,9,20,null,null,15,7],"labels":{"0":"-10","1":"9","2":"20 turn","5":"15","6":"7"},"highlights":{"2":"green","5":"primary","6":"primary"},"edge_highlights":[[2,5],[2,6]]}
```

```diagram
{"type":"tree","values":[2,-1,3],"labels":{"0":"through=5 return=5","1":"-1 clipped","2":"3 kept"},"highlights":{"0":"green","1":"red","2":"primary"},"edge_highlights":[[0,2]]}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"recursion","nodes":[{"id":"n","label":"node","x":2,"y":0,"role":"primary"},{"id":"l","label":"left=max(0,gain(left))","x":0,"y":1,"role":"amber"},{"id":"r","label":"right=max(0,gain(right))","x":4,"y":1,"role":"amber"},{"id":"b","label":"best=max(best,node+left+right)","x":2,"y":2,"role":"green"},{"id":"ret","label":"return node+max(left,right)","x":2,"y":3,"role":"muted"}],"edges":[{"from":"n","to":"l","label":"postorder","color":"dark"},{"from":"n","to":"r","label":"postorder","color":"dark"},{"from":"l","to":"b","label":"through","color":"green"},{"from":"r","to":"b","label":"through","color":"green"},{"from":"b","to":"ret","label":"single branch","color":"primary"}]}
```

### 9. Walkthrough

For `[-10,9,20,null,null,15,7]`, leaves return gains 9, 15, and 7. Node 20 updates `best` with `20 + 15 + 7 = 42` and returns 35. Root computes 34, so the answer remains 42.

### 10. Why It Works

Every path has a unique highest node. The through-node update evaluates that path when the traversal reaches the highest node. The return value is restricted to one branch so ancestors can still form legal non-forking paths.

### 11. Java

```java
class MaxPathSum {
    private int best;

    int maxPathSum(TreeNode root) {
        best = Integer.MIN_VALUE;
        gain(root);
        return best;
    }

    private int gain(TreeNode node) {
        if (node == null) return 0;
        int left = Math.max(0, gain(node.left));
        int right = Math.max(0, gain(node.right));
        best = Math.max(best, node.val + left + right);
        return node.val + Math.max(left, right);
    }
}
```

### 12. Code Walkthrough

Negative child gains are clipped because a path can stop at the current node instead of accepting a harmful extension. `best` starts at `Integer.MIN_VALUE`, preserving correctness for all-negative trees.

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(h) recursion depth.

### 14. Edge Cases

All-negative trees return the largest single node. Single-node trees return that node. If constraints allow sums beyond `int`, promote `best` and gains to `long`.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Returning `node + left + right` upward creates an illegal fork. Initializing `best` to 0 breaks all-negative input. Forgetting to clip negative gains forces bad branches into good paths.

### 16. Optimization

This is optimal. A production style can return a small pair `(bestInside, gainUp)` instead of using mutable object state.

### 17. Alternatives

For root-to-leaf paths, no global through-node split is needed. For leaf-to-leaf variants, base cases change because a valid path may need two leaves.

### 18. Interview Follow-Ups

Return the actual path by recording the best turning node and chosen child branches. For N-ary trees, keep the top two non-negative child gains for the through candidate and return only the top one.

### 19. Variations

Diameter, longest univalue path, maximum leaf-to-leaf path, and maximum root-to-node path are all return-vs-global tree DP variants.

### 20. Pattern Connection

This is the flagship return-value/global-answer split: parents receive a constrained contribution; the global answer records completed paths at every possible turning node.

---

## Kth Smallest Element in a BST

!!! pattern "Pattern: Inorder BST · T: O(h + k) · S: O(h)"
    **Signals:** BST, kth/order statistic, sorted stream.

### Problem

Given a BST and 1-indexed `k`, return the kth smallest value.

### Key Observation

!!! key "Key observation"
    Inorder traversal of a BST emits values in increasing order. Stop exactly when the kth value is visited; do not materialize the full sorted list unless required.

### Invariant

The emitted sequence is the sorted prefix of the BST. The stack holds ancestors whose left side is exhausted but whose value is still pending.

### Diagram

```diagram
{"type":"tree","values":[5,3,6,2,4,null,null,1],"labels":{"7":"#1","3":"#2","1":"#3","4":"#4","0":"#5","2":"#6"},"highlights":{"1":"green","7":"primary","3":"primary"}}
```

### Java

```java
int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> st = new ArrayDeque<>();
    TreeNode cur = root;
    while (cur != null || !st.isEmpty()) {
        while (cur != null) {
            st.push(cur);
            cur = cur.left;
        }
        cur = st.pop();
        if (--k == 0) return cur.val;
        cur = cur.right;
    }
    throw new IllegalArgumentException("k exceeds node count");
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(h + k). **S:** O(h).

### Pattern Connection

This is inorder-as-sorted-iterator. For frequent kth queries, augment nodes with subtree sizes and descend by rank in O(h).

---

## Construct Binary Tree from Preorder and Inorder

!!! pattern "Pattern: Recursive Partitioning · T: O(n) · S: O(n)"
    **Signals:** preorder supplies roots, inorder supplies left/right partition, values are unique.

### 1. Problem

Given preorder and inorder traversals of the same binary tree with unique values, reconstruct the original tree.

### 2. Intuition

Preorder's next value is the current subtree root. Inorder tells which values belong left and right of that root. Use bounds rather than copying subarrays.

### 3. Naive

Linearly search inorder and copy left/right slices at every recursive call. On skewed trees this becomes O(n²) time and excessive allocation.

### 4. Key Observation

!!! key "Key observation"
    Keep a moving preorder index for the next root, and represent the current subtree by an inorder interval. The root's inorder index splits that interval into left and right subtrees.

### 5. Pattern Recognition

**Signals.** One traversal is root-first; another shows left-root-right. **Shortcut.** Preorder chooses root, inorder sizes children. **Related.** Inorder+postorder build, preorder with null markers, expression parsing.

### 6. Invariant

`build(inLeft, inRight)` consumes exactly the preorder segment for the inorder slice `inLeft..inRight` and returns that subtree root. Empty slices consume nothing and return null.

### 7. Visual Explanation

```diagram
{"type":"tree","values":[3,9,20,null,null,15,7],"labels":{"0":"pre[0]=3","1":"left [9]","2":"right [15,20,7]","5":"15","6":"7"},"highlights":{"0":"primary","1":"amber","2":"green"}}
```

```diagram
{"type":"tree","values":[20,15,7],"labels":{"0":"pre root=20","1":"left [15]","2":"right [7]"},"highlights":{"0":"primary","1":"amber","2":"green"}}
```

### 8. Algorithm Flow Diagram

```diagram
{"type":"recursion","nodes":[{"id":"c","label":"build(L,R)","x":2,"y":0,"role":"primary"},{"id":"root","label":"root=pre[preIndex++]","x":2,"y":1,"role":"amber"},{"id":"mid","label":"mid=index[root]","x":2,"y":2,"role":"green"},{"id":"left","label":"build(L,mid-1)","x":0,"y":3,"role":"muted"},{"id":"right","label":"build(mid+1,R)","x":4,"y":3,"role":"muted"}],"edges":[{"from":"c","to":"root","label":"non-empty","color":"dark"},{"from":"root","to":"mid","label":"partition","color":"dark"},{"from":"mid","to":"left","label":"left slice","color":"amber"},{"from":"mid","to":"right","label":"right slice","color":"green"}]}
```

### 9. Walkthrough

`preorder=[3,9,20,15,7]`, `inorder=[9,3,15,20,7]`. Root 3 splits inorder into `[9]` and `[15,20,7]`. Next preorder root 9 builds the left leaf. Next root 20 splits the right slice into 15 and 7.

### 10. Why It Works

Preorder guarantees the first unconsumed value for a subtree is its root. With unique values, the root's inorder position uniquely determines left and right subtree membership. Building left before right matches preorder's root-left-right order.

### 11. Java

```java
class BuildTree {
    private int preIndex;
    private int[] preorder;
    private Map<Integer, Integer> inorderIndex;

    TreeNode buildTree(int[] preorder, int[] inorder) {
        this.preorder = preorder;
        this.preIndex = 0;
        this.inorderIndex = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inorderIndex.put(inorder[i], i);
        }
        return build(0, inorder.length - 1);
    }

    private TreeNode build(int inLeft, int inRight) {
        if (inLeft > inRight) return null;
        int rootVal = preorder[preIndex++];
        TreeNode root = new TreeNode(rootVal);
        int mid = inorderIndex.get(rootVal);
        root.left = build(inLeft, mid - 1);
        root.right = build(mid + 1, inRight);
        return root;
    }
}
```

### 12. Code Walkthrough

`preIndex` is preorder state: one non-empty subtree consumes one root. `inLeft..inRight` is structural state: it defines the subtree. The map makes root lookup O(1).

### 13. Complexity

!!! complexity "Complexity"
    **T:** O(n). **S:** O(n) for the index map plus O(h) recursion stack.

### 14. Edge Cases

Empty arrays return null. Single-element arrays return one node. Skewed trees produce O(n) recursion depth. Duplicate values make reconstruction ambiguous without extra identity information.

### 15. Common Mistakes

!!! pitfall "Common mistakes"
    Building right before left with preorder input desynchronizes `preIndex`; copying subarrays bloats complexity; omitting the empty-slice base case causes out-of-bounds reads.

### 16. Optimization

Bounds plus an index map are the intended optimization. For production handling of extremely deep trees, consider iterative construction to avoid stack limits.

### 17. Alternatives

Inorder + postorder is symmetric, but when scanning postorder backward you build right before left. Preorder + postorder alone is ambiguous unless the tree is full.

### 18. Interview Follow-Ups

Validate inconsistent traversals, handle duplicates with occurrence IDs, or build from preorder with explicit null markers and no inorder traversal.

### 19. Variations

Construct BST from preorder using bounds, recover a tree from preorder depth notation, and build expression trees from prefix/infix notation.

### 20. Pattern Connection

This is divide-and-conquer partitioning: one representation identifies the pivot/root, another defines the subproblem boundaries.

---

## Serialize and Deserialize Binary Tree

!!! pattern "Pattern: Structural Encoding · T: O(n) · S: O(n)"
    **Signals:** persist arbitrary binary tree, null shape matters, values alone are insufficient.

### Problem

Convert a binary tree to a string and reconstruct the identical tree from that string.

### Key Observation

!!! key "Key observation"
    A traversal is reversible for a general binary tree only if it records null children. Preorder with `#` null markers deserializes naturally by consuming tokens recursively in the same order.

### Invariant

`write(node)` emits one token for `node` and then complete encodings of its children, using `#` for null. `read(tokens)` consumes exactly one subtree's encoding and returns its root.

### Diagram

```diagram
{"type":"tree","values":[1,2,3,null,null,4,5],"labels":{"0":"1","1":"2","2":"3","5":"4","6":"5"},"highlights":{"0":"primary","1":"amber","2":"green","5":"muted","6":"muted"}}
```

### Java

```java
class Codec {
    private static final String NULL = "#";
    private static final String SEP = ",";

    String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        write(root, sb);
        return sb.toString();
    }

    private void write(TreeNode node, StringBuilder sb) {
        if (node == null) {
            sb.append(NULL).append(SEP);
            return;
        }
        sb.append(node.val).append(SEP);
        write(node.left, sb);
        write(node.right, sb);
    }

    TreeNode deserialize(String data) {
        Deque<String> tokens = new ArrayDeque<>(Arrays.asList(data.split(SEP)));
        return read(tokens);
    }

    private TreeNode read(Deque<String> tokens) {
        String token = tokens.removeFirst();
        if (token.equals(NULL)) return null;
        TreeNode node = new TreeNode(Integer.parseInt(token));
        node.left = read(tokens);
        node.right = read(tokens);
        return node;
    }
}
```

### Complexity

!!! complexity "Complexity"
    **T:** O(n) serialize and O(n) deserialize. **S:** O(n) output/tokens plus O(h) recursion stack.

### Pattern Connection

Serialization is traversal plus structure. For BSTs, preorder with bounds can avoid null markers; for arbitrary binary trees, null markers or another structural channel is mandatory.
