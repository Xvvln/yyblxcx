/**
 * 认证相关接口
 */
import request from '@/utils/request'

/**
 * 微信登录
 */
export function wxLogin(code: string) {
  return request.post('/auth/login', { code })
}

/**
 * 完善用户信息（注册）
 */
export function register(data: {
  nickname: string
  avatar?: string
  gender?: number
  birthday?: string
  height?: number
  weight?: number
}) {
  return request.post('/auth/register', data)
}

