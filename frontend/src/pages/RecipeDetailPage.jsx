import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Clock, Flame, Utensils, ChefHat, Users, CheckCircle2, Circle, ArrowLeft, Sparkles, Printer, Leaf } from 'lucide-react';
import NutritionBadge from '../components/NutritionBadge';
import ServingScaler from '../components/ServingScaler';
import RecipeCard from '../components/RecipeCard';
import { getRecipeById } from '../api/client';

export default function RecipeDetailPage() {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [currentServings, setCurrentServings] = useState(4);
  const [checkedIngredients, setCheckedIngredients] = useState({});
  const [checkedSteps, setCheckedSteps] = useState({});

  useEffect(() => {
    async function fetchRecipe() {
      try {
        setLoading(true);
        setError(null);
        const data = await getRecipeById(id);
        setRecipe(data);
        setCurrentServings(data.servings || 4);
        setCheckedIngredients({});
        setCheckedSteps({});
      } catch (err) {
        console.error('Failed loading recipe detail:', err);
        setError('Recipe not found or dataset error.');
      } finally {
        setLoading(false);
      }
    }
    fetchRecipe();
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-12 space-y-8 animate-pulse">
        <div className="h-8 w-32 bg-[#F4EFE6] rounded-xl" />
        <div className="h-96 w-full bg-[#F4EFE6] rounded-3xl" />
        <div className="h-40 w-full bg-[#F4EFE6] rounded-2xl" />
      </div>
    );
  }

  if (error || !recipe) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center space-y-4">
        <h2 className="text-2xl font-bold font-serif-warm text-[#231F1D]">Recipe Not Found</h2>
        <p className="text-sm text-[#6E6359] font-medium">{error || "The requested recipe could not be loaded."}</p>
        <Link to="/search" className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#244235] text-white font-bold text-sm shadow-xs">
          <ArrowLeft className="w-4 h-4" /> Return to Catalog
        </Link>
      </div>
    );
  }

  // Parse instructions into step items
  const instructionSteps = recipe.instructions
    .split(/\.\s+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 2);

  const scaleFactor = currentServings / (recipe.servings || 4);

  const toggleIngredient = (idx) => {
    setCheckedIngredients((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const toggleStep = (idx) => {
    setCheckedSteps((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10 bg-[#FAF7F2]">
      {/* Back button & controls */}
      <div className="flex items-center justify-between">
        <Link
          to="/search"
          className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white text-[#231F1D] hover:text-[#244235] text-xs font-bold border border-[#E3DAC9] shadow-xs transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Search
        </Link>

        <div className="flex items-center gap-2">
          <button
            onClick={handlePrint}
            className="p-2 rounded-xl bg-white text-[#231F1D] hover:text-[#244235] border border-[#E3DAC9] text-xs font-bold flex items-center gap-1.5 shadow-xs"
            title="Print Recipe"
          >
            <Printer className="w-4 h-4" /> Print
          </button>
        </div>
      </div>

      {/* Hero Showcase Header Banner */}
      <div className="bg-white rounded-3xl overflow-hidden border border-[#E3DAC9] p-8 sm:p-12 shadow-xs relative space-y-6">
        {/* Top Badges */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#F4EFE6] text-[#244235] border border-[#E5DCCB]">
              <Utensils className="w-3.5 h-3.5 text-[#244235]" />
              {recipe.cuisine} Cuisine
            </span>
            <span className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#FDF4E7] text-[#9A4918] border border-[#F6D9B6]">
              <ChefHat className="w-3.5 h-3.5 text-[#9A4918]" />
              {recipe.meal_type}
            </span>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            <span className="px-3 py-1.5 rounded-full text-xs font-bold bg-[#FAF7F2] text-[#231F1D] border border-[#E3DAC9]">
              {recipe.difficulty} Difficulty
            </span>
            {recipe.is_vegan ? (
              <span className="px-3 py-1.5 rounded-full text-xs font-bold bg-[#F4EFE6] text-[#244235] border border-[#E5DCCB] flex items-center gap-1">
                <Leaf className="w-3.5 h-3.5 text-[#244235]" /> Vegan
              </span>
            ) : recipe.is_vegetarian ? (
              <span className="px-3 py-1.5 rounded-full text-xs font-bold bg-[#F4EFE6] text-[#244235] border border-[#E5DCCB] flex items-center gap-1">
                <Leaf className="w-3.5 h-3.5 text-[#244235]" /> Vegetarian
              </span>
            ) : null}
          </div>
        </div>

        {/* Title */}
        <h1 className="text-3xl sm:text-5xl font-bold font-serif-warm text-[#231F1D] leading-tight">
          {recipe.recipe_name}
        </h1>

        {/* Key Metrics Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 divide-y sm:divide-y-0 sm:divide-x divide-[#EAE3D2] bg-[#FAF7F2] p-4 border-t border-[#E3DAC9] text-center">
          <div className="p-3">
            <div className="text-xs text-[#6E6359] font-bold flex items-center justify-center gap-1">
              <Clock className="w-3.5 h-3.5 text-[#244235]" /> Prep Time
            </div>
            <div className="text-base font-bold text-[#231F1D]">{recipe.prep_time} mins</div>
          </div>

          <div className="p-3">
            <div className="text-xs text-[#6E6359] font-bold flex items-center justify-center gap-1">
              <Clock className="w-3.5 h-3.5 text-[#244235]" /> Cook Time
            </div>
            <div className="text-base font-bold text-[#231F1D]">{recipe.cook_time} mins</div>
          </div>

          <div className="p-3">
            <div className="text-xs text-[#6E6359] font-bold flex items-center justify-center gap-1">
              <Flame className="w-3.5 h-3.5 text-[#C2593F]" /> Calories
            </div>
            <div className="text-base font-bold text-[#231F1D]">{Math.round(recipe.calories * scaleFactor)} kcal</div>
          </div>

          <div className="p-3">
            <div className="text-xs text-[#6E6359] font-bold flex items-center justify-center gap-1">
              <Users className="w-3.5 h-3.5 text-[#244235]" /> Servings
            </div>
            <div className="text-base font-bold text-[#231F1D]">{currentServings} people</div>
          </div>
        </div>
      </div>

      {/* Serving Scaler */}
      <ServingScaler
        baseServings={recipe.servings}
        currentServings={currentServings}
        onChange={(s) => setCurrentServings(s)}
      />

      {/* Nutrition Breakdown */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold font-serif-warm text-[#231F1D] flex items-center gap-2">
          <Flame className="w-5 h-5 text-[#C2593F]" /> Macro Nutrition Breakdown
        </h3>
        <NutritionBadge
          calories={Math.round(recipe.calories * scaleFactor)}
          protein={Math.round(recipe.protein * scaleFactor)}
          carbs={Math.round(recipe.carbs * scaleFactor)}
          fat={Math.round(recipe.fat * scaleFactor)}
        />
      </div>

      {/* Ingredients & Instructions Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Ingredients Column */}
        <div className="lg:col-span-1 bg-white p-6 rounded-3xl border border-[#E3DAC9] shadow-xs space-y-4 h-fit">
          <div className="flex items-center justify-between border-b border-[#EAE3D2] pb-3">
            <h3 className="font-bold font-serif-warm text-[#231F1D] text-lg flex items-center gap-2">
              <Utensils className="w-5 h-5 text-[#244235]" /> Ingredients
            </h3>
            <span className="text-xs text-[#244235] font-bold">{recipe.ingredients.length} items</span>
          </div>

          <p className="text-xs text-[#6E6359] font-medium">Click to check off ingredients as you prepare them:</p>

          <ul className="space-y-2.5">
            {recipe.ingredients.map((ing, idx) => {
              const isDone = checkedIngredients[idx];
              return (
                <li
                  key={idx}
                  onClick={() => toggleIngredient(idx)}
                  className={`p-3 rounded-xl border transition-all cursor-pointer flex items-start gap-3 text-xs ${
                    isDone
                      ? 'bg-[#F4EFE6] border-[#E3DAC9] text-[#8C7B6B] line-through'
                      : 'bg-[#FAF7F2] border-[#E3DAC9] text-[#231F1D] hover:border-[#244235]'
                  }`}
                >
                  {isDone ? (
                    <CheckCircle2 className="w-4 h-4 text-[#244235] shrink-0 mt-0.5" />
                  ) : (
                    <Circle className="w-4 h-4 text-[#8C7B6B] shrink-0 mt-0.5" />
                  )}
                  <span className="leading-relaxed font-bold">{ing}</span>
                </li>
              );
            })}
          </ul>
        </div>

        {/* Instructions Column */}
        <div className="lg:col-span-2 bg-white p-6 sm:p-8 rounded-3xl border border-[#E3DAC9] shadow-xs space-y-6">
          <div className="flex items-center justify-between border-b border-[#EAE3D2] pb-4">
            <h3 className="font-bold font-serif-warm text-[#231F1D] text-xl flex items-center gap-2 font-sans">
              <ChefHat className="w-6 h-6 text-[#244235]" /> Step-by-Step Instructions
            </h3>
            <span className="text-xs text-[#6E6359] font-bold">{instructionSteps.length} steps</span>
          </div>

          <div className="space-y-4">
            {instructionSteps.map((step, idx) => {
              const isStepDone = checkedSteps[idx];
              return (
                <div
                  key={idx}
                  onClick={() => toggleStep(idx)}
                  className={`p-5 rounded-2xl border transition-all cursor-pointer flex items-start gap-4 ${
                    isStepDone
                      ? 'bg-[#F4EFE6] border-[#E3DAC9] text-[#8C7B6B]'
                      : 'bg-[#FAF7F2] border-[#E3DAC9] text-[#231F1D] hover:border-[#244235]'
                  }`}
                >
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center font-bold text-xs shrink-0 ${
                    isStepDone
                      ? 'bg-[#E3DAC9] text-[#231F1D]'
                      : 'bg-[#244235] text-white shadow-xs'
                  }`}>
                    {idx + 1}
                  </div>
                  <div className="flex-grow">
                    <p className={`text-sm leading-relaxed ${isStepDone ? 'line-through text-[#8C7B6B]' : 'text-[#231F1D] font-medium'}`}>
                      {step}{step.endsWith('.') ? '' : '.'}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Similar Recipes */}
      {recipe.similar_recipes && recipe.similar_recipes.length > 0 && (
        <div className="space-y-6 pt-6">
          <div className="flex items-center justify-between border-b border-[#EAE3D2] pb-4">
            <div>
              <h3 className="text-xl font-bold font-serif-warm text-[#231F1D] flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-[#C2593F]" /> You Might Also Like
              </h3>
              <p className="text-xs text-[#6E6359] font-medium">Recipes with similar ingredients and flavor profiles</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {recipe.similar_recipes.map((sim) => (
              <RecipeCard key={sim.id} recipe={sim} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
