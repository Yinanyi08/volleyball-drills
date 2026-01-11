
import React from 'react';
import { FilterState, SkillCategory } from '../types';

interface FiltersProps {
  filters: FilterState;
  setFilters: React.Dispatch<React.SetStateAction<FilterState>>;
  categories: SkillCategory[];
}

const Filters: React.FC<FiltersProps> = ({ filters, setFilters, categories }) => {
  const ageGroups = ['入门', '进阶', '高中', '专业'];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex flex-wrap gap-8">
      <div className="flex-1 min-w-[200px]">
        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">适用阶段</h4>
        <div className="flex flex-wrap gap-2">
          {ageGroups.map(age => (
            <button
              key={age}
              onClick={() => setFilters({ ...filters, ageGroup: filters.ageGroup === age ? '' : age })}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all border ${
                filters.ageGroup === age 
                  ? 'bg-orange-500 border-orange-500 text-white shadow-md' 
                  : 'bg-white border-slate-200 text-slate-600 hover:border-orange-500'
              }`}
            >
              {age}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 min-w-[200px]">
        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">技能分类</h4>
        <div className="flex flex-wrap gap-2">
          {categories.map(cat => (
            <button
              key={cat}
              onClick={() => setFilters({ ...filters, category: filters.category === cat ? '' : cat })}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all border ${
                filters.category === cat 
                  ? 'bg-slate-900 border-slate-900 text-white shadow-md' 
                  : 'bg-white border-slate-200 text-slate-600 hover:border-slate-900'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Filters;
