<template>
  <view class="page">
    <view class="header">
      <text class="title">领券中心</text>
      <text class="desc">精选优惠券，限时领取</text>
    </view>
    
    <view class="coupon-list">
      <view 
        class="coupon-card" 
        v-for="coupon in availableCoupons" 
        :key="coupon.id"
        :class="{ received: coupon.is_received }"
      >
        <view class="coupon-left">
          <view class="amount-row">
            <text class="currency">¥</text>
            <text class="amount">{{ coupon.value }}</text>
          </view>
          <text class="condition">满{{ coupon.min_amount }}可用</text>
        </view>
        <view class="coupon-right">
          <text class="name">{{ coupon.name }}</text>
          <text class="scope">{{ coupon.type === 'percent' ? '折扣券' : '满减券' }}</text>
          <text class="expire">有效期至 {{ coupon.end_time }}</text>
          <text class="remaining">剩余 {{ coupon.remaining }} 张</text>
        </view>
        <view class="coupon-action">
          <button 
            v-if="!coupon.is_received" 
            class="receive-btn" 
            @click="receiveCoupon(coupon)"
            :loading="receivingId === coupon.id"
          >立即领取</button>
          <text v-else class="received-text">已领取</text>
        </view>
      </view>
      
      <view class="empty" v-if="availableCoupons.length === 0 && !loading">
        <wd-icon name="coupon" size="60px" color="#E5E5EA"></wd-icon>
        <text>暂无可领取的优惠券</text>
      </view>
      
      <view class="loading" v-if="loading">
        <wd-loading size="24px" />
        <text>加载中...</text>
      </view>
    </view>
    
    <!-- 使用说明 -->
    <view class="tips-section">
      <text class="tips-title">使用说明</text>
      <view class="tips-content">
        <text>1. 优惠券需在有效期内使用，过期作废</text>
        <text>2. 每张优惠券仅限使用一次</text>
        <text>3. 优惠券不可与其他优惠同时使用</text>
        <text>4. 订单取消后优惠券将自动退回</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getAvailableCoupons, receiveCoupon as apiReceiveCoupon } from '@/api/shop'

interface Coupon {
  id: number
  name: string
  type: string
  value: number
  min_amount: number
  max_discount?: number
  start_time: string
  end_time: string
  is_received: boolean
  remaining: number
}

const availableCoupons = ref<Coupon[]>([])
const loading = ref(false)
const receivingId = ref<number | null>(null)

onShow(() => {
  fetchAvailableCoupons()
})

async function fetchAvailableCoupons() {
  loading.value = true
  try {
    const res = await getAvailableCoupons()
    if (res.code === 200) {
      availableCoupons.value = res.data || []
    }
  } catch (e) {
    console.error('获取优惠券失败', e)
    // 使用模拟数据
    availableCoupons.value = [
      {
        id: 1,
        name: '新人专享券',
        type: 'fixed',
        value: 10,
        min_amount: 50,
        start_time: '2025-01-01',
        end_time: '2025-12-31',
        is_received: false,
        remaining: 100
      },
      {
        id: 2,
        name: '满100减20',
        type: 'fixed',
        value: 20,
        min_amount: 100,
        start_time: '2025-01-01',
        end_time: '2025-12-31',
        is_received: false,
        remaining: 50
      },
      {
        id: 3,
        name: '满200减50',
        type: 'fixed',
        value: 50,
        min_amount: 200,
        start_time: '2025-01-01',
        end_time: '2025-12-31',
        is_received: true,
        remaining: 20
      }
    ]
  } finally {
    loading.value = false
  }
}

async function receiveCoupon(coupon: Coupon) {
  if (coupon.is_received || receivingId.value) return
  
  receivingId.value = coupon.id
  try {
    const res = await apiReceiveCoupon(coupon.id)
    if (res.code === 200) {
      coupon.is_received = true
      coupon.remaining--
      uni.showToast({ title: '领取成功', icon: 'success' })
    } else {
      uni.showToast({ title: res.message || '领取失败', icon: 'none' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '领取失败', icon: 'none' })
  } finally {
    receivingId.value = null
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.header {
  background: linear-gradient(135deg, #0071e3 0%, #00c7be 100%);
  padding: 32px 20px;
  color: #FFFFFF;
  
  .title {
    font-size: 24px;
    font-weight: 700;
    display: block;
    margin-bottom: 8px;
  }
  
  .desc {
    font-size: 14px;
    opacity: 0.9;
  }
}

.coupon-list {
  padding: 16px;
}

.coupon-card {
  background: #FFFFFF;
  border-radius: 12px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  
  &.received {
    opacity: 0.7;
    
    .coupon-left {
      background: #AEAEB2;
    }
  }
  
  .coupon-left {
    width: 100px;
    padding: 20px 12px;
    background: linear-gradient(135deg, #0071e3 0%, #00c7be 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #FFFFFF;
    
    .amount-row {
      display: flex;
      align-items: baseline;
      
      .currency {
        font-size: 14px;
      }
      
      .amount {
        font-size: 32px;
        font-weight: 700;
      }
    }
    
    .condition {
      font-size: 11px;
      opacity: 0.9;
      margin-top: 4px;
    }
  }
  
  .coupon-right {
    flex: 1;
    padding: 16px;
    
    .name {
      font-size: 15px;
      font-weight: 600;
      color: #1D1D1F;
      display: block;
      margin-bottom: 4px;
    }
    
    .scope {
      font-size: 12px;
      color: #0071e3;
      background: #E8F4FD;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 6px;
    }
    
    .expire {
      font-size: 11px;
      color: #86868B;
      display: block;
      margin-bottom: 2px;
    }
    
    .remaining {
      font-size: 11px;
      color: #FF9500;
    }
  }
  
  .coupon-action {
    padding-right: 16px;
    
    .receive-btn {
      background: #0071e3;
      color: #FFFFFF;
      font-size: 12px;
      padding: 8px 16px;
      border-radius: 16px;
      border: none;
      
      &::after {
        border: none;
      }
    }
    
    .received-text {
      font-size: 12px;
      color: #86868B;
    }
  }
}

.empty {
  padding: 60px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  text {
    font-size: 14px;
    color: #86868B;
    margin-top: 16px;
  }
}

.loading {
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  
  text {
    font-size: 14px;
    color: #86868B;
  }
}

.tips-section {
  background: #FFFFFF;
  margin: 16px;
  padding: 20px;
  border-radius: 12px;
  
  .tips-title {
    font-size: 15px;
    font-weight: 600;
    color: #1D1D1F;
    display: block;
    margin-bottom: 12px;
  }
  
  .tips-content {
    text {
      display: block;
      font-size: 13px;
      color: #86868B;
      line-height: 2;
    }
  }
}
</style>












