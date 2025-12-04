<template>
  <div class="bg-white rounded-xl shadow-apple-card overflow-hidden">
    <!-- 顶部操作栏 -->
    <div class="p-6 border-b border-apple-border flex justify-between items-center flex-wrap gap-4">
      <div class="flex space-x-4 flex-wrap gap-2">
        <el-input
          v-model="searchQuery"
          placeholder="搜索反馈内容..."
          prefix-icon="Search"
          class="w-64"
          clearable
          @change="handleSearch"
        />
        <el-select v-model="filterStatus" placeholder="状态" class="w-32" @change="handleSearch">
          <el-option label="全部" :value="undefined" />
          <el-option label="待处理" :value="0" />
          <el-option label="已处理" :value="1" />
          <el-option label="已回复" :value="2" />
        </el-select>
      </div>
      <el-button @click="handleSearch">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <!-- 反馈列表 -->
    <el-table :data="feedbackList" style="width: 100%" class="apple-table" v-loading="loading">
      <el-table-column label="用户" min-width="180">
        <template #default="scope">
          <div class="flex items-center py-2">
            <el-avatar :size="36" :src="scope.row.user?.avatar || undefined">
              {{ scope.row.user?.nickname?.charAt(0) || '?' }}
            </el-avatar>
            <div class="ml-3">
              <p class="text-sm font-medium text-apple-dark">{{ scope.row.user?.nickname || '未知用户' }}</p>
              <p class="text-xs text-apple-text-gray">{{ scope.row.user?.phone || '-' }}</p>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="反馈内容" min-width="280">
        <template #default="scope">
          <div class="py-2">
            <p class="text-sm text-apple-dark line-clamp-2">{{ scope.row.content }}</p>
            <div v-if="scope.row.images?.length" class="flex mt-2 gap-1">
              <el-image 
                v-for="(img, idx) in scope.row.images.slice(0, 3)" 
                :key="idx"
                :src="img"
                :preview-src-list="scope.row.images"
                :initial-index="idx"
                fit="cover"
                class="w-12 h-12 rounded"
              />
              <span v-if="scope.row.images.length > 3" class="text-xs text-apple-text-gray self-center">+{{ scope.row.images.length - 3 }}</span>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="contact" label="联系方式" width="140">
        <template #default="scope">
          {{ scope.row.contact || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag 
            :type="getStatusTagType(scope.row.status)"
            size="small"
          >
            {{ getStatusName(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="提交时间" width="170" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button link type="primary" size="small" @click="viewDetail(scope.row)">详情</el-button>
          <el-button 
            link 
            type="success" 
            size="small"
            :disabled="scope.row.status === 2"
            @click="openReplyDialog(scope.row)"
          >
            回复
          </el-button>
          <el-button 
            link 
            type="danger" 
            size="small"
            @click="handleDelete(scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="p-6 flex justify-end border-t border-apple-border">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSearch"
        @current-change="fetchFeedbackList"
      />
    </div>
    
    <!-- 反馈详情弹窗 -->
    <el-dialog v-model="detailVisible" title="反馈详情" width="600px">
      <div v-if="currentFeedback" class="space-y-4">
        <div class="flex items-center">
          <el-avatar :size="48" :src="currentFeedback.user?.avatar || undefined">
            {{ currentFeedback.user?.nickname?.charAt(0) || '?' }}
          </el-avatar>
          <div class="ml-4">
            <h3 class="text-base font-medium">{{ currentFeedback.user?.nickname }}</h3>
            <p class="text-gray-500 text-sm">{{ currentFeedback.user?.phone || '-' }}</p>
          </div>
          <el-tag 
            :type="getStatusTagType(currentFeedback.status)"
            size="small"
            class="ml-auto"
          >
            {{ getStatusName(currentFeedback.status) }}
          </el-tag>
        </div>
        
        <el-descriptions :column="1" border>
          <el-descriptions-item label="反馈内容">
            <div class="whitespace-pre-wrap">{{ currentFeedback.content }}</div>
          </el-descriptions-item>
          <el-descriptions-item label="图片" v-if="currentFeedback.images?.length">
            <div class="flex gap-2 flex-wrap">
              <el-image 
                v-for="(img, idx) in currentFeedback.images" 
                :key="idx"
                :src="img"
                :preview-src-list="currentFeedback.images"
                :initial-index="idx"
                fit="cover"
                class="w-20 h-20 rounded"
              />
            </div>
          </el-descriptions-item>
          <el-descriptions-item label="联系方式">{{ currentFeedback.contact || '-' }}</el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ currentFeedback.created_at }}</el-descriptions-item>
          <el-descriptions-item label="回复内容" v-if="currentFeedback.reply">
            <div class="whitespace-pre-wrap text-blue-600">{{ currentFeedback.reply }}</div>
          </el-descriptions-item>
        </el-descriptions>
        
        <div class="flex justify-end gap-2" v-if="currentFeedback.status !== 2">
          <el-button v-if="currentFeedback.status === 0" @click="markAsProcessed(currentFeedback)">标记已处理</el-button>
          <el-button type="primary" @click="openReplyDialog(currentFeedback); detailVisible = false">回复</el-button>
        </div>
      </div>
    </el-dialog>
    
    <!-- 回复弹窗 -->
    <el-dialog v-model="replyVisible" title="回复反馈" width="500px">
      <el-form :model="replyForm" label-width="80px">
        <el-form-item label="反馈内容">
          <div class="text-sm text-gray-600 bg-gray-50 p-3 rounded">{{ currentFeedback?.content }}</div>
        </el-form-item>
        <el-form-item label="回复">
          <el-input 
            v-model="replyForm.reply" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入回复内容..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="replyVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitReply">提交回复</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { getFeedbackList, replyFeedback, updateFeedbackStatus, deleteFeedback } from '@/api/feedback'

const loading = ref(false)
const submitting = ref(false)
const searchQuery = ref('')
const filterStatus = ref<number | undefined>(undefined)
const feedbackList = ref<any[]>([])
const detailVisible = ref(false)
const replyVisible = ref(false)
const currentFeedback = ref<any>(null)

const replyForm = reactive({
  reply: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 状态映射
function getStatusName(status: number) {
  const map: Record<number, string> = {
    0: '待处理',
    1: '已处理',
    2: '已回复'
  }
  return map[status] || '未知'
}

function getStatusTagType(status: number) {
  if (status === 2) return 'success'
  if (status === 1) return 'info'
  return 'warning'
}

// 获取反馈列表
async function fetchFeedbackList() {
  loading.value = true
  try {
    const res = await getFeedbackList({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: searchQuery.value || undefined,
      status: filterStatus.value
    })
    
    if (res.code === 200) {
      feedbackList.value = res.data.list || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取反馈列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  fetchFeedbackList()
}

// 查看详情
function viewDetail(feedback: any) {
  currentFeedback.value = feedback
  detailVisible.value = true
}

// 打开回复弹窗
function openReplyDialog(feedback: any) {
  currentFeedback.value = feedback
  replyForm.reply = ''
  replyVisible.value = true
}

// 提交回复
async function submitReply() {
  if (!replyForm.reply.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }
  
  submitting.value = true
  try {
    const res = await replyFeedback(currentFeedback.value.id, { reply: replyForm.reply })
    if (res.code === 200) {
      ElMessage.success('回复成功')
      replyVisible.value = false
      fetchFeedbackList()
    }
  } catch (error: any) {
    ElMessage.error(error.message || '回复失败')
  } finally {
    submitting.value = false
  }
}

// 标记已处理
async function markAsProcessed(feedback: any) {
  try {
    const res = await updateFeedbackStatus(feedback.id, { status: 1 })
    if (res.code === 200) {
      ElMessage.success('已标记为已处理')
      feedback.status = 1
      detailVisible.value = false
      fetchFeedbackList()
    }
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

// 删除反馈
async function handleDelete(feedback: any) {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条反馈吗？此操作不可撤销。',
      '确认删除',
      { type: 'warning' }
    )
    
    const res = await deleteFeedback(feedback.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      fetchFeedbackList()
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

onMounted(() => {
  fetchFeedbackList()
})
</script>

<style scoped>
.apple-table :deep(.el-table__header) th {
  background-color: #f5f5f7;
  color: #86868b;
  font-weight: 500;
  border-bottom: 1px solid #d2d2d7;
}

.apple-table :deep(.el-table__row) td {
  border-bottom: 1px solid #f5f5f7;
}

.apple-table :deep(.el-table__row:hover) td {
  background-color: #fbfbfd;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

