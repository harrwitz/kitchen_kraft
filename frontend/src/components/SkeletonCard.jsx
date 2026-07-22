import React from 'react';

export function SkeletonCard() {
  return (
    <div className="glass-panel rounded-2xl overflow-hidden animate-pulse flex flex-col h-[380px]">
      <div className="h-48 bg-slate-800/80 w-full" />
      <div className="p-5 flex flex-col justify-between flex-grow">
        <div>
          <div className="flex justify-between items-center mb-3">
            <div className="h-3 w-16 bg-slate-800 rounded" />
            <div className="h-4 w-12 bg-slate-800 rounded" />
          </div>
          <div className="h-5 w-3/4 bg-slate-800 rounded mb-2" />
          <div className="h-4 w-1/2 bg-slate-800 rounded mb-4" />
          <div className="h-8 w-full bg-slate-800/60 rounded-xl" />
        </div>
        <div className="h-10 w-full bg-slate-800 rounded-xl mt-4" />
      </div>
    </div>
  );
}
