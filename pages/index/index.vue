<template>
  <view class="page">
    <!-- 顶部背景区 -->
    <view class="header-bg"></view>
    
    <!-- 顶部状态栏占位 -->
    <view class="status-bar" :style="{ height: statusBarHeight + 'px' }"></view>
    
    <!-- 自定义导航栏 -->
    <view class="nav-bar">
      <view class="user-header" @click="handleUserClick">
        <image :src="userStore.userInfo?.avatar || '/static/placeholder/avatar.png'" class="nav-avatar" mode="aspectFill" />
        <view class="header-text">
          <text class="user-name">{{ userStore.nickname || '点击登录' }}</text>
          <text class="greeting-text">{{ greeting }}</text>
        </view>
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
      
      <!-- 核心数据仪表盘 -->
      <view class="health-dashboard">
        <view class="dashboard-header">
          <view class="header-left">
            <text class="title">健康概览</text>
            <text class="subtitle">今日数据</text>
          </view>
          <view class="header-right" @click="navigateTo('/pages/health/index')">
            <text>详情</text>
            <wd-icon name="arrow-right" size="14px" color="#86868B"></wd-icon>
          </view>
        </view>

        <view class="dashboard-content">
          <!-- 左侧：BMI 状态 -->
          <view class="bmi-card">
            <view class="ring-container">
              <svg class="bmi-ring" viewBox="0 0 100 100">
                <!-- 背景圆环 -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#F2F2F7" stroke-width="8" stroke-linecap="round" />
                <!-- 进度圆环 -->
                <circle 
                  cx="50" cy="50" r="40" 
                  fill="none" 
                  :stroke="bmiRingColor" 
                  stroke-width="8" 
                  stroke-linecap="round" 
                  stroke-dasharray="251.2" 
                  :stroke-dashoffset="251.2 - (251.2 * Math.min((overview.latest_bmi || 0) / 35, 1))" 
                  transform="rotate(-90 50 50)"
                />
              </svg>
              <view class="ring-content">
                <text class="status-text" :class="bmiStatusClass">{{ bmiStatusText }}</text>
                <text class="bmi-label">身体状态</text>
              </view>
            </view>
            <view class="bmi-advice">
              <text>{{ bmiAdvice }}</text>
            </view>
          </view>

          <!-- 右侧：身体数据与活动 -->
          <view class="stats-column">
            <!-- 身体数据 -->
            <view class="body-row">
              <view class="stat-box">
                <text class="label">BMI</text>
                <text class="val">{{ overview.latest_bmi || '--' }}</text>
              </view>
              <view class="divider-v"></view>
              <view class="stat-box">
                <text class="label">身高</text>
                <view class="value-group">
                  <text class="val">{{ userStore.userInfo?.height || '--' }}</text>
                  <text class="unit">cm</text>
                </view>
              </view>
              <view class="divider-v"></view>
              <view class="stat-box">
                <text class="label">体重</text>
                <view class="value-group">
                  <text class="val">{{ userStore.userInfo?.weight || '--' }}</text>
                  <text class="unit">kg</text>
                </view>
              </view>
            </view>

            <!-- 活动数据列表 -->
            <view class="activity-column">
              <!-- 筛查结果 -->
              <view class="activity-item" @click="navigateTo('/pages/health/result')">
                <view class="icon-circle health">
                  <wd-icon name="check-circle-fill" size="16px" color="#34C759"></wd-icon>
                </view>
                <view class="info">
                  <text class="label">筛查结果</text>
                  <view class="right-val">
                    <text class="val text-green">{{ overview.latest_screening?.result || '未筛查' }}</text>
                    <wd-icon name="arrow-right" size="12px" color="#C7C7CC"></wd-icon>
                  </view>
                </view>
              </view>

              <!-- 饮食摄入 -->
              <view class="activity-item">
                <view class="icon-circle food">
                  <wd-icon name="fill" size="16px" color="#FF9500"></wd-icon>
                </view>
                <view class="info">
                  <text class="label">今日摄入</text>
                  <text class="val">{{ overview.today_calories_in || 0 }}<text class="unit">千卡</text></text>
                </view>
              </view>

              <!-- 运动消耗 -->
              <view class="activity-item">
                <view class="icon-circle fire">
                  <wd-icon name="hot-fill" size="16px" color="#FF3B30"></wd-icon>
                </view>
                <view class="info">
                  <text class="label">运动消耗</text>
                  <text class="val">{{ overview.week_sport?.total_calories || 0 }}<text class="unit">千卡</text></text>
                </view>
              </view>

              <!-- 运动时长 -->
              <view class="activity-item">
                <view class="icon-circle sport">
                  <wd-icon name="play-circle-fill" size="16px" color="#0071e3"></wd-icon>
                </view>
                <view class="info">
                  <text class="label">运动时长</text>
                  <text class="val">{{ overview.week_sport?.total_duration || 0 }}<text class="unit">分</text></text>
                </view>
              </view>
            </view>
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

const bmiStatusText = computed(() => {
  const bmi = Number(overview.value.latest_bmi)
  if (!bmi) return '未知'
  if (bmi < 18.5) return '偏瘦'
  if (bmi < 24) return '健康'
  if (bmi < 28) return '偏胖'
  return '肥胖'
})

