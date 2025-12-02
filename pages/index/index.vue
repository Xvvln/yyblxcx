<template>
  <view class="page">
    <!-- 顶部背景区 -->
    <view class="header-bg"></view>
    
    <!-- 顶部状态栏占位 -->
    <view class="status-bar" :style="{ height: statusBarHeight + 'px' }"></view>
    
    <!-- 自定义导航栏 -->
    <view class="nav-bar">
      <view class="date-info">
        <text class="date-text">{{ currentDate }}</text>
        <text class="greeting">{{ greeting }}，{{ userStore.nickname }}</text>
      </view>
      <view class="nav-right" @click="navigateTo('/pages/message/index')">
        <wd-icon name="bell" size="22px" color="#1D1D1F"></wd-icon>
        <view v-if="unreadCount > 0" class="badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</view>
      </view>
    </view>
    
    <scroll-view scroll-y class="content-scroll" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }" @scrolltolower="onScrollToLower">
      <!-- 轮播图 -->
      <swiper v-if="banners.length" class="banner-swiper" indicator-dots autoplay circular>
        <swiper-item v-for="banner in banners" :key="banner.id" @click="handleBannerClick(banner)">
          <image v-if="banner.image_url" :src="banner.image_url" mode="aspectFill" class="banner-image" />
          <view v-else class="banner-placeholder">
            <text>{{ banner.title || '轮播图' }}</text>
          </view>
        </swiper-item>
      </swiper>
      
      <!-- 签到卡片 -->
      <view class="checkin-card" @click="handleCheckin">
        <view class="checkin-left">
          <view class="checkin-icon">
            <wd-icon name="calendar-circle" size="24px" color="#0071e3"></wd-icon>
          </view>
          <view class="checkin-info">
            <text class="checkin-title">{{ checkinStatus.is_checked_in ? '今日已签到' : '每日签到' }}</text>
            <text class="checkin-desc">连续签到 {{ checkinStatus.continuous_days || 0 }} 天</text>
          </view>
        </view>
        <view class="checkin-btn" :class="{ disabled: checkinStatus.is_checked_in }">
          {{ checkinStatus.is_checked_in ? '已领取' : `+${(checkinStatus.base_reward || 5) * (checkinStatus.tomorrow_reward_multiplier || 1)}` }}
        </view>
      </view>
      
      <!-- 核心数据大卡片 -->
      <view class="health-hero-card">
        <view class="score-circle">
          <view class="score-inner">
            <text class="score-val">{{ overview.latest_bmi || '--' }}</text>
            <text class="score-label">BMI</text>
          </view>
          <svg class="progress-ring" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="6" />
            <circle cx="50" cy="50" r="45" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-dasharray="283" :stroke-dashoffset="283 - (283 * Math.min((overview.latest_bmi || 0) / 30 * 100, 100) / 100)" stroke-linecap="round" transform="rotate(-90 50 50)" />
          </svg>
        </view>
        
        <view class="hero-stats">
          <view class="stat-item">
            <text class="stat-val">{{ overview.week_sport?.total_duration || 0 }}</text>
            <text class="stat-key">本周运动(分钟)</text>
          </view>
          <view class="divider"></view>
          <view class="stat-item">
            <text class="stat-val">{{ overview.week_sport?.total_calories || 0 }}</text>
            <text class="stat-key">消耗(kcal)</text>
          </view>
        </view>
      </view>
      
      <!-- 快捷入口 -->
      <view class="quick-actions">
        <view class="action-capsule" @click="navigateTo('/pages/sport/index')">
          <view class="icon-box sport-bg">
            <wd-icon name="play-circle-fill" size="24px" color="#0071e3"></wd-icon>
          </view>
          <text class="name">去运动</text>
        </view>
        <view class="action-capsule" @click="navigateTo('/pages/food/index')">
          <view class="icon-box food-bg">
            <wd-icon name="goods" size="24px" color="#34C759"></wd-icon>
          </view>
          <text class="name">记饮食</text>
        </view>
        <view class="action-capsule" @click="navigateTo('/pages/health/index')">
          <view class="icon-box health-bg">
            <wd-icon name="warn-bold" size="24px" color="#FF9500"></wd-icon>
          </view>
          <text class="name">做筛查</text>
        </view>
        <view class="action-capsule" @click="navigateTo('/pages/ai/index')">
          <view class="icon-box ai-bg">
            <wd-icon name="chat" size="24px" color="#0071e3"></wd-icon>
          </view>
          <text class="name">问AI</text>
        </view>
        <view class="action-capsule" @click="navigateTo('/pages/doctor/index')">
          <view class="icon-box doctor-bg">
            <wd-icon name="user" size="24px" color="#FF3B30"></wd-icon>
          </view>
          <text class="name">问医生</text>
        </view>
      </view>
      
      <!-- 今日任务 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">今日目标</text>
          <text class="section-more" @click="navigateTo('/pages/user/points')">查看全部 ></text>
        </view>
        <view class="task-cards">
          <view class="task-card" v-for="task in dailyTasks" :key="task.id">
            <view class="task-left">
              <view class="checkbox" :class="{ checked: task.is_completed }">
                <wd-icon v-if="task.is_completed" name="check" size="14px" color="#FFFFFF"></wd-icon>
              </view>
              <view class="task-info">
                <text class="task-title">{{ task.name }}</text>
                <text class="task-reward">+{{ task.reward_amount }} {{ task.reward_coin_type === 'sport' ? '运动币' : '膳食币' }}</text>
              </view>
            </view>
            <view 
              class="task-btn" 
              :class="{ done: task.is_claimed, claimable: task.is_completed && !task.is_claimed }"
              @click="handleTaskAction(task)"
            >
              {{ task.is_claimed ? '已领取' : (task.is_completed ? '领取' : '去完成') }}
            </view>
          </view>
          <view v-if="!dailyTasks.length" class="empty-task">
            <text>暂无任务</text>
          </view>
        </view>
      </view>
      
      <!-- 积分信息 -->
      <view class="section">
        <view class="section-header">
          <text class="section-title">我的积分</text>
        </view>
        <view class="coins-card">
          <view class="coin-item">
            <view class="coin-icon-wrap sport">
              <wd-icon name="play-circle-fill" size="24px" color="#0071e3"></wd-icon>
            </view>
            <view class="coin-info">
              <text class="coin-val">{{ userStore.sportCoins }}</text>
              <text class="coin-name">运动币</text>
            </view>
          </view>
          <view class="coin-divider"></view>
          <view class="coin-item">
            <view class="coin-icon-wrap food">
              <wd-icon name="goods" size="24px" color="#34C759"></wd-icon>
            </view>
            <view class="coin-info">
              <text class="coin-val">{{ userStore.foodCoins }}</text>
              <text class="coin-name">膳食币</text>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 底部留白 -->
      <view style="height: 120px;"></view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad, onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'
