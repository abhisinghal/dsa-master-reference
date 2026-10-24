"""
Deterministic SVG diagram engine for the DSA Master Reference book.

Every diagram in the book is generated from a compact JSON spec embedded in the
Markdown source inside a fenced ```diagram block. This keeps all figures
regenerable, consistent, and print-quality.

Public entry point:  render(spec: dict) -> str   (returns an <svg> ... </svg>)
"""

from html import escape
import re

INK      = "#1f2933"
MUTED    = "#64748b"
FAINT    = "#94a3b8"
PRIMARY  = "#2563eb"
PRIMARY_D= "#1e40af"
ACCENT   = "#0ea5e9"
AMBER    = "#f59e0b"
AMBER_BG = "#fef3c7"
GREEN    = "#10b981"
GREEN_BG = "#d1fae5"
RED      = "#ef4444"
RED_BG   = "#fee2e2"
PANEL    = "#f1f5f9"
PANEL2   = "#e2e8f0"
LINE     = "#cbd5e1"
WHITE    = "#ffffff"
PURPLE   = "#7c3aed"
PURPLE_BG= "#ede9fe"

MONO = "'JetBrains Mono','DejaVu Sans Mono',Consolas,monospace"
SANS = "'Inter','Segoe UI',Helvetica,Arial,sans-serif"

ROLE = {
    "": (WHITE, INK, LINE),
    "plain": (WHITE, INK, LINE),
    "panel": (PANEL, INK, LINE),
    "primary": (PRIMARY, WHITE, PRIMARY_D),
    "accent": ("#e0f2fe", INK, ACCENT),
    "amber": (AMBER_BG, "#92400e", AMBER),
    "green": (GREEN_BG, "#065f46", GREEN),
    "red": (RED_BG, "#991b1b", RED),
    "purple": (PURPLE_BG, "#5b21b6", PURPLE),
    "muted": (PANEL2, MUTED, LINE),
    "dark": (INK, WHITE, INK),
}


def _role(name):
    return ROLE.get(name or "", ROLE[""])


def _svg(width, height, body, cls="dfig"):
    return (
        f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'font-family="{SANS}" role="img">'
        f'{_defs()}{body}</svg>'
    )


def _defs():
    return (
        '<defs>'
        f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0 0L10 5L0 10z" fill="{INK}"/></marker>'
        f'<marker id="arrb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0 0L10 5L0 10z" fill="{PRIMARY}"/></marker>'
        f'<marker id="arrr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0 0L10 5L0 10z" fill="{RED}"/></marker>'
        f'<marker id="arrg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        f'markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0 0L10 5L0 10z" fill="{GREEN}"/></marker>'
        '</defs>'
    )


def _t(x, y, s, size=14, fill=INK, weight="normal", anchor="middle",
       family=SANS, style=""):
    style_attr = (' style="' + style + '"') if style else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}" text-anchor="{anchor}" font-family="{family}" '
        f'dominant-baseline="middle"{style_attr}>'
        f'{escape(str(s))}</text>'
    )


