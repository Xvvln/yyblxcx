<template>
  <view class="page">
    <!-- 商品轮播图 -->
    <swiper class="product-swiper" :indicator-dots="true" :autoplay="true" :circular="true">
      <swiper-item v-for="(img, idx) in product.images" :key="idx">
        <image :src="img" mode="aspectFill" class="swiper-image" @click="previewImage(idx)" />
      </swiper-item>
      <swiper-item v-if="!product.images?.length">
        <view class="placeholder">
          <wd-icon name="picture" size="48px" color="#E5E5EA"></wd-icon>
        </view>
      </swiper-item>
    </swiper>
    
    <!-- 商品信息 -->
    <view class="info-section">
      <view class="price-row">
        <view class="price-info">
          <text class="currency">¥</text>
          <text class="price">{{ product.current_price }}</text>
          <text class="original-price" v-if="product.original_price > product.current_price">¥{{ product.original_price }}</text>
        </view>
        <view class="sales-info">
          <text>月销 {{ product.sales_count || 0 }}</text>
        </view>
      </view>
      <text class="title">{{ product.name }}</text>
      <text class="desc">{{ product.description }}</text>
      
      <view class="tags" v-if="product.tags?.length">
        <text class="tag" v-for="tag in product.tags" :key="tag">{{ tag }}</text>
      </view>
    </view>
    
    <!-- 规格选择 -->
    <view class="spec-section" @click="showSkuPicker = true">
      <text class="label">规格</text>
      <view class="spec-value">
        <text>{{ selectedSkuName || '请选择规格' }}</text>
        <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
      </view>
    </view>
    
    <!-- 服务保障 -->
    <view class="service-section">
      <view class="service-item">
        <wd-icon name="check-circle" size="14px" color="#34C759"></wd-icon>
        <text>正品保障</text>
      </view>
      <view class="service-item">
        <wd-icon name="check-circle" size="14px" color="#34C759"></wd-icon>
        <text>7天退换</text>
      </view>
      <view class="service-item">
        <wd-icon name="check-circle" size="14px" color="#34C759"></wd-icon>
        <text>极速发货</text>
      </view>
    </view>
    
    <!-- 商品详情 -->
    <view class="detail-section">
      <view class="section-title">商品详情</view>
      <view class="detail-content">
        <rich-text v-if="product.detail" :nodes="product.detail"></rich-text>
        <text v-else>暂无详情</text>
      </view>
    </view>
    
    <!-- 底部操作栏 -->
    <view class="footer">
      <view class="icons">
        <view class="icon-item" @click="goHome">
          <wd-icon name="home" size="22px" color="#86868B"></wd-icon>
          <text>首页</text>
        </view>
        <view class="icon-item" @click="goCart">
          <wd-badge :value="cartCount" :max="99" :hidden="!cartCount">
            <wd-icon name="cart" size="22px" color="#86868B"></wd-icon>
          </wd-badge>
          <text>购物车</text>
        </view>
        <view class="icon-item" @click="toggleCollect">
          <wd-icon :name="product.is_collected ? 'star-fill' : 'star'" size="22px" :color="product.is_collected ? '#FF9500' : '#86868B'"></wd-icon>
          <text>{{ product.is_collected ? '已收藏' : '收藏' }}</text>
        </view>
      </view>
      <view class="btns">
        <button class="btn add-cart" @click="addToCart">加入购物车</button>
        <button class="btn buy-now" @click="buyNow">立即购买</button>
      </view>
    </view>
    
    <!-- 规格选择弹窗 -->
    <wd-popup v-model="showSkuPicker" position="bottom" custom-style="border-radius: 20px 20px 0 0;">
      <view class="sku-picker">
        <view class="sku-header">
          <image :src="product.images?.[0] || '/static/placeholder/product.png'" class="sku-image" mode="aspectFill" />
          <view class="sku-info">
            <text class="sku-price">¥{{ selectedSku?.price || product.current_price }}</text>
            <text class="sku-stock">库存: {{ selectedSku?.stock || product.stock || 0 }}</text>
            <text class="sku-selected">已选: {{ selectedSkuName || '请选择规格' }}</text>
          </view>
          <view class="close-btn" @click="showSkuPicker = false">
            <wd-icon name="close" size="20px" color="#86868B"></wd-icon>
          </view>
        </view>
        
        <view class="sku-body">
          <view class="sku-group" v-for="(spec, sIdx) in product.specs" :key="sIdx">
            <text class="group-title">{{ spec.name }}</text>
            <view class="spec-values">
              <view 
                class="spec-value-item" 
                v-for="val in spec.values" 
                :key="val"
                :class="{ active: selectedSpecs[spec.name] === val }"
                @click="selectSpec(spec.name, val)"
              >{{ val }}</view>
            </view>
          </view>
          
          <view class="quantity-row">
            <text class="label">购买数量</text>
            <view class="quantity-ctrl">
              <view class="btn" @click="quantity > 1 && quantity--">-</view>
              <text class="num">{{ quantity }}</text>
              <view class="btn" @click="quantity++">+</view>
            </view>
          </view>
        </view>
        
        <view class="sku-footer">
          <button class="confirm-btn" @click="confirmSku">确定</button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getProductDetail, collectProduct, uncollectProduct } from '@/api/shop'
