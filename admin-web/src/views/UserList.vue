<template>
  <div class="bg-white rounded-xl shadow-apple-card overflow-hidden">
    <!-- 顶部操作栏 -->
    <div class="p-6 border-b border-apple-border flex justify-between items-center flex-wrap gap-4">
      <div class="flex space-x-4 flex-wrap gap-2">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户..."
          prefix-icon="Search"
          class="w-64"
          clearable
          @change="handleSearch"
        />
        <el-select v-model="filterStatus" placeholder="状态" class="w-32" @change="handleSearch">
          <el-option label="全部" :value="undefined" />
          <el-option label="正常" :value="1" />
          <el-option label="禁用" :value="0" />
        </el-select>
        <el-select v-model="filterMemberType" placeholder="会员类型" class="w-32" @change="handleSearch">
          <el-option label="全部" value="" />
          <el-option label="普通用户" value="none" />
          <el-option label="月度会员" value="month" />
          <el-option label="年度会员" value="year" />
          <el-option label="终身会员" value="lifetime" />
        </el-select>
      </div>
      <el-button @click="handleSearch">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <!-- 用户表格 -->
    <el-table :data="userList" style="width: 100%" class="apple-table" v-loading="loading">
      <el-table-column label="用户" min-width="220">
        <template #default="scope">
          <div class="flex items-center py-2">
            <el-avatar :size="40" :src="scope.row.avatar || undefined">
              {{ scope.row.nickname?.charAt(0) || '?' }}
            </el-avatar>
            <div class="ml-3">
              <p class="text-sm font-medium text-apple-dark">{{ scope.row.nickname || '未设置昵称' }}</p>
              <p class="text-xs text-apple-text-gray">ID: {{ scope.row.id }}</p>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="phone" label="手机号" width="130">
        <template #default="scope">
          {{ scope.row.phone || '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="member_type" label="会员类型" width="120">
        <template #default="scope">
          <el-tag 
            :type="getMemberTagType(scope.row.member_type)"
            size="small"
          >
            {{ getMemberTypeName(scope.row.member_type) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="积分" width="140">
        <template #default="scope">
          <div class="text-xs">
            <span class="text-blue-500">运动币: {{ scope.row.sport_coins }}</span><br>
            <span class="text-green-500">膳食币: {{ scope.row.food_coins }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间" width="170" />
      <el-table-column prop="status" label="状态" width="90">
        <template #default="scope">
          <span class="flex items-center text-sm">
            <span :class="`w-2 h-2 rounded-full mr-2 ${scope.row.status === 1 ? 'bg-green-500' : 'bg-red-500'}`"></span>
            {{ scope.row.status === 1 ? '正常' : '禁用' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button link type="primary" size="small" @click="viewDetail(scope.row)">详情</el-button>
          <el-button 
            link 
            :type="scope.row.status === 1 ? 'danger' : 'success'" 
            size="small"
            @click="toggleUserStatus(scope.row)"
          >
            {{ scope.row.status === 1 ? '禁用' : '启用' }}
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
        @current-change="handleSearch"
      />
    </div>
    
    <!-- 用户详情弹窗 -->
    <el-dialog v-model="detailVisible" title="用户详情" width="600px">
      <div v-if="currentUser" class="space-y-4">
        <div class="flex items-center">
          <el-avatar :size="64" :src="currentUser.avatar || undefined">
            {{ currentUser.nickname?.charAt(0) || '?' }}
          </el-avatar>
          <div class="ml-4">
            <h3 class="text-lg font-medium">{{ currentUser.nickname }}</h3>
            <p class="text-gray-500">ID: {{ currentUser.id }}</p>
          </div>
        </div>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="手机号">{{ currentUser.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ currentUser.gender === 1 ? '男' : currentUser.gender === 2 ? '女' : '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="会员类型">{{ getMemberTypeName(currentUser.member_type) }}</el-descriptions-item>
          <el-descriptions-item label="会员到期">{{ currentUser.member_expire_time || '-' }}</el-descriptions-item>
          <el-descriptions-item label="运动币">{{ currentUser.sport_coins }}</el-descriptions-item>
          <el-descriptions-item label="膳食币">{{ currentUser.food_coins }}</el-descriptions-item>
          <el-descriptions-item label="签到天数">{{ currentUser.total_checkin_days }}</el-descriptions-item>
          <el-descriptions-item label="连续签到">{{ currentUser.continuous_checkin_days }}天</el-descriptions-item>
          <el-descriptions-item label="粉丝数">{{ currentUser.follower_count }}</el-descriptions-item>
          <el-descriptions-item label="关注数">{{ currentUser.following_count }}</el-descriptions-item>
          <el-descriptions-item label="注册时间" :span="2">{{ currentUser.created_at }}</el-descriptions-item>
        </el-descriptions>
        
        <div v-if="currentUser.health_profile">
          <h4 class="font-medium mb-2">健康档案</h4>
          <el-descriptions :column="2" border size="small">
            <el-descriptions-item label="生日">{{ currentUser.health_profile.birthday || '-' }}</el-descriptions-item>
            <el-descriptions-item label="血型">{{ currentUser.health_profile.blood_type || '-' }}</el-descriptions-item>
            <el-descriptions-item label="身高">{{ currentUser.health_profile.height ? currentUser.health_profile.height + 'cm' : '-' }}</el-descriptions-item>
            <el-descriptions-item label="体重">{{ currentUser.health_profile.weight ? currentUser.health_profile.weight + 'kg' : '-' }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { getUserList, getUserDetail, updateUserStatus } from '@/api/user'

const loading = ref(false)
const searchQuery = ref('')
const filterStatus = ref<number | undefined>(undefined)
const filterMemberType = ref('')
const userList = ref<any[]>([])
const detailVisible = ref(false)
const currentUser = ref<any>(null)

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

// 会员类型映射
const memberTypeMap: Record<string, string> = {
  none: '普通用户',
  month: '月度会员',
  year: '年度会员',
  lifetime: '终身会员'
}

function getMemberTypeName(type: string) {
  return memberTypeMap[type] || '普通用户'
}

function getMemberTagType(type: string) {
  if (type === 'lifetime') return 'danger'
  if (type === 'year') return 'warning'
  if (type === 'month') return 'success'
  return 'info'
}

// 获取用户列表
async function fetchUsers() {
  loading.value = true
  try {
    const res = await getUserList({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: searchQuery.value || undefined,
      status: filterStatus.value,
      member_type: filterMemberType.value || undefined
    })
    
    if (res.code === 200) {
      userList.value = res.data.list || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  fetchUsers()
}

// 查看详情
async function viewDetail(user: any) {
  try {
    const res = await getUserDetail(user.id)
    if (res.code === 200) {
      currentUser.value = res.data
      detailVisible.value = true
    }
  } catch (error) {
    console.error('获取用户详情失败:', error)
  }
}

// 切换用户状态
async function toggleUserStatus(user: any) {
  const newStatus = user.status === 1 ? 0 : 1
  const action = newStatus === 1 ? '启用' : '禁用'
  
  try {
    await ElMessageBox.confirm(
      `确定要${action}用户 "${user.nickname}" 吗？`,
      '确认操作',
      { type: 'warning' }
    )
    
    const res = await updateUserStatus(user.id, { status: newStatus })
    if (res.code === 200) {
      ElMessage.success(`${action}成功`)
      user.status = newStatus
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || `${action}失败`)
    }
  }
}

onMounted(() => {
  fetchUsers()
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
</style>
