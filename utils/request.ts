/**
 * 请求封装
 * 统一处理接口请求、错误处理、loading 等
 */

// 基础配置
const BASE_URL = 'http://localhost:8000/api/v1'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: any
  loading?: boolean
  showError?: boolean
}

interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

const request = async <T = any>(options: RequestOptions): Promise<ApiResponse<T>> => {
  // 显示 loading
  if (options.loading !== false) {
    uni.showLoading({
      title: '加载中...',
      mask: true
    })
  }

  try {
    // 获取 token
    const token = uni.getStorageSync('token')
    
    return new Promise((resolve, reject) => {
      uni.request({
        url: BASE_URL + options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : '',
          ...options.header
        },
        success: (res: any) => {
          // HTTP 401 未授权
          if (res.statusCode === 401) {
            uni.removeStorageSync('token')
            uni.showToast({ title: '请重新登录', icon: 'none' })
            uni.reLaunch({ url: '/pages/login/index' })
            reject(res.data)
            return
          }
          
          if (res.statusCode === 200) {
            const data = res.data as ApiResponse<T>
            if (data.code === 200) {
              resolve(data)
            } else if (data.code === 401) {
              // 业务层 token 过期
              uni.removeStorageSync('token')
              uni.showToast({ title: '请重新登录', icon: 'none' })
              uni.reLaunch({ url: '/pages/login/index' })
              reject(data)
            } else {
              if (options.showError !== false) {
                uni.showToast({ title: data.message || '请求失败', icon: 'none' })
              }
              reject(data)
            }
          } else {
            uni.showToast({ title: '网络错误', icon: 'none' })
            reject(res)
          }
        },
        fail: (err) => {
          console.error('Request failed:', err)
          uni.showToast({ title: '网络异常', icon: 'none' })
          reject(err)
        },
        complete: () => {
          if (options.loading !== false) {
            uni.hideLoading()
          }
        }
      })
    })
  } catch (error) {
    if (options.loading !== false) uni.hideLoading()
    throw error
  }
}

// 上传文件
export const uploadFile = (filePath: string, name: string = 'file'): Promise<ApiResponse> => {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token')
    
    uni.uploadFile({
      url: BASE_URL + '/upload/image',
      filePath,
      name,
      header: {
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const data = JSON.parse(res.data)
          resolve(data)
        } else {
          reject(res)
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

export default {
  get<T = any>(url: string, data?: any, options?: Partial<RequestOptions>) {
    return request<T>({ url, method: 'GET', data, ...options })
  },
  post<T = any>(url: string, data?: any, options?: Partial<RequestOptions>) {
    return request<T>({ url, method: 'POST', data, ...options })
  },
  put<T = any>(url: string, data?: any, options?: Partial<RequestOptions>) {
    return request<T>({ url, method: 'PUT', data, ...options })
  },
  delete<T = any>(url: string, data?: any, options?: Partial<RequestOptions>) {
    return request<T>({ url, method: 'DELETE', data, ...options })
  }
}
