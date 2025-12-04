<template>
  <view class="login-container">
    <!-- 顶部操作栏 -->
    <view class="nav-bar">
      <text class="password-login" @click="handlePasswordLogin">密码登录</text>
    </view>

    <!-- 主要内容区 -->
    <view class="content">
      <!-- 标题 -->
      <view class="header">
        <text class="title">手机号登录或注册</text>
        <text class="subtitle">一站式记录你的营养与健康数据</text>
      </view>

      <!-- 输入区域 -->
      <view class="form-area">
        <view class="input-group">
          <view class="area-code">
            <text>+86</text>
            <wd-icon name="arrow-down-s" size="14px" color="#666"></wd-icon>
          </view>
          <input 
            class="phone-input"
            v-model="phone" 
            type="number" 
            maxlength="11"
            placeholder="输入手机号码" 
            placeholder-style="color: #999;"
          />
        </view>

        <!-- 登录按钮 -->
        <button 
          class="submit-btn" 
          :class="{ 'active': canSubmit }"
          hover-class="btn-hover"
          @click="handlePhoneLogin"
        >
          获取验证码
        </button>

        <!-- 辅助链接 -->
        <view class="links">
          <text class="link-text" @click="handleGuestMode">随便逛逛</text>
          <view class="divider"></view>
          <text class="link-text" @click="handleRetrieveAccount">找回账号</text>
        </view>
      </view>
    </view>

    <!-- 底部区域 -->
    <view class="footer">
      <!-- 第三方登录 -->
      <view class="social-login">
        <button 
          class="social-btn wechat-btn"
          open-type="login"
          @click="handleWxLogin"
        >
          <wd-icon name="chat-fill" size="32px" color="#fff"></wd-icon>
        </button>
      </view>

      <!-- 隐私协议 -->
      <view class="agreement-box" @click="toggleAgree">
        <view class="checkbox" :class="{ 'checked': agreed }">
          <wd-icon v-if="agreed" name="check" size="10px" color="#20bf55"></wd-icon>
        </view>
        <view class="agreement-text">
          <text>我已阅读并同意 </text>
          <text class="highlight">用户协议</text>
          <text> 和 </text>
          <text class="highlight">隐私政策</text>
        </view>
      </view>
    </view>

    <!-- 隐私政策弹窗 -->
    <wd-popup 
      v-model="showPrivacy" 
      position="center" 
      :close-on-click-modal="false"
      custom-style="border-radius: 16px; width: 85%; max-width: 320px; overflow: hidden;"
    >
      <view class="privacy-modal">
        <view class="modal-title">隐私保护政策</view>
        <view class="modal-content">
          <view class="welcome-text">欢迎来到营养健康助手！</view>
          <view class="policy-text">
            我们将通过《用户协议》和《隐私政策》帮助您了解我们为您提供的健康管理服务，以及收集、处理您个人身体数据（如身高、体重、饮食记录等）的方式。
          </view>
          <view class="policy-text">
            点击「同意并继续」按钮代表您已同意前述协议及政策。
          </view>
          <view class="policy-links">
            查看完整版 <text class="link">《用户协议》</text> 和 <text class="link">《隐私政策》</text>
          </view>
        </view>
        <view class="modal-actions">
          <button class="agree-btn" @click="handleAgreePrivacy">同意并继续</button>
          <view class="disagree-btn" @click="handleDisagreePrivacy">不同意</view>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 状态
const phone = ref('')
const agreed = ref(false)
const showPrivacy = ref(false) // 控制弹窗显示

// 页面加载时显示隐私弹窗
onLoad(() => {
  // 如果用户之前没有同意过，则弹出（这里为了演示效果，每次进入都弹，实际可加本地缓存判断）
  // const hasAgreed = uni.getStorageSync('has_agreed_privacy')
  // if (!hasAgreed) {
    showPrivacy.value = true
  // }
})

// 处理点击同意隐私政策
function handleAgreePrivacy() {
  showPrivacy.value = false
  agreed.value = true // 自动勾选
  uni.setStorageSync('has_agreed_privacy', true)
}

// 处理点击不同意
function handleDisagreePrivacy() {
  uni.showModal({
    title: '温馨提示',
    content: '您需要同意隐私政策才能使用我们的健康管理服务，以确保您的数据安全。',
    showCancel: false,
    confirmText: '我知道了',
    confirmColor: '#20bf55'
  })
}

