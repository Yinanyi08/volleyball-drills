const drillsData = require('../../data/drills.js');
const conditioningData = require('../../data/conditioning.js');
const favorites = require('../../utils/favorites.js');

Page({
  data: {
    favoritesList: [],
    isEmpty: true
  },

  onShow() {
    this.loadFavorites();
  },

  loadFavorites() {
    const favoriteIds = favorites.getFavorites();
    const allData = [...drillsData, ...conditioningData];
    
    const favoritesList = favoriteIds
      .map(id => {
        const item = allData.find(d => d.id === id);
        if (item) {
          // Determine type
          const isConditioning = conditioningData.some(c => c.id === id);
          return { ...item, type: isConditioning ? 'conditioning' : 'technical' };
        }
        return null;
      })
      .filter(Boolean);

    this.setData({
      favoritesList,
      isEmpty: favoritesList.length === 0
    });
  },

  goToDetail(e) {
    const { id, type } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/detail/detail?slug=${id}&type=${type}`
    });
  },

  removeFavorite(e) {
    const id = e.currentTarget.dataset.id;
    favorites.removeFavorite(id);
    
    wx.showToast({
      title: '已取消收藏',
      icon: 'success',
      duration: 1500
    });
    
    this.loadFavorites();
  },

  goHome() {
    wx.redirectTo({
      url: '/pages/index/index'
    });
  }
})
