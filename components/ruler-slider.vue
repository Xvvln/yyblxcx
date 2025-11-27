<template>
  <view class="ruler-container">
    <view class="value-display">
      <text class="value">{{ modelValue }}</text>
      <text class="unit">{{ unit }}</text>
    </view>
    
    <view class="ruler-wrapper">
      <scroll-view 
        scroll-x 
        class="ruler-scroll" 
        :scroll-left="scrollLeft"
        @scroll="onScroll"
        scroll-with-animation
      >
        <view class="ruler-content" :style="{ width: totalWidth + 'px' }">
          <view class="ruler-scale">
            <view 
              v-for="i in count" 
              :key="i" 
              class="scale-line"
              :class="{ 
                'long': (i - 1) % 10 === 0,
                'medium': (i - 1) % 5 === 0 && (i - 1) % 10 !== 0
              }"
            ></view>
          </view>
        </view>
      </scroll-view>
      
      <!-- 指针 -->
      <view class="pointer"></view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0
  },
  min: {
    type: Number,
    default: 0
  },
  max: {
    type: Number,
    default: 200
  },
  unit: {
    type: String,
    default: ''
  },
  step: {
    type: Number,
    default: 1
  }
})

const emit = defineEmits(['update:modelValue'])

const itemWidth = 10 // 每个刻度的宽度 px
const count = ref(0)
const totalWidth = ref(0)
const scrollLeft = ref(0)
const screenWidth = ref(375)

// 计算属性
const range = props.max - props.min
count.value = range / props.step + 1
totalWidth.value = count.value * itemWidth + screenWidth.value // 增加屏幕宽度以便首尾留白

onMounted(() => {
  uni.getSystemInfo({
    success: (res) => {
      screenWidth.value = res.windowWidth
      totalWidth.value = count.value * itemWidth + res.windowWidth
      
      // 初始化滚动位置
      nextTick(() => {
        scrollToValue(props.modelValue)
      })
    }
  })
})

function scrollToValue(val: number) {
  const diff = val - props.min
  const steps = diff / props.step
  // 计算 scrollLeft: 刻度位置 - 屏幕一半 + 边距补偿
  const targetLeft = steps * itemWidth
  scrollLeft.value = targetLeft
}

let scrollTimer: any = null

function onScroll(e: any) {
  if (scrollTimer) clearTimeout(scrollTimer)
  
  const left = e.detail.scrollLeft
  
  scrollTimer = setTimeout(() => {
    // 计算当前指向的值
    const steps = Math.round(left / itemWidth)
    let val = props.min + steps * props.step
    
    if (val < props.min) val = props.min
    if (val > props.max) val = props.max
    
    if (val !== props.modelValue) {
      emit('update:modelValue', val)
    }
  }, 100) // 节流更新
}

// 监听外部值变化更新位置
watch(() => props.modelValue, (newVal) => {
  // 这里可以加个判断，如果是滚动触发的变更则不重新 scrollTo
  // 简单起见暂不加
  // scrollToValue(newVal)
})
</script>

<style lang="scss" scoped>
.ruler-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.value-display {
  margin-bottom: 30px;
  display: flex;
  align-items: baseline;
  
  .value {
    font-size: 48px;
    font-weight: 800;
    color: var(--text-primary);
    font-family: 'DIN Alternate', sans-serif;
  }
  
  .unit {
    font-size: 16px;
    color: var(--text-secondary);
    margin-left: 8px;
    font-weight: 500;
  }
}

.ruler-wrapper {
  position: relative;
  width: 100%;
  height: 80px;
  
  .ruler-scroll {
    width: 100%;
    height: 100%;
    white-space: nowrap;
  }
  
  .ruler-content {
    height: 100%;
    display: flex;
    align-items: center;
    padding: 0 50vw; // 利用 padding 实现首尾留白
    box-sizing: border-box;
  }
  
  .ruler-scale {
    display: flex;
    align-items: flex-end;
    height: 40px;
    
    .scale-line {
      width: 1px; // 线宽
      margin-right: 9px; // 间距 = itemWidth - width
      height: 20px;
      background-color: #E5E5E5;
      flex-shrink: 0;
      
      &:last-child {
        margin-right: 0;
      }
      
      &.medium {
        height: 30px;
        background-color: #C7C7CC;
      }
      
      &.long {
        height: 40px;
        background-color: var(--color-primary);
        width: 2px;
        margin-right: 8px;
      }
    }
  }
  
  .pointer {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 4px;
    height: 50px;
    background-color: var(--color-success);
    border-radius: 2px;
    z-index: 10;
    
    &::after {
      content: '';
      position: absolute;
      bottom: -6px;
      left: 50%;
      transform: translateX(-50%);
      border: 6px solid transparent;
      border-top-color: var(--color-success);
    }
  }
  
  // 左右遮罩，制造立体感
  &::before, &::after {
    content: '';
    position: absolute;
    top: 0;
    bottom: 0;
    width: 20%;
    z-index: 5;
    pointer-events: none;
  }
  
  &::before {
    left: 0;
    background: linear-gradient(to right, #F5F5F7, transparent);
  }
  
  &::after {
    right: 0;
    background: linear-gradient(to left, #F5F5F7, transparent);
  }
}
</style>


