"""Execute the book's Java code against the same tests our reference passes.

Strategy: for each extracted solution, wrap it in a class + main() harness, compile,
run, and compare output to expected. This catches any actual bug in the book's code.
"""
import os, re, json, subprocess, tempfile, shutil, textwrap

with open("_extracted_solutions.json", encoding="utf-8") as fh:
    SOLUTIONS = json.load(fh)

TMP = tempfile.mkdtemp(prefix="dsa_val_")

# Per-slug: (Java class wrapper for the book's snippet, main() driver code)
# The snippet is spliced verbatim into the class body.

WRAPPERS = {
 "two-sum": {
   "main": r'''
     Solver s = new Solver();
     int[] r1 = s.twoSum(new int[]{2,7,11,15}, 9);
     System.out.println("[" + r1[0] + "," + r1[1] + "]");
     int[] r2 = s.twoSum(new int[]{3,2,4}, 6);
     System.out.println("[" + r2[0] + "," + r2[1] + "]");
     int[] r3 = s.twoSum(new int[]{3,3}, 6);
     System.out.println("[" + r3[0] + "," + r3[1] + "]");
   ''',
   "expected": ["[0,1]", "[1,2]", "[0,1]"],
   "method_name": "twoSum",
 },
 "product-of-array-except-self": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(java.util.Arrays.toString(s.productExceptSelf(new int[]{1,2,3,4})));
     System.out.println(java.util.Arrays.toString(s.productExceptSelf(new int[]{-1,1,0,-3,3})));
   ''',
   "expected": ["[24, 12, 8, 6]","[0, 0, 9, 0, 0]"],
   "method_name": "productExceptSelf",
 },
 "longest-consecutive-sequence": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.longestConsecutive(new int[]{100,4,200,1,3,2}));
     System.out.println(s.longestConsecutive(new int[]{0,3,7,2,5,8,4,6,0,1}));
     System.out.println(s.longestConsecutive(new int[]{}));
   ''',
   "expected": ["4","9","0"],
   "method_name": "longestConsecutive",
 },
 "daily-temperatures": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(java.util.Arrays.toString(s.dailyTemperatures(new int[]{73,74,75,71,69,72,76,73})));
     System.out.println(java.util.Arrays.toString(s.dailyTemperatures(new int[]{30,40,50,60})));
   ''',
   "expected": ["[1, 1, 4, 2, 1, 1, 0, 0]","[1, 1, 1, 0]"],
   "method_name": "dailyTemperatures",
 },
 "valid-parentheses": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.isValid("()"));
     System.out.println(s.isValid("()[]{}"));
     System.out.println(s.isValid("(]"));
     System.out.println(s.isValid("("));
     System.out.println(s.isValid("(()"));
   ''',
   "expected": ["true","true","false","false","false"],
   "method_name": "isValid",
 },
 "longest-repeating-character-replacement": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.characterReplacement("ABAB", 2));
     System.out.println(s.characterReplacement("AABABBA", 1));
     System.out.println(s.characterReplacement("ABBABCDEEE", 1));
     System.out.println(s.characterReplacement("ABBB", 2));
   ''',
   "expected": ["4","4","4","4"],
   "method_name": "characterReplacement",
 },
 "longest-substring-without-repeating-characters": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.lengthOfLongestSubstring("abcabcbb"));
     System.out.println(s.lengthOfLongestSubstring("bbbbb"));
     System.out.println(s.lengthOfLongestSubstring("pwwkew"));
     System.out.println(s.lengthOfLongestSubstring("abba"));
   ''',
   "expected": ["3","1","3","2"],
   "method_name": "lengthOfLongestSubstring",
 },
 "minimum-size-subarray-sum": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.minSubArrayLen(7, new int[]{2,3,1,2,4,3}));
     System.out.println(s.minSubArrayLen(4, new int[]{1,4,4}));
     System.out.println(s.minSubArrayLen(11, new int[]{1,1,1,1,1,1,1,1}));
   ''',
   "expected": ["2","1","0"],
   "method_name": "minSubArrayLen",
 },
 "minimum-window-substring": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.minWindow("ADOBECODEBANC", "ABC"));
     System.out.println(s.minWindow("a", "a"));
     System.out.println("[" + s.minWindow("a", "aa") + "]");
   ''',
   "expected": ["BANC","a","[]"],
   "method_name": "minWindow",
 },
 "3sum": {
   "main": r'''
     Solver s = new Solver();
     var r1 = s.threeSum(new int[]{-1,0,1,2,-1,-4});
     r1.sort(java.util.Comparator.comparing(Object::toString));
     System.out.println(r1);
     var r2 = s.threeSum(new int[]{0,1,1});
     System.out.println(r2);
     var r3 = s.threeSum(new int[]{0,0,0});
     System.out.println(r3);
   ''',
   "expected": ["[[-1, -1, 2], [-1, 0, 1]]","[]","[[0, 0, 0]]"],
   "method_name": "threeSum",
 },
 "container-with-most-water": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.maxArea(new int[]{1,8,6,2,5,4,8,3,7}));
     System.out.println(s.maxArea(new int[]{1,1}));
   ''',
   "expected": ["49","1"],
   "method_name": "maxArea",
 },
 "trapping-rain-water": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.trap(new int[]{0,1,0,2,1,0,1,3,2,1,2,1}));
     System.out.println(s.trap(new int[]{4,2,0,3,2,5}));
   ''',
   "expected": ["6","9"],
   "method_name": "trap",
 },
 "search-in-rotated-sorted-array": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.search(new int[]{4,5,6,7,0,1,2}, 0));
     System.out.println(s.search(new int[]{4,5,6,7,0,1,2}, 3));
     System.out.println(s.search(new int[]{1}, 0));
     System.out.println(s.search(new int[]{3,1}, 1));
   ''',
   "expected": ["4","-1","-1","1"],
   "method_name": "search",
 },
 "coin-change": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.coinChange(new int[]{1,2,5}, 11));
     System.out.println(s.coinChange(new int[]{2}, 3));
     System.out.println(s.coinChange(new int[]{1}, 0));
   ''',
   "expected": ["3","-1","0"],
   "method_name": "coinChange",
 },
 "sliding-window-maximum": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(java.util.Arrays.toString(s.maxSlidingWindow(new int[]{1,3,-1,-3,5,3,6,7}, 3)));
     System.out.println(java.util.Arrays.toString(s.maxSlidingWindow(new int[]{1}, 1)));
   ''',
   "expected": ["[3, 3, 5, 5, 6, 7]","[1]"],
   "method_name": "maxSlidingWindow",
 },
 "merge-intervals": {
   "main": r'''
     Solver s = new Solver();
     var r1 = s.merge(new int[][]{{1,3},{2,6},{8,10},{15,18}});
     StringBuilder sb1 = new StringBuilder();
     for (int[] iv : r1) sb1.append("[" + iv[0] + "," + iv[1] + "] ");
     System.out.println(sb1.toString().trim());
     var r2 = s.merge(new int[][]{{1,4},{4,5}});
     StringBuilder sb2 = new StringBuilder();
     for (int[] iv : r2) sb2.append("[" + iv[0] + "," + iv[1] + "] ");
     System.out.println(sb2.toString().trim());
   ''',
   "expected": ["[1,6] [8,10] [15,18]","[1,5]"],
   "method_name": "merge",
 },
 "maximum-subarray": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.maxSubArray(new int[]{-2,1,-3,4,-1,2,1,-5,4}));
     System.out.println(s.maxSubArray(new int[]{1}));
     System.out.println(s.maxSubArray(new int[]{5,4,-1,7,8}));
     System.out.println(s.maxSubArray(new int[]{-1,-2,-3}));
   ''',
   "expected": ["6","1","23","-1"],
   "method_name": "maxSubArray",
 },
 "house-robber": {
   "main": r'''
     Solver s = new Solver();
     System.out.println(s.rob(new int[]{1,2,3,1}));
     System.out.println(s.rob(new int[]{2,7,9,3,1}));
   ''',
   "expected": ["4","12"],
   "method_name": "rob",
 },
}

