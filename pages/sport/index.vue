<template>
  <view class="page">
    <!-- 顶部地图背景 -->
    <view class="map-header">
      <!-- 真实地图组件 -->
      <map 
        class="sport-map"
        :latitude="location.latitude" 
        :longitude="location.longitude"
        :scale="16"
        :show-location="true"
        :enable-zoom="false"
        :enable-scroll="false"
        :polyline="polyline"
      />
      <view class="top-mask"></view>
      
      <!-- 顶部状态栏 -->
      <view class="status-bar">
        <view class="back-btn" @click="goBack">
          <wd-icon name="arrow-left" size="20px" color="#FFF"></wd-icon>
        </view>
        <view class="mode-switch">
          <text 
            v-for="mode in sportModes" 
            :key="mode.type"
            :class="{ active: currentMode === mode.type }"
            @click="switchMode(mode.type)"
          >{{ mode.name }}</text>
        </view>
        <view class="settings-icon" @click="goHistory">
          <wd-icon name="list" size="20px" color="#FFF"></wd-icon>
        </view>
      </view>
    </view>
    
    <!-- 底部数据卡片 -->
    <view class="data-panel">
      <view class="main-data">
        <text class="label">累计距离 (公里)</text>
        <text class="value">{{ distance }}</text>
      </view>
      
      <view class="sub-data-row">
        <view class="sub-item">
          <text class="val">{{ duration }}</text>
          <text class="lbl">时长</text>
        </view>
        <view class="sub-item">
          <text class="val">{{ pace }}</text>
          <text class="lbl">配速</text>
        </view>
        <view class="sub-item">
          <text class="val">{{ kcal }}</text>
          <text class="lbl">千卡</text>
        </view>
      </view>
      
      <!-- 运动控制按钮 -->
      <view class="control-area">
        <view class="btn-circle small" v-if="isRunning" @click="lockScreen">
          <wd-icon name="lock" size="24px" color="#333"></wd-icon>
        </view>
        
        <view class="btn-circle large" :class="{ running: isRunning, paused: isPaused }" @click="toggleSport">
          <text class="btn-text">{{ isRunning ? (isPaused ? '继续' : '暂停') : 'GO' }}</text>
        </view>
        
        <view class="btn-circle small danger" v-if="isPaused" @click="finishSport">
          <wd-icon name="close" size="24px" color="#FF3B30"></wd-icon>
        </view>
        <view class="btn-circle small" v-else-if="isRunning" @click="playMusic">
          <wd-icon name="music" size="24px" color="#333"></wd-icon>
        </view>
      </view>
      
      <text class="tips" v-if="!isRunning">点击 GO 开始记录</text>
      <text class="tips" v-else-if="isPaused">点击继续或结束运动</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted, onMounted, reactive } from 'vue'
import { submitSportRecord } from '@/api/sport'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const sportModes = [
  { type: 'outdoor_run', name: '户外跑' },
  { type: 'treadmill', name: '跑步机' },
  { type: 'walk', name: '健走' },
]

const currentMode = ref('outdoor_run')
const isRunning = ref(false)
const isPaused = ref(false)
const timer = ref<any>(null)
const locationTimer = ref<any>(null)
const durationSec = ref(0)
const distanceVal = ref(0)
const startTime = ref<Date | null>(null)

// 定位相关
const location = reactive({
  latitude: 39.908823,
  longitude: 116.397470
})
const trackPoints = ref<{latitude: number, longitude: number}[]>([])

// 轨迹线
const polyline = computed(() => {
  if (trackPoints.value.length < 2) return []
  return [{
    points: trackPoints.value,
    color: '#0071e3',
    width: 6,
    arrowLine: true
  }]
})

// 获取当前位置
function getCurrentLocation() {
  uni.getLocation({
    type: 'gcj02',
    success: (res) => {
      location.latitude = res.latitude
      location.longitude = res.longitude
      
      // 如果正在运动，记录轨迹点
      if (isRunning.value && !isPaused.value) {
        const lastPoint = trackPoints.value[trackPoints.value.length - 1]
        if (lastPoint) {
          // 计算与上一点的距离
          const dist = calculateDistance(
            lastPoint.latitude, lastPoint.longitude,
            res.latitude, res.longitude
          )
          distanceVal.value += dist
        }
        trackPoints.value.push({
          latitude: res.latitude,
          longitude: res.longitude
        })
      }
    },
    fail: (err) => {
      console.error('获取位置失败', err)
    }
  })
}

