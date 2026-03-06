import fitz
import json

pdf_path = "cv.pdf"
out_path = "layout.json"

doc = fitz.open(pdf_path)
pages_output = []

for page_index in range(len(doc)):
    page = doc[page_index]
    d = page.get_text("dict")  # blocks -> lines -> spans Bech yati structure

    items = []
    for block in d.get("blocks", []):
        if block.get("type") != 0:  # 0 = text blocks only
            continue

        for line in block.get("lines", []): #nmchou b star b star 
            for span in line.get("spans", []):
                text = (span.get("text") or "").strip() #n5rj text ou nsup l espace
                if not text:
                    continue

                x0, y0, x1, y1 = span["bbox"]  #cordonner mt3 span
                item = {
                    "position": {"x": float(x0), "y": float(y0)},
                    "size": {"width": float(x1 - x0), "height": float(y1 - y0)},
                    "color": span.get("color", None),
                    "fontname": span.get("font", None),
                    "fontsize": float(span.get("size", 0)),
                    "thickness": None,
                    "text": text
                }
                items.append(item) #yzid item jdid

    pages_output.append({"page": page_index + 1, "items": items})

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(pages_output, f, ensure_ascii=False, indent=2)

print(f" Saved {out_path} with {len(pages_output)} pages")
