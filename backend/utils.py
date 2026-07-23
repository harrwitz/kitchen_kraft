import math
import pandas as pd
from preprocess import check_vegetarian, check_vegan

LOW_COST_KEYWORDS = {
    "flour", "bread", "rice", "egg", "eggs", "potato", "potatoes", "pasta", "bean", "beans",
    "noodle", "noodles", "oats", "oatmeal", "onion", "onions", "carrot", "carrots",
    "cabbage", "milk", "water", "salt", "pepper", "sugar", "corn", "garlic", "lentils",
    "chickpeas", "tortilla", "tortillas", "broth", "oil", "yeast", "vinegar"
}

HIGH_COST_KEYWORDS = {
    "beef", "steak", "salmon", "shrimp", "seafood", "crab", "lobster", "truffle",
    "saffron", "prosciutto", "walnut", "walnuts", "pecan", "pecans", "lamb", "halibut",
    "duck", "parmesan", "vanilla", "pine nuts", "scallops", "filet", "ribeye", "tuna"
}

def calculate_recipe_budget(row: pd.Series) -> dict:
    """
    Calculates estimated cost per serving and budget tier based on ingredients and servings.
    """
    ing_val = row.get('Ingredients') if row.get('Ingredients') is not None else row.get('ing', '')
    ing_text = str(ing_val or '').lower()
    try:
        serv_val = row.get('Servings') if row.get('Servings') is not None else row.get('serv', 4)
        servings = int(serv_val or 4)
    except (ValueError, TypeError):
        servings = 4
    if servings <= 0:
        servings = 4

    items = [i.strip() for i in ing_text.split(',') if i.strip()]
    if not items:
        items = [ing_text] if ing_text else ["ingredient"]

    batch_cost = 0.0
    for item in items:
        words = set(item.split())
        if words.intersection(HIGH_COST_KEYWORDS):
            batch_cost += 3.20
        elif words.intersection(LOW_COST_KEYWORDS):
            batch_cost += 0.85
        else:
            batch_cost += 1.60

    # Ensure reasonable base batch cost
    batch_cost = max(2.50, batch_cost)
    cost_per_serving = round(batch_cost / servings, 2)
    total_batch_cost = round(batch_cost, 2)

    is_budget = cost_per_serving <= 2.75
    if is_budget:
        budget_tier = "Budget Friendly"
        budget_symbol = "💲"
    elif cost_per_serving <= 5.00:
        budget_tier = "Moderate"
        budget_symbol = "💲💲"
    else:
        budget_tier = "Gourmet"
        budget_symbol = "💲💲💲"

    return {
        "cost_per_serving": cost_per_serving,
        "total_batch_cost": total_batch_cost,
        "is_budget": is_budget,
        "budget_tier": budget_tier,
        "budget_symbol": budget_symbol
    }

def filter_recipes_dataframe(
    df: pd.DataFrame,
    is_vegetarian: bool = None,
    is_vegan: bool = None,
    cuisine: str = None,
    meal_type: str = None,
    max_calories: int = None,
    max_cook_time: int = None,
    max_prep_time: int = None,
    difficulty: str = None,
    min_protein: int = None,
    is_budget: bool = None,
    budget_tier: str = None
) -> list[int]:
    """
    Applies filter parameters against DataFrame and returns matching row indices.
    """
    mask = pd.Series([True] * len(df), index=df.index)

    if cuisine and cuisine.strip() and cuisine.lower() != "all":
        mask &= (df['Cuisine'].str.lower() == cuisine.strip().lower())

    if meal_type and meal_type.strip() and meal_type.lower() != "all":
        mask &= (df['Meal Type'].str.lower() == meal_type.strip().lower())

    if max_calories is not None and max_calories > 0:
        mask &= (df['Calories'] <= max_calories)

    if max_cook_time is not None and max_cook_time > 0:
        mask &= (df['Cook Time'] <= max_cook_time)

    if max_prep_time is not None and max_prep_time > 0:
        mask &= (df['Prep Time'] <= max_prep_time)

    if difficulty and difficulty.strip() and difficulty.lower() != "all":
        mask &= (df['Difficulty'].str.lower() == difficulty.strip().lower())

    if min_protein is not None and min_protein > 0:
        mask &= (df['Protein'] >= min_protein)

    matching_indices = df[mask].index.tolist()

    filtered_indices = []
    for idx in matching_indices:
        row = df.loc[idx]
        ing_text = str(row['Ingredients'])
        recipe_name = str(row.get('Recipe Name', ''))
        
        if is_vegan and not check_vegan(ing_text, recipe_name):
            continue
        if is_vegetarian and not check_vegetarian(ing_text, recipe_name):
            continue
            
        budget_info = calculate_recipe_budget(row)
        if is_budget is True and not budget_info["is_budget"]:
            continue
        if budget_tier and budget_tier.lower() != "all" and budget_info["budget_tier"].lower() != budget_tier.lower():
            continue
            
        filtered_indices.append(idx)

    return filtered_indices

