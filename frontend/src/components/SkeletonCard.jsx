import React from 'react';

export function SkeletonCard() {
  return (
    <div className="bg-white rounded-3xl overflow-hidden border border-[#E3DAC9] animate-pulse flex flex-col h-[380px] shadow-xs">
      <div className="h-48 bg-[#EBE4D5] w-full" />
      <div className="p-5 flex flex-col justify-between flex-grow space-y-3">
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <div className="h-3 w-16 bg-[#EBE4D5] rounded-full" />
            <div className="h-4 w-12 bg-[#EBE4D5] rounded-full" />
          </div>
          <div className="h-6 w-3/4 bg-[#EBE4D5] rounded-lg" />
          <div className="h-4 w-1/2 bg-[#EBE4D5] rounded-lg" />
        </div>
        <div className="h-10 w-full bg-[#F4EFE6] rounded-xl" />
      </div>
    </div>
  );
}
