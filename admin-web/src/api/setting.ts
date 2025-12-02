/**
 * 系统设置接口
 */
import request from './request'

/**
 * 获取积分配置
 */
export function getPointsConfig() {
  return request.get('/setting/points')
}

/**
 * 更新积分配置
 */
export function updatePointsConfig(data: any) {
  return request.put('/setting/points', data)
}

/**
 * 获取会员配置
 */
export function getMemberConfig() {
  return request.get('/setting/member')
}

/**
 * 更新会员配置
 */
export function updateMemberConfig(data: any) {
  return request.put('/setting/member', data)
}














