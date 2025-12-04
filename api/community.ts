/**
 * 社区相关接口
 */
import request from '@/utils/request'

/**
 * 获取动态列表
 */
export function getPosts(params?: {
  page?: number
  page_size?: number
  topic_id?: number
  user_id?: number
  type?: string
}) {
  return request.get('/community/posts', params)
}

/**
 * 发布动态
 */
export function createPost(data: {
  content: string
  images?: string[]
  video_url?: string
  topic_id?: number
  location?: string
}) {
  return request.post('/community/post', data)
}

/**
 * 删除动态
 */
export function deletePost(id: number) {
  return request.delete(`/community/post/${id}`)
}

/**
 * 获取动态详情
 */
export function getPostDetail(id: number) {
  return request.get(`/community/post/${id}`)
}

/**
 * 点赞动态
 */
export function likePost(id: number) {
  return request.post(`/community/post/${id}/like`)
}

/**
 * 取消点赞
 */
export function unlikePost(id: number) {
  return request.delete(`/community/post/${id}/like`)
}

/**
 * 评论动态
 */
export function commentPost(id: number, data: {
  content: string
  parent_id?: number
  reply_to_user_id?: number
}) {
  return request.post(`/community/post/${id}/comment`, data)
}

/**
 * 获取评论列表
 */
export function getPostComments(id: number, params?: { page?: number; page_size?: number }) {
  return request.get(`/community/post/${id}/comments`, params)
}

/**
 * 获取话题列表
 */
export function getTopics(params?: { page?: number; page_size?: number; is_hot?: number }) {
  return request.get('/community/topics', params)
}

/**
 * 获取话题详情
 */
export function getTopicDetail(id: number) {
  return request.get(`/community/topic/${id}`)
}

/**
 * 获取排行榜
 */
export function getRanking(params?: { type?: string; period?: string }) {
  return request.get('/community/ranking', params)
}

/**
 * 关注用户
 */
export function followUser(userId: number) {
  return request.post(`/community/follow/${userId}`)
}

/**
 * 取消关注
 */
export function unfollowUser(userId: number) {
  return request.delete(`/community/follow/${userId}`)
}

/**
 * 获取关注列表
 */
export function getFollowing(params?: { page?: number; page_size?: number }) {
  return request.get('/community/following', params)
}

/**
 * 获取粉丝列表
 */
export function getFollowers(params?: { page?: number; page_size?: number }) {
  return request.get('/community/followers', params)
}


















