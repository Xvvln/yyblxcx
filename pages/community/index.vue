<template>
  <view class="page">
    <!-- 顶部导航 -->
    <view class="top-nav">
      <view 
        class="nav-item" 
        :class="{ active: currentTab === 'discover' }"
        @click="switchTab('discover')"
      >发现</view>
      <view 
        class="nav-item" 
        :class="{ active: currentTab === 'following' }"
        @click="switchTab('following')"
      >关注</view>
    </view>
    
    <!-- 搜索栏 -->
    <view class="search-wrap">
      <view class="search-bar" @click="goSearch">
        <wd-icon name="search" size="16px" color="#86868B"></wd-icon>
        <text class="placeholder">搜索动态、话题</text>
      </view>
    </view>
    
    <scroll-view scroll-y class="content-area" @scrolltolower="loadMore">
      <!-- 顶部话题 -->
      <scroll-view scroll-x class="topic-scroll" v-if="currentTab === 'discover'">
        <view 
          class="topic-item" 
          v-for="topic in topics" 
          :key="topic.id"
          @click="viewTopic(topic.id)"
        >
          <view class="icon-box" :style="{ background: topic.color || '#0071e3' }">
            <text class="emoji">#</text>
          </view>
          <text class="name">{{ topic.name }}</text>
          <text class="count">{{ topic.participant_count }}人参与</text>
        </view>
      </scroll-view>
      
      <!-- 瀑布流动态 -->
      <view class="waterfall">
        <view class="post-column">
          <view 
            class="post-item" 
            v-for="post in leftCol" 
            :key="post.id" 
            @click="viewDetail(post.id)"
          >
            <view class="post-image">
              <image v-if="post.images?.[0]" :src="post.images[0]" mode="aspectFill" />
              <view v-else class="image-placeholder">
                <text>📷</text>
              </view>
              <text class="tag" v-if="post.topic">{{ post.topic.name }}</text>
            </view>
            <view class="post-info">
              <text class="post-title">{{ post.content }}</text>
              <view class="post-meta">
                <view class="user-row" @click.stop="viewUserProfile(post.user?.id)">
                  <image v-if="post.user?.avatar" :src="post.user.avatar" class="avatar" />
                  <view v-else class="avatar-placeholder"></view>
                  <text class="username">{{ post.user?.nickname }}</text>
                </view>
                <view class="like-row" @click.stop="toggleLike(post)">
                  <wd-icon 
                    :name="post.is_liked ? 'thumb-up-fill' : 'thumb-up'" 
                    size="14px" 
                    :color="post.is_liked ? '#FF3B30' : '#86868B'"
                  ></wd-icon>
                  <text class="count">{{ post.like_count }}</text>
                </view>
              </view>
            </view>
          </view>
        </view>
        
        <view class="post-column">
          <view 
            class="post-item" 
            v-for="post in rightCol" 
            :key="post.id" 
            @click="viewDetail(post.id)"
          >
            <view class="post-image tall">
              <image v-if="post.images?.[0]" :src="post.images[0]" mode="aspectFill" />
              <view v-else class="image-placeholder">
                <text>📷</text>
              </view>
              <text class="tag" v-if="post.topic">{{ post.topic.name }}</text>
            </view>
            <view class="post-info">
              <text class="post-title">{{ post.content }}</text>
              <view class="post-meta">
                <view class="user-row" @click.stop="viewUserProfile(post.user?.id)">
                  <image v-if="post.user?.avatar" :src="post.user.avatar" class="avatar" />
                  <view v-else class="avatar-placeholder"></view>
                  <text class="username">{{ post.user?.nickname }}</text>
                </view>
                <view class="like-row" @click.stop="toggleLike(post)">
                  <wd-icon 
                    :name="post.is_liked ? 'thumb-up-fill' : 'thumb-up'" 
                    size="14px" 
                    :color="post.is_liked ? '#FF3B30' : '#86868B'"
                  ></wd-icon>
                  <text class="count">{{ post.like_count }}</text>
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 空状态 -->
      <view class="empty" v-if="!loading && postList.length === 0">
        <text class="empty-icon">📝</text>
        <text class="empty-text">{{ currentTab === 'following' ? '关注的人还没有发布动态' : '暂无动态' }}</text>
      </view>
          
      <view class="loading-more" v-if="loading">
        <wd-loading size="20px" />
        <text>加载中...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && postList.length > 0">
        <text>没有更多了</text>
      </view>
    </scroll-view>
    
    <!-- 发布按钮 -->
    <view class="fab-btn" @click="publish">
      <wd-icon name="add" size="32px" color="#FFFFFF"></wd-icon>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getPosts, likePost, unlikePost, getTopics } from '@/api/community'

const currentTab = ref('discover')
const postList = ref<any[]>([])
const topics = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 10
const total = ref(0)

const hasMore = computed(() => postList.value.length < total.value)
const leftCol = computed(() => postList.value.filter((_, i) => i % 2 === 0))
const rightCol = computed(() => postList.value.filter((_, i) => i % 2 !== 0))

// 获取话题
async function fetchTopics() {
  try {
    const res = await getTopics({ page: 1, page_size: 10, is_hot: 1 })
    if (res.code === 200) {
      // 给话题添加随机颜色
      const colors = ['#FF6B6B', '#4834D4', '#6AB04C', '#FF9F43', '#0071e3', '#34C759']
      topics.value = (res.data.list || []).map((t: any, i: number) => ({
        ...t,
        color: colors[i % colors.length]
      }))
    }
  } catch (e) {
    console.error(e)
  }
}

