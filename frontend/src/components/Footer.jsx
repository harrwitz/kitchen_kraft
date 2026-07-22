import React from 'react';
import { Utensils, Heart, User } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="mt-auto bg-white border-t border-[#E3DAC9] text-[#5C5248] py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        <div className="space-y-3 md:col-span-2">
          <div className="flex items-center gap-2 font-bold font-serif-warm text-[#231F1D] text-xl">
            <Utensils className="w-5.5 h-5.5 text-[#244235]" />
            <span>KitchenCraft</span>
          </div>
          <p className="text-xs text-[#6E6359] max-w-md leading-relaxed font-medium">
            An artisanal recipe discovery platform designed and developed by <strong className="text-[#231F1D] font-bold">Dhanush</strong>. Features bilingual Hindi & English ingredient matching to explore over 13,000 recipes effortlessly.
          </p>
          <div className="flex flex-wrap gap-2 pt-2">
            {['React 18', 'FastAPI', 'Python', 'Scikit-Learn', 'Tailwind CSS', 'Vite'].map((tech) => (
              <span key={tech} className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-[#F4EFE6] text-[#244235] border border-[#E3DAC9]">
                {tech}
              </span>
            ))}
          </div>
        </div>

        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#231F1D] mb-3">Navigation</h4>
          <ul className="space-y-2 text-xs font-semibold">
            <li><Link to="/" className="hover:text-[#244235] transition-colors">Home</Link></li>
            <li><Link to="/search" className="hover:text-[#244235] transition-colors">Explore Recipes</Link></li>
            <li><Link to="/recommend" className="hover:text-[#244235] transition-colors">Fridge Recommender</Link></li>
            <li><Link to="/about" className="hover:text-[#244235] transition-colors">About App & Tech Stack</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-[#231F1D] mb-3">Created By</h4>
          <div className="space-y-2 text-xs font-medium">
            <div className="flex items-center gap-2 text-[#244235] font-bold">
              <User className="w-4 h-4 text-[#244235]" />
              <span>Dhanush</span>
            </div>
            <p className="text-[11px] text-[#8C7B6B] leading-relaxed">
              Full-Stack Developer & Data Science Enthusiast.
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-[#EAE3D2] pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-[#8C7B6B] font-semibold">
        <div>&copy; {new Date().getFullYear()} KitchenCraft. Built by Dhanush.</div>
        <div className="flex items-center gap-1 mt-2 sm:mt-0">
          <span>Crafted with</span>
          <Heart className="w-3.5 h-3.5 text-[#C2593F] fill-[#C2593F] inline" />
          <span>by Dhanush</span>
        </div>
      </div>
    </footer>
  );
}
