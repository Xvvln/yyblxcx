<template>
  <view class="basic-info-page">
    <view class="nav-bar">
      <wd-icon name="arrow-left" size="18px" color="#111" @click="handleBack" />
      <view class="progress">
        <view v-for="n in 3" :key="n" class="progress-segment" :class="{ active: n === 1 }" />
      </view>
    </view>

    <view class="header">
      <text class="title">完善一下你的基础信息吧</text>
      <text class="subtitle">帮你更科学地制定专属运动方案</text>
    </view>

    <view class="info-card">
      <view class="info-item" @click="openModal('gender')">
        <view class="item-left">
          <view class="icon-circle male">
            <wd-icon name="user" size="16px" color="#fff" />
          </view>
          <text class="item-label">性别</text>
        </view>
        <view class="item-right">
          <text class="item-value">{{ genderLabel || '请填写' }}</text>
          <wd-icon name="arrow-right" size="14px" color="#b5bcc5" />
        </view>
      </view>

      <view class="info-item" @click="openModal('birthday')">
        <view class="item-left">
          <view class="icon-circle birthday">
            <wd-icon name="calendar" size="16px" color="#fff" />
          </view>
          <text class="item-label">生日</text>
        </view>
        <view class="item-right">
          <text class="item-value">{{ form.birthday || '请填写' }}</text>
          <wd-icon name="arrow-right" size="14px" color="#b5bcc5" />
        </view>
      </view>

      <view class="info-item" @click="openModal('height')">
        <view class="item-left">
          <view class="icon-circle height">
            <wd-icon name="ranking" size="16px" color="#fff" />
          </view>
          <text class="item-label">身高</text>
        </view>
        <view class="item-right">
          <text class="item-value">{{ form.height ? `${form.height.toFixed(1)} cm` : '请填写' }}</text>
          <wd-icon name="arrow-right" size="14px" color="#b5bcc5" />
        </view>
      </view>

      <view class="info-item" @click="openModal('weight')">
        <view class="item-left">
          <view class="icon-circle weight">
            <wd-icon name="giftcard" size="16px" color="#fff" />
          </view>
          <text class="item-label">体重</text>
        </view>
        <view class="item-right">
          <text class="item-value">{{ form.weight ? `${form.weight.toFixed(1)} kg` : '请填写' }}</text>
          <wd-icon name="arrow-right" size="14px" color="#b5bcc5" />
        </view>
      </view>
    </view>

    <!-- 底部下一步按钮 -->
    <view class="footer-action" v-show="!isAnyModalOpen">
      <view 
        class="next-btn" 
        :class="{ disabled: !isFormValid }"
        @click="handleNext"
      >
        生成专属方案
      </view>
    </view>

    <!-- 生成中全屏覆盖层 -->
    <view class="generating-overlay" v-if="isGenerating">
      <!-- 漂浮气泡背景 -->
      <view class="bubble b1"></view>
      <view class="bubble b2"></view>
      <view class="bubble b3"></view>
      
      <view class="gen-content">
        <view class="loading-circle">
          <view class="spinner"></view>
          <wd-icon name="check" size="40px" color="#2EBD59" v-if="genStep >= 3" class="success-icon" />
        </view>
        
        <view class="gen-title">正在为你生成专属方案</view>
        
        <view class="task-list">
          <view class="task-item" :class="{ active: genStep >= 1 }">
            <view class="task-icon">
              <wd-icon name="check" size="12px" color="#2EBD59" v-if="genStep >= 1" />
            </view>
            <text class="task-text">分析身体数据...</text>
          </view>
          <view class="task-item" :class="{ active: genStep >= 2 }">
            <view class="task-icon">
              <wd-icon name="check" size="12px" color="#2EBD59" v-if="genStep >= 2" />
            </view>
            <text class="task-text">评估健康风险...</text>
          </view>
          <view class="task-item" :class="{ active: genStep >= 3 }">
            <view class="task-icon">
              <wd-icon name="check" size="12px" color="#2EBD59" v-if="genStep >= 3" />
            </view>
            <text class="task-text">匹配运动计划...</text>
          </view>
        </view>
      </view>
    </view>
  </view>

  <!-- 弹窗部分保持不变 -->
  <!-- 性别弹窗 -->
  <wd-popup
    v-model="showGender"
    position="bottom"
    :round="20"
    custom-style="padding: 24rpx 32rpx 48rpx;"
  >
    <view class="modal-header">
      <text class="modal-title">性别</text>
      <wd-icon name="close" size="18px" color="#b5bcc5" @click="showGender = false" />
    </view>
    <text class="modal-subtitle">选择性别帮助我们匹配更合适的训练计划</text>

    <view class="gender-grid">
      <view
        v-for="option in genderOptions"
        :key="option.value"
        class="gender-card"
        :class="{ active: form.gender === option.value }"
        @click="form.gender = option.value"
      >
        <view class="gender-figure" :class="option.value"></view>
        <text class="gender-label">{{ option.label }}</text>
      </view>
    </view>

    <view class="modal-footer">
      <view class="confirm-btn" @click="showGender = false">确认</view>
    </view>
  </wd-popup>

  <!-- 生日弹窗 -->
  <wd-popup
    v-model="showBirthday"
    position="bottom"
    :round="20"
    custom-style="padding: 24rpx 32rpx 32rpx;"
  >
    <view class="modal-header">
      <text class="modal-title">生日</text>
      <wd-icon name="close" size="18px" color="#b5bcc5" @click="showBirthday = false" />
    </view>
    <text class="modal-subtitle">了解年龄有助于评估代谢水平与训练强度</text>

    <view class="picker-wrapper">
      <picker-view :value="birthdayIndexes" @change="handleBirthdayChange" class="picker-view">
        <picker-view-column>
          <view class="picker-item" v-for="year in years" :key="year">{{ year }}年</view>
        </picker-view-column>
        <picker-view-column>
          <view class="picker-item" v-for="month in months" :key="month">{{ month }}月</view>
        </picker-view-column>
        <picker-view-column>
          <view class="picker-item" v-for="day in days" :key="day">{{ day }}日</view>
        </picker-view-column>
      </picker-view>
    </view>

    <view class="modal-footer">
      <view class="confirm-btn" @click="confirmBirthday">确认</view>
    </view>
  </wd-popup>

  <!-- 身高弹窗 -->
  <wd-popup
    v-model="showHeight"
    position="bottom"
    :round="20"
    custom-style="padding: 24rpx 32rpx 48rpx;"
  >
    <view class="modal-header">
      <text class="modal-title">身高</text>
      <wd-icon name="close" size="18px" color="#b5bcc5" @click="showHeight = false" />
    </view>
    <text class="modal-subtitle">帮你更科学地制定专属运动方案</text>

    <ruler-picker
      :modelValue="tempHeight"
      @update:modelValue="val => tempHeight = val"
      :min="120"
      :max="210"
      :step="1"
      unit="厘米"
      :label-interval="5"
    />

    <view class="modal-footer">
      <view class="confirm-btn" @click="confirmHeight">确认</view>
    </view>
  </wd-popup>

  <!-- 体重弹窗 -->
  <wd-popup
    v-model="showWeight"
    position="bottom"
    :round="20"
    custom-style="padding: 24rpx 32rpx 48rpx;"
  >
    <view class="modal-header">
      <text class="modal-title">体重</text>
      <wd-icon name="close" size="18px" color="#b5bcc5" @click="showWeight = false" />
    </view>
    <text class="modal-subtitle">身高和体重可以计算人体健康指数（BMI）</text>

    <ruler-picker
      :modelValue="tempWeight"
      @update:modelValue="val => tempWeight = val"
      :min="30"
      :max="150"
      :step="1"
      unit="公斤"
      :label-interval="5"
    />

    <view class="bmi-card" v-if="bmi">
      <view>
        <text class="bmi-label">BMI</text>
        <text class="bmi-value">{{ bmi.value }}</text>
      </view>
      <text class="bmi-status" :class="bmi.statusClass">{{ bmi.statusText }}</text>
      <text class="bmi-tip">通过运动增加肌肉含量，可以更健康！</text>
    </view>

    <view class="modal-footer">
      <view class="confirm-btn" @click="confirmWeight">确认</view>
    </view>
  </wd-popup>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
