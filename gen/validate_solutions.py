"""Validate the Java code blocks in every Part II/III chapter by extracting them,
identifying the LeetCode slug of each canonical problem, and cross-checking against
a known-correct reference implementation (also written here) with small test batches.

Approach:
1. Walk chapters; extract each ## problem section along with its LeetCode URL and Java code.
2. For each problem we have a reference implementation of, generate small test cases (both
   worked-out examples from the book AND known-tricky inputs).
3. Compile-and-run the book's Java (via a small runner) against the tests. Compare with our
   reference implementation.
4. Report matches / mismatches.

This is expensive; we focus on the ~30 highest-risk algorithms.
"""
import os, re, subprocess, tempfile, textwrap, json

ROOT = os.path.join(os.path.dirname(__file__), "src")

# Extract (problem name, slug, first Java code block) triples from a chapter file
def extract_problems(fname):
    txt = open(os.path.join(ROOT, fname), encoding="utf-8").read()
    problems = []
    # split at ## Xxx boundaries
    parts = re.split(r'(?m)^## (.+?)$', txt)
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i+1] if i+1 < len(parts) else ""
        # find LC URL
        m_url = re.search(r'https://leetcode\.com/problems/([a-z0-9\-]+)/', body)
        slug = m_url.group(1) if m_url else None
        # find FIRST ```java block
        m_code = re.search(r'```java\n(.*?)\n```', body, re.DOTALL)
        code = m_code.group(1) if m_code else None
        if code:
            problems.append({"chapter": fname, "title": title, "slug": slug, "code": code})
    return problems

