import os
import json
import difflib
import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List

from preprocess import clean_text
from recommender import TFIDFRecommender
from utils import filter_recipes_dataframe, format_recipe_dict

CSV_PATH = os.path.join(os.path.dirname(__file__), "recipes.csv")
UNIQUE_INGREDIENTS_PATH = os.path.join(os.path.dirname(__file__), "unique_ingredients.json")

# In-Memory Global State Container
class AppState:
    df: Optional[pd.DataFrame] = None
    recommender: Optional[TFIDFRecommender] = None
    unique_ingredients: List[dict] = []

state = AppState()

def ensure_state_loaded():
    """
    Ensures dataset, recommender, and unique ingredients are loaded into memory.
    Safe for both serverless cold starts and Uvicorn server startup.
    """
    if state.df is not None:
        return

    print("Initializing AI Recipe Builder Backend...")
    if not os.path.exists(CSV_PATH):
        raise RuntimeError(f"Permanent dataset missing at {CSV_PATH}. Run prepare_dataset.py first!")

    print(f"Loading {CSV_PATH} into pandas DataFrame...")
    df = pd.read_csv(CSV_PATH)
    
    # Fill missing values
    df['Recipe Name'] = df['Recipe Name'].fillna('Untitled Recipe')
    df['Ingredients'] = df['Ingredients'].fillna('')
    df['Instructions'] = df['Instructions'].fillna('')
    df['Cuisine'] = df['Cuisine'].fillna('American')
    df['Meal Type'] = df['Meal Type'].fillna('Dinner')
    df['Prep Time'] = df['Prep Time'].fillna(15).astype(int)
    df['Cook Time'] = df['Cook Time'].fillna(30).astype(int)
    df['Calories'] = df['Calories'].fillna(400).astype(int)
    df['Protein'] = df['Protein'].fillna(20).astype(int)
    df['Carbs'] = df['Carbs'].fillna(40).astype(int)
    df['Fat'] = df['Fat'].fillna(15).astype(int)
    df['Difficulty'] = df['Difficulty'].fillna('Medium')
    df['Servings'] = df['Servings'].fillna(4).astype(int)
    df['Image URL'] = df['Image URL'].fillna('')

    state.df = df
    print(f"Loaded {len(df)} recipes into RAM.")

    # Train or load TF-IDF model
    recommender = TFIDFRecommender()
    recommender.load_or_train(df)
    state.recommender = recommender

    # Load unique ingredients list if available
    if os.path.exists(UNIQUE_INGREDIENTS_PATH):
        try:
            with open(UNIQUE_INGREDIENTS_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                state.unique_ingredients = data.get("ingredients", [])
                print(f"Loaded {len(state.unique_ingredients)} unique ingredient suggestions for autocomplete.")
        except Exception as e:
            print(f"Warning loading unique_ingredients.json: {e}")

    print("Backend initialization complete! Ready to accept requests.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for ASGI servers."""
    ensure_state_loaded()
    yield
    print("Shutting down AI Recipe Builder Backend...")

app = FastAPI(
    title="AI Recipe Builder API",
    description="Production Machine Learning Recipe Search & Recommendation API powered by TF-IDF & Cosine Similarity",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PYDANTIC SCHEMAS ---

INGREDIENT_EXPANSIONS = {
    # Hindi & Indian Synonyms with common typos & variants
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

    # Global Staples & Varieties
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
    """Expand generic tags & Hindi aliases with fuzzy typo fallback for broader TF-IDF matching."""
    expanded_terms = set()
    all_keys = list(INGREDIENT_EXPANSIONS.keys())
    
    for ing in ingredients_list:
        clean = ing.strip().lower()
        expanded_terms.add(clean)
        
        # 1. Direct dictionary match
        if clean in INGREDIENT_EXPANSIONS:
            expanded_terms.update(INGREDIENT_EXPANSIONS[clean])
        else:
            # 2. Substring check
            matched_substring = False
            for parent, varieties in INGREDIENT_EXPANSIONS.items():
                if parent in clean or clean in parent:
                    expanded_terms.update(varieties)
                    matched_substring = True
            
            # 3. Fuzzy match for typos e.g., 'panner' -> 'paneer'
            if not matched_substring:
                close_matches = difflib.get_close_matches(clean, all_keys, n=1, cutoff=0.65)
                if close_matches:
                    best_match = close_matches[0]
                    expanded_terms.update(INGREDIENT_EXPANSIONS[best_match])

    return " ".join(expanded_terms)

class SearchRequest(BaseModel):
    query: str = Field(..., description="Ingredient or dish search string e.g. 'chicken tomato garlic'", example="chicken tomato onion")
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

# --- ENDPOINTS ---

@app.get("/")
def get_root():
    """System health check and dataset metrics."""
    ensure_state_loaded()
    if state.df is None:
        raise HTTPException(status_code=500, detail="Server model state uninitialized")
    return {
        "status": "online",
        "message": "AI Recipe Builder API is running smoothly",
        "total_recipes": len(state.df),
        "engine": "TF-IDF Vectorizer + Cosine Similarity",
        "database": None
    }

@app.get("/recipes")
def get_recipes(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100),
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
    sort_by: Optional[str] = Query("id", enum=["id", "recipe_name", "calories", "cook_time", "prep_time", "protein"])
):
    """Retrieve paginated & filtered list of recipes."""
    ensure_state_loaded()
    if state.df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    df = state.df

    # 1. Filter candidates
    matching_indices = filter_recipes_dataframe(
        df,
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

    # 2. Text Search if provided
    if search and search.strip():
        search_terms = search.strip().split()
        expanded_query = expand_ingredients(search_terms)
        scored_candidates = state.recommender.search_query(expanded_query, df, top_n=len(matching_indices), candidate_indices=matching_indices)
        matching_indices = [idx for idx, _ in scored_candidates]
        score_dict = {idx: score for idx, score in scored_candidates}
    else:
        score_dict = {}

    # 3. Sorting
    sub_df = df.loc[matching_indices].copy()
    if sort_by == "recipe_name":
        sub_df = sub_df.sort_values(by="Recipe Name")
    elif sort_by in ["calories", "cook_time", "prep_time", "protein"]:
        col_map = {"calories": "Calories", "cook_time": "Cook Time", "prep_time": "Prep Time", "protein": "Protein"}
        sub_df = sub_df.sort_values(by=col_map[sort_by])

    sorted_indices = sub_df.index.tolist()

    # 4. Pagination
    total_count = len(sorted_indices)
    total_pages = max(1, (total_count + limit - 1) // limit)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    page_indices = sorted_indices[start_idx:end_idx]

    recipes = [
        format_recipe_dict(df.loc[idx], idx, score_dict.get(idx))
        for idx in page_indices
    ]

    return {
        "recipes": recipes,
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "total_pages": total_pages
    }


@app.get("/recipe/{recipe_id}")
def get_recipe_by_id(recipe_id: int):
    """Retrieve details for a single recipe by ID along with AI similar recommendations."""
    ensure_state_loaded()
    if state.df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    if recipe_id < 0 or recipe_id >= len(state.df):
        raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")

    row = state.df.loc[recipe_id]
    recipe_data = format_recipe_dict(row, recipe_id)

    # Get top 6 similar recipes using ML model
    similar_tuples = state.recommender.recommend_similar(recipe_id, state.df, top_n=6)
    similar_recipes = [
        format_recipe_dict(state.df.loc[idx], idx, similarity_score=score)
        for idx, score in similar_tuples
    ]

    recipe_data["similar_recipes"] = similar_recipes
    return recipe_data

@app.post("/search")
def search_recipes(payload: SearchRequest):
    """
    Search recipes based on ingredient/dish text query and optional filters.
    Returns TF-IDF ranked recipes with similarity match scores.
    """
    ensure_state_loaded()
    if state.df is None or state.recommender is None:
        raise HTTPException(status_code=500, detail="Search engine not ready")

    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Search query must not be empty")

    df = state.df

    matching_indices = filter_recipes_dataframe(
        df,
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

    if not matching_indices:
        return {"recipes": [], "query": payload.query, "total": 0}

    search_terms = payload.query.strip().split()
    expanded_query = expand_ingredients(search_terms)

    scored_candidates = state.recommender.search_query(
        expanded_query,
        df,
        top_n=payload.limit or 10,
        candidate_indices=matching_indices
    )

    results = [
        format_recipe_dict(df.loc[idx], idx, similarity_score=score)
        for idx, score in scored_candidates
    ]

    return {
        "recipes": results,
        "query": payload.query,
        "total": len(results)
    }

@app.post("/recommend")
def recommend_recipes(payload: RecommendRequest):
    """
    Generate AI recipe recommendations based on:
    - User input ingredient list e.g. ["chicken", "garlic", "tomato"]
    - OR an existing recipe_id
    """
    ensure_state_loaded()
    if state.df is None or state.recommender is None:
        raise HTTPException(status_code=500, detail="Recommendation engine not ready")

    df = state.df

    # 1. Filter indices
    matching_indices = filter_recipes_dataframe(
        df,
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

    scored_candidates = []

    if payload.recipe_id is not None and 0 <= payload.recipe_id < len(df):
        scored_candidates = state.recommender.recommend_similar(
            payload.recipe_id,
            df,
            top_n=payload.limit or 10,
            candidate_indices=matching_indices
        )
    elif payload.ingredients and len(payload.ingredients) > 0:
        query_str = expand_ingredients(payload.ingredients)
        scored_candidates = state.recommender.search_query(
            query_str,
            df,
            top_n=payload.limit or 10,
            candidate_indices=matching_indices
        )
    else:
        raise HTTPException(status_code=400, detail="Please provide either 'recipe_id' or a non-empty 'ingredients' list.")

    results = [
        format_recipe_dict(df.loc[idx], idx, similarity_score=score)
        for idx, score in scored_candidates
    ]

    return {
        "recipes": results,
        "total": len(results)
    }

@app.get("/cuisines")
def get_cuisines():
    """Returns unique cuisines and recipe count breakdown."""
    ensure_state_loaded()
    if state.df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    counts = state.df['Cuisine'].value_counts().to_dict()
    cuisines_list = [{"name": c, "count": int(cnt)} for c, cnt in counts.items()]
    return {"cuisines": cuisines_list}

@app.get("/meal-types")
def get_meal_types():
    """Returns unique meal types and recipe count breakdown."""
    ensure_state_loaded()
    if state.df is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")

    counts = state.df['Meal Type'].value_counts().to_dict()
    meal_types_list = [{"name": m, "count": int(cnt)} for m, cnt in counts.items()]
    return {"meal_types": meal_types_list}

@app.get("/ingredients/autocomplete")
def autocomplete_ingredients(q: str = Query("", min_length=1)):
    """Search unique ingredients for live multi-select autocompletion with Hindi display tags and fuzzy matching."""
    ensure_state_loaded()
    if not q or not q.strip():
        return {"ingredients": []}

    query_lower = q.lower().strip()
    matches = []

    # 1. Direct or fuzzy lookup in DISPLAY_NAME_MAP / INGREDIENT_EXPANSIONS
    matched_key = None
    if query_lower in INGREDIENT_EXPANSIONS:
        matched_key = query_lower
    else:
        # Check fuzzy match
        close = difflib.get_close_matches(query_lower, list(INGREDIENT_EXPANSIONS.keys()), n=1, cutoff=0.65)
        if close:
            matched_key = close[0]

    if matched_key:
        display_label = DISPLAY_NAME_MAP.get(matched_key, matched_key.capitalize())
        matches.append(display_label)

    # 2. Gather matching dataset unique ingredients
    for item in state.unique_ingredients:
        ing_name = item["ingredient"]
        if query_lower in ing_name.lower() or (matched_key and matched_key in ing_name.lower()):
            if ing_name.capitalize() not in matches and ing_name not in matches:
                matches.append(ing_name)

    return {"ingredients": matches[:15]}

