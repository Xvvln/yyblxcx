/**
 * 运动相关接口
 */
import request from '@/utils/request'

/**
 * 提交运动记录
 */
export function submitSportRecord(data: {
  sport_type: string
  sport_name?: string
  duration: number
  distance?: number
  avg_pace?: number
  avg_heart_rate?: number
  max_heart_rate?: number
  weather?: string
  feeling?: number
  notes?: string
  start_time: string
  end_time: string
  gps_track?: any
}) {
  return request.post('/sport/record', data)
}

/**
 * 获取运动记录列表
 */
export function getSportRecords(params?: { 
  page?: number
  page_size?: number
  sport_type?: string 
}) {
  return request.get('/sport/records', params)
}

/**
 * 运动打卡
 */
export function sportCheckin() {
  return request.post('/sport/checkin')
}

/**
 * 获取运动统计
 */
export function getSportStats(days: number = 30) {
  return request.get('/stats/sport', { days })
}

/**
 * 获取运动目标列表
 */
export function getSportGoals(params?: { period?: string; is_active?: number }) {
  return request.get('/sport-goal/list', params)
}

/**
 * 创建运动目标
 */
export function createSportGoal(data: {
  goal_type: string
  target_value: number
  unit: string
  period?: string
}) {
  return request.post('/sport-goal', data)
}

/**
 * 更新运动目标
 */
export function updateSportGoal(id: number, data: { target_value?: number }) {
  return request.put(`/sport-goal/${id}`, data)
}

/**
 * 删除运动目标
 */
export function deleteSportGoal(id: number) {
  return request.delete(`/sport-goal/${id}`)
}

/**
 * 获取课程列表
 */
export function getCourseList(params?: {
  page?: number
  page_size?: number
  sport_type?: string
  difficulty?: string
}) {
  return request.get('/course/list', params)
}

/**
 * 获取课程详情
 */
export function getCourseDetail(id: number) {
  return request.get(`/course/${id}`)
}

/**
 * 收藏课程
 */
export function collectCourse(id: number) {
  return request.post(`/course/${id}/collect`)
}

/**
 * 取消收藏课程
 */
export function uncollectCourse(id: number) {
  return request.delete(`/course/${id}/collect`)
}

/**
 * 我的课程收藏
 */
export function getMyCourseCollects(params?: { page?: number; page_size?: number }) {
  return request.get('/course/my-collects', params)
}














