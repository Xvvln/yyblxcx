<template>
  <view class="page">
    <view class="header">
      <text class="title">欢迎使用</text>
      <text class="subtitle">营养健康管理小程序</text>
    </view>
    
    <view class="form-area">
      <!-- 微信一键登录 -->
      <button 
        class="wx-login-btn"
        open-type="getPhoneNumber"
        @getphonenumber="handleWxLogin"
      >
        <wd-icon name="chat-fill" size="20px" color="#FFFFFF" custom-style="margin-right: 8px;"></wd-icon>
        微信一键登录
      </button>
      
      <view class="divider-line">
        <view class="line"></view>
        <text class="text">或</text>
        <view class="line"></view>
      </view>
      
      <!-- 手机号登录 -->
      <view class="input-group">
        <view class="prefix">+86</view>
        <wd-icon name="arrow-down" size="12px" color="#FFFFFF" custom-style="margin: 0 12px 0 4px;"></wd-icon>
        <input 
          v-model="phone" 
          type="number"
          placeholder="输入手机号码" 
          placeholder-style="color: rgba(255,255,255,0.4);"
          class="custom-input"
        />
      </view>
      
      <button 
        class="phone-login-btn"
        @click="handlePhoneLogin"
        :disabled="!phone"
      >
        获取验证码
      </button>
      
      <!-- 登录提示 -->
      <view class="login-tips">
        <text>登录后可享受完整服务</text>
      </view>
    </view>
    
    <view class="footer">
      <view class="agreement" @click="toggleAgreed">
        <view class="radio" :class="{ checked: agreed }">
          <wd-icon v-if="agreed" name="check" size="10px" color="#0071e3"></wd-icon>
        </view>
        <text class="text">我已阅读并同意 <text class="link">用户协议</text> 和 <text class="link">隐私政策</text></text>
      </view>
    </view>

    <!-- 隐私弹窗 -->
    <wd-popup v-model="showPrivacy" position="center" custom-style="border-radius: 16px; width: 80%;">
      <view class="privacy-modal">
        <text class="p-title">隐私保护政策</text>
        <text class="p-content">欢迎使用营养健康管理小程序！\n\n我们将通过《用户协议》和《隐私政策》帮助您了解我们为您提供的服务...</text>
        <button class="agree-btn" @click="agreePrivacy">同意并继续</button>
        <text class="p-cancel" @click="showPrivacy = false">不同意</text>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const phone = ref('')
const agreed = ref(false)
const showPrivacy = ref(false)
const pendingAction = ref<'wx' | 'phone' | null>(null)

function toggleAgreed() {
  agreed.value = !agreed.value
}

// 微信登录
async function handleWxLogin(e: any) {
  if (!agreed.value) {
    pendingAction.value = 'wx'
    showPrivacy.value = true
    return
  }
  
  doWxLogin()
}

async function doWxLogin() {
  uni.showLoading({ title: '登录中' })
  
  // 先清除旧的 token
  uni.removeStorageSync('token')
  
  try {
    // 获取微信登录code
    const loginRes = await new Promise<UniApp.LoginRes>((resolve, reject) => {
      uni.login({
        provider: 'weixin',
        success: resolve,
        fail: reject
      })
    })
    
    if (loginRes.code) {
      // 调用后端登录接口
      await userStore.login(loginRes.code)
      
      uni.hideLoading()
      
      // 等待一下确保 storage 同步完成
      setTimeout(() => {
        // 检查是否需要完善信息
        if (!userStore.userInfo?.nickname || userStore.userInfo.nickname.startsWith('微信用户')) {
          // 跳转到完善信息页面
          uni.redirectTo({ url: '/pages/health/screening' })
        } else {
          uni.switchTab({ url: '/pages/index/index' })
        }
      }, 100)
    }
  } catch (error: any) {
    uni.hideLoading()
    console.error('Login error:', error)
    
    // 开发环境模拟登录
    mockLogin()
  }
}

// 手机号登录
function handlePhoneLogin() {
  if (!phone.value) {
    uni.showToast({ title: '请输入手机号', icon: 'none' })
    return
  }
  
  if (!agreed.value) {
    pendingAction.value = 'phone'
    showPrivacy.value = true
    return
  }
  
  // 模拟手机号登录
  mockLogin()
}

