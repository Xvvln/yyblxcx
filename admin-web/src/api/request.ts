/**
 * HTTP请求封装
 */
import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://localhost:8000/api/admin/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data
    
    // 处理标准响应格式
    if (res.code !== undefined) {
      if (res.code !== 200) {
        ElMessage.error(res.message || '请求失败')
        
        // 401 未授权，跳转登录
        if (res.code === 401) {
          localStorage.removeItem('admin_token')
          router.push('/login')
        }
        
        return Promise.reject(new Error(res.message || '请求失败'))
      }
      return res
    }
    
    return response.data
  },
  (error: AxiosError) => {
    console.error('响应错误:', error)
    
    if (error.response?.status === 401) {
      localStorage.removeItem('admin_token')
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    } else if (error.response?.status === 403) {
      ElMessage.error('没有权限访问')
    } else if (error.response?.status === 404) {
      ElMessage.error('资源不存在')
    } else if (error.response?.status === 500) {
      ElMessage.error('服务器错误')
    } else {
      ElMessage.error(error.message || '网络错误')
    }
    
    return Promise.reject(error)
  }
)

// 请求方法封装
const request = {
  get<T = any>(url: string, params?: any, config?: AxiosRequestConfig): Promise<T> {
    return service.get(url, { params, ...config })
  },
  
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return service.post(url, data, config)
  },
  
  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return service.put(url, data, config)
  },
  
  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return service.delete(url, config)
  },
}

export default request

