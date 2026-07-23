import math
import pandas as pd
from preprocess import check_vegetarian, check_vegan

LOW_COST_KEYWORDS = {
    "flour", "bread", "rice", "salt", "pepper", "sugar", "onion", "onions",
    "garlic", "vinegar", "water", "oats", "oatmeal", "cabbage", "lentils", "chickpeas"
}

HIGH_COST_KEYWORDS = {
    "beef", "steak", "salmon", "shrimp", "seafood", "crab", "lobster", "truffle",
    "saffron", "prosciutto", "walnut", "walnuts", "pecan", "pecans", "lamb", "halibut",
    "duck", "parmesan", "vanilla", "pine nuts", "scallops", "filet", "ribeye", "tuna",
    "paneer", "chicken", "turkey", "pork", "cheese", "butter", "cream", "bacon"
}

ALCOHOL_KEYWORDS = {
    'bourbon', 'whiskey', 'whisky', 'rum', 'tequila', 'vodka', 'gin', 'brandy',
    'wine', 'vermouth', 'cynar', 'triple sec', 'liquor', 'liqueur', 'sazerac',
    'negroni', 'manhattan', 'margarita', 'mojito', 'martini', 'sangria', 'spritz',
    'ale', 'beer', 'champagne', 'prosecco', 'cognac', 'mezcal', 'sherry', 'campari',
    'aperol', 'absinthe', 'kahlua', 'amaretto', 'sake', 'cider', 'cocktail', 'toddy'
}

DRINK_KEYWORDS = {
    'smoothie', 'juice', 'cocktail', 'lemonade', 'shake', 'toddy', 'punch', 'spritz',
    'mocktail', 'latte', 'espresso', 'margarita', 'mojito', 'sangria', 'iced tea',
    'alimony', 'negroni', 'manhattan', 'martini', 'fizz', 'highball', 'cider'
}

def calculate_recipe_budget(row: pd.Series) -> dict:
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
            batch_cost += 4.50
        elif words.intersection(LOW_COST_KEYWORDS):
            batch_cost += 0.80
        else:
            batch_cost += 2.20

    batch_cost = max(4.00, batch_cost)
    cost_per_serving = round(batch_cost / servings, 2)
    total_batch_cost = round(batch_cost, 2)

    # Strict Budget Friendly threshold: <= $1.65 per serving
    is_budget = cost_per_serving <= 1.65
    if is_budget:
        budget_tier = "Budget Friendly"
        budget_symbol = "💲"
    elif cost_per_serving <= 3.50:
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

def sanitize_meal_and_alcohol(title: str, ing_text: str, raw_meal_type: str) -> tuple[str, bool, bool]:
    title_lower = (title or "").lower()
    combined = (title_lower + " " + (ing_text or "")).lower()
    
    is_drink = any(k in title_lower for k in DRINK_KEYWORDS)
    if is_drink:
        meal_type = "Beverage"
        has_alcohol = any(k in combined for k in ALCOHOL_KEYWORDS) and not any(k in combined for k in ["non-alcoholic", "zero-proof", "virgin", "mocktail"])
        return "Beverage", True, has_alcohol
    
    if (raw_meal_type or "").strip().lower() in ["beverage", "drink"]:
        if any(k in title_lower for k in ["pancake", "waffle", "oatmeal", "egg", "toast"]):
            meal_type = "Breakfast"
        elif any(w in title_lower for w in ["cake", "pie", "cookie", "tart", "brownie", "dessert", "poda"]):
            meal_type = "Dessert"
        else:
            meal_type = "Dinner"
    else:
        meal_type = (raw_meal_type or "Dinner").strip()

    return meal_type, False, False

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
    "paneer": ["https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=800&q=80"],
    "samosa": ["https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=800&q=80"],
    "cheesecake_dessert": ["https://images.unsplash.com/photo-1524351199678-941a58a3df50?auto=format&fit=crop&w=800&q=80"],
    "general": ["https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80"]
}

def get_smart_food_image(recipe_name: str, ingredients_text: str = "", cuisine: str = "", meal_type: str = "", is_veg: bool = False, image_name: str = "") -> str:
    return "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80"

def format_recipe_dict(row: pd.Series, recipe_id: int, similarity_score: float = None) -> dict:
    ing_raw = row['Ingredients']
    if isinstance(ing_raw, str):
        ingredients_list = [i.strip() for i in ing_raw.split(',') if i.strip()]
    else:
        ingredients_list = []

    ing_text = str(row['Ingredients'])
    recipe_name = str(row['Recipe Name'])
    cuisine = str(row['Cuisine'])
    raw_meal = str(row['Meal Type'])
    
    is_veg = check_vegetarian(ing_text, recipe_name)
    is_vgn = check_vegan(ing_text, recipe_name)
    meal_type, is_bev, is_alc = sanitize_meal_and_alcohol(recipe_name, ing_text, raw_meal)

    budget_info = calculate_recipe_budget(row)

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
        "image_url": "",
        "is_vegetarian": is_veg,
        "is_vegan": is_vgn,
        "is_beverage": is_bev,
        "is_alcoholic": is_alc,
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
