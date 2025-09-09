import re
import pandas as pd
from PyPDF2 import PdfReader

# Load your local PDF
pdf_path = r"C:\Users\Bikranta\Documents\8th_Semester\Major_Project\General Standard for Food Additives.pdf"
reader = PdfReader(pdf_path)

# Extract text from all pages
codex_text = ""
for page in reader.pages:
    codex_text += page.extract_text()

# Extract likely INS code + additive name pairs
raw_matches = re.findall(r"(INS\s*\d+|\b\d{3,4})\s*[–-]?\s*([A-Z][A-Za-z\s,()\-]+)", codex_text)

# Filter valid matches using keywords
keywords = ['acid', 'oxide', 'gum', 'starch', 'sorbate', 'color', 'nitrate',
            'sweetener', 'preservative', 'glutamate', 'cellulose', 'lecithin', 'enzyme']
seen = set()
codex_cleaned = []

for code, name in raw_matches:
    code_clean = code.replace("INS", "").strip()
    name_clean = name.strip()
    if len(name_clean) > 4 and any(k in name_clean.lower() for k in keywords):
        if (code_clean, name_clean) not in seen:
            seen.add((code_clean, name_clean))
            codex_cleaned.append({
                'aliases': f'INS {code_clean}',
                'ingredient': name_clean,
                'category': 'Unknown',
                'health concern': 'Not evaluated',
                'health score': 50
            })

df = pd.DataFrame(codex_cleaned)
df.to_csv('codex_additives.csv', index=False)
print("Saved: codex_additives.csv")
