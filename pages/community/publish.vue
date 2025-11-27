<template>
  <view class="page">
    <!-- 内容输入 -->
    <view class="input-area">
      <textarea 
        v-model="content" 
        placeholder="分享你的健康生活..." 
        :maxlength="500"
        class="content-input"
        :auto-height="true"
      />
      <text class="word-count">{{ content.length }}/500</text>
    </view>
    
    <!-- 图片上传 -->
    <view class="upload-area">
      <view class="image-list">
        <view class="image-item" v-for="(img, idx) in imageList" :key="idx">
          <image :src="img" mode="aspectFill" @click="previewImage(idx)" />
          <view class="delete-btn" @click="removeImage(idx)">
            <wd-icon name="close-fill" size="18px" color="#FFFFFF"></wd-icon>
          </view>
        </view>
        <view class="upload-btn" v-if="imageList.length < 9" @click="chooseImage">
          <wd-icon name="camera" size="28px" color="#86868B"></wd-icon>
          <text class="text">{{ imageList.length }}/9</text>
        </view>
      </view>
    </view>
    
    <!-- 选择话题 -->
    <view class="topic-section" @click="showTopicPicker = true">
      <view class="topic-label">
        <wd-icon name="tag" size="18px" color="#0071e3"></wd-icon>
        <text>选择话题</text>
      </view>
      <view class="topic-value">
        <text v-if="selectedTopic">{{ selectedTopic.name }}</text>
        <text v-else class="placeholder">添加话题获得更多曝光</text>
        <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
      </view>
    </view>
    
    <!-- 位置 -->
    <view class="location-section" @click="chooseLocation">
      <view class="location-label">
        <wd-icon name="location" size="18px" color="#0071e3"></wd-icon>
        <text>添加位置</text>
      </view>
      <view class="location-value">
        <text v-if="location">{{ location }}</text>
        <text v-else class="placeholder">可选</text>
        <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
      </view>
    </view>
    
    <!-- 底部发布按钮 -->
    <view class="footer">
      <button class="publish-btn" :disabled="!canPublish" :loading="publishing" @click="publish">
        发布
      </button>
    </view>
    
    <!-- 话题选择弹窗 -->
    <wd-popup v-model="showTopicPicker" position="bottom" custom-style="border-radius: 20px 20px 0 0;">
      <view class="topic-picker">
        <view class="picker-header">
          <text class="title">选择话题</text>
          <view class="close-btn" @click="showTopicPicker = false">
            <wd-icon name="close" size="20px" color="#86868B"></wd-icon>
          </view>
        </view>
        <scroll-view scroll-y class="topic-list">
          <view 
            class="topic-item" 
            v-for="topic in topicList" 
            :key="topic.id"
            :class="{ active: selectedTopic?.id === topic.id }"
            @click="selectTopic(topic)"
          >
            <text class="topic-name"># {{ topic.name }}</text>
            <text class="topic-count">{{ topic.post_count }}人参与</text>
          </view>
        </scroll-view>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { createPost, getTopics } from '@/api/community'

const content = ref('')
const imageList = ref<string[]>([])
const selectedTopic = ref<any>(null)
const location = ref('')
const publishing = ref(false)
const showTopicPicker = ref(false)
const topicList = ref<any[]>([])

const canPublish = computed(() => {
  return content.value.trim().length > 0 || imageList.value.length > 0
})

onMounted(() => {
  fetchTopics()
})

async function fetchTopics() {
  try {
    const res = await getTopics({ page: 1, page_size: 50 })
    if (res.code === 200) {
      topicList.value = res.data?.list || []
    }
  } catch (e) {
    console.error(e)
  }
}

function chooseImage() {
  uni.chooseImage({
    count: 9 - imageList.value.length,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      // 模拟上传，实际应调用上传接口
      imageList.value.push(...res.tempFilePaths)
    }
  })
}

function removeImage(index: number) {
  imageList.value.splice(index, 1)
}

function previewImage(index: number) {
  uni.previewImage({
    current: index,
    urls: imageList.value
  })
}

function selectTopic(topic: any) {
  selectedTopic.value = topic
  showTopicPicker.value = false
}

function chooseLocation() {
  uni.chooseLocation({
    success: (res) => {
      location.value = res.name || res.address
    },
    fail: () => {
      // 用户拒绝或失败时的处理
    }
  })
}

async function publish() {
  if (!canPublish.value) return
  
  publishing.value = true
  try {
    const res = await createPost({
      content: content.value,
      images: imageList.value,
      topic_id: selectedTopic.value?.id,
      location: location.value
    })
    
    if (res.code === 200) {
      uni.showToast({ title: '发布成功', icon: 'success' })
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    } else {
      uni.showToast({ title: res.message || '发布失败', icon: 'none' })
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '发布失败', icon: 'none' })
  } finally {
    publishing.value = false
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #FFFFFF;
  padding-bottom: 100px;
}

.input-area {
  padding: 16px;
  position: relative;
  
  .content-input {
    width: 100%;
    min-height: 150px;
    font-size: 16px;
    line-height: 1.6;
  }
  
  .word-count {
    position: absolute;
    right: 20px;
    bottom: 20px;
    font-size: 12px;
    color: #C7C7CC;
  }
}

.upload-area {
  padding: 0 16px 16px;
  
  .image-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .image-item {
    width: calc(33.33% - 7px);
    aspect-ratio: 1;
    position: relative;
    
    image {
      width: 100%;
      height: 100%;
      border-radius: 8px;
    }
    
    .delete-btn {
      position: absolute;
      top: -8px;
      right: -8px;
      width: 24px;
      height: 24px;
      background: rgba(0,0,0,0.6);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
  
  .upload-btn {
    width: calc(33.33% - 7px);
    aspect-ratio: 1;
    background: #F5F5F7;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    
    .text {
      font-size: 12px;
      color: #86868B;
      margin-top: 4px;
    }
  }
}

.topic-section, .location-section {
  padding: 16px;
  border-top: 1px solid #F5F5F7;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.topic-label, .location-label {
  display: flex;
  align-items: center;
  gap: 8px;
  
  text {
    font-size: 15px;
    color: #1D1D1F;
  }
}

.topic-value, .location-value {
  display: flex;
  align-items: center;
  gap: 4px;
  
  text {
    font-size: 14px;
    color: #1D1D1F;
  }
  
  .placeholder {
    color: #C7C7CC;
  }
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  background: #FFFFFF;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .publish-btn {
    width: 100%;
    height: 48px;
    background: #0071e3;
    border-radius: 24px;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 600;
    border: none;
    
    &:disabled {
      background: #E5E5EA;
      color: #FFFFFF;
    }
    
    &::after {
      border: none;
    }
  }
}

.topic-picker {
  padding: 20px;
  
  .picker-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    .title {
      font-size: 18px;
      font-weight: 600;
    }
  }
  
  .topic-list {
    max-height: 400px;
    
    .topic-item {
      padding: 14px 16px;
      border-radius: 12px;
      margin-bottom: 8px;
      background: #F5F5F7;
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      &.active {
        background: #E8F4FD;
        border: 1px solid #0071e3;
      }
      
      .topic-name {
        font-size: 15px;
        color: #1D1D1F;
      }
      
      .topic-count {
        font-size: 12px;
        color: #86868B;
      }
    }
  }
}
</style>