// 计算两点间距离（公里）
function calculateDistance(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const rad = Math.PI / 180
  const R = 6371 // 地球半径（公里）
  const dLat = (lat2 - lat1) * rad
  const dLng = (lng2 - lng1) * rad
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * rad) * Math.cos(lat2 * rad) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

// 初始化获取位置
onMounted(() => {
  getCurrentLocation()
})

const distance = computed(() => distanceVal.value.toFixed(2))
const kcal = computed(() => Math.floor(durationSec.value * 0.15))

const duration = computed(() => {
  const h = Math.floor(durationSec.value / 3600)
  const m = Math.floor((durationSec.value % 3600) / 60)
  const s = durationSec.value % 60
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

const pace = computed(() => {
  if (distanceVal.value <= 0) return "0'00\""
  const paceMinutes = durationSec.value / 60 / distanceVal.value
  const mins = Math.floor(paceMinutes)
  const secs = Math.round((paceMinutes - mins) * 60)
  return `${mins}'${secs.toString().padStart(2, '0')}"`
})

function switchMode(mode: string) {
  if (!isRunning.value) {
    currentMode.value = mode
  }
}

function toggleSport() {
  if (!isRunning.value) {
    // 开始运动
    isRunning.value = true
    isPaused.value = false
    startTime.value = new Date()
    trackPoints.value = []
    distanceVal.value = 0
    
    // 记录起始点
    getCurrentLocation()
    
    // 计时器
    timer.value = setInterval(() => {
      durationSec.value++
    }, 1000)
    
    // 位置追踪（每3秒更新一次）
    locationTimer.value = setInterval(() => {
      getCurrentLocation()
    }, 3000)
    
  } else if (!isPaused.value) {
    // 暂停
    isPaused.value = true
    if (timer.value) {
      clearInterval(timer.value)
      timer.value = null
    }
    if (locationTimer.value) {
      clearInterval(locationTimer.value)
      locationTimer.value = null
    }
  } else {
    // 继续
    isPaused.value = false
    timer.value = setInterval(() => {
      durationSec.value++
    }, 1000)
    locationTimer.value = setInterval(() => {
      getCurrentLocation()
    }, 3000)
  }
}

async function finishSport() {
  if (durationSec.value < 60) {
    uni.showToast({ title: '运动时间太短', icon: 'none' })
    resetSport()
    return
  }
  
  uni.showModal({
    title: '结束运动',
    content: `本次运动${duration.value}，将被保存到记录`,
    success: async (res) => {
      if (res.confirm) {
        await saveRecord()
      } else {
        // 取消结束，可以继续
      }
    }
  })
}

async function saveRecord() {
  uni.showLoading({ title: '保存中' })
  
  try {
    const endTime = new Date()
    const res = await submitSportRecord({
      sport_type: currentMode.value,
      sport_name: sportModes.find(m => m.type === currentMode.value)?.name,
      duration: Math.floor(durationSec.value / 60),
      distance: Math.round(distanceVal.value * 1000), // 转换为米
      start_time: startTime.value!.toISOString().replace('T', ' ').slice(0, 19),
      end_time: endTime.toISOString().replace('T', ' ').slice(0, 19),
      feeling: 3,
    })
    
    uni.hideLoading()
    
    if (res.code === 200) {
      uni.showToast({ 
        title: `已保存！+${res.data.coins_earned}运动币`, 
        icon: 'success' 
      })
      userStore.fetchUserInfo()
    }
    
    resetSport()
  } catch (e: any) {
    uni.hideLoading()
    uni.showToast({ title: e.message || '保存失败', icon: 'none' })
  }
}

function resetSport() {
  isRunning.value = false
  isPaused.value = false
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
  if (locationTimer.value) {
    clearInterval(locationTimer.value)
    locationTimer.value = null
  }
  distanceVal.value = 0
  durationSec.value = 0
  startTime.value = null
  trackPoints.value = []
}

function goBack() {
  if (isRunning.value) {
    uni.showModal({
      title: '提示',
      content: '运动正在进行中，确定要退出吗？',
      success: (res) => {
        if (res.confirm) {
          resetSport()
          uni.navigateBack()
        }
      }
    })
  } else {
    uni.navigateBack()
  }
}

function goHistory() {
  uni.navigateTo({ url: '/pages/sport/history' })
}

function lockScreen() {
  uni.showToast({ title: '锁屏功能开发中', icon: 'none' })
}

function playMusic() {
  uni.showToast({ title: '音乐功能开发中', icon: 'none' })
}

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
  if (locationTimer.value) {
    clearInterval(locationTimer.value)
  }
})
</script>