import { getBanners, getOverview } from '@/api/home'
import { getCheckinStatus, dailyCheckin, getDailyTasks, claimTaskReward } from '@/api/points'
import { getUnreadCount } from '@/api/message'
import dayjs from 'dayjs'

const userStore = useUserStore()

// 状态栏高度
const statusBarHeight = ref(20)
const banners = ref<any[]>([])
const overview = ref<any>({})
const checkinStatus = ref<any>({})
const dailyTasks = ref<any[]>([])
const unreadCount = ref(0)

const currentDate = computed(() => {
  return dayjs().format('MM月DD日 dddd')
})

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 6) return '凌晨好'
  if (hour < 9) return '早上好'
  if (hour < 12) return '上午好'
  if (hour < 14) return '中午好'
  if (hour < 17) return '下午好'
  if (hour < 19) return '傍晚好'
  return '晚上好'
})

// 页面跳转
function navigateTo(url: string) {
  uni.navigateTo({ url })
}

// 获取轮播图
async function fetchBanners() {
  try {
    const res = await getBanners('home')
    if (res.code === 200) {
      banners.value = res.data || []
    }
  } catch (e) {
    console.error('获取轮播图失败', e)
  }
}

// 获取数据概览
async function fetchOverview() {
  try {
    const res = await getOverview()
    if (res.code === 200) {
      overview.value = res.data || {}
    }
  } catch (e) {
    console.error('获取概览失败', e)
  }
}

// 获取签到状态
async function fetchCheckinStatus() {
  try {
    const res = await getCheckinStatus()
    if (res.code === 200) {
      checkinStatus.value = res.data || {}
    }
  } catch (e) {
    console.error('获取签到状态失败', e)
  }
}

