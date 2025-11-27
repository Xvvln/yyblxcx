<template>
  <view class="page">
    <!-- 消息类型切换 -->
    <view class="tab-bar">
      <view 
        class="tab-item" 
        :class="{ active: currentTab === 'notification' }"
        @click="currentTab = 'notification'"
      >
        <wd-badge :value="unreadCounts.notification" :max="99" :hidden="!unreadCounts.notification">
          <text>通知</text>
        </wd-badge>
      </view>
      <view 
        class="tab-item" 
        :class="{ active: currentTab === 'interaction' }"
        @click="currentTab = 'interaction'"
      >
        <wd-badge :value="unreadCounts.interaction" :max="99" :hidden="!unreadCounts.interaction">
          <text>互动</text>
        </wd-badge>
      </view>
      <view 
        class="tab-item" 
        :class="{ active: currentTab === 'system' }"
        @click="currentTab = 'system'"
      >
        <wd-badge :value="unreadCounts.system" :max="99" :hidden="!unreadCounts.system">
          <text>系统</text>
        </wd-badge>
      </view>
    </view>
    
    <!-- 消息列表 -->
    <scroll-view scroll-y class="msg-list" @scrolltolower="loadMore">
      <view class="msg-item" v-for="item in currentList" :key="item.id" @click="viewDetail(item)">
        <view class="avatar-wrap">
          <image v-if="item.sender?.avatar" :src="item.sender.avatar" class="avatar" />
          <view v-else class="avatar-placeholder">
            <wd-icon :name="getIconName(item.type)" size="20px" color="#86868B"></wd-icon>
          </view>
          <view class="unread-dot" v-if="!item.is_read"></view>
        </view>
        <view class="content">
          <view class="top">
            <text class="name">{{ item.sender?.nickname || getTypeName(item.type) }}</text>
            <text class="time">{{ formatTime(item.created_at) }}</text>
          </view>
          <text class="msg">{{ item.content }}</text>
        </view>
      </view>
      
      <view class="empty" v-if="currentList.length === 0 && !loading">
        <wd-icon name="bell" size="60px" color="#E5E5EA"></wd-icon>
        <text>暂无消息</text>
      </view>
      
      <view class="loading" v-if="loading">
        <text>加载中...</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { getNotifications, markAsRead } from '@/api/notification'

const currentTab = ref('notification')
const list = ref<any[]>([])
const loading = ref(false)
const page = ref(1)

const unreadCounts = ref({
  notification: 0,
  interaction: 0,
  system: 0
})

const currentList = computed(() => {
  return list.value.filter(item => {
    if (currentTab.value === 'notification') return ['order', 'delivery'].includes(item.type)
    if (currentTab.value === 'interaction') return ['like', 'comment', 'follow'].includes(item.type)
    if (currentTab.value === 'system') return ['system', 'activity'].includes(item.type)
    return true
  })
})

watch(currentTab, () => {
  page.value = 1
  fetchList()
})

onMounted(() => {
  fetchList()
})

async function fetchList() {
  loading.value = true
  try {
    const res = await getNotifications({ page: page.value, page_size: 20 })
    if (res.code === 200) {
      if (page.value === 1) {
        list.value = res.data?.list || []
      } else {
        list.value.push(...(res.data?.list || []))
      }
      // 计算未读数
      calculateUnread()
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function calculateUnread() {
  unreadCounts.value = {
    notification: list.value.filter(i => !i.is_read && ['order', 'delivery'].includes(i.type)).length,
    interaction: list.value.filter(i => !i.is_read && ['like', 'comment', 'follow'].includes(i.type)).length,
    system: list.value.filter(i => !i.is_read && ['system', 'activity'].includes(i.type)).length
  }
}

function loadMore() {
  page.value++
  fetchList()
}

async function viewDetail(item: any) {
  // 标记已读
  if (!item.is_read) {
    try {
      await markAsRead(item.id)
      item.is_read = true
      calculateUnread()
    } catch (e) {
      console.error(e)
    }
  }
  
  // 根据类型跳转
  switch (item.type) {
    case 'order':
      uni.navigateTo({ url: `/pages/order/detail?id=${item.extra?.order_id}` })
      break
    case 'like':
    case 'comment':
      if (item.extra?.post_id) {
        uni.navigateTo({ url: `/pages/community/detail?id=${item.extra.post_id}` })
      }
      break
    case 'follow':
      if (item.sender?.id) {
        uni.navigateTo({ url: `/pages/user/homepage?id=${item.sender.id}` })
      }
      break
    default:
      // 显示详情弹窗
      uni.showModal({
        title: getTypeName(item.type),
        content: item.content,
        showCancel: false
      })
  }
}

function getIconName(type: string) {
  const icons: Record<string, string> = {
    order: 'goods',
    delivery: 'logistics',
    like: 'thumb-up',
    comment: 'comment',
    follow: 'user',
    system: 'bell',
    activity: 'gift'
  }
  return icons[type] || 'bell'
}

function getTypeName(type: string) {
  const names: Record<string, string> = {
    order: '订单通知',
    delivery: '物流通知',
    like: '点赞',
    comment: '评论',
    follow: '关注',
    system: '系统通知',
    activity: '活动通知'
  }
  return names[type] || '通知'
}

function formatTime(time: string) {
  if (!time) return ''
  const formattedTime = time.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(formattedTime)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  if (diff < 172800000) return '昨天'
  
  return `${date.getMonth() + 1}/${date.getDate()}`
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #FFFFFF;
}

.tab-bar {
  display: flex;
  background: #FFFFFF;
  border-bottom: 1px solid #F5F5F7;
  
  .tab-item {
    flex: 1;
    text-align: center;
    padding: 14px 0;
    font-size: 15px;
    color: #86868B;
    position: relative;
    
    &.active {
      color: #0071e3;
      font-weight: 600;
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 24px;
        height: 3px;
        background: #0071e3;
        border-radius: 2px;
      }
    }
  }
}

.msg-list {
  height: calc(100vh - 50px);
  
  .msg-item {
    padding: 16px;
    display: flex;
    align-items: flex-start;
    border-bottom: 1px solid #F5F5F7;
    
    .avatar-wrap {
      position: relative;
      margin-right: 12px;
      
      .avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
      }
      
      .avatar-placeholder {
        width: 48px;
        height: 48px;
        background: #F5F5F7;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      .unread-dot {
        position: absolute;
        top: 0;
        right: 0;
        width: 10px;
        height: 10px;
        background: #FF3B30;
        border-radius: 50%;
        border: 2px solid #FFFFFF;
      }
    }
    
    .content {
      flex: 1;
      
      .top {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        
        .name {
          font-size: 15px;
          font-weight: 500;
          color: #1D1D1F;
        }
        
        .time {
          font-size: 12px;
          color: #86868B;
        }
      }
      
      .msg {
        font-size: 14px;
        color: #86868B;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        overflow: hidden;
      }
    }
  }
}

.empty {
  padding: 80px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  
  text {
    font-size: 14px;
    color: #86868B;
  }
}

.loading {
  padding: 20px;
  text-align: center;
  color: #86868B;
  font-size: 14px;
}
</style>
