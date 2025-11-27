<template>
  <view class="page">
    <view class="header">
      <text class="title">智能提醒</text>
      <text class="subtitle">保持健康的生活规律</text>
    </view>
    
    <view class="list" v-if="list.length > 0">
      <view class="item" v-for="item in list" :key="item.id" @click="editReminder(item)">
        <view class="info">
          <text class="time">{{ item.time }}</text>
          <view class="row">
            <text class="name">{{ item.name }}</text>
            <view class="days">
              <text v-for="d in item.repeat_days" :key="d">{{ dayName(d) }}</text>
            </view>
          </view>
        </view>
        <view class="actions">
          <wd-switch v-model="item.enabled" size="24px" active-color="#0071e3" @change="toggleReminder(item)" @click.stop />
          <view class="delete-btn" @click.stop="deleteReminder(item)">
            <wd-icon name="delete" size="18px" color="#FF3B30"></wd-icon>
          </view>
        </view>
      </view>
    </view>
    
    <view class="empty" v-else>
      <wd-icon name="bell" size="60px" color="#E5E5EA"></wd-icon>
      <text>暂无提醒</text>
      <text class="sub">添加提醒，养成健康好习惯</text>
    </view>
    
    <view class="footer">
      <button class="add-btn" @click="showAddModal = true">
        <wd-icon name="add" size="18px" color="#FFFFFF"></wd-icon>
        <text>添加提醒</text>
      </button>
    </view>
    
    <!-- 添加/编辑提醒弹窗 -->
    <wd-popup v-model="showAddModal" position="bottom" custom-style="border-radius: 20px 20px 0 0;">
      <view class="form-panel">
        <view class="panel-header">
          <text class="title">{{ isEdit ? '编辑提醒' : '添加提醒' }}</text>
          <view class="close-btn" @click="closeModal">
            <wd-icon name="close" size="20px" color="#86868B"></wd-icon>
          </view>
        </view>
        
        <view class="form-content">
          <view class="form-item">
            <text class="label">提醒名称</text>
            <input v-model="form.name" placeholder="如：喝水提醒" maxlength="20" />
          </view>
          
          <view class="form-item">
            <text class="label">提醒时间</text>
            <picker mode="time" :value="form.time" @change="onTimeChange">
              <view class="picker-value">
                <text>{{ form.time || '请选择时间' }}</text>
                <wd-icon name="arrow-right" size="16px" color="#C7C7CC"></wd-icon>
              </view>
            </picker>
          </view>
          
          <view class="form-item">
            <text class="label">重复</text>
            <view class="days-picker">
              <view 
                class="day-item" 
                v-for="(day, idx) in weekDays" 
                :key="idx"
                :class="{ active: form.repeat_days.includes(idx) }"
                @click="toggleDay(idx)"
              >{{ day }}</view>
            </view>
          </view>
          
          <view class="form-item">
            <text class="label">提醒方式</text>
            <view class="remind-types">
              <view 
                class="type-item" 
                :class="{ active: form.remind_type === 'vibrate' }"
                @click="form.remind_type = 'vibrate'"
              >
                <wd-icon name="phone" size="20px" :color="form.remind_type === 'vibrate' ? '#0071e3' : '#86868B'"></wd-icon>
                <text>震动</text>
              </view>
              <view 
                class="type-item" 
                :class="{ active: form.remind_type === 'sound' }"
                @click="form.remind_type = 'sound'"
              >
                <wd-icon name="bell" size="20px" :color="form.remind_type === 'sound' ? '#0071e3' : '#86868B'"></wd-icon>
                <text>铃声</text>
              </view>
              <view 
                class="type-item" 
                :class="{ active: form.remind_type === 'both' }"
                @click="form.remind_type = 'both'"
              >
                <wd-icon name="notification" size="20px" :color="form.remind_type === 'both' ? '#0071e3' : '#86868B'"></wd-icon>
                <text>震动+铃声</text>
              </view>
            </view>
          </view>
        </view>
        
        <view class="form-footer">
          <button class="save-btn" @click="saveReminder" :loading="saving">保存</button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

interface Reminder {
  id: number
  name: string
  time: string
  repeat_days: number[]
  remind_type: string
  enabled: boolean
}

const list = ref<Reminder[]>([])
const showAddModal = ref(false)
const isEdit = ref(false)
const editId = ref(0)
const saving = ref(false)

const weekDays = ['日', '一', '二', '三', '四', '五', '六']

const form = reactive({
  name: '',
  time: '08:00',
  repeat_days: [1, 2, 3, 4, 5] as number[],
  remind_type: 'vibrate'
})

onMounted(() => {
  loadReminders()
})

function loadReminders() {
  // 从本地存储加载
  const saved = uni.getStorageSync('reminders')
  if (saved) {
    list.value = JSON.parse(saved)
  } else {
    // 默认提醒
    list.value = [
      { id: 1, name: '喝水提醒', time: '09:00', repeat_days: [0,1,2,3,4,5,6], remind_type: 'vibrate', enabled: true },
      { id: 2, name: '午餐打卡', time: '12:00', repeat_days: [1,2,3,4,5], remind_type: 'both', enabled: true },
      { id: 3, name: '运动提醒', time: '20:00', repeat_days: [1,3,5], remind_type: 'sound', enabled: false }
    ]
    saveToStorage()
  }
}