// @ts-ignore
import RulerPicker from '@/components/ruler-picker.vue'
import { submitScreening } from '@/api/health'
import { updateUserProfile } from '@/api/user'

declare const uni: any

const form = reactive({
  gender: '' as 'male' | 'female' | '',
  birthday: '',
  height: 173,
  weight: 60,
})

const showGender = ref(false)
const showBirthday = ref(false)
const showHeight = ref(false)
const showWeight = ref(false)

const tempHeight = ref(form.height)
const tempWeight = ref(form.weight)

const isGenerating = ref(false)
const genStep = ref(0)

const genderOptions = [
  { label: '男性', value: 'male' as const },
  { label: '女性', value: 'female' as const },
]

const genderLabel = computed(() => {
  if (form.gender === 'male') return '男性'
  if (form.gender === 'female') return '女性'
  return ''
})

const isFormValid = computed(() => {
  return form.gender && form.birthday && form.height && form.weight
})

const isAnyModalOpen = computed(() => {
  return showGender.value || showBirthday.value || showHeight.value || showWeight.value
})

const years = Array.from({ length: 76 }, (_, i) => 1950 + i)
const months = Array.from({ length: 12 }, (_, i) => i + 1)
const birthdayIndexes = ref([20, 0, 0])

const days = computed(() => {
  const year = years[birthdayIndexes.value[0]] || 2000
  const month = months[birthdayIndexes.value[1]] || 1
  const total = new Date(year, month, 0).getDate()
  return Array.from({ length: total }, (_, i) => i + 1)
})

