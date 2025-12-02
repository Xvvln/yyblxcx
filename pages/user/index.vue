<template>
  <view class="page">
    <!-- 沉浸式头部 -->
    <view class="profile-header">
      <view class="header-content">
        <view class="user-row" @click="navigateTo('/pages/user/profile')">
          <view class="avatar-box">
            <image v-if="userStore.avatar" :src="userStore.avatar" class="avatar-img" mode="aspectFill" />
            <view v-else class="avatar-placeholder">
              <text>{{ userStore.nickname?.charAt(0) || '?' }}</text>
            </view>
          </view>
          <view class="user-info">
            <view class="name-wrap">
              <text class="nickname">{{ userStore.nickname || '未登录' }}</text>
              <view class="vip-badge" v-if="userStore.isVip">PRO</view>
            </view>
            <text class="uid">ID: {{ userStore.userInfo?.id || '--' }}</text>
          </view>
          <wd-icon name="arrow-right" size="18px" color="#C7C7CC"></wd-icon>
        </view>
        
        <!-- 数据概览 (悬浮卡片) -->
        <view class="stats-card">
          <view class="stat-item" @click="navigateTo('/pages/user/points')">
            <text class="val">{{ userStore.sportCoins }}</text>
            <text class="label">运动币</text>
          </view>
          <view class="v-line"></view>
          <view class="stat-item" @click="navigateTo('/pages/user/points')">
            <text class="val">{{ userStore.foodCoins }}</text>
            <text class="label">膳食币</text>
          </view>
          <view class="v-line"></view>
          <view class="stat-item">
            <text class="val">{{ userStore.userInfo?.continuous_checkin_days || 0 }}</text>
            <text class="label">连续打卡</text>
          </view>
        </view>
      </view>
    </view>
    
    <!-- 订单入口 -->
    <view class="order-section">
      <view class="section-header">
        <text class="title">我的订单</text>
        <view class="more" @click="navigateTo('/pages/order/index')">
          <text>全部订单</text>
          <wd-icon name="arrow-right" size="14px" color="#86868B"></wd-icon>
        </view>
      </view>
      <view class="order-tabs">
        <view class="order-tab" @click="navigateTo('/pages/order/index?status=1')">
          <view class="tab-icon">
            <wd-icon name="wallet" size="24px" color="#FF9500"></wd-icon>
          </view>
          <text class="tab-name">待付款</text>
        </view>
        <view class="order-tab" @click="navigateTo('/pages/order/index?status=2')">
          <view class="tab-icon">
            <wd-icon name="deliver" size="24px" color="#0071e3"></wd-icon>
          </view>
          <text class="tab-name">待发货</text>
        </view>
        <view class="order-tab" @click="navigateTo('/pages/order/index?status=3')">
          <view class="tab-icon">
            <wd-icon name="logistics" size="24px" color="#34C759"></wd-icon>
          </view>
          <text class="tab-name">待收货</text>
        </view>
        <view class="order-tab" @click="navigateTo('/pages/order/index?status=4')">
          <view class="tab-icon">
            <wd-icon name="comment" size="24px" color="#FF3B30"></wd-icon>
          </view>
          <text class="tab-name">已完成</text>
        </view>
      </view>
    </view>
    
    <!-- 功能菜单区 -->
    <view class="menu-section">
      <view class="menu-card">
        <view class="menu-title">我的服务</view>
        <view class="grid-menu">
          <view class="grid-item" @click="navigateTo('/pages/health/index')">
            <view class="icon file-icon">
              <wd-icon name="file" size="24px" color="#34C759"></wd-icon>
            </view>
            <text class="label">健康档案</text>
          </view>
          <view class="grid-item" @click="navigateTo('/pages/shop/collect')">
            <view class="icon star-icon">
              <wd-icon name="star" size="24px" color="#FF9500"></wd-icon>
            </view>
            <text class="label">我的收藏</text>
          </view>
          <view class="grid-item" @click="navigateTo('/pages/address/index')">
            <view class="icon loc-icon">
              <wd-icon name="location" size="24px" color="#FF3B30"></wd-icon>
            </view>
            <text class="label">地址管理</text>
          </view>
          <view class="grid-item" @click="navigateTo('/pages/coupon/index')">
            <view class="icon coupon-icon">
              <wd-icon name="coupon" size="24px" color="#AF52DE"></wd-icon>
            </view>
            <text class="label">优惠券</text>
          </view>
        </view>
      </view>
      
      <view class="menu-list-card">
        <view class="menu-item" @click="navigateTo('/pages/reminder/index')">
          <view class="item-left">
            <wd-icon name="clock" size="20px" color="#0071e3"></wd-icon>
            <text class="item-title">智能提醒</text>
          </view>
          <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/user/member')">
          <view class="item-left">
            <wd-icon name="crown" size="20px" color="#FFD700"></wd-icon>
            <text class="item-title">会员中心</text>
          </view>
          <view class="item-right">
            <text class="item-tag" v-if="!userStore.isVip">开通享特权</text>
            <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
          </view>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/help/index')">
          <view class="item-left">
            <wd-icon name="help-circle" size="20px" color="#86868B"></wd-icon>
            <text class="item-title">帮助与反馈</text>
          </view>
          <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
        </view>
        <view class="menu-item" @click="navigateTo('/pages/user/settings')">
          <view class="item-left">
            <wd-icon name="setting" size="20px" color="#86868B"></wd-icon>
            <text class="item-title">设置</text>
          </view>
          <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
        </view>
      </view>
    </view>
    
    <!-- 退出登录按钮 -->
    <view class="logout-section" v-if="userStore.isLoggedIn">
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

