/**
 * 用户管理接口
 */
import request from './request'

/**
 * 获取用户列表
 */
export function getUserList(params?: {
  page?: number
  page_size?: number
  keyword?: string
  status?: number
  member_type?: string
}) {
  return request.get('/user/list', params)
}

/**
 * 获取用户详情
 */
export function getUserDetail(id: number) {
  return request.get(`/user/${id}`)
}

/**
 * 更新用户状态
 */
export function updateUserStatus(id: number, data: { status: number; reason?: string }) {
  return request.put(`/user/${id}/status`, data)
}

