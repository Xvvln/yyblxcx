<template>
  <view class="page">
    <!-- 日期选择 -->
    <view class="date-nav">
      <view class="date-btn" @click="changeDate(-1)">
        <wd-icon name="arrow-left" size="16px" color="#86868B"></wd-icon>
      </view>
      <text class="date-text">{{ formatDate(currentDate) }}</text>
      <view class="date-btn" @click="changeDate(1)" v-if="!isToday">
        <wd-icon name="arrow-right" size="16px" color="#86868B"></wd-icon>
      </view>
      <view class="date-btn disabled" v-else>
        <wd-icon name="arrow-right" size="16px" color="#E5E5EA"></wd-icon>
      </view>
    </view>
    
    <!-- 顶部统计 -->
    <view class="summary-card">
      <view class="circle-chart">
        <view class="chart-inner">
          <text class="val">{{ totalCalories }}</text>
          <text class="label">已摄入</text>
        </view>
        <view class="chart-ring" :style="{ background: ringGradient }"></view>
      </view>
      
      <view class="nutrients">
        <view class="nutrient-item">
          <text class="n-label">碳水</text>
          <view class="progress-bar">
            <view class="bar-inner" :style="{ width: carbsPercent + '%', background: '#FF9500' }"></view>
          </view>
          <text class="n-val">{{ totalCarbs.toFixed(0) }}g</text>
        </view>
        <view class="nutrient-item">
          <text class="n-label">蛋白质</text>
          <view class="progress-bar">
            <view class="bar-inner" :style="{ width: proteinPercent + '%', background: '#34C759' }"></view>
          </view>
          <text class="n-val">{{ totalProtein.toFixed(0) }}g</text>
        </view>
        <view class="nutrient-item">
          <text class="n-label">脂肪</text>
          <view class="progress-bar">
            <view class="bar-inner" :style="{ width: fatPercent + '%', background: '#FF3B30' }"></view>
          </view>
          <text class="n-val">{{ totalFat.toFixed(0) }}g</text>
        </view>
      </view>
    </view>
    
    <!-- 记录列表 -->
    <view class="meal-section" v-for="meal in mealTypes" :key="meal.type">
      <view class="section-header">
        <view class="left">
          <text class="meal-name">{{ meal.name }}</text>
          <text class="meal-kcal">{{ getMealTotal(meal.type) }} kcal</text>
        </view>
        <view class="add-btn" @click="addFood(meal.type)">
          <wd-icon name="add" size="16px" color="#0071e3"></wd-icon>
        </view>
      </view>
      
      <view class="food-list" v-if="getMealFoods(meal.type).length > 0">
        <view class="food-item" v-for="food in getMealFoods(meal.type)" :key="food.id">
          <view class="food-image">
            <image v-if="food.food_image" :src="food.food_image" mode="aspectFill" />
            <text v-else class="placeholder">🍽️</text>
          </view>
          <view class="food-info">
            <text class="food-name">{{ food.food_name }}</text>
            <text class="food-amount">{{ food.amount ? food.amount + 'g' : '' }}</text>
          </view>
          <text class="food-cal">{{ food.calories }} kcal</text>
        </view>
      </view>
      
      <view class="empty-tip" v-else @click="addFood(meal.type)">
        <text>点击添加{{ meal.name }}</text>
      </view>
    </view>
    
    <!-- 拍照识别入口 -->
    <view class="camera-btn" @click="cameraIdentify">
      <wd-icon name="camera" size="20px" color="#FFFFFF"></wd-icon>
      <text>拍照识别</text>
    </view>
    
    <!-- 添加食物弹窗 -->
    <wd-popup v-model="showAddFood" position="bottom" custom-style="border-radius: 24px 24px 0 0;">
      <view class="add-food-panel">
        <view class="panel-header">
          <text class="panel-title">添加{{ currentMealName }}</text>
          <view class="close-btn" @click="showAddFood = false">
            <wd-icon name="close" size="20px" color="#86868B"></wd-icon>
          </view>
        </view>
        
        <!-- 搜索框 -->
        <view class="search-box">
          <wd-icon name="search" size="16px" color="#86868B"></wd-icon>
          <input v-model="searchKeyword" placeholder="搜索食物" @confirm="searchFood" />
        </view>
        
        <!-- 食物列表 -->
        <scroll-view scroll-y class="food-search-list">
          <view class="food-search-item" v-for="food in foodLibrary" :key="food.id" @click="selectFood(food)">
            <view class="food-search-info">
              <text class="name">{{ food.name }}</text>
              <text class="cal">{{ food.calories }} kcal/100g</text>
            </view>
            <wd-icon name="add-circle" size="24px" color="#0071e3"></wd-icon>
          </view>
          <view v-if="foodLibrary.length === 0" class="search-empty">
            <text>{{ searchKeyword ? '未找到相关食物' : '输入关键词搜索食物' }}</text>
          </view>
        </scroll-view>
        
        <!-- 手动添加 -->
        <view class="manual-add" @click="manualAdd">
          <wd-icon name="edit" size="18px" color="#0071e3"></wd-icon>
          <text>手动录入食物</text>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getFoodRecords, submitFoodRecord, searchFoodLibrary } from '@/api/food'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'