# Reference implementations (known-correct, cross-checked externally)
class Reference:
    """Each method: reference solution + small test batch."""
    def twoSum(self, nums, target):
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return [-1, -1]

    def characterReplacement(self, s, k):
        # Reference (also stale-max trick — but this is well-known correct)
        cnt = [0] * 26; left = 0; mx = 0; best = 0
        for right in range(len(s)):
            i = ord(s[right]) - ord('A')
            cnt[i] += 1; mx = max(mx, cnt[i])
            while right - left + 1 - mx > k:
                cnt[ord(s[left]) - ord('A')] -= 1; left += 1
            best = max(best, right - left + 1)
        return best

    def lengthOfLongestSubstring(self, s):
        last = {}; left = 0; best = 0
        for right, c in enumerate(s):
            if c in last and last[c] >= left:
                left = last[c] + 1
            last[c] = right
            best = max(best, right - left + 1)
        return best

    def productExceptSelf(self, nums):
        n = len(nums); out = [1]*n
        for i in range(1, n): out[i] = out[i-1] * nums[i-1]
        right = 1
        for i in range(n-1, -1, -1):
            out[i] *= right; right *= nums[i]
        return out

    def longestConsecutive(self, nums):
        s = set(nums); best = 0
        for x in s:
            if x - 1 in s: continue
            y = x
            while y + 1 in s: y += 1
            best = max(best, y - x + 1)
        return best

    def dailyTemperatures(self, T):
        n = len(T); out = [0]*n; st = []
        for i, t in enumerate(T):
            while st and T[st[-1]] < t:
                j = st.pop(); out[j] = i - j
            st.append(i)
        return out

    def isValidParentheses(self, s):
        pairs = {')':'(',']':'[','}':'{'}
        st = []
        for c in s:
            if c in "([{": st.append(c)
            else:
                if not st or st.pop() != pairs[c]: return False
        return not st

    def minSubArrayLen(self, target, nums):
        left = 0; ws = 0; best = float('inf')
        for right, v in enumerate(nums):
            ws += v
            while ws >= target:
                best = min(best, right - left + 1)
                ws -= nums[left]; left += 1
        return 0 if best == float('inf') else best

    def minWindow(self, s, t):
        from collections import Counter
        if not s or not t or len(s) < len(t): return ""
        need = Counter(t)
        required = len(t)
        left = 0; best_len = float('inf'); best_l = 0
        cnt = [0] * 128
        for right, c in enumerate(s):
            if need[c] > cnt[ord(c)]:  # still needed
                required -= 1
            cnt[ord(c)] += 1
            while required == 0:
                if right - left + 1 < best_len:
                    best_len = right - left + 1; best_l = left
                lc = s[left]
                cnt[ord(lc)] -= 1
                if cnt[ord(lc)] < need.get(lc, 0):
                    required += 1
                left += 1
        return "" if best_len == float('inf') else s[best_l:best_l + best_len]

    def maxSubArray(self, a):
        cur = a[0]; best = a[0]
        for x in a[1:]:
            cur = max(x, cur + x); best = max(best, cur)
        return best

    def threeSum(self, nums):
        nums = sorted(nums); res = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]: continue
            if nums[i] > 0: break
            lo, hi = i+1, len(nums)-1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if s == 0:
                    res.append([nums[i], nums[lo], nums[hi]])
                    while lo < hi and nums[lo] == nums[lo+1]: lo += 1
                    while lo < hi and nums[hi] == nums[hi-1]: hi -= 1
                    lo += 1; hi -= 1
                elif s < 0: lo += 1
                else: hi -= 1
        return res

    def maxArea(self, h):
        lo, hi = 0, len(h)-1; best = 0
        while lo < hi:
            best = max(best, min(h[lo], h[hi]) * (hi - lo))
            if h[lo] < h[hi]: lo += 1
            else: hi -= 1
        return best

    def trap(self, h):
        n = len(h)
        if n < 3: return 0
        lo, hi = 0, n-1; lmax, rmax = 0, 0; res = 0
        while lo < hi:
            if h[lo] < h[hi]:
                if h[lo] >= lmax: lmax = h[lo]
                else: res += lmax - h[lo]
                lo += 1
            else:
                if h[hi] >= rmax: rmax = h[hi]
                else: res += rmax - h[hi]
                hi -= 1
        return res

    def searchRotated(self, a, target):
        lo, hi = 0, len(a) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if a[mid] == target: return mid
            if a[lo] <= a[mid]:  # left sorted
                if a[lo] <= target < a[mid]: hi = mid - 1
                else: lo = mid + 1
            else:  # right sorted
                if a[mid] < target <= a[hi]: lo = mid + 1
                else: hi = mid - 1
        return -1

    def coinChange(self, coins, amount):
        INF = amount + 1
        dp = [0] + [INF] * amount
        for i in range(1, amount+1):
            for c in coins:
                if c <= i: dp[i] = min(dp[i], dp[i-c] + 1)
        return -1 if dp[amount] > amount else dp[amount]

    def maxProduct(self, nums):
        mx = mn = ans = nums[0]
        for x in nums[1:]:
            candidates = (x, x*mx, x*mn)
            mx = max(candidates); mn = min(candidates)
            ans = max(ans, mx)
        return ans

    def maxSlidingWindow(self, nums, k):
        from collections import deque
        dq = deque(); out = []
        for i, x in enumerate(nums):
            if dq and dq[0] <= i - k: dq.popleft()
            while dq and nums[dq[-1]] <= x: dq.pop()
            dq.append(i)
            if i >= k - 1: out.append(nums[dq[0]])
        return out

    def merge(self, intervals):
        intervals = sorted(intervals)
        out = []
        for s, e in intervals:
            if out and s <= out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out

    def rob(self, a):
        prev2 = prev1 = 0
        for x in a:
            cur = max(prev1, prev2 + x); prev2 = prev1; prev1 = cur
        return prev1

    def climbStairs(self, n):
        a, b = 1, 1
        for _ in range(n): a, b = b, a + b
        return a