function saveToStorage() {
  uni.setStorageSync('reminders', JSON.stringify(list.value))
}

function dayName(idx: number) {
  if (idx === 0) return '日'
  if (idx === 6) return '六'
  return ['一', '二', '三', '四', '五'][idx - 1]
}

function toggleDay(idx: number) {
  const index = form.repeat_days.indexOf(idx)
  if (index > -1) {
    form.repeat_days.splice(index, 1)
  } else {
    form.repeat_days.push(idx)
  }
}

function onTimeChange(e: any) {
  form.time = e.detail.value
}

function resetForm() {
  form.name = ''
  form.time = '08:00'
  form.repeat_days = [1, 2, 3, 4, 5]
  form.remind_type = 'vibrate'
}

function editReminder(item: Reminder) {
  isEdit.value = true
  editId.value = item.id
  form.name = item.name
  form.time = item.time
  form.repeat_days = [...item.repeat_days]
  form.remind_type = item.remind_type
  showAddModal.value = true
}

function closeModal() {
  showAddModal.value = false
  isEdit.value = false
  editId.value = 0
  resetForm()
}

function saveReminder() {
  if (!form.name.trim()) {
    uni.showToast({ title: '请输入提醒名称', icon: 'none' })
    return
  }
  if (!form.time) {
    uni.showToast({ title: '请选择提醒时间', icon: 'none' })
    return
  }
  if (form.repeat_days.length === 0) {
    uni.showToast({ title: '请选择重复日期', icon: 'none' })
    return
  }
  
  saving.value = true
  
  setTimeout(() => {
    if (isEdit.value) {
      // 编辑
      const idx = list.value.findIndex(r => r.id === editId.value)
      if (idx > -1) {
        list.value[idx] = {
          ...list.value[idx],
          name: form.name,
          time: form.time,
          repeat_days: [...form.repeat_days],
          remind_type: form.remind_type
        }
      }
    } else {
      // 新增
      list.value.push({
        id: Date.now(),
        name: form.name,
        time: form.time,
        repeat_days: [...form.repeat_days],
        remind_type: form.remind_type,
        enabled: true
      })
    }
    
    saveToStorage()
    saving.value = false
    closeModal()
    uni.showToast({ title: '保存成功', icon: 'success' })
  }, 500)
}

function toggleReminder(item: Reminder) {
  saveToStorage()
  uni.showToast({ 
    title: item.enabled ? '提醒已开启' : '提醒已关闭', 
    icon: 'none' 
  })
}

function deleteReminder(item: Reminder) {
  uni.showModal({
    title: '删除提醒',
    content: `确定删除"${item.name}"吗？`,
    success: (res) => {
      if (res.confirm) {
        const idx = list.value.findIndex(r => r.id === item.id)
        if (idx > -1) {
          list.value.splice(idx, 1)
          saveToStorage()
          uni.showToast({ title: '已删除', icon: 'success' })
        }
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #F5F5F7;
  padding: 16px;
  padding-bottom: 100px;
}

.header {
  margin-bottom: 20px;
  
  .title {
    font-size: 28px;
    font-weight: 700;
    color: #1D1D1F;
    display: block;
  }
  
  .subtitle {
    font-size: 14px;
    color: #86868B;
    margin-top: 4px;
  }
}

.list {
  .item {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    
    .info {
      flex: 1;
      
      .time {
        font-size: 32px;
        font-weight: 600;
        color: #1D1D1F;
        line-height: 1;
        margin-bottom: 8px;
        display: block;
      }
      
      .row {
        display: flex;
        align-items: center;
        gap: 12px;
        
        .name {
          font-size: 15px;
          color: #1D1D1F;
        }
        
        .days {
          display: flex;
          gap: 6px;
          
          text {
            font-size: 12px;
            color: #86868B;
            background: #F5F5F7;
            padding: 2px 6px;
            border-radius: 4px;
          }
        }
      }
    }
    
    .actions {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .delete-btn {
        padding: 8px;
      }
    }
  }
}

.empty {
  padding: 80px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  
  text {
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
  }
  
  .form-content {
    .form-item {
      margin-bottom: 24px;
      
      .label {
        font-size: 14px;
        color: #86868B;
        margin-bottom: 10px;
        display: block;
      }
      
      input {
        width: 100%;
        height: 48px;
        background: #F5F5F7;
        border-radius: 12px;
        padding: 0 16px;
        font-size: 15px;
      }
      
      .picker-value {
        height: 48px;
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
      }
      
      .days-picker {
        display: flex;
        gap: 8px;
        
        .day-item {
          width: 40px;
          height: 40px;
          background: #F5F5F7;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 14px;
          color: #1D1D1F;
          
          &.active {
            background: #0071e3;
            color: #FFFFFF;
          }
        }
      }
      
      .remind-types {
        display: flex;
        gap: 12px;
        
        .type-item {
          flex: 1;
          padding: 12px;
          background: #F5F5F7;
          border-radius: 12px;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 6px;
          
          text {
            font-size: 12px;
            color: #86868B;
          }
          
          &.active {
            background: #E8F4FD;
            border: 1px solid #0071e3;
            
            text {
              color: #0071e3;
            }
          }
        }
      }
    }
  }
  
  .form-footer {
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