const bmi = computed(() => {
  if (!tempHeight.value || !tempWeight.value) return null
  const h = tempHeight.value / 100
  const value = Number((tempWeight.value / (h * h)).toFixed(1))
  let statusText = ''
  let statusClass = ''

  if (value < 18.5) {
    statusText = '偏瘦'
    statusClass = 'low'
  } else if (value < 24) {
    statusText = '正常'
    statusClass = 'normal'
  } else if (value < 28) {
    statusText = '超重'
    statusClass = 'high'
  } else {
    statusText = '肥胖'
    statusClass = 'very-high'
  }

  return { value, statusText, statusClass }
})

function handleBack() {
  uni.navigateBack({ fail: () => uni.switchTab({ url: '/pages/index/index' }) })
}

function openModal(type: 'gender' | 'birthday' | 'height' | 'weight') {
  if (type === 'gender') showGender.value = true
  if (type === 'birthday') {
    syncBirthdayIndexes()
    showBirthday.value = true
  }
  if (type === 'height') {
    tempHeight.value = form.height
    showHeight.value = true
  }
  if (type === 'weight') {
    tempWeight.value = form.weight
    showWeight.value = true
  }
}

function handleBirthdayChange(e: any) {
  birthdayIndexes.value = e.detail.value
}

function confirmBirthday() {
  const year = years[birthdayIndexes.value[0]]
  const month = months[birthdayIndexes.value[1]]
  const day = days.value[birthdayIndexes.value[2]] || 1
  form.birthday = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  showBirthday.value = false
}

function syncBirthdayIndexes() {
  if (!form.birthday) return
  const parts = form.birthday.split('-').map((item) => Number(item))
  if (parts.length !== 3) return
  const [y, m, d] = parts
  const yearIdx = Math.max(0, years.indexOf(y))
  const monthIdx = Math.max(0, months.indexOf(m))
  const totalDays = new Date(y, m, 0).getDate()
  const dayIdx = Math.min(Math.max(d, 1), totalDays) - 1
  birthdayIndexes.value = [yearIdx, monthIdx, Math.max(dayIdx, 0)]
}

