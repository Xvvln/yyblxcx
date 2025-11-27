<template>
  <view class="page">
    <!-- 订单状态 -->
    <view class="status-card" :class="'status-' + order.status">
      <view class="status-icon">
        <wd-icon :name="statusIcon" size="32px" color="#FFFFFF"></wd-icon>
      </view>
      <view class="status-info">
        <text class="status-text">{{ statusText }}</text>
        <text class="status-desc">{{ statusDesc }}</text>
      </view>
    </view>
    
    <!-- 收货地址 -->
    <view class="address-card" v-if="order.address">
      <wd-icon name="location" size="20px" color="#0071e3"></wd-icon>
      <view class="address-info">
        <view class="user-row">
          <text class="name">{{ order.address.name }}</text>
          <text class="phone">{{ order.address.phone }}</text>
        </view>
        <text class="detail">{{ order.address.province }}{{ order.address.city }}{{ order.address.district }}{{ order.address.detail }}</text>
      </view>
    </view>
    
    <!-- 商品信息 -->
    <view class="goods-card">
      <view class="goods-item" v-for="item in order.items" :key="item.id">
        <image :src="item.product?.images?.[0] || '/static/placeholder/product.png'" class="goods-image" mode="aspectFill" />
        <view class="goods-info">
          <text class="goods-name">{{ item.product?.name }}</text>
          <text class="goods-spec">{{ item.sku_name || '默认规格' }}</text>
          <view class="goods-footer">
            <text class="goods-price">¥{{ item.price }}</text>
            <text class="goods-count">x{{ item.quantity }}</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 订单信息 -->
    <view class="info-card">
      <view class="info-item">
        <text class="label">订单编号</text>
        <view class="value-wrap">
          <text class="value">{{ order.order_no }}</text>
          <text class="copy-btn" @click="copyOrderNo">复制</text>
        </view>
      </view>
      <view class="info-item">
        <text class="label">下单时间</text>
        <text class="value">{{ order.created_at }}</text>
      </view>
      <view class="info-item" v-if="order.pay_time">
        <text class="label">支付时间</text>
        <text class="value">{{ order.pay_time }}</text>
      </view>
      <view class="info-item" v-if="order.ship_time">
        <text class="label">发货时间</text>
        <text class="value">{{ order.ship_time }}</text>
      </view>
      <view class="info-item" v-if="order.finish_time">
        <text class="label">完成时间</text>
        <text class="value">{{ order.finish_time }}</text>
      </view>
      <view class="info-item">
        <text class="label">支付方式</text>
        <text class="value">{{ order.pay_type === 'wechat' ? '微信支付' : '其他' }}</text>
      </view>
    </view>
    
    <!-- 金额信息 -->
    <view class="amount-card">
      <view class="amount-item">
        <text class="label">商品金额</text>
        <text class="value">¥{{ order.goods_amount?.toFixed(2) }}</text>
      </view>
      <view class="amount-item">
        <text class="label">运费</text>
        <text class="value">{{ order.freight > 0 ? '¥' + order.freight?.toFixed(2) : '免运费' }}</text>
      </view>
      <view class="amount-item" v-if="order.discount > 0">
        <text class="label">优惠</text>
        <text class="value discount">-¥{{ order.discount?.toFixed(2) }}</text>
      </view>
      <view class="amount-item total">
        <text class="label">实付金额</text>
        <text class="value">¥{{ order.total_amount?.toFixed(2) }}</text>
      </view>
    </view>
    
    <!-- 底部操作 -->
    <view class="footer" v-if="order.status === 1 || order.status === 3">
      <button v-if="order.status === 1" class="btn" @click="cancelOrder">取消订单</button>
      <button v-if="order.status === 1" class="btn primary" @click="payOrder">去支付</button>
      <button v-if="order.status === 3" class="btn primary" @click="confirmReceipt">确认收货</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getOrderDetail, cancelOrder as apiCancelOrder, confirmOrder, payOrder as apiPayOrder } from '@/api/order'

const orderId = ref(0)
const order = ref<any>({})

const statusIcon = computed(() => {
  const icons: Record<number, string> = {
    1: 'time',
    2: 'logistics',
    3: 'logistics',
    4: 'check',
    5: 'close'
  }
  return icons[order.value.status] || 'goods'
})

const statusText = computed(() => {
  const texts: Record<number, string> = {
    1: '待付款',
    2: '待发货',
    3: '待收货',
    4: '交易完成',
    5: '已取消'
  }
  return texts[order.value.status] || ''
})