// 计算属性
const canSubmit = computed(() => {
  return phone.value.length === 11 && agreed.value
})

// 方法
function toggleAgree() {
  agreed.value = !agreed.value
}

// 手机号登录（模拟/扩展）
async function handlePhoneLogin() {
  if (!agreed.value) {
    uni.showToast({ title: '请先同意用户协议', icon: 'none' })
    return
  }
  if (phone.value.length !== 11) {
    uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
    return
  }
  
  uni.showLoading({ title: '发送中...' })
  
  // TODO: 这里可以对接后端的短信发送接口
  // 目前后端主要支持微信一键登录，这里我们模拟一下
  setTimeout(() => {
    uni.hideLoading()
    uni.showToast({ title: '验证码功能暂未开放，请使用微信登录', icon: 'none' })
  }, 1000)
}

// 微信一键登录（核心功能）
async function handleWxLogin() {
  if (!agreed.value) {
    uni.showToast({ title: '请先同意用户协议', icon: 'none' })
    return
  }

  try {
    uni.showLoading({ title: '登录中...' })
    
    // 1. 获取微信 Code
    const loginRes = await uni.login({ provider: 'weixin' })
    if (loginRes.code) {
      // 2. 调用 Store 的登录方法 (请求后端 /auth/login)
      const data = await userStore.login(loginRes.code)
      
      uni.hideLoading()
      uni.showToast({ title: '登录成功', icon: 'success' })
      
      // 3. 跳转逻辑：新用户或未完善信息 -> 欢迎页；老用户 -> 首页
      setTimeout(() => {
        // 后端返回的 is_new_user 是最准确的判断
        // 也可以检查 userStore.userInfo.height/weight
        if (data.is_new_user || !userStore.userInfo?.height) {
           uni.redirectTo({ url: '/pages/onboarding/welcome' })
        } else {
           uni.switchTab({ url: '/pages/index/index' })
        }
      }, 1500)
    }
  } catch (error: any) {
    uni.hideLoading()
    uni.showToast({ title: error.message || '登录失败', icon: 'none' })
  }
}

function handleGuestMode() {
  uni.switchTab({ url: '/pages/index/index' })
}

function handlePasswordLogin() {
  uni.showToast({ title: '暂只支持验证码或微信登录', icon: 'none' })
}

