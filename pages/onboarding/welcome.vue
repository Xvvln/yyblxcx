<template>
  <view class="welcome-container">
    <view class="bg-elements">
      <!-- 装饰性漂浮元素 -->
      <view class="float-item item-1">
        <wd-icon name="chart-pie" size="40px" color="#FFB74D"></wd-icon>
      </view>
      <view class="float-item item-2">
        <wd-icon name="activity" size="32px" color="#4DB6AC"></wd-icon>
      </view>
      <view class="float-item item-3">
        <wd-icon name="thumb-up" size="28px" color="#F06292"></wd-icon>
      </view>
      <view class="float-item item-4">
        <wd-icon name="time" size="36px" color="#7986CB"></wd-icon>
      </view>
    </view>

    <view class="content">
      <!-- 顶部装饰 -->
      <view class="top-decoration">
        <view class="squiggle"></view>
        <view class="star"></view>
      </view>

      <!-- 主标题区域 -->
      <view class="header">
        <view class="title-group">
          <text class="welcome-text">欢迎来到</text>
          <text class="app-name">Health Keep</text>
        </view>
        <view class="subtitle">
          <text>通过几个简单问题</text>
          <text>让我们更了解你</text>
        </view>
      </view>

      <!-- 中心插图区域 (使用图标组合模拟3D效果) -->
      <view class="illustration">
        <view class="center-icon">
          <view class="circle-bg"></view>
          <wd-icon name="user-circle" size="80px" color="#FFFFFF"></wd-icon>
        </view>
        
        <!-- 环绕图标 -->
        <view class="orbit-icon icon-sport">
          <wd-icon name="play-circle-fill" size="32px" color="#0071e3"></wd-icon>
        </view>
        <view class="orbit-icon icon-food">
          <wd-icon name="goods" size="32px" color="#34C759"></wd-icon>
        </view>
        <view class="orbit-icon icon-health">
          <wd-icon name="heart" size="32px" color="#FF3B30"></wd-icon>
        </view>
      </view>

      <!-- 底部按钮 -->
      <view class="footer">
        <button class="start-btn" hover-class="btn-hover" @click="handleStart">
          现在开始
        </button>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
function handleStart() {
  // 跳转到基础信息填写页
  uni.redirectTo({
    url: '/pages/health/basic-info'
  })
}
</script>

<style lang="scss" scoped>
.welcome-container {
  height: 100vh;
  background: linear-gradient(180deg, #FFF5F5 0%, #FFFFFF 40%, #F0F9FF 100%);
  position: relative;
  overflow: hidden;
}

// 背景漂浮元素动画
.bg-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;

  .float-item {
    position: absolute;
    opacity: 0.6;
    animation: float 6s ease-in-out infinite;
    
    &.item-1 { top: 15%; left: 10%; animation-delay: 0s; transform: rotate(-15deg); }
    &.item-2 { top: 25%; right: 15%; animation-delay: 1s; transform: rotate(10deg); }
    &.item-3 { bottom: 30%; left: 15%; animation-delay: 2s; transform: rotate(-10deg); }
    &.item-4 { bottom: 20%; right: 10%; animation-delay: 3s; transform: rotate(15deg); }
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

.content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  padding: 0 32px;
  padding-top: calc(100px + env(safe-area-inset-top));
  box-sizing: border-box;
}

.top-decoration {
  position: absolute;
  top: 60px;
  width: 100%;
  
  .squiggle {
    position: absolute;
    left: 20%;
    top: 0;
    width: 40px;
    height: 40px;
    border: 4px solid #FFD54F;
    border-radius: 50% 0 50% 0;
    transform: rotate(45deg);
  }
  
  .star {
    position: absolute;
    right: 25%;
    top: 20px;
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-bottom: 20px solid #90CAF9;
    transform: rotate(35deg);
    
    &::after {
      content: '';
      position: absolute;
      top: 6px;
      left: -10px;
      width: 0;
      height: 0;
      border-left: 10px solid transparent;
      border-right: 10px solid transparent;
      border-top: 20px solid #90CAF9;
    }
  }
}

.header {
  text-align: center;
  margin-bottom: 60px;
  
  .title-group {
    margin-bottom: 24px;
    
    .welcome-text {
      display: block;
      font-size: 24px;
      color: #666;
      margin-bottom: 8px;
    }
    
    .app-name {
      display: block;
      font-size: 36px;
      font-weight: 800;
      color: #1D1D1F;
      letter-spacing: 1px;
    }
  }
  
  .subtitle {
    display: flex;
    flex-direction: column;
    gap: 8px;
    
    text {
      font-size: 20px;
      font-weight: 600;
      color: #333;
      letter-spacing: 0.5px;
    }
  }
}

.illustration {
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 60px;
  
  .center-icon {
    position: relative;
    z-index: 2;
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, #0071e3 0%, #42A5F5 100%);
    border-radius: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 20px 40px rgba(0, 113, 227, 0.3);
    transform: rotate(-10deg);
    
    .circle-bg {
      position: absolute;
      width: 90%;
      height: 90%;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
    }
  }
  
  .orbit-icon {
    position: absolute;
    width: 56px;
    height: 56px;
    background: #FFFFFF;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    z-index: 3;
    
    &.icon-sport {
      top: 0;
      right: -20px;
      transform: rotate(15deg);
      animation: bounce 4s ease-in-out infinite;
    }
    
    &.icon-food {
      bottom: 20px;
      left: -30px;
      transform: rotate(-10deg);
      animation: bounce 4s ease-in-out infinite 1s;
    }
    
    &.icon-health {
      bottom: -20px;
      right: 10px;
      transform: rotate(20deg);
      animation: bounce 4s ease-in-out infinite 2s;
    }
  }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0) rotate(var(--rotation)); }
  50% { transform: translateY(-10px) rotate(var(--rotation)); }
}

.footer {
  position: fixed;
  bottom: calc(150px + env(safe-area-inset-bottom));
  left: 0;
  right: 0;
  padding: 0 40px;
  z-index: 10;
  box-sizing: border-box;
  
  .start-btn {
    width: 100%;
    background: #0071e3; // 主题蓝
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 600;
    height: 56px;
    border-radius: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    box-shadow: 0 8px 24px rgba(0, 113, 227, 0.3);
    transition: all 0.3s;
    
    &::after { border: none; }
    
    &.btn-hover {
      transform: scale(0.98);
      box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
    }
  }
}
</style>