FOOD_IMAGES_CATEGORIES = {
    "cocktails_drinks": [
        "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1536935338788-846bb9981813?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1556881286-fc6915169721?auto=format&fit=crop&w=800&q=80"
    ],
    "smoothie_juice": [
        "https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?auto=format&fit=crop&w=800&q=80"
    ],
    "roast_chicken": [
        "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=800&q=80"
    ],
    "chicken": [
        "https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80"
    ],
    "squash_pumpkin": [
        "https://images.unsplash.com/photo-1570586437263-ab629fccc818?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1508747703725-719777637510?auto=format&fit=crop&w=800&q=80"
    ],
    "beef_steak": [
        "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=800&q=80"
    ],
    "salmon_fish": [
        "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=800&q=80"
    ],
    "seafood_shrimp": [
        "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1559742811-8228a365ccdf?auto=format&fit=crop&w=800&q=80"
    ],
    "burger": [
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=800&q=80"
    ],
    "pizza": [
        "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80"
    ],
    "lasagna": [
        "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?auto=format&fit=crop&w=800&q=80"
    ],
    "pasta": [
        "https://images.unsplash.com/photo-1621996346565-e3d5d6281358?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=80"
    ],
    "mac_cheese": [
        "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=800&q=80"
    ],
    "tacos_mexican": [
        "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?auto=format&fit=crop&w=800&q=80"
    ],
    "salad": [
        "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80"
    ],
    "soup_stew": [
        "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1608897013039-887f21d8c804?auto=format&fit=crop&w=800&q=80"
    ],
    "curry_paneer": [
        "https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=800&q=80"
    ],
    "ramen_noodles": [
        "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1617093727343-374698b1b08d?auto=format&fit=crop&w=800&q=80"
    ],
    "sushi": [
        "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=800&q=80"
    ],
    "sandwich": [
        "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=800&q=80"
    ],
    "breakfast_pancakes": [
        "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=80"
    ],
    "dessert_pie_cake": [
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=800&q=80"
    ],
    "potato": [
        "https://images.unsplash.com/photo-1518013431117-eb1465fa5752?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=800&q=80"
    ],
    "general": [
        "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1493770348161-369560ae357d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=800&q=80"
    ]
}

