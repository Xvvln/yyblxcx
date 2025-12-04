<template>
  <view class="page">
    <view class="logo-section">
      <image src="/static/logo.png" class="logo" mode="aspectFit" />
      <view class="app-name">健康管理</view>
      <view class="version">Version 1.0.0</view>
    </view>
    
    <wd-cell-group border>
      <wd-cell title="功能介绍" is-link @click="navigateTo('/pages/help/index')" />
      <wd-cell title="用户协议" is-link @click="navigateTo('/pages/help/index?type=agreement')" />
      <wd-cell title="隐私政策" is-link @click="navigateTo('/pages/help/index?type=privacy')" />
      <wd-cell title="检查更新" is-link @click="checkUpdate" />
    </wd-cell-group>
    
    <view class="copyright">
      <text>Copyright © 2024 Health Management</text>
      <text>All Rights Reserved</text>
    </view>
  </view>
</template>

<script setup lang="ts">
function navigateTo(url: string) {
  uni.navigateTo({ url })
}

function checkUpdate() {
  uni.showLoading({ title: '检查中...' })
  setTimeout(() => {
    uni.hideLoading()
    uni.showToast({ title: '当前已是最新版本', icon: 'none' })
  }, 1000)
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-top: 12px;
  display: flex;
  flex-direction: column;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 0;
  
  .logo {
    width: 80px;
    height: 80px;
    border-radius: 16px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }
  
  .app-name {
    font-size: 20px;
    font-weight: 600;
    color: #1D1D1F;
    margin-bottom: 4px;
  }
  
  .version {
    font-size: 14px;
    color: #86868B;
  }
}

.copyright {
  margin-top: auto;
  padding: 32px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  text {
    font-size: 12px;
    color: #C7C7CC;
    line-height: 1.6;
  }
}
</style>