import { addToCart as apiAddToCart, getCartCount } from '@/api/cart'

const productId = ref(0)
const product = ref<any>({})
const showSkuPicker = ref(false)
const selectedSpecs = ref<Record<string, string>>({})
const quantity = ref(1)
const cartCount = ref(0)
const pendingAction = ref<'cart' | 'buy' | null>(null)

const selectedSku = computed(() => {
  if (!product.value.skus) return null
  return product.value.skus.find((sku: any) => {
    return Object.entries(selectedSpecs.value).every(([k, v]) => sku.specs?.[k] === v)
  })
})

const selectedSkuName = computed(() => {
  const values = Object.values(selectedSpecs.value)
  return values.length > 0 ? values.join(' ') : ''
})

onLoad((options) => {
  productId.value = Number(options?.id || 0)
  if (productId.value) {
    fetchProductDetail()
  }
  fetchCartCount()
})

async function fetchProductDetail() {
  try {
    const res = await getProductDetail(productId.value)
    if (res.code === 200) {
      product.value = res.data
    }
  } catch (e) {
    console.error(e)
  }
}

async function fetchCartCount() {
  try {
    const res = await getCartCount()
    if (res.code === 200) {
      cartCount.value = res.data?.count || 0
    }
  } catch (e) {
    console.error(e)
  }
}

function previewImage(index: number) {
  uni.previewImage({
    current: index,
    urls: product.value.images || []
  })
}

function selectSpec(name: string, value: string) {
  selectedSpecs.value[name] = value
}

function goHome() {
  uni.switchTab({ url: '/pages/index/index' })
}

function goCart() {
  uni.navigateTo({ url: '/pages/cart/index' })
}

