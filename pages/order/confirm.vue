<template>
  <view class="page">
    <!-- 收货地址 -->
    <view class="address-card" @click="selectAddress">
      <view v-if="address" class="address-info">
        <view class="user-row">
          <text class="name">{{ address.name }}</text>
          <text class="phone">{{ address.phone }}</text>
        </view>
        <text class="detail">{{ address.province }}{{ address.city }}{{ address.district }}{{ address.detail }}</text>
      </view>
      <view v-else class="empty-address">
        <wd-icon name="location" size="24px" color="#86868B"></wd-icon>
        <text>请选择收货地址</text>
      </view>
      <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
    </view>
    
    <!-- 商品列表 -->
    <view class="goods-card">
      <view class="goods-item" v-for="item in orderItems" :key="item.id">
        <image :src="item.product?.images?.[0] || '/static/placeholder/product.png'" class="goods-image" mode="aspectFill" />
        <view class="goods-info">
          <text class="goods-name">{{ item.product?.name }}</text>
          <text class="goods-spec">{{ item.sku_name || '默认规格' }}</text>
          <view class="goods-footer">
            <text class="goods-price">¥{{ item.product?.current_price }}</text>
            <text class="goods-count">x{{ item.quantity }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 订单信息 -->
    <view class="order-info">
      <view class="info-item">
        <text class="label">商品金额</text>
        <text class="value">¥{{ goodsAmount.toFixed(2) }}</text>
      </view>
      <view class="info-item">
        <text class="label">运费</text>
        <text class="value">{{ freight > 0 ? '¥' + freight.toFixed(2) : '免运费' }}</text>
      </view>
      <view class="info-item" v-if="discount > 0">
        <text class="label">优惠</text>
        <text class="value discount">-¥{{ discount.toFixed(2) }}</text>
      </view>
    </view>
    
    <!-- 备注 -->
    <view class="remark-section">
      <text class="label">订单备注</text>
      <input v-model="remark" placeholder="选填，请输入备注信息" />
    </view>
    
    <!-- 底部支付栏 -->
    <view class="footer">
      <view class="total-info">
        <text class="label">合计：</text>
        <text class="total-price">¥{{ totalAmount.toFixed(2) }}</text>
      </view>
      <button class="pay-btn" @click="submitOrder" :loading="submitting" :disabled="!address">
        提交订单
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getCartList } from '@/api/cart'
import { getAddressList } from '@/api/user'
import { createOrder } from '@/api/order'

const orderItems = ref<any[]>([])
const address = ref<any>(null)
const remark = ref('')
const submitting = ref(false)
const fromCart = ref(true) // 是否从购物车来
const directBuy = ref<any>(null) // 直接购买的商品

// 选中的地址（从地址页返回）
const selectedAddress = ref<any>(null)

const goodsAmount = computed(() => {
  return orderItems.value.reduce((sum, item) => {
    return sum + (item.product?.current_price || 0) * item.quantity
  }, 0)
})

const freight = computed(() => {
  // 满99免运费
  return goodsAmount.value >= 99 ? 0 : 10
})

const discount = ref(0)

const totalAmount = computed(() => {
  return goodsAmount.value + freight.value - discount.value
})

onMounted(async () => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  
  // 判断来源
  if (currentPage.options?.product_id) {
    // 直接购买
    fromCart.value = false
    directBuy.value = {
      product_id: currentPage.options.product_id,
      quantity: Number(currentPage.options.quantity || 1)
    }
    // TODO: 获取商品信息
  }
  
  await fetchData()
})

onShow(() => {
  // 检查是否从地址页返回
  if (selectedAddress.value) {
    address.value = selectedAddress.value
  }
})

async function fetchData() {
  // 获取购物车商品
  if (fromCart.value) {
    try {
      const res = await getCartList()
      if (res.code === 200) {
        // 只获取选中的商品
        orderItems.value = (res.data?.list || []).filter((item: any) => item.selected)
      }
    } catch (e) {
      console.error(e)
    }
  }
  
  // 获取默认地址
  try {
    const res = await getAddressList()
    if (res.code === 200) {
      const list = res.data?.list || []
      address.value = list.find((a: any) => a.is_default) || list[0]
    }
  } catch (e) {
    console.error(e)
  }
}

