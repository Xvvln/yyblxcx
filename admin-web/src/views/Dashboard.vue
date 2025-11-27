<template>
  <div class="space-y-6">
    <!-- 数据概览卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="stat in statCards" :key="stat.label" class="bg-white rounded-xl p-6 shadow-apple-card hover:shadow-apple-hover transition-shadow duration-300">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-apple-text-gray">{{ stat.label }}</p>
            <p class="mt-2 text-3xl font-bold text-apple-dark">{{ stat.value }}</p>
          </div>
          <div :class="`p-3 rounded-full ${stat.bgClass}`">
            <el-icon :class="`text-xl ${stat.textClass}`"><component :is="stat.icon" /></el-icon>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span :class="stat.trend >= 0 ? 'text-green-500' : 'text-red-500'" class="font-medium flex items-center">
            {{ stat.trend >= 0 ? '+' : '' }}{{ stat.trend }}%
            <el-icon class="ml-1"><component :is="stat.trend >= 0 ? 'TopRight' : 'BottomRight'" /></el-icon>
          </span>
          <span class="ml-2 text-apple-text-gray">较昨日</span>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 主图表 -->
      <div class="lg:col-span-2 bg-white rounded-xl p-6 shadow-apple-card">
        <h3 class="text-lg font-semibold text-apple-dark mb-4">用户增长趋势</h3>
        <div ref="mainChartRef" class="h-80 w-full"></div>
      </div>

      <!-- 副图表 -->
      <div class="bg-white rounded-xl p-6 shadow-apple-card">
        <h3 class="text-lg font-semibold text-apple-dark mb-4">健康风险分布</h3>
        <div ref="pieChartRef" class="h-80 w-full"></div>
      </div>
    </div>

    <!-- 待处理事项 -->
    <div class="bg-white rounded-xl shadow-apple-card overflow-hidden">
      <div class="px-6 py-4 border-b border-apple-border flex items-center justify-between">
        <h3 class="text-lg font-semibold text-apple-dark">待处理事项</h3>
        <router-link to="/content" class="text-sm text-apple-blue hover:underline">查看全部</router-link>
      </div>
      <div class="divide-y divide-apple-border">
        <div v-for="item in todoList" :key="item.id" class="px-6 py-4 flex items-center justify-between hover:bg-apple-gray/50 transition-colors">
          <div class="flex items-center">
            <div :class="`w-2 h-2 rounded-full mr-4 ${item.priorityColor}`"></div>
            <div>
              <p class="text-sm font-medium text-apple-dark">{{ item.title }}</p>
              <p class="text-xs text-apple-text-gray mt-1">{{ item.time }}</p>
            </div>
          </div>
          <router-link :to="item.link" class="px-3 py-1 text-xs font-medium text-apple-blue bg-blue-50 rounded-full hover:bg-blue-100 transition-colors">
            处理
          </router-link>
        </div>
        <div v-if="todoList.length === 0" class="px-6 py-8 text-center text-apple-text-gray">
          暂无待处理事项
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, markRaw } from 'vue'
import * as echarts from 'echarts'
import { User, Goods, Money, TrendCharts, TopRight, BottomRight } from '@element-plus/icons-vue'
import { getOverview, getUserStats, getHealthStats } from '@/api/stats'

// 数据
const overview = ref<any>({})
const userStatsData = ref<any>({})
const healthStatsData = ref<any>({})

// 统计卡片
const statCards = computed(() => [
  { 
    label: '总用户数', 
    value: overview.value.users?.total?.toLocaleString() || '0', 
    trend: overview.value.users?.today_new && overview.value.users?.yesterday_new
      ? ((overview.value.users.today_new - overview.value.users.yesterday_new) / (overview.value.users.yesterday_new || 1) * 100).toFixed(1)
      : 0,
    icon: markRaw(User),
    bgClass: 'bg-blue-50',
    textClass: 'text-blue-500'
  },
  { 
    label: '今日订单', 
    value: overview.value.orders?.today_count?.toLocaleString() || '0', 
    trend: 0,
    icon: markRaw(Goods),
    bgClass: 'bg-orange-50',
    textClass: 'text-orange-500'
  },
  { 
    label: '今日收入', 
    value: `¥${(overview.value.orders?.today_amount || 0).toLocaleString()}`, 
    trend: 0,
    icon: markRaw(Money),
    bgClass: 'bg-green-50',
    textClass: 'text-green-500'
  },
  { 
    label: '今日打卡', 
    value: overview.value.activities?.today_checkins?.toLocaleString() || '0', 
    trend: 0,
    icon: markRaw(TrendCharts),
    bgClass: 'bg-purple-50',
    textClass: 'text-purple-500'
  },
])

const todoList = ref([
  { id: 1, title: '审核新发布的社区动态', time: '有待审核内容', priorityColor: 'bg-red-500', link: '/content' },
  { id: 2, title: '处理待发货订单', time: '有待处理订单', priorityColor: 'bg-orange-500', link: '/orders' },
])

const mainChartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()

// 获取数据
async function fetchData() {
  try {
    const [overviewRes, userStatsRes, healthStatsRes] = await Promise.all([
      getOverview(),
      getUserStats(7),
      getHealthStats(7),
    ])
    
    if (overviewRes.code === 200) {
      overview.value = overviewRes.data
    }
    if (userStatsRes.code === 200) {
      userStatsData.value = userStatsRes.data
      renderMainChart()
    }
    if (healthStatsRes.code === 200) {
      healthStatsData.value = healthStatsRes.data
      renderPieChart()
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 渲染主图表
function renderMainChart() {
  if (!mainChartRef.value) return
  
  const chart = echarts.init(mainChartRef.value)
  const dailyData = userStatsData.value.daily_new_users || []
  
  chart.setOption({
    grid: { top: 10, right: 10, bottom: 20, left: 40, containLabel: true },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: dailyData.map((d: any) => d.date.slice(5)),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#86868b' }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#f5f5f7' } },
      axisLabel: { color: '#86868b' }
    },
    series: [
      {
        name: '新增用户',
        data: dailyData.map((d: any) => d.count),
        type: 'line',
        smooth: true,
        showSymbol: false,
        lineStyle: { color: '#0071e3', width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(0, 113, 227, 0.2)' },
            { offset: 1, color: 'rgba(0, 113, 227, 0)' }
          ])
        }
      }
    ]
  })
  
  window.addEventListener('resize', () => chart.resize())
}

// 渲染饼图
function renderPieChart() {
  if (!pieChartRef.value) return
  
  const chart = echarts.init(pieChartRef.value)
  const riskData = healthStatsData.value.risk_distribution || []
  
  const colorMap: Record<string, string> = {
    low: '#34C759',
    medium: '#FF9500',
    high: '#FF3B30'
  }
  
  const nameMap: Record<string, string> = {
    low: '低风险',
    medium: '中风险',
    high: '高风险'
  }
  
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: '0%', left: 'center', icon: 'circle' },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: { show: false },
        data: riskData.map((item: any) => ({
          value: item.count,
          name: nameMap[item.level] || item.level,
          itemStyle: { color: colorMap[item.level] || '#999' }
        }))
      }
    ]
  })
  
  window.addEventListener('resize', () => chart.resize())
}

onMounted(() => {
  fetchData()
})
</script>
