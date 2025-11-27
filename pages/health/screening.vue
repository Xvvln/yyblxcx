<template>
  <view class="page">
    <!-- 顶部导航 -->
    <view class="nav-bar">
      <view class="back-btn" @click="handleBack">
        <wd-icon name="arrow-left" size="20px" color="#1D1D1F"></wd-icon>
      </view>
      <view class="progress-line">
        <view class="current" :style="{ width: (currentStep / totalSteps) * 100 + '%' }"></view>
      </view>
      <view class="skip-btn" @click="handleSkip" v-if="currentStep < totalSteps">
        <text>跳过</text>
      </view>
    </view>
    
    <view class="content">
      
      <!-- 步骤 1: 性别 -->
      <view v-if="currentStep === 1" class="step-container">
        <view class="step-header">
          <text class="step-title">你的性别是？</text>
          <text class="step-desc">性别有助于我们提供更精准的健康建议</text>
        </view>
        <gender-selector v-model="form.gender" />
      </view>
      
      <!-- 步骤 2: 生日 -->
      <view v-if="currentStep === 2" class="step-container">
        <view class="step-header">
          <text class="step-title">你的出生日期？</text>
          <text class="step-desc">我们将根据年龄评估代谢水平</text>
        </view>
        <view class="date-picker-wrap">
          <picker-view indicator-style="height: 50px;" :value="dateValue" @change="bindDateChange" class="picker-view">
            <picker-view-column>
              <view class="item" v-for="item in years" :key="item">{{item}}年</view>
            </picker-view-column>
            <picker-view-column>
              <view class="item" v-for="item in months" :key="item">{{item}}月</view>
            </picker-view-column>
            <picker-view-column>
              <view class="item" v-for="item in days" :key="item">{{item}}日</view>
            </picker-view-column>
          </picker-view>
        </view>
      </view>
      
      <!-- 步骤 3: 身高 -->
      <view v-if="currentStep === 3" class="step-container">
        <view class="step-header">
          <text class="step-title">你的身高是？</text>
          <text class="step-desc">用于计算 BMI 指数</text>
        </view>
        <ruler-slider 
          v-model="form.height" 
          :min="100" 
          :max="250" 
          unit="cm" 
        />
      </view>
      
      <!-- 步骤 4: 体重 -->
      <view v-if="currentStep === 4" class="step-container">
        <view class="step-header">
          <text class="step-title">你的体重是？</text>
          <text class="step-desc">用于计算 BMI 指数</text>
        </view>
        <ruler-slider 
          v-model="form.weight" 
          :min="30" 
          :max="150" 
          unit="kg" 
          :step="0.5"
        />
        <view class="bmi-preview" v-if="bmi > 0">
          <text class="label">BMI</text>
          <text class="value">{{ bmi }}</text>
          <text class="status" :class="bmiStatus.class">{{ bmiStatus.text }}</text>
        </view>
      </view>
      
      <!-- 步骤 5: 生成中 -->
      <view v-if="currentStep === 5" class="step-container generating">
        <view class="loading-circle">
          <view class="percent">{{ generatePercent }}%</view>
          <view class="loading-text">正在生成健康方案...</view>
        </view>
        <view class="check-list">
          <view class="check-item" :class="{ active: generatePercent > 30 }">
            <text class="icon">✓</text>
            <text class="text">分析基础代谢</text>
          </view>
          <view class="check-item" :class="{ active: generatePercent > 60 }">
            <text class="icon">✓</text>
            <text class="text">评估营养风险</text>
          </view>
          <view class="check-item" :class="{ active: generatePercent > 90 }">
            <text class="icon">✓</text>
            <text class="text">生成个性化建议</text>
          </view>
        </view>
      </view>
      
    </view>
    
    <!-- 底部按钮 -->
    <view class="footer" v-if="currentStep < 5">
      <button 
        class="next-btn"
        @click="nextStep"
        :disabled="isNextDisabled"
      >
        {{ currentStep === totalSteps - 1 ? '生成报告' : '下一步' }}
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { submitScreening } from '@/api/health'
import { useUserStore } from '@/stores/user'
import GenderSelector from '@/components/gender-selector.vue'
import RulerSlider from '@/components/ruler-slider.vue'

const userStore = useUserStore()

const currentStep = ref(1)
const totalSteps = 5
const generatePercent = ref(0)
const reportId = ref<number | null>(null)

const form = reactive({
  gender: 0,
  birthday: '1995-01-01',
  height: 170,
  weight: 60
})

// 日期选择器数据
const dateValue = ref([1995 - 1950, 0, 0])
const years: number[] = []
const months: number[] = []
const days: number[] = []

for (let i = 1950; i <= 2025; i++) years.push(i)
for (let i = 1; i <= 12; i++) months.push(i)
for (let i = 1; i <= 31; i++) days.push(i)

function bindDateChange(e: any) {
  const val = e.detail.value
  dateValue.value = val
  const y = years[val[0]]
  const m = String(months[val[1]]).padStart(2, '0')
  const d = String(days[val[2]]).padStart(2, '0')
  form.birthday = `${y}-${m}-${d}`
}

// BMI 计算
const bmi = computed(() => {
  if (form.height > 0 && form.weight > 0) {
    const h = form.height / 100
    return (form.weight / (h * h)).toFixed(1)
  }
  return '0.0'
})

