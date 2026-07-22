import React from 'react';
import { Link } from 'react-router-dom';
import { ChefHat, ArrowLeft } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="max-w-md mx-auto px-4 py-24 text-center space-y-6">
      <div className="w-20 h-20 rounded-3xl bg-slate-900 border border-slate-800 text-brand-400 flex items-center justify-center mx-auto shadow-2xl">
        <ChefHat className="w-10 h-10" />
      </div>

      <div className="space-y-2">
        <h1 className="text-4xl font-extrabold text-slate-100">404</h1>
        <h2 className="text-lg font-bold text-slate-300">Page Not Found</h2>
        <p className="text-xs text-slate-400">
          The requested page or recipe route does not exist in our system catalog.
        </p>
      </div>

      <Link
        to="/"
        className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-semibold text-xs shadow-lg transition-all"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Home Page
      </Link>
    </div>
  );
}
