<template>
  <view class="page">
    <!-- 聊天消息列表 -->
    <scroll-view 
      scroll-y 
      class="chat-list" 
      :scroll-top="scrollTop"
      :scroll-into-view="scrollIntoView"
      :scroll-with-animation="true"
    >
      <!-- 欢迎消息 -->
      <view class="welcome-card" v-if="messages.length === 0">
        <view class="avatar-wrap">
          <view class="ai-avatar">
            <wd-icon name="robot" size="36px" color="#0071e3"></wd-icon>
          </view>
        </view>
        <text class="title">我是您的健康AI助手</text>
        <text class="desc">有任何健康问题都可以问我，我会为您提供专业的建议</text>
        
        <view class="quick-questions">
          <view 
            class="question-item" 
            v-for="(q, idx) in quickQuestions" 
            :key="idx"
            @click="sendQuickQuestion(q)"
          >
            <text>{{ q }}</text>
            <wd-icon name="arrow-right" size="14px" color="#C7C7CC"></wd-icon>
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
          <image v-else :src="userStore.userInfo?.avatar || '/static/placeholder/avatar.png'" class="user-avatar" mode="aspectFill" />
        </view>
        <view class="content-wrapper">
          <view class="bubble">
            <text class="text" user-select>{{ msg.content }}</text>
          </view>
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
        <view class="content-wrapper">
          <view class="bubble loading-bubble">
            <view class="typing-indicator">
              <view class="dot"></view>
              <view class="dot"></view>
              <view class="dot"></view>
            </view>
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
          :cursor-spacing="20"
          @confirm="sendMessage"
        />
      </view>
      <view class="send-btn" :class="{ active: inputText.trim() && !loading }" @click="sendMessage">
        <wd-icon name="send" size="20px" :color="inputText.trim() && !loading ? '#FFFFFF' : '#C7C7CC'"></wd-icon>
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

const quickQuestions = [
  '如何制定健康的减肥计划？',
  '每天应该喝多少水？',
  '运动后应该吃什么？',
  '如何改善睡眠质量？'
]

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
    }, 100)
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
  box-sizing: border-box;
  padding: 20px 16px;
}

.welcome-card {
  background: #FFFFFF;
  border-radius: 24px;
  padding: 40px 24px;
  text-align: center;
  margin: 20px 4px 40px; // Add margin to prevent edge touching
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
  
  .avatar-wrap {
    margin-bottom: 20px;
  }
  
  .ai-avatar {
    width: 72px;
    height: 72px;
    background: linear-gradient(135deg, #E8F4FD 0%, #F2F8FD 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    box-shadow: 0 4px 12px rgba(0, 113, 227, 0.1);
  }
  
  .title {
    font-size: 20px;
    font-weight: 700;
    color: #1D1D1F;
    display: block;
    margin-bottom: 8px;
  }
  
  .desc {
    font-size: 14px;
    color: #86868B;
    display: block;
    margin-bottom: 32px;
    line-height: 1.5;
  }
  
  .quick-questions {
    display: flex;
    flex-direction: column;
    gap: 12px;
    
    .question-item {
      background: #F5F5F7;
      padding: 16px 20px;
      border-radius: 16px;
      font-size: 14px;
      color: #1D1D1F;
      font-weight: 500;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s;
      
      &:active {
        background: #E5E5EA;
        transform: scale(0.98);
      }
    }
  }
}

.message-item {
  display: flex;
  margin-bottom: 24px;
  padding: 0 4px; // Safety padding
  
  .avatar {
    margin-right: 12px;
    flex-shrink: 0;
    align-self: flex-end; // Align avatar to bottom of message
    margin-bottom: 4px;
    
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
      background: #F5F5F7;
    }
  }
  
  .content-wrapper {
    max-width: 72%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    
    .bubble {
      background: #FFFFFF;
      padding: 14px 18px;
      border-radius: 18px 18px 18px 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      
      .text {
        font-size: 16px;
        color: #1D1D1F;
        line-height: 1.5;
        display: block;
        word-wrap: break-word;
        white-space: pre-wrap;
      }
    }
    
    .time {
      font-size: 11px;
      color: #AEAEB2;
      margin-top: 6px;
      margin-left: 4px;
    }
  }
  
  &.user-msg {
    flex-direction: row-reverse;
    
    .avatar {
      margin-right: 0;
      margin-left: 12px;
    }
    
    .content-wrapper {
      align-items: flex-end;
      
      .bubble {
        background: #0071e3;
        border-radius: 18px 18px 4px 18px;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.2);
        
        .text {
          color: #FFFFFF;
        }
      }
      
      .time {
        margin-left: 0;
        margin-right: 4px;
      }
    }
  }
}

.loading-bubble {
  padding: 16px 20px !important;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
}

.typing-indicator {
  display: flex;
  gap: 5px;
  
  .dot {
    width: 6px;
    height: 6px;
    background: #86868B;
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out both;
    
    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
    &:nth-child(3) { animation-delay: 0; }
  }
}

@keyframes typing {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.scroll-anchor {
  height: 1px;
  width: 100%;
}

.footer {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  padding: 12px 16px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
  display: flex;
  align-items: flex-end;
  gap: 12px;
  border-top: 0.5px solid rgba(0,0,0,0.05);
  position: sticky;
  bottom: 0;
  z-index: 100;
  
  .input-wrap {
    flex: 1;
    background: #F5F5F7;
    border-radius: 24px;
    padding: 12px 18px;
    min-height: 24px;
    
    textarea {
      width: 100%;
      font-size: 16px;
      line-height: 1.4;
      max-height: 100px;
      padding: 0;
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
    transition: all 0.2s;
    
    &.active {
      background: #0071e3;
      box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
      transform: scale(1.05);
    }
    
    &:active {
      transform: scale(0.95);
    }
  }
}
</style>
