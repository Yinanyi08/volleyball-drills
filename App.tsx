
import React, { useState, useMemo } from 'react';
import { 
  Search, 
  Menu, 
  X, 
  Volleyball, 
  Users, 
  Filter,
  ArrowLeft,
  Bot,
  LayoutGrid,
  TrendingUp,
  Clock,
  Zap
} from 'lucide-react';
import { Drill, FilterState, SkillCategory } from './types';
import { DRILLS_DATA, SKILL_CATEGORIES, AGE_LEVELS } from './constants';
import DrillCard from './components/DrillCard';
import DrillDetail from './components/DrillDetail';
import Filters from './components/Filters';
import AICoach from './components/AICoach';

const App: React.FC = () => {
  const [selectedDrill, setSelectedDrill] = useState<Drill | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [showAICoach, setShowAICoach] = useState(false);
  const [filters, setFilters] = useState<FilterState>({
    search: '',
    ageGroup: '',
    category: ''
  });

  const filteredDrills = useMemo(() => {
    let result = DRILLS_DATA.filter(drill => {
      const matchesSearch = drill.title.toLowerCase().includes(filters.search.toLowerCase()) ||
                          drill.description.toLowerCase().includes(filters.search.toLowerCase());
      const matchesAge = filters.ageGroup ? drill.age_groups.includes(filters.ageGroup) : true;
      const matchesCategory = filters.category ? (drill.category === filters.category) : true;
      return matchesSearch && matchesAge && matchesCategory;
    });

    // 训练排序逻辑：热身 -> 技术 -> 实战 -> 体能
    const phaseOrder = { '热身': 1, '技术': 2, '实战': 3, '体能': 4 };
    return result.sort((a, b) => (phaseOrder[a.phase] || 99) - (phaseOrder[b.phase] || 99));
  }, [filters]);

  const handleDrillSelect = (drill: Drill) => {
    setSelectedDrill(drill);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleLevelSelect = (levelId: string) => {
    setFilters({ ...filters, ageGroup: levelId });
    window.scrollTo({ top: 400, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <header className="sticky top-0 z-50 bg-slate-900 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div 
              className="flex items-center cursor-pointer"
              onClick={() => { setSelectedDrill(null); setFilters({search: '', ageGroup: '', category: ''}); }}
            >
              <Volleyball className="h-8 w-8 text-orange-400 animate-bounce-slow" />
              <span className="ml-2 text-xl font-bold tracking-tight">排球精英 <span className="text-orange-400 underline decoration-2 underline-offset-4">教案库</span></span>
            </div>
            
            <div className="hidden md:flex items-center space-x-8">
              <button onClick={() => setSelectedDrill(null)} className="hover:text-orange-400 transition-colors">浏览训练</button>
              <button onClick={() => setShowAICoach(true)} className="hover:text-orange-400 transition-colors flex items-center gap-2">
                <Bot className="w-4 h-4" /> AI 教练
              </button>
            </div>

            <div className="flex items-center space-x-4">
              <button 
                onClick={() => setShowFilters(!showFilters)}
                className={`p-2 rounded-full transition-colors relative ${showFilters ? 'bg-orange-500 text-white' : 'hover:bg-slate-800'}`}
              >
                <Filter className="h-6 w-6" />
                {(filters.ageGroup || filters.category) && !showFilters && (
                  <span className="absolute top-1 right-1 w-3 h-3 bg-orange-500 rounded-full border-2 border-slate-900"></span>
                )}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {selectedDrill ? (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            <button 
              onClick={() => setSelectedDrill(null)}
              className="mb-6 flex items-center text-slate-500 hover:text-slate-900 transition-colors group"
            >
              <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
              返回训练列表
            </button>
            <DrillDetail drill={selectedDrill} />
          </div>
        ) : (
          <div className="space-y-12">
            {/* Hero & Quick Level Selection */}
            {!filters.search && !filters.ageGroup && !filters.category && (
              <div className="space-y-12">
                <div className="bg-gradient-to-br from-slate-900 to-indigo-900 rounded-[2rem] p-10 text-white relative overflow-hidden shadow-2xl">
                  <div className="relative z-10 max-w-2xl">
                    <h1 className="text-4xl md:text-5xl font-extrabold mb-4 leading-tight">按照等级 <br/><span className="text-orange-400">规划你的训练课。</span></h1>
                    <p className="text-slate-300 text-lg mb-8 leading-relaxed">参考国际先进青训体系，我们为不同年龄段的球员量身定制了阶梯式训练内容。从基础球感到实战对抗，一应俱全。</p>
                    <div className="flex items-center gap-4 text-sm">
                      <div className="flex items-center gap-1 bg-white/10 px-3 py-1 rounded-full"><TrendingUp className="w-4 h-4 text-green-400"/> 系统化课程</div>
                      <div className="flex items-center gap-1 bg-white/10 px-3 py-1 rounded-full"><Zap className="w-4 h-4 text-yellow-400"/> 实战模拟</div>
                    </div>
                  </div>
                  <div className="absolute right-0 bottom-0 top-0 w-1/3 opacity-10 flex items-center justify-center pointer-events-none">
                    <Volleyball className="w-64 h-64 rotate-12" />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {AGE_LEVELS.map(level => (
                    <button 
                      key={level.id}
                      onClick={() => handleLevelSelect(level.id)}
                      className="group bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md hover:border-orange-500 transition-all text-left"
                    >
                      <div className="bg-slate-100 group-hover:bg-orange-100 p-3 rounded-xl w-fit mb-4 transition-colors">
                        <Users className="w-6 h-6 text-slate-600 group-hover:text-orange-600" />
                      </div>
                      <h3 className="font-bold text-slate-900 mb-1">{level.label}</h3>
                      <p className="text-xs text-slate-500">{level.desc}</p>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Filter UI */}
            <div className="sticky top-[4.5rem] z-40 bg-slate-50/90 backdrop-blur-md py-4 space-y-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="relative flex-grow">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 h-5 w-5" />
                  <input 
                    type="text"
                    placeholder="在教案库中搜索 (如：蝴蝶、对打)..."
                    className="w-full pl-12 pr-4 py-4 bg-white rounded-2xl shadow-sm border border-slate-200 focus:outline-none focus:ring-2 focus:ring-orange-500 transition-shadow"
                    value={filters.search}
                    onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                  />
                </div>
              </div>

              {showFilters && (
                <div className="animate-in fade-in slide-in-from-top-4 duration-300">
                  <Filters 
                    filters={filters} 
                    setFilters={setFilters} 
                    categories={SKILL_CATEGORIES} 
                  />
                </div>
              )}
            </div>

            {/* Drills Section Header */}
            <div className="flex items-center justify-between border-b border-slate-200 pb-4">
              <div className="flex items-center gap-2">
                <LayoutGrid className="w-5 h-5 text-slate-400" />
                <h2 className="text-xl font-bold text-slate-800">
                  {filters.ageGroup ? `${filters.ageGroup}级训练内容` : '所有训练项目'}
                  <span className="ml-2 text-sm font-normal text-slate-500">({filteredDrills.length})</span>
                </h2>
              </div>
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <TrendingUp className="w-4 h-4" /> 自动排序：按课表逻辑
              </div>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredDrills.length > 0 ? (
                filteredDrills.map((drill, idx) => (
                  <DrillCard 
                    key={drill.slug + idx} 
                    drill={drill} 
                    onClick={() => handleDrillSelect(drill)} 
                  />
                ))
              ) : (
                <div className="col-span-full py-20 text-center bg-white rounded-3xl border border-dashed border-slate-300">
                  <h3 className="text-xl font-bold text-slate-800">该等级下暂无此分类训练</h3>
                  <p className="text-slate-500 mt-2">请尝试切换分类或重置筛选条件。</p>
                  <button 
                    onClick={() => setFilters({ search: '', ageGroup: '', category: '' })}
                    className="mt-6 px-6 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors"
                  >
                    显示所有训练
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="bg-slate-900 text-slate-400 py-12 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <div className="flex justify-center items-center mb-6">
            <Volleyball className="h-6 w-6 text-orange-400 mr-2" />
            <span className="text-white font-bold text-lg">VolleyPro 教案库</span>
          </div>
          <p className="max-w-md mx-auto mb-8 text-sm">对标 VolleyballXpert，打造中国最专业的数字化排球训练辅助工具。</p>
          <p className="text-xs">© 2024 VolleyPro Trainer. 基于专业排球理论体系构建。</p>
        </div>
      </footer>

      {showAICoach && (
        <AICoach onClose={() => setShowAICoach(false)} drills={DRILLS_DATA} />
      )}
    </div>
  );
};

export default App;
