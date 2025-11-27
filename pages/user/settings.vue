<template>
  <view class="page">
    <view class="settings-list">
      <view class="group-title">账号与安全</view>
      <wd-cell-group border>
        <wd-cell title="账号管理" is-link value="手机号/微信" @click="navigateTo('account')" />
        <wd-cell title="隐私设置" is-link @click="navigateTo('privacy')" />
      </wd-cell-group>
      
      <view class="group-title">通用</view>
      <wd-cell-group border>
        <wd-cell title="长辈模式" center>
          <wd-switch v-model="isElderlyMode" @change="toggleElderlyMode" size="24px" active-color="#0071e3" />
        </wd-cell>
        <wd-cell title="消息通知" is-link @click="navigateTo('notification')" />
        <wd-cell title="清除缓存" :value="cacheSize" is-link @click="clearCache" />
      </wd-cell-group>
      
      <view class="group-title">关于</view>
      <wd-cell-group border>
        <wd-cell title="用户协议" is-link @click="navigateTo('agreement')" />
        <wd-cell title="隐私政策" is-link @click="navigateTo('privacy-policy')" />
        <wd-cell title="关于我们" is-link @click="navigateTo('about')" />
        <wd-cell title="版本号" value="1.0.0" />
      </wd-cell-group>
      
      <view class="group-title">其他</view>
      <wd-cell-group border>
        <wd-cell title="意见反馈" is-link @click="navigateTo('feedback')" />
        <wd-cell title="帮助中心" is-link @click="navigateTo('help')" />
      </wd-cell-group>
    </view>
    
    <view class="footer">
      <button class="logout-btn" @click="logout">退出登录</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'

const appStore = useAppStore()
const userStore = useUserStore()

const isElderlyMode = ref(appStore.elderlyMode)
const cacheSize = ref('0KB')

onMounted(() => {
  calculateCacheSize()
})

function calculateCacheSize() {
  // 模拟缓存大小计算
  uni.getStorageInfo({
    success: (res) => {
      const size = res.currentSize
      if (size > 1024) {
        cacheSize.value = (size / 1024).toFixed(1) + 'MB'
      } else {
        cacheSize.value = size + 'KB'
      }
    }
  })
}

function toggleElderlyMode({ value }: { value: boolean }) {
  appStore.setElderlyMode(value)
  uni.showToast({
    title: value ? '已开启长辈模式' : '已关闭长辈模式',
    icon: 'none'
  })
}

function navigateTo(page: string) {
  switch (page) {
    case 'account':
      uni.showToast({ title: '账号管理', icon: 'none' })
      break
    case 'privacy':
      uni.showModal({
        title: '隐私设置',
        content: '您可以管理个人隐私数据的展示权限',
        showCancel: false
      })
      break
    case 'notification':
      uni.openSetting({
        success: () => {},
        fail: () => {
          uni.showToast({ title: '请在系统设置中管理通知', icon: 'none' })
        }
      })
      break
    case 'agreement':
      uni.navigateTo({ url: '/pages/help/index?type=agreement' })
      break
    case 'privacy-policy':
      uni.navigateTo({ url: '/pages/help/index?type=privacy' })
      break
    case 'about':
      uni.showModal({
        title: '关于我们',
        content: '营养不良筛查与健康管理小程序\n版本：1.0.0\n\n致力于为用户提供专业的健康管理服务',
        showCancel: false
      })
      break
    case 'feedback':
      uni.showModal({
        title: '意见反馈',
        editable: true,
        placeholderText: '请输入您的建议或问题',
        success: (res) => {
          if (res.confirm && res.content) {
            uni.showToast({ title: '感谢您的反馈', icon: 'success' })
          }
        }
      })
      break
    case 'help':
      uni.navigateTo({ url: '/pages/help/index' })
      break
    default:
      uni.showToast({ title: '功能开发中', icon: 'none' })
  }
}

function clearCache() {
  uni.showModal({
    title: '清除缓存',
    content: '确定要清除所有缓存吗？',
    success: (res) => {
      if (res.confirm) {
        uni.clearStorage({
          success: () => {
            // 保留 token
            const token = userStore.token
            if (token) {
              uni.setStorageSync('token', token)
            }
            cacheSize.value = '0KB'
            uni.showToast({ title: '清除成功', icon: 'success' })
          }
        })
      }
    }
  })
}

function logout() {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    confirmColor: '#FF3B30',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.reLaunch({ url: '/pages/login/index' })
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-top: 12px;
  padding-bottom: 100px;
}

.settings-list {
  padding: 0 16px;
}

.group-title {
  padding: 16px 4px 8px;
  font-size: 13px;
  color: #86868B;
}

.footer {
  padding: 32px 16px;
  
  .logout-btn {
    width: 100%;
    height: 48px;
    background: #FFFFFF;
    border-radius: 24px;
    border: none;
    color: #FF3B30;
    font-size: 16px;
    font-weight: 500;
    
    &::after {
      border: none;
    }
  }
}
</style>
