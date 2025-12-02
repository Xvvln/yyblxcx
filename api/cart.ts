/**
 * 购物车相关接口
 */
import request from '@/utils/request'

/**
 * 获取购物车列表
 */
export function getCartList() {
  return request.get('/cart')
}

/**
 * 获取购物车数量
 */
export function getCartCount() {
  return request.get('/cart/count')
}

/**
 * 添加商品到购物车
 */
export function addToCart(data: {
  product_id: number
  sku_id?: number | string
  quantity: number
}) {
  // 后端期望 spec_id
  return request.post('/cart', {
    product_id: data.product_id,
    spec_id: data.sku_id || null,
    quantity: data.quantity
  })
}

/**
 * 更新购物车商品
 */
export function updateCartItem(id: number, data: {
  quantity?: number
  selected?: number
}) {
  return request.put(`/cart/${id}`, data)
}

/**
 * 删除购物车商品
 */
export function deleteCartItem(id: number) {
  return request.delete(`/cart/${id}`)
}

/**
 * 清空购物车
 */
export function clearCart() {
  return request.delete('/cart/clear')
}

/**
 * 选中/取消选中全部
 */
export function selectAllCart(selected: boolean) {
  return request.post('/cart/select-all', { selected: selected ? 1 : 0 })
}

