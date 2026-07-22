import csv
import re
import os
import ast
import random

RAW_CSV = os.path.join(os.path.dirname(__file__), "Food Ingredients and Recipe Dataset with Image Name Mapping.csv")
TARGET_CSV = os.path.join(os.path.dirname(__file__), "recipes.csv")

# Unsplash High Quality Food Images keyed by category/cuisine
FOOD_IMAGES = {
    "Italian": [
        "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80", # Pizza
        "https://images.unsplash.com/photo-1621996346565-e3d5d6281358?auto=format&fit=crop&w=800&q=80", # Pasta
        "https://images.unsplash.com/photo-1579684947550-22e945225d9a?auto=format&fit=crop&w=800&q=80", # Lasagna
        "https://images.unsplash.com/photo-1595295333158-4742f28fbd85?auto=format&fit=crop&w=800&q=80", # Spag bol
    ],
    "Asian": [
        "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80", # Ramen
        "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=800&q=80", # Stir fry
        "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80", # Asian bowl
        "https://images.unsplash.com/photo-1617093727343-374698b1b08d?auto=format&fit=crop&w=800&q=80", # Dumplings
    ],
    "Mexican": [
        "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=800&q=80", # Tacos
        "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=800&q=80", # Burrito
        "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?auto=format&fit=crop&w=800&q=80", # Nachos
    ],
    "Indian": [
        "https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=800&q=80", # Curry
        "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80", # Butter chicken
        "https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&w=800&q=80", # Biryani
    ],
    "French": [
        "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80", # Bakery
        "https://images.unsplash.com/photo-1608897013039-887f21d8c804?auto=format&fit=crop&w=800&q=80", # French soup
    ],
    "Mediterranean": [
        "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80", # Salad bowl
        "https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=800&q=80", # Hummus pita
    ],
    "American": [
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80", # Burger
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80", # Salad
        "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?auto=format&fit=crop&w=800&q=80", # BBQ Ribs
    ],
    "Dessert": [
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=800&q=80", # Chocolate cake
        "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80", # Desserts
        "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?auto=format&fit=crop&w=800&q=80", # Cupcake
    ],
    "Default": [
        "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80", # Healthy spread
        "https://images.unsplash.com/photo-1493770348161-369560ae357d?auto=format&fit=crop&w=800&q=80", # Breakfast plate
        "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=800&q=80", # Food feast
    ]
}

CUISINE_KEYWORDS = {
    "Italian": ["pasta", "spaghetti", "pizza", "risotto", "parmesan", "mozzarella", "pesto", "lasagna", "gnocchi", "marinara", "ricotta", "prosciutto", "tiramisu"],
    "Asian": ["soy sauce", "ginger", "sesame", "ramen", "miso", "teriyaki", "tofu", "wok", "dumpling", "noodle", "sake", "wasabi", "hoisin", "bamboo"],
    "Mexican": ["taco", "tortilla", "salsa", "cilantro", "jalapeño", "jalapeno", "avocado", "guacamole", "burrito", "enchilada", "quesadilla", "chipotle", "casserole"],
    "Indian": ["curry", "turmeric", "garam masala", "cumin", "coriander", "paneer", "naan", "cardamom", "chutney", "masala", "tikka", "samosa"],
    "French": ["butter", "wine", "shallot", "tarragon", "baguette", "creme", "quiche", "brie", "soufflé", "dijon", "croissant"],
    "Mediterranean": ["olive oil", "feta", "cucumber", "tahini", "hummus", "greek", "pita", "falafel", "tzatziki", "olives", "lemon"],
    "Japanese": ["miso", "mirin", "dashi", "sushi", "wasabi", "norib", "matcha", "tempura"],
    "Thai": ["coconut milk", "fish sauce", "lemongrass", "pad thai", "curry paste", "galangal", "thai basil"],
}

MEAL_TYPE_KEYWORDS = {
    "Breakfast": ["pancake", "waffle", "egg", "bacon", "toast", "cereal", "oatmeal", "muffin", "frittata", "omelet", "smoothie", "granola"],
    "Dessert": ["cake", "cookie", "pie", "ice cream", "chocolate", "brownie", "tart", "pudding", "sweet", "frosting", "caramel", "vanilla"],
    "Beverage": ["cocktail", "smoothie", "juice", "tea", "coffee", "lemonade", "punch", "drink", "shake", "cider", "sangria"],
    "Appetizer": ["dip", "crostini", "wings", "slider", "bite", "skewers", "tartlet", "nacho", "bruschetta"],
    "Lunch": ["sandwich", "salad", "wrap", "soup", "burger", "panini"],
}

def infer_cuisine(title: str, ing_str: str) -> str:
    combined = (title + " " + ing_str).lower()
    for cuisine, keywords in CUISINE_KEYWORDS.items():
        if any(k in combined for k in keywords):
            return cuisine
    return "American"

