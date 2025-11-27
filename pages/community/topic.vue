<template>
  <view class="page">
    <!-- 话题头部 -->
    <view class="topic-header" v-if="topicInfo">
      <image class="cover" :src="topicInfo.cover_image || '/static/placeholder/topic.png'" mode="aspectFill" />
      <view class="info">
        <text class="name">#{{ topicInfo.name }}</text>
        <text class="desc">{{ topicInfo.description || '暂无描述' }}</text>
        <view class="stats">
          <text class="stat">{{ topicInfo.post_count || 0 }} 篇帖子</text>
          <text class="divider">|</text>
          <text class="stat">{{ topicInfo.participant_count || 0 }} 人参与</text>
        </view>
      </view>
    </view>

    <!-- 帖子列表 -->
    <view class="post-list">
      <view class="post-item" v-for="post in posts" :key="post.id" @click="goDetail(post.id)">
        <view class="post-header">
          <image class="avatar" :src="post.user?.avatar || '/static/placeholder/avatar.png'" mode="aspectFill" />
          <view class="user-info">
            <text class="nickname">{{ post.user?.nickname || '匿名用户' }}</text>
            <text class="time">{{ formatTime(post.created_at) }}</text>
          </view>
        </view>
        <text class="content">{{ post.content }}</text>
        <view class="images" v-if="post.images && post.images.length">
          <image 
            v-for="(img, idx) in post.images.slice(0, 3)" 
            :key="idx" 
            :src="img" 
            mode="aspectFill" 
            class="img"
          />
        </view>
        <view class="post-footer">
          <view class="action">
            <wd-icon name="eye" size="14px" color="#86868B"></wd-icon>
            <text>{{ post.view_count || 0 }}</text>
          </view>
          <view class="action">
            <wd-icon name="thumb-up" size="14px" color="#86868B"></wd-icon>
            <text>{{ post.like_count || 0 }}</text>
          </view>
          <view class="action">
            <wd-icon name="comment" size="14px" color="#86868B"></wd-icon>
            <text>{{ post.comment_count || 0 }}</text>
          </view>
        </view>
      </view>

      <view class="empty" v-if="!loading && posts.length === 0">
        <text>暂无帖子</text>
      </view>
    </view>

    <!-- 发帖按钮 -->
    <view class="fab" @click="goPublish">
      <wd-icon name="add" size="24px" color="#FFFFFF"></wd-icon>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTopicDetail, getPosts } from '@/api/community'

const topicId = ref<number>(0)
const topicInfo = ref<any>(null)
const posts = ref<any[]>([])
const loading = ref(false)

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  topicId.value = Number(currentPage.options?.id || 0)
  
  if (topicId.value) {
    fetchTopicInfo()
    fetchPosts()
  }
})

async function fetchTopicInfo() {
  try {
    const res = await getTopicDetail(topicId.value)
    if (res.code === 200) {
      topicInfo.value = res.data
    }
  } catch (e) {
    console.error('获取话题详情失败', e)
  }
}

async function fetchPosts() {
  loading.value = true
  try {
    const res = await getPosts({ topic_id: topicId.value })
    if (res.code === 200) {
      posts.value = res.data?.list || []
    }
  } catch (e) {
    console.error('获取帖子列表失败', e)
  } finally {
    loading.value = false
  }
}

function formatTime(time: string) {
  if (!time) return ''
  // 兼容 iOS 日期格式
  const formattedTime = time.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(formattedTime)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前'
  if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前'
  if (diff < 604800000) return Math.floor(diff / 86400000) + '天前'
  
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

function goDetail(id: number) {
  uni.navigateTo({ url: `/pages/community/detail?id=${id}` })
}

function goPublish() {
  uni.navigateTo({ url: `/pages/community/publish?topic_id=${topicId.value}` })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.topic-header {
  background: #FFFFFF;
  padding: 20px;
  display: flex;
  gap: 16px;
  
  .cover {
    width: 80px;
    height: 80px;
    border-radius: 12px;
    flex-shrink: 0;
  }
  
  .info {
    flex: 1;
    display: flex;
    flex-direction: column;
    
    .name {
      font-size: 18px;
      font-weight: 600;
      color: #1D1D1F;
      margin-bottom: 8px;
    }
    
    .desc {
      font-size: 13px;
      color: #86868B;
      margin-bottom: 12px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    
    .stats {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .stat {
        font-size: 12px;
        color: #86868B;
      }
      
      .divider {
        color: #E5E5EA;
      }
    }
  }
}

.post-list {
  padding: 12px;
  
  .post-item {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    
    .post-header {
      display: flex;
      align-items: center;
      margin-bottom: 12px;
      
      .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        margin-right: 10px;
      }
      
      .user-info {
        .nickname {
          font-size: 14px;
          font-weight: 500;
          color: #1D1D1F;
          display: block;
        }
        
        .time {
          font-size: 11px;
          color: #86868B;
        }
      }
    }
    
    .content {
      font-size: 15px;
      color: #1D1D1F;
      line-height: 1.6;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    
    .images {
      display: flex;
      gap: 8px;
      margin-top: 12px;
      
      .img {
        width: 100px;
        height: 100px;
        border-radius: 8px;
      }
    }
    
    .post-footer {
      display: flex;
      justify-content: flex-end;
      gap: 20px;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid #F5F5F7;
      
      .action {
        display: flex;
        align-items: center;
        gap: 4px;
        
        text {
          font-size: 12px;
          color: #86868B;
        }
      }
    }
  }
  
  .empty {
    text-align: center;
    padding: 60px 0;
    color: #86868B;
    font-size: 14px;
  }
}

.fab {
  position: fixed;
  right: 20px;
  bottom: 100px;
  width: 50px;
  height: 50px;
  background: #0071e3;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
}
</style>

