<template>
  <view class="page">
    <!-- 顶部会话信息栏 -->
    <view class="session-bar">
      <view class="session-info">
        <view class="ai-badge">
          <wd-icon name="robot" size="14px" color="#0071e3"></wd-icon>
          <text>健康AI助手</text>
        </view>
      </view>
      <view class="session-actions">
        <view class="action-btn" @click="openSessionList">
          <wd-icon name="history" size="18px" color="#86868B"></wd-icon>
        </view>
        <view class="action-btn" @click="startNewSession">
          <wd-icon name="add" size="18px" color="#86868B"></wd-icon>
        </view>
      </view>
    </view>

    <!-- 聊天消息列表 -->
    <scroll-view 
      scroll-y 
      class="chat-list" 
      :scroll-top="scrollTop"
      :scroll-into-view="scrollIntoView"
      :scroll-with-animation="true"
    >
      <!-- 加载历史消息中 -->
      <view class="loading-history" v-if="loadingMessages">
        <view class="loading-spinner"></view>
        <text>加载对话历史...</text>
      </view>

      <!-- 欢迎消息 -->
      <view class="welcome-card" v-else-if="messages.length === 0 && !loading">
        <view class="avatar-wrap">
          <view class="ai-avatar">
            <wd-icon name="robot" size="36px" color="#0071e3"></wd-icon>
          </view>
        </view>
        <text class="title">我是您的健康AI助手</text>
        <text class="desc">基于您的健康档案，为您提供个性化的营养与健康建议</text>
        
        <view class="features">
          <view class="feature-item">
            <wd-icon name="check-circle" size="16px" color="#34C759"></wd-icon>
            <text>个性化饮食建议</text>
          </view>
          <view class="feature-item">
            <wd-icon name="check-circle" size="16px" color="#34C759"></wd-icon>
            <text>运动方案定制</text>
          </view>
          <view class="feature-item">
            <wd-icon name="check-circle" size="16px" color="#34C759"></wd-icon>
            <text>体重管理指导</text>
          </view>
          <view class="feature-item">
            <wd-icon name="check-circle" size="16px" color="#34C759"></wd-icon>
            <text>健康知识科普</text>
          </view>
        </view>
        
        <view class="quick-questions">
          <view class="section-title">快速提问</view>
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
            <!-- AI回复使用Markdown渲染 -->
            <view v-if="msg.role === 'assistant'" class="markdown-content">
              <rich-text :nodes="renderMarkdown(msg.content)"></rich-text>
            </view>
            <!-- 用户消息纯文本 -->
            <text v-else class="text" user-select>{{ msg.content }}</text>
          </view>
          <text class="time">{{ formatTime(msg.time) }}</text>
        </view>
      </view>

      <!-- 思考中状态 -->
      <view class="message-item" v-if="loading">
        <view class="avatar">
          <view class="ai-avatar-small thinking">
            <wd-icon name="robot" size="20px" color="#0071e3"></wd-icon>
          </view>
        </view>
        <view class="content-wrapper">
          <view class="bubble thinking-bubble">
            <view class="thinking-content">
              <view class="thinking-dots">
                <view class="dot"></view>
                <view class="dot"></view>
                <view class="dot"></view>
              </view>
              <text class="thinking-text">正在思考中...</text>
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
          :maxlength="1000"
          :show-confirm-bar="false"
          :cursor-spacing="20"
          :disabled="loading"
          @confirm="sendMessage"
        />
      </view>
      <view class="send-btn" :class="{ active: inputText.trim() && !loading, disabled: loading }" @click="sendMessage">
        <wd-icon v-if="!loading" name="send" size="20px" :color="inputText.trim() ? '#FFFFFF' : '#C7C7CC'"></wd-icon>
        <view v-else class="btn-loading"></view>
      </view>
    </view>

    <!-- 会话列表弹窗 -->
    <wd-popup 
      v-model="showSessionList" 
      position="bottom" 
      :safe-area-inset-bottom="true" 
      custom-style="border-radius: 24px 24px 0 0; max-height: 70vh;"
    >
      <view class="session-list-popup">
        <view class="popup-header">
          <text class="popup-title">对话历史</text>
          <view class="popup-close" @click="showSessionList = false">
            <wd-icon name="close" size="20px" color="#86868B"></wd-icon>
          </view>
        </view>
        
        <view class="session-scroll">
          <!-- 加载中 -->
          <view v-if="loadingSessions" class="loading-tip">
            <view class="loading-spinner"></view>
            <text>加载中...</text>
          </view>
          
          <!-- 空状态 -->
          <view v-else-if="sessions.length === 0" class="empty-tip">
            <view class="empty-icon">
              <wd-icon name="comment" size="48px" color="#C7C7CC"></wd-icon>
            </view>
            <text class="empty-text">暂无对话历史</text>
            <text class="empty-desc">开始你的第一次健康咨询吧</text>
          </view>
          
          <!-- 会话列表 -->
          <view v-else class="session-list">
            <view 
              class="session-item" 
              v-for="session in sessions" 
              :key="session.session_id"
              :class="{ active: session.session_id === sessionId }"
              @click="switchSession(session.session_id)"
            >
              <view class="session-icon">
                <wd-icon name="comment" size="20px" color="#0071e3"></wd-icon>
              </view>
              <view class="session-content">
                <text class="session-title">{{ session.title }}</text>
                <text class="session-preview">{{ session.last_message }}</text>
              </view>
              <view class="session-meta">
                <text class="session-time">{{ formatSessionTime(session.last_time) }}</text>
                <view class="session-delete" @click.stop="deleteSession(session.session_id)">
                  <wd-icon name="delete" size="16px" color="#FF3B30"></wd-icon>
                </view>
              </view>
            </view>
          </view>
        </view>
        
        <view class="popup-footer" v-if="sessions.length > 0">
          <view class="clear-btn" @click="clearAllSessions">
            <wd-icon name="delete" size="16px" color="#FF3B30"></wd-icon>
            <text>清空所有记录</text>
          </view>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { chatWithAI, getAiSessions, getAiHistory, deleteAiHistory, clearAllAiHistory } from '@/api/ai'

