/**
 * 订单管理接口
 */
import request from './request'

/**
 * 获取订单列表
 */
export function getOrderList(params?: {
  page?: number
  page_size?: number
  order_no?: string
  status?: string
  start_date?: string
  end_date?: string
}) {
  return request.get('/order/list', params)
}

/**
 * 获取订单详情
 */
export function getOrderDetail(id: number) {
  return request.get(`/order/${id}`)
}

/**
 * 发货
 */
export function shipOrder(id: number, data: { tracking_company: string; tracking_no: string }) {
  return request.post(`/order/${id}/ship`, data)
}

/**
 * 退款
 */
export function refundOrder(id: number, data?: { refund_amount?: number; reason?: string }) {
  return request.post(`/order/${id}/refund`, data)
}














