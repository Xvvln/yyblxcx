<template>
  <view class="page">
    <!-- 顶部统计 -->
    <view class="stats-card">
      <view class="stat-item">
        <text class="value">{{ totalCount }}</text>
        <text class="label">运动次数</text>
      </view>
      <view class="stat-item">
        <text class="value">{{ totalDuration }}</text>
        <text class="label">累计时长(分)</text>
      </view>
      <view class="stat-item">
        <text class="value">{{ totalCalories }}</text>
        <text class="label">消耗千卡</text>
      </view>
    </view>

    <!-- 筛选栏 -->
    <view class="filter-bar">
      <view 
        class="filter-item" 
        :class="{ active: currentFilter === '' }"
        @click="setFilter('')"
      >全部</view>
      <view 
        class="filter-item" 
        :class="{ active: currentFilter === 'outdoor_run' }"
        @click="setFilter('outdoor_run')"
      >户外跑</view>
      <view 
        class="filter-item" 
        :class="{ active: currentFilter === 'treadmill' }"
        @click="setFilter('treadmill')"
      >跑步机</view>
      <view 
        class="filter-item" 
        :class="{ active: currentFilter === 'walk' }"
        @click="setFilter('walk')"
      >健走</view>
    </view>

    <!-- 记录列表 -->
    <scroll-view scroll-y class="record-list" @scrolltolower="loadMore">
      <view class="record-item" v-for="record in records" :key="record.id">
        <view class="record-header">
          <view class="type-icon">
            <text>{{ getTypeIcon(record.sport_type) }}</text>
          </view>
          <view class="record-info">
            <text class="type-name">{{ record.sport_name || getTypeName(record.sport_type) }}</text>
            <text class="time">{{ formatTime(record.start_time) }}</text>
          </view>
          <view class="coins">
            <text>+{{ record.coins_earned }}</text>
            <text class="coin-label">运动币</text>
          </view>
        </view>
        
        <view class="record-data">
          <view class="data-item">
            <text class="val">{{ record.duration }}</text>
            <text class="lbl">分钟</text>
          </view>
          <view class="data-item" v-if="record.distance">
            <text class="val">{{ (record.distance / 1000).toFixed(2) }}</text>
            <text class="lbl">公里</text>
          </view>
          <view class="data-item">
            <text class="val">{{ record.calories }}</text>
            <text class="lbl">千卡</text>
          </view>
          <view class="data-item">
            <text class="val">{{ getFeelingEmoji(record.feeling) }}</text>
            <text class="lbl">感受</text>
          </view>
        </view>
      </view>

      <view class="empty" v-if="!loading && records.length === 0">
        <text class="icon">🏃</text>
        <text class="text">还没有运动记录</text>
        <text class="sub">去运动吧，记录每一次进步</text>
      </view>

      <view class="loading" v-if="loading">
        <text>加载中...</text>
      </view>

      <view class="no-more" v-if="!hasMore && records.length > 0">
        <text>没有更多了</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getSportRecords } from '@/api/sport'

interface SportRecord {
  id: number
  sport_type: string
  sport_name?: string
  duration: number
  distance?: number
  calories: number
  coins_earned: number
  start_time: string
  feeling: number
}

const records = ref<SportRecord[]>([])
const loading = ref(false)
const currentFilter = ref('')
const page = ref(1)
const hasMore = ref(true)

const totalCount = computed(() => records.value.length)
const totalDuration = computed(() => records.value.reduce((sum, r) => sum + r.duration, 0))
const totalCalories = computed(() => records.value.reduce((sum, r) => sum + r.calories, 0))

onMounted(() => {
  fetchRecords(true)
})

