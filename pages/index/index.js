const drillsData = require('../../data/drills.js');
const favorites = require('../../utils/favorites.js');

Page({
  data: {
    drills: [],
    filteredDrills: [],
    searchQuery: '',
    selectedCategory: 'all',
    selectedAgeGroup: 'all',
    favoriteIds: [],
    categories: [
      { id: 'all', name: '全部' },
      { id: 'phase:热身', name: '热身' },
      { id: 'key:ball control', name: '控球' },
      { id: 'Blocking', name: '拦网' },
      { id: 'Defense', name: '防守' },
      { id: 'key:down ball', name: '下球' },
      { id: 'Hitting', name: '击球' },
      { id: 'key:middle', name: '副攻' },
      { id: 'key:attack', name: '进攻' },
      { id: 'key:hitter', name: '主攻' },
      { id: 'Passing', name: '传球' },
      { id: 'key:trans', name: '综合' },
      { id: 'key:pepper', name: '对垫' },
      { id: 'key:receive', name: '接发' },
      { id: 'key:serve', name: '发球' },
      { id: 'Setting', name: '传球' },
      { id: 'phase:体能', name: '体能' }
    ],
    ageGroups: [
      { id: 'all', name: '所有年龄' },
      { id: 'beginner', name: '小学/初级' },
      { id: 'intermediate', name: '中学/中级' },
      { id: 'high_school', name: '高中/进阶' },
      { id: 'advanced', name: '大学/专业' }
    ]
  },

  onLoad() {
    // 还原压缩的技术训练数据
    const restoredData = drillsData.map(d => ({
      id: d.i,
      title: d.t,
      description: d.d,
      category: d.c,
      phase: d.p,
      ageGroup: d.g,
      image: d.m,
      setup: d.s,
      steps: d.st,
      variations: d.v,
      coachingTips: d.ct
    }));

    this.setData({
      drills: restoredData,
      filteredDrills: restoredData
    });
  },

  onShow() {
    // Refresh favorite status when returning to page
    this.setData({
      favoriteIds: favorites.getFavorites()
    });
  },

  onSearchInput(e) {
    const query = e.detail.value.toLowerCase();
    this.setData({ searchQuery: query }, this.applyFilters);
  },

  onSelectCategory(e) {
    const cat = e.currentTarget.dataset.id;
    this.setData({ selectedCategory: cat }, this.applyFilters);
  },

  onSelectAgeGroup(e) {
    const age = e.currentTarget.dataset.id;
    this.setData({ selectedAgeGroup: age }, this.applyFilters);
  },

  applyFilters() {
    const { drills, searchQuery, selectedCategory, selectedAgeGroup } = this.data;
    let filtered = drills;

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(d => 
        (d.categories && d.categories.includes(selectedCategory)) ||
        (d.category === selectedCategory) ||
        (selectedCategory.startsWith('phase:') && d.phase === selectedCategory.split(':')[1]) 
      );
    }

    if (selectedAgeGroup !== 'all') {
      filtered = filtered.filter(d => d.ageGroup && d.ageGroup.includes(selectedAgeGroup));
    }

    if (searchQuery) {
      filtered = filtered.filter(d => 
        d.title.toLowerCase().includes(searchQuery) || 
        d.description.toLowerCase().includes(searchQuery)
      );
    }

    this.setData({ filteredDrills: filtered });
  },

  toggleFavorite(e) {
    const id = e.currentTarget.dataset.id;
    const newState = favorites.toggleFavorite(id);
    
    // Update local state
    this.setData({
      favoriteIds: favorites.getFavorites()
    });

    wx.showToast({
      title: newState ? '已收藏' : '已取消',
      icon: 'success',
      duration: 1000
    });
  },

  goToDetail(e) {
    const slug = e.currentTarget.dataset.slug;
    wx.navigateTo({
      url: `/pages/detail/detail?slug=${slug}`
    });
  },
  
  switchToConditioning() {
    wx.redirectTo({
      url: '/pages/conditioning/conditioning'
    });
  },

  goToFavorites() {
    wx.navigateTo({
      url: '/pages/favorites/favorites'
    });
  }
})
