import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Utensils, Sparkles, Menu, X, Heart } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Explore Recipes', path: '/search' },
    { name: 'Fridge Recommender', path: '/recommend' },
    { name: 'About App', path: '/about' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#FAF7F2]/95 backdrop-blur-md border-b border-[#EAE3D2] shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3.5 group">
          <div className="w-11 h-11 rounded-2xl bg-[#F4EFE6] border border-[#E3DAC9] flex items-center justify-center shadow-xs group-hover:scale-105 transition-transform duration-300">
            <Utensils className="w-5.5 h-5.5 text-[#244235]" />
          </div>
          <div>
            <div className="font-serif-warm text-2xl font-bold text-[#231F1D] tracking-tight flex items-center gap-2">
              <span>KitchenCraft</span>
              <span className="text-[10px] font-bold tracking-normal uppercase px-2 py-0.5 rounded-full bg-[#F4EFE6] text-[#244235] border border-[#E3DAC9]">
                Handcrafted
              </span>
            </div>
            <div className="text-[11px] font-semibold text-[#8C7B6B] hidden sm:block">Everyday Culinary Recipe Engine</div>
          </div>
        </Link>

        {/* Desktop Nav Links */}
        <nav className="hidden md:flex items-center gap-1.5 bg-white p-1.5 rounded-2xl border border-[#E3DAC9] shadow-xs">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all duration-200 ${
                isActive(link.path)
                  ? 'bg-[#244235] text-white shadow-xs'
                  : 'text-[#5C5248] hover:text-[#231F1D] hover:bg-[#F4EFE6]'
              }`}
            >
              {link.name}
            </Link>
          ))}
        </nav>

        {/* Action Button */}
        <div className="hidden sm:flex items-center gap-3">
          <Link
            to="/recommend"
            className="px-4.5 py-2.5 rounded-xl bg-[#244235] hover:bg-[#1B3228] text-white font-bold text-xs shadow-xs flex items-center gap-2 transition-all hover:scale-105"
          >
            <Sparkles className="w-4 h-4 text-[#F6D9B6]" />
            <span>Cook from Fridge</span>
          </Link>
        </div>

        {/* Mobile menu button */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="md:hidden p-2.5 rounded-xl bg-white text-[#231F1D] hover:text-[#244235] border border-[#E3DAC9]"
        >
          {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu Drawer */}
      {mobileOpen && (
        <div className="md:hidden bg-white border-b border-[#EAE3D2] px-4 py-4 space-y-2">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              onClick={() => setMobileOpen(false)}
              className={`block px-4 py-3 rounded-xl text-sm font-bold transition-all ${
                isActive(link.path)
                  ? 'bg-[#244235] text-white'
                  : 'text-[#231F1D] hover:bg-[#F4EFE6]'
              }`}
            >
              {link.name}
            </Link>
          ))}
          <div className="pt-2">
            <Link
              to="/recommend"
              onClick={() => setMobileOpen(false)}
              className="w-full py-2.5 px-4 rounded-xl bg-[#244235] text-white font-bold text-xs text-center block shadow-xs"
            >
              Cook from Fridge
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
