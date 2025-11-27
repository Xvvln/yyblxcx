<template>
  <view class="member-page">
    <!-- 会员信息卡片 -->
    <view class="member-card" :class="{ 'is-vip': memberInfo.is_member }">
      <view class="member-header">
        <view class="member-title">
          <text class="title">{{ memberInfo.member_level_name }}</text>
          <text v-if="memberInfo.is_member" class="expire">
            {{ memberInfo.expire_time ? `有效期至 ${memberInfo.expire_time.split(' ')[0]}` : '永久有效' }}
          </text>
        </view>
        <image v-if="memberInfo.is_member" class="vip-badge" src="/static/logo.png" mode="aspectFit" />
      </view>
      
      <view v-if="memberInfo.is_member" class="benefits-list">
        <view class="benefit-item" v-for="(benefit, index) in memberInfo.benefits" :key="index">
          <text class="benefit-icon">*</text>
          <text class="benefit-text">{{ benefit }}</text>
        </view>
      </view>
      
      <view v-else class="upgrade-hint">
        <text>升级会员享专属权益</text>
      </view>
    </view>
    
    <!-- 会员套餐 -->
    <view class="section">
      <view class="section-title">会员套餐</view>
      
      <view class="plan-list">
        <view 
          class="plan-item" 
          v-for="plan in plans" 
          :key="plan.id"
          :class="{ active: selectedPlan === plan.id }"
          @click="selectedPlan = plan.id"
        >
          <view class="plan-name">{{ plan.name }}</view>
          <view class="plan-price">
            <text class="currency">¥</text>
            <text class="amount">{{ plan.price }}</text>
          </view>
          <view class="plan-original">原价 ¥{{ plan.original_price }}</view>
          <view v-if="plan.id === 'year'" class="plan-tag">推荐</view>
        </view>
      </view>
    </view>
    
    <!-- 会员权益 -->
    <view class="section">
      <view class="section-title">会员权益</view>
      
      <view class="benefit-grid">
        <view class="benefit-card" v-for="(item, index) in benefitList" :key="index">
          <view class="benefit-icon-wrap">
            <text class="icon-text">{{ item.icon }}</text>
          </view>
          <text class="benefit-name">{{ item.name }}</text>
          <text class="benefit-desc">{{ item.desc }}</text>
        </view>
      </view>
    </view>
    
    <!-- 底部购买按钮 -->
    <view class="bottom-bar">
      <view class="price-info">
        <text class="label">应付：</text>
        <text class="price">¥{{ currentPlan?.price || 0 }}</text>
      </view>
      <button class="buy-btn" @click="handlePurchase" :loading="loading">
        {{ memberInfo.is_member ? '续费会员' : '立即开通' }}
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getMemberInfo, getMemberPlans, purchaseMember } from '@/api/member'

const loading = ref(false)
const selectedPlan = ref('year')

const memberInfo = ref({
  is_member: false,
  member_level: 0,
  member_level_name: '普通用户',
  expire_time: null as string | null,
  benefits: [] as string[]
})

const plans = ref<any[]>([])

const currentPlan = computed(() => {
  return plans.value.find(p => p.id === selectedPlan.value)
})

const benefitList = [
  { icon: '价', name: '专属会员价', desc: '商品享会员专属折扣' },
  { icon: '分', name: '积分加成', desc: '签到运动积分翻倍' },
  { icon: '服', name: '优先客服', desc: '专属客服优先响应' },
  { icon: '礼', name: '专属活动', desc: '会员专属福利活动' },
]

async function fetchData() {
  try {
    // 获取会员信息
    const infoRes = await getMemberInfo()
    if (infoRes.code === 200) {
      memberInfo.value = infoRes.data
    }
    
    // 获取套餐列表
    const plansRes = await getMemberPlans()
    if (plansRes.code === 200) {
      plans.value = plansRes.data
    }
  } catch (error) {
    console.error('获取会员信息失败:', error)
  }
}

