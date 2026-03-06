import json
import re

# Formats:
# 12/03/2002 , 12-03-2002 , 2002-03-12 , 2002/03/12

DATE_RE = re.compile(r"\b(?:\d{2}[\/\-]\d{2}[\/\-]\d{4}|\d{4}[\/\-]\d{2}[\/\-]\d{2})\b")
BIRTH_KW = re.compile(r"\b(geboren|born|birth|né|née|date de naissance|geb\.)\b", re.IGNORECASE)

with open("labeled_layout.json", "r", encoding="utf-8") as f:
    data = json.load(f)

date_count = 0

for page in data:
    for item in page["items"]:
        if item.get("label") != "other":
            continue #ya3ni lehou mail lehou num

        text = (item.get("text", "") or "").strip() #cleaning Lel text
        if not text:
            continue

        if DATE_RE.search(text) and BIRTH_KW.search(text):
            item["label"] = "birth_date"
            date_count += 1

with open("labeled_layout.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False) #yktb bl mn4m fi data ou y9bl lou8aat

print("Birth date detection done")
print("Date items:", date_count)
