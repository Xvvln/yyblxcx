import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'
import Dashboard from '@/views/Dashboard.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '仪表盘' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/UserList.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'content',
        name: 'Content',
        component: () => import('@/views/ContentAudit.vue'),
        meta: { title: '内容审核' }
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('@/views/ProductList.vue'),
        meta: { title: '商品管理' }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: () => import('@/views/OrderList.vue'),
        meta: { title: '订单管理' }
      },
      {
        path: 'feedback',
        name: 'Feedback',
        component: () => import('@/views/FeedbackList.vue'),
        meta: { title: '反馈管理' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue'),
        meta: { title: '系统设置' }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || '管理后台'} - 健康管理平台`
  
  const token = localStorage.getItem('admin_token')
  
  if (to.meta.requiresAuth && !token) {
    // 需要登录但未登录
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && token) {
    // 已登录访问登录页，跳转首页
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
