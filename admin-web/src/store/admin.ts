/**
 * 管理员状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, logout as apiLogout, getAdminInfo } from '@/api/auth'
import router from '@/router'

export interface AdminInfo {
  id: number
  username: string
  nickname: string
  avatar: string | null
  role: string
  last_login_at: string | null
}

export const useAdminStore = defineStore('admin', () => {
  // state
  const adminInfo = ref<AdminInfo | null>(null)
  const token = ref<string>(localStorage.getItem('admin_token') || '')

  // getters
  const isLoggedIn = computed(() => !!token.value)
  const nickname = computed(() => adminInfo.value?.nickname || adminInfo.value?.username || '管理员')

  // actions
  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('admin_token', newToken)
  }

  function setAdminInfo(info: AdminInfo) {
    adminInfo.value = info
  }

  async function login(username: string, password: string) {
    try {
      const res = await apiLogin({ username, password })
      if (res.code === 200 && res.data) {
        setToken(res.data.token)
        setAdminInfo({
          id: res.data.admin_id,
          username: res.data.username,
          nickname: res.data.nickname,
          avatar: res.data.avatar,
          role: res.data.role,
          last_login_at: null,
        })
        return res.data
      }
      throw new Error(res.message)
    } catch (error) {
      throw error
    }
  }

  async function fetchAdminInfo() {
    try {
      const res = await getAdminInfo()
      if (res.code === 200 && res.data) {
        setAdminInfo(res.data)
        return res.data
      }
    } catch (error) {
      console.error('获取管理员信息失败:', error)
    }
  }

  async function logout() {
    try {
      await apiLogout()
    } catch (error) {
      // 即使接口失败也清除本地状态
    }
    token.value = ''
    adminInfo.value = null
    localStorage.removeItem('admin_token')
    router.push('/login')
  }

  return {
    adminInfo,
    token,
    isLoggedIn,
    nickname,
    setToken,
    setAdminInfo,
    login,
    fetchAdminInfo,
    logout,
  }
})

