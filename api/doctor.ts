/**
 * 远程医疗相关接口
 */
import request from '@/utils/request'

/**
 * 获取医生列表
 */
export function getDoctorList(params?: {
  page?: number
  page_size?: number
  department?: string
}) {
  return request.get('/doctor/list', params)
}

/**
 * 获取医生详情
 */
export function getDoctorDetail(id: number) {
  return request.get(`/doctor/${id}`)
}

/**
 * 获取科普文章列表
 */
export function getArticleList(params?: {
  page?: number
  page_size?: number
  category?: string
}) {
  return request.get('/article/list', params)
}

/**
 * 获取文章详情
 */
export function getArticleDetail(id: number) {
  return request.get(`/article/${id}`)
}























