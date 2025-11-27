<template>
  <view class="page">
    <view class="address-list" v-if="list.length > 0">
      <view class="address-item" v-for="item in list" :key="item.id" @click="selectAddress(item)">
        <view class="info">
          <view class="user-row">
            <text class="name">{{ item.name }}</text>
            <text class="phone">{{ item.phone }}</text>
            <text class="tag" v-if="item.is_default">默认</text>
          </view>
          <text class="detail">{{ item.province }}{{ item.city }}{{ item.district }}{{ item.detail }}</text>
        </view>
        <view class="actions">
          <view class="action-btn" @click.stop="setDefault(item)" v-if="!item.is_default">
            <wd-icon name="location" size="18px" color="#86868B"></wd-icon>
          </view>
          <view class="action-btn" @click.stop="editAddress(item)">
            <wd-icon name="edit" size="18px" color="#86868B"></wd-icon>
          </view>
          <view class="action-btn" @click.stop="deleteAddress(item)">
            <wd-icon name="delete" size="18px" color="#FF3B30"></wd-icon>
          </view>
        </view>
      </view>
    </view>
    
    <view class="empty" v-else>
      <wd-icon name="location" size="60px" color="#E5E5EA"></wd-icon>
      <text class="text">暂无收货地址</text>
      <text class="sub">添加地址，方便下单配送</text>
    </view>
    
    <view class="footer">
      <button class="add-btn" @click="addAddress">
        <wd-icon name="add" size="18px" color="#FFFFFF"></wd-icon>
        <text>新增收货地址</text>
      </button>
    </view>
    
    <!-- 新增/编辑地址弹窗 -->
    <wd-popup v-model="showForm" position="bottom" custom-style="border-radius: 24px 24px 0 0;">
      <view class="form-panel">
        <view class="panel-header">
          <text class="title">{{ isEdit ? '编辑地址' : '新增地址' }}</text>
          <view class="close-btn" @click="showForm = false">
            <wd-icon name="close" size="20px" color="#86868B"></wd-icon>
          </view>
        </view>
        
        <view class="form-content">
          <view class="form-item">
            <text class="label">收货人</text>
            <input v-model="form.name" placeholder="请输入收货人姓名" />
          </view>
          <view class="form-item">
            <text class="label">手机号</text>
            <input v-model="form.phone" type="number" placeholder="请输入手机号" maxlength="11" />
          </view>
          <view class="form-item" @click="chooseRegion">
            <text class="label">所在地区</text>
            <view class="region-value">
              <text v-if="form.province">{{ form.province }} {{ form.city }} {{ form.district }}</text>
              <text v-else class="placeholder">请选择省市区</text>
              <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
            </view>
          </view>
          <view class="form-item">
            <text class="label">详细地址</text>
            <input v-model="form.detail" placeholder="街道、楼牌号等" />
          </view>
          <view class="form-item switch-item">
            <text class="label">设为默认地址</text>
            <switch :checked="form.is_default" @change="form.is_default = $event.detail.value" color="#0071e3" />
          </view>
        </view>
        
        <view class="form-footer">
          <button class="save-btn" @click="saveAddress" :loading="saving">保存地址</button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getAddressList, addAddress as apiAddAddress, updateAddress, deleteAddress as apiDeleteAddress, setDefaultAddress } from '@/api/user'

interface Address {
  id: number
  name: string
  phone: string
  province: string
  city: string
  district: string
  detail: string
  is_default: number
}

const list = ref<Address[]>([])
const showForm = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const saving = ref(false)
const selectMode = ref(false) // 是否是选择模式（从订单页进入）

const form = reactive({
  name: '',
  phone: '',
  province: '',
  city: '',
  district: '',
  detail: '',
  is_default: false
})

onMounted(() => {
  const pages = getCurrentPages()
  const currentPage = pages[pages.length - 1] as any
  selectMode.value = currentPage.options?.select === '1'
})

onShow(() => {
  fetchList()
})

async function fetchList() {
  try {
    const res = await getAddressList()
    if (res.code === 200) {
      list.value = res.data?.list || []
    }
  } catch (e) {
    console.error(e)
  }
}

function addAddress() {
  isEdit.value = false
  editId.value = 0
  resetForm()
  showForm.value = true
}

function editAddress(item: Address) {
  isEdit.value = true
  editId.value = item.id
  form.name = item.name
  form.phone = item.phone
  form.province = item.province
  form.city = item.city
  form.district = item.district
  form.detail = item.detail
  form.is_default = item.is_default === 1
  showForm.value = true
}

function resetForm() {
  form.name = ''
  form.phone = ''
  form.province = ''
  form.city = ''
  form.district = ''
  form.detail = ''
  form.is_default = false
}