interface Message {
  role: 'user' | 'assistant'
  content: string
  time: Date
}

interface Session {
  session_id: string
  title: string
  message_count: number
  last_message: string
  last_time: string
}

const userStore = useUserStore()
const messages = ref<Message[]>([])
const inputText = ref('')
const loading = ref(false)
const scrollTop = ref(0)
const scrollIntoView = ref('')
const scrollAnchor = ref('scroll-anchor')
const sessionId = ref<string>('')
const showSessionList = ref(false)
const sessions = ref<Session[]>([])
const loadingSessions = ref(false)
const loadingMessages = ref(false)

const quickQuestions = [
  '根据我的身体状况，给我制定减肥计划',
  '我每天应该吃多少热量？',
  '推荐适合我的运动方式',
  '如何改善我的睡眠质量？',
  '分析一下我的BMI情况'
]

onMounted(() => {
  sessionId.value = generateSessionId()
})

function generateSessionId(): string {
  return Math.random().toString(36).substring(2, 10)
}

// Markdown 渲染函数
function renderMarkdown(text: string): string {
  if (!text) return ''
  
  let html = text
    // 转义HTML特殊字符
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
  
  // 处理标题 (## 标题)
  html = html.replace(/^### (.+)$/gm, '<div style="font-size: 15px; font-weight: 600; color: #1D1D1F; margin: 12px 0 8px 0;">$1</div>')
  html = html.replace(/^## (.+)$/gm, '<div style="font-size: 16px; font-weight: 600; color: #1D1D1F; margin: 14px 0 10px 0;">$1</div>')
  html = html.replace(/^# (.+)$/gm, '<div style="font-size: 17px; font-weight: 700; color: #1D1D1F; margin: 16px 0 12px 0;">$1</div>')
  
  // 处理粗体 **text**
  html = html.replace(/\*\*(.+?)\*\*/g, '<span style="font-weight: 600; color: #1D1D1F;">$1</span>')
  
  // 处理斜体 *text*
  html = html.replace(/\*(.+?)\*/g, '<span style="font-style: italic;">$1</span>')
  
  // 处理emoji标记的列表项（如 🍽️ 饮食调整）
  html = html.replace(/^([🍽️🏃⏰💡⚠️🔥💪🧘📝🥗☕🌙📊📐💊🍎⚖️✨🎯]+)\s*(.+)$/gm, 
    '<div style="margin: 10px 0 6px 0;"><span style="margin-right: 6px;">$1</span><span style="font-weight: 600; color: #1D1D1F;">$2</span></div>')
  
  // 处理无序列表 - item
  html = html.replace(/^- (.+)$/gm, '<div style="margin: 4px 0; padding-left: 16px; position: relative;"><span style="position: absolute; left: 0; color: #0071e3;">•</span>$1</div>')
  
  // 处理有序列表 1. item
  html = html.replace(/^(\d+)\. (.+)$/gm, '<div style="margin: 4px 0; padding-left: 20px; position: relative;"><span style="position: absolute; left: 0; color: #0071e3; font-weight: 500;">$1.</span>$2</div>')
  
  // 处理换行
  html = html.replace(/\n\n/g, '<div style="height: 12px;"></div>')
  html = html.replace(/\n/g, '<br/>')
  
  return html
}

function sendQuickQuestion(question: string) {
  inputText.value = question
  sendMessage()
}

async function sendMessage() {
  if (!inputText.value.trim() || loading.value) return
  
  const userMessage = inputText.value.trim()
  inputText.value = ''
  
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
      session_id: sessionId.value
    })
    
    if (res.code === 200) {
      if (res.data?.session_id) {
        sessionId.value = res.data.session_id
      }
      
      messages.value.push({
        role: 'assistant',
        content: res.data?.reply || '抱歉，我暂时无法回答这个问题。',
        time: new Date()
      })
    } else {
      messages.value.push({
        role: 'assistant',
        content: res.message || '网络异常，请稍后重试。',
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

// 兼容iOS的日期解析
function parseDate(dateStr: string): Date {
  if (!dateStr) return new Date()
  // 将 "2025-12-04 15:24:17" 转换为 "2025/12/04 15:24:17"
  const compatibleStr = dateStr.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(compatibleStr)
  return isNaN(date.getTime()) ? new Date() : date
}

function formatTime(time: Date) {
  const h = time.getHours().toString().padStart(2, '0')
  const m = time.getMinutes().toString().padStart(2, '0')
  return `${h}:${m}`
}

function formatSessionTime(timeStr: string) {
  if (!timeStr) return ''
  // 兼容iOS：将 "2025-12-04 15:24:17" 转换为 "2025/12/04 15:24:17"
  const compatibleStr = timeStr.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(compatibleStr)
  
  if (isNaN(date.getTime())) return ''
  
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
  
  return `${date.getMonth() + 1}/${date.getDate()}`
}

async function startNewSession() {
  sessionId.value = generateSessionId()
  messages.value = []
  
  uni.showToast({
    title: '已创建新对话',
    icon: 'success'
  })
}

async function loadSessions() {
  loadingSessions.value = true
  try {
    const res = await getAiSessions({ page_size: 50 })
    if (res.code === 200 && res.data?.list) {
      sessions.value = res.data.list
    }
  } catch (e) {
    console.error('加载会话列表失败:', e)
  } finally {
    loadingSessions.value = false
  }
}

function openSessionList() {
  showSessionList.value = true
  loadSessions()
}

async function switchSession(targetSessionId: string) {
  if (targetSessionId === sessionId.value) {
    showSessionList.value = false
    return
  }
  
  showSessionList.value = false
  sessionId.value = targetSessionId
  messages.value = []
  
  // 加载该会话的历史消息
  await loadSessionMessages(targetSessionId)
}

async function loadSessionMessages(sid: string) {
  loadingMessages.value = true
  try {
    const res = await getAiHistory({ session_id: sid, page_size: 50 })
    console.log('加载会话消息响应:', res)
    if (res.code === 200 && res.data?.list) {
      messages.value = res.data.list.map((item: any) => ({
        role: item.role as 'user' | 'assistant',
        content: item.content,
        time: parseDate(item.created_at)
      }))
      nextTick(() => scrollToBottom())
    } else if (res.code === 200 && res.data?.items) {
      // 兼容 items 字段
      messages.value = res.data.items.map((item: any) => ({
        role: item.role as 'user' | 'assistant',
        content: item.content,
        time: parseDate(item.created_at)
      }))
      nextTick(() => scrollToBottom())
    } else {
      console.log('会话无消息或响应格式不对:', res)
    }
  } catch (e: any) {
    console.error('加载会话消息失败:', e)
    // 不显示toast，因为可能是空会话
  } finally {
    loadingMessages.value = false
  }
}

async function deleteSession(targetSessionId: string) {
  uni.showModal({
    title: '确认删除',
    content: '确定要删除这个对话吗？',
    success: async (result) => {
      if (result.confirm) {
        try {
          await deleteAiHistory(targetSessionId)
          sessions.value = sessions.value.filter(s => s.session_id !== targetSessionId)
          
          if (targetSessionId === sessionId.value) {
            sessionId.value = generateSessionId()
            messages.value = []
          }
          
          uni.showToast({
            title: '删除成功',
            icon: 'success'
          })
        } catch (e) {
          uni.showToast({
            title: '删除失败',
            icon: 'error'
          })
        }
      }
    }
  })
}

async function clearAllSessions() {
  uni.showModal({
    title: '确认清空',
    content: '确定要清空所有对话记录吗？此操作不可恢复。',
    success: async (result) => {
      if (result.confirm) {
        try {
          await clearAllAiHistory()
          sessions.value = []
          sessionId.value = generateSessionId()
          messages.value = []
          showSessionList.value = false
          
          uni.showToast({
            title: '已清空',
            icon: 'success'
          })
        } catch (e) {
          uni.showToast({
            title: '清空失败',
            icon: 'error'
          })
        }
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #F5F5F7;
}

.session-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #FFFFFF;
  border-bottom: 0.5px solid rgba(0,0,0,0.05);
  
  .session-info {
    .ai-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 113, 227, 0.1);
      padding: 6px 12px;
      border-radius: 16px;
      
      text {
        font-size: 14px;
        font-weight: 500;
        color: #0071e3;
      }
    }
  }
  
  .session-actions {
    display: flex;
    gap: 8px;
    
    .action-btn {
      width: 36px;
      height: 36px;
      background: #F5F5F7;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &:active {
        background: #E5E5EA;
      }
    }
  }
}

.chat-list {
  flex: 1;
  box-sizing: border-box;
  padding: 20px 16px;
}

.loading-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  gap: 16px;
  
  .loading-spinner {
    width: 36px;
    height: 36px;
    border: 3px solid #E5E5EA;
    border-top-color: #0071e3;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  
  text {
    font-size: 14px;
    color: #86868B;
  }
}

.welcome-card {
  background: #FFFFFF;
  border-radius: 24px;
  padding: 40px 24px;
  text-align: center;
  margin: 20px 4px 40px;
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
    margin-bottom: 24px;
    line-height: 1.5;
  }
  
  .features {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px 20px;
    margin-bottom: 32px;
    
    .feature-item {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      color: #1D1D1F;
    }
  }
  
  .section-title {
    font-size: 14px;
    font-weight: 600;
    color: #86868B;
    text-align: left;
    margin-bottom: 12px;
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
      text-align: left;
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
  padding: 0 4px;
  
  .avatar {
    margin-right: 12px;
    flex-shrink: 0;
    align-self: flex-start;
    
    .ai-avatar-small {
      width: 36px;
      height: 36px;
      background: #E8F4FD;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &.thinking {
        animation: pulse 1.5s infinite;
      }
    }
    
    .user-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #F5F5F7;
    }
  }
  
  .content-wrapper {
    max-width: 80%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    
    .bubble {
      background: #FFFFFF;
      padding: 14px 18px;
      border-radius: 4px 18px 18px 18px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      
      .text {
        font-size: 15px;
        color: #1D1D1F;
        line-height: 1.6;
        display: block;
        word-wrap: break-word;
        white-space: pre-wrap;
      }
      
      .markdown-content {
        font-size: 15px;
        color: #1D1D1F;
        line-height: 1.6;
        word-wrap: break-word;
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
        border-radius: 18px 4px 18px 18px;
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

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.8; }
}

.thinking-bubble {
  background: #FFFFFF !important;
  min-width: 140px;
  
  .thinking-content {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .thinking-text {
      font-size: 14px;
      color: #86868B;
    }
  }
  
  .thinking-dots {
    display: flex;
    gap: 4px;
    
    .dot {
      width: 6px;
      height: 6px;
      background: #0071e3;
      border-radius: 50%;
      animation: thinking 1.4s infinite ease-in-out both;
      
      &:nth-child(1) { animation-delay: -0.32s; }
      &:nth-child(2) { animation-delay: -0.16s; }
      &:nth-child(3) { animation-delay: 0; }
    }
  }
}

@keyframes thinking {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

.scroll-anchor {
  height: 1px;
  width: 100%;
}

.footer {
  background: rgba(255, 255, 255, 0.95);
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
      
      &[disabled] {
        opacity: 0.6;
      }
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
    }
    
    &.disabled {
      opacity: 0.6;
    }
    
    &:active:not(.disabled) {
      transform: scale(0.95);
    }
    
    .btn-loading {
      width: 20px;
      height: 20px;
      border: 2px solid #C7C7CC;
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 会话列表弹窗样式 */
.session-list-popup {
  background: #FFFFFF;
  padding: 20px;
  min-height: 300px;
  
  .popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 0.5px solid rgba(0,0,0,0.05);
    
    .popup-title {
      font-size: 18px;
      font-weight: 600;
      color: #1D1D1F;
    }
    
    .popup-close {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #F5F5F7;
      border-radius: 50%;
      
      &:active {
        background: #E5E5EA;
      }
    }
  }
  
  .session-scroll {
    max-height: 350px;
    overflow-y: auto;
  }
  
  .loading-tip {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 60px 20px;
    color: #86868B;
    font-size: 14px;
    
    .loading-spinner {
      width: 32px;
      height: 32px;
      border: 3px solid #E5E5EA;
      border-top-color: #0071e3;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
  }
  
  .empty-tip {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 20px;
    
    .empty-icon {
      width: 80px;
      height: 80px;
      background: #F5F5F7;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 16px;
    }
    
    .empty-text {
      font-size: 16px;
      font-weight: 500;
      color: #1D1D1F;
      margin-bottom: 8px;
    }
    
    .empty-desc {
      font-size: 14px;
      color: #86868B;
    }
  }
  
  .session-list {
    .session-item {
      display: flex;
      align-items: center;
      padding: 16px;
      background: #F5F5F7;
      border-radius: 16px;
      margin-bottom: 12px;
      transition: all 0.2s;
      
      &:active {
        background: #E5E5EA;
      }
      
      &.active {
        background: rgba(0, 113, 227, 0.1);
        border: 1px solid rgba(0, 113, 227, 0.2);
      }
      
      .session-icon {
        width: 40px;
        height: 40px;
        background: #FFFFFF;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        flex-shrink: 0;
      }
      
      .session-content {
        flex: 1;
        min-width: 0;
        
        .session-title {
          font-size: 15px;
          font-weight: 500;
          color: #1D1D1F;
          display: block;
          margin-bottom: 4px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        
        .session-preview {
          font-size: 13px;
          color: #86868B;
          display: block;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
      
      .session-meta {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 8px;
        margin-left: 12px;
        
        .session-time {
          font-size: 12px;
          color: #AEAEB2;
        }
        
        .session-delete {
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          
          &:active {
            background: rgba(255, 59, 48, 0.1);
          }
        }
      }
    }
  }
  
  .popup-footer {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 0.5px solid rgba(0,0,0,0.05);
    
    .clear-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 14px;
      color: #FF3B30;
      font-size: 14px;
      font-weight: 500;
      border-radius: 12px;
      
      &:active {
        background: rgba(255, 59, 48, 0.1);
      }
    }
  }
}
</style>