async function toggleCollect() {
  try {
    if (product.value.is_collected) {
      await uncollectProduct(productId.value)
      product.value.is_collected = false
      uni.showToast({ title: '已取消收藏', icon: 'none' })
    } else {
      await collectProduct(productId.value)
      product.value.is_collected = true
      uni.showToast({ title: '收藏成功', icon: 'success' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '操作失败', icon: 'none' })
  }
}

function addToCart() {
  pendingAction.value = 'cart'
  if (product.value.specs?.length > 0 && !selectedSkuName.value) {
    showSkuPicker.value = true
  } else {
    doAddToCart()
  }
}

function buyNow() {
  pendingAction.value = 'buy'
  if (product.value.specs?.length > 0 && !selectedSkuName.value) {
    showSkuPicker.value = true
  } else {
    doBuyNow()
  }
}

function confirmSku() {
  showSkuPicker.value = false
  if (pendingAction.value === 'cart') {
    doAddToCart()
  } else if (pendingAction.value === 'buy') {
    doBuyNow()
  }
  pendingAction.value = null
}

async function doAddToCart() {
  try {
    const res = await apiAddToCart({
      product_id: productId.value,
      sku_id: selectedSku.value?.id,
      quantity: quantity.value
    })
    
    if (res.code === 200) {
      uni.showToast({ title: '已加入购物车', icon: 'success' })
      fetchCartCount()
    } else {
      uni.showToast({ title: res.message || '添加失败', icon: 'none' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '添加失败', icon: 'none' })
  }
}

function doBuyNow() {
  uni.navigateTo({
    url: `/pages/order/confirm?product_id=${productId.value}&quantity=${quantity.value}&sku_id=${selectedSku.value?.id || ''}`
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-bottom: 80px;
}

.product-swiper {
  height: 375px;
  background: #FFFFFF;
  
  .swiper-image {
    width: 100%;
    height: 100%;
  }
  
  .placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F5F5F7;
  }
}

.info-section {
  background: #FFFFFF;
  padding: 16px;
  margin-bottom: 12px;
  
  .price-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 12px;
    
    .price-info {
      display: flex;
      align-items: baseline;
      
      .currency {
        font-size: 14px;
        color: #FF6B00;
        font-weight: 600;
      }
      
      .price {
        font-size: 28px;
        color: #FF6B00;
        font-weight: 700;
      }
      
      .original-price {
        font-size: 14px;
        color: #86868B;
        text-decoration: line-through;
        margin-left: 8px;
      }
    }
    
    .sales-info {
      font-size: 12px;
      color: #86868B;
    }
  }
  
  .title {
    font-size: 18px;
    font-weight: 600;
    color: #1D1D1F;
    line-height: 1.4;
    display: block;
    margin-bottom: 8px;
  }
  
  .desc {
    font-size: 14px;
    color: #86868B;
    line-height: 1.5;
  }
  
  .tags {
    display: flex;
    gap: 8px;
    margin-top: 12px;
    
    .tag {
      background: #E8F4FD;
      color: #0071e3;
      font-size: 11px;
      padding: 4px 8px;
      border-radius: 4px;
    }
  }
}

.spec-section {
  background: #FFFFFF;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .label {
    font-size: 14px;
    color: #86868B;
  }
  
  .spec-value {
    display: flex;
    align-items: center;
    gap: 4px;
    
    text {
      font-size: 14px;
      color: #1D1D1F;
    }
  }
}

.service-section {
  background: #FFFFFF;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-around;
  
  .service-item {
    display: flex;
    align-items: center;
    gap: 4px;
    
    text {
      font-size: 12px;
      color: #86868B;
    }
  }
}

.detail-section {
  background: #FFFFFF;
  padding: 16px;
  
  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: #1D1D1F;
    margin-bottom: 16px;
    padding-left: 10px;
    border-left: 3px solid #0071e3;
  }
  
  .detail-content {
    font-size: 14px;
    color: #1D1D1F;
    line-height: 1.6;
  }
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #FFFFFF;
  padding: 8px 16px;
  padding-bottom: calc(8px + env(safe-area-inset-bottom));
  display: flex;
  align-items: center;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .icons {
    display: flex;
    margin-right: 12px;
    
    .icon-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 50px;
      
      text {
        font-size: 10px;
        color: #86868B;
        margin-top: 2px;
      }
    }
  }
  
  .btns {
    flex: 1;
    display: flex;
    
    .btn {
      flex: 1;
      height: 44px;
      font-size: 14px;
      font-weight: 600;
      border: none;
      
      &::after {
        border: none;
      }
      
      &.add-cart {
        background: #FF9500;
        color: #FFFFFF;
        border-radius: 22px 0 0 22px;
      }
      
      &.buy-now {
        background: #0071e3;
        color: #FFFFFF;
        border-radius: 0 22px 22px 0;
      }
    }
  }
}

.sku-picker {
  padding: 20px;
  
  .sku-header {
    display: flex;
    padding-bottom: 16px;
    border-bottom: 1px solid #F5F5F7;
    
    .sku-image {
      width: 100px;
      height: 100px;
      border-radius: 8px;
      margin-right: 12px;
    }
    
    .sku-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      
      .sku-price {
        font-size: 22px;
        font-weight: 700;
        color: #FF6B00;
        margin-bottom: 4px;
      }
      
      .sku-stock {
        font-size: 12px;
        color: #86868B;
        margin-bottom: 4px;
      }
      
      .sku-selected {
        font-size: 13px;
        color: #1D1D1F;
      }
    }
    
    .close-btn {
      padding: 8px;
    }
  }
  
  .sku-body {
    padding: 16px 0;
    max-height: 300px;
    overflow-y: auto;
    
    .sku-group {
      margin-bottom: 20px;
      
      .group-title {
        font-size: 14px;
        color: #86868B;
        margin-bottom: 12px;
        display: block;
      }
      
      .spec-values {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        
        .spec-value-item {
          padding: 8px 16px;
          background: #F5F5F7;
          border-radius: 6px;
          font-size: 14px;
          color: #1D1D1F;
          
          &.active {
            background: #E8F4FD;
            color: #0071e3;
            border: 1px solid #0071e3;
          }
        }
      }
    }
    
    .quantity-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .label {
        font-size: 14px;
        color: #86868B;
      }
      
      .quantity-ctrl {
        display: flex;
        align-items: center;
        
        .btn {
          width: 32px;
          height: 32px;
          background: #F5F5F7;
          border-radius: 4px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 18px;
          color: #1D1D1F;
        }
        
        .num {
          width: 50px;
          text-align: center;
          font-size: 16px;
        }
      }
    }
  }
  
  .sku-footer {
    .confirm-btn {
      width: 100%;
      height: 48px;
      background: #0071e3;
      color: #FFFFFF;
      font-size: 16px;
      font-weight: 600;
      border-radius: 24px;
      border: none;
      
      &::after {
        border: none;
      }
    }
  }
}
</style>