async function fetchRecords(refresh = false) {
  if (loading.value) return
  
  if (refresh) {
    page.value = 1
    hasMore.value = true
  }
  
  loading.value = true
  try {
    const params: any = { page: page.value, page_size: 20 }
    if (currentFilter.value) {
      params.sport_type = currentFilter.value
    }
    
    const res = await getSportRecords(params)
    if (res.code === 200) {
      const list = res.data?.list || []
      if (refresh) {
        records.value = list
      } else {
        records.value.push(...list)
      }
      hasMore.value = list.length >= 20
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function setFilter(type: string) {
  currentFilter.value = type
  fetchRecords(true)
}

function loadMore() {
  if (hasMore.value && !loading.value) {
    page.value++
    fetchRecords()
  }
}

function getTypeIcon(type: string) {
  const icons: Record<string, string> = {
    'outdoor_run': '🏃',
    'treadmill': '🏃‍♂️',
    'walk': '🚶',
    'cycling': '🚴',
    'swimming': '🏊'
  }
  return icons[type] || '🏋️'
}

function getTypeName(type: string) {
  const names: Record<string, string> = {
    'outdoor_run': '户外跑',
    'treadmill': '跑步机',
    'walk': '健走',
    'cycling': '骑行',
    'swimming': '游泳'
  }
  return names[type] || '运动'
}

function getFeelingEmoji(feeling: number) {
  const emojis = ['', '😫', '😐', '🙂', '😊', '🤩']
  return emojis[feeling] || '🙂'
}

function formatTime(time: string) {
  const formattedTime = time.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(formattedTime)
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours().toString().padStart(2, '0')
  const minute = date.getMinutes().toString().padStart(2, '0')
  return `${month}月${day}日 ${hour}:${minute}`
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.stats-card {
  background: linear-gradient(135deg, #0071e3 0%, #00c7be 100%);
  margin: 16px;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  justify-content: space-around;
  
  .stat-item {
    text-align: center;
    
    .value {
      font-size: 28px;
      font-weight: 700;
      color: #FFFFFF;
      display: block;
    }
    
    .label {
      font-size: 12px;
      color: rgba(255,255,255,0.8);
      margin-top: 4px;
    }
  }
}

.filter-bar {
  display: flex;
  padding: 0 16px;
  margin-bottom: 12px;
  gap: 12px;
  
  .filter-item {
    padding: 8px 16px;
    background: #FFFFFF;
    border-radius: 20px;
    font-size: 13px;
    color: #86868B;
    
    &.active {
      background: #0071e3;
      color: #FFFFFF;
    }
  }
}

.record-list {
  height: calc(100vh - 250px);
  padding: 0 16px;
}

.record-item {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  
  .record-header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
    
    .type-icon {
      width: 44px;
      height: 44px;
      background: #F5F5F7;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      margin-right: 12px;
    }
    
    .record-info {
      flex: 1;
      
      .type-name {
        font-size: 16px;
        font-weight: 600;
        color: #1D1D1F;
        display: block;
      }
      
      .time {
        font-size: 12px;
        color: #86868B;
      }
    }
    
    .coins {
      text-align: right;
      
      text:first-child {
        font-size: 18px;
        font-weight: 700;
        color: #FF9500;
        display: block;
      }
      
      .coin-label {
        font-size: 10px;
        color: #86868B;
      }
    }
  }
  
  .record-data {
    display: flex;
    justify-content: space-around;
    padding-top: 12px;
    border-top: 1px solid #F5F5F7;
    
    .data-item {
      text-align: center;
      
      .val {
        font-size: 18px;
        font-weight: 600;
        color: #1D1D1F;
        display: block;
      }
      
      .lbl {
        font-size: 11px;
        color: #86868B;
      }
    }
  }
}

.empty {
  padding: 60px 20px;
  text-align: center;
  
  .icon {
    font-size: 48px;
    display: block;
    margin-bottom: 16px;
  }
  
  .text {
    font-size: 16px;
    color: #1D1D1F;
    display: block;
    margin-bottom: 8px;
  }
  
  .sub {
    font-size: 13px;
    color: #86868B;
  }
}

.loading, .no-more {
  text-align: center;
  padding: 20px;
  color: #86868B;
  font-size: 13px;
}
</style>

