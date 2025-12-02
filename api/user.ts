/**
 * 用户相关接口
 */
import request from '@/utils/request'

/**
 * 获取用户信息
 */
export function getUserProfile() {
  return request.get('/user/profile')
}

/**
 * 更新用户信息
 */
export function updateUserProfile(data: {
  nickname?: string
  avatar?: string
  gender?: number
  birthday?: string
  phone?: string
  height?: number
  weight?: number
}) {
  return request.put('/user/profile', data)
}

/**
 * 上传头像
 */
export function uploadAvatar(filePath: string) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token')
    uni.uploadFile({
      url: 'http://localhost:8000/api/v1/user/avatar',
      filePath,
      name: 'file',
      header: {
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(JSON.parse(res.data))
        } else {
          reject(res)
        }
      },
      fail: reject
    })
  })
}

/**
 * 获取健康档案
 */
export function getHealthProfile() {
  return request.get('/user/health-profile')
}

/**
 * 更新健康档案
 */
export function updateHealthProfile(data: {
  height?: number
  weight?: number
  blood_type?: string
  allergies?: string[]
  medical_history?: string[]
  health_goals?: string[]
}) {
  return request.put('/user/health-profile', data)
}

/**
 * 获取地址列表
 */
export async function getAddressList() {
  const res = await request.get('/address/list')
  // 转换后端字段名为前端期望的字段名
  if (res.code === 200 && res.data) {
    res.data.list = (res.data.list || res.data || []).map((item: any) => ({
      ...item,
      name: item.receiver_name || item.name,
      phone: item.receiver_phone || item.phone
    }))
  }
  return res
}

/**
 * 添加地址
 */
export function addAddress(data: {
  name: string
  phone: string
  province: string
  city: string
  district: string
  detail: string
  is_default?: number
}) {
  // 后端期望 receiver_name 和 receiver_phone
  return request.post('/address', {
    receiver_name: data.name,
    receiver_phone: data.phone,
    province: data.province,
    city: data.city,
    district: data.district,
    detail: data.detail,
    is_default: data.is_default || 0
  })
}

/**
 * 更新地址
 */
export function updateAddress(id: number, data: any) {
  // 后端期望 receiver_name 和 receiver_phone
  const mappedData: any = {}
  if (data.name !== undefined) mappedData.receiver_name = data.name
  if (data.phone !== undefined) mappedData.receiver_phone = data.phone
  if (data.province !== undefined) mappedData.province = data.province
  if (data.city !== undefined) mappedData.city = data.city
  if (data.district !== undefined) mappedData.district = data.district
  if (data.detail !== undefined) mappedData.detail = data.detail
  if (data.is_default !== undefined) mappedData.is_default = data.is_default
  
  return request.put(`/address/${id}`, mappedData)
}

/**
 * 删除地址
 */
export function deleteAddress(id: number) {
  return request.delete(`/address/${id}`)
}

/**
 * 设为默认地址
 */
export function setDefaultAddress(id: number) {
  return request.put(`/address/${id}/default`)
}

/**
 * 获取提醒列表
 */
export function getReminderList() {
  return request.get('/reminder/list')
}

/**
 * 添加提醒
 */
export function addReminder(data: {
  type: string
  time: string
  repeat_days?: number[]
  content?: string
}) {
  return request.post('/reminder', data)
}

/**
 * 更新提醒
 */
export function updateReminder(id: number, data: any) {
  return request.put(`/reminder/${id}`, data)
}

/**
 * 删除提醒
 */
export function deleteReminder(id: number) {
  return request.delete(`/reminder/${id}`)
}

