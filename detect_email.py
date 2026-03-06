import json
import re

EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b")

with open("layout.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for page in data:
    for item in page["items"]:
        text = item.get("text", "")

        if EMAIL_RE.search(text):
            item["label"] = "email_address"
        else:
            item["label"] = "other"

with open("labeled_layout.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Email detection done")
