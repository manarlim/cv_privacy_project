import json
import re

PHONE_RE = re.compile(r"""
\b(
  (?:\+?\d{1,3}[\s\-\.]?)?      
  (?:\(?\d{2,4}\)?[\s\-\.]?)?   
  \d{3,4}[\s\-\.]?\d{3,4}       
  (?:[\s\-\.]?\d{1,4})?         
)\b
""", re.VERBOSE)

with open("labeled_layout.json", "r", encoding="utf-8") as f:
    data = json.load(f)

phone_count = 0

for page in data:
    for item in page["items"]:
        #mnmsch l mail
        if item.get("label") != "other":
            continue

        text = (item.get("text", "") or "").strip()
        if not text:
            continue

        m = PHONE_RE.search(text)
        if not m:
            continue

        digits = re.sub(r"\D", "", text)
        if 8 <= len(digits) <= 15:
            item["label"] = "phone_number"
            phone_count += 1

with open("labeled_layout.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Phone detection done")
print("Phone items:", phone_count)