const bmiAdvice = computed(() => {
  const bmi = Number(overview.value.latest_bmi)
  if (!bmi) return '请完善信息'
  if (bmi < 18.5) return '注意补充营养'
  if (bmi < 24) return '继续保持哦'
  if (bmi < 28) return '适当多运动'
  return '科学减重'
})

const bmiRingColor = computed(() => {
  const bmi = Number(overview.value.latest_bmi)
  if (!bmi) return '#E5E5EA'
  if (bmi < 18.5) return '#FF9500'
  if (bmi < 24) return '#34C759'
  if (bmi < 28) return '#FF9500'
  return '#FF3B30'
})

const bmiStatusClass = computed(() => {
  const bmi = Number(overview.value.latest_bmi)
  if (!bmi) return 'unknown'
  if (bmi < 18.5) return 'thin'
  if (bmi < 24) return 'normal'
  if (bmi < 28) return 'fat'
  return 'obese'
})

function handleUserClick() {
  if (!userStore.isLoggedIn) {
    uni.navigateTo({ url: '/pages/login/index' })
  } else {
    uni.switchTab({ url: '/pages/user/index' })
  }
}

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
  
  .user-header {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .nav-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #FFFFFF;
      border: 2px solid #FFFFFF;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .header-text {
      display: flex;
      flex-direction: column;
      
      .user-name {
        font-size: 16px;
        font-weight: 600;
        color: #1D1D1F;
        line-height: 1.2;
      }
      
      .greeting-text {
        font-size: 11px;
        color: #86868B;
      }
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

.health-dashboard {
  margin: 0 20px 24px;
  background: #FFFFFF;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);

  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;

    .header-left {
      display: flex;
      flex-direction: column;
      
      .title {
        font-size: 18px;
        font-weight: 700;
        color: #1D1D1F;
        line-height: 1.2;
        margin-bottom: 2px;
      }
      
      .subtitle {
        font-size: 12px;
        color: #86868B;
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 4px;
      
      text {
        font-size: 13px;
        color: #86868B;
      }
    }
  }

  .dashboard-content {
    display: flex;
    gap: 24px;
  }

  .bmi-card {
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    
    .ring-container {
      width: 100px;
      height: 100px;
      position: relative;
      margin-bottom: 8px;

      .bmi-ring {
        width: 100%;
        height: 100%;
        // transform: rotate(-90deg); // Moved to HTML SVG transform
      }

      .ring-content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        align-items: center;

        .status-text {
          font-size: 20px;
          font-weight: 700;
          line-height: 1.2;
          letter-spacing: -0.5px;
          
          &.thin { color: #FF9500; }
          &.normal { color: #34C759; }
          &.fat { color: #FF9500; }
          &.obese { color: #FF3B30; }
          &.unknown { color: #86868B; }
        }

        .bmi-label {
          font-size: 11px;
          color: #86868B;
          margin-top: 2px;
          font-weight: 500;
        }
      }
    }

    .bmi-advice {
      background: #F5F5F7;
      padding: 4px 12px;
      border-radius: 12px;
      margin-top: 4px;

      text {
        font-size: 11px;
        font-weight: 500;
        color: #86868B;
      }
    }
  }

  .stats-column {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 16px;

    .body-row {
      display: flex;
      align-items: center;
      background: #F5F5F7;
      border-radius: 16px;
      padding: 12px 8px;
      
      .stat-box {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;

        .label {
          font-size: 11px;
          color: #86868B;
          margin-bottom: 4px;
        }

        .val {
          font-size: 16px;
          font-weight: 600;
          color: #1D1D1F;
        }

        .value-group {
          display: flex;
          align-items: baseline;
          gap: 1px;

          .val {
            font-size: 16px;
            font-weight: 600;
            color: #1D1D1F;
          }

          .unit {
            font-size: 10px;
            color: #86868B;
          }
        }
      }

      .divider-v {
        width: 1px;
        height: 20px;
        background: rgba(0,0,0,0.06);
        margin: 0 4px;
      }
    }

    .activity-column {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding-top: 4px;

      .activity-item {
        display: flex;
        align-items: center;
        gap: 12px;

        .icon-circle {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;

          &.sport { background: rgba(0, 113, 227, 0.1); }
          &.fire { background: rgba(255, 59, 48, 0.1); }
          &.health { background: rgba(52, 199, 89, 0.1); }
          &.food { background: rgba(255, 149, 0, 0.1); }
        }

        .info {
          flex: 1;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 0.5px solid rgba(0,0,0,0.05);
          padding-bottom: 8px;
          min-height: 32px;

          .label {
            font-size: 13px;
            color: #1D1D1F;
            font-weight: 500;
          }
          
          .right-val {
            display: flex;
            align-items: center;
            gap: 4px;
          }

          .val {
            font-size: 15px;
            font-weight: 600;
            color: #1D1D1F;
            font-family: "SF Pro Rounded", sans-serif;
            
            &.text-green { color: #34C759; }

            .unit {
              font-size: 11px;
              color: #86868B;
              margin-left: 2px;
              font-weight: 400;
            }
          }
        }
        
        &:last-child .info {
          border-bottom: none;
          padding-bottom: 0;
        }
      }
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
