<template>
  <div class="min-h-screen bg-apple-gray flex items-center justify-center px-4">
    <div class="bg-white w-full max-w-md rounded-2xl shadow-apple-hover p-8 md:p-10">
      <div class="text-center mb-8">
        <div class="w-12 h-12 bg-apple-blue rounded-xl flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4 shadow-lg shadow-blue-200">
          H
        </div>
        <h1 class="text-2xl font-bold text-apple-dark">管理员登录</h1>
        <p class="text-sm text-apple-text-gray mt-2">欢迎回到健康管理平台</p>
      </div>

      <el-form ref="loginFormRef" :model="form" :rules="rules" class="space-y-5">
        <el-form-item prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="用户名" 
            size="large"
            class="h-12"
          >
            <template #prefix>
              <el-icon class="text-gray-400"><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="密码" 
            size="large"
            show-password
            class="h-12"
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <el-icon class="text-gray-400"><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        
        <el-button 
          type="primary" 
          size="large" 
          class="w-full h-12 bg-apple-blue hover:bg-blue-600 border-none text-lg font-medium rounded-lg shadow-md shadow-blue-100 transition-all duration-200 transform active:scale-95"
          :loading="loading"
          @click="handleLogin"
        >
          登 录
        </el-button>
      </el-form>

      <div class="mt-6 text-center text-sm text-apple-text-gray">
        <p>测试账号: admin / admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { useAdminStore } from '@/store/admin'

const router = useRouter()
const route = useRoute()
const adminStore = useAdminStore()

const loginFormRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: 'admin',
  password: 'admin123'
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      await adminStore.login(form.username, form.password)
      ElMessage.success('登录成功')
      
      // 跳转到之前页面或首页
      const redirect = route.query.redirect as string
      router.push(redirect || '/')
    } catch (error: any) {
      ElMessage.error(error.message || '登录失败')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
/* Element Plus 样式覆盖 */
:deep(.el-input__wrapper) {
  background-color: #f5f5f7;
  box-shadow: none !important;
  border-radius: 8px;
  transition: all 0.2s;
}

:deep(.el-input__wrapper:hover),
:deep(.el-input__wrapper.is-focus) {
  background-color: #fff;
  box-shadow: 0 0 0 2px #0071e3 !important;
}
</style>
