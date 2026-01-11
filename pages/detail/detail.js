const drillsData = require('../../data/drills.js');
const conditioningData = require('../../data/conditioning.js');
const favorites = require('../../utils/favorites.js');

Page({
  data: {
    drill: null,
    type: 'technical',
    isFavorite: false
  },

  onLoad(options) {
    const { slug, type } = options;
    const isConditioning = type === 'conditioning';
    const dataSource = isConditioning ? conditioningData : drillsData;
    
    const rawDrill = dataSource.find(d => d.i === slug);
    if (rawDrill) {
      // 还原数据
      let drill;
      if (isConditioning) {
        drill = {
          id: rawDrill.i,
          title: rawDrill.t,
          description: rawDrill.d,
          category: rawDrill.c,
          intensity: rawDrill.n,
          ageGroup: rawDrill.g,
          image: rawDrill.m,
          setup: {
            equipment: rawDrill.s.e,
            players: rawDrill.s.p,
            court: rawDrill.s.u
          },
          steps: rawDrill.st,
          coachingTips: rawDrill.ct,
          variations: rawDrill.v
        };
      } else {
        drill = {
          id: rawDrill.i,
          title: rawDrill.t,
          description: rawDrill.d,
          category: rawDrill.c,
          phase: rawDrill.p,
          ageGroup: rawDrill.g,
          image: rawDrill.m,
          setup: rawDrill.s,
          steps: rawDrill.st,
          variations: rawDrill.v,
          coachingTips: rawDrill.ct
        };
      }

      this.setData({ 
        drill,
        type: isConditioning ? 'conditioning' : 'technical',
        isFavorite: favorites.isFavorite(slug)
      });
      
      // Extract Chinese title for navigation bar
      let title = drill.title;
      // ... (等后续代码)
      if (title.includes('(')) {
        title = title.split('(')[0].trim();
      }
      
      wx.setNavigationBarTitle({
        title: title || '训练详情'
      });
    }
  },

  onShow() {
    // Refresh favorite status when returning to page
    if (this.data.drill) {
      this.setData({
        isFavorite: favorites.isFavorite(this.data.drill.id)
      });
    }
  },

  toggleFavorite() {
    if (!this.data.drill) return;
    
    const newState = favorites.toggleFavorite(this.data.drill.id);
    this.setData({ isFavorite: newState });
    
    wx.showToast({
      title: newState ? '已收藏' : '已取消收藏',
      icon: 'success',
      duration: 1500
    });
  },

  previewImage() {
    if (!this.data.drill) return;
    const imageUrl = this.data.drill.image.startsWith('/public') 
      ? this.data.drill.image 
      : '/public' + this.data.drill.image;
      
    wx.previewImage({
      current: imageUrl,
      urls: [imageUrl]
    });
  }
})
