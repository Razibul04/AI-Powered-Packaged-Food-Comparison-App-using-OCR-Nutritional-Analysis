import pytesseract
from PIL import Image
import pandas as pd
import re
from rapidfuzz import process, fuzz

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Path to your local ingredient database
CSV_PATH = r"C:\1_PROFESSIONAL\RIST\8th Sem\MAJOR_PROJECT_DETAILS\8_Model\food-comparator\backend\utils\Final_Indian_Ingredient_HealthDataset_Scored - Copy.csv"

def load_known_ingredients_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        ingredients = df['ingredient'].dropna().str.lower().str.strip().tolist()
        return ingredients
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error reading image: {e}")
        return ""

def extract_ingredients_block(text):
    lines = text.lower().splitlines()

    # Step 1: Fuzzy search for the line that contains "ingredients"
    start_idx = -1
    for i, line in enumerate(lines):
        if fuzz.partial_ratio("ingredients", line) > 75:
            start_idx = i
            break

    if start_idx == -1:
        print("Could not find ingredients keyword.")
        return None

    # Step 2: Collect lines until a stopping keyword
    block = []
    stop_keywords = ["allergen", "may contain", "contains", "manufactured", "for mfg", "scan the barcode"]
    for line in lines[start_idx:]:
        if any(kw in line for kw in stop_keywords):
            break
        block.append(line)

    # Step 3: Clean up the result
    full_block = ' '.join(block)
    full_block = full_block.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('{', '').replace('}', '')
    return full_block.strip()

def clean_ingredient_list(raw_ingredients):
    if not raw_ingredients:
        return []
    ingredients = [i.strip() for i in raw_ingredients.split(',') if i.strip()]
    return ingredients

def correct_ingredient_name(name, known_ingredients):
    match, score, _ = process.extractOne(name, known_ingredients)
    return match if score > 80 else name

def get_cleaned_ingredient_list(image_path):
    print(f"Processing image: {image_path}")
    
    known_ingredients = load_known_ingredients_from_csv(CSV_PATH)
    if not known_ingredients:
        print("No known ingredients loaded. Check CSV file.")
        return []

    raw_text = extract_text_from_image(image_path)
    print("\n--- OCR Text Start ---\n", raw_text, "\n--- OCR Text End ---\n")

    raw_ingredients_block = extract_ingredients_block(raw_text)

    if not raw_ingredients_block:
        return []

    raw_ingredients = clean_ingredient_list(raw_ingredients_block)
    corrected_ingredients = [
        correct_ingredient_name(ing, known_ingredients)
        for ing in raw_ingredients
    ]
    return corrected_ingredients

# ✅ Wrapper to be imported and used by scoring.py
def extract_ingredient_list_from_image(image_path):
    return get_cleaned_ingredient_list(image_path)

# For direct testing
if __name__ == "__main__":
    test_image_path = r"C:\1_PROFESSIONAL\RIST\8th Sem\MAJOR_PROJECT_DETAILS\8_Model\food-comparator\test_images\test_sample1.jpg"
    ingredients = get_cleaned_ingredient_list(test_image_path)
    
    print("\nFinal Extracted Ingredients:")
    for i, ing in enumerate(ingredients, 1):
        print(f"{i}. {ing}")
