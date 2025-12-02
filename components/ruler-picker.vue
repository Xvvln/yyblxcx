<template>
  <view class="ruler-picker">
    <!-- 数值显示 - 点击可手动输入 -->
    <view class="value-display" @click="handleManualInput">
      <text class="value">{{ displayValue }}</text>
      <text class="unit">{{ unit }}</text>
      <view class="edit-icon">
        <text class="edit-text">✎</text>
      </view>
    </view>

    <!-- 刻度尺容器 -->
    <view 
      class="ruler-wrapper" 
      :id="maskId"
      @touchstart="handleTouchStart"
      @touchmove.prevent="handleTouchMove"
      @touchend="handleTouchEnd"
      @touchcancel="handleTouchEnd"
    >
      <!-- 刻度条本体 -->
      <view 
        class="ruler-track"
        :style="{ 
          transform: `translateX(${currentX}px)`,
          transition: isDragging ? 'none' : 'transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        }"
      >
        <!-- 渲染刻度 -->
        <view 
          v-for="(tick, index) in ticks" 
          :key="index" 
          class="tick-item"
          :style="{ left: tick.left + 'px' }"
        >
          <view 
            class="tick-line"
            :class="{
              'long': tick.isLong,
              'medium': tick.isMedium
            }"
          ></view>
          <text 
            v-if="tick.label !== null" 
            class="tick-label"
          >{{ tick.label }}</text>
        </view>
      </view>

      <!-- 固定指针 -->
      <view class="pointer">
        <view class="pointer-triangle"></view>
      </view>
      
      <!-- 左右遮罩 -->
      <view class="mask-left"></view>
      <view class="mask-right"></view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch, getCurrentInstance, nextTick } from 'vue'

// 声明 uni 变量
declare const uni: any

const props = withDefaults(
  defineProps<{
    modelValue: number
    min: number
    max: number
    step?: number
    unit?: string
  }>(),
  {
    step: 1,
    unit: '',
  }
)

const emit = defineEmits(['update:modelValue', 'change'])

// 常量配置
const TICK_SPACING = 15 // 刻度间距加大到 15px，更易操控
const MASK_WIDTH = ref(375) // 容器宽度
const maskId = `ruler-${Math.random().toString(36).slice(2)}`

// 状态
const currentX = ref(0) // 这一刻度尺当前的translateX
const startX = ref(0) // 触摸开始时的手指位置
const startTranslateX = ref(0) // 触摸开始时的尺子位置
const isDragging = ref(false)

// 生成刻度数据
const ticks = computed(() => {
  // 强制按整数生成刻度，因为用户要求刻度尺单位为1cm/1kg
  // 范围 min 到 max
  const count = Math.floor((props.max - props.min) / 1) 
  const list: Array<{
    value: number, 
    left: number, 
    isLong: boolean, 
    isMedium: boolean, 
    label: number | null
  }> = []
  
  for (let i = 0; i <= count; i++) {
    const value = props.min + i
    const isLong = value % 10 === 0 // 10的倍数长刻度
    const isMedium = value % 5 === 0 && !isLong // 5的倍数中刻度
    
    // 每10个单位显示一次数字
    const showLabel = value % 10 === 0
    
    list.push({
      value: value,
      left: i * TICK_SPACING,
      isLong,
      isMedium,
      label: showLabel ? value : null
    })
  }
  return list
})

// 显示数值
// 如果用户手动输入了小数，modelValue可能是小数
// 拖动时，modelValue会变成整数
const displayValue = computed(() => {
  // 如果是整数，不显示小数点；如果是小数，保留1位
  return Number.isInteger(props.modelValue) ? props.modelValue : props.modelValue.toFixed(1)
})

onMounted(() => {
  const instance = getCurrentInstance()
  initLayout(instance)
})

function initLayout(instance: any) {
  if (!instance) return
  const query = uni.createSelectorQuery().in(instance)
  
  query.select(`#${maskId}`).boundingClientRect((rect: any) => {
    if (rect && rect.width > 0) {
      MASK_WIDTH.value = rect.width
      // 初始化位置
      scrollToValue(props.modelValue)
    } else {
      // 如果宽度无效（可能在弹窗动画中），延迟重试
      setTimeout(() => initLayout(instance), 100)
    }
  }).exec()
}

/**
 * 核心坐标公式：
 * 屏幕中心 = MASK_WIDTH / 2
 * 目标刻度相对于尺子起点的距离 = (value - min) * SPACING
 * 目标刻度在屏幕上的位置 = currentX + 目标刻度距离
 * 我们希望：目标刻度在屏幕上的位置 === 屏幕中心
 * 所以：currentX = 屏幕中心 - 目标刻度距离
 */
function calculateX(value: number) {
  // 找到最接近的整数刻度
  const roundedVal = Math.round(value)
  const index = roundedVal - props.min
  return (MASK_WIDTH.value / 2) - (index * TICK_SPACING)
}

/**
 * 反推公式：
 * currentX = Center - Index * Spacing
 * Index * Spacing = Center - currentX
 * Index = (Center - currentX) / Spacing
 */
