import os
import csv
import sqlite3
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "recipes.csv")
DB_PATH = os.path.join(BASE_DIR, "recipes.db")
API_DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "api", "recipes.db"))

def convert_csv_to_sqlite():
    if not os.path.exists(CSV_PATH):
        alt_csv = os.path.abspath(os.path.join(BASE_DIR, "..", "api", "recipes.csv"))
        if os.path.exists(alt_csv):
            source_csv = alt_csv
        else:
            raise FileNotFoundError(f"Cannot find recipes.csv at {CSV_PATH} or {alt_csv}")
    else:
        source_csv = CSV_PATH

    print(f"Reading CSV from {source_csv}...")
    
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception as e:
            print(f"Warning: could not remove existing {DB_PATH}: {e}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_name TEXT NOT NULL,
        ingredients TEXT,
        instructions TEXT,
        cuisine TEXT,
        meal_type TEXT,
        prep_time INTEGER,
        cook_time INTEGER,
        calories INTEGER,
        protein INTEGER,
        carbs INTEGER,
        fat INTEGER,
        difficulty TEXT,
        servings INTEGER,
        image_url TEXT
    );
    """)

    with open(source_csv, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        rows_to_insert = []
        for row in reader:
            title = (row.get("Recipe Name") or row.get("name") or "").strip()
            ingredients = (row.get("Ingredients") or row.get("ing") or "").strip()
            instructions = (row.get("Instructions") or row.get("inst") or "").strip()
            cuisine = (row.get("Cuisine") or row.get("cuis") or "American").strip()
            meal_type = (row.get("Meal Type") or row.get("meal") or "Dinner").strip()

            try: prep_time = int(row.get("Prep Time") or row.get("prep") or 15)
            except (ValueError, TypeError): prep_time = 15

            try: cook_time = int(row.get("Cook Time") or row.get("cook") or 30)
            except (ValueError, TypeError): cook_time = 30

            try: calories = int(row.get("Calories") or row.get("cal") or 400)
            except (ValueError, TypeError): calories = 400

            try: protein = int(row.get("Protein") or row.get("prot") or 20)
            except (ValueError, TypeError): protein = 20

            try: carbs = int(row.get("Carbs") or row.get("carb") or 40)
            except (ValueError, TypeError): carbs = 40

            try: fat = int(row.get("Fat") or row.get("fat") or 15)
            except (ValueError, TypeError): fat = 15

            difficulty = (row.get("Difficulty") or row.get("diff") or "Medium").strip()

            try: servings = int(row.get("Servings") or row.get("serv") or 4)
            except (ValueError, TypeError): servings = 4

            image_url = (row.get("Image URL") or "").strip()

            rows_to_insert.append((
                title, ingredients, instructions, cuisine, meal_type,
                prep_time, cook_time, calories, protein, carbs, fat,
                difficulty, servings, image_url
            ))

    cursor.executemany("""
    INSERT INTO recipes (
        recipe_name, ingredients, instructions, cuisine, meal_type,
        prep_time, cook_time, calories, protein, carbs, fat,
        difficulty, servings, image_url
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, rows_to_insert)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_meal_type ON recipes(meal_type);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_recipes_difficulty ON recipes(difficulty);")

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM recipes;")
    total_count = cursor.fetchone()[0]
    conn.close()

    print(f"Successfully converted CSV data to SQLite database at {DB_PATH} with {total_count} records.")

    # Copy to api/ if api directory exists
    api_dir = os.path.dirname(API_DB_PATH)
    if os.path.exists(api_dir):
        shutil.copy2(DB_PATH, API_DB_PATH)
        print(f"Copied database to {API_DB_PATH}")

if __name__ == "__main__":
    convert_csv_to_sqlite()