# Some snippets miss method signatures or use wildcard names.
# Add helper: normalize snippet — strip re-declared "int[] a" params vs "int[] nums" etc.

def normalize_snippet(slug, code):
    """The book's snippet is verbatim, sometimes using `a` where LC uses `nums`.
    We just wrap it AS-IS in a class; that works if the snippet is a whole method."""
    # Ensure the method name matches what the test harness calls.
    expected_name = WRAPPERS[slug]["method_name"]
    # Detect the actual method name in the snippet
    m = re.search(r'(?:\b(?:public|private|static)\s+)?[\w<>\[\]?, ]+\s+(\w+)\s*\([^)]*\)\s*{', code)
    if m and m.group(1) != expected_name:
        # rename in signature (first occurrence)
        code_renamed = re.sub(r'\b' + re.escape(m.group(1)) + r'\b', expected_name, code, count=1)
        return code_renamed
    return code

def wrap_and_compile(slug, code):
    """Wrap in a Solver class + Main class, compile, run, capture stdout."""
    wrapper = WRAPPERS.get(slug)
    if not wrapper:
        return None, None, "no wrapper"
    snippet = normalize_snippet(slug, code)
    # If the snippet is not a method (e.g. a class), we can't do a simple wrap.
    java_src = f"""
import java.util.*;
class Solver {{
{textwrap.indent(snippet, '    ')}
}}
public class Main {{
    public static void main(String[] args) {{
{textwrap.indent(wrapper['main'], '        ')}
    }}
}}
"""
    src_path = os.path.join(TMP, f"Main_{slug.replace('-','_')}.java")
    # Java requires the file to be named after the public class; keep filename "Main.java" per compile
    src_dir = tempfile.mkdtemp(prefix=f"j_{slug.replace('-','_')}_", dir=TMP)
    src_file = os.path.join(src_dir, "Main.java")
    with open(src_file, "w", encoding="utf-8") as fh:
        fh.write(java_src)
    # Compile
    r = subprocess.run(["javac", "-encoding", "UTF-8", src_file], capture_output=True, text=True, cwd=src_dir)
    if r.returncode != 0:
        return None, java_src, f"COMPILE ERROR:\n{r.stderr}"
    # Run
    r2 = subprocess.run(["java", "-cp", src_dir, "Main"], capture_output=True, text=True)
    if r2.returncode != 0:
        return None, java_src, f"RUNTIME ERROR:\n{r2.stderr}"
    return r2.stdout.strip().split("\n"), java_src, None

