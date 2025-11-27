<template>
  <view class="gender-selector">
    <view 
      class="gender-card male" 
      :class="{ active: modelValue === 1 }"
      @click="select(1)"
    >
      <view class="icon-box">
        <wd-icon name="user" size="40px" color="#007AFF"></wd-icon>
      </view>
      <text class="label">男生</text>
      <view class="check-icon" v-if="modelValue === 1">
        <wd-icon name="check" color="#FFFFFF" size="14px"></wd-icon>
      </view>
    </view>
    
    <view 
      class="gender-card female" 
      :class="{ active: modelValue === 2 }"
      @click="select(2)"
    >
      <view class="icon-box">
        <wd-icon name="user" size="40px" color="#FF2D55"></wd-icon>
      </view>
      <text class="label">女生</text>
      <view class="check-icon" v-if="modelValue === 2">
        <wd-icon name="check" color="#FFFFFF" size="14px"></wd-icon>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
defineProps({
  modelValue: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update:modelValue'])

function select(val: number) {
  emit('update:modelValue', val)
}
</script>

<style lang="scss" scoped>
.gender-selector {
  display: flex;
  justify-content: center;
  gap: 24px;
  padding: 40px 0;
}

.gender-card {
  width: 140px;
  height: 180px;
  background: #FFFFFF;
  border-radius: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  
  .icon-box {
    width: 80px;
    height: 80px;
    background: #F5F5F7;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
  }
  
  .label {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
  }
  
  .check-icon {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 24px;
    height: 24px;
    background: var(--color-primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  &.active {
    border-color: var(--color-primary);
    background: #E8F2FF;
    
    .icon-box {
      background: #FFFFFF;
    }
    
    &.male {
      border-color: #007AFF;
      background: #E5F1FF;
      .check-icon { background: #007AFF; }
    }
    
    &.female {
      border-color: #FF2D55;
      background: #FFF0F2;
      .check-icon { background: #FF2D55; }
    }
  }
}
</style>