def _rect(x, y, w, h, fill=WHITE, stroke=LINE, rx=6, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def _line(x1, y1, x2, y2, stroke=INK, sw=1.5, marker=True, dash=None,
          mid="arr"):
    m = f' marker-end="url(#{mid})"' if marker else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{m}{d}/>')


def _title(x, y, text):
    if not text:
        return ""
    return _t(x, y, text, size=13, fill=MUTED, weight="600", anchor="middle",
              style="letter-spacing:.04em")


def _textw(s, size=13):
    if not s:
        return 0
    return int(len(str(s)) * size * 0.56) + 16


# --------------------------------------------------------------------------- ARRAY
def render_array(spec):
    values = spec.get("values", [])
    n = len(values)
    cell = spec.get("cell", 46)
    gap = spec.get("gap", 6)
    pointers = spec.get("pointers", [])
    highlights = spec.get("highlights", {})
    brackets = spec.get("brackets", [])
    show_index = spec.get("index", True)
    caption = spec.get("caption", "")
    title = spec.get("title", "")

    pad = 24
    top = 20
    if title:
        top += 24
    above = 0
    below_ptr = 0
    for p in pointers:
        if p.get("side", "top") == "top":
            above = max(above, 40)
        else:
            below_ptr = max(below_ptr, 40)
    bracket_space = 34 * len({b.get("row", 0) for b in brackets}) if brackets else 0
    idx_space = 22 if show_index else 0

    grid_y = top + above
    width = pad * 2 + n * cell + (n - 1) * gap
    height = grid_y + cell + idx_space + below_ptr + bracket_space + 20
    if caption:
        height += 22

    body = []
    if title:
        body.append(_title(width / 2, 18, title))

    def cx(i):
        return pad + i * (cell + gap) + cell / 2

    for i, v in enumerate(values):
        x = pad + i * (cell + gap)
        role = highlights.get(i, highlights.get(str(i), ""))
        bg, fg, st = _role(role)
        body.append(_rect(x, grid_y, cell, cell, fill=bg, stroke=st, rx=7,
                          sw=1.8 if role else 1.4))
        body.append(_t(x + cell / 2, grid_y + cell / 2, v, size=17, fill=fg,
                       weight="700", family=MONO))
        if show_index:
            body.append(_t(x + cell / 2, grid_y + cell + 13, i, size=12,
                           fill=FAINT, family=MONO))

    for p in pointers:
        i = p["index"]
        if i is None or i < 0 or i >= n:
            continue
        color = p.get("color", PRIMARY)
        name = p.get("name", "")
        side = p.get("side", "top")
        x = cx(i)
        if side == "top":
            y0 = grid_y - above + 6
            body.append(_t(x, y0, name, size=13, fill=color, weight="700",
                           family=MONO))
            body.append(_line(x, y0 + 10, x, grid_y - 3, stroke=color, sw=2))
        else:
            y0 = grid_y + cell + idx_space + 24
            body.append(_line(x, grid_y + cell + idx_space - 2, x, y0 - 12,
                              stroke=color, sw=2))
            body.append(_t(x, y0, name, size=13, fill=color, weight="700",
                           family=MONO))

    brow_y0 = grid_y + cell + idx_space + below_ptr + 14
    rows = sorted({b.get("row", 0) for b in brackets})
    for b in brackets:
        r = rows.index(b.get("row", 0))
        y = brow_y0 + r * 34
        a, z = b["from"], b["to"]
        x1 = pad + a * (cell + gap)
        x2 = pad + z * (cell + gap) + cell
        color = b.get("color", GREEN)
        body.append(f'<path d="M{x1:.1f} {y:.1f} L{x1:.1f} {y+8:.1f} '
                    f'L{x2:.1f} {y+8:.1f} L{x2:.1f} {y:.1f}" fill="none" '
                    f'stroke="{color}" stroke-width="2"/>')
        if b.get("label"):
            body.append(_t((x1 + x2) / 2, y + 20, b["label"], size=12,
                           fill=color, weight="700"))

    if caption:
        body.append(_t(width / 2, height - 12, caption, size=13, fill=MUTED))

    return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- FLOW
def render_flow(spec):
    steps = spec.get("steps", [])
    title = spec.get("title", "")
    w = spec.get("width", 460)
    box_w = spec.get("box", 300)
    cx = w / 2
    y = 24
    if title:
        y += 24
    gap = 30
    body = []
    if title:
        body.append(_title(cx, 20, title))

    positions = []
    for st in steps:
        kind = st.get("type", "process")
        text = st.get("text", "")
        lines = text.split("\n")
        h = 30 + 18 * len(lines)
        if kind == "decision":
            h = max(h, 74)
        positions.append((y, h, kind, st, lines))
        y += h + gap

    total_h = y - gap + 24
    max_right = w

    def draw_box(x0, yy, ww, hh, kind, lines):
        out = []
        if kind == "start" or kind == "end":
            bg, fg, stt = _role("primary" if kind == "start" else "dark")
            out.append(f'<rect x="{x0:.1f}" y="{yy:.1f}" width="{ww:.1f}" '
                       f'height="{hh:.1f}" rx="{hh/2:.1f}" fill="{bg}" '
                       f'stroke="{stt}" stroke-width="1.8"/>')
        elif kind == "decision":
            fg = "#92400e"
            mx, my = x0 + ww / 2, yy + hh / 2
            out.append(f'<path d="M{mx:.1f} {yy:.1f} L{x0+ww:.1f} {my:.1f} '
                       f'L{mx:.1f} {yy+hh:.1f} L{x0:.1f} {my:.1f} Z" '
                       f'fill="{AMBER_BG}" stroke="{AMBER}" stroke-width="1.8"/>')
        elif kind == "io":
            fg = INK
            sk = 14
            out.append(f'<path d="M{x0+sk:.1f} {yy:.1f} L{x0+ww:.1f} {yy:.1f} '
                       f'L{x0+ww-sk:.1f} {yy+hh:.1f} L{x0:.1f} {yy+hh:.1f} Z" '
                       f'fill="{PANEL}" stroke="{LINE}" stroke-width="1.6"/>')
        else:
            fg = INK
            out.append(_rect(x0, yy, ww, hh, fill=WHITE, stroke=PRIMARY, rx=8,
                             sw=1.6))
        ly = yy + hh / 2 - (len(lines) - 1) * 9
        for ln in lines:
            out.append(_t(x0 + ww / 2, ly, ln, size=13.5, fill=fg,
                          weight="600" if kind in ("start", "end", "decision") else "500"))
            ly += 18
        return "".join(out)

    for idx, (yy, hh, kind, st, lines) in enumerate(positions):
        bw = box_w if kind != "decision" else box_w + 20
        x0 = cx - bw / 2
        body.append(draw_box(x0, yy, bw, hh, kind, lines))

        if kind == "decision" and st.get("branch"):
            br = st["branch"]
            btext = br.get("text", "")
            blines = btext.split("\n")
            bh = 30 + 18 * len(blines)
            bw2 = max(130, _textw(max(blines, key=len, default=""), 12) + 20)
            bx = x0 + bw + 66
            by = yy + hh / 2 - bh / 2
            b_bg, b_fg, b_st = _role(br.get("role", "red"))
            body.append(_rect(bx, by, bw2, bh, fill=b_bg, stroke=b_st, rx=8,
                             sw=1.5))
            lly = by + bh / 2 - (len(blines) - 1) * 9
            for ln in blines:
                body.append(_t(bx + bw2 / 2, lly, ln, size=12.5, fill=b_fg,
                               weight="600"))
                lly += 18
            body.append(_line(x0 + bw, yy + hh / 2, bx, yy + hh / 2,
                              stroke=b_st, sw=1.6,
                              mid="arrg" if br.get("role") == "green" else
                                  ("arrb" if br.get("role") == "primary" else "arrr")))
            body.append(_t((x0 + bw + bx) / 2, yy + hh / 2 - 9,
                           br.get("label", "no"), size=11.5, fill=b_st,
                           weight="700"))
            max_right = max(max_right, bx + bw2 + 8)

        if idx < len(positions) - 1:
            ny = positions[idx + 1][0]
            body.append(_line(cx, yy + hh, cx, ny, stroke=INK, sw=1.6))
            if kind == "decision":
                body.append(_t(cx + 12, yy + hh + 12, st.get("yes", "yes"),
                               size=11.5, fill=GREEN, weight="700",
                               anchor="start"))

    return _svg(max(max_right + 12, w), total_h, "".join(body))


# --------------------------------------------------------------------------- DPTABLE
def render_dptable(spec):
    grid = spec.get("grid", [])
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    cell = spec.get("cell", 46)
    col_head = spec.get("col_head")
    row_head = spec.get("row_head")
    corner = spec.get("corner", "")
    highlights = spec.get("highlights", [])
    arrows = spec.get("arrows", [])
    title = spec.get("title", "")
    caption = spec.get("caption", "")

    hl = {(h[0], h[1]): (h[2] if len(h) > 2 else "amber") for h in highlights}

    lpad = 24 + (cell if row_head else 0)
    tpad = 20 + (28 if col_head else 0)
    if title:
        tpad += 22
    width = lpad + cols * cell + 24
    height = tpad + rows * cell + 24
    if caption:
        height += 22
    body = []
    if title:
        body.append(_title(width / 2, 18, title))

    def cellxy(r, c):
        return lpad + c * cell, tpad + r * cell

    if corner and row_head and col_head:
        body.append(_t(lpad - cell / 2, tpad - 14, corner, size=12, fill=FAINT,
                       family=MONO))
    if col_head:
        for c, h in enumerate(col_head):
            body.append(_t(lpad + c * cell + cell / 2, tpad - 14, h, size=12.5,
                           fill=MUTED, weight="700", family=MONO))
    if row_head:
        for r, h in enumerate(row_head):
            body.append(_t(lpad - cell / 2, tpad + r * cell + cell / 2, h,
                           size=12.5, fill=MUTED, weight="700", family=MONO))

    for r in range(rows):
        for c in range(cols):
            x, y = cellxy(r, c)
            role = hl.get((r, c), "")
            bg, fg, st = _role(role)
            body.append(_rect(x, y, cell, cell, fill=bg, stroke=st if role else LINE,
                              rx=4, sw=1.8 if role else 1))
            val = grid[r][c]
            if val is not None and val != "":
                body.append(_t(x + cell / 2, y + cell / 2, val, size=15, fill=fg,
                               weight="700" if role else "500", family=MONO))

    for a in arrows:
        (r1, c1), (r2, c2) = a["from"], a["to"]
        x1, y1 = cellxy(r1, c1)
        x2, y2 = cellxy(r2, c2)
        color = a.get("color", PRIMARY)
        mid = {"": "arrb", PRIMARY: "arrb", GREEN: "arrg", RED: "arrr"}.get(color, "arrb")
        body.append(_line(x1 + cell / 2, y1 + cell / 2, x2 + cell / 2,
                          y2 + cell / 2, stroke=color, sw=2, mid=mid))

    if caption:
        body.append(_t(width / 2, height - 12, caption, size=13, fill=MUTED))
    return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- TREE
def render_tree(spec):
    values = spec.get("values", [])
    highlights = spec.get("highlights", {})
    edges_hl = spec.get("edge_highlights", [])
    title = spec.get("title", "")
    caption = spec.get("caption", "")
    r = spec.get("radius", 20)
    labels = spec.get("labels", {})

    import math
    n = len(values)
    depth = max(1, math.ceil(math.log2(n + 1)))
    hgap = spec.get("hgap", 54)
    vgap = spec.get("vgap", 74)
    leaves = 2 ** (depth - 1)
    width = leaves * hgap + 40
    top = 30 + (22 if title else 0)
    height = top + (depth - 1) * vgap + 2 * r + 40
    if caption:
        height += 20

    def pos(i):
        lvl = int(math.floor(math.log2(i + 1)))
        idx_in = i - (2 ** lvl - 1)
        count = 2 ** lvl
        slot = width / count
        x = slot * (idx_in + 0.5)
        y = top + lvl * vgap + r
        return x, y

    body = []
    if title:
        body.append(_title(width / 2, 18, title))

    ehl = {tuple(e) for e in edges_hl}
    for i in range(n):
        if values[i] is None:
            continue
        for child in (2 * i + 1, 2 * i + 2):
            if child < n and values[child] is not None:
                x1, y1 = pos(i)
                x2, y2 = pos(child)
                hlc = (i, child) in ehl
                body.append(_line(x1, y1, x2, y2,
                                  stroke=PRIMARY if hlc else LINE,
                                  sw=2.4 if hlc else 1.6, marker=False))
    for i in range(n):
        if values[i] is None:
            continue
        x, y = pos(i)
        role = highlights.get(i, highlights.get(str(i), ""))
        bg, fg, st = _role(role if role else "plain")
        if not role:
            bg, fg, st = WHITE, INK, PRIMARY
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{bg}" '
                    f'stroke="{st}" stroke-width="2"/>')
        body.append(_t(x, y, values[i], size=14, fill=fg, weight="700",
                       family=MONO))
        if str(i) in labels or i in labels:
            lab = labels.get(i, labels.get(str(i)))
            body.append(_t(x, y - r - 10, lab, size=11.5, fill=MUTED,
                           weight="600"))
    if caption:
        body.append(_t(width / 2, height - 10, caption, size=13, fill=MUTED))
    return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- RECURSION