def main():
    print(f"Working in {TMP}\n")
    ok = 0; bad = 0
    fails = []
    for slug, entry in SOLUTIONS.items():
        if slug not in WRAPPERS:
            continue
        code = entry["code"]
        result, java_src, err = wrap_and_compile(slug, code)
        expected = WRAPPERS[slug]["expected"]
        if err:
            bad += 1
            fails.append((slug, entry["chapter"], "COMPILE/RUNTIME", err[:400]))
            print(f"  ✗ {slug} ({entry['chapter']}): {err[:120]}")
            continue
        if result == expected:
            ok += 1
            print(f"  ✓ {slug} ({entry['chapter']}): {len(expected)} tests pass")
        else:
            bad += 1
            fails.append((slug, entry["chapter"], "OUTPUT MISMATCH", f"got={result} expected={expected}"))
            print(f"  ✗ {slug} ({entry['chapter']}):")
            print(f"     got:      {result}")
            print(f"     expected: {expected}")
    print(f"\n=== SUMMARY ===")
    print(f"  Passed: {ok}")
    print(f"  Failed: {bad}")
    if fails:
        print("\n=== FAILURE DETAILS ===")
        for slug, chapter, kind, msg in fails:
            print(f"\n{slug} ({chapter}) — {kind}")
            print(f"  {msg}")

if __name__ == "__main__":
    main()