const statusDesc = computed(() => {
  const descs: Record<number, string> = {
    1: '请尽快完成支付',
    2: '商家正在备货',
    3: '商品已发出，请注意查收',
    4: '感谢您的购买',
    5: '订单已取消'
  }
  return descs[order.value.status] || ''
})

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  orderId.value = Number(currentPage.options?.id || 0)
  
  if (orderId.value) {
    fetchDetail()
  }
})

async function fetchDetail() {
  try {
    const res = await getOrderDetail(orderId.value)
    if (res.code === 200) {
      order.value = res.data
    }
  } catch (e) {
    console.error(e)
  }
}

function copyOrderNo() {
  uni.setClipboardData({
    data: order.value.order_no,
    success: () => {
      uni.showToast({ title: '已复制', icon: 'success' })
    }
  })
}

async function cancelOrder() {
  uni.showModal({
    title: '取消订单',
    content: '确定要取消此订单吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          const result = await apiCancelOrder(orderId.value)
          if (result.code === 200) {
            uni.showToast({ title: '已取消', icon: 'success' })
            order.value.status = 5
          }
        } catch (e: any) {
          uni.showToast({ title: e.message || '取消失败', icon: 'none' })
        }
      }
    }
  })
}

async function payOrder() {
  uni.showLoading({ title: '支付中...' })
  try {
    const res = await apiPayOrder(orderId.value, { pay_type: 'wechat' })
    if (res.code === 200) {
      uni.showToast({ title: '支付成功', icon: 'success' })
      order.value.status = 2
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '支付失败', icon: 'none' })
  } finally {
    uni.hideLoading()
  }
}

async function confirmReceipt() {
  uni.showModal({
    title: '确认收货',
    content: '确认已收到商品？',
    success: async (res) => {
      if (res.confirm) {
        try {
          const result = await confirmOrder(orderId.value)
          if (result.code === 200) {
            uni.showToast({ title: '已确认收货', icon: 'success' })
            order.value.status = 4
          }
        } catch (e: any) {
          uni.showToast({ title: e.message || '操作失败', icon: 'none' })
        }
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-bottom: 100px;
}

.status-card {
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  
  &.status-1 { background: linear-gradient(135deg, #FF9500 0%, #FFCC00 100%); }
  &.status-2 { background: linear-gradient(135deg, #0071e3 0%, #00C7BE 100%); }
  &.status-3 { background: linear-gradient(135deg, #34C759 0%, #30D158 100%); }
  &.status-4 { background: linear-gradient(135deg, #86868B 0%, #AEAEB2 100%); }
  &.status-5 { background: linear-gradient(135deg, #86868B 0%, #AEAEB2 100%); }
  
  .status-icon {
    width: 56px;
    height: 56px;
    background: rgba(255,255,255,0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .status-info {
    .status-text {
      font-size: 20px;
      font-weight: 600;
      color: #FFFFFF;
      display: block;
      margin-bottom: 4px;
    }
    
    .status-desc {
      font-size: 14px;
      color: rgba(255,255,255,0.8);
    }
  }
}

.address-card {
  background: #FFFFFF;
  margin: 16px;
  border-radius: 16px;
  padding: 16px;
  display: flex;
  gap: 12px;
  
  .address-info {
    flex: 1;
    
    .user-row {
      margin-bottom: 6px;
      
      .name {
        font-size: 15px;
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
}

.goods-card {
  background: #FFFFFF;
  margin: 0 16px 16px;
  border-radius: 16px;
  padding: 16px;
  
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

.info-card, .amount-card {
  background: #FFFFFF;
  margin: 0 16px 16px;
  border-radius: 16px;
  padding: 16px;
  
  .info-item, .amount-item {
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
    }
    
    .value-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .copy-btn {
        font-size: 12px;
        color: #0071e3;
      }
    }
  }
}

.amount-card {
  .amount-item {
    &.total {
      padding-top: 12px;
      border-top: 1px solid #F5F5F7;
      
      .label {
        font-weight: 600;
        color: #1D1D1F;
      }
      
      .value {
        font-size: 18px;
        font-weight: 700;
        color: #FF6B00;
      }
    }
    
    .discount {
      color: #34C759;
    }
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
  justify-content: flex-end;
  gap: 12px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .btn {
    padding: 10px 24px;
    font-size: 14px;
    border-radius: 20px;
    border: 1px solid #D2D2D7;
    background: #FFFFFF;
    color: #1D1D1F;
    
    &::after {
      border: none;
    }
    
    &.primary {
      background: #0071e3;
      border-color: #0071e3;
      color: #FFFFFF;
    }
  }
}
</style>
