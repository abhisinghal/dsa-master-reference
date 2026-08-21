#!/usr/bin/env python3
"""Add <JavaRunner> embed to top problems in src/.
Each embed goes RIGHT AFTER the LC-link line for a problem."""
import os, re, glob

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "gen", "src")

# Test cases per problem — used by JavaRunner via Judge0.
# Each test: input as stdin (n on line 1, array space-separated on line 2, target on line 3), expected output.
RUNNER_EMBEDS = {
    "two-sum": {
        "tests": [
            {"input": "4\n2 7 11 15\n9", "expected": "0 1"},
            {"input": "2\n3 3\n6",       "expected": "0 1"}
        ]
    },
    "longest-substring-without-repeating-characters": {
        "tests": [
            {"input": "abcabcbb", "expected": "3"},
            {"input": "bbbbb",    "expected": "1"},
            {"input": "pwwkew",   "expected": "3"}
        ]
    },
    "binary-search": {
        "tests": [
            {"input": "6\n-1 0 3 5 9 12\n9",  "expected": "4"},
            {"input": "6\n-1 0 3 5 9 12\n2",  "expected": "-1"}
        ]
    },
    "coin-change": {
        "tests": [
            {"input": "3\n1 2 5\n11", "expected": "3"},
            {"input": "1\n2\n3",     "expected": "-1"}
        ]
    },
    "reverse-linked-list": {
        "tests": [
            {"input": "5\n1 2 3 4 5", "expected": "5 4 3 2 1"},
            {"input": "2\n1 2",       "expected": "2 1"}
        ]
    },
    "climbing-stairs": {
        "tests": [
            {"input": "2", "expected": "2"},
            {"input": "3", "expected": "3"},
            {"input": "5", "expected": "8"}
        ]
    },
    "maximum-subarray": {
        "tests": [
            {"input": "9\n-2 1 -3 4 -1 2 1 -5 4", "expected": "6"},
            {"input": "1\n1",                     "expected": "1"}
        ]
    },
    "valid-parentheses": {
        "tests": [
            {"input": "()",     "expected": "true"},
            {"input": "()[]{}", "expected": "true"},
            {"input": "(]",     "expected": "false"}
        ]
    }
}

def add_runner(path: str, slug: str, cfg: dict) -> bool:
    """Add a JavaRunner embed to the given file for the given problem slug."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    # Skip if already has JavaRunner for this slug
    if f'problemSlug="{slug}"' in content:
        return False
    # Find the LC-link line for this slug
    pattern = re.compile(rf"(\*\[↗ LeetCode:.*?https://leetcode\.com/problems/{re.escape(slug)}/?\)\*)")
    m = pattern.search(content)
    if not m:
        return False
    # Build tests JSON inline
    tests_json = "[" + ", ".join(
        '{ input: "' + t["input"].replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '", expected: "' + t["expected"].replace('"', '\\"').replace("\n", "\\n") + '" }'
        for t in cfg["tests"]
    ) + "]"
    embed = f'\n\n### Try it yourself\n\nEdit the Java code below and click **▶ Run tests** to check it against real examples. Powered by [Judge0](https://ce.judge0.com); your code auto-saves in your browser.\n\n<JavaRunner problemSlug="{slug}" :tests=\'{tests_json}\' />\n'
    # Insert AFTER the LC link line
    new_content = content[:m.end()] + embed + content[m.end():]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

def main():
    added = 0
    for path in sorted(glob.glob(os.path.join(SRC, "*.md"))):
        for slug, cfg in RUNNER_EMBEDS.items():
            if add_runner(path, slug, cfg):
                print(f"  {os.path.basename(path)}: +JavaRunner for {slug}")
                added += 1
    print(f"\nTotal JavaRunner embeds added: {added}")

if __name__ == "__main__":
    main()
