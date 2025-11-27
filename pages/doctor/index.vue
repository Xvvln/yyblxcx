<template>
  <view class="page">
    <wd-tabs v-model="currentTab" sticky>
      <wd-tab title="找医生" name="doctor"></wd-tab>
      <wd-tab title="健康科普" name="article"></wd-tab>
    </wd-tabs>
    
    <view class="content">
      <view class="doctor-list" v-if="currentTab === 'doctor'">
        <view class="doctor-item" v-for="item in doctorList" :key="item.id" @click="goDoctorDetail(item.id)">
          <view class="avatar-placeholder">
            <wd-icon name="user" size="24px" color="#86868B"></wd-icon>
          </view>
          <view class="info">
            <view class="row">
              <text class="name">{{ item.name }}</text>
              <text class="title">{{ item.title }}</text>
            </view>
            <text class="hospital">{{ item.hospital }}</text>
            <text class="specialty">擅长: {{ item.specialty }}</text>
            <view class="tags">
              <text class="tag">从业{{ item.exp }}年</text>
              <text class="tag">好评率{{ item.rate }}</text>
            </view>
          </view>
          <wd-button size="small" type="primary" plain>咨询</wd-button>
        </view>
      </view>
      
      <view class="article-list" v-if="currentTab === 'article'">
        <view class="article-item" v-for="item in articleList" :key="item.id" @click="goArticleDetail(item.id)">
          <view class="info">
            <text class="title">{{ item.title }}</text>
            <text class="desc">{{ item.desc }}</text>
            <view class="meta">
              <text class="author">{{ item.author }}</text>
              <text class="views">{{ item.views }}阅读</text>
            </view>
          </view>
          <view class="image-placeholder">
            <wd-icon name="picture" size="24px" color="#86868B"></wd-icon>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentTab = ref('doctor')

const doctorList = ref([
  { id: 1, name: '王医生', title: '副主任医师', hospital: '北京协和医院', specialty: '营养搭配、减脂塑形', exp: 15, rate: '99%' },
  { id: 2, name: '李医生', title: '主治医师', hospital: '上海华山医院', specialty: '运动康复、骨科', exp: 8, rate: '98%' }
])

const articleList = ref([
  { id: 1, title: '如何科学减脂不反弹？', desc: '揭秘减脂核心原理，教你吃出好身材...', author: '王医生', views: 2300 },
  { id: 2, title: '春季流感预防指南', desc: '近期流感高发，这些预防措施你做到了吗？', author: '李医生', views: 1500 }
])

function goDoctorDetail(id: number) {
  uni.navigateTo({ url: `/pages/doctor/detail?id=${id}` })
}

function goArticleDetail(id: number) {
  uni.showToast({ title: '查看文章详情', icon: 'none' })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
}

.doctor-list,
.article-list {
  padding: 16px;
}

.doctor-item {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
  
  .avatar-placeholder {
    width: 60px;
    height: 60px;
    background: #F5F5F7;
    border-radius: 50%;
    margin-right: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .info {
    flex: 1;
    margin-right: 12px;
    
    .row {
      display: flex;
      align-items: baseline;
      margin-bottom: 4px;
      
      .name {
        font-size: 16px;
        font-weight: 600;
        margin-right: 8px;
        color: #1D1D1F;
      }
      
      .title {
        font-size: 12px;
        color: #86868B;
      }
    }
    
    .hospital {
      font-size: 12px;
      color: #86868B;
      margin-bottom: 8px;
      display: block;
    }
    
    .specialty {
      font-size: 13px;
      color: #1D1D1F;
      margin-bottom: 8px;
      display: block;
    }
    
    .tags {
      display: flex;
      gap: 8px;
      
      .tag {
        font-size: 10px;
        background: #E8F4FD;
        color: #0071e3;
        padding: 2px 6px;
        border-radius: 4px;
      }
    }
  }
}

.article-item {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  
  .info {
    flex: 1;
    margin-right: 12px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    
    .title {
      font-size: 15px;
      font-weight: 500;
      color: #1D1D1F;
      line-height: 1.4;
      margin-bottom: 8px;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
    }
    
    .desc {
      font-size: 12px;
      color: #86868B;
      margin-bottom: 8px;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 1;
      overflow: hidden;
    }
    
    .meta {
      font-size: 11px;
      color: #AEAEB2;
      display: flex;
      justify-content: space-between;
    }
  }
  
  .image-placeholder {
    width: 100px;
    height: 75px;
    background: #F5F5F7;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
