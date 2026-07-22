import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, Flame, Utensils, ChefHat, ArrowRight, Leaf, Sparkles } from 'lucide-react';

export default function RecipeCard({ recipe }) {
  if (!recipe) return null;

  const difficultyColors = {
    Easy: "bg-[#F4EFE6] text-[#244235] border-[#E5DCCB]",
    Medium: "bg-[#FDF4E7] text-[#9A4918] border-[#F6D9B6]",
    Hard: "bg-[#FDF0ED] text-[#C2593F] border-[#F5C7BD]"
  };

  return (
    <div className="group bg-white rounded-2xl overflow-hidden flex flex-col transition-all duration-300 hover:-translate-y-1.5 border border-[#E3DAC9] relative shadow-xs hover:shadow-md hover:border-[#D4C9B4]">
      {/* Image container */}
      <div className="relative h-48 sm:h-52 w-full overflow-hidden bg-[#FAF7F2]">
        <img
          src={recipe.image_url || "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80"}
          alt={recipe.recipe_name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          onError={(e) => {
            e.target.src = "https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=800&q=80";
          }}
        />

        <div className="absolute inset-0 bg-gradient-to-t from-[#231F1D]/60 via-transparent to-black/10" />

        {/* Top Left Cuisine Badge */}
        <div className="absolute top-3 left-3 flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-white/95 backdrop-blur-md text-[#231F1D] border border-[#E3DAC9] shadow-xs">
            <Utensils className="w-3 h-3 text-[#244235]" />
            {recipe.cuisine}
          </span>
        </div>

        {/* Top Right Similarity Score Badge if present */}
        {recipe.similarity_percent && (
          <div className="absolute top-3 right-3">
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-extrabold bg-[#244235] text-white border border-[#37614F] shadow-xs">
              <Sparkles className="w-3 h-3 text-[#F6D9B6]" />
              {recipe.similarity_percent} Match
            </span>
          </div>
        )}

        {/* Bottom Left Dietary Tag */}
        <div className="absolute bottom-3 left-3 flex flex-wrap items-center gap-1.5">
          {recipe.is_vegan ? (
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-white/90 text-[#244235] border border-[#E3DAC9] backdrop-blur-xs">
              <Leaf className="w-3 h-3 text-[#244235]" /> Vegan
            </span>
          ) : recipe.is_vegetarian ? (
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-white/90 text-[#244235] border border-[#E3DAC9] backdrop-blur-xs">
              <Leaf className="w-3 h-3 text-[#244235]" /> Vegetarian
            </span>
          ) : null}
        </div>
      </div>

      {/* Card Content */}
      <div className="p-5 flex flex-col flex-grow justify-between bg-white">
        <div>
          <div className="flex items-center justify-between gap-2 mb-2">
            <span className="text-xs font-bold text-[#8C7B6B] flex items-center gap-1">
              <ChefHat className="w-3.5 h-3.5 text-[#8C7B6B]" />
              {recipe.meal_type}
            </span>
            <span className={`px-2.5 py-0.5 rounded-md text-[11px] font-bold border ${difficultyColors[recipe.difficulty] || difficultyColors.Medium}`}>
              {recipe.difficulty}
            </span>
          </div>

          <h3 className="text-lg font-bold font-serif-warm text-[#231F1D] group-hover:text-[#244235] transition-colors line-clamp-2 mb-3 leading-snug">
            {recipe.recipe_name}
          </h3>

          {/* Quick Metrics Grid */}
          <div className="grid grid-cols-2 gap-2 py-2.5 px-3 rounded-xl bg-[#FAF7F2] border border-[#EAE3D2] text-xs text-[#231F1D] font-semibold mb-4">
            <div className="flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-[#244235]" />
              <span>{recipe.total_time} mins</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Flame className="w-3.5 h-3.5 text-[#C2593F]" />
              <span>{recipe.calories} kcal</span>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <Link
          to={`/recipe/${recipe.id}`}
          className="w-full py-2.5 px-4 rounded-xl bg-[#F4EFE6] hover:bg-[#244235] text-[#231F1D] hover:text-white font-bold text-xs transition-all duration-200 flex items-center justify-center gap-2 group/btn border border-[#E3DAC9] hover:border-[#244235] shadow-xs"
        >
          <span>View Recipe</span>
          <ArrowRight className="w-4 h-4 transition-transform group-hover/btn:translate-x-1" />
        </Link>
      </div>
    </div>
  );
}