def render_recursion(spec):
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    title = spec.get("title", "")
    caption = spec.get("caption", "")
    colw = spec.get("colw", 70)
    rowh = spec.get("rowh", 78)
    nw = spec.get("node_w", 58)
    nh = spec.get("node_h", 34)

    maxx = max((nd["x"] for nd in nodes), default=1)
    maxy = max((nd["y"] for nd in nodes), default=1)
    left = 26
    top = 28 + (22 if title else 0)
    width = left * 2 + maxx * colw + nw
    height = top + maxy * rowh + nh + (24 if caption else 12)

    idpos = {}
    for nd in nodes:
        x = left + nd["x"] * colw
        y = top + nd["y"] * rowh
        idpos[nd["id"]] = (x + nw / 2, y + nh / 2, x, y)

    body = []
    if title:
        body.append(_title(width / 2, 18, title))
    for e in edges:
        cx1, cy1, _, _ = idpos[e["from"]]
        cx2, cy2, x2, y2 = idpos[e["to"]]
        color = e.get("color", LINE)
        dash = "5 4" if e.get("dash") else None
        mid = {GREEN: "arrg", RED: "arrr", PRIMARY: "arrb"}.get(color, "arr")
        body.append(_line(cx1, cy1 + nh / 2 - 2, cx2, y2, stroke=color,
                          sw=1.8, dash=dash, mid=mid))
        if e.get("label"):
            body.append(_t((cx1 + cx2) / 2 + 8, (cy1 + cy2) / 2, e["label"],
                           size=11, fill=color if color != LINE else MUTED,
                           weight="700", anchor="start"))
    for nd in nodes:
        cxx, cyy, x, y = idpos[nd["id"]]
        role = nd.get("role", "")
        bg, fg, st = _role(role if role else "plain")
        if not role:
            bg, fg, st = WHITE, INK, PRIMARY
        body.append(_rect(x, y, nw, nh, fill=bg, stroke=st, rx=8, sw=1.6))
        body.append(_t(cxx, cyy, nd["label"], size=12.5, fill=fg, weight="600",
                       family=MONO))
    if caption:
        body.append(_t(width / 2, height - 10, caption, size=13, fill=MUTED))
    return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- LINKEDLIST
