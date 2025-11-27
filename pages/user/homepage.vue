<template>
  <view class="page">
    <!-- 顶部导航 -->
    <view class="nav-bar">
      <view class="back-btn" @click="goBack">
        <wd-icon name="arrow-left" size="20px" color="#1D1D1F"></wd-icon>
      </view>
      <text class="nav-title">个人主页</text>
      <view class="more-btn">
        <wd-icon name="more" size="20px" color="#1D1D1F"></wd-icon>
      </view>
    </view>

    <!-- 用户信息卡片 -->
    <view class="user-card" v-if="userInfo">
      <view class="user-header">
        <image class="avatar" :src="userInfo.avatar || '/static/placeholder/avatar.png'" mode="aspectFill" />
        <view class="user-info">
          <text class="nickname">{{ userInfo.nickname || '用户' }}</text>
          <text class="bio">{{ userInfo.bio || '这个人很懒，什么都没写~' }}</text>
        </view>
      </view>
      
      <view class="stats-row">
        <view class="stat-item">
          <text class="num">{{ userInfo.following_count || 0 }}</text>
          <text class="label">关注</text>
        </view>
        <view class="stat-item">
          <text class="num">{{ userInfo.follower_count || 0 }}</text>
          <text class="label">粉丝</text>
        </view>
        <view class="stat-item">
          <text class="num">{{ userInfo.like_count || 0 }}</text>
          <text class="label">获赞</text>
        </view>
      </view>

      <view class="action-row" v-if="!isSelf">
        <button 
          class="follow-btn" 
          :class="{ followed: isFollowed }"
          @click="toggleFollow"
        >
          {{ isFollowed ? '已关注' : '+ 关注' }}
        </button>
        <button class="msg-btn" @click="sendMessage">私信</button>
      </view>
    </view>

    <!-- 动态列表 -->
    <view class="section-title">
      <text>TA的动态</text>
      <text class="count">{{ posts.length }}篇</text>
    </view>

    <view class="post-list">
      <view class="post-item" v-for="post in posts" :key="post.id" @click="viewPost(post.id)">
        <view class="post-content">
          <text class="content">{{ post.content }}</text>
          <view class="images" v-if="post.images?.length">
            <image 
              v-for="(img, idx) in post.images.slice(0, 3)" 
              :key="idx" 
              :src="img" 
              mode="aspectFill" 
              class="img"
            />
          </view>
        </view>
        <view class="post-footer">
          <text class="time">{{ formatTime(post.created_at) }}</text>
          <view class="actions">
            <view class="action-item">
              <wd-icon name="thumb-up" size="14px" color="#86868B"></wd-icon>
              <text>{{ post.like_count || 0 }}</text>
            </view>
            <view class="action-item">
              <wd-icon name="comment" size="14px" color="#86868B"></wd-icon>
              <text>{{ post.comment_count || 0 }}</text>
            </view>
          </view>
        </view>
      </view>

      <view class="empty" v-if="!loading && posts.length === 0">
        <text>暂无动态</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getPosts, followUser, unfollowUser } from '@/api/community'
import { useUserStore } from '@/stores/user'
import request from '@/utils/request'

const userStore = useUserStore()
const userId = ref<number>(0)
const userInfo = ref<any>(null)
const posts = ref<any[]>([])
const loading = ref(false)
const isFollowed = ref(false)

const isSelf = computed(() => {
  return userId.value === userStore.userInfo?.id
})

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  userId.value = Number(currentPage.options?.id || 0)
  
  if (userId.value) {
    fetchUserInfo()
    fetchUserPosts()
  }
})

async function fetchUserInfo() {
  try {
    const res = await request.get(`/user/${userId.value}/profile`)
    if (res.code === 200) {
      userInfo.value = res.data
      isFollowed.value = res.data?.is_followed || false
    }
  } catch (e) {
    console.error('获取用户信息失败', e)
  }
}

async function fetchUserPosts() {
  loading.value = true
  try {
    const res = await getPosts({ user_id: userId.value })
    if (res.code === 200) {
      posts.value = res.data?.list || []
    }
  } catch (e) {
    console.error('获取动态失败', e)
  } finally {
    loading.value = false
  }
}

async function toggleFollow() {
  try {
    if (isFollowed.value) {
      await unfollowUser(userId.value)
      isFollowed.value = false
      if (userInfo.value) userInfo.value.follower_count--
      uni.showToast({ title: '已取消关注', icon: 'none' })
    } else {
      await followUser(userId.value)
      isFollowed.value = true
      if (userInfo.value) userInfo.value.follower_count++
      uni.showToast({ title: '关注成功', icon: 'success' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '操作失败', icon: 'none' })
  }
}

function sendMessage() {
  uni.showToast({ title: '私信功能开发中', icon: 'none' })
}

function viewPost(id: number) {
  uni.navigateTo({ url: `/pages/community/detail?id=${id}` })
}

function formatTime(time: string) {
  if (!time) return ''
  const formattedTime = time.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(formattedTime)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.nav-bar {
  height: 44px;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  padding-top: var(--status-bar-height);
  box-sizing: content-box;
  
  .back-btn, .more-btn {
    padding: 8px;
  }
  
  .nav-title {
    font-size: 17px;
    font-weight: 600;
    color: #1D1D1F;
  }
}

.user-card {
  background: #FFFFFF;
  padding: 20px;
  margin-bottom: 12px;
  
  .user-header {
    display: flex;
    margin-bottom: 20px;
    
    .avatar {
      width: 70px;
      height: 70px;
      border-radius: 50%;
      margin-right: 16px;
    }
    
    .user-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      
      .nickname {
        font-size: 20px;
        font-weight: 600;
        color: #1D1D1F;
        margin-bottom: 8px;
      }
      
      .bio {
        font-size: 13px;
        color: #86868B;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
    }
  }
  
  .stats-row {
    display: flex;
    justify-content: space-around;
    padding: 16px 0;
    border-top: 1px solid #F5F5F7;
    border-bottom: 1px solid #F5F5F7;
    
    .stat-item {
      text-align: center;
      
      .num {
        font-size: 18px;
        font-weight: 600;
        color: #1D1D1F;
        display: block;
      }
      
      .label {
        font-size: 12px;
        color: #86868B;
      }
    }
  }
  
  .action-row {
    display: flex;
    gap: 12px;
    margin-top: 16px;
    
    .follow-btn {
      flex: 1;
      height: 40px;
      background: #0071e3;
      border-radius: 20px;
      border: none;
      color: #FFFFFF;
      font-size: 15px;
      font-weight: 500;
      
      &::after {
        border: none;
      }
      
      &.followed {
        background: #F5F5F7;
        color: #86868B;
      }
    }
    
    .msg-btn {
      width: 80px;
      height: 40px;
      background: #F5F5F7;
      border-radius: 20px;
      border: none;
      color: #1D1D1F;
      font-size: 15px;
      
      &::after {
        border: none;
      }
    }
  }
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  font-size: 16px;
  font-weight: 600;
  color: #1D1D1F;
  
  .count {
    font-size: 13px;
    font-weight: 400;
    color: #86868B;
  }
}

.post-list {
  padding: 0 16px 20px;
  
  .post-item {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    
    .post-content {
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
    }
    
    .post-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid #F5F5F7;
      
      .time {
        font-size: 12px;
        color: #86868B;
      }
      
      .actions {
        display: flex;
        gap: 16px;
        
        .action-item {
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
  }
  
  .empty {
    text-align: center;
    padding: 40px 0;
    color: #86868B;
    font-size: 14px;
  }
}
</style>

