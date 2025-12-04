/**
 * 反馈管理接口
 */
import request from './request'

/**
 * 获取反馈列表
 */
export function getFeedbackList(params?: {
  page?: number
  page_size?: number
  keyword?: string
  status?: number
}) {
  return request.get('/feedback/list', params)
}

/**
 * 获取反馈详情
 */
export function getFeedbackDetail(id: number) {
  return request.get(`/feedback/${id}`)
}

/**
 * 更新反馈状态
 */
export function updateFeedbackStatus(id: number, data: { status: number }) {
  return request.put(`/feedback/${id}`, data)
}

/**
 * 回复反馈
 */
export function replyFeedback(id: number, data: { reply: string }) {
  return request.post(`/feedback/${id}/reply`, data)
}

/**
 * 删除反馈
 */
export function deleteFeedback(id: number) {
  return request.delete(`/feedback/${id}`)
}


