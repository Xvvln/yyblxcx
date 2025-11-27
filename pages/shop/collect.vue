<template>
  <view class="page">
    <scroll-view scroll-y class="product-list" @scrolltolower="loadMore">
      <view class="product-item" v-for="item in list" :key="item.id" @click="viewProduct(item)">
        <image :src="item.product?.images?.[0] || '/static/placeholder/product.png'" class="product-image" mode="aspectFill" />
        <view class="product-info">
          <text class="name">{{ item.product?.name }}</text>
          <text class="desc">{{ item.product?.description }}</text>
          <view class="bottom-row">
            <text class="price">¥{{ item.product?.current_price }}</text>
            <view class="btns">
              <button class="btn cart" @click.stop="addToCart(item)">
                <wd-icon name="cart" size="16px" color="#0071e3"></wd-icon>
              </button>
              <button class="btn remove" @click.stop="removeCollect(item)">
                <wd-icon name="star-fill" size="16px" color="#FF9500"></wd-icon>
              </button>
            </view>
          </view>
        </view>
      </view>
      
      <view class="empty" v-if="list.length === 0 && !loading">
        <wd-icon name="star" size="60px" color="#E5E5EA"></wd-icon>
        <text>暂无收藏</text>
        <button class="go-shop-btn" @click="goShop">去逛逛</button>
      </view>
      
      <view class="loading" v-if="loading">
        <text>加载中...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && list.length > 0">
        <text>没有更多了</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getCollectList, uncollectProduct } from '@/api/shop'
import { addToCart as apiAddToCart } from '@/api/cart'

const list = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const hasMore = ref(true)

onShow(() => {
  page.value = 1
  hasMore.value = true
  fetchList()
})

async function fetchList() {
  if (loading.value) return
  
  loading.value = true
  try {
    const res = await getCollectList({ page: page.value, page_size: 20 })
    if (res.code === 200) {
      const data = res.data?.list || []
      if (page.value === 1) {
        list.value = data
      } else {
        list.value.push(...data)
      }
      hasMore.value = data.length >= 20
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function loadMore() {
  if (hasMore.value && !loading.value) {
    page.value++
    fetchList()
  }
}

function viewProduct(item: any) {
  uni.navigateTo({ url: `/pages/shop/detail?id=${item.product_id || item.product?.id}` })
}

async function addToCart(item: any) {
  try {
    const res = await apiAddToCart({
      product_id: item.product_id || item.product?.id,
      quantity: 1
    })
    if (res.code === 200) {
      uni.showToast({ title: '已加入购物车', icon: 'success' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '添加失败', icon: 'none' })
  }
}

async function removeCollect(item: any) {
  uni.showModal({
    title: '取消收藏',
    content: '确定取消收藏该商品吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          const productId = item.product_id || item.product?.id
          const result = await uncollectProduct(productId)
          if (result.code === 200) {
            // 从列表中移除
            const idx = list.value.findIndex(i => i.id === item.id)
            if (idx > -1) {
              list.value.splice(idx, 1)
            }
            uni.showToast({ title: '已取消收藏', icon: 'success' })
          }
        } catch (e: any) {
          uni.showToast({ title: e.message || '操作失败', icon: 'none' })
        }
      }
    }
  })
}

function goShop() {
  uni.switchTab({ url: '/pages/shop/index' })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.product-list {
  height: 100vh;
  padding: 16px;
  
  .product-item {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
    display: flex;
    
    .product-image {
      width: 100px;
      height: 100px;
      border-radius: 12px;
      margin-right: 12px;
      flex-shrink: 0;
    }
    
    .product-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      
      .name {
        font-size: 15px;
        font-weight: 500;
        color: #1D1D1F;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 1;
        overflow: hidden;
      }
      
      .desc {
        font-size: 12px;
        color: #86868B;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        overflow: hidden;
      }
      
      .bottom-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .price {
          font-size: 18px;
          font-weight: 700;
          color: #FF6B00;
        }
        
        .btns {
          display: flex;
          gap: 8px;
          
          .btn {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0;
            border: none;
            
            &.cart {
              background: #E8F4FD;
            }
            
            &.remove {
              background: #FFF3E0;
            }
            
            &::after {
              border: none;
            }
          }
        }
      }
    }
  }
}

.empty {
  padding: 80px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  text {
    font-size: 14px;
    color: #86868B;
    margin-top: 16px;
  }
  
  .go-shop-btn {
    margin-top: 24px;
    background: #0071e3;
    color: #FFFFFF;
    font-size: 14px;
    padding: 10px 32px;
    border-radius: 20px;
    border: none;
    
    &::after {
      border: none;
    }
  }
}

.loading, .no-more {
  padding: 20px;
  text-align: center;
  color: #86868B;
  font-size: 14px;
}
</style>