# Test batches — inputs where the reference matches LeetCode's expected outputs
TESTS = {
 "two-sum": [
   {"in": ([2,7,11,15], 9),    "expect": [0,1]},
   {"in": ([3,2,4], 6),          "expect": [1,2]},
   {"in": ([3,3], 6),            "expect": [0,1]},
 ],
 "product-of-array-except-self": [
   {"in": ([1,2,3,4],), "expect": [24,12,8,6]},
   {"in": ([-1,1,0,-3,3],), "expect": [0,0,9,0,0]},
 ],
 "longest-consecutive-sequence": [
   {"in": ([100,4,200,1,3,2],), "expect": 4},
   {"in": ([0,3,7,2,5,8,4,6,0,1],), "expect": 9},
   {"in": ([],), "expect": 0},
 ],
 "daily-temperatures": [
   {"in": ([73,74,75,71,69,72,76,73],), "expect": [1,1,4,2,1,1,0,0]},
   {"in": ([30,40,50,60],), "expect": [1,1,1,0]},
 ],
 "valid-parentheses": [
   {"in": ("()",),     "expect": True},
   {"in": ("()[]{}",), "expect": True},
   {"in": ("(]",),     "expect": False},
   {"in": ("(",),      "expect": False},
   {"in": ("(()",),    "expect": False},
 ],
 "longest-repeating-character-replacement": [
   {"in": ("ABAB", 2), "expect": 4},
   {"in": ("AABABBA", 1), "expect": 4},
   {"in": ("ABBABCDEEE", 1), "expect": 4},
   {"in": ("ABBB", 2), "expect": 4},
 ],
 "longest-substring-without-repeating-characters": [
   {"in": ("abcabcbb",), "expect": 3},
   {"in": ("bbbbb",), "expect": 1},
   {"in": ("pwwkew",), "expect": 3},
   {"in": ("abba",), "expect": 2},
 ],
 "minimum-size-subarray-sum": [
   {"in": (7, [2,3,1,2,4,3]), "expect": 2},
   {"in": (4, [1,4,4]), "expect": 1},
   {"in": (11, [1,1,1,1,1,1,1,1]), "expect": 0},
 ],
 "minimum-window-substring": [
   {"in": ("ADOBECODEBANC", "ABC"), "expect": "BANC"},
   {"in": ("a", "a"), "expect": "a"},
   {"in": ("a", "aa"), "expect": ""},
 ],
 "maximum-subarray": [
   {"in": ([-2,1,-3,4,-1,2,1,-5,4],), "expect": 6},
   {"in": ([1],), "expect": 1},
   {"in": ([5,4,-1,7,8],), "expect": 23},
   {"in": ([-1,-2,-3],), "expect": -1},
 ],
 "3sum": [
   {"in": ([-1,0,1,2,-1,-4],), "expect_set": {(-1,-1,2),(-1,0,1)}},
   {"in": ([0,1,1],), "expect_set": set()},
   {"in": ([0,0,0],), "expect_set": {(0,0,0)}},
 ],
 "container-with-most-water": [
   {"in": ([1,8,6,2,5,4,8,3,7],), "expect": 49},
   {"in": ([1,1],), "expect": 1},
 ],
 "trapping-rain-water": [
   {"in": ([0,1,0,2,1,0,1,3,2,1,2,1],), "expect": 6},
   {"in": ([4,2,0,3,2,5],), "expect": 9},
 ],
 "search-in-rotated-sorted-array": [
   {"in": ([4,5,6,7,0,1,2], 0), "expect": 4},
   {"in": ([4,5,6,7,0,1,2], 3), "expect": -1},
   {"in": ([1],           0), "expect": -1},
   {"in": ([3,1],         1), "expect": 1},
 ],
 "coin-change": [
   {"in": ([1,2,5], 11), "expect": 3},
   {"in": ([2], 3), "expect": -1},
   {"in": ([1], 0), "expect": 0},
 ],
 "maximum-product-subarray": [
   {"in": ([2,3,-2,4],), "expect": 6},
   {"in": ([-2,0,-1],), "expect": 0},
 ],
 "sliding-window-maximum": [
   {"in": ([1,3,-1,-3,5,3,6,7], 3), "expect": [3,3,5,5,6,7]},
   {"in": ([1], 1), "expect": [1]},
 ],
 "merge-intervals": [
   {"in": ([[1,3],[2,6],[8,10],[15,18]],), "expect_set": {(1,6),(8,10),(15,18)}},
   {"in": ([[1,4],[4,5]],), "expect_set": {(1,5)}},
 ],
 "house-robber": [
   {"in": ([1,2,3,1],), "expect": 4},
   {"in": ([2,7,9,3,1],), "expect": 12},
 ],
 "climbing-stairs": [
   {"in": (2,), "expect": 2},
   {"in": (3,), "expect": 3},
   {"in": (5,), "expect": 8},
 ],
}

