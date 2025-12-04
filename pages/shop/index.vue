<template>
  <view class="page">
    <!-- 顶部固定区域 -->
    <view class="header-fixed">
      <!-- 顶部栏：头像 + 搜索 + 购物车 -->
      <view class="top-bar">
        <!-- 左侧头像 -->
        <view class="user-avatar" @click="goUser">
          <image :src="userStore.userInfo?.avatar || '/static/placeholder/avatar.png'" mode="aspectFill" />
        </view>
        
        <!-- 中间搜索框 -->
        <view class="search-box" @click="goSearch">
          <wd-icon name="search" size="16px" color="#999999"></wd-icon>
          <text class="placeholder">Keep 女士蛋白粉</text>
        </view>
        
        <!-- 右侧购物车 -->
        <view class="cart-btn" @click="goCart">
          <wd-icon name="cart" size="24px" color="#333333"></wd-icon>
          <view v-if="cartCount > 0" class="badge">{{ cartCount > 99 ? '99+' : cartCount }}</view>
        </view>
      </view>
      
      <!-- 分类 Tab -->
      <scroll-view scroll-x class="category-tabs" :show-scrollbar="false">
        <view 
          class="tab-item" 
          v-for="cat in categories" 
          :key="cat.id"
          :class="{ active: currentCategory === cat.id }"
          @click="selectCategory(cat.id)"
        >
          <text class="name">{{ cat.name }}</text>
          <view class="indicator" v-if="currentCategory === cat.id"></view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 内容滚动区 -->
    <scroll-view scroll-y class="content-scroll" @scrolltolower="loadMore">
      <!-- 顶部占位 (Header高度 + Tab高度) -->
      <view class="header-placeholder"></view>
      
      <!-- 新人首单礼 Banner -->
      <view class="new-user-banner">
        <view class="banner-header">
          <view class="title-wrap">
            <text class="main-title">新人首单礼</text>
            <view class="tag">NEW</view>
          </view>
          <view class="action-btn">
            <text>领100券包</text>
            <wd-icon name="arrow-right" size="10px" color="#FFFFFF"></wd-icon>
          </view>
        </view>
        
        <scroll-view scroll-x class="goods-scroll" :show-scrollbar="false">
          <view class="goods-item" v-for="(item, index) in newArrivals" :key="index" @click="goDetail(item.id)">
            <view class="img-box">
              <image :src="item.image" mode="aspectFill" class="goods-img" />
            </view>
            <view class="price-row">
              <text class="symbol">¥</text>
              <text class="price">{{ item.price }}</text>
            </view>
            <view class="original-price">¥{{ item.original_price }}</view>
            <!-- 底部红色胶囊标签 -->
            <view class="bottom-tag">{{ item.tag }}</view>
          </view>
        </scroll-view>
      </view>
      
      <!-- 功能金刚区 (图标占位) -->
      <view class="grid-menu">
        <view class="grid-item" v-for="(item, index) in menuItems" :key="index" @click="handleMenuClick(item)">
          <!-- 使用统一的图标占位，实际项目中替换为图片 -->
          <view class="icon-placeholder" :class="item.bgClass">
            <!-- 暂时用 wd-icon 占位，之后可换 image -->
            <!-- <image :src="item.iconUrl" /> -->
          </view>
          <text class="label">{{ item.name }}</text>
        </view>
      </view>
      
      <!-- 营销卡片区 -->
      <view class="promo-cards">
        <view class="promo-card vip-card" @click="navigateTo('/pages/user/member')">
          <view class="card-content">
            <view class="card-header">
              <view class="vip-badge">VIP</view>
              <image src="/static/images/vip-icon.png" class="card-icon-placeholder" />
            </view>
            <text class="title">年卡</text>
            <text class="desc">买2年送1只智能手环</text>
            <view class="gift-row">
              <text class="gift-tag">送智能手环</text>
            </view>
          </view>
        </view>
        
        <view class="promo-card new-card">
          <view class="card-content">
            <view class="card-header">
              <view class="new-badge">新品</view>
              <image src="/static/images/scale-icon.png" class="card-icon-placeholder" />
            </view>
            <text class="title">智能体脂秤</text>
            <text class="desc">精准测量 24项数据</text>
            <view class="price-row">
              <text class="price-tag">¥89</text>
              <text class="unit">起</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 商品瀑布流 -->
      <view class="product-section">
        <view class="section-header">
          <text class="title">全部商品</text>
          <view class="filter-tags">
            <text class="tag active">综合</text>
            <text class="tag">销量</text>
            <text class="tag">价格</text>
          </view>
        </view>
        
        <view class="waterfall-grid">
          <view class="product-item" v-for="item in products" :key="item.id" @click="goDetail(item.id)">
            <view class="img-wrap">
              <image v-if="item.images?.[0]" :src="item.images[0]" mode="aspectFill" />
              <view class="placeholder" v-else>商品图</view>
            </view>
            <view class="info-wrap">
              <text class="name">{{ item.name }}</text>
              <view class="tags" v-if="item.tags && item.tags.length">
                <text class="tag" v-for="tag in item.tags" :key="tag">{{ tag }}</text>
              </view>
              <view class="price-row">
                <text class="price"><text class="symbol">¥</text>{{ item.current_price }}</text>
                <text class="sales">{{ item.sales_count || 0 }}人付款</text>
              </view>
            </view>
          </view>
        </view>
        
        <view class="loading-status">
          <text v-if="loading">加载中...</text>
          <text v-else-if="!hasMore">没有更多了</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'
