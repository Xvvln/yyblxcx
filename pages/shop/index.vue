<template>
  <view class="page">
    <!-- 搜索头部 -->
    <view class="search-header">
      <view class="search-box" @click="goSearch">
        <wd-icon name="search" size="18px" color="#86868B"></wd-icon>
        <text class="placeholder">搜索运动装备、健康食品</text>
      </view>
      <view class="cart-icon" @click="goCart">
        <wd-icon name="cart" size="22px" color="#1D1D1F"></wd-icon>
        <view v-if="cartCount > 0" class="badge">{{ cartCount > 99 ? '99+' : cartCount }}</view>
      </view>
    </view>
    
    <!-- 分类导航 -->
    <scroll-view scroll-x class="nav-scroll">
      <view 
        class="nav-item" 
        v-for="cat in categories" 
        :key="cat.id"
        :class="{ active: currentCategory === cat.id }"
        @click="selectCategory(cat.id)"
      >
        <view class="icon-box">
          <text class="emoji">{{ cat.icon || '📦' }}</text>
        </view>
        <text class="name">{{ cat.name }}</text>
      </view>
    </scroll-view>
    
    <!-- Banner -->
    <swiper v-if="banners.length" class="banner-swiper" indicator-dots autoplay circular>
      <swiper-item v-for="banner in banners" :key="banner.id">
        <view class="banner-card">
          <view class="banner-tag">热销</view>
          <text class="banner-title">{{ banner.title || '精选好物' }}</text>
          <text class="banner-desc">品质保证 健康生活</text>
        </view>
      </swiper-item>
    </swiper>
    
    <!-- 商品列表 -->
    <view class="section-title">
      <text class="main">{{ currentCategoryName }}</text>
      <text class="sub">精选好物</text>
    </view>
    
    <view class="product-grid">
      <view class="product-card" v-for="item in products" :key="item.id" @click="goDetail(item.id)">
        <view class="img-box">
          <image v-if="item.images?.[0]" :src="item.images[0]" mode="aspectFill" />
          <text v-else class="placeholder">商品图</text>
        </view>
        <view class="info">
          <text class="name">{{ item.name }}</text>
          <text class="subtitle" v-if="item.subtitle">{{ item.subtitle }}</text>
          <view class="price-row">
            <text class="price"><text class="symbol">¥</text>{{ item.current_price }}</text>
            <text class="original" v-if="item.original_price > item.current_price">¥{{ item.original_price }}</text>
          </view>
          <view class="sales-row">
            <text class="sales">已售{{ item.sales_count || 0 }}</text>
            <view class="add-cart" @click.stop="addToCart(item)">
              <wd-icon name="add" size="16px" color="#FFFFFF"></wd-icon>
            </view>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 加载更多 -->
    <view class="load-more" v-if="hasMore">
      <text @click="loadMore">加载更多</text>
    </view>
    <view class="no-more" v-else-if="products.length > 0">
      <text>没有更多了</text>
    </view>
    
    <!-- 空状态 -->
    <view class="empty" v-if="!loading && products.length === 0">
      <text class="empty-icon">🛒</text>
      <text class="empty-text">暂无商品</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getCategories, getProducts, addToCart as apiAddToCart, getCartList } from '@/api/shop'
import { getBanners } from '@/api/home'

const categories = ref<any[]>([{ id: 0, name: '全部', icon: '🔥' }])
const products = ref<any[]>([])
const banners = ref<any[]>([])
const currentCategory = ref(0)
const page = ref(1)
const pageSize = 10
const total = ref(0)
const loading = ref(false)
const cartCount = ref(0)

const hasMore = computed(() => products.value.length < total.value)

const currentCategoryName = computed(() => {
  if (currentCategory.value === 0) return '热门推荐'
  const cat = categories.value.find(c => c.id === currentCategory.value)
  return cat?.name || '商品列表'
})

// 获取分类
async function fetchCategories() {
  try {
    const res = await getCategories()
    if (res.code === 200 && res.data) {
      categories.value = [{ id: 0, name: '全部', icon: '🔥' }, ...res.data]
    }
  } catch (e) {
    console.error(e)
  }
}

