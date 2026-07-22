import React from 'react';
import { Flame, Dumbbell, Wheat, Droplet } from 'lucide-react';

export default function NutritionBadge({ calories, protein, carbs, fat, compact = false }) {
  if (compact) {
    return (
      <div className="flex items-center gap-3 text-xs text-slate-300">
        <span className="flex items-center gap-1 font-medium text-amber-400">
          <Flame className="w-3.5 h-3.5" />
          {calories} kcal
        </span>
        <span className="flex items-center gap-1 font-medium text-emerald-400">
          <Dumbbell className="w-3.5 h-3.5" />
          {protein}g Protein
        </span>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <div className="glass-panel p-3.5 rounded-xl flex items-center gap-3 border border-amber-500/20 bg-amber-950/10">
        <div className="w-10 h-10 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center">
          <Flame className="w-5 h-5" />
        </div>
        <div>
          <div className="text-xs font-medium text-slate-400">Calories</div>
          <div className="text-lg font-bold text-slate-100">{calories} <span className="text-xs text-slate-400">kcal</span></div>
        </div>
      </div>

      <div className="glass-panel p-3.5 rounded-xl flex items-center gap-3 border border-emerald-500/20 bg-emerald-950/10">
        <div className="w-10 h-10 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
          <Dumbbell className="w-5 h-5" />
        </div>
        <div>
          <div className="text-xs font-medium text-slate-400">Protein</div>
          <div className="text-lg font-bold text-slate-100">{protein} <span className="text-xs text-slate-400">g</span></div>
        </div>
      </div>

      <div className="glass-panel p-3.5 rounded-xl flex items-center gap-3 border border-blue-500/20 bg-blue-950/10">
        <div className="w-10 h-10 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center">
          <Wheat className="w-5 h-5" />
        </div>
        <div>
          <div className="text-xs font-medium text-slate-400">Carbs</div>
          <div className="text-lg font-bold text-slate-100">{carbs} <span className="text-xs text-slate-400">g</span></div>
        </div>
      </div>

      <div className="glass-panel p-3.5 rounded-xl flex items-center gap-3 border border-rose-500/20 bg-rose-950/10">
        <div className="w-10 h-10 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center">
          <Droplet className="w-5 h-5" />
        </div>
        <div>
          <div className="text-xs font-medium text-slate-400">Fat</div>
          <div className="text-lg font-bold text-slate-100">{fat} <span className="text-xs text-slate-400">g</span></div>
        </div>
      </div>
    </div>
  );
}
