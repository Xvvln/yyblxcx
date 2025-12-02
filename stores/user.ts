/**
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { wxLogin, devLogin as apiDevLogin, register } from '@/api/auth'
import { getUserProfile } from '@/api/user'

export interface UserInfo {
  id: number
  nickname: string
  avatar: string
  phone?: string
  gender?: number
  birthday?: string
  height?: number
  weight?: number
  sport_coins: number
  food_coins: number
  user_level?: number
  member_type?: string
  member_expire_time?: string
  continuous_checkin_days?: number
  total_checkin_days?: number
  follower_count?: number
  following_count?: number
}

export const useUserStore = defineStore('user', () => {
  // state
  const userInfo = ref<UserInfo | null>(null)
  const token = ref<string>(uni.getStorageSync('token') || '')
  
  // getters
  const isLoggedIn = computed(() => !!token.value)
  const nickname = computed(() => userInfo.value?.nickname || '游客')
  const avatar = computed(() => userInfo.value?.avatar || '/static/placeholder/avatar.png')
  const sportCoins = computed(() => userInfo.value?.sport_coins || 0)
  const foodCoins = computed(() => userInfo.value?.food_coins || 0)
  const totalCoins = computed(() => sportCoins.value + foodCoins.value)
  const isVip = computed(() => {
    if (!userInfo.value?.member_expire_time) return false
    return new Date(userInfo.value.member_expire_time).getTime() > Date.now()
  })
  const userLevel = computed(() => userInfo.value?.user_level || 1)
  
  // actions
  function setToken(newToken: string) {
    token.value = newToken
    uni.setStorageSync('token', newToken)
  }
  
  function setUserInfo(info: UserInfo) {
    userInfo.value = info
  }
  
  /**
   * 微信登录
   */
  async function login(code: string) {
    try {
      const res = await wxLogin(code)
      if (res.code === 200) {
        setToken(res.data.token)
        if (res.data.user) {
          setUserInfo(res.data.user)
        }
        return res.data
      }
      throw new Error(res.message)
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }
  
  /**
   * 开发环境登录（无需微信）
   */
  async function devLogin(openid?: string) {
    try {
      const res = await apiDevLogin(openid)
      if (res.code === 200) {
        setToken(res.data.token)
        // 设置基础用户信息
        setUserInfo({
          id: res.data.user_id,
          nickname: res.data.nickname || '测试用户',
          avatar: res.data.avatar || '',
          sport_coins: 0,
          food_coins: 0
        })
        return res.data
      }
      throw new Error(res.message)
    } catch (error) {
      console.error('Dev login failed:', error)
      throw error
    }
  }
  
  /**
   * 完善用户信息（注册）
   */
  async function completeProfile(data: {
    nickname: string
    avatar?: string
    gender?: number
    birthday?: string
    height?: number
    weight?: number
  }) {
    try {
      const res = await register(data)
      if (res.code === 200 && res.data) {
        setUserInfo(res.data)
        return res.data
      }
      throw new Error(res.message)
    } catch (error) {
      console.error('Register failed:', error)
      throw error
    }
  }
  
  /**
   * 获取用户信息
   */
  async function fetchUserInfo() {
    try {
      const res = await getUserProfile()
      if (res.code === 200 && res.data) {
        setUserInfo(res.data)
        return res.data
      }
    } catch (error) {
      console.error('Fetch user info failed:', error)
    }
  }
  
  /**
   * 退出登录
   */
  function logout() {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync('token')
  }
  
  /**
   * 检查登录状态
   */
  async function checkLoginStatus() {
    if (token.value) {
      await fetchUserInfo()
    }
  }
  
  return {
    userInfo,
    token,
    isLoggedIn,
    nickname,
    avatar,
    sportCoins,
    foodCoins,
    totalCoins,
    isVip,
    userLevel,
    setToken,
    setUserInfo,
    login,
    devLogin,
    completeProfile,
    fetchUserInfo,
    logout,
    checkLoginStatus
  }
})
