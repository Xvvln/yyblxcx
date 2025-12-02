/**
 * 应用全局状态
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 适老化模式（默认关闭）
  const elderlyMode = ref<boolean>(false)
  
  // 系统信息
  const systemInfo = ref<UniApp.GetSystemInfoResult | null>(null)
  
  // 设置适老化模式
  function setElderlyMode(value: boolean) {
    elderlyMode.value = value
    uni.setStorageSync('elderlyMode', value)
  }
  
  // 初始化
  function init() {
    // 读取适老化设置
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
    init
  }
})








