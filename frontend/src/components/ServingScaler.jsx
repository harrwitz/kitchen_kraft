import React from 'react';
import { Users, Minus, Plus } from 'lucide-react';

export default function ServingScaler({ baseServings = 4, currentServings, onChange }) {
  const options = [2, 4, 6, 8];

  const handleDecrement = () => {
    if (currentServings > 1) onChange(currentServings - 1);
  };

  const handleIncrement = () => {
    if (currentServings < 16) onChange(currentServings + 1);
  };

  return (
    <div className="glass-panel p-4 rounded-2xl flex flex-wrap items-center justify-between gap-3 border border-white/10">
      <div className="flex items-center gap-2">
        <Users className="w-5 h-5 text-brand-400" />
        <div>
          <div className="text-sm font-semibold text-slate-200">Adjust Servings</div>
          <div className="text-xs text-slate-400">Recalculates ingredient quantities dynamically</div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center bg-slate-900 border border-slate-700/60 rounded-xl overflow-hidden p-1">
          <button
            onClick={handleDecrement}
            disabled={currentServings <= 1}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-300 hover:bg-slate-800 disabled:opacity-30 transition-colors"
          >
            <Minus className="w-4 h-4" />
          </button>
          <span className="w-10 text-center font-bold text-brand-400 text-base">
            {currentServings}
          </span>
          <button
            onClick={handleIncrement}
            disabled={currentServings >= 16}
            className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-300 hover:bg-slate-800 disabled:opacity-30 transition-colors"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>

        {/* Quick select pills */}
        <div className="hidden sm:flex items-center gap-1.5 bg-slate-900/60 p-1 rounded-xl border border-white/5">
          {options.map((opt) => (
            <button
              key={opt}
              onClick={() => onChange(opt)}
              className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                currentServings === opt
                  ? 'bg-brand-500 text-white shadow-sm shadow-brand-900/50'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {opt}p
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
