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
    <div className="bg-white p-5 rounded-3xl border border-[#E3DAC9] shadow-xs flex flex-wrap items-center justify-between gap-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-2xl bg-[#F4EFE6] text-[#244235] flex items-center justify-center border border-[#E3DAC9]">
          <Users className="w-5 h-5" />
        </div>
        <div>
          <div className="text-sm font-extrabold text-[#231F1D]">Adjust Recipe Servings</div>
          <div className="text-xs font-medium text-[#6E6359]">Recalculates ingredient quantities & macros dynamically</div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center bg-[#FAF7F2] border border-[#E3DAC9] rounded-2xl p-1.5 shadow-2xs">
          <button
            onClick={handleDecrement}
            disabled={currentServings <= 1}
            className="w-9 h-9 rounded-xl flex items-center justify-center text-[#231F1D] bg-white border border-[#E3DAC9] hover:bg-[#244235] hover:text-white hover:border-[#244235] disabled:opacity-30 disabled:hover:bg-white disabled:hover:text-[#231F1D] transition-all font-bold"
            title="Decrease Servings"
          >
            <Minus className="w-4 h-4" />
          </button>
          <span className="w-12 text-center font-black text-[#244235] text-lg font-serif-warm">
            {currentServings}
          </span>
          <button
            onClick={handleIncrement}
            disabled={currentServings >= 16}
            className="w-9 h-9 rounded-xl flex items-center justify-center text-[#231F1D] bg-white border border-[#E3DAC9] hover:bg-[#244235] hover:text-white hover:border-[#244235] disabled:opacity-30 disabled:hover:bg-white disabled:hover:text-[#231F1D] transition-all font-bold"
            title="Increase Servings"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>

        {/* Quick select pills */}
        <div className="hidden sm:flex items-center gap-1.5 bg-[#FAF7F2] p-1.5 rounded-2xl border border-[#E3DAC9]">
          {options.map((opt) => (
            <button
              key={opt}
              onClick={() => onChange(opt)}
              className={`px-3 py-1.5 rounded-xl text-xs font-extrabold transition-all ${
                currentServings === opt
                  ? 'bg-[#244235] text-white shadow-xs'
                  : 'text-[#6E6359] hover:text-[#231F1D] hover:bg-[#F4EFE6]'
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
