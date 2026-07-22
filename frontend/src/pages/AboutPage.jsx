import React from 'react';
import { Code2, Sparkles, Layers, User, Cpu, Database, Layout, Flame } from 'lucide-react';

export default function AboutPage() {
  const techStack = [
    {
      category: "Frontend Web Stack",
      icon: Layout,
      color: "bg-sage-100 text-sage-800 border-sage-300",
      items: [
        { name: "React 18", desc: "Component-driven user interface architecture" },
        { name: "Tailwind CSS", desc: "Custom utility-first pastel design system" },
        { name: "Vite", desc: "Lightning fast frontend bundler & dev server" },
        { name: "Lucide React", desc: "Modern iconography set" }
      ]
    },
    {
      category: "Backend API Stack",
      icon: Cpu,
      color: "bg-peach-100 text-peach-950 border-peach-300",
      items: [
        { name: "FastAPI", desc: "High-performance asynchronous Python API framework" },
        { name: "Python 3.13", desc: "Core backend execution environment" },
        { name: "Uvicorn", desc: "ASGI server worker management" },
        { name: "Pydantic", desc: "Strict schema validation and data serialization" }
      ]
    },
    {
      category: "Machine Learning & Data Engine",
      icon: Database,
      color: "bg-honey-100 text-honey-950 border-honey-300",
      items: [
        { name: "Scikit-Learn", desc: "TF-IDF vectorizer & cosine similarity matrix matching" },
        { name: "Pandas", desc: "In-memory DataFrame indexing across 13,493 recipes" },
        { name: "NumPy", desc: "Fast numerical matrix operations" },
        { name: "Canonical Taxonomy", desc: "Ingredient variety expansion and alias grouping" }
      ]
    }
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12 bg-[#F7F4EF]">
      {/* Title Header */}
      <div className="text-center space-y-4">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-sage-100 text-sage-950 border border-sage-300 text-xs font-bold shadow-2xs">
          <User className="w-4 h-4 text-sage-700" />
          <span>Made by Dhanush</span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold text-warmgray-900 tracking-tight font-sans">
          About Savory Crafts
        </h1>

        <p className="text-base text-warmgray-700 max-w-2xl mx-auto leading-relaxed font-medium">
          A full-stack recipe discovery web application architected and developed by <span className="font-extrabold text-sage-950 underline decoration-sage-400">Dhanush</span>, featuring smart ingredient matching and Machine Learning search.
        </p>
      </div>

      {/* Developer Callout Banner */}
      <div className="bg-white p-8 rounded-3xl border border-cream-300 shadow-pastel flex flex-col md:flex-row items-center gap-6">
        <div className="w-20 h-20 rounded-3xl bg-sage-600 text-white flex items-center justify-center font-extrabold text-2xl shrink-0 shadow-2xs">
          D
        </div>
        <div className="space-y-2 text-center md:text-left">
          <div className="inline-flex items-center gap-1.5 text-xs font-bold text-sage-700 bg-sage-100 px-3 py-0.5 rounded-full border border-sage-300">
            Developer & Architect
          </div>
          <h2 className="text-2xl font-extrabold text-warmgray-900">Crafted by Dhanush</h2>
          <p className="text-xs text-warmgray-700 leading-relaxed font-medium max-w-2xl">
            This project was built to combine clean user experience design with classic Machine Learning principles. It enables home cooks to quickly search over 13,000 recipes by ingredient combinations without needing complex filters or generic search terms.
          </p>
        </div>
      </div>

      {/* Tech Stack Breakdown Section */}
      <div className="space-y-6">
        <div className="text-center max-w-xl mx-auto space-y-2">
          <span className="text-xs font-extrabold uppercase tracking-wider text-sage-700">Engineering</span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-warmgray-900">
            Technology Stack Used
          </h2>
          <p className="text-xs text-warmgray-600 font-medium">
            Full breakdown of libraries, frameworks, and algorithms powering the app.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {techStack.map((sec) => {
            const IconComp = sec.icon;
            return (
              <div key={sec.category} className="bg-white p-6 rounded-3xl border border-cream-300 shadow-pastel space-y-4">
                <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-extrabold border ${sec.color}`}>
                  <IconComp className="w-4 h-4" />
                  <span>{sec.category}</span>
                </div>
                <div className="space-y-3 pt-2">
                  {sec.items.map((item) => (
                    <div key={item.name} className="p-3 rounded-2xl bg-cream-50 border border-cream-200 space-y-1">
                      <div className="font-extrabold text-sm text-warmgray-900">{item.name}</div>
                      <div className="text-xs text-warmgray-600 font-medium">{item.desc}</div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Core Algorithm Overview */}
      <div className="bg-white p-8 rounded-3xl border border-cream-300 shadow-pastel space-y-6">
        <h3 className="text-xl sm:text-2xl font-extrabold text-warmgray-900 flex items-center gap-2">
          <Code2 className="w-6 h-6 text-sage-700" /> How The Search Engine Works
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs text-warmgray-700 font-medium leading-relaxed">
          <div className="p-5 rounded-2xl bg-cream-50 border border-cream-200 space-y-2">
            <div className="font-extrabold text-sm text-warmgray-900 flex items-center gap-2">
              <Layers className="w-4 h-4 text-sage-700" /> 1. TF-IDF Ingredient Vectorization
            </div>
            <p>
              Recipe ingredients and titles are converted into term vectors. TF-IDF assigns higher importance weights to unique flavor ingredients (such as <em>basil</em>, <em>parmesan</em>, or <em>turmeric</em>) while lower weights are assigned to common staples.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-cream-50 border border-cream-200 space-y-2">
            <div className="font-extrabold text-sm text-warmgray-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-honey-700" /> 2. Smart Variety Matching
            </div>
            <p>
              When a user types <strong>bread</strong>, the engine expands the search query behind the scenes to encompass <em>sourdough</em>, <em>country bread</em>, <em>white bread</em>, and <em>pita</em> so relevant recipes are matched effortlessly.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