const userStore = useUserStore()

const currentDate = ref(new Date())
const records = ref<any[]>([])
const showAddFood = ref(false)
const currentMealType = ref('breakfast')
const searchKeyword = ref('')
const foodLibrary = ref<any[]>([])

const mealTypes = [
  { type: 'breakfast', name: '早餐' },
  { type: 'lunch', name: '午餐' },
  { type: 'dinner', name: '晚餐' },
  { type: 'snack', name: '加餐' },
]

const isToday = computed(() => {
  return dayjs(currentDate.value).isSame(dayjs(), 'day')
})

const currentMealName = computed(() => {
  return mealTypes.find(m => m.type === currentMealType.value)?.name || ''
})

// 营养统计
const totalCalories = computed(() => records.value.reduce((sum, r) => sum + (r.calories || 0), 0))
const totalCarbs = computed(() => records.value.reduce((sum, r) => sum + parseFloat(r.carbs || 0), 0))
const totalProtein = computed(() => records.value.reduce((sum, r) => sum + parseFloat(r.protein || 0), 0))
const totalFat = computed(() => records.value.reduce((sum, r) => sum + parseFloat(r.fat || 0), 0))

// 营养百分比（假设每日推荐：碳水300g，蛋白质60g，脂肪60g）
const carbsPercent = computed(() => Math.min((totalCarbs.value / 300) * 100, 100))
const proteinPercent = computed(() => Math.min((totalProtein.value / 60) * 100, 100))
const fatPercent = computed(() => Math.min((totalFat.value / 60) * 100, 100))

// 圆环渐变
const ringGradient = computed(() => {
  const percent = Math.min((totalCalories.value / 2000) * 100, 100)
  return `conic-gradient(#34C759 0% ${percent}%, #F5F5F7 ${percent}% 100%)`
})

function formatDate(date: Date) {
  const d = dayjs(date)
  if (d.isSame(dayjs(), 'day')) return '今天'
  if (d.isSame(dayjs().subtract(1, 'day'), 'day')) return '昨天'
  return d.format('MM月DD日')
}

function changeDate(delta: number) {
  const newDate = dayjs(currentDate.value).add(delta, 'day')
  if (newDate.isAfter(dayjs())) return
  currentDate.value = newDate.toDate()
  fetchRecords()
}

function getMealFoods(type: string) {
  return records.value.filter(r => r.meal_type === type)
}

function getMealTotal(type: string) {
  return getMealFoods(type).reduce((sum, r) => sum + (r.calories || 0), 0)
}

async function fetchRecords() {
  try {
    const dateStr = dayjs(currentDate.value).format('YYYY-MM-DD')
    const res = await getFoodRecords({ record_date: dateStr, page_size: 50 })
    if (res.code === 200) {
      records.value = res.data.list || []
    }
  } catch (e) {
    console.error(e)
  }
}

function addFood(type: string) {
  currentMealType.value = type
  searchKeyword.value = ''
  foodLibrary.value = []
  showAddFood.value = true
}

async function searchFood() {
  if (!searchKeyword.value.trim()) {
    foodLibrary.value = []
    return
  }
  
  try {
    const res = await searchFoodLibrary({ keyword: searchKeyword.value })
    if (res.code === 200) {
      foodLibrary.value = res.data.list || []
    }
  } catch (e) {
    console.error(e)
  }
}

async function selectFood(food: any) {
  try {
    const res = await submitFoodRecord({
      meal_type: currentMealType.value as any,
      record_date: dayjs(currentDate.value).format('YYYY-MM-DD'),
      food_name: food.name,
      amount: 100,
      calories: food.calories,
      protein: food.protein,
      carbs: food.carbs,
      fat: food.fat,
      fiber: food.fiber,
    })
    
    if (res.code === 200) {
      uni.showToast({ title: `添加成功！+${res.data.coins_earned}膳食币`, icon: 'success' })
      showAddFood.value = false
      fetchRecords()
      userStore.fetchUserInfo()
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '添加失败', icon: 'none' })
  }
}

function manualAdd() {
  // 手动录入
  uni.showModal({
    title: '手动录入',
    editable: true,
    placeholderText: '输入食物名称',
    success: async (res) => {
      if (res.confirm && res.content) {
        try {
          const result = await submitFoodRecord({
            meal_type: currentMealType.value as any,
            record_date: dayjs(currentDate.value).format('YYYY-MM-DD'),
            food_name: res.content,
            calories: 100,
          })
          
          if (result.code === 200) {
            uni.showToast({ title: '添加成功', icon: 'success' })
            showAddFood.value = false
            fetchRecords()
            userStore.fetchUserInfo()
          }
        } catch (e: any) {
          uni.showToast({ title: e.message || '添加失败', icon: 'none' })
        }
      }
    }
  })
}

