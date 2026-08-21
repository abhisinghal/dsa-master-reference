#!/usr/bin/env python3
"""Build the DSA Master Reference book (Markdown -> paged HTML)."""
import json
import re
import sys
from pathlib import Path

import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, JavaLexer, TextLexer
from pygments.formatters import HtmlFormatter

sys.path.insert(0, str(Path(__file__).parent))
import diagrams  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
CONTENT = SRC / "content"
BUILD = ROOT / "build"
ASSETS = ROOT / "assets"

FENCE_RE = re.compile(r"^```([^\n`]*)\n(.*?)^```[ \t]*$", re.S | re.M)
UNI_RE = re.compile(r"\\U([0-9a-fA-F]{8})|\\u([0-9a-fA-F]{4})")


def _decode_unicode(text):
    def r(m):
        h = m.group(1) or m.group(2)
        try:
            return chr(int(h, 16))
        except ValueError:
            return m.group(0)
    return UNI_RE.sub(r, text)


LANG_LABEL = {
    "java": "Java", "python": "Python", "py": "Python", "text": "",
    "pseudo": "Pseudocode", "pseudocode": "Pseudocode", "bash": "Shell",
    "json": "JSON", "": "",
}


def highlight_code(code, lang):
    lang = (lang or "").strip().lower()
    label = LANG_LABEL.get(lang, lang.capitalize() if lang else "")
    if lang in ("", "text", "pseudo", "pseudocode"):
        lexer = TextLexer()
    else:
        try:
            lexer = get_lexer_by_name(lang, stripnl=False)
        except Exception:
            lexer = JavaLexer(stripnl=False)
    fmt = HtmlFormatter(nowrap=True)
    inner = highlight(code, lexer, fmt)
    lbl = (f'<span class="code-lang">{label}</span>') if label else ""
    return (f'<div class="codeblock">{lbl}'
            f'<pre class="hl"><code>{inner}</code></pre></div>')


def preprocess(md_text, tokens):
    def repl(m):
        lang = m.group(1).strip()
        body = m.group(2)
        if lang == "diagram":
            try:
                spec = json.loads(body)
                svg = diagrams.render(spec)
            except Exception as e:
                svg = (f'<pre style="color:#b91c1c">diagram JSON error: '
                       f'{e}</pre>')
            html = f'<div class="fig-wrap">{svg}</div>'
        else:
            html = highlight_code(body, lang)
        key = f"@@BLK{len(tokens)}@@"
        tokens[key] = html
        return "\n\n" + key + "\n\n"

    out = FENCE_RE.sub(repl, md_text)
    out = _decode_unicode(out)
    try:
        out = out.encode("utf-16", "surrogatepass").decode("utf-16")
    except UnicodeError:
        pass
    return out


MD_EXT = [
    "extra", "admonition", "sane_lists", "attr_list", "def_list",
    "tables", "md_in_html", "toc",
]


def _safe_slugify(value, sep):
    from markdown.extensions.toc import slugify as _slug
    s = _slug(value, sep)
    if not s or not s[0].isalpha():
        s = "h-" + s
    return s


def make_md():
    return markdown.Markdown(
        extensions=MD_EXT,
        extension_configs={
            "toc": {"toc_depth": "2-3", "permalink": False,
                    "slugify": _safe_slugify},
        },
        output_format="html5",
    )


HEADING_RE = re.compile(r'<(h[23])[^>]*id="([^"]+)"[^>]*>(.*?)</\1>', re.S)
HEAD_ID_RE = re.compile(r'(<h[1-6]\b[^>]*?\bid=")([^"]+)(")')


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).strip()


def prefix_heading_ids(html, chap_id):
    return HEAD_ID_RE.sub(lambda m: f'{m.group(1)}{chap_id}--{m.group(2)}{m.group(3)}',
                          html)


def convert_file(path, md, tokens, chap_id):
    raw = path.read_text(encoding="utf-8")
    raw = preprocess(raw, tokens)
    md.reset()
    html = md.convert(raw)
    html = prefix_heading_ids(html, chap_id)
    heads = []
    for m in HEADING_RE.finditer(html):
        heads.append((m.group(1), m.group(2), strip_tags(m.group(3))))
    return html, heads


def restore_tokens(html, tokens):
    for key, val in tokens.items():
        html = html.replace(f"<p>{key}</p>", val)
        html = html.replace(key, val)
    return html


