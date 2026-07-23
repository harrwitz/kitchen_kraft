import os
import sys

# Ensure backend directory is in sys.path for cross-environment imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import csv
import json
import difflib
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List

from preprocess import clean_text, check_vegetarian, check_vegan
from utils import calculate_recipe_budget, get_smart_food_image

CSV_PATH = os.path.join(os.path.dirname(__file__), "recipes.csv")
UNIQUE_INGREDIENTS_PATH = os.path.join(os.path.dirname(__file__), "unique_ingredients.json")

class AppState:
    recipes: List[dict] = []
    recipes_by_id: dict = {}
    unique_ingredients: List[dict] = []
    is_loaded: bool = False

state = AppState()

def ensure_state_loaded():
    """
    Fast, lightweight, zero-heavy-dependency state loader.
    Supports gzipped compact JSON dataset (~5.8MB) for instant Vercel Serverless cold starts.
    """
    if state.is_loaded:
        return

    print("Initializing AI Recipe Builder Backend (Lightweight Serverless Engine)...")

    raw_data = []

    candidate_csv_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api", "recipes.csv")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "recipes.csv")),
        os.path.join(os.getcwd(), "api", "recipes.csv"),
        os.path.join(os.getcwd(), "backend", "recipes.csv"),
    ]

    # 1. Try reading recipes.csv (from api/ directory or backend/ directory)
    for csv_path in candidate_csv_paths:
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                    raw_data = list(csv.DictReader(f))
                    print(f"Loaded {len(raw_data)} recipes from CSV at {csv_path}.")
                    break
            except Exception as e:
                print(f"CSV load error for {csv_path}: {e}")

    # 2. Try compressed JSON.GZ file fallback
    if not raw_data:
        candidate_gz_paths = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api", "recipes_compact.json.gz")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "recipes_compact.json.gz")),
            os.path.join(os.getcwd(), "api", "recipes_compact.json.gz"),
            os.path.join(os.getcwd(), "backend", "recipes_compact.json.gz"),
        ]
        for gz_path in candidate_gz_paths:
            if os.path.exists(gz_path):
                try:
                    import gzip
                    with gzip.open(gz_path, 'rt', encoding='utf-8') as f:
                        raw_data = json.load(f)
                        print(f"Loaded {len(raw_data)} recipes from {gz_path}.")
                        break
                except Exception as e:
                    print(f"GZ load error for {gz_path}: {e}")

    # 3. Try JSON file fallback
    if not raw_data:
        candidate_json_paths = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api", "recipes_compact.json")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "recipes_compact.json")),
            os.path.join(os.getcwd(), "api", "recipes_compact.json"),
            os.path.join(os.getcwd(), "backend", "recipes_compact.json"),
        ]
        for json_path in candidate_json_paths:
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        raw_data = json.load(f)
                        print(f"Loaded {len(raw_data)} recipes from {json_path}.")
                        break
                except Exception as e:
                    print(f"JSON load error for {json_path}: {e}")

    if not raw_data:
        raise RuntimeError("No recipe data available to load!")

    loaded_recipes = []
    loaded_by_id = {}

    for idx, row in enumerate(raw_data):
        title = (row.get('Recipe Name') or row.get('name') or 'Untitled Recipe').strip()
        ing_text = (row.get('Ingredients') or row.get('ing') or '').strip()
        instructions = (row.get('Instructions') or row.get('inst') or '').strip()
        cuisine = (row.get('Cuisine') or row.get('cuis') or 'American').strip()
        meal_type = (row.get('Meal Type') or row.get('meal') or 'Dinner').strip()

        if ing_text.startswith('[') and ing_text.endswith(']'):
            try:
                import ast
                ing_parsed = ast.literal_eval(ing_text)
                ingredients_list = [i.strip() for i in ing_parsed if i.strip()]
            except Exception:
                ingredients_list = [i.strip() for i in ing_text.split(',') if i.strip()]
        else:
            ingredients_list = [i.strip() for i in ing_text.split(',') if i.strip()]

        try:
            prep_val = row.get('Prep Time') if row.get('Prep Time') is not None else row.get('prep', 15)
            prep_time = int(prep_val if prep_val is not None else 15)
        except (ValueError, TypeError): prep_time = 15

        try:
            cook_val = row.get('Cook Time') if row.get('Cook Time') is not None else row.get('cook', 30)
            cook_time = int(cook_val if cook_val is not None else 30)
        except (ValueError, TypeError): cook_time = 30

        try:
            cal_val = row.get('Calories') if row.get('Calories') is not None else row.get('cal', 400)
            calories = int(cal_val if cal_val is not None else 400)
        except (ValueError, TypeError): calories = 400

        try:
            prot_val = row.get('Protein') if row.get('Protein') is not None else row.get('prot', 20)
            protein = int(prot_val if prot_val is not None else 20)
        except (ValueError, TypeError): protein = 20

        try:
            carb_val = row.get('Carbs') if row.get('Carbs') is not None else row.get('carb', 40)
            carbs = int(carb_val if carb_val is not None else 40)
        except (ValueError, TypeError): carbs = 40

        try:
            fat_val = row.get('Fat') if row.get('Fat') is not None else row.get('fat', 15)
            fat = int(fat_val if fat_val is not None else 15)
        except (ValueError, TypeError): fat = 15

        try:
            serv_val = row.get('Servings') if row.get('Servings') is not None else row.get('serv', 4)
            servings = int(serv_val if serv_val is not None else 4)
        except (ValueError, TypeError): servings = 4

        difficulty = (row.get('Difficulty') or row.get('diff') or 'Medium').strip()

        is_veg = check_vegetarian(ing_text, title)
        is_vgn = check_vegan(ing_text, title)
        budget_info = calculate_recipe_budget(row)
        smart_image = get_smart_food_image(title, ing_text, cuisine, meal_type, is_veg)

        item = {
            "id": idx,
            "recipe_name": title,
            "ingredients": ingredients_list,
            "raw_ingredients": ing_text,
            "instructions": instructions,
            "cuisine": cuisine,
            "meal_type": meal_type,
            "prep_time": prep_time,
            "cook_time": cook_time,
            "total_time": prep_time + cook_time,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "difficulty": difficulty,
            "servings": servings,
            "image_url": smart_image,
            "is_vegetarian": is_veg,
            "is_vegan": is_vgn,
            "is_budget": budget_info["is_budget"],
            "budget_tier": budget_info["budget_tier"],
            "budget_symbol": budget_info["budget_symbol"],
            "cost_per_serving": budget_info["cost_per_serving"],
            "total_batch_cost": budget_info["total_batch_cost"]
        }
        loaded_recipes.append(item)
        loaded_by_id[idx] = item

    state.recipes = loaded_recipes
    state.recipes_by_id = loaded_by_id

    candidate_ing_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api", "unique_ingredients.json")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "unique_ingredients.json")),
        os.path.join(os.getcwd(), "api", "unique_ingredients.json"),
        os.path.join(os.getcwd(), "backend", "unique_ingredients.json"),
    ]

    for ing_path in candidate_ing_paths:
        if os.path.exists(ing_path):
            try:
                with open(ing_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    state.unique_ingredients = data.get("ingredients", [])
                    print(f"Loaded {len(state.unique_ingredients)} unique ingredients from {ing_path}.")
                    break
            except Exception as e:
                print(f"Warning loading unique_ingredients.json from {ing_path}: {e}")

    state.is_loaded = True
    print(f"Loaded {len(state.recipes)} recipes into RAM.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_state_loaded()
    yield

app = FastAPI(
    title="AI Recipe Builder API",
    description="Production Machine Learning Recipe Search & Recommendation API powered by TF-IDF & Cosine Similarity",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def fix_vercel_path(request, call_next):
    path = request.scope.get("path", "")
    headers = request.headers
    matched = headers.get("x-matched-path") or headers.get("x-invoke-path") or headers.get("x-forwarded-uri") or headers.get("x-url")

    if path in ["/api", "/api/"] or path.startswith("/api/index.py"):
        if matched and matched not in ["/", "/api", "/api/index.py"]:
            request.scope["path"] = matched if matched.startswith("/api") else f"/api{matched}"
        elif path.startswith("/api/index.py"):
            sub = path.replace("/api/index.py", "")
            if sub and sub != "/":
                request.scope["path"] = sub if sub.startswith("/api") else f"/api{sub}"

    return await call_next(request)

INGREDIENT_EXPANSIONS = {
    "paneer": ["paneer", "cottage cheese", "indian cottage cheese", "chenna"],
    "panner": ["paneer", "cottage cheese", "indian cottage cheese", "chenna"],
    "paner": ["paneer", "cottage cheese", "indian cottage cheese", "chenna"],
    "panneer": ["paneer", "cottage cheese", "indian cottage cheese", "chenna"],
    "panir": ["paneer", "cottage cheese", "indian cottage cheese", "chenna"],
    "cottage cheese": ["cottage cheese", "paneer", "indian cottage cheese", "chenna"],
    "haldi": ["haldi", "turmeric", "ground turmeric", "turmeric powder"],
    "haldii": ["haldi", "turmeric", "ground turmeric", "turmeric powder"],
    "turmeric": ["turmeric", "haldi", "ground turmeric", "turmeric powder"],
    "jeera": ["jeera", "zeera", "jira", "zira", "geera", "cumin", "cumin seeds", "ground cumin"],
    "zeera": ["zeera", "jeera", "cumin", "cumin seeds", "ground cumin"],
    "jira": ["jira", "jeera", "cumin", "cumin seeds", "ground cumin"],
    "zira": ["zira", "jeera", "cumin", "cumin seeds"],
    "cumin": ["cumin", "jeera", "zeera", "cumin seeds", "ground cumin"],
    "dhania": ["dhania", "dhaniya", "coriander", "coriander powder", "coriander seeds", "cilantro"],
    "dhaniya": ["dhaniya", "dhania", "coriander", "coriander powder", "coriander seeds", "cilantro"],
    "coriander": ["coriander", "dhania", "dhaniya", "cilantro", "coriander powder"],
    "cilantro": ["cilantro", "coriander", "dhania", "fresh coriander"],
    "adrak": ["adrak", "adrakh", "ginger", "fresh ginger", "ginger paste"],
    "adrakh": ["adrakh", "adrak", "ginger", "fresh ginger", "ginger paste"],
    "ginger": ["ginger", "adrak", "fresh ginger", "ginger paste"],
    "lehsun": ["lehsun", "lahsun", "lehson", "lesun", "garlic", "garlic cloves", "minced garlic"],
    "lahsun": ["lahsun", "lehsun", "garlic", "garlic cloves", "minced garlic"],
    "garlic": ["garlic", "lehsun", "lahsun", "garlic cloves", "minced garlic"],
    "pyaaz": ["pyaaz", "pyaz", "piaz", "kanda", "onion", "onions", "yellow onion", "red onion"],
    "pyaz": ["pyaz", "pyaaz", "piaz", "kanda", "onion", "onions", "yellow onion", "red onion"],
    "kanda": ["kanda", "pyaz", "pyaaz", "onion", "onions"],
    "onion": ["onion", "onions", "pyaz", "pyaaz", "kanda", "yellow onion", "red onion", "shallots"],
    "aloo": ["aloo", "alu", "allu", "potato", "potatoes", "russet potato", "sweet potato"],
    "alu": ["alu", "aloo", "potato", "potatoes"],
    "potato": ["potato", "potatoes", "aloo", "alu", "russet potato", "sweet potato"],
    "tamatar": ["tamatar", "tomato", "tomatoes", "diced tomatoes", "tomato paste"],
    "tomato": ["tomato", "tomatoes", "tamatar", "cherry tomatoes", "tomato paste", "roma tomatoes"],
    "palak": ["palak", "spinach", "fresh spinach", "baby spinach"],
    "spinach": ["spinach", "palak", "fresh spinach", "baby spinach"],
    "methi": ["methi", "fenugreek", "fenugreek leaves"],
    "fenugreek": ["fenugreek", "methi", "fenugreek leaves"],
    "dal": ["dal", "daal", "dhal", "lentils", "yellow lentils", "red lentils", "chana dal", "urad dal", "toor dal", "moong dal"],
    "daal": ["daal", "dal", "lentils", "yellow lentils", "red lentils"],
    "lentils": ["lentils", "dal", "daal", "yellow lentils", "red lentils"],
    "chana": ["chana", "chole", "chickpeas", "garbanzo beans", "kabuli chana"],
    "chole": ["chole", "chana", "chickpeas", "garbanzo beans"],
    "chickpeas": ["chickpeas", "chana", "chole", "garbanzo beans", "kabuli chana"],
    "rajma": ["rajma", "kidney beans", "red kidney beans"],
    "kidney beans": ["kidney beans", "rajma", "red kidney beans"],
    "atta": ["atta", "maida", "flour", "wheat flour", "whole wheat flour", "all-purpose flour"],
    "maida": ["maida", "atta", "flour", "all-purpose flour"],
    "flour": ["flour", "atta", "maida", "all-purpose flour", "whole wheat flour"],
    "dahi": ["dahi", "curd", "yogurt", "greek yogurt", "plain yogurt"],
    "curd": ["curd", "dahi", "yogurt"],
    "yogurt": ["yogurt", "dahi", "curd", "greek yogurt"],
    "ghee": ["ghee", "clarified butter", "butter"],
    "butter": ["butter", "ghee", "clarified butter"],
    "sarson": ["sarson", "rai", "mustard", "mustard seeds", "mustard oil"],
    "rai": ["rai", "sarson", "mustard", "mustard seeds"],
    "mustard": ["mustard", "sarson", "rai", "mustard seeds", "mustard oil"],
    "hing": ["hing", "asafoetida"],
    "asafoetida": ["asafoetida", "hing"],
    "elaichi": ["elaichi", "cardamom", "green cardamom"],
    "cardamom": ["cardamom", "elaichi", "green cardamom"],
    "laung": ["laung", "lavang", "cloves", "whole cloves"],
    "cloves": ["cloves", "laung", "lavang", "whole cloves"],
    "dalchini": ["dalchini", "cinnamon", "cinnamon stick", "ground cinnamon"],
    "cinnamon": ["cinnamon", "dalchini", "ground cinnamon"],
    "pudina": ["pudina", "mint", "fresh mint"],
    "mint": ["mint", "pudina", "fresh mint"],
    "hari mirch": ["hari mirch", "green chili", "green chilies", "green chili pepper"],
    "green chili": ["green chili", "hari mirch", "green chilies"],
    "lal mirch": ["lal mirch", "red chili", "red chili powder", "cayenne pepper"],
    "red chili": ["red chili", "lal mirch", "red chili powder"],
    "suji": ["suji", "sooji", "semolina"],
    "sooji": ["sooji", "suji", "semolina"],
    "semolina": ["semolina", "suji", "sooji"],
    "besan": ["besan", "gram flour", "chickpea flour"],
    "gram flour": ["gram flour", "besan", "chickpea flour"],
    "poha": ["poha", "flattened rice"],
    "matar": ["matar", "peas", "green peas"],
    "peas": ["peas", "matar", "green peas"],
    "bhindi": ["bhindi", "okra", "ladyfinger"],
    "okra": ["okra", "bhindi", "ladyfinger"],
    "gobi": ["gobi", "gobhi", "cauliflower"],
    "gobhi": ["gobhi", "gobi", "cauliflower"],
    "cauliflower": ["cauliflower", "gobi", "gobhi"],
    "baingan": ["baingan", "eggplant", "brinjal"],
    "eggplant": ["eggplant", "baingan", "brinjal"],
    "kaddu": ["kaddu", "pumpkin"],
    "kaju": ["kaju", "cashew", "cashews"],
    "badam": ["badam", "almond", "almonds"],
    "saunf": ["saunf", "fennel", "fennel seeds"],
    "amchur": ["amchur", "amchoor", "dry mango powder"],
    "kasuri methi": ["kasuri methi", "dried fenugreek"],
    "bread": ["bread", "country bread", "sourdough", "white bread", "whole wheat bread", "french bread", "pita", "rye bread", "brioche", "baguette", "ciabatta", "roti", "naan"],
    "cheese": ["cheese", "cheddar", "mozzarella", "parmesan", "feta", "swiss cheese", "ricotta", "paneer", "cottage cheese"],
    "chicken": ["chicken", "chicken breast", "chicken thighs", "ground chicken", "whole chicken"],
    "rice": ["rice", "white rice", "brown rice", "basmati rice", "jasmine rice"],
    "pasta": ["pasta", "spaghetti", "penne", "macaroni", "fettuccine", "rigatoni"]
}

DISPLAY_NAME_MAP = {
    "paneer": "Paneer (Cottage Cheese)",
    "panner": "Paneer (Cottage Cheese)",
    "haldi": "Haldi (Turmeric)",
    "jeera": "Jeera (Cumin)",
    "dhania": "Dhania (Coriander)",
    "adrak": "Adrak (Ginger)",
    "lehsun": "Lehsun (Garlic)",
    "pyaz": "Pyaz (Onion)",
    "pyaaz": "Pyaz (Onion)",
    "aloo": "Aloo (Potato)",
    "tamatar": "Tamatar (Tomato)",
    "palak": "Palak (Spinach)",
    "dal": "Dal (Lentils)",
    "chana": "Chana (Chickpeas)",
    "rajma": "Rajma (Kidney Beans)",
    "dahi": "Dahi (Yogurt / Curd)",
    "ghee": "Ghee (Clarified Butter)",
    "atta": "Atta (Wheat Flour)",
    "besan": "Besan (Gram Flour)",
    "bhindi": "Bhindi (Okra)",
    "gobi": "Gobi (Cauliflower)",
    "matar": "Matar (Green Peas)",
    "hing": "Hing (Asafoetida)"
}

def expand_ingredients(ingredients_list: List[str]) -> str:
    expanded_terms = set()
    all_keys = list(INGREDIENT_EXPANSIONS.keys())
    
    for ing in ingredients_list:
        clean = ing.strip().lower()
        expanded_terms.add(clean)
        
        if clean in INGREDIENT_EXPANSIONS:
            expanded_terms.update(INGREDIENT_EXPANSIONS[clean])
        else:
            matched_substring = False
            for parent, varieties in INGREDIENT_EXPANSIONS.items():
                if parent in clean or clean in parent:
                    expanded_terms.update(varieties)
                    matched_substring = True
            
            if not matched_substring:
                close_matches = difflib.get_close_matches(clean, all_keys, n=1, cutoff=0.65)
                if close_matches:
                    best_match = close_matches[0]
                    expanded_terms.update(INGREDIENT_EXPANSIONS[best_match])

    return " ".join(expanded_terms)

class SearchRequest(BaseModel):
    query: str = Field(..., description="Ingredient or dish search string", example="chicken tomato onion")
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_budget: Optional[bool] = None
    budget_tier: Optional[str] = None
    cuisine: Optional[str] = None
    meal_type: Optional[str] = None
    max_calories: Optional[int] = None
    max_cook_time: Optional[int] = None
    max_prep_time: Optional[int] = None
    difficulty: Optional[str] = None
    min_protein: Optional[int] = None
    limit: Optional[int] = Field(10, ge=1, le=100)

class RecommendRequest(BaseModel):
    recipe_id: Optional[int] = Field(None, description="Optional baseline recipe ID to match against")
    ingredients: Optional[List[str]] = Field(None, description="List of fridge ingredients available")
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_budget: Optional[bool] = None
    budget_tier: Optional[str] = None
    cuisine: Optional[str] = None
    meal_type: Optional[str] = None
    max_calories: Optional[int] = None
    max_cook_time: Optional[int] = None
    difficulty: Optional[str] = None
    limit: Optional[int] = Field(10, ge=1, le=50)

def filter_candidates(
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
) -> List[dict]:
    res = []
    for r in state.recipes:
        if cuisine and cuisine.strip() and cuisine.lower() != "all" and r["cuisine"].lower() != cuisine.strip().lower():
            continue
        if meal_type and meal_type.strip() and meal_type.lower() != "all" and r["meal_type"].lower() != meal_type.strip().lower():
            continue
        if max_calories is not None and max_calories > 0 and r["calories"] > max_calories:
            continue
        if max_cook_time is not None and max_cook_time > 0 and r["cook_time"] > max_cook_time:
            continue
        if max_prep_time is not None and max_prep_time > 0 and r["prep_time"] > max_prep_time:
            continue
        if difficulty and difficulty.strip() and difficulty.lower() != "all" and r["difficulty"].lower() != difficulty.strip().lower():
            continue
        if min_protein is not None and min_protein > 0 and r["protein"] < min_protein:
            continue
        if is_vegan is True and not r["is_vegan"]:
            continue
        if is_vegetarian is True and not r["is_vegetarian"]:
            continue
        if is_budget is True and not r["is_budget"]:
            continue
        if budget_tier and budget_tier.lower() != "all" and r["budget_tier"].lower() != budget_tier.lower():
            continue
        res.append(r)
    return res

def rank_by_query(query: str, candidates: List[dict], top_n: int = 12) -> List[dict]:
    if not query or not query.strip():
        return candidates[:top_n]

    expanded_str = expand_ingredients(query.strip().split())
    query_terms = [clean_text(t) for t in expanded_str.split() if clean_text(t)]
    if not query_terms:
        return candidates[:top_n]

    scored = []
    for r in candidates:
        name_lower = r["recipe_name"].lower()
        ing_lower = r["raw_ingredients"].lower()
        text_lower = f"{name_lower} {ing_lower} {r['cuisine'].lower()} {r['meal_type'].lower()}"

        score = 0.0
        for t in query_terms:
            if t in name_lower:
                score += 4.0
            if t in ing_lower:
                score += 2.0
            elif t in text_lower:
                score += 1.0

        if score > 0:
            pct = min(99.0, round(50.0 + (score / (len(query_terms) * 4.0)) * 49.0, 1))
            item = dict(r)
            item["similarity_score"] = pct
            item["similarity_percent"] = f"{pct}%"
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:top_n]]

def recommend_similar_items(recipe_id: int, candidates: List[dict], top_n: int = 6) -> List[dict]:
    target = state.recipes_by_id.get(recipe_id)
    if not target:
        return []

    target_text = clean_text(f"{target['recipe_name']} {target['raw_ingredients']} {target['cuisine']}")
    target_tokens = set(target_text.split())

    scored = []
    for r in candidates:
        if r["id"] == recipe_id:
            continue
        r_tokens = set(clean_text(f"{r['recipe_name']} {r['raw_ingredients']} {r['cuisine']}").split())
        intersection = target_tokens.intersection(r_tokens)
        if not intersection:
            continue

        score = len(intersection) / float(len(target_tokens.union(r_tokens)))
        pct = min(99.0, round(max(35.0, score * 100.0), 1))
        item = dict(r)
        item["similarity_score"] = pct
        item["similarity_percent"] = f"{pct}%"
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:top_n]]

