import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, ArrowUpDown, Filter, X, Sparkles } from 'lucide-react';
import SearchBar from '../components/SearchBar';
import RecipeCard from '../components/RecipeCard';
import FilterSidebar from '../components/FilterSidebar';
import { SkeletonCard } from '../components/SkeletonCard';
import Pagination from '../components/Pagination';
import { getRecipes, searchRecipes } from '../api/client';

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();

  // Extract initial params from URL
  const queryParam = searchParams.get('q') || '';
  const cuisineParam = searchParams.get('cuisine') || 'All';
  const mealTypeParam = searchParams.get('meal_type') || 'All';
  const isVegParam = searchParams.get('is_vegetarian') === 'true';
  const isVeganParam = searchParams.get('is_vegan') === 'true';
  const maxCookParam = searchParams.get('max_cook_time') ? parseInt(searchParams.get('max_cook_time')) : null;
  const minProteinParam = searchParams.get('min_protein') ? parseInt(searchParams.get('min_protein')) : null;

  const [query, setQuery] = useState(queryParam);
  const [filters, setFilters] = useState({
    cuisine: cuisineParam,
    meal_type: mealTypeParam,
    is_vegetarian: isVegParam,
    is_vegan: isVeganParam,
    max_calories: null,
    max_cook_time: maxCookParam,
    difficulty: 'All',
    min_protein: minProteinParam,
  });

  const [sortBy, setSortBy] = useState('id');
  const [page, setPage] = useState(1);
  const [recipes, setRecipes] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);

  // Sync state when URL params change
  useEffect(() => {
    setQuery(searchParams.get('q') || '');
  }, [searchParams]);

  useEffect(() => {
    async function fetchResults() {
      try {
        setLoading(true);

        if (query.trim()) {
          const res = await searchRecipes({
            query: query.trim(),
            cuisine: filters.cuisine !== 'All' ? filters.cuisine : undefined,
            meal_type: filters.meal_type !== 'All' ? filters.meal_type : undefined,
            is_vegetarian: filters.is_vegetarian || undefined,
            is_vegan: filters.is_vegan || undefined,
            max_calories: filters.max_calories || undefined,
            max_cook_time: filters.max_cook_time || undefined,
            difficulty: filters.difficulty !== 'All' ? filters.difficulty : undefined,
            min_protein: filters.min_protein || undefined,
            limit: 12
          });
          setRecipes(res.recipes || []);
          setTotalCount(res.total || 0);
          setTotalPages(1);
        } else {
          const res = await getRecipes({
            page,
            limit: 12,
            cuisine: filters.cuisine !== 'All' ? filters.cuisine : undefined,
            meal_type: filters.meal_type !== 'All' ? filters.meal_type : undefined,
            is_vegetarian: filters.is_vegetarian || undefined,
            is_vegan: filters.is_vegan || undefined,
            max_calories: filters.max_calories || undefined,
            max_cook_time: filters.max_cook_time || undefined,
            difficulty: filters.difficulty !== 'All' ? filters.difficulty : undefined,
            min_protein: filters.min_protein || undefined,
            sort_by: sortBy
          });
          setRecipes(res.recipes || []);
          setTotalCount(res.total_count || 0);
          setTotalPages(res.total_pages || 1);
        }
      } catch (err) {
        console.error('Failed fetching search results:', err);
        setRecipes([]);
      } finally {
        setLoading(false);
      }
    }

    fetchResults();
  }, [query, filters, sortBy, page]);

  const handleResetFilters = () => {
    setFilters({
      cuisine: 'All',
      meal_type: 'All',
      is_vegetarian: false,
      is_vegan: false,
      max_calories: null,
      max_cook_time: null,
      difficulty: 'All',
      min_protein: null,
    });
    setSearchParams({});
    setPage(1);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 bg-[#FAF7F2]">
      {/* Search Header */}
      <div className="space-y-4">
        <h1 className="text-3xl font-bold font-serif-warm text-[#231F1D] tracking-tight flex items-center gap-2">
          <Search className="w-7 h-7 text-[#244235]" /> Explore Kitchen Recipes
        </h1>
        <p className="text-sm text-[#6E6359] font-medium">
          Search over 13,000 recipes by Hindi or English ingredient names (e.g., <span className="font-bold text-[#244235]">paneer</span>, <span className="font-bold text-[#9A4918]">haldi</span>, <span className="font-bold text-[#C2593F]">aloo</span>).
        </p>
        <SearchBar
          initialQuery={query}
          onSearch={(q) => {
            setQuery(q);
            setPage(1);
            setSearchParams(q ? { q } : {});
          }}
        />
      </div>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Desktop Filter Sidebar */}
        <div className="hidden lg:block lg:col-span-1">
          <FilterSidebar
            filters={filters}
            onFilterChange={(newF) => {
              setFilters(newF);
              setPage(1);
            }}
            onReset={handleResetFilters}
          />
        </div>

        {/* Results Column */}
        <div className="lg:col-span-3 space-y-6">
          {/* Controls Bar */}
          <div className="bg-white p-4 rounded-2xl flex flex-wrap items-center justify-between gap-4 border border-[#E3DAC9] shadow-xs">
            <div className="text-sm text-[#231F1D] font-bold">
              Showing <span className="text-[#244235]">{totalCount}</span> {totalCount === 1 ? 'recipe' : 'recipes'}
              {query && <span className="text-[#6E6359] font-normal"> for "{query}"</span>}
            </div>

            <div className="flex items-center gap-3">
              {/* Mobile Filter Toggle */}
              <button
                onClick={() => setMobileFilterOpen(true)}
                className="lg:hidden px-3 py-2 rounded-xl bg-[#F4EFE6] border border-[#E3DAC9] text-xs font-bold text-[#231F1D] flex items-center gap-1.5"
              >
                <Filter className="w-4 h-4 text-[#244235]" /> Filters
              </button>

              {/* Sorting Selector */}
              <div className="flex items-center gap-2">
                <ArrowUpDown className="w-4 h-4 text-[#8C7B6B]" />
                <select
                  value={sortBy}
                  onChange={(e) => {
                    setSortBy(e.target.value);
                    setPage(1);
                  }}
                  className="bg-[#FAF7F2] border border-[#E3DAC9] px-3 py-1.5 rounded-xl text-xs font-bold text-[#231F1D] focus:outline-none"
                >
                  <option value="id">Default Sort</option>
                  <option value="recipe_name">Recipe Name (A-Z)</option>
                  <option value="calories">Lowest Calories</option>
                  <option value="cook_time">Shortest Cook Time</option>
                  <option value="protein">Highest Protein</option>
                </select>
              </div>
            </div>
          </div>

          {/* Recipes Grid */}
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {Array.from({ length: 6 }).map((_, i) => (
                <SkeletonCard key={i} />
              ))}
            </div>
          ) : recipes.length === 0 ? (
            <div className="bg-white p-12 rounded-3xl text-center border border-[#E3DAC9] shadow-xs space-y-4">
              <div className="w-16 h-16 rounded-full bg-[#F4EFE6] text-[#8C7B6B] flex items-center justify-center mx-auto border border-[#E3DAC9]">
                <Search className="w-8 h-8 text-[#244235]" />
              </div>
              <h3 className="text-xl font-bold font-serif-warm text-[#231F1D]">No Recipes Found</h3>
              <p className="text-xs text-[#6E6359] max-w-md mx-auto font-semibold leading-relaxed">
                No matching recipes found for "{query}". Try searching for common terms like "paneer", "haldi", "aloo", "bread", or reset active filters.
              </p>
              <button
                onClick={handleResetFilters}
                className="px-4 py-2.5 rounded-xl bg-[#244235] hover:bg-[#1B3228] text-white font-bold text-xs shadow-xs"
              >
                Reset All Filters
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {recipes.map((r) => (
                <RecipeCard key={r.id} recipe={r} />
              ))}
            </div>
          )}

          {/* Pagination */}
          {!query && totalPages > 1 && (
            <Pagination page={page} totalPages={totalPages} onPageChange={(p) => setPage(p)} />
          )}
        </div>
      </div>

      {/* Mobile Filter Drawer Modal */}
      {mobileFilterOpen && (
        <div className="fixed inset-0 z-50 bg-[#231F1D]/60 backdrop-blur-xs flex justify-end">
          <div className="w-full max-w-md bg-white h-full p-6 overflow-y-auto space-y-4 shadow-xl border-l border-[#E3DAC9]">
            <div className="flex items-center justify-between border-b border-[#EAE3D2] pb-4">
              <h2 className="text-lg font-bold font-serif-warm text-[#231F1D]">Filters</h2>
              <button
                onClick={() => setMobileFilterOpen(false)}
                className="p-2 rounded-xl text-[#8C7B6B] hover:text-[#231F1D]"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <FilterSidebar
              filters={filters}
              onFilterChange={(newF) => {
                setFilters(newF);
                setPage(1);
              }}
              onReset={handleResetFilters}
            />
            <button
              onClick={() => setMobileFilterOpen(false)}
              className="w-full py-3 rounded-xl bg-[#244235] text-white font-bold text-sm"
            >
              Apply Filters
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

const None = undefined;
