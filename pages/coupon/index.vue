<template>
  <view class="page">
    <!-- 顶部栏 -->
    <view class="header-bar">
      <!-- 切换Tab -->
      <view class="tab-bar">
        <view 
          class="tab-item" 
          :class="{ active: currentTab === 'unused' }"
          @click="switchTab('available')"
        >可使用</view>
        <view 
          class="tab-item" 
          :class="{ active: currentTab === 'used' }"
          @click="switchTab('used')"
        >已使用</view>
        <view 
          class="tab-item" 
          :class="{ active: currentTab === 'expired' }"
          @click="switchTab('expired')"
        >已过期</view>
      </view>
      <view class="header-action" @click="goCouponCenter">
        <wd-icon name="coupon" size="16px" color="#0071e3"></wd-icon>
        <text>领券</text>
      </view>
    </view>

    <!-- 优惠券列表 -->
    <scroll-view scroll-y class="coupon-list" @scrolltolower="loadMore">
      <view 
        class="coupon-item" 
        v-for="coupon in filteredList" 
        :key="coupon.id"
        :class="{ disabled: currentTab !== 'unused' }"
      >
        <view class="coupon-left">
          <view class="amount-row">
            <text class="currency">¥</text>
            <text class="amount">{{ coupon.amount }}</text>
          </view>
          <text class="condition">满{{ coupon.min_amount }}可用</text>
        </view>
        <view class="coupon-right">
          <text class="name">{{ coupon.name }}</text>
          <text class="scope">{{ coupon.scope_desc || '全场通用' }}</text>
          <text class="expire">{{ coupon.expire_time }}</text>
        </view>
        <view class="coupon-action">
          <button 
            v-if="currentTab === 'unused'" 
            class="use-btn" 
            @click="useCoupon(coupon)"
          >去使用</button>
          <text v-else class="status-text">{{ currentTab === 'used' ? '已使用' : '已过期' }}</text>
        </view>
        <view class="coupon-tag" v-if="coupon.is_new">新</view>
      </view>

      <view class="empty" v-if="filteredList.length === 0 && !loading">
        <wd-icon name="coupon" size="60px" color="#E5E5EA"></wd-icon>
        <text>暂无优惠券</text>
        <button class="get-btn" @click="goCouponCenter">去领券</button>
      </view>

      <view class="loading" v-if="loading">
        <text>加载中...</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getMyCoupons } from '@/api/shop'

interface Coupon {
  id: number
  name: string
  amount: number
  min_amount: number
  scope_desc?: string
  expire_time: string
  status: string
  is_new?: boolean
}

const currentTab = ref('unused') // 使用后端期望的状态值
const list = ref<Coupon[]>([])
const loading = ref(false)
const page = ref(1)

// 状态映射：前端显示 -> 后端状态
const tabToStatus: Record<string, string> = {
  'available': 'unused',
  'used': 'used',
  'expired': 'expired'
}

const filteredList = computed(() => list.value)

onMounted(() => {
  fetchCoupons()
})

function switchTab(tab: string) {
  currentTab.value = tabToStatus[tab] || 'unused'
  fetchCoupons()
}

async function fetchCoupons() {
  loading.value = true
  try {
    const res = await getMyCoupons({ status: currentTab.value })
    if (res.code === 200) {
      // 转换后端数据格式
      list.value = (res.data?.list || []).map((item: any) => ({
        id: item.id,
        name: item.name,
        amount: item.type === 'fixed' ? item.value : item.value, // 固定金额或百分比
        min_amount: item.min_amount,
        scope_desc: item.type === 'percent' ? `${item.value}%折扣` : undefined,
        expire_time: item.end_time,
        status: item.status === 'unused' ? 'available' : item.status,
        is_new: false
      }))
    }
  } catch (e) {
    console.error(e)
    list.value = []
  } finally {
    loading.value = false
  }
}

function loadMore() {
  // 加载更多
}

function useCoupon(coupon: Coupon) {
  uni.switchTab({ url: '/pages/shop/index' })
}

function goCouponCenter() {
  uni.navigateTo({ url: '/pages/coupon/center' })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.header-bar {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  padding: 12px 16px;
  
  .header-action {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 12px;
    background: #E8F4FD;
    border-radius: 16px;
    
    text {
      font-size: 12px;
      color: #0071e3;
      font-weight: 500;
    }
  }
}

.tab-bar {
  display: flex;
  flex: 1;
  
  .tab-item {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #86868B;
    padding: 8px 0;
    position: relative;
    
    &.active {
      color: #0071e3;
      font-weight: 600;
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 24px;
        height: 3px;
        background: #0071e3;
        border-radius: 2px;
      }
    }
  }
}

.coupon-list {
  height: calc(100vh - 60px);
  padding: 16px;
}

.coupon-item {
  background: #FFFFFF;
  border-radius: 12px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  
  &.disabled {
    opacity: 0.6;
    
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
      margin-bottom: 6px;
    }
    
    .scope {
      font-size: 12px;
      color: #86868B;
      margin-bottom: 4px;
      display: block;
    }
    
    .expire {
      font-size: 11px;
      color: #AEAEB2;
    }
  }
  
  .coupon-action {
    padding-right: 16px;
    
    .use-btn {
      background: #0071e3;
      color: #FFFFFF;
      font-size: 12px;
      padding: 6px 14px;
      border-radius: 14px;
      border: none;
      
      &::after {
        border: none;
      }
    }
    
    .status-text {
      font-size: 12px;
      color: #AEAEB2;
    }
  }
  
  .coupon-tag {
    position: absolute;
    top: 0;
    right: 0;
    background: #FF3B30;
    color: #FFFFFF;
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 0 12px 0 8px;
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
  
  .get-btn {
    margin-top: 20px;
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

.loading {
  text-align: center;
  padding: 20px;
  color: #86868B;
  font-size: 14px;
}
</style>

