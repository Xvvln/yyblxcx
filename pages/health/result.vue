<template>
  <view class="page">
    <view class="header">
      <view class="score-circle" :class="result.risk_level">
        <text class="score-text">{{ result.bmi || '--' }}</text>
        <text class="score-label">BMI</text>
      </view>
      <text class="report-title">评估报告</text>
      <text class="report-date">{{ result.created_at }}</text>
    </view>
    
    <view class="content">
      <!-- 核心结论 -->
      <view class="card highlight">
        <view class="card-header">
          <text class="title">核心结论</text>
        </view>
        <view class="risk-box" :class="result.risk_level">
          <text class="risk-tag">{{ riskText(result.risk_level) }}</text>
          <text class="risk-desc">{{ result.ai_suggestion }}</text>
        </view>
        
        <!-- 风险标签 -->
        <view class="risk-tags" v-if="result.risk_tags?.length">
          <text class="tag" v-for="(tag, index) in result.risk_tags" :key="index">{{ tag }}</text>
        </view>
      </view>
      
      <!-- 健康数据 -->
      <view class="card data-card" v-if="result.height || result.weight">
        <view class="card-header">
          <text class="title">健康数据</text>
        </view>
        <view class="data-grid">
          <view class="data-item" v-if="result.height">
            <text class="data-val">{{ result.height }}</text>
            <text class="data-label">身高(cm)</text>
          </view>
          <view class="data-item" v-if="result.weight">
            <text class="data-val">{{ result.weight }}</text>
            <text class="data-label">体重(kg)</text>
          </view>
          <view class="data-item" v-if="result.heart_rate">
            <text class="data-val">{{ result.heart_rate }}</text>
            <text class="data-label">心率</text>
          </view>
          <view class="data-item" v-if="result.blood_pressure_high">
            <text class="data-val">{{ result.blood_pressure_high }}/{{ result.blood_pressure_low }}</text>
            <text class="data-label">血压</text>
          </view>
        </view>
      </view>
      
      <!-- 专属计划 -->
      <view class="card plan-card">
        <view class="card-header">
          <text class="title">专属改善计划</text>
        </view>
        
        <view class="plan-section" v-if="result.diet_suggestion">
          <view class="plan-icon food-bg">
            <wd-icon name="edit" size="20px" color="#34C759"></wd-icon>
          </view>
          <view class="plan-content">
            <text class="p-title">饮食建议</text>
            <text class="p-text">{{ result.diet_suggestion }}</text>
          </view>
        </view>
        
        <view class="divider" v-if="result.diet_suggestion && result.exercise_suggestion"></view>
        
        <view class="plan-section" v-if="result.exercise_suggestion">
          <view class="plan-icon sport-bg">
            <wd-icon name="check-circle" size="20px" color="#0071e3"></wd-icon>
          </view>
          <view class="plan-content">
            <text class="p-title">运动建议</text>
            <text class="p-text">{{ result.exercise_suggestion }}</text>
          </view>
        </view>
        
        <view class="divider" v-if="result.exercise_suggestion && result.lifestyle_suggestion"></view>
        
        <view class="plan-section" v-if="result.lifestyle_suggestion">
          <view class="plan-icon life-bg">
            <wd-icon name="tips" size="20px" color="#FF9500"></wd-icon>
          </view>
          <view class="plan-content">
            <text class="p-title">生活方式</text>
            <text class="p-text">{{ result.lifestyle_suggestion }}</text>
          </view>
        </view>
      </view>
      
      <!-- 推荐会员 -->
      <view class="vip-card" @click="goVip">
        <view class="vip-left">
          <text class="vip-title">开通健康会员</text>
          <text class="vip-desc">获取详细营养成分分析与食谱</text>
        </view>
        <view class="vip-btn">了解更多</view>
      </view>
    </view>
    
    <view class="footer">
      <button class="home-btn" @click="goHome">返回首页</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getScreeningReport } from '@/api/health'

const result = ref<any>({})

function riskText(level: string) {
  const map: Record<string, string> = {
    low: '低风险',
    medium: '中风险',
    high: '高风险'
  }
  return map[level] || '未知'
}