# --- ENDPOINTS ---

# --- ENDPOINTS ---

@app.get("/api")
def get_root():
    ensure_state_loaded()
    return {
        "status": "online",
        "message": "AI Recipe Builder API is running smoothly",
        "total_recipes": len(state.recipes),
        "engine": "Lightweight In-Memory Search Engine",
        "database": None
    }

@app.get("/recipes")
@app.get("/api/recipes")
def get_recipes(
    page: int = 1,
    limit: int = 12,
    search: Optional[str] = None,
    cuisine: Optional[str] = None,
    meal_type: Optional[str] = None,
    is_vegetarian: Optional[bool] = None,
    is_vegan: Optional[bool] = None,
    is_budget: Optional[bool] = None,
    budget_tier: Optional[str] = None,
    max_calories: Optional[int] = None,
    max_cook_time: Optional[int] = None,
    max_prep_time: Optional[int] = None,
    difficulty: Optional[str] = None,
    min_protein: Optional[int] = None,
    sort_by: Optional[str] = "id"
):
    ensure_state_loaded()
    page = int(page) if page else 1
    limit = int(limit) if limit else 12

    candidates = filter_candidates(
        is_vegetarian=is_vegetarian,
        is_vegan=is_vegan,
        is_budget=is_budget,
        budget_tier=budget_tier,
        cuisine=cuisine,
        meal_type=meal_type,
        max_calories=max_calories,
        max_cook_time=max_cook_time,
        max_prep_time=max_prep_time,
        difficulty=difficulty,
        min_protein=min_protein
    )

    if search and search.strip():
        candidates = rank_by_query(search, candidates, top_n=len(candidates))

    if sort_by == "recipe_name":
        candidates.sort(key=lambda r: r["recipe_name"])
    elif sort_by in ["calories", "cook_time", "prep_time", "protein"]:
        candidates.sort(key=lambda r: r[sort_by])

    total_count = len(candidates)
    total_pages = max(1, (total_count + limit - 1) // limit)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    page_recipes = candidates[start_idx:end_idx]

    return {
        "recipes": page_recipes,
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "total_pages": total_pages
    }

@app.get("/recipe/{recipe_id}")
@app.get("/api/recipe/{recipe_id}")
def get_recipe_by_id(recipe_id: int):
    ensure_state_loaded()
    recipe_data = state.recipes_by_id.get(recipe_id)
    if not recipe_data:
        raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")

    res = dict(recipe_data)
    res["similar_recipes"] = recommend_similar_items(recipe_id, state.recipes, top_n=6)
    return res

@app.post("/search")
@app.post("/api/search")
def search_recipes(payload: SearchRequest):
    ensure_state_loaded()
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Search query must not be empty")

    candidates = filter_candidates(
        is_vegetarian=payload.is_vegetarian,
        is_vegan=payload.is_vegan,
        is_budget=payload.is_budget,
        budget_tier=payload.budget_tier,
        cuisine=payload.cuisine,
        meal_type=payload.meal_type,
        max_calories=payload.max_calories,
        max_cook_time=payload.max_cook_time,
        max_prep_time=payload.max_prep_time,
        difficulty=payload.difficulty,
        min_protein=payload.min_protein
    )

    results = rank_by_query(payload.query, candidates, top_n=payload.limit or 10)
    return {
        "recipes": results,
        "query": payload.query,
        "total": len(results)
    }

@app.post("/recommend")
@app.post("/api/recommend")
def recommend_recipes(payload: RecommendRequest):
    ensure_state_loaded()
    candidates = filter_candidates(
        is_vegetarian=payload.is_vegetarian,
        is_vegan=payload.is_vegan,
        is_budget=payload.is_budget,
        budget_tier=payload.budget_tier,
        cuisine=payload.cuisine,
        meal_type=payload.meal_type,
        max_calories=payload.max_calories,
        max_cook_time=payload.max_cook_time,
        difficulty=payload.difficulty
    )

    if payload.recipe_id is not None:
        results = recommend_similar_items(payload.recipe_id, candidates, top_n=payload.limit or 10)
    elif payload.ingredients and len(payload.ingredients) > 0:
        query_str = " ".join(payload.ingredients)
        results = rank_by_query(query_str, candidates, top_n=payload.limit or 10)
    else:
        raise HTTPException(status_code=400, detail="Please provide either 'recipe_id' or a non-empty 'ingredients' list.")

    return {
        "recipes": results,
        "total": len(results)
    }

@app.get("/cuisines")
@app.get("/api/cuisines")
def get_cuisines():
    ensure_state_loaded()
    counts = {}
    for r in state.recipes:
        c = r["cuisine"]
        counts[c] = counts.get(c, 0) + 1
    cuisines_list = [{"name": c, "count": cnt} for c, cnt in counts.items()]
    return {"cuisines": cuisines_list}

@app.get("/meal-types")
@app.get("/api/meal-types")
def get_meal_types():
    ensure_state_loaded()
    counts = {}
    for r in state.recipes:
        m = r["meal_type"]
        counts[m] = counts.get(m, 0) + 1
    meal_types_list = [{"name": m, "count": cnt} for m, cnt in counts.items()]
    return {"meal_types": meal_types_list}

@app.get("/ingredients/autocomplete")
@app.get("/api/ingredients/autocomplete")
def autocomplete_ingredients(q: str = Query("", min_length=1)):
    ensure_state_loaded()
    if not q or not q.strip():
        return {"ingredients": []}

    query_lower = q.lower().strip()
    matches = []

    matched_key = None
    if query_lower in INGREDIENT_EXPANSIONS:
        matched_key = query_lower
    else:
        close = difflib.get_close_matches(query_lower, list(INGREDIENT_EXPANSIONS.keys()), n=1, cutoff=0.65)
        if close:
            matched_key = close[0]

    if matched_key:
        display_label = DISPLAY_NAME_MAP.get(matched_key, matched_key.capitalize())
        matches.append(display_label)

    for item in state.unique_ingredients:
        ing_name = item["ingredient"]
        if query_lower in ing_name.lower() or (matched_key and matched_key in ing_name.lower()):
            if ing_name.capitalize() not in matches and ing_name not in matches:
                matches.append(ing_name)

    return {"ingredients": matches[:15]}

# --- STATIC FILE SERVING FOR FULL-STACK RENDER DEPLOYMENT ---
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))

if os.path.exists(FRONTEND_DIST):
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
