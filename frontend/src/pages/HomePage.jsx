import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, Utensils, Leaf, Clock, Dumbbell, ArrowRight, User, Heart, Compass } from 'lucide-react';
import SearchBar from '../components/SearchBar';
import RecipeCard from '../components/RecipeCard';
import { SkeletonCard } from '../components/SkeletonCard';
import { getRecipes } from '../api/client';

export default function HomePage() {
  const navigate = useNavigate();
  const [featuredRecipes, setFeaturedRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHomeData() {
      try {
        setLoading(true);
        const data = await getRecipes({ limit: 6, sort_by: 'id' });
        setFeaturedRecipes(data.recipes || []);
      } catch (err) {
        console.error('Failed loading homepage recipes:', err);
      } finally {
        setLoading(false);
      }
    }
    loadHomeData();
  }, []);

  const popularCuisines = [
    { name: 'Indian', image: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=400&q=80', desc: 'Paneer, Dal, Curries & Naan' },
    { name: 'Italian', image: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=400&q=80', desc: 'Pasta, Risotto & Pizza' },
    { name: 'Asian', image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=400&q=80', desc: 'Ramen, Stir Fry & Miso' },
    { name: 'Mexican', image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=400&q=80', desc: 'Tacos, Burritos & Salsa' },
    { name: 'Mediterranean', image: 'https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=400&q=80', desc: 'Hummus, Feta & Olives' },
    { name: 'American', image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=400&q=80', desc: 'Burgers, BBQ & Salads' },
  ];

  const quickFilters = [
    { label: 'Paneer Dishes', path: '/search?q=paneer', icon: Sparkles, color: 'bg-[#FDF4E7] text-[#9A4918] border-[#F6D9B6] hover:bg-[#FBE3C5]' },
    { label: 'Vegetarian Specialties', path: '/search?is_vegetarian=true', icon: Leaf, color: 'bg-[#F4EFE6] text-[#244235] border-[#E5DCCB] hover:bg-[#EAE3D2]' },
    { label: 'Quick & Easy (<25m)', path: '/search?max_cook_time=25', icon: Clock, color: 'bg-[#FDF0ED] text-[#C2593F] border-[#F5C7BD] hover:bg-[#FAC5B9]' },
    { label: 'High Protein (>30g)', path: '/search?min_protein=30', icon: Dumbbell, color: 'bg-[#F0F6F5] text-[#1B4942] border-[#D0E2DF] hover:bg-[#D9ECE8]' },
  ];

  return (
    <div className="space-y-12 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto bg-[#FAF7F2]">
      {/* Hero Editorial Card */}
      <section className="relative rounded-3xl overflow-hidden bg-white p-8 sm:p-12 md:p-16 border border-[#E3DAC9] shadow-xs text-center flex flex-col items-center justify-center">
        
        {/* Editorial Handcrafted Badge Stamp */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#F4EFE6] border border-[#E3DAC9] text-[#244235] text-xs font-bold mb-6 shadow-xs">
          <User className="w-3.5 h-3.5 text-[#244235]" />
          <span>Handcrafted & Designed by Dhanush</span>
        </div>

        <h1 className="text-3xl sm:text-5xl md:text-6xl font-bold tracking-tight text-[#231F1D] max-w-4xl leading-tight mb-6 font-serif-warm">
          Cook Wonderful Dishes <br />
          <span className="text-[#244235]">With Ingredients You Have</span>
        </h1>

        <p className="text-base sm:text-lg text-[#5C5248] font-medium max-w-2xl leading-relaxed mb-8">
          Search over 13,000 recipes with bilingual ingredient matching for <span className="font-bold text-[#244235] bg-[#F4EFE6] px-2.5 py-0.5 rounded-md border border-[#E3DAC9]">Paneer</span>, <span className="font-bold text-[#9A4918] bg-[#FDF4E7] px-2.5 py-0.5 rounded-md border border-[#F6D9B6]">Haldi</span>, <span className="font-bold text-[#C2593F] bg-[#FDF0ED] px-2.5 py-0.5 rounded-md border border-[#F5C7BD]">Aloo</span>, or <span className="font-bold text-[#231F1D] bg-[#FAF7F2] px-2.5 py-0.5 rounded-md border border-[#E3DAC9]">Chicken</span>.
        </p>

        {/* Search Bar Container */}
        <div className="w-full flex justify-center mb-8">
          <SearchBar placeholder="Type ingredients in Hindi or English e.g. 'paneer haldi', 'panner', 'aloo'..." />
        </div>

        {/* Quick Filter Badges */}
        <div className="flex flex-wrap justify-center items-center gap-2.5">
          {quickFilters.map((qf) => {
            const IconComp = qf.icon;
            return (
              <button
                key={qf.label}
                onClick={() => navigate(qf.path)}
                className={`px-4 py-2 rounded-xl border text-xs font-bold flex items-center gap-2 transition-all hover:scale-105 shadow-xs ${qf.color}`}
              >
                <IconComp className="w-3.5 h-3.5" />
                <span>{qf.label}</span>
              </button>
            );
          })}
        </div>
      </section>

      {/* Smart Ingredient Taxonomy & Alias Showcase Cards */}
      <section className="bg-white rounded-3xl p-8 border border-[#E3DAC9] shadow-xs space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-[#244235]">Bilingual Matching</span>
          <h2 className="text-2xl sm:text-3xl font-bold font-serif-warm text-[#231F1D]">
            Intelligent Hindi & Regional Alias Matching
          </h2>
          <p className="text-xs text-[#6E6359] font-semibold">
            Search with popular Indian ingredient names or common spellings to automatically find all matching recipes.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={() => navigate('/search?q=paneer')}
            className="p-5 rounded-2xl bg-[#FDF4E7] border border-[#F6D9B6] space-y-2 text-left hover:scale-[1.02] transition-transform"
          >
            <div className="flex items-center justify-between font-bold text-[#9A4918] text-sm">
              <span>🧀 Paneer / Panner</span>
              <span className="text-[10px] bg-white px-2 py-0.5 rounded-full border border-[#F6D9B6]">Hindi & English</span>
            </div>
            <p className="text-xs text-[#7A360E] font-medium leading-relaxed">
              Typing "panner" or "paneer" automatically matches Cottage Cheese, Indian Cottage Cheese & Chenna recipes.
            </p>
          </button>

          <button
            onClick={() => navigate('/search?q=haldi')}
            className="p-5 rounded-2xl bg-[#FFFBEA] border border-[#FDE68A] space-y-2 text-left hover:scale-[1.02] transition-transform"
          >
            <div className="flex items-center justify-between font-bold text-[#B45309] text-sm">
              <span>🌾 Haldi & Spices</span>
              <span className="text-[10px] bg-white px-2 py-0.5 rounded-full border border-[#FDE68A]">Hindi & English</span>
            </div>
            <p className="text-xs text-[#92400E] font-medium leading-relaxed">
              Matches Haldi, Turmeric, Ground Turmeric, Jeera (Cumin), Dhania (Coriander) & Ginger (Adrak).
            </p>
          </button>

          <button
            onClick={() => navigate('/search?q=aloo')}
            className="p-5 rounded-2xl bg-[#FDF0ED] border border-[#F5C7BD] space-y-2 text-left hover:scale-[1.02] transition-transform"
          >
            <div className="flex items-center justify-between font-bold text-[#C2593F] text-sm">
              <span>🥔 Aloo & Veggies</span>
              <span className="text-[10px] bg-white px-2 py-0.5 rounded-full border border-[#F5C7BD]">Hindi & English</span>
            </div>
            <p className="text-xs text-[#8F331B] font-medium leading-relaxed">
              Matches Aloo (Potato), Pyaz (Onion), Tamatar (Tomato), Palak (Spinach) & Bhindi (Okra).
            </p>
          </button>

          <button
            onClick={() => navigate('/search?q=dal')}
            className="p-5 rounded-2xl bg-[#F4EFE6] border border-[#E3DAC9] space-y-2 text-left hover:scale-[1.02] transition-transform"
          >
            <div className="flex items-center justify-between font-bold text-[#244235] text-sm">
              <span>🫘 Dal, Chana & Rajma</span>
              <span className="text-[10px] bg-white px-2 py-0.5 rounded-full border border-[#E3DAC9]">Hindi & English</span>
            </div>
            <p className="text-xs text-[#1B3228] font-medium leading-relaxed">
              Matches Dal (Lentils), Chana (Chickpeas), Rajma (Kidney Beans), Atta & Basmati Rice.
            </p>
          </button>
        </div>
      </section>

      {/* Popular Cuisines Section */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold font-serif-warm text-[#231F1D] tracking-tight flex items-center gap-2">
              <Compass className="w-6 h-6 text-[#244235]" /> Popular Culinary Styles
            </h2>
            <p className="text-xs text-[#6E6359] font-medium">Explore curated recipes by regional tradition</p>
          </div>
          <Link to="/search" className="text-xs font-bold text-[#244235] hover:underline flex items-center gap-1">
            View All Cuisines <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {popularCuisines.map((c) => (
            <button
              key={c.name}
              onClick={() => navigate(`/search?cuisine=${c.name}`)}
              className="group bg-white rounded-2xl p-3 text-left overflow-hidden border border-[#E3DAC9] hover:border-[#244235] hover:-translate-y-1 transition-all duration-300 relative shadow-xs"
            >
              <div className="h-28 rounded-xl overflow-hidden mb-3 relative bg-[#FAF7F2]">
                <img
                  src={c.image}
                  alt={c.name}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#231F1D]/50 via-transparent to-transparent" />
              </div>
              <h3 className="font-bold text-sm text-[#231F1D] group-hover:text-[#244235] transition-colors">{c.name}</h3>
              <p className="text-[11px] text-[#8C7B6B] font-medium truncate">{c.desc}</p>
            </button>
          ))}
        </div>
      </section>

      {/* Featured Recipes Grid */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold font-serif-warm text-[#231F1D] tracking-tight flex items-center gap-2">
              <Utensils className="w-6 h-6 text-[#C2593F]" /> Featured Kitchen Recipes
            </h2>
            <p className="text-xs text-[#6E6359] font-medium">Handpicked everyday recipes ready for cooking</p>
          </div>
          <Link to="/search" className="text-xs font-bold text-[#244235] hover:underline flex items-center gap-1">
            Explore All Recipes <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading
            ? Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)
            : featuredRecipes.map((r) => <RecipeCard key={r.id} recipe={r} />)}
        </div>
      </section>
    </div>
  );
}