<style lang="scss" scoped>
.page {
  height: 100vh;
  position: relative;
  background: #1D1D1F;
  overflow: hidden;
}

.map-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 340px; // 给底部面板留出固定空间
  background: #1D1D1F;
  
  .sport-map {
    width: 100%;
    height: 100%;
  }
  
  .top-mask {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 120px;
    background: linear-gradient(to bottom, rgba(0,0,0,0.6), transparent);
    pointer-events: none;
  }
  
  .status-bar {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 0 16px;
    padding-top: calc(var(--status-bar-height) + 10px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
    
    .back-btn {
      width: 36px;
      height: 36px;
      background: rgba(0,0,0,0.3);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .mode-switch {
      flex: 1;
      display: flex;
      justify-content: center;
      gap: 20px;
      color: rgba(255,255,255,0.5);
      font-size: 15px;
      
      text {
        padding: 4px 0;
        transition: all 0.2s;
      }
      
      .active {
        color: #FFF;
        font-size: 17px;
        font-weight: 700;
        position: relative;
        
        &::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 20px;
          height: 3px;
          background: #0071e3;
          border-radius: 2px;
        }
      }
    }
    
    .settings-icon {
      width: 36px;
      height: 36px;
      background: rgba(0,0,0,0.3);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}

.data-panel {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 340px; // 固定高度
  background: #FFFFFF;
  border-radius: 24px 24px 0 0;
  z-index: 10;
  padding: 32px 24px;
  padding-bottom: calc(50px + env(safe-area-inset-bottom));
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  
  .main-data {
    text-align: center;
    margin-bottom: 32px;
    
    .label { font-size: 14px; color: #86868B; margin-bottom: 8px; display: block; }
    .value { font-size: 64px; font-weight: 800; color: #1D1D1F; line-height: 1; }
  }
  
  .sub-data-row {
    width: 100%;
    display: flex;
    justify-content: space-between;
    margin-bottom: 40px;
    
    .sub-item {
      text-align: center;
      
      .val { font-size: 24px; font-weight: 700; color: #1D1D1F; display: block; margin-bottom: 4px; }
      .lbl { font-size: 12px; color: #86868B; }
    }
  }
  
  .control-area {
    display: flex;
    align-items: center;
    gap: 32px;
    
    .btn-circle {
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      transition: all 0.2s;
      
      &.small {
        width: 48px;
        height: 48px;
        background: #F5F5F7;
        
        &.danger {
          background: #FFEBEE;
        }
      }
      
      &.large {
        width: 96px;
        height: 96px;
        background: #0071e3;
        box-shadow: 0 8px 24px rgba(0, 113, 227, 0.4);
        
        .btn-text {
          color: #FFF;
          font-size: 22px;
          font-weight: 700;
        }
        
        &.running {
          background: #FF9500;
          box-shadow: 0 8px 24px rgba(255, 149, 0, 0.4);
        }
        
        &.paused {
          background: #34C759;
          box-shadow: 0 8px 24px rgba(52, 199, 89, 0.4);
        }
        
        &:active { transform: scale(0.95); }
      }
    }
  }
  
  .tips {
    margin-top: 16px;
    font-size: 12px;
    color: #86868B;
  }
}
</style>
