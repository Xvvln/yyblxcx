<template>
  <div class="bg-white rounded-xl shadow-apple-card overflow-hidden">
    <!-- 顶部筛选 -->
    <div class="p-6 border-b border-apple-border flex justify-between items-center flex-wrap gap-4">
      <div class="flex space-x-4 flex-wrap gap-2">
        <el-input
          v-model="searchQuery"
          placeholder="搜索订单号..."
          prefix-icon="Search"
          class="w-64"
          clearable
          @change="handleSearch"
        />
        <el-select v-model="filterStatus" placeholder="订单状态" class="w-32" clearable @change="handleSearch">
          <el-option label="待付款" value="pending" />
          <el-option label="已付款" value="paid" />
          <el-option label="已发货" value="shipped" />
          <el-option label="已收货" value="received" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
          <el-option label="已退款" value="refunded" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          @change="handleSearch"
        />
      </div>
      <el-button @click="handleSearch">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>

    <!-- 订单表格 -->
    <el-table :data="orderList" style="width: 100%" class="apple-table" v-loading="loading">
      <el-table-column prop="order_no" label="订单号" min-width="180" />
      <el-table-column label="用户" min-width="120">
        <template #default="scope">
          <span>{{ scope.row.user?.nickname || '未知用户' }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="total_amount" label="订单金额" min-width="100">
        <template #default="scope">
          <span class="font-medium text-red-500">¥{{ scope.row.total_amount }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="pay_amount" label="实付金额" min-width="100">
        <template #default="scope">
          <span class="font-bold text-red-500">¥{{ scope.row.pay_amount }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" min-width="90">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)" size="small">
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="receiver_name" label="收货人" min-width="90" />
      <el-table-column prop="receiver_phone" label="联系电话" min-width="120" />
      <el-table-column prop="created_at" label="下单时间" min-width="160" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button link type="primary" size="small" @click="viewDetail(scope.row)">详情</el-button>
          <el-button 
            v-if="scope.row.status === 'paid'" 
            link 
            type="success" 
            size="small"
            @click="openShipDialog(scope.row)"
          >
            发货
          </el-button>
          <el-button 
            v-if="['paid', 'shipped'].includes(scope.row.status)" 
            link 
            type="danger" 
            size="small"
            @click="openRefundDialog(scope.row)"
          >
            退款
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
        @current-change="fetchOrders"
      />
    </div>
    
    <!-- 订单详情弹窗 -->
    <el-dialog v-model="detailVisible" title="订单详情" width="700px">
      <div v-if="currentOrder" class="space-y-4">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ currentOrder.order_no }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentOrder.status)">{{ getStatusText(currentOrder.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="用户">{{ currentOrder.user?.nickname }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.user?.phone || currentOrder.receiver_phone }}</el-descriptions-item>
          <el-descriptions-item label="收货人">{{ currentOrder.receiver_name }}</el-descriptions-item>
          <el-descriptions-item label="收货电话">{{ currentOrder.receiver_phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址" :span="2">{{ currentOrder.receiver_address }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">¥{{ currentOrder.total_amount }}</el-descriptions-item>
          <el-descriptions-item label="运费">¥{{ currentOrder.freight_amount || 0 }}</el-descriptions-item>
          <el-descriptions-item label="优惠金额">¥{{ currentOrder.discount_amount || 0 }}</el-descriptions-item>
          <el-descriptions-item label="实付金额">
            <span class="text-red-500 font-bold">¥{{ currentOrder.pay_amount }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ currentOrder.created_at }}</el-descriptions-item>
          <el-descriptions-item label="支付时间">{{ currentOrder.pay_time || '-' }}</el-descriptions-item>
          <el-descriptions-item label="发货时间">{{ currentOrder.ship_time || '-' }}</el-descriptions-item>
          <el-descriptions-item label="收货时间">{{ currentOrder.receive_time || '-' }}</el-descriptions-item>
          <el-descriptions-item v-if="currentOrder.tracking_company" label="快递公司">{{ currentOrder.tracking_company }}</el-descriptions-item>
          <el-descriptions-item v-if="currentOrder.tracking_no" label="快递单号">{{ currentOrder.tracking_no }}</el-descriptions-item>
          <el-descriptions-item v-if="currentOrder.remark" label="备注" :span="2">{{ currentOrder.remark }}</el-descriptions-item>
        </el-descriptions>
        
        <h4 class="font-medium">商品列表</h4>
        <el-table :data="currentOrder.items" border size="small">
          <el-table-column label="商品" min-width="200">
            <template #default="scope">
              <div class="flex items-center">
                <el-image 
                  v-if="scope.row.product_image" 
                  :src="scope.row.product_image" 
                  class="w-12 h-12 rounded mr-3"
                  fit="cover"
                />
                <div>
                  <p class="text-sm">{{ scope.row.product_name }}</p>
                  <p v-if="scope.row.spec_name" class="text-xs text-gray-500">{{ scope.row.spec_name }}</p>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="price" label="单价" width="100">
            <template #default="scope">¥{{ scope.row.price }}</template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="80" />
          <el-table-column label="小计" width="100">
            <template #default="scope">¥{{ (scope.row.price * scope.row.quantity).toFixed(2) }}</template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
    
    <!-- 发货弹窗 -->
    <el-dialog v-model="shipDialogVisible" title="订单发货" width="400px">
      <el-form :model="shipForm" label-position="top">
        <el-form-item label="快递公司" required>
          <el-select v-model="shipForm.tracking_company" placeholder="请选择快递公司" class="w-full">
            <el-option label="顺丰速运" value="顺丰速运" />
            <el-option label="中通快递" value="中通快递" />
            <el-option label="圆通快递" value="圆通快递" />
            <el-option label="韵达快递" value="韵达快递" />
            <el-option label="申通快递" value="申通快递" />
            <el-option label="京东物流" value="京东物流" />
            <el-option label="邮政EMS" value="邮政EMS" />
          </el-select>
        </el-form-item>
        <el-form-item label="快递单号" required>
          <el-input v-model="shipForm.tracking_no" placeholder="请输入快递单号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="shipDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleShip">确认发货</el-button>
      </template>
    </el-dialog>
    
    <!-- 退款弹窗 -->
    <el-dialog v-model="refundDialogVisible" title="订单退款" width="400px">
      <el-form :model="refundForm" label-position="top">
        <el-form-item label="退款金额">
          <el-input-number 
            v-model="refundForm.refund_amount" 
            :min="0" 
            :max="currentOrder?.pay_amount || 0"
            :precision="2"
            class="w-full"
          />
          <p class="text-xs text-gray-500 mt-1">不填则全额退款，最大可退：¥{{ currentOrder?.pay_amount }}</p>
        </el-form-item>
        <el-form-item label="退款原因">
          <el-input v-model="refundForm.reason" type="textarea" :rows="2" placeholder="请输入退款原因（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="refundDialogVisible = false">取消</el-button>
        <el-button type="danger" :loading="submitLoading" @click="handleRefund">确认退款</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { getOrderList, getOrderDetail, shipOrder, refundOrder } from '@/api/order'

const loading = ref(false)
const submitLoading = ref(false)
const searchQuery = ref('')
const filterStatus = ref('')
const dateRange = ref<[string, string] | null>(null)
const orderList = ref<any[]>([])
const detailVisible = ref(false)
const shipDialogVisible = ref(false)
const refundDialogVisible = ref(false)
const currentOrder = ref<any>(null)

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const shipForm = reactive({
  tracking_company: '',
  tracking_no: ''
})

const refundForm = reactive({
  refund_amount: undefined as number | undefined,
  reason: ''
})

// 状态映射
const statusMap: Record<string, { text: string; type: string }> = {
  pending: { text: '待付款', type: 'warning' },
  paid: { text: '已付款', type: 'primary' },
  shipped: { text: '已发货', type: 'info' },
  received: { text: '已收货', type: '' },
  completed: { text: '已完成', type: 'success' },
  cancelled: { text: '已取消', type: 'info' },
  refunded: { text: '已退款', type: 'danger' },
}

function getStatusText(status: string) {
  return statusMap[status]?.text || status
}

function getStatusType(status: string) {
  return statusMap[status]?.type || ''
}

// 获取订单列表
async function fetchOrders() {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      page_size: pagination.pageSize,
    }
    
    if (searchQuery.value) params.order_no = searchQuery.value
    if (filterStatus.value) params.status = filterStatus.value
    if (dateRange.value) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }
    
    const res = await getOrderList(params)
    if (res.code === 200) {
      orderList.value = res.data.list || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取订单列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  fetchOrders()
}

// 查看详情
async function viewDetail(order: any) {
  try {
    const res = await getOrderDetail(order.id)
    if (res.code === 200) {
      currentOrder.value = res.data
      detailVisible.value = true
    }
  } catch (error) {
    console.error('获取订单详情失败:', error)
  }
}

// 发货
function openShipDialog(order: any) {
  currentOrder.value = order
  shipForm.tracking_company = ''
  shipForm.tracking_no = ''
  shipDialogVisible.value = true
}

async function handleShip() {
  if (!shipForm.tracking_company || !shipForm.tracking_no) {
    ElMessage.warning('请填写快递信息')
    return
  }
  
  submitLoading.value = true
  try {
    await shipOrder(currentOrder.value.id, shipForm)
    ElMessage.success('发货成功')
    shipDialogVisible.value = false
    fetchOrders()
  } catch (error: any) {
    ElMessage.error(error.message || '发货失败')
  } finally {
    submitLoading.value = false
  }
}

// 退款
function openRefundDialog(order: any) {
  currentOrder.value = order
  refundForm.refund_amount = undefined
  refundForm.reason = ''
  refundDialogVisible.value = true
}

async function handleRefund() {
  try {
    await ElMessageBox.confirm('确定要对该订单进行退款吗？此操作不可撤销。', '确认退款', { type: 'warning' })
    
    submitLoading.value = true
    await refundOrder(currentOrder.value.id, {
      refund_amount: refundForm.refund_amount,
      reason: refundForm.reason
    })
    ElMessage.success('退款成功')
    refundDialogVisible.value = false
    fetchOrders()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '退款失败')
    }
  } finally {
    submitLoading.value = false
  }
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.apple-table :deep(.el-table__header) th {
  background-color: #f5f5f7;
  color: #86868b;
  font-weight: 500;
}
</style>

