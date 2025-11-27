/**
 * 订单相关接口
 */
import request from '@/utils/request'

/**
 * 获取订单列表
 */
export function getOrderList(params?: {
  page?: number
  page_size?: number
  status?: number
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
 * 创建订单
 */
export function createOrder(data: {
  address_id: number
  items: Array<{
    product_id: number
    sku_id?: number
    quantity: number
  }>
  coupon_id?: number
  remark?: string
  from_cart?: boolean
}) {
  return request.post('/order', data)
}

/**
 * 支付订单
 */
export function payOrder(id: number, data?: { pay_type?: string }) {
  return request.post(`/order/${id}/pay`, data)
}

/**
 * 取消订单
 */
export function cancelOrder(id: number, data?: { reason?: string }) {
  return request.post(`/order/${id}/cancel`, data)
}

/**
 * 确认收货
 */
export function confirmOrder(id: number) {
  return request.post(`/order/${id}/confirm`)
}

/**
 * 申请退款
 */
export function refundOrder(id: number, data: {
  reason: string
  description?: string
  images?: string[]
}) {
  return request.post(`/order/${id}/refund`, data)
}

/**
 * 获取物流信息
 */
export function getOrderLogistics(id: number) {
  return request.get(`/order/${id}/logistics`)
}

