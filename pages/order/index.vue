<template>
  <view class="page">
    <wd-tabs v-model="currentStatus" sticky @change="onTabChange">
      <wd-tab title="全部" :name="0"></wd-tab>
      <wd-tab title="待付款" :name="1"></wd-tab>
      <wd-tab title="待发货" :name="2"></wd-tab>
      <wd-tab title="待收货" :name="3"></wd-tab>
      <wd-tab title="已完成" :name="4"></wd-tab>
    </wd-tabs>
    
    <scroll-view scroll-y class="order-list" @scrolltolower="loadMore">
      <view class="order-item" v-for="order in orderList" :key="order.id" @click="viewDetail(order)">
        <view class="header">
          <text class="order-no">订单号: {{ order.order_no }}</text>
          <text class="status" :class="'status-' + order.status">{{ statusText(order.status) }}</text>
        </view>
        
        <view class="goods-list">
          <view class="goods-item" v-for="goods in order.items" :key="goods.id">
            <image :src="goods.product?.images?.[0] || '/static/placeholder/product.png'" class="goods-image" mode="aspectFill" />
            <view class="goods-info">
              <text class="name">{{ goods.product?.name }}</text>
              <text class="spec">{{ goods.sku_name || '默认规格' }}</text>
            </view>
            <view class="price-col">
              <text class="price">¥{{ goods.price }}</text>
              <text class="count">x{{ goods.quantity }}</text>
            </view>
          </view>
        </view>
        
        <view class="footer">
          <text class="total">共{{ order.total_quantity }}件，合计: <text class="price">¥{{ order.total_amount }}</text></text>
          <view class="btns">
            <button v-if="order.status === 1" class="btn cancel" @click.stop="cancelOrder(order)">取消订单</button>
            <button v-if="order.status === 1" class="btn primary" @click.stop="payOrder(order)">去支付</button>
            <button v-if="order.status === 3" class="btn primary" @click.stop="confirmReceipt(order)">确认收货</button>
            <button v-if="order.status === 4" class="btn" @click.stop="reviewOrder(order)">评价</button>
            <button v-if="order.status === 4" class="btn" @click.stop="buyAgain(order)">再次购买</button>
          </view>
        </view>
      </view>
      
      <view class="empty" v-if="orderList.length === 0 && !loading">
        <wd-icon name="goods" size="60px" color="#E5E5EA"></wd-icon>
        <text>暂无订单</text>
      </view>
      
      <view class="loading" v-if="loading">
        <text>加载中...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && orderList.length > 0">
        <text>没有更多了</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getOrderList, cancelOrder as apiCancelOrder, confirmOrder, payOrder as apiPayOrder } from '@/api/order'

const currentStatus = ref(0)
const orderList = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const hasMore = ref(true)

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  if (currentPage.options?.status) {
    currentStatus.value = Number(currentPage.options.status)
  }
})

onShow(() => {
  page.value = 1
  hasMore.value = true
  fetchOrders()
})

function onTabChange() {
  page.value = 1
  hasMore.value = true
  orderList.value = []
  fetchOrders()
}

async function fetchOrders() {
  if (loading.value) return
  
  loading.value = true
  try {
    const res = await getOrderList({
      status: currentStatus.value === 0 ? undefined : currentStatus.value,
      page: page.value,
      page_size: 10
    })
    
    if (res.code === 200) {
      const list = res.data?.list || []
      if (page.value === 1) {
        orderList.value = list
      } else {
        orderList.value.push(...list)
      }
      hasMore.value = list.length >= 10
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
    fetchOrders()
  }
}

function statusText(status: number) {
  const map: Record<number, string> = {
    1: '待付款',
    2: '待发货',
    3: '待收货',
    4: '已完成',
    5: '已取消'
  }
  return map[status] || ''
}

function viewDetail(order: any) {
  uni.navigateTo({ url: `/pages/order/detail?id=${order.id}` })
}

async function cancelOrder(order: any) {
  uni.showModal({
    title: '取消订单',
    content: '确定要取消此订单吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          const result = await apiCancelOrder(order.id)
          if (result.code === 200) {
            uni.showToast({ title: '已取消', icon: 'success' })
            order.status = 5
          }
        } catch (e: any) {
          uni.showToast({ title: e.message || '取消失败', icon: 'none' })
        }
      }
    }
  })
}

async function payOrder(order: any) {
  uni.showLoading({ title: '支付中...' })
  try {
    const res = await apiPayOrder(order.id, { pay_type: 'wechat' })
    if (res.code === 200) {
      uni.showToast({ title: '支付成功', icon: 'success' })
      order.status = 2
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '支付失败', icon: 'none' })
  } finally {
    uni.hideLoading()
  }
}

async function confirmReceipt(order: any) {
  uni.showModal({
    title: '确认收货',
    content: '确认已收到商品？',
    success: async (res) => {
      if (res.confirm) {
        try {
          const result = await confirmOrder(order.id)
          if (result.code === 200) {
            uni.showToast({ title: '已确认收货', icon: 'success' })
            order.status = 4
          }
        } catch (e: any) {
          uni.showToast({ title: e.message || '操作失败', icon: 'none' })
        }
      }
    }
  })
}

function reviewOrder(order: any) {
  uni.showToast({ title: '评价功能开发中', icon: 'none' })
}

function buyAgain(order: any) {
  // 将订单商品加入购物车
  uni.showToast({ title: '已加入购物车', icon: 'success' })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.order-list {
  height: calc(100vh - 44px);
  padding: 16px;
  
  .order-item {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
    
    .header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 12px;
      
      .order-no {
        font-size: 13px;
        color: #86868B;
      }
      
      .status {
        font-size: 13px;
        font-weight: 500;
        
        &.status-1 { color: #FF9500; }
        &.status-2 { color: #0071e3; }
        &.status-3 { color: #34C759; }
        &.status-4 { color: #86868B; }
        &.status-5 { color: #86868B; }
      }
    }
    
    .goods-item {
      display: flex;
      margin-bottom: 12px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .goods-image {
        width: 70px;
        height: 70px;
        border-radius: 8px;
        margin-right: 12px;
      }
      
      .goods-info {
        flex: 1;
        
        .name {
          font-size: 14px;
          color: #1D1D1F;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          overflow: hidden;
          margin-bottom: 4px;
        }
        
        .spec {
          font-size: 12px;
          color: #86868B;
        }
      }
      
      .price-col {
        text-align: right;
        
        .price {
          font-size: 14px;
          color: #1D1D1F;
          display: block;
        }
        
        .count {
          font-size: 12px;
          color: #86868B;
        }
      }
    }
    
    .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid #F5F5F7;
      
      .total {
        font-size: 13px;
        color: #86868B;
        
        .price {
          font-size: 15px;
          font-weight: 600;
          color: #1D1D1F;
        }
      }
      
      .btns {
        display: flex;
        gap: 8px;
        
        .btn {
          padding: 6px 14px;
          font-size: 13px;
          border-radius: 16px;
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
          
          &.cancel {
            color: #86868B;
          }
        }
      }
    }
  }
}

.empty {
  padding: 80px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  
  text {
    font-size: 14px;
    color: #86868B;
  }
}

.loading, .no-more {
  padding: 20px;
  text-align: center;
  color: #86868B;
  font-size: 14px;
}
</style>