def render_linkedlist(spec):
    values = spec.get("values", [])
    title = spec.get("title", "")
    caption = spec.get("caption", "")
    pointers = spec.get("pointers", [])
    cycle_to = spec.get("cycle_to", None)
    doubly = spec.get("doubly", False)
    node_w, node_h = 58, 40
    gap = 46
    pad = 24
    top = 28 + (22 if title else 0)
    above = 40 if pointers else 0
    n = len(values)
    width = pad * 2 + n * node_w + (n - 1) * gap + 40
    height = top + above + node_h + (60 if cycle_to is not None else 24)

    def nx(i):
        return pad + i * (node_w + gap)

    y = top + above
    body = []
    if title:
        body.append(_title(width / 2, 18, title))
    for i, v in enumerate(values):
        x = nx(i)
        body.append(_rect(x, y, node_w, node_h, fill=WHITE, stroke=PRIMARY,
                          rx=7, sw=1.6))
        body.append(_line(x + node_w * 0.66, y, x + node_w * 0.66, y + node_h,
                          stroke=LINE, sw=1.2, marker=False))
        body.append(_t(x + node_w * 0.33, y + node_h / 2, v, size=14,
                       fill=INK, weight="700", family=MONO))
        if i < n - 1:
            body.append(_line(x + node_w, y + node_h / 2, nx(i + 1),
                              y + node_h / 2, stroke=INK, sw=1.6))
            if doubly:
                body.append(_line(nx(i + 1), y + node_h * 0.78,
                                  x + node_w, y + node_h * 0.78,
                                  stroke=FAINT, sw=1.2))
        else:
            if cycle_to is None:
                body.append(_line(x + node_w, y + node_h / 2, x + node_w + 26,
                                  y + node_h / 2, stroke=INK, sw=1.6))
                body.append(_t(x + node_w + 34, y + node_h / 2, "\u2205",
                               size=15, fill=MUTED, anchor="start"))
    if cycle_to is not None and n:
        xs = nx(n - 1) + node_w / 2
        xt = nx(cycle_to) + node_w / 2
        yb = y + node_h
        body.append(f'<path d="M{xs:.1f} {yb:.1f} C {xs:.1f} {yb+40:.1f} '
                    f'{xt:.1f} {yb+40:.1f} {xt:.1f} {yb+3:.1f}" fill="none" '
                    f'stroke="{RED}" stroke-width="1.8" marker-end="url(#arrr)"/>')
        body.append(_t((xs + xt) / 2, yb + 46, "cycle", size=11.5, fill=RED,
                       weight="700"))
    for p in pointers:
        i = p["index"]
        if i is None or i >= n:
            continue
        color = p.get("color", PRIMARY)
        x = nx(i) + node_w * 0.33
        body.append(_t(x, top + 8, p.get("name", ""), size=13, fill=color,
                       weight="700", family=MONO))
        body.append(_line(x, top + 18, x, y - 3, stroke=color, sw=2))
    if caption:
        body.append(_t(width / 2, height - 10, caption, size=13, fill=MUTED))
    return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- STACK