async function fetchReport(id: string) {
  try {
    const res = await getScreeningReport(Number(id))
    if (res.code === 200) {
      result.value = res.data
    }
  } catch (e) {
    console.error(e)
    uni.showToast({ title: '获取报告失败', icon: 'none' })
  }
}

function goHome() {
  uni.switchTab({ url: '/pages/index/index' })
}

function goVip() {
  uni.navigateTo({ url: '/pages/user/points' })
}

onLoad((options) => {
  if (options?.id) {
    fetchReport(options.id)
  }
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
  padding-bottom: 100px;
}

.header {
  background: #FFFFFF;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 0 0 32px 32px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  
  .score-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    border: 6px solid;
    
    &.low { border-color: #34C759; color: #34C759; }
    &.medium { border-color: #FF9500; color: #FF9500; }
    &.high { border-color: #FF3B30; color: #FF3B30; }
    
    .score-text {
      font-size: 36px;
      font-weight: 800;
      line-height: 1;
    }
    
    .score-label {
      font-size: 12px;
      opacity: 0.8;
      margin-top: 4px;
    }
  }
  
  .report-title {
    font-size: 20px;
    font-weight: 600;
    color: #1D1D1F;
  }
  
  .report-date {
    font-size: 12px;
    color: #86868B;
    margin-top: 4px;
  }
}

.content {
  padding: 20px;
  margin-top: -20px;
}

.card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    .title { font-size: 16px; font-weight: 700; color: #1D1D1F; }
  }
}

.highlight {
  .risk-box {
    background: #F5F5F7;
    padding: 16px;
    border-radius: 12px;
    
    &.low { background: #E8F5E9; }
    &.medium { background: #FFF3E0; }
    &.high { background: #FFEBEE; }
    
    .risk-tag {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
      margin-bottom: 8px;
      background: rgba(255,255,255,0.8);
    }
    
    .risk-desc {
      font-size: 14px;
      line-height: 1.6;
      color: #1D1D1F;
      display: block;
    }
  }
  
  .risk-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
    
    .tag {
      padding: 4px 12px;
      background: #F5F5F7;
      border-radius: 12px;
      font-size: 12px;
      color: #86868B;
    }
  }
}

.data-card {
  .data-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    
    .data-item {
      text-align: center;
      padding: 12px;
      background: #F5F5F7;
      border-radius: 12px;
      
      .data-val {
        font-size: 24px;
        font-weight: 700;
        color: #1D1D1F;
        display: block;
      }
      
      .data-label {
        font-size: 12px;
        color: #86868B;
        margin-top: 4px;
      }
    }
  }
}

.plan-card {
  .plan-section {
    display: flex;
    
    .plan-icon {
      width: 40px;
      height: 40px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 12px;
      flex-shrink: 0;
      
      &.food-bg { background: #E3F9E5; }
      &.sport-bg { background: #E8F4FD; }
      &.life-bg { background: #FFF3E0; }
    }
    
    .plan-content {
      flex: 1;
      
      .p-title {
        font-size: 14px;
        font-weight: 600;
        color: #1D1D1F;
        margin-bottom: 4px;
        display: block;
      }
      
      .p-text {
        font-size: 13px;
        color: #86868B;
        line-height: 1.5;
      }
    }
  }
  
  .divider {
    height: 1px;
    background: #F5F5F7;
    margin: 16px 0 16px 52px;
  }
}

.vip-card {
  background: linear-gradient(135deg, #1D1D1F 0%, #3a3a3c 100%);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #F0D6A6;
  
  .vip-left {
    .vip-title { font-size: 16px; font-weight: 700; display: block; margin-bottom: 4px; }
    .vip-desc { font-size: 12px; opacity: 0.8; }
  }
  
  .vip-btn {
    padding: 8px 16px;
    background: rgba(240, 214, 166, 0.2);
    border-radius: 16px;
    font-size: 13px;
    font-weight: 500;
  }
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px 20px;
  padding-bottom: 40px;
  background: #FFFFFF;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .home-btn {
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
  }
}
</style>