// 同意隐私政策
function agreePrivacy() {
  showPrivacy.value = false
  agreed.value = true
  
  if (pendingAction.value === 'wx') {
    doWxLogin()
  } else if (pendingAction.value === 'phone') {
    mockLogin()
  }
  pendingAction.value = null
}

// 模拟登录（开发环境）
async function mockLogin() {
  uni.showLoading({ title: '登录中' })
  
  try {
    // 先清除旧的 token
    uni.removeStorageSync('token')
    
    // 调用后端登录接口，使用手机号或时间戳作为code
    const mockCode = phone.value || String(Date.now())
    await userStore.login(mockCode)
    
    uni.hideLoading()
    
    // 等待一下确保 storage 同步完成
    setTimeout(() => {
      // 跳转到健康筛查页面
      uni.redirectTo({ url: '/pages/health/screening' })
    }, 100)
  } catch (error: any) {
    uni.hideLoading()
    console.error('Mock login failed:', error)
    uni.showToast({ title: '登录失败，请重试', icon: 'none' })
  }
}

</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  color: #FFFFFF;
}

.header {
  margin-top: 80px;
  margin-bottom: 60px;
  text-align: center;
  
  .title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 12px;
    display: block;
    letter-spacing: 2px;
  }
  
  .subtitle {
    font-size: 16px;
    opacity: 0.7;
  }
}

.form-area {
  .wx-login-btn {
    width: 100%;
    height: 50px;
    background: #07C160;
    border-radius: 25px;
    border: none;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    
    &::after {
      border: none;
    }
  }
  
  .divider-line {
    display: flex;
    align-items: center;
    margin: 32px 0;
    
    .line {
      flex: 1;
      height: 1px;
      background: rgba(255,255,255,0.2);
    }
    
    .text {
      padding: 0 16px;
      font-size: 12px;
      color: rgba(255,255,255,0.5);
    }
  }
  
  .input-group {
    background: rgba(255,255,255,0.1);
    border-radius: 25px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    
    .prefix {
      font-size: 16px;
      color: #FFFFFF;
    }
    
    .custom-input {
      flex: 1;
      font-size: 16px;
      color: #FFFFFF;
    }
  }
  
  .phone-login-btn {
    width: 100%;
    height: 50px;
    margin-top: 20px;
    background: rgba(255,255,255,0.15);
    border-radius: 25px;
    border: none;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 500;
    
    &::after {
      border: none;
    }
    
    &[disabled] {
      opacity: 0.5;
    }
  }
  
  .login-tips {
    display: flex;
    justify-content: center;
    margin-top: 24px;
    font-size: 13px;
    color: rgba(255,255,255,0.5);
  }
}

.footer {
  margin-top: auto;
  padding-bottom: 40px;
  
  .agreement {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: rgba(255,255,255,0.6);
    
    .radio {
      width: 16px;
      height: 16px;
      border-radius: 50%;
      border: 1.5px solid rgba(255,255,255,0.4);
      margin-right: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &.checked {
        background: #FFFFFF;
        border-color: #FFFFFF;
      }
    }
    
    .link {
      color: #0071e3;
    }
  }
}

.privacy-modal {
  padding: 24px;
  background: #FFFFFF;
  border-radius: 16px;
  text-align: center;
  
  .p-title {
    font-size: 18px;
    font-weight: 600;
    color: #1D1D1F;
    margin-bottom: 16px;
    display: block;
  }
  
  .p-content {
    font-size: 14px;
    color: #86868B;
    text-align: left;
    margin-bottom: 24px;
    display: block;
    line-height: 1.6;
    white-space: pre-line;
  }
  
  .agree-btn {
    width: 100%;
    height: 44px;
    background: #0071e3;
    border-radius: 22px;
    border: none;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 500;
    
    &::after {
      border: none;
    }
  }
  
  .p-cancel {
    font-size: 14px;
    color: #86868B;
    margin-top: 16px;
    display: block;
  }
}
</style>
