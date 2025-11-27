/**
 * 积分任务相关接口
 */
import request from '@/utils/request'

/**
 * 获取积分余额
 */
export function getPointsBalance() {
  return request.get('/points/balance')
}

/**
 * 获取积分记录
 */
export function getPointsRecords(params?: {
  page?: number
  page_size?: number
  coin_type?: string
}) {
  return request.get('/points/records', params)
}

/**
 * 获取可兑换礼品
 */
export function getPointsGifts(params?: { page?: number; page_size?: number }) {
  return request.get('/points/gifts', params)
}

/**
 * 兑换礼品
 */
export function exchangeGift(data: { gift_id: number; quantity?: number }) {
  return request.post('/points/exchange', data)
}

// ========== 每日任务 ==========

/**
 * 获取今日任务
 */
export function getDailyTasks() {
  return request.get('/task/daily')
}

/**
 * 获取任务进度
 */
export function getTaskProgress() {
  return request.get('/task/progress')
}

/**
 * 领取任务奖励
 */
export function claimTaskReward(taskId: number) {
  return request.post(`/task/${taskId}/claim`)
}

// ========== 签到 ==========

/**
 * 每日签到
 */
export function dailyCheckin() {
  return request.post('/checkin')
}

/**
 * 获取签到状态
 */
export function getCheckinStatus() {
  return request.get('/checkin/status')
}

/**
 * 获取签到日历
 */
export function getCheckinCalendar(params?: { year?: number; month?: number }) {
  return request.get('/checkin/calendar', params)
}

/**
 * 获取签到统计
 */
export function getCheckinStats() {
  return request.get('/checkin/stats')
}

