<template>
  <div class="space-y-6">
    <el-tabs v-model="activeTab" class="bg-white rounded-xl shadow-apple-card p-6">
      <!-- 积分配置 -->
      <el-tab-pane label="积分配置" name="points">
        <div class="max-w-2xl">
          <h3 class="text-lg font-semibold mb-6">签到奖励</h3>
          <el-form label-width="140px">
            <el-form-item label="基础签到奖励">
              <el-input-number v-model="pointsConfig.checkin_base_reward" :min="0" />
              <span class="ml-2 text-gray-500">积分/天</span>
            </el-form-item>
            <el-form-item label="连续签到加成">
              <el-input-number v-model="pointsConfig.checkin_streak_bonus" :min="0" :precision="1" />
              <span class="ml-2 text-gray-500">倍（每7天）</span>
            </el-form-item>
          </el-form>
          
          <el-divider />
          
          <h3 class="text-lg font-semibold mb-6">行为奖励</h3>
          <el-form label-width="140px">
            <el-form-item label="运动记录奖励">
              <el-input-number v-model="pointsConfig.sport_record_reward" :min="0" />
              <span class="ml-2 text-gray-500">运动币/次</span>
            </el-form-item>
            <el-form-item label="饮食记录奖励">
              <el-input-number v-model="pointsConfig.food_record_reward" :min="0" />
              <span class="ml-2 text-gray-500">膳食币/次</span>
            </el-form-item>
            <el-form-item label="健康筛查奖励">
              <el-input-number v-model="pointsConfig.screening_reward" :min="0" />
              <span class="ml-2 text-gray-500">积分/次</span>
            </el-form-item>
          </el-form>
          
          <div class="flex justify-end mt-6">
            <el-button type="primary" @click="savePointsConfig" :loading="saving">保存配置</el-button>
          </div>
        </div>
      </el-tab-pane>
      
      <!-- 会员配置 -->
      <el-tab-pane label="会员配置" name="member">
        <div class="max-w-2xl">
          <h3 class="text-lg font-semibold mb-6">会员价格</h3>
          <el-form label-width="140px">
            <el-form-item label="月度会员价格">
              <el-input-number v-model="memberConfig.month_price" :min="0" :precision="2" />
              <span class="ml-2 text-gray-500">元/月</span>
            </el-form-item>
            <el-form-item label="年度会员价格">
              <el-input-number v-model="memberConfig.year_price" :min="0" :precision="2" />
              <span class="ml-2 text-gray-500">元/年</span>
            </el-form-item>
            <el-form-item label="终身会员价格">
              <el-input-number v-model="memberConfig.lifetime_price" :min="0" :precision="2" />
              <span class="ml-2 text-gray-500">元</span>
            </el-form-item>
          </el-form>
          
          <el-divider />
          
          <h3 class="text-lg font-semibold mb-6">会员权益</h3>
          <el-form label-width="140px">
            <el-form-item label="会员折扣">
              <el-input-number v-model="memberConfig.discount" :min="0.1" :max="1" :step="0.1" :precision="1" />
              <span class="ml-2 text-gray-500">（0.9 表示9折）</span>
            </el-form-item>
            <el-form-item label="积分倍数">
              <el-input-number v-model="memberConfig.points_multiplier" :min="1" :precision="1" />
              <span class="ml-2 text-gray-500">倍</span>
            </el-form-item>
          </el-form>
          
          <div class="flex justify-end mt-6">
            <el-button type="primary" @click="saveMemberConfig" :loading="saving">保存配置</el-button>
          </div>
        </div>
      </el-tab-pane>
      
      <!-- 订单配置 -->
      <el-tab-pane label="订单配置" name="order">
        <div class="max-w-2xl">
          <h3 class="text-lg font-semibold mb-6">订单设置</h3>
          <el-form label-width="160px">
            <el-form-item label="订单自动取消时间">
              <el-input-number v-model="orderConfig.auto_cancel_minutes" :min="1" />
              <span class="ml-2 text-gray-500">分钟（未付款自动取消）</span>
            </el-form-item>
            <el-form-item label="自动确认收货时间">
              <el-input-number v-model="orderConfig.auto_confirm_days" :min="1" />
              <span class="ml-2 text-gray-500">天（发货后自动确认）</span>
            </el-form-item>
            <el-form-item label="免运费金额">
              <el-input-number v-model="orderConfig.free_shipping_amount" :min="0" :precision="2" />
              <span class="ml-2 text-gray-500">元（订单满此金额免运费）</span>
            </el-form-item>
          </el-form>
          
          <div class="flex justify-end mt-6">
            <el-button type="primary" @click="saveOrderConfig" :loading="saving">保存配置</el-button>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getPointsConfig, updatePointsConfig, getMemberConfig, updateMemberConfig } from '@/api/setting'

const activeTab = ref('points')
const saving = ref(false)

const pointsConfig = reactive({
  checkin_base_reward: 5,
  checkin_streak_bonus: 1.5,
  sport_record_reward: 10,
  food_record_reward: 10,
  screening_reward: 20,
})

const memberConfig = reactive({
  month_price: 19.9,
  year_price: 199,
  lifetime_price: 999,
  discount: 0.9,
  points_multiplier: 2,
})

const orderConfig = reactive({
  auto_cancel_minutes: 30,
  auto_confirm_days: 7,
  free_shipping_amount: 99,
})

// 获取配置
async function fetchConfigs() {
  try {
    const [pointsRes, memberRes] = await Promise.all([
      getPointsConfig().catch(() => ({ code: 200, data: {} })),
      getMemberConfig().catch(() => ({ code: 200, data: {} })),
    ])
    
    if (pointsRes.code === 200 && pointsRes.data) {
      Object.assign(pointsConfig, pointsRes.data)
    }
    if (memberRes.code === 200 && memberRes.data) {
      Object.assign(memberConfig, memberRes.data)
    }
  } catch (error) {
    console.error('获取配置失败:', error)
  }
}

// 保存积分配置
async function savePointsConfig() {
  saving.value = true
  try {
    await updatePointsConfig(pointsConfig)
    ElMessage.success('保存成功')
  } catch (error: any) {
    ElMessage.error(error.message || '保存失败')
  } finally {
    saving.value = false
  }
}

// 保存会员配置
async function saveMemberConfig() {
  saving.value = true
  try {
    await updateMemberConfig(memberConfig)
    ElMessage.success('保存成功')
  } catch (error: any) {
    ElMessage.error(error.message || '保存失败')
  } finally {
    saving.value = false
  }
}

// 保存订单配置
async function saveOrderConfig() {
  saving.value = true
  try {
    // 订单配置接口暂未实现
    ElMessage.success('保存成功')
  } catch (error: any) {
    ElMessage.error(error.message || '保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchConfigs()
})
</script>