// 获取今日任务
async function fetchDailyTasks() {
  try {
    const res = await getDailyTasks()
    if (res.code === 200) {
      dailyTasks.value = res.data || []
    }
  } catch (e) {
    console.error('获取任务失败', e)
  }
}

// 获取未读消息数
async function fetchUnreadCount() {
  try {
    const res = await getUnreadCount()
    if (res.code === 200) {
      unreadCount.value = res.data?.count || 0
    }
  } catch (e) {
    console.error('获取未读数失败', e)
  }
}

// 处理签到
async function handleCheckin() {
  if (checkinStatus.value.is_checked_in) {
    uni.showToast({ title: '今日已签到', icon: 'none' })
    return
  }
  
  try {
    const res = await dailyCheckin()
    if (res.code === 200) {
      uni.showToast({ 
        title: `签到成功！+${res.data.sport_coins_earned + res.data.food_coins_earned}积分`, 
        icon: 'success' 
      })
      fetchCheckinStatus()
      userStore.fetchUserInfo()
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '签到失败', icon: 'none' })
  }
}

// 处理任务操作
async function handleTaskAction(task: any) {
  if (task.is_claimed) return
  
  if (!task.is_completed) {
    // 跳转去完成任务
    if (task.task_type === 'sport') {
      navigateTo('/pages/sport/index')
    } else if (task.task_type === 'food') {
      navigateTo('/pages/food/index')
    } else if (task.task_type === 'checkin') {
      handleCheckin()
    } else {
      navigateTo('/pages/health/basic-info')
    }
    return
  }
  
  // 领取奖励
  try {
    const res = await claimTaskReward(task.id)
    if (res.code === 200) {
      uni.showToast({ title: `领取成功！+${res.data.reward_amount}`, icon: 'success' })
      fetchDailyTasks()
      userStore.fetchUserInfo()
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '领取失败', icon: 'none' })
  }
}

// 轮播图点击
function handleBannerClick(banner: any) {
  if (banner.link_type === 'page' && banner.link_value) {
    uni.navigateTo({ url: banner.link_value })
  } else if (banner.link_type === 'product' && banner.link_value) {
    uni.navigateTo({ url: `/pages/shop/detail?id=${banner.link_value}` })
  }
}

function onScrollToLower() {
  // 触底加载更多
}

// 加载数据
async function loadData() {
  if (!userStore.isLoggedIn) {
    // 未登录时只加载轮播图
    fetchBanners()
    return
  }
  
  await Promise.all([
    fetchBanners(),
    fetchOverview(),
    fetchCheckinStatus(),
    fetchDailyTasks(),
    fetchUnreadCount(),
    userStore.fetchUserInfo()
  ])
}

// 页面加载
onLoad(() => {
  // 获取系统信息
  uni.getSystemInfo({
    success: (res) => {
      statusBarHeight.value = res.statusBarHeight || 20
    }
  })
})