function navigateTo(url: string) {
  uni.navigateTo({ url })
}

function handleLogout() {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.reLaunch({ url: '/pages/login/index' })
      }
    }
  })
}

onShow(() => {
  if (typeof uni.getTabBar === 'function' && uni.getTabBar()) {
    uni.getTabBar().setData({
      selected: 3
    })
  }
  if (userStore.isLoggedIn) {
    userStore.fetchUserInfo()
  }
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
  padding-bottom: 120px;
}

.profile-header {
  background-color: #FFFFFF;
  padding-bottom: 40px;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 40px;
    background: #F5F5F7;
    border-radius: 24px 24px 0 0;
  }
  
  .header-content {
    padding: 60px 24px 0;
  }
  
  .user-row {
    display: flex;
    align-items: center;
    margin-bottom: 32px;
    
    .avatar-box {
      position: relative;
      margin-right: 16px;
      
      .avatar-img {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        border: 3px solid #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      }
      
      .avatar-placeholder {
        width: 72px;
        height: 72px;
        background: linear-gradient(135deg, #0071e3, #34C759);
        border-radius: 50%;
        border: 3px solid #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        
        text {
          font-size: 28px;
          color: #FFFFFF;
          font-weight: 700;
        }
      }
    }
    
    .user-info {
      flex: 1;
      
      .name-wrap {
        display: flex;
        align-items: center;
        margin-bottom: 6px;
        
        .nickname {
          font-size: 24px;
          font-weight: 700;
          color: #1D1D1F;
          margin-right: 8px;
        }
        
        .vip-badge {
          background: linear-gradient(135deg, #1D1D1F, #3a3a3c);
          color: #FFD700;
          font-size: 10px;
          padding: 2px 8px;
          border-radius: 4px;
          font-weight: 800;
          letter-spacing: 1px;
        }
      }
      
      .uid {
        font-size: 12px;
        color: #86868B;
      }
    }
  }
  
  .stats-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 24px 0;
    display: flex;
    align-items: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
    position: relative;
    z-index: 10;
    margin-bottom: -20px;
    
    .stat-item {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      
      .val {
        font-size: 24px;
        font-weight: 700;
        color: #1D1D1F;
        margin-bottom: 4px;
      }
      
      .label {
        font-size: 12px;
        color: #86868B;
      }
    }
    
    .v-line {
      width: 1px;
      height: 28px;
      background: #F5F5F7;
    }
  }
}

.order-section {
  margin: 0 20px 16px;
  background: #FFFFFF;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    .title {
      font-size: 16px;
      font-weight: 700;
      color: #1D1D1F;
    }
    
    .more {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 13px;
      color: #86868B;
    }
  }
  
  .order-tabs {
    display: flex;
    justify-content: space-between;
    
    .order-tab {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      
      .tab-icon {
        width: 48px;
        height: 48px;
        background: #F5F5F7;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      .tab-name {
        font-size: 12px;
        color: #1D1D1F;
        font-weight: 500;
      }
    }
  }
}

.menu-section {
  padding: 0 20px;
  
  .menu-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    
    .menu-title {
      font-size: 16px;
      font-weight: 700;
      color: #1D1D1F;
      margin-bottom: 20px;
    }
    
    .grid-menu {
      display: flex;
      justify-content: space-between;
      
      .grid-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        
        .icon {
          width: 48px;
          height: 48px;
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          
          &.file-icon { background: #E3F9E5; }
          &.star-icon { background: #FFF3E0; }
          &.loc-icon { background: #FFEBEE; }
          &.coupon-icon { background: #F3E5F5; }
        }
        
        .label {
          font-size: 12px;
          color: #1D1D1F;
          font-weight: 500;
        }
      }
    }
  }
  
  .menu-list-card {
    background: #FFFFFF;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    
    .menu-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px;
      border-bottom: 1px solid #F5F5F7;
      
      &:last-child {
        border-bottom: none;
      }
      
      .item-left {
        display: flex;
        align-items: center;
        gap: 12px;
        
        .item-title {
          font-size: 15px;
          color: #1D1D1F;
        }
      }
      
      .item-right {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .item-tag {
          font-size: 11px;
          color: #FF9500;
          background: #FFF3E0;
          padding: 2px 8px;
          border-radius: 10px;
        }
      }
    }
  }
}

.logout-section {
  padding: 24px 20px;
  
  .logout-btn {
    width: 100%;
    height: 48px;
    background: #FFFFFF;
    border: 1px solid #FF3B30;
    border-radius: 24px;
    color: #FF3B30;
    font-size: 16px;
    font-weight: 500;
    
    &::after {
      border: none;
    }
  }
}
</style>
