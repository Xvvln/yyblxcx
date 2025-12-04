<template>
  <div class="layout-container flex h-screen w-full bg-apple-gray">
    <!-- 侧边栏 -->
    <aside class="sidebar w-64 bg-white border-r border-apple-border flex flex-col transition-all duration-300">
      <!-- Logo -->
      <div class="h-16 flex items-center px-6 border-b border-apple-border">
        <div class="w-8 h-8 bg-apple-blue rounded-lg mr-3 flex items-center justify-center text-white font-bold">
          H
        </div>
        <span class="text-lg font-semibold text-apple-dark">健康管理平台</span>
      </div>

      <!-- 导航菜单 -->
      <div class="flex-1 overflow-y-auto py-4">
        <nav class="space-y-1 px-3">
          <template v-for="item in menuItems" :key="item.path">
            <router-link
              :to="item.path"
              class="flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
              :class="[
                route.path.startsWith(item.path) 
                  ? 'bg-apple-blue text-white shadow-sm' 
                  : 'text-apple-dark hover:bg-apple-gray'
              ]"
            >
              <el-icon class="w-5 h-5 mr-3"><component :is="item.icon" /></el-icon>
              {{ item.title }}
            </router-link>
          </template>
        </nav>
      </div>

      <!-- 底部用户区 -->
      <div class="p-4 border-t border-apple-border">
        <el-dropdown trigger="click" class="w-full">
          <div class="flex items-center p-2 rounded-lg hover:bg-apple-gray cursor-pointer transition-colors w-full">
            <el-avatar :size="32" :src="adminStore.adminInfo?.avatar || undefined">
              {{ adminStore.nickname?.charAt(0) || 'A' }}
            </el-avatar>
            <div class="ml-3 flex-1">
              <p class="text-sm font-medium text-apple-dark">{{ adminStore.nickname }}</p>
              <p class="text-xs text-apple-text-gray">{{ adminStore.adminInfo?.role || '管理员' }}</p>
            </div>
            <el-icon class="text-gray-400"><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handleLogout">
                <el-icon class="mr-2"><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <!-- 顶部栏 -->
      <header class="h-16 bg-white/80 backdrop-blur-md border-b border-apple-border flex items-center justify-between px-6 sticky top-0 z-10">
        <div class="flex items-center">
          <h1 class="text-xl font-semibold text-apple-dark">{{ currentRouteTitle }}</h1>
        </div>
        <div class="flex items-center space-x-4">
          <el-button text @click="handleRefresh">
            <el-icon><Refresh /></el-icon>
          </el-button>
          <div class="relative">
            <el-icon class="text-apple-text-gray text-xl cursor-pointer hover:text-apple-dark transition-colors"><Bell /></el-icon>
            <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
          </div>
        </div>
      </header>

      <!-- 页面内容 -->
      <div class="flex-1 overflow-auto p-6">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import {
  Odometer,
  User,
  Document,
  Goods,
  List,
  Setting,
  Bell,
  ArrowDown,
  SwitchButton,
  Refresh,
  ChatDotRound
} from '@element-plus/icons-vue'
import { useAdminStore } from '@/store/admin'

const route = useRoute()
const router = useRouter()
const adminStore = useAdminStore()

const menuItems = [
  { title: '仪表盘', path: '/dashboard', icon: Odometer },
  { title: '用户管理', path: '/users', icon: User },
  { title: '内容审核', path: '/content', icon: Document },
  { title: '商品管理', path: '/products', icon: Goods },
  { title: '订单管理', path: '/orders', icon: List },
  { title: '反馈管理', path: '/feedback', icon: ChatDotRound },
  { title: '系统设置', path: '/settings', icon: Setting },
]

const currentRouteTitle = computed(() => {
  return route.meta.title || 'Dashboard'
})

function handleRefresh() {
  router.go(0)
}

async function handleLogout() {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', { type: 'warning' })
    await adminStore.logout()
  } catch (error) {
    // 取消
  }
}

onMounted(() => {
  // 获取管理员信息
  if (adminStore.isLoggedIn && !adminStore.adminInfo) {
    adminStore.fetchAdminInfo()
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
