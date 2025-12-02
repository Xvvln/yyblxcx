<template>
  <view class="page">
    <!-- 顶部关闭按钮 - 移至左上角 -->
    <view class="close-area" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="close-btn" @click="handleClose">
        <text class="skip-text">跳过</text>
      </view>
    </view>

    <!-- 顶部视觉区 -->
    <view class="header-visual">
      <image class="bg-tech" src="/static/images/member-tech-bg.png" mode="aspectFill"></image>
      <!-- 这里使用 CSS 模拟参考图中的科技感分析图，实际开发建议切图 -->
      <view class="tech-overlay">
        <view class="scan-line"></view>
        <view class="data-card left-top">
          <text class="label">健康综合评分</text>
          <view class="score-display">
            <text class="score">85</text>
            <text class="sub">良好</text>
          </view>
          <view class="chart-bar-group">
            <view class="bar" style="height: 60%"></view>
            <view class="bar" style="height: 40%"></view>
            <view class="bar active" style="height: 85%"></view>
            <view class="bar" style="height: 50%"></view>
          </view>
        </view>
        <view class="data-card right-top">
          <text class="label">营养摄入分析</text>
          <view class="tag-row">
            <text class="tag green">蛋白质充足</text>
          </view>
          <view class="tag-row">
            <text class="tag orange">碳水控制</text>
          </view>
        </view>
        
        <!-- 新增：左下卡片 -->
        <view class="data-card left-bottom">
          <text class="label">有氧耐力评估</text>
          <view class="progress-bar">
            <view class="progress-val" style="width: 72%"></view>
          </view>
          <text class="sub-text">VO2max: 优秀</text>
        </view>
        
        <!-- 新增：右下卡片 -->
        <view class="data-card right-bottom">
          <text class="label">体态风险扫描</text>
          <view class="risk-item">
            <view class="dot red"></view>
            <text class="risk-name">骨盆前倾</text>
          </view>
          <view class="risk-item">
            <view class="dot green"></view>
            <text class="risk-name">脊柱正常</text>
          </view>
        </view>
        
        <view class="body-model">
          <!-- 模拟人体模型占位 -->
          <view class="model-shape"></view>
        </view>
        <!-- 底部文字 -->
        <view class="header-text-group">
          <text class="title">解锁 AI 智能健康方案</text>
          <text class="subtitle">精准饮食推荐 · 科学运动指导 · 实时健康追踪</text>
          <view class="dots">
            <view class="dot active"></view>
            <view class="dot"></view>
            <view class="dot"></view>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部卡片区 - 悬浮样式 -->
    <view class="card-container-wrapper">
      <!-- 浮动标签 -->
      <view class="float-tag">新人限时特惠</view>
      
      <view class="card-container">
        <!-- 套餐选择 -->
        <view class="plans-row">
          <!-- 7天特惠 -->
          <view 
            class="plan-item" 
            :class="{ active: selectedPlan === 'trial' }"
            @click="selectPlan('trial')"
          >
            <view class="plan-top-tag">7 天特惠</view>
            <view class="price-row">
              <text class="currency">¥</text>
              <text class="amount">0</text>
              <text class="unit">/月</text>
            </view>
            <text class="original-price">¥198/年</text>
            <view class="countdown">
              <text class="time">{{ countdown.m }}</text>:<text class="time">{{ countdown.s }}</text>:<text class="time ms">{{ countdown.ms }}</text>
            </view>
          </view>

          <!-- 半年会员 -->
          <view 
            class="plan-item" 
            :class="{ active: selectedPlan === 'half_year' }"
            @click="selectPlan('half_year')"
          >
            <view class="plan-name">半年会员</view>
            <view class="price-row">
              <text class="currency">¥</text>
              <text class="amount">25</text>
              <text class="unit">/月</text>
            </view>
            <text class="original-price">¥150/半年</text>
          </view>
        </view>

        <view class="tips">到期按 198 元/年自动续费，可随时取消</view>

        <!-- 底部按钮 -->
        <view class="action-area">
          <button class="main-btn" @click="handleSubscribe">
            {{ selectedPlan === 'trial' ? '免费试用 7 天' : '立即开通' }}
          </button>
          
          <view class="agreement" @click="toggleAgree">
            <view class="checkbox" :class="{ checked: agreed }">
              <wd-icon v-if="agreed" name="check" size="10px" color="#8B6943"></wd-icon>
            </view>
            <text>我已阅读并同意 <text class="link">会员服务协议</text> 和 <text class="link">自动续费服务声明</text></text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onUnmounted, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const statusBarHeight = ref(0)
const selectedPlan = ref('trial') // trial, half_year
const agreed = ref(false)
const reportId = ref('')

// 倒计时逻辑
const countdown = reactive({ m: '29', s: '59', ms: '99' })
let timer: any = null

