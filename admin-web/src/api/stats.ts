/**
 * 统计数据接口
 */
import request from './request'

/**
 * 获取数据概览
 */
export function getOverview() {
  return request.get('/stats/overview')
}

/**
 * 获取用户统计
 */
export function getUserStats(days: number = 7) {
  return request.get('/stats/user', { days })
}

/**
 * 获取订单统计
 */
export function getOrderStats(days: number = 7) {
  return request.get('/stats/order', { days })
}

/**
 * 获取健康数据统计
 */
export function getHealthStats(days: number = 7) {
  return request.get('/stats/health', { days })
}














