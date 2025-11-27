/**
 * AI助手相关接口
 */
import request from '@/utils/request'

/**
 * AI对话
 */
export function aiChat(data: {
  message: string
  session_id?: string
}) {
  return request.post('/ai/chat', data)
}

/**
 * AI对话（带上下文）
 */
export function chatWithAI(data: {
  message: string
  context?: { role: string; content: string }[]
}) {
  return request.post('/ai/chat', data)
}

/**
 * 获取AI对话历史
 */
export function getAiHistory(params?: {
  session_id?: string
  page?: number
  page_size?: number
}) {
  return request.get('/ai/history', params)
}

/**
 * 删除对话历史
 */
export function deleteAiHistory(sessionId: string) {
  return request.delete(`/ai/history/${sessionId}`)
}