function startCountdown() {
  let totalMs = 30 * 60 * 100 // 30分钟
  timer = setInterval(() => {
    totalMs--
    if (totalMs <= 0) {
      clearInterval(timer)
      return
    }
    const m = Math.floor(totalMs / 6000)
    const s = Math.floor((totalMs % 6000) / 100)
    const ms = totalMs % 100
    
    countdown.m = String(m).padStart(2, '0')
    countdown.s = String(s).padStart(2, '0')
    countdown.ms = String(ms).padStart(2, '0')
  }, 10)
}

onLoad((options) => {
  const sys = uni.getSystemInfoSync()
  statusBarHeight.value = sys.statusBarHeight || 20
  if (options && options.reportId) {
    reportId.value = options.reportId
  }
  startCountdown()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

function handleClose() {
  // 无论如何，直接回首页（跳过购买）
  uni.switchTab({ url: '/pages/index/index' })
}

function selectPlan(plan: string) {
  selectedPlan.value = plan
}

function toggleAgree() {
  agreed.value = !agreed.value
}

function handleSubscribe() {
  if (!agreed.value) {
    uni.showToast({ title: '请先同意协议', icon: 'none' })
    return
  }
  
  uni.showLoading({ title: '开通中...' })
  setTimeout(() => {
    uni.hideLoading()
    uni.showToast({ title: '开通成功', icon: 'success' })
    setTimeout(() => {
      handleClose() // 使用统一的关闭逻辑
    }, 1500)
  }, 1000)
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #1c1c1e;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* 关闭/跳过按钮 - 左上角 */
.close-area {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 20;
  display: flex;
  justify-content: flex-start;
  padding-left: 16px;
  padding-top: 10px;
  
  .close-btn {
    padding: 6px 12px;
    background: rgba(0,0,0,0.3);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255,255,255,0.1);
    
    .skip-text {
      color: rgba(255,255,255,0.8);
      font-size: 13px;
    }
  }
}

/* 顶部视觉区 */
.header-visual {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* 关键布局调整：为底部卡片留出空间，内容上移 */
  justify-content: flex-start; 
  padding-top: 15vh;
  background: radial-gradient(circle at 50% 30%, #2c2c2e 0%, #000000 100%);
  
  .bg-tech {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0.3;
  }
  
  .tech-overlay {
    width: 300px;
    height: 300px;
    position: relative;
    
    // 模拟人体发光模型
    .body-model {
      width: 120px;
      height: 240px;
      background: linear-gradient(180deg, #fff 0%, rgba(255,255,255,0.2) 100%);
      border-radius: 60px 60px 30px 30px;
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      filter: blur(20px);
      opacity: 0.5;
    }
    
    .scan-line {
      position: absolute;
      width: 100%;
      height: 2px;
      background: #00ff9d;
      top: 50%;
      box-shadow: 0 0 10px #00ff9d;
      animation: scan 3s infinite linear;
    }
    
    .data-card {
      position: absolute;
      background: rgba(255,255,255,0.1);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 8px;
      padding: 10px;
      backdrop-filter: blur(8px);
      z-index: 2; /* 确保在模型之上 */
      
      &.left-top {
        top: 10%;
        left: -15%; /* 稍微往外移一点 */
        width: 120px;
        
        .score-display {
          display: flex;
          align-items: baseline;
          margin: 4px 0;
          
          .score { font-size: 22px; font-weight: bold; color: #fff; margin-right: 4px; font-family: 'DIN Alternate', sans-serif; }
          .sub { font-size: 10px; color: #00ff9d; }
        }
        
        .chart-bar-group {
          display: flex;
          align-items: flex-end;
          height: 24px;
          gap: 6px;
          margin-top: 6px;
          
          .bar {
            width: 6px;
            background: rgba(255,255,255,0.2);
            border-radius: 2px;
            transition: height 0.5s;
            
            &.active { background: #00ff9d; box-shadow: 0 0 8px rgba(0, 255, 157, 0.4); }
          }
        }
      }
      
      &.right-top {
        top: 18%;
        right: -15%;
        
        .tag-row {
          margin-top: 8px;
          
          .tag {
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 4px;
            display: inline-block;
            white-space: nowrap;
            
            &.green { color: #00ff9d; border: 1px solid #00ff9d; background: rgba(0,255,157,0.1); }
            &.orange { color: #ff9d00; border: 1px solid #ff9d00; background: rgba(255,157,0,0.1); }
          }
        }
      }
      
      &.left-bottom {
        top: 55%;
        left: -12%;
        width: 110px;
        
        .progress-bar {
          height: 4px;
          background: rgba(255,255,255,0.2);
          border-radius: 2px;
          margin: 8px 0 4px;
          overflow: hidden;
          
          .progress-val {
            height: 100%;
            background: #00a8ff;
            border-radius: 2px;
          }
        }
        
        .sub-text {
          font-size: 10px;
          color: #00a8ff;
        }
      }
      
      &.right-bottom {
        top: 60%;
        right: -12%;
        width: 100px;
        
        .risk-item {
          display: flex;
          align-items: center;
          margin-top: 4px;
          
          .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            margin-right: 6px;
            
            &.red { background: #ff4d4d; box-shadow: 0 0 4px #ff4d4d; }
            &.green { background: #00ff9d; }
          }
          
          .risk-name {
            font-size: 10px;
            color: rgba(255,255,255,0.9);
          }
        }
      }
      
      .label {
        font-size: 11px;
        color: rgba(255,255,255,0.7);
        margin-bottom: 4px;
        display: block;
      }
    }
    
    .header-text-group {
      position: absolute;
      bottom: -80px;
      left: 0;
      right: 0;
      text-align: center;
      
      .title {
        font-size: 24px;
        font-weight: bold;
        color: #fff;
        display: block;
        margin-bottom: 8px;
        letter-spacing: 1px;
      }
      
      .subtitle {
        font-size: 14px;
        color: rgba(255,255,255,0.6);
      }
      
      .dots {
        display: flex;
        justify-content: center;
        gap: 6px;
        margin-top: 16px;
        
        .dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: rgba(255,255,255,0.2);
          
          &.active {
            background: #00ff9d;
            width: 12px;
            border-radius: 3px;
          }
        }
      }
    }
  }
}

/* 底部悬浮卡片区 */
.card-container-wrapper {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0 16px;
  padding-bottom: calc(20px + env(safe-area-inset-bottom));
}

.float-tag {
  display: inline-block;
  background: linear-gradient(90deg, #E6C288 0%, #D4A35C 100%);
  color: #5A3D1B;
  font-size: 12px;
  font-weight: bold;
  padding: 4px 12px;
  border-radius: 8px 8px 0 0;
  margin-left: 12px;
  position: relative;
  top: 2px;
  z-index: 2;
}

.card-container {
  background: #fff;
  border-radius: 20px;
  padding: 20px;
  position: relative;
  z-index: 1;
  
  .plans-row {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
    
    .plan-item {
      flex: 1;
      background: #fff;
      border: 1px solid #E5E5E5;
      border-radius: 12px;
      padding: 24px 12px 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
      transition: all 0.3s;
      overflow: hidden;
      
      &.active {
        background: #FFF9F0;
        border-color: #D4A35C;
        box-shadow: 0 4px 12px rgba(212, 163, 92, 0.1);
        
        .plan-top-tag {
          background: #D4A35C;
          color: #fff;
        }
      }
      
      .plan-top-tag {
        position: absolute;
        top: 0;
        left: 0;
        background: #E5E5E5;
        color: #86868B;
        font-size: 10px;
        padding: 2px 8px;
        border-radius: 0 0 8px 0;
      }
      
      .plan-name {
        font-size: 14px;
        font-weight: 600;
        color: #1D1D1F;
        margin-bottom: 8px;
      }
      
      .price-row {
        display: flex;
        align-items: baseline;
        color: #C89F63;
        margin: 4px 0;
        
        .currency { font-size: 14px; }
        .amount { font-size: 32px; font-weight: bold; margin: 0 2px; line-height: 1; }
        .unit { font-size: 12px; color: #C89F63; }
      }
      
      .original-price {
        font-size: 12px;
        color: #86868B;
        text-decoration: line-through;
        margin-bottom: 8px;
      }
      
      .countdown {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        color: #D4A35C;
        background: rgba(212, 163, 92, 0.1);
        padding: 2px 8px;
        border-radius: 4px;
        width: 100%;
        
        .time {
          font-weight: bold;
          min-width: 14px;
          text-align: center;
        }
      }
    }
  }
  
  .tips {
    font-size: 11px;
    color: #86868B;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .main-btn {
    width: 100%;
    height: 50px;
    background: linear-gradient(90deg, #E6C288 0%, #D4A35C 100%);
    border-radius: 25px;
    color: #5A3D1B;
    font-size: 18px;
    font-weight: bold;
    border: none;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(212, 163, 92, 0.3);
    
    &::after { border: none; }
    &:active { opacity: 0.9; }
  }
  
  .agreement {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 11px;
    color: #86868B;
    
    .checkbox {
      width: 14px;
      height: 14px;
      border: 1px solid #C7C7CC;
      border-radius: 50%;
      margin-right: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &.checked {
        border-color: #D4A35C;
        background: #D4A35C; /* 实心勾选 */
      }
    }
    
    .link {
      color: #86868B;
    }
  }
}

@keyframes scan {
  0% { top: 20%; opacity: 0; }
  50% { opacity: 1; }
  100% { top: 80%; opacity: 0; }
}
</style>

