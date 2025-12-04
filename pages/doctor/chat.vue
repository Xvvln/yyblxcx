<template>
  <view class="page">
    <!-- 顶部导航栏（仅在H5/APP显示，小程序自带） -->
    <!-- <wd-navbar :title="doctor?.name ? `${doctor.name}医生` : '在线咨询'" left-arrow @click-left="handleBack"></wd-navbar> -->

    <!-- 聊天消息列表 -->
    <scroll-view 
      scroll-y 
      class="chat-list" 
      :scroll-top="scrollTop"
      :scroll-into-view="scrollIntoView"
    >
      <!-- 医生信息卡片 -->
      <view class="doctor-card" v-if="doctor">
        <view class="avatar-wrap">
          <image :src="doctor.avatar || '/static/placeholder/avatar.png'" class="doctor-avatar" mode="aspectFill" />
        </view>
        <text class="title">{{ doctor.name }} {{ doctor.title }}</text>
        <text class="desc">{{ doctor.hospital }}</text>
        <text class="tip">医生会在24小时内回复，请耐心等待</text>
      </view>

      <!-- 消息列表 -->
      <view 
        class="message-item" 
        v-for="(msg, index) in messages" 
        :key="msg.id || index"
        :class="{ 'user-msg': msg.sender_id === userStore.userInfo?.id }"
        :id="'msg-' + index"
      >
        <view class="avatar">
          <image 
            v-if="msg.sender_id === userStore.userInfo?.id" 
            :src="userStore.userInfo?.avatar || '/static/placeholder/avatar.png'" 
            class="user-avatar" 
          />
          <image 
            v-else 
            :src="doctor?.avatar || '/static/placeholder/avatar.png'" 
            class="doctor-avatar-small" 
          />
        </view>
        <view class="content">
          <text class="text">{{ msg.content }}</text>
          <text class="time">{{ formatTime(msg.created_at) }}</text>
        </view>
      </view>

      <!-- 加载中 -->
      <view class="message-item" v-if="loading">
        <!-- 仅在发送时显示sending状态，或者历史记录加载 -->
      </view>

      <view class="scroll-anchor" :id="scrollAnchor"></view>
    </scroll-view>

    <!-- 底部输入 -->
    <view class="footer">
      <view class="input-wrap">
        <textarea 
          v-model="inputText" 
          placeholder="请输入您的健康咨询问题..."
          :auto-height="true"
          :maxlength="500"
          :show-confirm-bar="false"
          @confirm="handleSend"
        />
      </view>
      <view class="send-btn" :class="{ active: inputText.trim() && !sending }" @click="handleSend">
        <wd-icon name="send" size="22px" :color="inputText.trim() && !sending ? '#FFFFFF' : '#C7C7CC'"></wd-icon>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'
import { getDoctorDetail } from '@/api/doctor'
import { getChatHistory, sendMessage } from '@/api/message'
import dayjs from 'dayjs'

const userStore = useUserStore()
const doctorId = ref(0)
const doctor = ref<any>(null)
const messages = ref<any[]>([])
const inputText = ref('')
const sending = ref(false)
const scrollTop = ref(0)
const scrollIntoView = ref('')
const scrollAnchor = ref('scroll-anchor')

onLoad((options) => {
  doctorId.value = Number(options?.id || 0)
  if (doctorId.value) {
    initData()
  }
})

async function initData() {
  uni.setNavigationBarTitle({ title: '在线咨询' })
  await fetchDoctorInfo()
  await fetchHistory()
}

async function fetchDoctorInfo() {
  try {
    const res = await getDoctorDetail(doctorId.value)
    if (res.code === 200) {
      doctor.value = res.data
      uni.setNavigationBarTitle({ title: `${doctor.value.name}医生` })
    }
  } catch (e) {
    console.error('获取医生详情失败', e)
  }
}