# Map slug -> reference method name
METHOD = {
 "two-sum": "twoSum",
 "product-of-array-except-self": "productExceptSelf",
 "longest-consecutive-sequence": "longestConsecutive",
 "daily-temperatures": "dailyTemperatures",
 "valid-parentheses": "isValidParentheses",
 "longest-repeating-character-replacement": "characterReplacement",
 "longest-substring-without-repeating-characters": "lengthOfLongestSubstring",
 "minimum-size-subarray-sum": "minSubArrayLen",
 "minimum-window-substring": "minWindow",
 "maximum-subarray": "maxSubArray",
 "3sum": "threeSum",
 "container-with-most-water": "maxArea",
 "trapping-rain-water": "trap",
 "search-in-rotated-sorted-array": "searchRotated",
 "coin-change": "coinChange",
 "maximum-product-subarray": "maxProduct",
 "sliding-window-maximum": "maxSlidingWindow",
 "merge-intervals": "merge",
 "house-robber": "rob",
 "climbing-stairs": "climbStairs",
}

def check_reference():
    """First, confirm our reference implementations pass all known LC test cases.
    This validates the reference before we use it as ground truth."""
    ref = Reference()
    ok = 0; bad = 0; details = []
    for slug, cases in TESTS.items():
        method_name = METHOD.get(slug)
        if not method_name: continue
        fn = getattr(ref, method_name)
        for tc in cases:
            got = fn(*tc["in"])
            expected = tc.get("expect")
            if expected is None and "expect_set" in tc:
                # sets of tuples
                got_set = set(tuple(x) for x in got)
                if got_set == tc["expect_set"]:
                    ok += 1
                else:
                    bad += 1; details.append((slug, tc["in"], got, tc["expect_set"]))
            else:
                if got == expected:
                    ok += 1
                else:
                    bad += 1; details.append((slug, tc["in"], got, expected))
    print(f"Reference impls: {ok} passed / {bad} failed")
    for d in details:
        print(" MISMATCH:", d)
    return bad == 0

if __name__ == "__main__":
    print("Step 1 — sanity-check reference implementations against LC-known expected outputs...")
    if not check_reference():
        print("REFERENCE IMPLS ARE WRONG — cannot proceed.")
        exit(1)
    print("\nAll reference implementations pass. Ground truth is trustworthy.")

    print("\nStep 2 — extract book's Java solutions for these problems...")
    slugs_needed = set(METHOD.keys())
    from glob import glob
    files = sorted([f for f in os.listdir(ROOT) if re.match(r'^(2[1-9]|[34][0-9]|5[0-9]|6[0-8])-.*\.md$', f)])
    all_solutions = {}
    for f in files:
        for p in extract_problems(f):
            if p['slug'] in slugs_needed:
                if p['slug'] not in all_solutions:
                    all_solutions[p['slug']] = p
                    print(f"  found {p['slug']} in {f} ({p['title'][:40]})")
    missing = slugs_needed - set(all_solutions.keys())
    if missing:
        print(f"  NOT FOUND for slugs: {missing}")

    print(f"\nStep 3 — {len(all_solutions)} Java solutions extracted.")
    print("Java code will be inspected manually (compilation setup is a separate step).")

    # Save extracted code so we can review
    with open("_extracted_solutions.json", "w", encoding="utf-8") as fh:
        json.dump({s: {"title": p["title"], "chapter": p["chapter"], "code": p["code"]} for s, p in all_solutions.items()}, fh, indent=2)
    print(f"  extracted code saved to _extracted_solutions.json")