def infer_meal_type(title: str, ing_str: str) -> str:
    combined = (title + " " + ing_str).lower()
    for meal, keywords in MEAL_TYPE_KEYWORDS.items():
        if any(k in combined for k in keywords):
            return meal
    return "Dinner" if ("roast" in combined or "chicken" in combined or "steak" in combined or "stew" in combined) else "Lunch"

def estimate_times(instructions: str) -> tuple[int, int]:
    # Extract minutes from text if mentioned e.g. "30 minutes"
    matches = re.findall(r'(\d+)\s*(?:-|to)?\s*(\d+)?\s*(?:minutes|mins|hr|hours)', instructions.lower())
    times = []
    for m in matches:
        val = int(m[0])
        if 'hr' in instructions or 'hour' in instructions:
            if val < 10: val *= 60
        times.append(val)
    
    total = sum(times) if times else random.randint(20, 60)
    prep = max(5, int(total * 0.3)) if total <= 60 else random.randint(10, 30)
    cook = max(10, total - prep)
    return prep, cook

def estimate_nutrition(title: str, ing_str: str) -> tuple[int, int, int, int]:
    combined = (title + " " + ing_str).lower()
    
    is_high_protein = any(k in combined for k in ["chicken", "beef", "pork", "steak", "turkey", "fish", "salmon", "shrimp", "tofu", "egg"])
    is_dessert = any(k in combined for k in ["sugar", "chocolate", "cake", "cookie", "sweet", "cream", "pie"])
    is_light = any(k in combined for k in ["salad", "soup", "cucumber", "zucchini", "spinach", "vegetable"])
    
    if is_dessert:
        cal = random.randint(350, 650)
        protein = random.randint(3, 10)
        carbs = random.randint(45, 90)
        fat = random.randint(12, 35)
    elif is_light:
        cal = random.randint(150, 350)
        protein = random.randint(5, 18)
        carbs = random.randint(10, 35)
        fat = random.randint(6, 18)
    elif is_high_protein:
        cal = random.randint(450, 750)
        protein = random.randint(28, 55)
        carbs = random.randint(15, 55)
        fat = random.randint(14, 38)
    else:
        cal = random.randint(300, 550)
        protein = random.randint(10, 25)
        carbs = random.randint(30, 65)
        fat = random.randint(10, 25)
        
    return cal, protein, carbs, fat

def assign_image(cuisine: str, title: str) -> str:
    pool = FOOD_IMAGES.get(cuisine, FOOD_IMAGES["Default"])
    # Deterministic choice based on hash of title
    idx = abs(hash(title)) % len(pool)
    return pool[idx]

def prepare_recipes_csv():
    print(f"Reading raw dataset from {RAW_CSV}...")
    if not os.path.exists(RAW_CSV):
        print(f"Error: {RAW_CSV} not found.")
        return

    fieldnames = [
        "Recipe Name", "Ingredients", "Instructions", "Cuisine", "Meal Type",
        "Prep Time", "Cook Time", "Calories", "Protein", "Carbs", "Fat",
        "Difficulty", "Servings", "Image URL"
    ]

    out_rows = []
    
    with open(RAW_CSV, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            title = (row.get("Title") or "").strip()
            instructions = (row.get("Instructions") or "").strip()
            raw_ing = row.get("Cleaned_Ingredients") or row.get("Ingredients") or ""

            if not title or len(title) < 3 or not instructions:
                continue

            # Format ingredients list string cleanly
            try:
                if raw_ing.startswith('[') and raw_ing.endswith(']'):
                    ing_parsed = ast.literal_eval(raw_ing)
                    ing_str = ", ".join(ing_parsed)
                else:
                    ing_str = raw_ing
            except Exception:
                ing_str = raw_ing.replace('[', '').replace(']', '').replace("'", "")

            cuisine = infer_cuisine(title, ing_str)
            meal_type = infer_meal_type(title, ing_str)
            prep_time, cook_time = estimate_times(instructions)
            cal, protein, carbs, fat = estimate_nutrition(title, ing_str)
            
            total_time = prep_time + cook_time
            if total_time <= 25:
                difficulty = "Easy"
            elif total_time <= 55:
                difficulty = "Medium"
            else:
                difficulty = "Hard"

            servings = random.choice([2, 4, 4, 6, 6, 8])
            image_url = assign_image(cuisine, title)

            out_rows.append({
                "Recipe Name": title,
                "Ingredients": ing_str,
                "Instructions": instructions,
                "Cuisine": cuisine,
                "Meal Type": meal_type,
                "Prep Time": prep_time,
                "Cook Time": cook_time,
                "Calories": cal,
                "Protein": protein,
                "Carbs": carbs,
                "Fat": fat,
                "Difficulty": difficulty,
                "Servings": servings,
                "Image URL": image_url
            })

    print(f"Writing {len(out_rows)} formatted recipes to {TARGET_CSV}...")
    with open(TARGET_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"Successfully generated permanent dataset at {TARGET_CSV}!")

if __name__ == "__main__":
    prepare_recipes_csv()