function confirmHeight() {
  form.height = Number(tempHeight.value.toFixed(1))
  showHeight.value = false
}

function confirmWeight() {
  form.weight = Number(tempWeight.value.toFixed(1))
  showWeight.value = false
}

async function handleNext() {
  if (!isFormValid.value) {
    return uni.showToast({ title: '请完善所有信息', icon: 'none' })
  }
  
  // 开启生成动画
  isGenerating.value = true
  genStep.value = 1
  
  try {
    // 1. 更新用户信息
    await updateUserProfile({
      gender: form.gender === 'male' ? 1 : 2,
      birthday: form.birthday,
      height: form.height,
      weight: form.weight
    })
    
    setTimeout(() => genStep.value = 2, 800)
    
    // 2. 提交筛查数据
    const res = await submitScreening({
      height: form.height,
      weight: form.weight
    })
    
    if (res.code === 200) {
      setTimeout(() => genStep.value = 3, 1600)
      
      // 延迟跳转，让用户看完动画
      setTimeout(() => {
        uni.reLaunch({
          url: `/pages/health/result?id=${res.data.id}`
        })
      }, 2500)
    } else {
       throw new Error(res.message || '提交失败')
    }
  } catch (e: any) {
    isGenerating.value = false
    uni.showToast({ title: e.message || '网络错误，请重试', icon: 'none' })
  }
}
</script>