// 获取动态
async function fetchPosts(refresh = false) {
  if (loading.value) return
  loading.value = true
  
  try {
    if (refresh) {
      page.value = 1
      postList.value = []
    }
    
    const params: any = {
      page: page.value,
      page_size: pageSize,
    }
    
    if (currentTab.value === 'following') {
      params.following_only = 1
    }
    
    const res = await getPosts(params)
    if (res.code === 200 && res.data) {
      if (refresh) {
        postList.value = res.data.list || []
      } else {
        postList.value.push(...(res.data.list || []))
      }
      total.value = res.data.total || 0
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 切换Tab
function switchTab(tab: string) {
  if (currentTab.value === tab) return
  currentTab.value = tab
  fetchPosts(true)
}

// 加载更多
function loadMore() {
  if (hasMore.value && !loading.value) {
    page.value++
    fetchPosts()
  }
}

// 点赞/取消点赞
async function toggleLike(post: any) {
  try {
    if (post.is_liked) {
      await unlikePost(post.id)
      post.is_liked = false
      post.like_count--
    } else {
      await likePost(post.id)
      post.is_liked = true
      post.like_count++
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '操作失败', icon: 'none' })
  }
}

function viewDetail(id: number) {
  uni.navigateTo({ url: `/pages/community/detail?id=${id}` })
}

function viewTopic(id: number) {
  uni.navigateTo({ url: `/pages/community/topic?id=${id}` })
}

function viewUserProfile(userId?: number) {
  if (!userId) return
  uni.navigateTo({ url: `/pages/user/homepage?id=${userId}` })
}

function goSearch() {
  uni.showToast({ title: '搜索功能开发中', icon: 'none' })
}

function publish() {
  uni.navigateTo({ url: '/pages/community/publish' })
}

onShow(() => {
  fetchTopics()
  fetchPosts(true)
})
</script>

<style lang="scss" scoped>
.page {
  height: 100vh;
  background-color: #F5F5F7;
  display: flex;
  flex-direction: column;
}

.top-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  background: #FFFFFF;
  gap: 32px;
  
  .nav-item {
    font-size: 15px;
    color: #86868B;
    font-weight: 500;
    position: relative;
    padding: 8px 0;
    
    &.active {
      color: #1D1D1F;
      font-size: 17px;
      font-weight: 700;
      
      &::after {
        content: '';
        position: absolute;
        bottom: 4px;
        left: 50%;
        transform: translateX(-50%);
        width: 20px;
        height: 3px;
        background: #0071e3;
        border-radius: 2px;
      }
    }
  }
}

.search-wrap {
  background: #FFFFFF;
  padding: 8px 16px 12px;
  
  .search-bar {
    background: #F5F5F7;
    height: 36px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    
    .placeholder {
      font-size: 14px;
      color: #86868B;
    }
  }
}

.content-area {
  flex: 1;
  height: 0;
}

.topic-scroll {
  white-space: nowrap;
  padding: 12px 16px;
  background: #FFFFFF;
  margin-bottom: 8px;
  
  .topic-item {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    margin-right: 20px;
    
    .icon-box {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 6px;
      
      .emoji {
        font-size: 20px;
        color: #FFFFFF;
        font-weight: 700;
      }
    }
    
    .name {
      font-size: 12px;
      color: #1D1D1F;
      font-weight: 500;
      margin-bottom: 2px;
    }
    
    .count {
      font-size: 10px;
      color: #86868B;
    }
  }
}

.waterfall {
  padding: 8px;
  display: flex;
  justify-content: space-between;
  
  .post-column {
    width: 48%;
  }
  
  .post-item {
    background: #FFFFFF;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    
    .post-image {
      width: 100%;
      height: 160px;
      background: #F5F5F7;
      position: relative;
      
      &.tall {
        height: 200px;
      }
      
      image {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      
      .image-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
      }
      
      .tag {
        position: absolute;
        bottom: 8px;
        left: 8px;
        background: rgba(0,0,0,0.5);
        color: #FFFFFF;
        font-size: 10px;
        padding: 2px 8px;
        border-radius: 10px;
      }
    }
    
    .post-info {
      padding: 12px;
      
      .post-title {
        font-size: 14px;
        color: #1D1D1F;
        line-height: 1.4;
        margin-bottom: 10px;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        overflow: hidden;
        font-weight: 500;
      }
      
      .post-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        .user-row {
          display: flex;
          align-items: center;
          
          .avatar, .avatar-placeholder {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            margin-right: 6px;
          }
          
          .avatar-placeholder {
            background: #E5E5EA;
          }
          
          .username {
            font-size: 11px;
            color: #86868B;
            max-width: 60px;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
          }
        }
        
        .like-row {
          display: flex;
          align-items: center;
          gap: 4px;
          padding: 4px;
          
          .count {
            font-size: 11px;
            color: #86868B;
          }
        }
      }
    }
  }
}

.empty {
  padding: 60px 20px;
  text-align: center;
  
  .empty-icon {
    font-size: 48px;
    display: block;
    margin-bottom: 12px;
  }
  
  .empty-text {
    font-size: 14px;
    color: #86868B;
  }
}

.loading-more {
  padding: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  color: #86868B;
  font-size: 12px;
}

.no-more {
  padding: 16px;
  text-align: center;
  font-size: 12px;
  color: #C7C7CC;
}

.fab-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  background: #0071e3;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 20px rgba(0, 113, 227, 0.4);
  z-index: 100;
}
</style>
