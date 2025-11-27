<template>
  <view class="page">
    <!-- 聊天消息列表 -->
    <scroll-view 
      scroll-y 
      class="chat-list" 
      :scroll-top="scrollTop"
      :scroll-into-view="scrollIntoView"
    >
      <!-- 欢迎消息 -->
      <view class="welcome-card" v-if="messages.length === 0">
        <view class="avatar-wrap">
          <view class="ai-avatar">
            <wd-icon name="robot" size="32px" color="#0071e3"></wd-icon>
          </view>
        </view>
        <text class="title">我是您的健康AI助手</text>
        <text class="desc">有任何健康问题都可以问我，我会为您提供专业的建议</text>
        
        <view class="quick-questions">
          <view class="question-item" @click="sendQuickQuestion('如何制定健康的减肥计划？')">
            如何制定健康的减肥计划？
          </view>
          <view class="question-item" @click="sendQuickQuestion('每天应该喝多少水？')">
            每天应该喝多少水？
          </view>
          <view class="question-item" @click="sendQuickQuestion('运动后应该吃什么？')">
            运动后应该吃什么？
          </view>
          <view class="question-item" @click="sendQuickQuestion('如何改善睡眠质量？')">
            如何改善睡眠质量？
          </view>
        </view>
      </view>

      <!-- 消息列表 -->
      <view 
        class="message-item" 
        v-for="(msg, index) in messages" 
        :key="index"
        :class="{ 'user-msg': msg.role === 'user' }"
        :id="'msg-' + index"
      >
        <view class="avatar">
          <view v-if="msg.role === 'assistant'" class="ai-avatar-small">
            <wd-icon name="robot" size="20px" color="#0071e3"></wd-icon>
          </view>
          <image v-else :src="userStore.avatar || '/static/placeholder/avatar.png'" class="user-avatar" />
        </view>
        <view class="content">
          <text class="text">{{ msg.content }}</text>
          <text class="time">{{ formatTime(msg.time) }}</text>
        </view>
      </view>

      <!-- 加载中 -->
      <view class="message-item" v-if="loading">
        <view class="avatar">
          <view class="ai-avatar-small">
            <wd-icon name="robot" size="20px" color="#0071e3"></wd-icon>
          </view>
        </view>
        <view class="content">
          <view class="typing-indicator">
            <view class="dot"></view>
            <view class="dot"></view>
            <view class="dot"></view>
          </view>
        </view>
      </view>

      <view class="scroll-anchor" :id="scrollAnchor"></view>
    </scroll-view>

    <!-- 底部输入 -->
    <view class="footer">
      <view class="input-wrap">
        <textarea 
          v-model="inputText" 
          placeholder="输入您的健康问题..."
          :auto-height="true"
          :maxlength="500"
          :show-confirm-bar="false"
          @confirm="sendMessage"
        />
      </view>
      <view class="send-btn" :class="{ active: inputText.trim() && !loading }" @click="sendMessage">
        <wd-icon name="send" size="22px" :color="inputText.trim() && !loading ? '#FFFFFF' : '#C7C7CC'"></wd-icon>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useUserStore } from '@/stores/user'
import { chatWithAI } from '@/api/ai'

interface Message {
  role: 'user' | 'assistant'
  content: string
  time: Date
}

const userStore = useUserStore()
const messages = ref<Message[]>([])
const inputText = ref('')
const loading = ref(false)
const scrollTop = ref(0)
const scrollIntoView = ref('')
const scrollAnchor = ref('scroll-anchor')

function sendQuickQuestion(question: string) {
  inputText.value = question
  sendMessage()
}

async function sendMessage() {
  if (!inputText.value.trim() || loading.value) return
  
  const userMessage = inputText.value.trim()
  inputText.value = ''
  
  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: userMessage,
    time: new Date()
  })
  
  scrollToBottom()
  loading.value = true
  
  try {
    const res = await chatWithAI({
      message: userMessage,
      context: messages.value.slice(-10).map(m => ({
        role: m.role,
        content: m.content
      }))
    })
    
    if (res.code === 200) {
      messages.value.push({
        role: 'assistant',
        content: res.data?.reply || '抱歉，我暂时无法回答这个问题。',
        time: new Date()
      })
    } else {
      messages.value.push({
        role: 'assistant',
        content: '网络异常，请稍后重试。',
        time: new Date()
      })
    }
  } catch (e: any) {
    messages.value.push({
      role: 'assistant',
      content: e.message || '请求失败，请检查网络连接。',
      time: new Date()
    })
  } finally {
    loading.value = false
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

function formatTime(time: Date) {
  const h = time.getHours().toString().padStart(2, '0')
  const m = time.getMinutes().toString().padStart(2, '0')
  return `${h}:${m}`
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

.welcome-card {
  background: #FFFFFF;
  border-radius: 20px;
  padding: 32px 24px;
  text-align: center;
  margin-bottom: 20px;
  
  .avatar-wrap {
    margin-bottom: 16px;
  }
  
  .ai-avatar {
    width: 64px;
    height: 64px;
    background: #E8F4FD;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
  }
  
  .title {
    font-size: 18px;
    font-weight: 700;
    color: #1D1D1F;
    display: block;
    margin-bottom: 8px;
  }
  
  .desc {
    font-size: 14px;
    color: #86868B;
    display: block;
    margin-bottom: 24px;
  }
  
  .quick-questions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    
    .question-item {
      background: #F5F5F7;
      padding: 10px 16px;
      border-radius: 20px;
      font-size: 13px;
      color: #1D1D1F;
    }
  }
}

.message-item {
  display: flex;
  margin-bottom: 16px;
  
  .avatar {
    margin-right: 12px;
    flex-shrink: 0;
    
    .ai-avatar-small {
      width: 36px;
      height: 36px;
      background: #E8F4FD;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .user-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
    }
  }
  
  .content {
    max-width: 75%;
    
    .text {
      background: #FFFFFF;
      padding: 12px 16px;
      border-radius: 0 16px 16px 16px;
      font-size: 15px;
      color: #1D1D1F;
      line-height: 1.5;
      display: block;
      word-break: break-all;
    }
    
    .time {
      font-size: 11px;
      color: #86868B;
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

.typing-indicator {
  background: #FFFFFF;
  padding: 16px 20px;
  border-radius: 0 16px 16px 16px;
  display: flex;
  gap: 6px;
  
  .dot {
    width: 8px;
    height: 8px;
    background: #86868B;
    border-radius: 50%;
    animation: typing 1.4s infinite;
    
    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }
}

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-8px); }
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