def cover_html(meta):
    b = "".join(f'<span class="badge">{x}</span>' for x in meta["cover"]["badges"])
    return f'''<section class="cover">
  <div class="grid-lines"></div>
  <div class="inner">
    <div class="eyebrow">{meta["cover"]["eyebrow"]}</div>
    <h1>{meta["cover"]["title"]}<span class="thin">{meta["cover"]["subtitle"]}</span></h1>
    <div class="tagline">{meta["cover"]["tagline"]}</div>
    <div class="spacer"></div>
    <div class="badges">{b}</div>
    <div class="author"><b>{meta["cover"]["author"]}</b><br>{meta["cover"]["footer"]}</div>
  </div>
</section>'''


def part_html(item):
    return f'''<section class="part-opener" id="{item["id"]}">
  <div class="pnum">{item["label"]}</div>
  <h1>{item["title"]}</h1>
  <div class="subtitle">{item.get("subtitle","")}</div>
</section>'''


def chapter_wrap(item, body, heads):
    if item.get("opener", True):
        links = "".join(
            f'<li>{t}</li>' for tag, hid, t in heads
            if tag == "h2" and t.strip().lower() != item["title"].strip().lower())
        mini = f'<ul class="toc-mini">{links}</ul>' if links else ""
        opener = f'''<div class="chapter-opener" id="{item["id"]}">
  <div class="kicker">{item.get("kicker","")}</div>
  <h1>{item["title"]}</h1>
  <div class="rule"></div>
  <div class="subtitle">{item.get("subtitle","")}</div>
  {mini}
</div>'''
        return f'<section class="chapter">{opener}<div class="chapter-body">{body}</div></section>'
    else:
        return f'<section class="chapter" id="{item["id"]}"><div class="chapter-body">{body}</div></section>'


def build_toc(toc_entries):
    lis = []
    for e in toc_entries:
        cls = e["cls"]
        if cls == "l-part":
            lis.append(f'<li class="l-part">{e["title"]}</li>')
        else:
            lis.append(
                f'<li class="{cls}"><a href="#{e["id"]}">'
                f'<span class="t">{e["title"]}</span>'
                f'<span class="lead"></span></a></li>')
    return ('<section class="toc" id="toc"><h1>Table of Contents</h1>'
            '<ul>' + "".join(lis) + '</ul></section>')


def main():
    meta = json.loads((SRC / "manifest.json").read_text(encoding="utf-8"))
    md = make_md()
    tokens = {}
    toc_entries = []
    cover = cover_html(meta)

    chapter_htmls = []
    for item in meta["items"]:
        if item["type"] == "part":
            toc_entries.append({"cls": "l-part", "title": item["title"]})
            chapter_htmls.append(("part", part_html(item), item))
        elif item["type"] == "chapter":
            path = CONTENT / item["file"]
            if not path.exists():
                print(f"  [skip missing] {item['file']}")
                continue
            body, heads = convert_file(path, md, tokens, item["id"])
            toc_entries.append({"cls": "l-h2", "title": item["title"],
                                "id": item["id"]})
            for tag, hid, txt in heads:
                if tag == "h2" and item.get("toc_h2", True):
                    if txt.strip().lower() == item["title"].strip().lower():
                        continue
                    toc_entries.append({"cls": "l-h3", "title": txt, "id": hid})
            chapter_htmls.append(("chapter", chapter_wrap(item, body, heads), item))

    toc_html = build_toc(toc_entries)
    parts_html = "".join(h for _, h, _ in chapter_htmls)
    full_body = cover + toc_html + parts_html
    full_body = restore_tokens(full_body, tokens)

    pyg_css = HtmlFormatter().get_style_defs(".hl")
    css = (ASSETS / "book.css").read_text(encoding="utf-8")
    code_css = (ASSETS / "code.css").read_text(encoding="utf-8") \
        if (ASSETS / "code.css").exists() else ""

    doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{meta["title"]}</title>
<style>{css}</style>
<style>{code_css}</style>
<style>{pyg_css}</style>
</head><body>
{full_body}
</body></html>'''

    BUILD.mkdir(exist_ok=True)
    out = BUILD / "book.html"
    out.write_text(doc, encoding="utf-8")
    print(f"  chapters: {sum(1 for t,_,_ in chapter_htmls if t=='chapter')}")
    print(f"  diagrams+code blocks: {len(tokens)}")
    print(f"  wrote {out}  ({out.stat().st_size//1024} KB)")


if __name__ == "__main__":
    main()
