import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, Flame, Utensils, ArrowRight, Leaf, Sparkles } from 'lucide-react';

export default function RecipeCard({ recipe }) {
  if (!recipe) return null;

  const difficultyColors = {
    Easy: "bg-[#F4EFE6] text-[#244235] border-[#E5DCCB]",
    Medium: "bg-[#FDF4E7] text-[#9A4918] border-[#F6D9B6]",
    Hard: "bg-[#FDF0ED] text-[#C2593F] border-[#F5C7BD]"
  };

  const totalTime = (recipe.prep_time || 15) + (recipe.cook_time || 25);

  return (
    <div className="group bg-white rounded-2xl overflow-hidden flex flex-col justify-between transition-all duration-300 hover:-translate-y-1.5 border border-[#E3DAC9] p-6 shadow-xs hover:shadow-md hover:border-[#244235] relative">
      <div className="space-y-4">
        {/* Top Badges Header */}
        <div className="flex items-center justify-between gap-2 flex-wrap">
          <span className="px-3 py-1 rounded-full bg-[#F4EFE6] border border-[#E5DCCB] text-[#244235] text-xs font-bold flex items-center gap-1.5">
            <Utensils className="w-3.5 h-3.5 text-[#244235]" />
            <span>{recipe.cuisine || 'American'}</span>
          </span>

          <div className="flex items-center gap-2">
            {recipe.is_vegetarian && (
              <span className="px-2.5 py-1 rounded-full bg-[#F4EFE6] border border-[#E5DCCB] text-[#244235] text-xs font-bold flex items-center gap-1">
                <Leaf className="w-3 h-3 text-[#244235]" />
                <span>Vegetarian</span>
              </span>
            )}
            <span className={`px-2.5 py-1 rounded-full text-xs font-bold border ${difficultyColors[recipe.difficulty] || difficultyColors.Medium}`}>
              {recipe.meal_type || 'Dinner'}
            </span>
          </div>
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold font-serif-warm text-[#231F1D] group-hover:text-[#244235] transition-colors leading-snug line-clamp-2">
          {recipe.recipe_name}
        </h3>

        {/* Macros & Culinary Specs Pill Grid */}
        <div className="grid grid-cols-2 gap-2.5 text-xs font-semibold text-[#5C5248]">
          <div className="bg-[#FAF7F2] p-3 rounded-xl border border-[#EBE4D5] flex items-center gap-2">
            <Clock className="w-4 h-4 text-[#244235]" />
            <span>{totalTime} mins</span>
          </div>
          <div className="bg-[#FAF7F2] p-3 rounded-xl border border-[#EBE4D5] flex items-center gap-2">
            <Flame className="w-4 h-4 text-[#9A4918]" />
            <span>{recipe.calories || 400} kcal</span>
          </div>
        </div>
      </div>

      {/* Footer Action Bar */}
      <div className="pt-4 mt-6 border-t border-[#EBE4D5] flex items-center justify-between">
        <span className="text-xs font-bold text-[#244235] bg-[#F4EFE6] px-3 py-1 rounded-lg border border-[#E5DCCB]">
          {recipe.budget_symbol || '💲'} {recipe.budget_tier || 'Budget'}
        </span>
        <Link
          to={`/recipe/${recipe.id}`}
          className="inline-flex items-center gap-1.5 text-xs font-bold text-[#244235] hover:text-[#1B3329] group-hover:translate-x-1 transition-transform"
        >
          <span>View Recipe</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
}
