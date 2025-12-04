/**
 * 首页相关接口
 */
import request from '@/utils/request'

/**
 * 获取轮播图
 */
export function getBanners(position: string = 'home') {
  return request.get('/banner/list', { position })
}

/**
 * 获取个人数据概览
 */
export function getOverview() {
  return request.get('/stats/overview')
}


















