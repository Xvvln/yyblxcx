/**
 * 商城相关接口
 */
import request from '@/utils/request'

/**
 * 获取商品分类
 */
export function getCategories() {
  return request.get('/shop/categories')
}

/**
 * 获取商品列表
 */
export function getProducts(params?: {
  page?: number
  page_size?: number
  category_id?: number
  keyword?: string
  sort?: string
}) {
  return request.get('/shop/products', params)
}

/**
 * 获取商品详情
 */
export function getProductDetail(id: number) {
  return request.get(`/shop/product/${id}`)
}

/**
 * 获取商品评价
 */
export function getProductReviews(id: number, params?: { page?: number; page_size?: number }) {
  return request.get(`/shop/product/${id}/reviews`, params)
}

// ========== 收藏 ==========

/**
 * 收藏商品
 */
export function collectProduct(id: number) {
  return request.post(`/shop/product/${id}/collect`)
}

/**
 * 取消收藏
 */
export function uncollectProduct(id: number) {
  return request.delete(`/shop/product/${id}/collect`)
}

/**
 * 获取收藏列表
 */
export function getCollectList(params?: { page?: number; page_size?: number }) {
  return request.get('/shop/collect', params)
}

// ========== 购物车 ==========

/**
 * 获取购物车列表
 */
export function getCartList() {
  return request.get('/cart')
}

/**
 * 添加到购物车
 */
export function addToCart(data: { product_id: number; quantity: number }) {
  return request.post('/cart', data)
}

/**
 * 更新购物车数量
 */
export function updateCartItem(id: number, data: { quantity?: number; is_selected?: number }) {
  return request.put(`/cart/${id}`, data)
}

/**
 * 删除购物车商品
 */
export function deleteCartItem(id: number) {
  return request.delete(`/cart/${id}`)
}

// ========== 订单 ==========

/**
 * 创建订单
 */
export function createOrder(data: {
  address_id: number
  items: Array<{ product_id: number; quantity: number }>
  coupon_id?: number
  remark?: string
}) {
  return request.post('/order', data)
}

/**
 * 获取订单列表
 */
export function getOrderList(params?: { page?: number; page_size?: number; status?: string }) {
  return request.get('/order/list', params)
}

/**
 * 获取订单详情
 */
export function getOrderDetail(id: number) {
  return request.get(`/order/${id}`)
}

/**
 * 支付订单
 */
export function payOrder(id: number, data?: { pay_method?: string }) {
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
 * 提交评价
 */
export function submitOrderReview(id: number, data: {
  items: Array<{
    product_id: number
    rating: number
    content?: string
    images?: string[]
  }>
}) {
  return request.post(`/order/${id}/review`, data)
}

// ========== 优惠券 ==========

/**
 * 获取可领取优惠券
 */
export function getAvailableCoupons() {
  return request.get('/coupon/available')
}

/**
 * 领取优惠券
 */
export function receiveCoupon(id: number) {
  return request.post(`/coupon/${id}/receive`)
}

/**
 * 我的优惠券
 */
export function getMyCoupons(params?: { status?: string }) {
  return request.get('/coupon/my-coupons', params)
}