// 每次显示时刷新
onShow(() => {
  if (typeof uni.getTabBar === 'function' && uni.getTabBar()) {
    uni.getTabBar().setData({
      selected: 0
    })
  }
  loadData()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
  position: relative;
}

.header-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 280px;
  background: linear-gradient(180deg, #E8F4FD 0%, #F5F5F7 100%);
  z-index: 0;
}

.status-bar {
  position: relative;
  z-index: 10;
}

.nav-bar {
  height: 44px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 10;
  
  .date-info {
    display: flex;
    flex-direction: column;
    
    .date-text {
      font-size: 12px;
      color: #86868B;
      font-weight: 500;
    }
    
    .greeting {
      font-size: 18px;
      font-weight: 700;
      color: #1D1D1F;
    }
  }
  
  .nav-right {
    position: relative;
    padding: 8px;
    
    .badge {
      position: absolute;
      top: 4px;
      right: 4px;
      min-width: 16px;
      height: 16px;
      background: #FF3B30;
      border-radius: 8px;
      font-size: 10px;
      color: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 4px;
    }
  }
}

.content-scroll {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.banner-swiper {
  margin: 10px 20px;
  height: 140px;
  border-radius: 16px;
  overflow: hidden;
  
  .banner-image {
    width: 100%;
    height: 100%;
  }
  
  .banner-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #0071e3 0%, #34C759 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    
    text {
      color: #FFFFFF;
      font-size: 18px;
      font-weight: 600;
    }
  }
}

.checkin-card {
  margin: 16px 20px;
  padding: 16px 20px;
  background: #FFFFFF;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  
  .checkin-left {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .checkin-icon {
      width: 44px;
      height: 44px;
      background: #E8F4FD;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .checkin-info {
      display: flex;
      flex-direction: column;
      
      .checkin-title {
        font-size: 15px;
        font-weight: 600;
        color: #1D1D1F;
      }
      
      .checkin-desc {
        font-size: 12px;
        color: #86868B;
        margin-top: 2px;
      }
    }
  }
  
  .checkin-btn {
    padding: 8px 20px;
    background: #0071e3;
    border-radius: 20px;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 600;
    
    &.disabled {
      background: #E5E5EA;
      color: #86868B;
    }
  }
}

.health-hero-card {
  margin: 0 20px 24px;
  background: #0071e3;
  border-radius: 24px;
  padding: 30px 24px;
  color: #FFFFFF;
  box-shadow: 0 10px 30px rgba(0, 113, 227, 0.25);
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    transform: scale(2);
  }
  
  .score-circle {
    width: 120px;
    height: 120px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    
    .score-inner {
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 2;
      
      .score-val {
        font-size: 36px;
        font-weight: 800;
        line-height: 1;
      }
      
      .score-label {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 4px;
      }
    }
    
    .progress-ring {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
  }
  
  .hero-stats {
    display: flex;
    width: 100%;
    justify-content: space-around;
    align-items: center;
    
    .stat-item {
      text-align: center;
      
      .stat-val {
        font-size: 24px;
        font-weight: 700;
        display: block;
        margin-bottom: 4px;
      }
      
      .stat-key {
        font-size: 12px;
        opacity: 0.7;
      }
    }
    
    .divider {
      width: 1px;
      height: 24px;
      background: rgba(255,255,255,0.2);
    }
  }
}

.quick-actions {
  display: flex;
  justify-content: space-between;
  padding: 0 16px;
  margin-bottom: 32px;
  
  .action-capsule {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    
    .icon-box {
      width: 50px;
      height: 50px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      transition: transform 0.1s;
      
      &:active {
        transform: scale(0.95);
      }
      
      &.sport-bg { background: #E8F4FD; }
      &.food-bg { background: #E3F9E5; }
      &.health-bg { background: #FFF3E0; }
      &.ai-bg { background: #E8F4FD; }
      &.doctor-bg { background: #FFE5E5; }
    }
    
    .name {
      font-size: 11px;
      color: #1D1D1F;
      font-weight: 500;
    }
  }
}

.section {
  margin-bottom: 24px;
  padding: 0 20px;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    .section-title {
      font-size: 18px;
      font-weight: 700;
      color: #1D1D1F;
    }
    
    .section-more {
      font-size: 13px;
      color: #86868B;
    }
  }
}

.task-cards {
  .task-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    
    .task-left {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .checkbox {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 2px solid #E5E5EA;
        display: flex;
        align-items: center;
        justify-content: center;
        
        &.checked {
          background: #34C759;
          border-color: #34C759;
        }
      }
      
      .task-info {
        display: flex;
        flex-direction: column;
        
        .task-title {
          font-size: 15px;
          font-weight: 600;
          color: #1D1D1F;
          margin-bottom: 2px;
        }
        
        .task-reward {
          font-size: 12px;
          color: #FF9500;
          font-weight: 500;
        }
      }
    }
    
    .task-btn {
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      background: #F5F5F7;
      color: #1D1D1F;
      
      &.claimable {
        background: #0071e3;
        color: #FFFFFF;
      }
      
      &.done {
        background: transparent;
        color: #86868B;
      }
    }
  }
  
  .empty-task {
    text-align: center;
    padding: 32px;
    color: #86868B;
    font-size: 14px;
  }
}

.coins-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  
  .coin-item {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    
    .coin-icon-wrap {
      width: 48px;
      height: 48px;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &.sport {
        background: #E8F4FD;
      }
      
      &.food {
        background: #E3F9E5;
      }
    }
    
    .coin-info {
      display: flex;
      flex-direction: column;
      
      .coin-val {
        font-size: 24px;
        font-weight: 700;
        color: #1D1D1F;
      }
      
      .coin-name {
        font-size: 12px;
        color: #86868B;
      }
    }
  }
  
  .coin-divider {
    width: 1px;
    height: 40px;
    background: #E5E5EA;
  }
}
</style>
