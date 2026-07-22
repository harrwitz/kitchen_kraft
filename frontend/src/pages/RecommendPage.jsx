import React, { useState } from 'react';
import { Sparkles, Refrigerator, RefreshCw } from 'lucide-react';
import IngredientTagsInput from '../components/IngredientTagsInput';
import RecipeCard from '../components/RecipeCard';
import { SkeletonCard } from '../components/SkeletonCard';
import { recommendRecipes } from '../api/client';

export default function RecommendPage() {
  const [ingredients, setIngredients] = useState(['paneer', 'haldi', 'tomato']);
  const [cuisine, setCuisine] = useState('All');
  const [mealType, setMealType] = useState('All');
  const [isVegetarian, setIsVegetarian] = useState(false);
  const [isVegan, setIsVegan] = useState(false);

  const [recommendedRecipes, setRecommendedRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleRecommend = async () => {
    if (ingredients.length === 0) return;

    try {
      setLoading(true);
      setHasSearched(true);

      const res = await recommendRecipes({
        ingredients,
        cuisine: cuisine !== 'All' ? cuisine : undefined,
        meal_type: mealType !== 'All' ? mealType : undefined,
        is_vegetarian: isVegetarian || undefined,
        is_vegan: isVegan || undefined,
        limit: 12
      });

      setRecommendedRecipes(res.recipes || []);
    } catch (err) {
      console.error('Failed generating recommendations:', err);
      setRecommendedRecipes([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10 bg-[#FAF7F2]">
      {/* Header Banner */}
      <div className="bg-white p-8 sm:p-10 rounded-3xl border border-[#E3DAC9] shadow-xs relative overflow-hidden text-center space-y-4">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#F4EFE6] text-[#244235] border border-[#E3DAC9] text-xs font-bold shadow-xs">
          <Refrigerator className="w-4 h-4 text-[#244235]" />
          <span>Fridge Ingredient Matcher</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-bold font-serif-warm text-[#231F1D] tracking-tight">
          What's in Your Kitchen? <span className="text-[#244235]">Find Matching Recipes</span>
        </h1>

        <p className="text-sm text-[#6E6359] max-w-xl mx-auto leading-relaxed font-medium">
          Add items from your pantry. Searches with Hindi terms like <span className="font-bold text-[#244235]">Paneer</span> or <span className="font-bold text-[#9A4918]">Haldi</span> automatically match English counterparts like cottage cheese and turmeric.
        </p>
      </div>

      {/* Input Hub Card */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-[#E3DAC9] shadow-xs space-y-6">
        <div className="space-y-2">
          <label className="text-xs font-bold uppercase tracking-wider text-[#231F1D] flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-[#244235]" /> Available Fridge Ingredients
          </label>
          <IngredientTagsInput ingredients={ingredients} onChange={(tags) => setIngredients(tags)} />
        </div>

        {/* Filters bar */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 pt-2">
          <div>
            <label className="text-xs font-bold text-[#6E6359] block mb-1.5">Cuisine Preference</label>
            <select
              value={cuisine}
              onChange={(e) => setCuisine(e.target.value)}
              className="w-full bg-[#FAF7F2] border border-[#E3DAC9] px-3 py-2 rounded-xl text-xs font-bold text-[#231F1D] focus:outline-none"
            >
              <option value="All">Any Cuisine</option>
              <option value="Indian">Indian</option>
              <option value="Italian">Italian</option>
              <option value="Asian">Asian</option>
              <option value="Mexican">Mexican</option>
              <option value="Mediterranean">Mediterranean</option>
              <option value="American">American</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-bold text-[#6E6359] block mb-1.5">Meal Type</label>
            <select
              value={mealType}
              onChange={(e) => setMealType(e.target.value)}
              className="w-full bg-[#FAF7F2] border border-[#E3DAC9] px-3 py-2 rounded-xl text-xs font-bold text-[#231F1D] focus:outline-none"
            >
              <option value="All">Any Meal</option>
              <option value="Breakfast">Breakfast</option>
              <option value="Lunch">Lunch</option>
              <option value="Dinner">Dinner</option>
              <option value="Dessert">Dessert</option>
              <option value="Appetizer">Appetizer</option>
            </select>
          </div>

          <div className="flex items-end gap-2 sm:col-span-2">
            <button
              type="button"
              onClick={() => setIsVegetarian(!isVegetarian)}
              className={`flex-1 py-2 px-3 rounded-xl border text-xs font-bold transition-all ${
                isVegetarian
                  ? 'bg-[#244235] text-white border-[#244235] shadow-xs'
                  : 'bg-[#FAF7F2] text-[#231F1D] border-[#E3DAC9] hover:bg-[#F4EFE6]'
              }`}
            >
              Vegetarian Only
            </button>

            <button
              type="button"
              onClick={() => setIsVegan(!isVegan)}
              className={`flex-1 py-2 px-3 rounded-xl border text-xs font-bold transition-all ${
                isVegan
                  ? 'bg-[#244235] text-white border-[#244235] shadow-xs'
                  : 'bg-[#FAF7F2] text-[#231F1D] border-[#E3DAC9] hover:bg-[#F4EFE6]'
              }`}
            >
              Vegan Only
            </button>
          </div>
        </div>

        {/* Generate Button */}
        <div className="pt-2 flex justify-center">
          <button
            onClick={handleRecommend}
            disabled={ingredients.length === 0 || loading}
            className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-[#244235] hover:bg-[#1B3228] text-white font-bold text-sm shadow-xs disabled:opacity-40 transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Searching Recipes...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-[#F6D9B6]" />
                <span>Find Recipes</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Recommended Output Grid */}
      <div className="space-y-6">
        <div className="flex items-center justify-between border-b border-[#EAE3D2] pb-4">
          <h2 className="text-xl font-bold font-serif-warm text-[#231F1D] flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-[#244235]" />
            <span>Recommended Kitchen Recipes</span>
          </h2>
          {recommendedRecipes.length > 0 && (
            <span className="text-xs text-[#6E6359] font-bold">
              Found <span className="text-[#244235]">{recommendedRecipes.length}</span> matching recipes
            </span>
          )}
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
          </div>
        ) : recommendedRecipes.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendedRecipes.map((r) => (
              <RecipeCard key={r.id} recipe={r} />
            ))}
          </div>
        ) : hasSearched ? (
          <div className="bg-white p-10 rounded-2xl text-center space-y-3 border border-[#E3DAC9] shadow-xs">
            <p className="text-[#231F1D] font-bold font-serif-warm text-base">No Matching Recipes Found</p>
            <p className="text-xs text-[#6E6359] font-medium">Try adding terms like "paneer", "haldi", "bread", or "chicken".</p>
          </div>
        ) : (
          <div className="bg-white p-12 rounded-3xl text-center space-y-4 border border-[#E3DAC9] shadow-xs">
            <div className="w-16 h-16 rounded-2xl bg-[#F4EFE6] text-[#244235] flex items-center justify-center mx-auto border border-[#E3DAC9]">
              <Sparkles className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold font-serif-warm text-[#231F1D]">Ready to Find Your Next Meal?</h3>
            <p className="text-xs text-[#6E6359] max-w-md mx-auto font-medium leading-relaxed">
              Add your available ingredients above and click "Find Recipes" to generate personalized recommendations!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
