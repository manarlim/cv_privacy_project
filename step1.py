# --- 1. Import the tools (libraries) ---
import re        # The “Hook”: searches for patterns (like @ or numbers).
import spacy     # The “Brain”: reads the text and identifies names of people and places.
import pycountry
# --- 2. Load and activate the model (NLP) ---
# nlp is the engine. “en_core_web_sm” is an English model that helps it understand the context.
nlp = spacy.load("en_core_web_sm") 

# --- 3. The main function ---
def run_step_1(green_blocks):
    # An empty notebook to store the results (extracted PII).
    extracted_pii = []
    # --- Countries and Languages (Dynamic Lists) ---
    all_countries = [c.name for c in pycountry.countries]
    country_pattern = r'\b(' + '|'.join(all_countries) + r')\b'
    # Here we added all languages (more than 7,000 languages).
    all_languages = [l.name for l in pycountry.languages]
    lang_pattern = r'\b(' + '|'.join(all_languages) + r')\b'
    # --- 4. The “Hooks” (Regex Dictionary) ---
    patterns = {
        "Email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', # pattern of @
        "Phone": r'\+?(\d{1,3})?[-.\s]?\d{2,4}[-.\s]?\d{3,4}',        # pattern of numbers
        "Profile_URL": r'(https?://)?(www\.)?(github|linkedin|facebook|twitter)\.com/[\w-]+', # Links
        "Birth_Date": r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',       # pattern of Date
        "Gender": r'\b(Male|Female|Man|Woman|Homme|Femme)\b',       # Keywords of gender
        "Country": country_pattern, 
        "Nationality_Header": r'\b(Nationality|Citizenship|Nationalité)\b',
        "Language": lang_pattern,     
        "Lang_Header": r'\b(Languages|Langues|Mother tongue|Native language)\b', 
        "Driving_License": r'\b(Driving [Ll]icense|[Pp]ermis de conduire|Type B|Category B)\b',   
    }
    # --- 5. Loop through the blocks ---
    for block in green_blocks:

        text = block['text']
        coords = block['coords'] 

        # --- 6. Check Regex (Success Patterns) ---
        
        for pii_type, pattern in patterns.items():
            
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                
                extracted_pii.append({
                    "val": match if isinstance(match, str) else match[0],
                    "type": pii_type,
                    "coords": coords,
                    "status": "Success"
                })

        # --- 7. Check NER (SpaCy Brain) ---
        # Here we let the nlp model read the entire block.
        doc = nlp(text)
        
        # We look for entities in "doc" (the understood text).
        for ent in doc.ents:
            
            # A. Full Name: Itha l9a PERSON (, Manar...)
            if ent.label_ == "PERSON":
                extracted_pii.append({
                    "val": ent.text, 
                    "type": "Full_Name", 
                    "coords": coords, 
                    "status": "Soft Failure" # "Soft" because we need to verify in Step 2
                })
            
            # B. Birth Location / Residence: If it finds  GPE (Cities) or LOC (Regions)
            if ent.label_ in ["GPE", "LOC"]:
                extracted_pii.append({
                    "val": ent.text, 
                    "type": "Location", 
                    "coords": coords, 
                    "status": "Soft Failure"
                })

    # --- 8. return the result ---
    return extracted_pii