import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function SearchBar({ initialQuery = '', placeholder = "Try searching: 'paneer haldi', 'panner', 'aloo', 'chicken tomato'...", onSearch }) {
  const [query, setQuery] = useState(initialQuery);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    if (onSearch) {
      onSearch(query);
    } else {
      navigate(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full max-w-3xl">
      <div className="bg-white p-2 rounded-2xl flex items-center gap-3 border border-[#E3DAC9] focus-within:border-[#244235] focus-within:ring-2 focus-within:ring-[#244235]/15 shadow-sm transition-all">
        <div className="pl-3 text-[#244235]">
          <Sparkles className="w-5 h-5 text-[#9A4918]" />
        </div>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="w-full bg-transparent text-[#231F1D] placeholder-[#8C7B6B] font-semibold text-sm sm:text-base focus:outline-none py-2"
        />

        <button
          type="submit"
          className="px-5 py-3 rounded-xl bg-[#244235] hover:bg-[#1B3228] text-white font-bold text-sm transition-all duration-200 flex items-center gap-2 shadow-xs shrink-0"
        >
          <span>Search</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </form>
  );
}
