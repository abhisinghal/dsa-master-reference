## The Pattern

Two pointers exploit ordered structure by moving two indices according to a dominance argument. Unlike sliding window, the pointers do not necessarily describe a live valid interval; they may converge from both ends, partition regions, or use one pointer as a writer while the other scans.

!!! pattern "Recognition signals"
    Sorted array pair/triple search, in-place compaction, partition around categories/pivots, duplicate removal, palindrome-style symmetry, or any proof that moving one side discards a dominated set of candidates.

```diagram
{"type":"array","values":[1,2,4,7,11,15],"pointers":[{"name":"lo","index":0,"color":"primary","side":"bottom"},{"name":"hi","index":5,"color":"accent","side":"bottom"}],"caption":"In a sorted array, if sum is too small move lo right; if too large move hi left."}
```

## The Invariant

The invariant is an exclusion boundary: all candidates outside the active pointer region have been proven impossible or already placed. For converging pointers, `[lo, hi]` contains every remaining feasible pair. For partitioning, regions such as `[0, low)`, `[low, mid)`, and `(high, n)` already have final meaning. For writer patterns, `[0, write)` is the compacted answer prefix.

## Template

```java
// Converging pointers on sorted input.
int[] twoSumSorted(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        long sum = (long) a[lo] + a[hi];
        if (sum == target) return new int[]{lo, hi};
        if (sum < target) lo++;
        else hi--;
    }
    return new int[]{-1, -1};
}

// Fast/slow-as-writer: keep a compacted prefix in-place.
int removeDuplicates(int[] a) {
    if (a.length == 0) return 0;
    int write = 1;
    for (int read = 1; read < a.length; read++) {
        if (a[read] != a[write - 1]) {
            a[write++] = a[read];
        }
    }
    return write;
}

// Dutch flag partition: three finalized regions.
void sortColors(int[] a) {
    int low = 0, mid = 0, high = a.length - 1;
    while (mid <= high) {
        if (a[mid] == 0) swap(a, low++, mid++);
        else if (a[mid] == 1) mid++;
        else swap(a, mid, high--);
    }
}

void swap(int[] a, int i, int j) {
    int tmp = a[i];
    a[i] = a[j];
    a[j] = tmp;
}
```

## Worked Recognition

- **Dutch National Flag (Three-Way Partition)**: in-place, three categories, single pass. The proof is entirely region invariants, not sorting.
- **Median of Two Sorted Arrays (partition binary search)**: not two pointers in its optimal form, but the sorted-boundary dominance idea is the same; Part I shows why binary search dominates naive convergence.
- **Reverse Linked List II (Reverse a Sublist)**: not an array two-pointer problem, but it reinforces pointer boundary discipline: preserve the prefix, mutate the active segment, reconnect suffix.

```diagram
{"type":"flow","width":430,"box":260,"title":"Sorted pair movement","steps":[{"type":"start","text":"lo = 0; hi = n - 1"},{"type":"decision","text":"a[lo] + a[hi] == target?","yes":"return pair","branch":{"label":"no","text":"compare sum","role":"primary"}},{"type":"decision","text":"sum < target?","yes":"lo++","branch":{"label":"no","text":"hi--","role":"red"}},{"type":"end","text":"stop when lo >= hi"}]}
```

## Complexity

!!! complexity "Complexity"
    **T:** Usually O(n) after any required sorting; 3Sum is O(n²) because each fixed first element runs a linear convergence. **S:** O(1) for in-place pointer movement, excluding output.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Applying converging pointers to unsorted input without a dominance proof; moving both pointers after an unequal comparison; forgetting duplicate-skips in pair/triple enumeration; incrementing `mid` after swapping with `high` in Dutch flag; confusing writer-pointer compaction with a validity window.

## When NOT to use it

Do not use two pointers when no ordering/partition invariant tells you which candidates can be discarded, when the problem needs arbitrary membership lookup instead of boundary movement, or when "contiguous valid interval" is the real signal — that is usually Sliding Window.
