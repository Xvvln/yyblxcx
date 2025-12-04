<template>
  <view class="page">
    <view v-if="loading" class="loading">
      <wd-loading />
    </view>
    <template v-else>
      <wd-cell-group border>
        <wd-cell title="向医生展示健康数据" center label="允许授权医生查看您的健康档案与筛查报告">
          <wd-switch v-model="privacy.shareHealthData" size="24px" active-color="#0071e3" @change="handleShareHealthDataChange" />
        </wd-cell>
        <wd-cell title="允许陌生人查看动态" center label="关闭后，仅关注您的人可见">
          <wd-switch v-model="privacy.publicProfile" size="24px" active-color="#0071e3" @change="handlePublicProfileChange" />
        </wd-cell>
        <wd-cell title="个性化推荐" center label="根据您的健康数据推荐相关内容">
          <wd-switch v-model="privacy.personalized" size="24px" active-color="#0071e3" @change="handlePersonalizedChange" />
        </wd-cell>
      </wd-cell-group>
      
      <view class="tip">
        <text>开启"向医生展示健康数据"后，您咨询的医生将能够查看您的详细健康档案，以便提供更准确的诊断建议。</text>
      </view>
    </template>
  </view>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { getUserSettings, updateUserSettings } from '@/api/user'

const loading = ref(true)
const privacy = reactive({
  shareHealthData: false,
  publicProfile: true,
  personalized: true
})

onMounted(async () => {
  await loadSettings()
})

async function loadSettings() {
  try {
    const res = await getUserSettings()
    if (res.code === 200 && res.data) {
      privacy.shareHealthData = res.data.share_health_data === 1
      privacy.publicProfile = res.data.public_profile === 1
      privacy.personalized = res.data.personalized === 1
    }
  } catch (e) {
    console.error('加载设置失败', e)
  } finally {
    loading.value = false
  }
}

async function handleShareHealthDataChange({ value }: { value: boolean }) {
  await saveSettings({ share_health_data: value ? 1 : 0 })
}

async function handlePublicProfileChange({ value }: { value: boolean }) {
  await saveSettings({ public_profile: value ? 1 : 0 })
}

async function handlePersonalizedChange({ value }: { value: boolean }) {
  await saveSettings({ personalized: value ? 1 : 0 })
}

async function saveSettings(data: any) {
  try {
    const res = await updateUserSettings(data)
    if (res.code === 200) {
      uni.showToast({ title: '设置已保存', icon: 'none' })
    }
  } catch (e) {
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding-top: 12px;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.tip {
  padding: 16px;
  font-size: 12px;
  color: #86868B;
  line-height: 1.5;
}
</style>
