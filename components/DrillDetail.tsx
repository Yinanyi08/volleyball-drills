
import React from 'react';
import { Drill } from '../types';
import { 
  Users, 
  Map, 
  Wrench, 
  Info, 
  ListOrdered, 
  Lightbulb, 
  Shuffle,
  Clock,
  Star,
  Activity
} from 'lucide-react';

interface DrillDetailProps {
  drill: Drill;
}

const DrillDetail: React.FC<DrillDetailProps> = ({ drill }) => {
  return (
    <div className="bg-white rounded-[2rem] shadow-2xl overflow-hidden border border-slate-200 max-w-5xl mx-auto mb-20">
      <div className="grid grid-cols-1 lg:grid-cols-5 h-full">
        {/* Sidebar Info */}
        <div className="lg:col-span-2 bg-slate-50 p-8 lg:p-10 border-r border-slate-200">
          <div className="mb-8">
            <img 
              src={drill.image_url} 
              alt={drill.title}
              className="w-full h-64 object-cover rounded-2xl shadow-lg mb-6"
            />
            <div className="flex flex-wrap gap-2 mb-4">
              {drill.age_groups.map(age => (
                <span key={age} className="px-3 py-1 bg-slate-900 text-white text-[10px] font-bold rounded-lg uppercase">
                  {age}级
                </span>
              ))}
              <span className="px-3 py-1 bg-orange-500 text-white text-[10px] font-bold rounded-lg uppercase">
                {drill.phase}阶段
              </span>
            </div>
            <h2 className="text-3xl font-black text-slate-900 leading-tight mb-4">{drill.title}</h2>
            <div className="flex items-center gap-4 text-sm text-slate-500 mb-6">
              <span className="flex items-center gap-1"><Clock className="w-4 h-4"/> {drill.duration}</span>
              <div className="flex text-yellow-400">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className={`w-3.5 h-3.5 ${i < drill.difficulty ? 'fill-current' : 'text-slate-200'}`} />
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="bg-white p-2.5 rounded-xl shadow-sm"><Users className="w-5 h-5 text-orange-500" /></div>
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">参与人员</h4>
                <p className="text-sm text-slate-700 font-medium">{drill.setup.players}</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="bg-white p-2.5 rounded-xl shadow-sm"><Map className="w-5 h-5 text-blue-500" /></div>
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">场地要求</h4>
                <p className="text-sm text-slate-700 font-medium">{drill.setup.court}</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="bg-white p-2.5 rounded-xl shadow-sm"><Wrench className="w-5 h-5 text-green-500" /></div>
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">器材清单</h4>
                <p className="text-sm text-slate-700 font-medium">{drill.setup.equipment}</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="bg-white p-2.5 rounded-xl shadow-sm"><Info className="w-5 h-5 text-purple-500" /></div>
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">角色分工</h4>
                <p className="text-sm text-slate-700 font-medium">{drill.setup.roles}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Content Section */}
        <div className="lg:col-span-3 p-8 lg:p-12 space-y-12">
          <section>
            <div className="flex items-center gap-3 mb-6">
              <Activity className="w-6 h-6 text-orange-500" />
              <h3 className="text-2xl font-bold text-slate-900 italic">训练初衷</h3>
            </div>
            <p className="text-lg text-slate-600 leading-relaxed border-l-4 border-slate-200 pl-6">
              {drill.description}
            </p>
          </section>

          <section>
            <div className="flex items-center gap-3 mb-8">
              <ListOrdered className="w-6 h-6 text-slate-900" />
              <h3 className="text-2xl font-bold text-slate-900">执行步骤 (Step-by-Step)</h3>
            </div>
            <div className="space-y-6">
              {drill.steps.map((step, idx) => (
                <div key={idx} className="flex gap-6 group">
                  <div className="flex-shrink-0 w-10 h-10 rounded-2xl bg-slate-100 flex items-center justify-center font-black text-slate-400 group-hover:bg-orange-600 group-hover:text-white transition-all transform group-hover:scale-110">
                    {idx + 1}
                  </div>
                  <div className="pt-2">
                    <p className="text-slate-700 leading-relaxed text-base">{step}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="bg-yellow-50/50 p-8 rounded-3xl border border-yellow-100">
            <div className="flex items-center gap-3 mb-4">
              <Lightbulb className="w-6 h-6 text-yellow-600" />
              <h3 className="text-xl font-bold text-slate-900">教练关键提示 (Coaching Keys)</h3>
            </div>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {drill.coaching_tips.map((tip, idx) => (
                <li key={idx} className="flex items-start gap-3 text-sm text-slate-600 bg-white/60 p-3 rounded-xl border border-yellow-100 shadow-sm">
                  <div className="w-1.5 h-1.5 bg-yellow-400 rounded-full mt-2" />
                  {tip}
                </li>
              ))}
            </ul>
          </section>

          <section>
            <div className="flex items-center gap-3 mb-6">
              <Shuffle className="w-6 h-6 text-indigo-500" />
              <h3 className="text-xl font-bold text-slate-900">进阶变体</h3>
            </div>
            <div className="grid grid-cols-1 gap-4">
              {drill.variations.map((v, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-slate-50 border border-slate-100 text-sm text-slate-600">
                  <span className="font-bold text-indigo-600 mr-2">方案 {idx + 1}:</span> {v}
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default DrillDetail;