def render_stack(spec):
    items = spec.get("items", [])
    title = spec.get("title", "")
    caption = spec.get("caption", "")
    highlights = spec.get("highlights", {})
    note_top = spec.get("top_label", "top")
    orient = spec.get("orient", "vertical")
    cw, ch = spec.get("cell_w", 90), spec.get("cell_h", 34)
    pad = 24
    top = 30 + (22 if title else 0)
    n = len(items)
    if orient == "vertical":
        width = pad * 2 + cw + 70
        height = top + max(n, 1) * ch + 40
        x = pad + 30
        body = []
        if title:
            body.append(_title(width / 2, 18, title))
        for k, v in enumerate(items):
            y = top + (n - 1 - k) * ch
            role = highlights.get(k, highlights.get(str(k), ""))
            bg, fg, st = _role(role if role else "panel")
            body.append(_rect(x, y, cw, ch, fill=bg, stroke=st, rx=5, sw=1.5))
            body.append(_t(x + cw / 2, y + ch / 2, v, size=14, fill=fg,
                           weight="700", family=MONO))
            if k == n - 1:
                body.append(_t(x + cw + 12, y + ch / 2, "\u2190 " + note_top,
                               size=12, fill=PRIMARY, weight="700",
                               anchor="start"))
        body.append(_line(x - 4, top + n * ch, x + cw + 4, top + n * ch,
                          stroke=INK, sw=2.4, marker=False))
        if caption:
            body.append(_t(width / 2, height - 10, caption, size=13, fill=MUTED))
        return _svg(width, height, "".join(body))
    else:
        width = pad * 2 + n * cw + 40
        height = top + ch + 40
        body = []
        if title:
            body.append(_title(width / 2, 18, title))
        for k, v in enumerate(items):
            x = pad + k * cw
            role = highlights.get(k, highlights.get(str(k), ""))
            bg, fg, st = _role(role if role else "panel")
            body.append(_rect(x, top, cw, ch, fill=bg, stroke=st, rx=5, sw=1.5))
            body.append(_t(x + cw / 2, top + ch / 2, v, size=14, fill=fg,
                           weight="700", family=MONO))
        body.append(_t(pad, top + ch + 18, "front", size=11.5, fill=MUTED,
                       anchor="start", weight="700"))
        body.append(_t(pad + n * cw, top + ch + 18, "rear", size=11.5,
                       fill=MUTED, anchor="end", weight="700"))
        if caption:
            body.append(_t(width / 2, height - 8, caption, size=13, fill=MUTED))
        return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- INTERVALS
