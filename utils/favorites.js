/**
 * 收藏管理工具
 * 使用本地存储实现收藏功能
 */

const STORAGE_KEY = 'volleypro_favorites';

/**
 * 获取所有收藏的训练ID
 * @returns {Array} 收藏ID列表
 */
function getFavorites() {
  try {
    const data = wx.getStorageSync(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch (e) {
    console.error('获取收藏失败:', e);
    return [];
  }
}

/**
 * 检查某个训练是否已收藏
 * @param {string} id 训练ID
 * @returns {boolean}
 */
function isFavorite(id) {
  const favorites = getFavorites();
  return favorites.includes(id);
}

/**
 * 添加收藏
 * @param {string} id 训练ID
 * @returns {boolean} 是否成功
 */
function addFavorite(id) {
  try {
    const favorites = getFavorites();
    if (!favorites.includes(id)) {
      favorites.push(id);
      wx.setStorageSync(STORAGE_KEY, JSON.stringify(favorites));
    }
    return true;
  } catch (e) {
    console.error('添加收藏失败:', e);
    return false;
  }
}

/**
 * 移除收藏
 * @param {string} id 训练ID
 * @returns {boolean} 是否成功
 */
function removeFavorite(id) {
  try {
    let favorites = getFavorites();
    favorites = favorites.filter(fid => fid !== id);
    wx.setStorageSync(STORAGE_KEY, JSON.stringify(favorites));
    return true;
  } catch (e) {
    console.error('移除收藏失败:', e);
    return false;
  }
}

/**
 * 切换收藏状态
 * @param {string} id 训练ID
 * @returns {boolean} 切换后的收藏状态
 */
function toggleFavorite(id) {
  if (isFavorite(id)) {
    removeFavorite(id);
    return false;
  } else {
    addFavorite(id);
    return true;
  }
}

/**
 * 获取收藏数量
 * @returns {number}
 */
function getFavoriteCount() {
  return getFavorites().length;
}

module.exports = {
  getFavorites,
  isFavorite,
  addFavorite,
  removeFavorite,
  toggleFavorite,
  getFavoriteCount
};