import { getCategories, getProducts, getCartList } from '@/api/shop'

const userStore = useUserStore()

// 模拟数据 - 新人首单礼 (图片暂时使用占位)
const newArrivals = ref([
  { id: 1, price: '255', original_price: '279', tag: '必买精选', image: '' },
  { id: 2, price: '89', original_price: '121', tag: '热销爆款', image: '' },
  { id: 3, price: '55', original_price: '85', tag: '必买精选', image: '' },
  { id: 4, price: '79', original_price: '120', tag: '90天低价', image: '' }
])

// 模拟数据 - 金刚区 (移除 Emoji，使用背景色占位)
const menuItems = ref([
  { name: '赠网易云', bgClass: 'bg-1' },
  { name: '身体数据', bgClass: 'bg-2' },
  { name: '运动装备', bgClass: 'bg-3' },
  { name: '家用智能', bgClass: 'bg-4' },
  { name: '运动服饰', bgClass: 'bg-5' },
  { name: '户外装备', bgClass: 'bg-6' },
  { name: '健康食品', bgClass: 'bg-7' },
  { name: '全部分类', bgClass: 'bg-8' }
])

const categories = ref<any[]>([
  { id: 0, name: '全部' },
  { id: 1, name: '服饰' },
  { id: 2, name: '装备' },
  { id: 3, name: '食品' },
  { id: 4, name: '器械' },
  { id: 5, name: '周边' }
])

const products = ref<any[]>([])
const currentCategory = ref(0)
const page = ref(1)
const pageSize = 10
const total = ref(0)
const loading = ref(false)
const cartCount = ref(0)

const hasMore = computed(() => products.value.length < total.value)

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

function selectCategory(id: number) {
  currentCategory.value = id
  fetchProducts(true)
}

function loadMore() {
  if (hasMore.value && !loading.value) {
    page.value++
    fetchProducts()
  }
}

function goDetail(id: number) {
  uni.navigateTo({ url: `/pages/shop/detail?id=${id}` })
}

function goCart() {
  uni.navigateTo({ url: '/pages/cart/index' })
}

function goSearch() {
  uni.showToast({ title: '搜索功能开发中', icon: 'none' })
}

function goUser() {
  uni.switchTab({ url: '/pages/user/index' })
}

function navigateTo(url: string) {
  uni.navigateTo({ url })
}

function handleMenuClick(item: any) {
  uni.showToast({ title: `点击了${item.name}`, icon: 'none' })
}

onShow(() => {
  fetchProducts(true)
  fetchCartCount()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
}

.header-fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: #FFFFFF;
  padding-bottom: 0;
}

