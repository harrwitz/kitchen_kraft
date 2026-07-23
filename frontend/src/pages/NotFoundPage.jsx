import React from 'react';
import { Link } from 'react-router-dom';
import { ChefHat, ArrowLeft } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="max-w-md mx-auto px-4 py-24 text-center space-y-6">
      <div className="w-20 h-20 rounded-3xl bg-[#F4EFE6] border border-[#E3DAC9] text-[#244235] flex items-center justify-center mx-auto shadow-xs">
        <ChefHat className="w-10 h-10" />
      </div>

      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-[#231F1D] font-serif-warm">404</h1>
        <h2 className="text-lg font-bold text-[#6E6359]">Page Not Found</h2>
        <p className="text-xs text-[#8C7B6B] font-medium">
          The requested page or recipe route does not exist in our catalog.
        </p>
      </div>

      <Link
        to="/"
        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#244235] hover:bg-[#1C3329] text-white font-bold text-xs shadow-xs transition-all"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Home Page
      </Link>
    </div>
  );
}
