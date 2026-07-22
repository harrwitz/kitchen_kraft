import csv
import json
import re
import ast
import os
from collections import Counter

RAW_CSV_PATH = os.path.join(os.path.dirname(__file__), "Food Ingredients and Recipe Dataset with Image Name Mapping.csv")
OUTPUT_JSON_PATH = os.path.join(os.path.dirname(__file__), "unique_ingredients.json")

MEASURE_WORDS = {
    "tsp", "tsp.", "teaspoon", "teaspoons", "tbsp", "tbsp.", "tablespoon", "tablespoons",
    "cup", "cups", "oz", "oz.", "ounce", "ounces", "lb", "lb.", "lbs", "pound", "pounds",
    "g", "kg", "ml", "l", "pinch", "pinches", "dash", "dashes", "clove", "cloves",
    "can", "cans", "package", "packages", "slice", "slices", "bunch", "bunches",
    "head", "heads", "stalk", "stalks", "sprig", "sprigs", "piece", "pieces", "container",
    "divided", "plus", "more", "optional", "to", "taste", "about", "freshly", "ground",
    "diced", "chopped", "sliced", "minced", "grated", "peeled", "trimmed", "crushed",
    "large", "medium", "small", "extra-virgin", "virgin", "kosher", "fine", "pure",
    "raw", "whole", "softened", "melted", "room", "temperature", "warm", "cold"
}

def clean_ingredient_string(raw_ing: str) -> str:
    """Normalize and extract canonical ingredient name from a raw string."""
    text = raw_ing.lower()
    # Remove contents inside parentheses e.g. (3-4 lb.)
    text = re.sub(r'\(.*?\)', '', text)
    # Remove numbers and fractions e.g. 1/2, 2.5, 3-4, ⅓
    text = re.sub(r'[\d½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞\/.\-+]+', ' ', text)
    # Remove punctuation except letters and spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Split into words and remove measurement modifiers
    words = text.split()
    clean_words = [w for w in words if w not in MEASURE_WORDS and len(w) > 1]
    
    result = " ".join(clean_words).strip()
    return result

def extract_unique_ingredients():
    print(f"Reading dataset from {RAW_CSV_PATH}...")
    if not os.path.exists(RAW_CSV_PATH):
        print(f"Error: {RAW_CSV_PATH} not found.")
        return []

    ingredient_counts = Counter()
    raw_ingredient_examples = {}

    with open(RAW_CSV_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_ing_field = row.get('Cleaned_Ingredients') or row.get('Ingredients') or ""
            if not raw_ing_field:
                continue
            
            # Parse list format e.g. "['1 cup flour', '2 eggs']"
            try:
                if raw_ing_field.startswith('[') and raw_ing_field.endswith(']'):
                    ing_list = ast.literal_eval(raw_ing_field)
                else:
                    ing_list = raw_ing_field.split(',')
            except Exception:
                ing_list = raw_ing_field.replace('[', '').replace(']', '').replace("'", "").split(',')

            for ing in ing_list:
                cleaned = clean_ingredient_string(ing)
                if cleaned and len(cleaned) >= 2:
                    ingredient_counts[cleaned] += 1
                    if cleaned not in raw_ingredient_examples:
                        raw_ingredient_examples[cleaned] = ing.strip()

    # Filter ingredients with at least 2 occurrences for cleaner catalog
    unique_list = []
    for ing, count in ingredient_counts.most_common():
        if count >= 2:
            unique_list.append({
                "ingredient": ing,
                "count": count,
                "sample_raw": raw_ingredient_examples.get(ing, ing)
            })

    print(f"Extracted {len(unique_list)} unique canonical ingredients!")
    
    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({
            "total_unique": len(unique_list),
            "ingredients": unique_list
        }, f, indent=2)

    print(f"Saved unique ingredients to {OUTPUT_JSON_PATH}")
    return unique_list

if __name__ == "__main__":
    extract_unique_ingredients()
