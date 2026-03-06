import json
from step1 import run_step_1

# 1. Loading the Data: Na9raw el JSON file mta3 el CV
# El file hadha fih akther men 2000 ligne mta3 information
with open("cv_preprocessing.json", "r") as f:
    data = json.load(f)

# 2. Data Extraction: Nkharjou el blocks mta3 el ktaba wel coordinates
my_blocks = []
for page in data['documentContentJson']['pages']:
    for item in page['items']:
        my_blocks.append({
            "text": item['text'],
            "coords": [item['x'], item['y'], item['width'], item['height']]
        })

# 3. PII Detection: Nkhaddmu el "Scanner" mta3na (Step 1) 
# Hna el code bech ytalla3 el assemi, el emails, wel nationalities
results = run_step_1(my_blocks)

# 4. Display Results: Nwarru el natija le5ra fil Terminal
print("\n--- [ PII DETECTION RESULTS ] ---")
for r in results:
    print(f"Type: {r['type']} | Value: {r['val']}")