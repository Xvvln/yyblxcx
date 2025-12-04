<template>
  <view class="page">
    <view class="header">
      <view class="score-container">
        <view class="score-circle" :class="result.risk_level">
          <view class="inner-circle">
            <text class="score-text">{{ result.bmi || '--' }}</text>
            <text class="score-label">BMI</text>
          </view>
        </view>
      </view>
      <text class="report-title">健康评估报告</text>
      <text class="report-date">{{ result.created_at || '刚刚' }}</text>
    </view>
    
    <view class="content">
      <!-- 核心结论 -->
      <view class="card highlight">
        <view class="card-header">
          <view class="icon-title">
            <wd-icon name="star-on" size="18px" color="#FF9500"></wd-icon>
            <text class="title">核心结论</text>
          </view>
        </view>
        <view class="risk-box" :class="result.risk_level">
          <view class="risk-header">
            <text class="risk-tag">{{ riskText(result.risk_level) }}</text>
            <text class="risk-summary">根据您的身体数据分析</text>
          </view>
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
          <view class="icon-title">
            <wd-icon name="chart-bar" size="18px" color="#0071e3"></wd-icon>
            <text class="title">身体指标</text>
          </view>
        </view>
        <view class="data-grid">
          <view class="data-item" v-if="result.height">
            <text class="data-val">{{ result.height }}<text class="unit">cm</text></text>
            <text class="data-label">身高</text>
          </view>
          <view class="data-item" v-if="result.weight">
            <text class="data-val">{{ result.weight }}<text class="unit">kg</text></text>
            <text class="data-label">体重</text>
          </view>
          <view class="data-item" v-if="result.heart_rate">
            <text class="data-val">{{ result.heart_rate }}<text class="unit">bpm</text></text>
            <text class="data-label">心率</text>
          </view>
          <view class="data-item" v-if="result.blood_pressure_high">
            <text class="data-val bp">{{ result.blood_pressure_high }}/{{ result.blood_pressure_low }}</text>
            <text class="data-label">血压 (mmHg)</text>
          </view>
        </view>
      </view>
      
      <!-- 专属计划 -->
      <view class="card plan-card">
        <view class="card-header">
          <view class="icon-title">
            <wd-icon name="edit-1" size="18px" color="#34C759"></wd-icon>
            <text class="title">专属改善计划</text>
          </view>
        </view>
        
        <view class="plan-list">
          <view class="plan-section" v-if="result.diet_suggestion">
            <view class="plan-icon food-bg">
              <wd-icon name="goods" size="20px" color="#34C759"></wd-icon>
            </view>
            <view class="plan-content">
              <text class="p-title">饮食建议</text>
              <text class="p-text">{{ result.diet_suggestion }}</text>
            </view>
          </view>
          
          <view class="plan-section" v-if="result.exercise_suggestion">
            <view class="plan-icon sport-bg">
              <wd-icon name="play-circle-fill" size="20px" color="#0071e3"></wd-icon>
            </view>
            <view class="plan-content">
              <text class="p-title">运动建议</text>
              <text class="p-text">{{ result.exercise_suggestion }}</text>
            </view>
          </view>
          
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
      </view>
      
      <!-- 推荐会员 -->
      <view class="vip-card" @click="goVip">
        <view class="vip-bg-pattern"></view>
        <view class="vip-left">
          <view class="vip-header">
            <wd-icon name="star-fill" size="16px" color="#F0D6A6" style="margin-right: 6px;"></wd-icon>
            <text class="vip-title">开通健康会员</text>
          </view>
          <text class="vip-desc">获取详细营养成分分析、定制食谱与专家一对一解读</text>
        </view>
        <view class="vip-btn">立即开通</view>
      </view>
    </view>
    
    <view class="footer">
      <button class="home-btn" hover-class="btn-hover" @click="goHome">完成</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getScreeningReport } from '@/api/health'
import dayjs from 'dayjs'

const result = ref<any>({})

function riskText(level: string) {
  const map: Record<string, string> = {
    low: '低风险',
    medium: '注意',
    high: '高风险'
  }
  return map[level] || '未知'
}

async function fetchReport(id: string) {
  try {
    const res = await getScreeningReport(Number(id))
    if (res.code === 200) {
      result.value = {
        ...res.data,
        created_at: res.data.created_at ? dayjs(res.data.created_at).format('YYYY年MM月DD日 HH:mm') : ''
      }
    }
  } catch (e) {
    console.error(e)
    uni.showToast({ title: '获取报告失败', icon: 'none' })
  }
}

function goHome() {
  // 如果有报告ID，且从生成页过来，跳转去会员引导
  if (result.value?.id) {
     uni.redirectTo({ url: `/pages/user/member-guide?reportId=${result.value.id}` })
  } else {
     uni.switchTab({ url: '/pages/index/index' })
  }
}

function goVip() {
  // 跳转到会员引导页
  uni.navigateTo({ url: `/pages/user/member-guide?reportId=${result.value?.id || ''}` })
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
  padding-bottom: 120px;
}

