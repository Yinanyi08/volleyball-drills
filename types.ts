
export interface DrillSetup {
  players: string;
  court: string;
  equipment: string;
  roles: string;
}

export interface Drill {
  url: string;
  slug: string;
  title: string;
  description: string;
  setup: DrillSetup;
  steps: string[];
  variations: string[];
  coaching_tips: string[];
  image_url: string;
  local_image: string;
  age_groups: string[];
  category: SkillCategory;
  phase: '热身' | '技术' | '实战' | '体能'; // 训练排序阶段
  difficulty: 1 | 2 | 3 | 4 | 5;
  duration: string;
}

export type SkillCategory = '垫球' | '发球' | '传球' | '防守' | '扣球' | '拦网' | '综合';

export interface FilterState {
  search: string;
  ageGroup: string;
  category: string;
}