async function handlePurchase() {
  if (!currentPlan.value) {
    uni.showToast({ title: '请选择套餐', icon: 'none' })
    return
  }
  
  loading.value = true
  try {
    const res = await purchaseMember({
      plan_type: selectedPlan.value,
      pay_type: 'wechat'
    })
    
    if (res.code === 200) {
      uni.showToast({ title: '购买成功', icon: 'success' })
      // 刷新会员信息
      await fetchData()
    } else {
      uni.showToast({ title: res.message || '购买失败', icon: 'none' })
    }
  } catch (error: any) {
    uni.showToast({ title: error.message || '购买失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style lang="scss" scoped>
.member-page {
  min-height: 100vh;
  background: #f5f5f7;
  padding-bottom: 120rpx;
}

.member-card {
  margin: 24rpx;
  padding: 40rpx;
  background: linear-gradient(135deg, #0071e3 0%, #00C7BE 100%);
  border-radius: 24rpx;
  color: #fff;
  
  &.is-vip {
    background: linear-gradient(135deg, #FF9500 0%, #FF6B00 100%);
  }
  
  .member-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
  
  .member-title {
    .title {
      font-size: 40rpx;
      font-weight: 600;
      display: block;
    }
    
    .expire {
      font-size: 24rpx;
      opacity: 0.8;
      margin-top: 8rpx;
      display: block;
    }
  }
  
  .vip-badge {
    width: 80rpx;
    height: 80rpx;
  }
  
  .benefits-list {
    margin-top: 32rpx;
    
    .benefit-item {
      display: flex;
      align-items: center;
      margin-bottom: 12rpx;
      
      .benefit-icon {
        margin-right: 12rpx;
        font-size: 24rpx;
      }
      
      .benefit-text {
        font-size: 26rpx;
      }
    }
  }
  
  .upgrade-hint {
    margin-top: 32rpx;
    font-size: 28rpx;
    opacity: 0.9;
  }
}

.section {
  margin: 24rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 32rpx;
  
  .section-title {
    font-size: 32rpx;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 24rpx;
  }
}

.plan-list {
  display: flex;
  gap: 20rpx;
  
  .plan-item {
    flex: 1;
    padding: 24rpx;
    border: 2rpx solid #d2d2d7;
    border-radius: 16rpx;
    text-align: center;
    position: relative;
    transition: all 0.3s;
    
    &.active {
      border-color: #0071e3;
      background: rgba(0, 113, 227, 0.05);
    }
    
    .plan-name {
      font-size: 28rpx;
      color: #1d1d1f;
      margin-bottom: 16rpx;
    }
    
    .plan-price {
      color: #f12711;
      
      .currency {
        font-size: 24rpx;
      }
      
      .amount {
        font-size: 44rpx;
        font-weight: 600;
      }
    }
    
    .plan-original {
      font-size: 22rpx;
      color: #86868b;
      text-decoration: line-through;
      margin-top: 8rpx;
    }
    
    .plan-tag {
      position: absolute;
      top: -2rpx;
      right: -2rpx;
      background: #f12711;
      color: #fff;
      font-size: 20rpx;
      padding: 4rpx 12rpx;
      border-radius: 0 16rpx 0 16rpx;
    }
  }
}

.benefit-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
  
  .benefit-card {
    background: #f5f5f7;
    border-radius: 12rpx;
    padding: 24rpx;
    text-align: center;
    
    .benefit-icon-wrap {
      width: 72rpx;
      height: 72rpx;
      background: linear-gradient(135deg, #0071e3 0%, #00c6ff 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 16rpx;
      
      .icon-text {
        color: #fff;
        font-size: 28rpx;
        font-weight: 600;
      }
    }
    
    .benefit-name {
      display: block;
      font-size: 28rpx;
      color: #1d1d1f;
      font-weight: 500;
      margin-bottom: 8rpx;
    }
    
    .benefit-desc {
      display: block;
      font-size: 22rpx;
      color: #86868b;
    }
  }
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.05);
  
  .price-info {
    .label {
      font-size: 26rpx;
      color: #86868b;
    }
    
    .price {
      font-size: 40rpx;
      font-weight: 600;
      color: #f12711;
    }
  }
  
  .buy-btn {
    background: linear-gradient(135deg, #0071e3 0%, #00c6ff 100%);
    color: #fff;
    font-size: 30rpx;
    font-weight: 500;
    padding: 24rpx 64rpx;
    border-radius: 48rpx;
    border: none;
    
    &::after {
      border: none;
    }
  }
}
</style>