.top-bar {
  display: flex;
  align-items: center;
  padding: 10px 12px 6px; // 减少内边距
  gap: 12px;
  height: 44px;
  
  .user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    overflow: hidden;
    background: #F0F0F0;
    flex-shrink: 0;
    border: 1px solid #FFFFFF; // 增加白色边框
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    
    image {
      width: 100%;
      height: 100%;
    }
  }
  
  .search-box {
    flex: 1;
    height: 32px; // 略微调小高度
    background: #F5F5F7;
    border-radius: 16px;
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 6px;
    
    .placeholder {
      font-size: 13px;
      color: #999999;
    }
  }
  
  .cart-btn {
    position: relative;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .badge {
      position: absolute;
      top: -2px;
      right: -2px;
      min-width: 14px;
      height: 14px;
      line-height: 14px;
      background: #FF3B30;
      color: #FFFFFF;
      font-size: 9px;
      border-radius: 7px;
      text-align: center;
      padding: 0 3px;
      border: 1px solid #FFFFFF;
    }
  }
}

.category-tabs {
  white-space: nowrap;
  padding: 0 12px;
  height: 40px; // 固定高度
  
  .tab-item {
    display: inline-block;
    padding: 8px 4px;
    margin-right: 24px;
    position: relative;
    
    .name {
      font-size: 14px;
      color: #666666;
      font-weight: 400;
      transition: all 0.2s;
    }
    
    &.active {
      .name {
        color: #333333;
        font-size: 16px;
        font-weight: 600;
      }
      
      .indicator {
        position: absolute;
        bottom: 4px;
        left: 50%;
        transform: translateX(-50%);
        width: 16px; // 稍微加宽指示器
        height: 3px;
        background: #0071e3;
        border-radius: 2px;
      }
    }
  }
}

.content-scroll {
  height: 100vh;
}

.header-placeholder {
  height: 94px; // 44px(top-bar) + 40px(tabs) + padding
}

.new-user-banner {
  margin: 12px 12px;
  background: linear-gradient(180deg, #FF6B00 0%, #FF3B30 100%);
  border-radius: 16px;
  padding: 16px;
  color: #FFFFFF;
  
  .banner-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    .title-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .main-title {
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 0.5px;
      }
      
      .tag {
        background: #FFFFFF;
        color: #FF3B30;
        font-size: 10px;
        padding: 1px 5px;
        border-radius: 8px 8px 8px 0;
        font-weight: 800;
      }
    }
    
    .action-btn {
      background: rgba(255, 255, 255, 0.2);
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 11px;
      display: flex;
      align-items: center;
      gap: 2px;
      font-weight: 500;
    }
  }
  
  .goods-scroll {
    white-space: nowrap;
    
    .goods-item {
      display: inline-block;
      width: 100px;
      background: #FFFFFF;
      border-radius: 12px;
      padding: 8px;
      margin-right: 8px;
      text-align: center;
      position: relative; // 为底部标签定位
      
      .img-box {
        width: 84px;
        height: 84px;
        margin: 0 auto 8px;
        background: #F8F8F8;
        border-radius: 8px;
        
        .goods-img {
          width: 100%;
          height: 100%;
          border-radius: 8px;
        }
      }
      
      .price-row {
        color: #333333;
        font-weight: 700;
        font-size: 16px;
        line-height: 1;
        margin-bottom: 4px;
        
        .symbol { font-size: 11px; margin-right: 1px; }
      }
      
      .original-price {
        font-size: 10px;
        color: #999999;
        margin-bottom: 16px; // 留出标签空间
      }
      
      .bottom-tag {
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 9px;
        color: #FFFFFF;
        background: #FF3B30;
        padding: 2px 8px;
        border-radius: 10px;
        line-height: 1.2;
        white-space: nowrap;
      }
    }
  }
}

