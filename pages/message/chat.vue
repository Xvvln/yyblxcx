<template>
  <view class="page">
    <!-- 聊天消息列表 -->
    <scroll-view 
      scroll-y 
      class="chat-list" 
      :scroll-top="scrollTop"
      :scroll-into-view="scrollIntoView"
    >
      <!-- 加载更多 -->
      <view class="load-more" v-if="hasMore" @click="loadMore">
        <text>加载更多消息</text>
      </view>

      <!-- 消息列表 -->
      <view 
        class="message-item" 
        v-for="(msg, index) in messages" 
        :key="msg.id || index"
        :class="{ 'my-msg': msg.is_self }"
        :id="'msg-' + index"
      >
        <image 
          v-if="!msg.is_self" 
          :src="targetUser.avatar || '/static/placeholder/avatar.png'" 
          class="avatar" 
          @click="viewProfile"
        />
        <view class="content">
          <text class="text">{{ msg.content }}</text>
          <text class="time">{{ formatTime(msg.created_at) }}</text>
        </view>
        <image 
          v-if="msg.is_self" 
          :src="userStore.avatar || '/static/placeholder/avatar.png'" 
          class="avatar" 
        />
      </view>

      <view class="scroll-anchor" :id="scrollAnchor"></view>
    </scroll-view>

    <!-- 底部输入 -->
    <view class="footer">
      <view class="input-wrap">
        <textarea 
          v-model="inputText" 
          placeholder="发送消息..."
          :auto-height="true"
          :maxlength="500"
          :show-confirm-bar="false"
          @confirm="sendMsg"
        />
      </view>
      <view class="send-btn" :class="{ active: inputText.trim() && !sending }" @click="sendMsg">
        <wd-icon name="send" size="22px" :color="inputText.trim() && !sending ? '#FFFFFF' : '#C7C7CC'"></wd-icon>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'
import { getChatHistory, sendMessage } from '@/api/message'
import request from '@/utils/request'

interface Message {
  id?: number
  content: string
  is_self: boolean
  created_at: string
}

const userStore = useUserStore()
const targetUserId = ref(0)
const targetUser = ref<any>({})
const messages = ref<Message[]>([])
const inputText = ref('')
const sending = ref(false)
const loading = ref(false)
const scrollTop = ref(0)
const scrollIntoView = ref('')
const scrollAnchor = ref('scroll-anchor')
const page = ref(1)
const hasMore = ref(false)

onLoad((options) => {
  if (options?.id) {
    targetUserId.value = Number(options.id)
    // 设置导航栏标题
    if (options?.name) {
      uni.setNavigationBarTitle({ title: decodeURIComponent(options.name) })
    }
    fetchUserInfo()
    fetchMessages()
  }
})

// 获取对方用户信息
async function fetchUserInfo() {
  try {
    const res = await request.get(`/user/${targetUserId.value}/profile`)
    if (res.code === 200) {
      targetUser.value = res.data
      uni.setNavigationBarTitle({ title: res.data.nickname || '聊天' })
    }
  } catch (e) {
    console.error('获取用户信息失败', e)
  }
}

// 获取聊天记录
async function fetchMessages(loadMore = false) {
  if (loading.value) return
  loading.value = true
  
  try {
    const res = await getChatHistory(targetUserId.value, {
      page: page.value,
      page_size: 20
    })
    
    if (res.code === 200) {
      const list = res.data?.list || []
      if (loadMore) {
        messages.value = [...list.reverse(), ...messages.value]
      } else {
        messages.value = list.reverse()
        scrollToBottom()
      }
      hasMore.value = list.length >= 20
    }
  } catch (e) {
    console.error('获取聊天记录失败', e)
  } finally {
    loading.value = false
  }
}

// 加载更多
function loadMore() {
  if (hasMore.value && !loading.value) {
    page.value++
    fetchMessages(true)
  }
}

// 发送消息
async function sendMsg() {
  if (!inputText.value.trim() || sending.value) return
  
  const content = inputText.value.trim()
  inputText.value = ''
  sending.value = true
  
  // 先添加到本地显示
  const tempMsg: Message = {
    content,
    is_self: true,
    created_at: new Date().toISOString()
  }
  messages.value.push(tempMsg)
  scrollToBottom()
  
  try {
    const res = await sendMessage({
      receiver_id: targetUserId.value,
      content
    })
    
    if (res.code === 200) {
      // 更新消息ID
      tempMsg.id = res.data?.id
    } else {
      uni.showToast({ title: '发送失败', icon: 'none' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '发送失败', icon: 'none' })
  } finally {
    sending.value = false
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

function viewProfile() {
  uni.navigateTo({ url: `/pages/user/homepage?id=${targetUserId.value}` })
}

function formatTime(time: string) {
  if (!time) return ''
  const formattedTime = time.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(formattedTime)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  const h = date.getHours().toString().padStart(2, '0')
  const m = date.getMinutes().toString().padStart(2, '0')
  
  // 今天
  if (date.toDateString() === now.toDateString()) {
    return `${h}:${m}`
  }
  
  // 昨天
  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)
  if (date.toDateString() === yesterday.toDateString()) {
    return `昨天 ${h}:${m}`
  }
  
  // 更早
  return `${date.getMonth() + 1}/${date.getDate()} ${h}:${m}`
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
}

.load-more {
  text-align: center;
  padding: 12px;
  
  text {
    font-size: 13px;
    color: #0071e3;
  }
}

.message-item {
  display: flex;
  margin-bottom: 16px;
  align-items: flex-start;
  
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  
  .content {
    max-width: 70%;
    margin: 0 12px;
    
    .text {
      background: #FFFFFF;
      padding: 12px 16px;
      border-radius: 4px 18px 18px 18px;
      font-size: 15px;
      color: #1D1D1F;
      line-height: 1.5;
      display: block;
      word-break: break-all;
      box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    
    .time {
      font-size: 11px;
      color: #86868B;
      margin-top: 4px;
      display: block;
    }
  }
  
  &.my-msg {
    flex-direction: row-reverse;
    
    .content {
      .text {
        background: #0071e3;
        color: #FFFFFF;
        border-radius: 18px 4px 18px 18px;
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












