/**
 * 商品管理接口
 */
import request from './request'

/**
 * 获取商品列表
 */
export function getProductList(params?: {
  page?: number
  page_size?: number
  keyword?: string
  category_id?: number
  is_on_sale?: number
}) {
  return request.get('/product/list', params)
}

/**
 * 创建商品
 */
export function createProduct(data: {
  category_id: number
  name: string
  subtitle?: string
  images?: string[]
  description?: string
  original_price: number
  current_price: number
  member_price?: number
  stock?: number
  suitable_tags?: string[]
  health_tags?: string[]
  specs?: any[]
  is_recommend?: number
  is_on_sale?: number
  sort_order?: number
}) {
  return request.post('/product', data)
}

/**
 * 更新商品
 */
export function updateProduct(id: number, data: Partial<{
  category_id: number
  name: string
  subtitle: string
  images: string[]
  description: string
  original_price: number
  current_price: number
  member_price: number
  stock: number
  suitable_tags: string[]
  health_tags: string[]
  specs: any[]
  is_recommend: number
  is_on_sale: number
  sort_order: number
}>) {
  return request.put(`/product/${id}`, data)
}

/**
 * 删除商品
 */
export function deleteProduct(id: number) {
  return request.delete(`/product/${id}`)
}

// ========== 分类管理 ==========

/**
 * 获取分类列表
 */
export function getCategoryList() {
  return request.get('/category/list')
}

/**
 * 创建分类
 */
export function createCategory(data: {
  name: string
  parent_id?: number
  icon?: string
  sort_order?: number
  is_active?: number
}) {
  return request.post('/category', data)
}

/**
 * 更新分类
 */
export function updateCategory(id: number, data: Partial<{
  name: string
  parent_id: number
  icon: string
  sort_order: number
  is_active: number
}>) {
  return request.put(`/category/${id}`, data)
}

/**
 * 删除分类
 */
export function deleteCategory(id: number) {
  return request.delete(`/category/${id}`)
}