.grid-menu {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px 0;
  padding: 16px 0;
  background: #FFFFFF;
  margin: 0 12px 12px;
  border-radius: 16px;
  
  .grid-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    
    .icon-placeholder {
      width: 44px;
      height: 44px;
      border-radius: 16px;
      // 使用不同颜色作为占位
      &.bg-1 { background: #FFF0F0; }
      &.bg-2 { background: #E8F4FD; }
      &.bg-3 { background: #FFF0F5; }
      &.bg-4 { background: #E0F7FA; }
      &.bg-5 { background: #E8EAF6; }
      &.bg-6 { background: #F3E5F5; }
      &.bg-7 { background: #E8F5E9; }
      &.bg-8 { background: #F5F5F7; }
    }
    
    .label {
      font-size: 12px;
      color: #333333;
    }
  }
}

.promo-cards {
  display: flex;
  gap: 10px;
  padding: 0 12px 16px;
  
  .promo-card {
    flex: 1;
    height: 130px;
    border-radius: 16px;
    position: relative;
    overflow: hidden;
    
    .card-content {
      position: relative;
      z-index: 1;
      padding: 16px;
      height: 100%;
      display: flex;
      flex-direction: column;
      box-sizing: border-box;
    }
    
    .card-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      
      .card-icon-placeholder {
        width: 40px;
        height: 40px;
        opacity: 0; // 占位隐藏
      }
    }
    
    .title {
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 4px;
    }
    
    .desc {
      font-size: 11px;
      margin-bottom: auto;
    }
    
    .gift-row {
      margin-top: auto;
    }
    
    &.vip-card {
      background: #F2EBFF; // 浅紫色背景
      
      .vip-badge {
        background: #6236FF;
        color: #FFFFFF;
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 4px;
        align-self: flex-start;
      }
      
      .title { color: #4B3080; }
      .desc { color: #7A68A0; }
      
      .gift-tag {
        font-size: 10px;
        color: #6236FF;
        background: #FFFFFF;
        padding: 2px 8px;
        border-radius: 10px;
      }
    }
    
    &.new-card {
      background: #FFF0E6; // 浅橙色背景
      
      .new-badge {
        background: #FF3B30;
        color: #FFFFFF;
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 4px;
        align-self: flex-start;
      }
      
      .title { color: #8B2D00; }
      .desc { color: #A06040; }
      
      .price-row {
        display: flex;
        align-items: baseline;
        gap: 2px;
        margin-top: auto;
        
        .price-tag { color: #FF3B30; font-weight: 700; font-size: 16px; }
        .unit { color: #FF3B30; font-size: 11px; }
      }
    }
  }
}

.product-section {
  padding: 0 12px 20px;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    
    .title {
      font-size: 16px;
      font-weight: 600;
      color: #333333;
    }
    
    .filter-tags {
      display: flex;
      gap: 16px;
      
      .tag {
        font-size: 13px;
        color: #999999;
        
        &.active {
          color: #333333;
          font-weight: 600;
        }
      }
    }
  }
  
  .waterfall-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    
    .product-item {
      background: #FFFFFF;
      border-radius: 12px;
      overflow: hidden;
      
      .img-wrap {
        height: 170px;
        background: #F8F8F8;
        position: relative;
        
        image {
          width: 100%;
          height: 100%;
        }
        
        .placeholder {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-size: 12px;
          color: #CCCCCC;
        }
      }
      
      .info-wrap {
        padding: 10px;
        
        .name {
          font-size: 14px;
          color: #333333;
          line-height: 1.4;
          margin-bottom: 6px;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          overflow: hidden;
        }
        
        .tags {
          display: flex;
          flex-wrap: wrap;
          gap: 4px;
          margin-bottom: 8px;
          
          .tag {
            font-size: 9px;
            color: #FF3B30;
            border: 0.5px solid #FF3B30;
            padding: 1px 4px;
            border-radius: 4px;
          }
        }
        
        .price-row {
          display: flex;
          justify-content: space-between;
          align-items: flex-end;
          
          .price {
            color: #FF3B30;
            font-size: 16px;
            font-weight: 700;
            
            .symbol { font-size: 11px; margin-right: 1px; }
          }
          
          .sales {
            font-size: 10px;
            color: #999999;
          }
        }
      }
    }
  }
  
  .loading-status {
    text-align: center;
    padding: 20px 0;
    
    text {
      font-size: 12px;
      color: #999999;
    }
  }
}
</style>