function cameraIdentify() {
  uni.chooseImage({
    count: 1,
    success: () => {
      uni.showLoading({ title: '识别中...' })
      // AI识别暂缓实现，返回模拟结果
      setTimeout(() => {
        uni.hideLoading()
        uni.showToast({ title: 'AI识别功能开发中', icon: 'none' })
      }, 1500)
    }
  })
}

onShow(() => {
  fetchRecords()
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
  padding: 16px;
  padding-bottom: 100px;
}

.date-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 16px;
  
  .date-btn {
    width: 32px;
    height: 32px;
    background: #FFFFFF;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    
    &.disabled {
      opacity: 0.5;
    }
  }
  
  .date-text {
    font-size: 17px;
    font-weight: 600;
    color: #1D1D1F;
    min-width: 80px;
    text-align: center;
  }
}

.summary-card {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 24px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  
  .circle-chart {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 24px;
    position: relative;
    
    .chart-ring {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      mask: radial-gradient(transparent 35px, #000 36px);
      -webkit-mask: radial-gradient(transparent 35px, #000 36px);
    }
    
    .chart-inner {
      text-align: center;
      z-index: 1;
      
      .val {
        font-size: 20px;
        font-weight: 700;
        color: #1D1D1F;
        display: block;
      }
      
      .label {
        font-size: 11px;
        color: #86868B;
      }
    }
  }
  
  .nutrients {
    flex: 1;
    
    .nutrient-item {
      margin-bottom: 10px;
      
      &:last-child { margin-bottom: 0; }
      
      .n-label {
        font-size: 12px;
        color: #86868B;
        display: block;
        margin-bottom: 4px;
      }
      
      .progress-bar {
        height: 6px;
        background: #F5F5F7;
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 2px;
        
        .bar-inner {
          height: 100%;
          border-radius: 3px;
          transition: width 0.3s;
        }
      }
      
      .n-val {
        font-size: 12px;
        color: #1D1D1F;
        font-weight: 500;
      }
    }
  }
}

.meal-section {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    
    .left {
      .meal-name {
        font-size: 16px;
        font-weight: 600;
        color: #1D1D1F;
        margin-right: 8px;
      }
      
      .meal-kcal {
        font-size: 12px;
        color: #86868B;
      }
    }
    
    .add-btn {
      width: 28px;
      height: 28px;
      background: #E8F4FD;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
  
  .food-list {
    .food-item {
      display: flex;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid #F5F5F7;
      
      &:last-child { border-bottom: none; }
      
      .food-image {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        background: #F5F5F7;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        
        image {
          width: 100%;
          height: 100%;
        }
        
        .placeholder {
          font-size: 20px;
        }
      }
      
      .food-info {
        flex: 1;
        margin-left: 12px;
        
        .food-name {
          font-size: 15px;
          color: #1D1D1F;
          display: block;
          font-weight: 500;
        }
        
        .food-amount {
          font-size: 12px;
          color: #86868B;
        }
      }
      
      .food-cal {
        font-size: 14px;
        font-weight: 500;
        color: #1D1D1F;
      }
    }
  }
  
  .empty-tip {
    text-align: center;
    padding: 16px;
    font-size: 13px;
    color: #86868B;
    background: #F5F5F7;
    border-radius: 10px;
  }
}

.camera-btn {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: #0071e3;
  color: #FFFFFF;
  padding: 14px 28px;
  border-radius: 28px;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 6px 20px rgba(0, 113, 227, 0.35);
  font-size: 15px;
  font-weight: 600;
}

.add-food-panel {
  padding: 24px;
  padding-bottom: 40px;
  
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    .panel-title {
      font-size: 18px;
      font-weight: 700;
      color: #1D1D1F;
    }
    
    .close-btn {
      padding: 8px;
    }
  }
  
  .search-box {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #F5F5F7;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 16px;
    
    input {
      flex: 1;
      font-size: 15px;
    }
  }
  
  .food-search-list {
    height: 300px;
    
    .food-search-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 0;
      border-bottom: 1px solid #F5F5F7;
      
      .food-search-info {
        .name {
          font-size: 15px;
          color: #1D1D1F;
          display: block;
          font-weight: 500;
        }
        
        .cal {
          font-size: 12px;
          color: #86868B;
        }
      }
    }
    
    .search-empty {
      text-align: center;
      padding: 40px;
      color: #86868B;
      font-size: 14px;
    }
  }
  
  .manual-add {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 16px;
    margin-top: 16px;
    background: #E8F4FD;
    border-radius: 12px;
    color: #0071e3;
    font-size: 15px;
    font-weight: 500;
  }
}
</style>
