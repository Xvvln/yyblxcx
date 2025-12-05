/**
 * 内容审核接口
 */
import request from './request'

/**
 * 获取待审核动态列表
 */
export function getPendingPosts(params?: {
  page?: number
  page_size?: number
  status?: number
}) {
  return request.get('/audit/posts', params)
}

/**
 * 审核动态
 */
export function auditPost(id: number, data: { status: number; reason?: string }) {
  return request.put(`/audit/post/${id}`, data)
}

/**
 * 获取待审核评论列表
 */
export function getPendingComments(params?: {
  page?: number
  page_size?: number
  status?: number
}) {
  return request.get('/audit/comments', params)
}

/**
 * 审核评论
 */
export function auditComment(id: number, data: { status: number; reason?: string }) {
  return request.put(`/audit/comment/${id}`, data)
}