async function fetchHistory() {
  try {
    const res = await getChatHistory(doctorId.value)
    if (res.code === 200) {
      // API返回的是 { list: [], total: ... }
      messages.value = res.data?.list || []
      scrollToBottom()
    }
  } catch (e) {
    console.error('获取聊天记录失败', e)
    // 模拟空数据
    messages.value = []
  }
}

async function handleSend() {
  if (!inputText.value.trim() || sending.value) return
  
  const content = inputText.value.trim()
  sending.value = true
  
  // 乐观UI更新
  const tempMsg = {
    id: Date.now(), // 临时ID
    sender_id: userStore.userInfo?.id,
    content: content,
    created_at: new Date(),
    status: 'sending'
  }
  messages.value.push(tempMsg)
  inputText.value = ''
  scrollToBottom()
  
  try {
    const res = await sendMessage({
      receiver_id: doctorId.value,
      content: content,
      type: 'text' // 假设支持消息类型
    })
    
    if (res.code === 200) {
      // 发送成功，可以更新消息状态或替换为服务器返回的消息
      // 这里简单处理，假设不需要替换，只是确认发送成功
    } else {
      uni.showToast({ title: '发送失败', icon: 'none' })
      // 可以标记消息为失败状态
    }
  } catch (e) {
    uni.showToast({ title: '发送失败', icon: 'none' })
  } finally {
    sending.value = false
    scrollToBottom()
  }
}

function scrollToBottom() {
  nextTick(() => {
    scrollIntoView.value = ''
    setTimeout(() => {
      scrollIntoView.value = scrollAnchor.value
    }, 50)
  })
}

function formatTime(time: string | Date) {
  return dayjs(time).format('HH:mm')
}

function handleBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #F5F5F7;
}

.chat-list {
  flex: 1;
  padding: 16px;
  padding-bottom: 100px;
  box-sizing: border-box;
}

.doctor-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 24px 16px;
  text-align: center;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  
  .avatar-wrap {
    margin-bottom: 12px;
    .doctor-avatar {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: #F5F5F7;
    }
  }
  
  .title {
    font-size: 16px;
    font-weight: 600;
    color: #1D1D1F;
    display: block;
    margin-bottom: 4px;
  }
  
  .desc {
    font-size: 13px;
    color: #86868B;
    display: block;
    margin-bottom: 12px;
  }
  
  .tip {
    font-size: 12px;
    color: #AEAEB2;
    background: #F5F5F7;
    padding: 4px 12px;
    border-radius: 12px;
  }
}

.message-item {
  display: flex;
  margin-bottom: 16px;
  
  .avatar {
    margin-right: 12px;
    flex-shrink: 0;
    
    .doctor-avatar-small {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #F5F5F7;
    }
    
    .user-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
    }
  }
  
  .content {
    max-width: 70%;
    
    .text {
      background: #FFFFFF;
      padding: 10px 16px;
      border-radius: 0 16px 16px 16px;
      font-size: 15px;
      color: #1D1D1F;
      line-height: 1.5;
      display: block;
      word-break: break-all;
    }
    
    .time {
      font-size: 11px;
      color: #AEAEB2;
      margin-top: 4px;
      display: block;
    }
  }
  
  &.user-msg {
    flex-direction: row-reverse;
    
    .avatar {
      margin-right: 0;
      margin-left: 12px;
    }
    
    .content {
      .text {
        background: #0071e3;
        color: #FFFFFF;
        border-radius: 16px 0 16px 16px;
      }
      
      .time {
        text-align: right;
      }
    }
  }
}

.scroll-anchor {
  height: 1px;
}

.footer {
  background: #FFFFFF;
  padding: 12px 16px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
  display: flex;
  align-items: flex-end;
  gap: 12px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .input-wrap {
    flex: 1;
    background: #F5F5F7;
    border-radius: 20px;
    padding: 10px 16px;
    
    textarea {
      width: 100%;
      font-size: 15px;
      line-height: 1.4;
      max-height: 100px;
    }
  }
  
  .send-btn {
    width: 44px;
    height: 44px;
    background: #E5E5EA;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    
    &.active {
      background: #0071e3;
    }
  }
}
</style>