def render_intervals(spec):
    items = spec.get("intervals", [])
    title = spec.get("title", "")
    caption = spec.get("caption", "")
    lo = spec.get("min", min((i["start"] for i in items), default=0))
    hi = spec.get("max", max((i["end"] for i in items), default=10))
    unit = spec.get("unit", 34)
    pad = 40
    top = 30 + (22 if title else 0)
    rowh = 30
    span = hi - lo
    width = pad * 2 + span * unit
    height = top + len(items) * rowh + 44
    if caption:
        height += 18

    def X(v):
        return pad + (v - lo) * unit

    body = []
    if title:
        body.append(_title(width / 2, 18, title))
    axis_y = top + len(items) * rowh + 12
    body.append(_line(pad, axis_y, width - pad + 10, axis_y, stroke=FAINT,
                      sw=1.2, marker=False))
    for v in range(lo, hi + 1):
        body.append(_line(X(v), axis_y - 3, X(v), axis_y + 3, stroke=FAINT,
                          sw=1, marker=False))
        body.append(_t(X(v), axis_y + 14, v, size=11, fill=FAINT, family=MONO))
    for r, it in enumerate(items):
        y = top + r * rowh
        role = it.get("role", "primary")
        bg, fg, st = _role(role)
        x1, x2 = X(it["start"]), X(it["end"])
        body.append(_rect(x1, y, x2 - x1, rowh - 10, fill=bg, stroke=st, rx=6,
                          sw=1.5))
        body.append(_t((x1 + x2) / 2, y + (rowh - 10) / 2,
                       it.get("label", f'[{it["start"]},{it["end"]}]'),
                       size=12, fill=fg, weight="700"))
    if caption:
        body.append(_t(width / 2, height - 8, caption, size=13, fill=MUTED))
    return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- SEARCHSPACE
