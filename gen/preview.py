import sys, fitz, os
pdf = r"C:\Users\absinghal\Downloads\Int\DSA_MASTER_REFERENCE6.pdf"
doc = fitz.open(pdf)
print("PAGES:", doc.page_count)
outdir = os.path.join(os.path.dirname(__file__), "preview")
os.makedirs(outdir, exist_ok=True)
pages = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(min(6, doc.page_count)))
for p in pages:
    if p < 0 or p >= doc.page_count: continue
    pg = doc[p]
    pix = pg.get_pixmap(dpi=110)
    fn = os.path.join(outdir, f"p{p:03d}.png")
    pix.save(fn)
    print("saved", fn)
