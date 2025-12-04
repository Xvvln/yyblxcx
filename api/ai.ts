/**
 * AI健康助手相关接口
 * 
 * 功能：
 * - AI对话（支持上下文记忆）
 * - 会话管理
 * - 对话历史
 */
import request from '@/utils/request'

/**
 * AI对话
 * @param data.message 用户消息
 * @param data.session_id 会话ID（可选，不传则创建新会话）
 */
export function aiChat(data: {
  message: string
  session_id?: string
}) {
  // 禁用全局loading，AI页面有自己的加载状态
  return request.post('/ai/chat', data, { loading: false })
}

/**
 * AI对话（带上下文 - 兼容旧接口）
 */
export function chatWithAI(data: {
  message: string
  context?: { role: string; content: string }[]
  session_id?: string
}) {
  // 禁用全局loading，AI页面有自己的加载状态
  return request.post('/ai/chat', {
    message: data.message,
    session_id: data.session_id
  }, { loading: false })
}

/**
 * 创建新会话
 * @returns 新的会话ID
 */
export function createNewSession() {
  return request.post('/ai/new-session', {}, { loading: false })
}

/**
 * 获取会话列表
 */
export function getAiSessions(params?: {
  page?: number
  page_size?: number
}) {
  // 禁用全局loading和错误提示，弹窗有自己的加载状态
  return request.get('/ai/sessions', params, { loading: false, showError: false })
}

/**
 * 获取AI对话历史
 * @param params.session_id 会话ID（可选，不传则返回会话列表）
 */
export function getAiHistory(params?: {
  session_id?: string
  page?: number
  page_size?: number
}) {
  // 禁用全局loading和错误提示
  return request.get('/ai/history', params, { loading: false, showError: false })
}

/**
 * 删除指定会话
 */
export function deleteAiHistory(sessionId: string) {
  return request.delete(`/ai/history/${sessionId}`, {}, { loading: false })
}

/**
 * 清空所有对话历史
 */
export function clearAllAiHistory() {
  return request.delete('/ai/history', {}, { loading: false })
}
