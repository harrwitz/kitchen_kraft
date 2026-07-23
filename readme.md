live demo:https://ai-recipe-generator-2cybt6foz-harrwitzs-projects.vercel.app/search
# AI Recipe Builder 🥗

A production-quality, high-performance **AI Recipe Builder & Search Engine** web application built with **FastAPI, Pandas, Scikit-Learn (TF-IDF + Cosine Similarity), React 18, Vite, and Tailwind CSS**.

> 💡 **Architectural Contract**: This project **does not use any external database** (MySQL, PostgreSQL, MongoDB, SQLite, Firebase, etc.) nor **any LLM APIs or Cloud AI services**. The entire application operates strictly over an immutable, read-only 13,500+ recipe dataset (`backend/recipes.csv`), loading TF-IDF matrix features once into memory on startup for sub-millisecond similarity lookups.

---

## 🌟 Key Features

- **Sub-Millisecond TF-IDF Vector Search**: Search over 13,500+ culinary recipes by free-text ingredients or dish terms (e.g. `"chicken tomato onion garlic"`) with relevance scores.
- **Smart Fridge & Pantry Recommender**: Select or input available kitchen ingredients to generate recipes ranked by exact **Cosine Similarity Match Percentage** (e.g. `94.2% Match`).
- **Ingredient Analyzer & Deduplicator**: `analyze_ingredients.py` script parses raw recipe ingredients, strips unit measures, normalizes text, deduplicates entries, and produces `unique_ingredients.json` for live multi-select autocompletion.
- **Multi-Factor Filter Panel**: Filter by Vegetarian, Vegan, Cuisine, Meal Type, Cooking Time, Calorie limits, Protein minimums, and Difficulty levels.
- **Dynamic Serving Scaler**: Interactively scale recipe servings (2p, 4p, 6p, 8p+) on the recipe detail page to recalculate nutritional macros and ingredient quantities on the fly.
- **Step-by-Step Cooking Mode**: Interactive ingredient checklist and step-by-step instruction checkmarks.
- **Modern Culinary Glassmorphism UI**: Built with React 18, Vite, Tailwind CSS v3, and Lucide Icons with responsive dark-mode styling.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend API** | Python 3.13 + FastAPI | Asynchronous RESTful API framework |
| **ML Vectorizer** | Scikit-learn (`TfidfVectorizer`) | Unigram/Bigram text vectorization |
| **Recommender Engine** | Scikit-learn (`cosine_similarity`) | Matrix similarity matching |
| **Data Engine** | Pandas & NumPy | In-memory feature dataframe manipulation |
| **Frontend UI** | React 18 + Vite | Single Page Application (SPA) |
| **Styling** | Tailwind CSS v3 | Custom dark-mode glassmorphic design system |
| **HTTP Client** | Axios | Frontend-backend API integration |
| **Dataset Source** | Permanent `recipes.csv` | Read-only dataset (13,493 recipes) |

---

## 📐 Machine Learning & Vector Math Architecture

The recommendation engine uses classical natural language processing and spatial vector math:

1. **Feature Engineering**:
   $$\text{FeatureText} = \text{Recipe Name} \oplus \text{Ingredients} \oplus \text{Cuisine} \oplus \text{Meal Type}$$

2. **TF-IDF Calculation**:
   $$\text{TF-IDF}(t, d, D) = \text{tf}(t, d) \times \log\left(\frac{N}{\text{df}(t)}\right)$$
   *Penalizes generic terms ("water", "salt", "cup") while boosting distinctive ingredients ("miso", "tarragon", "panzanella").*

3. **Cosine Similarity Match**:
   $$\text{Similarity}(q, d) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\| \|\vec{d}\|}$$
   *Scores candidates from $0.0$ to $1.0$, converted to visual percentage match badges.*

---

## 📂 Project Structure

```
recipe-builder/
├── backend/
│   ├── recipes.csv               # Permanent read-only dataset (13,493 rows, 14 columns)
│   ├── analyze_ingredients.py    # Parses & extracts deduplicated unique ingredients
│   ├── unique_ingredients.json   # Extracted 7,500+ unique canonical ingredients catalog
│   ├── prepare_dataset.py        # Dataset cleaner & metadata enricher
│   ├── main.py                   # FastAPI server & lifespan context
│   ├── recommender.py            # TF-IDF Vectorizer & Cosine Similarity recommender class
│   ├── preprocess.py             # Text normalization & vegetarian/vegan classifiers
│   ├── utils.py                  # Filtering, sorting, and JSON formatting helpers
│   ├── requirements.txt          # Backend dependencies
│   ├── model.pkl                 # Cached TF-IDF matrix artifact
│   └── vectorizer.pkl            # Cached fitted TfidfVectorizer artifact
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── index.html
    └── src/
        ├── api/client.js          # Axios REST API client
        ├── components/            # RecipeCard, SearchBar, FilterSidebar, ServingScaler, etc.
        ├── pages/                 # Home, Search, Recommend, RecipeDetail, About, NotFound
        ├── hooks/useDebounce.js   # Input debouncing hook
        ├── App.jsx                # React Router routes
        ├── main.jsx               # Vite entrypoint
        └── index.css              # Tailwind & glassmorphic utility styles
```

---

## 🚀 Installation & Running

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Running the Backend Server

```bash
# Navigate to backend folder
cd backend

# Install Python requirements
pip install -r requirements.txt

# Start FastAPI server using Uvicorn
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Backend will be live at: `http://127.0.0.1:8000`

### 2. Running the Frontend App

```bash
# Navigate to frontend folder
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```

Frontend UI will be live at: `http://127.0.0.1:3000`

---

## 🔌 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | System health check and total recipe metrics |
| `GET` | `/recipes` | Paginated & filtered recipe dataset listing |
| `GET` | `/recipe/{id}` | Recipe detail view + 6 top TF-IDF similar recommendations |
| `POST` | `/search` | TF-IDF text query search with candidate filters |
| `POST` | `/recommend` | Ingredient list fridge matcher ranking recipes by % similarity |
| `GET` | `/cuisines` | Available cuisines breakdown with counts |
| `GET` | `/meal-types` | Available meal types breakdown with counts |
| `GET` | `/ingredients/autocomplete` | Live ingredient autocompletion suggestions |

---

## 🖼️ Application Screenshots

*(Place screenshot images in `frontend/src/assets/` when building production marketing materials)*
- **Home Page**: Hero search bar, quick diet filters, popular cuisine cards.
- **Pantry AI Recommender**: Multi-select ingredient tags and cosine similarity match scores.
- **Recipe Detail Page**: Hero dish showcase, serving multiplier scale, macro breakdown cards.

---

## 🔮 Future Improvements

- **Locally Trained Word2Vec / FastText Embeddings**: Hybrid sparse (TF-IDF) + dense vector semantic matching.
- **Export Shopping List**: Download checked ingredients as PDF or text file.
- **Meal Prep Planner Calendar**: Drag-and-drop weekly meal schedule generator.
