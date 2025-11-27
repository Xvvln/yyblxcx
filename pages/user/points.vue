<template>
  <view class="page">
    <!-- 顶部积分卡 -->
    <view class="points-card">
      <view class="points-row">
        <view class="points-item">
          <text class="label">运动币</text>
          <text class="value">{{ userStore.sportCoins }}</text>
        </view>
        <view class="divider"></view>
        <view class="points-item">
          <text class="label">膳食币</text>
          <text class="value">{{ userStore.foodCoins }}</text>
        </view>
      </view>
      <view class="tips">
        <wd-icon name="info-circle" size="14px" color="#86868B"></wd-icon>
        <text>积分可用于兑换商城礼品或抵扣购物</text>
      </view>
    </view>

    <!-- 切换tab -->
    <view class="tab-bar">
      <view 
        class="tab-item" 
        :class="{ active: currentTab === 'sport' }"
        @click="currentTab = 'sport'"
      >运动币</view>
      <view 
        class="tab-item" 
        :class="{ active: currentTab === 'food' }"
        @click="currentTab = 'food'"
      >膳食币</view>
    </view>
    
    <!-- 积分记录列表 -->
    <scroll-view scroll-y class="list" @scrolltolower="loadMore">
      <view class="item" v-for="item in filteredList" :key="item.id">
        <view class="left">
          <view class="icon-wrap" :class="item.amount > 0 ? 'plus' : 'minus'">
            <wd-icon :name="item.amount > 0 ? 'add' : 'decrease'" size="16px" :color="item.amount > 0 ? '#34C759' : '#FF3B30'"></wd-icon>
          </view>
          <view class="info">
            <text class="desc">{{ item.description }}</text>
            <text class="time">{{ formatTime(item.created_at) }}</text>
          </view>
        </view>
        <text class="amount" :class="{ plus: item.amount > 0 }">
          {{ item.amount > 0 ? '+' : '' }}{{ item.amount }}
        </text>
      </view>
      
      <view class="empty" v-if="filteredList.length === 0 && !loading">
        <text>暂无积分记录</text>
      </view>
      
      <view class="loading" v-if="loading">
        <text>加载中...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && filteredList.length > 0">
        <text>没有更多了</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getPointsRecords } from '@/api/points'

const userStore = useUserStore()
const currentTab = ref('sport')
const list = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const hasMore = ref(true)

const filteredList = computed(() => {
  return list.value.filter(item => item.coin_type === currentTab.value)
})

watch(currentTab, () => {
  page.value = 1
  list.value = []
  hasMore.value = true
  fetchRecords()
})

onMounted(() => {
  fetchRecords()
})

async function fetchRecords() {
  if (loading.value) return
  
  loading.value = true
  try {
    const res = await getPointsRecords({
      coin_type: currentTab.value,
      page: page.value,
      page_size: 20
    })
    
    if (res.code === 200) {
      const records = res.data?.list || []
      if (page.value === 1) {
        list.value = records
      } else {
        list.value.push(...records)
      }
      hasMore.value = records.length >= 20
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
    fetchRecords()
  }
}

function formatTime(time: string) {
  if (!time) return ''
  const formattedTime = time.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(formattedTime)
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hour = date.getHours().toString().padStart(2, '0')
  const minute = date.getMinutes().toString().padStart(2, '0')
  return `${month}-${day} ${hour}:${minute}`
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.points-card {
  background: linear-gradient(135deg, #0071e3 0%, #00c7be 100%);
  margin: 16px;
  border-radius: 20px;
  padding: 24px;
  
  .points-row {
    display: flex;
    align-items: center;
    
    .points-item {
      flex: 1;
      text-align: center;
      
      .label {
        font-size: 13px;
        color: rgba(255,255,255,0.8);
        display: block;
        margin-bottom: 8px;
      }
      
      .value {
        font-size: 32px;
        font-weight: 700;
        color: #FFFFFF;
      }
    }
    
    .divider {
      width: 1px;
      height: 40px;
      background: rgba(255,255,255,0.3);
    }
  }
  
  .tips {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.2);
    
    text {
      font-size: 12px;
      color: rgba(255,255,255,0.8);
    }
  }
}

.tab-bar {
  display: flex;
  background: #FFFFFF;
  margin: 0 16px;
  border-radius: 12px;
  padding: 4px;
  
  .tab-item {
    flex: 1;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    color: #86868B;
    border-radius: 8px;
    
    &.active {
      background: #0071e3;
      color: #FFFFFF;
      font-weight: 600;
    }
  }
}

.list {
  height: calc(100vh - 280px);
  background: #FFFFFF;
  margin: 16px;
  border-radius: 16px;
  padding: 0 16px;
  
  .item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    border-bottom: 1px solid #F5F5F7;
    
    &:last-child {
      border-bottom: none;
    }
    
    .left {
      display: flex;
      align-items: center;
      
      .icon-wrap {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        
        &.plus {
          background: #E8F9E9;
        }
        
        &.minus {
          background: #FFEBEE;
        }
      }
      
      .info {
        .desc {
          font-size: 15px;
          color: #1D1D1F;
          display: block;
          margin-bottom: 4px;
        }
        
        .time {
          font-size: 12px;
          color: #86868B;
        }
      }
    }
    
    .amount {
      font-size: 18px;
      font-weight: 600;
      color: #FF3B30;
      
      &.plus {
        color: #34C759;
      }
    }
  }
}

.empty, .loading, .no-more {
  text-align: center;
  padding: 40px 0;
  color: #86868B;
  font-size: 14px;
}
</style>
