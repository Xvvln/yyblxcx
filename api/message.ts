/**
 * 消息相关接口
 */
import request from '@/utils/request'

/**
 * 获取会话列表
 */
export function getConversations() {
  return request.get('/message/conversations')
}

/**
 * 获取聊天记录
 */
export function getChatHistory(userId: number, params?: { page?: number; page_size?: number }) {
  return request.get(`/message/history/${userId}`, params)
}

/**
 * 发送消息
 */
export function sendMessage(data: {
  receiver_id: number
  content: string
  type?: string
}) {
  return request.post('/message/send', data)
}

/**
 * 标记已读
 */
export function markAsRead(conversationId: number) {
  return request.post(`/message/read/${conversationId}`)
}

/**
 * 获取通知列表
 */
export function getNotifications(params?: {
  page?: number
  page_size?: number
  type?: string
  is_read?: number
}) {
  return request.get('/notification/list', params)
}

/**
 * 标记通知已读
 */
export function markNotificationRead(ids: number[]) {
  return request.post('/notification/read', { ids })
}

/**
 * 全部标记已读
 */
export function markAllNotificationRead() {
  return request.post('/notification/read-all')
}

/**
 * 获取未读数量
 */
export function getUnreadCount() {
  return request.get('/notification/unread-count')
}

/**
 * 删除通知
 */
export function deleteNotification(id: number) {
  return request.delete(`/notification/${id}`)
}

