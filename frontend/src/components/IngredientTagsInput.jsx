import React, { useState, useEffect, useRef } from 'react';
import { Plus, X, Search, ChevronDown, Sparkles } from 'lucide-react';
import { autocompleteIngredients } from '../api/client';
import { useDebounce } from '../hooks/useDebounce';
import { INGREDIENT_CATEGORIES, POPULAR_INGREDIENT_TAGS } from '../data/ingredientTaxonomy';

export default function IngredientTagsInput({ ingredients = [], onChange }) {
  const [inputVal, setInputVal] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [showCategories, setShowCategories] = useState(false);
  const debouncedQuery = useDebounce(inputVal, 150);
  const containerRef = useRef(null);

  useEffect(() => {
    async function fetchSuggestions() {
      if (!debouncedQuery || debouncedQuery.trim().length < 1) {
        setSuggestions([]);
        return;
      }
      try {
        const res = await autocompleteIngredients(debouncedQuery);
        setSuggestions(res.ingredients || []);
      } catch (err) {
        console.error('Failed to fetch autocomplete ingredients:', err);
      }
    }
    fetchSuggestions();
  }, [debouncedQuery]);

  useEffect(() => {
    function handleClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const addIngredient = (item) => {
    // Extract base term if format is "Paneer (Cottage Cheese)"
    let cleanTerm = item.split('(')[0].trim().toLowerCase();
    if (cleanTerm && !ingredients.includes(cleanTerm)) {
      onChange([...ingredients, cleanTerm]);
    }
    setInputVal('');
    setSuggestions([]);
    setIsOpen(false);
  };

  const removeIngredient = (idxToRemove) => {
    onChange(ingredients.filter((_, idx) => idx !== idxToRemove));
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (inputVal.trim()) {
        addIngredient(inputVal);
      }
    }
  };

  return (
    <div ref={containerRef} className="relative w-full space-y-3">
      {/* Main Handcrafted Input Container */}
      <div className="bg-white p-3.5 rounded-2xl flex flex-wrap items-center gap-2 border border-[#E3DAC9] shadow-sm focus-within:border-[#244235] focus-within:ring-2 focus-within:ring-[#244235]/15 transition-all">
        {ingredients.map((ing, idx) => (
          <span
            key={idx}
            className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-[#F4EFE6] text-[#244235] border border-[#E5DCCB]"
          >
            <span className="capitalize">{ing}</span>
            <button
              type="button"
              onClick={() => removeIngredient(idx)}
              className="text-[#8C7B6B] hover:text-[#244235] transition-colors ml-0.5"
              title="Remove ingredient"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </span>
        ))}

        <div className="flex-grow flex items-center min-w-[220px]">
          <Search className="w-4 h-4 text-[#8C7B6B] mr-2.5 flex-shrink-0" />
          <input
            type="text"
            value={inputVal}
            onChange={(e) => {
              setInputVal(e.target.value);
              setIsOpen(true);
            }}
            onFocus={() => setIsOpen(true)}
            onKeyDown={handleKeyDown}
            placeholder={ingredients.length === 0 ? "Type in Hindi or English (e.g. paneer, haldi, aloo, bread...)" : "Add more ingredients..."}
            className="w-full bg-transparent text-sm font-semibold text-[#231F1D] placeholder-[#9E9083] focus:outline-none"
          />
        </div>
      </div>

      {/* Hindi & Popular Ingredient Quick Select Shortcuts */}
      <div className="flex flex-wrap items-center gap-1.5 pt-1">
        <span className="text-xs font-bold text-[#6E6359] mr-1 flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-[#C2593F]" /> Quick Select:
        </span>
        {POPULAR_INGREDIENT_TAGS.map((tag) => {
          const isSelected = ingredients.includes(tag.toLowerCase());
          return (
            <button
              key={tag}
              type="button"
              onClick={() => isSelected ? removeIngredient(ingredients.indexOf(tag.toLowerCase())) : addIngredient(tag)}
              className={`px-3 py-1 rounded-full text-xs font-bold transition-all ${
                isSelected
                  ? 'bg-[#244235] text-white shadow-xs'
                  : 'bg-white border border-[#E3DAC9] text-[#231F1D] hover:bg-[#F4EFE6] hover:border-[#D4C9B4]'
              }`}
            >
              {tag} {isSelected && '✓'}
            </button>
          );
        })}
      </div>

      {/* Category Pills Bar for Browsing */}
      <div className="flex flex-wrap gap-2 pt-1 border-t border-[#EAE3D2]">
        <button
          type="button"
          onClick={() => setShowCategories(!showCategories)}
          className="text-xs font-bold px-3 py-1.5 rounded-xl bg-[#F4EFE6] text-[#244235] hover:bg-[#EAE3D2] transition-colors flex items-center gap-1 border border-[#E3DAC9]"
        >
          <span>{showCategories ? 'Hide Categories' : 'Browse Categories (Paneer, Masala & Dals)'}</span>
          <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showCategories ? 'rotate-180' : ''}`} />
        </button>

        {showCategories && (
          <div className="w-full grid grid-cols-1 sm:grid-cols-2 gap-4 bg-[#FAF7F2] p-4.5 rounded-2xl border border-[#E3DAC9] my-2">
            {INGREDIENT_CATEGORIES.map((cat) => (
              <div key={cat.id} className="space-y-2">
                <div className="text-xs font-bold text-[#244235] border-b border-[#E3DAC9] pb-1 font-serif-warm">
                  {cat.name}
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {cat.tags.map((t) => (
                    <button
                      key={t.name}
                      type="button"
                      onClick={() => addIngredient(t.name)}
                      className="px-2.5 py-1 rounded-lg text-xs bg-white border border-[#E3DAC9] text-[#231F1D] hover:border-[#244235] hover:bg-[#F4EFE6] text-left transition-all font-semibold"
                    >
                      {t.name}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Autocomplete Suggestions Dropdown */}
      {isOpen && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl border border-[#E3DAC9] shadow-lg z-50 overflow-hidden max-h-72 overflow-y-auto">
          <div className="p-2.5 text-xs font-bold text-[#6E6359] border-b border-[#EAE3D2] bg-[#FAF7F2] flex items-center justify-between">
            <span>Matching Ingredients & Regional Aliases</span>
            <span className="text-[10px] text-[#8C7B6B] font-normal">Click to add to fridge</span>
          </div>

          {suggestions.map((item, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => addIngredient(item)}
              className="w-full text-left px-4 py-2.5 text-sm text-[#231F1D] hover:bg-[#F4EFE6] transition-colors flex items-center justify-between border-b border-[#F4EFE6] last:border-0 font-semibold group"
            >
              <span className="capitalize">{item}</span>
              <div className="w-5.5 h-5.5 rounded-full bg-[#FAF7F2] group-hover:bg-[#244235] group-hover:text-white flex items-center justify-center text-[#6E6359] transition-colors">
                <Plus className="w-3.5 h-3.5" />
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