function handleRetrieveAccount() {
  uni.showToast({ title: '请联系管理员', icon: 'none' })
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  // 白绿渐变：从顶部的纯净白过渡到底部的清新绿
  background: linear-gradient(180deg, #FFFFFF 0%, #F1F8E9 40%, #C8E6C9 100%);
  
  padding: 0 32px;
  position: relative;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  overflow: hidden;

  // 背景装饰图案 - 改为浅绿色纹理
  &::before {
    content: '';
    position: absolute;
    top: -15%;
    right: -10%;
    width: 500px;
    height: 500px;
    // 浅绿色光晕
    background: radial-gradient(circle, rgba(76, 175, 80, 0.08) 0%, rgba(76, 175, 80, 0) 60%);
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: 10%;
    left: -10%;
    width: 400px;
    height: 400px;
    // 深一点的绿色线条
    border: 40px solid rgba(76, 175, 80, 0.05);
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
    transform: rotate(-45deg);
  }
}

/* 额外的背景装饰层 */
.nav-bar {
  height: 44px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-top: var(--status-bar-height);
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
  
  .password-login {
    // 深色文字
    color: #666;
    font-size: 14px;
    font-weight: 500;
  }
}

/* 主要内容 */
.content {
  flex: 1;
  position: relative;
  z-index: 1;
  
  .header {
    margin-bottom: 60px;
    
    .title {
      display: block;
      font-size: 32px; 
      font-weight: bold;
      // 深黑色标题
      color: #1D1D1F;
      margin-bottom: 12px;
      letter-spacing: 1px;
      text-shadow: none;
    }
    
    .subtitle {
      font-size: 15px;
      // 深灰色副标题
      color: #86868B;
      letter-spacing: 0.5px;
    }
  }
}

/* 表单区域 */
.form-area {
  .input-group {
    height: 56px;
    // 浅灰色输入框背景
    background: #F5F5F7;
    border-radius: 28px;
    display: flex;
    align-items: center;
    padding: 0 24px;
    margin-bottom: 24px;
    // 移除磨砂效果，改用实色
    border: 1px solid transparent;
    transition: all 0.3s;

    &:focus-within {
      background: #FFFFFF;
      // 绿色边框
      border-color: #4CAF50;
      box-shadow: 0 4px 12px rgba(76, 175, 80, 0.1);
    }
    
    .area-code {
      display: flex;
      align-items: center;
      margin-right: 16px;
      padding-right: 16px;
      border-right: 1px solid #E5E5EA;
      height: 20px;
      
      text {
        // 深色文字
        color: #1D1D1F;
        font-size: 16px;
        margin-right: 4px;
        font-weight: 500;
      }
    }
    
    .phone-input {
      flex: 1;
      height: 100%;
      // 深色输入文字
      color: #1D1D1F;
      font-size: 18px;
      font-weight: 500;
    }
  }
  
  .submit-btn {
    height: 56px;
    border-radius: 28px;
    // 绿色主按钮
    background: #4CAF50; 
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    transition: all 0.3s;
    border: none;
    opacity: 0.9;
    box-shadow: 0 8px 20px rgba(76, 175, 80, 0.25);
    
    &.active {
      opacity: 1;
      transform: translateY(-1px);
      box-shadow: 0 10px 25px rgba(76, 175, 80, 0.35);
    }
    
    &::after {
      border: none;
    }
  }
  
  .links {
    display: flex;
    justify-content: center;
    align-items: center;
    
    .link-text {
      // 灰色链接
      color: #86868B;
      font-size: 14px;
      font-weight: 500;
    }
    
    .divider {
      width: 1px;
      height: 12px;
      background: #C7C7CC;
      margin: 0 20px;
    }
  }
}

/* 底部区域 */
.footer {
  padding-bottom: 40px;
  padding-bottom: calc(40px + env(safe-area-inset-bottom));
  position: relative;
  z-index: 1;
  
  .social-login {
    display: flex;
    justify-content: center;
    margin-bottom: 30px;
    
    .social-btn {
      width: 64px; 
      height: 64px;
      border-radius: 50%;
      // 微信绿
      background: #07c160; 
      display: flex;
      align-items: center;
      justify-content: center;
      // 白色边框
      border: 4px solid rgba(255, 255, 255, 0.8); 
      padding: 0;
      margin: 0;
      transition: all 0.2s;
      box-shadow: 0 6px 20px rgba(7, 193, 96, 0.25);
      
      &::after {
        border: none;
      }
      
      &:active {
        transform: scale(0.95);
        background: #06ad56;
      }
    }
  }
  
  .agreement-box {
    display: flex;
    justify-content: center;
    align-items: center;
    
    .checkbox {
      width: 16px;
      height: 16px;
      border-radius: 50%;
      // 灰色边框
      border: 1px solid #C7C7CC;
      margin-right: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: transparent;
      transition: all 0.2s;
      
      &.checked {
        background: #4CAF50;
        border-color: #4CAF50;
      }
    }
    
    .agreement-text {
      font-size: 12px;
      color: #86868B;
      
      .highlight {
        color: #4CAF50;
        text-decoration: none;
        font-weight: bold;
        margin: 0 2px;
        border-bottom: none;
      }
    }
  }
}
/* 隐私弹窗样式 */
.privacy-modal {
  background: #fff;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .modal-title {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-bottom: 20px;
  }
  
  .modal-content {
    margin-bottom: 24px;
    
    .welcome-text {
      font-size: 15px;
      font-weight: 500;
      color: #333;
      margin-bottom: 12px;
    }
    
    .policy-text {
      font-size: 14px;
      color: #666;
      line-height: 1.6;
      margin-bottom: 12px;
      text-align: justify;
    }
    
    .policy-links {
      font-size: 13px;
      color: #999;
      margin-top: 8px;
      
      .link {
        color: #20bf55;
        display: inline;
      }
    }
  }
  
  .modal-actions {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    
    .agree-btn {
      width: 100%;
      height: 44px;
      background: #20bf55;
      border-radius: 22px;
      color: #fff;
      font-size: 16px;
      font-weight: bold;
      display: flex;
      align-items: center;
      justify-content: center;
      border: none;
      margin: 0;
      
      &:active {
        opacity: 0.9;
      }
      
      &::after { border: none; }
    }
    
    .disagree-btn {
      font-size: 14px;
      color: #999;
      padding: 8px 20px;
    }
  }
}
</style>
