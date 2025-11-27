<template>
  <div class="space-y-6">
    <!-- 顶部统计 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-xl shadow-apple-card">
        <p class="text-sm text-apple-text-gray">在售商品</p>
        <p class="text-2xl font-bold text-apple-dark mt-1">{{ onSaleCount }}</p>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-apple-card">
        <p class="text-sm text-apple-text-gray">库存预警</p>
        <p class="text-2xl font-bold text-red-500 mt-1">{{ lowStockCount }}</p>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-apple-card">
        <p class="text-sm text-apple-text-gray">商品总数</p>
        <p class="text-2xl font-bold text-apple-blue mt-1">{{ pagination.total }}</p>
      </div>
    </div>

    <!-- 商品列表 -->
    <div class="bg-white rounded-xl shadow-apple-card overflow-hidden">
      <div class="p-6 border-b border-apple-border flex justify-between items-center flex-wrap gap-4">
        <div class="flex space-x-4 flex-wrap gap-2">
          <el-input
            v-model="searchQuery"
            placeholder="搜索商品名称..."
            prefix-icon="Search"
            class="w-64"
            clearable
            @change="handleSearch"
          />
          <el-select v-model="filterCategory" placeholder="全部分类" class="w-40" clearable @change="handleSearch">
            <el-option 
              v-for="cat in categories" 
              :key="cat.id" 
              :label="cat.name" 
              :value="cat.id" 
            />
          </el-select>
          <el-select v-model="filterOnSale" placeholder="上架状态" class="w-32" clearable @change="handleSearch">
            <el-option label="已上架" :value="1" />
            <el-option label="已下架" :value="0" />
          </el-select>
        </div>
        <el-button type="primary" class="bg-apple-blue border-none" @click="openDialog()">
          <el-icon class="mr-2"><Plus /></el-icon>发布商品
        </el-button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-6" v-loading="loading">
        <div v-for="product in productList" :key="product.id" class="group bg-white border border-apple-border rounded-xl overflow-hidden hover:shadow-apple-hover transition-all duration-300">
          <div class="relative h-48 bg-gray-100">
            <img 
              v-if="product.images?.[0]" 
              :src="product.images[0]" 
              class="object-cover w-full h-full" 
            />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
              暂无图片
            </div>
            <div class="absolute top-2 right-2 flex gap-1">
              <span v-if="product.stock < 10 && product.stock > 0" class="px-2 py-1 text-xs font-bold text-white bg-orange-500 rounded-full shadow-sm">
                库存不足
              </span>
              <span v-if="product.stock === 0" class="px-2 py-1 text-xs font-bold text-white bg-red-500 rounded-full shadow-sm">
                已售罄
              </span>
              <span v-if="product.is_recommend" class="px-2 py-1 text-xs font-bold text-white bg-blue-500 rounded-full shadow-sm">
                推荐
              </span>
            </div>
            <div v-if="!product.is_on_sale" class="absolute inset-0 bg-black/50 flex items-center justify-center">
              <span class="text-white font-bold">已下架</span>
            </div>
          </div>
          <div class="p-4">
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-sm font-semibold text-apple-dark line-clamp-2 flex-1">{{ product.name }}</h3>
            </div>
            <div class="flex items-baseline gap-2 mb-2">
              <span class="text-lg font-bold text-red-500">¥{{ product.current_price }}</span>
              <span v-if="product.original_price > product.current_price" class="text-xs text-gray-400 line-through">
                ¥{{ product.original_price }}
              </span>
            </div>
            <div class="flex justify-between items-center text-xs text-apple-text-gray mb-4">
              <span>销量 {{ product.sales_count }}</span>
              <span>库存 {{ product.stock }}</span>
            </div>
            <div class="flex space-x-2">
              <button 
                class="flex-1 px-3 py-1.5 text-xs font-medium text-apple-dark bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                @click="openDialog(product)"
              >
                编辑
              </button>
              <button 
                class="flex-1 px-3 py-1.5 text-xs font-medium rounded-lg transition-colors"
                :class="product.is_on_sale ? 'text-red-600 bg-red-50 hover:bg-red-100' : 'text-green-600 bg-green-50 hover:bg-green-100'"
                @click="toggleOnSale(product)"
              >
                {{ product.is_on_sale ? '下架' : '上架' }}
              </button>
            </div>
          </div>
        </div>
        
        <div v-if="productList.length === 0 && !loading" class="col-span-full text-center py-12 text-apple-text-gray">
          暂无商品
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="p-6 border-t border-apple-border flex justify-end">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[12, 24, 48]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSearch"
          @current-change="fetchProducts"
        />
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑商品' : '发布新商品'"
      width="600px"
    >
      <el-form :model="productForm" label-position="top" ref="formRef">
        <el-form-item label="商品名称" required>
          <el-input v-model="productForm.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="副标题">
          <el-input v-model="productForm.subtitle" placeholder="请输入副标题" />
        </el-form-item>
        <el-form-item label="商品分类" required>
          <el-select v-model="productForm.category_id" placeholder="请选择分类" class="w-full">
            <el-option 
              v-for="cat in categories" 
              :key="cat.id" 
              :label="cat.name" 
              :value="cat.id" 
            />
          </el-select>
        </el-form-item>
        <div class="grid grid-cols-3 gap-4">
          <el-form-item label="原价" required>
            <el-input-number v-model="productForm.original_price" :min="0" :precision="2" controls-position="right" class="w-full" />
          </el-form-item>
          <el-form-item label="现价" required>
            <el-input-number v-model="productForm.current_price" :min="0" :precision="2" controls-position="right" class="w-full" />
          </el-form-item>
          <el-form-item label="库存" required>
            <el-input-number v-model="productForm.stock" :min="0" controls-position="right" class="w-full" />
          </el-form-item>
        </div>
        <el-form-item label="商品描述">
          <el-input v-model="productForm.description" type="textarea" :rows="3" placeholder="请输入商品描述" />
        </el-form-item>
        <div class="grid grid-cols-2 gap-4">
          <el-form-item label="是否推荐">
            <el-switch v-model="productForm.is_recommend" :active-value="1" :inactive-value="0" />
          </el-form-item>
          <el-form-item label="是否上架">
            <el-switch v-model="productForm.is_on_sale" :active-value="1" :inactive-value="0" />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" class="bg-apple-blue border-none" :loading="submitLoading" @click="handleSubmit">
          {{ isEdit ? '保存' : '发布' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getProductList, createProduct, updateProduct, getCategoryList } from '@/api/product'

const loading = ref(false)
const submitLoading = ref(false)
const searchQuery = ref('')
const filterCategory = ref<number | undefined>(undefined)
const filterOnSale = ref<number | undefined>(undefined)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref<number | null>(null)

const productList = ref<any[]>([])
const categories = ref<any[]>([])

const pagination = reactive({
  page: 1,
  pageSize: 12,
  total: 0
})

const productForm = reactive({
  name: '',
  subtitle: '',
  category_id: undefined as number | undefined,
  original_price: 0,
  current_price: 0,
  stock: 0,
  description: '',
  is_recommend: 0,
  is_on_sale: 1,
})

// 统计
const onSaleCount = computed(() => productList.value.filter(p => p.is_on_sale).length)
const lowStockCount = computed(() => productList.value.filter(p => p.stock < 10 && p.stock > 0).length)

// 获取分类
async function fetchCategories() {
  try {
    const res = await getCategoryList()
    if (res.code === 200) {
      // 扁平化分类树
      const flatCategories: any[] = []
      const flatten = (items: any[]) => {
        items.forEach(item => {
          flatCategories.push(item)
          if (item.children?.length) {
            flatten(item.children)
          }
        })
      }
      flatten(res.data || [])
      categories.value = flatCategories
    }
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

// 获取商品列表
async function fetchProducts() {
  loading.value = true
  try {
    const res = await getProductList({
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: searchQuery.value || undefined,
      category_id: filterCategory.value,
      is_on_sale: filterOnSale.value,
    })
    
    if (res.code === 200) {
      productList.value = res.data.list || []
      pagination.total = res.data.total || 0
    }
  } catch (error) {
    console.error('获取商品列表失败:', error)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.page = 1
  fetchProducts()
}

// 打开弹窗
function openDialog(product?: any) {
  if (product) {
    isEdit.value = true
    editId.value = product.id
    Object.assign(productForm, {
      name: product.name,
      subtitle: product.subtitle || '',
      category_id: product.category_id,
      original_price: product.original_price,
      current_price: product.current_price,
      stock: product.stock,
      description: product.description || '',
      is_recommend: product.is_recommend,
      is_on_sale: product.is_on_sale,
    })
  } else {
    isEdit.value = false
    editId.value = null
    Object.assign(productForm, {
      name: '',
      subtitle: '',
      category_id: undefined,
      original_price: 0,
      current_price: 0,
      stock: 0,
      description: '',
      is_recommend: 0,
      is_on_sale: 1,
    })
  }
  dialogVisible.value = true
}

// 提交
async function handleSubmit() {
  if (!productForm.name || !productForm.category_id) {
    ElMessage.warning('请填写必填项')
    return
  }
  
  submitLoading.value = true
  try {
    if (isEdit.value && editId.value) {
      await updateProduct(editId.value, productForm)
      ElMessage.success('更新成功')
    } else {
      await createProduct(productForm as any)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchProducts()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

// 上下架
async function toggleOnSale(product: any) {
  const newStatus = product.is_on_sale ? 0 : 1
  const action = newStatus ? '上架' : '下架'
  
  try {
    await ElMessageBox.confirm(`确定要${action}商品 "${product.name}" 吗？`, '确认操作', { type: 'warning' })
    await updateProduct(product.id, { is_on_sale: newStatus })
    ElMessage.success(`${action}成功`)
    product.is_on_sale = newStatus
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '操作失败')
    }
  }
}

onMounted(() => {
  fetchCategories()
  fetchProducts()
})
</script>
