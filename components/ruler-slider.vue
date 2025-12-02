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
      >
        <view class="ruler-content" :style="{ width: totalWidth + 'px' }">
          <view class="ruler-spacer" :style="{ width: spacerWidth + 'px' }"></view>
          <view class="ruler-scale">
            <view 
              v-for="i in count" 
              :key="i" 
              class="scale-item"
            >
              <view 
                class="scale-line"
                :class="{ 
                  'long': (i - 1) % 10 === 0,
                  'medium': (i - 1) % 5 === 0 && (i - 1) % 10 !== 0
                }"
              ></view>
              <!-- 添加数值显示 -->
              <text 
                v-if="(i - 1) % 10 === 0" 
                class="scale-text"
              >
                {{ min + (i - 1) * step }}
              </text>
            </view>
          </view>
          <view class="ruler-spacer" :style="{ width: spacerWidth + 'px' }"></view>
        </view>
      </scroll-view>
      
      <!-- 指针 -->
      <view class="pointer"></view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'

// 声明全局 uni 变量，防止 TS 报错
declare const uni: any

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
const spacerWidth = ref(0)

// 计算属性
const range = props.max - props.min
count.value = range / props.step + 1

onMounted(() => {
  uni.getSystemInfo({
    success: (res) => {
      screenWidth.value = res.windowWidth
      spacerWidth.value = res.windowWidth / 2
      totalWidth.value = count.value * itemWidth + res.windowWidth
      
      nextTick(() => {
        setTimeout(() => {
          scrollToValue(props.modelValue)
        }, 50)
      })
    }
  })
})

function scrollToValue(val: number) {
  const diff = val - props.min
  const steps = diff / props.step
  const targetLeft = steps * itemWidth + spacerWidth.value
  scrollLeft.value = targetLeft
}

let scrollTimer: any = null
let isScrolling = false

function onScroll(e: any) {
  isScrolling = true
  if (scrollTimer) clearTimeout(scrollTimer)
  
  const left = e.detail.scrollLeft
  const effectiveLeft = Math.max(left - spacerWidth.value, 0)
  
  scrollTimer = setTimeout(() => {
    const steps = Math.round(effectiveLeft / itemWidth)
    let val = props.min + steps * props.step
    
    if (val < props.min) val = props.min
    if (val > props.max) val = props.max
    
    const decimals = String(props.step).split('.')[1]?.length || 0
    val = Number(val.toFixed(decimals))
    
    if (val !== props.modelValue) {
      emit('update:modelValue', val)
    }
    
    const alignLeft = steps * itemWidth + spacerWidth.value
    if (Math.abs(alignLeft - left) > 1) {
      scrollLeft.value = alignLeft
    }
    
    isScrolling = false
  }, 100)
}

watch(() => props.modelValue, (newVal) => {
  if (!isScrolling) {
    scrollToValue(newVal)
  }
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
  height: 100px; /* 增加高度以容纳下方文字 */
  overflow: visible; /* 允许内容溢出容器（虽然增加高度后一般不需要） */
  
  .ruler-scroll {
    width: 100%;
    height: 100%;
    white-space: nowrap;
  }
  
.ruler-content {
  height: 100%;
  display: flex;
  align-items: flex-start;
  box-sizing: border-box;
  padding-top: 10px;
}

.ruler-spacer {
  height: 100%;
  flex-shrink: 0;
}
  
  .ruler-scale {
    display: flex;
    align-items: flex-start; /* 刻度线顶部对齐 */
    height: 80px; 
    
    .scale-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 10px; 
      flex-shrink: 0;
      position: relative;
    }

    .scale-line {
      width: 1px; 
      height: 20px;
      background-color: #E5E5E5;
      margin-bottom: 8px; /* 刻度线和文字的间距 */
      
      &.medium {
        height: 30px;
        background-color: #C7C7CC;
      }
      
      &.long {
        height: 40px;
        background-color: var(--color-primary);
        width: 2px;
      }
    }
    
    .scale-text {
      position: absolute;
      top: 45px; /* 调整文字位置，相对于 scale-item 顶部 */
      font-size: 12px;
      color: #86868B;
      transform: translateX(-50%);
      left: 50%;
      white-space: nowrap;
      font-weight: 500;
    }
  }
  
  .pointer {
    position: absolute;
    top: 10px;
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














