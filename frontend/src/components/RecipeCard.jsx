import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, Flame, Utensils, ArrowRight, Leaf, Sparkles, CircleDot } from 'lucide-react';

export default function RecipeCard({ recipe }) {
  if (!recipe) return null;

  const mealTypeColors = {
    Breakfast: "bg-[#FEF3C7] text-[#92400E] border-[#FDE68A]",
    Lunch: "bg-[#D1FAE5] text-[#065F46] border-[#A7F3D0]",
    Dinner: "bg-[#E0E7FF] text-[#3730A3] border-[#C7D2FE]",
    Dessert: "bg-[#FFE4E6] text-[#9F1239] border-[#FECDD3]",
    Beverage: "bg-[#F3E8FF] text-[#6B21A8] border-[#E9D5FF]",
    Snack: "bg-[#FFEDD5] text-[#9A3412] border-[#FED7AA]"
  };

  const mealType = recipe.meal_type || 'Dinner';
  const mealBadgeColor = mealTypeColors[mealType] || "bg-[#F4EFE6] text-[#244235] border-[#E5DCCB]";

  const totalTime = (recipe.prep_time || 15) + (recipe.cook_time || 25);
  
  // Strict check for actual budget friendly recipes
  const isBudget = recipe.is_budget === true || (typeof recipe.cost_per_serving === 'number' && recipe.cost_per_serving <= 2.75);

  return (
    <div className="group bg-white rounded-2xl overflow-hidden flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 border border-[#E3DAC9] p-6 shadow-xs hover:shadow-md hover:border-[#244235] relative">
      <div className="space-y-4">
        
        {/* Fixed Top Row: Green Vegetarian OR Red Non-Veg Badge on Left, Color-coded Meal Type Badge on Right */}
        <div className="flex items-center justify-between gap-2 w-full">
          {recipe.is_vegetarian ? (
            <span className="px-2.5 py-1 rounded-full bg-[#DCFCE7] text-[#15803D] border border-[#86EFAC] text-xs font-bold flex items-center gap-1.5 shadow-2xs">
              <Leaf className="w-3.5 h-3.5 text-[#15803D]" />
              <span>Vegetarian</span>
            </span>
          ) : (
            <span className="px-2.5 py-1 rounded-full bg-[#FEE2E2] text-[#B91C1C] border border-[#FCA5A5] text-xs font-bold flex items-center gap-1.5 shadow-2xs">
              <CircleDot className="w-3.5 h-3.5 text-[#B91C1C]" />
              <span>Non-Veg</span>
            </span>
          )}

          <span className={`px-3 py-1 rounded-full text-xs font-bold border shadow-2xs ${mealBadgeColor}`}>
            {mealType}
          </span>
        </div>

        {/* Recipe Title (Full text without truncation) */}
        <h3 className="text-lg sm:text-xl font-bold font-serif-warm text-[#231F1D] group-hover:text-[#244235] transition-colors leading-snug">
          {recipe.recipe_name}
        </h3>

        {/* Cuisine Badge (Positioned BELOW the Recipe Title) */}
        <div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#F4EFE6] border border-[#E5DCCB] text-[#244235] text-xs font-bold">
            <Utensils className="w-3.5 h-3.5 text-[#244235]" />
            <span>{recipe.cuisine || 'American'} Cuisine</span>
          </span>
        </div>

        {/* Metrics Grid (Cook Time & Calories) */}
        <div className="grid grid-cols-2 gap-2.5 text-xs font-semibold text-[#5C5248]">
          <div className="bg-[#FAF7F2] p-2.5 rounded-xl border border-[#EBE4D5] flex items-center gap-2">
            <Clock className="w-4 h-4 text-[#244235]" />
            <span>{totalTime} mins</span>
          </div>
          <div className="bg-[#FAF7F2] p-2.5 rounded-xl border border-[#EBE4D5] flex items-center gap-2">
            <Flame className="w-4 h-4 text-[#9A4918]" />
            <span>{recipe.calories || 400} kcal</span>
          </div>
        </div>
      </div>

      {/* Footer Action Bar: Only show Budget badge if ACTUAL budget friendly, View Recipe link on Right */}
      <div className="pt-4 mt-5 border-t border-[#EBE4D5] flex items-center justify-between min-h-[42px]">
        {isBudget ? (
          <span className="text-xs font-bold text-[#15803D] bg-[#DCFCE7] px-2.5 py-1 rounded-lg border border-[#86EFAC] flex items-center gap-1">
            <span>💲</span> Budget Friendly
          </span>
        ) : (
          <div />
        )}
        <Link
          to={`/recipe/${recipe.id}`}
          className="inline-flex items-center gap-1.5 text-xs font-bold text-[#244235] hover:text-[#1B3329] group-hover:translate-x-1 transition-transform ml-auto"
        >
          <span>View Recipe</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
}
