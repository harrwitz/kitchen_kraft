import React, { useState, useEffect } from 'react';
import { Filter, RotateCcw, Flame, Clock, Dumbbell, Utensils, ChefHat, Leaf, ShieldAlert } from 'lucide-react';
import { getCuisines, getMealTypes } from '../api/client';

export default function FilterSidebar({ filters, onFilterChange, onReset }) {
  const [cuisines, setCuisines] = useState([]);
  const [mealTypes, setMealTypes] = useState([]);

  useEffect(() => {
    async function loadMetadata() {
      try {
        const [cRes, mRes] = await Promise.all([getCuisines(), getMealTypes()]);
        setCuisines(cRes.cuisines || []);
        setMealTypes(mRes.meal_types || []);
      } catch (err) {
        console.error('Failed loading metadata:', err);
      }
    }
    loadMetadata();
  }, []);

  const handleChange = (key, value) => {
    onFilterChange({ ...filters, [key]: value });
  };

  return (
    <aside className="bg-white p-5 rounded-2xl border border-[#E3DAC9] space-y-6 shadow-xs">
      <div className="flex items-center justify-between border-b border-[#EAE3D2] pb-4">
        <div className="flex items-center gap-2 font-bold font-serif-warm text-[#231F1D] text-base">
          <Filter className="w-5 h-5 text-[#244235]" />
          <span>Refine Recipes</span>
        </div>
        <button
          onClick={onReset}
          className="text-xs text-[#6E6359] hover:text-[#244235] flex items-center gap-1 transition-colors font-bold"
        >
          <RotateCcw className="w-3.5 h-3.5" /> Reset All
        </button>
      </div>

      {/* Dietary Switches */}
      <div className="space-y-3">
        <label className="text-xs font-bold uppercase tracking-wider text-[#6E6359] flex items-center gap-1.5">
          <Leaf className="w-4 h-4 text-[#244235]" /> Diet & Lifestyle
        </label>
        <div className="grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={() => handleChange('is_vegetarian', !filters.is_vegetarian)}
            className={`p-2.5 rounded-xl border text-xs font-bold flex items-center justify-center gap-1.5 transition-all ${
              filters.is_vegetarian
                ? 'bg-[#244235] text-white border-[#244235] shadow-xs'
                : 'bg-[#FAF7F2] text-[#231F1D] border-[#E3DAC9] hover:bg-[#F4EFE6]'
            }`}
          >
            <span>Vegetarian</span>
            {filters.is_vegetarian && '✓'}
          </button>

          <button
            type="button"
            onClick={() => handleChange('is_vegan', !filters.is_vegan)}
            className={`p-2.5 rounded-xl border text-xs font-bold flex items-center justify-center gap-1.5 transition-all ${
              filters.is_vegan
                ? 'bg-[#244235] text-white border-[#244235] shadow-xs'
                : 'bg-[#FAF7F2] text-[#231F1D] border-[#E3DAC9] hover:bg-[#F4EFE6]'
            }`}
          >
            <span>Vegan</span>
            {filters.is_vegan && '✓'}
          </button>
        </div>
      </div>

      {/* Cuisine Select */}
      <div className="space-y-2">
        <label className="text-xs font-bold uppercase tracking-wider text-[#6E6359] flex items-center gap-1.5">
          <Utensils className="w-4 h-4 text-[#244235]" /> Cuisine Type
        </label>
        <select
          value={filters.cuisine || 'All'}
          onChange={(e) => handleChange('cuisine', e.target.value)}
          className="w-full bg-[#FAF7F2] border border-[#E3DAC9] px-3.5 py-2.5 rounded-xl text-sm font-bold text-[#231F1D] focus:outline-none focus:border-[#244235]"
        >
          <option value="All">All Cuisines</option>
          {cuisines.map((c) => (
            <option key={c.name} value={c.name}>
              {c.name} ({c.count})
            </option>
          ))}
        </select>
      </div>

      {/* Meal Type Select */}
      <div className="space-y-2">
        <label className="text-xs font-bold uppercase tracking-wider text-[#6E6359] flex items-center gap-1.5">
          <ChefHat className="w-4 h-4 text-[#244235]" /> Meal Type
        </label>
        <select
          value={filters.meal_type || 'All'}
          onChange={(e) => handleChange('meal_type', e.target.value)}
          className="w-full bg-[#FAF7F2] border border-[#E3DAC9] px-3.5 py-2.5 rounded-xl text-sm font-bold text-[#231F1D] focus:outline-none focus:border-[#244235]"
        >
          <option value="All">All Meal Types</option>
          {mealTypes.map((m) => (
            <option key={m.name} value={m.name}>
              {m.name} ({m.count})
            </option>
          ))}
        </select>
      </div>

      {/* Difficulty */}
      <div className="space-y-2">
        <label className="text-xs font-bold uppercase tracking-wider text-[#6E6359] flex items-center gap-1.5">
          <ShieldAlert className="w-4 h-4 text-[#C2593F]" /> Difficulty Level
        </label>
        <select
          value={filters.difficulty || 'All'}
          onChange={(e) => handleChange('difficulty', e.target.value)}
          className="w-full bg-[#FAF7F2] border border-[#E3DAC9] px-3.5 py-2.5 rounded-xl text-sm font-bold text-[#231F1D] focus:outline-none focus:border-[#244235]"
        >
          <option value="All">Any Difficulty</option>
          <option value="Easy">Easy (&le; 25 mins)</option>
          <option value="Medium">Medium (25 - 55 mins)</option>
          <option value="Hard">Hard (&gt; 55 mins)</option>
        </select>
      </div>

      {/* Cooking Time Slider */}
      <div className="space-y-2">
        <div className="flex justify-between items-center text-xs">
          <span className="font-bold uppercase tracking-wider text-[#6E6359] flex items-center gap-1">
            <Clock className="w-3.5 h-3.5 text-[#244235]" /> Max Cook Time
          </span>
          <span className="text-[#231F1D] font-bold">{filters.max_cook_time ? `${filters.max_cook_time}m` : 'Any'}</span>
        </div>
        <input
          type="range"
          min="10"
          max="120"
          step="5"
          value={filters.max_cook_time || 120}
          onChange={(e) => handleChange('max_cook_time', parseInt(e.target.value))}
          className="w-full accent-[#244235] cursor-pointer h-1.5 bg-[#EAE3D2] rounded-lg"
        />
      </div>

      {/* Calories Slider */}
      <div className="space-y-2">
        <div className="flex justify-between items-center text-xs">
          <span className="font-bold uppercase tracking-wider text-[#6E6359] flex items-center gap-1">
            <Flame className="w-3.5 h-3.5 text-[#C2593F]" /> Max Calories
          </span>
          <span className="text-[#231F1D] font-bold">{filters.max_calories ? `${filters.max_calories} kcal` : 'Any'}</span>
        </div>
        <input
          type="range"
          min="150"
          max="1000"
          step="25"
          value={filters.max_calories || 1000}
          onChange={(e) => handleChange('max_calories', parseInt(e.target.value))}
          className="w-full accent-[#C2593F] cursor-pointer h-1.5 bg-[#EAE3D2] rounded-lg"
        />
      </div>

      {/* Protein Slider */}
      <div className="space-y-2">
        <div className="flex justify-between items-center text-xs">
          <span className="font-bold uppercase tracking-wider text-[#6E6359] flex items-center gap-1">
            <Dumbbell className="w-3.5 h-3.5 text-[#244235]" /> Min Protein
          </span>
          <span className="text-[#231F1D] font-bold">{filters.min_protein ? `${filters.min_protein}g` : '0g'}</span>
        </div>
        <input
          type="range"
          min="0"
          max="60"
          step="5"
          value={filters.min_protein || 0}
          onChange={(e) => handleChange('min_protein', parseInt(e.target.value))}
          className="w-full accent-[#244235] cursor-pointer h-1.5 bg-[#EAE3D2] rounded-lg"
        />
      </div>
    </aside>
  );
}
