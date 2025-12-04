/**
 * 认证相关接口
 */
import request from './request'

/**
 * 管理员登录
 */
export function login(data: { username: string; password: string }) {
  return request.post('/auth/login', data)
}

/**
 * 退出登录
 */
export function logout() {
  return request.post('/auth/logout')
}

/**
 * 获取当前管理员信息
 */
export function getAdminInfo() {
  return request.get('/auth/info')
}


















