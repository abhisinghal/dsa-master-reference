# Generates multi-step "complete run" SVG visualizations for all 21 pattern cards
# and replaces each card's existing svg + figcap in src/20-patterns.md.
import re, os

COL = {'r':'#dc2626','g':'#16a34a','b':'#2563eb','a':'#b7791f','m':'#64748b','k':'#0b1220'}

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def spans(s, base):
    out=''; cur=base
    for p in re.split(r'(\{[rgbamk]\}|\{/\})', s):
        if not p: continue
        if p=='{/}': cur=base
        elif len(p)==3 and p[0]=='{' and p[1] in COL: cur=COL[p[1]]
        else: out+=f'<tspan fill="{cur}">{esc(p)}</tspan>'
    return out

STY = {'.':('#f4f6f9','#cbd5e1',1,'#0b1220'),
       'A':('#eef5ff','#2563eb',2,'#0b1220'),
       'g':('#f0fdf4','#16a34a',2,'#0b1220'),
       'r':('#fef2f2','#dc2626',2,'#0b1220'),
       'd':('#eef1f5','#dfe4ea',1,'#9aa4b2'),
       'p':('#fff7ed','#e0a52b',2,'#7c5b12'),
       'f':('#dcfce7','#16a34a',2,'#065f46')}

def film(title, steps, width=None):
    x0=40; cw=40; stp=42
    ncols=max(len(s['cells']) for s in steps)
    annot=x0+ncols*stp+20
    W=width or max(650, annot+300)
    y=40; ys=[]
    for s in steps:
        ta=15 if s.get('above') else 4
        ba=24 if s.get('below') else 8
        rh=ta+32+ba
        ys.append((y,ta,rh)); y+=rh
    H=y+8
    o=[f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">']
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fbfcfe"/>')
    o.append(f'<text x="20" y="25" font-size="13" font-weight="700" fill="#2563eb">{esc(title)}</text>')
    for s,(y0,ta,rh) in zip(steps,ys):
        cy=y0+ta
        if s.get('hl'):
            o.append(f'<rect x="26" y="{y0}" width="{W-52}" height="{rh-4}" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-dasharray="4 3"/>')
        cells=s['cells']; style=s.get('style','.'*len(cells))
        for i,val in enumerate(cells):
            fill,stroke,sw,tc=STY[style[i] if i<len(style) else '.']
            x=x0+i*stp
            o.append(f'<rect x="{x}" y="{cy}" width="{cw}" height="32" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
            o.append(f'<text x="{x+cw//2}" y="{cy+21}" font-size="14" font-weight="700" fill="{tc}" text-anchor="middle">{esc(val)}</text>')
        for i,(lbl,c) in (s.get('above') or {}).items():
            o.append(f'<text x="{x0+i*stp+cw//2}" y="{cy-4}" font-size="10" font-weight="700" fill="{COL.get(c,c)}" text-anchor="middle">{esc(lbl)}</text>')
        for i,(lbl,c) in (s.get('below') or {}).items():
            cx=x0+i*stp+cw//2
            o.append(f'<line x1="{cx}" y1="{cy+34}" x2="{cx}" y2="{cy+40}" stroke="{COL.get(c,c)}" stroke-width="2"/>')
            o.append(f'<text x="{cx}" y="{cy+50}" font-size="10" font-weight="700" fill="{COL.get(c,c)}" text-anchor="middle">{esc(lbl)}</text>')
        if s.get('note'):
            o.append(f'<text x="{annot}" y="{cy+13}" font-size="12" font-weight="700">{spans(s["note"],"#0b1220")}</text>')
        if s.get('note2'):
            o.append(f'<text x="{annot}" y="{cy+29}" font-size="11">{spans(s["note2"],"#475569")}</text>')
        if s.get('result'):
            o.append(f'<text x="{W-24}" y="{cy+20}" font-size="12" font-weight="700" fill="#16a34a" text-anchor="end">{esc(s["result"])}</text>')
    o.append('</svg>')
    return "\n".join(o)

def C(vals): return [str(v) for v in vals]

SV = {}

# 2 Two Pointers
SV[2]=(film("Two Pointers — converge on a sorted array until the pair is found", [
 dict(cells=C([2,3,5,6,8,11]), style="g....r", below={0:('lo','g'),5:('hi','r')}, note="2 + 11 = 13  {r}> 9 → move hi left{/}"),
 dict(cells=C([2,3,5,6,8,11]), style="g...rd", below={0:('lo','g'),4:('hi','r')}, note="2 + 8 = 10  {r}> 9 → hi--{/}"),
 dict(cells=C([2,3,5,6,8,11]), style="g..rdd", below={0:('lo','g'),3:('hi','r')}, note="2 + 6 = 8  {b}< 9 → move lo right{/}"),
 dict(cells=C([2,3,5,6,8,11]), style="dg.gdd", below={1:('lo','g'),3:('hi','g')}, note="3 + 6 = 9  {g}= target ✓{/}", hl=True, result="found (1,3)"),
], ), "target = 9. Each step discards a number that provably can't help, so the whole scan is O(n) after sorting.")

# 4 Prefix Sum
SV[4]=(film("Prefix Sum — precompute once, then every range sum is one subtraction", [
 dict(cells=C([3,1,4,1,5]), style="....." , note="array a  (indices 0..4)"),
 dict(cells=C([0,3,4,8,9,14]), style="AAAAAA", note="pre[k] = sum of the first k elements"),
 dict(cells=C([0,3,4,8,9,14]), style=".r..g.", note="sum(1..3) = pre[4] − pre[1] = 9 − 3 = {g}6{/}", hl=True, result="O(1) / query"),
], ), "Build the prefix array in O(n); afterwards any range sum is pre[r+1] − pre[l] in O(1).")

# 5 Hashing (Two Sum)
SV[5]=(film("Hashing — one pass, remembering what you've seen (Two Sum, target 6)", [
 dict(cells=C([3,2,4]), style="A..", below={0:('i','b')}, note="need 6 − 3 = 3;  map {} → store 3"),
 dict(cells=C([3,2,4]), style="dA.", below={1:('i','b')}, note="need 6 − 2 = 4;  not in map → store 2"),
 dict(cells=C([3,2,4]), style="dgA", below={2:('i','b')}, note="need 6 − 4 = {g}2 → in map ✓{/}", note2="answer = indices (1, 2)", hl=True, result="O(n)"),
], ), "The map trades memory for O(1) recall, collapsing the O(n²) pair scan to a single pass.")

# 6 Monotonic Stack (next greater)
SV[6]=(film("Monotonic Stack — each bar is pushed and popped once (Next Greater Element)", [
 dict(cells=C([2,1,2,4,3]), style="A....", note="push 2  →  stack [2]"),
 dict(cells=C([2,1,2,4,3]), style=".A...", note="1 < 2 → push  →  stack [2, 1]"),
 dict(cells=C([2,1,2,4,3]), style="..A..", note="2 > 1 → pop (NGE of 1 = 2), push  →  stack [2, 2]"),
 dict(cells=C([2,1,2,4,3]), style="...A.", note="4 pops 2, 2 (their NGE = 4)  →  stack [4]"),
 dict(cells=C([2,1,2,4,3]), style="....A", note="3 < 4 → push  →  stack [4, 3]", note2="what's left on the stack has no greater element to the right", hl=True, result="O(n)"),
], ), "The stack stays decreasing; every pop is the moment an element finds its next-greater neighbour.")

# 7 Binary Search
SV[7]=(film("Binary Search — each guess throws away half (target 9)", [
 dict(cells=C([1,3,5,7,9,11,13]), style="...A...", below={0:('lo','m'),3:('mid','b'),6:('hi','m')}, note="mid = a[3] = 7  {b}< 9 → go right{/}"),
 dict(cells=C([1,3,5,7,9,11,13]), style="dddd.A.", below={4:('lo','m'),5:('mid','b'),6:('hi','m')}, note="mid = a[5] = 11  {r}> 9 → go left{/}"),
 dict(cells=C([1,3,5,7,9,11,13]), style="ddddfdd", below={4:('lo=mid=hi','b')}, note="mid = a[4] = 9  {g}= target ✓{/}", hl=True, result="~log n steps"),
], ), "Because the array is ordered, one comparison at the midpoint eliminates half the remaining range.")

# 8 Binary Search on Answer
SV[8]=(film("Binary Search on the Answer — feasibility is monotone F…F T…T", [
 dict(cells=C([1,2,3,4,5,6,7,8]), style="...A....", below={3:('mid','b')}, note="speed 4 fits? {g}yes → try slower (hi = 4){/}"),
 dict(cells=C([1,2,3,4,5,6,7,8]), style=".A..dddd", below={1:('mid','b')}, note="speed 2 fits? {r}no → go faster (lo = 3){/}"),
 dict(cells=C([1,2,3,4,5,6,7,8]), style="ddA.dddd", below={2:('mid','b')}, note="speed 3 fits? {r}no → lo = 4{/}"),
 dict(cells=C([1,2,3,4,5,6,7,8]), style="dddfdddd", note="{g}least feasible speed = 4 ✓{/}", hl=True, result="min that works"),
], ), "Feasibility flips false→true exactly once; binary-search that boundary, testing each guess in O(n).")

# 9 Top-K / Heap
SV[9]=(film("Top-K — a size-k min-heap keeps the k largest (k = 3)", [
 dict(cells=C([4,1,7,3,8,5]), style="A.....", note="push 4  →  min-heap {4}"),
 dict(cells=C([4,1,7,3,8,5]), style=".A....", note="push 1  →  {1, 4}"),
 dict(cells=C([4,1,7,3,8,5]), style="..A...", note="push 7  →  {1, 4, 7}"),
 dict(cells=C([4,1,7,3,8,5]), style="...A..", note="push 3, size > 3 → pop min 1  →  {3, 4, 7}"),
 dict(cells=C([4,1,7,3,8,5]), style="....A.", note="push 8, pop 3  →  {4, 7, 8}"),
 dict(cells=C([4,1,7,3,8,5]), style=".....A", note="push 5, pop 4  →  {5, 7, 8}", note2="heap root 5 = the 3rd largest", hl=True, result="O(n log k)"),
], ), "The heap only ever holds k items, so each element costs O(log k) to insert and evict.")

# 10 K-way Merge
SV[10]=(film("K-way Merge — a heap of list-heads yields the global next-smallest", [
 dict(cells=C([1]), style="g", note="heads {1ᴬ, 1ᴮ, 2ꟲ} → pop 1ᴬ; push 4ᴬ.  heap {1ᴮ, 2ꟲ, 4ᴬ}"),
 dict(cells=C([1,1]), style="gg", note="pop 1ᴮ; push 3ᴮ.  heap {2ꟲ, 3ᴮ, 4ᴬ}"),
 dict(cells=C([1,1,2]), style="ggg", note="pop 2ꟲ; push 6ꟲ.  heap {3ᴮ, 4ᴬ, 6ꟲ}"),
 dict(cells=C([1,1,2,3]), style="gggg", note="pop 3ᴮ.  heap {4ᴬ, 6ꟲ}"),
 dict(cells=C([1,1,2,3,4]), style="ggggg", note="pop 4ᴬ.  heap {6ꟲ}"),
 dict(cells=C([1,1,2,3,4,6]), style="gggggg", note="pop 6ꟲ → merged output complete", hl=True, result="O(N log k)"),
], ), "Lists A=[1,4], B=[1,3], C=[2,6]. The heap of current heads always surfaces the next output.")

# 13 Topological Sort
SV[13]=(film("Topological Sort (Kahn) — repeatedly emit an in-degree-0 node", [
 dict(cells=C([0,1,2,3]), style="A...", note="in-degree [0,1,1,2];  queue [0]"),
 dict(cells=C([0,1,2,3]), style="fAA.", note="emit 0 → order [0];  decrement → queue [1, 2]"),
 dict(cells=C([0,1,2,3]), style="ffA.", note="emit 1 → [0,1];  node 3 in-degree 2 → 1"),
 dict(cells=C([0,1,2,3]), style="fffA", note="emit 2 → [0,1,2];  node 3 in-degree → 0 → queue [3]"),
 dict(cells=C([0,1,2,3]), style="ffff", note="emit 3 → order [0,1,2,3] ✓", note2="if the queue empties before all nodes emit, a cycle exists", hl=True, result="O(V+E)"),
], ), "Edges 0→1, 0→2, 1→3, 2→3. Emit a node once its prerequisites are all done.")

# 14 Union-Find
SV[14]=(film("Union-Find — merge sets as edges arrive; 'same group?' is ~O(1)", [
 dict(cells=C([0,1,2,3,4]), style="gg...", note="union(0,1)  →  {0,1} {2} {3} {4}"),
 dict(cells=C([0,1,2,3,4]), style="ggAA.", note="union(2,3)  →  {0,1} {2,3} {4}"),
 dict(cells=C([0,1,2,3,4]), style="gggg.", note="union(1,3) links the two sets  →  {0,1,2,3} {4}", note2="path compression flattens parent pointers on the way up", hl=True, result="2 components"),
], ), "Each node points at a set representative; unions and 'find' run in near-constant amortized time.")

# 15 Greedy (Jump Game II)
SV[15]=(film("Greedy — farthest-reach jumps (Jump Game II)", [
 dict(cells=C([2,3,1,1,4]), style="A....", below={0:('i','b')}, note="i=0: reach = 0+2 = 2;  end of jump 1 = index 2"),
 dict(cells=C([2,3,1,1,4]), style="gAg..", below={1:('i','b')}, note="i=1: farthest = max(2, 1+3) = 4"),
 dict(cells=C([2,3,1,1,4]), style="ggAgg", below={2:('i','b')}, note="i=2 = end → {g}take jump 2{/}; new end = 4"),
 dict(cells=C([2,3,1,1,4]), style="ggggf", note="index 4 reached", hl=True, result="min jumps = 2"),
], ), "Extend the reachable frontier as you scan; jump only when you hit the current frontier's end.")

# 18 Dynamic Programming (Climbing Stairs)
SV[18]=(film("Dynamic Programming — fill the table once (Climbing Stairs)", [
 dict(cells=C([1,1,'?','?','?','?']), style="gg....", note="base: dp[0] = dp[1] = 1"),
 dict(cells=C([1,1,2,'?','?','?']), style="ggA...", note="dp[2] = dp[1] + dp[0] = 2"),
 dict(cells=C([1,1,2,3,'?','?']), style="gggA..", note="dp[3] = dp[2] + dp[1] = 3"),
 dict(cells=C([1,1,2,3,5,'?']), style="ggggA.", note="dp[4] = dp[3] + dp[2] = 5"),
 dict(cells=C([1,1,2,3,5,8]), style="gggggf", note="dp[5] = dp[4] + dp[3] = 8 ✓", note2="each state solved once, then reused → O(n)", hl=True, result="ways to top"),
], ), "State dp[i] = ways to reach step i. Every subproblem is computed once and reused.")

# 20 Bit Manipulation (Single Number, XOR)
SV[20]=(film("Bit Manipulation — XOR cancels pairs (Single Number)", [
 dict(cells=C([4,1,2,1,2]), style="A....", note="acc = 0 ^ 4 = 4"),
 dict(cells=C([4,1,2,1,2]), style=".A...", note="acc = 4 ^ 1 = 5"),
 dict(cells=C([4,1,2,1,2]), style="..A..", note="acc = 5 ^ 2 = 7"),
 dict(cells=C([4,1,2,1,2]), style="...A.", note="acc = 7 ^ 1 = 6"),
 dict(cells=C([4,1,2,1,2]), style="....A", note="acc = 6 ^ 2 = {g}4{/}", note2="x ^ x = 0, so every duplicate cancels — the loner survives", hl=True, result="= 4"),
], ), "XOR is associative and self-inverse, so the order doesn't matter and pairs vanish to 0.")

# 21 Quickselect
SV[21]=(film("Quickselect — partition fixes the pivot's final rank (2nd largest)", [
 dict(cells=C([7,2,1,8,4,5]), style=".....p", note="pivot = 5 → partition: smaller left, larger right"),
 dict(cells=C([2,1,4,5,7,8]), style="dddp..", note="5 lands at index 3; the 2nd-largest is on the {b}right{/} side"),
 dict(cells=C([2,1,4,5,7,8]), style="....fp", note="recurse right → pivot 8; {g}2nd largest = 7{/}", hl=True, result="O(n) average"),
], ), "Only the side of the array containing rank k is recursed into, giving O(n) expected time.")

# ---------- bespoke structural runs ----------

def svg_open(w,h,title):
    return [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Arial, sans-serif">',
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="#fbfcfe"/>',
            f'<text x="20" y="25" font-size="13" font-weight="700" fill="#2563eb">{esc(title)}</text>']

# 3 Fast / Slow pointers
def fastslow():
    vals=[3,2,0,-4]; xs=[110,210,310,410]; steps=[(0,0),(1,2),(2,1),(3,3)]
    rowh=78; H=44+len(steps)*rowh; W=560
    o=svg_open(W,H,"Fast / Slow Pointers — two speeds must meet inside the loop")
    o.append('<defs><marker id="fa" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/></marker></defs>')
    for r,(sp,fp) in enumerate(steps):
        cy=68+r*rowh; meet=sp==fp
        if meet:
            o.append(f'<rect x="26" y="{cy-30}" width="{W-52}" height="64" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-dasharray="4 3"/>')
        for i in range(3):
            o.append(f'<line x1="{xs[i]+18}" y1="{cy}" x2="{xs[i+1]-18}" y2="{cy}" stroke="#94a3b8" stroke-width="1.6" marker-end="url(#fa)"/>')
        # back edge n3 -> n1
        o.append(f'<path d="M {xs[3]} {cy-18} C {xs[3]} {cy-52}, {xs[1]} {cy-52}, {xs[1]} {cy-18}" fill="none" stroke="#cbd5e1" stroke-width="1.6" marker-end="url(#fa)"/>')
        for i,v in enumerate(vals):
            o.append(f'<circle cx="{xs[i]}" cy="{cy}" r="18" fill="#ffffff" stroke="#94a3b8" stroke-width="1.6"/>')
            o.append(f'<text x="{xs[i]}" y="{cy+5}" font-size="13" font-weight="700" fill="#0b1220" text-anchor="middle">{esc(v)}</text>')
        o.append(f'<circle cx="{xs[sp]-7}" cy="{cy+34}" r="6" fill="#2563eb"/><text x="{xs[sp]-7}" y="{cy+50}" font-size="10" font-weight="700" fill="#2563eb" text-anchor="middle">S</text>')
        o.append(f'<circle cx="{xs[fp]+7}" cy="{cy+34}" r="6" fill="#dc2626"/><text x="{xs[fp]+7}" y="{cy+50}" font-size="10" font-weight="700" fill="#dc2626" text-anchor="middle">F</text>')
        lab=["start","after 1 step","after 2 steps","meet ✓"][r]
        o.append(f'<text x="470" y="{cy+4}" font-size="11" font-weight="700" fill="#475569">{esc(lab)}</text>')
    o.append('</svg>')
    return "\n".join(o)
SV[3]=(fastslow(), "List 3→2→0→−4→(back to 2). Slow moves 1, fast moves 2; they collide inside the cycle (at −4).")

# 11 Merge Intervals
def intervals():
    W=640; H=210
    def sx(v): return 60+v*29
    o=svg_open(W,H,"Merge Intervals — sort by start, then fuse overlaps left→right")
    # axis
    o.append(f'<line x1="55" y1="176" x2="600" y2="176" stroke="#cbd5e1"/>')
    for v in [1,3,6,8,10,15,18]:
        o.append(f'<line x1="{sx(v)}" y1="172" x2="{sx(v)}" y2="180" stroke="#cbd5e1"/><text x="{sx(v)}" y="194" font-size="9" fill="#94a3b8" text-anchor="middle">{v}</text>')
    o.append('<text x="20" y="52" font-size="11" font-weight="700" fill="#475569">input</text>')
    raw=[(1,3,'#2563eb'),(2,6,'#2563eb'),(8,10,'#64748b'),(15,18,'#64748b')]
    for i,(a,b,c) in enumerate(raw):
        y=44+i*20
        o.append(f'<rect x="{sx(a)}" y="{y}" width="{sx(b)-sx(a)}" height="14" rx="4" fill="{c}" opacity="0.75"/>')
        o.append(f'<text x="{sx(a)-6}" y="{y+11}" font-size="9" fill="#64748b" text-anchor="end">[{a},{b}]</text>')
    o.append('<text x="20" y="150" font-size="11" font-weight="700" fill="#16a34a">merged</text>')
    for (a,b,c) in [(1,6,'#16a34a'),(8,10,'#16a34a'),(15,18,'#16a34a')]:
        o.append(f'<rect x="{sx(a)}" y="140" width="{sx(b)-sx(a)}" height="16" rx="4" fill="{c}" opacity="0.85"/>')
        o.append(f'<text x="{(sx(a)+sx(b))//2}" y="152" font-size="9" font-weight="700" fill="#ffffff" text-anchor="middle">[{a},{b}]</text>')
    o.append('<text x="300" y="112" font-size="11" fill="#dc2626">[1,3] & [2,6] overlap (2 ≤ 3) → [1,6]</text>')
    o.append('</svg>')
    return "\n".join(o)
SV[11]=(intervals(), "After sorting by start, an interval overlaps the running one iff next.start ≤ cur.end — one comparison per interval.")

# 12 Sweep Line
def sweep():
    W=640; H=210
    def sx(v): return 55+v*17
    o=svg_open(W,H,"Sweep Line — +1 at a start, −1 at an end; the running peak is the answer")
    o.append(f'<line x1="50" y1="150" x2="600" y2="150" stroke="#cbd5e1"/>')
    for v in [0,5,10,15,20,30]:
        o.append(f'<line x1="{sx(v)}" y1="146" x2="{sx(v)}" y2="154" stroke="#cbd5e1"/><text x="{sx(v)}" y="167" font-size="9" fill="#94a3b8" text-anchor="middle">{v}</text>')
    ivs=[(0,30),(5,10),(15,20)]
    for i,(a,b) in enumerate(ivs):
        y=42+i*18
        o.append(f'<rect x="{sx(a)}" y="{y}" width="{sx(b)-sx(a)}" height="12" rx="3" fill="#2563eb" opacity="0.65"/>')
    # events
    for v,d in [(0,'+'),(5,'+'),(10,'-'),(15,'+'),(20,'-'),(30,'-')]:
        c='#16a34a' if d=='+' else '#dc2626'
        o.append(f'<text x="{sx(v)}" y="112" font-size="10" font-weight="700" fill="{c}" text-anchor="middle">{d}1</text>')
    # running count line
    pts=[(0,1),(5,2),(10,1),(15,2),(20,1),(30,0)]
    path="M "+f"{sx(0)} {150-1*22}"
    prev=1
    for v,cnt in pts:
        path+=f" L {sx(v)} {150-prev*22} L {sx(v)} {150-cnt*22}"
        prev=cnt
    o.append(f'<path d="{path} L {sx(30)} 150" fill="none" stroke="#e0a52b" stroke-width="2"/>')
    o.append('<text x="270" y="132" font-size="11" font-weight="700" fill="#b7791f">running count peaks at 2 → 2 rooms</text>')
    o.append('</svg>')
    return "\n".join(o)
SV[12]=(sweep(), "Meetings [0,30],[5,10],[15,20]. Sweep the +1/−1 events in time order; the maximum running sum is the peak concurrency.")

# 16 Backtracking (subset tree)
def backtrack():
    W=620; H=240
    o=svg_open(W,H,"Backtracking — choose → recurse → un-choose (all subsets of [1,2,3])")
    nodes={'[]':(300,44),'[1]':(150,104),'[2]':(310,104),'[3]':(470,104),
           '[1,2]':(110,166),'[1,3]':(210,166),'[2,3]':(360,166),'[1,2,3]':(110,222)}
    edges=[('[]','[1]'),('[]','[2]'),('[]','[3]'),('[1]','[1,2]'),('[1]','[1,3]'),('[2]','[2,3]'),('[1,2]','[1,2,3]')]
    for a,b in edges:
        x1,y1=nodes[a]; x2,y2=nodes[b]
        o.append(f'<line x1="{x1}" y1="{y1+13}" x2="{x2}" y2="{y2-13}" stroke="#cbd5e1" stroke-width="1.5"/>')
    for lbl,(x,y) in nodes.items():
        leaf = lbl in ('[1,2,3]','[1,3]','[2,3]','[3]')
        fill,st = ('#f0fdf4','#16a34a') if leaf else ('#eef5ff','#2563eb')
        w=max(30,10+len(lbl)*8)
        o.append(f'<rect x="{x-w//2}" y="{y-13}" width="{w}" height="26" rx="6" fill="{fill}" stroke="{st}" stroke-width="1.6"/>')
        o.append(f'<text x="{x}" y="{y+5}" font-size="11" font-weight="700" fill="#0b1220" text-anchor="middle">{esc(lbl)}</text>')
    o.append('<text x="360" y="210" font-size="11" fill="#475569">every node is one partial choice;</text>')
    o.append('<text x="360" y="226" font-size="11" fill="#475569">undo on the way back up → 2ⁿ subsets</text>')
    o.append('</svg>')
    return "\n".join(o)
SV[16]=(backtrack(), "Each downward edge 'includes' the next element; the un-choose step on return lets one code path enumerate every subset.")

# 17 Divide & Conquer (merge sort)
def mergesort():
    W=620; H=250
    o=svg_open(W,H,"Divide & Conquer — split to singletons, merge sorted halves back up")
    def box(x,y,txt,c='#2563eb',fill='#eef5ff'):
        w=max(40,14+len(txt)*9)
        o.append(f'<rect x="{x-w//2}" y="{y-14}" width="{w}" height="28" rx="6" fill="{fill}" stroke="{c}" stroke-width="1.6"/>')
        o.append(f'<text x="{x}" y="{y+5}" font-size="12" font-weight="700" fill="#0b1220" text-anchor="middle">{esc(txt)}</text>')
    def line(x1,y1,x2,y2,c='#cbd5e1'):
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.5"/>')
    line(300,58,190,96); line(300,58,410,96)
    line(190,110,150,148); line(190,110,240,148); line(410,110,360,148); line(410,110,450,148)
    box(300,44,"5 2 4 1"); box(190,96,"5 2"); box(410,96,"4 1")
    box(150,148,"5"); box(240,148,"2"); box(360,148,"4"); box(450,148,"1")
    o.append('<text x="40" y="200" font-size="11" font-weight="700" fill="#16a34a">merge ↑</text>')
    box(190,200,"2 5",'#16a34a','#f0fdf4'); box(410,200,"1 4",'#16a34a','#f0fdf4')
    box(300,232,"1 2 4 5",'#16a34a','#dcfce7')
    line(190,186,190,214,'#a7f3d0'); line(410,186,410,214,'#a7f3d0')
    line(190,214,300,232,'#a7f3d0'); line(410,214,300,232,'#a7f3d0')
    o.append('</svg>')
    return "\n".join(o)
SV[17]=(mergesort(), "log n levels of splitting, then an O(n) merge per level → O(n log n). The clever work is the linear merge.")

# 19 Trie
def trie():
    W=560; H=258
    o=svg_open(W,H,"Trie — shared prefixes share nodes (insert: cat, car, dog)")
    nodes={'root':(280,44),'c':(190,104),'d':(390,104),'a':(190,158),'o':(390,158),
           't':(140,212),'r':(250,212),'g':(390,212)}
    edges=[('root','c'),('root','d'),('c','a'),('d','o'),('a','t'),('a','r'),('o','g')]
    ends={'t','r','g'}
    for a,b in edges:
        x1,y1=nodes[a]; x2,y2=nodes[b]
        o.append(f'<line x1="{x1}" y1="{y1+16}" x2="{x2}" y2="{y2-16}" stroke="#cbd5e1" stroke-width="1.5"/>')
    for lbl,(x,y) in nodes.items():
        if lbl=='root':
            o.append(f'<circle cx="{x}" cy="{y}" r="16" fill="#e2e8f0" stroke="#94a3b8"/><text x="{x}" y="{y+4}" font-size="9" fill="#475569" text-anchor="middle">root</text>')
            continue
        end = lbl in ends
        fill,st = ('#dcfce7','#16a34a') if end else ('#eef5ff','#2563eb')
        o.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{fill}" stroke="{st}" stroke-width="1.7"/>')
        o.append(f'<text x="{x}" y="{y+5}" font-size="13" font-weight="700" fill="#0b1220" text-anchor="middle">{esc(lbl)}</text>')
        if end:
            o.append(f'<text x="{x}" y="{y+30}" font-size="9" font-weight="700" fill="#16a34a" text-anchor="middle">end</text>')
    o.append('<text x="430" y="150" font-size="11" fill="#475569">"ca" is stored</text>')
    o.append('<text x="430" y="166" font-size="11" fill="#475569">once, shared by</text>')
    o.append('<text x="430" y="182" font-size="11" fill="#475569">cat &amp; car</text>')
    o.append('</svg>')
    return "\n".join(o)
SV[19]=(trie(), "A path spells a prefix; cat and car share the c-a nodes, so lookups are O(L) regardless of dictionary size.")

# ---------- rewrite the markdown ----------
path=os.path.join(os.path.dirname(__file__),"src","20-patterns.md")
md=open(path,encoding="utf-8").read()
parts=re.split(r'(?m)(^## \d+\. .*$)', md)
res=parts[0]; i=1; replaced=0
while i < len(parts):
    header=parts[i]; body=parts[i+1] if i+1<len(parts) else ''
    N=int(re.match(r'^## (\d+)\.',header).group(1))
    if N in SV:
        svg,cap=SV[N]
        newblock="```svg\n"+svg+"\n```\n<div class=\"figcap\">"+cap+"</div>"
        body,n=re.subn(r'```svg\n.*?\n```\n<div class="figcap">.*?</div>', lambda m: newblock, body, count=1, flags=re.DOTALL)
        if n==0:
            body,n=re.subn(r'```svg\n.*?\n```', lambda m: "```svg\n"+svg+"\n```", body, count=1, flags=re.DOTALL)
        replaced+=n
    res+=header+body; i+=2
open(path,"w",encoding="utf-8").write(res)
print("cards with svg replaced:", replaced, "of", len(SV), "generated")
