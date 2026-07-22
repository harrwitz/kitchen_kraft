import React from 'react';
import { Sparkles } from 'lucide-react';

export default function SimilarityBadge({ score, percent }) {
  if (score === undefined || score === null) return null;

  const val = typeof score === 'number' ? score : parseFloat(percent || '0');
  
  let colorClasses = "bg-sage-100 text-sage-800 border-sage-200";
  if (val >= 80) {
    colorClasses = "bg-sage-100 text-sage-800 border-sage-300";
  } else if (val >= 50) {
    colorClasses = "bg-honey-100 text-honey-800 border-honey-300";
  } else {
    colorClasses = "bg-warmgray-100 text-warmgray-700 border-warmgray-200";
  }

  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-bold border shadow-2xs backdrop-blur-xs ${colorClasses}`}>
      <Sparkles className="w-3 h-3 text-sage-600" />
      {percent || `${val}% Match`}
    </span>
  );
}