def get_smart_food_image(recipe_name: str, ingredients_text: str, cuisine: str, meal_type: str, is_veg: bool) -> str:
    name_lower = (recipe_name or "").lower()
    combined = (name_lower + " " + (ingredients_text or "")).lower()
    name_hash = abs(hash(recipe_name or "food"))

    # Priority matching on cocktails & drinks
    if any(w in name_lower for w in [
        "alimony", "cocktail", "drink", "beverage", "punch", "sangria", "mojito", "margarita",
        "martini", "cynar", "sherry", "vermouth", "spritz", "bourbon", "whiskey", "rum", "tequila",
        "vodka", "brandy", "mocktail", "tonic", "fizz", "highball", "sour", "slushie", "negroni", "manhattan"
    ]) or any(w in combined for w in ["sherry", "cynar", "dry vermouth", "gin", "bourbon", "tequila", "triple sec", "simple syrup", "angostura"]):
        pool = FOOD_IMAGES_CATEGORIES["cocktails_drinks"]
    elif any(w in name_lower for w in ["smoothie", "juice", "lemonade", "shake", "milkshake"]):
        pool = FOOD_IMAGES_CATEGORIES["smoothie_juice"]
    # Priority matching on specific dish titles
    elif any(w in name_lower for w in ["roast chicken", "roasted chicken"]):
        pool = FOOD_IMAGES_CATEGORIES["roast_chicken"]
    elif any(w in name_lower for w in ["squash", "pumpkin"]):
        pool = FOOD_IMAGES_CATEGORIES["squash_pumpkin"]
    elif any(w in name_lower for w in ["lasagna"]):
        pool = FOOD_IMAGES_CATEGORIES["lasagna"]
    elif any(w in name_lower for w in ["macaroni", "mac and cheese"]):
        pool = FOOD_IMAGES_CATEGORIES["mac_cheese"]
    elif any(w in name_lower for w in ["burger", "cheeseburger"]):
        pool = FOOD_IMAGES_CATEGORIES["burger"]
    elif any(w in name_lower for w in ["pizza"]):
        pool = FOOD_IMAGES_CATEGORIES["pizza"]
    elif any(w in name_lower for w in ["taco", "burrito", "nacho", "quesadilla", "enchilada"]):
        pool = FOOD_IMAGES_CATEGORIES["tacos_mexican"]
    elif any(w in name_lower for w in ["salmon", "tuna", "trout"]):
        pool = FOOD_IMAGES_CATEGORIES["salmon_fish"]
    elif any(w in name_lower for w in ["shrimp", "prawn", "lobster", "crab", "seafood"]):
        pool = FOOD_IMAGES_CATEGORIES["seafood_shrimp"]
    elif any(w in name_lower for w in ["steak", "beef", "brisket", "ribeye", "filet"]):
        pool = FOOD_IMAGES_CATEGORIES["beef_steak"]
    elif any(w in name_lower for w in ["chicken", "poultry", "turkey", "wing"]):
        pool = FOOD_IMAGES_CATEGORIES["chicken"]
    elif any(w in name_lower for w in ["pasta", "spaghetti", "penne", "fettuccine", "rigatoni", "noodle"]):
        pool = FOOD_IMAGES_CATEGORIES["pasta"]
    elif any(w in name_lower for w in ["salad", "greens"]):
        pool = FOOD_IMAGES_CATEGORIES["salad"]
    elif any(w in name_lower for w in ["soup", "stew", "chowder", "bisque", "broth"]):
        pool = FOOD_IMAGES_CATEGORIES["soup_stew"]
    elif any(w in name_lower for w in ["paneer", "tikka", "dal", "curry", "masala"]):
        pool = FOOD_IMAGES_CATEGORIES["curry_paneer"]
    elif any(w in name_lower for w in ["ramen", "pho", "dumpling", "tofu"]):
        pool = FOOD_IMAGES_CATEGORIES["ramen_noodles"]
    elif any(w in name_lower for w in ["sushi", "sashimi", "roll"]):
        pool = FOOD_IMAGES_CATEGORIES["sushi"]
    elif any(w in name_lower for w in ["sandwich", "panini", "wrap", "toast"]):
        pool = FOOD_IMAGES_CATEGORIES["sandwich"]
    elif any(w in name_lower for w in ["pancake", "waffle", "french toast"]):
        pool = FOOD_IMAGES_CATEGORIES["breakfast_pancakes"]
    elif any(w in name_lower for w in ["pie", "cake", "tart", "brownie", "ice cream", "cookie"]):
        pool = FOOD_IMAGES_CATEGORIES["dessert_pie_cake"]
    # Fallback to combined ingredient checking
    elif any(w in combined for w in ["chicken", "poultry"]):
        pool = FOOD_IMAGES_CATEGORIES["chicken"]
    elif any(w in combined for w in ["beef", "steak", "pork", "lamb"]):
        pool = FOOD_IMAGES_CATEGORIES["beef_steak"]
    elif any(w in combined for w in ["fish", "salmon", "shrimp", "seafood"]):
        pool = FOOD_IMAGES_CATEGORIES["salmon_fish"]
    elif any(w in combined for w in ["pasta", "spaghetti"]):
        pool = FOOD_IMAGES_CATEGORIES["pasta"]
    elif any(w in combined for w in ["salad", "lettuce", "greens"]):
        pool = FOOD_IMAGES_CATEGORIES["salad"]
    elif any(w in combined for w in ["soup", "stew"]):
        pool = FOOD_IMAGES_CATEGORIES["soup_stew"]
    else:
        pool = FOOD_IMAGES_CATEGORIES["general"]

    return pool[name_hash % len(pool)]

def format_recipe_dict(row: pd.Series, recipe_id: int, similarity_score: float = None) -> dict:
    """Format DataFrame row into clean JSON API response object."""
    ing_raw = row['Ingredients']
    if isinstance(ing_raw, str):
        ingredients_list = [i.strip() for i in ing_raw.split(',') if i.strip()]
    else:
        ingredients_list = []

    ing_text = str(row['Ingredients'])
    recipe_name = str(row['Recipe Name'])
    cuisine = str(row['Cuisine'])
    meal_type = str(row['Meal Type'])
    
    is_veg = check_vegetarian(ing_text, recipe_name)
    is_vgn = check_vegan(ing_text, recipe_name)

    budget_info = calculate_recipe_budget(row)
    smart_image = get_smart_food_image(recipe_name, ing_text, cuisine, meal_type, is_veg)

    res = {
        "id": int(recipe_id),
        "recipe_name": recipe_name,
        "ingredients": ingredients_list,
        "raw_ingredients": ing_text,
        "instructions": str(row['Instructions']),
        "cuisine": cuisine,
        "meal_type": meal_type,
        "prep_time": int(row['Prep Time']),
        "cook_time": int(row['Cook Time']),
        "total_time": int(row['Prep Time']) + int(row['Cook Time']),
        "calories": int(row['Calories']),
        "protein": int(row['Protein']),
        "carbs": int(row['Carbs']),
        "fat": int(row['Fat']),
        "difficulty": str(row['Difficulty']),
        "servings": int(row['Servings']),
        "image_url": smart_image,
        "is_vegetarian": is_veg,
        "is_vegan": is_vgn,
        "is_budget": budget_info["is_budget"],
        "budget_tier": budget_info["budget_tier"],
        "budget_symbol": budget_info["budget_symbol"],
        "cost_per_serving": budget_info["cost_per_serving"],
        "total_batch_cost": budget_info["total_batch_cost"]
    }

    if similarity_score is not None:
        pct = round(max(0.0, min(1.0, similarity_score)) * 100, 1)
        res["similarity_score"] = pct
        res["similarity_percent"] = f"{pct}%"

    return res