function selectAddress() {
  uni.navigateTo({ url: '/pages/address/index?select=1' })
}

async function submitOrder() {
  if (!address.value) {
    uni.showToast({ title: '请选择收货地址', icon: 'none' })
    return
  }
  
  if (orderItems.value.length === 0) {
    uni.showToast({ title: '请选择商品', icon: 'none' })
    return
  }
  
  submitting.value = true
  try {
    const res = await createOrder({
      address_id: address.value.id,
      items: orderItems.value.map(item => ({
        product_id: item.product?.id || item.product_id,
        sku_id: item.sku_id,
        quantity: item.quantity
      })),
      remark: remark.value,
      from_cart: fromCart.value
    })
    
    if (res.code === 200) {
      // 跳转支付
      const orderId = res.data?.order_id
      uni.showModal({
        title: '订单提交成功',
        content: `订单金额：¥${totalAmount.value.toFixed(2)}`,
        confirmText: '去支付',
        success: (result) => {
          if (result.confirm) {
            // 模拟支付
            uni.showLoading({ title: '支付中...' })
            setTimeout(() => {
              uni.hideLoading()
              uni.showToast({ title: '支付成功', icon: 'success' })
              setTimeout(() => {
                uni.redirectTo({ url: '/pages/order/index' })
              }, 1500)
            }, 1500)
          } else {
            uni.redirectTo({ url: '/pages/order/index' })
          }
        }
      })
    } else {
      uni.showToast({ title: res.message || '提交失败', icon: 'none' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '提交失败', icon: 'none' })
  } finally {
    submitting.value = false
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding: 16px;
  padding-bottom: 100px;
}

.address-card {
  background: #FFFFFF;
  padding: 16px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  
  .address-info {
    flex: 1;
    
    .user-row {
      margin-bottom: 6px;
      
      .name {
        font-size: 16px;
        font-weight: 600;
        margin-right: 12px;
      }
      
      .phone {
        font-size: 14px;
        color: #86868B;
      }
    }
    
    .detail {
      font-size: 14px;
      color: #1D1D1F;
      line-height: 1.4;
    }
  }
  
  .empty-address {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
    
    text {
      font-size: 15px;
      color: #86868B;
    }
  }
}

.goods-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
  
  .goods-item {
    display: flex;
    margin-bottom: 16px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .goods-image {
      width: 80px;
      height: 80px;
      border-radius: 8px;
      margin-right: 12px;
    }
    
    .goods-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      
      .goods-name {
        font-size: 14px;
        color: #1D1D1F;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        overflow: hidden;
      }
      
      .goods-spec {
        font-size: 12px;
        color: #86868B;
      }
      
      .goods-footer {
        display: flex;
        justify-content: space-between;
        
        .goods-price {
          font-size: 15px;
          font-weight: 600;
          color: #FF6B00;
        }
        
        .goods-count {
          font-size: 13px;
          color: #86868B;
        }
      }
    }
  }
}

.order-info {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
  
  .info-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .label {
      font-size: 14px;
      color: #86868B;
    }
    
    .value {
      font-size: 14px;
      color: #1D1D1F;
      
      &.discount {
        color: #34C759;
      }
    }
  }
}

.remark-section {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 16px;
  display: flex;
  align-items: center;
  
  .label {
    font-size: 14px;
    color: #1D1D1F;
    margin-right: 12px;
  }
  
  input {
    flex: 1;
    font-size: 14px;
  }
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #FFFFFF;
  padding: 12px 16px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .total-info {
    .label {
      font-size: 14px;
      color: #86868B;
    }
    
    .total-price {
      font-size: 20px;
      font-weight: 700;
      color: #FF6B00;
    }
  }
  
  .pay-btn {
    background: #0071e3;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 600;
    padding: 12px 32px;
    border-radius: 24px;
    border: none;
    
    &:disabled {
      background: #E5E5EA;
    }
    
    &::after {
      border: none;
    }
  }
}
</style>
