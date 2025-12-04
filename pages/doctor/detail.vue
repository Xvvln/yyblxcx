<template>
  <view class="page">
    <!-- 加载占位 -->
    <view class="loading-placeholder" v-if="!doctor">
      <wd-loading size="32px" />
      <text>加载中...</text>
    </view>
    
    <template v-else>
      <view class="header">
        <image :src="doctor.avatar || '/static/placeholder/avatar.png'" class="avatar" mode="aspectFill" />
        <text class="name">{{ doctor.name }}</text>
        <text class="title">{{ doctor.title }} | {{ doctor.hospital }}</text>
        <view class="tags">
          <text class="tag" v-if="doctor.experience">从业{{ doctor.experience }}年</text>
          <text class="tag" v-if="doctor.rating">好评率{{ doctor.rating }}</text>
        </view>
      </view>
      
      <view class="section">
        <view class="section-title">擅长领域</view>
        <text class="content">{{ doctor.specialty || '暂无信息' }}</text>
      </view>
      
      <view class="section">
        <view class="section-title">医生简介</view>
        <text class="content">{{ doctor.introduction || '暂无简介' }}</text>
      </view>
      
      <view class="section" v-if="doctor.certificates?.length">
        <view class="section-title">资质证书</view>
        <view class="cert-list">
          <text class="cert-item" v-for="(cert, idx) in doctor.certificates" :key="idx">{{ cert }}</text>
        </view>
      </view>
      
      <view class="section">
        <view class="section-title">服务项目</view>
        <view class="service-list">
          <view class="service-item" v-for="service in services" :key="service.id">
            <view class="service-info">
              <text class="service-name">{{ service.name }}</text>
              <text class="service-desc">{{ service.description }}</text>
            </view>
            <view class="service-price">
              <text class="price">¥{{ service.price }}</text>
              <text class="unit">/次</text>
            </view>
          </view>
        </view>
      </view>
      
      <view class="footer">
        <view class="contact-info">
          <view class="price-row">
            <text class="label">咨询费用</text>
            <text class="price">¥{{ doctor.consult_price || 0 }}</text>
            <text class="unit">/次</text>
          </view>
        </view>
        <button class="consult-btn" @click="startConsult">
          <wd-icon name="chat" size="18px" color="#FFFFFF"></wd-icon>
          <text>立即咨询</text>
        </button>
      </view>
    </template>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import request from '@/utils/request'

const doctorId = ref(0)
const doctor = ref<any>(null)
const services = ref<any[]>([
  { id: 1, name: '图文咨询', description: '24小时内回复', price: 30 },
  { id: 2, name: '电话咨询', description: '15分钟通话', price: 100 },
  { id: 3, name: '视频咨询', description: '15分钟视频', price: 150 }
])

onLoad((options) => {
  doctorId.value = Number(options?.id || 0)
  if (doctorId.value) {
    fetchDoctorDetail()
  }
})

async function fetchDoctorDetail() {
  try {
    const res = await request.get(`/doctor/${doctorId.value}`)
    if (res.code === 200) {
      doctor.value = res.data
    } else {
      // 使用模拟数据
      doctor.value = {
        id: doctorId.value,
        name: '王医生',
        avatar: '',
        title: '副主任医师',
        hospital: '北京协和医院',
        specialty: '营养搭配、减脂塑形、慢性病营养管理、老年人营养调理、儿童生长发育营养指导',
        introduction: '从事临床营养工作15年，擅长各类人群的营养评估与干预。曾多次参与国家级营养相关课题研究，发表核心期刊论文20余篇。擅长个性化营养方案制定，帮助数千患者改善健康状况。',
        experience: 15,
        rating: '99%',
        consult_price: 30,
        certificates: ['执业医师资格证', '营养师资格证', '健康管理师证']
      }
    }
  } catch (e) {
    console.error(e)
    // 使用模拟数据
    doctor.value = {
      id: doctorId.value,
      name: '王医生',
      title: '副主任医师',
      hospital: '北京协和医院',
      specialty: '营养搭配、减脂塑形、慢性病营养管理',
      introduction: '从事临床营养工作15年，擅长各类人群的营养评估与干预。',
      experience: 15,
      rating: '99%',
      consult_price: 30
    }
  }
}

function startConsult() {
  uni.showModal({
    title: '开始咨询',
    content: `咨询费用：¥${doctor.value?.consult_price || 30}/次\n确定开始咨询？`,
    success: (res) => {
      if (res.confirm) {
        // 跳转到在线咨询页面
        uni.navigateTo({ url: `/pages/doctor/chat?id=${doctorId.value}` })
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-bottom: 100px;
}

.loading-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  gap: 16px;
  
  text {
    font-size: 14px;
    color: #86868B;
  }
}

.header {
  background: #FFFFFF;
  padding: 32px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 12px;
  
  .avatar {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    margin-bottom: 16px;
    background: #F5F5F7;
  }
  
  .name {
    font-size: 22px;
    font-weight: 700;
    color: #1D1D1F;
    margin-bottom: 8px;
  }
  
  .title {
    font-size: 14px;
    color: #86868B;
    margin-bottom: 12px;
  }
  
  .tags {
    display: flex;
    gap: 10px;
    
    .tag {
      background: #E8F4FD;
      color: #0071e3;
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 12px;
    }
  }
}

.section {
  background: #FFFFFF;
  padding: 20px;
  margin-bottom: 12px;
  
  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: #1D1D1F;
    margin-bottom: 12px;
    padding-left: 10px;
    border-left: 3px solid #0071e3;
  }
  
  .content {
    font-size: 14px;
    line-height: 1.8;
    color: #1D1D1F;
  }
  
  .cert-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    
    .cert-item {
      background: #F5F5F7;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 13px;
      color: #86868B;
    }
  }
  
  .service-list {
    .service-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 14px 0;
      border-bottom: 1px solid #F5F5F7;
      
      &:last-child {
        border-bottom: none;
      }
      
      .service-info {
        .service-name {
          font-size: 15px;
          font-weight: 500;
          color: #1D1D1F;
          display: block;
          margin-bottom: 4px;
        }
        
        .service-desc {
          font-size: 12px;
          color: #86868B;
        }
      }
      
      .service-price {
        text-align: right;
        
        .price {
          font-size: 18px;
          font-weight: 600;
          color: #FF6B00;
        }
        
        .unit {
          font-size: 12px;
          color: #86868B;
        }
      }
    }
  }
}

.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #FFFFFF;
  padding: 12px 20px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .contact-info {
    .price-row {
      display: flex;
      align-items: baseline;
      
      .label {
        font-size: 13px;
        color: #86868B;
        margin-right: 8px;
      }
      
      .price {
        font-size: 22px;
        font-weight: 700;
        color: #FF6B00;
      }
      
      .unit {
        font-size: 12px;
        color: #86868B;
      }
    }
  }
  
  .consult-btn {
    background: #0071e3;
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 600;
    padding: 12px 28px;
    border-radius: 24px;
    border: none;
    display: flex;
    align-items: center;
    gap: 6px;
    
    &::after {
      border: none;
    }
  }
}
</style>
