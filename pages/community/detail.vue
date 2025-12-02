<template>
  <view class="page">
    <!-- 动态内容 -->
    <view class="post-card" v-if="post">
      <view class="user-row" @click="viewUserProfile(post.user?.id)">
        <image v-if="post.user?.avatar" :src="post.user.avatar" class="avatar" mode="aspectFill" />
        <view v-else class="avatar-placeholder"></view>
        <view class="user-info">
          <text class="username">{{ post.user?.nickname || '用户' }}</text>
          <text class="time">{{ formatTime(post.created_at) }}</text>
        </view>
        <view class="follow-btn" v-if="!post.is_self" @click.stop="toggleFollow">
          {{ post.is_followed ? '已关注' : '+ 关注' }}
        </view>
      </view>
      
      <text class="content">{{ post.content }}</text>
      
      <view class="images" v-if="post.images?.length">
        <image 
          v-for="(img, idx) in post.images" 
          :key="idx" 
          :src="img" 
          mode="aspectFill"
          class="img"
          @click="previewImage(idx)"
        />
      </view>
      
      <view class="topic-tag" v-if="post.topic">
        <text># {{ post.topic.name }}</text>
      </view>
      
      <view class="action-row">
        <view class="action-item" @click="toggleLike">
          <wd-icon :name="post.is_liked ? 'thumb-up-fill' : 'thumb-up'" size="20px" :color="post.is_liked ? '#FF3B30' : '#86868B'"></wd-icon>
          <text>{{ post.like_count || 0 }}</text>
        </view>
        <view class="action-item">
          <wd-icon name="comment" size="20px" color="#86868B"></wd-icon>
          <text>{{ post.comment_count || 0 }}</text>
        </view>
        <button class="action-item share-btn" open-type="share">
          <wd-icon name="share" size="20px" color="#86868B"></wd-icon>
          <text>分享</text>
        </button>
      </view>
    </view>
    
    <!-- 评论区 -->
    <view class="comment-section">
      <view class="section-header">
        <text class="title">评论 ({{ comments.length }})</text>
      </view>
      
      <view class="comment-list" v-if="comments.length > 0">
        <view class="comment-item" v-for="item in comments" :key="item.id">
          <image v-if="item.user?.avatar" :src="item.user.avatar" class="avatar-small" @click="viewUserProfile(item.user?.id)" />
          <view v-else class="avatar-small placeholder" @click="viewUserProfile(item.user?.id)"></view>
          <view class="comment-info">
            <view class="comment-header">
              <text class="name" @click="viewUserProfile(item.user?.id)">{{ item.user?.nickname || '用户' }}</text>
              <text class="time">{{ formatTime(item.created_at) }}</text>
            </view>
            <text class="comment-text">{{ item.content }}</text>
            <view class="comment-actions">
              <view class="like-btn" @click="likeComment(item)">
                <wd-icon name="thumb-up" size="14px" color="#86868B"></wd-icon>
                <text>{{ item.like_count || 0 }}</text>
              </view>
              <view class="reply-btn" @click="replyTo(item)">回复</view>
            </view>
          </view>
        </view>
      </view>
      
      <view class="empty-comments" v-else>
        <text>暂无评论，快来抢沙发吧~</text>
      </view>
    </view>
    
    <!-- 底部评论输入 -->
    <view class="footer">
      <view class="input-wrap">
        <input 
          v-model="commentText" 
          :placeholder="replyPlaceholder" 
          @confirm="submitComment"
        />
      </view>
      <view class="send-btn" :class="{ active: commentText.trim() }" @click="submitComment">
        <wd-icon name="send" size="20px" :color="commentText.trim() ? '#0071e3' : '#C7C7CC'"></wd-icon>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { onShareAppMessage, onShareTimeline } from '@dcloudio/uni-app'
import { getPostDetail, getPostComments, likePost, unlikePost, commentPost, followUser, unfollowUser } from '@/api/community'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const postId = ref(0)
const post = ref<any>(null)
const comments = ref<any[]>([])
const commentText = ref('')
const replyToUser = ref<any>(null)
const loading = ref(false)

// 分享给朋友
onShareAppMessage(() => {
  const content = post.value?.content || ''
  const title = content.length > 30 ? content.substring(0, 30) + '...' : content
  return {
    title: title || '来看看这条动态',
    path: `/pages/community/detail?id=${postId.value}`,
    imageUrl: post.value?.images?.[0] || ''
  }
})

// 分享到朋友圈
onShareTimeline(() => {
  const content = post.value?.content || ''
  const title = content.length > 30 ? content.substring(0, 30) + '...' : content
  return {
    title: title || '来看看这条动态',
    query: `id=${postId.value}`,
    imageUrl: post.value?.images?.[0] || ''
  }
})

const replyPlaceholder = computed(() => {
  return replyToUser.value ? `回复 @${replyToUser.value.nickname}` : '说点什么...'
})

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  postId.value = Number(currentPage.options?.id || 0)
  
  if (postId.value) {
    fetchPostDetail()
    fetchComments()
  }
})

async function fetchPostDetail() {
  try {
    const res = await getPostDetail(postId.value)
    if (res.code === 200) {
      post.value = res.data
      post.value.is_self = post.value.user?.id === userStore.userInfo?.id
    }
  } catch (e) {
    console.error(e)
  }
}

async function fetchComments() {
  try {
    const res = await getPostComments(postId.value)
    if (res.code === 200) {
      comments.value = res.data?.list || []
    }
  } catch (e) {
    console.error(e)
  }
}