// 获取商品
async function fetchProducts(refresh = false) {
  if (loading.value) return
  loading.value = true
  
  try {
    if (refresh) {
      page.value = 1
      products.value = []
    }
    
    const params: any = {
      page: page.value,
      page_size: pageSize,
    }
    
    if (currentCategory.value > 0) {
      params.category_id = currentCategory.value
    }
    
    const res = await getProducts(params)
    if (res.code === 200 && res.data) {
      if (refresh) {
        products.value = res.data.list || []
      } else {
        products.value.push(...(res.data.list || []))
      }
      total.value = res.data.total || 0
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 获取轮播图
async function fetchBanners() {
  try {
    const res = await getBanners('shop')
    if (res.code === 200) {
      banners.value = res.data || []
    }
  } catch (e) {
    console.error(e)
  }
}

// 获取购物车数量
async function fetchCartCount() {
  try {
    const res = await getCartList()
    if (res.code === 200 && res.data) {
      cartCount.value = res.data.length || 0
    }
  } catch (e) {
    console.error(e)
  }
}

// 选择分类
function selectCategory(id: number) {
  currentCategory.value = id
  fetchProducts(true)
}

// 加载更多
function loadMore() {
  if (hasMore.value && !loading.value) {
    page.value++
    fetchProducts()
  }
}

// 添加到购物车
async function addToCart(item: any) {
  try {
    const res = await apiAddToCart({ product_id: item.id, quantity: 1 })
    if (res.code === 200) {
      uni.showToast({ title: '已加入购物车', icon: 'success' })
      cartCount.value++
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '添加失败', icon: 'none' })
  }
}

// 跳转
function goDetail(id: number) {
  uni.navigateTo({ url: `/pages/shop/detail?id=${id}` })
}

function goCart() {
  uni.navigateTo({ url: '/pages/cart/index' })
}

function goSearch() {
  // 可以跳转到搜索页面
  uni.showToast({ title: '搜索功能开发中', icon: 'none' })
}

onShow(() => {
  fetchCategories()
  fetchProducts(true)
  fetchBanners()
  fetchCartCount()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
  padding-bottom: 120px;
}

.search-header {
  background: #FFFFFF;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: sticky;
  top: 0;
  z-index: 100;
  
  .search-box {
    flex: 1;
    height: 36px;
    background: #F5F5F7;
    border-radius: 18px;
    display: flex;
    align-items: center;
    padding: 0 14px;
    gap: 8px;
    
    .placeholder {
      font-size: 14px;
      color: #86868B;
    }
  }
  
  .cart-icon {
    position: relative;
    padding: 8px;
    
    .badge {
      position: absolute;
      top: 2px;
      right: 2px;
      min-width: 16px;
      height: 16px;
      background: #FF3B30;
      border-radius: 8px;
      font-size: 10px;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 4px;
    }
  }
}

.nav-scroll {
  white-space: nowrap;
  padding: 16px;
  background: #FFFFFF;
  
  .nav-item {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    margin-right: 20px;
    opacity: 0.6;
    transition: all 0.2s;
    
    &.active {
      opacity: 1;
      
      .icon-box {
        transform: scale(1.1);
      }
      
      .name {
        color: #0071e3;
        font-weight: 600;
      }
    }
    
    .icon-box {
      width: 48px;
      height: 48px;
      border-radius: 16px;
      background: #F5F5F7;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 8px;
      transition: transform 0.2s;
      
      .emoji { font-size: 24px; }
    }
    
    .name { font-size: 12px; color: #1D1D1F; }
  }
}

.banner-swiper {
  margin: 16px;
  height: 140px;
  border-radius: 16px;
  overflow: hidden;
  
  .banner-card {
    height: 100%;
    background: linear-gradient(135deg, #1D1D1F 0%, #3a3a3c 100%);
    border-radius: 16px;
    padding: 24px;
    position: relative;
    color: #FFF;
    
    .banner-tag {
      display: inline-block;
      padding: 2px 8px;
      background: #FF9500;
      color: #FFF;
      font-size: 10px;
      font-weight: 600;
      border-radius: 4px;
      margin-bottom: 8px;
    }
    
    .banner-title {
      font-size: 20px;
      font-weight: 700;
      display: block;
      margin-bottom: 4px;
    }
    
    .banner-desc {
      font-size: 12px;
      opacity: 0.7;
    }
  }
}

.section-title {
  padding: 16px 16px 12px;
  display: flex;
  align-items: baseline;
  gap: 8px;
  
  .main { font-size: 18px; font-weight: 700; color: #1D1D1F; }
  .sub { font-size: 12px; color: #86868B; }
}

.product-grid {
  padding: 0 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  
  .product-card {
    background: #FFFFFF;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    
    .img-box {
      height: 160px;
      background: #F5F5F7;
      display: flex;
      align-items: center;
      justify-content: center;
      
      image {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      
      .placeholder { color: #C7C7CC; font-size: 12px; }
    }
    
    .info {
      padding: 12px;
      
      .name {
        font-size: 14px;
        color: #1D1D1F;
        font-weight: 500;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        overflow: hidden;
        min-height: 40px;
        margin-bottom: 4px;
      }
      
      .subtitle {
        font-size: 11px;
        color: #86868B;
        margin-bottom: 8px;
        display: block;
      }
      
      .price-row {
        display: flex;
        align-items: baseline;
        gap: 6px;
        margin-bottom: 8px;
        
        .price {
          color: #FF3B30;
          font-size: 18px;
          font-weight: 700;
          
          .symbol { font-size: 12px; }
        }
        
        .original {
          font-size: 12px;
          color: #C7C7CC;
          text-decoration: line-through;
        }
      }
      
      .sales-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .sales {
          font-size: 11px;
          color: #86868B;
        }
        
        .add-cart {
          width: 24px;
          height: 24px;
          background: #0071e3;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }
      }
    }
  }
}

.load-more, .no-more {
  text-align: center;
  padding: 20px;
  font-size: 13px;
  color: #86868B;
}

.load-more text {
  color: #0071e3;
}

.empty {
  padding: 60px 20px;
  text-align: center;
  
  .empty-icon {
    font-size: 48px;
    display: block;
    margin-bottom: 12px;
  }
  
  .empty-text {
    font-size: 14px;
    color: #86868B;
  }
}
</style>
