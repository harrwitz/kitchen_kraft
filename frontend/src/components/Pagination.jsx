import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function Pagination({ page, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  const getPageNumbers = () => {
    const pages = [];
    const maxVisible = 5;

    let start = Math.max(1, page - 2);
    let end = Math.min(totalPages, start + maxVisible - 1);

    if (end - start + 1 < maxVisible) {
      start = Math.max(1, end - maxVisible + 1);
    }

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  };

  return (
    <div className="flex items-center justify-center gap-2 mt-10 mb-6 select-none">
      <button
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
        className="p-2.5 rounded-xl bg-white text-[#231F1D] border border-[#E3DAC9] shadow-xs hover:bg-[#244235] hover:text-white hover:border-[#244235] active:scale-95 disabled:opacity-40 disabled:hover:bg-white disabled:hover:text-[#231F1D] disabled:hover:border-[#E3DAC9] transition-all cursor-pointer disabled:cursor-not-allowed"
        aria-label="Previous Page"
      >
        <ChevronLeft className="w-5 h-5" />
      </button>

      {getPageNumbers().map((p) => (
        <button
          key={p}
          onClick={() => onPageChange(p)}
          className={`w-10 h-10 rounded-xl font-bold text-sm flex items-center justify-center transition-all cursor-pointer ${
            p === page
              ? 'bg-[#244235] text-white border border-[#244235] shadow-md scale-105'
              : 'bg-white text-[#231F1D] hover:bg-[#F4EFE6] hover:text-[#244235] border border-[#E3DAC9] shadow-xs'
          }`}
        >
          {p}
        </button>
      ))}

      <button
        onClick={() => onPageChange(page + 1)}
        disabled={page >= totalPages}
        className="p-2.5 rounded-xl bg-white text-[#231F1D] border border-[#E3DAC9] shadow-xs hover:bg-[#244235] hover:text-white hover:border-[#244235] active:scale-95 disabled:opacity-40 disabled:hover:bg-white disabled:hover:text-[#231F1D] disabled:hover:border-[#E3DAC9] transition-all cursor-pointer disabled:cursor-not-allowed"
        aria-label="Next Page"
      >
        <ChevronRight className="w-5 h-5" />
      </button>
    </div>
  );
}

