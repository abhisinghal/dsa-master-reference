"""Render selected PDF pages to PNG for visual QC."""
import sys
import fitz

pdf = sys.argv[1]
pages = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
out_prefix = sys.argv[3] if len(sys.argv) > 3 else "page"
doc = fitz.open(pdf)
print(f"{pdf}: {doc.page_count} pages")
idxs = pages if pages else range(doc.page_count)
for i in idxs:
    if i < 0 or i >= doc.page_count:
        continue
    p = doc[i]
    pix = p.get_pixmap(dpi=110)
    fn = f"build/{out_prefix}_{i+1:03d}.png"
    pix.save(fn)
    print("wrote", fn)