const bmiStatus = computed(() => {
  const b = parseFloat(bmi.value)
  if (b < 18.5) return { text: '偏瘦', class: 'thin' }
  if (b < 24) return { text: '正常', class: 'normal' }
  if (b < 28) return { text: '超重', class: 'fat' }
  return { text: '肥胖', class: 'obese' }
})

// 按钮禁用状态
const isNextDisabled = computed(() => {
  if (currentStep.value === 1 && form.gender === 0) return true
  return false
})

function handleBack() {
  if (currentStep.value > 1) {
    currentStep.value--
  } else {
    uni.navigateBack()
  }
}

function handleSkip() {
  if (currentStep.value < totalSteps - 1) {
    currentStep.value++
  }
}

function nextStep() {
  if (currentStep.value < totalSteps - 1) {
    currentStep.value++
  } else {
    startGenerating()
  }
}

async function startGenerating() {
  // 检查登录状态
  const token = uni.getStorageSync('token')
  if (!token) {
    uni.showToast({ title: '请先登录', icon: 'none' })
    setTimeout(() => {
      uni.reLaunch({ url: '/pages/login/index' })
    }, 1500)
    return
  }
  
  currentStep.value = 5
  
  // 开始进度动画
  const timer = setInterval(() => {
    if (generatePercent.value < 90) {
      generatePercent.value += Math.floor(Math.random() * 5) + 1
    }
  }, 100)
  
  try {
    // 提交筛查数据
    const res = await submitScreening({
      height: form.height,
      weight: form.weight,
      questionnaire_data: {
        gender: form.gender,
        birthday: form.birthday
      }
    })
    
    clearInterval(timer)
    
    if (res.code === 200 && res.data) {
      reportId.value = res.data.id
      generatePercent.value = 100
      
      // 更新用户信息
      userStore.fetchUserInfo()
      
      setTimeout(() => {
        uni.redirectTo({ url: `/pages/health/result?id=${reportId.value}` })
      }, 800)
    } else {
      throw new Error(res.message || '提交失败')
    }
  } catch (e: any) {
    clearInterval(timer)
    console.error(e)
    uni.showToast({ title: e.message || '提交失败', icon: 'none' })
    currentStep.value = 4
    generatePercent.value = 0
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #FFFFFF;
  display: flex;
  flex-direction: column;
}

.nav-bar {
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  padding-top: var(--status-bar-height);
  
  .back-btn {
    padding: 8px;
  }
  
  .progress-line {
    flex: 1;
    height: 4px;
    background: #F5F5F7;
    border-radius: 2px;
    margin: 0 20px;
    
    .current {
      height: 100%;
      background: #0071e3;
      border-radius: 2px;
      transition: width 0.3s ease;
    }
  }
  
  .skip-btn {
    font-size: 14px;
    color: #86868B;
    padding: 8px;
  }
}

.content {
  flex: 1;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
}

.step-header {
  text-align: center;
  margin-bottom: 40px;
  
  .step-title {
    font-size: 28px;
    font-weight: 700;
    color: #1D1D1F;
    display: block;
    margin-bottom: 12px;
  }
  
  .step-desc {
    font-size: 14px;
    color: #86868B;
  }
}

.date-picker-wrap {
  height: 300px;
  margin-top: 40px;
  
  .picker-view {
    width: 100%;
    height: 100%;
  }
  
  .item {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: #1D1D1F;
  }
}

.bmi-preview {
  margin-top: 40px;
  background: #F5F5F7;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  
  .label { font-size: 16px; font-weight: 600; color: #86868B; }
  .value { font-size: 24px; font-weight: 700; color: #1D1D1F; }
  
  .status {
    font-size: 12px;
    padding: 4px 8px;
    border-radius: 4px;
    
    &.thin { background: #E3F2FD; color: #007AFF; }
    &.normal { background: #E8F5E9; color: #34C759; }
    &.fat { background: #FFF3E0; color: #FF9500; }
    &.obese { background: #FFEBEE; color: #FF3B30; }
  }
}

.generating {
  align-items: center;
  justify-content: center;
  
  .loading-circle {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    border: 8px solid #F5F5F7;
    border-top-color: #0071e3;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 60px;
    animation: spin 2s linear infinite;
    
    .percent {
      font-size: 40px;
      font-weight: 700;
      color: #1D1D1F;
      animation: none;
    }
    
    .loading-text {
      font-size: 12px;
      color: #86868B;
      margin-top: 8px;
      animation: none;
    }
  }
  
  .check-list {
    width: 100%;
    padding: 0 40px;
    
    .check-item {
      display: flex;
      align-items: center;
      margin-bottom: 20px;
      opacity: 0.3;
      transition: all 0.3s;
      
      &.active {
        opacity: 1;
        
        .icon {
          background: #34C759;
          border-color: #34C759;
          color: #FFF;
        }
        
        .text {
          font-weight: 600;
        }
      }
      
      .icon {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 2px solid #C7C7CC;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        font-size: 14px;
        color: transparent;
      }
      
      .text {
        font-size: 16px;
        color: #1D1D1F;
      }
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.footer {
  padding: 24px;
  padding-bottom: 40px;
  
  .next-btn {
    width: 100%;
    height: 50px;
    background: #0071e3;
    border-radius: 25px;
    border: none;
    color: #FFFFFF;
    font-size: 17px;
    font-weight: 600;
    
    &::after {
      border: none;
    }
    
    &[disabled] {
      background: #E5E5EA;
      color: #86868B;
    }
  }
}
</style>