function calculateValueFromX(x: number) {
  const center = MASK_WIDTH.value / 2
  const indexFloat = (center - x) / TICK_SPACING
  let index = Math.round(indexFloat)
  
  let val = props.min + index
  // 边界限制
  if (val < props.min) val = props.min
  if (val > props.max) val = props.max
  
  return val
}

// 移动尺子到指定数值的位置
function scrollToValue(val: number) {
  currentX.value = calculateX(val)
}

// 手动输入
function handleManualInput() {
  uni.showModal({
    title: `请输入${props.unit === '厘米' ? '身高' : '体重'}`,
    content: '',
    editable: true,
    placeholderText: '例如：175.5',
    success: (res: any) => {
      if (res.confirm && res.content) {
        let val = parseFloat(res.content)
        if (isNaN(val)) return
        
        // 范围限制
        if (val < props.min) val = props.min
        if (val > props.max) val = props.max
        
        // 保留一位小数
        val = Math.round(val * 10) / 10
        
        // 更新数值
        emit('update:modelValue', val)
        emit('change', val)
        
        // 尺子跳到最近的整数位置
        scrollToValue(val)
      }
    }
  })
}

// 触摸事件
function handleTouchStart(e: any) {
  if (e.touches.length !== 1) return
  isDragging.value = true
  startX.value = e.touches[0].pageX
  startTranslateX.value = currentX.value
}

function handleTouchMove(e: any) {
  if (!isDragging.value) return
  const moveX = e.touches[0].pageX - startX.value
  let newX = startTranslateX.value + moveX
  
  // 增加阻尼边界：允许拖出范围一点点
  const minX = calculateX(props.max) - 50
  const maxX = calculateX(props.min) + 50
  
  if (newX < minX) newX = minX
  if (newX > maxX) newX = maxX
  
  // 实时移动 DOM
  currentX.value = newX
  
  // 实时计算对应的整数数值
  const val = calculateValueFromX(newX)
  
  // 只有数值变化时才触发更新
  if (val !== Math.round(props.modelValue)) {
    emit('update:modelValue', val)
  }
}

function handleTouchEnd() {
  isDragging.value = false
  // 吸附：计算最近的整数刻度对应的位置
  const val = calculateValueFromX(currentX.value)
  const targetX = calculateX(val)
  
  // 触发吸附动画
  currentX.value = targetX
  
  // 确保最终值为整数
  emit('update:modelValue', val)
  emit('change', val)
}

// 监听 prop 变化（非拖拽时响应）
watch(() => props.modelValue, (newVal) => {
  if (!isDragging.value) {
    // 如果当前显示的整数值 和 尺子位置对应的整数值 不一致，才修正位置
    // 这样可以避免微小的小数变化导致尺子抖动
    // 但如果是手动输入的大变化，需要响应
    const currentRulerVal = calculateValueFromX(currentX.value)
    if (Math.round(newVal) !== currentRulerVal) {
      scrollToValue(newVal)
    }
  }
})
</script>

<style scoped lang="scss">
.ruler-picker {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.value-display {
  display: flex;
  align-items: baseline;
  margin-bottom: 20px;
  padding: 4px 12px;
  border-radius: 8px;
  background-color: #f8f8f8;
  transition: background-color 0.2s;

  &:active {
    background-color: #eee;
  }

  .value {
    font-size: 48px;
    font-weight: 800;
    color: #111;
    font-family: 'DIN Alternate', sans-serif;
  }

  .unit {
    font-size: 16px;
    color: #666;
    margin-left: 8px;
    font-weight: 500;
  }
  
  .edit-icon {
    margin-left: 8px;
    .edit-text {
      font-size: 14px;
      color: #2EBD59;
    }
  }
}

.ruler-wrapper {
  position: relative;
  width: 100%;
  height: 80px;
  overflow: hidden;
  background: #fff;
  touch-action: none;
}

.ruler-track {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  will-change: transform;
  /* transition由JS控制，拖拽时为none，松开时有动画 */
}

.tick-item {
  position: absolute;
  top: 0;
  width: 1px; 
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .tick-line {
    width: 1.5px;
    height: 20px;
    background: #E0E0E0;
    margin-top: 30px; 
    border-radius: 1px;
    
    &.medium {
      height: 30px;
      margin-top: 25px;
      background: #C0C0C0;
    }
    
    &.long {
      height: 40px;
      margin-top: 20px;
      background: #2EBD59; 
      width: 2px;
    }
  }
  
  .tick-label {
    position: absolute;
    bottom: 0;
    font-size: 12px;
    color: #999;
    transform: translateX(-50%);
    white-space: nowrap;
    font-family: 'DIN Alternate', sans-serif;
  }
}

.pointer {
  position: absolute;
  top: 20px; /* 调整指针垂直位置，对齐长刻度顶部 */
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
  
  .pointer-triangle {
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 10px solid #111;
    /* 不需要竖线，只保留三角，符合用户参考图 */
  }
}

/* 渐变遮罩增强 */
.mask-left, .mask-right {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 80px; /* 加宽遮罩 */
  z-index: 5;
  pointer-events: none;
}

.mask-left {
  left: 0;
  background: linear-gradient(to right, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 100%);
}

.mask-right {
  right: 0;
  background: linear-gradient(to left, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 100%);
}
</style>
