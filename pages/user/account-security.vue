<template>
  <view class="page">
    <view class="group-title">账号绑定</view>
    <wd-cell-group border>
      <wd-cell title="手机号" :value="maskedPhone" is-link @click="handlePhoneClick" />
      <wd-cell title="微信" value="已绑定" />
    </wd-cell-group>
    
    <view class="group-title">安全设置</view>
    <wd-cell-group border>
      <wd-cell title="注销账号" is-link @click="handleDeleteAccount" />
    </wd-cell-group>
    
    <!-- 绑定手机号弹窗 -->
    <wd-popup v-model="showBindPopup" position="bottom" :safe-area-inset-bottom="true" custom-style="border-radius: 16px 16px 0 0;">
      <view class="bind-popup">
        <view class="popup-header">
          <text class="popup-title">{{ userStore.userInfo?.phone ? '换绑手机号' : '绑定手机号' }}</text>
          <view class="close-btn" @click="showBindPopup = false">
            <wd-icon name="close" size="20px" color="#86868B" />
          </view>
        </view>
        
        <view class="form-item">
          <wd-input 
            v-model="phoneForm.phone" 
            placeholder="请输入手机号" 
            type="number"
            maxlength="11"
            no-border
            custom-style="background: #F5F5F7; border-radius: 12px; padding: 0 16px;"
          />
        </view>
        
        <view class="form-item code-item">
          <wd-input 
            v-model="phoneForm.code" 
            placeholder="请输入验证码" 
            type="number"
            maxlength="6"
            no-border
            custom-style="background: #F5F5F7; border-radius: 12px; padding: 0 16px; flex: 1;"
          />
          <button 
            class="code-btn" 
            :disabled="countdown > 0" 
            @click="sendCode"
          >
            {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
          </button>
        </view>
        
        <wd-button block size="large" :loading="binding" @click="confirmBind">确认绑定</wd-button>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { sendVerificationCode, bindPhone, deleteAccount } from '@/api/user'

const userStore = useUserStore()

const showBindPopup = ref(false)
const binding = ref(false)
const countdown = ref(0)
let timer: ReturnType<typeof setInterval> | null = null

const phoneForm = reactive({
  phone: '',
  code: ''
})

const maskedPhone = computed(() => {
  const phone = userStore.userInfo?.phone
  if (phone) {
    return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
  }
  return '未绑定'
})

function handlePhoneClick() {
  phoneForm.phone = ''
  phoneForm.code = ''
  showBindPopup.value = true
}

async function sendCode() {
  if (!phoneForm.phone || phoneForm.phone.length !== 11) {
    uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
    return
  }
  
  if (!/^1[3-9]\d{9}$/.test(phoneForm.phone)) {
    uni.showToast({ title: '手机号格式不正确', icon: 'none' })
    return
  }
  
  try {
    const res = await sendVerificationCode(phoneForm.phone)
    if (res.code === 200) {
      uni.showToast({ title: res.message || '验证码已发送', icon: 'none' })
      // 开始倒计时
      countdown.value = 60
      timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
          clearInterval(timer!)
          timer = null
        }
      }, 1000)
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '发送失败', icon: 'none' })
  }
}

async function confirmBind() {
  if (!phoneForm.phone || phoneForm.phone.length !== 11) {
    uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
    return
  }
  
  if (!phoneForm.code || phoneForm.code.length < 4) {
    uni.showToast({ title: '请输入验证码', icon: 'none' })
    return
  }
  
  binding.value = true
  try {
    const res = await bindPhone({
      phone: phoneForm.phone,
      code: phoneForm.code
    })
    
    if (res.code === 200) {
      uni.showToast({ title: '绑定成功', icon: 'success' })
      showBindPopup.value = false
      // 刷新用户信息
      await userStore.fetchUserInfo()
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '绑定失败', icon: 'none' })
  } finally {
    binding.value = false
  }
}

function handleDeleteAccount() {
  uni.showModal({
    title: '危险操作',
    content: '注销账号后，您的所有数据（包括健康档案、积分、会员权益等）将被永久删除且无法恢复。确定要继续吗？',
    confirmColor: '#FF3B30',
    success: (res) => {
      if (res.confirm) {
        // 二次确认
        uni.showModal({
          title: '最终确认',
          content: '此操作不可逆，请再次确认是否注销当前账号？',
          confirmColor: '#FF3B30',
          success: async (res2) => {
            if (res2.confirm) {
              uni.showLoading({ title: '注销中...' })
              try {
                const res = await deleteAccount()
                if (res.code === 200) {
                  uni.hideLoading()
                  userStore.logout()
                  uni.reLaunch({ url: '/pages/login/index' })
                  uni.showToast({ title: '账号已注销', icon: 'none' })
                }
              } catch (e) {
                uni.hideLoading()
                uni.showToast({ title: '注销失败', icon: 'none' })
              }
            }
          }
        })
      }
    }
  })
}

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-top: 12px;
}

.group-title {
  padding: 16px 16px 8px;
  font-size: 13px;
  color: #86868B;
}

.bind-popup {
  padding: 20px;
  
  .popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    .popup-title {
      font-size: 18px;
      font-weight: 600;
      color: #1D1D1F;
    }
    
    .close-btn {
      padding: 4px;
    }
  }
  
  .form-item {
    margin-bottom: 16px;
  }
  
  .code-item {
    display: flex;
    gap: 12px;
    
    .code-btn {
      width: 120px;
      height: 48px;
      background: #0071e3;
      color: #FFFFFF;
      font-size: 14px;
      border-radius: 12px;
      border: none;
      
      &[disabled] {
        background: #E5E5EA;
        color: #86868B;
      }
    }
  }
}
</style>
