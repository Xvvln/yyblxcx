<template>
  <view class="page">
    <!-- 协议/政策页面 -->
    <view v-if="pageType" class="content-page">
      <rich-text :nodes="contentHtml"></rich-text>
    </view>
    
    <!-- 帮助中心 -->
    <view v-else class="help-list">
      <wd-cell-group border>
        <wd-cell title="功能介绍" is-link @click="showFeatures" />
        <wd-cell title="常见问题" is-link @click="showFaq" />
        <wd-cell title="联系客服" is-link value="09:00-18:00" @click="contactService" />
        <wd-cell title="意见反馈" is-link @click="feedback" />
      </wd-cell-group>
      
      <view class="faq-section" v-if="showFaqList">
        <view class="faq-title">常见问题</view>
        <view class="faq-item" v-for="(item, idx) in faqList" :key="idx" @click="item.expanded = !item.expanded">
          <view class="faq-question">
            <text>{{ item.q }}</text>
            <wd-icon :name="item.expanded ? 'arrow-up' : 'arrow-down'" size="16px" color="#86868B"></wd-icon>
          </view>
          <view class="faq-answer" v-if="item.expanded">
            <text>{{ item.a }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const pageType = ref('')
const showFaqList = ref(false)

const faqList = ref([
  { 
    q: '如何使用健康筛查功能？', 
    a: '进入首页，点击"做筛查"按钮，按照引导填写问卷，系统会自动生成健康评估报告。',
    expanded: false 
  },
  { 
    q: '运动币和膳食币有什么用？', 
    a: '运动币和膳食币可以用于兑换商城礼品、抵扣购物金额等。完成运动、饮食记录和每日签到都可以获得积分。',
    expanded: false 
  },
  { 
    q: '如何开通会员？', 
    a: '进入"我的"页面，点击"会员中心"，选择适合您的会员套餐进行购买。会员可享受专属折扣、无广告体验等特权。',
    expanded: false 
  },
  { 
    q: '如何修改个人信息？', 
    a: '进入"我的"页面，点击头像区域进入"个人资料"页面，即可修改昵称、头像、身高体重等信息。',
    expanded: false 
  },
  { 
    q: 'AI助手能做什么？', 
    a: 'AI健康助手可以回答您的健康问题，提供饮食建议、运动计划、睡眠改善等专业指导。',
    expanded: false 
  },
])

const agreementContent = `
<h2>用户协议</h2>
<p>欢迎使用营养不良筛查与健康管理小程序（以下简称"本应用"）。</p>
<h3>1. 服务说明</h3>
<p>本应用提供健康筛查、运动记录、饮食管理等健康服务功能。所有功能仅供参考，不构成医疗建议。</p>
<h3>2. 用户责任</h3>
<p>用户应确保提供的个人信息真实、准确。用户对其账号下的所有行为负责。</p>
<h3>3. 隐私保护</h3>
<p>我们重视用户隐私，详见《隐私政策》。</p>
<h3>4. 知识产权</h3>
<p>本应用的所有内容版权归开发者所有。</p>
`

const privacyContent = `
<h2>隐私政策</h2>
<p>本隐私政策说明我们如何收集、使用和保护您的个人信息。</p>
<h3>1. 信息收集</h3>
<p>我们收集您主动提供的信息，包括：注册信息、健康数据、运动记录、饮食记录等。</p>
<h3>2. 信息使用</h3>
<p>您的信息仅用于提供和改善服务，不会出售给第三方。</p>
<h3>3. 信息安全</h3>
<p>我们采用行业标准的安全措施保护您的数据。</p>
<h3>4. 您的权利</h3>
<p>您可以随时查看、修改或删除您的个人信息。</p>
`

const contentHtml = computed(() => {
  if (pageType.value === 'agreement') return agreementContent
  if (pageType.value === 'privacy') return privacyContent
  return ''
})

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  pageType.value = currentPage.options?.type || ''
  
  // 根据类型设置标题
  if (pageType.value === 'agreement') {
    uni.setNavigationBarTitle({ title: '用户协议' })
  } else if (pageType.value === 'privacy') {
    uni.setNavigationBarTitle({ title: '隐私政策' })
  }
})

function showFeatures() {
  uni.showModal({
    title: '功能介绍',
    content: '本应用提供以下核心功能：\n\n1. 健康筛查 - 营养状况评估\n2. 运动记录 - GPS轨迹、卡路里计算\n3. 饮食管理 - 食物热量查询\n4. AI助手 - 智能健康咨询\n5. 社区互动 - 分享、交流\n6. 健康商城 - 健康产品购买',
    showCancel: false
  })
}

function showFaq() {
  showFaqList.value = !showFaqList.value
}

function contactService() {
  uni.showModal({
    title: '联系客服',
    content: '客服热线：400-123-4567\n服务时间：09:00-18:00\n\n您也可以通过意见反馈功能留言',
    showCancel: false
  })
}

function feedback() {
  uni.showModal({
    title: '意见反馈',
    editable: true,
    placeholderText: '请输入您的建议或问题',
    success: (res) => {
      if (res.confirm && res.content) {
        uni.showToast({ title: '感谢您的反馈', icon: 'success' })
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
}

.content-page {
  background: #FFFFFF;
  padding: 20px;
  
  :deep(h2) {
    font-size: 20px;
    font-weight: 700;
    color: #1D1D1F;
    margin-bottom: 16px;
  }
  
  :deep(h3) {
    font-size: 16px;
    font-weight: 600;
    color: #1D1D1F;
    margin: 16px 0 8px;
  }
  
  :deep(p) {
    font-size: 14px;
    color: #1D1D1F;
    line-height: 1.8;
    margin-bottom: 12px;
  }
}

.help-list {
  padding-top: 16px;
}

.faq-section {
  margin-top: 20px;
  padding: 0 16px;
  
  .faq-title {
    font-size: 16px;
    font-weight: 600;
    color: #1D1D1F;
    margin-bottom: 12px;
  }
  
  .faq-item {
    background: #FFFFFF;
    border-radius: 12px;
    margin-bottom: 12px;
    overflow: hidden;
    
    .faq-question {
      padding: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      text {
        font-size: 15px;
        color: #1D1D1F;
        flex: 1;
      }
    }
    
    .faq-answer {
      padding: 0 16px 16px;
      
      text {
        font-size: 14px;
        color: #86868B;
        line-height: 1.6;
      }
    }
  }
}
</style>