function chooseRegion() {
  uni.chooseLocation({
    success: () => {
      // 微信位置选择
    },
    fail: () => {
      // 使用地区选择器
      // @ts-ignore
      uni.showToast({ title: '请手动输入地区', icon: 'none' })
    }
  })
  
  // 模拟地区选择
  uni.showActionSheet({
    itemList: ['北京市', '上海市', '广东省深圳市', '广东省广州市', '浙江省杭州市'],
    success: (res) => {
      const regions = [
        { province: '北京市', city: '北京市', district: '朝阳区' },
        { province: '上海市', city: '上海市', district: '浦东新区' },
        { province: '广东省', city: '深圳市', district: '南山区' },
        { province: '广东省', city: '广州市', district: '天河区' },
        { province: '浙江省', city: '杭州市', district: '西湖区' },
      ]
      const region = regions[res.tapIndex]
      form.province = region.province
      form.city = region.city
      form.district = region.district
    }
  })
}

async function saveAddress() {
  if (!form.name.trim()) {
    uni.showToast({ title: '请输入收货人', icon: 'none' })
    return
  }
  if (!form.phone || !/^1\d{10}$/.test(form.phone)) {
    uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
    return
  }
  if (!form.province || !form.city || !form.district) {
    uni.showToast({ title: '请选择所在地区', icon: 'none' })
    return
  }
  if (!form.detail.trim()) {
    uni.showToast({ title: '请输入详细地址', icon: 'none' })
    return
  }
  
  saving.value = true
  try {
    const data = {
      name: form.name,
      phone: form.phone,
      province: form.province,
      city: form.city,
      district: form.district,
      detail: form.detail,
      is_default: form.is_default ? 1 : 0
    }
    
    let res
    if (isEdit.value) {
      res = await updateAddress(editId.value, data)
    } else {
      res = await apiAddAddress(data)
    }
    
    if (res.code === 200) {
      uni.showToast({ title: '保存成功', icon: 'success' })
      showForm.value = false
      fetchList()
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '保存失败', icon: 'none' })
  } finally {
    saving.value = false
  }
}

async function deleteAddress(item: Address) {
  uni.showModal({
    title: '提示',
    content: '确定删除该地址吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          const result = await apiDeleteAddress(item.id)
          if (result.code === 200) {
            uni.showToast({ title: '已删除', icon: 'success' })
            fetchList()
          }
        } catch (e: any) {
          uni.showToast({ title: e.message || '删除失败', icon: 'none' })
        }
      }
    }
  })
}

async function setDefault(item: Address) {
  try {
    const res = await setDefaultAddress(item.id)
    if (res.code === 200) {
      uni.showToast({ title: '设置成功', icon: 'success' })
      fetchList()
    }
  } catch (e: any) {
    uni.showToast({ title: e.message || '设置失败', icon: 'none' })
  }
}

function selectAddress(item: Address) {
  if (selectMode.value) {
    // 返回选中的地址
    const pages = getCurrentPages()
    const prevPage = pages[pages.length - 2] as any
    if (prevPage && prevPage.$vm) {
      prevPage.$vm.selectedAddress = item
    }
    uni.navigateBack()
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding: 16px;
  padding-bottom: 100px;
}

.address-item {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  
  .info {
    flex: 1;
    
    .user-row {
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      
      .name {
        font-size: 16px;
        font-weight: 600;
        color: #1D1D1F;
        margin-right: 12px;
      }
      
      .phone {
        font-size: 14px;
        color: #86868B;
        margin-right: 8px;
      }
      
      .tag {
        background: #0071e3;
        color: #FFFFFF;
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 4px;
      }
    }
    
    .detail {
      font-size: 14px;
      color: #1D1D1F;
      line-height: 1.4;
    }
  }
  
  .actions {
    display: flex;
    gap: 8px;
    
    .action-btn {
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}

.empty {
  padding: 80px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .text {
    font-size: 16px;
    color: #1D1D1F;
    margin-top: 16px;
  }
  
  .sub {
    font-size: 13px;
    color: #86868B;
    margin-top: 8px;
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
  
  .add-btn {
    width: 100%;
    height: 48px;
    background: #0071e3;
    border-radius: 24px;
    border: none;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    
    &::after {
      border: none;
    }
  }
}

.form-panel {
  padding: 24px;
  padding-bottom: 40px;
  
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    .title {
      font-size: 18px;
      font-weight: 700;
      color: #1D1D1F;
    }
    
    .close-btn {
      padding: 8px;
    }
  }
  
  .form-content {
    .form-item {
      margin-bottom: 20px;
      
      .label {
        font-size: 14px;
        color: #86868B;
        margin-bottom: 8px;
        display: block;
      }
      
      input {
        width: 100%;
        height: 44px;
        background: #F5F5F7;
        border-radius: 12px;
        padding: 0 16px;
        font-size: 15px;
      }
      
      .region-value {
        height: 44px;
        background: #F5F5F7;
        border-radius: 12px;
        padding: 0 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        
        text {
          font-size: 15px;
          color: #1D1D1F;
        }
        
        .placeholder {
          color: #C7C7CC;
        }
      }
      
      &.switch-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        
        .label {
          margin-bottom: 0;
        }
      }
    }
  }
  
  .form-footer {
    margin-top: 24px;
    
    .save-btn {
      width: 100%;
      height: 48px;
      background: #0071e3;
      border-radius: 24px;
      border: none;
      color: #FFFFFF;
      font-size: 16px;
      font-weight: 600;
      
      &::after {
        border: none;
      }
    }
  }
}
</style>
