<template>
  <view class="page">
    <view class="section-title">问题描述</view>
    <view class="feedback-area">
      <wd-textarea 
        v-model="content" 
        placeholder="请详细描述您遇到的问题或建议，以便我们更好地为您服务" 
        :maxlength="500"
        show-word-limit
        custom-style="background: #fff; border-radius: 12px; padding: 12px;"
      />
    </view>
    
    <view class="section-title">图片上传（选填，最多3张）</view>
    <view class="upload-area">
      <view class="image-list">
        <view class="image-item" v-for="(img, idx) in images" :key="idx">
          <image :src="img" mode="aspectFill" class="preview-img" />
          <view class="delete-btn" @click="removeImage(idx)">
            <wd-icon name="close" size="12px" color="#fff" />
          </view>
        </view>
        <view class="add-btn" v-if="images.length < 3" @click="chooseImage">
          <wd-icon name="add" size="24px" color="#86868B" />
        </view>
      </view>
    </view>
    
    <view class="section-title">联系方式（选填）</view>
    <view class="contact-input">
      <wd-input 
        v-model="contact" 
        placeholder="请留下手机号或微信号，方便我们联系您" 
        no-border
        custom-style="background: #fff; border-radius: 12px;"
      />
    </view>
    
    <view class="footer">
      <wd-button block size="large" @click="submit" :loading="submitting" :disabled="!content.trim()">提交反馈</wd-button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { submitFeedback } from '@/api/user'

const content = ref('')
const contact = ref('')
const images = ref<string[]>([])
const submitting = ref(false)

function chooseImage() {
  uni.chooseImage({
    count: 3 - images.value.length,
    sizeType: ['compressed'],
    sourceType: ['album', 'camera'],
    success: (res) => {
      // 直接使用本地路径预览（生产环境应上传到服务器）
      images.value.push(...res.tempFilePaths)
    }
  })
}

function removeImage(index: number) {
  images.value.splice(index, 1)
}

async function submit() {
  if (!content.value.trim()) {
    uni.showToast({ title: '请输入反馈内容', icon: 'none' })
    return
  }
  
  submitting.value = true
  
  try {
    const res = await submitFeedback({
      content: content.value.trim(),
      images: images.value.length > 0 ? images.value : undefined,
      contact: contact.value.trim() || undefined
    })
    
    if (res.code === 200) {
      uni.showToast({ title: '感谢您的反馈', icon: 'success' })
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '提交失败', icon: 'none' })
  } finally {
    submitting.value = false
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding: 16px;
  box-sizing: border-box;
}

.section-title {
  font-size: 14px;
  color: #86868B;
  margin-bottom: 8px;
  margin-top: 16px;
  
  &:first-child {
    margin-top: 0;
  }
}

.feedback-area, .upload-area, .contact-input {
  margin-bottom: 8px;
}

.upload-area {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  
  .image-list {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    
    .image-item {
      position: relative;
      width: 80px;
      height: 80px;
      
      .preview-img {
        width: 100%;
        height: 100%;
        border-radius: 8px;
      }
      
      .delete-btn {
        position: absolute;
        top: -6px;
        right: -6px;
        width: 20px;
        height: 20px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
    }
    
    .add-btn {
      width: 80px;
      height: 80px;
      background: #F5F5F7;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px dashed #C7C7CC;
    }
  }
}

.footer {
  margin-top: 32px;
}
</style>