def render_searchspace(spec):
    values = spec.get("values", [])
    lo = spec.get("lo")
    mid = spec.get("mid")
    hi = spec.get("hi")
    eliminated = set(spec.get("eliminated", []))
    target = spec.get("target")
    title = spec.get("title", "")
    caption = spec.get("caption", "")
    cell = 44
    gap = 5
    pad = 24
    n = len(values)
    top = 56 + (22 if title else 0)
    width = pad * 2 + n * cell + (n - 1) * gap
    height = top + cell + 66
    body = []
    if title:
        body.append(_title(width / 2, 18, title))

    def cx(i):
        return pad + i * (cell + gap) + cell / 2

    for i, v in enumerate(values):
        x = pad + i * (cell + gap)
        if i in eliminated:
            bg, fg, st = PANEL, FAINT, LINE
        elif i == mid:
            bg, fg, st = _role("amber")
        else:
            bg, fg, st = WHITE, INK, PRIMARY
        body.append(_rect(x, top, cell, cell, fill=bg, stroke=st, rx=6,
                          sw=1.8 if i == mid else 1.4))
        body.append(_t(x + cell / 2, top + cell / 2, v, size=15, fill=fg,
                       weight="700", family=MONO))
        body.append(_t(x + cell / 2, top + cell + 13, i, size=11, fill=FAINT,
                       family=MONO))
    for name, i, col in (("lo", lo, PRIMARY), ("mid", mid, AMBER),
                         ("hi", hi, PURPLE)):
        if i is None or i < 0 or i >= n:
            continue
        x = cx(i)
        body.append(_t(x, top - 30, name, size=12.5, fill=col, weight="700",
                       family=MONO))
        body.append(_line(x, top - 20, x, top - 3, stroke=col, sw=2))
    if target is not None:
        body.append(_t(width / 2, height - 12,
                       f"target = {target}", size=13, fill=MUTED, weight="600"))
    elif caption:
        body.append(_t(width / 2, height - 12, caption, size=13, fill=MUTED))
    return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- GRAPH
def render_graph(spec):
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    title = spec.get("title", "")
    caption = spec.get("caption", "")
    directed = spec.get("directed", False)
    r = spec.get("radius", 20)
    scale = spec.get("scale", 66)
    pad = 40
    maxx = max((nd["x"] for nd in nodes), default=4)
    maxy = max((nd["y"] for nd in nodes), default=3)
    top = 26 + (22 if title else 0)
    width = pad * 2 + maxx * scale
    height = top + maxy * scale + pad + (16 if caption else 0)
    P = {}
    for nd in nodes:
        P[nd["id"]] = (pad + nd["x"] * scale, top + nd["y"] * scale)
    body = []
    if title:
        body.append(_title(width / 2, 18, title))
    import math
    for e in edges:
        x1, y1 = P[e["from"]]
        x2, y2 = P[e["to"]]
        color = e.get("color", FAINT)
        dash = "6 4" if e.get("dash") else None
        dir_ = e.get("directed", directed)
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d
        sx, sy = x1 + ux * r, y1 + uy * r
        ex, ey = x2 - ux * r, y2 - uy * r
        mid = {GREEN: "arrg", RED: "arrr", PRIMARY: "arrb"}.get(color, "arr")
        body.append(_line(sx, sy, ex, ey, stroke=color,
                          sw=e.get("sw", 1.8), marker=dir_, dash=dash, mid=mid))
        if "w" in e:
            mxp, myp = (x1 + x2) / 2, (y1 + y2) / 2
            body.append(f'<rect x="{mxp-11:.1f}" y="{myp-10:.1f}" width="22" '
                        f'height="18" rx="4" fill="{WHITE}" stroke="{LINE}" '
                        f'stroke-width="1"/>')
            body.append(_t(mxp, myp, e["w"], size=11.5, fill=PRIMARY_D,
                           weight="700", family=MONO))
    for nd in nodes:
        x, y = P[nd["id"]]
        role = nd.get("role", "")
        bg, fg, st = _role(role if role else "plain")
        if not role:
            bg, fg, st = WHITE, INK, PRIMARY
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{bg}" '
                    f'stroke="{st}" stroke-width="2.2"/>')
        body.append(_t(x, y, nd.get("label", nd["id"]), size=13, fill=fg,
                       weight="700", family=MONO))
    if caption:
        body.append(_t(width / 2, height - 8, caption, size=13, fill=MUTED))
    return _svg(width, height, "".join(body))


