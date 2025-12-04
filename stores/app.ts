/**
 * 应用全局状态
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getUserSettings, updateUserSettings } from '@/api/user'

export const useAppStore = defineStore('app', () => {
  // 适老化模式（默认关闭）
  const elderlyMode = ref<boolean>(false)
  
  // 系统信息
  const systemInfo = ref<UniApp.GetSystemInfoResult | null>(null)
  
  // 设置适老化模式
  async function setElderlyMode(value: boolean) {
    elderlyMode.value = value
    uni.setStorageSync('elderlyMode', value)
    
    // 同步到服务器
    try {
      await updateUserSettings({ elderly_mode: value ? 1 : 0 })
    } catch (e) {
      console.error('同步长辈模式设置失败', e)
    }
  }
  
  // 从服务器加载设置
  async function loadSettings() {
    try {
      const res = await getUserSettings()
      if (res.code === 200 && res.data) {
        elderlyMode.value = res.data.elderly_mode === 1
        uni.setStorageSync('elderlyMode', elderlyMode.value)
      }
    } catch (e) {
      // 如果服务器获取失败，使用本地缓存
      elderlyMode.value = uni.getStorageSync('elderlyMode') || false
    }
  }
  
  // 初始化
  function init() {
    // 先读取本地缓存
    elderlyMode.value = uni.getStorageSync('elderlyMode') || false
    
    // 获取系统信息
    uni.getSystemInfo({
      success: (res) => {
        systemInfo.value = res
      }
    })
  }
  
  return {
    elderlyMode,
    systemInfo,
    setElderlyMode,
    loadSettings,
    init
  }
})
