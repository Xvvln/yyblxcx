/**
 * 饮食相关接口
 */
import request from '@/utils/request'

/**
 * 提交饮食记录
 */
export function submitFoodRecord(data: {
  meal_type: 'breakfast' | 'lunch' | 'dinner' | 'snack'
  record_date: string
  food_name: string
  food_image?: string
  amount?: number
  calories?: number
  protein?: number
  carbs?: number
  fat?: number
  fiber?: number
  notes?: string
}) {
  return request.post('/food/record', data)
}

/**
 * 获取饮食记录列表
 */
export function getFoodRecords(params?: {
  page?: number
  page_size?: number
  record_date?: string
  meal_type?: string
}) {
  return request.get('/food/records', params)
}

/**
 * 饮食打卡
 */
export function foodCheckin() {
  return request.post('/food/checkin')
}

/**
 * 获取饮食统计
 */
export function getFoodStats(days: number = 30) {
  return request.get('/stats/food', { days })
}

/**
 * 搜索食物库
 */
export function searchFoodLibrary(params?: {
  keyword?: string
  category?: string
  page?: number
  page_size?: number
}) {
  return request.get('/food-library/search', params)
}

/**
 * 获取食物分类
 */
export function getFoodCategories() {
  return request.get('/food-library/categories')
}

/**
 * 获取食物详情
 */
export function getFoodDetail(id: number) {
  return request.get(`/food-library/${id}`)
}














