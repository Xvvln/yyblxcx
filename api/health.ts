/**
 * 健康筛查相关接口
 */
import request from '@/utils/request'

/**
 * 提交筛查数据
 */
export function submitScreening(data: {
  height?: number
  weight?: number
  heart_rate?: number
  blood_pressure_high?: number
  blood_pressure_low?: number
  body_temperature?: number
  blood_sugar?: number
  face_image?: string
  body_image?: string
  questionnaire_data?: any
}) {
  return request.post('/health/screening', data)
}

/**
 * 获取筛查记录列表
 */
export function getScreeningRecords(params?: { page?: number; page_size?: number }) {
  return request.get('/health/records', params)
}

/**
 * 获取报告详情
 */
export function getScreeningReport(id: number) {
  return request.get(`/health/report/${id}`)
}

/**
 * 获取健康数据趋势
 */
export function getHealthTrend(days: number = 30) {
  return request.get('/stats/health', { days })
}























