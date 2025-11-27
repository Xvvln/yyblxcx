<template>
  <view class="page">
    <wd-cell-group border>
      <wd-cell title="头像" is-link>
        <view class="avatar-wrapper" @click="changeAvatar">
          <image 
            v-if="form.avatar" 
            :src="form.avatar" 
            class="avatar-img" 
            mode="aspectFill"
          />
          <view v-else class="avatar-placeholder">
            <wd-icon name="user" size="24px" color="#86868B"></wd-icon>
          </view>
        </view>
      </wd-cell>
      <wd-input label="昵称" v-model="form.nickname" placeholder="请输入昵称" input-align="right" />
      <wd-cell title="性别" is-link clickable>
        <view @click="showGenderPicker = true">
          {{ form.gender === 1 ? '男' : (form.gender === 2 ? '女' : '未设置') }}
        </view>
      </wd-cell>
      <wd-cell title="出生日期" is-link clickable>
        <picker mode="date" :value="form.birthday" @change="onDateChange">
          <view>{{ form.birthday || '请选择' }}</view>
        </picker>
      </wd-cell>
      <wd-input label="身高(cm)" type="number" v-model="form.height" placeholder="请输入" input-align="right" />
      <wd-input label="体重(kg)" type="number" v-model="form.weight" placeholder="请输入" input-align="right" />
      <wd-input label="手机号" type="number" v-model="form.phone" placeholder="请输入" input-align="right" />
    </wd-cell-group>
    
    <view class="footer">
      <wd-button block type="primary" @click="save" :loading="saving">保存修改</wd-button>
    </view>

    <!-- 性别选择器 -->
    <wd-popup v-model="showGenderPicker" position="bottom">
        <wd-picker 
            :columns="genderColumns" 
            label-key="label" 
            value-key="value"
            @confirm="onGenderConfirm"
            @cancel="showGenderPicker = false"
        />
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'
import { updateUserProfile, uploadAvatar } from '@/api/user'

const userStore = useUserStore()
const showGenderPicker = ref(false)
const saving = ref(false)

const form = reactive({
  nickname: '',
  avatar: '',
  gender: 0,
  birthday: '',
  height: '',
  weight: '',
  phone: ''
})

const genderColumns = [
    { label: '男', value: 1 },
    { label: '女', value: 2 }
]

function onGenderConfirm({ value }: { value: number }) {
    form.gender = value
    showGenderPicker.value = false
}

function onDateChange(e: any) {
    form.birthday = e.detail.value
}

async function changeAvatar() {
    uni.chooseImage({
        count: 1,
        success: async (res) => {
            const filePath = res.tempFilePaths[0]
            uni.showLoading({ title: '上传中' })
            
            try {
                const result = await uploadAvatar(filePath)
                uni.hideLoading()
                
                if (result.code === 200) {
                    form.avatar = result.data.avatar
                    uni.showToast({ title: '头像上传成功', icon: 'success' })
                }
            } catch (e: any) {
                uni.hideLoading()
                uni.showToast({ title: e.message || '上传失败', icon: 'none' })
            }
        }
    })
}

async function save() {
    if (!form.nickname.trim()) {
        uni.showToast({ title: '请输入昵称', icon: 'none' })
        return
    }
    
    saving.value = true
    
    try {
        const res = await updateUserProfile({
            nickname: form.nickname,
            gender: form.gender || undefined,
            birthday: form.birthday || undefined,
            height: form.height ? Number(form.height) : undefined,
            weight: form.weight ? Number(form.weight) : undefined,
            phone: form.phone || undefined
        })
        
        if (res.code === 200) {
            uni.showToast({ title: '保存成功', icon: 'success' })
            await userStore.fetchUserInfo()
            setTimeout(() => {
                uni.navigateBack()
            }, 1500)
        }
    } catch (e: any) {
        uni.showToast({ title: e.message || '保存失败', icon: 'none' })
    } finally {
        saving.value = false
    }
}

onLoad(() => {
    const info = userStore.userInfo
    if (info) {
        form.nickname = info.nickname || ''
        form.avatar = info.avatar || ''
        form.gender = info.gender || 0
        form.birthday = info.birthday || ''
        form.height = String(info.height || '')
        form.weight = String(info.weight || '')
        form.phone = info.phone || ''
    }
})
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F7;
  padding-top: 16px;
}

.footer {
    padding: 32px 16px;
}

.avatar-wrapper {
    display: flex;
    justify-content: flex-end;
    
    .avatar-img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
    }
    
    .avatar-placeholder {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #E5E5EA;
        display: flex;
        align-items: center;
        justify-content: center;
    }
}
</style>