<style scoped lang="scss">
.basic-info-page {
  min-height: 100vh;
  background: #f7f8fa;
  padding: 32rpx;
  padding-bottom: 140rpx;
  box-sizing: border-box;
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24rpx;

  .progress {
    flex: 1;
    display: flex;
    gap: 8rpx;
    margin-left: 24rpx;

    .progress-segment {
      flex: 1;
      height: 8rpx;
      border-radius: 8rpx;
      background: #e1e3e6;

      &.active {
        background: linear-gradient(90deg, #63e2b7 0%, #2ec28b 100%);
      }
    }
  }
}

.header {
  margin-bottom: 40rpx;

  .title {
    font-size: 40rpx;
    font-weight: 700;
    color: #111;
    display: block;
    margin-bottom: 12rpx;
  }

  .subtitle {
    font-size: 26rpx;
    color: #8a929c;
  }
}

.info-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 8rpx 0;
  box-shadow: 0 16rpx 40rpx rgba(0, 0, 0, 0.06);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx;

  &:not(:last-child) {
    border-bottom: 1px solid #f1f2f5;
  }

  .item-left {
    display: flex;
    align-items: center;
    gap: 20rpx;

    .icon-circle {
      width: 64rpx;
      height: 64rpx;
      border-radius: 20rpx;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;

      &.male {
        background: linear-gradient(135deg, #6bb6ff, #478dff);
      }

      &.birthday {
        background: linear-gradient(135deg, #ffb94a, #ff9044);
      }

      &.height {
        background: linear-gradient(135deg, #63e2b7, #2ec28b);
      }

      &.weight {
        background: linear-gradient(135deg, #ff8f93, #ff6d7c);
      }
    }

    .item-label {
      font-size: 30rpx;
      color: #1f2329;
      font-weight: 600;
    }
  }

  .item-right {
    display: flex;
    align-items: center;
    gap: 12rpx;

    .item-value {
      font-size: 28rpx;
      color: #8a929c;
    }
  }
}

.footer-action {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  background: #fff;
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05);
  z-index: 100;

  .next-btn {
    height: 96rpx;
    border-radius: 48rpx;
    background: linear-gradient(90deg, #2ec28b, #1aa06b);
    color: #fff;
    font-size: 34rpx;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;

    &.disabled {
      background: #e1e3e6;
      color: #fff;
      pointer-events: none;
    }
    
    &:active {
      opacity: 0.9;
      transform: scale(0.98);
    }
  }
}

/* Generating Overlay */
.generating-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #2EBD59; /* 纯绿色背景 */
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  overflow: hidden;
  
  .gen-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 2;
  }
  
  .loading-circle {
    width: 80px;
    height: 80px;
    background: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    position: relative;
    
    .spinner {
      width: 50px;
      height: 50px;
      border: 4px solid #f3f3f3;
      border-top: 4px solid #2EBD59;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    
    .success-icon {
      position: absolute;
    }
  }
  
  .gen-title {
    font-size: 24px;
    font-weight: bold;
    color: #fff;
    margin-bottom: 40px;
  }
  
  .task-list {
    width: 240px;
    
    .task-item {
      display: flex;
      align-items: center;
      margin-bottom: 16px;
      opacity: 0.6;
      transition: all 0.3s;
      
      &.active {
        opacity: 1;
        transform: translateX(10px);
      }
      
      .task-icon {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
      }
      
      .task-text {
        color: #fff;
        font-size: 16px;
        font-weight: 500;
      }
    }
  }
  
  /* 漂浮气泡 */
  .bubble {
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    animation: float 6s infinite ease-in-out;
    
    &.b1 {
      width: 120px;
      height: 120px;
      top: 10%;
      left: -20px;
      animation-delay: 0s;
    }
    &.b2 {
      width: 80px;
      height: 80px;
      bottom: 20%;
      right: -10px;
      animation-delay: 2s;
    }
    &.b3 {
      width: 40px;
      height: 40px;
      top: 40%;
      right: 20%;
      animation-delay: 4s;
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* Modals */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;

  .modal-title {
    font-size: 32rpx;
    font-weight: 700;
    color: #111;
  }
}

.modal-subtitle {
  font-size: 26rpx;
  color: #8a929c;
  margin-bottom: 32rpx;
  display: block;
}

.gender-grid {
  display: flex;
  gap: 24rpx;
  margin-bottom: 40rpx;

  .gender-card {
    flex: 1;
    border-radius: 24rpx;
    padding: 24rpx;
    border: 2rpx solid transparent;
    background: #f7f8fa;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16rpx;
    transition: all 0.2s;

    &.active {
      border-color: #2ec28b;
      box-shadow: 0 16rpx 40rpx rgba(46, 194, 139, 0.15);
      background: #e8fff5;
    }

    .gender-figure {
      width: 160rpx;
      height: 160rpx;
      border-radius: 20rpx;
      background: linear-gradient(135deg, #dcdfe6, #f0f2f5);

      &.male {
        background: linear-gradient(135deg, #92c4ff, #5a9bff);
      }

      &.female {
        background: linear-gradient(135deg, #ffbbc1, #ff8fa0);
      }
    }

    .gender-label {
      font-size: 30rpx;
      font-weight: 600;
      color: #111;
    }
  }
}

.picker-wrapper {
  height: 420rpx;

  .picker-view {
    width: 100%;
    height: 100%;
  }

  .picker-item {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 32rpx;
    color: #111;
  }
}

.modal-footer {
  margin-top: 24rpx;

  .confirm-btn {
    height: 90rpx;
    border-radius: 90rpx;
    background: linear-gradient(90deg, #2ec28b, #1aa06b);
    color: #fff;
    font-size: 32rpx;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.bmi-card {
  margin-top: 32rpx;
  padding: 24rpx;
  border-radius: 20rpx;
  background: #f7f8fa;
  display: flex;
  align-items: center;
  gap: 24rpx;

  .bmi-label {
    font-size: 26rpx;
    color: #8a929c;
  }

  .bmi-value {
    font-size: 40rpx;
    font-weight: 700;
    color: #111;
    margin-left: 8rpx;
  }

  .bmi-status {
    font-size: 28rpx;
    font-weight: 600;

    &.low {
      color: #ff9f43;
    }

    &.normal {
      color: #2ec28b;
    }

    &.high,
    &.very-high {
      color: #ff6b6b;
    }
  }

  .bmi-tip {
    font-size: 24rpx;
    color: #8a929c;
    margin-left: auto;
  }
}
</style>