# --------------------------------------------------------------------------- BARS
def render_bars(spec):
    values = spec.get("values", [])
    title = spec.get("title", "")
    caption = spec.get("caption", "")
    highlights = spec.get("highlights", {})
    bw = spec.get("bar_w", 40)
    gap = spec.get("gap", 6)
    unit = spec.get("unit", 20)
    pad = 30
    n = len(values)
    top = 24 + (22 if title else 0)
    maxv = max(values) if values else 1
    plot_h = maxv * unit
    width = pad * 2 + n * bw + (n - 1) * gap
    height = top + plot_h + 46
    base = top + plot_h
    body = []
    if title:
        body.append(_title(width / 2, 18, title))
    body.append(_line(pad - 6, base, width - pad + 6, base, stroke=FAINT,
                      sw=1.2, marker=False))
    for i, v in enumerate(values):
        x = pad + i * (bw + gap)
        h = v * unit
        role = highlights.get(i, highlights.get(str(i), ""))
        bg, fg, st = _role(role if role else "accent")
        body.append(_rect(x, base - h, bw, h, fill=bg, stroke=st, rx=4, sw=1.4))
        body.append(_t(x + bw / 2, base - h - 10, v, size=12, fill=INK,
                       weight="700", family=MONO))
        body.append(_t(x + bw / 2, base + 14, i, size=11, fill=FAINT,
                       family=MONO))
    if caption:
        body.append(_t(width / 2, height - 8, caption, size=13, fill=MUTED))
    return _svg(width, height, "".join(body))


_RENDERERS = {
    "array": render_array,
    "pointers": render_array,
    "flow": render_flow,
    "dptable": render_dptable,
    "grid": render_dptable,
    "tree": render_tree,
    "recursion": render_recursion,
    "linkedlist": render_linkedlist,
    "stack": render_stack,
    "queue": render_stack,
    "intervals": render_intervals,
    "searchspace": render_searchspace,
    "graph": render_graph,
    "bars": render_bars,
}


def render(spec):
    t = spec.get("type", "")
    fn = _RENDERERS.get(t)
    if not fn:
        return (f'<svg class="dfig" xmlns="http://www.w3.org/2000/svg" '
                f'viewBox="0 0 400 40" width="400" height="40">'
                f'<text x="8" y="24" fill="{RED}" font-size="13">'
                f'[diagram: unknown type "{escape(str(t))}"]</text></svg>')
    try:
        svg = fn(spec)
        return _expand_for_text(svg, spec)
    except Exception as e:
        return (f'<svg class="dfig" xmlns="http://www.w3.org/2000/svg" '
                f'viewBox="0 0 500 40" width="500" height="40">'
                f'<text x="8" y="24" fill="{RED}" font-size="12">'
                f'[diagram error in "{escape(str(t))}": {escape(str(e))}]'
                f'</text></svg>')


def _expand_for_text(svg, spec):
    need = max(_textw(spec.get("caption", ""), 13),
               _textw(spec.get("title", ""), 13))
    m = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', svg)
    if not m:
        return svg
    W, Hs = float(m.group(1)), m.group(2)
    if need <= W:
        return svg
    dx = (need - W) / 2
    gt = svg.index('>') + 1
    head, inner = svg[:gt], svg[gt:-len('</svg>')]
    head = head.replace(f'viewBox="0 0 {m.group(1)} {m.group(2)}"',
                        f'viewBox="0 0 {need:.1f} {Hs}"')
    head = re.sub(r'width="[0-9.]+"', f'width="{need:.1f}"', head, count=1)
    return f'{head}<g transform="translate({dx:.1f},0)">{inner}</g></svg>'
