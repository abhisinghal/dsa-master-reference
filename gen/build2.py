#!/usr/bin/env python3
# Builds from src2/ → DSA_MASTER_REFERENCE8 output.
# Runs the same build.py logic but with different SRC + OUT_MD.
import os, sys, subprocess, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))

# Monkey-patch environment so build.py picks up src2/ and v8 output
os.environ["DSA_SRC_DIR"] = "src2"
os.environ["DSA_OUT_MD"] = r"C:\Users\absinghal\Downloads\Int\DSA_MASTER_REFERENCE9.md"
os.environ["DSA_OUT_HTML_LIGHT"] = os.path.join(ROOT, "output8.html")
os.environ["DSA_OUT_HTML_DARK"] = os.path.join(ROOT, "output8_dark.html")

# Read build.py, override constants, execute
with open(os.path.join(ROOT, "build.py"), encoding="utf-8") as f:
    code = f.read()

# Simple textual overrides
code = code.replace('SRC  = os.path.join(ROOT, "src")',
                    'SRC  = os.path.join(ROOT, os.environ.get("DSA_SRC_DIR", "src"))')
code = code.replace(r'OUT_MD = r"C:\Users\absinghal\Downloads\Int\DSA_MASTER_REFERENCE7.md"',
                    r'OUT_MD = os.environ.get("DSA_OUT_MD", r"C:\Users\absinghal\Downloads\Int\DSA_MASTER_REFERENCE7.md")')
# Override output.html path
code = code.replace('"output.html"',
                    'os.environ.get("DSA_OUT_HTML_LIGHT", "output.html")')
code = code.replace('"output_dark.html"',
                    'os.environ.get("DSA_OUT_HTML_DARK", "output_dark.html")')

exec(compile(code, "build.py", "exec"), {"__name__": "__main__", "__file__": os.path.join(ROOT, "build.py")})