async function toggleLike() {
  if (!post.value) return
  try {
    if (post.value.is_liked) {
      await unlikePost(postId.value)
      post.value.is_liked = false
      post.value.like_count--
    } else {
      await likePost(postId.value)
      post.value.is_liked = true
      post.value.like_count++
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '操作失败', icon: 'none' })
  }
}

async function toggleFollow() {
  if (!post.value?.user) return
  try {
    if (post.value.is_followed) {
      await unfollowUser(post.value.user.id)
      post.value.is_followed = false
      uni.showToast({ title: '已取消关注', icon: 'none' })
    } else {
      await followUser(post.value.user.id)
      post.value.is_followed = true
      uni.showToast({ title: '关注成功', icon: 'success' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '操作失败', icon: 'none' })
  }
}

function replyTo(comment: any) {
  replyToUser.value = comment.user
}

async function submitComment() {
  if (!commentText.value.trim()) return
  
  try {
    const res = await commentPost(postId.value, {
      content: commentText.value,
      parent_id: replyToUser.value?.comment_id,
      reply_to_user_id: replyToUser.value?.id
    })
    
    if (res.code === 200) {
      uni.showToast({ title: '评论成功', icon: 'success' })
      commentText.value = ''
      replyToUser.value = null
      fetchComments()
      if (post.value) post.value.comment_count++
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '评论失败', icon: 'none' })
  }
}

function likeComment(comment: any) {
  // 点赞评论功能
  uni.showToast({ title: '点赞成功', icon: 'none' })
}

function viewUserProfile(userId?: number) {
  if (!userId) return
  uni.navigateTo({ url: `/pages/user/homepage?id=${userId}` })
}

function previewImage(index: number) {
  if (!post.value?.images) return
  uni.previewImage({
    current: index,
    urls: post.value.images
  })
}

function formatTime(time: string) {
  if (!time) return ''
  // 兼容 iOS 日期格式：将 "2025-11-27 11:51:58" 转换为 "2025/11/27 11:51:58"
  const formattedTime = time.replace(/-/g, '/').replace('T', ' ')
  const date = new Date(formattedTime)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return `${date.getMonth() + 1}月${date.getDate()}日`
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-bottom: 70px;
}

.post-card {
  background: #FFFFFF;
  padding: 16px;
  margin-bottom: 12px;
  
  .user-row {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    
    .avatar {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      margin-right: 12px;
    }
    
    .avatar-placeholder {
      width: 44px;
      height: 44px;
      background: #E5E5EA;
      border-radius: 50%;
      margin-right: 12px;
    }
    
    .user-info {
      flex: 1;
      
      .username {
        font-size: 15px;
        font-weight: 600;
        color: #1D1D1F;
        display: block;
      }
      
      .time {
        font-size: 12px;
        color: #86868B;
      }
    }
    
    .follow-btn {
      padding: 6px 12px;
      background: #0071e3;
      color: #FFFFFF;
      font-size: 12px;
      border-radius: 14px;
    }
  }
  
  .content {
    font-size: 16px;
    color: #1D1D1F;
    line-height: 1.6;
    margin-bottom: 12px;
    display: block;
  }
  
  .images {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
    
    .img {
      width: calc(33.33% - 6px);
      aspect-ratio: 1;
      border-radius: 8px;
    }
  }
  
  .topic-tag {
    margin-bottom: 12px;
    
    text {
      background: #E8F4FD;
      color: #0071e3;
      font-size: 12px;
      padding: 4px 8px;
      border-radius: 4px;
    }
  }
  
  .action-row {
    display: flex;
    justify-content: space-around;
    padding-top: 12px;
    border-top: 1px solid #F5F5F7;
    
    .action-item {
      display: flex;
      align-items: center;
      gap: 6px;
      
      text {
        font-size: 13px;
        color: #86868B;
      }
    }
    
    .share-btn {
      background: transparent;
      border: none;
      padding: 0;
      margin: 0;
      line-height: normal;
      
      &::after {
        border: none;
      }
    }
  }
}

.comment-section {
  background: #FFFFFF;
  padding: 16px;
  
  .section-header {
    margin-bottom: 16px;
    
    .title {
      font-size: 16px;
      font-weight: 600;
      color: #1D1D1F;
    }
  }
  
  .comment-item {
    display: flex;
    margin-bottom: 16px;
    
    .avatar-small {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      margin-right: 12px;
      flex-shrink: 0;
      
      &.placeholder {
        background: #E5E5EA;
      }
    }
    
    .comment-info {
      flex: 1;
      
      .comment-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        
        .name {
          font-size: 13px;
          font-weight: 500;
          color: #1D1D1F;
        }
        
        .time {
          font-size: 11px;
          color: #86868B;
        }
      }
      
      .comment-text {
        font-size: 14px;
        color: #1D1D1F;
        line-height: 1.5;
        margin-bottom: 8px;
        display: block;
      }
      
      .comment-actions {
        display: flex;
        gap: 16px;
        
        .like-btn, .reply-btn {
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 12px;
          color: #86868B;
        }
      }
    }
  }
  
  .empty-comments {
    text-align: center;
    padding: 40px 0;
    color: #86868B;
    font-size: 14px;
  }
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #FFFFFF;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .input-wrap {
    flex: 1;
    background: #F5F5F7;
    border-radius: 20px;
    padding: 10px 16px;
    
    input {
      width: 100%;
      font-size: 14px;
    }
  }
  
  .send-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
