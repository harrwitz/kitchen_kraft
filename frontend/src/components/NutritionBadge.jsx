import React from 'react';
import { Flame, Dumbbell, Wheat, Droplet } from 'lucide-react';

export default function NutritionBadge({ calories, protein, carbs, fat, compact = false }) {
  if (compact) {
    return (
      <div className="flex items-center gap-3 text-xs text-[#6E6359] font-medium">
        <span className="flex items-center gap-1 font-bold text-[#C2593F]">
          <Flame className="w-3.5 h-3.5" />
          {calories} kcal
        </span>
        <span className="flex items-center gap-1 font-bold text-[#244235]">
          <Dumbbell className="w-3.5 h-3.5" />
          {protein}g Protein
        </span>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
      {/* Calories */}
      <div className="p-4 rounded-2xl flex items-center gap-3.5 border border-amber-200/90 bg-gradient-to-br from-amber-50 to-orange-50/60 shadow-xs hover:shadow-md transition-all">
        <div className="w-11 h-11 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0 shadow-xs">
          <Flame className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-extrabold uppercase tracking-wider text-amber-900/80">Calories</div>
          <div className="text-xl font-black text-amber-950 leading-tight">
            {calories} <span className="text-xs font-bold text-amber-800/90">kcal</span>
          </div>
        </div>
      </div>

      {/* Protein */}
      <div className="p-4 rounded-2xl flex items-center gap-3.5 border border-emerald-200/90 bg-gradient-to-br from-emerald-50 to-teal-50/60 shadow-xs hover:shadow-md transition-all">
        <div className="w-11 h-11 rounded-xl bg-emerald-600 text-white flex items-center justify-center shrink-0 shadow-xs">
          <Dumbbell className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-extrabold uppercase tracking-wider text-emerald-900/80">Protein</div>
          <div className="text-xl font-black text-emerald-950 leading-tight">
            {protein} <span className="text-xs font-bold text-emerald-800/90">g</span>
          </div>
        </div>
      </div>

      {/* Carbs */}
      <div className="p-4 rounded-2xl flex items-center gap-3.5 border border-blue-200/90 bg-gradient-to-br from-blue-50 to-indigo-50/60 shadow-xs hover:shadow-md transition-all">
        <div className="w-11 h-11 rounded-xl bg-blue-600 text-white flex items-center justify-center shrink-0 shadow-xs">
          <Wheat className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-extrabold uppercase tracking-wider text-blue-900/80">Carbs</div>
          <div className="text-xl font-black text-blue-950 leading-tight">
            {carbs} <span className="text-xs font-bold text-blue-800/90">g</span>
          </div>
        </div>
      </div>

      {/* Fat */}
      <div className="p-4 rounded-2xl flex items-center gap-3.5 border border-rose-200/90 bg-gradient-to-br from-rose-50 to-pink-50/60 shadow-xs hover:shadow-md transition-all">
        <div className="w-11 h-11 rounded-xl bg-rose-600 text-white flex items-center justify-center shrink-0 shadow-xs">
          <Droplet className="w-5 h-5" />
        </div>
        <div>
          <div className="text-[11px] font-extrabold uppercase tracking-wider text-rose-900/80">Fat</div>
          <div className="text-xl font-black text-rose-950 leading-tight">
            {fat} <span className="text-xs font-bold text-rose-800/90">g</span>
          </div>
        </div>
      </div>
    </div>
  );
}
