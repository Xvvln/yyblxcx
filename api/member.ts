/**
 * 会员相关接口
 */
import request from '@/utils/request'

/**
 * 获取会员信息
 */
export function getMemberInfo() {
  return request.get('/member/info')
}

/**
 * 获取会员套餐列表
 */
export function getMemberPlans() {
  return request.get('/member/plans')
}

/**
 * 购买会员
 */
export function purchaseMember(data: { plan_type: string; pay_type?: string }) {
  return request.post('/member/purchase', data)
}

/**
 * 获取会员购买记录
 */
export function getMemberOrders(params?: { page?: number; page_size?: number }) {
  return request.get('/member/orders', params)
}

