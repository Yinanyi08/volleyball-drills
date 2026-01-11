
import React from 'react';
import { Drill } from '../types';
import { Users, Clock, ArrowRight, Star } from 'lucide-react';

interface DrillCardProps {
  drill: Drill;
  onClick: () => void;
}

const DrillCard: React.FC<DrillCardProps> = ({ drill, onClick }) => {
  const phaseColors = {
    '热身': 'bg-blue-100 text-blue-700',
    '技术': 'bg-green-100 text-green-700',
    '实战': 'bg-orange-100 text-orange-700',
    '体能': 'bg-purple-100 text-purple-700'
  };

  return (
    <div 
      className="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all cursor-pointer border border-slate-200 flex flex-col h-full"
      onClick={onClick}
    >
      <div className="relative h-52 overflow-hidden bg-slate-100">
        <img 
          src={drill.image_url} 
          alt={drill.title}
          className="w-full h-full object-contain p-2 bg-white transition-transform group-hover:scale-105 duration-700"
          loading="lazy"
          onError={(e) => {
            // 如果真实图片加载失败，回退到占位图
            (e.target as HTMLImageElement).src = 'https://via.placeholder.com/350x250?text=VolleyPro+Image';
          }}
        />
        {/* Age Level Tags */}
        <div className="absolute top-3 left-3 flex flex-wrap gap-2">
          {drill.age_groups.map((age) => (
            <span key={age} className="px-2 py-0.5 bg-slate-900/80 backdrop-blur text-[9px] font-bold rounded shadow-md text-white uppercase tracking-tighter">
              {age}级
            </span>
          ))}
        </div>
        {/* Phase Badge */}
        <div className={`absolute bottom-3 right-3 px-3 py-1 rounded-full text-[10px] font-black shadow-sm border border-white/20 ${phaseColors[drill.phase]}`}>
          {drill.phase}
        </div>
      </div>
      
      <div className="p-5 flex-grow flex flex-col">
        <div className="flex items-center justify-between mb-2.5">
          <span className="text-[10px] font-black text-orange-600 bg-orange-50 px-2 py-0.5 rounded border border-orange-100 uppercase">
            {drill.category}
          </span>
          <div className="flex text-yellow-400 scale-90 origin-right">
            {[...Array(5)].map((_, i) => (
              <Star key={i} className={`w-3 h-3 ${i < drill.difficulty ? 'fill-current' : 'text-slate-200'}`} />
            ))}
          </div>
        </div>

        <h3 className="text-base font-bold text-slate-900 mb-2 leading-snug group-hover:text-orange-600 transition-colors">
          {drill.title}
        </h3>
        <p className="text-slate-500 text-xs line-clamp-3 mb-4 leading-relaxed flex-grow">
          {drill.description}
        </p>
        
        <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-50">
          <div className="flex items-center gap-3 text-[10px] text-slate-400 font-bold">
            <span className="flex items-center gap-1"><Clock className="w-3 h-3"/> {drill.duration}</span>
            <span className="flex items-center gap-1"><Users className="w-3 h-3"/> {drill.setup.players.includes('个人') ? '单人' : '团队'}</span>
          </div>
          <div className="text-orange-600 group-hover:translate-x-1 transition-transform">
            <ArrowRight className="w-4 h-4" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DrillCard;