.header {
  background: linear-gradient(180deg, #FFFFFF 0%, #F5F5F7 100%);
  padding: 20px 20px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .score-container {
    position: relative;
    margin: 20px 0 24px;
    
    &::after {
      content: '';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 100%;
      height: 100%;
      border-radius: 50%;
      box-shadow: 0 10px 30px rgba(0,0,0,0.08);
      z-index: 0;
    }
  }
  
  .score-circle {
    position: relative;
    z-index: 1;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #FFFFFF;
    
    &.low { 
      border: 4px solid rgba(52, 199, 89, 0.2);
      .inner-circle { border: 4px solid #34C759; color: #34C759; }
    }
    &.medium { 
      border: 4px solid rgba(255, 149, 0, 0.2);
      .inner-circle { border: 4px solid #FF9500; color: #FF9500; }
    }
    &.high { 
      border: 4px solid rgba(255, 59, 48, 0.2);
      .inner-circle { border: 4px solid #FF3B30; color: #FF3B30; }
    }
    
    .inner-circle {
      width: 116px;
      height: 116px;
      border-radius: 50%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: #FFFFFF;
      
      .score-text {
        font-size: 42px;
        font-weight: 800;
        line-height: 1;
        font-family: "SF Pro Rounded", sans-serif;
        letter-spacing: -1px;
      }
      
      .score-label {
        font-size: 13px;
        font-weight: 600;
        margin-top: 4px;
        opacity: 0.8;
      }
    }
  }
  
  .report-title {
    font-size: 22px;
    font-weight: 700;
    color: #1D1D1F;
    letter-spacing: 0.5px;
  }
  
  .report-date {
    font-size: 13px;
    color: #86868B;
    margin-top: 6px;
    font-weight: 500;
  }
}

.content {
  padding: 0 20px;
  margin-top: -20px;
}

.card {
  background: #FFFFFF;
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
  transition: transform 0.2s;
  
  &:active {
    transform: scale(0.995);
  }
  
  .card-header {
    margin-bottom: 20px;
    
    .icon-title {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .title {
        font-size: 17px;
        font-weight: 700;
        color: #1D1D1F;
      }
    }
  }
}

.highlight {
  .risk-box {
    background: #F5F5F7;
    padding: 20px;
    border-radius: 16px;
    
    &.low { background: linear-gradient(135deg, #F2FCF4 0%, #E3F9E5 100%); }
    &.medium { background: linear-gradient(135deg, #FFF8E6 0%, #FFF3E0 100%); }
    &.high { background: linear-gradient(135deg, #FFF0F0 0%, #FFEBEE 100%); }
    
    .risk-header {
      display: flex;
      align-items: center;
      margin-bottom: 12px;
      gap: 8px;
      
      .risk-tag {
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 700;
        background: rgba(255,255,255,0.9);
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        
        .low & { color: #34C759; }
        .medium & { color: #FF9500; }
        .high & { color: #FF3B30; }
      }
      
      .risk-summary {
        font-size: 13px;
        color: rgba(0,0,0,0.5);
      }
    }
    
    .risk-desc {
      font-size: 15px;
      line-height: 1.6;
      color: #1D1D1F;
      display: block;
      text-align: justify;
    }
  }
  
  .risk-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
    
    .tag {
      padding: 6px 14px;
      background: #F5F5F7;
      border-radius: 100px;
      font-size: 12px;
      font-weight: 500;
      color: #666;
    }
  }
}

.data-card {
  .data-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    
    .data-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 16px;
      background: #F9F9FA;
      border-radius: 16px;
      
      .data-val {
        font-size: 20px;
        font-weight: 700;
        color: #1D1D1F;
        font-family: "SF Pro Rounded", sans-serif;
        
        &.bp { font-size: 18px; }
        
        .unit {
          font-size: 12px;
          font-weight: 500;
          color: #86868B;
          margin-left: 2px;
        }
      }
      
      .data-label {
        font-size: 12px;
        color: #86868B;
        margin-top: 6px;
      }
    }
  }
}

.plan-card {
  .plan-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    
    .plan-section {
      display: flex;
      align-items: flex-start;
      
      .plan-icon {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 14px;
        flex-shrink: 0;
        
        &.food-bg { background: #E3F9E5; }
        &.sport-bg { background: #E8F4FD; }
        &.life-bg { background: #FFF3E0; }
      }
      
      .plan-content {
        flex: 1;
        padding-top: 2px;
        
        .p-title {
          font-size: 15px;
          font-weight: 600;
          color: #1D1D1F;
          margin-bottom: 6px;
          display: block;
        }
        
        .p-text {
          font-size: 14px;
          color: #666;
          line-height: 1.6;
          display: block;
          text-align: justify;
        }
      }
    }
  }
}

.vip-card {
  background: #1D1D1F;
  border-radius: 24px;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  
  .vip-bg-pattern {
    position: absolute;
    top: -50%;
    right: -20%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(240, 214, 166, 0.2) 0%, rgba(240, 214, 166, 0) 70%);
    border-radius: 50%;
  }
  
  .vip-left {
    position: relative;
    z-index: 1;
    flex: 1;
    margin-right: 16px;
    
    .vip-header {
      display: flex;
      align-items: center;
      margin-bottom: 6px;
      
      .vip-title { 
        font-size: 17px; 
        font-weight: 700; 
        color: #F0D6A6;
      }
    }
    
    .vip-desc { 
      font-size: 12px; 
      color: rgba(255,255,255,0.7); 
      line-height: 1.4;
      display: block;
    }
  }
  
  .vip-btn {
    position: relative;
    z-index: 1;
    padding: 8px 16px;
    background: linear-gradient(135deg, #F0D6A6 0%, #D4B886 100%);
    border-radius: 18px;
    font-size: 13px;
    font-weight: 600;
    color: #1D1D1F;
    white-space: nowrap;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  }
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 32px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-top: 0.5px solid rgba(0,0,0,0.05);
  z-index: 10;
  
  .home-btn {
    width: 100%;
    height: 52px;
    background: #0071e3;
    border-radius: 26px;
    border: none;
    color: #FFFFFF;
    font-size: 17px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 20px rgba(0, 113, 227, 0.3);
    transition: all 0.2s;
    
    &::after { border: none; }
    
    &.btn-hover {
      transform: scale(0.98);
      box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
    }
  }
}
</style>
