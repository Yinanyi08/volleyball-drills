const conditioningData = require('../../data/conditioning.js');
const favorites = require('../../utils/favorites.js');

Page({
  data: {
    drills: [],
    filteredDrills: [],
    selectedIntensity: 'all',
    selectedCategory: 'all',
    favoriteIds: [],
    intensities: [
      { id: 'all', name: '全部强度' },
      { id: '低', name: '低' },
      { id: '中', name: '中' },
      { id: '高', name: '高' }
    ],
    categories: [
      { id: 'all', name: '全部类型' },
      { id: '力量', name: '力量' },
      { id: '核心稳定', name: '核心' },
      { id: '柔韧性', name: '柔韧' },
      { id: '爆发力', name: '爆发力' }
    ]
  },

  onLoad() {
    // 还原高度压缩的字段名以兼容原有模板
    const restoredData = conditioningData.map(d => ({
      id: d.i,
      title: d.t,
      description: d.d,
      category: d.c,
      intensity: d.n,
      ageGroup: d.g,
      image: d.m,
      setup: {
        equipment: d.s.e,
        players: d.s.p,
        court: d.s.u
      },
      steps: d.st,
      coachingTips: d.ct,
      variations: d.v
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

  onSelectIntensity(e) {
    const id = e.currentTarget.dataset.id;
    this.setData({ selectedIntensity: id }, this.applyFilters);
  },

  onSelectCategory(e) {
    const id = e.currentTarget.dataset.id;
    this.setData({ selectedCategory: id }, this.applyFilters);
  },

  applyFilters() {
    const { drills, selectedIntensity, selectedCategory } = this.data;
    let filtered = drills;

    if (selectedIntensity !== 'all') {
      filtered = filtered.filter(d => d.intensity === selectedIntensity);
    }

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(d => d.category === selectedCategory);
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
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/detail/detail?slug=${id}&type=conditioning`
    });
  },

  switchToTechnical() {
    wx.redirectTo({
      url: '/pages/index/index'
    });
  },

  goToFavorites() {
    wx.navigateTo({
      url: '/pages/favorites/favorites'
    });
  }
})
