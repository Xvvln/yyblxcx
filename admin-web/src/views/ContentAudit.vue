<template>
  <div class="space-y-6">
    <!-- Tab切换 -->
    <div class="flex space-x-4 mb-6">
      <button 
        v-for="tab in tabs" 
        :key="tab.value"
        class="px-4 py-2 text-sm font-medium rounded-full transition-all duration-200"
        :class="currentTab === tab.value ? 'bg-apple-dark text-white shadow-md' : 'bg-white text-apple-text-gray hover:bg-gray-50'"
        @click="switchTab(tab.value)"
      >
        {{ tab.label }}
        <span v-if="tab.count !== undefined" class="ml-1">
          ({{ tab.count }})
        </span>
      </button>
    </div>

    <!-- 内容类型切换 -->
    <div class="flex space-x-2 mb-4">
      <el-radio-group v-model="contentType" @change="handleSearch">
        <el-radio-button value="posts">动态</el-radio-button>
        <el-radio-button value="comments">评论</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 列表 -->
    <div class="grid grid-cols-1 gap-6" v-loading="loading">
      <div v-for="item in auditList" :key="item.id" class="bg-white rounded-xl p-6 shadow-apple-card flex gap-6">
        <!-- 左侧：用户信息与内容 -->
        <div class="flex-1">
          <div class="flex items-center mb-4">
            <el-avatar :size="32" :src="item.user?.avatar || undefined">
              {{ item.user?.nickname?.charAt(0) || '?' }}
            </el-avatar>
            <div class="ml-3">
              <p class="text-sm font-medium text-apple-dark">{{ item.user?.nickname || '未知用户' }}</p>
              <p class="text-xs text-apple-text-gray">{{ item.created_at }}</p>
            </div>
          </div>
          
          <div class="bg-apple-gray/50 rounded-lg p-4 mb-4">
            <p class="text-sm text-apple-dark leading-relaxed">{{ item.content }}</p>
            <div v-if="item.images && item.images.length" class="grid grid-cols-3 gap-2 mt-3">
              <el-image 
                v-for="(img, idx) in item.images" 
                :key="idx" 
                :src="img"
                :preview-src-list="item.images"
                fit="cover"
                class="w-full h-24 rounded-lg cursor-zoom-in"
              />
            </div>
          </div>

          <div class="flex items-center space-x-4 text-xs text-apple-text-gray">
            <span v-if="contentType === 'posts'" class="flex items-center">
              <el-icon class="mr-1"><View /></el-icon>
              {{ item.view_count }} 浏览
            </span>
            <span class="flex items-center">
              <el-icon class="mr-1"><Star /></el-icon>
              {{ item.like_count }} 点赞
            </span>
            <span v-if="contentType === 'posts'" class="flex items-center">
              <el-icon class="mr-1"><ChatDotRound /></el-icon>
              {{ item.comment_count }} 评论
            </span>
          </div>
        </div>

        <!-- 右侧：操作区 -->
        <div class="w-48 flex flex-col justify-center border-l border-apple-border pl-6 space-y-3">
          <button 
            v-if="item.status === 0"
            class="w-full py-2 text-sm font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 transition-colors shadow-sm"
            @click="handleAudit(item, 1)"
          >
            通过
          </button>
          <button 
            v-if="item.status === 0"
            class="w-full py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 transition-colors shadow-sm"
            @click="handleReject(item)"
          >
            拒绝
          </button>
          <div v-if="item.status === 1" class="text-center text-green-500 font-medium">
            ✓ 已通过
          </div>
          <div v-if="item.status === 2" class="text-center text-red-500 font-medium">
            ✗ 已拒绝
          </div>
        </div>
      </div>
      
      <div v-if="auditList.length === 0" class="bg-white rounded-xl p-12 shadow-apple-card text-center text-apple-text-gray">
        暂无{{ tabs.find(t => t.value === currentTab)?.label }}内容
      </div>
    </div>
    
    <!-- 分页 -->
    <div class="flex justify-center" v-if="pagination.total > 0">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        layout="prev, pager, next"
        @current-change="handleSearch"
      />
    </div>
    
    <!-- 拒绝原因弹窗 -->
    <el-dialog v-model="rejectDialogVisible" title="拒绝原因" width="400px">
      <el-input
        v-model="rejectReason"
        type="textarea"
        :rows="3"
        placeholder="请输入拒绝原因（可选）"
      />
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmReject">确认拒绝</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { View, Star, ChatDotRound } from '@element-plus/icons-vue'
import { getPendingPosts, auditPost, getPendingComments, auditComment } from '@/api/audit'

const loading = ref(false)
const contentType = ref<'posts' | 'comments'>('posts')
const currentTab = ref(0) // 0: 待审核, 1: 已通过, 2: 已拒绝
const auditList = ref<any[]>([])
const rejectDialogVisible = ref(false)
const rejectReason = ref('')
const currentItem = ref<any>(null)

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const tabs = computed(() => [
  { label: '待审核', value: 0 },
  { label: '已通过', value: 1 },
  { label: '已拒绝', value: 2 },
])

// 获取列表
async function fetchList() {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      status: currentTab.value
    }
    
    const res = contentType.value === 'posts' 
      ? await getPendingPosts(params)
      : await getPendingComments(params)
    
    if (res.code === 200) {
      auditList.value = res.data.list || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取列表失败:', error)
  } finally {
    loading.value = false
  }
}

function switchTab(tab: number) {
  currentTab.value = tab
  pagination.page = 1
  fetchList()
}

function handleSearch() {
  pagination.page = 1
  fetchList()
}

// 审核通过
async function handleAudit(item: any, status: number) {
  try {
    const res = contentType.value === 'posts'
      ? await auditPost(item.id, { status })
      : await auditComment(item.id, { status })
    
    if (res.code === 200) {
      ElMessage.success('审核成功')
      item.status = status
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

// 拒绝
function handleReject(item: any) {
  currentItem.value = item
  rejectReason.value = ''
  rejectDialogVisible.value = true
}

async function confirmReject() {
  if (!currentItem.value) return
  
  try {
    const res = contentType.value === 'posts'
      ? await auditPost(currentItem.value.id, { status: 2, reason: rejectReason.value })
      : await auditComment(currentItem.value.id, { status: 2, reason: rejectReason.value })
    
    if (res.code === 200) {
      ElMessage.success('已拒绝')
      currentItem.value.status = 2
      rejectDialogVisible.value = false
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

onMounted(() => {
  fetchList()
})
</script>
