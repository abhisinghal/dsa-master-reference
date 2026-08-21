## The Pattern

Binary Search on Answer turns an optimization question into repeated yes/no feasibility checks. Recognize wording like **minimize the maximum**, **maximize the minimum**, **smallest feasible X**, or "minimum capacity/speed/time so all work finishes." The key is that the array is often not sorted; the **answer range** is.

!!! pattern "Recognition signals"
    **Signals:** candidate answer is numeric; `can(x)` is monotone; direct construction is hard but checking a candidate is linear or near-linear. If `can(x)` flips from false→true, find the first true. If it flips true→false, find the last true.

```diagram
{"type":"searchspace","title":"Search the answer range, not the input array","values":[1,2,3,4,5,6,7,8,9,10],"lo":1,"mid":5,"hi":10,"eliminated":[1,2,3,4],"target":7,"caption":"For smallest feasible X, values below the boundary fail; binary search narrows on the first true."}
```

## The Invariant

Define `can(x)` so monotonicity is explicit. For "minimum X that works," maintain: all answers `< lo` are known impossible, all answers `>= hi` remain potentially feasible, and `hi` is a feasible candidate when initialized tightly. When `can(mid)` is true, keep `mid` and discard the right half above it only by moving `hi = mid`; when false, move `lo = mid + 1`.

## Template

```java
int minFeasible(int[] a) {
    int lo = lowerBound(a);
    int hi = upperBound(a);
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (can(a, mid)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

boolean can(int[] a, int x) {
    // Linear feasibility check: never mutate the search boundaries here.
    return true;
}
```

```diagram
{"type":"flow","width":460,"box":270,"title":"First feasible answer","steps":[{"type":"start","text":"lo = minimum possible\nhi = maximum possible"},{"type":"decision","text":"lo < hi?","yes":"yes","branch":{"label":"no","text":"return lo","role":"green"}},{"type":"process","text":"mid = lo + (hi - lo) / 2"},{"type":"decision","text":"can(mid)?","yes":"yes","branch":{"label":"no","text":"lo = mid + 1","role":"red"}},{"type":"process","text":"hi = mid"}]}
```

For "maximum minimum" problems, either invert the predicate or use upper-mid:

```java
while (lo < hi) {
    int mid = lo + (hi - lo + 1) / 2;
    if (can(mid)) lo = mid;
    else hi = mid - 1;
}
```

## Worked Recognition

- **Koko Eating Bananas** (Module 3): the answer is eating speed `k`. If Koko can finish at speed `k`, she can finish at any larger speed, so find the smallest feasible `k`.
- **Capacity to Ship Packages Within D Days** (Module 3): capacity `C` is the answer. If capacity `C` ships within `D` days, any larger capacity also works.
- **Book Allocation** (Module 3): minimize the maximum pages assigned to one student. `can(limit)` greedily counts students needed under that page limit.

## Complexity

!!! complexity "Complexity"
    **T:** O(checkCost · log R), where `R = hi - lo + 1`. For most array problems, `checkCost = O(n)`. **S:** usually O(1). Use `long` for sums, capacities, products, and time bounds.

## Common Pitfalls

!!! pitfall "Common pitfalls"
    Searching indices instead of the answer domain; writing a predicate that is not monotone; using loose bounds that overflow; returning `mid` after the loop; or updating `hi = mid - 1` in a first-true search and accidentally discarding the valid boundary.

## When NOT to use it

Do not use this pattern when feasibility is non-monotone, when the answer is categorical rather than ordered, or when a direct greedy/DP solution gives the optimum in one pass without the extra `log R` factor.
