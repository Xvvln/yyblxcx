<template>
  <view class="page">
    <view class="header">
      <text class="title">健康筛查</text>
      <text class="subtitle">快速评估您的营养健康状况</text>
    </view>
    
    <!-- 筛查入口 -->
    <view class="screening-card" @click="startScreening">
      <view class="card-icon">
        <wd-icon name="file" size="28px" color="#FFFFFF"></wd-icon>
      </view>
      <view class="card-content">
        <text class="card-title">开始健康筛查</text>
        <text class="card-desc">问卷 + 数据采集 + AI分析</text>
      </view>
      <view class="card-arrow">
        <wd-icon name="arrow-right" size="18px" color="#86868B"></wd-icon>
      </view>
    </view>
    
    <!-- 历史记录 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">筛查记录</text>
        <text class="section-more" v-if="records.length > 3" @click="viewMore">查看全部</text>
      </view>
      
      <view class="record-list" v-if="records.length > 0">
        <view class="record-item" v-for="record in records.slice(0, 5)" :key="record.id" @click="viewReport(record.id)">
          <view class="record-left">
            <view class="record-date">{{ record.created_at }}</view>
            <view class="record-bmi" v-if="record.bmi">BMI: {{ record.bmi }}</view>
          </view>
          <view class="record-right">
            <text class="record-tag" :class="record.risk_level">{{ riskText(record.risk_level) }}</text>
            <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
          </view>
        </view>
      </view>
      
      <view class="empty" v-else>
        <view class="empty-icon">📋</view>
        <text class="empty-text">暂无筛查记录</text>
        <text class="empty-hint">完成首次筛查，获取健康建议</text>
      </view>
    </view>
    
    <!-- 健康趋势 -->
    <view class="section" v-if="records.length >= 2">
      <view class="section-header">
        <text class="section-title">BMI趋势</text>
      </view>
      <view class="trend-card">
        <view class="trend-chart">
          <view class="chart-placeholder">
            <text>趋势图</text>
          </view>
        </view>
        <view class="trend-summary">
          <text class="summary-text">
            最近{{ records.length }}次筛查，BMI变化 
            <text :class="bmiTrend > 0 ? 'up' : 'down'">{{ bmiTrend > 0 ? '+' : '' }}{{ bmiTrend }}</text>
          </text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getScreeningRecords } from '@/api/health'

interface ScreeningRecord {
  id: number
  bmi: number | null
  risk_level: 'low' | 'medium' | 'high'
  created_at: string
}

const records = ref<ScreeningRecord[]>([])
const loading = ref(false)

// 风险等级文字
function riskText(level: string) {
  const map: Record<string, string> = {
    low: '低风险',
    medium: '中风险',
    high: '高风险'
  }
  return map[level] || '未知'
}

// BMI趋势
const bmiTrend = computed(() => {
  if (records.value.length < 2) return 0
  const latest = records.value[0]?.bmi || 0
  const previous = records.value[1]?.bmi || 0
  return (latest - previous).toFixed(1)
})

// 获取记录
async function fetchRecords() {
  loading.value = true
  try {
    const res = await getScreeningRecords({ page: 1, page_size: 10 })
    if (res.code === 200) {
      records.value = res.data.list || []
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 开始筛查
function startScreening() {
  uni.navigateTo({ url: '/pages/health/basic-info' })
}

// 查看报告
function viewReport(id: number) {
  uni.navigateTo({ url: `/pages/health/result?id=${id}` })
}

// 查看更多
function viewMore() {
  // 可以跳转到历史记录列表页
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
}

.header {
  padding: 24px 0;
  
  .title {
    font-size: 28px;
    font-weight: 700;
    color: #1D1D1F;
    display: block;
  }
  
  .subtitle {
    font-size: 14px;
    color: #86868B;
    margin-top: 8px;
  }
}

.screening-card {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  
  .card-icon {
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #0071e3 0%, #34C759 100%);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .card-content {
    flex: 1;
    margin-left: 16px;
    
    .card-title {
      font-size: 17px;
      font-weight: 600;
      color: #1D1D1F;
      display: block;
    }
    
    .card-desc {
      font-size: 13px;
      color: #86868B;
      margin-top: 4px;
    }
  }
  
  .card-arrow {
    padding: 8px;
  }
}

.section {
  margin-bottom: 24px;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    
    .section-title {
      font-size: 17px;
      font-weight: 600;
      color: #1D1D1F;
    }
    
    .section-more {
      font-size: 13px;
      color: #0071e3;
    }
  }
}

.record-list {
  background: #FFFFFF;
  border-radius: 16px;
  overflow: hidden;
  
  .record-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid #F5F5F7;
    
    &:last-child {
      border-bottom: none;
    }
    
    .record-left {
      .record-date {
        font-size: 15px;
        color: #1D1D1F;
        font-weight: 500;
      }
      
      .record-bmi {
        font-size: 12px;
        color: #86868B;
        margin-top: 2px;
      }
    }
    
    .record-right {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .record-tag {
        font-size: 12px;
        font-weight: 500;
        padding: 4px 10px;
        border-radius: 10px;
        
        &.low { background: #E8F5E9; color: #34C759; }
        &.medium { background: #FFF3E0; color: #FF9500; }
        &.high { background: #FFEBEE; color: #FF3B30; }
      }
    }
  }
}

.empty {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 48px 16px;
  text-align: center;
  
  .empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }
  
  .empty-text {
    font-size: 15px;
    color: #1D1D1F;
    display: block;
  }
  
  .empty-hint {
    font-size: 13px;
    color: #86868B;
    margin-top: 8px;
  }
}

.trend-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 20px;
  
  .trend-chart {
    height: 120px;
    margin-bottom: 12px;
    
    .chart-placeholder {
      width: 100%;
      height: 100%;
      background: #F5F5F7;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #86868B;
      font-size: 14px;
    }
  }
  
  .trend-summary {
    text-align: center;
    
    .summary-text {
      font-size: 13px;
      color: #86868B;
      
      .up { color: #FF3B30; }
      .down { color: #34C759; }
    }
  }
}
</style>


