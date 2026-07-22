import re
import pandas as pd

NON_VEGETARIAN_KEYWORDS = {
    "chicken", "beef", "pork", "steak", "bacon", "turkey", "lamb", "duck",
    "fish", "salmon", "tuna", "shrimp", "prawn", "crab", "lobster", "anchovy",
    "anchovies", "prosciutto", "pancetta", "sausage", "pepperoni", "ham", "veal",
    "halibut", "cod", "clam", "mussel", "squid", "calamari", "scallop", "lard",
    "brisket", "briskets", "ribs", "short ribs", "meat", "meatball", "meatballs",
    "mutton", "venison", "bison", "tallow", "suet", "tripe", "charcuterie",
    "pastrami", "salami", "bologna", "chorizo", "mortadella", "gelatin", "foie gras",
    "poultry", "ox", "oyster", "oysters", "octopus", "eel", "tilapia", "trout",
    "sardine", "sardines", "flounder", "mahi", "snapper", "catfish", "haddock",
    "swordfish", "caviar", "crawfish", "crayfish", "pork belly", "sirloin",
    "tenderloin", "ribeye", "flank", "skirt steak", "ground beef", "ground meat",
    "ground pork", "ground lamb", "ground turkey", "pork chop", "pork chops",
    "lamb chop", "lamb chops"
}

NON_VEGAN_KEYWORDS = NON_VEGETARIAN_KEYWORDS.union({
    "egg", "eggs", "egg white", "egg yolk", "butter", "cheese", "milk", "cream",
    "yogurt", "parmesan", "mozzarella", "cheddar", "ricotta", "ghee", "honey",
    "mayonnaise", "half-and-half", "heavy cream", "sour cream", "condensed milk"
})

def clean_text(text: str) -> str:
    """Normalize text: lowercases, removes punctuation & non-alpha characters, trims spaces."""
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Replace punctuation and special characters with spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove digits
    text = re.sub(r'\d+', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_ingredients(ingredients_str: str) -> list[str]:
    """Splits raw ingredients string into clean list of ingredient strings."""
    if not isinstance(ingredients_str, str):
        return []
    raw_items = ingredients_str.split(',')
    cleaned_items = [clean_text(item) for item in raw_items if item.strip()]
    return [item for item in cleaned_items if item]

def create_combined_features(df: pd.DataFrame) -> pd.Series:
    """
    Create combined feature text using:
    Recipe Name + Ingredients + Cuisine + Meal Type
    """
    names = df['Recipe Name'].fillna('').apply(clean_text)
    ingredients = df['Ingredients'].fillna('').apply(clean_text)
    cuisines = df['Cuisine'].fillna('').apply(clean_text)
    meal_types = df['Meal Type'].fillna('').apply(clean_text)
    
    return names + " " + ingredients + " " + cuisines + " " + meal_types

def check_vegetarian(ingredients_text: str, recipe_name: str = "") -> bool:
    combined = (str(recipe_name) + " " + str(ingredients_text)).lower()
    return not any(w in combined for w in NON_VEGETARIAN_KEYWORDS)

def check_vegan(ingredients_text: str, recipe_name: str = "") -> bool:
    combined = (str(recipe_name) + " " + str(ingredients_text)).lower()
    return not any(w in combined for w in NON_VEGAN_KEYWORDS)
