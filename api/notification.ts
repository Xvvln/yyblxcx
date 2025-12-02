/**
 * 通知消息相关接口
 */
import request from '@/utils/request'

/**
 * 获取通知列表
 */
export function getNotifications(params?: {
  page?: number
  page_size?: number
  type?: string
}) {
  return request.get('/notification/list', params)
}

/**
 * 获取未读消息数量
 */
export function getUnreadCount() {
  return request.get('/notification/unread-count')
}

/**
 * 标记消息为已读
 */
export function markAsRead(id: number) {
  return request.post(`/notification/${id}/read`)
}

/**
 * 标记全部已读
 */
export function markAllAsRead() {
  return request.post('/notification/read-all')
}

/**
 * 删除通知
 */
export function deleteNotification(id: number) {
  return request.delete(`/notification/${id}`)
}














